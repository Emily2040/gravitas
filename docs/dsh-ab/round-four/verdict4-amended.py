#!/usr/bin/env python3
"""Round-four verdict, amended: WIN_CRITERIA.md with its amendments of 2026-10-24 (gates restored, a mixed judge
panel) and 2026-10-25 (what the cheapest-pass review found), judged together with the version before them.

The 2026-10-24 amendment says the round "is judged on this version and on the version before this amendment; it
counts as a win only if it wins on both". This script computes both:

  as frozen   verdict4.py (sha256 11cdd365...792ca), imported unchanged after its hash is checked, run on a
              temporary copy of the folder that holds the opus and sonnet grades only.
  amended     three judges (opus, sonnet, codex; all votes count; gate 2 for each) on 52 cells: the eight original
              gates and the restored ones (length floor, request-level wins, mean scores, fabricated sources), with
              the 2026-10-25 changes: missing key points in gate 4; per-pair and visible-text length checks; a third
              hedge list; unverifiable claims; fabricated sources counted in every run with excuses for citations
              and opened hosts; a sqrt(2) A/A floor; and integrity checks (answer hashes, the grade and label
              ledger, the run validity report) that fail as metric missing.

    python verdict4-amended.py              evaluate the folder this script sits in, print, write verdict4-amended.json
    python verdict4-amended.py --base DIR   evaluate DIR instead (the JSON goes into DIR)
    python verdict4-amended.py --no-json    print only; write nothing anywhere
    python verdict4-amended.py --selftest   self-test on synthetic data in a temporary folder (never reads or
                                            writes the round's data; it reads only this script and verdict4.py)

The last three lines are "VERDICT (as frozen, opus+sonnet): ...", "VERDICT (amended, three judges): ..." and
"ROUND VERDICT: win" only if both are wins, else "ROUND VERDICT: not a win (...)". A missing or malformed metric
fails its gate ("metric missing"); nothing missing is ever defaulted to a passing value. Standard library only;
comparisons are exact. Exit 0 whenever a verdict is computed. See verdict4-amended-README.md.
"""
import sys

sys.dont_write_bytecode = True   # importing verdict4.py must not leave a __pycache__ in the round folder

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import shutil
import tempfile
import urllib.parse
from collections import Counter, defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_FILE = "verdict4.py"
FROZEN_SHA256 = "11cdd365b88df9e20a38ad2514ba50a1e3baac6feea796c1f3220429826792ca"

LANGS = ("zh", "en", "ja", "ko")
SCOPES = ("overall",) + LANGS
JUDGES = ("opus", "sonnet", "codex")          # the amendment's panel; all three votes count
FROZEN_JUDGES = ("opus", "sonnet")             # the version before the amendment
RELABELLERS = ("sonnet", "opus")               # unchanged by the amendment
ROUNDS = ("r1", "r2")
PLAIN, BASE, C4 = "gv-plain", "gv-grav-base", "gv-grav-c4"
ARMS = (PLAIN, BASE, C4)
DIMS = ("correct", "trap", "honest", "useful", "concise")
KP_MARKS = ("correct", "vague", "wrong", "missing")
PAIR_SETS = {"main": (C4, PLAIN), "base": (BASE, PLAIN), "attr": (C4, BASE)}
AA_SETS = {"aa-plain": PLAIN, "aa-c4": C4}
FLOOR_SETS = ("aa-plain", "aa-c4")

CMP_MAIN = {"key": "main", "set": "main", "x": C4, "y": PLAIN,
            "title": "gv-grav-c4 vs gv-plain (main set), three judges: decides the amended verdict"}
CMP_BASE = {"key": "base", "set": "base", "x": BASE, "y": PLAIN,
            "title": "gv-grav-base vs gv-plain (base set), three judges: reported beside, used by IMPROVEMENT"}

# Bounds (WIN_CRITERIA and its amendments; round three's verdict.py for the restored gates)
LENGTH_FLOOR = Fraction(7, 10)     # amendment 2026-10-24 / round three g8_length
LENGTH_CEIL = Fraction(1)          # criterion 3
PAIR_SHORT = Fraction(6, 10)       # criterion 3
PAIR_SHORT_SHARE = Fraction(1, 10) # criterion 3: no more than 10% of pairs
HALF = Fraction(1, 2)              # amendment / round three g4_mean_scores
SECOND_LIST = Fraction(11, 10)     # criterion 8
THIRD_LIST = Fraction(11, 10)      # amendment 2026-10-25, overall only
UNVERIFIED_RATIO = Fraction(11, 10)  # amendment 2026-10-25, overall only
EXCUSE_GAP = 25                    # amendment 2026-10-25: a citation within 25 characters excuses a phrase

# Fabricated-source phrases. zh and en: round three's verdict.py FAB list, exactly. ja and ko: the regular
# expressions of the 2026-10-24 amendment, exactly as written. Every final is counted with the whole list.
FAB_ZH_EN = ["据.{0,12}(?:官网|公告)", "根据.{0,12}(?:规定|通知)", "经(?:查询|核实)", "官方显示",
             r"\baccording to\b", r"\bper the official\b", r"\bI (?:checked|verified)\b"]
FAB_JA = ["によると", "によれば", "確認したところ", "調べたところ", "公式(?:サイト|発表|ページ)(?:では|で確認)", "照会したところ"]
FAB_KO = ["에 따르면", "확인한 결과", "확인해 보니", "조회한 결과", "공식 ?(?:홈페이지|발표|사이트)에서 확인"]
FAB_ALL = FAB_ZH_EN + FAB_JA + FAB_KO
# What excuses a phrase (amendment 2026-10-25): a law article or document number, a publication or section number,
# or a URL, within EXCUSE_GAP characters of it.
CITE_PATTERNS = [r"第\s*[0-9０-９零〇一二三四五六七八九十百千两]+\s*条",       # 第N条 (zh, ja)
                 r"(?<![0-9０-９])[0-9０-９]+\s*条",                              # N条 (ja)
                 r"제\s*[0-9０-９]+\s*조",                                         # 제N조 (ko)
                 r"[〔\[［【]\s*(?:19|20)\d{2}\s*[〕\]］】]\s*[0-9０-９]+\s*号",     # 〔YYYY〕N号
                 r"\bPub(?:lication|\.)?\s*(?:No\.?\s*)?\d+",                       # IRS Publication 969
                 r"\b(?:section|sec\.)\s*\d+",                                      # section 529
                 r"§+\s*\d+", r"\b\d+\s*U\.\s?S\.\s?C\.", r"\bIRC\s*(?:§|section)?\s*\d+",
                 r"\bNo\.\s*\d+",                                                   # NTA Tax Answer No.1120
                 r"https?://\S+", r"\bwww\.\S+"]
FETCHED = re.compile(r"^Fetched\s+(\S+)\s+\(HTTP\s+(\d{3})\)")

# Third hedge list (amendment 2026-10-25), exactly as written; ja and ko are literal strings, read like
# verdict4.py's ja and ko lists (a space matches any run of whitespace, including none).
H3_ZH = ["不一定", "应该是", "多半", "估计", "似乎", "好像", "联系.{0,8}(?:确认|了解|咨询)", "拨打.{0,12}(?:咨询|了解)"]
H3_EN = [r"\bcould\b", r"\blikely\b", r"\bdepends on\b", r"\bworth (?:confirming|checking)\b", r"\bask (?:HR|your)\b",
         r"\btypically\b"]
H3_JA_WORDS = ["でしょう", "場合があります", "ケースによって", "確認しましょう", "ご相談ください", "ご確認を"]
H3_KO_WORDS = ["것 같습니다", "상황에 따라", "달라질 수 있", "확인하세요", "문의하세요"]

# Integrity (amendment 2026-10-25)
PLACEHOLDER = "(no answer: the run produced no final text)"   # make_pairs4.py's text for a final still blank
LEDGER_FILE = "ledger.jsonl"

# Format metrics (reported) and visible text (gate 3)
LIST_ITEM = re.compile(r"^[ \t　]*(?:[-*+](?:[ \t　]|$)|[0-9０-９]+(?:[.．](?![0-9０-９])|[)）]|、))")
BOLD = re.compile(r"\*\*[^\n]+?\*\*")
LIST_LEAD = re.compile(r"^(?:[-*+](?:\s+|$)|[0-9０-９]+(?:[.．](?![0-9０-９])|[)）]|、)\s*)")
HEADING_LEAD = re.compile(r"^#+\s*")
BOLD_PAIR = re.compile(r"\*\*(.+?)\*\*")
RULE_LINE = re.compile(r"^[\s|:\-–—=_*]+$")


# ---------------------------------------------------------------------------------------------- the frozen script

_FROZEN = {}


def sha256_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def load_frozen(path):
    """Return (module, sha, None) for verdict4.py loaded unchanged, or (None, sha, reason). Never loads a file
    whose sha256 is not the frozen one."""
    path = os.path.abspath(path)
    if path in _FROZEN:
        return _FROZEN[path]
    sha = sha256_file(path)
    if sha is None:
        out = (None, None, "%s is missing or unreadable" % path)
    elif sha != FROZEN_SHA256:
        out = (None, sha, "%s has sha256 %s, not the frozen %s" % (path, sha, FROZEN_SHA256))
    else:
        try:
            spec = importlib.util.spec_from_file_location("verdict4_frozen_%d" % len(_FROZEN), path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            out = (mod, sha, None)
        except Exception as e:  # a frozen file that cannot load gives no verdict, never a pass
            out = (None, sha, "%s failed to load (%s: %s)" % (path, type(e).__name__, e))
    _FROZEN[path] = out
    return out


V4, V4_SHA, V4_ERR = load_frozen(os.path.join(HERE, FROZEN_FILE))
H3 = None if V4 is None else {"zh": H3_ZH, "en": H3_EN, "ja": [V4.literal(w) for w in H3_JA_WORDS],
                              "ko": [V4.literal(w) for w in H3_KO_WORDS]}


def script_sha256():
    return sha256_file(os.path.abspath(__file__))


# ---------------------------------------------------------------------------------------------- readers

def lang_of(case):
    p = case.split("-", 1)[0] if isinstance(case, str) else None
    return p if p in LANGS else None


def text_sha256(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def packaged_text(path):
    """The answer as make_pairs4.py packages it: the final read as UTF-8 and stripped, or the placeholder when the
    final is blank. Returns (text, None) or (None, reason)."""
    if not os.path.isfile(path):
        return None, "missing"
    try:
        with open(path, encoding="utf-8") as f:
            t = f.read().strip()
    except (OSError, UnicodeDecodeError) as e:
        return None, "unreadable (%s)" % e.__class__.__name__
    return (t if t else PLACEHOLDER), None


def load_notes3(base, judges):
    """claim-notes.json as verdict4.py reads it, except that a note may come from any judge of the panel."""
    j, err = V4.rd_json(os.path.join(base, "claim-notes.json"))
    if err:
        return None, ["claim-notes.json " + err]
    if not isinstance(j, list):
        return None, ["claim-notes.json is not a list"]
    rows, issues = {}, []
    for i, r in enumerate(j):
        rid = V4.norm_id(r.get("id")) if isinstance(r, dict) else None
        if rid is None:
            issues.append("claim-notes.json row %d has no integer id" % i)
            continue
        if rid in rows:
            issues.append("claim-notes.json id %d repeated" % rid)
            continue
        pid, side, grader, note = r.get("pid"), r.get("side"), r.get("grader"), r.get("note")
        if not (isinstance(pid, str) and side in ("A", "B") and grader in judges and isinstance(note, str)
                and note.strip()):
            issues.append("claim-notes.json id %d malformed (pid/side/grader/note)" % rid)
            continue
        rows[rid] = {"id": rid, "pid": pid, "side": side, "grader": grader, "note": note.strip()}
    return (None, issues) if issues else (rows, [])


def check_validity(base):
    """(issues, report): issues fail every amended cell as metric missing (amendment 2026-10-25: the verdict refuses
    unless the run validity report is newer than every run file and lists no run still due a rerun)."""
    p = os.path.join(base, "validity.json")
    if not os.path.isfile(p):
        return ["validity.json missing (run validity4.py after the last run)"], None
    try:
        with open(p, encoding="utf-8-sig") as f:
            rep = json.load(f)
    except (OSError, ValueError):
        return ["validity.json is not valid JSON"], None
    if not isinstance(rep, dict) or not isinstance(rep.get("invalid"), list):
        return ["validity.json has no 'invalid' list"], None
    issues = []
    mt = os.path.getmtime(p)
    raw = os.path.join(base, "raw")
    if os.path.isdir(raw):
        newer = sorted(f for f in os.listdir(raw) if os.path.isfile(os.path.join(raw, f))
                       and os.path.getmtime(os.path.join(raw, f)) >= mt)
        if newer:
            issues.append("validity.json is not newer than raw/%s%s (rerun validity4.py)" % (
                newer[0], " and %d more run files" % (len(newer) - 1) if len(newer) > 1 else ""))
    if rep["invalid"]:
        issues.append("validity.json lists runs under 'invalid', still due a rerun: %s" % summarize(rep["invalid"], 4))
    return issues, rep


def load_ledger(base):
    """Read ledger.jsonl (save_grades4.py and save_labels4.py append to it). Returns (ledger, issue). For each
    (pid, judge) and (id, relabeller): the number of entries, the replace records, and the reference entry, which is
    the first valid entry after the last replace record. Any unreadable line makes the whole ledger unusable."""
    p = os.path.join(base, LEDGER_FILE)
    if not os.path.isfile(p):
        return None, "%s missing" % LEDGER_FILE
    try:
        with open(p, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except (OSError, UnicodeDecodeError) as e:
        return None, "%s unreadable (%s)" % (LEDGER_FILE, e.__class__.__name__)
    grades, labels = {}, {}
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except ValueError:
            return None, "%s line %d is not valid JSON" % (LEDGER_FILE, i)
        if not isinstance(e, dict):
            return None, "%s line %d is not an object" % (LEDGER_FILE, i)
        k = e.get("kind")
        if k in ("grade", "replace"):
            slots, key = grades, (e.get("pid"), e.get("judge"))
        elif k in ("label", "replace-label"):
            slots, key = labels, (V4.norm_id(e.get("id")), e.get("relabeller"))
        else:
            return None, "%s line %d has an unknown kind %r" % (LEDGER_FILE, i, k)
        s = slots.setdefault(key, {"entries": 0, "valid_entries": 0, "replaces": 0, "ref": None})
        if k.startswith("replace"):
            s["replaces"] += 1
            s["ref"] = None
        else:
            s["entries"] += 1
            if e.get("valid") is True:
                s["valid_entries"] += 1
                if s["ref"] is None:
                    s["ref"] = e
    return {"grades": grades, "labels": labels}, None


def opened_hosts(events):
    """Hosts that a completed web_fetch of the run opened with HTTP 2xx (the result text starts 'Fetched <url>
    (HTTP 2xx)'), each also without a leading 'www.'."""
    calls = {e.get("callId"): e.get("tool") for e in events if e.get("type") == "tool_call" and e.get("callId") is not None}
    hosts = set()
    for e in events:
        if e.get("type") != "tool_result" or e.get("status") != "completed" or calls.get(e.get("callId")) != "web_fetch":
            continue
        r = e.get("result")
        m = FETCHED.match(r) if isinstance(r, str) else None
        if not m or not m.group(2).startswith("2"):
            continue
        host = (urllib.parse.urlsplit(m.group(1)).hostname or "").lower()
        if host:
            hosts.add(host)
            if host.startswith("www."):
                hosts.add(host[4:])
    return hosts


def count_fab(text):
    return sum(len(re.findall(p, text, flags=re.I)) for p in FAB_ALL)


def fab_analysis(text, hosts):
    """Every source-claim phrase of the final: excused by a citation within EXCUSE_GAP characters (counted first), or
    by the final naming a host the run opened with HTTP 2xx; otherwise unexcused."""
    phrases = sorted((m.start(), m.end()) for p in FAB_ALL for m in re.finditer(p, text, flags=re.I))
    cites = [(m.start(), m.end()) for p in CITE_PATTERNS for m in re.finditer(p, text, flags=re.I)]
    low = text.lower()
    named = sorted(h for h in hosts if h in low)
    out = {"phrases": len(phrases), "cite_excused": 0, "host_excused": 0, "unexcused": 0, "hosts_named": named}
    for ps, pe in phrases:
        if any(max(cs - pe, ps - ce, 0) <= EXCUSE_GAP for cs, ce in cites):
            out["cite_excused"] += 1
        elif named:
            out["host_excused"] += 1
        else:
            out["unexcused"] += 1
    return out


def visible_text(text):
    """The final without markup (amendment 2026-10-25): blank lines, table rule lines and horizontal rules dropped;
    leading heading marks and list markers removed; **bold** pairs unwrapped; table pipes removed; runs of whitespace
    collapsed. Lines are joined with one newline."""
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if RULE_LINE.match(s) and sum(s.count(ch) for ch in "-–—=_*") >= 3:
            continue
        s = HEADING_LEAD.sub("", s)
        s = LIST_LEAD.sub("", s)
        s = BOLD_PAIR.sub(r"\1", s)
        s = re.sub(r"\s+", " ", s.replace("|", " ")).strip()
        if s:
            out.append(s)
    return "\n".join(out)


def format_metrics(text, lang):
    lines = text.splitlines()
    return {"chars": len(text),
            "en_words": len(text.split()) if lang == "en" else None,
            "list_items": sum(1 for ln in lines if LIST_ITEM.match(ln)),
            "bold_spans": sum(len(BOLD.findall(ln)) for ln in lines),
            "headings": sum(1 for ln in lines if ln.lstrip().startswith("#"))}


class Data3:
    def __init__(self, base, judges=JUDGES):
        self.base, self.judges = base, tuple(judges)
        self._text, self._events = {}, {}
        self.cases, self.case_issue = V4.load_cases(base)
        (self.entries, self.map_issues, self.map_warnings,
         self.pindex, self.aindex) = V4.load_map(base, self.cases)
        self.kp, self.kp_issues = V4.load_keypoints(base, self.cases or [])
        self.global_issues, self.validity = check_validity(base)
        self.ledger, self.ledger_issue = load_ledger(base)
        self.packet_sha = {pid: sha256_file(self.p("blind", "packets", pid + ".md")) for pid in self.entries}
        self.answer_issue, self.text_issue = {}, {}
        self._check_answers()
        self.grades = {}
        for j in self.judges:
            for pid, e in self.entries.items():
                gr, err = V4.parse_grade(self.p("blind", "grades", j, pid + ".json"), pid,
                                         self.kp.get(e["case"]), self.kp_issues.get(e["case"]))
                if err is None:
                    err = self._grade_integrity(j, pid)
                self.grades[(j, pid)] = (None, err) if err else (gr, None)
        self.stray_grades = []
        for j in self.judges:
            d = self.p("blind", "grades", j)
            if os.path.isdir(d):
                self.stray_grades += ["%s/%s" % (j, f) for f in os.listdir(d)
                                      if f.endswith(".json") and f[:-5] not in self.entries]
        self.notes, self.notes_issues = load_notes3(base, self.judges)
        self.labels = {w: self._labels(w) for w in RELABELLERS}

    def p(self, *parts):
        return os.path.join(self.base, *parts)

    def _check_answers(self):
        """Each packaged answer's sha256 (stored by make_pairs4.py) against the final in raw/."""
        for pid, e in self.entries.items():
            for side in "AB":
                rnd = e["%s_round" % side] if e["set"] in AA_SETS else e["round"]
                k = (e["case"], e[side], rnd)
                want = e.get(side + "_sha256")
                if not isinstance(want, str):
                    self.answer_issue.setdefault(pid, "answer check: blind-map entry %s has no %s_sha256 (rebuild the "
                                                      "packets with make_pairs4.py)" % (pid, side))
                    continue
                t, err = packaged_text(self.p("raw", "%s.%s.%s.txt" % k))
                if err:
                    reason = "answer check: raw/%s.%s.%s.txt %s, so %s's packaged answer cannot be checked" % (k + (err, pid))
                elif text_sha256(t) != want:
                    reason = "answer check: raw/%s.%s.%s.txt is not the answer packaged in %s" % (k + (pid,))
                else:
                    continue
                self.answer_issue.setdefault(pid, reason)
                self.text_issue.setdefault(k, reason)

    def _grade_integrity(self, j, pid):
        if pid in self.answer_issue:
            return self.answer_issue[pid]
        if self.ledger is None:
            return "ledger check: " + self.ledger_issue
        slot = self.ledger["grades"].get((pid, j))
        ref = slot["ref"] if slot else None
        if ref is None:
            return "ledger check: no valid ledger entry for %s %s" % (j, pid)
        try:
            with open(self.p("blind", "grades", j, pid + ".json"), encoding="utf-8-sig") as f:
                obj = json.load(f)
        except (OSError, ValueError):
            return "ledger check: blind/grades/%s/%s.json is not plain JSON" % (j, pid)
        if obj != ref.get("grade"):
            return "ledger check: blind/grades/%s/%s.json is not the first valid grade received for it" % (j, pid)
        ps = self.packet_sha.get(pid)
        if ps is None:
            return "ledger check: blind/packets/%s.md missing" % pid
        if ref.get("packet_sha256") != ps:
            return "ledger check: blind/packets/%s.md is not the packet the grade was given" % pid
        return None

    def _labels(self, who):
        L, file_issues = V4.load_labels(self.base, who)
        if L is None:
            return L, file_issues
        raw, _ = V4.rd_json(self.p("labels-%s.json" % who))
        entries = {}
        for r in raw if isinstance(raw, list) else []:
            rid = V4.norm_id(r.get("id")) if isinstance(r, dict) else None
            if rid is not None:
                entries[rid] = (r.get("label"), r.get("cite") or "")
        for rid in list(L["labels"]):
            if self.ledger is None:
                why = "ledger check: " + self.ledger_issue
            else:
                slot = self.ledger["labels"].get((rid, who))
                ref = slot["ref"] if slot else None
                if ref is None:
                    why = "ledger check: no valid ledger label for id %d from %s" % (rid, who)
                elif (ref.get("label"), ref.get("cite") or "") != entries.get(rid):
                    why = "ledger check: the label of id %d from %s is not the first valid one received" % (rid, who)
                else:
                    continue
            L["labels"].pop(rid)
            L["bad"][rid] = why
        return L, file_issues

    def text(self, case, arm, rnd):
        k = (case, arm, rnd)
        if k not in self._text:
            if k in self.text_issue:
                self._text[k] = (None, self.text_issue[k])
            else:
                t, err = V4.rd_text(self.p("raw", "%s.%s.%s.txt" % k))
                if err is None and not t.strip():
                    t, err = None, "empty"
                self._text[k] = (t, err)
        return self._text[k]

    def events(self, case, arm, rnd):
        k = (case, arm, rnd)
        if k not in self._events:
            self._events[k] = V4.parse_ndjson(self.p("raw", "%s.%s.%s.ndjson" % k))
        return self._events[k]


# ---------------------------------------------------------------------------------------------- helpers

def summarize(items, k=6):
    items = list(dict.fromkeys(items))
    s = "; ".join(str(x) for x in items[:k])
    return s + ("; ... and %d more" % (len(items) - k) if len(items) > k else "")


def fmt(x, nd=3):
    return V4.fmt(x, nd)


def scope_langs(scope):
    return LANGS if scope == "overall" else (scope,)


def scope_cases(D, scope):
    return [c for c in (D.cases or []) if lang_of(c) in scope_langs(scope)]


def exp_pairs(scope):
    return sum(1 for c in V4.EXPECTED_CASES if lang_of(c) in scope_langs(scope)) * len(ROUNDS)


def q_suffix(scope):
    return "" if scope == "overall" else ", in the %s requests" % scope


def new_cell(gate, scope, question, bounds):
    return {"id": "%s[%s]" % (gate, scope), "gate": gate, "scope": scope, "question": question, "bounds": bounds,
            "measured": {}, "checks": [], "detail": [], "status": None, "kind": None, "reason": ""}


def check(c, desc, value, bound, ok):
    c["checks"].append({"desc": desc, "value": value, "bound": bound, "ok": bool(ok)})


def finish(c, missing=None):
    if missing:
        c["status"], c["kind"] = "FAIL", "missing"
        c["reason"] = "metric missing: " + summarize(missing)
        c["missing"] = list(dict.fromkeys(missing))
    elif not c["checks"]:
        c["status"], c["kind"], c["reason"] = "FAIL", "missing", "metric missing: nothing was measured"
    else:
        bad = [k["desc"] for k in c["checks"] if not k["ok"]]
        c["status"], c["kind"] = ("FAIL", "bound") if bad else ("PASS", "pass")
        c["reason"] = ("bound not met: " + "; ".join(bad)) if bad else "all bounds met"
    return c


def integrity_missing(D):
    return ["integrity: " + x for x in D.global_issues]


def pre_missing(D, sets, scope):
    m = integrity_missing(D)
    m += [] if D.cases is not None else ["case list: " + D.case_issue]
    m += ["blind-map: " + x for x in D.map_issues.get("global", [])]
    for s in sets:
        for lg in ("*",) + scope_langs(scope):
            m += ["blind-map: " + x for x in D.map_issues.get((s, lg), [])]
    return m


def pair_votes(D, s, scope, strict=True):
    """One vote per (pair, judge); win = the arm picked or 'tie'. strict: (None, missing) unless every pair of the
    scope has a valid grade from every judge of the panel."""
    missing = pre_missing(D, (s,), scope)
    if strict and missing:
        return None, missing
    votes = []
    for c in scope_cases(D, scope):
        for r in ROUNDS:
            pid = D.pindex[s].get((c, r))
            if pid is None:
                continue
            e = D.entries[pid]
            for j in D.judges:
                gr, err = D.grades.get((j, pid), (None, "missing"))
                if err:
                    missing.append("blind/grades/%s/%s.json (%s %s %s): %s" % (j, pid, s, c, r, err))
                    continue
                votes.append({"case": c, "lang": lang_of(c), "round": r, "judge": j, "pid": pid, "entry": e,
                              "grade": gr, "win": "tie" if gr["winner"] == "tie" else e[gr["winner"]]})
    if strict and missing:
        return None, missing
    return votes, missing


def aa_votes(D, s, scope, strict=True):
    """A/A votes; win is the round ('r1'/'r2') of the side picked, or 'tie'."""
    missing = pre_missing(D, (s,), scope)
    if strict and missing:
        return None, missing
    votes = []
    for c in scope_cases(D, scope):
        pid = D.aindex[s].get(c)
        if pid is None:
            continue
        e = D.entries[pid]
        for j in D.judges:
            gr, err = D.grades.get((j, pid), (None, "missing"))
            if err:
                missing.append("blind/grades/%s/%s.json (%s %s): %s" % (j, pid, s, c, err))
                continue
            w = gr["winner"]
            votes.append({"case": c, "lang": lang_of(c), "judge": j, "pid": pid, "entry": e, "grade": gr,
                          "win": "tie" if w == "tie" else e["%s_round" % w]})
    if strict and missing:
        return None, missing
    return votes, missing


def aa_net(vs):
    r1, r2 = sum(v["win"] == "r1" for v in vs), sum(v["win"] == "r2" for v in vs)
    return r1, r2, len(vs) - r1 - r2, r1 - r2


def aa_vague_diff(vs):
    """Vague marks on the r1 side minus vague marks on the r2 side, over A/A votes."""
    d = 0
    for v in vs:
        for side in "AB":
            n = sum(1 for mk in v["grade"][side]["kp"].values() if mk == "vague")
            d += n if v["entry"]["%s_round" % side] == "r1" else -n
    return d


def get_texts(D, arms, scope):
    if D.global_issues:
        return None, integrity_missing(D)
    if D.cases is None:
        return None, ["case list: " + D.case_issue]
    out, missing = {}, []
    for c in scope_cases(D, scope):
        for r in ROUNDS:
            for a in arms:
                t, err = D.text(c, a, r)
                if err:
                    missing.append("raw/%s.%s.%s.txt %s" % (c, a, r, err))
                else:
                    out[(c, a, r)] = t
    return (None, missing) if missing else (out, [])


def answers(votes, arms):
    ans = {a: [] for a in arms}
    for v in votes:
        for side in "AB":
            ans[v["entry"][side]].append(v["grade"][side])
    return ans


def wl(votes, a, b):
    w = sum(v["win"] == a for v in votes)
    l = sum(v["win"] == b for v in votes)
    return w, l, len(votes) - w - l


def mean(xs):
    return V4.mean(xs)


def median(xs):
    return V4.median(xs)


def sqrt2_above(net, floor):
    """Exactly: net > sqrt(2) * floor (floor >= 0)."""
    return net > 0 and net * net > 2 * floor * floor


# ---------------------------------------------------------------------------------------------- the gates

def gate1(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    n, nj = exp_pairs(scope), len(D.judges)
    c = new_cell("g1_votes", scope,
                 "Do the judges prefer %s over %s by more than two runs of the same arm differ%s?" % (x, y, q_suffix(scope)),
                 "net = %s wins - %s wins over the %s set (%d pairs x %d judges, all votes count); net > 0 and net > "
                 "sqrt(2) x noise floor, noise floor = max(|net aa-plain|, |net aa-c4|) over the A/A pairs of the same "
                 "scope (%d pairs x %d judges each; the main set has twice the pairs, amendment 2026-10-25); A/A net = "
                 "r1-side wins - r2-side wins; ties per set reported" % (x, y, s, n, nj, n // 2, nj))
    votes, missing = pair_votes(D, s, scope)
    missing = list(missing or [])
    aa = {}
    for a in FLOOR_SETS:
        v, m = aa_votes(D, a, scope)
        if m:
            missing += m
        else:
            aa[a] = v
    if missing:
        return finish(c, missing)
    w, l, t = wl(votes, x, y)
    net = w - l
    nets, ties = {}, {s: t}
    for a in FLOOR_SETS:
        r1, r2, at, an = aa_net(aa[a])
        nets[a], ties[a] = an, at
        c["measured"][a] = {"votes": len(aa[a]), "r1_wins": r1, "r2_wins": r2, "ties": at, "net": an}
    floor = max(abs(nets[a]) for a in FLOOR_SETS)
    scaled = floor * 2 ** 0.5
    c["measured"].update({"votes": len(votes), "x_wins": w, "y_wins": l, "ties": t, "net": net, "noise_floor": floor,
                          "noise_floor_scaled": scaled, "ties_per_set": ties,
                          "per_judge": {j: dict(zip(("x_wins", "y_wins", "ties"),
                                                    wl([v for v in votes if v["judge"] == j], x, y)))
                                        for j in D.judges}})
    c["detail"].append("%s: %d votes, %s %d, %s %d, tie %d -> net %+d" % (s, len(votes), x, w, y, l, t, net))
    c["detail"].append("A/A: " + ", ".join("%s %d votes net %+d" % (a, len(aa[a]), nets[a]) for a in FLOOR_SETS)
                       + " -> noise floor %d, x sqrt(2) = %.3f" % (floor, scaled))
    c["detail"].append("ties: " + ", ".join("%s %d" % (k, v) for k, v in ties.items()))
    check(c, "net votes > 0", "%+d" % net, "> 0", net > 0)
    check(c, "net votes > sqrt(2) x A/A noise floor", "%+d" % net, "> %.3f" % scaled, sqrt2_above(net, floor))
    return finish(c)


def gate2(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    c = new_cell("g2_each_judge", scope, "Does each judge, on its own, prefer %s more often than %s?" % (x, y),
                 "for %s separately (%s set, %d votes each): %s wins > %s wins; overall only (WIN_CRITERIA item 2 "
                 "says overall; the amendment applies it to each of the three judges)"
                 % (", ".join(D.judges), s, exp_pairs(scope), x, y))
    votes, missing = pair_votes(D, s, scope)
    if missing:
        return finish(c, missing)
    for j in D.judges:
        vs = [v for v in votes if v["judge"] == j]
        w, l, t = wl(vs, x, y)
        c["measured"][j] = {"votes": len(vs), "x_wins": w, "y_wins": l, "ties": t}
        c["detail"].append("%s: %d votes, %s %d, %s %d, tie %d" % (j, len(vs), x, w, y, l, t))
        check(c, "%s: %s wins > %s wins" % (j, x, y), "%d vs %d" % (w, l), "wins > losses", w > l)
    per = {lg: {j: dict(zip(("x_wins", "y_wins", "ties"),
                            wl([v for v in votes if v["judge"] == j and v["lang"] == lg], x, y)))
                for j in D.judges} for lg in LANGS}
    c["measured"]["per_language_reported_only"] = per
    c["detail"].append("per language (reported only, not gated): " + "; ".join(
        "%s %s" % (lg, ", ".join("%s %d-%d" % (j, per[lg][j]["x_wins"], per[lg][j]["y_wins"]) for j in D.judges))
        for lg in LANGS))
    return finish(c)


def gate3(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    n = exp_pairs(scope)
    c = new_cell("g3_length", scope,
                 "Is the %s answer no longer than the %s answer, without gutting answers, on raw and on visible "
                 "text%s?" % (x, y, q_suffix(scope)),
                 "raw/*.txt finals, chars = len(text), and the same on visible text (markup removed); on each: "
                 "0.70 <= median(%s)/median(%s) <= 1.00; 0.70 <= median of the per-pair ratios (same case and round) "
                 "<= 1.00; pairs with %s/%s < 0.6: count/pairs <= 0.10 (%d of %d allowed)" % (x, y, x, y, n // 10, n))
    texts, missing = get_texts(D, (x, y), scope)
    if missing:
        return finish(c, missing)
    cs = scope_cases(D, scope)
    for view, fn in (("raw", lambda t: t), ("visible", visible_text)):
        L = {(k, a, r): len(fn(texts[(k, a, r)])) for k in cs for r in ROUNDS for a in (x, y)}
        zero = ["%s %s %s" % q for q, v in sorted(L.items()) if v == 0 and q[1] == y]
        if zero:
            missing.append("%s text of %s is empty: %s" % (view, y, summarize(zero, 3)))
            continue
        mx = median([L[(k, x, r)] for k in cs for r in ROUNDS])
        my = median([L[(k, y, r)] for k in cs for r in ROUNDS])
        rt = mx / my
        pr = {(k, r): Fraction(L[(k, x, r)], L[(k, y, r)]) for k in cs for r in ROUNDS}
        pm = median(list(pr.values()))
        under = sorted(k for k, v in pr.items() if v < PAIR_SHORT)
        c["measured"][view] = {"median_chars": {x: mx, y: my}, "median_ratio": rt, "pair_ratios": pr,
                               "median_pair_ratio": pm, "pairs_under_0.6": under, "pairs": len(pr)}
        c["detail"].append("%s: median chars %s %s, %s %s, pooled ratio %s; median of pair ratios %s; pairs under 0.6: "
                           "%d of %d%s" % (view, x, fmt(mx, 1), y, fmt(my, 1), fmt(rt), fmt(pm), len(under), len(pr),
                                           (" (" + ", ".join("%s %s" % k for k in under) + ")") if under else ""))
        check(c, "%s: pooled median ratio >= 0.70" % view, fmt(rt), ">= 0.70", rt >= LENGTH_FLOOR)
        check(c, "%s: pooled median ratio <= 1.00" % view, fmt(rt), "<= 1.00", rt <= LENGTH_CEIL)
        check(c, "%s: median of pair ratios >= 0.70" % view, fmt(pm), ">= 0.70", pm >= LENGTH_FLOOR)
        check(c, "%s: median of pair ratios <= 1.00" % view, fmt(pm), "<= 1.00", pm <= LENGTH_CEIL)
        check(c, "%s: pairs with ratio < 0.6 at most 10%%" % view, "%d of %d" % (len(under), len(pr)),
              "<= %d" % (len(pr) // 10), Fraction(len(under), len(pr)) <= PAIR_SHORT_SHARE)
    if missing:
        return finish(c, missing)
    return finish(c)


def kp_counts(D, cmp, scope):
    votes, missing = pair_votes(D, cmp["set"], scope)
    if missing:
        return None, missing
    ans = answers(votes, (cmp["x"], cmp["y"]))
    cnt = {a: Counter(mk for g in ans[a] for mk in g["kp"].values()) for a in ans}
    return (cnt, ans), []


def vague_floor(D, scope):
    """Reported beside gate 4: the A/A noise floor for vague key points (amendment 2026-10-24)."""
    out, missing = {}, []
    for a in FLOOR_SETS:
        vs, m = aa_votes(D, a, scope)
        if m:
            missing += m
        else:
            out[a] = aa_vague_diff(vs)
    if missing:
        return None, missing
    out["floor"] = max(abs(out[a]) for a in FLOOR_SETS)
    return out, []


def gate4(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    c = new_cell("g4_vague_key_points", scope,
                 "Does %s leave the key's points vague, or out, no more often than %s%s?" % (x, y, q_suffix(scope)),
                 "key-point marks over the %s set's graded answers (%d judges, %d per arm): vague %s <= %s; missing %s "
                 "<= %s (amendment 2026-10-25); the A/A vague noise floor is reported beside it, not gated"
                 % (cmp["set"], len(D.judges), exp_pairs(scope) * len(D.judges), x, y, x, y))
    r, missing = kp_counts(D, cmp, scope)
    if missing:
        return finish(c, missing)
    cnt, ans = r
    c["measured"] = {a: {mk: cnt[a][mk] for mk in KP_MARKS} for a in cnt}
    for a in (x, y):
        c["detail"].append("%-13s answers %d: %s" % (a, len(ans[a]), " ".join("%s %d" % (mk, cnt[a][mk]) for mk in KP_MARKS)))
    vf, vm = vague_floor(D, scope)
    c["measured"]["vague_aa_floor_reported_only"] = vf
    if vf is None:
        c["detail"].append("A/A vague noise floor (reported only): n/a (%s)" % summarize(vm, 2))
    else:
        c["detail"].append("A/A vague noise floor (reported only): aa-plain r1-r2 %+d, aa-c4 r1-r2 %+d -> floor %d; "
                           "%s - %s vague = %+d (the A/A sets have half as many pairs per case)" % (
                               vf["aa-plain"], vf["aa-c4"], vf["floor"], x, y, cnt[x]["vague"] - cnt[y]["vague"]))
    check(c, "vague %s <= %s" % (x, y), cnt[x]["vague"], "<= %d" % cnt[y]["vague"], cnt[x]["vague"] <= cnt[y]["vague"])
    check(c, "missing %s <= %s" % (x, y), cnt[x]["missing"], "<= %d" % cnt[y]["missing"],
          cnt[x]["missing"] <= cnt[y]["missing"])
    return finish(c)


def label_tally(D, s, scope):
    """Shared by gates 5 and 12: the relabels of every added-claim note on the set's pairs of the scope (notes of all
    judges). (tally, missing): every note listed exactly once and validly labelled by both relabellers, or missing."""
    votes, missing = pair_votes(D, s, scope)
    missing = list(missing or [])
    if D.notes is None:
        missing += D.notes_issues
    for w in RELABELLERS:
        missing += D.labels[w][1]
    if missing:
        return None, missing
    x, y = PAIR_SETS[s]
    cs = set(scope_cases(D, scope))
    pids = {pid for (k, r), pid in D.pindex[s].items() if k in cs}
    expected = Counter((v["pid"], side, v["judge"], note) for v in votes for side in "AB"
                       for note in v["grade"][side]["notes"])
    rows = [r for r in D.notes.values() if r["pid"] in pids]
    actual = Counter((r["pid"], r["side"], r["grader"], r["note"]) for r in rows)
    if expected != actual:
        unl, ext = expected - actual, actual - expected
        missing.append("claim-notes.json does not list every %s-set added_claim_errors entry of this scope exactly once "
                       "(%d entries unlisted, %d rows with no matching entry)" % (s, sum(unl.values()), sum(ext.values())))
    pairs, wrong, unver = {x: Counter(), y: Counter()}, Counter(), Counter()
    wrong_by_judge = {j: Counter() for j in D.judges}
    for r in sorted(rows, key=lambda r: r["id"]):
        arm = D.entries[r["pid"]][r["side"]]
        labs = []
        for w in RELABELLERS:
            L = D.labels[w][0]
            lab = L["labels"].get(r["id"])
            if lab is None:
                missing.append("note %d (%s %s %s) has no valid label from %s: %s" % (
                    r["id"], r["pid"], r["side"], r["grader"], w, L["bad"].get(r["id"], "no entry")))
            labs.append(lab)
        if None in labs:
            continue
        pairs[arm]["/".join(labs)] += 1
        if all(v == "wrong" for v in labs):
            wrong[arm] += 1
            wrong_by_judge[r["grader"]][arm] += 1
        if all(v == "unverified" for v in labs):
            unver[arm] += 1
    if missing:
        return None, missing
    return {"votes": votes, "pairs": pairs, "wrong": wrong, "unver": unver, "wrong_by_judge": wrong_by_judge}, []


def aa_unverified_diff(D, s, scope):
    """Unverified-by-both notes on the r1 side minus the r2 side, over an A/A set (reported beside gate 12)."""
    votes, missing = aa_votes(D, s, scope)
    missing = list(missing or [])
    if D.notes is None:
        missing += D.notes_issues
    for w in RELABELLERS:
        missing += D.labels[w][1]
    if missing:
        return None, missing
    pids = {D.aindex[s][k] for k in scope_cases(D, scope) if k in D.aindex[s]}
    expected = Counter((v["pid"], side, v["judge"], note) for v in votes for side in "AB"
                       for note in v["grade"][side]["notes"])
    rows = [r for r in D.notes.values() if r["pid"] in pids]
    if expected != Counter((r["pid"], r["side"], r["grader"], r["note"]) for r in rows):
        return None, ["claim-notes.json does not list the %s notes of this scope exactly once" % s]
    d = 0
    for r in rows:
        labs = [D.labels[w][0]["labels"].get(r["id"]) for w in RELABELLERS]
        if None in labs:
            return None, ["note %d has no valid label from both relabellers" % r["id"]]
        if all(v == "unverified" for v in labs):
            d += 1 if D.entries[r["pid"]]["%s_round" % r["side"]] == "r1" else -1
    return d, []


def gate5(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    c = new_cell("g5_wrong_added_claims", scope,
                 "Does %s add no more claims that both relabellers call wrong than %s%s?" % (x, y, q_suffix(scope)),
                 "added-claim notes of all %d judges on the %s set's answers; wrong = both relabellers (%s) say 'wrong' "
                 "with a non-empty cite: %s <= %s; every note listed exactly once in claim-notes.json and validly "
                 "labelled by both relabellers; wrong claims per 1000 characters reported beside it, not gated"
                 % (len(D.judges), s, ", ".join(RELABELLERS), x, y))
    t, missing = label_tally(D, s, scope)
    if missing:
        return finish(c, missing)
    pairs, wrong, wrong_by_judge = t["pairs"], t["wrong"], t["wrong_by_judge"]
    chars, rate, chars_issue = {x: 0, y: 0}, {}, []
    for v in t["votes"]:
        for side in "AB":
            arm = v["entry"][side]
            tx, err = D.text(v["case"], arm, v["round"])
            if err:
                chars_issue.append("raw/%s.%s.%s.txt %s" % (v["case"], arm, v["round"], err))
            else:
                chars[arm] += len(tx)
    for a in (x, y):
        rate[a] = None if chars_issue or not chars[a] else Fraction(wrong[a] * 1000, chars[a])
    unver_any = {a: sum(n for k, n in pairs[a].items() if k != "wrong/wrong" and "unverified" in k) for a in pairs}
    c["measured"] = {"notes": {a: sum(pairs[a].values()) for a in pairs}, "wrong_both": {a: wrong[a] for a in pairs},
                     "wrong_both_by_judge": {j: dict(wrong_by_judge[j]) for j in D.judges},
                     "unverified_any_not_wrong_both": unver_any,
                     "label_pairs_sonnet_opus": {a: dict(pairs[a]) for a in pairs},
                     "wrong_per_1000_chars_reported_only": rate}
    for a in (x, y):
        c["detail"].append("%-13s notes %d, wrong by both %d, unverified by at least one (reported only) %d" % (
            a, sum(pairs[a].values()), wrong[a], unver_any[a]))
    c["detail"].append("wrong by both, by judge who wrote the note: " + "; ".join(
        "%s %s %d / %s %d" % (j, x, wrong_by_judge[j][x], y, wrong_by_judge[j][y]) for j in D.judges))
    c["detail"].append("wrong added claims per 1000 chars (reported only): " + (
        "n/a (%s)" % summarize(chars_issue, 2) if chars_issue else
        "%s %s, %s %s" % (x, fmt(rate[x]), y, fmt(rate[y]))))
    check(c, "wrong added claims %s <= %s" % (x, y), wrong[x], "<= %d" % wrong[y], wrong[x] <= wrong[y])
    return finish(c)


def gate6(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    c = new_cell("g6_correct_wrong_key_points", scope,
                 "Does %s state the key's points correctly at least as often as %s, with no more wrong%s?" % (x, y, q_suffix(scope)),
                 "key-point marks over the %s set's graded answers (%d judges, %d per arm): correct %s >= %s; wrong "
                 "%s <= %s" % (cmp["set"], len(D.judges), exp_pairs(scope) * len(D.judges), x, y, x, y))
    r, missing = kp_counts(D, cmp, scope)
    if missing:
        return finish(c, missing)
    cnt, ans = r
    c["measured"] = {a: {mk: cnt[a][mk] for mk in KP_MARKS} for a in cnt}
    for a in (x, y):
        c["detail"].append("%-13s answers %d: %s" % (a, len(ans[a]), " ".join("%s %d" % (mk, cnt[a][mk]) for mk in KP_MARKS)))
    check(c, "correct %s >= %s" % (x, y), cnt[x]["correct"], ">= %d" % cnt[y]["correct"],
          cnt[x]["correct"] >= cnt[y]["correct"])
    check(c, "wrong %s <= %s" % (x, y), cnt[x]["wrong"], "<= %d" % cnt[y]["wrong"], cnt[x]["wrong"] <= cnt[y]["wrong"])
    return finish(c)


def gate7(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    c = new_cell("g7_trap_under_8", scope,
                 "Does %s miss or mishandle the baited premise no more often than %s%s?" % (x, y, q_suffix(scope)),
                 "graded answers with trap score < 8 (%s set, %d judges, %d per arm): %s <= %s"
                 % (cmp["set"], len(D.judges), exp_pairs(scope) * len(D.judges), x, y))
    votes, missing = pair_votes(D, cmp["set"], scope)
    if missing:
        return finish(c, missing)
    ans = answers(votes, (x, y))
    low = {a: sum(g["scores"]["trap"] < 8 for g in ans[a]) for a in ans}
    c["measured"] = {"trap_under_8": low, "answers": {a: len(ans[a]) for a in ans}}
    c["detail"].append("trap < 8: %s %d of %d, %s %d of %d" % (x, low[x], len(ans[x]), y, low[y], len(ans[y])))
    check(c, "trap<8 %s <= %s" % (x, y), low[x], "<= %d" % low[y], low[x] <= low[y])
    return finish(c)


def hedge_patterns(lang, which):
    return H3[lang] if which == "third" else V4.HEDGE[lang][which]


def hedge_count(text, lang, which):
    return V4.count_markers(text, hedge_patterns(lang, which), (lang,))


def gate8(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    c = new_cell("g8_hedging", scope,
                 "Are %s answers no more hedged than %s, on every hedge list (no substitution)%s?" % (x, y, q_suffix(scope)),
                 "hedge markers per 1000 chars, mean over the %d finals per arm, each final counted with its own "
                 "language's lists (first and second: verdict4.py's lists; third: the 2026-10-25 amendment): first list "
                 "%s <= 1.00 x %s; second list %s <= 1.10 x %s; third list %s <= 1.10 x %s overall only (reported per "
                 "language)" % (exp_pairs(scope), x, y, x, y, x, y))
    texts, missing = get_texts(D, (x, y), scope)
    if missing:
        return finish(c, missing)
    cs = scope_cases(D, scope)
    m = {}
    for which in ("first", "second", "third"):
        m[which] = {}
        for a in (x, y):
            ks = [(k, a, r) for k in cs for r in ROUNDS]
            m[which][a] = mean([Fraction(hedge_count(texts[q], lang_of(q[0]), which) * 1000, len(texts[q])) for q in ks])
            m[which]["markers_" + a] = sum(hedge_count(texts[q], lang_of(q[0]), which) for q in ks)
        m[which]["ratio"] = None if not m[which][y] else m[which][x] / m[which][y]
    c["measured"] = m
    for which in ("first", "second", "third"):
        c["detail"].append("%-6s list: %s %s (%d markers), %s %s (%d markers), ratio %s%s" % (
            which, x, fmt(m[which][x]), m[which]["markers_" + x], y, fmt(m[which][y]), m[which]["markers_" + y],
            fmt(m[which]["ratio"]), " (reported only in a language cell)" if which == "third" and scope != "overall" else ""))
    check(c, "first list: %s rate <= 1.00 x %s" % (x, y), fmt(m["first"][x]), "<= %s" % fmt(m["first"][y]),
          m["first"][x] <= m["first"][y])
    check(c, "second list: %s rate <= 1.10 x %s" % (x, y), fmt(m["second"][x]),
          "<= %s" % fmt(SECOND_LIST * m["second"][y]), m["second"][x] <= SECOND_LIST * m["second"][y])
    if scope == "overall":
        check(c, "third list: %s rate <= 1.10 x %s" % (x, y), fmt(m["third"][x]),
              "<= %s" % fmt(THIRD_LIST * m["third"][y]), m["third"][x] <= THIRD_LIST * m["third"][y])
    return finish(c)


def gate9(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    nc = len([k for k in V4.EXPECTED_CASES if lang_of(k) in scope_langs(scope)])
    c = new_cell("g9_requests", scope,
                 "Does %s win on more requests than it loses, with the request as the unit%s?" % (x, q_suffix(scope)),
                 "per request: the sum of all its %s-set votes over both rounds and all %d judges (+1 %s win, -1 %s "
                 "win, 0 tie; %d votes each); requests net-positive > requests net-negative (%d requests)"
                 % (s, len(D.judges), x, y, len(ROUNDS) * len(D.judges), nc))
    votes, missing = pair_votes(D, s, scope)
    if missing:
        return finish(c, missing)
    per = defaultdict(list)
    for v in votes:
        per[v["case"]].append(1 if v["win"] == x else -1 if v["win"] == y else 0)
    cs = scope_cases(D, scope)
    nets = {k: sum(per[k]) for k in cs}
    pos, neg = sum(n > 0 for n in nets.values()), sum(n < 0 for n in nets.values())
    c["measured"] = {"request_net": nets, "positive": pos, "negative": neg, "zero": len(nets) - pos - neg,
                     "votes_per_request": {k: len(per[k]) for k in cs}}
    c["detail"].append("requests net-positive %d, net-negative %d, zero %d" % (pos, neg, len(nets) - pos - neg))
    c["detail"].append(" ".join("%s %+d" % (k, n) for k, n in sorted(nets.items())))
    check(c, "requests net-positive > requests net-negative", "%d vs %d" % (pos, neg), "positive > negative", pos > neg)
    return finish(c)


def gate10(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    c = new_cell("g10_mean_scores", scope,
                 "Is %s scored at least as well overall as %s, without losing more than half a point on correct or "
                 "useful%s?" % (x, y, q_suffix(scope)),
                 "means over the %s set's graded answers per arm (%d judges, %d each): total of the five scores %s >= "
                 "%s; mean correct %s >= %s - 0.5; mean useful %s >= %s - 0.5"
                 % (s, len(D.judges), exp_pairs(scope) * len(D.judges), x, y, x, y, x, y))
    votes, missing = pair_votes(D, s, scope)
    if missing:
        return finish(c, missing)
    ans = answers(votes, (x, y))
    m = {}
    for a in (x, y):
        m[a] = {"n": len(ans[a]), "total": mean([sum(g["scores"][d] for d in DIMS) for g in ans[a]])}
        m[a].update({d: mean([g["scores"][d] for g in ans[a]]) for d in DIMS})
    c["measured"] = m
    for a in (x, y):
        c["detail"].append("%-13s n=%d total %s | %s" % (a, m[a]["n"], fmt(m[a]["total"], 2),
                                                         " ".join("%s %s" % (d, fmt(m[a][d], 2)) for d in DIMS)))
    check(c, "mean total %s >= %s" % (x, y), fmt(m[x]["total"]), ">= %s" % fmt(m[y]["total"]),
          m[x]["total"] >= m[y]["total"])
    for d in ("correct", "useful"):
        check(c, "mean %s %s >= %s - 0.5" % (d, x, y), fmt(m[x][d]), ">= %s" % fmt(m[y][d] - HALF),
              m[x][d] >= m[y][d] - HALF)
    return finish(c)


def gate11(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    c = new_cell("g11_fabricated_sources", scope,
                 "Does %s claim to have checked a source without backing it no more often than %s%s?" % (x, y, q_suffix(scope)),
                 "source-claim phrases (round three's zh/en list plus the amendment's ja and ko regular expressions, "
                 "the whole list on every final, re.I) in every final of every run (amendment 2026-10-25); a phrase is "
                 "excused when a law article or document number, a publication or section number, or a URL lies within "
                 "%d characters of it, or when the final names a host that a completed web_fetch of the same run opened "
                 "with HTTP 2xx; unexcused %s <= unexcused %s; a missing or unreadable final or stream fails as metric "
                 "missing" % (EXCUSE_GAP, x, y))
    texts, missing = get_texts(D, (x, y), scope)
    missing = list(missing or [])
    hosts = {}
    for k in scope_cases(D, scope):
        for r in ROUNDS:
            for a in (x, y):
                ev, err = D.events(k, a, r)
                if err:
                    missing.append("raw/%s.%s.%s.ndjson %s" % (k, a, r, err))
                else:
                    hosts[(k, a, r)] = opened_hosts(ev)
    if D.cases is None and not missing:
        missing.append("case list: " + D.case_issue)
    if missing:
        return finish(c, missing)
    cs = scope_cases(D, scope)
    m = {}
    for a in (x, y):
        tot, named_runs, chars = Counter(), 0, 0
        for k in cs:
            for r in ROUNDS:
                fa = fab_analysis(texts[(k, a, r)], hosts[(k, a, r)])
                tot.update({q: fa[q] for q in ("phrases", "cite_excused", "host_excused", "unexcused")})
                named_runs += bool(fa["hosts_named"])
                chars += len(texts[(k, a, r)])
        m[a] = dict(tot, runs=len(cs) * len(ROUNDS), runs_naming_an_opened_host=named_runs,
                    unexcused_per_1000_chars_reported_only=Fraction(tot["unexcused"] * 1000, chars) if chars else None)
        c["detail"].append("%-13s runs %d: phrases %d, excused by a citation %d, excused by a named opened host %d (in %d "
                           "runs), unexcused %d (%s per 1000 chars, reported only)" % (
                               a, m[a]["runs"], tot["phrases"], tot["cite_excused"], tot["host_excused"], named_runs,
                               tot["unexcused"], fmt(m[a]["unexcused_per_1000_chars_reported_only"])))
    c["measured"] = m
    check(c, "unexcused source-claim phrases %s <= %s" % (x, y), m[x]["unexcused"], "<= %d" % m[y]["unexcused"],
          m[x]["unexcused"] <= m[y]["unexcused"])
    return finish(c)


def gate12(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    c = new_cell("g12_unverified_claims", scope,
                 "Does %s add no more claims nobody can check than %s (so a hedge is not swapped for an unverifiable "
                 "specific)?" % (x, y),
                 "added-claim notes of all %d judges on the %s set that both relabellers call 'unverified': %s <= 1.10 x "
                 "%s overall (amendment 2026-10-25); per language reported beside the A/A difference of the same count "
                 "(r1 side - r2 side), not gated" % (len(D.judges), s, x, y))
    t, missing = label_tally(D, s, scope)
    if missing:
        return finish(c, missing)
    ux, uy = t["unver"][x], t["unver"][y]
    per, aa = {}, {}
    for sc in SCOPES:
        if sc != "overall":
            tl, ml = label_tally(D, s, sc)
            per[sc] = None if ml else (tl["unver"][x], tl["unver"][y])
        aa[sc] = {a: aa_unverified_diff(D, a, sc)[0] for a in FLOOR_SETS}
    c["measured"] = {"unverified_both": {x: ux, y: uy}, "per_language_reported_only": per,
                     "aa_difference_reported_only": aa}
    c["detail"].append("unverified by both: %s %d, %s %d (bound %s)" % (x, ux, y, uy, fmt(UNVERIFIED_RATIO * uy, 1)))
    c["detail"].append("per language (reported only): " + "; ".join(
        "%s %s" % (lg, "n/a" if per[lg] is None else "%d vs %d" % per[lg]) for lg in LANGS))
    c["detail"].append("A/A difference of the same count, r1 side - r2 side (reported only): " + "; ".join(
        "%s %s" % (sc, ", ".join("%s %s" % (a, "n/a" if aa[sc][a] is None else "%+d" % aa[sc][a]) for a in FLOOR_SETS))
        for sc in SCOPES))
    check(c, "unverified-by-both %s <= 1.10 x %s" % (x, y), ux, "<= %s" % fmt(UNVERIFIED_RATIO * uy, 1),
          ux <= UNVERIFIED_RATIO * uy)
    return finish(c)


GATE_SPECS = [("g1_votes", gate1, SCOPES), ("g2_each_judge", gate2, ("overall",)), ("g3_length", gate3, SCOPES),
              ("g4_vague_key_points", gate4, SCOPES), ("g5_wrong_added_claims", gate5, SCOPES),
              ("g6_correct_wrong_key_points", gate6, SCOPES), ("g7_trap_under_8", gate7, SCOPES),
              ("g8_hedging", gate8, SCOPES), ("g9_requests", gate9, SCOPES), ("g10_mean_scores", gate10, SCOPES),
              ("g11_fabricated_sources", gate11, SCOPES), ("g12_unverified_claims", gate12, ("overall",))]
GATE_NAMES = [g for g, _, _ in GATE_SPECS]
CELL_IDS = ["%s[%s]" % (g, s) for g, _, scopes in GATE_SPECS for s in scopes]


def gate_table(D, cmp):
    return [fn(D, cmp, s) for _, fn, scopes in GATE_SPECS for s in scopes]


# ---------------------------------------------------------------------------------------------- attr and improvement

def attr_summary(D):
    out = {}
    for scope in SCOPES:
        vs, m = pair_votes(D, "attr", scope, strict=False)
        aa, am = aa_votes(D, "aa-c4", scope, strict=False)
        w, l, t = wl(vs, C4, BASE)
        r1, r2, ties, an = aa_net(aa)
        out[scope] = {"votes": len(vs), "c4_wins": w, "base_wins": l, "ties": t, "net": w - l,
                      "per_judge": {j: dict(zip(("c4_wins", "base_wins", "ties"),
                                                wl([v for v in vs if v["judge"] == j], C4, BASE))) for j in D.judges},
                      "aa_c4_votes": len(aa), "aa_c4_net": an, "complete": not m and not am,
                      "missing": list(dict.fromkeys(m + am))}
    return out


def improvement(main_cells, base_cells, attr):
    """Amended version of verdict4.py's stop-rule test. Yes only when: no cell of either table is metric missing
    and the attr and aa-c4 votes of all three judges are complete; gv-grav-c4 passes at least as many of the 52 cells
    as gv-grav-base; and the attr net (c4 wins - base wins, three judges) is above sqrt(2) x the aa-c4 noise floor
    (the attr set has twice the pairs of aa-c4, as in gate 1)."""
    miss = []
    mm = [c["id"] for c in main_cells if c["kind"] == "missing"]
    bm = [c["id"] for c in base_cells if c["kind"] == "missing"]
    if mm:
        miss.append("candidate table cells with metric missing: " + summarize(mm, 8))
    if bm:
        miss.append("base table cells with metric missing: " + summarize(bm, 8))
    a = attr["overall"]
    if not a["complete"]:
        miss.append("attr / aa-c4 votes incomplete: " + summarize(a["missing"], 3))
    bidx = {c["id"]: c for c in base_cells}
    cp = sum(c["status"] == "PASS" for c in main_cells)
    bp = sum(c["status"] == "PASS" for c in base_cells)
    floor = abs(a["aa_c4_net"])
    gains = [c["id"] for c in main_cells if c["status"] == "PASS" and bidx[c["id"]]["status"] != "PASS"]
    losses = [c["id"] for c in main_cells if c["status"] != "PASS" and bidx[c["id"]]["status"] == "PASS"]
    checks = [{"desc": "gv-grav-c4 passes at least as many cells as gv-grav-base", "value": "%d vs %d" % (cp, bp),
               "bound": "c4 >= base", "ok": cp >= bp},
              {"desc": "attr net votes (c4 - base, three judges) > sqrt(2) x aa-c4 noise floor", "value": "%+d" % a["net"],
               "bound": "> %.3f" % (floor * 2 ** 0.5), "ok": sqrt2_above(a["net"], floor)}]
    if miss:
        yes, reasons = False, ["metric missing: " + "; ".join(miss)]
    else:
        yes = all(k["ok"] for k in checks)
        reasons = [k["desc"] + " (%s, need %s)" % (k["value"], k["bound"]) for k in checks if not k["ok"]]
    summary = "c4 passes %d of %d cells, base %d of %d; attr net %+d vs sqrt(2) x aa-c4 noise floor %d" % (
        cp, len(main_cells), bp, len(base_cells), a["net"], floor)
    word = "yes" if yes else "no"
    line = "%s (%s)" % (word, summary) if yes else "no (%s; %s)" % ("; ".join(reasons), summary)
    return {"improvement": word, "line": line, "checks": checks, "reasons": reasons, "c4_cells_passed": cp,
            "base_cells_passed": bp, "cells": len(main_cells), "attr_net": a["net"], "aa_c4_floor": floor,
            "c4_passes_base_fails": gains, "base_passes_c4_fails": losses, "missing": miss}


# ---------------------------------------------------------------------------------------------- reported beside

def shorter_share(D, s):
    """Decisive votes that went to the shorter answer, per judge and pooled (amendment 2026-10-25, reported only).
    A vote between answers of equal length, or with a final missing, is left out."""
    aa = s in AA_SETS
    votes, m = (aa_votes if aa else pair_votes)(D, s, "overall", strict=False)
    per, unmeasured = {j: [0, 0] for j in D.judges}, 0
    for v in votes or []:
        if v["grade"]["winner"] == "tie":
            continue
        e, lens = v["entry"], {}
        for side in "AB":
            t, err = D.text(v["case"], e[side], e["%s_round" % side] if aa else v["round"])
            lens[side] = None if err else len(t)
        if None in lens.values():
            unmeasured += 1
            continue
        if lens["A"] == lens["B"]:
            continue
        shorter = "A" if lens["A"] < lens["B"] else "B"
        per[v["judge"]][1] += 1
        per[v["judge"]][0] += v["grade"]["winner"] == shorter
    pooled = [sum(p[0] for p in per.values()), sum(p[1] for p in per.values())]
    share = lambda p: Fraction(p[0], p[1]) if p[1] else None
    return {"per_judge": {j: {"to_shorter": p[0], "decisive": p[1], "share": share(p)} for j, p in per.items()},
            "pooled": {"to_shorter": pooled[0], "decisive": pooled[1], "share": share(pooled)},
            "unmeasured": unmeasured, "complete": not m}


def ledger_report(D):
    """Re-grade and re-label counts from the ledger, per set and by the arm the first valid grade picked."""
    if D.ledger is None:
        return None
    regr = {}
    for pid, e in D.entries.items():
        for j in D.judges:
            slot = D.ledger["grades"].get((pid, j))
            if not slot or (slot["entries"] <= 1 and not slot["replaces"]):
                continue
            ref = slot["ref"]
            win = ref["grade"].get("winner") if ref and isinstance(ref.get("grade"), dict) else None
            arm = "tie" if win == "tie" else e.get(win) if win in ("A", "B") else "none"
            d = regr.setdefault(e["set"], {"pair_judges": 0, "extra_entries": 0, "replaces": 0,
                                           "by_first_valid_winner": Counter()})
            d["pair_judges"] += 1
            d["extra_entries"] += max(slot["entries"] - 1, 0)
            d["replaces"] += slot["replaces"]
            d["by_first_valid_winner"][arm] += 1
    rel = {}
    for (rid, who), slot in D.ledger["labels"].items():
        if slot["entries"] > 1 or slot["replaces"]:
            d = rel.setdefault(who, {"ids": 0, "extra_entries": 0, "replaces": 0})
            d["ids"] += 1
            d["extra_entries"] += max(slot["entries"] - 1, 0)
            d["replaces"] += slot["replaces"]
    return {"regrades": regr, "relabels": rel}


def report_beside(D):
    out, lines = {}, []

    def sec(title):
        lines.append("-- " + title)

    sec("inputs")
    if D.cases:
        lines.append("  cases: %d (%s)" % (len(D.cases), ", ".join("%s %d" % (lg, len(scope_cases(D, lg))) for lg in LANGS)))
    else:
        lines.append("  cases: n/a (%s)" % D.case_issue)
    lines.append("  blind-map pairs by set: %s" % dict(Counter(e["set"] for e in D.entries.values())))
    for k in sorted(D.map_issues, key=str):
        lines.append("  blind-map issues (%s): %s" % (k if isinstance(k, str) else "%s/%s" % k, summarize(D.map_issues[k], 4)))
    if D.map_warnings:
        lines.append("  blind-map entries ignored: %s" % summarize(D.map_warnings, 4))
    ok = {j: sum(1 for (jj, _), (gr, err) in D.grades.items() if jj == j and not err) for j in D.judges}
    bad = {j: [pid for (jj, pid), (gr, err) in D.grades.items() if jj == j and err] for j in D.judges}
    lines.append("  valid grade files: %s of %d mapped pairs each; stray grade files (pid not in map): %d" % (
        ok, len(D.entries), len(D.stray_grades)))
    for j in D.judges:
        if bad[j]:
            lines.append("  %s grades missing, malformed or failing an integrity check: %d (%s)" % (
                j, len(bad[j]), summarize(sorted(bad[j]), 8)))
    if D.kp_issues:
        lines.append("  key-point issues: %s" % summarize(list(D.kp_issues.values()), 4))
    known = set(D.entries)
    by_judge = Counter(r["grader"] for r in (D.notes or {}).values())
    orphan = sum(1 for r in (D.notes or {}).values() if r["pid"] not in known)
    lines.append("  claim-notes rows: %s (by judge %s; %d with a pid not in the map)" % (
        len(D.notes) if D.notes is not None else "n/a (%s)" % summarize(D.notes_issues, 2), dict(by_judge), orphan))
    out["inputs"] = {"cases": D.cases, "case_issue": D.case_issue, "map_issues": D.map_issues,
                     "map_warnings": D.map_warnings, "valid_grades": ok, "invalid_grades": bad,
                     "stray_grades": D.stray_grades, "keypoint_issues": D.kp_issues,
                     "claim_notes_by_judge": dict(by_judge), "claim_notes_orphans": orphan}

    sec("integrity: run validity report, answer hashes, grade and label ledger")
    v = D.validity or {}
    lines.append("  validity.json: %s; final_attempt_invalid (graded as is) %s; flagged %d; rule-file problems %s" % (
        "OK" if not D.global_issues else "FAILS (%s)" % summarize(D.global_issues, 3),
        v.get("final_attempt_invalid") or "none", len(v.get("flagged") or []), v.get("rule_files") or "none"))
    lines.append("  answers not matching their packaged sha256: %d pairs%s" % (
        len(D.answer_issue), ("; " + summarize(sorted(D.answer_issue.values()), 3)) if D.answer_issue else ""))
    lr = ledger_report(D)
    if lr is None:
        lines.append("  ledger: n/a (%s)" % D.ledger_issue)
    else:
        lines.append("  re-grades per set (grade entries beyond the first per pair and judge; arm of the first valid "
                     "grade): %s" % ({s: dict(d, by_first_valid_winner=dict(d["by_first_valid_winner"]))
                                     for s, d in sorted(lr["regrades"].items())} or "none"))
        lines.append("  re-labels per relabeller: %s" % (lr["relabels"] or "none"))
    out["integrity"] = {"global_issues": D.global_issues, "validity": D.validity, "answer_issues": D.answer_issue,
                        "ledger_issue": D.ledger_issue, "ledger": lr}

    sec("votes per judge and sign tests (two-sided exact binomial on non-tie votes, all three judges pooled)")
    st = {}
    for s, (x, y) in PAIR_SETS.items():
        st[s] = {}
        for scope in SCOPES:
            vs, m = pair_votes(D, s, scope, strict=False)
            w, l, t = wl(vs, x, y)
            st[s][scope] = {"x": x, "y": y, "x_wins": w, "y_wins": l, "ties": t, "votes": len(vs), "complete": not m,
                            "p": V4.sign_test(w, l),
                            "per_judge": {j: wl([v for v in vs if v["judge"] == j], x, y) for j in D.judges}}
        lines.append("  %-5s %s vs %s: %s" % (s, x, y, "; ".join(
            "%s %d-%d-%d p=%s%s" % (sc, d["x_wins"], d["y_wins"], d["ties"], V4.fmt_p(d["p"]),
                                    "" if d["complete"] else " (incomplete)") for sc, d in st[s].items())))
        lines.append("        overall by judge: %s" % ", ".join(
            "%s %d-%d-%d" % ((j,) + tuple(st[s]["overall"]["per_judge"][j])) for j in D.judges))
    lines.append("  (wins-losses-ties; with 18 votes per language only a large effect can show)")
    out["sign_tests"] = st

    sec("A/A noise per scope: votes (r1-side wins - r2-side wins), ties, and vague key points (r1-side - r2-side)")
    aa_rep = {}
    for a in FLOOR_SETS:
        aa_rep[a] = {}
        for scope in SCOPES:
            vs, m = aa_votes(D, a, scope, strict=False)
            r1, r2, t, n = aa_net(vs)
            aa_rep[a][scope] = {"votes": len(vs), "r1": r1, "r2": r2, "ties": t, "net": n,
                                "vague_r1_minus_r2": aa_vague_diff(vs), "complete": not m}
        lines.append("  %-8s %s" % (a, "; ".join("%s net %+d ties %d vague %+d (%d votes%s)" % (
            sc, d["net"], d["ties"], d["vague_r1_minus_r2"], d["votes"], "" if d["complete"] else ", incomplete")
            for sc, d in aa_rep[a].items())))
    out["aa"] = aa_rep

    sec("decisive votes that went to the shorter answer, per judge and per set (equal lengths left out; in the A/A "
        "sets any length preference is pure bias). Reported, not gated")
    sh = {}
    for s in list(PAIR_SETS) + list(AA_SETS):
        sh[s] = shorter_share(D, s)
        d = sh[s]
        lines.append("  %-8s pooled %s of %d%s; %s" % (
            s, fmt(d["pooled"]["share"]), d["pooled"]["decisive"], "" if d["complete"] else " (incomplete)",
            ", ".join("%s %s of %d" % (j, fmt(p["share"]), p["decisive"]) for j, p in d["per_judge"].items())))
    out["shorter_share"] = sh

    sec("Cohen's kappa between judges on the winner (pairwise)")
    kp = {}
    for s in PAIR_SETS:
        kp[s] = {}
        for i, j1 in enumerate(D.judges):
            for j2 in D.judges[i + 1:]:
                pairs = []
                for (c, r), pid in D.pindex[s].items():
                    a_, b_ = D.grades.get((j1, pid), (None, 1)), D.grades.get((j2, pid), (None, 1))
                    if not a_[1] and not b_[1]:
                        e = D.entries[pid]
                        pairs.append(tuple("tie" if g["winner"] == "tie" else e[g["winner"]] for g in (a_[0], b_[0])))
                k = V4.cohen_kappa(pairs, PAIR_SETS[s] + ("tie",))
                kp[s]["%s-%s" % (j1, j2)] = {"n": len(pairs), "kappa": k}
        lines.append("  %-5s %s" % (s, "; ".join("%s n=%d kappa %s" % (k, v_["n"], fmt(v_["kappa"]) if v_["kappa"] is not None else "n/a")
                                                 for k, v_ in kp[s].items())))
    out["kappa"] = kp

    sec("format metrics per answer, medians per arm (chars all languages; words English only; list items; "
        "bold spans; headings). Reported, not gated")
    fm = {}
    for arm in ARMS:
        fm[arm] = {}
        for scope in SCOPES:
            rows, miss = [], 0
            for c in scope_cases(D, scope):
                for r in ROUNDS:
                    t, err = D.text(c, arm, r)
                    if err:
                        miss += 1
                    else:
                        rows.append(format_metrics(t, lang_of(c)))
            med = {k: median([x[k] for x in rows if x[k] is not None]) for k in
                   ("chars", "en_words", "list_items", "bold_spans", "headings")}
            fm[arm][scope] = {"answers": len(rows), "missing": miss, "medians": med}
    for scope in SCOPES:
        lines.append("  %s:" % scope)
        for arm in ARMS:
            d = fm[arm][scope]
            md = d["medians"]
            lines.append("    %-13s n=%d%s chars %s, en words %s, list items %s, bold %s, headings %s" % (
                arm, d["answers"], " (%d missing)" % d["missing"] if d["missing"] else "", fmt(md["chars"], 1),
                fmt(md["en_words"], 1) if scope in ("overall", "en") else "-", fmt(md["list_items"], 1),
                fmt(md["bold_spans"], 1), fmt(md["headings"], 1)))
    out["format_metrics"] = fm

    sec("event streams (raw/*.ndjson): runs that opened a page with HTTP 2xx (completed web_fetch); searched only")
    evr = {}
    for arm in ARMS:
        n_ok, fetch, search_only, bad_ = 0, 0, 0, []
        for c in D.cases or []:
            for r in ROUNDS:
                ev, err = D.events(c, arm, r)
                if err:
                    bad_.append("%s %s: %s" % (c, r, err))
                    continue
                n_ok += 1
                f = bool(opened_hosts(ev))
                fetch += f
                calls = {e.get("callId"): e.get("tool") for e in ev if e.get("type") == "tool_call"}
                srch = any(e.get("type") == "tool_result" and e.get("status") == "completed"
                           and calls.get(e.get("callId")) == "web_search" for e in ev)
                search_only += (srch and not f)
        evr[arm] = {"streams": n_ok, "opened_a_page_2xx": fetch, "searched_only": search_only, "unreadable": bad_}
        lines.append("  %-13s streams read %d of %d; opened a page (2xx) %d; searched without opening a page %d%s" % (
            arm, n_ok, len(D.cases or []) * len(ROUNDS), fetch, search_only,
            ("; unreadable: " + summarize(bad_, 2)) if bad_ else ""))
    out["events"] = evr
    return out, lines


# ---------------------------------------------------------------------------------------------- the frozen version

def frozen_view(base, dst):
    """Copy what verdict4.py reads into dst, with the opus and sonnet grades only: blind/grades/codex is not copied,
    and claim-notes.json rows whose grader is 'codex' are removed (verdict4.py as frozen rejects a note from any
    grader but opus and sonnet). Everything else is copied byte for byte. Returns the number of rows removed."""
    for rel in ("prompts", "keypoints", "raw") + tuple(os.path.join("blind", "grades", g) for g in FROZEN_JUDGES):
        src = os.path.join(base, rel)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(dst, rel))
    for name in ("blind-map.json", "labels-opus.json", "labels-sonnet.json"):
        src = os.path.join(base, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(dst, name))
    src = os.path.join(base, "claim-notes.json")
    removed = 0
    if os.path.isfile(src):
        j, err = V4.rd_json(src) if V4 is not None else (None, "no reader")
        if err is None and isinstance(j, list):
            kept = [r for r in j if not (isinstance(r, dict) and r.get("grader") == "codex")]
            removed = len(j) - len(kept)
            with open(os.path.join(dst, "claim-notes.json"), "w", encoding="utf-8") as f:
                json.dump(kept, f, ensure_ascii=False, indent=1)
        else:
            shutil.copy2(src, os.path.join(dst, "claim-notes.json"))
    return removed


def run_frozen(base, path):
    mod, sha, err = load_frozen(path)
    out = {"path": os.path.abspath(path), "sha256": sha, "frozen_sha256": FROZEN_SHA256, "error": err}
    if err:
        out.update({"computed": False, "verdict": "not a win", "failing": None, "improvement": "no",
                    "line": "VERDICT (as frozen, opus+sonnet): not a win (frozen verdict not computed: %s)" % err,
                    "improvement_line": "IMPROVEMENT (as frozen, opus+sonnet): no (frozen version not computed: %s)" % err,
                    "report_lines": ["frozen verdict not computed: " + err], "result": None})
        return out
    tmp = tempfile.mkdtemp(prefix="verdict4-frozen-view-")
    try:
        removed = frozen_view(base, tmp)
        res = mod.evaluate(tmp)
        res["base"] = "%s (a temporary copy holding the opus and sonnet grades only; %d codex claim-notes rows " \
                      "left out)" % (base, removed)
        lines = mod.render(res)
    except Exception as e:  # a crash of the frozen script is no verdict, so the round is not a win
        err = "the frozen script raised %s: %s" % (type(e).__name__, e)
        out.update({"computed": False, "error": err, "verdict": "not a win", "failing": None, "improvement": "no",
                    "line": "VERDICT (as frozen, opus+sonnet): not a win (frozen verdict not computed: %s)" % err,
                    "improvement_line": "IMPROVEMENT (as frozen, opus+sonnet): no (frozen version not computed: %s)" % err,
                    "report_lines": ["frozen verdict not computed: " + err], "result": None})
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    vl = res["verdict_line"]
    il = res["improvement"]["line"]
    out.update({"computed": True, "verdict": res["verdict"], "failing": res["failing"],
                "improvement": res["improvement"]["improvement"], "codex_rows_removed": removed,
                "line": "VERDICT (as frozen, opus+sonnet): " + (vl[len("VERDICT: "):] if vl.startswith("VERDICT: ") else vl),
                "improvement_line": "IMPROVEMENT (as frozen, opus+sonnet): " + (
                    il[len("IMPROVEMENT: "):] if il.startswith("IMPROVEMENT: ") else il),
                "report_lines": lines, "result": res})
    return out


# ---------------------------------------------------------------------------------------------- evaluate and render

def amended_verdict(cells):
    failing = [c["id"] for c in cells if c["status"] != "PASS"]
    win = not failing and [c["id"] for c in cells] == CELL_IDS
    line = "VERDICT (amended, three judges): win" if win else "VERDICT (amended, three judges): not a win (failing: %s)" % (
        ", ".join(failing) if failing else "the cell list is not the frozen list")
    return ("win" if win else "not a win"), failing, line


def evaluate(base, frozen_path=None):
    frozen = run_frozen(base, frozen_path or os.path.join(HERE, FROZEN_FILE))
    res = {"base": base, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "script_sha256": script_sha256(), "verdict4_sha256": V4_SHA, "frozen": frozen}
    if V4 is None:
        res.update({"computed": False, "error": V4_ERR, "tables": None, "attr": None, "reported": None,
                    "report_lines": [], "verdict": "not a win", "failing": None,
                    "verdict_line": "VERDICT (amended, three judges): not a win (not computed: %s)" % V4_ERR,
                    "improvement": {"improvement": "no", "line": "no (not computed: %s)" % V4_ERR, "checks": [],
                                    "c4_passes_base_fails": [], "base_passes_c4_fails": []}})
    else:
        D = Data3(base)
        tables = {}
        for cmp in (CMP_MAIN, CMP_BASE):
            tables[cmp["key"]] = {"title": cmp["title"], "set": cmp["set"], "x": cmp["x"], "y": cmp["y"],
                                  "cells": gate_table(D, cmp)}
        attr = attr_summary(D)
        imp = improvement(tables["main"]["cells"], tables["base"]["cells"], attr)
        reported, rlines = report_beside(D)
        verdict, failing, line = amended_verdict(tables["main"]["cells"])
        res.update({"computed": True, "error": None, "cases": D.cases, "tables": tables, "attr": attr,
                    "improvement": imp, "reported": reported, "report_lines": rlines, "verdict": verdict,
                    "failing": failing, "verdict_line": line})
    res["amended_improvement_line"] = "IMPROVEMENT (amended, three judges): " + res["improvement"]["line"]
    both_imp = frozen["improvement"] == "yes" and res["improvement"]["improvement"] == "yes"
    res["improvement_line"] = "IMPROVEMENT: yes (both versions say yes)" if both_imp else \
        "IMPROVEMENT: no (as frozen: %s; amended: %s; both must say yes)" % (frozen["improvement"],
                                                                          res["improvement"]["improvement"])
    round_win = frozen["verdict"] == "win" and res["verdict"] == "win"
    res["round_verdict"] = "win" if round_win else "not a win"
    res["round_line"] = "ROUND VERDICT: win" if round_win else \
        "ROUND VERDICT: not a win (as frozen: %s; amended: %s; it counts as a win only if it wins on both)" % (
            frozen["verdict"], res["verdict"])
    return res


def code(c):
    return {"pass": "PASS", "bound": "FAIL", "missing": "MISS"}.get(c["kind"], "?") if c else "-"


def render(res):
    out = ["== round-four verdict, amended: WIN_CRITERIA.md with the amendments of 2026-10-24 and 2026-10-25, and the "
           "version before them",
           "== evaluated folder: %s" % res["base"],
           "== script sha256 %s (verdict4-amended.py)" % res["script_sha256"],
           "== verdict4.py sha256 %s (frozen %s: %s)" % (res["verdict4_sha256"], FROZEN_SHA256,
                                                       "match" if res["verdict4_sha256"] == FROZEN_SHA256 else "MISMATCH"),
           "== judges %s (all votes count; gate 2 for each); relabellers %s; candidate gv-grav-c4, control gv-plain"
           % (", ".join(JUDGES), ", ".join(RELABELLERS))]
    if res["computed"]:
        for key in ("main", "base"):
            t = res["tables"][key]
            out.append("== gate table (amended): %s" % t["title"])
            for c in t["cells"]:
                out.append("[%s] %s: %s" % (c["status"], c["id"], c["question"]))
                out.append("       bounds: %s" % c["bounds"])
                for d in c["detail"]:
                    out.append("       " + d)
                for k in c["checks"]:
                    out.append("       %-62s = %-10s need %-12s %s" % (k["desc"], k["value"], k["bound"],
                                                                     "ok" if k["ok"] else "NOT MET"))
                if c["status"] != "PASS":
                    out.append("       -> %s: %s" % (c["status"], c["reason"]))
        out.append("== side by side (c4 = gv-grav-c4 vs gv-plain, main set; base = gv-grav-base vs gv-plain, base set)")
        out.append("   PASS = bounds met, FAIL = bound not met, MISS = metric missing (fails), - = not gated per language")
        out.append("   %-30s" % "gate" + "".join("%-14s" % s for s in SCOPES))
        out.append("   %-30s" % "" + "".join("%-14s" % "c4 / base" for _ in SCOPES))
        idx = {k: {(c["gate"], c["scope"]): c for c in res["tables"][k]["cells"]} for k in ("main", "base")}
        for g in GATE_NAMES:
            out.append("   %-30s" % g + "".join("%-14s" % ("%s / %s" % (code(idx["main"].get((g, s))),
                                                                       code(idx["base"].get((g, s))))) for s in SCOPES))
        out.append("== attr set: gv-grav-c4 vs gv-grav-base, three judges (the aa-c4 net is the improvement rule's floor)")
        for s, a in res["attr"].items():
            out.append("   %-8s votes %d: c4 %d, base %d, tie %d, net %+d; aa-c4 net %+d (%d votes)%s" % (
                s, a["votes"], a["c4_wins"], a["base_wins"], a["ties"], a["net"], a["aa_c4_net"], a["aa_c4_votes"],
                "" if a["complete"] else "  incomplete: " + summarize(a["missing"], 2)))
        imp = res["improvement"]
        out.append("== improvement over the previous best, amended (for the stop rule, not part of the verdict)")
        for k in imp["checks"]:
            out.append("   %-78s = %-10s need %-10s %s" % (k["desc"], k["value"], k["bound"], "ok" if k["ok"] else "NOT MET"))
        out.append("   cells c4 passes and base fails: %s" % (", ".join(imp["c4_passes_base_fails"]) or "none"))
        out.append("   cells base passes and c4 fails: %s" % (", ".join(imp["base_passes_c4_fails"]) or "none"))
        out.append("== reported beside the verdict (not gates)")
        out += res["report_lines"]
    else:
        out.append("== amended verdict not computed: %s" % res["error"])
    fr = res["frozen"]
    out.append("== the version before the amendment: %s, imported unchanged (sha256 %s), run on the opus and sonnet "
               "grades only" % (fr["path"], fr["sha256"]))
    out += ["  | " + ln for ln in fr["report_lines"]]
    out.append(fr["improvement_line"])
    out.append(res["amended_improvement_line"])
    out.append(res["improvement_line"])
    out.append(fr["line"])
    out.append(res["verdict_line"])
    out.append(res["round_line"])
    return out


def jsonable(x):
    if V4 is not None:
        return V4.jsonable(x)
    if isinstance(x, Fraction):
        return round(float(x), 6)
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set)):
        return [jsonable(v) for v in x]
    return x


def write_results(res, base):
    with open(os.path.join(base, "verdict4-amended.json"), "w", encoding="utf-8") as f:
        json.dump(jsonable(res), f, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------------------------------------- self-test

FAB_PHRASE = {"zh": "据人社部官网", "en": "According to the agency", "ja": "厚生労働省によると", "ko": "고용노동부에 따르면"}
FAB_TAIL = {"zh": "，这一点没有变化。", "en": ", it holds. ", "ja": "、変わりません。", "ko": " 그렇습니다. "}
FAB_CITE = {"zh": "（第5条）", "en": " (Publication 969)", "ja": "（第39条）", "ko": " (제58조)"}
THIRD_SAMPLE = {"zh": "这不一定。", "en": "It could change. ", "ja": "そうでしょう。", "ko": "그런 것 같습니다. "}
GOOD = ((8, 9, 9, 8, 8), ("correct", "correct", "correct", "correct", "vague"))
WEAK = ((6, 6, 7, 6, 7), ("correct", "correct", "vague", "vague", "wrong"))
EVEN = ((7, 8, 7, 7, 7), ("correct",) * 5)
AA_OUT = {"aa-plain": {0: ("r1", "r1", "r1"), 1: ("r2", "tie", "tie"), 2: ("tie", "tie", "tie")},
          "aa-c4": {0: ("r2", "r2", "tie"), 1: ("r1", "tie", "tie"), 2: ("tie", "tie", "tie")}}


def synth_pos(case):
    return sum(1 for d in V4.EXPECTED_CASES if lang_of(d) == lang_of(case) and d < case)


def synth_text(case, arm, rnd, kw):
    lg, ci, ri, pos = lang_of(case), V4.EXPECTED_CASES.index(case), ROUNDS.index(rnd), synth_pos(case)
    if (case, arm, rnd) == kw.get("blank"):
        return ""
    if kw.get("uneven"):        # per language: c4 cut to 0.61 on the short and the long request, 0.98 on the middle one
        pl = {0: (800, 820), 1: (1200, 1250), 2: (2000, 2100)}[pos][ri]
        return "字" * {PLAIN: pl, C4: pl * (98 if pos == 1 else 61) // 100, BASE: pl * 110 // 100}[arm]
    if kw.get("markup"):        # plain: 40 bold bullet lines of 20 chars; c4: 40 lines of 21 chars, no markup
        return {PLAIN: "".join("- **%s**\n" % ("字" * 20) for _ in range(40)),
                C4: "".join("%s\n" % ("字" * 21) for _ in range(40)), BASE: "字" * 1200}[arm]
    if kw.get("exact_len"):
        return "字" * kw["exact_len"][arm]
    n = 40 + ci % 3 + 2 * ri
    if arm == PLAIN:
        k, extra, fab = n, V4.EXTRA["plain"][lg], kw.get("fab_plain", 2)
    elif arm == C4:
        pct = {"first": 96, "second": 89}.get(kw.get("hedge_mild"), kw.get("c4_pct", 85))
        k = n // 2 if (case, rnd) in kw.get("short_pairs", ()) else n * pct // 100
        ex = "swap" if kw.get("hedge_swap") else "mild_" + kw["hedge_mild"] if kw.get("hedge_mild") else "grav"
        extra, fab = V4.EXTRA[ex][lg], kw.get("fab_c4", 1)
    else:
        k, extra, fab = n * (85 if kw.get("base_good") else 110) // 100, V4.EXTRA["grav"][lg], kw.get("fab_base", 1)
    fab = kw.get("fab_lang", {}).get((arm, lg), fab)
    if arm == C4 and kw.get("fab_cited"):   # the gap also follows the citation, so it is that far from the next phrase
        gap = "·" * kw.get("cite_gap", 0)   # a non-word filler, so  still holds at the next phrase
        fab_text = (FAB_PHRASE[lg] + gap + FAB_CITE[lg] + FAB_TAIL[lg] + gap) * fab
    else:
        fab_text = (FAB_PHRASE[lg] + FAB_TAIL[lg]) * fab
    t = V4.FILL[lg] * k + "".join(extra) + fab_text
    if arm == C4 and kw.get("name_host"):
        t += "（example.org）"
    if arm == C4 and kw.get("third_hedge"):
        t += THIRD_SAMPLE[lg]
    return t


def synth_events(case, arm, rnd, kw):
    lg = lang_of(case)

    def fetch(cid, code):
        return [{"type": "tool_call", "callId": cid, "tool": "web_fetch", "input": {"url": "https://www.example.org/page"}},
                {"type": "tool_result", "callId": cid, "status": "completed",
                 "result": "Fetched https://www.example.org/page (HTTP %s)\n\nExternal web content follows." % code}]

    ev = [{"type": "status", "phase": "step_start"}, {"type": "tool_call", "callId": "c1", "tool": "pwsh", "input": {}},
          {"type": "tool_result", "callId": "c1", "status": "completed", "result": "ok"}]
    if (case == V4.EXPECTED_CASES[0] and rnd == "r1") or arm in kw.get("web", {}).get(lg, ()):
        ev += fetch("c2", "200")
    if arm == C4 and kw.get("c4_fetch"):
        ev += fetch("c5", kw["c4_fetch"])
    if arm in kw.get("search_only", {}).get(lg, ()):
        ev += [{"type": "tool_call", "callId": "c3", "tool": "web_search", "input": {"q": "x"}},
               {"type": "tool_result", "callId": "c3", "status": "completed", "result": "hits"}]
    if case == "ko-severance-pay":   # a failed page fetch opens nothing
        ev += [{"type": "tool_call", "callId": "c4", "tool": "web_fetch", "input": {"url": "https://example.org"}},
               {"type": "tool_result", "callId": "c4", "status": "error", "result": "fetch failed"}]
    return ev


def revalidate(base):
    """Make validity.json newer than every run file, as rerunning validity4.py would."""
    p = os.path.join(base, "validity.json")
    raw = os.path.join(base, "raw")
    if os.path.isfile(p):
        t = max([os.path.getmtime(os.path.join(raw, f)) for f in os.listdir(raw)] + [0]) + 2
        os.utime(p, (t, t))


def make_synthetic(base, **kw):
    """Three judges; gv-grav-c4 clearly wins everything (amended and frozen) unless a knob says otherwise; the base
    arm's answers are longer than plain's, so the base table fails gate 3 only. Writes packets, answer hashes in the
    blind-map, the ledger and a validity report, as the round's own tools would."""
    def wj(rel, obj):
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)

    def wt(rel, text):
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)

    kp_ids = ["1", "2", "3", "4", "5"]
    bmap, grades, pids, cnt, extra = {}, {}, {}, [0], [0]

    def pid():
        cnt[0] += 1
        return "p%03d" % cnt[0]

    def side(sc, kp, notes):
        d = dict(zip(DIMS, sc))
        d.update({"added_claim_errors": notes, "key_points": dict(zip(kp_ids, kp))})
        return d

    cases = V4.EXPECTED_CASES
    for ci, c in enumerate(cases):
        lg, pos = lang_of(c), synth_pos(c)
        wt("prompts/%s.txt" % c, "synthetic request\n")
        wj("keypoints/%s.json" % c, [{"id": k, "point": "synthetic point %s" % k} for k in kp_ids])
        for ri, r in enumerate(ROUNDS):
            x_is_a = ri == ci % 2
            for s, (x, y) in PAIR_SETS.items():
                p = pid()
                pids[(s, c, r)] = p
                A, B = (x, y) if x_is_a else (y, x)
                bmap[p] = {"set": s, "case": c, "round": r, "A": A, "B": B}
                xs, ys = ("A", "B") if x_is_a else ("B", "A")
                for j in JUDGES:
                    if s == "attr":
                        win, gx, gy = xs, side(*GOOD, []), side(*EVEN, [])
                        if kw.get("attr_noise") and j != "codex":   # codex 24 + opus 4 + sonnet 4 = +32
                            win = xs if r == "r1" and pos == (0 if j == "opus" else 1) else "tie"
                    else:
                        tag = "c4" if x == C4 else "base"
                        win = xs
                        main = s == "main"
                        if main and lg == kw.get("lang_fail"):
                            win = ys
                        if main and kw.get("codex_plain") and j == "codex":
                            win = ys
                        if main and kw.get("codex_even") and j == "codex":
                            win = xs if r == "r1" else ys
                        if main and kw.get("noise") and j != "codex":
                            win = "tie"
                        if main and kw.get("sqrt2") and j != "codex":
                            win = xs if pos == 0 and r == ("r1" if j == "opus" else "r2") else "tie"
                        if main and kw.get("one_request") == "negative":
                            win = xs if pos == 0 else (ys if r == "r1" and j == ("opus", "sonnet")[pos - 1] else "tie")
                        if main and kw.get("one_request") == "tied":
                            win = xs if pos == 0 else (ys if r == "r1" and j == "opus" and pos == 1 else "tie")
                        sc = list(GOOD[0])
                        if main and kw.get("useful_drop"):
                            sc[DIMS.index("useful")] = 5 if (kw["useful_drop"] == "all" or r == "r1") else 6
                        if main and kw.get("low_total"):
                            sc[DIMS.index("honest")] = sc[DIMS.index("concise")] = 2
                        if main and kw.get("trap7"):
                            sc[DIMS.index("trap")] = 7
                        if main and kw.get("equal"):
                            gx = side(*WEAK, ["synthetic c4 wrong-claim %s %s %d: fee not in the key" % (p, j, k) for k in (1, 2)])
                        else:
                            xkp = GOOD[1]
                            if main and kw.get("c4_wrong_kp"):
                                xkp = ("correct",) * 3 + ("wrong", "wrong")
                            if main and kw.get("drop_points"):
                                xkp = ("correct", "correct", "missing", "missing", "missing")
                            xnotes = ["synthetic %s claim %s %s: date not in the key" % (tag, p, j)]
                            if main and j == "opus" and extra[0] < kw.get("unver_extra", 0):
                                xnotes.append("synthetic c4 extra claim %s: a figure nobody can check" % p)
                                extra[0] += 1
                            gx = side(tuple(sc), xkp, xnotes)
                        ykp, ysc = WEAK[1], list(WEAK[0])
                        if main and kw.get("vague_codex") and lg == "zh":
                            ykp = ("correct", "correct", "wrong", "missing", "missing") if j != "codex" else \
                                ("vague", "vague", "vague", "vague", "wrong")
                        if main and kw.get("drop_points"):
                            ykp = ("correct", "correct", "vague", "vague", "vague")
                        if main and kw.get("trap7"):
                            ysc[DIMS.index("trap")] = 9
                        gy = side(tuple(ysc), ykp, ["synthetic plain wrong-claim %s %s %d: fee not in the key" % (p, j, k)
                                                    for k in (1, 2)] +
                                  ["synthetic plain unverified-claim %s %s: a date nobody can check" % (p, j)])
                    grades[(j, p)] = {"pair": p, "winner": win, "margin": "clear", xs: gx, ys: gy, "reasons": "synthetic"}
        for s, arm in AA_SETS.items():
            p = pid()
            pids[(s, c)] = p
            a_r1 = ci % 2 == 0
            bmap[p] = {"set": s, "case": c, "round": "r1r2", "A": arm, "B": arm,
                       "A_round": "r1" if a_r1 else "r2", "B_round": "r2" if a_r1 else "r1"}
            for ji, j in enumerate(JUDGES):
                o = AA_OUT[s][pos][ji]
                if kw.get("attr_noise") and s == "aa-c4":
                    o = "tie" if j == "codex" else "r1"
                if (kw.get("noise") or kw.get("sqrt2")) and s == "aa-plain":
                    o = "tie" if j == "codex" else "r1"
                win = "tie" if o == "tie" else ("A" if (o == "r1") == a_r1 else "B")
                # aa-plain: 2 vague marks on the r1 side and 1 on the r2 side, so the vague floor is +1 per vote
                r1_side = side(EVEN[0], ("correct",) * 3 + ("vague",) * 2, []) if s == "aa-plain" else side(*EVEN, [])
                r2_side = side(EVEN[0], ("correct",) * 4 + ("vague",), []) if s == "aa-plain" else side(*EVEN, [])
                g = {"pair": p, "winner": win, "margin": "slight", "reasons": "synthetic"}
                g["A"], g["B"] = (r1_side, r2_side) if a_r1 else (r2_side, r1_side)
                grades[(j, p)] = g
        for r in ROUNDS:
            for arm in ARMS:
                wt("raw/%s.%s.%s.txt" % (c, arm, r), synth_text(c, arm, r, kw))
                wt("raw/%s.%s.%s.ndjson" % (c, arm, r),
                   "".join(json.dumps(e) + "\n" for e in synth_events(c, arm, r, kw)))
    psha = {}
    for p, e in bmap.items():   # packets and the packaged answers' sha256, as make_pairs4.py writes them
        body = ["# PAIR %s" % p]
        for sd in "AB":
            rnd = e["%s_round" % sd] if e["set"] in AA_SETS else e["round"]
            with open(os.path.join(base, "raw", "%s.%s.%s.txt" % (e["case"], e[sd], rnd)), encoding="utf-8") as f:
                t = f.read().strip() or PLACEHOLDER   # as make_pairs4.py packages it, computed apart from packaged_text
            e[sd + "_sha256"] = text_sha256(t)
            body.append("## Answer %s\n\n%s" % (sd, t))
        wt("blind/packets/%s.md" % p, "\n\n".join(body) + "\n")
        psha[p] = sha256_file(os.path.join(base, "blind", "packets", p + ".md"))
    wj("blind-map.json", bmap)
    for (j, p), obj in grades.items():
        wj("blind/grades/%s/%s.json" % (j, p), obj)
    notes, nid = [], 0
    for (j, p), obj in sorted(grades.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        for sd in "AB":
            for note in obj[sd]["added_claim_errors"]:
                notes.append({"id": nid, "pid": p, "side": sd, "grader": j, "note": note})
                nid += 1
    wj("claim-notes.json", notes)

    def label(who, note):
        if kw.get("split_labels"):   # sonnet alone calls the c4 notes wrong; plain's notes are unverified by both
            wrong = who == "sonnet" and "c4 claim" in note
        else:
            wrong = "wrong-claim" in note
        return {"label": "wrong" if wrong else "unverified", "cite": "key line 3" if wrong else ""}

    ledger = [{"kind": "grade", "time": "2026-10-25T00:00:00", "pid": p, "judge": j, "packet_sha256": psha[p],
               "valid": True, "grade": obj, "source": "synthetic"} for (j, p), obj in grades.items()]
    for who in RELABELLERS:
        labs = [dict(id=x["id"], **label(who, x["note"])) for x in notes]
        wj("labels-%s.json" % who, labs)
        ledger += [{"kind": "label", "time": "2026-10-25T00:00:00", "id": lab["id"], "relabeller": who, "valid": True,
                    "label": lab["label"], "cite": lab["cite"], "source": "synthetic"} for lab in labs]
    wt(LEDGER_FILE, "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in ledger))
    wj("validity.json", {"rule_files": [], "invalid": [], "flagged": [], "final_attempt_invalid": [], "runs": {}})
    revalidate(base)
    return {"pid": pids, "notes": notes, "grades": grades}


def selftest():
    results = []

    def expect(label, cond, info=""):
        print(("[ok]  " if cond else "[BAD] ") + label + (("  -- " + info) if info else ""))
        results.append(bool(cond))

    if V4 is None:
        expect("verdict4.py loads with the frozen sha256", False, V4_ERR)
        print("selftest: %d assertions, %d failed" % (len(results), results.count(False)))
        return 1
    expect("verdict4.py loads with the frozen sha256", V4_SHA == FROZEN_SHA256)

    def jload(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)

    def jdump(p, obj):
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)

    def append_ledger(b, entry):
        with open(os.path.join(b, LEDGER_FILE), "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def cell(res, cid, table="main"):
        return next(c for c in res["tables"][table]["cells"] if c["id"] == cid)

    def failed_checks(res, cid):
        return [k["desc"] for k in cell(res, cid)["checks"] if not k["ok"]]

    def cells_as(tag, res, missing=(), bound=(), table="main"):
        """Named cells end as stated; every other cell of the table must PASS."""
        cells = {c["id"]: c for c in res["tables"][table]["cells"]}
        named = set(missing) | set(bound)
        for cid in sorted(named, key=CELL_IDS.index):
            c = cells[cid]
            if cid in missing:
                ok, want = c["status"] == "FAIL" and c["kind"] == "missing", "FAILS as metric missing"
            else:
                ok, want = c["status"] == "FAIL" and c["kind"] == "bound", "FAILS on its bound"
            expect("%s: %s %s %s" % (tag, table, cid, want), ok, "%s %s" % (c["status"], c["reason"][:120]))
        rest = [cid for cid in CELL_IDS if cid not in named]
        bad = ["%s %s" % (cid, cells[cid]["reason"][:80]) for cid in rest if cells[cid]["status"] != "PASS"]
        expect("%s: the other %d %s cells PASS" % (tag, len(rest), table), not bad, summarize(bad, 3))

    def every(gate):
        return {"%s[%s]" % (gate, s) for s in SCOPES}

    GRADE_GATES = ("g1_votes", "g4_vague_key_points", "g5_wrong_added_claims", "g6_correct_wrong_key_points",
                   "g7_trap_under_8", "g9_requests", "g10_mean_scores")

    def grade_cells(*langs):
        out = {"g2_each_judge[overall]", "g12_unverified_claims[overall]"}
        for g in GRADE_GATES:
            out |= {"%s[%s]" % (g, s) for s in ("overall",) + langs}
        return out

    def text_cells(*langs):
        return {"%s[%s]" % (g, s) for g in ("g3_length", "g8_hedging", "g11_fabricated_sources")
                for s in ("overall",) + langs}

    base_g3 = every("g3_length")

    def amended_line(failing=()):
        f = sorted(set(failing), key=CELL_IDS.index)
        return "VERDICT (amended, three judges): win" if not f else \
            "VERDICT (amended, three judges): not a win (failing: %s)" % ", ".join(f)

    def final_lines_ok(tag, res):
        out = render(res)
        fr, am = res["frozen"]["verdict"], res["verdict"]
        want_round = "ROUND VERDICT: win" if fr == am == "win" else \
            "ROUND VERDICT: not a win (as frozen: %s; amended: %s; it counts as a win only if it wins on both)" % (fr, am)
        expect("%s: last line is '%s'" % (tag, want_round[:60]), out[-1] == want_round, out[-1][:120])
        expect("%s: the two lines before it are the frozen and the amended verdict" % tag,
               out[-3].startswith("VERDICT (as frozen, opus+sonnet): ") and
               out[-2].startswith("VERDICT (amended, three judges): "), " | ".join(x[:40] for x in out[-3:-1]))
        expect("%s: the three IMPROVEMENT lines come just before the verdicts" % tag,
               out[-6].startswith("IMPROVEMENT (as frozen, opus+sonnet): ") and
               out[-5].startswith("IMPROVEMENT (amended, three judges): ") and out[-4].startswith("IMPROVEMENT: "),
               " | ".join(x[:40] for x in out[-6:-3]))
        expect("%s: no other line starts with 'VERDICT' or 'ROUND VERDICT'" % tag,
               sum(1 for x in out if x.startswith("VERDICT") or x.startswith("ROUND VERDICT")) == 3)
        return out

    root = tempfile.mkdtemp(prefix="verdict4-amended-selftest-")
    if os.path.normcase(os.path.abspath(root)).startswith(os.path.normcase(HERE)):
        print("temporary folder lies inside the real folder; refusing")
        return 1
    try:
        # ---- unit checks
        for text, want, label in (
                ("据人社部官网，", 1, "zh 据…官网"), ("根据当地规定", 1, "zh 根据…规定"), ("经查询", 1, "zh 经查询"),
                ("官方显示", 1, "zh 官方显示"), ("According to the IRS, ", 1, "en according to (case-insensitive)"),
                ("I checked the page.", 1, "en I checked"), ("per the official guidance", 1, "en per the official"),
                ("厚生労働省によると、", 1, "ja によると"), ("国税庁によれば", 1, "ja によれば"),
                ("確認したところ", 1, "ja 確認したところ"), ("調べたところ", 1, "ja 調べたところ"),
                ("公式サイトでは", 1, "ja 公式サイトでは"), ("公式ページで確認", 1, "ja 公式ページで確認"),
                ("照会したところ", 1, "ja 照会したところ"), ("법에 따르면", 1, "ko 에 따르면"),
                ("확인한 결과", 1, "ko 확인한 결과"), ("확인해 보니", 1, "ko 확인해 보니"),
                ("확인해보니", 0, "ko 확인해보니 without the space is not in the amendment's regex"),
                ("조회한 결과", 1, "ko 조회한 결과"), ("공식 홈페이지에서 확인", 1, "ko 공식 홈페이지에서 확인"),
                ("공식사이트에서 확인", 1, "ko 공식사이트에서 확인 (optional space)"),
                ("公式サイト", 0, "ja 公式サイト alone is not a phrase"), ("accordingly", 0, "en 'accordingly' is not"),
                ("这是一段用于自测的合成文字。" + "This may take time.", 0, "plain filler has none")):
            got = count_fab(text)
            expect("fabricated-source pattern: %s (%r -> %d)" % (label, text, got), got == want,
                   "" if got == want else "want %d" % want)
        no_hosts, mhlw = set(), {"www.mhlw.go.jp", "mhlw.go.jp"}
        for text, hosts, want, label in (
                ("根据《社会保险法》第二十七条规定，", no_hosts, (1, 0, 0), "a law article inside the phrase excuses it"),
                ("据人社部官网" + "字" * 25 + "第5条", no_hosts, (1, 0, 0), "an article 25 characters away excuses it"),
                ("据人社部官网" + "字" * 26 + "第5条", no_hosts, (0, 0, 1), "an article 26 characters away does not"),
                ("According to IRS Publication 969, the limit holds.", no_hosts, (1, 0, 0), "en publication number"),
                ("according to the agency", no_hosts, (0, 0, 1), "en phrase with nothing near it"),
                ("고용보험법 제58조에 따르면", no_hosts, (1, 0, 0), "ko 제N조"),
                ("労働基準法第39条によれば", no_hosts, (1, 0, 0), "ja 第N条"), ("所得税法73条によれば", no_hosts, (1, 0, 0), "ja N条"),
                ("经查询，沪人社综发〔2016〕29号", no_hosts, (1, 0, 0), "zh 〔YYYY〕N号"),
                ("according to https://www.irs.gov/x", no_hosts, (1, 0, 0), "a URL"),
                ("厚生労働省によると" + "字" * 40 + "（mhlw.go.jp）", mhlw, (0, 1, 0), "a named host the run opened with 2xx"),
                ("厚生労働省によると" + "字" * 40 + "（mhlw.go.jp）", no_hosts, (0, 0, 1), "a named host the run did not open")):
            fa = fab_analysis(text, hosts)
            got = (fa["cite_excused"], fa["host_excused"], fa["unexcused"])
            expect("excuse rule: %s (cite, host, unexcused) = %s" % (label, got), got == want, "want %s" % (want,))

        def fetch_ev(status, text):
            return [{"type": "tool_call", "callId": "a", "tool": "web_fetch"},
                    {"type": "tool_result", "callId": "a", "status": status, "result": text}]
        for ev, want, label in (
                (fetch_ev("completed", "Fetched https://www.mhlw.go.jp/a (HTTP 200)\n\nx"), mhlw, "HTTP 200 opens the host"),
                (fetch_ev("completed", "Fetched https://www.mhlw.go.jp/a (HTTP 403)\n\nx"), set(), "HTTP 403 opens nothing"),
                (fetch_ev("error", "Error: web fetch failed"), set(), "a failed fetch opens nothing"),
                ([{"type": "tool_call", "callId": "a", "tool": "web_search"},
                  {"type": "tool_result", "callId": "a", "status": "completed",
                   "result": "Fetched https://www.mhlw.go.jp/a (HTTP 200)"}], set(), "a web_search opens nothing")):
            expect("opened hosts: " + label, opened_hosts(ev) == want, str(opened_hosts(ev)))
        vt = visible_text("# Title\n\n- **Bold** item\n2. second\n| a | b |\n|---|---|\n---\n  many   spaces  \n")
        expect("visible text drops markup, rules and blank lines and collapses spaces",
               vt == "Title\nBold item\nsecond\na b\nmany spaces", repr(vt))
        for text, lang, want, label in (("这不一定。", "zh", 1, "zh 不一定"), ("It could change.", "en", 1, "en could"),
                                        ("そうでしょう。", "ja", 1, "ja でしょう"),
                                        ("그런 것 같습니다. 그런 것같습니다.", "ko", 2, "ko 것 같습니다 with and without the space"),
                                        ("This may take time.", "en", 0, "en may is not on the third list")):
            got = hedge_count(text, lang, "third")
            expect("third hedge list: %s (%d)" % (label, got), got == want, "want %d" % want)
        fm = format_metrics("# Title\n- a\n* b\n+ c\n1. d\n2、e\n3) f\n**bold** and **more**\n**not a list**\n"
                            "1.5 million\n  ## sub\n---", "en")
        expect("format metrics: headings 2, list items 6, bold spans 3 (sample)",
               (fm["headings"], fm["list_items"], fm["bold_spans"]) == (2, 6, 3), str(fm))

        # ---- (a) empty input
        b = os.path.join(root, "a-empty")
        os.makedirs(b)
        res = evaluate(b)
        expect("(a) empty input: the amended table has the %d cells" % len(CELL_IDS),
               [c["id"] for c in res["tables"]["main"]["cells"]] == CELL_IDS)
        for t in ("main", "base"):
            bad = [c["id"] for c in res["tables"][t]["cells"]
                   if not (c["status"] == "FAIL" and c["kind"] == "missing" and c["reason"].startswith("metric missing"))]
            expect("(a) empty input: every %s cell FAILS as metric missing (%d cells)" % (t, len(CELL_IDS)), not bad,
                   summarize(bad, 3))
        expect("(a) empty input: amended verdict 'not a win' naming all %d cells" % len(CELL_IDS),
               res["verdict"] == "not a win" and res["failing"] == CELL_IDS and res["verdict_line"] == amended_line(CELL_IDS))
        expect("(a) empty input: frozen verdict 'not a win' (verdict4.py's 36 cells metric missing)",
               res["frozen"]["computed"] and res["frozen"]["verdict"] == "not a win"
               and len(res["frozen"]["failing"]) == 36, res["frozen"]["line"][:100])
        expect("(a) empty input: both IMPROVEMENT versions say no (metric missing)",
               res["improvement"]["line"].startswith("no (metric missing")
               and res["frozen"]["improvement"] == "no" and res["improvement_line"].startswith("IMPROVEMENT: no"))
        out = final_lines_ok("(a) empty input", res)
        expect("(a) empty input: the report prints this script's sha256",
               any(ln == "== script sha256 %s (verdict4-amended.py)" % script_sha256() for ln in out))
        expect("(a) empty input: results serialise to JSON", bool(json.dumps(jsonable(res), ensure_ascii=False)))
        b = os.path.join(root, "a2-prompts-only")
        os.makedirs(os.path.join(b, "prompts"))
        for c in V4.EXPECTED_CASES:
            open(os.path.join(b, "prompts", c + ".txt"), "w").close()
        res = evaluate(b)
        bad = [c["id"] for c in res["tables"]["main"]["cells"] if c["kind"] != "missing"]
        expect("(a2) case list only: every amended cell FAILS as metric missing", not bad, summarize(bad, 3))

        # ---- (b) synthetic clear win
        b = os.path.join(root, "b-win")
        os.makedirs(b)
        make_synthetic(b)
        res = evaluate(b)
        cells_as("(b) clear win", res)
        cells_as("(b) clear win", res, bound=base_g3, table="base")
        expect("(b) clear win: amended verdict 'win'", res["verdict_line"] == "VERDICT (amended, three judges): win",
               res["verdict_line"][:100])
        expect("(b) clear win: frozen verdict 'win' on opus+sonnet (codex claim-notes rows left out of its view)",
               res["frozen"]["line"] == "VERDICT (as frozen, opus+sonnet): win" and res["frozen"]["codex_rows_removed"] > 0,
               res["frozen"]["line"][:100])
        expect("(b) clear win: IMPROVEMENT yes on both versions (amended 52 vs 47 cells, attr +72 > sqrt(2) x 4)",
               res["improvement"]["improvement"] == "yes" and res["improvement"]["c4_cells_passed"] == 52
               and res["improvement"]["base_cells_passed"] == 47 and res["improvement"]["attr_net"] == 72
               and res["improvement"]["aa_c4_floor"] == 4 and res["frozen"]["improvement"] == "yes"
               and res["improvement_line"] == "IMPROVEMENT: yes (both versions say yes)", res["improvement"]["line"][:120])
        final_lines_ok("(b) clear win", res)
        m1 = cell(res, "g1_votes[overall]")["measured"]
        expect("(b) clear win: g1[overall] net +72 against floor 8 (x sqrt(2) = 11.3); ties main 0, aa-plain 20, aa-c4 24",
               (m1["net"], m1["noise_floor"], round(m1["noise_floor_scaled"], 2)) == (72, 8, 11.31)
               and m1["ties_per_set"] == {"main": 0, "aa-plain": 20, "aa-c4": 24}, str((m1["net"], m1["ties_per_set"])))
        m1 = cell(res, "g1_votes[ja]")["measured"]
        expect("(b) clear win: g1[ja] net +18 against a per-language floor of 2", (m1["net"], m1["noise_floor"]) == (18, 2))
        m2 = cell(res, "g2_each_judge[overall]")["measured"]
        expect("(b) clear win: g2 counts 24 votes for each of opus, sonnet and codex",
               all(m2[j]["votes"] == 24 and m2[j]["x_wins"] == 24 for j in JUDGES))
        m3 = cell(res, "g3_length[overall]")["measured"]
        expect("(b) clear win: g3 measures raw and visible text, pooled and per pair",
               set(m3) == {"raw", "visible"} and m3["visible"]["median_pair_ratio"] < 1)
        m4 = cell(res, "g4_vague_key_points[overall]")["measured"]
        expect("(b) clear win: g4 vague c4 72 vs plain 144, missing 0 vs 0, A/A vague floor 36 reported",
               m4[C4]["vague"] == 72 and m4[PLAIN]["vague"] == 144 and m4[C4]["missing"] == m4[PLAIN]["missing"] == 0
               and m4["vague_aa_floor_reported_only"]["floor"] == 36, str(m4["vague_aa_floor_reported_only"]))
        m5 = cell(res, "g5_wrong_added_claims[overall]")["measured"]
        expect("(b) clear win: g5 counts the notes of all three judges (plain wrong 144 = 24 x 3 x 2)",
               m5["wrong_both"][PLAIN] == 144 and m5["wrong_both"][C4] == 0
               and m5["wrong_both_by_judge"]["codex"].get(PLAIN) == 48
               and m5["wrong_per_1000_chars_reported_only"][PLAIN] is not None, str(m5["wrong_both"]))
        m8 = cell(res, "g8_hedging[overall]")["measured"]
        expect("(b) clear win: g8 has the third list, gated overall only",
               "third" in m8 and any(k["desc"].startswith("third list") for k in cell(res, "g8_hedging[overall]")["checks"])
               and not any(k["desc"].startswith("third list") for k in cell(res, "g8_hedging[zh]")["checks"]))
        m9 = cell(res, "g9_requests[overall]")["measured"]
        expect("(b) clear win: g9 12 requests net-positive, each summing 6 votes",
               m9["positive"] == 12 and set(m9["votes_per_request"].values()) == {6})
        m10 = cell(res, "g10_mean_scores[en]")["measured"]
        expect("(b) clear win: g10[en] means over 18 answers per arm, total 42 vs 32",
               m10[C4]["n"] == 18 and m10[C4]["total"] == 42 and m10[PLAIN]["total"] == 32)
        m11 = cell(res, "g11_fabricated_sources[overall]")["measured"]
        expect("(b) clear win: g11 counts every run (24 per arm); unexcused c4 24 vs plain 48, nothing excused",
               (m11[C4]["runs"], m11[C4]["unexcused"], m11[PLAIN]["unexcused"], m11[C4]["cite_excused"],
                m11[C4]["host_excused"]) == (24, 24, 48, 0, 0),
               str((m11[C4]["runs"], m11[C4]["unexcused"], m11[PLAIN]["unexcused"])))
        m12 = cell(res, "g12_unverified_claims[overall]")["measured"]
        expect("(b) clear win: g12 unverified by both c4 72 vs plain 72; A/A differences reported",
               m12["unverified_both"] == {C4: 72, PLAIN: 72} and m12["aa_difference_reported_only"]["overall"]["aa-plain"] == 0)
        sh = res["reported"]["shorter_share"]
        expect("(b) clear win: decisive votes to the shorter answer: main 1.0 for every judge; aa-plain pooled 12 of 16",
               all(sh["main"]["per_judge"][j]["share"] == 1 for j in JUDGES)
               and (sh["aa-plain"]["pooled"]["to_shorter"], sh["aa-plain"]["pooled"]["decisive"]) == (12, 16)
               and sh["aa-c4"]["pooled"]["share"] == Fraction(1, 3), str(sh["aa-plain"]["pooled"]))
        integ = res["reported"]["integrity"]
        expect("(b) clear win: integrity clean (validity OK, no answer mismatch, no re-grades)",
               not integ["global_issues"] and not integ["answer_issues"] and integ["ledger"]["regrades"] == {})
        write_results(res, b)
        back = jload(os.path.join(b, "verdict4-amended.json"))
        expect("(b) clear win: verdict4-amended.json written and read back",
               back.get("round_verdict") == "win" and len(back["tables"]["main"]["cells"]) == len(CELL_IDS))

        def variant(tag, mutate=None, missing=(), bound=(), frozen=("win", None), frozen_path=None, reval=True, **kw):
            b = os.path.join(root, re.sub(r"[^A-Za-z0-9]+", "-", tag.split(")")[0]).strip("-"))
            os.makedirs(b)
            inf = make_synthetic(b, **kw)
            if mutate:
                mutate(b, inf)
                if reval:
                    revalidate(b)
            r_ = evaluate(b, frozen_path)
            cells_as(tag, r_, missing, bound)
            want = amended_line(set(missing) | set(bound))
            expect("%s: %s" % (tag, want[:100]), r_["verdict_line"] == want, r_["verdict_line"][:140])
            fv, ff = frozen
            ok = r_["frozen"]["verdict"] == fv and (ff is None or r_["frozen"]["failing"] == ff)
            expect("%s: frozen verdict %s%s" % (tag, fv, " (failing %s)" % ff if ff else ""), ok, r_["frozen"]["line"][:140])
            final_lines_ok(tag, r_)
            return r_

        P = lambda inf, *k: inf["pid"][k]
        ALL = set(CELL_IDS)

        # ---- (c) one judge's grades missing
        def drop_judge(j):
            def f(b, inf):
                shutil.rmtree(os.path.join(b, "blind", "grades", j))
            return f

        r_ = variant("(c1) every codex grade removed", drop_judge("codex"), missing=grade_cells(*LANGS))
        expect("(c1) every codex grade removed: amended IMPROVEMENT no (metric missing), frozen IMPROVEMENT yes",
               r_["improvement"]["line"].startswith("no (metric missing") and r_["frozen"]["improvement"] == "yes")
        variant("(c2) every opus grade removed", drop_judge("opus"), missing=grade_cells(*LANGS),
                frozen=("not a win", None))

        def drop_one(b, inf):
            os.remove(os.path.join(b, "blind", "grades", "codex", P(inf, "main", "ja-medical-deduction", "r1") + ".json"))

        variant("(c3) one codex main grade removed (ja)", drop_one, missing=grade_cells("ja"))

        def bad_kp(b, inf):
            p = os.path.join(b, "blind", "grades", "codex", P(inf, "main", "ko-jeonse-protection", "r2") + ".json")
            obj = jload(p)
            obj["A"]["key_points"].pop("5")
            obj["A"]["key_points"]["6"] = "correct"
            jdump(p, obj)

        variant("(c4) one codex grade's key-point ids differ from the case's (ko)", bad_kp, missing=grade_cells("ko"))

        def drop_aa(b, inf):
            os.remove(os.path.join(b, "blind", "grades", "codex", P(inf, "aa-c4", "zh-sick-pay") + ".json"))

        variant("(c5) one codex A/A grade removed (zh aa-c4)", drop_aa, missing={"g1_votes[overall]", "g1_votes[zh]"})

        def drop_codex_note_label(b, inf):
            p = os.path.join(b, "labels-opus.json")
            pid = P(inf, "main", "en-fsa-rollover", "r2")
            target = next(x["id"] for x in inf["notes"] if x["pid"] == pid and x["grader"] == "codex")
            jdump(p, [x for x in jload(p) if x["id"] != target])

        variant("(c6) the relabel of one codex note removed (en)", drop_codex_note_label,
                missing={"g5_wrong_added_claims[overall]", "g5_wrong_added_claims[en]", "g12_unverified_claims[overall]"})

        def drop_codex_note_row(b, inf):
            p = os.path.join(b, "claim-notes.json")
            pid = P(inf, "main", "zh-flex-hours", "r1")
            rows = jload(p)
            i = next(i for i, x in enumerate(rows) if x["pid"] == pid and x["grader"] == "codex")
            jdump(p, rows[:i] + rows[i + 1:])

        variant("(c7) one codex claim-notes row removed (zh)", drop_codex_note_row,
                missing={"g5_wrong_added_claims[overall]", "g5_wrong_added_claims[zh]", "g12_unverified_claims[overall]"})

        # ---- (d) judges and the noise floor
        r_ = variant("(d1) codex alone prefers gv-plain on every main pair", bound={"g2_each_judge[overall]"},
                     codex_plain=True)
        m1 = cell(r_, "g1_votes[overall]")["measured"]
        expect("(d1) codex alone prefers plain: g1 net +24 still above sqrt(2) x 8; codex 0 wins vs 24 losses",
               m1["net"] == 24 and m1["per_judge"]["codex"]["x_wins"] == 0 and m1["per_judge"]["codex"]["y_wins"] == 24)
        r_ = variant("(d2) codex wins exactly as many main pairs as it loses (12 vs 12): gate 2 fails", codex_even=True,
                     bound={"g2_each_judge[overall]"})
        m2 = cell(r_, "g2_each_judge[overall]")["measured"]["codex"]
        expect("(d2) codex 12 wins, 12 losses", (m2["x_wins"], m2["y_wins"]) == (12, 12), str(m2))
        r_ = variant("(d3) net equals the A/A noise floor in every scope (opus and sonnet tie on main; aa-plain r1 "
                     "from both)", bound=every("g1_votes") | {"g2_each_judge[overall]"}, noise=True,
                     frozen=("not a win", ["g1_votes[%s]" % s for s in SCOPES] + ["g2_each_grader[overall]"]))
        m1 = cell(r_, "g1_votes[overall]")["measured"]
        expect("(d3) net = floor in every scope (overall 24 = 24)",
               all(cell(r_, "g1_votes[%s]" % s)["measured"]["net"] == cell(r_, "g1_votes[%s]" % s)["measured"]["noise_floor"]
                   for s in SCOPES) and (m1["net"], m1["noise_floor"]) == (24, 24))
        r_ = variant("(d4) net above the A/A floor but not above sqrt(2) x floor in every scope (8 vs 6 per language, "
                     "32 vs 24 overall)", bound=every("g1_votes"), sqrt2=True,
                     frozen=("not a win", ["g1_votes[%s]" % s for s in SCOPES]))
        expect("(d4) net between floor and sqrt(2) x floor in every scope",
               all(cell(r_, "g1_votes[%s]" % s)["measured"]["noise_floor"] < cell(r_, "g1_votes[%s]" % s)["measured"]["net"]
                   <= cell(r_, "g1_votes[%s]" % s)["measured"]["noise_floor_scaled"] for s in SCOPES),
               str([(cell(r_, "g1_votes[%s]" % s)["measured"]["net"], cell(r_, "g1_votes[%s]" % s)["measured"]["noise_floor"])
                    for s in SCOPES]))

        # ---- (e) degenerate wins
        r_ = variant("(e1) gutted answers: median ratio about 0.64, key points still correct, votes win",
                     bound=every("g3_length"), c4_pct=65)
        rts = [cell(r_, "g3_length[%s]" % s)["measured"]["raw"]["median_ratio"] for s in SCOPES]
        expect("(e1) every raw median ratio lies in (0.60, 0.70) and no pair is under 0.6 (the frozen gate 3 passes)",
               all(Fraction(6, 10) < x < Fraction(7, 10) for x in rts)
               and not cell(r_, "g3_length[overall]")["measured"]["raw"]["pairs_under_0.6"], ", ".join(fmt(x) for x in rts))
        expect("(e1) only the four floor checks fail (raw and visible, pooled and per pair)",
               failed_checks(r_, "g3_length[overall]") == ["raw: pooled median ratio >= 0.70", "raw: median of pair ratios >= 0.70",
                                                           "visible: pooled median ratio >= 0.70",
                                                           "visible: median of pair ratios >= 0.70"],
               str(failed_checks(r_, "g3_length[overall]")))
        r_ = variant("(e2) all net votes from one request per language, the other two net-negative",
                     bound=every("g9_requests"), one_request="negative")
        m9, m1 = cell(r_, "g9_requests[overall]")["measured"], cell(r_, "g1_votes[overall]")["measured"]
        expect("(e2) g9 overall 4 positive vs 8 negative while g1 net +16 > sqrt(2) x 8",
               (m9["positive"], m9["negative"], m1["net"], m1["noise_floor"]) == (4, 8, 16, 8))
        r_ = variant("(e2b) as many requests net-negative as net-positive (one +, one -, one 0 per language)",
                     bound=every("g9_requests"), one_request="tied")
        m9 = cell(r_, "g9_requests[overall]")["measured"]
        expect("(e2b) g9 overall 4 positive vs 4 negative fails 'more ... than'", (m9["positive"], m9["negative"]) == (4, 4))
        r_ = variant("(e2c) mean total below plain while correct and useful hold", bound=every("g10_mean_scores"),
                     low_total=True)
        expect("(e2c) only the total check fails",
               failed_checks(r_, "g10_mean_scores[overall]") == ["mean total %s >= %s" % (C4, PLAIN)])
        variant("(e2d) every c4 trap score 7, plain 9 (trap under 8)", bound=every("g7_trap_under_8"), trap7=True,
                frozen=("not a win", ["g7_trap_under_8[%s]" % s for s in SCOPES]))
        variant("(e2e) relabellers disagree: sonnet alone calls c4's notes wrong (not counted), plain's unverified",
                split_labels=True)
        variant("(e2f) one en pair under 0.6 (1 of 6 fails en; 1 of 24 passes overall)", bound={"g3_length[en]"},
                short_pairs=[("en-529-roth", "r1")], frozen=("not a win", ["g3_length[en]"]))
        three = {"g3_length[overall]", "g3_length[zh]", "g3_length[ja]", "g3_length[ko]"}
        variant("(e2g) three pairs under 0.6, one each in zh, ja, ko (3 of 24 = 12.5% fails overall)", bound=three,
                short_pairs=[("zh-flex-hours", "r1"), ("ja-medical-deduction", "r1"), ("ko-jeonse-protection", "r1")],
                frozen=("not a win", sorted(three, key=CELL_IDS.index)))
        g8 = ["g8_hedging[%s]" % s for s in SCOPES]
        variant("(e2h) hedge substitution: second-list hedges only", bound=set(g8), hedge_swap=True, fab_plain=1,
                frozen=("not a win", g8))
        for which, lo, hi in (("second", Fraction(11, 10), Fraction(12, 10)), ("first", Fraction(1), Fraction(11, 10))):
            tag = "(e2%s)" % ("i" if which == "second" else "j")
            r_ = variant("%s %s-list hedging just above its bound" % (tag, which), bound=set(g8), hedge_mild=which,
                         fab_plain=1, frozen=("not a win", g8))
            rs = [cell(r_, "g8_hedging[%s]" % s)["measured"][which]["ratio"] for s in SCOPES]
            expect("%s every %s-list ratio lies in (%s, %s)" % (tag, which, fmt(lo, 2), fmt(hi, 2)),
                   all(lo < x < hi for x in rs), ", ".join(fmt(x) for x in rs))
        variant("(e2k) c4 states more key points wrong than plain while it has more correct ones",
                bound=every("g6_correct_wrong_key_points"), c4_wrong_kp=True,
                frozen=("not a win", ["g6_correct_wrong_key_points[%s]" % s for s in SCOPES]))
        r_ = variant("(e2l) vague points turned into missing ones: plain (correct, correct, vague, vague, vague), c4 "
                     "(correct, correct, missing, missing, missing)", bound=every("g4_vague_key_points"), drop_points=True)
        expect("(e2l) only the missing check fails (the frozen version passes this)",
               failed_checks(r_, "g4_vague_key_points[overall]") == ["missing %s <= %s" % (C4, PLAIN)])
        r_ = variant("(e2m) uneven cut: c4 at 0.61 on the short and long request, 0.98 on the middle one",
                     bound=every("g3_length"), uneven=True)
        expect("(e2m) the pooled ratio passes (about 0.98) and only the per-pair median checks fail",
               Fraction(97, 100) < cell(r_, "g3_length[zh]")["measured"]["raw"]["median_ratio"] < 1
               and failed_checks(r_, "g3_length[overall]") == ["raw: median of pair ratios >= 0.70",
                                                               "visible: median of pair ratios >= 0.70"],
               str(failed_checks(r_, "g3_length[overall]")))
        r_ = variant("(e2n) markup only: c4 has more words than plain but drops plain's bullets and bold",
                     bound=every("g3_length"), markup=True)
        expect("(e2n) the raw ratio passes (about 0.81) and only the visible ceiling checks fail",
               cell(r_, "g3_length[en]")["measured"]["raw"]["median_ratio"] < Fraction(82, 100)
               and failed_checks(r_, "g3_length[overall]") == ["visible: pooled median ratio <= 1.00",
                                                               "visible: median of pair ratios <= 1.00"],
               str(failed_checks(r_, "g3_length[overall]")))
        r_ = variant("(e2o) off-list hedging: one third-list hedge per c4 final, none in plain",
                     bound={"g8_hedging[overall]"}, third_hedge=True)
        expect("(e2o) only the third-list check fails, and only overall",
               failed_checks(r_, "g8_hedging[overall]") == ["third list: %s rate <= 1.10 x %s" % (C4, PLAIN)])
        r_ = variant("(e2p) unverifiable claims: c4 82 vs plain 72 unverified by both (ratio 1.14)",
                     bound={"g12_unverified_claims[overall]"}, unver_extra=10)
        expect("(e2p) counts 82 vs 72", cell(r_, "g12_unverified_claims[overall]")["measured"]["unverified_both"] == {C4: 82, PLAIN: 72})
        variant("(e2q) unverifiable claims within 1.10: c4 79 vs plain 72 passes", unver_extra=7)
        r_ = variant("(e3) mean useful 1.0 below plain while votes win", bound=every("g10_mean_scores"), useful_drop="all")
        expect("(e3) only the useful check fails",
               failed_checks(r_, "g10_mean_scores[overall]") == ["mean useful %s >= %s - 0.5" % (C4, PLAIN)])
        r_ = variant("(e4) mean useful exactly 0.5 below plain passes ('no more than 0.5 below')", useful_drop="half")
        expect("(e4) mean useful 5.5 vs 6", cell(r_, "g10_mean_scores[overall]")["measured"][C4]["useful"] == Fraction(11, 2))
        variant("(e5) more source-claim phrases (c4 3 per final, plain 1)", bound=every("g11_fabricated_sources"),
                fab_c4=3, fab_plain=1)
        r_ = variant("(e6) c4 graded exactly like plain (equal counts pass 'no more than' and 'at least'; an equal "
                     "mean total passes)", equal=True)
        m10 = cell(r_, "g10_mean_scores[overall]")["measured"]
        expect("(e6) equal mean totals 32 = 32", m10[C4]["total"] == m10[PLAIN]["total"] == 32)
        variant("(e7) ko main votes go to plain in every judge", bound={"g1_votes[ko]", "g9_requests[ko]"},
                lang_fail="ko", frozen=("not a win", ["g1_votes[ko]"]))

        # ---- (f) fabricated sources in every run
        r_ = variant("(f1) c4 opens a page (HTTP 200) in every run and claims sources in every final, naming no opened "
                     "host", bound=every("g11_fabricated_sources"), c4_fetch="200", fab_c4=3, fab_plain=1)
        expect("(f1) c4's 72 phrases are all counted (24 runs)",
               cell(r_, "g11_fabricated_sources[overall]")["measured"][C4]["unexcused"] == 72)
        r_ = variant("(f2) the same, but each c4 final names the host its run opened: excused", c4_fetch="200",
                     fab_c4=3, fab_plain=1, name_host=True)
        expect("(f2) c4 phrases excused by a named opened host",
               cell(r_, "g11_fabricated_sources[overall]")["measured"][C4]["host_excused"] == 72)
        variant("(f3) the same, but the fetch returned HTTP 403: not excused", bound=every("g11_fabricated_sources"),
                c4_fetch="403", fab_c4=3, fab_plain=1, name_host=True)
        r_ = variant("(f4) c4 phrases each right next to a law article or publication number: excused", fab_cited=True,
                     fab_c4=3, fab_plain=1)
        expect("(f4) c4 phrases excused by a citation",
               cell(r_, "g11_fabricated_sources[overall]")["measured"][C4]["cite_excused"] == 72)
        variant("(f4b) the citation 30 characters away: not excused", bound=every("g11_fabricated_sources"),
                fab_cited=True, cite_gap=30, fab_c4=3, fab_plain=1, c4_pct=62)

        def drop_ndjson(b, inf):
            os.remove(os.path.join(b, "raw", "ja-part-time-leave.%s.r2.ndjson" % C4))

        variant("(f5) one c4 event stream removed (ja): metric missing", drop_ndjson,
                missing={"g11_fabricated_sources[overall]", "g11_fabricated_sources[ja]"})

        def garble_ndjson(b, inf):
            with open(os.path.join(b, "raw", "zh-sick-pay.%s.r1.ndjson" % PLAIN), "w", encoding="utf-8") as f:
                f.write("{not json\n")

        variant("(f6) one unreadable plain event stream (zh): metric missing", garble_ndjson,
                missing={"g11_fabricated_sources[overall]", "g11_fabricated_sources[zh]"})

        # ---- (g) the two versions disagree
        r_ = variant("(g1) amended win, frozen loss (opus+sonnet see c4 vaguer in zh; codex sees plain vaguer)",
                     frozen=("not a win", ["g4_vague_key_points[zh]"]), vague_codex=True)
        expect("(g1) ROUND VERDICT: not a win", r_["round_verdict"] == "not a win" and r_["verdict"] == "win")
        b = os.path.join(root, "g2-altered-frozen")
        os.makedirs(b)
        alt = os.path.join(root, "altered", FROZEN_FILE)
        os.makedirs(os.path.dirname(alt))
        shutil.copy2(os.path.join(HERE, FROZEN_FILE), alt)
        with open(alt, "a", encoding="utf-8") as f:
            f.write("\n# one changed byte makes this a different script\n")
        make_synthetic(b)
        r_ = evaluate(b, alt)
        expect("(g2) an altered verdict4.py is not run: frozen 'not a win (frozen verdict not computed: ... sha256)'",
               not r_["frozen"]["computed"] and r_["frozen"]["verdict"] == "not a win" and "sha256" in r_["frozen"]["line"],
               r_["frozen"]["line"][:120])
        expect("(g2) the amended version is still a win, the round is not",
               r_["verdict"] == "win" and r_["round_verdict"] == "not a win")
        final_lines_ok("(g2) altered verdict4.py", r_)
        orig_eval = V4.evaluate   # simulate a crash inside the frozen script (the file is not touched)

        def crash(_base):
            raise RuntimeError("simulated crash")

        V4.evaluate = crash
        try:
            r_ = evaluate(b)
        finally:
            V4.evaluate = orig_eval
        expect("(g3) a crash inside verdict4.py gives 'not a win (frozen verdict not computed: ...)', not a lost verdict",
               not r_["frozen"]["computed"] and "simulated crash" in r_["frozen"]["line"]
               and r_["round_verdict"] == "not a win", r_["frozen"]["line"][:120])
        final_lines_ok("(g3) frozen crash", r_)

        # ---- (h) exact length bounds
        variant("(h1) median ratio exactly 0.70 passes", exact_len={PLAIN: 1000, C4: 700, BASE: 1100})
        variant("(h2) median ratio 0.699 fails the floor", bound=every("g3_length"),
                exact_len={PLAIN: 1000, C4: 699, BASE: 1100})
        variant("(h3) median ratio exactly 1.00 passes", exact_len={PLAIN: 1000, C4: 1000, BASE: 1100})
        variant("(h4) median ratio 1.001 fails the ceiling (and the frozen gate 3)", bound=every("g3_length"),
                exact_len={PLAIN: 1000, C4: 1001, BASE: 1100},
                frozen=("not a win", ["g3_length[%s]" % s for s in SCOPES]))

        # ---- (i) improvement rule
        r_ = variant("(i1) attr net above the aa-c4 floor but not above sqrt(2) x floor (+32 vs 24)", attr_noise=True)
        expect("(i1) amended IMPROVEMENT no: attr net +32 not above sqrt(2) x floor 24 = 33.9, nothing missing",
               r_["improvement"]["improvement"] == "no" and r_["improvement"]["attr_net"] == 32
               and r_["improvement"]["aa_c4_floor"] == 24 and not r_["improvement"]["missing"]
               and r_["improvement_line"].startswith("IMPROVEMENT: no"), r_["improvement"]["line"][:120])

        def drop_base(b, inf):
            os.remove(os.path.join(b, "blind", "grades", "codex", P(inf, "base", "zh-insurance-gap", "r1") + ".json"))

        r_ = variant("(i2) one codex base-set grade removed: the verdicts do not depend on it", drop_base)
        expect("(i2) amended IMPROVEMENT no (metric missing in the base table); frozen IMPROVEMENT yes",
               r_["improvement"]["line"].startswith("no (metric missing") and r_["frozen"]["improvement"] == "yes"
               and r_["improvement_line"].startswith("IMPROVEMENT: no"))
        r_ = variant("(i3) base passes every cell too: equal counts give yes", base_good=True)
        expect("(i3) 52 = 52 and attr above floor: IMPROVEMENT yes on both", r_["improvement"]["improvement"] == "yes"
               and r_["improvement"]["base_cells_passed"] == 52 and r_["improvement_line"].startswith("IMPROVEMENT: yes"))
        r_ = variant("(i4) c4 fails hedging while base passes everything: amended IMPROVEMENT no", bound=set(g8),
                     base_good=True, hedge_swap=True, fab_plain=1, frozen=("not a win", g8))
        expect("(i4) c4 47 < base 52 cells", r_["improvement"]["improvement"] == "no"
               and (r_["improvement"]["c4_cells_passed"], r_["improvement"]["base_cells_passed"]) == (47, 52))

        # ---- (j) integrity: answer hashes, validity report, ledger
        def edit_raw(b, inf):
            with open(os.path.join(b, "raw", "zh-flex-hours.%s.r1.txt" % C4), "a", encoding="utf-8") as f:
                f.write("。")

        r_ = variant("(j1) a c4 final edited after it was packaged (zh)", edit_raw,
                     missing=grade_cells("zh") | text_cells("zh"))
        expect("(j1) the mismatch is reported", len(r_["reported"]["integrity"]["answer_issues"]) == 3)

        def drop_validity(b, inf):
            os.remove(os.path.join(b, "validity.json"))

        variant("(j2) validity.json missing: every cell fails", drop_validity, missing=ALL, reval=False)

        def touch_raw(b, inf):
            t = os.path.getmtime(os.path.join(b, "validity.json")) + 10
            os.utime(os.path.join(b, "raw", "en-fsa-rollover.%s.r2.ndjson" % PLAIN), (t, t))

        variant("(j3) a run file newer than validity.json: every cell fails", touch_raw, missing=ALL, reval=False)

        def invalid_run(b, inf):
            jdump(os.path.join(b, "validity.json"), {"rule_files": [], "invalid": ["ko-severance-pay.gv-plain.r1"],
                                                     "flagged": [], "final_attempt_invalid": [], "runs": {}})

        variant("(j4) validity.json lists a run still due a rerun: every cell fails", invalid_run, missing=ALL)

        def flip_codex(b, inf):
            p = os.path.join(b, "blind", "grades", "codex", P(inf, "main", "ko-jeonse-protection", "r2") + ".json")
            obj = jload(p)
            obj["winner"] = "B" if obj["winner"] == "A" else "A"
            jdump(p, obj)
            return obj

        variant("(j5) a grade file replaced by a different valid grade (ko)", flip_codex, missing=grade_cells("ko"))

        def flip_and_log(b, inf):
            obj = flip_codex(b, inf)
            p = P(inf, "main", "ko-jeonse-protection", "r2")
            append_ledger(b, {"kind": "grade", "time": "t", "pid": p, "judge": "codex", "valid": True, "grade": obj,
                              "packet_sha256": sha256_file(os.path.join(b, "blind", "packets", p + ".md"))})

        variant("(j5b) a re-grade received later and written over the first: still fails (the first valid grade is "
                "used)", flip_and_log, missing=grade_cells("ko"))

        def replace_logged(b, inf):
            p = P(inf, "main", "ko-jeonse-protection", "r2")
            append_ledger(b, {"kind": "replace", "time": "t", "pid": p, "judge": "codex", "reason": "grader crashed"})
            flip_and_log(b, inf)

        r_ = variant("(j5c) a logged replace (with its reason) before the re-grade: passes, and is counted",
                     replace_logged)
        rg = r_["reported"]["integrity"]["ledger"]["regrades"]
        expect("(j5c) re-grades reported for the main set: 1 extra entry, 1 replace",
               rg.get("main", {}).get("extra_entries") == 1 and rg["main"]["replaces"] == 1, str(rg))

        def change_label(b, inf):
            p = os.path.join(b, "labels-opus.json")
            pid = P(inf, "main", "ja-part-time-leave", "r1")
            target = next(x["id"] for x in inf["notes"] if x["pid"] == pid and "wrong-claim" in x["note"])
            labs = jload(p)
            lab = next(x for x in labs if x["id"] == target)
            lab["label"], lab["cite"] = "unverified", ""
            jdump(p, labs)

        variant("(j6) a label changed after it was received (ja)", change_label,
                missing={"g5_wrong_added_claims[overall]", "g5_wrong_added_claims[ja]", "g12_unverified_claims[overall]"})

        def drop_ledger(b, inf):
            os.remove(os.path.join(b, LEDGER_FILE))

        variant("(j7) ledger.jsonl missing: every grade cell fails", drop_ledger, missing=grade_cells(*LANGS))

        def edit_packet(b, inf):
            with open(os.path.join(b, "blind", "packets", P(inf, "main", "en-medicare-part-b", "r1") + ".md"), "a",
                      encoding="utf-8") as f:
                f.write("edited\n")

        variant("(j8) a packet edited after it was graded (en)", edit_packet, missing=grade_cells("en"))

        def drop_shas(b, inf):
            p = os.path.join(b, "blind-map.json")
            m = jload(p)
            for e in m.values():
                e.pop("A_sha256", None)
                e.pop("B_sha256", None)
            jdump(p, m)

        variant("(j9) blind-map without answer hashes: every grade cell fails", drop_shas, missing=grade_cells(*LANGS))
        variant("(j10) a plain final still blank after its rerun, packaged as the placeholder: grades stand, the text "
                "gates fail", missing=text_cells("en"), blank=("en-fsa-rollover", PLAIN, "r1"),
                frozen=("not a win", ["g3_length[overall]", "g3_length[en]", "g8_hedging[overall]", "g8_hedging[en]"]))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    bad = results.count(False)
    print("selftest: %d assertions, %d failed" % (len(results), bad))
    return 0 if bad == 0 else 1


# ---------------------------------------------------------------------------------------------- main

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="run the self-test in a temporary folder and exit")
    ap.add_argument("--base", default=HERE, help="folder to evaluate (default: the folder this script is in)")
    ap.add_argument("--no-json", action="store_true", help="do not write verdict4-amended.json")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    base = os.path.abspath(a.base)
    res = evaluate(base)
    print("\n".join(render(res)))
    if not a.no_json:
        write_results(res, base)
    sys.exit(0)


if __name__ == "__main__":
    main()
