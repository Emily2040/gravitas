#!/usr/bin/env python3
"""Round-four verdict: does Gravitas (gv-grav-c4) beat plain DSH (gv-plain) by WIN_CRITERIA.md?

Implements the eight win criteria of docs/dsh-ab/WIN_CRITERIA.md (gravitas-claim-check) with both amendments
(all four languages; Japanese and Korean hedge lists) for gv-grav-c4 against gv-plain on the main set, overall
and separately in zh, en, ja and ko wherever a criterion can be measured per language. Beside the verdict it
reports the same gate table for gv-grav-base against gv-plain (base set), the attr-set votes c4 vs base, and
whether the candidate improves on the previous best (WIN_CRITERIA's stop rule needs it; it is not part of the
win verdict). Written and frozen by an agent that builds nothing in this round.

    python verdict4.py                 evaluate the folder this script sits in, print, write verdict4.json there
    python verdict4.py --base DIR      evaluate DIR instead (verdict4.json is written into DIR)
    python verdict4.py --selftest      self-test in a temporary folder (never reads or writes the real data)

Standard library only. A missing or malformed metric fails its gate with "metric missing"; nothing missing is
ever defaulted to a passing value. Comparisons are exact (fractions).
"""
import argparse
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))

# The twelve held-out requests of round four (prompts/ as listed on 2026-10-23, before any run), three per language.
# prompts/ must hold exactly these; a swapped or dropped request fails every gate until this list is re-frozen.
EXPECTED_CASES = sorted([
    "zh-flex-hours", "zh-insurance-gap", "zh-sick-pay",
    "en-529-roth", "en-fsa-rollover", "en-medicare-part-b",
    "ja-medical-deduction", "ja-part-time-leave", "ja-wallpaper-restoration",
    "ko-jeonse-protection", "ko-severance-pay", "ko-unemployment-quit",
])
LANGS = ("zh", "en", "ja", "ko")
SCOPES = ("overall",) + LANGS
GRADERS = ("opus", "sonnet")
RELABELLERS = ("sonnet", "opus")
ROUNDS = ("r1", "r2")
PLAIN, BASE, C4 = "gv-plain", "gv-grav-base", "gv-grav-c4"
ARMS = (PLAIN, BASE, C4)
DIMS = ("correct", "trap", "honest", "useful", "concise")
KP_MARKS = ("correct", "vague", "wrong", "missing")
LABELS = ("wrong", "unverified", "not an error")
PAIR_SETS = {"main": (C4, PLAIN), "base": (BASE, PLAIN), "attr": (C4, BASE)}
AA_SETS = {"aa-plain": PLAIN, "aa-c4": C4}
KNOWN_SETS = ("main", "base", "attr", "aa-plain", "aa-c4")
FLOOR_SETS = ("aa-plain", "aa-c4")          # the round's two A/A sets; criterion 1's noise floor
PID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

CMP_MAIN = {"key": "main", "set": "main", "x": C4, "y": PLAIN,
            "title": "gv-grav-c4 vs gv-plain (main set): decides the verdict"}
CMP_BASE = {"key": "base", "set": "base", "x": BASE, "y": PLAIN,
            "title": "gv-grav-base vs gv-plain (base set): reported beside, not part of the verdict"}

# ---------------------------------------------------------------------------------------------- hedge lists
# zh and en: round three's verdict.py lists (round-one list H_ROUND1, extended list H_EXTENDED), split by the
# language each pattern is written in. ja and ko: WIN_CRITERIA amendment of 2026-10-23, literal strings.
H1_ZH = ["可能", "大概", "也许", "或许", "以.{0,12}为准", "建议.{0,6}核实", "建议.{0,6}确认", "不确定", "请咨询", "仅供参考"]
H1_EN = [r"\bmay\b", r"\bmight\b", r"\bprobably\b", r"\bcheck with\b", r"\bconfirm with\b", r"\bnot sure\b", r"\bverify\b"]
H2_ZH = ["一般", "通常", "原则上", "视.{0,12}而定", "具体.{0,12}(?:咨询|确认|为准)", "向.{0,12}(?:咨询|询问|核实|确认)",
         "各地.{0,12}(?:不同|不一)", "因地而异", "建议.{0,6}(?:核实|确认|咨询)", "以.{0,12}为准",
         r"打.{0,12}(?:(?<!\d)\d{5}(?!\d)|五位号码).{0,12}问"]
H2_EN = [r"\btypically\b", r"\busually\b", r"\bgenerally\b", r"\bdepending on\b", r"\bmay vary\b", r"\bcan vary\b",
         r"\bcontact the\b", r"\bcheck (?:the|with)\b", r"\breach out\b", r"\bdouble[- ]check\b"]
H1_JA_WORDS = ["かもしれ", "おそらく", "恐らく", "たぶん", "可能性があ", "と思われ", "断言できませ", "ご確認ください", "確認してください"]
H2_JA_WORDS = ["一般的に", "通常は", "場合によ", "地域によ", "自治体によ", "お問い合わせ", "問い合わせて", "相談してください", "目安"]
H1_KO_WORDS = ["아마", "일지도", "할지도", "가능성이 있", "확실하지", "확인해 보세요", "확인하시기 바랍니다"]
H2_KO_WORDS = ["일반적으로", "보통은", "경우에 따라", "지역마다", "다를 수 있", "문의하", "상담하"]


def literal(word):
    """A literal marker; a space inside it matches any run of whitespace, including none (Korean auxiliary-verb
    spacing such as 확인해 보세요 / 확인해보세요 is optional in standard orthography)."""
    return r"\s*".join(re.escape(part) for part in word.split(" "))


HEDGE = {
    "zh": {"first": H1_ZH, "second": H2_ZH},
    "en": {"first": H1_EN, "second": H2_EN},
    "ja": {"first": [literal(w) for w in H1_JA_WORDS], "second": [literal(w) for w in H2_JA_WORDS]},
    "ko": {"first": [literal(w) for w in H1_KO_WORDS], "second": [literal(w) for w in H2_KO_WORDS]},
}
# Round three's exclusions, kept with the lists they belong to: 不可能 (zh) and "May" + day/year (en).
MAY_DATE = re.compile(r"May,?\s+(?:\d{1,2}(?:st|nd|rd|th)?\b|\d{4}\b)")


def count_markers(text, patterns, excl):
    """Matches of each pattern summed (round three's tally); excl holds the languages whose exclusions apply."""
    n = 0
    for p in patterns:
        for m in re.finditer(p, text, flags=re.I):
            s = m.start()
            if "zh" in excl and m.group().startswith("可能") and s > 0 and text[s - 1] == "不":
                continue
            if "en" in excl and text.startswith("May", s) and MAY_DATE.match(text, s):
                continue
            n += 1
    return n


def lang_of(case):
    p = case.split("-", 1)[0] if isinstance(case, str) else None
    return p if p in LANGS else None


# ---------------------------------------------------------------------------------------------- readers

def rd_text(path):
    if not os.path.isfile(path):
        return None, "missing"
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read(), None
    except (OSError, UnicodeDecodeError) as e:
        return None, "unreadable (%s)" % e.__class__.__name__


def rd_json(path):
    t, err = rd_text(path)
    if err:
        return None, err
    try:
        return json.loads(t), None
    except ValueError:
        return None, "not valid JSON"


def salvage_json(t):
    for a, b in (("[", "]"), ("{", "}")):
        i, j = t.find(a), t.rfind(b)
        if 0 <= i < j:
            try:
                return json.loads(t[i:j + 1])
            except ValueError:
                pass
    return None


def norm_id(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str) and v.strip().isdigit():
        return int(v.strip())
    return None


def load_cases(base):
    d = os.path.join(base, "prompts")
    if not os.path.isdir(d):
        return None, "prompts/ folder missing"
    stems = sorted(f[:-4] for f in os.listdir(d) if f.endswith(".txt") and os.path.isfile(os.path.join(d, f)))
    if not stems:
        return None, "no prompts/*.txt"
    miss, extra = sorted(set(EXPECTED_CASES) - set(stems)), sorted(set(stems) - set(EXPECTED_CASES))
    if miss or extra:
        return None, "prompts/ does not hold the 12 frozen held-out cases (missing %s, extra %s)" % (miss, extra)
    return stems, None


def load_map(base, cases):
    """Issues are keyed 'global' (fails every gate) or (set, lang) with lang in LANGS or '*' (all languages)."""
    issues, warnings, entries = defaultdict(list), [], {}
    pidx = {s: defaultdict(list) for s in PAIR_SETS}
    aidx = {s: defaultdict(list) for s in AA_SETS}
    pindex, aindex = {s: {} for s in PAIR_SETS}, {s: {} for s in AA_SETS}
    m, err = rd_json(os.path.join(base, "blind-map.json"))
    if err:
        issues["global"].append("blind-map.json " + err)
        return entries, dict(issues), warnings, pindex, aindex
    if not isinstance(m, dict) or not m:
        issues["global"].append("blind-map.json is not a non-empty object")
        return entries, dict(issues), warnings, pindex, aindex
    cs = set(cases or [])
    for pid, e in m.items():
        if not PID_RE.match(pid):
            issues["global"].append("pid %r is not a plain file name" % pid)
            continue
        if not isinstance(e, dict):
            issues["global"].append("%s: entry is not an object" % pid)
            continue
        s = e.get("set")
        if s not in KNOWN_SETS:
            warnings.append("%s: set %r is not a round-four set; ignored" % (pid, s))
            continue
        c = e.get("case")
        lg = lang_of(c) or "*"
        if not isinstance(c, str) or (cases is not None and c not in cs):
            issues[(s, lg)].append("%s: case %r is not one of the 12 held-out cases" % (pid, c))
            continue
        A, B = e.get("A"), e.get("B")
        if s in AA_SETS:
            arm = AA_SETS[s]
            if A != arm or B != arm:
                issues[(s, lg)].append("%s: %s pair must be %s vs %s, is %r vs %r" % (pid, s, arm, arm, A, B))
                continue
            if {e.get("A_round"), e.get("B_round")} != set(ROUNDS):
                issues[(s, lg)].append("%s: A_round/B_round must be r1 and r2" % pid)
                continue
            aidx[s][c].append(pid)
        else:
            if e.get("round") not in ROUNDS:
                issues[(s, lg)].append("%s: round %r is not r1/r2" % (pid, e.get("round")))
                continue
            if not (isinstance(A, str) and isinstance(B, str)) or A == B or {A, B} != set(PAIR_SETS[s]):
                issues[(s, lg)].append("%s: %s pair must be %s vs %s, is %r vs %r" % (pid, s, PAIR_SETS[s][0],
                                                                                    PAIR_SETS[s][1], A, B))
                continue
            pidx[s][(c, e["round"])].append(pid)
        entries[pid] = e
    if cases is None:
        issues["global"].append("case list unavailable, pair coverage cannot be checked")
        return entries, dict(issues), warnings, pindex, aindex
    for c in cases:
        lg = lang_of(c)
        for s in PAIR_SETS:
            for r in ROUNDS:
                p = pidx[s].get((c, r), [])
                if len(p) != 1:
                    issues[(s, lg)].append("%s %s %s has %d pairs in blind-map (need exactly 1)" % (s, c, r, len(p)))
                else:
                    pindex[s][(c, r)] = p[0]
        for s in AA_SETS:
            p = aidx[s].get(c, [])
            if len(p) != 1:
                issues[(s, lg)].append("%s %s has %d pairs in blind-map (need exactly 1)" % (s, c, len(p)))
            else:
                aindex[s][c] = p[0]
    return entries, dict(issues), warnings, pindex, aindex


def load_keypoints(base, cases):
    kp, issues = {}, {}
    for c in cases:
        j, err = rd_json(os.path.join(base, "keypoints", c + ".json"))
        if err:
            issues[c] = "keypoints/%s.json %s" % (c, err)
            continue
        if not isinstance(j, list) or not j or not all(isinstance(x, dict) for x in j):
            issues[c] = "keypoints/%s.json is not a non-empty list of objects" % c
            continue
        ids = [str(x.get("id")).strip() if isinstance(x.get("id"), (str, int)) and not isinstance(x.get("id"), bool)
               else None for x in j]
        if None in ids or "" in ids or len(set(ids)) != len(ids):
            issues[c] = "keypoints/%s.json ids missing or repeated" % c
            continue
        if not all(isinstance(x.get("point"), str) and x["point"].strip() for x in j):
            issues[c] = "keypoints/%s.json has a point without text" % c
            continue
        kp[c] = ids
    return kp, issues


def parse_grade(path, pid, kp_ids, kp_err):
    """Return (grade, None) or (None, reason). A grade with any invalid field is malformed as a whole."""
    t, err = rd_text(path)
    if err:
        return None, err
    try:
        obj = json.loads(t)
    except ValueError:
        obj = salvage_json(t)
        if obj is None:
            return None, "not valid JSON"
    if isinstance(obj, list):
        if len(obj) != 1:
            return None, "array of %d objects (need exactly one pair)" % len(obj)
        obj = obj[0]
    if not isinstance(obj, dict):
        return None, "not a JSON object"
    if obj.get("pair") != pid:
        return None, "pair field %r does not match %s" % (obj.get("pair"), pid)
    w = obj.get("winner")
    w = w.strip() if isinstance(w, str) else None
    w = w.upper() if w and w.upper() in ("A", "B") else ("tie" if w and w.lower() == "tie" else None)
    if w is None:
        return None, "winner %r not A, B or tie" % obj.get("winner")
    if kp_ids is None:
        return None, "key points unavailable for this case (%s)" % (kp_err or "case list unavailable")
    out = {"winner": w, "margin": obj.get("margin")}
    for side in "AB":
        s = obj.get(side)
        if not isinstance(s, dict):
            return None, "%s object missing" % side
        scores = {}
        for d in DIMS:
            v = s.get(d)
            if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 10:
                return None, "%s.%s = %r is not an integer 0-10" % (side, d, v)
            scores[d] = v
        notes = s.get("added_claim_errors")
        if not isinstance(notes, list) or not all(isinstance(x, str) and x.strip() for x in notes):
            return None, "%s.added_claim_errors is not a list of non-empty strings" % side
        kp = s.get("key_points")
        top = obj.get("key_points")
        if kp is None and isinstance(top, dict):
            kp = top.get(side)
        if not isinstance(kp, dict):
            return None, "%s.key_points missing" % side
        kp2 = {}
        for k, v in kp.items():
            mk = v.strip().lower() if isinstance(v, str) else None
            if mk not in KP_MARKS:
                return None, "%s.key_points[%s] = %r is not correct/vague/wrong/missing" % (side, k, v)
            kp2[str(k).strip()] = mk
        if len(kp2) != len(kp) or set(kp2) != set(kp_ids):
            return None, "%s.key_points ids %s do not equal the case's ids %s" % (side, sorted(kp2), sorted(kp_ids))
        out[side] = {"scores": scores, "notes": [x.strip() for x in notes], "kp": kp2}
    return out, None


def load_notes(base):
    j, err = rd_json(os.path.join(base, "claim-notes.json"))
    if err:
        return None, ["claim-notes.json " + err]
    if not isinstance(j, list):
        return None, ["claim-notes.json is not a list"]
    rows, issues = {}, []
    for i, r in enumerate(j):
        rid = norm_id(r.get("id")) if isinstance(r, dict) else None
        if rid is None:
            issues.append("claim-notes.json row %d has no integer id" % i)
            continue
        if rid in rows:
            issues.append("claim-notes.json id %d repeated" % rid)
            continue
        pid, side, grader, note = r.get("pid"), r.get("side"), r.get("grader"), r.get("note")
        if not (isinstance(pid, str) and side in ("A", "B") and grader in GRADERS and isinstance(note, str)
                and note.strip()):
            issues.append("claim-notes.json id %d malformed (pid/side/grader/note)" % rid)
            continue
        rows[rid] = {"id": rid, "pid": pid, "side": side, "grader": grader, "note": note.strip()}
    return (None, issues) if issues else (rows, [])


def load_labels(base, who):
    """Return ({"labels": {id: label}, "bad": {id: reason}}, file_issues)."""
    name = "labels-%s.json" % who
    j, err = rd_json(os.path.join(base, name))
    if err:
        return None, [name + " " + err]
    if not isinstance(j, list):
        return None, [name + " is not a list"]
    labs, bad, file_issues, seen = {}, {}, [], Counter()
    for i, r in enumerate(j):
        rid = norm_id(r.get("id")) if isinstance(r, dict) else None
        if rid is None:
            file_issues.append("%s entry %d has no integer id" % (name, i))
            continue
        seen[rid] += 1
        lab = r.get("label")
        lab = lab.strip().lower() if isinstance(lab, str) else None
        cite = r.get("cite")
        if lab not in LABELS:
            bad[rid] = "label %r is not wrong/unverified/not an error" % r.get("label")
        elif lab == "wrong" and not (isinstance(cite, str) and cite.strip()):
            bad[rid] = "'wrong' label without a cite"
        else:
            labs[rid] = lab
    for rid, n in seen.items():
        if n > 1:
            labs.pop(rid, None)
            bad[rid] = "labelled %d times" % n
    return {"labels": labs, "bad": bad}, file_issues


def parse_ndjson(path):
    t, err = rd_text(path)
    if err:
        return None, err
    events = []
    for i, line in enumerate(t.splitlines(), 1):
        s = line.strip()
        if not s.startswith("{"):
            continue
        try:
            ev = json.loads(s)
        except ValueError:
            return None, "line %d is not valid JSON" % i
        if isinstance(ev, dict):
            events.append(ev)
    if not events:
        return None, "no events"
    return events, None


def web_opened(events):
    calls = {e.get("callId"): e.get("tool") for e in events if e.get("type") == "tool_call"}
    return any(e.get("type") == "tool_result" and e.get("status") == "completed"
               and calls.get(e.get("callId")) in ("web_fetch", "web_search") for e in events)


class Data:
    def __init__(self, base):
        self.base = base
        self._text, self._events = {}, {}
        self.cases, self.case_issue = load_cases(base)
        (self.entries, self.map_issues, self.map_warnings,
         self.pindex, self.aindex) = load_map(base, self.cases)
        self.kp, self.kp_issues = load_keypoints(base, self.cases or [])
        self.grades = {}
        for g in GRADERS:
            for pid, e in self.entries.items():
                self.grades[(g, pid)] = parse_grade(self.p("blind", "grades", g, pid + ".json"), pid,
                                                    self.kp.get(e["case"]), self.kp_issues.get(e["case"]))
        self.stray_grades = []
        for g in GRADERS:
            d = self.p("blind", "grades", g)
            if os.path.isdir(d):
                self.stray_grades += ["%s/%s" % (g, f) for f in os.listdir(d)
                                      if f.endswith(".json") and f[:-5] not in self.entries]
        self.notes, self.notes_issues = load_notes(base)
        self.labels = {w: load_labels(base, w) for w in RELABELLERS}

    def p(self, *parts):
        return os.path.join(self.base, *parts)

    def text(self, case, arm, rnd):
        k = (case, arm, rnd)
        if k not in self._text:
            t, err = rd_text(self.p("raw", "%s.%s.%s.txt" % k))
            if err is None and not t.strip():
                t, err = None, "empty"
            self._text[k] = (t, err)
        return self._text[k]

    def events(self, case, arm, rnd):
        k = (case, arm, rnd)
        if k not in self._events:
            self._events[k] = parse_ndjson(self.p("raw", "%s.%s.%s.ndjson" % k))
        return self._events[k]


# ---------------------------------------------------------------------------------------------- helpers

def summarize(items, k=6):
    items = list(dict.fromkeys(items))
    s = "; ".join(items[:k])
    return s + ("; ... and %d more" % (len(items) - k) if len(items) > k else "")


def fmt(x, nd=3):
    if x is None:
        return "n/a"
    if isinstance(x, Fraction):
        x = float(x)
    if isinstance(x, float):
        return ("%." + str(nd) + "f") % x
    return str(x)


def mean(xs):
    xs = list(xs)
    return Fraction(sum(xs), len(xs)) if xs else None


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if not n:
        return None
    return Fraction(xs[n // 2]) if n % 2 else Fraction(xs[n // 2 - 1] + xs[n // 2], 2)


def ratio(a, b):
    return None if a is None or not b else Fraction(a) / Fraction(b)


def sign_test(a, b):
    """Two-sided exact binomial test on a wins against b wins (ties dropped)."""
    n, k = a + b, min(a, b)
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def fmt_p(p):
    return "%.4f" % p if p >= 1e-4 else "%.1e" % p


def cohen_kappa(pairs, cats):
    n = len(pairs)
    if not n:
        return None
    po = Fraction(sum(a == b for a, b in pairs), n)
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(Fraction(ca[c] * cb[c], n * n) for c in cats)
    return None if pe == 1 else (po - pe) / (1 - pe)


def jsonable(x):
    if isinstance(x, Fraction):
        return round(float(x), 6)
    if isinstance(x, dict):
        return {(k if isinstance(k, str) else "|".join(map(str, k)) if isinstance(k, tuple) else str(k)): jsonable(v)
                for k, v in x.items()}
    if isinstance(x, set):
        return [jsonable(v) for v in sorted(x)]
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x


def scope_langs(scope):
    return LANGS if scope == "overall" else (scope,)


def scope_cases(D, scope):
    return [c for c in (D.cases or []) if lang_of(c) in scope_langs(scope)]


def exp_pairs(scope):
    return sum(1 for c in EXPECTED_CASES if lang_of(c) in scope_langs(scope)) * len(ROUNDS)


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


def pre_missing(D, sets, scope):
    m = [] if D.cases is not None else ["case list: " + D.case_issue]
    m += ["blind-map: " + x for x in D.map_issues.get("global", [])]
    for s in sets:
        for lg in ("*",) + scope_langs(scope):
            m += ["blind-map: " + x for x in D.map_issues.get((s, lg), [])]
    return m


def pair_votes(D, s, scope, strict=True):
    """Votes of a paired set in a scope, one per (pair, grader); win = the arm picked or 'tie'.
    strict: (None, missing) unless every pair of the scope has a valid grade from both graders."""
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
            for g in GRADERS:
                gr, err = D.grades.get((g, pid), (None, "missing"))
                if err:
                    missing.append("blind/grades/%s/%s.json (%s %s %s): %s" % (g, pid, s, c, r, err))
                    continue
                votes.append({"case": c, "lang": lang_of(c), "round": r, "grader": g, "pid": pid, "entry": e,
                              "grade": gr, "win": "tie" if gr["winner"] == "tie" else e[gr["winner"]]})
    if strict and missing:
        return None, missing
    return votes, missing


def aa_votes(D, s, scope, strict=True):
    """A/A votes in a scope; win is the round ('r1'/'r2') of the side picked, or 'tie'."""
    missing = pre_missing(D, (s,), scope)
    if strict and missing:
        return None, missing
    votes = []
    for c in scope_cases(D, scope):
        pid = D.aindex[s].get(c)
        if pid is None:
            continue
        e = D.entries[pid]
        for g in GRADERS:
            gr, err = D.grades.get((g, pid), (None, "missing"))
            if err:
                missing.append("blind/grades/%s/%s.json (%s %s): %s" % (g, pid, s, c, err))
                continue
            w = gr["winner"]
            votes.append({"case": c, "lang": lang_of(c), "grader": g, "pid": pid,
                          "win": "tie" if w == "tie" else e["%s_round" % w]})
    if strict and missing:
        return None, missing
    return votes, missing


def aa_net(vs):
    r1, r2 = sum(v["win"] == "r1" for v in vs), sum(v["win"] == "r2" for v in vs)
    return r1, r2, len(vs) - r1 - r2, r1 - r2


def get_texts(D, arms, scope):
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


# ---------------------------------------------------------------------------------------------- gates (WIN_CRITERIA 1-8)

def gate1(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    n = exp_pairs(scope)
    c = new_cell("g1_votes", scope,
                 "Do the graders prefer %s over %s by more than two runs of the same arm differ%s?" % (x, y, q_suffix(scope)),
                 "net = %s wins - %s wins over the %s set (%d pairs x 2 graders); net > 0 and net > noise floor = "
                 "max(|net aa-plain|, |net aa-c4|) over the A/A pairs of the same scope (%d pairs x 2 graders each); "
                 "A/A net = r1-side wins - r2-side wins" % (x, y, s, n, n // 2))
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
    nets = {}
    for a in FLOOR_SETS:
        r1, r2, ties, an = aa_net(aa[a])
        nets[a] = an
        c["measured"][a] = {"votes": len(aa[a]), "r1_wins": r1, "r2_wins": r2, "ties": ties, "net": an}
    floor = max(abs(v) for v in nets.values())
    c["measured"].update({"votes": len(votes), "x_wins": w, "y_wins": l, "ties": t, "net": net, "noise_floor": floor})
    c["detail"].append("%s: %d votes, %s %d, %s %d, tie %d -> net %+d" % (s, len(votes), x, w, y, l, t, net))
    c["detail"].append("A/A: " + ", ".join("%s %d votes net %+d" % (a, len(aa[a]), nets[a]) for a in FLOOR_SETS)
                       + " -> noise floor %d" % floor)
    check(c, "net votes > 0", "%+d" % net, "> 0", net > 0)
    check(c, "net votes > A/A noise floor", "%+d" % net, "> %d" % floor, net > floor)
    return finish(c)


def gate2(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    c = new_cell("g2_each_grader", scope, "Does each grader, on its own, prefer %s more often than %s?" % (x, y),
                 "for opus and for sonnet separately (%s set, %d votes each): %s wins > %s wins; overall only "
                 "(WIN_CRITERIA item 2 says overall, and the amendment's per-language list omits it)"
                 % (s, exp_pairs(scope), x, y))
    votes, missing = pair_votes(D, s, scope)
    if missing:
        return finish(c, missing)
    for g in GRADERS:
        vs = [v for v in votes if v["grader"] == g]
        w, l, t = wl(vs, x, y)
        c["measured"][g] = {"votes": len(vs), "x_wins": w, "y_wins": l, "ties": t}
        c["detail"].append("%s: %d votes, %s %d, %s %d, tie %d" % (g, len(vs), x, w, y, l, t))
        check(c, "%s: %s wins > %s wins" % (g, x, y), "%d vs %d" % (w, l), "wins > losses", w > l)
    per = {}
    for lg in LANGS:
        per[lg] = {}
        for g in GRADERS:
            w, l, t = wl([v for v in votes if v["grader"] == g and v["lang"] == lg], x, y)
            per[lg][g] = {"x_wins": w, "y_wins": l, "ties": t}
    c["measured"]["per_language_reported_only"] = per
    c["detail"].append("per language (reported only, not gated): " + "; ".join(
        "%s %s" % (lg, ", ".join("%s %d-%d" % (g, per[lg][g]["x_wins"], per[lg][g]["y_wins"]) for g in GRADERS))
        for lg in LANGS))
    return finish(c)


def gate3(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    n = exp_pairs(scope)
    c = new_cell("g3_length", scope,
                 "Is the median %s answer no longer than the median %s answer, with few gutted answers%s?" % (x, y, q_suffix(scope)),
                 "raw/*.txt finals, chars = len(text): median(%s) / median(%s) <= 1.00; pairs (same case and round) "
                 "with %s/%s chars < 0.6: at most 10%% of pairs, i.e. count/pairs <= 0.10 (%d of %d allowed)"
                 % (x, y, x, y, n // 10, n))
    texts, missing = get_texts(D, (x, y), scope)
    if missing:
        return finish(c, missing)
    cs = scope_cases(D, scope)
    lx = [len(texts[(k, x, r)]) for k in cs for r in ROUNDS]
    ly = [len(texts[(k, y, r)]) for k in cs for r in ROUNDS]
    mx, my = median(lx), median(ly)
    rt = mx / my
    pr = {(k, r): Fraction(len(texts[(k, x, r)]), len(texts[(k, y, r)])) for k in cs for r in ROUNDS}
    under = sorted(k for k, v in pr.items() if v < Fraction(6, 10))
    c["measured"] = {"median_chars": {x: mx, y: my}, "median_ratio": rt, "pair_ratios": pr,
                     "pairs_under_0.6": under, "pairs": len(pr)}
    c["detail"].append("median chars %s %s, %s %s, ratio %s" % (x, fmt(mx, 1), y, fmt(my, 1), fmt(rt)))
    c["detail"].append("pairs under 0.6: %d of %d%s" % (len(under), len(pr),
                                                        (" (" + ", ".join("%s %s" % k for k in under) + ")") if under else ""))
    check(c, "median chars ratio <= 1.00", fmt(rt), "<= 1.00", rt <= 1)
    check(c, "pairs with ratio < 0.6 at most 10%", "%d of %d" % (len(under), len(pr)), "<= %d" % (len(pr) // 10),
          Fraction(len(under), len(pr)) <= Fraction(1, 10))
    return finish(c)


def kp_counts(D, cmp, scope):
    votes, missing = pair_votes(D, cmp["set"], scope)
    if missing:
        return None, missing
    ans = answers(votes, (cmp["x"], cmp["y"]))
    cnt = {a: Counter(mk for g in ans[a] for mk in g["kp"].values()) for a in ans}
    return (cnt, ans), []


def gate4(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    c = new_cell("g4_vague_key_points", scope,
                 "Does %s leave the key's points vague no more often than %s%s?" % (x, y, q_suffix(scope)),
                 "key-point marks 'vague' over the %s set's graded answers (both graders, %d per arm): %s <= %s"
                 % (cmp["set"], exp_pairs(scope) * 2, x, y))
    r, missing = kp_counts(D, cmp, scope)
    if missing:
        return finish(c, missing)
    cnt, ans = r
    c["measured"] = {a: {mk: cnt[a][mk] for mk in KP_MARKS} for a in cnt}
    for a in (x, y):
        c["detail"].append("%-13s answers %d: %s" % (a, len(ans[a]), " ".join("%s %d" % (mk, cnt[a][mk]) for mk in KP_MARKS)))
    check(c, "vague %s <= %s" % (x, y), cnt[x]["vague"], "<= %d" % cnt[y]["vague"], cnt[x]["vague"] <= cnt[y]["vague"])
    return finish(c)


def gate5(D, cmp, scope):
    x, y, s = cmp["x"], cmp["y"], cmp["set"]
    c = new_cell("g5_wrong_added_claims", scope,
                 "Does %s add no more claims that both relabellers call wrong than %s%s?" % (x, y, q_suffix(scope)),
                 "added-claim notes on the %s set's answers (both graders); wrong = both relabellers say 'wrong' with a "
                 "non-empty cite: %s <= %s; every note listed exactly once in claim-notes.json and validly labelled by "
                 "both relabellers (a 'wrong' without a cite is malformed)" % (s, x, y))
    votes, missing = pair_votes(D, s, scope)
    missing = list(missing or [])
    if D.notes is None:
        missing += D.notes_issues
    for w in RELABELLERS:
        missing += D.labels[w][1]
    if missing:
        return finish(c, missing)
    cs = set(scope_cases(D, scope))
    pids = {pid for (k, r), pid in D.pindex[s].items() if k in cs}
    expected = Counter((v["pid"], side, v["grader"], note) for v in votes for side in "AB"
                       for note in v["grade"][side]["notes"])
    rows = [r for r in D.notes.values() if r["pid"] in pids]
    actual = Counter((r["pid"], r["side"], r["grader"], r["note"]) for r in rows)
    if expected != actual:
        unl, ext = expected - actual, actual - expected
        missing.append("claim-notes.json does not list every %s-set added_claim_errors entry of this scope exactly once "
                       "(%d entries unlisted, %d rows with no matching entry)" % (s, sum(unl.values()), sum(ext.values())))
    wrong, pairs = Counter(), {x: Counter(), y: Counter()}
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
    if missing:
        return finish(c, missing)
    unver = {a: sum(n for k, n in pairs[a].items() if k != "wrong/wrong" and "unverified" in k) for a in pairs}
    c["measured"] = {"notes": {a: sum(pairs[a].values()) for a in pairs}, "wrong_both": {a: wrong[a] for a in pairs},
                     "unverified_any_not_wrong_both": unver, "label_pairs_sonnet_opus": {a: dict(pairs[a]) for a in pairs}}
    for a in (x, y):
        c["detail"].append("%-13s notes %d, wrong by both %d, unverified by at least one (reported only) %d" % (
            a, sum(pairs[a].values()), wrong[a], unver[a]))
    check(c, "wrong added claims %s <= %s" % (x, y), wrong[x], "<= %d" % wrong[y], wrong[x] <= wrong[y])
    return finish(c)


def gate6(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    c = new_cell("g6_correct_wrong_key_points", scope,
                 "Does %s state the key's points correctly at least as often as %s, with no more wrong%s?" % (x, y, q_suffix(scope)),
                 "key-point marks over the %s set's graded answers (both graders, %d per arm): correct %s >= %s; "
                 "wrong %s <= %s" % (cmp["set"], exp_pairs(scope) * 2, x, y, x, y))
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
                 "graded answers with trap score < 8 (%s set, both graders, %d per arm): %s <= %s"
                 % (cmp["set"], exp_pairs(scope) * 2, x, y))
    votes, missing = pair_votes(D, cmp["set"], scope)
    if missing:
        return finish(c, missing)
    ans = answers(votes, (x, y))
    low = {a: sum(g["scores"]["trap"] < 8 for g in ans[a]) for a in ans}
    c["measured"] = {"trap_under_8": low, "answers": {a: len(ans[a]) for a in ans}}
    c["detail"].append("trap < 8: %s %d of %d, %s %d of %d" % (x, low[x], len(ans[x]), y, low[y], len(ans[y])))
    check(c, "trap<8 %s <= %s" % (x, y), low[x], "<= %d" % low[y], low[x] <= low[y])
    return finish(c)


def hedge_rate(text, lang, which):
    return Fraction(count_markers(text, HEDGE[lang][which], (lang,)) * 1000, len(text))


def gate8(D, cmp, scope):
    x, y = cmp["x"], cmp["y"]
    lists = "zh/en: round three's round-one and extended lists split by language; ja/ko: the 2026-10-23 amendment"
    c = new_cell("g8_hedging", scope,
                 "Are %s answers no more hedged than %s, on the first list and the second list (no substitution)%s?"
                 % (x, y, q_suffix(scope)),
                 "hedge markers per 1000 chars, mean over the %d finals per arm, each final counted with its own "
                 "language's lists (by case prefix; %s): first list %s <= 1.00 x %s; second list %s <= 1.10 x %s"
                 % (exp_pairs(scope), lists, x, y, x, y))
    texts, missing = get_texts(D, (x, y), scope)
    if missing:
        return finish(c, missing)
    cs = scope_cases(D, scope)
    m = {}
    for which in ("first", "second"):
        m[which] = {}
        for a in (x, y):
            rates = [hedge_rate(texts[(k, a, r)], lang_of(k), which) for k in cs for r in ROUNDS]
            m[which][a] = mean(rates)
            m[which]["markers_" + a] = sum(count_markers(texts[(k, a, r)], HEDGE[lang_of(k)][which], (lang_of(k),))
                                           for k in cs for r in ROUNDS)
        m[which]["ratio"] = ratio(m[which][x], m[which][y])
    c["measured"] = m
    for which in ("first", "second"):
        c["detail"].append("%-6s list: %s %s (%d markers), %s %s (%d markers), ratio %s" % (
            which, x, fmt(m[which][x]), m[which]["markers_" + x], y, fmt(m[which][y]), m[which]["markers_" + y],
            fmt(m[which]["ratio"])))
    check(c, "first list: %s rate <= 1.00 x %s" % (x, y), fmt(m["first"][x]), "<= %s" % fmt(m["first"][y]),
          m["first"][x] <= m["first"][y])
    check(c, "second list: %s rate <= 1.10 x %s" % (x, y), fmt(m["second"][x]),
          "<= %s" % fmt(Fraction(11, 10) * m["second"][y]), m["second"][x] <= Fraction(11, 10) * m["second"][y])
    return finish(c)


GATE_SPECS = [("g1_votes", gate1, SCOPES), ("g2_each_grader", gate2, ("overall",)), ("g3_length", gate3, SCOPES),
              ("g4_vague_key_points", gate4, SCOPES), ("g5_wrong_added_claims", gate5, SCOPES),
              ("g6_correct_wrong_key_points", gate6, SCOPES), ("g7_trap_under_8", gate7, SCOPES),
              ("g8_hedging", gate8, SCOPES)]
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
                      "aa_c4_votes": len(aa), "aa_c4_net": an, "complete": not m and not am,
                      "missing": list(dict.fromkeys(m + am))}
    return out


def improvement(main_cells, base_cells, attr):
    """Candidate improves on the previous best: it passes at least as many gate cells (overall + per language) as
    the base on the same requests AND the attr-set net votes (c4 - base) are above the aa-c4 noise floor.
    Any metric missing on either side, or incomplete attr/aa-c4 votes, makes the answer 'no'."""
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
    cp = sum(c["status"] == "PASS" for c in main_cells)
    bp = sum(c["status"] == "PASS" for c in base_cells)
    floor = abs(a["aa_c4_net"])
    bidx = {c["id"]: c for c in base_cells}
    gains = [c["id"] for c in main_cells if c["status"] == "PASS" and bidx[c["id"]]["status"] != "PASS"]
    losses = [c["id"] for c in main_cells if c["status"] != "PASS" and bidx[c["id"]]["status"] == "PASS"]
    checks = [{"desc": "gv-grav-c4 passes at least as many gate cells as gv-grav-base", "value": "%d vs %d" % (cp, bp),
               "bound": "c4 >= base", "ok": cp >= bp},
              {"desc": "attr net votes (c4 - base) > aa-c4 noise floor", "value": "%+d" % a["net"],
               "bound": "> %d" % floor, "ok": a["net"] > floor}]
    if miss:
        yes = False
        reasons = ["metric missing: " + "; ".join(miss)]
    else:
        yes = all(k["ok"] for k in checks)
        reasons = [k["desc"] + " (%s, need %s)" % (k["value"], k["bound"]) for k in checks if not k["ok"]]
    summary = "c4 passes %d of %d gate cells, base %d of %d; attr net %+d vs aa-c4 noise floor %d" % (
        cp, len(main_cells), bp, len(base_cells), a["net"], floor)
    line = "IMPROVEMENT: yes (%s)" % summary if yes else "IMPROVEMENT: no (%s; %s)" % ("; ".join(reasons), summary)
    return {"improvement": "yes" if yes else "no", "line": line, "checks": checks, "reasons": reasons,
            "c4_cells_passed": cp, "base_cells_passed": bp, "cells": len(main_cells), "attr_net": a["net"],
            "aa_c4_floor": floor, "c4_passes_base_fails": gains, "base_passes_c4_fails": losses, "missing": miss}


# ---------------------------------------------------------------------------------------------- reported beside

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
    ok = {g: sum(1 for (gg, _), (gr, err) in D.grades.items() if gg == g and not err) for g in GRADERS}
    lines.append("  valid grade files: %s of %d mapped pairs each; stray grade files (pid not in map): %d" % (
        ok, len(D.entries), len(D.stray_grades)))
    if D.kp_issues:
        lines.append("  key-point issues: %s" % summarize(list(D.kp_issues.values()), 4))
    known = set(D.entries)
    orphan = sum(1 for r in (D.notes or {}).values() if r["pid"] not in known)
    lines.append("  claim-notes rows: %s (%d with a pid not in the map)" % (
        len(D.notes) if D.notes is not None else "n/a (%s)" % summarize(D.notes_issues, 2), orphan))
    out["inputs"] = {"cases": D.cases, "case_issue": D.case_issue, "map_issues": D.map_issues,
                     "map_warnings": D.map_warnings, "valid_grades": ok, "stray_grades": D.stray_grades,
                     "keypoint_issues": D.kp_issues, "claim_notes_orphans": orphan}

    sec("sign tests, two-sided exact binomial on non-tie votes")
    st = {}
    for s, (x, y) in PAIR_SETS.items():
        st[s] = {}
        for scope in SCOPES:
            vs, m = pair_votes(D, s, scope, strict=False)
            w, l, t = wl(vs, x, y)
            st[s][scope] = {"x": x, "y": y, "x_wins": w, "y_wins": l, "ties": t, "votes": len(vs),
                            "complete": not m, "p": sign_test(w, l)}
        lines.append("  %-5s %s vs %s: %s" % (s, x, y, "; ".join(
            "%s %d-%d-%d p=%s%s" % (sc, d["x_wins"], d["y_wins"], d["ties"], fmt_p(d["p"]), "" if d["complete"] else " (incomplete)")
            for sc, d in st[s].items())))
    lines.append("  (wins-losses-ties; with 12 votes per language only a large effect can show)")
    out["sign_tests"] = st

    sec("A/A noise per language (r1-side wins - r2-side wins)")
    aa_rep = {}
    for a in FLOOR_SETS:
        aa_rep[a] = {}
        for scope in SCOPES:
            vs, m = aa_votes(D, a, scope, strict=False)
            r1, r2, t, n = aa_net(vs)
            aa_rep[a][scope] = {"votes": len(vs), "r1": r1, "r2": r2, "ties": t, "net": n, "complete": not m}
        lines.append("  %-8s %s" % (a, "; ".join("%s net %+d (%d votes%s)" % (sc, d["net"], d["votes"], "" if d["complete"] else ", incomplete")
                                                 for sc, d in aa_rep[a].items())))
    out["aa"] = aa_rep

    sec("Cohen's kappa between opus and sonnet on the winner")
    kp = {}
    for s in PAIR_SETS:
        pairs = []
        for (c, r), pid in D.pindex[s].items():
            a_, b_ = D.grades.get(("opus", pid), (None, 1)), D.grades.get(("sonnet", pid), (None, 1))
            if not a_[1] and not b_[1]:
                e = D.entries[pid]
                pairs.append(tuple("tie" if g["winner"] == "tie" else e[g["winner"]] for g in (a_[0], b_[0])))
        kp[s] = {"n": len(pairs), "kappa": cohen_kappa(pairs, PAIR_SETS[s] + ("tie",))}
        lines.append("  %-5s n=%d kappa %s" % (s, kp[s]["n"], fmt(kp[s]["kappa"]) if kp[s]["kappa"] is not None else "n/a"))
    out["kappa"] = kp

    sec("A/B balance of the paired sets")
    bal = {}
    for s, (x, _) in PAIR_SETS.items():
        idx = D.pindex[s]
        xa = sum(D.entries[p]["A"] == x for p in idx.values())
        bad = [c for c in (D.cases or []) if (c, "r1") in idx and (c, "r2") in idx
               and D.entries[idx[(c, "r1")]]["A"] == D.entries[idx[(c, "r2")]]["A"]]
        bal[s] = {"x_is_A": xa, "pairs": len(idx), "cases_not_alternating": bad}
        lines.append("  %-5s %s is A in %d of %d pairs; cases where it is A in both or neither round: %s" % (
            s, x, xa, len(idx), bad or "none"))
    out["ab_balance"] = bal

    sec("event streams (raw/*.ndjson), reported only")
    evr = {}
    for arm in ARMS:
        n_ok, web, tcs, bad = 0, 0, [], []
        for c in D.cases or []:
            for r in ROUNDS:
                ev, err = D.events(c, arm, r)
                if err:
                    bad.append("%s %s: %s" % (c, r, err))
                    continue
                n_ok += 1
                web += web_opened(ev)
                tcs.append(sum(1 for e in ev if e.get("type") == "tool_call"))
        evr[arm] = {"streams": n_ok, "web_opened": web, "tool_calls_mean": mean(tcs), "unreadable": bad}
        lines.append("  %-13s streams read %d of %d; runs that opened a web page %d; tool calls mean %s%s" % (
            arm, n_ok, len(D.cases or []) * len(ROUNDS), web, fmt(mean(tcs), 1),
            ("; unreadable: " + summarize(bad, 2)) if bad else ""))
    out["events"] = evr

    sec("hedging with round three's combined zh+en lists on the zh and en finals (comparable with round three)")
    comb = {}
    zhen = [c for c in (D.cases or []) if lang_of(c) in ("zh", "en")]
    for arm in ARMS:
        ts = [D.text(c, arm, r) for c in zhen for r in ROUNDS]
        if not zhen or any(err for _, err in ts):
            comb[arm] = None
            continue
        comb[arm] = {name: mean(Fraction(count_markers(t, pats, ("zh", "en")) * 1000, len(t)) for t, _ in ts)
                     for name, pats in (("round1", H1_ZH + H1_EN), ("extended", H2_ZH + H2_EN))}
    for arm in ARMS:
        lines.append("  %-13s %s" % (arm, "n/a (finals missing)" if comb[arm] is None else
                                     "round-one %s, extended %s" % (fmt(comb[arm]["round1"]), fmt(comb[arm]["extended"]))))
    out["hedging_round3_combined"] = comb
    return out, lines


# ---------------------------------------------------------------------------------------------- evaluate and render

def script_sha256():
    try:
        with open(os.path.abspath(__file__), "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def evaluate(base):
    D = Data(base)
    tables = {}
    for cmp in (CMP_MAIN, CMP_BASE):
        tables[cmp["key"]] = {"title": cmp["title"], "set": cmp["set"], "x": cmp["x"], "y": cmp["y"],
                              "cells": gate_table(D, cmp)}
    attr = attr_summary(D)
    imp = improvement(tables["main"]["cells"], tables["base"]["cells"], attr)
    reported, rlines = report_beside(D)
    failing = [c["id"] for c in tables["main"]["cells"] if c["status"] != "PASS"]
    verdict = "win" if not failing else "not a win"
    line = "VERDICT: win" if not failing else "VERDICT: not a win (failing: %s)" % ", ".join(failing)
    return {"base": base, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "script_sha256": script_sha256(), "cases": D.cases, "tables": tables, "attr": attr,
            "improvement": imp, "reported": reported, "report_lines": rlines,
            "verdict": verdict, "failing": failing, "verdict_line": line}


def code(c):
    return {"pass": "PASS", "bound": "FAIL", "missing": "MISS"}.get(c["kind"], "?") if c else "-"


def render(res):
    out = ["== round-four verdict on %s" % res["base"],
           "== WIN_CRITERIA.md gates 1-8 with both amendments; candidate gv-grav-c4, control gv-plain",
           "== script sha256 %s" % res["script_sha256"]]
    for key in ("main", "base"):
        t = res["tables"][key]
        out.append("== gate table: %s" % t["title"])
        for c in t["cells"]:
            out.append("[%s] %s: %s" % (c["status"], c["id"], c["question"]))
            out.append("       bounds: %s" % c["bounds"])
            for d in c["detail"]:
                out.append("       " + d)
            for k in c["checks"]:
                out.append("       %-58s = %-10s need %-12s %s" % (k["desc"], k["value"], k["bound"], "ok" if k["ok"] else "NOT MET"))
            if c["status"] != "PASS":
                out.append("       -> FAIL: " + c["reason"])
    out.append("== side by side (c4 = gv-grav-c4 vs gv-plain, main set; base = gv-grav-base vs gv-plain, base set)")
    out.append("   PASS = bounds met, FAIL = bound not met, MISS = metric missing, - = not measured per language")
    out.append("   %-30s" % "gate" + "".join("%-14s" % s for s in SCOPES))
    out.append("   %-30s" % "" + "".join("%-14s" % "c4 / base" for _ in SCOPES))
    idx = {k: {(c["gate"], c["scope"]): c for c in res["tables"][k]["cells"]} for k in ("main", "base")}
    for g in GATE_NAMES:
        out.append("   %-30s" % g + "".join("%-14s" % ("%s / %s" % (code(idx["main"].get((g, s))), code(idx["base"].get((g, s)))))
                                            for s in SCOPES))
    out.append("== attr set: gv-grav-c4 vs gv-grav-base (aa-c4 net is the noise floor for the improvement rule)")
    for s, a in res["attr"].items():
        out.append("   %-8s votes %d: c4 %d, base %d, tie %d, net %+d; aa-c4 net %+d (%d votes)%s" % (
            s, a["votes"], a["c4_wins"], a["base_wins"], a["ties"], a["net"], a["aa_c4_net"], a["aa_c4_votes"],
            "" if a["complete"] else "  incomplete: " + summarize(a["missing"], 2)))
    imp = res["improvement"]
    out.append("== improvement over the previous best (reported for the stop rule, not part of the verdict)")
    for k in imp["checks"]:
        out.append("   %-62s = %-10s need %-10s %s" % (k["desc"], k["value"], k["bound"], "ok" if k["ok"] else "NOT MET"))
    out.append("   cells c4 passes and base fails: %s" % (", ".join(imp["c4_passes_base_fails"]) or "none"))
    out.append("   cells base passes and c4 fails: %s" % (", ".join(imp["base_passes_c4_fails"]) or "none"))
    out.append(imp["line"])
    out.append("== reported beside the verdict (not gates)")
    out += res["report_lines"]
    out.append(res["verdict_line"])
    return out


def write_results(res, base):
    with open(os.path.join(base, "verdict4.json"), "w", encoding="utf-8") as f:
        json.dump(jsonable(res), f, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------------------------------------- self-test

FILL = {"zh": "这是一段用于自测的合成文字，没有实际含义。",
        "en": "This is synthetic self-test text with no real meaning. ",
        "ja": "これは自己テスト用の合成テキストで、実際の意味はありません。",
        "ko": "이것은 자체 시험용 합성 문장이며 실제 의미는 없습니다. "}
EXTRA = {
    "plain": {"zh": ["这可能需要时间。"] * 3 + ["通常需要十天。"] * 2,
              "en": ["This may take time. "] * 3 + ["It usually takes ten days. "] * 2,
              "ja": ["時間がかかるかもしれません。"] * 3 + ["通常は十日かかります。"] * 2,
              "ko": ["아마 시간이 걸립니다. "] * 3 + ["보통은 열흘 걸립니다. "] * 2},
    "grav": {"zh": ["这不可能。", "这可能需要时间。", "通常需要十天。"],
             "en": ["It opened on May 5, 2026. ", "This may take time. ", "It usually takes ten days. "],
             "ja": ["時間がかかるかもしれません。", "通常は十日かかります。"],
             "ko": ["아마 시간이 걸립니다. ", "보통은 열흘 걸립니다. "]},
    "swap": {"zh": ["这不可能。"] + ["通常如此。", "一般如此。"] * 6,
             "en": ["It opened on May 5, 2026. "] + ["It usually works. ", "It generally works. "] * 6,
             "ja": ["一般的にそうです。", "通常はそうです。"] * 6,
             "ko": ["일반적으로 그렇습니다. ", "보통은 그렇습니다. "] * 6},
    # near the bounds: second list about 1.18x plain (above 1.10); first list about 1.06x plain (above 1.00)
    "mild_second": {"zh": ["这不可能。", "这可能需要时间。"] + ["通常需要十天。"] * 2,
                    "en": ["It opened on May 5, 2026. ", "This may take time. "] + ["It usually takes ten days. "] * 2,
                    "ja": ["時間がかかるかもしれません。"] + ["通常は十日かかります。"] * 2,
                    "ko": ["아마 시간이 걸립니다. "] + ["보통은 열흘 걸립니다. "] * 2},
    "mild_first": {"zh": ["这可能需要时间。"] * 3 + ["通常需要十天。"],
                   "en": ["This may take time. "] * 3 + ["It usually takes ten days. "],
                   "ja": ["時間がかかるかもしれません。"] * 3 + ["通常は十日かかります。"],
                   "ko": ["아마 시간이 걸립니다. "] * 3 + ["보통은 열흘 걸립니다. "]},
}


def synth_text(case, arm, rnd, kw):
    lg, ci, ri = lang_of(case), EXPECTED_CASES.index(case), ROUNDS.index(rnd)
    n = 40 + ci % 3 + 2 * ri
    if arm == PLAIN:
        k, extra = n, EXTRA["plain"][lg]
    elif arm == C4:
        if kw.get("gut") or (case, rnd) == kw.get("short_pair"):
            k = n // 2
        elif kw.get("c4_long"):
            k = n * 106 // 100
        elif kw.get("hedge_mild") == "first":
            k = n * 96 // 100
        else:
            k = n * 85 // 100
        extra = EXTRA["swap" if kw.get("hedge_swap") else "mild_" + kw["hedge_mild"] if kw.get("hedge_mild") else "grav"][lg]
    else:
        k = n * 85 // 100 if kw.get("base_good") else n * 110 // 100
        extra = EXTRA["grav"][lg]
    return FILL[lg] * k + "".join(extra)


def make_synthetic(base, **kw):
    """A dataset in which gv-grav-c4 clearly wins everything and improves on gv-grav-base (whose answers are longer
    than plain's, so it fails gate 3), unless a knob says otherwise. Returns pids and notes for the mutations."""
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
    bmap, grades, pids, cnt = {}, {}, {}, [0]

    def pid():
        cnt[0] += 1
        return "p%03d" % cnt[0]

    def side(sc, kp, notes):
        d = dict(zip(DIMS, sc))
        d.update({"added_claim_errors": notes, "key_points": dict(zip(kp_ids, kp))})
        return d

    good = ((8, 9, 9, 8, 8), ("correct", "correct", "correct", "correct", "vague"))
    weak = ((6, 6, 7, 6, 7), ("correct", "correct", "vague", "vague", "wrong"))
    even = ((7, 8, 7, 7, 7), ("correct",) * 5)
    aa_out = {"aa-plain": ["r1", "r1", "r2", "tie", "tie", "tie"], "aa-c4": ["r2", "r2", "r1", "tie", "tie", "tie"]}
    if kw.get("noise"):
        aa_out["aa-plain"] = ["r1"] * 6
    if kw.get("attr_noise") or kw.get("noise_c4"):
        aa_out["aa-c4"] = ["r1"] * 6
    pos = {c: sum(1 for d in EXPECTED_CASES if lang_of(d) == lang_of(c) and d < c) for c in EXPECTED_CASES}
    for ci, c in enumerate(EXPECTED_CASES):
        lg = lang_of(c)
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
                for g in GRADERS:
                    if s == "attr":
                        win = "tie" if kw.get("attr_ties") or (kw.get("attr_noise") and g == "opus") else xs
                        gx, gy = side(*good, []), side(*even, [])
                    else:
                        tag = "c4" if x == C4 else "base"
                        win = xs
                        if s == "main" and lg == kw.get("lang_fail"):
                            win = ys
                        if s == "main" and (kw.get("noise") or kw.get("noise_c4")) and g == "opus":
                            win = "tie"
                        if s == "main" and kw.get("equal"):
                            gx = side(*weak, ["synthetic c4 wrong-claim %s %s %d: fee not in the key" % (p, g, k) for k in (1, 2)])
                        else:
                            gx = side(*good, ["synthetic %s claim %s %s: date not in the key" % (tag, p, g)])
                        gy = side(*weak, ["synthetic plain wrong-claim %s %s %d: fee not in the key" % (p, g, k) for k in (1, 2)])
                    grades[(g, p)] = {"pair": p, "winner": win, "margin": "clear", xs: gx, ys: gy, "reasons": "synthetic"}
        for s, arm in AA_SETS.items():
            p = pid()
            pids[(s, c)] = p
            a_r1 = ci % 2 == 0
            bmap[p] = {"set": s, "case": c, "round": "r1r2", "A": arm, "B": arm,
                       "A_round": "r1" if a_r1 else "r2", "B_round": "r2" if a_r1 else "r1"}
            for gi, g in enumerate(GRADERS):
                o = aa_out[s][pos[c] * 2 + gi]
                win = "tie" if o == "tie" else ("A" if (o == "r1") == a_r1 else "B")
                grades[(g, p)] = {"pair": p, "winner": win, "margin": "slight",
                                  "A": side(*even, []), "B": side(*even, []), "reasons": "synthetic"}
        for r in ROUNDS:
            for arm in ARMS:
                wt("raw/%s.%s.%s.txt" % (c, arm, r), synth_text(c, arm, r, kw))
                ev = [{"type": "status", "phase": "step_start"}, {"type": "tool_call", "callId": "c1", "tool": "pwsh"},
                      {"type": "tool_result", "callId": "c1", "status": "completed"}]
                if ci == 0 and r == "r1":
                    ev += [{"type": "tool_call", "callId": "c2", "tool": "web_fetch"},
                           {"type": "tool_result", "callId": "c2", "status": "completed"}]
                wt("raw/%s.%s.%s.ndjson" % (c, arm, r), "".join(json.dumps(e) + "\n" for e in ev))
    wj("blind-map.json", bmap)
    for (g, p), obj in grades.items():
        wj("blind/grades/%s/%s.json" % (g, p), obj)
    notes, nid = [], 0
    for (g, p), obj in sorted(grades.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        for sd in "AB":
            for note in obj[sd]["added_claim_errors"]:
                notes.append({"id": nid, "pid": p, "side": sd, "grader": g, "note": note})
                nid += 1
    wj("claim-notes.json", notes)
    for who in RELABELLERS:
        wj("labels-%s.json" % who, [{"id": x["id"], "label": "wrong" if "wrong-claim" in x["note"] else "unverified",
                                     "cite": "key line 3" if "wrong-claim" in x["note"] else ""} for x in notes])
    return {"pid": pids, "notes": notes}


def selftest():
    results = []

    def expect(label, cond, info=""):
        print(("[ok]  " if cond else "[BAD] ") + label + (("  -- " + info) if info else ""))
        results.append(bool(cond))

    def jload(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)

    def jdump(p, obj):
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)

    def serialises(res):
        try:
            json.dumps(jsonable(res), ensure_ascii=False)
            return True
        except (TypeError, ValueError):
            return False

    def cells_as(tag, res, missing=(), bound=(), table="main"):
        """Named cells fail as stated; every other cell of the table must PASS."""
        cells = {c["id"]: c for c in res["tables"][table]["cells"]}
        for cid in sorted(set(missing) | set(bound), key=CELL_IDS.index):
            c = cells[cid]
            want = "missing" if cid in missing else "bound"
            expect("%s: %s %s FAILS %s" % (tag, table, cid, "as metric missing" if want == "missing" else "on its bound"),
                   c["status"] == "FAIL" and c["kind"] == want, "%s %s" % (c["status"], c["reason"][:120]))
        rest = [cid for cid in CELL_IDS if cid not in missing and cid not in bound]
        bad = ["%s %s" % (cid, cells[cid]["reason"][:80]) for cid in rest if cells[cid]["status"] != "PASS"]
        expect("%s: the other %d %s cells PASS" % (tag, len(rest), table), not bad, summarize(bad, 3))

    def grade_cells(lang):
        return {"g1_votes[overall]", "g2_each_grader[overall]", "g4_vague_key_points[overall]",
                "g5_wrong_added_claims[overall]", "g6_correct_wrong_key_points[overall]", "g7_trap_under_8[overall]",
                "g1_votes[%s]" % lang, "g4_vague_key_points[%s]" % lang, "g5_wrong_added_claims[%s]" % lang,
                "g6_correct_wrong_key_points[%s]" % lang, "g7_trap_under_8[%s]" % lang}

    def text_cells(lang):
        return {"g3_length[overall]", "g8_hedging[overall]", "g3_length[%s]" % lang, "g8_hedging[%s]" % lang}

    def every(gate):
        return {"%s[%s]" % (gate, s) for s in SCOPES}

    base_g3 = every("g3_length")   # default synthetic base answers are longer than plain's

    root = tempfile.mkdtemp(prefix="verdict4-selftest-")
    if os.path.normcase(os.path.abspath(root)).startswith(os.path.normcase(HERE)):
        print("temporary folder lies inside the real folder; refusing")
        return 1
    try:
        # ---- pattern units
        for text, lang, which, want, label in (
                ("这不可能。", "zh", "first", 0, "zh: 不可能 is not a hedge"),
                ("这可能需要时间。", "zh", "first", 1, "zh: 可能 is a hedge"),
                ("请拨打12333问一下", "zh", "second", 1, "zh: 打 + five-digit number + 问"),
                ("具体以当地规定为准", "zh", "second", 2, "zh: 具体…为准 and 以…为准 both count"),
                ("It opened on May 5, 2026.", "en", "first", 0, "en: 'May 5' is a date"),
                ("Due in May 2026.", "en", "first", 0, "en: 'May 2026' is a date"),
                ("You may need it.", "en", "first", 1, "en: 'may' is a hedge"),
                ("It may vary; check with the office.", "en", "second", 2, "en: may vary + check with"),
                ("変わるかもしれません。おそらく大丈夫です。", "ja", "first", 2, "ja: かもしれ + おそらく"),
                ("一般的には、自治体によって異なります。", "ja", "second", 2, "ja: 一般的に + 自治体によ"),
                ("这可能需要时间，一般来说。", "ja", "first", 0, "ja list does not count Chinese 可能"),
                ("这可能需要时间，一般来说。", "ja", "second", 0, "ja list does not count Chinese 一般"),
                ("확인해 보세요. 확인해보세요.", "ko", "first", 2, "ko: 확인해 보세요 with and without the space"),
                ("아마도 그럴 겁니다.", "ko", "first", 1, "ko: 아마"),
                ("지역마다 다를 수 있습니다.", "ko", "second", 2, "ko: 지역마다 + 다를 수 있"),
                ("일반적으로 문의하세요.", "ko", "second", 2, "ko: 일반적으로 + 문의하"),
                ("This may take time.", "zh", "first", 0, "zh list does not count English 'may'")):
            got = count_markers(text, HEDGE[lang][which], (lang,))
            expect("pattern %s (%r -> %d)" % (label, text, got), got == want, "" if got == want else "want %d" % want)

        # ---- (a) empty input
        b = os.path.join(root, "a-empty")
        os.makedirs(b)
        res = evaluate(b)
        expect("(a) empty input: the main table has the %d gate cells" % len(CELL_IDS),
               [c["id"] for c in res["tables"]["main"]["cells"]] == CELL_IDS)
        for t in ("main", "base"):
            bad = [c["id"] for c in res["tables"][t]["cells"] if not (c["status"] == "FAIL" and c["kind"] == "missing"
                                                                      and c["reason"].startswith("metric missing"))]
            expect("(a) empty input: every %s cell FAILS as metric missing (%d cells)" % (t, len(CELL_IDS)), not bad,
                   summarize(bad, 3))
        for cid in CELL_IDS:
            c = next(x for x in res["tables"]["main"]["cells"] if x["id"] == cid)
            expect("(a) empty input: %s FAILS as metric missing" % cid, c["kind"] == "missing", c["reason"][:90])
        expect("(a) empty input: verdict 'not a win' naming all %d cells" % len(CELL_IDS),
               res["verdict_line"].startswith("VERDICT: not a win") and res["failing"] == CELL_IDS, res["verdict_line"][:80])
        expect("(a) empty input: IMPROVEMENT: no (metric missing)",
               res["improvement"]["line"].startswith("IMPROVEMENT: no (metric missing"), res["improvement"]["line"][:90])
        expect("(a) empty input: last rendered line is the verdict", render(res)[-1] == res["verdict_line"])
        expect("(a) empty input: results serialise to JSON", serialises(res))

        # ---- (a2) case list only
        b = os.path.join(root, "a2-prompts-only")
        os.makedirs(os.path.join(b, "prompts"))
        for c in EXPECTED_CASES:
            open(os.path.join(b, "prompts", c + ".txt"), "w").close()
        res = evaluate(b)
        bad = [c["id"] for c in res["tables"]["main"]["cells"] if c["kind"] != "missing"]
        expect("(a2) case list only: every main cell FAILS as metric missing", not bad, summarize(bad, 3))

        # ---- (b) synthetic clear win
        b = os.path.join(root, "b-win")
        os.makedirs(b)
        make_synthetic(b)
        res = evaluate(b)
        cells_as("(b) synthetic win", res)
        cells_as("(b) synthetic win", res, bound=base_g3, table="base")
        expect("(b) synthetic win: verdict line is 'VERDICT: win'", res["verdict_line"] == "VERDICT: win", res["verdict_line"][:80])
        expect("(b) synthetic win: last rendered line is 'VERDICT: win'", render(res)[-1] == "VERDICT: win")
        expect("(b) synthetic win: IMPROVEMENT: yes (36 vs 31 cells, attr net +48 > floor 4)",
               res["improvement"]["improvement"] == "yes" and res["improvement"]["c4_cells_passed"] == 36
               and res["improvement"]["base_cells_passed"] == 31 and res["improvement"]["attr_net"] == 48
               and res["improvement"]["aa_c4_floor"] == 4, res["improvement"]["line"][:120])
        m1 = next(c for c in res["tables"]["main"]["cells"] if c["id"] == "g1_votes[ko]")["measured"]
        expect("(b) synthetic win: g1_votes[ko] measures net 12 against a per-language floor of 1",
               m1.get("net") == 12 and m1.get("noise_floor") == 1, str({k: m1.get(k) for k in ("net", "noise_floor")}))
        for lg, want in (("zh", (18, 12, 6, 6)), ("en", (18, 12, 6, 6)), ("ja", (18, 12, 6, 6)), ("ko", (18, 12, 6, 6))):
            m8 = next(c for c in res["tables"]["main"]["cells"] if c["id"] == "g8_hedging[%s]" % lg)["measured"]
            got = (m8["first"]["markers_" + PLAIN], m8["second"]["markers_" + PLAIN],
                   m8["first"]["markers_" + C4], m8["second"]["markers_" + C4])
            expect("(b) synthetic win: g8_hedging[%s] counts the language's own markers (plain 18/12, c4 6/6 after "
                   "exclusions)" % lg, got == want, "got %s" % (got,))
        write_results(res, b)
        back = jload(os.path.join(b, "verdict4.json"))
        expect("(b) synthetic win: verdict4.json written and read back", back.get("verdict") == "win"
               and len(back["tables"]["main"]["cells"]) == len(CELL_IDS))

        def variant(tag, mutate=None, missing=(), bound=(), verdict=None, **kw):
            b = os.path.join(root, re.sub(r"[^A-Za-z0-9]+", "-", tag.split(")")[0]).strip("-"))
            os.makedirs(b)
            inf = make_synthetic(b, **kw)
            if mutate:
                mutate(b, inf)
            r_ = evaluate(b)
            cells_as(tag, r_, missing, bound)
            fails = sorted(set(missing) | set(bound), key=CELL_IDS.index)
            want = "VERDICT: win" if not fails else "VERDICT: not a win (failing: %s)" % ", ".join(fails)
            expect("%s: %s" % (tag, want[:90]), r_["verdict_line"] == want, r_["verdict_line"][:120])
            return r_

        P = lambda inf, *k: inf["pid"][k]

        # ---- (c) one language fails
        variant("(c) ko votes go to plain, all else a win", bound={"g1_votes[ko]"}, lang_fail="ko")

        # ---- (d) one input removed or malformed at a time
        def drop_grade(b, inf):
            os.remove(os.path.join(b, "blind", "grades", "opus", P(inf, "main", "ja-medical-deduction", "r1") + ".json"))

        def drop_label(b, inf):
            p = os.path.join(b, "labels-opus.json")
            pid = P(inf, "main", "en-529-roth", "r1")
            target = next(x["id"] for x in inf["notes"] if x["pid"] == pid)
            jdump(p, [x for x in jload(p) if x["id"] != target])

        def drop_text(b, inf):
            os.remove(os.path.join(b, "raw", "zh-flex-hours.%s.r2.txt" % C4))

        def empty_text(b, inf):
            with open(os.path.join(b, "raw", "en-fsa-rollover.%s.r1.txt" % PLAIN), "w", encoding="utf-8") as f:
                f.write("  \n")

        def drop_aa_grade(b, inf):
            os.remove(os.path.join(b, "blind", "grades", "sonnet", P(inf, "aa-plain", "ko-severance-pay") + ".json"))

        def bad_keypoints(b, inf):
            p = os.path.join(b, "blind", "grades", "sonnet", P(inf, "main", "ko-jeonse-protection", "r2") + ".json")
            obj = jload(p)
            obj["A"]["key_points"].pop("5")
            obj["A"]["key_points"]["6"] = "correct"
            jdump(p, obj)

        def wrong_without_cite(b, inf):
            p = os.path.join(b, "labels-sonnet.json")
            pid = P(inf, "main", "zh-sick-pay", "r1")
            ids = {x["id"] for x in inf["notes"] if x["pid"] == pid and "wrong-claim" in x["note"]}
            labs = jload(p)
            next(x for x in labs if x["id"] in ids)["cite"] = ""
            jdump(p, labs)

        def drop_note_row(b, inf):
            p = os.path.join(b, "claim-notes.json")
            pid = P(inf, "main", "ja-part-time-leave", "r2")
            rows = jload(p)
            i = next(i for i, x in enumerate(rows) if x["pid"] == pid)
            jdump(p, rows[:i] + rows[i + 1:])

        def dup_main_pair(b, inf):
            p = os.path.join(b, "blind-map.json")
            m = jload(p)
            m["p999"] = dict(m[P(inf, "main", "en-medicare-part-b", "r2")])
            jdump(p, m)

        def unknown_set(b, inf):
            p = os.path.join(b, "blind-map.json")
            m = jload(p)
            m["q001"] = {"set": "posthoc", "case": "zh-sick-pay", "round": "r1", "A": C4, "B": PLAIN}
            jdump(p, m)

        variant("(d1) one main-set grade removed (ja)", drop_grade, missing=grade_cells("ja"))
        variant("(d2) one relabel entry removed (en)", drop_label,
                missing={"g5_wrong_added_claims[overall]", "g5_wrong_added_claims[en]"})
        variant("(d3) one gv-grav-c4 final text removed (zh)", drop_text, missing=text_cells("zh"))
        variant("(d4) one gv-plain final text empty (en)", empty_text, missing=text_cells("en"))
        r_ = variant("(d5) one A/A grade removed (ko aa-plain)", drop_aa_grade, missing={"g1_votes[overall]", "g1_votes[ko]"})
        expect("(d5) one A/A grade removed: IMPROVEMENT: no (metric missing)",
               r_["improvement"]["line"].startswith("IMPROVEMENT: no (metric missing"), r_["improvement"]["line"][:90])
        variant("(d6) one grade's key_points ids differ from the case's (ko)", bad_keypoints, missing=grade_cells("ko"))
        variant("(d7) one 'wrong' relabel without a cite (zh)", wrong_without_cite,
                missing={"g5_wrong_added_claims[overall]", "g5_wrong_added_claims[zh]"})
        variant("(d8) one claim-notes row removed (ja)", drop_note_row,
                missing={"g5_wrong_added_claims[overall]", "g5_wrong_added_claims[ja]"})
        variant("(d9) a duplicated main pair in blind-map (en)", dup_main_pair, missing=grade_cells("en"))
        r_ = variant("(d10) an entry of an unknown set in blind-map is ignored", unknown_set)
        expect("(d10) the ignored entry is reported", any("q001" in w for w in r_["reported"]["inputs"]["map_warnings"]))

        # ---- (e) degenerate wins fail on their bounds
        variant("(e1) gutted gv-grav-c4 answers (half length)", bound=every("g3_length"), gut=True)
        variant("(e2) one en pair under 0.6 (1 of 6 fails en; 1 of 24 passes overall)", bound={"g3_length[en]"},
                short_pair=("en-529-roth", "r1"))
        variant("(e3) hedge substitution (second-list hedges only)", bound=every("g8_hedging"), hedge_swap=True)
        r_ = variant("(e4) net equals the A/A noise floor (opus all ties; aa-plain all r1)",
                     bound=every("g1_votes") | {"g2_each_grader[overall]"}, noise=True)
        variant("(e5) c4 answers graded exactly like plain's (equal counts pass 'no more than' / 'at least')", equal=True)
        variant("(e6) net equals the aa-c4 floor (opus all ties; aa-c4 all r1)",
                bound=every("g1_votes") | {"g2_each_grader[overall]"}, noise_c4=True)
        r6 = variant("(e7) c4 median a little longer than plain (ratio about 1.02-1.03)", bound=every("g3_length"), c4_long=True)
        rts = [next(c for c in r6["tables"]["main"]["cells"] if c["id"] == "g3_length[%s]" % s)["measured"]["median_ratio"]
               for s in SCOPES]
        expect("(e7) every median ratio lies in (1.00, 1.05)", all(1 < x < Fraction(105, 100) for x in rts),
               ", ".join(fmt(x) for x in rts))
        for which, tag in (("second", "(e8) second-list hedging about 1.18x plain (bound 1.10)"),
                           ("first", "(e9) first-list hedging about 1.06x plain (bound 1.00)")):
            r8 = variant(tag, bound=every("g8_hedging"), hedge_mild=which)
            lo, hi = (Fraction(11, 10), Fraction(2)) if which == "second" else (Fraction(1), Fraction(11, 10))
            rs = [next(c for c in r8["tables"]["main"]["cells"] if c["id"] == "g8_hedging[%s]" % s)["measured"][which]["ratio"]
                  for s in SCOPES]
            expect("%s every %s-list ratio lies in (%s, %s)" % (tag.split(")")[0] + ")", which, fmt(lo, 2), fmt(hi, 2)),
                   all(lo < x < hi for x in rs), ", ".join(fmt(x) for x in rs))
        m1 = next(c for c in r_["tables"]["main"]["cells"] if c["id"] == "g1_votes[overall]")["measured"]
        expect("(e4) net 24 and noise floor 24 measured", m1.get("net") == 24 and m1.get("noise_floor") == 24,
               str({k: m1.get(k) for k in ("net", "noise_floor")}))

        # ---- (f) improvement rule
        r_ = variant("(f1) attr votes all ties", attr_ties=True)
        expect("(f1) attr all ties: IMPROVEMENT: no (attr net +0 not above floor 4)",
               r_["improvement"]["improvement"] == "no" and not r_["improvement"]["missing"], r_["improvement"]["line"][:120])
        r_ = variant("(f2) attr net equals the aa-c4 floor (opus ties; aa-c4 all r1)", attr_noise=True)
        expect("(f2) attr net 24 = floor 24: IMPROVEMENT: no",
               r_["improvement"]["improvement"] == "no" and r_["improvement"]["attr_net"] == 24
               and r_["improvement"]["aa_c4_floor"] == 24, r_["improvement"]["line"][:120])

        def drop_base_grade(b, inf):
            os.remove(os.path.join(b, "blind", "grades", "opus", P(inf, "base", "zh-insurance-gap", "r1") + ".json"))

        r_ = variant("(f3) one base-set grade removed: the verdict does not depend on it", drop_base_grade)
        cells_as("(f3) one base-set grade removed", r_, missing=grade_cells("zh"), bound=base_g3, table="base")
        expect("(f3) one base-set grade removed: IMPROVEMENT: no (metric missing)",
               r_["improvement"]["line"].startswith("IMPROVEMENT: no (metric missing"), r_["improvement"]["line"][:90])
        r_ = variant("(f4) base passes every cell too", base_good=True)
        cells_as("(f4) base passes every cell too", r_, table="base")
        expect("(f4) equal cell counts (36 = 36) and attr above floor: IMPROVEMENT: yes",
               r_["improvement"]["improvement"] == "yes", r_["improvement"]["line"][:120])
        r_ = variant("(f5) c4 fails hedging, base passes everything", bound=every("g8_hedging"), base_good=True, hedge_swap=True)
        expect("(f5) c4 31 < base 36 cells: IMPROVEMENT: no",
               r_["improvement"]["improvement"] == "no" and r_["improvement"]["c4_cells_passed"] == 31
               and r_["improvement"]["base_cells_passed"] == 36, r_["improvement"]["line"][:120])
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
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    base = os.path.abspath(a.base)
    res = evaluate(base)
    print("\n".join(render(res)))
    write_results(res, base)
    sys.exit(0)


if __name__ == "__main__":
    main()
