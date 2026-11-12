#!/usr/bin/env python3
"""Round-five tuning check: computes every metric of design/tuning-decision-rule.md and applies its pass-1 outcomes
1-6 and its pass-2 gates G1-G9 exactly, printing every number, every bound and the outcome.

    python tuning_check5.py --calibration [BATCH]   the rule's calibration conditions on the 48 baselines
                                                    (BATCH defaults to the newest calibration grades file)
    python tuning_check5.py --pass 1                pass-1 outcome (1-6)      -> decision-pass1.json
    python tuning_check5.py --pass 2                pass-2 GO or ABANDON      -> decision-pass2.json
    python tuning_check5.py --baseline-text         text metrics of the 48 baselines and the RD regex scan of every
                                                    round-four run (needs no grades; a check of the instrument)
    python tuning_check5.py --selftest              synthetic checks of every outcome and gate (temporary folders;
                                                    reads round four's files only to import its scripts and, in one
                                                    dry build, its answers; writes nothing in either round folder)
    options: --validity PATH (default ..\\validity-tuning-<pass>.json, written by validity5.py --tuning N in
             validity4.py's format), --validity1 PATH (pass 1's report when checking pass 2; default
             ..\\validity-tuning-1.json), --no-write, --base4/--base5/--inst DIR

Inputs: grades-<batch>.json (save_tuning_grades5.py), the answers and NDJSON streams (round four's raw\\ for the
baselines, ..\\tuning\\<case>.gv-grav-c5.r<pass>.* for c5), the run validity report, and rd-hand-pass<N>.json (the
hand reading of the RD regex hits; a template is written beside it). A missing or malformed metric fails its gate
("MISSING"): an ABANDON condition or an overshoot trigger that cannot be computed counts as holding, "moved" and every
G check that cannot be computed count as not met. Nothing missing is ever defaulted to a passing value. Comparisons are
exact (fractions). Standard library only. See README.md for every reading of the rule this script had to choose.
"""
import sys

sys.dont_write_bytecode = True

import argparse
import datetime
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tuning_common5 as T  # noqa: E402

FR = Fraction
GRADE_KEYS = ("F", "K", "C", "V", "M", "W", "AW", "AU", "S", "SP", "SR", "PC")
TEXT_KEYS = ("H1", "H2", "H3", "CD", "BL", "WF", "UX")
LANG_KEYS = ("F_lang", "M_lang")
ALL_KEYS = GRADE_KEYS + TEXT_KEYS
GROUP_NAMES = ("c5", "base r1", "base r2", "plain r1", "plain r2")

# ------------------------------------------------------------------------------------------- frozen regexes
# CD: condition words, exactly the rule's list, one alternation per language so a phrase is counted once ("only if"
# is one hit, not "only if" + "if"). Counted on visible text, each answer with its own language's list. Exclusions
# (frozen with the lists; each removes a non-conditional use, which makes the c5/base ratio more sensitive):
# zh 若干 (some); ja ならない/ならず/ならび/ならでは (must, not a condition); ko 면/라면 only at the end of a word
# (하면, 이라면), not inside nouns such as 면제 or 측면에서, and not 면서 (while).
CD_RE = {
    "en": re.compile(r"\b(?:up to|at most|only if|unless|if)\b", re.I),
    "zh": re.compile(r"最多|不超过|只有[^。！？；\n]{0,30}?才|除非|如果|若(?!干)"),
    "ja": re.compile(r"最大|まで|なら(?![なずびで])|限り"),
    "ko": re.compile(r"최대|까지|(?<=[가-힣])라면(?![가-힣])|(?<=[가-힣])면(?![가-힣])"),
}
# BL: a visible line that opens with a conditional. en and zh: the line starts with a conditional word (zh also: its
# first clause ends in 的话). ja and ko, where the condition closes its clause: the line starts with もし/만약, or its
# first clause (no punctuation before it, within 40 characters) carries a conditional ending: ja なら, 場合(は), たら,
# れば, 限り; ko -면, 라면, 경우(에는).
BL_RE = {
    "en": re.compile(r"^(?:(?:even |only )?if|unless|in case|provided(?: that)?|as long as)\b", re.I),
    "zh": re.compile(r"^(?:如果|若(?!干)|倘若|假如|假设|要是|万一|除非|只有|只要|一旦)|^[^，,。：:；;！？!?]{0,40}?的话"),
    "ja": re.compile(r"^もし|^[^、，,。：:；;！？!?]{0,40}?(?:なら(?![なずびで])|場合(?:は|には|でも|(?=[、，,：:\s]|$))|"
                     r"たら(?![すい])|れば|限り)"),
    "ko": re.compile(r"^(?:만약|만일|혹시)|^[^,，.。:：;；!?！？]{0,40}?(?:(?<=[가-힣])면|라면|경우(?:에는|에|라면)?)"
                     r"(?=[\s,，.:：;；!?)]|$)"),
}
# RD: phrases that quote or apply the change-5 sentence (design/change5.md), in the four languages the rule ships in
# and the English that the runs think in. Searched in the run's thinking events only (its reasoning, not its final
# answer), case-insensitive. Every hit is printed with its context to be read by hand (rd-hand-pass<N>.json).
RD_PATTERNS = [
    r"more absolute than (?:what|it)", r"plainly never means", r"stays in the sentence that states", r"in a step too",
    r"chosen to be safe", r"beside the rule", r"the rule it is safer than", r"flat absolute",
    r"bare [\"“']?(?:may|probably)", r"adding no (?:new )?sentence", r"no sentence or branch", r"a fact of theirs",
    r"\b(?:limit|cap|maximum|condition)s? (?:must |should |has to |needs to )?stays? (?:in|with)\b",
    r"\bkeep(?:s|ing)? the (?:limit|cap|condition|maximum)s? (?:in|with)\b", r"\bmaximum as [\"“']?up to",
    r"\bsafer? (?:pick|choice)\b", r"\bas (?:a|that) (?:safe )?choice beside",
    r"比查到的更绝对", r"不等于说得比", r"留在说出它的那句话", r"写在步骤里也一样", r"为了稳妥而选", r"为稳妥而作的选择",
    r"不另加句子", r"句子或分支", r"说得过满",
    r"見つけた以上に断定", r"それを述べる文の中に残", r"手順の中でも同じ", r"念のための選択", r"念のために選んだ",
    r"実際の規則をその隣", r"文や枝分かれ", r"言い過ぎの言葉", r"言い切るとは",
    r"찾아낸 것보다 더 단정", r"말하는 문장 안에 남", r"단계 안내 안에서도", r"안전하게 하려고 고른", r"그런 선택이라고 밝히",
    r"실제 규정을 그 옆에", r"문장이나 갈래", r"얼버무리지 않고 말한다는 것",
]
RD_RE = re.compile("|".join("(?:%s)" % p for p in RD_PATTERNS), re.I)

# Calibration items of the rule (case, arm, run, key point id).
CAL_FLAT = (("en-529-roth", T.BASE, "r1", "7"), ("ja-medical-deduction", T.BASE, "r1", "7"),
            ("ko-jeonse-protection", T.BASE, "r2", "5"))
CAL_KEPT = (("en-529-roth", T.PLAIN, "r1", "7"), ("en-fsa-rollover", T.PLAIN, "r1", "3"))


# ------------------------------------------------------------------------------------------- three-valued helpers

def known(*xs):
    return all(x is not None for x in xs)


def add(*xs):
    return sum(xs, FR(0)) if known(*xs) else None


def sub(a, b):
    return a - b if known(a, b) else None


def mul(k, a):
    return FR(k) * a if known(a) else None


def mean2(a, b):
    return FR(a + b, 2) if known(a, b) else None


def min2(a, b):
    return min(a, b) if known(a, b) else None


def max2(a, b):
    return max(a, b) if known(a, b) else None


def median(xs):
    if xs is None or not xs or any(x is None for x in xs):
        return None
    s = sorted(xs)
    n = len(s)
    return FR(s[n // 2]) if n % 2 else FR(s[n // 2 - 1] + s[n // 2], 2)


OPS = {"<=": lambda a, b: a <= b, "<": lambda a, b: a < b, ">=": lambda a, b: a >= b, ">": lambda a, b: a > b,
       "==": lambda a, b: a == b}


def fmt(x):
    if x is None:
        return "MISSING"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int, Fraction)) and FR(x).denominator == 1:
        return str(int(x))
    return "%.3f" % float(x)


def chk(name, value, op, bound, bexpr=""):
    """One comparison: result True/False, or None when a side is missing."""
    res = OPS[op](value, bound) if known(value, bound) else None
    return {"name": name, "value": value, "op": op, "bound": bound, "bound_expr": bexpr, "result": res}


def and3(*rs):
    if any(r is False for r in rs):
        return False
    return None if any(r is None for r in rs) else True


def or3(*rs):
    if any(r is True for r in rs):
        return True
    return None if any(r is None for r in rs) else False


def g(rec, k):
    return (rec or {}).get(k)


# ------------------------------------------------------------------------------------------- per-answer metrics

def text_metrics(V, case, arm, run, b4, b5):
    """Metrics of one answer from its final text and NDJSON stream. Each value is None when it cannot be computed."""
    out = {k: None for k in ("vis", "H1", "H2", "H3", "CD", "BL", "WF", "UX")}
    issues = []
    if V is None:
        return out, ["round four's verdict scripts did not load"]
    V4 = V.V4
    p = T.answer_path(case, arm, run, b4, b5)
    t, err = V4.rd_text(p)
    if err or not t.strip():
        return out, ["%s %s" % (p, err or "empty")]
    lang = T.lang_of(case)
    for k, which in (("H1", "first"), ("H2", "second"), ("H3", "third")):
        out[k] = FR(V.hedge_count(t, lang, which) * 1000, len(t))
    vt = V.visible_text(t)
    out["vis"] = len(vt)
    if vt:
        out["CD"] = FR(len(CD_RE[lang].findall(vt)) * 1000, len(vt))
        out["BL"] = sum(1 for ln in vt.split("\n") if BL_RE[lang].search(ln))
    else:
        issues.append("%s has no visible text" % p)
    sp = T.stream_path(case, arm, run, b4, b5)
    ev, err = V4.parse_ndjson(sp)
    if err:
        issues.append("%s %s" % (sp, err))
    else:
        out["WF"] = sum(1 for e in ev if e.get("type") == "tool_call" and e.get("tool") == "web_fetch")
        out["UX"] = V.fab_analysis(t, V.opened_hosts(ev))["unexcused"]
    return out, issues


def group_text(V, arm, run, b4, b5):
    """Text metrics of one group of 12 answers: H1-H3 and CD are means over answers, BL, WF and UX are sums."""
    per, issues = {}, []
    for c in T.CASES:
        m, iss = text_metrics(V, c, arm, run, b4, b5)
        per[c] = m
        issues += iss
    rec = {"vis": {c: per[c]["vis"] for c in T.CASES}}
    for k in ("H1", "H2", "H3", "CD"):
        xs = [per[c][k] for c in T.CASES]
        rec[k] = FR(sum(xs), len(xs)) if known(*xs) else None
    for k in ("BL", "WF", "UX"):
        xs = [per[c][k] for c in T.CASES]
        rec[k] = sum(xs) if known(*xs) else None
    rec["per_case"] = per
    return rec, issues


def grade_group(items, info):
    """Grader metrics of one group of 12 graded answers (items: {case: grade or None})."""
    rec = {k: None for k in GRADE_KEYS}
    rec["F_lang"] = {lg: None for lg in T.LANGS}
    rec["M_lang"] = {lg: None for lg in T.LANGS}
    rec["PC_all"] = None
    rec["per_case_F"] = {c: None for c in T.CASES}
    if any(items.get(c) is None for c in T.CASES):
        return rec
    cnt = Counter()
    fl, ml = Counter(), Counter()
    pca = 0
    for c in T.CASES:
        gr = items[c]
        lk = Counter(gr["lkp"][i] for i in info[c]["lkp"])
        kp = Counter(gr["key_points"][i] for i in info[c]["kp"])
        f = lk["FLAT"] + lk["WRONG"]
        cnt["F"] += f
        cnt["K"] += lk["KEPT"]
        cnt["C"] += kp["correct"]
        cnt["V"] += kp["vague"]
        cnt["M"] += kp["missing"]
        cnt["W"] += kp["wrong"]
        for k in T.LIST_FIELDS:
            cnt[k] += len(gr[k])
        cnt["PC"] += gr["PC"] == "yes"
        # PC_all (reported, never gated): the gated point and every reported premise correction in the opening
        pca += all(gr["PC_points"].get(i) == "yes" for i in info[c]["pc_points"])
        fl[T.lang_of(c)] += f
        ml[T.lang_of(c)] += kp["missing"]
        rec["per_case_F"][c] = f
    for k in GRADE_KEYS:
        rec[k] = cnt[k]
    rec["F_lang"] = {lg: fl[lg] for lg in T.LANGS}
    rec["M_lang"] = {lg: ml[lg] for lg in T.LANGS}
    rec["PC_all"] = pca
    return rec


# ------------------------------------------------------------------------------------------- the rule's logic

def sum_recs(recs):
    """Pooling: each metric summed over the passes (None if any pass lacks it)."""
    out = {}
    for k in ALL_KEYS:
        out[k] = add(*[g(r, k) for r in recs]) if recs else None
    for k in LANG_KEYS:
        out[k] = {lg: add(*[(g(r, k) or {}).get(lg) for r in recs]) if recs else None for lg in T.LANGS}
    return out


def lv_list(c5, ref):
    """Per prompt: c5's visible length divided by the mean of the two reference runs for that prompt."""
    out = []
    for c in T.CASES:
        a = (g(c5, "vis") or {}).get(c)
        r1 = (g(ref[0], "vis") or {}).get(c) if len(ref) > 0 else None
        r2 = (g(ref[1], "vis") or {}).get(c) if len(ref) > 1 else None
        out.append(FR(2 * a, r1 + r2) if known(a, r1, r2) and r1 + r2 > 0 else None)
    return out


def scope_of(pds):
    """The numbers of one scope: one pass alone, or both passes pooled (outcome 3)."""
    pds = [pd or {} for pd in pds]
    S = {"passes": [pd.get("n") for pd in pds]}
    S["c5"] = sum_recs([pd.get("c5") for pd in pds])
    S["base"] = [sum_recs([(pd.get("base") or [None, None])[i] for pd in pds]) for i in (0, 1)]
    S["plain"] = [sum_recs([(pd.get("plain") or [None, None])[i] for pd in pds]) for i in (0, 1)]
    S["lv_by_pass"] = [lv_list(pd.get("c5"), pd.get("plain") or []) for pd in pds]
    S["lb_by_pass"] = [lv_list(pd.get("c5"), pd.get("base") or []) for pd in pds]
    S["lv"] = [x for xs in S["lv_by_pass"] for x in xs]
    S["lb"] = [x for xs in S["lb_by_pass"] for x in xs]
    S["lv_lang"] = {lg: [x for xs in S["lv_by_pass"] for c, x in zip(T.CASES, xs) if T.lang_of(c) == lg]
                    for lg in T.LANGS}
    first = pds[0] if pds else {}
    base_lv = []
    for b in (first.get("base") or []):
        base_lv.append(lv_list(b, first.get("plain") or []))
    S["base_lv_lang"] = {lg: [x for xs in base_lv for c, x in zip(T.CASES, xs) if T.lang_of(c) == lg] or [None]
                         for lg in T.LANGS}
    S["S_by_pass"] = [g(pd.get("c5"), "S") for pd in pds]
    S["SP_by_pass"] = [g(pd.get("c5"), "SP") for pd in pds]
    return S


def bx(S, k):
    """Baseline numbers of metric k in scope S: base mean, min, max; plain mean, max."""
    b1, b2 = g(S["base"][0], k), g(S["base"][1], k)
    p1, p2 = g(S["plain"][0], k), g(S["plain"][1], k)
    return {"b_mean": mean2(b1, b2), "b_min": min2(b1, b2), "b_max": max2(b1, b2),
            "p_mean": mean2(p1, p2), "p_max": max2(p1, p2)}


def blang(S, k, lg, which):
    xs = [(g(r, k) or {}).get(lg) for r in S[which]]
    return mean2(*xs) if len(xs) == 2 else None


def triggers(S):
    """O1-O6 on a one-pass scope. Each trigger fires when its condition holds or cannot be computed."""
    c = S["c5"]
    F, K, V, M = g(c, "F"), g(c, "K"), g(c, "V"), g(c, "M")
    out = {}
    mlv, mlb = median(S["lv"]), median(S["lb"])
    cks = [chk("median Lv > 1.00", mlv, ">", FR(1)), chk("median Lb > 1.05", mlb, ">", FR(105, 100))]
    out["O1"] = {"label": "length", "checks": cks, "join": "and", "result": and3(*[x["result"] for x in cks])}
    cks = [chk("S >= 3", g(c, "S"), ">=", 3)]
    out["O2"] = {"label": "spraying", "checks": cks, "join": "or", "result": or3(cks[0]["result"])}
    cd, bl = bx(S, "CD"), bx(S, "BL")
    cks = [chk("CD > 1.5 x CD-bar-b", g(c, "CD"), ">", mul(FR(3, 2), cd["b_mean"]), "1.5 x %s" % fmt(cd["b_mean"])),
           chk("BL > 1.5 x BL-bar-b", g(c, "BL"), ">", mul(FR(3, 2), bl["b_mean"]), "1.5 x %s" % fmt(bl["b_mean"]))]
    out["O3"] = {"label": "conditional density", "checks": cks, "join": "or", "result": or3(*[x["result"] for x in cks])}
    f, k, v, m = bx(S, "F"), bx(S, "K"), bx(S, "V"), bx(S, "M")
    cks = [chk("K - K-bar-b < 0.5 x (F-bar-b - F)", sub(K, k["b_mean"]), "<", mul(FR(1, 2), sub(f["b_mean"], F)),
               "0.5 x (%s - %s)" % (fmt(f["b_mean"]), fmt(F))),
           chk("V > V-bar-p + 2", V, ">", add(v["p_mean"], 2), "%s + 2" % fmt(v["p_mean"])),
           chk("M > M-bar-p", M, ">", m["p_mean"])]
    out["O4"] = {"label": "blur", "checks": cks, "join": "or", "result": or3(*[x["result"] for x in cks])}
    cks = [chk("%s > %sb_max" % (h, h), g(c, h), ">", bx(S, h)["b_max"]) for h in ("H1", "H2", "H3")]
    out["O5"] = {"label": "hedges", "checks": cks, "join": "or", "result": or3(*[x["result"] for x in cks])}
    au = bx(S, "AU")
    cks = [chk("AU > 1.10 x AUp_max", g(c, "AU"), ">", mul(FR(11, 10), au["p_max"]), "1.10 x %s" % fmt(au["p_max"])),
           chk("SP >= 2", g(c, "SP"), ">=", 2), chk("SR >= 1", g(c, "SR"), ">=", 1)]
    out["O6"] = {"label": "unverified claims and safe picks", "checks": cks, "join": "or",
                 "result": or3(*[x["result"] for x in cks])}
    for t in out.values():
        t["fires"] = t["result"] is not False
    return out


def moved_check(S, delta=1):
    f = bx(S, "F")
    return chk("F <= Fb_min - %d" % delta, g(S["c5"], "F"), "<=", sub(f["b_min"], delta), "%s - %d" % (fmt(f["b_min"]), delta))


OUTCOME_TEXT = {
    1: "ABANDON now (no pass 2)",
    3: "moved and no trigger: no revision; pass 2 reruns the same text as a replicate",
    4: "moved and a trigger: revision R-b (delete the parenthetical in all four languages); pass 2 runs R-b",
    5: "not moved, no trigger, RD <= 2 (the sentence was not read): revision R-a (move the unchanged text to the end "
       "of item 7); pass 2 runs R-a",
    6: "not moved, and a trigger or RD >= 3: ABANDON",
}


def pass1_outcome(pd):
    """The rule's pass-1 outcome. pd: {"n", "c5", "base": [r1, r2], "plain": [r1, r2], "invalid_after_rerun", "RD"}."""
    pd = pd or {}
    S = scope_of([pd])
    c = S["c5"]
    m = bx(S, "M")
    ab = [chk("PC <= 10", g(c, "PC"), "<=", 10),
          chk("runs still invalid after their rerun >= 1", pd.get("invalid_after_rerun"), ">=", 1),
          chk("median Lv < 0.70", median(S["lv"]), "<", FR(7, 10)),
          chk("M >= M-bar-b + 6", g(c, "M"), ">=", add(m["b_mean"], 6), "%s + 6" % fmt(m["b_mean"]))]
    for x in ab:
        x["holds"] = x["result"] is not False
    mv = moved_check(S)
    moved = mv["result"] is True
    trig = triggers(S)
    any_t = any(t["fires"] for t in trig.values())
    rd = chk("RD <= 2", pd.get("RD"), "<=", 2)
    rd_le2 = rd["result"] is True
    if any(x["holds"] for x in ab):
        outcome = 1
    elif moved and not any_t:
        outcome = 3
    elif moved:
        outcome = 4
    elif not any_t and rd_le2:
        outcome = 5
    else:
        outcome = 6
    return {"outcome": outcome, "text": OUTCOME_TEXT[outcome], "abandon_checks": ab, "moved": mv, "is_moved": moved,
            "triggers": trig, "any_trigger": any_t, "rd": rd, "scope": S}


def gate(name, question, checks):
    return {"gate": name, "question": question, "checks": checks, "pass": all(x["result"] is True for x in checks)}


def pass2_decision(pd1, pd2, outcome1, stop=False):
    """GO or ABANDON after pass 2. outcome1 is pass 1's outcome (3 pools both passes; 4 and 5 judge pass 2 alone)."""
    pd1, pd2 = pd1 or {}, pd2 or {}
    if outcome1 not in (3, 4, 5):
        raise ValueError("pass 2 follows only outcomes 3, 4 and 5 (pass 1 gave %r)" % outcome1)
    pooled = outcome1 == 3
    S = scope_of([pd1, pd2] if pooled else [pd2])
    S2 = scope_of([pd2])
    c = S["c5"]
    gates = []
    f = bx(S, "F")
    if pooled:
        f2 = bx(S2, "F")
        cks = [chk("F <= F-bar-p", g(c, "F"), "<=", f["p_mean"]),
               chk("F <= Fb_min - 2", g(c, "F"), "<=", sub(f["b_min"], 2), "%s - 2" % fmt(f["b_min"])),
               chk("pass 2 alone: F <= F-bar-b", g(S2["c5"], "F"), "<=", f2["b_mean"])]
    else:
        cks = [chk("F <= F-bar-p + 1", g(c, "F"), "<=", add(f["p_mean"], 1), "%s + 1" % fmt(f["p_mean"])),
               chk("F <= Fb_min - 1", g(c, "F"), "<=", sub(f["b_min"], 1), "%s - 1" % fmt(f["b_min"]))]
    gates.append(gate("G1", "Is the target down to plain's level and below both base runs?", cks))
    k = bx(S, "K")
    gates.append(gate("G2", "Do the reductions land as KEPT rather than vague?", [
        chk("K - K-bar-b >= 0.5 x (F-bar-b - F)", sub(g(c, "K"), k["b_mean"]), ">=",
            mul(FR(1, 2), sub(f["b_mean"], g(c, "F"))), "0.5 x (%s - %s)" % (fmt(f["b_mean"]), fmt(g(c, "F"))))]))
    cc, mm, vv, ww = bx(S, "C"), bx(S, "M"), bx(S, "V"), bx(S, "W")
    cslack = 4 if pooled else 2
    gates.append(gate("G3", "Correct, missing, vague and wrong key points no worse than plain (and correct near base)?", [
        chk("C >= C-bar-p", g(c, "C"), ">=", cc["p_mean"]),
        chk("C >= C-bar-b - %d" % cslack, g(c, "C"), ">=", sub(cc["b_mean"], cslack), "%s - %d" % (fmt(cc["b_mean"]), cslack)),
        chk("M <= M-bar-p", g(c, "M"), "<=", mm["p_mean"]),
        chk("V <= V-bar-p", g(c, "V"), "<=", vv["p_mean"]),
        chk("W <= W-bar-p + 1", g(c, "W"), "<=", add(ww["p_mean"], 1), "%s + 1" % fmt(ww["p_mean"]))]))
    aw, au = bx(S, "AW"), bx(S, "AU")
    if pooled:
        cks = [chk("AW <= AW-bar-p", g(c, "AW"), "<=", aw["p_mean"]),
               chk("AU <= 1.10 x AU-bar-p", g(c, "AU"), "<=", mul(FR(11, 10), au["p_mean"]), "1.10 x %s" % fmt(au["p_mean"]))]
    else:
        cks = [chk("AW <= AWp_max", g(c, "AW"), "<=", aw["p_max"]),
               chk("AU <= 1.10 x AUp_max", g(c, "AU"), "<=", mul(FR(11, 10), au["p_max"]), "1.10 x %s" % fmt(au["p_max"]))]
    gates.append(gate("G4", "Wrong and unverified added claims no more than plain?", cks))
    h1, h2, h3 = bx(S, "H1"), bx(S, "H2"), bx(S, "H3")
    gates.append(gate("G5", "The three hedge lists?", [
        chk("H1 <= 1.05 x H1-bar-p", g(c, "H1"), "<=", mul(FR(105, 100), h1["p_mean"]), "1.05 x %s" % fmt(h1["p_mean"])),
        chk("H1 <= H1-bar-b", g(c, "H1"), "<=", h1["b_mean"]),
        chk("H2 <= max(H2-bar-b, 1.10 x H2-bar-p)", g(c, "H2"), "<=", max2(h2["b_mean"], mul(FR(11, 10), h2["p_mean"])),
            "max(%s, 1.10 x %s)" % (fmt(h2["b_mean"]), fmt(h2["p_mean"]))),
        chk("H3 <= H3-bar-b", g(c, "H3"), "<=", h3["b_mean"])]))
    mlv, mlb = median(S["lv"]), median(S["lb"])
    cks = [chk("median Lv >= 0.80", mlv, ">=", FR(8, 10)), chk("median Lv <= 1.00", mlv, "<=", FR(1)),
           chk("median Lb <= 1.04", mlb, "<=", FR(104, 100))]
    for n, xs in zip(S["passes"], S["lv_by_pass"]):
        short = None if any(x is None for x in xs) or not xs else sum(1 for x in xs if x < FR(6, 10))
        cks.append(chk("pass %s: prompts with Lv < 0.60 <= 1 (per 12)" % n, short, "<=", 1))
    for lg in ("en", "ko"):
        bm = median(S["base_lv_lang"][lg])
        cks.append(chk("%s median Lv <= base's own %s median Lv + 0.03" % (lg, lg), median(S["lv_lang"][lg]),
                       "<=", add(bm, FR(3, 100)), "%s + 0.03" % fmt(bm)))
    gates.append(gate("G6", "Length between 0.80 and 1.00 of plain and no more than 1.04 of base?", cks))
    pc1, pc2 = g(pd1.get("c5"), "PC"), g(pd2.get("c5"), "PC")
    gates.append(gate("G7", "Premise corrections kept?", [
        chk("every pass-2 answer corrects the premise (PC of pass 2 == 12)", pc2, "==", 12),
        chk("c5 answers missing it across both passes <= 1 (24 - PC1 - PC2)", sub(24, add(pc1, pc2)), "<=", 1)]))
    cd, bl, ux, wf = bx(S, "CD"), bx(S, "BL"), bx(S, "UX"), bx(S, "WF")
    cks = []
    for n, s, sp in zip(S["passes"], S["S_by_pass"], S["SP_by_pass"]):
        cks.append(chk("pass %s: S <= 2 (per 12)" % n, s, "<=", 2))
        cks.append(chk("pass %s: SP <= 1 (per 12)" % n, sp, "<=", 1))
    cks += [chk("SR == 0", g(c, "SR"), "==", 0),
            chk("CD <= 1.5 x CD-bar-b", g(c, "CD"), "<=", mul(FR(3, 2), cd["b_mean"]), "1.5 x %s" % fmt(cd["b_mean"])),
            chk("BL <= 1.5 x BL-bar-b", g(c, "BL"), "<=", mul(FR(3, 2), bl["b_mean"]), "1.5 x %s" % fmt(bl["b_mean"])),
            chk("unexcused source phrases (g11 rule) <= base mean", g(c, "UX"), "<=", ux["b_mean"]),
            chk("WF >= 0.75 x WF-bar-b", g(c, "WF"), ">=", mul(FR(3, 4), wf["b_mean"]), "0.75 x %s" % fmt(wf["b_mean"]))]
    gates.append(gate("G8", "Guards against spraying, safe picks, conditionals, sources and fetching?", cks))
    cks = []
    for lg in T.LANGS:
        cks.append(chk("%s: F <= F-bar-b" % lg, (g(c, "F_lang") or {}).get(lg), "<=", blang(S, "F_lang", lg, "base")))
        cks.append(chk("%s: M <= M-bar-p + 2" % lg, (g(c, "M_lang") or {}).get(lg), "<=",
                       add(blang(S, "M_lang", lg, "plain"), 2), "%s + 2" % fmt(blang(S, "M_lang", lg, "plain"))))
    gates.append(gate("G9", "Per language: the target and missing key points?", cks))
    extra = []
    if outcome1 == 5:
        extra.append(gate("R-a", "Does revision R-a clear its trigger (pass 2 alone is moved)?", [moved_check(S2)]))
    elif outcome1 == 4:
        t2 = triggers(S2)
        extra.append(gate("R-b", "Does revision R-b clear its trigger (no O1 to O6 on pass 2 alone)?", [
            {"name": "%s (%s) does not fire" % (kk, t["label"]), "value": t["result"], "op": "==", "bound": False,
             "bound_expr": "", "result": None if t["result"] is None else t["result"] is False} for kk, t in t2.items()]))
    inv = pd2.get("invalid_after_rerun")
    extra.append(gate("V", "Validity (instrument reading): is every pass-2 run valid after at most one rerun?", [
        chk("pass-2 runs still invalid after their rerun", inv, "==", 0)]))
    allpass = all(x["pass"] for x in gates + extra)
    decision = "GO" if allpass else "ABANDON"
    if decision == "GO" and stop:
        decision = "STOP_ASK_EMILY"
    return {"decision": decision, "scope": "both passes pooled (24 answers)" if pooled else "pass 2 alone (12 answers)",
            "gates": gates, "extra": extra, "scope_numbers": S}


# ------------------------------------------------------------------------------------------- loading real data

class Ctx:
    def __init__(self, base4=T.B4, base5=T.B5, inst=T.INST, real=True):
        self.b4, self.b5, self.inst, self.real = base4, base5, inst, real
        self.V, self.verdict_issue = T.load_verdict(base4)
        self.info, self.info_issues = T.load_case_lists(inst, base4)
        base = T.read_json(os.path.join(inst, T.SCHEMA_FILE))
        self.schemas = ({c: T.schema_for_case(base, self.info[c]["kp"], self.info[c]["lkp"], self.info[c]["pc_points"])
                         for c in T.CASES} if self.info else {})
        self._text = {}

    def instrument_issues(self):
        out = list(self.info_issues)
        if self.real and T.sha256_file(T.RULE_FILE) != T.RULE_SHA256:
            out.append("design/tuning-decision-rule.md changed since this instrument was built from it (sha256 %s); "
                       "the instrument must be reviewed against the new rule" % T.sha256_file(T.RULE_FILE))
        return out

    def text_group(self, arm, run):
        k = (arm, run)
        if k not in self._text:
            self._text[k] = group_text(self.V, arm, run, self.b4, self.b5)
        return self._text[k]


def superseded_files(ctx, batch):
    """Files that show a batch was rebuilt or regraded: a moved-aside grades file, id map or script folder."""
    out = []
    for d, pat in ((ctx.inst, r"grades-%s\.superseded-\d+\.json" % re.escape(batch)),
                   (os.path.join(ctx.inst, "maps"), r"%s-idmap\.superseded-\d+\.json" % re.escape(batch)),
                   (os.path.join(ctx.inst, "workflows"), r"%s\.superseded-\d+" % re.escape(batch))):
        try:
            names = sorted(os.listdir(d))
        except OSError:
            continue
        out += [n for n in names if re.fullmatch(pat, n)]
    return out


def batch_integrity(ctx, batch, obj):
    """The rule grades each pass as one shuffled batch. Problems found here mean that may not hold: the batch was
    rebuilt or regraded, a saved grade is not the first valid grade the ledger holds for its id, or a rerun was built
    for an id that already had a valid grade (or before its original grade was saved). Returns a list of problems."""
    out = []
    sup = superseded_files(ctx, batch)
    if sup:
        out.append("%s was rebuilt or regraded: superseded file(s) %s" % (batch, ", ".join(sup)))
    msha = T.sha256_file(os.path.join(ctx.inst, "maps", "%s-idmap.json" % batch))
    osha = obj.get("idmap_sha256")
    if msha is None or osha != msha:
        out.append("grades-%s.json was not saved against the current maps\\%s-idmap.json" % (batch, batch))
    rows, lprobs = T.read_ledger(ctx.inst)
    out += lprobs
    mine = [r for r in rows if r.get("batch") == batch]
    other = sorted({str(r.get("idmap_sha256"))[:12] for r in mine if r.get("idmap_sha256") != osha})
    if other:
        out.append("ledger5.jsonl holds grades of %s made under another id map (%s): the batch was rebuilt and graded "
                   "again" % (batch, ", ".join(other)))
    brows = [r for r in mine if r.get("idmap_sha256") == osha]
    first = T.first_valid_rows(brows)
    bad = [str(it.get("id")) for it in obj.get("items", [])
           if first.get(it.get("id")) is None or first[it["id"]].get("grade") != it.get("grade")]
    if bad:
        out.append("%d grade(s) in grades-%s.json are not the earliest valid ledger row for their id: %s"
                   % (len(bad), batch, ", ".join(bad[:8])))
    rr_path = os.path.join(ctx.inst, "maps", "%s-reruns.json" % batch)
    if os.path.exists(rr_path):
        try:
            reruns = T.read_json(rr_path)
        except (OSError, ValueError):
            reruns = None
        if not isinstance(reruns, list):
            out.append("maps\\%s-reruns.json is unreadable or not a list" % batch)
            reruns = []
        for k, rr in enumerate(reruns, 1):
            created = T.iso_epoch(rr.get("created")) if isinstance(rr, dict) else None
            ids = rr.get("ids") if isinstance(rr, dict) else None
            if created is None or not isinstance(ids, list):
                out.append("rerun record %d of %s is malformed" % (k, batch))
                continue
            for i in ids:
                # ledger rows and rerun records carry microsecond times; "before" is strictly earlier
                before = [r for r in brows if r.get("id") == i and T.iso_epoch(r.get("time")) is not None
                          and T.iso_epoch(r.get("time")) < created]
                if any(r.get("valid") is True for r in before):
                    out.append("rerun %d of %s was built for %s, which already had a valid grade" % (k, batch, i))
                elif not before:
                    out.append("rerun %d of %s was built for %s before any grade of it was saved" % (k, batch, i))
    return out


def load_grades(ctx, batch):
    """(obj, items{(case, arm, run): grade}, issues, integrity): grades-<batch>.json checked again, item by item.
    integrity lists the batch_integrity problems; when there are any, every item is None (the grades are not used)."""
    p = os.path.join(ctx.inst, "grades-%s.json" % batch)
    try:
        obj = T.read_json(p)
    except (OSError, ValueError) as e:
        return None, {}, ["grades-%s.json missing or unreadable (%s)" % (batch, e.__class__.__name__)], []
    if not isinstance(obj, dict):
        return None, {}, ["grades-%s.json is not an object" % batch], []
    issues, items = [], {}
    if obj.get("batch") != batch:
        issues.append("grades-%s.json is for batch %r" % (batch, obj.get("batch")))
    for f, key in ((T.LKP_FILE, "lkp_sha256"), (T.PREMISE_FILE, "premise_sha256"), (T.SCHEMA_FILE, "schema_sha256")):
        if T.sha256_file(os.path.join(ctx.inst, f)) != obj.get(key):
            issues.append("%s is not the file grades-%s.json was graded with" % (f, batch))
    for it in obj.get("items", []):
        k = (it.get("case"), it.get("arm"), it.get("run"))
        if k in items:
            issues.append("grades-%s.json repeats %s %s %s" % ((batch,) + k))
            continue
        if it.get("case") not in ctx.schemas:
            issues.append("grades-%s.json names an unknown case %r" % (batch, it.get("case")))
            continue
        probs, _ = T.validate_grade(it.get("grade"), ctx.schemas[it["case"]], it.get("id"),
                                    pc_ids=ctx.info[it["case"]]["premise"])
        t, err = T.packaged_text(T.answer_path(it["case"], it["arm"], it["run"], ctx.b4, ctx.b5))
        if probs:
            issues.append("%s (%s %s %s): %s" % (it.get("id"), it["case"], it["arm"], it["run"], "; ".join(probs[:3])))
            items[k] = None
        elif err or T.sha256_text(t) != it.get("answer_sha256"):
            issues.append("%s (%s %s %s): the answer on disk is %s" % (it.get("id"), it["case"], it["arm"], it["run"],
                                                                       err or "not the answer that was graded"))
            items[k] = None
        else:
            items[k] = it["grade"]
    integ = batch_integrity(ctx, batch, obj)
    if integ:
        issues += ["integrity: " + x for x in integ]
        items = {k: None for k in items}
    return obj, items, issues, integ


def calib_eval(items):
    rows, nflat = [], 0
    for c, a, r, i in CAL_FLAT:
        gr = items.get((c, a, r))
        mark = gr["lkp"].get(i) if gr else None
        ok = mark in ("FLAT", "WRONG")
        nflat += ok
        rows.append({"item": "%s %s %s kp%s" % (c, a, r, i), "want": "FLAT or WRONG", "got": mark or "MISSING", "ok": ok})
    kept = []
    for c, a, r, i in CAL_KEPT:
        gr = items.get((c, a, r))
        mark = gr["lkp"].get(i) if gr else None
        kept.append(mark == "KEPT")
        rows.append({"item": "%s %s %s kp%s" % (c, a, r, i), "want": "KEPT", "got": mark or "MISSING", "ok": mark == "KEPT"})
    checks = [chk("all-judges-wrong items marked FLAT or WRONG (of 3)", nflat, ">=", 2),
              chk("plain items marked KEPT (of 2)", sum(kept), "==", 2)]
    # PC bar (added after review, 2026-10-26): every round-four baseline group must reach the rule's own pass-1 PC bar
    # (PC <= 10 abandons, so PC >= 11) under this rubric. A rubric that fails answers which do correct the premise at
    # the top would abandon any change on PC alone; if a group falls short, the rubric is fixed, never the change.
    for a, r in T.BASELINE_GROUPS:
        grs = [items.get((c, a, r)) for c in T.CASES]
        n = sum(1 for x in grs if x["PC"] == "yes") if all(grs) else None
        checks.append(chk("%s %s: answers correcting the premise in the opening (PC) >= 11 of 12"
                          % ("base" if a == T.BASE else "plain", r), n, ">=", 11))
    return {"rows": rows, "checks": checks, "pass": all(x["result"] is True for x in checks)}


def calibration_status(ctx, batch):
    obj, items, issues, _ = load_grades(ctx, batch)
    want = {(c, a, r) for c in T.CASES for a, r in T.BASELINE_GROUPS}
    missing = sorted(want - set(items))
    extra = sorted(set(items) - want)
    if missing:
        issues.append("%d of the 48 baselines have no grade (first: %s)" % (len(missing), " ".join(missing[0])))
    if extra:
        issues.append("a calibration batch holds non-baseline answers: %s" % " ".join(extra[0]))
    ev = calib_eval(items)
    ok = ev["pass"] and not issues and obj is not None
    # When the calibration was saved: the later of the file's own "saved" time and its modification time (either one
    # missing gives None, which never counts as "before the first pass-1 run").
    saved = None
    if obj is not None:
        t = T.iso_epoch(obj.get("saved"))
        try:
            m = os.path.getmtime(os.path.join(ctx.inst, "grades-%s.json" % batch))
        except OSError:
            m = None
        saved = max(t, m) if t is not None and m is not None else None
    return {"batch": batch, "prompt_sha256": (obj or {}).get("prompt_sha256"), "issues": issues, "eval": ev, "pass": ok,
            "items": items, "saved_epoch": saved}


def calibration_batches(ctx):
    out = []
    for b in ("calibration", "calibration2", "calibration3"):
        if os.path.exists(os.path.join(ctx.inst, "grades-%s.json" % b)):
            out.append(b)
    return out


def read_validity(path, keys, files):
    """validity4.py-format report -> {"invalid_after_rerun": n or None, "invalid_count", "issues"}."""
    out = {"path": path, "invalid_after_rerun": None, "invalid_count": None, "still_invalid": [], "pending": [],
           "issues": []}
    try:
        rep = T.read_json(path)
    except (OSError, ValueError) as e:
        out["issues"].append("validity report %s missing or unreadable (%s)" % (path, e.__class__.__name__))
        return out
    if not (isinstance(rep, dict) and isinstance(rep.get("invalid"), list) and isinstance(rep.get("runs"), dict)
            and isinstance(rep.get("final_attempt_invalid", []), list)):
        out["issues"].append("validity report %s is not in validity4.py's format" % path)
        return out
    for k in ("round", "rule_files"):
        if rep.get(k):
            out["issues"].append("validity report lists %s problems: %s" % (k, "; ".join(map(str, rep[k]))[:300]))
    absent = [k for k in keys if k not in rep["runs"]]
    if absent:
        out["issues"].append("validity report has no entry for %s" % ", ".join(absent))
    mt = os.path.getmtime(path)
    newer = [f for f in files if os.path.exists(f) and os.path.getmtime(f) >= mt]
    if newer:
        out["issues"].append("validity report is not newer than %s (rerun the validity check)" % os.path.basename(newer[0]))
    fai = rep.get("final_attempt_invalid", [])
    out["still_invalid"] = [k for k in keys if k in fai]
    out["pending"] = [k for k in keys if k in rep["invalid"]]
    if out["pending"]:
        out["issues"].append("runs still due their one rerun: %s" % ", ".join(out["pending"]))
    out["invalid_count"] = sum(1 for k in keys if k in rep["invalid"] or k in fai
                               or (isinstance(rep["runs"].get(k), dict) and rep["runs"][k].get("rerun") is True))
    if not out["issues"]:
        out["invalid_after_rerun"] = len(out["still_invalid"])
    return out


def rd_scan(ctx, arm, run):
    """Regex hits of RD_PATTERNS in each run's thinking events: {case: [excerpts]} and truncation counts."""
    hits, trunc, issues = {}, 0, []
    for c in T.CASES:
        sp = T.stream_path(c, arm, run, ctx.b4, ctx.b5)
        if ctx.V is None:
            issues.append("verdict scripts not loaded")
            break
        ev, err = ctx.V.V4.parse_ndjson(sp)
        if err:
            issues.append("%s %s" % (sp, err))
            continue
        ex = []
        for e in ev:
            if e.get("type") != "thinking" or not isinstance(e.get("text"), str):
                continue
            trunc += bool(e.get("truncated"))
            for m in RD_RE.finditer(e["text"]):
                s = e["text"][max(0, m.start() - 120):m.end() + 120].replace("\n", " ")
                ex.append(s)
        if ex:
            hits[c] = ex
    return hits, trunc, issues


def rd_value(ctx, n, hits, scan_issues, hand_path):
    """RD from the hand reading of the regex hits. Missing (None) unless the hand file is present, well formed and
    has a true/false entry for every run with hits. Runs without hits that the hand reading marks true also count."""
    notes = []
    if scan_issues:
        return None, ["RD scan incomplete: " + "; ".join(scan_issues[:3])]
    if not os.path.exists(hand_path):
        if not hits:
            return 0, ["no regex hits in any run and no hand file; RD = 0"]
        return None, ["%s not found: RD needs the hand reading of the %d runs with regex hits (template written)"
                      % (os.path.basename(hand_path), len(hits))]
    try:
        hand = T.read_json(hand_path)
    except (OSError, ValueError):
        return None, ["%s unreadable" % hand_path]
    if not isinstance(hand, dict):
        return None, ["%s is not an object" % hand_path]
    bad = [c for c in hits if not (isinstance(hand.get(c), dict) and isinstance(hand[c].get("reads"), bool))]
    if bad:
        return None, ["%s has no true/false 'reads' for runs with hits: %s" % (os.path.basename(hand_path), ", ".join(bad))]
    rd = 0
    for c, v in hand.items():
        if c not in T.CASES or not isinstance(v, dict) or not isinstance(v.get("reads"), bool):
            if c not in hits:
                notes.append("hand entry %r ignored (not a case with a true/false 'reads')" % c)
            continue
        if v["reads"]:
            rd += 1
            if c not in hits:
                notes.append("%s has no regex hit but the hand reading marks it read; counted" % c)
    return rd, notes


def earliest_pass1_run(ctx):
    """Epoch seconds of the earliest evidence of a pass-1 c5 run: a start time in run-ledger.tsv (run.sh writes one
    row per attempt) or the creation or modification time of any of its files in tuning\\ or tuning\\attempt1\\.
    None when there is no such evidence."""
    times = []
    try:
        with open(os.path.join(ctx.b5, "run-ledger.tsv"), encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.rstrip("\r\n").split("\t")
                if (len(parts) >= 3 and parts[0].endswith(".%s.r1" % T.C5)
                        and parts[1].replace("\\", "/").rstrip("/").endswith("/tuning")):
                    try:
                        times.append(float(parts[2]))
                    except ValueError:
                        pass
    except OSError:
        pass
    pat = re.compile(r"\.%s\.r1\." % re.escape(T.C5))
    for d in (os.path.join(ctx.b5, "tuning"), os.path.join(ctx.b5, "tuning", "attempt1")):
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for name in names:
            if pat.search(name):
                try:
                    st = os.stat(os.path.join(d, name))
                except OSError:
                    continue
                times.append(min(st.st_mtime, st.st_ctime))
    return min(times) if times else None


def fmt_epoch(t):
    return "MISSING" if t is None else datetime.datetime.fromtimestamp(t).astimezone().isoformat(timespec="seconds")


def build_pass(ctx, n, validity_path, instrument_issues, calibrated):
    """Load everything for pass n. Returns (pd, report) where pd feeds pass1_outcome / pass2_decision."""
    batch = "pass%d" % n
    rep = {"batch": batch, "issues": list(instrument_issues), "notes": [], "integrity": []}
    obj, items, gissues, integ = load_grades(ctx, batch)
    rep["grades_file_sha256"] = T.sha256_file(os.path.join(ctx.inst, "grades-%s.json" % batch))
    rep["prompt_sha256"] = (obj or {}).get("prompt_sha256")
    grade_ok = obj is not None and not instrument_issues
    if integ:
        rep["integrity"] += integ
        grade_ok = False
    t0 = earliest_pass1_run(ctx)
    rep["earliest_pass1_run"] = fmt_epoch(t0)
    rep["calibration_used"] = None
    if obj is not None and rep["prompt_sha256"] not in calibrated:
        rep["issues"].append("the grades of %s were made with a grader prompt (sha256 %s) that has no passed "
                             "calibration" % (batch, str(rep["prompt_sha256"])[:12]))
        grade_ok = False
    elif obj is not None:
        # The calibration that counts must have been saved before the first pass-1 c5 run, so the rubric cannot be
        # refitted or recalibrated after any tuning answer exists (the rule: calibration before any DeepSeek run).
        cands = calibrated[rep["prompt_sha256"]]
        early = [b for b, t in cands if t is not None and t0 is not None and t < t0]
        if early:
            rep["calibration_used"] = early[0]
        else:
            msg = ("no passed calibration for this grader prompt was saved before the earliest pass-1 c5 run (%s): %s"
                   % (fmt_epoch(t0), ", ".join("%s saved %s" % (b, fmt_epoch(t)) for b, t in cands)))
            rep["issues"].append(msg)
            rep["integrity"].append(msg)
            grade_ok = False
    rep["issues"] += gissues
    groups = {"c5": (T.C5, "r%d" % n), "base r1": (T.BASE, "r1"), "base r2": (T.BASE, "r2"),
              "plain r1": (T.PLAIN, "r1"), "plain r2": (T.PLAIN, "r2")}
    want = {(c, a, r) for c in T.CASES for a, r in groups.values()}
    stray = sorted(set(items) - want)
    if stray:
        rep["issues"].append("grades-%s.json holds answers outside the pass: %s" % (batch, " ".join(stray[0])))
        grade_ok = False
    recs = {}
    for name, (a, r) in groups.items():
        gi = {c: items.get((c, a, r)) for c in T.CASES} if grade_ok and ctx.info else {}
        if grade_ok and any(v is None for v in gi.values()):
            rep["issues"].append("%s: %d of 12 answers have no usable grade" % (name, sum(v is None for v in gi.values())))
        grec = grade_group(gi, ctx.info or {})
        trec, tiss = ctx.text_group(a, r)
        if instrument_issues:
            trec = {k: None for k in TEXT_KEYS}
            trec["vis"] = {}
        rep["issues"] += ["%s: %s" % (name, x) for x in tiss]
        recs[name] = dict(grec, **{k: trec.get(k) for k in TEXT_KEYS}, vis=trec.get("vis") or {},
                          per_case_text=trec.get("per_case"))
    keys = ["%s.%s.r%d" % (c, T.C5, n) for c in T.CASES]
    files = [T.answer_path(c, T.C5, "r%d" % n, ctx.b4, ctx.b5) for c in T.CASES]
    files += [f[:-4] + ".ndjson" for f in files]
    val = read_validity(validity_path, keys, files)
    rep["validity"] = val
    rep["issues"] += val["issues"]
    hits, trunc, siss = rd_scan(ctx, T.C5, "r%d" % n)
    hand_path = os.path.join(ctx.inst, "rd-hand-pass%d.json" % n)
    rd, rnotes = rd_value(ctx, n, hits, siss, hand_path)
    rep["rd"] = {"regex_runs": sorted(hits), "hits": hits, "thinking_truncated_events": trunc, "RD": rd, "notes": rnotes,
                 "hand_file": hand_path}
    pd = {"n": n, "c5": recs["c5"], "base": [recs["base r1"], recs["base r2"]],
          "plain": [recs["plain r1"], recs["plain r2"]], "invalid_after_rerun": val["invalid_after_rerun"], "RD": rd}
    stop = val["invalid_count"] is not None and val["invalid_count"] > 2
    rep["stop_ask_emily"] = stop
    # One shuffled batch per pass (the rule): any sign that the batch was rebuilt, regraded or re-ordered, or graded
    # with a rubric calibrated after the tuning runs began, stops the round for Emily whatever the numbers say.
    rep["stop_integrity"] = bool(rep["integrity"])
    return pd, rep, items


# ------------------------------------------------------------------------------------------- printing

def show_check(x, mode):
    """mode 'gate' (pass only when True), 'cond' (holds when True or missing), 'plain'."""
    r = x["result"]
    if mode == "gate":
        tag = "PASS" if r is True else ("FAIL" if r is False else "FAIL: metric missing")
    elif mode == "cond":
        tag = "holds" if r is True else ("no" if r is False else "holds: metric missing")
    else:
        tag = "yes" if r is True else ("no" if r is False else "MISSING")
    b = fmt(x["bound"]) + (" (= %s)" % x["bound_expr"] if x.get("bound_expr") else "")
    return "  [%s] %s: %s %s %s" % (tag, x["name"], fmt(x["value"]), x["op"], b)


def print_groups(pd, label):
    print("\n--- Metrics per group of 12 answers (%s) ---" % label)
    hdr = ["group"] + list(GRADE_KEYS) + ["PCall"] + list(TEXT_KEYS)
    print("  " + " ".join("%-9s" % h for h in hdr))
    rows = [("c5", pd.get("c5"))] + list(zip(("base r1", "base r2"), pd.get("base") or [])) + \
        list(zip(("plain r1", "plain r2"), pd.get("plain") or []))
    for name, r in rows:
        vals = [fmt(g(r, k)) for k in GRADE_KEYS] + [fmt(g(r, "PC_all"))] + [fmt(g(r, k)) for k in TEXT_KEYS]
        print("  " + " ".join("%-9s" % v for v in [name] + vals))
    for name, r in rows:
        print("  %-9s F by language %s | M by language %s" % (
            name, " ".join("%s %s" % (lg, fmt((g(r, "F_lang") or {}).get(lg))) for lg in T.LANGS),
            " ".join("%s %s" % (lg, fmt((g(r, "M_lang") or {}).get(lg))) for lg in T.LANGS)))


def print_c5_table(pd):
    S = scope_of([pd])
    print("\n--- c5 per prompt (pass %s) ---" % pd.get("n"))
    print("  %-26s %5s %7s %7s %7s %7s" % ("case", "F", "vis", "plain", "Lv", "Lb"))
    for c, lv, lb in zip(T.CASES, S["lv"], S["lb"]):
        pv = [(g(p, "vis") or {}).get(c) for p in pd.get("plain") or []]
        pm = mean2(*pv) if len(pv) == 2 else None
        print("  %-26s %5s %7s %7s %7s %7s" % (c, fmt((g(pd.get("c5"), "per_case_F") or {}).get(c)),
                                              fmt((g(pd.get("c5"), "vis") or {}).get(c)), fmt(pm), fmt(lv), fmt(lb)))
    print("  median Lv %s, median Lb %s" % (fmt(median(S["lv"])), fmt(median(S["lb"]))))


def print_derived(S, title):
    print("\n--- Baseline numbers (%s) ---" % title)
    for k in ALL_KEYS:
        b = bx(S, k)
        print("  %-3s c5 %-9s | base mean %-9s min %-9s max %-9s | plain mean %-9s max %-9s" % (
            k, fmt(g(S["c5"], k)), fmt(b["b_mean"]), fmt(b["b_min"]), fmt(b["b_max"]), fmt(b["p_mean"]), fmt(b["p_max"])))


def print_pass1(res, pd):
    print("\n--- Pass 1, checked in the rule's order ---")
    print("1. ABANDON now if any of:")
    for x in res["abandon_checks"]:
        print(show_check(x, "cond"))
    print("2. Moved: " + show_check(res["moved"], "plain").strip() + "  -> %s" % ("moved" if res["is_moved"] else "not moved"))
    print("   Overshoot triggers (a trigger fires when its condition holds or cannot be computed):")
    for k, t in res["triggers"].items():
        print("   %s %s (%s): %s" % (k, t["label"], t["join"], "FIRES" if t["fires"] else "quiet"))
        for x in t["checks"]:
            print("  " + show_check(x, "cond"))
    print("   RD (runs whose reasoning quotes or applies the sentence): %s" % fmt(pd.get("RD")))
    print("   " + show_check(res["rd"], "plain").strip())
    print("\nOUTCOME %d: %s" % (res["outcome"], res["text"]))


def print_pass2(res):
    print("\n--- Pass 2: GO needs every check of G1 to G9 (scope: %s) ---" % res["scope"])
    for gt in res["gates"] + res["extra"]:
        print("%s %s %s" % (gt["gate"], "PASS" if gt["pass"] else "FAIL", gt["question"]))
        for x in gt["checks"]:
            print(show_check(x, "gate"))
    print("\nDECISION: %s" % res["decision"])


def jsonable(x):
    if isinstance(x, Fraction):
        return int(x) if x.denominator == 1 else {"value": float(x), "exact": "%d/%d" % (x.numerator, x.denominator)}
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x


def write_result(ctx, name, obj, nowrite):
    if nowrite:
        return
    p = os.path.join(ctx.inst, name)
    old = T.move_aside(p)
    T.write_json(p, jsonable(obj))
    print("\nwrote %s%s" % (p, " (the previous one moved to %s)" % old if old else ""))


def retest_report(ctx, pass_items, label):
    """The grader's retest change on the 48 baselines: this pass's grades against an earlier grading."""
    cals = [b for b in calibration_batches(ctx)]
    refs = []
    for b in cals:
        st = calibration_status(ctx, b)
        if st["pass"]:
            refs.append((b, st["items"]))
    if label != "pass1" and os.path.exists(os.path.join(ctx.inst, "grades-pass1.json")):
        _, it1, _, _ = load_grades(ctx, "pass1")
        refs.append(("pass1", it1))
    print("\n--- Grader retest on the 48 baselines (reported, not gated) ---")
    out = {}
    for name, ref in refs:
        same_l = tot_l = same_k = tot_k = same_f = 0
        deltas = {}
        for a, r in T.BASELINE_GROUPS:
            ga = grade_group({c: pass_items.get((c, a, r)) for c in T.CASES}, ctx.info)
            gb = grade_group({c: ref.get((c, a, r)) for c in T.CASES}, ctx.info)
            deltas["%s %s" % (a, r)] = {k: sub(g(ga, k), g(gb, k)) for k in GRADE_KEYS}
            for c in T.CASES:
                x, y = pass_items.get((c, a, r)), ref.get((c, a, r))
                if not (x and y):
                    continue
                for i in ctx.info[c]["lkp"]:
                    tot_l += 1
                    same_l += x["lkp"][i] == y["lkp"][i]
                    same_f += (x["lkp"][i] in ("FLAT", "WRONG")) == (y["lkp"][i] in ("FLAT", "WRONG"))
                for i in ctx.info[c]["kp"]:
                    tot_k += 1
                    same_k += x["key_points"][i] == y["key_points"][i]
        print("  against %s: LKP marks the same %d of %d; FLAT-or-WRONG status the same %d of %d; key-point marks the "
              "same %d of %d" % (name, same_l, tot_l, same_f, tot_l, same_k, tot_k))
        for grp, d in deltas.items():
            print("    %-16s change %s" % (grp, " ".join("%s %s" % (k, fmt(v)) for k, v in d.items())))
        out[name] = {"lkp_same": same_l, "lkp_total": tot_l, "flat_status_same": same_f, "kp_same": same_k,
                     "kp_total": tot_k, "metric_change": deltas}
    if not refs:
        print("  no earlier grading of the baselines to compare with")
    return out


def calibrated_prompts(ctx):
    """{grader prompt sha256: [(calibration batch, saved epoch or None)]} for every passed calibration."""
    out = {}
    for b in calibration_batches(ctx):
        st = calibration_status(ctx, b)
        if st["pass"]:
            out.setdefault(st["prompt_sha256"], []).append((b, st["saved_epoch"]))
    return out


def write_rd_template(ctx, n, rd, nowrite):
    if nowrite or not rd["hits"]:
        return
    p = os.path.join(ctx.inst, "rd-hand-pass%d.template.json" % n)
    T.write_json(p, {c: {"reads": None, "note": "", "hits": ex[:12]} for c, ex in sorted(rd["hits"].items())})
    print("wrote %s (copy to rd-hand-pass%d.json and set each 'reads' to true or false after reading the hits)" % (p, n))


def run_pass(ctx, n, validity, validity1, nowrite):
    inst_issues = ctx.instrument_issues()
    if ctx.verdict_issue:
        inst_issues.append(ctx.verdict_issue)
    calibrated = calibrated_prompts(ctx)
    print("=== Round-five tuning check, pass %d ===" % n)
    print("rule: %s (sha256 %s)" % (T.RULE_FILE, T.sha256_file(T.RULE_FILE)))
    print("passed calibrations: %s" % (", ".join("%s (prompt %s, saved %s)" % (b, s[:12], fmt_epoch(t))
                                                 for s, bs in calibrated.items() for b, t in bs) or "none"))
    pd, rep, items = build_pass(ctx, n, validity, inst_issues, calibrated)
    print("earliest pass-1 c5 run: %s; calibration that counts for pass %d: %s"
          % (rep["earliest_pass1_run"], n, rep["calibration_used"] or "none"))
    print_groups(pd, "graded in pass %d" % n)
    print_c5_table(pd)
    rt = retest_report(ctx, items, "pass%d" % n) if ctx.info else {}
    print("\n--- RD regex scan of the pass-%d c5 thinking ---" % n)
    for c, ex in sorted(rep["rd"]["hits"].items()):
        print("  %s: %d hits; first: ...%s..." % (c, len(ex), ex[0][:240]))
    print("  runs with hits %d; thinking events marked truncated %d; RD %s" % (
        len(rep["rd"]["hits"]), rep["rd"]["thinking_truncated_events"], fmt(rep["rd"]["RD"])))
    for x in rep["rd"]["notes"]:
        print("  note: " + x)
    write_rd_template(ctx, n, rep["rd"], nowrite)
    v = rep["validity"]
    print("\nvalidity (%s): still invalid after rerun %s; runs that were invalid at least once %s" % (
        v["path"], fmt(v["invalid_after_rerun"]), fmt(v["invalid_count"])))
    if rep["issues"]:
        print("\nISSUES (the metrics they touch count as MISSING):")
        for x in rep["issues"]:
            print("  - " + x)
    out = {"pass": n, "created": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "rule_sha256": T.sha256_file(T.RULE_FILE), "grades_file_sha256": rep["grades_file_sha256"],
           "prompt_sha256": rep["prompt_sha256"], "issues": rep["issues"], "validity": v,
           "rd": dict({k: rep["rd"][k] for k in ("regex_runs", "RD", "notes", "thinking_truncated_events")},
                      hits={c: ex[:12] for c, ex in rep["rd"]["hits"].items()}),
           "earliest_pass1_run": rep["earliest_pass1_run"], "calibration_used": rep["calibration_used"],
           "integrity": list(rep["integrity"]), "stop_ask_emily": rep["stop_ask_emily"], "retest": rt,
           "groups": {"c5": pd["c5"], "base r1": pd["base"][0], "base r2": pd["base"][1],
                      "plain r1": pd["plain"][0], "plain r2": pd["plain"][1]}}
    if n == 1:
        res = pass1_outcome(pd)
        print_derived(res["scope"], "pass 1")
        print_pass1(res, pd)
        out.update(outcome=res["outcome"], outcome_text=res["text"], abandon_checks=res["abandon_checks"],
                   moved=res["moved"], triggers=res["triggers"], rd_check=res["rd"],
                   lv=res["scope"]["lv"], lb=res["scope"]["lb"])
        out["action"] = "STOP_ASK_EMILY" if rep["stop_ask_emily"] or rep["stop_integrity"] else (
            "ABANDON" if res["outcome"] in (1, 6) else "PASS 2 (%s)" % {3: "same text", 4: "R-b", 5: "R-a"}[res["outcome"]])
        integ_all = list(rep["integrity"])
    else:
        dp = os.path.join(ctx.inst, "decision-pass1.json")
        try:
            d1 = T.read_json(dp)
        except (OSError, ValueError):
            print("\nREFUSED: decision-pass1.json missing; run --pass 1 first")
            return 2
        o1 = d1.get("outcome")
        if o1 not in (3, 4, 5):
            print("\nREFUSED: pass 1 gave outcome %r (%s); there is no pass 2" % (o1, d1.get("outcome_text")))
            return 2
        pd1, rep1, _ = build_pass(ctx, 1, validity1, inst_issues, calibrated)
        re1 = pass1_outcome(pd1)
        pre = []
        if d1.get("grades_file_sha256") != rep1["grades_file_sha256"]:
            pre.append("grades-pass1.json is not the file decision-pass1.json was computed from")
        if re1["outcome"] != o1:
            pre.append("pass 1 recomputed now gives outcome %d, not the %d in decision-pass1.json" % (re1["outcome"], o1))
        if d1.get("action") == "STOP_ASK_EMILY":
            pre.append("decision-pass1.json says STOP_ASK_EMILY")
        print("\npass 1: outcome %d (%s); recomputed %d" % (o1, OUTCOME_TEXT[o1], re1["outcome"]))
        print_groups(pd1, "pass 1, graded in pass 1")
        res = pass2_decision(pd1, pd, o1, stop=rep["stop_ask_emily"] or rep1["stop_ask_emily"])
        print_derived(res["scope_numbers"], res["scope"])
        if pre:
            res["extra"].append({"gate": "P1", "question": "Is pass 1's decision the one its files give now?",
                                 "checks": [{"name": x, "value": None, "op": "==", "bound": None, "bound_expr": "",
                                             "result": False} for x in pre], "pass": False})
            res["decision"] = "ABANDON"
        integ_all = list(rep["integrity"]) + ["pass 1: " + x for x in rep1["integrity"]]
        if integ_all:
            res["extra"].append({"gate": "I", "question": "Was each pass graded as one shuffled batch, with a rubric "
                                 "calibrated before the tuning runs?",
                                 "checks": [{"name": x, "value": None, "op": "==", "bound": None, "bound_expr": "",
                                             "result": False} for x in integ_all], "pass": False})
            res["decision"] = "STOP_ASK_EMILY"   # in place of GO or ABANDON: the numbers cannot be trusted either way
        print_pass2(res)
        out.update(pass1_outcome=o1, decision=res["decision"], scope=res["scope"], gates=res["gates"], extra=res["extra"],
                   lv=res["scope_numbers"]["lv"], lb=res["scope_numbers"]["lb"])
        out["integrity"] = integ_all
        out["action"] = res["decision"]
    if rep["stop_ask_emily"]:
        print("STOP: more than 2 runs of pass %d were invalid at least once; the rule says stop and ask Emily before "
              "acting on this result" % n)
    if integ_all:
        print("\nINTEGRITY (the rule grades each pass as one shuffled batch, calibrated before any DeepSeek run):")
        for x in integ_all:
            print("  - " + x)
        print("STOP: the grading of this round may have been repeated, re-ordered or recalibrated after the runs; "
              "STOP_ASK_EMILY whatever the numbers say")
    write_result(ctx, "decision-pass%d.json" % n, out, nowrite)
    return 0


def run_calibration(ctx, batch, nowrite):
    print("=== Round-five tuning check: calibration ===")
    batches = calibration_batches(ctx)
    if batch is None:
        if not batches:
            print("REFUSED: no grades-calibration*.json")
            return 2
        batch = batches[-1]
    st = calibration_status(ctx, batch)
    inst = ctx.instrument_issues() + ([ctx.verdict_issue] if ctx.verdict_issue else [])
    with open(os.path.join(ctx.inst, T.PROMPT_FILE), encoding="utf-8") as f:
        cur = T.sha256_text(f.read().rstrip())
    print("batch %s, grader prompt sha256 %s (current file %s)" % (batch, st["prompt_sha256"], cur))
    t0 = earliest_pass1_run(ctx)
    print("saved %s; earliest pass-1 c5 run %s" % (fmt_epoch(st["saved_epoch"]), fmt_epoch(t0) if t0 else "none yet"))
    if t0 is not None and not (st["saved_epoch"] is not None and st["saved_epoch"] < t0):
        print("NOTE: this calibration was not saved before the first pass-1 c5 run, so it cannot count for pass 1 or 2 "
              "(the rule calibrates before any DeepSeek run)")
    for r in st["eval"]["rows"]:
        print("  %-48s want %-13s got %-8s %s" % (r["item"], r["want"], r["got"], "ok" if r["ok"] else "NO"))
    for x in st["eval"]["checks"]:
        print(show_check(x, "gate"))
    for x in st["issues"] + inst:
        print("  ISSUE: " + x)
    ok = st["pass"] and not inst
    pd = {"n": 0, "c5": {}, "base": [], "plain": []}
    for name, (a, r) in zip(("base r1", "base r2", "plain r1", "plain r2"), T.BASELINE_GROUPS):
        grec = grade_group({c: st["items"].get((c, a, r)) for c in T.CASES}, ctx.info or {})
        trec, _ = ctx.text_group(a, r)
        rec = dict(grec, **{k: trec.get(k) for k in TEXT_KEYS}, vis=trec.get("vis") or {})
        (pd["base"] if a == T.BASE else pd["plain"]).append(rec)
    print_groups(pd, "the calibration grading")
    print("\nCALIBRATION %s" % ("PASSED" if ok else "FAILED: fix the rubric (not the change) and recalibrate"))
    write_result(ctx, "calibration-%s.json" % batch, {"batch": batch, "pass": ok, "prompt_sha256": st["prompt_sha256"],
                                                      "saved": fmt_epoch(st["saved_epoch"]),
                                                      "rows": st["eval"]["rows"], "checks": st["eval"]["checks"],
                                                      "issues": st["issues"] + inst,
                                                      "groups": {"base": pd["base"], "plain": pd["plain"]}}, nowrite)
    return 0 if ok else 1


def run_baseline_text(ctx):
    print("=== Text metrics of the 48 baselines (no grades needed) ===")
    if ctx.verdict_issue:
        print("ISSUE: " + ctx.verdict_issue)
    recs = {}
    for a, r in T.BASELINE_GROUPS:
        rec, iss = ctx.text_group(a, r)
        recs[(a, r)] = rec
        print("  %-13s %s  %s" % (a, r, " ".join("%s %s" % (k, fmt(rec.get(k))) for k in TEXT_KEYS)))
        for x in iss:
            print("    issue: " + x)
    pl = [recs[(T.PLAIN, "r1")], recs[(T.PLAIN, "r2")]]
    for rr in ("r1", "r2"):
        lv = lv_list(recs[(T.BASE, rr)], pl)
        print("  base %s visible length / plain mean: median %s; by language %s" % (rr, fmt(median(lv)), " ".join(
            "%s %s" % (lg, fmt(median([x for c, x in zip(T.CASES, lv) if T.lang_of(c) == lg]))) for lg in T.LANGS)))
    print("\n--- RD regex scan of round four's thinking (none of these runs saw change 5: every hit is a false positive) ---")
    total = 0
    for arm in (T.BASE, T.PLAIN, "gv-grav-c4"):
        for rr in T.RUNS:
            hits, trunc, iss = rd_scan(ctx, arm, rr)
            total += len(hits)
            print("  %-13s %s: runs with hits %d; truncated thinking events %d%s" % (
                arm, rr, len(hits), trunc, ("; issues: " + "; ".join(iss[:2])) if iss else ""))
            for c, ex in sorted(hits.items()):
                print("    %s: ...%s..." % (c, ex[0][:200]))
    print("  false-positive runs: %d of 72" % total)
    return 0


# ------------------------------------------------------------------------------------------- self-test

def selftest():
    fails = []

    def expect(label, cond, info=""):
        print("  [%s] %s%s" % ("ok" if cond else "FAIL", label, (" (%s)" % (info,)) if info and not cond else ""))
        if not cond:
            fails.append(label)

    def rec(**kw):
        r = {"F": 9, "K": 25, "C": 63, "V": 14, "M": 5, "W": 9, "AW": 7, "AU": 21, "S": 0, "SP": 0, "SR": 0, "PC": 12,
             "H1": FR(19, 10), "H2": FR(1), "H3": FR(14, 10), "CD": FR(12), "BL": 7, "WF": 30, "UX": 1,
             "F_lang": {"zh": 3, "en": 2, "ja": 2, "ko": 2}, "M_lang": {"zh": 2, "en": 1, "ja": 1, "ko": 1},
             "vis": {c: 900 for c in T.CASES}}
        for k, v in kw.items():
            if k in ("F_lang", "M_lang"):
                r[k] = dict(r[k], **v)
            elif k == "vis":
                r[k] = dict(r[k], **v) if isinstance(v, dict) else {c: v for c in T.CASES}
            else:
                r[k] = v
        return r

    B1 = rec(F=14, K=20, C=60, V=15, M=6, W=10, AW=8, AU=20, H1=FR(2), H2=FR(1), H3=FR(15, 10), CD=FR(10), BL=6, WF=30,
             UX=2, F_lang={"zh": 4, "en": 4, "ja": 3, "ko": 3}, M_lang={"zh": 2, "en": 1, "ja": 2, "ko": 1}, vis=1000)
    B2 = rec(F=12, K=22, C=62, V=14, M=6, W=9, AW=8, AU=22, H1=FR(22, 10), H2=FR(11, 10), H3=FR(16, 10), CD=FR(11), BL=7,
             WF=34, UX=2, F_lang={"zh": 3, "en": 4, "ja": 3, "ko": 2}, M_lang={"zh": 2, "en": 1, "ja": 2, "ko": 1}, vis=1000)
    P1 = rec(F=10, K=24, C=63, V=14, M=5, W=8, AW=7, AU=20, H1=FR(19, 10), H2=FR(1), H3=FR(12, 10), CD=FR(9), BL=5, WF=25,
             UX=1, F_lang={"zh": 3, "en": 3, "ja": 2, "ko": 2}, M_lang={"zh": 2, "en": 1, "ja": 1, "ko": 1}, vis=1000)
    P2 = rec(F=12, K=22, C=61, V=16, M=7, W=10, AW=9, AU=24, H1=FR(21, 10), H2=FR(12, 10), H3=FR(14, 10), CD=FR(10), BL=6,
             WF=27, UX=2, F_lang={"zh": 3, "en": 3, "ja": 3, "ko": 3}, M_lang={"zh": 2, "en": 1, "ja": 1, "ko": 1}, vis=1000)

    def pd(n=1, c5=None, **kw):
        d = {"n": n, "c5": c5 or rec(), "base": [B1, B2], "plain": [P1, P2], "invalid_after_rerun": 0, "RD": 0}
        d.update(kw)
        return d

    print("pass-1 outcomes")
    r = pass1_outcome({})
    expect("empty metrics object: ABANDON (outcome 1)", r["outcome"] == 1, r["outcome"])
    expect("empty metrics object: every ABANDON condition holds as missing",
           all(x["result"] is None and x["holds"] for x in r["abandon_checks"]))
    expect("empty metrics object: not moved, every trigger fires",
           not r["is_moved"] and all(t["fires"] for t in r["triggers"].values()))
    expect("good c5: outcome 3", pass1_outcome(pd())["outcome"] == 3, pass1_outcome(pd())["outcome"])
    for label, d in (("PC = 10", pd(c5=rec(PC=10))), ("a run still invalid after its rerun", pd(invalid_after_rerun=1)),
                     ("validity unknown", pd(invalid_after_rerun=None)), ("median Lv 0.69", pd(c5=rec(vis=690))),
                     ("M = M-bar-b + 6", pd(c5=rec(M=12)))):
        o = pass1_outcome(d)["outcome"]
        expect("outcome 1 from %s alone" % label, o == 1, o)
    for label, d in (("PC = 11", pd(c5=rec(PC=11))), ("median Lv 0.70", pd(c5=rec(vis=700))),
                     ("M = M-bar-b + 5", pd(c5=rec(M=11, V=14)))):
        o = pass1_outcome(d)["outcome"]
        expect("boundary %s does not abandon" % label, o != 1, o)
    o = pass1_outcome(pd(c5=rec(F=11)))
    expect("boundary F = Fb_min - 1 counts as moved (outcome 3)", o["outcome"] == 3, o["outcome"])
    for label, c5, trig in (("O1 (Lv 1.10, Lb 1.10)", rec(vis=1100), "O1"), ("O2 (S = 3)", rec(S=3), "O2"),
                            ("O3 (CD > 1.5 x base)", rec(CD=FR(16)), "O3"), ("O3 (BL > 1.5 x base)", rec(BL=10), "O3"),
                            ("O4 (K gain short)", rec(K=22), "O4"), ("O4 (V > V-bar-p + 2)", rec(V=18), "O4"),
                            ("O4 (M > M-bar-p)", rec(M=7), "O4"), ("O5 (H1 > H1b_max)", rec(H1=FR(23, 10)), "O5"),
                            ("O5 (H3 > H3b_max)", rec(H3=FR(17, 10)), "O5"), ("O6 (AU > 1.10 x AUp_max)", rec(AU=27), "O6"),
                            ("O6 (SP = 2)", rec(SP=2), "O6"), ("O6 (SR = 1)", rec(SR=1), "O6")):
        res = pass1_outcome(pd(c5=c5))
        fired = [k for k, t in res["triggers"].items() if t["fires"]]
        expect("outcome 4 from %s alone" % label, res["outcome"] == 4 and fired == [trig], "%s %s" % (res["outcome"], fired))
    for label, c5 in (("S = 2", rec(S=2)), ("SP = 1", rec(SP=1)), ("Lv 1.05 with Lb 1.05", rec(vis=1050)),
                      ("CD = 1.5 x base mean", rec(CD=FR(63, 4)))):
        o = pass1_outcome(pd(c5=c5))["outcome"]
        expect("boundary %s fires nothing (outcome 3)" % label, o == 3, o)
    nm = rec(F=12)
    o = pass1_outcome(pd(c5=nm, RD=2))["outcome"]
    expect("outcome 5: not moved, no trigger, RD = 2", o == 5, o)
    o = pass1_outcome(pd(c5=rec(F=12, S=3), RD=0))["outcome"]
    expect("outcome 6: not moved and a trigger", o == 6, o)
    o = pass1_outcome(pd(c5=nm, RD=3))["outcome"]
    expect("outcome 6: not moved and RD = 3", o == 6, o)
    o = pass1_outcome(pd(c5=nm, RD=None))["outcome"]
    expect("outcome 6: not moved and RD missing (counts as read)", o == 6, o)
    o = pass1_outcome(pd(c5=rec(F=None)))["outcome"]
    expect("F missing: not moved; with a quiet run and RD 0 that is outcome 5 only if nothing fires", o in (5, 6), o)
    expect("F missing makes O4 fire (missing counts as firing) so outcome 6", o == 6, o)

    print("pass-2 decisions")
    for o1 in (3, 4, 5):
        r = pass2_decision({}, {}, o1)
        expect("empty metrics object after outcome %d: every G fails, ABANDON" % o1,
               r["decision"] == "ABANDON" and not any(gt["pass"] for gt in r["gates"]) and len(r["gates"]) == 9,
               [gt["gate"] for gt in r["gates"] if gt["pass"]])
        expect("empty metrics object after outcome %d: every check is a metric-missing fail" % o1,
               all(x["result"] is None for gt in r["gates"] for x in gt["checks"]))
    good1, good2 = pd(1), pd(2)
    for o1 in (3, 4, 5):
        r = pass2_decision(good1, good2, o1)
        expect("GO after outcome %d (%s)" % (o1, r["scope"]), r["decision"] == "GO",
               [(gt["gate"], [x["name"] for x in gt["checks"] if x["result"] is not True]) for gt in r["gates"] + r["extra"]
                if not gt["pass"]])
    r = pass2_decision(good1, good2, 3, stop=True)
    expect("GO with more than 2 invalid runs becomes STOP_ASK_EMILY", r["decision"] == "STOP_ASK_EMILY", r["decision"])
    r = pass2_decision(good1, pd(2, invalid_after_rerun=1), 4)
    expect("a pass-2 run invalid after its rerun blocks GO", r["decision"] == "ABANDON")

    breaks = {  # each perturbs pass 2 so that exactly one gate fails, in both scopes
        "G1": {"F": 14, "F_lang": {}},
        "G2": {"K": 20},
        "G3": {"C": 55},
        "G4": {"AU": 40},
        "G5": {"H3": FR(3)},
        "G6": {"vis": 1200},
        "G7": {"PC": 11},
        "G8": {"SR": 1},
        "G9": {"F_lang": {"zh": 5}},
    }
    for o1 in (3, 4, 5):
        for gname, kw in breaks.items():
            kw2 = dict(kw)
            if o1 in (4, 5) and gname == "G1":
                kw2 = {"F": 13}            # single scope: F <= 11 + 1 fails, F <= F-bar-b still holds
            if o1 in (4, 5) and gname == "G4":
                kw2 = {"AW": 10}           # single scope: AW <= AWp_max (9)
            if o1 in (4, 5) and gname == "G6":
                kw2 = {"vis": 700}          # single scope: median Lv 0.70 < 0.80 (Lv >= 0.60, so no short count)
            r = pass2_decision(good1, pd(2, c5=rec(**kw2)), o1)
            failed = [gt["gate"] for gt in r["gates"] if not gt["pass"]]
            fx = [gt["gate"] for gt in r["extra"] if not gt["pass"]]
            expected_extra = []
            if o1 == 5 and gname == "G1":
                expected_extra = ["R-a"]   # R-a (moved on pass 2) is the same bound as G1's second check
            if o1 == 4 and gname in ("G1", "G2", "G3", "G4", "G5", "G6", "G8"):
                expected_extra = None      # some triggers mirror these gates; R-b may fail with them
            ok = failed == [gname] and r["decision"] == "ABANDON" and (expected_extra is None or fx == expected_extra)
            expect("after outcome %d: %s failing on its own gives ABANDON" % (o1, gname), ok, "%s %s" % (failed, fx))
    r = pass2_decision(pd(1, c5=rec(F=8)), pd(2, c5=rec(F=14, F_lang={})), 3)
    g1 = r["gates"][0]
    expect("pooled: 'pass 2 alone F <= F-bar-b' failing on its own fails G1 only",
           [gt["gate"] for gt in r["gates"] if not gt["pass"]] == ["G1"]
           and [x["name"] for x in g1["checks"] if x["result"] is not True] == ["pass 2 alone: F <= F-bar-b"],
           [x["name"] for x in g1["checks"] if x["result"] is not True])
    r = pass2_decision(pd(1, c5=rec(PC=11)), pd(2), 4)
    expect("G7 counts pass 1's misses even when pass 2 is judged alone (1 miss allowed)", r["decision"] == "GO")
    r = pass2_decision(pd(1, c5=rec(PC=11)), pd(2, c5=rec(PC=11)), 4)
    expect("G7 fails with one miss in each pass", [gt["gate"] for gt in r["gates"] if not gt["pass"]] == ["G7"])
    r = pass2_decision(pd(1, c5=rec(S=3)), pd(2), 3)
    expect("pooled G8 'S <= 2 per 12' is checked in each pass", [gt["gate"] for gt in r["gates"] if not gt["pass"]] == ["G8"])
    r = pass2_decision(good1, pd(2, c5=rec(S=3)), 4)
    expect("after outcome 4, a trigger on pass 2 fails R-b", any(gt["gate"] == "R-b" and not gt["pass"] for gt in r["extra"]))
    r = pass2_decision(good1, pd(2, c5=rec(F=12)), 5)
    expect("after outcome 5, pass 2 not moved fails R-a",
           any(gt["gate"] == "R-a" and not gt["pass"] for gt in r["extra"]) and r["decision"] == "ABANDON")

    print("regexes")
    expect("CD en counts 'only if' once", len(CD_RE["en"].findall("Only if you file, up to $5, unless late; if not.")) == 4)
    expect("CD zh skips 若干", len(CD_RE["zh"].findall("若干问题；如果超过最多不超过，只有满一年才可以，除非")) == 5)
    expect("CD ja skips ならない", len(CD_RE["ja"].findall("提出しなければならない。会社員なら最大10日まで、限りなく")) == 4)
    expect("CD ko counts word-final 면 and 라면, skips 면제", len(CD_RE["ko"].findall("퇴사하면 최대 14일까지, 근로자라면 면제 대상")) == 4)
    expect("BL en", bool(BL_RE["en"].search("If the plan has a grace period: ...")) and not BL_RE["en"].search("The plan, if any"))
    expect("BL ja first clause", bool(BL_RE["ja"].search("会社員の場合：申告は不要")) and not BL_RE["ja"].search("申告は不要です。もし…"))
    expect("BL ko first clause", bool(BL_RE["ko"].search("1년 이상 근무했다면 퇴직금이 나옵니다.")) and not BL_RE["ko"].search("퇴직금은 14일 안에 줘야 합니다. 늦으면"))
    expect("BL zh", bool(BL_RE["zh"].search("如果公司有审批：")) and bool(BL_RE["zh"].search("没有审批的话，按标准工时")))
    expect("RD finds the English sentence", bool(RD_RE.search("Rule 4 says plainly never means more absolute than what it found")))
    expect("RD finds the Korean sentence", bool(RD_RE.search("그 한도나 조건은 그것을 말하는 문장 안에 남깁니다")))
    expect("RD ignores 'to be safe'", not RD_RE.search("I'll say December 31 to be safe."))

    print("files: maker, saver and checker end to end (temporary folders)")
    file_tests(expect)
    print("dry build of the real calibration batch (reads round four's answers; writes only to a temporary folder)")
    dry_build(expect)
    print("\nSELFTEST %s (%d failures)" % ("PASSED" if not fails else "FAILED", len(fails)))
    for f in fails:
        print("  failed: " + f)
    return 0 if not fails else 1


FILLER = {"en": "This sentence is filler for the self-test and says nothing.",
          "zh": "这是一段用于自测的合成文字，没有实际含义。",
          "ja": "これは自己テスト用の合成文で、意味はありません。",
          "ko": "이 문장은 자체 시험용 합성 문장이며 뜻이 없습니다."}


def synth_text(case, n):
    return "\n\n".join([FILLER[T.lang_of(case)]] * n) + "\n"


def synth_stream(fetches, thinking=""):
    ev = [{"type": "session", "sessionId": "s", "cwd": "x"}]
    if thinking:
        ev.append({"type": "thinking", "text": thinking, "truncated": False})
    for i in range(fetches):
        ev.append({"type": "tool_call", "callId": "c%d" % i, "tool": "web_fetch", "input": {"url": "https://example.org"}})
        ev.append({"type": "tool_result", "callId": "c%d" % i, "status": "completed", "result": "Fetched https://example.org (HTTP 200)"})
    ev.append({"type": "final", "text": "x"})
    return "\n".join(json.dumps(e) for e in ev) + "\n"


def synth_grade(iid, case, info, arm, f_count, cal=None):
    """A valid grade: LKP FLAT for the first f_count limited points, KEPT for the rest; cal overrides one LKP mark."""
    kp = {i: "correct" for i in info[case]["kp"]}
    lkp = {}
    for n, i in enumerate(info[case]["lkp"]):
        lkp[i] = "FLAT" if n < f_count else "KEPT"
    if cal:
        lkp[cal[0]] = cal[1]
    return {"id": iid, "key_points": kp, "lkp": lkp, "lkp_quotes": {i: FILLER[T.lang_of(case)][:10] for i in lkp},
            "AW": [], "AU": [], "S": [], "SP": [], "SR": [], "PC": "yes",
            "PC_points": {i: "yes" for i in info[case]["pc_points"]}, "PC_quote": FILLER[T.lang_of(case)][:10]}


def file_tests(expect):
    import contextlib
    import io
    import time
    import make_tuning_grade_script as MK
    import save_tuning_grades5 as SV
    tmp = tempfile.mkdtemp(prefix="tuning5-selftest-")

    def quietly(fn, *a, **kw):
        with contextlib.redirect_stdout(io.StringIO()):
            return fn(*a, **kw)

    def read_or_empty(p):
        """A decision file, or {} when the checker refused and wrote none (the failing check then says so)."""
        try:
            return T.read_json(p)
        except (OSError, ValueError):
            return {}

    def refused(fn, *a, **kw):
        try:
            quietly(fn, *a, **kw)
        except SystemExit:
            return True
        return False

    try:
        b4, b5, inst = (os.path.join(tmp, d) for d in ("ab4", "ab5", "inst"))
        for d in ("prompts", "keys", "keypoints", "raw"):
            os.makedirs(os.path.join(b4, d))
        os.makedirs(os.path.join(b5, "tuning"))
        os.makedirs(inst)
        for f in (T.VERDICT_AMENDED, "verdict4.py"):
            shutil.copy2(os.path.join(T.B4, f), os.path.join(b4, f))
        for c in T.CASES:
            for d, ext in (("prompts", ".txt"), ("keys", ".md"), ("keypoints", ".json")):
                shutil.copy2(os.path.join(T.B4, d, c + ext), os.path.join(b4, d, c + ext))
            for a, r in T.BASELINE_GROUPS:
                with open(os.path.join(b4, "raw", "%s.%s.%s.txt" % (c, a, r)), "w", encoding="utf-8") as f:
                    f.write(synth_text(c, 10))
                with open(os.path.join(b4, "raw", "%s.%s.%s.ndjson" % (c, a, r)), "w", encoding="utf-8") as f:
                    f.write(synth_stream(3))

        def write_c5():
            """The c5 answers are written only after the calibration is saved, as in the real order of work."""
            for c in T.CASES:
                for rr, think in (("r1", "Plainly never means more absolute than what it found." if c == T.CASES[0] else ""),
                                  ("r2", "")):
                    with open(os.path.join(b5, "tuning", "%s.%s.%s.txt" % (c, T.C5, rr)), "w", encoding="utf-8") as f:
                        f.write(synth_text(c, 9))
                    with open(os.path.join(b5, "tuning", "%s.%s.%s.ndjson" % (c, T.C5, rr)), "w", encoding="utf-8") as f:
                        f.write(synth_stream(3, think))

        for f in (T.LKP_FILE, T.PREMISE_FILE, T.PROMPT_FILE, T.SCHEMA_FILE):
            shutil.copy2(os.path.join(T.INST, f), os.path.join(inst, f))
        info, _ = T.load_case_lists(inst, b4)

        print("  premise points and PC")
        expect("premise points: PC is gated on key point 1 alone in all 12 cases",
               all(info[c]["premise"] == ["1"] for c in T.CASES), {c: info[c]["premise"] for c in T.CASES})
        expect("premise points: the 6 other premise corrections are reported, not gated",
               sum(len(info[c]["reported"]) for c in T.CASES) == 6
               and info["ja-wallpaper-restoration"]["pc_points"] == ["1", "2", "3"])
        wc = "ja-wallpaper-restoration"
        sch = T.schema_for_case(T.read_json(os.path.join(inst, T.SCHEMA_FILE)), info[wc]["kp"], info[wc]["lkp"],
                                info[wc]["pc_points"])
        gr = synth_grade("t001", wc, info, T.BASE, 0)
        gr["PC_points"]["2"] = "no"
        expect("validator: PC yes with a reported premise point no is valid (only key point 1 is gated)",
               T.validate_grade(gr, sch, "t001", pc_ids=info[wc]["premise"])[0] == [])
        expect("validator: without the gated ids every PC_points entry is gated (the stricter default)",
               T.validate_grade(gr, sch, "t001")[0] != [])
        gr2 = synth_grade("t001", wc, info, T.BASE, 0)
        gr2["PC"] = "no"
        expect("validator: PC no while the gated premise point is yes is refused",
               T.validate_grade(gr2, sch, "t001", pc_ids=info[wc]["premise"])[0] != [])
        grs = {c: synth_grade("t001", c, info, T.BASE, 0) for c in T.CASES}
        grs[wc]["PC_points"]["3"] = "no"
        gg = grade_group(grs, info)
        expect("checker: PC counts the gated point (12) and PC_all reports every premise point (11)",
               gg["PC"] == 12 and gg["PC_all"] == 11, (gg["PC"], gg["PC_all"]))

        print("  maker and saver")
        m = quietly(MK.build, "calibration", inst, b4, b5, 120000, False)
        ids = [it["id"] for it in m["items"]]
        expect("maker: 48 ids t001-t048", ids == ["t%03d" % i for i in range(1, 49)])
        order = [(it["case"], it["arm"], it["run"]) for it in m["items"]]
        expect("maker: shuffled with the seed (not in build order)", order != MK.batch_items("calibration", b4, b5))
        expect("maker: split into parts under the limit", len(m["parts"]) > 1 and all(p["bytes"] <= 120000 for p in m["parts"]),
               [p["bytes"] for p in m["parts"]])
        scripts = "".join(open(os.path.join(inst, p["file"]), encoding="utf-8").read() for p in m["parts"])
        expect("maker: no arm, run or folder name in the scripts", not any(s in scripts for s in MK.ARM_STRINGS))
        expect("maker: scripts use model opus and opaque labels", "model: 'opus'" in scripts and "label: `grade:${it.id}`" in scripts)
        expect("maker: every id appears in exactly one part", sorted(i for p in m["parts"] for i in p["ids"]) == sorted(ids))
        expect("maker: refuses to rebuild a batch without --replace",
               refused(MK.build, "calibration", inst, b4, b5, 120000, False))

        def out_rows(idmap, override=None, drop=None):
            rows = []
            for it in idmap["items"]:
                if drop and it["id"] in drop:
                    continue
                cal = None
                for cc, a, r, i in CAL_FLAT:
                    if (it["case"], it["arm"], it["run"]) == (cc, a, r):
                        cal = (i, "FLAT")
                for cc, a, r, i in CAL_KEPT:
                    if (it["case"], it["arm"], it["run"]) == (cc, a, r):
                        cal = (i, "KEPT")
                fc = {T.BASE: 2, T.PLAIN: 1, T.C5: 0}[it["arm"]]
                gr = synth_grade(it["id"], it["case"], info, it["arm"], fc, cal)
                if override and it["id"] in override:
                    override[it["id"]](gr)
                rows.append({"id": it["id"], "grade": gr})
            return rows

        def write_out(name, rows):
            p = os.path.join(tmp, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False)
            return p

        first, second = ids[0], ids[1]
        bad_cases = {
            "a missing id": dict(drop={first}),
            "a bad key-point value": dict(override={first: lambda gr: gr["key_points"].update({"1": "half"})}),
            "a missing key-point id": dict(override={first: lambda gr: gr["key_points"].pop("1")}),
            "an extra LKP id": dict(override={first: lambda gr: gr["lkp"].update({"99": "KEPT"})}),
            "PC yes with the gated premise point no": dict(override={first: lambda gr: gr["PC_points"].update({"1": "no"})}),
            "PC no with the gated premise point yes": dict(override={first: lambda gr: gr.update({"PC": "no"})}),
            "a missing reported premise point": dict(override={
                it["id"]: (lambda gr: gr["PC_points"].pop(list(gr["PC_points"])[-1]))
                for it in m["items"] if info[it["case"]]["reported"]}),
            "ABSENT on a key point not marked missing": dict(override={first: lambda gr: gr["lkp"].update(
                {list(gr["lkp"])[0]: "ABSENT"})}),
            "a wrong grade id": dict(override={first: lambda gr: gr.update({"id": "t999"})}),
            "an empty quote in AW": dict(override={first: lambda gr: gr["AW"].append({"quote": "", "reason": "x"})}),
        }
        for label, kw in bad_cases.items():
            p = write_out("bad.json", out_rows(m, **kw))
            ok, probs, _ = SV.save("calibration", [p], inst, b4, b5, quiet=True)
            expect("saver refuses %s" % label, not ok and probs and not os.path.exists(os.path.join(inst, "grades-calibration.json")),
                   probs[:1])
        rows = out_rows(m)
        rows.append({"id": "t777", "grade": rows[0]["grade"]})
        ok, probs, _ = SV.save("calibration", [write_out("bad.json", rows)], inst, b4, b5, quiet=True)
        expect("saver refuses an id outside the map", not ok)
        led = os.path.join(inst, T.LEDGER_FILE)
        lrows, lprobs = T.read_ledger(inst)
        expect("saver: every row received is on the ledger with its id map's sha256",
               len(lrows) > 48 and not lprobs and all(r.get("idmap_sha256") == T.sha256_file(
                   os.path.join(inst, "maps", "calibration-idmap.json")) for r in lrows))
        os.remove(led)   # the rerun tests below start from an empty ledger (a temporary folder, not the real one)

        print("  one batch per pass: reruns and the order of outputs")
        expect("maker --only refuses an id with no ledger row (the part output is not saved yet)",
               refused(MK.rerun, "calibration", [first], inst, b4, b5, 500000))
        rows_a = out_rows(m)
        for row in rows_a:
            if row["id"] == first:
                row["grade"] = None              # the agent returned nothing for this id
        p_a = write_out("part_a.json", rows_a)
        ok, probs, _ = SV.save("calibration", [p_a], inst, b4, b5, quiet=True)
        expect("saver refuses while one id has no valid grade", not ok and any(first in x for x in probs), probs[:2])
        expect("maker --only refuses an id that already has a valid grade on the ledger",
               refused(MK.rerun, "calibration", [second], inst, b4, b5, 500000))
        expect("maker --only builds a rerun for an id whose only ledger row has no grade",
               not refused(MK.rerun, "calibration", [first], inst, b4, b5, 500000)
               and os.path.exists(os.path.join(inst, "workflows", "calibration", "grade-calibration.rerun1.js")))
        g_first = [r for r in out_rows(m) if r["id"] == first][0]["grade"]
        g_second_orig = [r for r in out_rows(m) if r["id"] == second][0]["grade"]
        g_second_new = json.loads(json.dumps(g_second_orig))
        kp1 = info[[it for it in m["items"] if it["id"] == second][0]["case"]]["kp"][0]
        g_second_new["key_points"][kp1] = "vague"   # still valid, and a different grade
        p_rr = write_out("rerun1.json", {"result": [{"id": first, "grade": g_first}, {"id": second, "grade": g_second_new}]})
        ok, probs, notes = SV.save("calibration", [p_rr, p_a], inst, b4, b5, quiet=True)
        gc_path = os.path.join(inst, "grades-calibration.json")
        saved = {it["id"]: it["grade"] for it in T.read_json(gc_path)["items"]} if ok else {}
        expect("saver uses the earliest valid ledger grade for each id, whatever order the files are given in",
               ok and saved.get(second) == g_second_orig and saved.get(first) == g_first
               and any(second in x and "not used" in x for x in notes), (probs[:2], notes[:2]))
        ctx = Ctx(b4, b5, inst, real=False)
        st = calibration_status(ctx, "calibration")
        expect("checker: calibration passes on the designed marks (PC >= 11 in every baseline group too)", st["pass"],
               st["issues"][:2] + [x["name"] for x in st["eval"]["checks"] if x["result"] is not True])
        expect("checker: the calibration's rerun record agrees with the ledger",
               batch_integrity(ctx, "calibration", T.read_json(gc_path)) == [])

        m2 = quietly(MK.build, "calibration2", inst, b4, b5, 500000, False)
        flip = {}
        for it in m2["items"]:
            for cc, a, r, i in CAL_FLAT[:2] + CAL_KEPT[:1]:
                if (it["case"], it["arm"], it["run"]) == (cc, a, r):
                    flip[it["id"]] = (lambda i_: (lambda gr: gr["lkp"].update({i_: "WRONG" if gr["lkp"][i_] == "KEPT" else "KEPT"})))(i)
        rows2 = out_rows(m2)
        for row in rows2:
            if row["id"] in flip:
                flip[row["id"]](row["grade"])
        ok, probs, _ = SV.save("calibration2", [write_out("cal2.json", rows2)], inst, b4, b5, quiet=True)
        st2 = calibration_status(ctx, "calibration2")
        expect("checker: a calibration with 1 of 3 FLAT and a plain item not KEPT fails", ok and not st2["pass"],
               st2["eval"]["checks"])
        m3 = quietly(MK.build, "calibration3", inst, b4, b5, 500000, False)
        rows3 = out_rows(m3)
        no_pc = {(c, T.PLAIN, "r2") for c in T.CASES[:2]}
        for row, it in zip(rows3, m3["items"]):
            if (it["case"], it["arm"], it["run"]) in no_pc:
                row["grade"]["PC"] = "no"
                row["grade"]["PC_points"]["1"] = "no"
        ok, probs, _ = SV.save("calibration3", [write_out("cal3.json", rows3)], inst, b4, b5, quiet=True)
        st3 = calibration_status(ctx, "calibration3")
        failed = [x["name"] for x in st3["eval"]["checks"] if x["result"] is not True]
        expect("checker: a calibration with PC 10 of 12 in one baseline group fails on that group's PC check alone",
               ok and not st3["pass"] and len(failed) == 1 and failed[0].startswith("plain r2: "), (ok, failed))

        time.sleep(0.05)
        write_c5()
        for n in (1, 2):
            mp = quietly(MK.build, "pass%d" % n, inst, b4, b5, 500000, False)
            expect("maker: pass%d has 60 ids t%d01-t%d60" % (n, n, n),
                   [it["id"] for it in mp["items"]] == ["t%03d" % (100 * n + i) for i in range(1, 61)])
            ok, probs, _ = SV.save("pass%d" % n, [write_out("p%d.json" % n, out_rows(mp))], inst, b4, b5, quiet=True)
            expect("saver: pass%d saved" % n, ok, probs[:2])
        vpath = os.path.join(b5, "validity-tuning.json")
        T.write_json(vpath, {"rule_files": [], "round": [], "invalid": [], "flagged": [], "final_attempt_invalid": [],
                             "runs": {"%s.%s.r%d" % (c, T.C5, n): {"rerun": False, "problems": []}
                                      for c in T.CASES for n in (1, 2)}})
        dp1 = os.path.join(inst, "decision-pass1.json")
        quietly(run_pass, ctx, 1, vpath, vpath, False)
        d1 = T.read_json(dp1)
        expect("checker pass 1 without the hand reading: RD missing and the hit run listed",
               d1["rd"]["RD"] is None and d1["rd"]["regex_runs"] == [T.CASES[0]], d1["rd"])
        expect("checker pass 1: moved (c5 F 0 vs base 24) and quiet text gives outcome 3", d1["outcome"] == 3,
               (d1["outcome"], [k for k, t in d1["triggers"].items() if t["fires"]], d1["issues"][:3]))
        expect("checker pass 1: the calibration saved before the c5 runs is the one that counts",
               d1["calibration_used"] == "calibration" and d1["integrity"] == [], (d1["calibration_used"], d1["integrity"]))
        T.write_json(os.path.join(inst, "rd-hand-pass1.json"), {T.CASES[0]: {"reads": True, "note": "quotes it"}})
        quietly(run_pass, ctx, 1, vpath, vpath, False)
        d1 = T.read_json(dp1)
        expect("checker pass 1 with the hand reading: RD 1, outcome 3, old decision kept aside",
               d1["rd"]["RD"] == 1 and d1["outcome"] == 3
               and os.path.exists(os.path.join(inst, "decision-pass1.superseded-1.json")), d1["rd"])
        expect("checker pass 1: text metrics measured from the files (vis, WF 36, UX 0)",
               d1["groups"]["c5"]["WF"] == 36 and d1["groups"]["c5"]["UX"] == 0 and d1["lv"][0] is not None)
        quietly(run_pass, ctx, 2, vpath, vpath, False)
        d2 = read_or_empty(os.path.join(inst, "decision-pass2.json"))
        expect("checker pass 2 (pooled after outcome 3): GO on the designed data", d2.get("decision") == "GO",
               [(gt["gate"], [x["name"] for x in gt["checks"] if x["result"] is not True])
                for gt in d2.get("gates", []) + d2.get("extra", [])
                if not gt["pass"]])

        print("  one batch per pass: the checker's integrity checks")
        gp1 = os.path.join(inst, "grades-pass1.json")
        with open(gp1, "rb") as f:
            gp1_bytes = f.read()

        def restore_gp1():
            with open(gp1, "wb") as f:
                f.write(gp1_bytes)

        def pass1_stops(label):
            quietly(run_pass, ctx, 1, vpath, vpath, False)
            d = T.read_json(dp1)
            expect("checker pass 1: %s gives STOP_ASK_EMILY and no grade metric" % label,
                   d["action"] == "STOP_ASK_EMILY" and d["integrity"] and d["groups"]["c5"]["F"] is None
                   and d["groups"]["base r1"]["F"] is None, (d["action"], d["integrity"][:2]))

        obj = json.loads(gp1_bytes.decode("utf-8"))
        it0 = obj["items"][0]
        it0["grade"]["key_points"][info[it0["case"]]["kp"][0]] = "vague"
        T.write_json(gp1, obj)
        pass1_stops("a saved grade that is not the earliest valid ledger row")
        restore_gp1()
        sup = os.path.join(inst, "grades-pass1.superseded-1.json")
        shutil.copy2(gp1, sup)
        pass1_stops("a superseded grades file (the pass was regraded)")
        os.remove(sup)
        rr1 = os.path.join(inst, "maps", "pass1-reruns.json")
        T.write_json(rr1, [{"file": "workflows/pass1/grade-pass1.rerun1.js", "sha256": "0", "ids": ["t101"],
                            "created": datetime.datetime.now().astimezone().isoformat(timespec="microseconds")}])
        pass1_stops("a rerun record for an id that already had a valid grade")
        os.remove(rr1)
        expect("maker --only refuses every id of a fully graded pass", refused(MK.rerun, "pass2", ["t201"], inst, b4, b5, 500000))
        gc_stat = os.stat(gc_path)
        later = time.time() + 120
        os.utime(gc_path, (later, later))
        pass1_stops("a calibration saved after the first pass-1 c5 run")
        quietly(run_pass, ctx, 1, vpath, vpath, False)
        d1 = T.read_json(dp1)
        expect("checker pass 1: the late calibration is named in the issues",
               any("saved before the earliest pass-1 c5 run" in x for x in d1["issues"]), d1["issues"][:3])
        os.utime(gc_path, (gc_stat.st_atime, gc_stat.st_mtime))
        quietly(run_pass, ctx, 1, vpath, vpath, False)
        d1 = T.read_json(dp1)
        expect("checker pass 1: with every integrity problem undone, outcome 3 again", d1["outcome"] == 3
               and d1["action"] == "PASS 2 (same text)" and d1["integrity"] == [], (d1["outcome"], d1["action"], d1["integrity"]))
        sup2 = os.path.join(inst, "maps", "pass2-idmap.superseded-1.json")
        shutil.copy2(os.path.join(inst, "maps", "pass2-idmap.json"), sup2)
        quietly(run_pass, ctx, 2, vpath, vpath, False)
        d2 = read_or_empty(os.path.join(inst, "decision-pass2.json"))
        expect("checker pass 2: a rebuilt pass-2 batch gives STOP_ASK_EMILY in place of the decision",
               d2.get("decision") == "STOP_ASK_EMILY" and any(gt["gate"] == "I" for gt in d2.get("extra", [])),
               d2.get("decision"))
        os.remove(sup2)
        supc = os.path.join(inst, "grades-calibration.superseded-1.json")
        shutil.copy2(gc_path, supc)
        stc = calibration_status(ctx, "calibration")
        expect("checker: a regraded calibration batch does not count", not stc["pass"]
               and any("superseded" in x for x in stc["issues"]), stc["issues"][:2])
        os.remove(supc)

        T.write_json(vpath, {"rule_files": [], "round": [], "invalid": [], "flagged": [],
                             "final_attempt_invalid": ["%s.%s.r1" % (T.CASES[1], T.C5)],
                             "runs": {"%s.%s.r%d" % (c, T.C5, n): {"rerun": c in T.CASES[1:4], "problems": []}
                                      for c in T.CASES for n in (1, 2)}})
        quietly(run_pass, ctx, 1, vpath, vpath, False)
        d1 = T.read_json(dp1)
        expect("checker pass 1: a run invalid after its rerun gives outcome 1; 3 reruns give STOP_ASK_EMILY",
               d1["outcome"] == 1 and d1["action"] == "STOP_ASK_EMILY", (d1["outcome"], d1["action"]))
        os.remove(gp1)
        quietly(run_pass, ctx, 1, vpath, vpath, False)
        d1 = T.read_json(dp1)
        expect("checker pass 1 with no grades file: every grade metric missing, outcome 1",
               d1["outcome"] == 1 and d1["groups"]["c5"]["F"] is None)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def dry_build(expect):
    import contextlib
    import io
    import make_tuning_grade_script as MK
    tmp = tempfile.mkdtemp(prefix="tuning5-dry-")
    try:
        for f in (T.LKP_FILE, T.PREMISE_FILE, T.PROMPT_FILE, T.SCHEMA_FILE):
            shutil.copy2(os.path.join(T.INST, f), os.path.join(tmp, f))
        with contextlib.redirect_stdout(io.StringIO()):
            m = MK.build("calibration", tmp, T.B4, T.B5, MK.MAX_BYTES, False)
        sizes = [p["bytes"] for p in m["parts"]]
        expect("real calibration batch: 48 answers in %d part(s) of %s bytes, each under %d" % (
            len(sizes), "/".join(map(str, sizes)), MK.MAX_BYTES), len(m["items"]) == 48 and max(sizes) <= MK.MAX_BYTES)
        scripts = "".join(open(os.path.join(tmp, p["file"]), encoding="utf-8").read() for p in m["parts"])
        expect("real calibration batch: no arm or run name in the scripts",
               not any(s in scripts for s in ("gv-plain", "gv-grav")))
        with open(os.path.join(tmp, m["parts"][0]["file"]), encoding="utf-8") as f:
            head = f.read(400)
        expect("real calibration batch: script starts with a pure-literal meta", head.startswith("export const meta = {\n  name: '"))
        expect("real calibration batch: every packet names key point 1 as the PC point",
               scripts.count("### Premise point for PC (id)\\n\\n1\\n\\n### Other premise corrections") == 12)
        expect("real calibration batch: the reported premise corrections are in their packets (ja-wallpaper 2, 3)",
               "(ids; marked in PC_points, not part of PC)\\n\\n2, 3\"" in scripts)
        expect("real calibration batch: the grader prompt carries the two-paragraph opening and the corrective heading",
               "the first two paragraphs of the answer's body" in scripts and "itself says the belief is wrong" in scripts)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--calibration", nargs="?", const="", default=None, metavar="BATCH")
    ap.add_argument("--pass", dest="pass_n", type=int, choices=(1, 2))
    ap.add_argument("--baseline-text", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validity", default=None, help="default: ..\\validity-tuning-<pass>.json (validity5.py --tuning N)")
    ap.add_argument("--validity1", default=None, help="pass 1's report when checking pass 2; default ..\\validity-tuning-1.json")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--base4", default=T.B4)
    ap.add_argument("--base5", default=T.B5)
    ap.add_argument("--inst", default=T.INST)
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    real = (a.base4, a.base5, a.inst) == (T.B4, T.B5, T.INST)
    ctx = Ctx(a.base4, a.base5, a.inst, real=real)
    if a.baseline_text:
        sys.exit(run_baseline_text(ctx))
    if a.calibration is not None:
        sys.exit(run_calibration(ctx, a.calibration or None, a.no_write))
    if a.pass_n:
        v = a.validity or os.path.join(a.base5, "validity-tuning-%d.json" % a.pass_n)
        v1 = a.validity1 or (v if a.pass_n == 1 else os.path.join(a.base5, "validity-tuning-1.json"))
        sys.exit(run_pass(ctx, a.pass_n, v, v1, a.no_write))
    ap.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
