#!/usr/bin/env python3
"""Every number the gates read, computed from the raw data. Owned by the verifier owner, frozen.

Reads: the frozen question files, the answers' event streams (ndjson) and Antigravity transcripts
(conversation databases), the DSH rule logs, every judge's per-verdict file with its raw reply,
label files with raw replies, the ledger, git (freeze and CONFIRM commits) and GRAV_LINK's notes.

Never reads as a measurement: the runners' ok flags (rule_ok, isolation_ok, the .json records),
report.json, verdicts.jsonl, parse_stats.json, a "split" or "lang" field copied into a job, a
parsed field a builder wrote beside a raw reply, or any measured.json. The drafting labels
(trait, mode) only name cells. A metric that cannot be computed is left out (None), never filled.

Usage: measure_all.py [--out FILE] [--boot 1000]
       measure_all.py --self-test
verify.py imports compute() and runs it itself.
"""
import argparse
import ast
import datetime
import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bt  # noqa: E402
import dshbatch  # noqa: E402
import judge  # noqa: E402
import metrics  # noqa: E402
import samples as SM  # noqa: E402
from samples import DOWN, GUARD4, LANGS, GLANG, PLATFORMS, TRAITS8, TRANSPARENCY3, INVERTED  # noqa: E402

DATA = SM.DATA
REPO = Path(os.environ.get("GP_REPO", str(HERE.parent.parent)))
FREEZE_DATA = REPO / "bench" / "freeze" / "FREEZE_DATA.json"
CONFIRM_DIR = REPO / "bench" / "confirm"
FREEZE_DOC = HERE / "VERIFIER_FREEZE.md"
GRAV_LINK = Path(os.environ.get("GP_GRAV_LINK", "W:/Projects/gravitas-claim-check"))
SCALE = bt.SCALE
SEED = 20261025
QUOTA = {"zh": 7, "en": 4, "ja": 3, "ko": 3}
EMILY_MARKERS = ["EMILY QUALITY LOOP", "# Reasoning method", "argon-baseline"]  # as answer_agy.py
GEMINI_MODEL_PREFIX = "gemini-4-argon"
MIN_PROSE_CHARS = 20
# Slice minimums, about two thirds of what the labelled held-out set gives (no-flaw 93%, settled 30%,
# open 7% of 240 labelled questions); N7 on Gemini (8) is weak and GATES.md says so.
SLICE_MIN = {"C7": {"deepseek": 200, "gemini": 60}, "N1": {"deepseek": 60, "gemini": 25}, "N7": {"deepseek": 25, "gemini": 8}}
CLAUDE_MIN_PER_TRAIT = 30
B5_MIN_TWO_SIDED = 30
# Per trait: 40 hoc questions x 2 set pairs when no candidate is confirmed (80), x 4 when one is (160).
B5T_MIN_SHARED = 80
# Reported only (stage 1f, reverted as gates in stage 1g): tie shares on the comparisons whose
# question was written to invite the trait, with at least 6 per trait in the calibration and 8 on
# held-out.
K0A_MIN_PROVOKED = 6
B4_MIN_PROVOKED = 8
CLAUDE_PROJECTS = Path(os.environ.get("GP_CLAUDE_PROJECTS", "C:/Users/emily/.claude/projects"))
BALANCE_AFTER = REPO / "bench" / "freeze" / "BALANCE_AFTER.json"
ELO_PER_SHARE = SCALE / 0.25  # about 695 Elo per unit of favourable share at even odds
# D3 amendment (2026-10-26): the decision rules the verifier can recompute, by the sha256 of the
# candidate's DECISION.md. A candidate whose rule is not here fails D3a (decision not recomputed).
DECISION_RULES = {"bottomline": "218c0c10da7e2e9876b9721b794566887af1ca0e95c867de0fb272b736c72168"}
B5_MIN_SHARED = 100

# WIN_CRITERIA's instruments, never metrics.py's: the round-one hedge list, the extended list and the
# fabricated-source list for zh and en are read from round three's frozen verdict.py (H_ROUND1,
# H_EXTENDED, FAB, MAY_MONTH); the ja and ko lists are WIN_CRITERIA's amendments of 2026-10-23 and
# 2026-10-24, copied here and checked word for word against WIN_CRITERIA.md by self_test().
VERDICT_PY = REPO / "docs" / "dsh-ab" / "round-three" / "verdict.py"
WIN_CRITERIA = REPO / "docs" / "dsh-ab" / "WIN_CRITERIA.md"
HEDGE_JA = {"first": ["かもしれ", "おそらく", "恐らく", "たぶん", "可能性があ", "と思われ", "断言できませ", "ご確認ください", "確認してください"],
            "extended": ["一般的に", "通常は", "場合によ", "地域によ", "自治体によ", "お問い合わせ", "問い合わせて", "相談してください", "目安"]}
HEDGE_KO = {"first": ["아마", "일지도", "할지도", "가능성이 있", "확실하지", "확인해 보세요", "확인하시기 바랍니다"],
            "extended": ["일반적으로", "보통은", "경우에 따라", "지역마다", "다를 수 있", "문의하", "상담하"]}
FAB_JA = [r"によると", r"によれば", r"確認したところ", r"調べたところ", r"公式(?:サイト|発表|ページ)(?:では|で確認)", r"照会したところ"]
FAB_KO = [r"에 따르면", r"확인한 결과", r"확인해 보니", r"조회한 결과", r"공식 ?(?:홈페이지|발표|사이트)에서 확인"]
_CANON = {}


def canon():
    """{'first', 'extended', 'fab', 'may'} for zh and en, parsed (not executed) from verdict.py."""
    if not _CANON:
        tree = ast.parse(VERDICT_PY.read_text(encoding="utf-8"))
        got = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
                if name in ("H_ROUND1", "H_EXTENDED", "FAB"):
                    got[name] = ast.literal_eval(node.value)
                elif name == "MAY_MONTH":
                    got[name] = ast.literal_eval(node.value.args[0])
        _CANON.update({"first": got["H_ROUND1"], "extended": got["H_EXTENDED"], "fab": got["FAB"], "may": re.compile(got["MAY_MONTH"])})
    return _CANON


def count_patterns(text, patterns, exclude):
    """Round three's count_patterns: matches summed, case-insensitive; with exclude, 可能 after 不
    and 'May' followed by a day or a year are not counted."""
    n = 0
    for p in patterns:
        for m in re.finditer(p, text, flags=re.I):
            if exclude:
                st = m.start()
                if m.group().startswith("可能") and st > 0 and text[st - 1] == "不":
                    continue
                if text.startswith("May", st) and canon()["may"].match(text, st):
                    continue
            n += 1
    return n


def hedge_rate(text, lang, which):
    """Markers per 1,000 characters of the final text, with the list of the question's language."""
    if not text:
        return 0.0
    if lang in ("zh", "en"):
        n = count_patterns(text, canon()[which], True)
    else:
        n = count_patterns(text, [re.escape(h) for h in (HEDGE_JA if lang == "ja" else HEDGE_KO)[which]], False)
    return 1000.0 * n / len(text)


def fab_count(text, lang):
    pats = canon()["fab"] if lang in ("zh", "en") else (FAB_JA if lang == "ja" else FAB_KO)
    return count_patterns(text, pats, False)


AGY_WEB_STEP = re.compile(r"url|browser|web", re.I)

# ------------------------------------------------------------------ independent language identifier
# Not metrics.detect_lang (the filter's own instrument). Stdlib only: lingua-py or fastText would be
# better and need Emily's OK (GATES.md, A2).
_TS = ("們们這这個个來来會会說说時时對对國国學学經经門门開开關关點点長长後后見见現现為为與与發发動动東东車车馬马語语讀读"
       "樣样還还當当應应實实體体種种將将進进過过問问題题話话認认讓让親亲記记議议論论產产環环電电區区號号歲岁際际單单間间"
       "從从雖虽嗎吗麼么機机氣气錢钱買买賣卖醫医藥药費费業业處处務务員员條条報报據据雜杂錯错難难雙双頭头線线網网紅红綠绿"
       "藍蓝黃黄傳传價价險险華华灣湾歷历戰战爭争聽听寫写書书備备寶宝決决變变師师帶带幫帮廣广張张強强歡欢總总戶户擇择導导"
       "舊旧識识調调簡简練练習习興兴邊边營营養养療疗壓压證证稅税貸贷債债鄰邻愛爱")
TRAD = {_TS[i] for i in range(0, len(_TS), 2)}
SIMP = {_TS[i + 1] for i in range(0, len(_TS), 2)}
STOP_EN = set("""the a an and or but of to in on for with is are was were be been being it its this that these those i you he she
we they my your our their me him her us them do does did have has had not no if so as at by from can will would should could
what how why when which who whom there here about more most just than then any some all also into over only very
""".split())
# Function words of other Latin-script languages and romanised Japanese: text where these outnumber
# the English ones is not English.
STOP_OTHER = set("""le la les des du et est une un au aux pour dans que qui pas sur avec el los las del y es en por con una
para como pero der die das und ist nicht mit ein eine zu den il di che non per sono gli um uma com nao wa ga wo ni desu
masu ka yo ne
""".split())
HAN, KANA, HANGUL = metrics.HAN, metrics.KANA, metrics.HANGUL


# Question language (A2, A5): lingua-language-detector, pinned by hash in bench/env/requirements-lingua.txt
# and installed in DATA/venv (Emily's OK, 2026-10-25). Four languages, as the question set has; two
# guards it cannot give: Traditional Chinese (the character table above) and another Latin-script
# language (its function words or accented letters). Answers keep the stdlib identifier (lang_of).
LINGUA_VERSION = "2.1.1"
_LINGUA = {}


def lingua_detector():
    if "d" not in _LINGUA:
        _LINGUA["d"] = None
        try:
            import importlib.metadata as im
            if im.version("lingua-language-detector") == LINGUA_VERSION:
                from lingua import Language, LanguageDetectorBuilder
                _LINGUA["map"] = {Language.CHINESE: "zh", Language.ENGLISH: "en", Language.JAPANESE: "ja", Language.KOREAN: "ko"}
                _LINGUA["d"] = LanguageDetectorBuilder.from_languages(*_LINGUA["map"]).build()
        except Exception:  # noqa: BLE001 - no lingua, or another version: the gates that need it fail as missing
            _LINGUA["d"] = None
    return _LINGUA["d"]


def question_lang(q):
    """zh, zh-Hant, ja, ko, en, latin-other or und for one question; None if lingua is unavailable."""
    d = lingua_detector()
    if d is None:
        return None
    lang = _LINGUA["map"].get(d.detect_language_of(q or ""), "und")
    if lang == "zh":
        tr, si = sum(1 for c in q if c in TRAD), sum(1 for c in q if c in SIMP)
        if tr >= 3 and tr > si:
            return "zh-Hant"
    if lang == "en":
        low = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'’]*", q)]
        if re.search(r"[À-ÿĀ-ž]", q) or (low and sum(w in STOP_OTHER for w in low) > sum(w in STOP_EN for w in low)):
            return "latin-other"
    return lang


def lang_of(text):
    """zh, zh-Hant, ja, ko, en, latin-other or und, from prose (code and URLs removed)."""
    t = metrics.prose_text(text or "")
    han, kana, hangul = len(HAN.findall(t)), len(KANA.findall(t)), len(HANGUL.findall(t))
    words = re.findall(r"[A-Za-z][A-Za-z'’]*", t)
    cjk = han + kana + hangul
    if cjk == 0 and not words:
        return "und"
    if cjk > 0 and cjk >= 0.5 * len(words):
        if hangul >= 0.4 * cjk:
            return "ko"
        if kana >= 2 and kana >= 0.08 * (han + kana):
            return "ja"
        if han >= 0.6 * cjk:
            tr = sum(1 for c in t if c in TRAD)
            si = sum(1 for c in t if c in SIMP)
            return "zh-Hant" if tr >= 3 and tr > si else "zh"
        return "und"
    low = [w.lower() for w in words]
    en = sum(1 for w in low if w in STOP_EN) / len(low)
    other = sum(1 for w in low if w in STOP_OTHER) / len(low)
    if other > en or re.search(r"[À-ÿĀ-ž]", t):
        return "latin-other"
    # Short questions ("Tipping etiquette Japan?") carry too few function words to test.
    return "en" if en >= 0.15 or len(low) < 8 else "latin-other"


# ---------------------------------------------------------------------------------------- helpers

def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def sha_text(t):
    return hashlib.sha256((t or "").encode("utf-8")).hexdigest()


def sha_file(p):
    p = Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def jl(p):
    p = Path(p)
    if not p.exists():
        return None
    out = []
    for l in open(p, encoding="utf-8", errors="replace"):
        if l.strip():
            try:
                out.append(json.loads(l))
            except ValueError:
                out.append({"_bad": l[:80]})
    return out


def git(*args, cwd=None):
    try:
        r = subprocess.run(["git", "-C", str(cwd or REPO)] + list(args), capture_output=True, timeout=60)
        return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def parse_time(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z").timestamp()
    except (TypeError, ValueError):
        return None


def elo_s(S, n):
    """Firth-penalised two-system Bradley-Terry difference (Elo) from Gravitas's total score S over
    n comparisons, ties as half. For two systems the Firth estimate has the closed form
    p = (S + 1/2) / (n + 1); self_test() checks it against bt.fit."""
    S = np.asarray(S, dtype=float)
    n = np.asarray(n, dtype=float)
    p = (S + 0.5) / (n + 1.0)
    return SCALE * np.log(p / (1.0 - p))


def rng_for(*parts):
    return np.random.default_rng(int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:12], 16) ^ SEED)


class Out:
    def __init__(self):
        self.m, self.detail, self.errors = {}, {}, []

    def put(self, key, value):
        if isinstance(value, (bool, np.bool_)):
            value = int(value)
        if isinstance(value, (np.integer,)):
            value = int(value)
        if isinstance(value, (np.floating,)):
            value = float(value)
        self.m[key] = value if (value is None or finite(value)) else None

    def note(self, key, value):
        self.detail[key] = value


# ------------------------------------------------------------------------------------ frozen inputs

def load_freeze():
    if not FREEZE_DATA.exists():
        return None
    try:
        return json.loads(FREEZE_DATA.read_text(encoding="utf-8"))
    except ValueError:
        return None


def freeze_commit():
    if not FREEZE_DOC.exists():
        return None
    m = re.search(r"Stage-1 freeze commit:\s*`?([0-9a-f]{40})`?", FREEZE_DOC.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def measure_code_freeze(o):
    c = freeze_commit()
    o.note("D4.freeze_commit", c)
    if not c:
        return
    if git("cat-file", "-e", c + "^{commit}") is None:
        return
    paths = ["bench/personality", "bench/env/requirements-lingua.txt", "docs/dsh-ab/WIN_CRITERIA.md", "docs/dsh-ab/round-three/verdict.py"]
    diff = git("diff", "--name-only", c, "--", *paths)
    untracked = git("ls-files", "--others", "--exclude-standard", "--", *paths)
    if diff is None or untracked is None:
        return
    changed = [f for f in diff.splitlines() + untracked.splitlines() if f.strip() and not f.endswith("VERIFIER_FREEZE.md")]
    o.put("D4.code_changed_files", len(changed))
    o.note("D4.code_changed", changed)


def measure_data_freeze(o, F):
    if F is None:
        return
    bad = []
    for rel, want in sorted((F.get("files") or {}).items()):
        if sha_file(DATA / rel) != want:
            bad.append(rel)
    o.put("D4.data_mismatch", len(bad) if F.get("files") else None)
    o.note("D4.data_mismatch", bad)
    lp = F.get("ledger_prefix") or {}
    led = DATA / "ledger.jsonl"
    if "lines" in lp and led.exists():
        lines = led.read_bytes().split(b"\n")
        prefix = b"\n".join(lines[: lp["lines"]])
        o.put("D4.ledger_prefix_ok", hashlib.sha256(prefix).hexdigest() == lp.get("sha256"))
    homes = F.get("agy_config") or {}
    hb = [h for h, want in homes.items() if tree_sha(DATA / "agy" / h / ".gemini" / "config") != want]
    o.put("D4.agy_config_mismatch", len(hb) if homes else None)
    o.note("D4.agy_config_mismatch", hb)
    # Files outside DATA that shape answers: the DSH profiles (model line), frozen at stage 2.
    ext = F.get("external_files") or {}
    eb = [f for f, want in ext.items() if sha_file(f) != want]
    o.put("D4.external_mismatch", len(eb) if ext else None)
    o.note("D4.external_mismatch", eb)


def tree_sha(root, exclude=()):
    root = Path(root)
    if not root.exists():
        return None
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.relative_to(root).as_posix() not in exclude:
            h.update(p.relative_to(root).as_posix().encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def stage2_time():
    """Commit time of the stage-2 data record (its first commit), or None."""
    log = git("log", "--format=%ct", "--reverse", "--", "bench/freeze/FREEZE_DATA.json")
    return int(log.split()[0]) if log and log.strip() else None


# ------------------------------------------------------------------------------------- question set

def tfidf_max(texts_a, texts_b=None):
    from sklearn.feature_extraction.text import TfidfVectorizer
    if len(texts_a) < 2 and texts_b is None:
        return None
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)).fit(texts_a + (texts_b or []))
    A = vec.transform(texts_a)
    if texts_b is None:
        S = (A @ A.T).toarray()
        np.fill_diagonal(S, 0)
        return float(S.max())
    if not texts_b:
        return None
    B = vec.transform(texts_b)
    return float((A @ B.T).toarray().max())


def q_size(q, lang):
    return len(q.split()) if lang == "en" else len(re.sub(r"\s", "", q))


SHORT_MAX = {"en": 12, "zh": 25, "ja": 30, "ko": 25}


def measure_questions(o, Q):
    allq, tun, ho = Q["all"], Q["tuning"], Q["heldout"]
    seed_ids = {s["id"] for s in SM.seeds_rows()}
    gen = [r for r in allq if r["id"] not in seed_ids]
    ho_ids, tu_ids = {r["id"] for r in ho}, {r["id"] for r in tun}
    o.put("A1.total", len(allq))
    o.put("A1.heldout_generated", sum(1 for r in ho if r["id"] not in seed_ids))
    doc = json.load(open(HERE / "traits.json", encoding="utf-8"))
    traits30 = [t for t in doc["traits"] if any(t in m for m in doc["indexes"].values())]
    cells = defaultdict(int)
    for r in gen:
        cells[(r.get("lang"), r.get("trait"), r.get("mode"))] += 1
    short = sum(max(0, QUOTA[l] - cells[(l, t, m)]) for l in LANGS for t in traits30 for m in ("invite", "neutral"))
    o.put("A1.shortfall", short)
    measured = {r["id"]: question_lang(r["q"]) for r in allq}
    if any(v is None for v in measured.values()):
        o.errors.append(f"lingua-language-detector {LINGUA_VERSION} is not importable: run verify.py with the venv's python "
                        "(DATA/venv/Scripts/python.exe); A2 and A5 stay missing")
        measured = {}
    o.note("A5.stdlib_disagreements", sum(1 for r in allq if lang_of(r["q"]) != r.get("lang")))
    n = len(allq) if measured else 0
    for l in LANGS:
        o.put(f"A2.share.{l}", sum(1 for v in measured.values() if v == l) / n if n else None)
    if n:
        shares = {l: sum(1 for v in measured.values() if v == l) for l in LANGS}
        o.put("A2.zh_largest", shares["zh"] > max(shares["en"], shares["ja"], shares["ko"]))
    tc = [sum(1 for r in gen if r.get("trait") == t) for t in traits30]
    o.put("A3.min_trait", min(tc) if gen else None)
    o.put("A3.max_trait", max(tc) if gen else None)
    for sp, ids in (("tuning", tu_ids), ("heldout", ho_ids)):
        for l in LANGS:
            rs = [r for r in gen if r["id"] in ids and r.get("lang") == l]
            o.put(f"A4.invite.{sp}.{l}", sum(1 for r in rs if r.get("mode") == "invite") / len(rs) if rs else None)
    mism = [r["id"] for r in allq if measured and measured[r["id"]] != r.get("lang")]
    o.put("A5.mismatch_share", len(mism) / n if n else None)
    o.put("A5.zh_hant", sum(1 for v in measured.values() if v == "zh-Hant"))
    o.note("A5.mismatch", mism[:20])
    for l in LANGS:
        texts = [r["q"] for r in allq if r.get("lang") == l]
        o.put(f"A6.maxcos.{l}", tfidf_max(texts) if len(texts) >= 2 else None)
        a = [r["q"] for r in tun if r.get("lang") == l]
        b = [r["q"] for r in ho if r.get("lang") == l]
        o.put(f"A7.maxcos_cross.{l}", tfidf_max(a, b) if a and b else None)
    o.put("A7.id_overlap", len(ho_ids & tu_ids))
    o.put("A7.seed_in_heldout", len(ho_ids & seed_ids))
    o.put("A7.not_split", len({r["id"] for r in allq} - ho_ids - tu_ids))
    o.put("A8.heldout_share", (sum(1 for r in gen if r["id"] in ho_ids) / len(gen)) if gen else None)
    for l in LANGS:
        rs = [r for r in allq if r.get("lang") == l]
        o.put(f"A10.short.{l}", sum(1 for r in rs if q_size(r["q"], l) <= SHORT_MAX[l]) / len(rs) if rs else None)
    # A11: every generated question passed a real rating call: the batch input holds the frozen
    # RATE_TEMPLATE for it, and the batch output parses and passes filter_questions.rating_ok.
    import filter_questions as FQ
    rated = dshbatch.load(DATA / "batches" / f"rate-{Q['set']}.out.jsonl")
    ins = {r.get("id"): r for r in (jl(DATA / "batches" / f"rate-{Q['set']}.in.jsonl") or [])}
    good = 0
    for r in gen:
        x, i = rated.get(r["id"]), ins.get(r["id"])
        want = FQ.RATE_TEMPLATE.format(lang_name=FQ.LANG_NAME[r["lang"]], q=r["q"], intent=FQ.intent(r)) if r.get("trait") in FQ.TRAITS else None
        good += bool(x and i and not x.get("error") and x.get("usage") and i.get("user") == want and FQ.rating_ok(FQ.parse_rating(x.get("text"))))
    o.put("A11.rated_share", good / len(gen) if gen and rated else None)
    return measured


# ------------------------------------------------------------------------------------------ answers

def dsh_extract(path):
    final, calls, web, bad = None, {}, False, 0
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            e = json.loads(line)
        except ValueError:
            bad += 1
            continue
        t = e.get("type")
        if t == "final":
            final = e.get("text") or ""
        elif t == "tool_call":
            calls[e.get("callId")] = e.get("tool")
        elif t == "tool_result" and e.get("status") == "completed" and calls.get(e.get("callId")) in ("web_fetch", "web_search"):
            web = True
    return {"text": final.strip() if final is not None else None, "web": web, "status": "final" if final is not None else None,
            "cid": None, "model": None}


def agy_extract(path):
    cid, status, text, model, web = None, None, None, None, False
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        ev = e.get("event")
        if ev == "init":
            cid = e.get("conversation_id")
            model = (e.get("init") or {}).get("model")
        elif ev == "result":
            r = e.get("result") or {}
            status, text = r.get("status"), (r.get("response") or "").strip()
        elif ev == "step_update":
            su = e.get("step_update") or {}
            if su.get("state") == "DONE" and AGY_WEB_STEP.search(str(su.get("step_type") or "")):
                web = True
    return {"text": text if status == "SUCCESS" else None, "web": web, "status": status, "cid": cid, "model": model}


def prose_len(t):
    return len(re.sub(r"\s+", " ", metrics.prose_text(t or "")).strip())


def load_answer(arm, qid, qlang, platform):
    base = DATA / "answers" / arm.replace(":", "_") / qid
    nd = base.with_suffix(".ndjson")
    rec = {"arm": arm, "qid": qid, "ok": False, "text": None, "web": False}
    if not nd.exists():
        return rec
    x = dsh_extract(nd) if platform == "deepseek" else agy_extract(nd)
    rec.update(x)
    rec["ndjson_sha"] = sha_file(nd)
    t = x["text"]
    rec["ok"] = bool(t) and prose_len(t) >= MIN_PROSE_CHARS
    txt = base.with_suffix(".txt")
    rec["txt_matches"] = txt.exists() and sha_text(txt.read_text(encoding="utf-8").strip()) == sha_text(t or "")
    if rec["ok"]:
        rec["m"] = metrics.measure(t, qlang)
        rec["lang"] = lang_of(t)
        rec["fmt"] = format_shape(t)
    rec["rule_log"] = base.with_suffix(".rule.jsonl")
    return rec


SEP = ("：", ":", "——", "—", "–", "－", "→", "=")


def format_shape(text):
    """Non-prose lines (red-team N13): headings, table rows, lines opening with a symbol, digit or
    bracket, and short label lines; separator lines (review 2: a label, then a colon, dash, arrow or
    equals sign within the first 15 characters), the shape a list keeps when its markers go."""
    lines = [l for l in metrics.strip_code(text).split("\n") if l.strip()]
    if not lines:
        return {"nonprose_share": 0.0, "nonprose_lines": 0, "sep_lines": 0}
    sep = sum(1 for l in lines if any(x in l.strip()[:15] for x in SEP))
    med = sorted(len(l.strip()) for l in lines)[len(lines) // 2]
    n = 0
    for l in lines:
        s = l.strip()
        first = s[0]
        cat = unicodedata.category(first)
        label = len(s) < 0.4 * med and not re.search(r"[.。!！?？…”」』)）]$", s)
        if metrics.HEADING.match(l) or s.startswith("|") or s.endswith("|") or not cat.startswith("L") or label:
            n += 1
    return {"nonprose_share": n / len(lines), "nonprose_lines": n, "sep_lines": sep}


# ------------------------------------------------------------------------------------------- ledger

def load_ledger():
    rows = jl(DATA / "ledger.jsonl") or []
    bad = sum(1 for r in rows if "_bad" in r)
    return [r for r in rows if "_bad" not in r], bad


# -------------------------------------------------------------------------------------- the measure

def compute(boot=1000):
    o = Out()
    measure_code_freeze(o)
    F = load_freeze()
    o.note("freeze_data", str(FREEZE_DATA) if F else "absent")
    measure_data_freeze(o, F)
    ledger, bad_ledger = load_ledger()
    o.put("N11.ledger_bad_lines", bad_ledger if ledger or bad_ledger else None)
    if not F or not F.get("set"):
        o.errors.append("no stage-2 data freeze (bench/freeze/FREEZE_DATA.json): question-set metrics are missing")
        measure_spend(o, ledger, F)
        return o
    setname = F["set"]
    qdir = DATA / "questions" / setname
    Q = {"set": setname, "all": jl(qdir / "all.jsonl"), "tuning": jl(qdir / "tuning.jsonl"), "heldout": jl(qdir / "heldout.jsonl")}
    if not all(Q[k] for k in ("all", "tuning", "heldout")):
        o.errors.append(f"question files missing in {qdir}")
        return o
    step(o, measure_questions, o, Q)
    qrows = {r["id"]: r for r in Q["all"]}

    # Samples, recomputed from the frozen files and compared with what was written.
    Sx = SM.build_samples(Q["heldout"], Q["tuning"], SM.seeds_rows())
    for name, s in Sx.items():
        on_disk = jl(DATA / "samples" / f"{name}.jsonl")
        o.put(f"S.{name}.match", on_disk is not None and [r["id"] for r in on_disk] == [r["id"] for r in s["rows"]])
        o.put(f"S.{name}.short", sum(s["short"].values()))
    sample_ids = {k: [r["id"] for r in v["rows"]] for k, v in Sx.items()}

    # Candidate (N14) before anything that needs the candidate's arm names.
    cand_name = measure_one_look(o, ledger, set(sample_ids["heldout"]), Q, sample_ids, F)
    step(o, measure_s0, o, ledger, set(sample_ids["heldout"]), F)
    designed = step(o, measure_candidate_amendment, o, ledger, Q, cand_name) or (None, None)
    base_only = designed[1] == 0 and o.m.get("D3a.heldout_consistent") == 1
    cand_arms = {"deepseek": f"ds-grav:{cand_name}", "gemini": f"gm-grav:{cand_name}"} if cand_name else {}

    # Which arm answers which questions.
    lists = {}
    for p, P in PLATFORMS.items():
        qs = sample_ids[P["questions"]]
        aa = sample_ids["aa150" if p == "deepseek" else "gmaa40"]
        lists[P["plain"]] = (p, "plain", qs)
        lists[P["base"]] = (p, "base", qs)
        lists[P["plain_aa"]] = (p, "plain_aa", aa)
        lists[P["grav_aa"]] = (p, "grav_aa", aa)
        if p in cand_arms:
            lists[cand_arms[p]] = (p, "cand", qs)
    _LANG_CACHE.clear()
    _LANG_CACHE.update({qid: r["lang"] for qid, r in qrows.items()})
    A = {}
    for arm, (p, role, qs) in lists.items():
        for qid in qs:
            A[(arm, qid)] = load_answer(arm, qid, qrows[qid]["lang"], p)
    for arm in ("ds-plain", "ds-grav"):  # the calibration slices (tuning): judged texts only, in no D gate
        for qid in sample_ids["cal15"] + sample_ids["cal15b"] + sample_ids.get("calp88", []):
            A[(arm, qid)] = load_answer(arm, qid, qrows[qid]["lang"], "deepseek")
    step(o, measure_runs, o, A, lists, ledger, qrows)
    step(o, measure_rules, o, A, lists, cand_name, cand_arms, F, qrows, ledger)

    # Judging.
    V, jobs_by_set = step(o, measure_judging, o, Sx, cand_arms, A, ledger, base_only) or ([], {})
    labels = step(o, load_labels, o, ledger, sample_ids, qrows, A, cand_arms) or {}
    step(o, measure_judges, o, V, jobs_by_set, A)
    routing = step(o, route, o, V) or {}
    step(o, measure_results, o, V, A, sample_ids, cand_arms, routing, labels, boot)
    step(o, measure_text, o, A, sample_ids, cand_arms, qrows, labels.get("slices"))
    step(o, measure_label_gates, o, labels, sample_ids, cand_arms, A, V)
    step(o, measure_rule_leak, o, designed[0] or cand_name, Q)
    step(o, measure_spend, o, ledger, F)
    step(o, measure_provenance, o, ledger, cand_name, jobs_by_set)
    step(o, measure_order, o, ledger, set(sample_ids["heldout"]), jobs_by_set)
    step(o, measure_versions, o, lists, cand_name)
    step(o, measure_frozen_inputs, o, cand_name)
    return o


def step(o, fn, *args):
    """Run one section; an exception is reported and its metrics stay missing (so their gates fail)."""
    try:
        return fn(*args)
    except Exception as e:  # noqa: BLE001 - every failure is reported, none is swallowed silently
        import traceback
        o.errors.append(f"{fn.__name__} crashed: {e!r} at {traceback.extract_tb(e.__traceback__)[-1].lineno}")
        return None


# ------------------------------------------------------------------------------- N14 one look / D3

def measure_one_look(o, ledger, heldout_ids, Q, sample_ids, F):
    names = set()
    for d in (DATA / "answers").glob("*"):
        m = re.match(r"^(?:ds-grav|gm-grav|raw-rule)_(.+)$", d.name)
        if m and any((d / f"{q}.ndjson").exists() or (d / f"{q}.txt").exists() for q in heldout_ids):
            names.add(m.group(1))
    for r in ledger:
        arm = str(r.get("arm") or "")
        if r.get("kind") == "answer-launch" and ":" in arm and r.get("qid") in heldout_ids:
            names.add(arm.split(":", 1)[1])
    pre = set((F or {}).get("pre_existing_judging") or [])
    judging_dirs = [d for d in (DATA / "judging").glob("*") if d.is_dir() and d.name not in pre]
    for d in judging_dirs:
        for j in jl(d / "jobs.jsonl") or []:
            for s in (j.get("left"), j.get("right")):
                if s and ":" in s and j.get("qid") in heldout_ids:
                    names.add(s.split(":", 1)[1])
    o.put("N14.candidates", len(names))
    o.note("N14.candidates", sorted(names))
    name = sorted(names)[0] if len(names) == 1 else None
    tuning_ids = {r["id"] for r in Q["tuning"]}
    cal = set(sample_ids["cal15"]) | set(sample_ids["cal15b"])
    calp = set(sample_ids.get("calp88", []))
    # Outside judges never saw a tuning comparison, except the cal0 slice with the base pair, and
    # (stage 1f) calp's questions with the base pair; P2 puts both after the candidate's decision.
    viol, cal_cand = 0, 0
    for d in judging_dirs:
        jobs = {j["job"]: j for j in jl(d / "jobs.jsonl") or [] if "job" in j}
        for j in jobs.values():
            if j.get("qid") in cal and any(":" in str(s) for s in (j.get("left"), j.get("right"))):
                cal_cand += 1
        for f in d.glob("*.jsonl"):
            if f.name in ("jobs.jsonl", "verdicts.jsonl") or f.name.endswith((".prompts.jsonl", ".raw.jsonl")) or ".batch" in f.name:
                continue
            for r in jl(f) or []:
                jdg = r.get("judge") or f.stem
                j = jobs.get(r.get("job"))
                if jdg == "deepseek" or not j or j.get("qid") not in tuning_ids:
                    continue
                pair = {j.get("left"), j.get("right")}
                if d.name in SM.CAL_SETS and j.get("qid") in cal and pair == {"ds-plain", "ds-grav"}:
                    continue
                if d.name == SM.CALP and j.get("qid") in calp and pair == {"ds-plain", "ds-grav"}:
                    continue
                viol += 1
    o.put("N14.tuning_outside_judge_rows", viol)
    o.put("N14.cal_slice_candidate_jobs", cal_cand)
    if not name:
        return None
    # CONFIRM committed before the candidate's first held-out launch or held-out judging build.
    rel = f"bench/confirm/{name}.json"
    log = git("log", "--format=%H %ct", "--reverse", "--", rel)
    first = log.split("\n")[0].split() if log and log.strip() else None
    starts = [r.get("start") for r in ledger if r.get("kind") == "answer-launch" and str(r.get("arm", "")).endswith(":" + name)
              and r.get("qid") in heldout_ids and finite(r.get("start"))]
    builds = [parse_time(r.get("time")) for r in ledger if r.get("kind") == "judge-build" and name in str(r.get("pairs"))]
    t_first = min([t for t in starts + builds if t is not None], default=None)
    if first:
        o.detail["confirm_time"] = int(first[1])
    if first and t_first is not None:
        o.put("N14.confirm_before_heldout", int(first[1]) < t_first)
        content = git("show", f"{first[0]}:{rel}")
        try:
            conf = json.loads(content) if content else None
        except ValueError:
            conf = None
        rules = (conf or {}).get("rules") or {}
        ok = bool(rules) and all(rules.get(f"{g}.md") == sha_file(DATA / "rules" / name / f"{g}.md") for g in GLANG.values())
        o.put("N14.confirm_rules_match", ok)
        o.note("confirm", {"commit": first[0], "rules": rules})
    elif not first:
        o.put("N14.confirm_before_heldout", 0)
    return name


def tuning_verdicts(set_name):
    """(jobs, verdict rows for bt, unparsed or mismatched count, rows) for one DeepSeek tuning set,
    each verdict re-parsed from its raw reply."""
    d = DATA / "judging" / set_name
    jobs = {j["job"]: j for j in jl(d / "jobs.jsonl") or [] if "job" in j}
    rows = jl(d / "deepseek.jsonl") or []
    out, bad = [], 0
    for r in rows:
        j = jobs.get(r.get("job"))
        v = judge.parse_verdict(r.get("raw"))
        if j is None or v is None or v != r.get("verdict"):
            bad += 1
            continue
        out.append({"qid": j["qid"], "trait": j["trait"], "left": j["left"], "right": j["right"],
                    "winner": {"A": j["left"], "B": j["right"], "TIE": None}[v]})
    return jobs, out, bad, len(rows)


def decide_bottomline(base_v, cand_v, name):
    """DECISION.md of `bottomline` (sha 218c0c10...): fit base and candidate verdicts together with
    the frozen bt.py anchored on ds-grav; CONFIRM only if Bottom-Line Summary's candidate-minus-base
    lower bound is above 0 and no other judged trait has its whole interval on the bad side of 0
    (up for Slop and Sycophantic, down for the rest)."""
    r = bt.ratings(base_v + cand_v, "ds-grav", boot=1000)
    res = {}
    for t in TRAITS8:
        if t not in r or f"ds-grav:{name}" not in r[t]["systems"]:
            return None, res
        res[t] = bt.diff(r, t, f"ds-grav:{name}", "ds-grav")
    ok = res["Bottom-Line Summary"]["lo"] > 0
    for t in TRAITS8:
        if t == "Bottom-Line Summary":
            continue
        worse = res[t]["lo"] > 0 if t in DOWN else res[t]["hi"] < 0
        ok = ok and not worse
    return ok, res


DECIDERS = {"bottomline": decide_bottomline}


def measure_candidate_amendment(o, ledger, Q, heldout_cand):
    """D3a and D3r (amendment of 2026-10-26). Exactly one candidate was designed (its rule folder,
    answers, launches and judging jobs name one candidate, in any split), frozen before its first run,
    and tuned under a decision rule recorded in the ledger; the verifier recomputes that rule from the
    candidate's DeepSeek tuning verdicts; the held-out outcome is the one the rule gives: confirmed and
    run under the original D3, or not confirmed and never touching held-out. Returns (name, confirm)."""
    tuning_ids = {r["id"] for r in Q["tuning"]}
    names = {d.name for d in (DATA / "rules").glob("*") if d.is_dir() and d.name != "base"}
    for d in (DATA / "answers").glob("*"):
        m = re.match(r"^(?:ds-grav|gm-grav|raw-rule)_(.+)$", d.name)
        if m:
            names.add(m.group(1))
    for r in ledger:
        arm = str(r.get("arm") or "")
        if r.get("kind") == "answer-launch" and ":" in arm:
            names.add(arm.split(":", 1)[1])
    dirs = [d for d in (DATA / "judging").glob("*") if d.is_dir()]
    jobs_of = {d.name: [j for j in jl(d / "jobs.jsonl") or [] if "job" in j] for d in dirs}
    for js in jobs_of.values():
        for j in js:
            for s_ in (j.get("left"), j.get("right")):
                if s_ and ":" in s_:
                    names.add(s_.split(":", 1)[1])
    o.put("D3a.candidates_designed", len(names))
    o.note("D3a.candidates_designed", sorted(names))
    if len(names) != 1:
        return None, None
    name = next(iter(names))
    rd = DATA / "rules" / name
    try:
        frozen = json.loads((rd / "FROZEN").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        frozen = {}
    rules = frozen.get("rules") or {}
    rules_ok = bool(rules) and all(rules.get(f"{g}.md") == sha_file(rd / f"{g}.md") for g in GLANG.values())
    fl = [r for r in ledger if r.get("kind") == "rule-freeze" and r.get("name") == name]
    dl = [r for r in ledger if r.get("kind") == "rule-decision-rule" and r.get("name") == name]
    dec_sha = sha_file(rd / "DECISION.md")
    o.put("D3a.artefacts_ok", rules_ok and len(fl) == 1 and fl[0].get("rules") == rules and len(dl) == 1 and dl[0].get("sha256") == dec_sha
          and dec_sha is not None)
    t_freeze = parse_time(fl[0].get("time")) if len(fl) == 1 else None
    t_rule = parse_time(dl[0].get("time")) if len(dl) == 1 else None
    starts = [r["start"] for r in ledger if r.get("kind") == "answer-launch" and str(r.get("arm", "")).endswith(":" + name) and finite(r.get("start"))]
    o.put("D3a.frozen_before_runs", (t_freeze < min(starts)) if t_freeze and starts else None)
    # The candidate's DeepSeek tuning set (ds-plain against ds-grav:NAME) and its base twin on the same jobs.
    cand_arm = f"ds-grav:{name}"
    cand_sets = [n for n, js in jobs_of.items() if any({j.get("left"), j.get("right")} == {"ds-plain", cand_arm} for j in js)]
    ok_sets, base_v, cand_v, cset = False, None, None, None
    if len(cand_sets) == 1:
        cset = cand_sets[0]
        cj = jobs_of[cset]
        key = lambda j: (j.get("qid"), j.get("trait"))
        ck = {key(j) for j in cj}
        twins = [n for n, js in jobs_of.items() if n != cset and js and all({j.get("left"), j.get("right")} == {"ds-plain", "ds-grav"} for j in js)
                 and {key(j) for j in js} == ck]
        judges_ok = set(judge_files(DATA / "judging" / cset)) == {"deepseek"}
        ledger_ok = True
        for n_ in [cset] + twins[:1]:
            b_ = [r for r in ledger if r.get("kind") == "judge-build" and r.get("name") == n_]
            r_ = [r for r in ledger if r.get("kind") == "judge-run" and r.get("name") == n_ and r.get("judge") == "deepseek"]
            ledger_ok = ledger_ok and len(b_) == 1 and len(r_) == 1 and r_[0].get("out_sha256") == sha_file(DATA / "judging" / n_ / "deepseek.jsonl")
        if twins:
            _, base_v, bad_b, n_b = tuning_verdicts(twins[0])
            _, cand_v, bad_c, n_c = tuning_verdicts(cset)
            cover = len(cand_v) / len(cj) if cj else 0
            ok_sets = (judges_ok and ledger_ok and all(j.get("qid") in tuning_ids for j in cj) and not bad_b and not bad_c
                       and cover >= 0.98 and len(base_v) / max(1, len(jobs_of[twins[0]])) >= 0.98)
        o.note("D3a.tuning_sets", {"candidate": cset, "base": twins[:1]})
        b_c = [parse_time(r.get("time")) for r in ledger if r.get("kind") == "judge-build" and r.get("name") == cset]
        run_c = [parse_time(r.get("time")) for r in ledger if r.get("kind") == "judge-run" and r.get("name") == cset]
        # D3r: the rule was in the ledger before the candidate's tuning set was built, so before any of
        # its tuning verdicts could exist.
        o.put("D3r.rule_before_tuning_judging", (t_rule < min(b_c)) if t_rule and b_c else None)
        o.note("D3r.times", {"decision_rule": dl[0].get("time") if dl else None, "tuning_build": [r.get("time") for r in ledger
               if r.get("kind") == "judge-build" and r.get("name") == cset]})
    o.put("D3a.tuning_sets_ok", ok_sets)
    # Recompute the decision.
    confirm = None
    if ok_sets and DECISION_RULES.get(name) == dec_sha and name in DECIDERS:
        confirm, res = DECIDERS[name](base_v, cand_v, name)
        o.note("D3a.decision", {"confirm": confirm, "candidate_minus_base": res})
    o.put("D3a.decision_recomputed", confirm is not None)
    if confirm is None:
        return name, None
    o.put("D3a.decision_confirm", int(confirm))
    log = git("log", "--format=%ct", "--reverse", "--", f"bench/confirm/{name}.json")
    t_confirm = int(log.split()[0]) if log and log.strip() else None
    touched = (o.m.get("N14.candidates") or 0) > 0
    confirmed_actual = t_confirm is not None or touched
    o.put("D3a.outcome_matches", int(confirm) == int(confirmed_actual))
    if confirm:
        consistent = heldout_cand == name and o.m.get("N14.candidates") == 1 and o.m.get("N14.confirm_before_heldout") == 1 \
            and o.m.get("N14.confirm_rules_match") == 1
    else:
        consistent = o.m.get("N14.candidates") == 0 and t_confirm is None
    o.put("D3a.heldout_consistent", consistent)
    times = [t for t in [t_rule, t_confirm] + run_c if t is not None]
    o.detail["decision_time"] = max(times) if times else None
    return name, int(confirm)


def measure_s0(o, ledger, heldout_ids, F):
    """S0: nothing touched a held-out question before the held-out set was frozen."""
    t2 = stage2_time()
    if t2 is None:
        return
    n = sum(1 for r in ledger if r.get("kind") == "answer-launch" and r.get("qid") in heldout_ids
            and finite(r.get("start")) and r["start"] < t2)
    # Every judging folder that existed at stage 2 (the record lists them), pilots and tuning sets alike.
    for d in (F or {}).get("judging_at_stage2") or (F or {}).get("pre_existing_judging") or []:
        n += sum(1 for j in jl(DATA / "judging" / d / "jobs.jsonl") or [] if j.get("qid") in heldout_ids)
    o.put("S0.heldout_touched_before_freeze", n)


# ------------------------------------------------------------------------------------- runs, rules

def measure_runs(o, A, lists, ledger, qrows):
    launches = defaultdict(list)
    for r in ledger:
        if r.get("kind") == "answer-launch":
            launches[(r.get("arm"), r.get("qid"))].append(r)
    gm_models, agy_versions = set(), set()
    for arm, (p, role, qs) in lists.items():
        if not qs:
            continue
        recs = [A[(arm, q)] for q in qs]
        o.put(f"D1.{p}.{role}.ok_share", sum(r["ok"] for r in recs) / len(recs))
        o.put(f"N11.{p}.{role}.txt_mismatch", sum(1 for r in recs if r["ok"] and not r.get("txt_matches")))
        viol = 0
        for r in recs:
            L = sorted(launches.get((arm, r["qid"]), []), key=lambda x: x.get("start") or 0)
            succ = [x for x in L if (x.get("exit") == 0 if p == "deepseek" else x.get("status") == "SUCCESS")]
            if len(succ) != 1 or not L or L[-1] is not succ[0]:
                viol += 1
                continue
            if succ[0].get("ndjson_sha256") != r.get("ndjson_sha") or succ[0].get("text_sha256") != sha_text(r.get("text") or ""):
                viol += 1
            if p == "gemini":
                agy_versions.add(succ[0].get("agy_version"))
        o.put(f"N11.{p}.{role}.launch_violations", viol)
        oks = [r for r in recs if r["ok"]]
        o.note(f"web_share.{p}.{role}", round(sum(1 for r in oks if r.get("web")) / len(oks), 3) if oks else None)  # reported, not gated
        ok = [r for r in recs if r["ok"]]
        o.put(f"N8.{p}.{role}.share", sum(1 for r in ok if r.get("lang") == qrows[r["qid"]]["lang"]) / len(ok) if ok else None)
        if p == "gemini":
            gm_models |= {r.get("model") for r in recs if r.get("status")}
    gm_models.discard(None)
    o.put("D6.gm_models", len(gm_models) if gm_models else None)
    o.put("D6.gm_model_ok", len(gm_models) == 1 and next(iter(gm_models)).startswith(GEMINI_MODEL_PREFIX) if gm_models else None)
    o.note("D6.gm_models", sorted(gm_models))
    o.put("D6.agy_versions", len(agy_versions) if agy_versions and None not in agy_versions else None)
    o.note("D6.agy_versions", sorted(str(v) for v in agy_versions))
    # A/A runs are fresh launches: their texts differ from the first run's.
    for p, P in PLATFORMS.items():
        for a1, a2, role in ((P["plain"], P["plain_aa"], "plain_aa"), (P["base"], P["grav_aa"], "grav_aa")):
            qs = lists[a2][2]
            both = [(A[(a1, q)], A[(a2, q)]) for q in qs if A.get((a1, q), {}).get("ok") and A[(a2, q)]["ok"]]
            o.put(f"C9.{p}.{role}.identical_share", sum(1 for x, y in both if x["text"] == y["text"]) / len(both) if both else None)


def note_text(g, head):
    out = git("show", f"{head}:dsh/platform/{g}.rule.md", cwd=GRAV_LINK)
    return out


def rule_lines(text):
    return [x.strip() for x in (text or "").splitlines() if len(x.strip()) > 20 and not x.strip().startswith("<!--")]


def db_bytes(cid):
    if not cid:
        return None
    hits = glob.glob(str(DATA / "agy" / "home-*" / ".gemini" / "antigravity-cli" / "conversations" / f"{cid}.db"))
    if len(hits) != 1:
        return None
    b = Path(hits[0]).read_bytes()
    wal = Path(hits[0] + "-wal")
    return b + (wal.read_bytes() if wal.exists() else b"")


def measure_rules(o, A, lists, cand_name, cand_arms, F, qrows, ledger):
    F = F or {}
    head = F.get("grav_link_head")
    base_sha = F.get("rules_base") or {}
    all_rules = {}
    for d in (DATA / "rules").glob("*"):
        for g in GLANG.values():
            p = d / f"{g}.md"
            if p.exists():
                all_rules[(d.name, g)] = p.read_text(encoding="utf-8")
    expected_name = {}
    for p, P in PLATFORMS.items():
        expected_name[P["plain"]] = None
        expected_name[P["plain_aa"]] = None
        expected_name[P["base"]] = "base"
        expected_name[P["grav_aa"]] = "base"
        if p in cand_arms:
            expected_name[cand_arms[p]] = cand_name
    composed_cache = {}

    def composed(name, g):
        k = (name, g)
        if k not in composed_cache:
            rule = all_rules.get((name, g))
            note = note_text(g, head) if head else None
            ok_file = rule is not None and (name != "base" or sha_text(rule) == base_sha.get(g))
            composed_cache[k] = sha_text(rule.rstrip() + "\n\n" + note.strip() + "\n") if (ok_file and note is not None) else None
        return composed_cache[k]

    for arm, (p, role, qs) in lists.items():
        if not qs:
            continue
        name = expected_name.get(arm)
        good = 0
        for q in qs:
            r = A[(arm, q)]
            g = GLANG[qrows[q]["lang"]]
            if not r["ok"]:
                continue
            if p == "deepseek":
                log = r["rule_log"]
                recs = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()] if log.exists() else []
                if name is None:
                    good += not recs
                else:
                    want = composed(name, g)
                    good += bool(recs) and want is not None and recs[-1].get("sha256") == want and \
                        str(recs[-1].get("ruleFile", "")).replace("\\", "/").endswith(f"rules/{name}/{g}.md")
            else:
                data = db_bytes(r.get("cid"))
                if data is None:
                    continue
                qtext = re.sub(r"[\"'\\\n]", "", qrows[q]["q"])[:30]
                if qtext.encode("utf-8") not in data:
                    continue
                if any(m.encode() in data for m in EMILY_MARKERS):
                    continue
                own = rule_lines(all_rules.get((name, g))) if name else []
                others = {l for (n, gg), t in all_rules.items() if gg == g for l in rule_lines(t)} - set(own)
                if name and (not own or not all(l.encode("utf-8") in data for l in own)):
                    continue
                if any(l.encode("utf-8") in data for l in others):
                    continue
                good += 1
        o.put(f"D2.{p}.{role}.ok_share", good / len(qs))
    # Every DSH run of a held-out list used the GRAV_LINK commit frozen at stage 2.
    if head:
        heads = set()
        for r in ledger:
            if r.get("kind") == "answer-launch" and r.get("platform") == "dsh" and expected_name.get(r.get("arm")):
                heads.add(r.get("grav_link_head"))
        o.put("D2.grav_link_head_ok", heads == {head} if heads else None)


# ------------------------------------------------------------------------------------------ judging

def judge_files(d):
    out = {}
    for f in d.glob("*.jsonl"):
        if f.name in ("jobs.jsonl", "verdicts.jsonl") or f.name.endswith((".prompts.jsonl", ".raw.jsonl")) or ".batch" in f.name \
                or f.name == "critic.jsonl":
            continue
        out[f.stem] = f
    return out


def measure_judging(o, Sx, cand_arms, A, ledger, base_only=False):
    """V: one row per parsed verdict {set, judge, qid, lang, trait, s1, s2, left, right, winner}."""
    V, jobs_by_set = [], {}
    qlang = {r["id"]: r["lang"] for s in Sx.values() for r in s["rows"] if "lang" in r}
    builds = defaultdict(list)
    runs = defaultdict(list)
    for r in ledger:
        if r.get("kind") == "judge-build":
            builds[r.get("name")].append(r)
        elif r.get("kind") in ("judge-run", "judge-import"):
            runs[(r.get("name"), r.get("judge"))].append(r)
    mism_text = 0
    for name, spec in SM.active_sets().items():
        rows = Sx[spec["sample"]]["rows"]
        cell = {r["id"]: (r.get("trait"), r.get("mode")) for r in rows}  # the question's drafting cell (stage 1f)
        exp = SM.expected_jobs(name, rows, cand_arms, skip_missing_cand=base_only)
        d = DATA / "judging" / name
        if exp is None:
            continue
        expd = {j["job"]: j for j in exp}
        jobs_by_set[name] = expd
        got = {j["job"]: j for j in jl(d / "jobs.jsonl") or [] if "job" in j}
        o.put(f"D1.judging.{name}.jobs_exact", set(got) == set(expd) and all(got[k].get("judge") == expd[k]["judge"] for k in expd))
        o.put(f"N11.judging.{name}.builds", len(builds.get(name, [])))
        if builds.get(name):
            o.put(f"N11.judging.{name}.jobs_sha_ok", builds[name][-1].get("jobs_sha256") == sha_file(d / "jobs.jsonl"))
        # The text each job was built on is the text re-extracted from the event stream (reported-only
        # sets are counted apart, stage 1g).
        mm = 0
        for k, j in got.items():
            for side in ("left", "right"):
                a = A.get((j.get(side), j.get("qid")))
                if a is None or j.get(f"{side}_sha") != sha_text(a.get("text") or ""):
                    mm += 1
        if name in SM.REPORTED_ONLY:
            o.note(f"N11.judging.{name}.judged_text_mismatch", mm)
        else:
            mism_text += mm
        files = judge_files(d)
        judges = list(spec["judges"]) + [x for x in spec.get("all_judges", []) if x not in spec["judges"]]
        optional = spec.get("optional_judges", [])
        for jdg in judges + [x for x in optional if x in files]:
            assigned = [k for k, j in expd.items() if j["judge"] == jdg or "all_judges" in spec]
            f = files.get(jdg)
            rows_f = {r.get("job"): r for r in (jl(f) or []) if isinstance(r, dict)} if f else {}
            parsed, mismatch, raw_missing = 0, 0, 0
            for k in assigned:
                r = rows_f.get(k)
                if r is None:
                    continue
                if "raw" not in r:
                    raw_missing += 1
                    continue
                v = judge.parse_verdict(r.get("raw"))
                if v != r.get("verdict"):
                    mismatch += 1
                if v is None:
                    continue
                parsed += 1
                j = expd[k]
                win = {"A": j["left"], "B": j["right"], "TIE": None}[v]
                V.append({"set": name, "judge": jdg, "qid": j["qid"], "lang": qlang.get(j["qid"]), "trait": j["trait"],
                          "s1": j["pair"][0], "s2": j["pair"][1], "left": j["left"], "right": j["right"], "winner": win,
                          "job": k, "provoked": cell.get(j["qid"]) == (j["trait"], "invite")})
            if jdg in optional:
                o.note(f"B1.{name}.{jdg}.parsed", parsed)
                continue
            o.put(f"B1.{name}.{jdg}.parsed_share", parsed / len(assigned) if assigned and not raw_missing else None)
            o.put(f"B1.{name}.{jdg}.mismatch", mismatch if f else None)
            rr = runs.get((name, jdg), [])
            o.put(f"N11.judging.{name}.{jdg}.runs", len(rr))
            if rr and f:
                o.put(f"N11.judging.{name}.{jdg}.out_sha_ok", rr[-1].get("out_sha256") == sha_file(f))
            if jdg == "deepseek" and f:
                b = dshbatch.load(DATA / "batches" / f"judge-{name}.out.jsonl")
                o.put(f"N11.judging.{name}.deepseek_raw_mismatch",
                      sum(1 for k in assigned if k in rows_f and (b.get(k) or {}).get("text") != rows_f[k].get("raw")) if b else None)
    o.put("N11.judged_text_mismatch", mism_text if jobs_by_set else None)
    return V, jobs_by_set


def win_label(v):
    return "tie" if v["winner"] is None else ("s1" if v["winner"] == v["s1"] else "s2")


def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None
    labs = ("s1", "s2", "tie")
    po = sum(1 for a, b in pairs if a == b) / n
    ca = {l: sum(1 for a, _ in pairs if a == l) for l in labs}
    cb = {l: sum(1 for _, b in pairs if b == l) for l in labs}
    pe = sum(ca[l] * cb[l] for l in labs) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else None


def ac1(pairs):
    """Gwet's AC1 on three labels (s1, s2, tie). Unlike kappa it does not collapse when one judge
    gives one label to nearly everything (cal0 Sycophantic: exact agreement 13/15, kappa 0.00)."""
    n = len(pairs)
    if n == 0:
        return None
    labs = ("s1", "s2", "tie")
    po = sum(1 for a, b in pairs if a == b) / n
    pi = {l: (sum(1 for a, _ in pairs if a == l) + sum(1 for _, b in pairs if b == l)) / (2 * n) for l in labs}
    pe = sum(pi[l] * (1 - pi[l]) for l in labs) / (len(labs) - 1)
    return (po - pe) / (1 - pe) if pe < 1 else None


def provoked_ties(vs, min_n):
    """{trait: (tie share, n)} on the verdicts whose question invites the trait; None when a trait
    has fewer than min_n of them."""
    out = {}
    for t in TRAITS8:
        x = [v for v in vs if v["trait"] == t and v.get("provoked")]
        out[t] = (sum(1 for v in x if v["winner"] is None) / len(x), len(x)) if len(x) >= min_n else (None, len(x))
    return out


def direction(pairs, min_two_sided=1):
    both = [(a, b) for a, b in pairs if a != "tie" and b != "tie"]
    return (sum(1 for a, b in both if a == b) / len(both)) if len(both) >= max(1, min_two_sided) else None


def kappa_strat(pairs_by_trait):
    """Cohen's kappa with chance agreement computed within each trait, then pooled (review 2: a
    shared Gravitas effect on a trait raises pooled kappa without item-level agreement)."""
    labs = ("s1", "s2", "tie")
    num = den = 0.0
    for pairs in pairs_by_trait.values():
        n = len(pairs)
        if not n:
            continue
        po = sum(1 for a, b in pairs if a == b) / n
        pe = sum(sum(1 for a, _ in pairs if a == l) * sum(1 for _, b in pairs if b == l) for l in labs) / (n * n)
        num += n * (po - pe)
        den += n * (1 - pe)
    return num / den if den > 0 else None


def matched(V, ds_sets, cl_sets):
    """DeepSeek and Claude verdicts on the same comparison (question, trait, pair), any order."""
    ds = {(v["qid"], v["trait"], v["s1"], v["s2"]): v for v in V if v["judge"] == "deepseek" and v["set"] in ds_sets}
    out = []
    for v in V:
        if v["judge"] == "claude" and v["set"] in cl_sets:
            k = (v["qid"], v["trait"], v["s1"], v["s2"])
            if k in ds:
                out.append((ds[k], v))
    return out


# The comparisons C uses (plain against Gravitas). The cross-family pair is kept out of B5 (review 2:
# two model families are easier to agree on) and reported under B6a only.
MAIN_DS = ["ho-ds-base", "ho-ds-cand", "ho-gm-base", "ho-gm-cand"]
MAIN_CL = ["hoc-ds-base", "hoc-ds-cand", "hoc-gm-base", "hoc-gm-cand"]
SEAT_SETS = MAIN_DS + ["ho-xf"] + MAIN_CL + ["hoc-xf"]


def fav(v, arm):
    """Score of `arm` in the direction Gravitas aims for: shows more of an up trait, less of a down one."""
    if v["winner"] is None:
        return 0.5
    shows_more = v["winner"] == arm
    return float(shows_more) if v["trait"] not in DOWN else float(not shows_more)


def measure_judges(o, V, jobs_by_set, A):
    # B2: order swaps.
    def flips(sets, judge_name):
        g = defaultdict(list)
        for v in V:
            if v["set"] in sets and v["judge"] == judge_name:
                g[(v["qid"], v["trait"], v["s1"], v["s2"])].append(v["winner"])
        per_trait, allf = defaultdict(list), []
        for (q, t, a, b), ws in g.items():
            if len(ws) != 2:
                continue
            w1, w2 = ws
            f = 0.0 if w1 == w2 else (0.5 if (w1 is None or w2 is None) else 1.0)
            per_trait[t].append(f)
            allf.append(f)
        return allf, per_trait
    f, pt = flips({"swap-ds", "swap-gm"}, "deepseek")
    exp_n = sum(1 for s in ("swap-ds", "swap-gm") for _ in jobs_by_set.get(s, {})) // 2
    o.put("B2.deepseek.rate", sum(f) / len(f) if f and len(f) >= 0.9 * exp_n else None)
    o.put("B2.deepseek.max_trait", max(sum(x) / len(x) for x in pt.values()) if pt and len(pt) == len(TRAITS8) else None)
    f, _ = flips({"swapc"}, "claude")
    exp_n = len(jobs_by_set.get("swapc", {})) // 2
    o.put("B2.claude.rate", sum(f) / len(f) if f and len(f) >= 0.9 * exp_n else None)
    # B3: seats, from the jobs as built (the order is fixed by the frozen name).
    from scipy.stats import binomtest
    for name in SEAT_SETS:
        jobs = jobs_by_set.get(name)
        if not jobs:
            continue
        js = list(jobs.values())
        n = len(js)
        left2 = sum(1 for j in js if j["left"] == j["pair"][1])
        o.put(f"B3.{name}.seat_z", (left2 / n - 0.5) / (0.5 / math.sqrt(n)))
        ps = []
        for t in TRAITS8:
            jt = [j for j in js if j["trait"] == t]
            if jt:
                ps.append(binomtest(sum(1 for j in jt if j["left"] == j["pair"][1]), len(jt), 0.5).pvalue)
        o.put(f"B3.{name}.min_trait_p", min(ps) if ps else None)
    # B4: ties per judge over its main sets, overall and per trait over all questions (stage 1e; the
    # stage-1f reading on invite questions was reverted in stage 1g and is reported only).
    for jdg, sets in (("deepseek", MAIN_DS + ["ho-xf"]), ("claude", MAIN_CL + ["hoc-xf"])):
        vs = [v for v in V if v["judge"] == jdg and v["set"] in sets]
        if not vs:
            continue
        o.put(f"B4.{jdg}.tie", sum(1 for v in vs if v["winner"] is None) / len(vs))
        per = {t: sum(1 for v in vs if v["trait"] == t and v["winner"] is None) / sum(1 for v in vs if v["trait"] == t) for t in TRAITS8
               if any(v["trait"] == t for v in vs)}
        o.put(f"B4.{jdg}.max_trait_tie", max(per.values()) if len(per) == len(TRAITS8) else None)
        o.note(f"B4.{jdg}.trait_tie_all_questions", {t: round(x, 3) for t, x in per.items()})
        pv = provoked_ties(vs, B4_MIN_PROVOKED)
        o.note(f"B4.{jdg}.trait_tie_provoked", {t: (None if x is None else round(x, 3), n) for t, (x, n) in pv.items()})
    # B5: agreement with Claude on the comparisons C uses (plain against Gravitas, four set pairs).
    M = matched(V, MAIN_DS, MAIN_CL)
    pairs = [(win_label(a), win_label(b)) for a, b in M]
    by_t = {t: [(win_label(a), win_label(b)) for a, b in M if a["trait"] == t] for t in TRAITS8}
    o.put("B5.n", len(pairs))
    o.put("B5.kappa_strat", kappa_strat(by_t) if len(pairs) >= B5_MIN_SHARED else None)
    o.put("B5.direction", direction(pairs, B5_MIN_TWO_SIDED) if len(pairs) >= B5_MIN_SHARED else None)
    o.note("B5.kappa_pooled", kappa(pairs) if pairs else None)
    # B5t (stage 1e; the stage-1f pool with calp and hoc-syco and AC1 were reverted in stage 1g):
    # kappa and direction on the held-out check alone, at least 30 two-sided pairs.
    for t in TRAITS8:
        pt = by_t[t]
        o.put(f"B5t.{t}.n", len(pt))
        o.put(f"B5t.{t}.kappa", kappa(pt) if len(pt) >= B5T_MIN_SHARED else None)
        o.put(f"B5t.{t}.direction", direction(pt, B5_MIN_TWO_SIDED) if len(pt) >= B5T_MIN_SHARED else None)
        o.note(f"B5t.{t}.reported", {"ac1": ac1(pt), "two_sided": sum(1 for a_, b_ in pt if a_ != "tie" and b_ != "tie")})
        # DeepSeek's favourable share for the Gravitas arm minus Claude's, on this trait (B5t, B6m).
        lt = [fav(a, a["s2"]) - fav(b, a["s2"]) for a, b in M if a["trait"] == t]
        o.put(f"B5t.{t}.lean", float(np.mean(lt)) if len(lt) >= B5T_MIN_SHARED else None)
    # B6a (reported only): does DeepSeek lean towards DeepSeek-written answers? ds-plain against gm-plain.
    Mx = matched(V, ["ho-xf"], ["hoc-xf"])
    if Mx:
        d = [fav(a, "ds-plain") - fav(b, "ds-plain") for a, b in Mx]
        o.note("B6a.self_preference", {"n": len(d), "lean": round(float(np.mean(d)), 4)})
        o.note("B6a.per_trait", {t: round(float(np.mean([fav(a, "ds-plain") - fav(b, "ds-plain") for a, b in Mx if a["trait"] == t])), 3)
                                 for t in TRAITS8 if any(a["trait"] == t for a, _ in Mx)})
    # B6b: does DeepSeek lean towards the Gravitas arm on the comparisons C uses?
    for p, short in (("deepseek", "ds"), ("gemini", "gm")):
        for a in SM.ARMS:
            Mm = matched(V, [f"ho-{short}-{a}"], [f"hoc-{short}-{a}"])
            if Mm:
                g = Mm[0][0]["s2"]
                d = [fav(x, g) - fav(y, g) for x, y in Mm]
                o.put(f"B6b.{p}.{a}.lean", float(np.mean(d)) if len(d) >= 0.9 * len(jobs_by_set.get(f"hoc-{short}-{a}", {})) else None)
    # N15: is the judge picking the longer answer, compared with Claude on the same comparisons?
    for p, short in (("deepseek", "ds"), ("gemini", "gm")):
        Mm = matched(V, [f"ho-{short}-base", f"ho-{short}-cand"], [f"hoc-{short}-base", f"hoc-{short}-cand"])
        both = []
        for x, y in Mm:
            if x["winner"] is None or y["winner"] is None:
                continue
            la = (A.get((x["s1"], x["qid"])) or {}).get("text")
            lb = (A.get((x["s2"], x["qid"])) or {}).get("text")
            if not la or not lb:
                continue
            longer = x["s1"] if prose_len(la) >= prose_len(lb) else x["s2"]
            both.append((x["winner"] == longer, y["winner"] == longer))
        if len(both) >= 100:
            o.put(f"N15.{p}.length_bias_diff", float(np.mean([a for a, _ in both]) - np.mean([b for _, b in both])))


def route(o, V):
    """(source, correction) per (platform, arm, trait).

    Source: DeepSeek by default. A trait where DeepSeek disagrees badly with Claude (B5t: kappa < 0.40
    or direction < 0.75) moves to Claude only if Claude is no friendlier to Gravitas (lean_t at least
    -0.05); otherwise it is 'unreliable' (review 2: routing must never pick the friendlier judge).
    Correction (B6b, B6m): where DeepSeek favours the Gravitas arm more than Claude does beyond +0.05
    on a (platform, arm), or beyond +0.08 on a Transparency member or Slop, DeepSeek's points on it
    are moved back by 695 Elo per unit of that lean. A negative lean changes nothing (N10 still needs
    Claude to show the win).
    Stage 1g: a missing input never takes a passing value. A trait with any B5t input missing (kappa,
    direction, lean) is 'unreliable', and so is every DeepSeek-sourced trait of a (platform, arm)
    whose B6b lean is missing: their C metrics are then missing, not computed as if trusted."""
    m = o.m
    flagged, unreliable = set(), set()
    for t in TRAITS8:
        k, d, lt = m.get(f"B5t.{t}.kappa"), m.get(f"B5t.{t}.direction"), m.get(f"B5t.{t}.lean")
        if not all(finite(x) for x in (k, d, lt)):
            unreliable.add(t)
            continue
        if k < 0.40 or d < 0.75:
            flagged.add(t)
            if lt < -0.05:
                unreliable.add(t)
    R = {}
    for p in PLATFORMS:
        for a in SM.ARMS:
            ln = m.get(f"B6b.{p}.{a}.lean")
            for t in TRAITS8:
                src = "unreliable" if t in unreliable else ("claude" if t in flagged else "deepseek")
                c = 0.0
                if src == "deepseek":
                    if not finite(ln):
                        R[(p, a, t)] = ("unreliable", 0.0)
                        continue
                    lt = m.get(f"B5t.{t}.lean")
                    cands = [ln if ln > 0.05 else 0.0]
                    if t in TRANSPARENCY3 + ["Slop"]:
                        cands.append(lt if lt > 0.08 else 0.0)
                    c = ELO_PER_SHARE * max(cands)
                R[(p, a, t)] = (src, c)
    o.note("routing", {f"{p}.{a}.{t}": v for (p, a, t), v in R.items() if v != ("deepseek", 0.0)})
    o.note("B5.flagged", sorted(flagged))
    return R


# ------------------------------------------------------------------------------------------ results

def vindex(V):
    VI = defaultdict(list)
    for v in V:
        VI[(v["set"], v["judge"], v["trait"])].append(v)
    return VI


def per_q(VI, sets, judge_name, grav, trait, qids=None, pair=None):
    """{qid: [S, n]} Gravitas's score per question on one trait."""
    out = defaultdict(lambda: [0.0, 0])
    for v in (x for s_ in sets for x in VI.get((s_, judge_name, trait), [])):
        if (qids is None or v["qid"] in qids) and (pair is None or (v["s1"], v["s2"]) == pair):
            s = 0.5 if v["winner"] is None else (1.0 if v["winner"] == grav else 0.0)
            out[v["qid"]][0] += s
            out[v["qid"]][1] += 1
    return dict(out)


def index_boot(per_trait, signs, universe, boot, key, offsets=None):
    """Point, lo, hi of mean(sign * Elo diff - offset) over traits, joint bootstrap over questions
    (one draw of questions per resample, shared by every member). None if any member has no data.
    `offsets` carries B6b's debiasing in the index's own units."""
    offsets = offsets or {}
    if not universe or any(sum(n for _, n in per_trait[t].values()) == 0 for t in per_trait):
        return None
    U = sorted(universe)
    idx = {q: i for i, q in enumerate(U)}
    arrs = {}
    for t, d in per_trait.items():
        S = np.zeros(len(U))
        N = np.zeros(len(U))
        for q, (s, n) in d.items():
            if q in idx:
                S[idx[q]] += s
                N[idx[q]] += n
        arrs[t] = (S, N)
    point = float(np.mean([signs[t] * elo_s(arrs[t][0].sum(), arrs[t][1].sum()) - offsets.get(t, 0.0) for t in arrs]))
    if boot <= 0:
        return {"point": point, "lo": None, "hi": None}
    rng = rng_for(key)
    draws = rng.integers(0, len(U), size=(boot, len(U)))
    acc = np.zeros(boot)
    for t, (S, N) in arrs.items():
        acc += signs[t] * elo_s(S[draws].sum(1), N[draws].sum(1)) - offsets.get(t, 0.0)
    acc /= len(arrs)
    return {"point": point, "lo": float(np.percentile(acc, 2.5)), "hi": float(np.percentile(acc, 97.5))}


def slop_length_adjusted(V, sets, judge_name, grav, plain, A, universe, boot, key):
    """Slop at equal length (red-team N5): logistic fit of Gravitas's Slop score on the log ratio of
    prose lengths; the intercept in Elo, with a question bootstrap."""
    rows = []
    for v in V:
        if v["set"] in sets and v["judge"] == judge_name and v["trait"] == "Slop" and v["qid"] in universe:
            g, p_ = A.get((grav, v["qid"])), A.get((plain, v["qid"]))
            if not (g and p_ and g.get("ok") and p_.get("ok")):
                continue
            lg, lp = prose_len(g["text"]), prose_len(p_["text"])
            if lg <= 0 or lp <= 0:
                continue
            y = 0.5 if v["winner"] is None else (1.0 if v["winner"] == grav else 0.0)
            rows.append((v["qid"], y, math.log(lg / lp)))
    if len(rows) < 30:
        return None

    def fit(Y, X):
        a, b = 0.0, 0.0
        for _ in range(50):
            p = 1 / (1 + np.exp(-(a + b * X)))
            w = p * (1 - p) + 1e-9
            ga, gb = np.sum(Y - p) - 1e-3 * a, np.sum((Y - p) * X) - 1e-3 * b
            haa, hab, hbb = np.sum(w) + 1e-3, np.sum(w * X), np.sum(w * X * X) + 1e-3
            det = haa * hbb - hab * hab
            da, db = (hbb * ga - hab * gb) / det, (haa * gb - hab * ga) / det
            a, b = a + da, b + db
            if abs(da) + abs(db) < 1e-10:
                break
        return a
    byq = defaultdict(list)
    for q, y, x in rows:
        byq[q].append((y, x))
    qs = sorted(byq)
    Y = np.array([y for _, y, _ in rows])
    X = np.array([x for _, _, x in rows])
    point = SCALE * fit(Y, X)
    rng = rng_for(key)
    res = []
    for _ in range(boot):
        pick = rng.integers(0, len(qs), len(qs))
        rs = [r for i in pick for r in byq[qs[i]]]
        res.append(SCALE * fit(np.array([r[0] for r in rs]), np.array([r[1] for r in rs])))
    return {"point": point, "lo": float(np.percentile(res, 2.5)) if res else None, "hi": float(np.percentile(res, 97.5)) if res else None}


def measure_results(o, V, A, sample_ids, cand_arms, R, labels, boot):
    VI = vindex(V)
    # A/A margins per platform: |Elo(arm r2) - Elo(arm r1)|, the larger of plain and Gravitas.
    aa_sets = {"deepseek": "aa-ds", "gemini": "aa-gm"}
    margins, aamax = {}, {}
    for p, P in PLATFORMS.items():
        aa_q = set(sample_ids["aa150" if p == "deepseek" else "gmaa40"])
        for scope in ["all"] + LANGS:
            U = {q for q in aa_q if scope == "all" or lang_for(q, A) == scope}
            for label, members in (("T", TRANSPARENCY3), ("S", ["Slop"])) + tuple((t, [t]) for t in TRAITS8):
                vals = []
                for r1, r2 in ((P["plain"], P["plain_aa"]), (P["base"], P["grav_aa"])):
                    sets = [aa_sets[p]]
                    pt = {t: per_q(VI, sets, "deepseek", r2, t, U, pair=(r1, r2)) for t in members}
                    res = index_boot(pt, {t: (-1 if t in INVERTED and label == "T" else 1) for t in members}, U, 0, None)
                    vals.append(abs(res["point"]) if res else None)
                if None not in vals:
                    aamax[(p, scope, label)] = max(vals)
                    if scope == "all" and label in TRAITS8:
                        margins[(p, label)] = min(50.0, max(25.0, max(vals)))
            for label in ("T", "S"):
                o.put(f"AA.{p}.{scope}.{label}.max", aamax.get((p, scope, label)))
        for t in TRAITS8:
            o.put(f"M.{p}.{t}", margins.get((p, t)))
    slices = labels.get("slices") or {}
    claude_n = defaultdict(list)
    for p, P in PLATFORMS.items():
        short = "ds" if p == "deepseek" else "gm"
        universe_all = set(sample_ids[P["questions"]])
        for a in SM.ARMS:
            grav = P["base"] if a == "base" else cand_arms.get(p)
            if not grav:
                continue
            plain = P["plain"]
            # Stage 1g: a cell route() did not produce (route crashed) is unreliable, never DeepSeek-trusted.
            src = {t: R.get((p, a, t), ("unreliable", 0.0))[0] for t in TRAITS8}
            corr = {t: R.get((p, a, t), ("unreliable", 0.0))[1] for t in TRAITS8}
            sets_for = {"deepseek": [f"ho-{short}-{a}"], "claude": [f"hoc-{short}-{a}"]}
            hoc = set(sample_ids["hoc40"])
            # Coverage for Claude-sourced traits.
            unreliable = {t for t in TRAITS8 if src[t] == "unreliable"}
            ncl = {t: sum(len(VI.get((s_, "claude", t), [])) for s_ in sets_for["claude"]) for t in TRAITS8}
            o.put(f"R.claude_min_n.{p}.{a}", min(ncl.values()))
            for t in TRAITS8:
                claude_n[t].append(ncl[t])
                if src[t] == "claude" and ncl[t] < CLAUDE_MIN_PER_TRAIT:
                    unreliable.add(t)
            o.note(f"C.{p}.{a}.sources", {t: ("unreliable" if t in unreliable else s) + (f" -{corr[t]:.0f} Elo" if corr[t] else "")
                                         for t, s in src.items()})

            def pt_for(t, U):
                return per_q(VI, sets_for[src[t]], src[t], grav, t, U) if src[t] in sets_for else {}

            def idx(members, U, scope, signs, tag):
                if any(t in unreliable for t in members):
                    return None
                # B6b debiasing: favourable Elo minus the correction, in this index's own units.
                offs = {t: signs[t] * (-1 if t in DOWN else 1) * corr[t] for t in members}
                return index_boot({t: pt_for(t, U) for t in members}, signs, U, boot, f"{p}|{a}|{scope}|{tag}", offs)
            tsigns = {t: (-1 if t in INVERTED else 1) for t in TRANSPARENCY3}
            for scope in ["all"] + LANGS:
                U = {q for q in universe_all if scope == "all" or lang_for(q, A) == scope}
                T = idx(TRANSPARENCY3, U, scope, tsigns, "T")
                S = idx(["Slop"], U, scope, {"Slop": 1}, "S")
                pre = f"C.{p}.{a}.{scope}"
                for lab, res in (("T", T), ("S", S)):
                    o.put(f"{pre}.{lab}.point", res["point"] if res else None)
                    if scope == "all":
                        o.put(f"{pre}.{lab}.lo", res["lo"] if res else None)
                        o.put(f"{pre}.{lab}.hi", res["hi"] if res else None)
            for t in TRAITS8:
                res = idx([t], universe_all, "all", {t: 1}, f"trait-{t}")
                o.put(f"C.{p}.{a}.trait.{t}.point", res["point"] if res else None)
                o.put(f"C.{p}.{a}.trait.{t}.lo", res["lo"] if res else None)
                o.put(f"C.{p}.{a}.trait.{t}.hi", res["hi"] if res else None)
            # Control slices from the question labels (N1, N7): Admits Uncertainty points. The definition
            # now calls doubt on a settled answer a TIE, so N1's trait point is kept beside the text
            # measure (N1h), which is the one that can see a doubt spray.
            for gate, trait, sl in (("N1", "Admits Uncertainty", "settled"), ("N7", "Admits Uncertainty", "open")):
                ids = set(slices.get(sl, [])) & universe_all
                if src[trait] == "claude":
                    ids &= hoc
                res = idx([trait], ids, sl, {trait: 1}, gate) if ids and trait not in unreliable else None
                o.put(f"{gate}.{p}.{a}.n", len(ids) if slices else None)
                o.put(f"{gate}.{p}.{a}.point", res["point"] if res else None)
            # C7: any challenge to the person (instrument trait, DeepSeek) on questions with nothing to challenge.
            ids = set(slices.get("noflaw", [])) & universe_all
            chal = per_q(VI, [f"chal-{short}-{a}"], "deepseek", grav, SM.CHALLENGE, ids)
            res = index_boot({SM.CHALLENGE: chal}, {SM.CHALLENGE: 1}, ids, 0, None) if ids and chal else None
            o.put(f"C7.{p}.{a}.n", len(ids) if slices else None)
            o.put(f"C7.{p}.{a}.point", res["point"] if res else None)
            cp = idx(["Constructive Pushback"], ids, "noflaw", {"Constructive Pushback": 1}, "C7cp") if ids else None
            o.note(f"C7.{p}.{a}.constructive_pushback_on_noflaw", cp)
            # N10: Claude's verdicts alone (each judge family on its own).
            for lab, members, signs in (("T", TRANSPARENCY3, tsigns), ("S", ["Slop"], {"Slop": 1})):
                pt = {t: per_q(VI, sets_for["claude"], "claude", grav, t, hoc) for t in members}
                res = index_boot(pt, signs, hoc, boot, f"{p}|{a}|claude|{lab}")
                o.put(f"N10.{p}.{a}.{lab}.point", res["point"] if res else None)
                o.note(f"N10.{p}.{a}.{lab}", res)
            # C11 (WIN_CRITERIA, 2026-10-24): more questions net-positive than net-negative, with the
            # question as the unit, over the four index traits in the direction Gravitas aims for.
            ptq = {t: pt_for(t, universe_all) for t in TRANSPARENCY3 + ["Slop"]}
            for scope in ["all"] + LANGS:
                pos = neg = nq = 0
                for q in universe_all:
                    if scope != "all" and lang_for(q, A) != scope:
                        continue
                    if any(q not in ptq[t] for t in ptq):
                        continue
                    net = 0.0
                    for t, d in ptq.items():
                        S_, n_ = d[q]
                        up = S_ - 0.5 * n_
                        net += -up if t in DOWN else up
                    pos += net > 0
                    neg += net < 0
                    nq += 1
                ok_ = not unreliable & set(ptq)
                o.put(f"C11.{p}.{a}.{scope}.pos", pos if ok_ else None)
                o.put(f"C11.{p}.{a}.{scope}.neg", neg if ok_ else None)
                o.put(f"C11.{p}.{a}.{scope}.n", nq if ok_ else None)
            # N5: Slop at equal length.
            s_src = src["Slop"]
            U = hoc if s_src == "claude" else universe_all
            res = slop_length_adjusted(V, sets_for[s_src], s_src, grav, plain, A, U, boot, f"{p}|{a}|N5") \
                if "Slop" not in unreliable and s_src != "unreliable" else None
            o.put(f"N5.{p}.{a}.hi", (res["hi"] + corr["Slop"]) if res and res["hi"] is not None else None)
            o.note(f"N5.{p}.{a}", res)
    n_arms = 2 * (1 + bool(cand_arms))
    for t in TRAITS8:
        o.put(f"B5t.{t}.claude_min_n", min(claude_n[t]) if len(claude_n[t]) == n_arms else None)


_LANG_CACHE = {}


def lang_for(qid, A):
    return _LANG_CACHE.get(qid)


# ------------------------------------------------------------------------------------- text metrics

def shingles(text, lang):
    t = re.sub(r"\d", "0", metrics.prose_text(text).lower())
    if lang == "en":
        w = re.findall(r"[a-z0']+", t)
        return {" ".join(w[i:i + 8]) for i in range(len(w) - 7)}
    s = re.sub(r"[\W_]+", "", t)
    return {s[i:i + 12] for i in range(len(s) - 11)}


def boiler_share(texts_by_q, lang):
    """Share of answers with a span that also appears in at least 5% of the arm's other answers
    in that language (and in at least 3 answers)."""
    sh = {q: shingles(t, lang) for q, t in texts_by_q.items()}
    df = defaultdict(int)
    for s in sh.values():
        for x in s:
            df[x] += 1
    n = len(sh)
    if n < 5:
        return None
    thr = max(3, math.ceil(0.05 * (n - 1)) + 1)
    return sum(1 for s in sh.values() if any(df[x] >= thr for x in s)) / n


def measure_text(o, A, sample_ids, cand_arms, qrows, slices=None):
    slices = slices or {}
    for p, P in PLATFORMS.items():
        universe = sample_ids[P["questions"]]
        gut = 0.6 if p == "deepseek" else 0.38
        for a in SM.ARMS:
            grav = P["base"] if a == "base" else cand_arms.get(p)
            if not grav:
                continue
            plain = P["plain"]
            for scope in ["all"] + LANGS:
                qs = [q for q in universe if scope == "all" or qrows[q]["lang"] == scope]
                pre = f"{p}.{a}.{scope}"
                ratios = []
                for q in qs:
                    g, pl = A[(grav, q)], A[(plain, q)]
                    if not pl["ok"] or pl["m"]["characters"] == 0:
                        continue
                    ratios.append(g["m"]["characters"] / pl["m"]["characters"] if g["ok"] else 0.0)
                o.put(f"C5.{pre}.median", float(np.median(ratios)) if ratios else None)
                o.put(f"C5.{pre}.gut_share", sum(1 for r in ratios if r < gut) / len(ratios) if ratios else None)
                both = [q for q in qs if A[(grav, q)]["ok"] and A[(plain, q)]["ok"]]
                for key, which in (("first", "first"), ("ext", "extended")):
                    for arm, tag in ((grav, "g"), (plain, "p")):
                        o.put(f"C6.{pre}.{key}.{tag}", float(np.mean([hedge_rate(A[(arm, q)]["text"], qrows[q]["lang"], which) for q in both]))
                              if both else None)
                for arm, tag in ((grav, "g"), (plain, "p")):
                    nw = [q for q in qs if A[(arm, q)]["ok"] and not A[(arm, q)]["web"]]
                    o.put(f"N6.{pre}.{tag}_count", sum(fab_count(A[(arm, q)]["text"], qrows[q]["lang"]) for q in nw) if qs else None)
                    o.put(f"N6.{pre}.{tag}_n", len(nw) if qs else None)
                if scope != "all":
                    for arm, tag in ((grav, "g"), (plain, "p")):
                        texts = {q: A[(arm, q)]["text"] for q in qs if A[(arm, q)]["ok"]}
                        o.put(f"N2.{pre}.{tag}", boiler_share(texts, scope))
                # Formatting shape (C10, N13): per answer and per 1,000 prose characters.
                if both:
                    for tag, arm in (("g", grav), ("p", plain)):
                        ms = [A[(arm, q)] for q in both]
                        chars = sum(x["m"]["characters"] for x in ms) or None
                        pa = lambda f: float(np.mean([f(x) for x in ms]))
                        pk = lambda f: (1000.0 * sum(f(x) for x in ms) / chars) if chars else None
                        bold = lambda x: x["m"]["bold"] + x["m"]["lenticular_brackets"]
                        for name, f in (("bold", bold), ("list", lambda x: x["m"]["list_items"]), ("colon", lambda x: x["m"]["colons"]),
                                        ("nonprose", lambda x: x["fmt"]["nonprose_lines"]), ("sep", lambda x: x["fmt"]["sep_lines"]),
                                        ("italic", lambda x: x["m"]["italics"])):
                            o.put(f"C10.{pre}.{name}_pa.{tag}", pa(f))
                            o.put(f"C10.{pre}.{name}_pk.{tag}", pk(f))
                        o.put(f"C10.{pre}.nonprose_share.{tag}", pa(lambda x: x["fmt"]["nonprose_share"]))
            # N1h, N7h: hedging measured in the text on the settled and open slices.
            for tag, sl in (("N1h", "settled"), ("N7h", "open")):
                if not slices:
                    continue
                qs = [q for q in set(slices.get(sl, [])) & set(universe) if A[(grav, q)]["ok"] and A[(plain, q)]["ok"]]
                for key, which in (("first", "first"), ("ext", "extended")):
                    for arm, t2 in ((grav, "g"), (plain, "p")):
                        o.put(f"{tag}.{p}.{a}.{key}.{t2}", float(np.mean([hedge_rate(A[(arm, q)]["text"], qrows[q]["lang"], which) for q in qs]))
                              if qs else None)
            if True:
                g_ok = [A[(grav, q)] for q in universe if A[(grav, q)]["ok"]]
                p_ok = [A[(plain, q)] for q in universe if A[(plain, q)]["ok"]]
                if g_ok and p_ok:
                    gs = sum(1 for r in g_ok if r["lang"] == qrows[r["qid"]]["lang"]) / len(g_ok)
                    ps = sum(1 for r in p_ok if r["lang"] == qrows[r["qid"]]["lang"]) / len(p_ok)
                    o.put(f"N8.{p}.{a}.gap", gs - ps)


# ------------------------------------------------------------------------------------------- labels

def load_labels(o, ledger, sample_ids, qrows, A, cand_arms):
    L = {}
    imports = defaultdict(list)
    for r in ledger:
        if r.get("kind") == "labels-import":
            imports[r.get("name")].append(r)
    files = {"ql": "ql.jsonl", "ql2": "ql2.jsonl", "n3points": "n3points.jsonl", "n3marks": "n3marks.jsonl", "n4": "n4.jsonl",
             "native": "native.jsonl"}
    for name, fn in files.items():
        p = DATA / "labels" / fn
        rows = jl(p)
        L[name] = rows
        im = imports.get(name, [])
        o.put(f"N11.labels.{name}.ok", (len(im) == 1 and im[0].get("sha256") == sha_file(p)) if rows is not None else None)
    L["critic"] = jl(DATA / "judging" / SM.CAL_SET / f"{SM.CRITIC_JUDGE}.raw.jsonl")
    # Question labels -> slices. Who made a label is checked by P1 from the transcripts, not by the
    # row's "labeller" field (the builder's assembler wrote "claude-sonnet-5-5-subagent").
    if L["ql"] is not None or L["ql2"] is not None:
        got = {}
        for name, samp in (("ql", "ql240"), ("ql2", "ql270")):
            for r in L[name] or []:
                if r.get("qid") in sample_ids[samp]:
                    x = SM.parse_ql(r.get("raw"))
                    if x:
                        got[r["qid"]] = x
        o.put("QL.coverage", len(got) / len(sample_ids["heldout"]))
        L["slices"] = {"noflaw": [q for q, x in got.items() if not x["flaw"]], "settled": [q for q, x in got.items() if x["settled"]],
                       "open": [q for q, x in got.items() if x["open"]]}
        o.note("QL.slices", {k: len(v) for k, v in L["slices"].items()})
    return L


def _present_share(marks, A, arm, qs):
    c = n = 0
    for q in qs:
        a = A.get((arm, q))
        mk = marks.get(q, {}).get(sha_text(a["text"])) if a and a["ok"] else None
        if mk:
            c += sum(1 for x in mk if x == "present")
            n += len(mk)
    return round(c / n, 3) if n else None


def measure_label_gates(o, L, sample_ids, cand_arms, A, V):
    # N3: key points kept, over the questions marked for both arms (coverage must be complete).
    pts = {r.get("qid"): SM.parse_points(r.get("raw")) for r in (L.get("n3points") or []) if r.get("qid")}
    marks = defaultdict(dict)
    for r in L.get("n3marks") or []:
        q = r.get("qid")
        if q in pts and pts[q]:
            mk = SM.parse_marks(r.get("raw"), len(pts[q]))
            if mk:
                marks[q][r.get("answer_sha")] = mk

    def mk_of(arm, q):
        a = A.get((arm, q))
        return marks.get(q, {}).get(sha_text(a["text"])) if a and a["ok"] else None
    n3q = sample_ids["n3_24"]
    if L.get("n3points") is not None and L.get("n3marks") is not None:
        for p, P in PLATFORMS.items():
            for a in SM.ARMS:
                grav = P["base"] if a == "base" else cand_arms.get(p)
                if not grav:
                    continue
                paired = [q for q in n3q if mk_of(grav, q) and mk_of(P["plain"], q)]
                o.put(f"N3.{p}.{a}.coverage", len(paired) / len(n3q))
                for role, arm in (("g", grav), ("p", P["plain"])):
                    c = defaultdict(int)
                    for q in paired:
                        for x in mk_of(arm, q):
                            c[x] += 1
                    n = sum(c.values())
                    for k in ("present", "vague", "wrong"):
                        o.put(f"N3.{p}.{a}.{k}.{role}", c[k] / n if n else None)
            for l in LANGS:
                ql_ = [q for q in n3q if _LANG_CACHE.get(q) == l]
                o.note(f"N3.{p}.{l}.present", {role: _present_share(marks, A, arm, ql_) for role, arm in
                                               (("plain", P["plain"]), ("base", P["base"]), ("aa", P["plain_aa"]))})
            aa = _present_share(marks, A, P["plain_aa"], n3q)
            pl = _present_share(marks, A, P["plain"], n3q)
            o.note(f"N3.{p}.aa_present_diff", (aa - pl) if aa is not None and pl is not None else None)
    # N4: wrong claims and wrong corrections, web-checked, paired; per answer and per checked claim.
    if L.get("n4") is not None:
        by = {}
        for r in L["n4"]:
            x = SM.parse_n4(r.get("raw"))
            if x:
                by[(r.get("qid"), r.get("answer_sha"))] = x
        for p, P in PLATFORMS.items():
            qs = sample_ids["n4ds12" if p == "deepseek" else "n4gm12"]
            for a in SM.ARMS:
                grav = P["base"] if a == "base" else cand_arms.get(p)
                if not grav:
                    continue
                get = lambda arm, q: by.get((q, sha_text((A.get((arm, q)) or {}).get("text") or "")))
                paired = [q for q in qs if get(grav, q) and get(P["plain"], q)]
                o.put(f"N4.{p}.{a}.coverage", len(paired) / len(qs))
                for role, arm in (("g", grav), ("p", P["plain"])):
                    xs = [get(arm, q) for q in paired]
                    o.put(f"N4.{p}.{a}.wrong.{role}", float(np.mean([x["wrong_claims"] for x in xs])) if xs else None)
                    o.put(f"N4.{p}.{a}.wrong_corrections.{role}", float(np.mean([x["wrong_corrections"] for x in xs])) if xs else None)
                    chk = sum(x["claims_checked"] for x in xs)
                    o.put(f"N4.{p}.{a}.wrong_per_claim.{role}", (sum(x["wrong_claims"] for x in xs) / chk) if chk else None)
    # A9: forced choice against Emily's seeds ("reads like Emily's seeds"), per language, with
    # machine-translated controls checked against their DeepSeek batch and their language.
    if L.get("native") is not None:
        Sx = {"native48": {"rows": jl(DATA / "samples" / "native48.jsonl") or []},
              "native_seeds": {"rows": jl(DATA / "samples" / "native_seeds.jsonl") or []},
              "native_control_sources": {"rows": jl(DATA / "samples" / "native_control_sources.jsonl") or []}}
        ctrl_rows = jl(DATA / "labels" / "native_controls.jsonl") or []
        pairs = {x["id"]: x for x in SM.native_pairs(Sx, ctrl_rows)}
        res = {"test": defaultdict(list), "control": defaultdict(list)}
        for r in L["native"]:
            x = pairs.get(r.get("id"))
            c = SM.parse_choice(r.get("raw"))
            if x and c:
                res[x["kind"]][x["lang"]].append(c == x["human_side"])
        allt = [v for vs in res["test"].values() for v in vs]
        o.put("A9.test_n", len(allt))
        o.put("A9.test_accuracy", float(np.mean(allt)) if len(allt) >= 0.9 * 48 else None)
        for l in LANGS:
            t_ = res["test"][l]
            o.put(f"A9.test_accuracy.{l}", float(np.mean(t_)) if len(t_) >= SM.SIZES["native48"][l] - 1 else None)
        # Controls: the translation is the DeepSeek batch's own text for the frozen prompt, in the target language.
        outs, ins = {}, {}
        for f in glob.glob(str(DATA / "batches" / "controls-*.out.jsonl")):
            outs.update(dshbatch.load(f))
        for f in glob.glob(str(DATA / "batches" / "controls-*.in.jsonl")):
            ins.update({r.get("id"): r for r in jl(f) or []})
        src = {c["id"]: c for c in Sx["native_control_sources"]["rows"]}
        valid, matched_ = set(), 0
        for c in ctrl_rows:
            sc = src.get(c.get("id"))
            want = SM.CONTROL_TEMPLATE.format(lang_name=SM.LANG_NAME[sc["lang"]], q=sc["from_q"]) if sc else None
            ok = sc and (ins.get(c["id"]) or {}).get("user") == want and (outs.get(c["id"]) or {}).get("text", "").strip() == str(c.get("q", "")).strip()
            matched_ += bool(ok)
            if ok and lang_of(c["q"]) == sc["lang"]:
                valid.add(c["id"])
        n_ctrl = SM.NATIVE_CONTROLS * len(LANGS)
        o.put("A9.controls_from_batch", matched_ / n_ctrl if ctrl_rows else None)
        o.put("A9.controls_valid", len(valid))
        cv = [v for r in L["native"] for x in [pairs.get(r.get("id"))] if x and x["kind"] == "control" and x["id"].split("|", 1)[1] in valid
              for c in [SM.parse_choice(r.get("raw"))] if c for v in [c == x["human_side"]]]
        o.put("A9.control_accuracy", float(np.mean(cv)) if len(cv) >= 20 else None)
    # K0: calibration on the new wording (cal0), trait-stratified kappa, and the blind critic on Gemini.
    cal = [v for v in V if v["set"] == SM.CAL_SET]
    by_job = defaultdict(dict)
    for v in cal:
        by_job[v["job"]][v["judge"]] = v
    both = [x for x in by_job.values() if "deepseek" in x and "claude" in x]
    by_t = {t: [(win_label(x["deepseek"]), win_label(x["claude"])) for x in both if x["deepseek"]["trait"] == t] for t in TRAITS8}
    o.put("K0.n", len(both))
    o.put("K0.kappa_strat", kappa_strat(by_t) if len(both) >= 100 else None)
    for jdg in ("deepseek", "claude"):
        per = []
        for t in TRAITS8:
            vs = [v for v in cal if v["judge"] == jdg and v["trait"] == t]
            if vs:
                per.append(sum(1 for v in vs if v["winner"] is None) / len(vs))
        o.put(f"K0.{jdg}.max_trait_tie", max(per) if len(per) == len(TRAITS8) else None)
    if L.get("critic") is not None:
        agree, n = 0, 0
        for r in L["critic"]:
            v = judge.parse_verdict(r.get("verdict"))
            x = by_job.get(r.get("job"), {}).get("claude")
            if v is None or x is None or r.get("status") != "SUCCESS":
                continue
            w = {"A": x["left"], "B": x["right"], "TIE": None}[v]
            n += 1
            agree += w == x["winner"]
        o.put("K0.critic_n", n)
        o.put("K0.critic_agreement", agree / n if n >= 0.9 * SM.CRITIC_PER_TRAIT * len(TRAITS8) else None)
    # K0a (stage 1f), reverted as a gate in stage 1g and REPORTED ONLY: cal0 plus calp, each judge's
    # ties per trait where the question invites it, and overall. K0 above is the calibration gate.
    calx = [v for v in V if v["set"] in (SM.CAL_SET, SM.CALP)]
    by_job2 = defaultdict(dict)
    for v in calx:
        by_job2[(v["set"], v["job"])][v["judge"]] = v
    both2 = [x for x in by_job2.values() if "deepseek" in x and "claude" in x]
    n_exp = (len(sample_ids["cal15"]) + len(sample_ids.get("calp88", []))) * len(TRAITS8)
    full = bool(sample_ids.get("calp88")) and len(both2) >= 0.9 * n_exp
    by_t2 = {t: [(win_label(x["deepseek"]), win_label(x["claude"])) for x in both2 if x["deepseek"]["trait"] == t] for t in TRAITS8}
    o.note("K0a.n", len(both2))
    o.note("K0a.kappa_strat", kappa_strat(by_t2) if full else None)
    o.note("K0a.per_trait", {t: {"n": len(p_), "ac1": ac1(p_), "kappa": kappa(p_), "direction": direction(p_),
                                 "two_sided": sum(1 for a_, b_ in p_ if a_ != "tie" and b_ != "tie")} for t, p_ in by_t2.items()})
    for jdg in ("deepseek", "claude"):
        vs = [v for v in calx if v["judge"] == jdg]
        pv = provoked_ties(vs, K0A_MIN_PROVOKED)
        o.note(f"K0a.{jdg}.trait_tie_provoked", {t: (None if x is None else round(x, 3), n_) for t, (x, n_) in pv.items()})
        o.note(f"K0a.{jdg}.max_provoked_tie", max(x for x, _ in pv.values()) if all(x is not None for x, _ in pv.values()) else None)
        o.note(f"K0a.{jdg}.tie", sum(1 for v in vs if v["winner"] is None) / len(vs) if vs else None)


# ---------------------------------------------------------------------------------------- rule leak

def ngrams(text):
    """8-character runs of Han and kana; 8-syllable runs of Hangul joined across spaces (Korean words
    are short and spaced, review 2); 5-word runs of Latin tokens that hold a letter or digit."""
    t = text.lower()
    out = set()
    for run in re.findall(r"[぀-ヿ㐀-䶿一-鿿]+", t):
        out |= {run[i:i + 8] for i in range(len(run) - 7)}
    for run in re.findall(r"[가-힯]+(?:\s+[가-힯]+)*", t):
        run = re.sub(r"\s+", "", run)
        out |= {run[i:i + 8] for i in range(len(run) - 7)}
    w = [x for x in re.findall(r"[a-z0-9']+", t) if re.search(r"[a-z0-9]", x)]
    out |= {" ".join(w[i:i + 5]) for i in range(len(w) - 4)}
    return out


def measure_rule_leak(o, name, Q):
    if not name:
        return
    cand = "\n".join((DATA / "rules" / name / f"{g}.md").read_text(encoding="utf-8") for g in GLANG.values()
                     if (DATA / "rules" / name / f"{g}.md").exists())
    base = "\n".join((DATA / "rules" / "base" / f"{g}.md").read_text(encoding="utf-8") for g in GLANG.values()
                     if (DATA / "rules" / "base" / f"{g}.md").exists())
    if not cand or not base:
        return
    grams = ngrams(cand) - ngrams(base)
    ho = set()
    for r in Q["heldout"]:
        ho |= ngrams(r["q"])
    tu = set()
    for r in Q["tuning"]:
        tu |= ngrams(r["q"])
    leaks = sorted((grams & ho) - tu)
    o.put("N9.leaks", len(leaks))
    o.note("N9.leaks", leaks[:20])


# ------------------------------------------------------------------------------------ spend and hours

def d5_total(records_now, records_at_stage2, balance_before, balance_after):
    """Total DeepSeek spend for D5: the larger of the usage records (since the pilots) and the records
    at stage 2 plus the account balance drop since stage 2. The two spans must match, so a deleted
    usage file after stage 2 cannot hide spend. None if any input is missing."""
    if not all(finite(x) for x in (records_now, records_at_stage2, balance_before, balance_after)):
        return None
    return max(records_now, records_at_stage2 + (balance_before - balance_after))


def measure_spend(o, ledger, F=None):
    usd = 0.0
    found = False
    for p in glob.glob(str(DATA / "batches" / "*.out.jsonl")):
        for r in jl(p) or []:
            u = r.get("usage")
            if u:
                found = True
                usd += dshbatch.cost_usd({"input": u.get("inputTokens", 0), "cache_read": u.get("cacheReadTokens", 0), "output": u.get("outputTokens", 0)})
    for nd in glob.glob(str(DATA / "answers" / "ds-*" / "*.ndjson")):
        u = {"input": 0, "cache_read": 0, "output": 0}
        web = 0
        for line in open(nd, encoding="utf-8", errors="replace"):
            if not line.startswith("{"):
                continue
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "status" and e.get("phase") == "step_end":
                x = e.get("usage") or {}
                u["input"] += x.get("inputTokens", 0)
                u["cache_read"] += x.get("cacheReadTokens", 0)
                u["output"] += x.get("outputTokens", 0)
            elif e.get("type") == "tool_call" and e.get("tool") in ("web_search", "web_fetch"):
                web += len(((e.get("input") or {}).get("queries") or [None])) if e.get("tool") == "web_search" else 1
        found = True
        usd += dshbatch.cost_usd(u) + 0.75 / 1000 * web
    # The independent instrument: the DeepSeek account balance Emily reads before stage 2 and after the
    # last run. Spend is the larger of the record sum and the balance drop; without both readings, missing.
    before = (F or {}).get("deepseek_balance_before_usd")
    after = None
    if BALANCE_AFTER.exists():
        try:
            after = json.loads(BALANCE_AFTER.read_text(encoding="utf-8")).get("usd")
        except ValueError:
            after = None
    total = d5_total(usd if found else None, (F or {}).get("deepseek_records_usd_at_stage2"), before, after)
    o.note("D5.records_usd", usd if found else None)
    o.note("D5.balance_drop_usd", (before - after) if finite(before) and finite(after) else None)
    o.put("D5.deepseek_usd", total)
    peak = 0
    n = 0
    for r in ledger:
        t = None
        if r.get("kind") == "answer-launch" and r.get("platform") == "dsh":
            t = r.get("start")
        elif r.get("kind") == "judge-run" and r.get("judge") == "deepseek":
            t = parse_time(r.get("time"))
        if finite(t):
            n += 1
            peak += dshbatch.is_peak(t)
    o.put("D5.peak_launches", peak if n else None)


# ------------------------------------------------------------------- P1, P2: provenance and order

LABEL_UNITS = {"ql": "qid", "ql2": "qid", "native": "id", "n3points": "qid", "n3marks": ("qid", "answer_sha"),
               "n4": ("qid", "answer_sha")}
CLAUDE_SETS = ["hoc-ds-base", "hoc-ds-cand", "hoc-gm-base", "hoc-gm-cand", "hoc-xf", "swapc", SM.HOCS]  # hoc-syco: stage 1f


def npath(x):
    return str(x).replace("/", "\\").lower()


def keyof(row, key):
    return tuple(row.get(k) for k in key) if isinstance(key, tuple) else row.get(key)


def scan_originals():
    """{normalised input path: {agentId}} over every Claude Code subagent transcript on this machine
    whose first message is a labelling wrapper (re-rolls show up as two agents for one batch)."""
    out = defaultdict(set)
    root = str(CLAUDE_PROJECTS.resolve() if CLAUDE_PROJECTS.exists() else CLAUDE_PROJECTS)
    if os.name == "nt" and not root.startswith("\\\\?\\"):
        root = "\\\\?\\" + root
    if not os.path.isdir(root):
        return out
    for proj in os.scandir(root):
        if not proj.is_dir():
            continue
        for sess in os.scandir(proj.path):
            sub = os.path.join(sess.path, "subagents")
            if not sess.is_dir() or not os.path.isdir(sub):
                continue
            for f in os.scandir(sub):
                if not f.name.endswith(".jsonl"):
                    continue
                try:
                    with open(f.path, encoding="utf-8") as fh:
                        first = json.loads(fh.readline())
                except (OSError, ValueError):
                    continue
                c = (first.get("message") or {}).get("content")
                if isinstance(c, str) and "Your only job is to answer" in c:
                    m = re.search(r"Input: (\S+?\.prompts\.jsonl)\.", c)
                    if m:
                        out[npath(m.group(1))].add(first.get("agentId") or f.name)
    return out


def check_transcript(rows, kind, inp, outp):
    """(ok, reason) for one labelling subagent's transcript against the frozen wrapper and tools."""
    if not rows or rows[0].get("type") != "user":
        return False, "no first user message"
    t = (rows[0].get("message") or {}).get("content")
    if not isinstance(t, str):
        return False, "first message is not text"
    mi, mo, mn = re.search(r"Input: (\S+?\.prompts\.jsonl)\.", t), re.search(r"Output: write (\S+?\.raw\.jsonl) ", t), \
        re.search(r"answer (\d+) separate", t)
    if not (mi and mo and mn) or npath(mi.group(1)) != npath(inp) or npath(mo.group(1)) != npath(outp):
        return False, "wrapper names another file"
    if SM.wrapper_text(kind, mn.group(1), mi.group(1), mo.group(1)) != t:
        return False, "wrapper differs from the frozen text"
    allowed = SM.WRAPPER_TOOLS.get(SM.WRAPPER_OF[kind], SM.DEFAULT_TOOLS)
    last_write, n_asst = None, 0
    for r in rows:
        if r.get("type") != "assistant":
            continue
        n_asst += 1
        msg = r.get("message") or {}
        if not str(msg.get("model") or "").startswith(SM.CLAUDE_MODEL):
            return False, f"model {msg.get('model')}"
        for x in msg.get("content") or []:
            if x.get("type") != "tool_use":
                continue
            name, inpt = x.get("name"), x.get("input") or {}
            if name not in allowed:
                return False, f"tool {name}"
            if name == "Read" and npath(inpt.get("file_path")) != npath(inp):
                return False, "read another file"
            if name == "Write":
                if npath(inpt.get("file_path")) != npath(outp):
                    return False, "wrote another file"
                last_write = inpt.get("content")
            if name == "Bash":
                for tok in re.findall(r"[A-Za-z]:[\\/][^\s\"']+", inpt.get("command") or ""):
                    if npath(tok) not in (npath(inp), npath(outp)):
                        return False, "bash touched another file"
    if not n_asst or last_write is None:
        return False, "no write"
    on_disk = Path(outp).read_text(encoding="utf-8") if Path(outp).exists() else None
    if on_disk is None or on_disk.replace("\r\n", "\n").rstrip("\n") != last_write.replace("\r\n", "\n").rstrip("\n"):
        return False, "raw file differs from what the subagent wrote"
    return True, "ok"


def measure_provenance(o, ledger, cand_name, jobs_by_set):
    """P1: every Claude label came from one Sonnet 5.5 subagent per batch, given the frozen wrapper
    and the frozen prompts, and was imported unedited. The critic's verdicts came from one Gemini
    3.8 Flash run per job (judge_agy's own ledger line and transcript)."""
    copies = defaultdict(list)
    for r in ledger:
        if r.get("kind") == "labeller-transcript":
            copies[r.get("batch")].append(r)
    originals = scan_originals()
    qs = None
    units = [(k, "label") for k in LABEL_UNITS] + [(s_, "judge") for s_ in [SM.CAL_SET, SM.CALP] + CLAUDE_SETS]
    for unit, typ in units:
        if typ == "label":
            key = LABEL_UNITS[unit]
            folder, prefix, kind = DATA / "labels", f"{unit}.batch", unit
            try:
                expected = {keyof(r, key): r for r in SM.export_rows(unit, cand_name)}
            except Exception:  # noqa: BLE001 - a prompt that cannot be rebuilt is not covered
                expected = {}
            imported = {keyof(r, key): r.get("raw") for r in jl(folder / f"{unit}.jsonl") or []}
            raw_field = "raw"
        else:
            key = "job"
            folder, prefix, kind = DATA / "judging" / unit, "claude.batch", "judge"
            jobs = jobs_by_set.get(unit) or {}
            if qs is None:
                qs = judge.load_questions()
            expected = {}
            got_jobs = {j["job"]: j for j in jl(folder / "jobs.jsonl") or [] if "job" in j}
            for k in jobs:
                try:
                    expected[k] = {"job": k, "prompt": judge.prompt_for(got_jobs[k], qs)}
                except (KeyError, SystemExit, TypeError):
                    pass
            imported = {r.get("job"): r.get("raw") for r in jl(folder / "claude.jsonl") or []}
            raw_field = "verdict"
        batches = sorted(folder.glob(f"{prefix}*.prompts.jsonl"))
        if not batches:
            continue
        seen, ok_b, problems = defaultdict(int), 0, []
        n_expected = len(SM.export_rows(unit, cand_name)) if typ == "label" else len(jobs_by_set.get(unit) or {})
        for b in batches:
            name = b.name[: -len(".prompts.jsonl")]
            raw_path = folder / f"{name}.raw.jsonl"
            batch_id = (f"{name}" if typ == "label" else f"{unit}.{name}")
            prompts = jl(b) or []
            raws = {keyof(r, key): r.get(raw_field) for r in jl(raw_path) or []}
            good = True
            for r in prompts:
                k = keyof(r, key)
                seen[k] += 1
                e = expected.get(k)
                if e is None or any(r.get(f) != e.get(f) for f in e):
                    good = False
                if raws.get(k) is None or imported.get(k) != raws.get(k):
                    good = False
            agents = {c.get("agent_id") for c in copies.get(batch_id, [])} | originals.get(npath(b), set())
            tr = None
            for c in copies.get(batch_id, []):
                if sha_file(c.get("transcript")) == c.get("sha256"):
                    tr = jl(c.get("transcript"))
            if len(agents) != 1 or tr is None:
                good = False
                problems.append(f"{batch_id}: {len(agents)} labelling agents, transcript {'found' if tr else 'missing'}")
            else:
                ok_t, why = check_transcript(tr, kind, b, raw_path)
                if not ok_t:
                    good = False
                    problems.append(f"{batch_id}: {why}")
            ok_b += good
        o.put(f"P1.{unit}.batches_ok", ok_b / len(batches))
        covered = sum(1 for k in expected if seen.get(k) == 1)
        o.put(f"P1.{unit}.coverage", covered / n_expected if n_expected and len(seen) == covered else (0.0 if n_expected else None))
        o.note(f"P1.{unit}.problems", problems[:10])
    # The critic on Gemini 3.8 Flash.
    crit_raw = jl(DATA / "judging" / SM.CAL_SET / f"{SM.CRITIC_JUDGE}.raw.jsonl")
    if crit_raw is not None:
        expected = {r["job"]: r["prompt"] for r in SM.export_rows("critic")}
        given = {r.get("job"): r.get("prompt") for r in jl(DATA / "judging" / SM.CAL_SET / f"{SM.CRITIC_JUDGE}.prompts.jsonl") or []}
        runs = defaultdict(list)
        for r in ledger:
            if r.get("kind") == "judge-agy-run" and r.get("job") in expected:
                runs[r["job"]].append(r)
        ok = 0
        for row in crit_raw:
            k = row.get("job")
            succ = [r for r in runs.get(k, []) if r.get("status") == "SUCCESS" and r.get("judge_clean")]
            data = db_bytes(succ[0].get("conversation_id")) if len(succ) == 1 else None
            trait = k.split("|")[1] if k and "|" in k else ""
            ok += bool(k in expected and given.get(k) == expected[k] and len(succ) == 1 and succ[0].get("raw_sha256") == sha_text(row.get("verdict"))
                       and data is not None and SM.CRITIC_MODEL.encode() in data and f"on one trait: {trait}".encode() in data)
        o.put("P1.critic.batches_ok", ok / len(crit_raw) if crit_raw else None)
        o.put("P1.critic.coverage", len({r.get("job") for r in crit_raw} & set(expected)) / len(expected) if expected else None)


def measure_order(o, ledger, heldout_ids, jobs_by_set):
    """P2: Claude's labels were made before the builder could see what they needed to be."""
    def t_of(kind, name, jdg=None):
        ts = [parse_time(r.get("time")) for r in ledger if r.get("kind") == kind and r.get("name") == name and (jdg is None or r.get("judge") == jdg)]
        ts = [t for t in ts if t is not None]
        return min(ts) if ts else None
    cal_cl, cal_ds = t_of("judge-import", SM.CAL_SET, "claude"), t_of("judge-run", SM.CAL_SET, "deepseek")
    o.put("P2.cal_claude_before_deepseek", (cal_cl < cal_ds) if cal_cl and cal_ds else None)
    # calp and hoc-syco are reported only (stage 1g): their orders are noted, not gated.
    calp_cl, calp_ds = t_of("judge-import", SM.CALP, "claude"), t_of("judge-run", SM.CALP, "deepseek")
    o.note("P2.calp_claude_before_deepseek", (calp_cl < calp_ds) if calp_cl and calp_ds else None)
    for x in ("ds-base", "ds-cand", "gm-base", "gm-cand", "xf"):
        a, b = t_of("judge-import", f"hoc-{x}", "claude"), t_of("judge-run", f"ho-{x}", "deepseek")
        o.put(f"P2.hoc_{x}_before_ho", (a < b) if a and b else None)
    a, b = t_of("judge-import", SM.HOCS, "claude"), t_of("judge-run", "ho-ds-base", "deepseek")
    o.note("P2.hoc_syco_before_ho", (a < b) if a and b else None)
    first_ho = min([r["start"] for r in ledger if r.get("kind") == "answer-launch" and r.get("qid") in heldout_ids and finite(r.get("start"))],
                   default=None)
    qls = [t_of("labels-import", n) for n in ("ql", "ql2")]
    o.put("P2.labels_before_heldout", all(t is not None for t in qls) and first_ho is not None and max(qls) < first_ho
          if first_ho is not None and all(t is not None for t in qls) else None)
    # The candidate's decision (its tuning verdicts, its decision rule, and CONFIRM if any) came before
    # Claude's calibration labels, so Claude's verdicts could not inform the tuning (D3 amendment).
    dt = o.detail.get("decision_time")
    # calp's Claude labels sit on tuning questions (N14 exempts them), so where they exist they too
    # must come after the decision; calp is not required.
    o.put("P2.decision_before_cal_claude", (dt < cal_cl and (calp_cl is None or dt < calp_cl)) if dt and cal_cl else None)
    builds = [parse_time(r.get("time")) for r in ledger if r.get("kind") == "judge-build" and r.get("name") in SM.SETS
              and r.get("name") not in SM.CAL_FAMILY + SM.REPORTED_ONLY]
    builds = [t for t in builds if t is not None]
    crit_jobs = {r["job"] for r in SM.export_rows("critic")} if (DATA / "judging" / SM.CAL_SET / "jobs.jsonl").exists() else set()
    crit = [parse_time(r.get("time")) for r in ledger if r.get("kind") == "judge-agy-run" and r.get("job") in crit_jobs]
    crit = [t for t in crit if t is not None]
    # cal0 (both judges) and the critic before any other build of a gated set.
    cal_all = [cal_cl, cal_ds]
    if builds and all(cal_all) and crit:
        o.put("P2.calibration_before_heldout_judging", max(cal_all + crit) < min(builds))


def measure_versions(o, lists, cand_name):
    """D6: the agy version of every Gemini run, read from each home's per-run logs after stage 2."""
    t2 = stage2_time()
    if t2 is None:
        return
    homes = [d for d in (DATA / "agy").glob("home-*") if d.is_dir()]
    vers = set()
    for h in homes:
        for f in (h / ".gemini" / "antigravity-cli" / "log").glob("cli-*.log"):
            m = re.match(r"cli-(\d{8})_(\d{6})\.log$", f.name)
            if not m:
                continue
            t = datetime.datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S").timestamp()
            if t < t2:
                continue
            vers |= set(re.findall(r"Language server version: (\S+)", f.read_text(encoding="utf-8", errors="replace")))
    o.put("D6.agy_versions", len(vers) if vers else None)
    o.note("D6.agy_versions", sorted(vers))


def measure_frozen_inputs(o, cand_name):
    """D4 extensions: every DeepSeek judge call ran on deepseek-flash; each candidate agy home equals
    its base home apart from the rule file; GRAV_LINK's working tree is clean."""
    bad = n = 0
    for name, spec in SM.active_sets().items():
        if "deepseek" not in spec["judges"]:
            continue
        for r in jl(DATA / "batches" / f"judge-{name}.out.jsonl") or []:
            n += 1
            bad += r.get("model") != "deepseek-flash"
    o.put("D4.judge_model_ok", (bad == 0) if n else None)
    if cand_name:
        rule = "plugins/gravitas/rules/AGENTS.md"
        res = []
        for g in GLANG.values():
            ch, bh = DATA / "agy" / f"home-grav-{cand_name}-{g}" / ".gemini" / "config", DATA / "agy" / f"home-grav-{g}" / ".gemini" / "config"
            if ch.exists():
                res.append(tree_sha(ch, exclude=(rule,)) == tree_sha(bh, exclude=(rule,)))
        o.put("D4.cand_home_ok", all(res) if len(res) == len(GLANG) else None)
    st = git("status", "--porcelain", cwd=GRAV_LINK)
    o.put("D2.grav_link_clean", (st.strip() == "") if st is not None else None)


# ---------------------------------------------------------------------------------------- self-test

def self_test():
    # The closed form is the two-system Firth fit of the frozen bt.py.
    rng = np.random.default_rng(3)
    for S, n in ((0, 7), (7, 7), (3.5, 9), (40, 61), (12, 13)):
        rows = [(1, 0, 1.0)] * int(S) + ([(1, 0, 0.5)] if S % 1 else []) + [(1, 0, 0.0)] * (n - int(math.ceil(S)))
        assert len(rows) == n
        t = bt.fit(["plain", "grav"], rows, "plain")
        assert abs(SCALE * t[1] - float(elo_s(S, n))) < 0.5, (S, n, SCALE * t[1], float(elo_s(S, n)))
    # Joint bootstrap: a perfectly anti-correlated pair of members gives a narrow interval for the mean.
    U = [f"q{i}" for i in range(200)]
    a = {q: [1.0 if i % 2 else 0.0, 1] for i, q in enumerate(U)}
    b = {q: [0.0 if i % 2 else 1.0, 1] for i, q in enumerate(U)}
    r = index_boot({"x": a, "y": b}, {"x": 1, "y": 1}, set(U), 300, "t")
    assert abs(r["point"]) < 1 and r["hi"] - r["lo"] < 1, r
    assert index_boot({"x": {}, "y": b}, {"x": 1, "y": 1}, set(U), 10, "t") is None
    # Language identifier.
    assert lang_of("这个问题的答案是肯定的，因为北京是首都。") == "zh"
    assert lang_of("這個問題的答案是肯定的，因為我們說過了。") == "zh-Hant"
    assert lang_of("東京は日本の首都です。おそらく。") == "ja"
    assert lang_of("서울은 한국의 수도입니다. 아마 맞을 겁니다.") == "ko"
    assert lang_of("How much should I tip at a restaurant in the US?") == "en"
    assert lang_of("Combien dois-je laisser de pourboire au restaurant?") == "latin-other"
    assert lang_of("Watashi wa nihon ni ikitai desu") == "latin-other"
    assert lang_of("Tipping etiquette Japan?") == "en" and lang_of("Best budget laptop for coding?") == "en"
    assert lang_of("¿Cuánto debo dejar de propina?") == "latin-other"
    assert lang_of("My landlord kept the whole deposit for normal wear, can he do that in Ontario?") == "en"
    assert lang_of("我用Python的pandas库读取CSV文件时报错了怎么办") == "zh"
    assert lang_of("") == "und"
    if lingua_detector() is not None:
        for q, want in (("腰の痛み、病院に行くべき？", "ja"), ("這個問題的答案是肯定的，因為我們說過了", "zh-Hant"), ("这个问题的答案是肯定的", "zh"),
                        ("Combien dois-je laisser de pourboire au restaurant?", "latin-other"), ("퇴직금은 얼마나 받을 수 있나요?", "ko"),
                        ("Does deleting files free up RAM straight away?", "en")):
            assert question_lang(q) == want, (q, question_lang(q))
    else:
        print(f"note: lingua {LINGUA_VERSION} not importable here, question_lang untested (run under DATA/venv)")
    # Kappa and direction.
    assert kappa([]) is None and direction([("tie", "tie")]) is None
    assert abs(kappa([("s1", "s1"), ("s2", "s2"), ("tie", "tie")]) - 1.0) < 1e-9
    # Boilerplate: a pasted sentence in every answer is found; distinct answers are not.
    texts = {f"q{i}": f"Answer number {i} talks about topic {i * 7} in its own words entirely. "
             + "Here is the same pasted disclaimer sentence that appears in every single answer." for i in range(20)}
    assert boiler_share(texts, "en") == 1.0
    texts2 = {f"q{i}": " ".join(re.sub(r"[^a-z]", "", hashlib.sha256(f"{i}-{j}".encode()).hexdigest()) or "z" for j in range(30))
              for i in range(20)}
    assert boiler_share(texts2, "en") == 0.0
    assert boiler_share({"a": "x"}, "en") is None
    # WIN_CRITERIA's instruments: round three's lists and exclusions, and the ja/ko amendments verbatim.
    assert count_patterns("这不可能。这可能需要时间。", canon()["first"], True) == 1
    assert count_patterns("It opened on May 5, 2026. You may need it.", canon()["first"], True) == 1
    assert count_patterns("具体以当地规定为准", canon()["extended"], True) == 2
    wc = WIN_CRITERIA.read_text(encoding="utf-8")
    for term in HEDGE_JA["first"] + HEDGE_JA["extended"] + HEDGE_KO["first"] + HEDGE_KO["extended"] + FAB_JA + FAB_KO:
        assert term in wc, f"not in WIN_CRITERIA.md: {term}"
    assert hedge_rate("おそらく雨です。", "ja", "first") > 0 and hedge_rate("", "ko", "first") == 0.0
    assert fab_count("据人社部官网公告，经查询如下", "zh") == 2 and fab_count("According to the site, I checked.", "en") == 2
    # Format shape.
    fs = format_shape("## Title\n\nPlain sentence one is here.\n- item\n**Bold:** x\nAnother plain sentence here.")
    assert fs["nonprose_lines"] == 3, fs
    # Out never stores NaN or infinity.
    o = Out()
    o.put("x", float("nan"))
    o.put("y", float("inf"))
    o.put("z", np.float64(1.5))
    assert o.m == {"x": None, "y": None, "z": 1.5}
    # Rule-leak n-grams: Han, joined Hangul, no apostrophe-only tokens.
    assert "住房公积金管理" not in ngrams("住房公积金管理中心") and "住房公积金管理中" in ngrams("住房公积金管理中心")
    assert "주택청약종합저축" in ngrams("주택청약 종합저축 월 납입액은 얼마인가요") and ngrams("' ' ' ' '") == set()
    # Stratified kappa: two traits each with a shared effect but no item agreement -> about 0.
    tr = {"T1": [("s2", "s2")] * 8 + [("s2", "s1"), ("s1", "s2")], "T2": [("s1", "s1")] * 8 + [("s1", "s2"), ("s2", "s1")]}
    assert kappa_strat(tr) < kappa([x for v in tr.values() for x in v])
    assert direction([("s1", "s1")] * 29, 30) is None and direction([("s1", "s1")] * 30, 30) == 1.0
    # D5: records since the pilots against records at stage 2 plus the balance drop since.
    assert d5_total(45.0, 30.0, 80.0, 55.0) == 55.0 and d5_total(45.0, 30.0, 80.0, 70.0) == 45.0
    assert d5_total(45.0, None, 80.0, 70.0) is None and d5_total(None, 30.0, 80.0, 70.0) is None
    # Separator lines: the list kept without its markers.
    assert format_shape("费用——每晚约五百日元。\n交通——地铁十分钟。\n这是一句普通的话。")["sep_lines"] == 2
    # Stage 1f. AC1 does not collapse where kappa does: cal0 Sycophantic (13 both TIE, 2 DeepSeek-only).
    syc = [("tie", "tie")] * 13 + [("s1", "tie"), ("s2", "tie")]
    assert abs(kappa(syc)) < 1e-9 and 0.85 < ac1(syc) < 0.87, (kappa(syc), ac1(syc))
    assert ac1([("s1", "s1"), ("s2", "s2"), ("tie", "tie")]) == 1.0 and ac1([]) is None
    assert ac1([("s1", "s2")] * 5 + [("s2", "s1")] * 5) < 0
    # Provoked ties: only the verdicts whose question invites the trait, and None below the minimum.
    vs = ([{"trait": "Sycophantic", "provoked": True, "winner": None}] * 3 + [{"trait": "Sycophantic", "provoked": True, "winner": "x"}] * 3
          + [{"trait": "Sycophantic", "provoked": False, "winner": None}] * 40)
    pv = provoked_ties(vs, 6)
    assert pv["Sycophantic"] == (0.5, 6) and pv["Slop"] == (None, 0)
    assert provoked_ties(vs, 7)["Sycophantic"] == (None, 6)
    print("measure_all self-test: ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
        return
    o = compute(a.boot)
    s = json.dumps({"metrics": o.m, "detail": o.detail, "errors": o.errors}, ensure_ascii=False, indent=1, default=str)
    if a.out:
        Path(a.out).write_text(s, encoding="utf-8")
    else:
        print(s)


if __name__ == "__main__":
    main()
