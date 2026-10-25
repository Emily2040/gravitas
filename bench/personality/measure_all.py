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
SLICE_MIN = {"C7": {"deepseek": 60, "gemini": 40}, "N1": {"deepseek": 40, "gemini": 25}, "N7": {"deepseek": 20, "gemini": 12}}
CLAUDE_MIN_PER_TRAIT = 30
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
    paths = ["bench/personality", "docs/dsh-ab/WIN_CRITERIA.md", "docs/dsh-ab/round-three/verdict.py"]
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


def tree_sha(root):
    root = Path(root)
    if not root.exists():
        return None
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file():
            h.update(p.relative_to(root).as_posix().encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


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
    traits30 = list(json.load(open(HERE / "traits.json", encoding="utf-8"))["traits"])
    cells = defaultdict(int)
    for r in gen:
        cells[(r.get("lang"), r.get("trait"), r.get("mode"))] += 1
    short = sum(max(0, QUOTA[l] - cells[(l, t, m)]) for l in LANGS for t in traits30 for m in ("invite", "neutral"))
    o.put("A1.shortfall", short)
    measured = {r["id"]: lang_of(r["q"]) for r in allq}
    n = len(allq)
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
    mism = [r["id"] for r in allq if measured[r["id"]] != r.get("lang")]
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
    rated = dshbatch.load(DATA / "batches" / f"rate-{Q['set']}.out.jsonl")
    ok = {i for i, r in rated.items() if not r.get("error") and r.get("usage")}
    o.put("A11.rated_share", (sum(1 for r in gen if r["id"] in ok) / len(gen)) if gen and rated else None)
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


def format_shape(text):
    """Non-prose lines (red-team N13): headings, table rows, lines opening with a symbol, digit or
    bracket, and short label lines; per answer and per 1,000 prose characters."""
    lines = [l for l in metrics.strip_code(text).split("\n") if l.strip()]
    if not lines:
        return {"nonprose_share": 0.0, "nonprose_lines": 0}
    med = sorted(len(l.strip()) for l in lines)[len(lines) // 2]
    n = 0
    for l in lines:
        s = l.strip()
        first = s[0]
        cat = unicodedata.category(first)
        label = len(s) < 0.4 * med and not re.search(r"[.。!！?？…”」』)）]$", s)
        if metrics.HEADING.match(l) or s.startswith("|") or s.endswith("|") or not cat.startswith("L") or label:
            n += 1
    return {"nonprose_share": n / len(lines), "nonprose_lines": n}


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
        measure_spend(o, ledger)
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
        for qid in sample_ids["cal15"] + sample_ids["cal15b"]:
            A[(arm, qid)] = load_answer(arm, qid, qrows[qid]["lang"], "deepseek")
    step(o, measure_runs, o, A, lists, ledger, qrows)
    step(o, measure_rules, o, A, lists, cand_name, cand_arms, F, qrows, ledger)

    # Judging.
    V, jobs_by_set = step(o, measure_judging, o, Sx, cand_arms, A, ledger) or ([], {})
    labels = step(o, load_labels, o, ledger, sample_ids, qrows, A, cand_arms) or {}
    step(o, measure_judges, o, V, jobs_by_set, A)
    routing = step(o, route, o, V) or {}
    step(o, measure_results, o, V, A, sample_ids, cand_arms, routing, labels, boot)
    step(o, measure_text, o, A, sample_ids, cand_arms, qrows)
    step(o, measure_label_gates, o, labels, sample_ids, cand_arms, A, V)
    step(o, measure_rule_leak, o, cand_name, Q)
    step(o, measure_spend, o, ledger)
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
    # Outside judges never saw a tuning comparison, except the cal0 slice with the base pair.
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
    ql = [parse_time(r.get("time")) for r in ledger if r.get("kind") == "labels-import" and r.get("name") == "ql"]
    if ql and t_first is not None:
        o.put("N14.labels_before_candidate", max(t for t in ql if t is not None) < t_first)
    return name


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


def measure_judging(o, Sx, cand_arms, A, ledger):
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
        exp = SM.expected_jobs(name, rows, cand_arms)
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
        # The text each job was built on is the text re-extracted from the event stream.
        for k, j in got.items():
            for side in ("left", "right"):
                a = A.get((j.get(side), j.get("qid")))
                if a is None or j.get(f"{side}_sha") != sha_text(a.get("text") or ""):
                    mism_text += 1
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
                          "job": k})
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


def direction(pairs):
    both = [(a, b) for a, b in pairs if a != "tie" and b != "tie"]
    return (sum(1 for a, b in both if a == b) / len(both)) if both else None


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


MAIN_DS = ["ho-ds-base", "ho-ds-cand", "ho-gm-base", "ho-gm-cand", "ho-xf"]
MAIN_CL = ["hoc-ds-base", "hoc-ds-cand", "hoc-gm-base", "hoc-gm-cand", "hoc-xf"]


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
    for name in MAIN_DS + MAIN_CL:
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
    # B4: ties per judge over its main sets.
    for jdg, sets in (("deepseek", MAIN_DS), ("claude", MAIN_CL)):
        vs = [v for v in V if v["judge"] == jdg and v["set"] in sets]
        if not vs:
            continue
        o.put(f"B4.{jdg}.tie", sum(1 for v in vs if v["winner"] is None) / len(vs))
        per = [sum(1 for v in vs if v["trait"] == t and v["winner"] is None) / max(1, sum(1 for v in vs if v["trait"] == t)) for t in TRAITS8
               if any(v["trait"] == t for v in vs)]
        o.put(f"B4.{jdg}.max_trait_tie", max(per) if len(per) == len(TRAITS8) else None)
    # B5: agreement with Claude on the held-out comparisons C uses (and the cross-family pairs).
    M = matched(V, MAIN_DS, MAIN_CL)
    pairs = [(win_label(a), win_label(b)) for a, b in M]
    o.put("B5.n", len(pairs))
    o.put("B5.kappa", kappa(pairs) if len(pairs) >= B5_MIN_SHARED else None)
    o.put("B5.direction", direction(pairs) if len(pairs) >= B5_MIN_SHARED else None)
    for t in TRAITS8:
        pt = [(win_label(a), win_label(b)) for a, b in M if a["trait"] == t]
        o.put(f"B5t.{t}.n", len(pt))
        o.put(f"B5t.{t}.kappa", kappa(pt) if len(pt) >= B5_MIN_SHARED else None)
        o.put(f"B5t.{t}.direction", direction(pt) if len(pt) >= B5_MIN_SHARED else None)
    # B6a: does DeepSeek lean towards DeepSeek-written answers? ds-plain against gm-plain.
    Mx = matched(V, ["ho-xf"], ["hoc-xf"])
    if Mx:
        d = [fav(a, "ds-plain") - fav(b, "ds-plain") for a, b in Mx]
        o.put("B6a.n", len(d))
        o.put("B6a.self_preference", float(np.mean(d)) if len(d) >= 0.9 * len(jobs_by_set.get("hoc-xf", {})) else None)
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
    """Which judge's verdicts each (platform, arm, trait) result uses. DeepSeek by default; Claude
    when DeepSeek disagrees badly on the trait (B5t), leans towards DeepSeek-written answers (B6a,
    Gemini platform) or leans towards the Gravitas arm (B6b)."""
    m = o.m
    flagged = set()
    for t in TRAITS8:
        k, d = m.get(f"B5t.{t}.kappa"), m.get(f"B5t.{t}.direction")
        if k is not None and d is not None and (k < 0.40 or d < 0.75):
            flagged.add(t)
    sp = m.get("B6a.self_preference")
    sp_fail = sp is not None and abs(sp) > 0.10
    R = {}
    for p in PLATFORMS:
        for a in SM.ARMS:
            ln = m.get(f"B6b.{p}.{a}.lean")
            lean_fail = ln is not None and abs(ln) > 0.10
            for t in TRAITS8:
                R[(p, a, t)] = "claude" if (t in flagged or (p == "gemini" and sp_fail) or lean_fail) else "deepseek"
    o.note("routing", {f"{p}.{a}.{t}": s for (p, a, t), s in R.items() if s != "deepseek"})
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


def index_boot(per_trait, signs, universe, boot, key):
    """Point, lo, hi of mean(sign * Elo diff) over traits, joint bootstrap over questions (one draw
    of questions per resample, shared by every member). None if any member has no data."""
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
    point = float(np.mean([signs[t] * elo_s(arrs[t][0].sum(), arrs[t][1].sum()) for t in arrs]))
    if boot <= 0:
        return {"point": point, "lo": None, "hi": None}
    rng = rng_for(key)
    draws = rng.integers(0, len(U), size=(boot, len(U)))
    acc = np.zeros(boot)
    for t, (S, N) in arrs.items():
        acc += signs[t] * elo_s(S[draws].sum(1), N[draws].sum(1))
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
            src = {t: R.get((p, a, t), "deepseek") for t in TRAITS8}
            sets_for = {"deepseek": [f"ho-{short}-{a}"], "claude": [f"hoc-{short}-{a}"]}
            hoc = set(sample_ids["hoc40"])
            # Coverage for Claude-sourced traits.
            unreliable = set()
            ncl = {t: sum(len(VI.get((s_, "claude", t), [])) for s_ in sets_for["claude"]) for t in TRAITS8}
            o.put(f"R.claude_min_n.{p}.{a}", min(ncl.values()))
            for t in TRAITS8:
                claude_n[t].append(ncl[t])
                if src[t] == "claude" and ncl[t] < CLAUDE_MIN_PER_TRAIT:
                    unreliable.add(t)
            o.note(f"C.{p}.{a}.sources", {t: ("unreliable" if t in unreliable else s) for t, s in src.items()})

            def pt_for(t, U):
                return per_q(VI, sets_for[src[t]], src[t], grav, t, U)

            def idx(members, U, scope, signs, tag):
                if any(t in unreliable for t in members):
                    return None
                return index_boot({t: pt_for(t, U) for t in members}, signs, U, boot, f"{p}|{a}|{scope}|{tag}")
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
            # Control slices from the question labels (C7, N1, N7): points only.
            for gate, trait, sl in (("C7", "Constructive Pushback", "noflaw"), ("N1", "Admits Uncertainty", "settled"), ("N7", "Admits Uncertainty", "open")):
                ids = set(slices.get(sl, [])) & universe_all
                if src[trait] == "claude":
                    ids &= hoc
                res = idx([trait], ids, sl, {trait: 1}, gate) if ids and trait not in unreliable else None
                o.put(f"{gate}.{p}.{a}.n", len(ids) if slices else None)
                o.put(f"{gate}.{p}.{a}.point", res["point"] if res else None)
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
                pos = neg = 0
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
                o.put(f"C11.{p}.{a}.{scope}.pos", pos if not unreliable & set(ptq) else None)
                o.put(f"C11.{p}.{a}.{scope}.neg", neg if not unreliable & set(ptq) else None)
            # N5: Slop at equal length.
            s_src = src["Slop"]
            U = hoc if s_src == "claude" else universe_all
            res = slop_length_adjusted(V, sets_for[s_src], s_src, grav, plain, A, U, boot, f"{p}|{a}|N5") if "Slop" not in unreliable else None
            o.put(f"N5.{p}.{a}.hi", res["hi"] if res else None)
            o.note(f"N5.{p}.{a}", res)
    for t in TRAITS8:
        o.put(f"B5t.{t}.claude_min_n", min(claude_n[t]) if len(claude_n[t]) == 4 else None)


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


def measure_text(o, A, sample_ids, cand_arms, qrows):
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
                                        ("nonprose", lambda x: x["fmt"]["nonprose_lines"])):
                            o.put(f"C10.{pre}.{name}_pa.{tag}", pa(f))
                            o.put(f"C10.{pre}.{name}_pk.{tag}", pk(f))
                        o.put(f"C10.{pre}.nonprose_share.{tag}", pa(lambda x: x["fmt"]["nonprose_share"]))
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
    files = {"ql": "ql.jsonl", "n3points": "n3points.jsonl", "n3marks": "n3marks.jsonl", "n4": "n4.jsonl", "native": "native.jsonl"}
    for name, fn in files.items():
        p = DATA / "labels" / fn
        rows = jl(p)
        L[name] = rows
        im = imports.get(name, [])
        o.put(f"N11.labels.{name}.ok", (len(im) == 1 and im[0].get("sha256") == sha_file(p)) if rows is not None else None)
    crit = DATA / "judging" / SM.CAL_SET / "critic.jsonl"
    L["critic"] = jl(crit)
    im = imports.get("critic", [])
    o.put("N11.labels.critic.ok", (len(im) == 1 and im[0].get("sha256") == sha_file(crit)) if L["critic"] is not None else None)
    # Question labels -> slices.
    if L["ql"] is not None:
        got = {}
        for r in L["ql"]:
            if r.get("qid") in sample_ids["ql240"] and r.get("labeller") == "claude":
                x = SM.parse_ql(r.get("raw"))
                if x:
                    got[r["qid"]] = x
        o.put("QL.coverage", len(got) / len(sample_ids["ql240"]))
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
    # N3: key points kept.
    pts = {r.get("qid"): SM.parse_points(r.get("raw")) for r in (L.get("n3points") or []) if r.get("qid")}
    marks = defaultdict(dict)
    for r in L.get("n3marks") or []:
        q = r.get("qid")
        if q in pts and pts[q]:
            mk = SM.parse_marks(r.get("raw"), len(pts[q]))
            if mk:
                marks[q][r.get("answer_sha")] = mk
    n3q = sample_ids["n3_24"]
    if L.get("n3points") is not None and L.get("n3marks") is not None:
        for p, P in PLATFORMS.items():
            arms = {"plain": P["plain"], "base": P["base"], "aa": P["plain_aa"]}
            if p in cand_arms:
                arms["cand"] = cand_arms[p]
            tot = {}
            for role, arm in arms.items():
                c = {"present": 0, "vague": 0, "wrong": 0, "absent": 0}
                cov = 0
                for q in n3q:
                    a = A.get((arm, q))
                    if not a or not a["ok"]:
                        continue
                    mk = marks.get(q, {}).get(sha_text(a["text"]))
                    if mk:
                        cov += 1
                        for x in mk:
                            c[x] += 1
                n = sum(c.values())
                tot[role] = {k: (v / n if n else None) for k, v in c.items()}
                o.put(f"N3.{p}.{role}.coverage", cov / len(n3q))
            for a in SM.ARMS:
                if a not in tot:
                    continue
                for k in ("present", "vague", "wrong"):
                    o.put(f"N3.{p}.{a}.{k}.g", tot[a][k])
                    o.put(f"N3.{p}.{a}.{k}.p", tot["plain"][k])
            for l in LANGS:
                ql_ = [q for q in n3q if _LANG_CACHE.get(q) == l]
                o.note(f"N3.{p}.{l}.present", {role: _present_share(marks, A, arm, ql_) for role, arm in arms.items()})
            if tot["plain"]["present"] is not None and tot["aa"]["present"] is not None:
                o.note(f"N3.{p}.aa_present_diff", tot["aa"]["present"] - tot["plain"]["present"])
    # N4: wrong claims and wrong corrections, web-checked.
    if L.get("n4") is not None:
        by = {}
        for r in L["n4"]:
            x = SM.parse_n4(r.get("raw"))
            if x:
                by[(r.get("qid"), r.get("answer_sha"))] = x
        for p, P in PLATFORMS.items():
            samp = "n4ds12" if p == "deepseek" else "n4gm12"
            qs = sample_ids[samp]
            for a in SM.ARMS:
                grav = P["base"] if a == "base" else cand_arms.get(p)
                if not grav:
                    continue
                for role, arm in (("g", grav), ("p", P["plain"])):
                    xs = [by.get((q, sha_text((A.get((arm, q)) or {}).get("text") or ""))) for q in qs]
                    xs = [x for x in xs if x]
                    o.put(f"N4.{p}.{a}.coverage.{role}", len(xs) / len(qs))
                    o.put(f"N4.{p}.{a}.wrong.{role}", float(np.mean([x["wrong_claims"] for x in xs])) if xs else None)
                    o.put(f"N4.{p}.{a}.wrong_corrections.{role}", float(np.mean([x["wrong_corrections"] for x in xs])) if xs else None)
    # A9: forced choice against Emily's seeds, with machine-translated controls.
    if L.get("native") is not None:
        Sx = {"native48": {"rows": jl(DATA / "samples" / "native48.jsonl") or []},
              "native_seeds": {"rows": jl(DATA / "samples" / "native_seeds.jsonl") or []},
              "native_control_sources": {"rows": jl(DATA / "samples" / "native_control_sources.jsonl") or []}}
        pairs = {x["id"]: x for x in SM.native_pairs(Sx, jl(DATA / "labels" / "native_controls.jsonl") or [])}
        res = {"test": [], "control": []}
        for r in L["native"]:
            x = pairs.get(r.get("id"))
            c = SM.parse_choice(r.get("raw"))
            if x and c:
                res[x["kind"]].append(c == x["human_side"])
        n_ctrl_exp = SM.NATIVE_CONTROLS * len(LANGS)
        o.put("A9.test_n", len(res["test"]))
        o.put("A9.test_accuracy", float(np.mean(res["test"])) if len(res["test"]) >= 0.9 * 48 else None)
        o.put("A9.control_accuracy", float(np.mean(res["control"])) if len(res["control"]) >= 0.9 * n_ctrl_exp else None)
    # Calibration on the new wording (cal0) and the blind critic.
    cal = [v for v in V if v["set"] == SM.CAL_SET]
    by_job = defaultdict(dict)
    for v in cal:
        by_job[v["job"]][v["judge"]] = v
    pairs = [(win_label(x["deepseek"]), win_label(x["claude"])) for x in by_job.values() if "deepseek" in x and "claude" in x]
    o.put("K0.n", len(pairs))
    o.put("K0.kappa", kappa(pairs) if len(pairs) >= 100 else None)
    gem = [(win_label(x["claude"]), win_label(x["gemini"])) for x in by_job.values() if "claude" in x and "gemini" in x]
    o.note("K0.claude_gemini_kappa", kappa(gem) if gem else None)
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
            v = judge.parse_verdict(r.get("raw"))
            x = by_job.get(r.get("job"), {}).get("claude")
            if v is None or x is None:
                continue
            w = {"A": x["left"], "B": x["right"], "TIE": None}[v]
            n += 1
            agree += w == x["winner"]
        o.put("K0.critic_n", n)
        o.put("K0.critic_agreement", agree / n if n >= 0.9 * SM.CRITIC_PER_TRAIT * len(TRAITS8) else None)


# ---------------------------------------------------------------------------------------- rule leak

def ngrams(text):
    t = text.lower()
    out = set()
    for run in re.findall(r"[぀-ヿ㐀-䶿一-鿿가-힯]+", t):
        out |= {run[i:i + 8] for i in range(len(run) - 7)}
    w = re.findall(r"[a-z0-9']+", t)
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

def measure_spend(o, ledger):
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
    o.put("D5.deepseek_usd", usd if found else None)
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
    # Rule-leak n-grams.
    assert "住房公积金管理" not in ngrams("住房公积金管理中心") and "住房公积金管理中" in ngrams("住房公积金管理中心")
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
