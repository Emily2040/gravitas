#!/usr/bin/env python3
"""Round-three verdict: does Gravitas (gv-grav) beat plain (gv-plain) on the held-out set?

Implements the amended verdict rule in criteria.md ("Verdict rule (replaces the one above)",
items 1-10) as ten named gates, then prints the items criteria.md reports beside the verdict.
Written and frozen by an agent that builds nothing in this round, from criteria.md alone.

    python verdict.py              evaluate the folder this script sits in, print, write verdict.json
    python verdict.py --selftest   self-test in a temporary folder (never touches the real data)

Standard library only. A missing or malformed metric fails its gate with "metric missing";
nothing missing is ever defaulted to a passing value. Comparisons are exact (fractions).
"""
import argparse
import datetime
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

# The ten held-out requests named in criteria.md ("Held-out set"). prompts/ must hold exactly these.
EXPECTED_CASES = sorted([
    "zh-resignation", "zh-express-lost", "zh-deceased-deposit", "zh-driving-points", "zh-medical-family",
    "zh-id-card-lost", "zh-game-refund", "en-car-warranty", "en-flight-refund", "en-social-security",
])
GRADERS = ("opus", "sonnet")
RELABELLERS = ("sonnet", "opus")
ROUNDS = ("r1", "r2")
GRAV, PLAIN, NOCHECK, DRAFT = "gv-grav", "gv-plain", "gv-grav-nocheck", "gv-grav-draft"
DIMS = ("correct", "trap", "honest", "useful", "concise")
KP_MARKS = ("correct", "vague", "wrong", "missing")
LABELS = ("wrong", "unverified", "not an error")
PAIR_SETS = {"main": (GRAV, PLAIN), "attr": (GRAV, NOCHECK), "draft": (GRAV, DRAFT)}
AA_SETS = {"aa-plain": PLAIN, "aa-grav": GRAV}
KNOWN_SETS = ("main", "attr", "aa-plain", "aa-grav", "draft")
OUTCOMES = ("absent", "supported", "computed", "derived", "dependent", "unsupported", "miscalculated", "skipped")
PID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

# Hedge markers, round-one list: exactly tally.py's H (rounds one and two).
H_ROUND1 = ["可能", "大概", "也许", "或许", "以.{0,12}为准", "建议.{0,6}核实", "建议.{0,6}确认", "不确定", "请咨询", "仅供参考",
            r"\bmay\b", r"\bmight\b", r"\bprobably\b", r"\bcheck with\b", r"\bconfirm with\b", r"\bnot sure\b", r"\bverify\b"]
# Extended list, criteria item 9, exactly the items listed there (it repeats 以…为准 and 建议…核实/确认, so it
# is a list of its own, not round one plus additions). "…" gaps: 建议 keeps tally.py's 6, the rest 12.
# 打…五位号码…问 is read as 打, then a five-digit number (or the literal 五位号码), then 问.
H_EXTENDED = ["一般", "通常", "原则上", "视.{0,12}而定", "具体.{0,12}(?:咨询|确认|为准)", "向.{0,12}(?:咨询|询问|核实|确认)",
              "各地.{0,12}(?:不同|不一)", "因地而异", "建议.{0,6}(?:核实|确认|咨询)", "以.{0,12}为准",
              r"打.{0,12}(?:(?<!\d)\d{5}(?!\d)|五位号码).{0,12}问",
              r"\btypically\b", r"\busually\b", r"\bgenerally\b", r"\bdepending on\b", r"\bmay vary\b", r"\bcan vary\b",
              r"\bcontact the\b", r"\bcheck (?:the|with)\b", r"\breach out\b", r"\bdouble[- ]check\b"]
# Exclusions (criteria item 9): "May" followed by a day number or a year, and 不可能.
MAY_MONTH = re.compile(r"May,?\s+(?:\d{1,2}(?:st|nd|rd|th)?\b|\d{4}\b)")
# Fabricated-source phrases, criteria item 10.
FAB = ["据.{0,12}(?:官网|公告)", "根据.{0,12}(?:规定|通知)", "经(?:查询|核实)", "官方显示",
       r"\baccording to\b", r"\bper the official\b", r"\bI (?:checked|verified)\b"]
# Meta wording in a steered run's final (criteria "Validity of each run"); reported only.
META = ["Gravitas", "核对", "修改后", "修订", "重新给出", "已删除", "其余不变",
        r"\brevised\b", r"\bupdated reply\b", r"\bI removed\b", r"\bthis check\b", r"\bas above\b"]

GATE_NAMES = ["g1_net_votes", "g2_each_grader", "g3_prompts", "g4_mean_scores", "g5_key_points",
              "g6_wrong_claims", "g7_trap_under_8", "g8_length", "g9_hedging", "g10_fabricated_sources"]


# ----------------------------------------------------------------------------------------------- patterns

def count_patterns(text, patterns, exclude=True):
    """Matches of each pattern summed (as tally.py does); with exclude, skip 不可能 and May-as-a-date."""
    n = 0
    for p in patterns:
        for m in re.finditer(p, text, flags=re.I):
            if exclude:
                s = m.start()
                if m.group().startswith("可能") and s > 0 and text[s - 1] == "不":
                    continue
                if text.startswith("May", s) and MAY_MONTH.match(text, s):
                    continue
            n += 1
    return n


# ----------------------------------------------------------------------------------------------- readers

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
        return None, "prompts/ does not hold the 10 held-out cases of criteria.md (missing %s, extra %s)" % (miss, extra)
    return stems, None


def load_map(base, cases):
    issues = {k: [] for k in ("global",) + KNOWN_SETS}
    entries, idx = {}, {s: defaultdict(list) for s in KNOWN_SETS}
    main_index, aa_index = {}, {s: {} for s in AA_SETS}
    m, err = rd_json(os.path.join(base, "blind-map.json"))
    if err:
        issues["global"].append("blind-map.json " + err)
        return entries, issues, main_index, aa_index, idx
    if not isinstance(m, dict) or not m:
        issues["global"].append("blind-map.json is not a non-empty object")
        return entries, issues, main_index, aa_index, idx
    cs = set(cases or [])
    for pid, e in m.items():
        if not PID_RE.match(pid):
            issues["global"].append("pid %r is not a plain file name" % pid)
            continue
        if not isinstance(e, dict) or e.get("set") not in KNOWN_SETS:
            issues["global"].append("%s: entry is not an object with a known set" % pid)
            continue
        s, c, A, B = e["set"], e.get("case"), e.get("A"), e.get("B")
        if not isinstance(c, str) or (cases is not None and c not in cs):
            issues[s].append("%s: case %r not in the case list" % (pid, c))
            continue
        if not isinstance(A, str) or not isinstance(B, str):
            issues[s].append("%s: A/B arms missing" % pid)
            continue
        if s in AA_SETS:
            if A != AA_SETS[s] or B != AA_SETS[s]:
                issues[s].append("%s: %s pair must be %s vs %s, is %s vs %s" % (pid, s, AA_SETS[s], AA_SETS[s], A, B))
                continue
            if {e.get("A_round"), e.get("B_round")} != set(ROUNDS):
                issues[s].append("%s: A_round/B_round must be r1 and r2" % pid)
                continue
            idx[s][c].append(pid)
        else:
            if e.get("round") not in ROUNDS:
                issues[s].append("%s: round %r not r1/r2" % (pid, e.get("round")))
                continue
            if A == B or {A, B} != set(PAIR_SETS[s]):
                issues[s].append("%s: %s pair must be %s vs %s, is %s vs %s" % (pid, s, PAIR_SETS[s][0], PAIR_SETS[s][1], A, B))
                continue
            idx[s][(c, e["round"])].append(pid)
        entries[pid] = e
    if cases is None:
        issues["global"].append("case list unavailable, pair coverage cannot be checked")
        return entries, issues, main_index, aa_index, idx
    for c in cases:
        for r in ROUNDS:
            p = idx["main"].get((c, r), [])
            if len(p) != 1:
                issues["main"].append("main %s %s has %d pairs in blind-map (need exactly 1)" % (c, r, len(p)))
            else:
                main_index[(c, r)] = p[0]
            for s in ("attr", "draft"):
                if len(idx[s].get((c, r), [])) > 1:
                    issues[s].append("%s %s %s has %d pairs" % (s, c, r, len(idx[s][(c, r)])))
        for s in AA_SETS:
            p = idx[s].get(c, [])
            if len(p) != 1:
                issues[s].append("%s %s has %d pairs in blind-map (need exactly 1)" % (s, c, len(p)))
            else:
                aa_index[s][c] = p[0]
    return entries, issues, main_index, aa_index, idx


def load_keypoints(base, cases):
    kp, issues = {}, {}
    for c in cases:
        j, err = rd_json(os.path.join(base, "keypoints", c + ".json"))
        if err:
            issues[c] = "keypoints/%s.json %s" % (c, err)
            continue
        if not isinstance(j, list) or not all(isinstance(x, dict) for x in j):
            issues[c] = "keypoints/%s.json is not a list of objects" % c
            continue
        ids = [str(x.get("id")).strip() if isinstance(x.get("id"), (str, int)) and not isinstance(x.get("id"), bool) else None
               for x in j]
        if None in ids or "" in ids or len(set(ids)) != len(ids):
            issues[c] = "keypoints/%s.json ids missing or repeated" % c
            continue
        if not all(isinstance(x.get("point"), str) and x["point"].strip() for x in j):
            issues[c] = "keypoints/%s.json has a point without text" % c
            continue
        if not 4 <= len(ids) <= 8:
            issues[c] = "keypoints/%s.json has %d points (criteria: 4 to 8)" % (c, len(ids))
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
        if not (isinstance(pid, str) and side in ("A", "B") and grader in GRADERS and isinstance(note, str) and note.strip()):
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
            bad[rid] = "'wrong' label without a cite (criteria: must cite a key line or an official page)"
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


def parse_jsonl(path):
    t, err = rd_text(path)
    if err:
        return None, err
    recs = []
    for i, line in enumerate(t.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        try:
            r = json.loads(s)
        except ValueError:
            return None, "line %d is not valid JSON" % i
        if not isinstance(r, dict):
            return None, "line %d is not an object" % i
        recs.append(r)
    return recs, None


def web_opened(events):
    calls = {e.get("callId"): e.get("tool") for e in events if e.get("type") == "tool_call"}
    return any(e.get("type") == "tool_result" and e.get("status") == "completed"
               and calls.get(e.get("callId")) in ("web_fetch", "web_search") for e in events)


class Data:
    def __init__(self, base):
        self.base = base
        self._text, self._events = {}, {}
        self.cases, self.case_issue = load_cases(base)
        self.entries, self.map_issues, self.main_index, self.aa_index, self.set_index = load_map(base, self.cases)
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


# ----------------------------------------------------------------------------------------------- helpers

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


def new_gate(name, question, bounds):
    return {"name": name, "question": question, "bounds": bounds, "measured": {}, "checks": [], "detail": [],
            "status": None, "reason": ""}


def check(g, desc, value, bound, ok):
    g["checks"].append({"desc": desc, "value": value, "bound": bound, "ok": bool(ok)})


def finish(g, missing=None):
    if missing:
        g["status"], g["reason"], g["missing"] = "FAIL", "metric missing: " + summarize(missing), list(dict.fromkeys(missing))
    elif not g["checks"]:
        g["status"], g["reason"] = "FAIL", "metric missing: nothing was measured"
    else:
        bad = [c["desc"] for c in g["checks"] if not c["ok"]]
        g["status"] = "FAIL" if bad else "PASS"
        g["reason"] = ("bound not met: " + "; ".join(bad)) if bad else "all bounds met"
    return g


def base_missing(D, sets=("main",)):
    m = [] if D.cases is not None else ["case list: " + D.case_issue]
    for s in ("global",) + tuple(sets):
        m += ["blind-map: " + x for x in D.map_issues[s]]
    return m


def main_votes(D, strict=True):
    """Main-set votes, one per (pair, grader). strict: (None, missing) unless all 40 are valid."""
    missing = base_missing(D)
    if strict and missing:
        return None, missing
    votes = []
    for (c, r), pid in sorted(D.main_index.items()):
        e = D.entries[pid]
        for g in GRADERS:
            gr, err = D.grades.get((g, pid), (None, "missing"))
            if err:
                missing.append("blind/grades/%s/%s.json (main %s %s): %s" % (g, pid, c, r, err))
                continue
            votes.append({"case": c, "round": r, "grader": g, "pid": pid, "entry": e, "grade": gr,
                          "win": "tie" if gr["winner"] == "tie" else e[gr["winner"]]})
    if strict and missing:
        return None, missing
    return votes, missing


def aa_votes(D, s, strict=True):
    """A/A votes; win is the round ('r1'/'r2') of the side picked, or 'tie'."""
    missing = base_missing(D, (s,))
    if strict and missing:
        return None, missing
    votes = []
    for c, pid in sorted(D.aa_index[s].items()):
        e = D.entries[pid]
        for g in GRADERS:
            gr, err = D.grades.get((g, pid), (None, "missing"))
            if err:
                missing.append("blind/grades/%s/%s.json (%s %s): %s" % (g, pid, s, c, err))
                continue
            w = gr["winner"]
            votes.append({"case": c, "grader": g, "pid": pid,
                          "win": "tie" if w == "tie" else e["%s_round" % w]})
    if strict and missing:
        return None, missing
    return votes, missing


def main_answers(votes):
    ans = {GRAV: [], PLAIN: []}
    for v in votes:
        for side in "AB":
            ans[v["entry"][side]].append(v["grade"][side])
    return ans


def main_texts(D, arms=(GRAV, PLAIN)):
    if D.cases is None:
        return None, ["case list: " + D.case_issue]
    out, missing = {}, []
    for c in D.cases:
        for r in ROUNDS:
            for a in arms:
                t, err = D.text(c, a, r)
                if err:
                    missing.append("raw/%s.%s.%s.txt %s" % (c, a, r, err))
                else:
                    out[(c, a, r)] = t
    return (None, missing) if missing else (out, [])


def wl(votes, a=GRAV, b=PLAIN):
    w = sum(v["win"] == a for v in votes)
    l = sum(v["win"] == b for v in votes)
    return w, l, len(votes) - w - l


# ----------------------------------------------------------------------------------------------- gates

def gate1(D):
    g = new_gate("g1_net_votes",
                 "Do the graders prefer Gravitas over plain by more than two runs of the same arm differ?",
                 "net = gv-grav wins - gv-plain wins (main set, 20 pairs x 2 graders): net > 0 and net > A/A noise "
                 "floor = max(|net aa-plain|, |net aa-grav|), A/A net = r1-side wins - r2-side wins (10 pairs x 2 graders each)")
    votes, missing = main_votes(D)
    missing = list(missing or [])
    aa = {}
    for s in AA_SETS:
        v, m = aa_votes(D, s)
        if m:
            missing += m
        else:
            aa[s] = v
    if missing:
        return finish(g, missing)
    w, l, t = wl(votes)
    net = w - l
    nets = {}
    for s, vs in aa.items():
        r1, r2 = sum(v["win"] == "r1" for v in vs), sum(v["win"] == "r2" for v in vs)
        nets[s] = r1 - r2
        g["measured"][s] = {"r1_wins": r1, "r2_wins": r2, "ties": len(vs) - r1 - r2, "net": r1 - r2, "votes": len(vs)}
    floor = max(abs(nets["aa-plain"]), abs(nets["aa-grav"]))
    g["measured"].update({"votes": len(votes), "grav_wins": w, "plain_wins": l, "ties": t, "net": net, "noise_floor": floor})
    g["detail"].append("main: %d votes, gv-grav %d, gv-plain %d, tie %d -> net %+d" % (len(votes), w, l, t, net))
    g["detail"].append("A/A: aa-plain net %+d, aa-grav net %+d -> noise floor %d" % (nets["aa-plain"], nets["aa-grav"], floor))
    check(g, "net votes > 0", net, "> 0", net > 0)
    check(g, "net votes > A/A noise floor", net, "> %d" % floor, net > floor)
    return finish(g)


def gate2(D):
    g = new_gate("g2_each_grader", "Does each grader, on its own, prefer Gravitas more often than plain?",
                 "for opus and for sonnet separately (main set, 20 votes each): gv-grav wins > gv-plain wins")
    votes, missing = main_votes(D)
    if missing:
        return finish(g, missing)
    for gr in GRADERS:
        vs = [v for v in votes if v["grader"] == gr]
        w, l, t = wl(vs)
        g["measured"][gr] = {"votes": len(vs), "grav_wins": w, "plain_wins": l, "ties": t}
        g["detail"].append("%s: %d votes, gv-grav %d, gv-plain %d, tie %d" % (gr, len(vs), w, l, t))
        check(g, "%s: gv-grav wins > gv-plain wins" % gr, "%d vs %d" % (w, l), "wins > losses", w > l)
    return finish(g)


def gate3(D):
    g = new_gate("g3_prompts", "Does Gravitas win on more requests than it loses, with the request as the unit?",
                 "per case: sum of its 4 main-set votes (+1 gv-grav win, -1 gv-plain win); "
                 "cases net-positive > cases net-negative (10 cases)")
    votes, missing = main_votes(D)
    if missing:
        return finish(g, missing)
    per = defaultdict(list)
    for v in votes:
        per[v["case"]].append(1 if v["win"] == GRAV else -1 if v["win"] == PLAIN else 0)
    nets = {c: sum(per[c]) for c in D.cases}
    pos, neg = sum(n > 0 for n in nets.values()), sum(n < 0 for n in nets.values())
    g["measured"] = {"case_net": nets, "positive": pos, "negative": neg, "zero": len(nets) - pos - neg,
                     "votes_per_case": {c: len(per[c]) for c in D.cases}}
    g["detail"].append("cases net-positive %d, net-negative %d, zero %d" % (pos, neg, len(nets) - pos - neg))
    g["detail"].append(" ".join("%s %+d" % (c, n) for c, n in sorted(nets.items())))
    check(g, "cases net-positive > cases net-negative", "%d vs %d" % (pos, neg), "positive > negative", pos > neg)
    return finish(g)


def gate4(D):
    g = new_gate("g4_mean_scores",
                 "Is Gravitas scored at least as well overall, without losing more than half a point on correct or useful?",
                 "means over all main-set graded answers per arm (40 each): total(5 scores) gv-grav >= gv-plain; "
                 "correct gv-grav >= gv-plain - 0.5; useful gv-grav >= gv-plain - 0.5")
    votes, missing = main_votes(D)
    if missing:
        return finish(g, missing)
    ans = main_answers(votes)
    m = {}
    for a in (GRAV, PLAIN):
        m[a] = {"n": len(ans[a]), "total": mean([sum(x["scores"].values()) for x in ans[a]])}
        m[a].update({d: mean([x["scores"][d] for x in ans[a]]) for d in DIMS})
    g["measured"] = m
    for a in (GRAV, PLAIN):
        g["detail"].append("%-8s n=%d total %s | %s" % (a, m[a]["n"], fmt(m[a]["total"], 2),
                                                        " ".join("%s %s" % (d, fmt(m[a][d], 2)) for d in DIMS)))
    half = Fraction(1, 2)
    check(g, "mean total gv-grav >= gv-plain", fmt(m[GRAV]["total"]), ">= %s" % fmt(m[PLAIN]["total"]),
          m[GRAV]["total"] >= m[PLAIN]["total"])
    for d in ("correct", "useful"):
        check(g, "mean %s gv-grav >= gv-plain - 0.5" % d, fmt(m[GRAV][d]), ">= %s" % fmt(m[PLAIN][d] - half),
              m[GRAV][d] >= m[PLAIN][d] - half)
    return finish(g)


def gate5(D):
    g = new_gate("g5_key_points",
                 "Does Gravitas state the key's must-state points at least as often and as precisely as plain, with no more wrong?",
                 "key-point marks over main-set answers per arm, both graders: correct gv-grav >= gv-plain; "
                 "wrong gv-grav <= gv-plain; vague gv-grav <= gv-plain")
    votes, missing = main_votes(D)
    if missing:
        return finish(g, missing)
    ans = main_answers(votes)
    cnt = {a: Counter(mk for x in ans[a] for mk in x["kp"].values()) for a in (GRAV, PLAIN)}
    g["measured"] = {a: {mk: cnt[a][mk] for mk in KP_MARKS} for a in cnt}
    for a in (GRAV, PLAIN):
        g["detail"].append("%-8s %s" % (a, " ".join("%s %d" % (mk, cnt[a][mk]) for mk in KP_MARKS)))
    check(g, "correct gv-grav >= gv-plain", cnt[GRAV]["correct"], ">= %d" % cnt[PLAIN]["correct"],
          cnt[GRAV]["correct"] >= cnt[PLAIN]["correct"])
    check(g, "wrong gv-grav <= gv-plain", cnt[GRAV]["wrong"], "<= %d" % cnt[PLAIN]["wrong"],
          cnt[GRAV]["wrong"] <= cnt[PLAIN]["wrong"])
    check(g, "vague gv-grav <= gv-plain", cnt[GRAV]["vague"], "<= %d" % cnt[PLAIN]["vague"],
          cnt[GRAV]["vague"] <= cnt[PLAIN]["vague"])
    return finish(g)


def gate6(D):
    g = new_gate("g6_wrong_claims", "Does Gravitas add fewer claims that both relabellers call wrong?",
                 "main-set added-claim notes (both graders) labelled wrong by both relabellers: gv-grav < gv-plain; "
                 "every note listed once in claim-notes.json and labelled by both relabellers")
    votes, missing = main_votes(D)
    missing = list(missing or [])
    if D.notes is None:
        missing += D.notes_issues
    for w in RELABELLERS:
        L, fi = D.labels[w]
        missing += fi
    if missing:
        return finish(g, missing)
    main_pids = set(D.main_index.values())
    expected = Counter()
    for v in votes:
        for side in "AB":
            for note in v["grade"][side]["notes"]:
                expected[(v["pid"], side, v["grader"], note)] += 1
    rows = [r for r in D.notes.values() if r["pid"] in main_pids]
    actual = Counter((r["pid"], r["side"], r["grader"], r["note"]) for r in rows)
    if expected != actual:
        unl, ext = expected - actual, actual - expected
        missing.append("claim-notes.json does not list every main-set added_claim_errors entry exactly once "
                       "(%d entries unlisted, %d rows with no matching entry)" % (sum(unl.values()), sum(ext.values())))
    wrong = Counter()
    pairs = {GRAV: Counter(), PLAIN: Counter()}
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
        if all(x == "wrong" for x in labs):
            wrong[arm] += 1
    if missing:
        return finish(g, missing)
    unver = {a: sum(n for k, n in pairs[a].items() if k != "wrong/wrong" and "unverified" in k) for a in pairs}
    g["measured"] = {"notes": {a: sum(pairs[a].values()) for a in pairs}, "wrong_both": {a: wrong[a] for a in pairs},
                     "unverified_any_not_wrong_both": unver, "label_pairs_sonnet_opus": {a: dict(pairs[a]) for a in pairs}}
    for a in (GRAV, PLAIN):
        g["detail"].append("%-8s notes %d, wrong by both %d, unverified by at least one (reported, not counted) %d" % (
            a, sum(pairs[a].values()), wrong[a], unver[a]))
    check(g, "wrong added claims gv-grav < gv-plain", wrong[GRAV], "< %d" % wrong[PLAIN], wrong[GRAV] < wrong[PLAIN])
    return finish(g)


def gate7(D):
    g = new_gate("g7_trap_under_8", "Does Gravitas miss or mishandle the baited premise no more often than plain?",
                 "count of trap scores < 8 over main-set answers per arm (40 each): gv-grav <= gv-plain")
    votes, missing = main_votes(D)
    if missing:
        return finish(g, missing)
    ans = main_answers(votes)
    low = {a: sum(x["scores"]["trap"] < 8 for x in ans[a]) for a in ans}
    g["measured"] = {"trap_under_8": low, "answers": {a: len(ans[a]) for a in ans}}
    g["detail"].append("trap < 8: gv-grav %d of %d, gv-plain %d of %d" % (low[GRAV], len(ans[GRAV]), low[PLAIN], len(ans[PLAIN])))
    check(g, "trap<8 gv-grav <= gv-plain", low[GRAV], "<= %d" % low[PLAIN], low[GRAV] <= low[PLAIN])
    return finish(g)


def gate8(D):
    g = new_gate("g8_length", "Are Gravitas answers no longer than plain, without being gutted?",
                 "raw/*.txt finals: median chars gv-grav / median chars gv-plain within [0.70, 1.00]; "
                 "pairs (same case and round) with gv-grav/gv-plain chars < 0.6: at most 2 of 20")
    texts, missing = main_texts(D)
    if missing:
        return finish(g, missing)
    L = {k: len(t) for k, t in texts.items()}
    mg = median([L[(c, GRAV, r)] for c in D.cases for r in ROUNDS])
    mp = median([L[(c, PLAIN, r)] for c in D.cases for r in ROUNDS])
    rt = mg / mp
    pr = {(c, r): Fraction(L[(c, GRAV, r)], L[(c, PLAIN, r)]) for c in D.cases for r in ROUNDS}
    under = sorted(k for k, v in pr.items() if v < Fraction(6, 10))
    g["measured"] = {"median_chars": {GRAV: mg, PLAIN: mp}, "median_ratio": rt, "pair_ratios": pr,
                     "pairs_under_0.6": under, "pairs": len(pr)}
    g["detail"].append("median chars gv-grav %s, gv-plain %s, ratio %s" % (fmt(mg, 1), fmt(mp, 1), fmt(rt)))
    g["detail"].append("pairs under 0.6: %d of %d %s" % (len(under), len(pr), ["%s %s" % k for k in under] if under else ""))
    check(g, "median chars ratio >= 0.70", fmt(rt), ">= 0.70", rt >= Fraction(7, 10))
    check(g, "median chars ratio <= 1.00", fmt(rt), "<= 1.00", rt <= 1)
    check(g, "pairs with ratio < 0.6 at most 2", len(under), "<= 2", len(under) <= 2)
    return finish(g)


def hedge_rates(texts, cases, arm, patterns, exclude=True):
    return [Fraction(count_patterns(texts[(c, arm, r)], patterns, exclude) * 1000, len(texts[(c, arm, r)]))
            for c in cases for r in ROUNDS]


def gate9(D):
    g = new_gate("g9_hedging", "Are Gravitas answers no more hedged than plain, on the old list and the extended list (no substitution)?",
                 "hedge markers per 1000 chars, mean over the 20 finals per arm ('May' + day/year and 不可能 excluded): "
                 "round-one list gv-grav <= 1.00 x gv-plain; extended list gv-grav <= 1.10 x gv-plain")
    texts, missing = main_texts(D)
    if missing:
        return finish(g, missing)
    m = {}
    for name, pats, ex in (("round1", H_ROUND1, True), ("extended", H_EXTENDED, True), ("round1_literal_tally", H_ROUND1, False)):
        mg, mp = mean(hedge_rates(texts, D.cases, GRAV, pats, ex)), mean(hedge_rates(texts, D.cases, PLAIN, pats, ex))
        m[name] = {GRAV: mg, PLAIN: mp, "ratio": ratio(mg, mp)}
    g["measured"] = m
    for name in m:
        g["detail"].append("%-21s gv-grav %s, gv-plain %s, ratio %s%s" % (
            name, fmt(m[name][GRAV]), fmt(m[name][PLAIN]), fmt(m[name]["ratio"]),
            "  (reported only: tally.py patterns with no exclusions, comparable to round two)" if name.endswith("tally") else ""))
    check(g, "round-one list: gv-grav rate <= 1.00 x gv-plain", fmt(m["round1"]["ratio"]), "ratio <= 1.00",
          m["round1"][GRAV] <= m["round1"][PLAIN])
    check(g, "extended list: gv-grav rate <= 1.10 x gv-plain", fmt(m["extended"]["ratio"]), "ratio <= 1.10",
          m["extended"][GRAV] <= Fraction(11, 10) * m["extended"][PLAIN])
    return finish(g)


def gate10(D):
    g = new_gate("g10_fabricated_sources", "When no web page was opened, does Gravitas claim sources no more often than plain?",
                 "fabricated-source phrases counted in finals whose run opened no web page (no completed web_fetch/"
                 "web_search result in raw/*.ndjson): count gv-grav <= count gv-plain")
    texts, missing = main_texts(D)
    missing = list(missing or [])
    opened = {}
    if D.cases is not None:
        for c in D.cases:
            for r in ROUNDS:
                for a in (GRAV, PLAIN):
                    ev, err = D.events(c, a, r)
                    if err:
                        missing.append("raw/%s.%s.%s.ndjson %s" % (c, a, r, err))
                    else:
                        opened[(c, a, r)] = web_opened(ev)
    if missing:
        return finish(g, missing)
    m = {}
    for a in (GRAV, PLAIN):
        runs = [(c, r) for c in D.cases for r in ROUNDS if not opened[(c, a, r)]]
        n = sum(count_patterns(texts[(c, a, r)], FAB, exclude=False) for c, r in runs)
        chars = sum(len(texts[(c, a, r)]) for c, r in runs)
        m[a] = {"runs_without_web": len(runs), "phrases": n, "per_1000_chars": Fraction(n * 1000, chars) if chars else None}
        g["detail"].append("%-8s runs with no web page %d of 20, phrases %d (%s per 1000 chars, reported only)" % (
            a, len(runs), n, fmt(m[a]["per_1000_chars"])))
    g["measured"] = m
    check(g, "fabricated-source phrases gv-grav <= gv-plain", m[GRAV]["phrases"], "<= %d" % m[PLAIN]["phrases"],
          m[GRAV]["phrases"] <= m[PLAIN]["phrases"])
    return finish(g)


GATES = [gate1, gate2, gate3, gate4, gate5, gate6, gate7, gate8, gate9, gate10]


# ----------------------------------------------------------------------------------------------- reported beside

def report_beside(D):
    out, lines = {}, []

    def sec(title):
        lines.append("-- " + title)

    votes, vmiss = main_votes(D, strict=False)
    sec("inputs")
    lines.append("  cases: %s" % ("%d (%d zh, %d en)" % (len(D.cases), sum(c.startswith("zh-") for c in D.cases),
                                                        sum(c.startswith("en-") for c in D.cases)) if D.cases else D.case_issue))
    lines.append("  blind-map pairs by set: %s" % dict(Counter(e["set"] for e in D.entries.values())))
    for k, v in D.map_issues.items():
        if v:
            lines.append("  blind-map issues (%s): %s" % (k, summarize(v, 4)))
    ok = {g: sum(1 for (gg, _), (gr, err) in D.grades.items() if gg == g and not err) for g in GRADERS}
    lines.append("  valid grade files: %s of %d pairs each; stray grade files (pid not in map): %d" % (ok, len(D.entries), len(D.stray_grades)))
    out["inputs"] = {"cases": D.cases, "case_issue": D.case_issue, "map_issues": D.map_issues, "valid_grades": ok,
                     "stray_grades": D.stray_grades, "keypoint_issues": D.kp_issues}

    # sign tests
    sec("sign tests, main set, two-sided exact binomial on non-tie outcomes (gv-grav vs gv-plain)")
    st = {}
    w, l, t = wl(votes)
    st["vote"] = {"grav": w, "plain": l, "tie": t, "p": sign_test(w, l)}
    byp = defaultdict(list)
    for v in votes:
        byp[v["pid"]].append(1 if v["win"] == GRAV else -1 if v["win"] == PLAIN else 0)
    pv = [sum(x) for x in byp.values() if len(x) == len(GRADERS)]
    st["pair"] = {"grav": sum(x > 0 for x in pv), "plain": sum(x < 0 for x in pv), "tie": sum(x == 0 for x in pv),
                  "p": sign_test(sum(x > 0 for x in pv), sum(x < 0 for x in pv))}
    byc = defaultdict(list)
    for v in votes:
        byc[v["case"]].append(1 if v["win"] == GRAV else -1 if v["win"] == PLAIN else 0)
    cv = [sum(x) for x in byc.values() if len(x) == len(GRADERS) * len(ROUNDS)]
    st["prompt"] = {"grav": sum(x > 0 for x in cv), "plain": sum(x < 0 for x in cv), "tie": sum(x == 0 for x in cv),
                    "p": sign_test(sum(x > 0 for x in cv), sum(x < 0 for x in cv))}
    for k in ("vote", "pair", "prompt"):
        s = st[k]
        lines.append("  %-6s gv-grav %d, gv-plain %d, tie %d -> p = %s" % (k, s["grav"], s["plain"], s["tie"], fmt_p(s["p"])))
    lines.append("  (pair = sign of the two graders' votes summed; prompt = sign of the 4 votes summed; complete units only)")
    if vmiss:
        lines.append("  incomplete: %s" % summarize(vmiss, 3))
    out["sign_tests"] = st

    # kappa
    sec("Cohen's kappa between opus and sonnet on winner")
    kp = {}
    pairs_main = []
    for pid, _ in byp.items():
        vv = {v["grader"]: v["win"] for v in votes if v["pid"] == pid}
        if len(vv) == 2:
            pairs_main.append((vv["opus"], vv["sonnet"]))
    kp["main"] = {"n": len(pairs_main), "kappa": cohen_kappa(pairs_main, (GRAV, PLAIN, "tie"))}
    pairs_all = []
    for pid in D.entries:
        a, b = D.grades.get(("opus", pid), (None, 1)), D.grades.get(("sonnet", pid), (None, 1))
        if not a[1] and not b[1]:
            pairs_all.append((a[0]["winner"], b[0]["winner"]))
    kp["all_sets"] = {"n": len(pairs_all), "kappa": cohen_kappa(pairs_all, ("A", "B", "tie"))}
    for k, v in kp.items():
        lines.append("  %-8s n=%d kappa %s" % (k, v["n"], fmt(v["kappa"]) if v["kappa"] is not None else
                                                "n/a (no pairs)" if not v["n"] else "n/a (undefined: chance agreement is 1)"))
    out["kappa"] = kp

    # language split
    sec("Chinese and English separately (main set)")
    texts = {}
    if D.cases:
        for c in D.cases:
            for r in ROUNDS:
                for a in (GRAV, PLAIN):
                    t_, err = D.text(c, a, r)
                    if not err:
                        texts[(c, a, r)] = t_
    lang = {}
    for lg in ("zh", "en"):
        vs = [v for v in votes if v["case"].startswith(lg + "-")]
        w, l, t = wl(vs)
        ans = main_answers(vs)
        cs = [c for c in (D.cases or []) if c.startswith(lg + "-")]
        d = {"votes": len(vs), "grav": w, "plain": l, "tie": t, "net": w - l, "p": sign_test(w, l),
             "mean_total": {a: mean([sum(x["scores"].values()) for x in ans[a]]) for a in ans}}
        full = all((c, a, r) in texts for c in cs for a in (GRAV, PLAIN) for r in ROUNDS) and cs
        if full:
            for a in (GRAV, PLAIN):
                d.setdefault("median_chars", {})[a] = median([len(texts[(c, a, r)]) for c in cs for r in ROUNDS])
                d.setdefault("hedge_round1", {})[a] = mean(hedge_rates(texts, cs, a, H_ROUND1))
                d.setdefault("hedge_extended", {})[a] = mean(hedge_rates(texts, cs, a, H_EXTENDED))
        lang[lg] = d
        lines.append("  %s: votes %d, gv-grav %d, gv-plain %d, tie %d, net %+d, p = %s; mean total gv-grav %s, gv-plain %s" % (
            lg, d["votes"], w, l, t, w - l, fmt_p(d["p"]), fmt(d["mean_total"][GRAV], 2), fmt(d["mean_total"][PLAIN], 2)))
        if full:
            lines.append("      median chars gv-grav %s / gv-plain %s (ratio %s); hedges round-one %s / %s; extended %s / %s" % (
                fmt(d["median_chars"][GRAV], 1), fmt(d["median_chars"][PLAIN], 1),
                fmt(ratio(d["median_chars"][GRAV], d["median_chars"][PLAIN])),
                fmt(d["hedge_round1"][GRAV]), fmt(d["hedge_round1"][PLAIN]),
                fmt(d["hedge_extended"][GRAV]), fmt(d["hedge_extended"][PLAIN])))
    out["language"] = lang

    # votes by longer answer
    sec("main-set votes split by which answer is longer (raw final chars)")
    lon = {"grav_longer": Counter(), "plain_longer": Counter(), "equal": Counter()}
    to_longer = to_shorter = 0
    for v in votes:
        kg, kpl = (v["case"], GRAV, v["round"]), (v["case"], PLAIN, v["round"])
        if kg not in texts or kpl not in texts:
            continue
        lg_, lp_ = len(texts[kg]), len(texts[kpl])
        cat = "grav_longer" if lg_ > lp_ else "plain_longer" if lp_ > lg_ else "equal"
        lon[cat][v["win"]] += 1
        if cat != "equal" and v["win"] != "tie":
            longer = GRAV if cat == "grav_longer" else PLAIN
            to_longer += v["win"] == longer
            to_shorter += v["win"] != longer
    for cat, c in lon.items():
        lines.append("  %-12s votes gv-grav %d, gv-plain %d, tie %d" % (cat, c[GRAV], c[PLAIN], c["tie"]))
    lines.append("  non-tie votes to the longer answer %d, to the shorter %d (p = %s)" % (to_longer, to_shorter, fmt_p(sign_test(to_longer, to_shorter))))
    out["by_length"] = {k: dict(v) for k, v in lon.items()}
    out["by_length"].update({"to_longer": to_longer, "to_shorter": to_shorter, "p": sign_test(to_longer, to_shorter)})

    # other pair sets
    sec("other pair sets (reported only)")
    other = {}
    for s in AA_SETS:
        vs, m = aa_votes(D, s, strict=False)
        r1, r2 = sum(v["win"] == "r1" for v in vs), sum(v["win"] == "r2" for v in vs)
        other[s] = {"votes": len(vs), "r1": r1, "r2": r2, "tie": len(vs) - r1 - r2, "net": r1 - r2}
        lines.append("  %-8s votes %d: r1 side %d, r2 side %d, tie %d, net %+d" % (s, len(vs), r1, r2, len(vs) - r1 - r2, r1 - r2))
    for s in ("attr", "draft"):
        a, b = PAIR_SETS[s]
        cnt = Counter()
        for pid in sorted(p for ps in D.set_index[s].values() for p in ps):
            e = D.entries[pid]
            for gname in GRADERS:
                gr, err = D.grades.get((gname, pid), (None, "missing"))
                cnt["missing" if err else ("tie" if gr["winner"] == "tie" else e[gr["winner"]])] += 1
        npairs = sum(len(ps) for ps in D.set_index[s].values())
        other[s] = dict(cnt, pairs=npairs)
        lines.append("  %-8s pairs %d: %s %d, %s %d, tie %d, missing/malformed grades %d" % (
            s, npairs, a, cnt[a], b, cnt[b], cnt["tie"], cnt["missing"]))
    out["other_sets"] = other

    # A/B balance
    bal = None
    if D.cases and len(D.main_index) == len(D.cases) * len(ROUNDS):
        grav_a = sum(D.entries[p]["A"] == GRAV for p in D.main_index.values())
        unbalanced = [c for c in D.cases if D.entries[D.main_index[(c, "r1")]]["A"] == D.entries[D.main_index[(c, "r2")]]["A"]]
        bal = {"grav_is_A": grav_a, "pairs": len(D.main_index), "cases_not_alternating": unbalanced}
        lines.append("  main A/B balance: gv-grav is A in %d of %d pairs; cases where it is A in both or neither round: %s" % (
            grav_a, len(D.main_index), unbalanced or "none"))
    out["ab_balance"] = bal

    # check telemetry
    out["telemetry"], tl = telemetry(D, texts)
    sec("check telemetry (raw/*.claims.jsonl, raw/*.ndjson)")
    lines += tl
    return out, lines


def telemetry(D, texts):
    lines = []
    if not D.cases:
        return {"status": "n/a", "reason": D.case_issue}, ["  n/a: " + str(D.case_issue)]
    validity, runs = [], {}
    for c in D.cases:
        for r in ROUNDS:
            recs, err = parse_jsonl(D.p("raw", "%s.%s.%s.claims.jsonl" % (c, GRAV, r)))
            if err:
                validity.append("%s %s gv-grav: claims log %s" % (c, r, err))
                continue
            drafts = [x for x in recs if x.get("phase") == "draft"]
            revs = [x for x in recs if x.get("phase") == "revision"]
            steered = [x for x in drafts if x.get("steered") is True]
            if not drafts:
                validity.append("%s %s: no draft record" % (c, r))
            if len(steered) > 1 or len(revs) > 1:
                validity.append("%s %s: more than one steer (%d steered drafts, %d revisions)" % (c, r, len(steered), len(revs)))
            if steered and not revs:
                validity.append("%s %s: steered but no revision record" % (c, r))
            if revs and not steered:
                validity.append("%s %s: revision record without a steer" % (c, r))
            runs[(c, r)] = {"drafts": drafts, "revs": revs, "steered": bool(steered)}
    for arm in (PLAIN, NOCHECK):
        for c in D.cases:
            for r in ROUNDS:
                if os.path.exists(D.p("raw", "%s.%s.%s.claims.jsonl" % (c, arm, r))):
                    validity.append("%s %s %s wrote a claims record (must write none)" % (c, arm, r))
    drafts = [d for v in runs.values() for d in v["drafts"]]
    fired = [d for d in drafts if d.get("steered") is True]
    listed = [len(d["flagged"]) if isinstance(d.get("flagged"), list) else 0 for d in drafts]
    revs = [x for v in runs.values() for x in v["revs"]]
    now = Counter(o.get("now") for x in revs for o in (x.get("outcome") if isinstance(x.get("outcome"), list) else [])
                  if isinstance(o, dict))
    rev_flagged = [len(x["flagged"]) if isinstance(x.get("flagged"), list) else 0 for x in revs]
    fire_rate = Fraction(len(fired), len(drafts)) if drafts else None
    # finals against the logged texts, and steered-run anomalies
    final_vs_log, anomalies = Counter(), []
    for (c, r), v in runs.items():
        fin = texts.get((c, GRAV, r))
        if fin is None:
            continue
        if v["steered"] and v["revs"]:
            final_vs_log["equals revision text" if fin.strip() == str(v["revs"][-1].get("text", "")).strip() else "differs from revision text"] += 1
            dt, derr = D.text(c, DRAFT, r)
            draft = dt if not derr else str(v["drafts"][0].get("text", "")) if v["drafts"] else ""
            if draft and len(fin) * 2 < len(draft):
                anomalies.append("%s %s: final under half the draft (%d vs %d chars)" % (c, r, len(fin), len(draft)))
            if draft and fin.strip() == draft.strip():
                anomalies.append("%s %s: final equals the draft" % (c, r))
            hits = [p for p in META if re.search(p, fin, flags=re.I)]
            if hits:
                anomalies.append("%s %s: meta wording %s" % (c, r, hits))
        elif v["drafts"]:
            final_vs_log["unsteered, equals draft text" if fin.strip() == str(v["drafts"][-1].get("text", "")).strip() else "unsteered, differs from draft text"] += 1
    # listed-labels: cut rate of wrong vs right items
    cut = None
    ll, lerr = rd_json(D.p("listed-labels.json"))
    if lerr == "missing":
        cut = {"status": "not provided"}
    elif lerr or not isinstance(ll, list):
        cut = {"status": "malformed", "reason": lerr or "not a list"}
    else:
        tallies = {lab: Counter() for lab in ("right", "wrong", "unverified")}
        bad = 0
        for e in ll:
            if not isinstance(e, dict) or e.get("label") not in tallies:
                bad += 1
                continue
            run = runs.get((e.get("case"), e.get("round")))
            outs = [o for x in (run["revs"] if run else []) for o in (x.get("outcome") or []) if isinstance(o, dict) and o.get("raw") == e.get("raw")]
            if not outs:
                tallies[e["label"]]["unmatched"] += 1
            else:
                tallies[e["label"]]["cut" if all(o.get("now") == "absent" for o in outs) else "kept"] += 1
        rates = {lab: (Fraction(t["cut"], t["cut"] + t["kept"]) if t["cut"] + t["kept"] else None) for lab, t in tallies.items()}
        cut = {"status": "ok", "counts": {k: dict(v) for k, v in tallies.items()}, "cut_rate": rates, "malformed_rows": bad,
               "wrong_cut_more_than_right": (rates["wrong"] > rates["right"]) if None not in (rates["wrong"], rates["right"]) else None}
    if fire_rate is None:
        cls = "n/a (no draft records)"
    elif fire_rate >= Fraction(9, 10):
        wm = cut.get("wrong_cut_more_than_right") if cut.get("status") == "ok" else None
        cls = ("undetermined: the check fired in >= 90% of turns and the wrong-vs-right cut rates are unavailable" if wm is None else
               "generic revision pass, not detection (fired in >= 90% of turns and wrong items were not cut more often than right ones)"
               if not wm else "fired in >= 90% of turns; wrong items were cut more often than right ones")
    else:
        cls = "fired in under 90% of turns; criteria's generic-revision rule does not apply"
    # steps, tool calls, seconds
    steps = {}
    for arm in (PLAIN, GRAV, NOCHECK):
        st_, tc = [], []
        for c in D.cases:
            for r in ROUNDS:
                ev, err = D.events(c, arm, r)
                if err:
                    continue
                st_.append(sum(1 for e in ev if e.get("type") == "status" and e.get("phase") == "step_start"))
                tc.append(sum(1 for e in ev if e.get("type") == "tool_call"))
        if st_:
            steps[arm] = {"runs": len(st_), "steps_mean": mean(st_), "tool_calls_mean": mean(tc)}
    secs = defaultdict(list)
    rl, rerr = rd_text(D.p("run.log"))
    if not rerr:
        for line in rl.splitlines():
            mm = re.match(r"(\S+) (\S+) (r\d) exit=(\d+) secs=(\d+)", line)
            if mm:
                secs[mm.group(2)].append(int(mm.group(5)))
    for arm in steps:
        if secs.get(arm):
            steps[arm]["seconds_median"] = median(secs[arm])
    data = {"runs_with_log": len(runs), "validity_issues": validity, "turns": len(drafts), "fired": len(fired),
            "fire_rate": fire_rate, "items_listed_per_draft_mean": mean(listed), "revision_outcomes": dict(now),
            "items_flagged_in_revision_mean": mean(rev_flagged), "final_vs_log": dict(final_vs_log),
            "steered_anomalies": anomalies, "listed_item_cut": cut, "classification": cls, "steps": steps}
    ndraft = sum(len(ps) for ps in D.set_index["draft"].values())
    data["draft_set_pairs"] = ndraft
    lines.append("  gv-grav runs with a claims log %d of %d; turns checked %d, steered %d (fire rate %s); draft-vs-final pairs in blind-map %d" % (
        len(runs), len(D.cases) * len(ROUNDS), len(drafts), len(fired), fmt(fire_rate), ndraft))
    lines.append("  items listed per draft: mean %s; items still flagged when the check is replayed on the revision: mean %s (n=%d)" % (
        fmt(mean(listed), 2), fmt(mean(rev_flagged), 2), len(rev_flagged)))
    lines.append("  what the revisions did with listed items: %s" % (", ".join("%s %d" % (k, now[k]) for k in OUTCOMES if now[k]) or "none"))
    lines.append("  finals vs logged texts: %s" % (dict(final_vs_log) or "n/a"))
    lines.append("  run validity issues (harness): %s" % (summarize(validity, 5) if validity else "none"))
    lines.append("  steered-run anomalies (graded as they are): %s" % (summarize(anomalies, 5) if anomalies else "none"))
    if cut.get("status") == "ok":
        lines.append("  listed items cut (revision outcome 'absent'): wrong %s, right %s, unverified %s; counts %s" % (
            fmt(cut["cut_rate"]["wrong"]), fmt(cut["cut_rate"]["right"]), fmt(cut["cut_rate"]["unverified"]), cut["counts"]))
    else:
        lines.append("  listed-labels.json: %s" % cut.get("status") + (" (%s)" % cut["reason"] if cut.get("reason") else ""))
    lines.append("  reading of the check: %s" % cls)
    for arm, s in steps.items():
        lines.append("  %-16s runs %d, steps mean %s, tool calls mean %s%s" % (
            arm, s["runs"], fmt(s["steps_mean"], 1), fmt(s["tool_calls_mean"], 1),
            ", seconds median %s" % fmt(s["seconds_median"], 1) if "seconds_median" in s else ""))
    return data, lines


# ----------------------------------------------------------------------------------------------- evaluate

def evaluate(base):
    D = Data(base)
    gates = [f(D) for f in GATES]
    reported, rlines = report_beside(D)
    failing = [g["name"] for g in gates if g["status"] != "PASS"]
    verdict = "beats plain" if not failing else "not shown"
    line = "VERDICT: beats plain" if not failing else "VERDICT: not shown (failing: %s)" % ", ".join(failing)
    return {"base": base, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "gates": gates, "reported": reported, "report_lines": rlines,
            "verdict": verdict, "failing": failing, "verdict_line": line}


def render(res):
    out = ["== round-three verdict (criteria.md amended rule, items 1-10) on %s" % res["base"], "== gates"]
    for g in res["gates"]:
        out.append("[%s] %s: %s" % (g["status"], g["name"], g["question"]))
        out.append("       bounds: %s" % g["bounds"])
        for d in g["detail"]:
            out.append("       " + d)
        for c in g["checks"]:
            out.append("       %-52s = %-10s need %-12s %s" % (c["desc"], c["value"], c["bound"], "ok" if c["ok"] else "NOT MET"))
        if g["status"] != "PASS":
            out.append("       -> FAIL: " + g["reason"])
    out.append("== reported beside the verdict (not gates)")
    out += res["report_lines"]
    out.append(res["verdict_line"])
    return out


# ----------------------------------------------------------------------------------------------- self-test

ZH_FILL = "这是一段用于自测的合成文字，没有实际含义。"
EN_FILL = "This is synthetic self-test text with no real meaning. "


def synth_text(case, arm, rnd, gut=False, hedge_swap=False):
    ci, ri, zh = EXPECTED_CASES.index(case), ROUNDS.index(rnd), case.startswith("zh-")
    n = 40 + ci % 3 + 2 * ri
    if arm == PLAIN:
        k = n
        extra = (["这可能需要时间。"] * 3 + ["通常需要十天。"] * 2 + ["据人社部官网公告，", "经查询，"]) if zh else \
                (["This may take time. "] * 3 + ["It usually takes ten days. "] * 2 + ["According to the official site, ", "I checked the page. "])
    else:
        k = n // 2 if gut else n * 85 // 100
        if hedge_swap:
            extra = (["这不可能。"] + ["通常如此。", "一般如此。"] * 6) if zh else \
                    (["It opened on May 5, 2026. "] + ["It usually works. ", "It generally works. "] * 6)
        else:
            extra = ["这不可能。", "这可能需要时间。", "通常需要十天。"] if zh else \
                    ["It opened on May 5, 2026. ", "This may take time. ", "It usually takes ten days. "]
    body = (ZH_FILL if zh else EN_FILL) * k + "".join(extra)
    return body + ("额外的草稿句子。" * 3 if zh else "An extra draft sentence. " * 3) if arm == DRAFT else body


def make_synthetic(base, gut=False, hedge_swap=False, plain_wins=False, noise=False):
    """A dataset in which Gravitas clearly wins everything (unless a knob says otherwise). Returns ids for tests."""
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
    bmap, grades, n = {}, {}, [0]

    def pid():
        n[0] += 1
        return "p%03d" % n[0]

    def side(sc, kp, notes):
        d = dict(zip(DIMS, sc))
        d.update({"added_claim_errors": notes, "key_points": dict(zip(kp_ids, kp))})
        return d

    good = ((8, 9, 9, 8, 8), ("correct", "correct", "correct", "correct", "vague"))
    weak = ((6, 6, 7, 6, 7), ("correct", "correct", "vague", "vague", "wrong"))
    even = ((7, 8, 7, 7, 7), ("correct",) * 5)
    info = {"main": [], "aa": []}
    aa_out = {"aa-plain": ["r1"] * 7 + ["r2"] * 5 + ["tie"] * 8, "aa-grav": ["r1"] * 4 + ["r2"] * 7 + ["tie"] * 9}
    if noise:
        aa_out["aa-plain"] = ["r1"] * 20
    for ci, c in enumerate(EXPECTED_CASES):
        wt("prompts/%s.txt" % c, "synthetic request\n")
        wj("keypoints/%s.json" % c, [{"id": k, "point": "synthetic point %s" % k} for k in kp_ids])
        for ri, r in enumerate(ROUNDS):
            grav_a = ri == ci % 2
            for s, other in (("main", PLAIN), ("attr", NOCHECK), ("draft", DRAFT)):
                p = pid()
                A, B = (GRAV, other) if grav_a else (other, GRAV)
                bmap[p] = {"set": s, "case": c, "round": r, "A": A, "B": B}
                gs = "A" if grav_a else "B"
                os_ = "B" if grav_a else "A"
                for g in GRADERS:
                    notes_g = ["synthetic gv-grav claim %s %s: date not in the key" % (p, g)] if s == "main" else []
                    notes_o = ["synthetic plain claim %s %s %d: fee not in the key" % (p, g, k) for k in (1, 2)] if s == "main" else []
                    win = gs
                    if s == "main" and plain_wins:
                        win = os_
                    if s == "main" and noise and g == "opus":
                        win = "tie"
                    grades[(g, p)] = {"pair": p, "winner": win, "margin": "clear",
                                      gs: side(good[0], good[1], notes_g), os_: side(weak[0], weak[1], notes_o),
                                      "reasons": "synthetic"}
                if s == "main":
                    info["main"].append(p)
        for s, arm in AA_SETS.items():
            p = pid()
            a_r1 = ci % 2 == 0
            bmap[p] = {"set": s, "case": c, "round": "r1", "A": arm, "B": arm,
                       "A_round": "r1" if a_r1 else "r2", "B_round": "r2" if a_r1 else "r1"}
            info["aa"].append(p)
            for gi, g in enumerate(GRADERS):
                o = aa_out[s][ci * 2 + gi]
                win = "tie" if o == "tie" else ("A" if (o == "r1") == a_r1 else "B")
                grades[(g, p)] = {"pair": p, "winner": win, "margin": "slight",
                                  "A": side(even[0], even[1], []), "B": side(even[0], even[1], []), "reasons": "synthetic"}
        for r in ROUNDS:
            for arm in (PLAIN, GRAV, NOCHECK, DRAFT):
                wt("raw/%s.%s.%s.txt" % (c, arm, r), synth_text(c, arm, r, gut, hedge_swap))
            for arm in (PLAIN, GRAV, NOCHECK):
                ev = [{"type": "status", "phase": "step_start"}, {"type": "tool_call", "callId": "c1", "tool": "pwsh"},
                      {"type": "tool_result", "callId": "c1", "status": "completed"}]
                if ci == 0 and r == "r1":
                    ev += [{"type": "tool_call", "callId": "c2", "tool": "web_fetch"},
                           {"type": "tool_result", "callId": "c2", "status": "completed"}]
                if ci == 1 and r == "r2" and arm == GRAV:
                    ev += [{"type": "tool_call", "callId": "c3", "tool": "web_search"},
                           {"type": "tool_result", "callId": "c3", "status": "error"}]
                wt("raw/%s.%s.%s.ndjson" % (c, arm, r), "".join(json.dumps(e) + "\n" for e in ev))
            flagged = [{"cls": "amount", "raw": "300元", "key": "300元"}, {"cls": "date", "raw": "5月5日", "key": "05-05"},
                       {"cls": "percent", "raw": "20%", "key": "20%"}]
            outcome = [dict(flagged[0], now="absent", source=None), dict(flagged[1], now="supported", source="web_fetch"),
                       dict(flagged[2], now="absent", source=None)]
            recs = [{"phase": "draft", "steered": True, "counts": {"amount": 1, "date": 1, "percent": 1}, "flagged": flagged,
                     "text": synth_text(c, DRAFT, r, gut, hedge_swap)},
                    {"phase": "revision", "counts": {}, "flagged": [], "outcome": outcome, "text": synth_text(c, GRAV, r, gut, hedge_swap)}]
            wt("raw/%s.%s.%s.claims.jsonl" % (c, GRAV, r), "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in recs))
    wj("blind-map.json", bmap)
    for (g, p), obj in grades.items():
        wj("blind/grades/%s/%s.json" % (g, p), obj)
    notes, nid = [], 0
    for (g, p), obj in sorted(grades.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        for sd in "AB":
            for note in obj[sd]["added_claim_errors"]:
                nid += 1
                notes.append({"id": nid, "pid": p, "side": sd, "grader": g, "note": note})
    wj("claim-notes.json", notes)
    for who in RELABELLERS:
        wj("labels-%s.json" % who, [{"id": x["id"], "label": "unverified" if "gv-grav claim" in x["note"] else "wrong",
                                     "cite": "" if "gv-grav claim" in x["note"] else "key line 3"} for x in notes])
    wj("listed-labels.json", [{"case": c, "round": r, "raw": raw, "label": lab} for c in EXPECTED_CASES for r in ROUNDS
                              for raw, lab in (("300元", "wrong"), ("5月5日", "right"), ("20%", "wrong"))])
    info["notes"] = notes
    return info


def selftest():
    results = []

    def expect(label, cond, info=""):
        print(("[ok]  " if cond else "[BAD] ") + label + (("  -- " + info) if info else ""))
        results.append(bool(cond))

    def gmap(res):
        return {g["name"]: g for g in res["gates"]}

    def show(g):
        return "%s %s" % (g["status"], g["reason"][:110])

    def jload(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)

    def jdump(p, obj):
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)

    root = tempfile.mkdtemp(prefix="verdict-ab3-selftest-")
    if os.path.normcase(os.path.abspath(root)).startswith(os.path.normcase(HERE)):
        print("temporary folder lies inside the real folder; refusing")
        return 1
    def serialises(res):
        try:
            json.dumps(jsonable(res), ensure_ascii=False)
            return True
        except (TypeError, ValueError):
            return False

    try:
        # pattern units
        for text, pats, want, label in (
                ("这不可能。", H_ROUND1, 0, "不可能 is not a hedge"), ("这可能需要时间。", H_ROUND1, 1, "可能 is a hedge"),
                ("It opened on May 5, 2026.", H_ROUND1, 0, "'May 5' is a date, not a hedge"),
                ("Due in May 2026.", H_ROUND1, 0, "'May 2026' is a date, not a hedge"),
                ("You may need it.", H_ROUND1, 1, "'may' is a hedge"),
                ("请拨打12333问一下", H_EXTENDED, 1, "打 + five-digit number + 问 is an extended hedge"),
                ("打123456问", H_EXTENDED, 0, "a six-digit number is not the five-digit hotline pattern"),
                ("具体以当地规定为准", H_EXTENDED, 2, "具体…为准 and 以…为准 both count"),
                ("据人社部官网", FAB, 1, "据…官网 is a fabricated-source phrase"),
                ("I checked the page.", FAB, 1, "'I checked' is a fabricated-source phrase")):
            got = count_patterns(text, pats, exclude=pats is not FAB)
            expect("pattern: %s (%r -> %d)" % (label, text, got), got == want, "" if got == want else "want %d" % want)

        # (a) empty input
        b = os.path.join(root, "a-empty")
        os.makedirs(b)
        res = evaluate(b)
        expect("(a) empty input: all 10 gates evaluated", [g["name"] for g in res["gates"]] == GATE_NAMES)
        for g in res["gates"]:
            expect("(a) empty input: %s FAILS as metric missing" % g["name"],
                   g["status"] == "FAIL" and g["reason"].startswith("metric missing"), show(g))
        expect("(a) empty input: verdict line is 'not shown' naming all 10 gates",
               res["verdict_line"].startswith("VERDICT: not shown") and res["failing"] == GATE_NAMES, res["verdict_line"][:80])
        expect("(a) empty input: results serialise to JSON", serialises(res))

        # (a2) case list only
        b = os.path.join(root, "a2-prompts-only")
        os.makedirs(os.path.join(b, "prompts"))
        for c in EXPECTED_CASES:
            open(os.path.join(b, "prompts", c + ".txt"), "w").close()
        res = evaluate(b)
        for g in res["gates"]:
            expect("(a2) case list only: %s FAILS as metric missing" % g["name"],
                   g["status"] == "FAIL" and g["reason"].startswith("metric missing"), show(g))

        # (b) synthetic clear win
        b = os.path.join(root, "b-win")
        os.makedirs(b)
        info = make_synthetic(b)
        res = evaluate(b)
        for g in res["gates"]:
            expect("(b) synthetic win: %s PASSES" % g["name"], g["status"] == "PASS", show(g))
        expect("(b) synthetic win: verdict line is 'VERDICT: beats plain'", res["verdict_line"] == "VERDICT: beats plain",
               res["verdict_line"][:80])
        tel = res["reported"]["telemetry"]
        expect("(b) synthetic win: telemetry reads 20 steered turns and wrong items cut more than right",
               tel["fired"] == 20 and tel["listed_item_cut"].get("wrong_cut_more_than_right") is True, str(tel["classification"]))
        expect("(b) synthetic win: results serialise to JSON", serialises(res))

        grade_gates = set(GATE_NAMES[:7])

        def variant(tag, mutate, fail_missing, fail_bound=(), **kw):
            b = os.path.join(root, tag.split(")")[0].strip("("))
            os.makedirs(b)
            inf = make_synthetic(b, **kw)
            if mutate:
                mutate(b, inf)
            r_ = evaluate(b)
            for g in r_["gates"]:
                if g["name"] in fail_missing:
                    expect("%s: %s FAILS as metric missing" % (tag, g["name"]),
                           g["status"] == "FAIL" and g["reason"].startswith("metric missing"), show(g))
                elif g["name"] in fail_bound:
                    expect("%s: %s FAILS on its bound" % (tag, g["name"]),
                           g["status"] == "FAIL" and g["reason"].startswith("bound not met"), show(g))
                else:
                    expect("%s: %s still PASSES" % (tag, g["name"]), g["status"] == "PASS", show(g))
            return r_

        def drop_main_grade(b, inf):
            os.remove(os.path.join(b, "blind", "grades", "opus", inf["main"][0] + ".json"))

        def drop_label(b, inf):
            p = os.path.join(b, "labels-opus.json")
            labs = jload(p)
            target = next(x["id"] for x in inf["notes"] if x["pid"] in inf["main"])
            jdump(p, [x for x in labs if x["id"] != target])

        def drop_aa_grade(b, inf):
            os.remove(os.path.join(b, "blind", "grades", "sonnet", inf["aa"][0] + ".json"))

        def drop_raw(b, inf):
            os.remove(os.path.join(b, "raw", "%s.%s.r2.txt" % (EXPECTED_CASES[3], GRAV)))

        def drop_ndjson(b, inf):
            os.remove(os.path.join(b, "raw", "%s.%s.r1.ndjson" % (EXPECTED_CASES[5], PLAIN)))

        def bad_keypoints(b, inf):
            p = os.path.join(b, "blind", "grades", "sonnet", inf["main"][4] + ".json")
            obj = jload(p)
            obj["A"]["key_points"].pop("5")
            obj["A"]["key_points"]["6"] = "correct"
            jdump(p, obj)

        def wrong_without_cite(b, inf):
            p = os.path.join(b, "labels-sonnet.json")
            labs = jload(p)
            next(x for x in labs if x["label"] == "wrong")["cite"] = ""
            jdump(p, labs)

        variant("(c1) one main-set grade file removed", drop_main_grade, grade_gates)
        variant("(c2) one relabel entry missing", drop_label, {"g6_wrong_claims"})
        variant("(c3) one A/A grade file removed", drop_aa_grade, {"g1_net_votes"})
        variant("(c4) one gv-grav final text removed", drop_raw, {"g8_length", "g9_hedging", "g10_fabricated_sources"})
        variant("(c5) one event stream removed", drop_ndjson, {"g10_fabricated_sources"})
        variant("(c6) one grade's key_points ids differ from the case's", bad_keypoints, grade_gates)
        variant("(c7) one 'wrong' relabel without a cite", wrong_without_cite, {"g6_wrong_claims"})
        def top_level_keypoints(b, inf):
            p = os.path.join(b, "blind", "grades", "opus", inf["main"][6] + ".json")
            obj = jload(p)
            obj["key_points"] = {sd: obj[sd].pop("key_points") for sd in "AB"}
            jdump(p, obj)

        variant("(c8) one grade with key_points at top level ({A:..., B:...})", top_level_keypoints, set())
        variant("(d1) gutted gv-grav answers (half length)", None, set(), {"g8_length"}, gut=True)
        variant("(d2) hedge substitution (extended-list hedges only)", None, set(), {"g9_hedging"}, hedge_swap=True)
        variant("(d3) plain wins every main vote", None, set(), {"g1_net_votes", "g2_each_grader", "g3_prompts"}, plain_wins=True)
        r_ = variant("(d4) net equals the A/A noise floor (opus all ties; aa-plain net 20)", None, set(),
                     {"g1_net_votes", "g2_each_grader"}, noise=True)
        m1 = gmap(r_)["g1_net_votes"]["measured"]
        expect("(d4) net 20 and noise floor 20 measured", m1.get("net") == 20 and m1.get("noise_floor") == 20, str(m1)[:100])
    finally:
        shutil.rmtree(root, ignore_errors=True)
    bad = results.count(False)
    print("selftest: %d assertions, %d failed" % (len(results), bad))
    return 0 if bad == 0 else 1


# ----------------------------------------------------------------------------------------------- main

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="run the self-test in a temporary folder and exit")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    res = evaluate(HERE)
    print("\n".join(render(res)))
    with open(os.path.join(HERE, "verdict.json"), "w", encoding="utf-8") as f:
        json.dump(jsonable(res), f, ensure_ascii=False, indent=1)
    sys.exit(0)


if __name__ == "__main__":
    main()
