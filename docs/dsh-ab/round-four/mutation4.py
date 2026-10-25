#!/usr/bin/env python3
"""Mutation test of the round-four grading suite: verdict4.py (frozen), verdict4-amended.py, and the integrity tools
save_grades4.py, save_labels4.py and make_pairs4.py.

    python mutation4.py                 run every mutant, write mutation/mutation-report.txt next to this script
    python mutation4.py --jobs 8        mutants run in parallel (default 8)
    python mutation4.py --only A07,V05  run only these mutants (the report then says it is partial)

Each mutant is one deliberate breakage, applied to a copy of the script in its own temporary folder (beside unmodified
copies of verdict4.py, verdict4-amended.py and grader-prompt4.md); the copy's own --selftest is run there. A mutant is
KILLED when the self-test exits non-zero (an assertion failed, the script crashed or timed out), and SURVIVES when the
self-test still passes. A mutant that removes a fix is the evidence that the fix's self-test fails without it. The
unmutated scripts are run the same way first and must pass. The original files are never written: their sha256 is
checked before and after. Every survivor must have an explanation in EXPLAIN below, or this script exits 1.
Standard library only.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = "verdict4.py"
AMENDED = "verdict4-amended.py"
COPIED = (FROZEN, AMENDED, "grader-prompt4.md")
FROZEN_SHA256 = "11cdd365b88df9e20a38ad2514ba50a1e3baac6feea796c1f3220429826792ca"

# (id, what the breakage does, exact text in the original, replacement, expected number of occurrences)
V4_MUTANTS = [
    ("V01", "drop a grader: sonnet's votes are ignored",
     'GRADERS = ("opus", "sonnet")', 'GRADERS = ("opus",)', 1),
    ("V02", "gate 1: net equal to the noise floor passes (> becomes >=)",
     '"> %d" % floor, net > floor)', '"> %d" % floor, net >= floor)', 1),
    ("V03", "gate 1: noise floor from aa-c4 only",
     "floor = max(abs(v) for v in nets.values())", 'floor = abs(nets["aa-c4"])', 1),
    ("V04", "gate 2: a grader with as many losses as wins passes",
     '"wins > losses", w > l)', '"wins > losses", w >= l)', 1),
    ("V05", "gate 3: median ratio up to 1.10 passes",
     'check(c, "median chars ratio <= 1.00", fmt(rt), "<= 1.00", rt <= 1)',
     'check(c, "median chars ratio <= 1.00", fmt(rt), "<= 1.00", rt <= Fraction(11, 10))', 1),
    ("V06", "gate 3: short pairs are those under 0.5, not 0.6",
     "under = sorted(k for k, v in pr.items() if v < Fraction(6, 10))",
     "under = sorted(k for k, v in pr.items() if v < Fraction(5, 10))", 1),
    ("V07", "gate 3: up to 20% short pairs allowed",
     "Fraction(len(under), len(pr)) <= Fraction(1, 10))", "Fraction(len(under), len(pr)) <= Fraction(2, 10))", 1),
    ("V08", "gate 4: flip 'no more than' into 'fewer than'",
     'cnt[x]["vague"] <= cnt[y]["vague"])', 'cnt[x]["vague"] < cnt[y]["vague"])', 1),
    ("V09", "gate 5: one relabeller saying wrong is enough (all -> any)",
     'if all(v == "wrong" for v in labs):', 'if any(v == "wrong" for v in labs):', 1),
    ("V10", "gate 5: a 'wrong' label without a cite is accepted",
     'elif lab == "wrong" and not (isinstance(cite, str) and cite.strip()):', "elif False:", 1),
    ("V11", "gate 6: flip the correct comparison",
     'cnt[x]["correct"] >= cnt[y]["correct"])', 'cnt[x]["correct"] <= cnt[y]["correct"])', 1),
    ("V12", "gate 7: trap threshold 6 instead of 8",
     'low = {a: sum(g["scores"]["trap"] < 8 for g in ans[a]) for a in ans}',
     'low = {a: sum(g["scores"]["trap"] < 6 for g in ans[a]) for a in ans}', 1),
    ("V13", "gate 8: second list allowed 1.20 x plain",
     'm["second"][x] <= Fraction(11, 10) * m["second"][y])', 'm["second"][x] <= Fraction(12, 10) * m["second"][y])', 1),
    ("V14", "gate 8: first-list check removed",
     'm["first"][x] <= m["first"][y])', "True)", 1),
    ("V15", "a missing metric is defaulted to passing",
     '        c["status"], c["kind"] = "FAIL", "missing"', '        c["status"], c["kind"] = "PASS", "pass"', 1),
    ("V16", "a cell with nothing measured passes",
     'c["status"], c["kind"], c["reason"] = "FAIL", "missing", "metric missing: nothing was measured"',
     'c["status"], c["kind"], c["reason"] = "PASS", "pass", "nothing was measured"', 1),
    ("V17", "a missing main-set grade is dropped silently",
     'missing.append("blind/grades/%s/%s.json (%s %s %s): %s" % (g, pid, s, c, r, err))', "pass", 1),
    ("V18", "swap the arms of the main comparison",
     'CMP_MAIN = {"key": "main", "set": "main", "x": C4, "y": PLAIN,',
     'CMP_MAIN = {"key": "main", "set": "main", "x": PLAIN, "y": C4,', 1),
    ("V19", "the verdict is read from the base table",
     'failing = [c["id"] for c in tables["main"]["cells"] if c["status"] != "PASS"]',
     'failing = [c["id"] for c in tables["base"]["cells"] if c["status"] != "PASS"]', 1),
    ("V20", "hedging: 'May' as a date is counted as a hedge",
     'if "en" in excl and text.startswith("May", s) and MAY_DATE.match(text, s):', "if False:", 1),
    ("V21", "improvement: attr net equal to the floor counts",
     '"bound": "> %d" % floor, "ok": a["net"] > floor}]', '"bound": "> %d" % floor, "ok": a["net"] >= floor}]', 1),
    ("V22", "a grade whose key-point ids differ from the case's is accepted",
     "if len(kp2) != len(kp) or set(kp2) != set(kp_ids):", "if False:", 1),
    ("V23", "a duplicated pair in blind-map is accepted",
     "                p = pidx[s].get((c, r), [])\n                if len(p) != 1:",
     "                p = pidx[s].get((c, r), [])\n                if len(p) < 1:", 1),
    ("V24", "Japanese finals are counted with the Chinese first list",
     '"ja": {"first": [literal(w) for w in H1_JA_WORDS]', '"ja": {"first": H1_ZH', 1),
    ("V25", "hedging: 不可能 is counted as 可能",
     'if "zh" in excl and m.group().startswith("可能") and s > 0 and text[s - 1] == "不":', "if False:", 1),
    ("V26", "the A/A noise floor uses one grader",
     '        for g in GRADERS:\n            gr, err = D.grades.get((g, pid), (None, "missing"))\n            if err:\n'
     '                missing.append("blind/grades/%s/%s.json (%s %s): %s" % (g, pid, s, c, err))',
     '        for g in GRADERS[:1]:\n            gr, err = D.grades.get((g, pid), (None, "missing"))\n            if err:\n'
     '                missing.append("blind/grades/%s/%s.json (%s %s): %s" % (g, pid, s, c, err))', 1),
    ("V27", "gate 5: claim-notes coverage is not checked",
     "    if expected != actual:", "    if False:", 1),
]

AM_MUTANTS = [
    ("A01", "drop a judge: codex's votes are ignored everywhere",
     'JUDGES = ("opus", "sonnet", "codex")', 'JUDGES = ("opus", "sonnet")', 1),
    ("A02", "gate 1: the sqrt(2) scaling of the noise floor removed (2026-10-25)",
     'check(c, "net votes > sqrt(2) x A/A noise floor", "%+d" % net, "> %.3f" % scaled, sqrt2_above(net, floor))',
     'check(c, "net votes > sqrt(2) x A/A noise floor", "%+d" % net, "> %.3f" % scaled, net > floor)', 1),
    ("A03", "gate 1: noise floor from aa-c4 only",
     "floor = max(abs(nets[a]) for a in FLOOR_SETS)", 'floor = abs(nets["aa-c4"])', 1),
    ("A04", "gate 1: the 'net > 0' check removed",
     'check(c, "net votes > 0", "%+d" % net, "> 0", net > 0)', "pass", 1),
    ("A05", "gate 2: a judge with as many losses as wins passes",
     '"wins > losses", w > l)', '"wins > losses", w >= l)', 1),
    ("A06", "gate 2: codex is not checked on its own",
     '    for j in D.judges:\n        vs = [v for v in votes if v["judge"] == j]',
     '    for j in D.judges[:2]:\n        vs = [v for v in votes if v["judge"] == j]', 1),
    ("A07", "gate 3: the pooled 0.70 floor removed",
     "rt >= LENGTH_FLOOR)", "True)", 1),
    ("A08", "gate 3: floor lowered to 0.60",
     "LENGTH_FLOOR = Fraction(7, 10)", "LENGTH_FLOOR = Fraction(6, 10)", 1),
    ("A09", "gate 3: ratio up to 1.10 passes",
     "LENGTH_CEIL = Fraction(1)", "LENGTH_CEIL = Fraction(11, 10)", 1),
    ("A10", "gate 3: up to 20% short pairs allowed",
     "PAIR_SHORT_SHARE = Fraction(1, 10)", "PAIR_SHORT_SHARE = Fraction(2, 10)", 1),
    ("A11", "gate 3: short pairs are those under 0.5, not 0.6",
     "PAIR_SHORT = Fraction(6, 10)", "PAIR_SHORT = Fraction(5, 10)", 1),
    ("A12", "gate 4: flip the vague comparison",
     'cnt[x]["vague"] <= cnt[y]["vague"])', 'cnt[x]["vague"] >= cnt[y]["vague"])', 1),
    ("A13", "gate 5: one relabeller saying wrong is enough (all -> any)",
     'if all(v == "wrong" for v in labs):', 'if any(v == "wrong" for v in labs):', 1),
    ("A14", "gate 5: only sonnet relabels",
     'RELABELLERS = ("sonnet", "opus")', 'RELABELLERS = ("sonnet",)', 1),
    ("A15", "gate 6: flip the correct comparison",
     'cnt[x]["correct"] >= cnt[y]["correct"])', 'cnt[x]["correct"] <= cnt[y]["correct"])', 1),
    ("A16", "gate 6: the wrong-key-points check removed",
     'check(c, "wrong %s <= %s" % (x, y), cnt[x]["wrong"], "<= %d" % cnt[y]["wrong"], cnt[x]["wrong"] <= cnt[y]["wrong"])',
     "pass", 1),
    ("A17", "gate 7: trap threshold 6 instead of 8",
     'low = {a: sum(g["scores"]["trap"] < 8 for g in ans[a]) for a in ans}',
     'low = {a: sum(g["scores"]["trap"] < 6 for g in ans[a]) for a in ans}', 1),
    ("A18", "gate 8: second list allowed 1.20 x plain",
     "SECOND_LIST = Fraction(11, 10)", "SECOND_LIST = Fraction(12, 10)", 1),
    ("A19", "gate 8: first-list check removed",
     'm["first"][x] <= m["first"][y])', "True)", 1),
    ("A20", "gate 9: as many requests negative as positive passes",
     '"positive > negative", pos > neg)', '"positive > negative", pos >= neg)', 1),
    ("A21", "gate 9: vote-level net instead of the request as the unit",
     '"positive > negative", pos > neg)', '"positive > negative", sum(nets.values()) > 0)', 1),
    ("A22", "gate 10: correct and useful may fall 1.0 below plain",
     "HALF = Fraction(1, 2)", "HALF = Fraction(1)", 1),
    ("A23", "gate 10: the useful check removed",
     '    for d in ("correct", "useful"):\n        check(c, "mean %s %s >= %s - 0.5"',
     '    for d in ("correct",):\n        check(c, "mean %s %s >= %s - 0.5"', 1),
    ("A24", "gate 10: the mean-total check removed",
     'm[x]["total"] >= m[y]["total"])', "True)", 1),
    ("A25", "gate 11: citations excuse a phrase from 60 characters away, not 25",
     "EXCUSE_GAP = 25", "EXCUSE_GAP = 60", 1),
    ("A26", "gate 11: an opened host excuses phrases whatever the HTTP status",
     'if not m or not m.group(2).startswith("2"):', "if not m:", 1),
    ("A27", "gate 11: a web_search counts as opening a page",
     'or calls.get(e.get("callId")) != "web_fetch":', 'or calls.get(e.get("callId")) not in ("web_fetch", "web_search"):', 1),
    ("A28", "gate 11: the old rule, phrases counted only in runs that opened no page",
     "                fa = fab_analysis(texts[(k, a, r)], hosts[(k, a, r)])",
     "                fa = fab_analysis(texts[(k, a, r)], hosts[(k, a, r)]) if not hosts[(k, a, r)] else "
     "dict(phrases=0, cite_excused=0, host_excused=0, unexcused=0, hosts_named=[])", 1),
    ("A29", "gate 11: a missing event stream is taken as 'no page opened'",
     '                    missing.append("raw/%s.%s.%s.ndjson %s" % (k, a, r, err))',
     "                    hosts[(k, a, r)] = set()", 1),
    ("A30", "gate 11: the Japanese phrases dropped",
     "FAB_ALL = FAB_ZH_EN + FAB_JA + FAB_KO", "FAB_ALL = FAB_ZH_EN + FAB_KO", 1),
    ("A31", "a missing metric is defaulted to passing",
     '        c["status"], c["kind"] = "FAIL", "missing"\n        c["reason"] = "metric missing: " + summarize(missing)',
     '        c["status"], c["kind"] = "PASS", "pass"\n        c["reason"] = "metric missing: " + summarize(missing)', 1),
    ("A32", "a cell with nothing measured passes",
     'c["status"], c["kind"], c["reason"] = "FAIL", "missing", "metric missing: nothing was measured"',
     'c["status"], c["kind"], c["reason"] = "PASS", "pass", "nothing was measured"', 1),
    ("A33", "swap the arms of the main comparison",
     'CMP_MAIN = {"key": "main", "set": "main", "x": C4, "y": PLAIN,',
     'CMP_MAIN = {"key": "main", "set": "main", "x": PLAIN, "y": C4,', 1),
    ("A34", "gate 12: unverifiable claims allowed 1.20 x plain",
     "UNVERIFIED_RATIO = Fraction(11, 10)", "UNVERIFIED_RATIO = Fraction(12, 10)", 1),
    ("A35", "the round is a win if either version wins",
     'round_win = frozen["verdict"] == "win" and res["verdict"] == "win"',
     'round_win = frozen["verdict"] == "win" or res["verdict"] == "win"', 1),
    ("A36", "the frozen view keeps codex's claim-notes rows",
     'kept = [r for r in j if not (isinstance(r, dict) and r.get("grader") == "codex")]', "kept = list(j)", 1),
    ("A37", "the frozen script's sha256 is not checked",
     "    elif sha != FROZEN_SHA256:", "    elif False:", 1),
    ("A38", "a missing main-set grade is dropped silently",
     'missing.append("blind/grades/%s/%s.json (%s %s %s): %s" % (j, pid, s, c, r, err))', "pass", 1),
    ("A39", "the A/A noise floor uses two judges",
     '        for j in D.judges:\n            gr, err = D.grades.get((j, pid), (None, "missing"))\n            if err:\n'
     '                missing.append("blind/grades/%s/%s.json (%s %s): %s"',
     '        for j in D.judges[:2]:\n            gr, err = D.grades.get((j, pid), (None, "missing"))\n            if err:\n'
     '                missing.append("blind/grades/%s/%s.json (%s %s): %s"', 1),
    ("A40", "claim-notes rows from codex are rejected",
     'and side in ("A", "B") and grader in judges and', 'and side in ("A", "B") and grader in FROZEN_JUDGES and', 1),
    ("A41", "improvement: the attr floor without the sqrt(2) scaling",
     '"bound": "> %.3f" % (floor * 2 ** 0.5), "ok": sqrt2_above(a["net"], floor)}]',
     '"bound": "> %.3f" % (floor * 2 ** 0.5), "ok": a["net"] > floor}]', 1),
    ("A42", "improvement: c4 must pass more cells than base, not as many",
     '"bound": "c4 >= base", "ok": cp >= bp},', '"bound": "c4 >= base", "ok": cp > bp},', 1),
    ("A43", "improvement: missing metrics ignored",
     '    if miss:\n        yes, reasons = False,', '    if False:\n        yes, reasons = False,', 1),
    ("A44", "IMPROVEMENT is yes if either version says yes",
     'both_imp = frozen["improvement"] == "yes" and res["improvement"]["improvement"] == "yes"',
     'both_imp = frozen["improvement"] == "yes" or res["improvement"]["improvement"] == "yes"', 1),
    ("A45", "reported A/A vague floor ignores which side is r1",
     'd += n if v["entry"]["%s_round" % side] == "r1" else -n', "d += n", 1),
    ("A46", "gate 5: claim-notes coverage is not checked",
     "    if expected != actual:", "    if False:", 1),
    ("A47", "gate 11: the zh/en phrases dropped",
     "FAB_ALL = FAB_ZH_EN + FAB_JA + FAB_KO", "FAB_ALL = FAB_JA + FAB_KO", 1),
    ("A48", "a frozen-script crash is not caught (the round verdict is never printed)",
     "    except Exception as e:  # a crash of the frozen script is no verdict, so the round is not a win",
     "    except KeyError as e:", 1),
    ("A49", "gate 4: the missing-key-points check removed (2026-10-25)",
     'check(c, "missing %s <= %s" % (x, y), cnt[x]["missing"], "<= %d" % cnt[y]["missing"],\n'
     '          cnt[x]["missing"] <= cnt[y]["missing"])', "pass", 1),
    ("A50", "gate 3: the per-pair median floor removed (2026-10-25)",
     "pm >= LENGTH_FLOOR)", "True)", 1),
    ("A51", "gate 3: visible text not checked (2026-10-25)",
     'for view, fn in (("raw", lambda t: t), ("visible", visible_text)):', 'for view, fn in (("raw", lambda t: t),):', 1),
    ("A52", "visible text keeps list markers",
     '        s = LIST_LEAD.sub("", s)', "        s = s", 1),
    ("A53", "gate 8: the third list not gated overall (2026-10-25)",
     '    if scope == "overall":\n        check(c, "third list', '    if False:\n        check(c, "third list', 1),
    ("A54", "gate 8: the Japanese third list empty",
     '"ja": [V4.literal(w) for w in H3_JA_WORDS]', '"ja": []', 1),
    ("A55", "gate 12: counts wrong-by-both instead of unverified-by-both",
     'ux, uy = t["unver"][x], t["unver"][y]', 'ux, uy = t["wrong"][x], t["wrong"][y]', 1),
    ("A56", "integrity: a grade file is not compared with its ledger grade",
     '        if obj != ref.get("grade"):', "        if False:", 1),
    ("A57", "integrity: the last valid ledger grade is used, not the first",
     '                if s["ref"] is None:\n                    s["ref"] = e', '                s["ref"] = e', 1),
    ("A58", "integrity: a logged replace record is ignored",
     '            s["replaces"] += 1\n            s["ref"] = None', '            s["replaces"] += 1', 1),
    ("A59", "integrity: the packet's sha256 is not compared with the ledger",
     '        if ref.get("packet_sha256") != ps:', "        if False:", 1),
    ("A60", "integrity: the packaged answer's sha256 is not compared with raw/",
     "                elif text_sha256(t) != want:", "                elif False:", 1),
    ("A61", "integrity: validity.json may be older than the run files",
     "                       and os.path.getmtime(os.path.join(raw, f)) >= mt)",
     "                       and os.path.getmtime(os.path.join(raw, f)) >= mt + 1e9)", 1),
    ("A62", "integrity: runs listed under 'invalid' are ignored",
     '    if rep["invalid"]:', "    if False:", 1),
    ("A63", "integrity: a missing validity.json passes",
     'return ["validity.json missing (run validity4.py after the last run)"], None', "return [], None", 1),
    ("A64", "integrity: a label is not compared with its ledger label",
     '                elif (ref.get("label"), ref.get("cite") or "") != entries.get(rid):', "                elif False:", 1),
    ("A65", "integrity: a blank final's placeholder answer is not recognised",
     "    return (t if t else PLACEHOLDER), None", "    return t, None", 1),
    ("A66", "integrity: validity problems do not reach the text gates",
     "    if D.global_issues:\n        return None, integrity_missing(D)",
     "    if False:\n        return None, integrity_missing(D)", 1),
    ("A67", "reported: decisive votes counted to the longer answer",
     '        per[v["judge"]][0] += v["grade"]["winner"] == shorter', '        per[v["judge"]][0] += v["grade"]["winner"] != shorter', 1),
]

SG_MUTANTS = [
    ("S01", "route (a): a row's prompt is not compared with the frozen prompt",
     "    if prompt != expected:", "    if False:", 1),
    ("S02", "route (a): a row's packet path is not checked",
     "    if os.path.normcase(os.path.abspath(packet_path)) != want:", "    if False:", 1),
    ("S03", "route (b): the last valid ledger grade is used, not the first",
     '                        if s["ref"] is None:\n                            s["ref"] = e',
     '                        s["ref"] = e', 1),
    ("S04", "route (b): --replace does not log its replace record and reason",
     'R.append([{"kind": "replace", "time": now(), "pid": pid, "judge": grader, "reason": replace_reason}])', "pass", 1),
    ("S05", "route (b): invalid rows are not logged",
     '            R.append([entry])\n            slot["entries"] += 1',
     '            if entry["valid"]:\n                R.append([entry])\n            slot["entries"] += 1', 1),
    ("S06", "route (b): a grade file is not compared with its ledger grade",
     '    if ref.get("grade") != g:', "    if False:", 1),
    ("S07", "route (a): a codex session's prompt is not checked",
     "return [] if got == expected else", "return [] if True else", 1),
    ("S08", "route (b): the packet's sha256 is not compared with the ledger",
     '    if ref.get("packet_sha256") != R.packet_sha(pid) or R.packet_sha(pid) is None:', "    if False:", 1),
    ("S09", "route (b): a later different valid grade silently replaces the first",
     '            if ref is None:\n                slot["ref"] = entry', '            if True:\n                slot["ref"] = entry', 1),
    ("S10", "a lower-case winner is accepted",
     '    if g.get("winner") not in WINNERS:', '    if str(g.get("winner")).upper() not in ("A", "B", "TIE"):', 1),
]

SL_MUTANTS = [
    ("L01", "route (c): labels written although there are problems",
     "    if problems:\n        return problems, notes, False", "    if False:\n        return problems, notes, False", 1),
    ("L02", "route (c): two different labels for one id in the outputs are not flagged",
     "if k in seen and seen[k] != (lab, cite):", "if False:", 1),
    ("L03", "route (b): the last valid ledger label is used, not the first",
     "                if refs.get(k) is None:\n                    refs[k] = e", "                refs[k] = e", 1),
    ("L04", "route (c): an empty batch that nothing fills is not reported",
     '            problems.append("batch %s from %s returned nothing and no later output fills it" % key)',
     "            pass", 1),
    ("L05", "route (b): invalid labels are not logged",
     "    if entries:\n        append_ledger(base, entries)",
     '    if entries:\n        append_ledger(base, [e for e in entries if e["valid"]])', 1),
    ("L06", "a 'wrong' label without a cite is accepted",
     'elif lab == "wrong" and not str(cite).strip():', "elif False:", 1),
    ("L07", "a logged replace record is ignored",
     '            if e.get("kind") == "replace-label":\n                refs[(e.get("id"), e.get("relabeller"))] = None',
     '            if False:\n                refs[(e.get("id"), e.get("relabeller"))] = None', 1),
]

MP_MUTANTS = [
    ("M01", "route (d): the packaged answers' sha256 not stored",
     '"A_sha256": hashlib.sha256(A[2].encode("utf-8")).hexdigest(),', '"A_sha256": None,', 1),
    ("M02", "route (d): answers naming an arm or the harness are not refused",
     '        if m:\n            raise SystemExit("answer %s names an arm or the harness',
     '        if False:\n            raise SystemExit("answer %s names an arm or the harness', 1),
    ("M03", "route (d): the leak pattern misses AgentData and r4-",
     r'LEAK = re.compile(r"gv-(plain|grav)|gravitas-dsh|AgentData|\br4-")',
     r'LEAK = re.compile(r"gv-(plain|grav)|gravitas-dsh")', 1),
    ("M04", "route (d): a final blank after its rerun still stops the build",
     '            if "%s.%s.%s" % (case, arm, rnd) in reruns:\n                return PLACEHOLDER',
     '            if False:\n                return PLACEHOLDER', 1),
    ("M05", "a blank final that was never rerun is packaged as the placeholder",
     '            if "%s.%s.%s" % (case, arm, rnd) in reruns:\n                return PLACEHOLDER',
     '            if True:\n                return PLACEHOLDER', 1),
]

TARGETS = {FROZEN: V4_MUTANTS, AMENDED: AM_MUTANTS, "save_grades4.py": SG_MUTANTS, "save_labels4.py": SL_MUTANTS,
           "make_pairs4.py": MP_MUTANTS}

# Why each surviving mutant survives (a survivor without an entry fails this script).
EXPLAIN = {
    "V09": "Equivalent on every dataset the frozen self-test builds: its two relabellers always give the same "
           "label, so 'all say wrong' and 'any says wrong' select the same notes. verdict4-amended.py's self-test "
           "has the disagreeing case (e2e) and kills the same mutation there (A13); that scenario also checks that "
           "the unmodified verdict4.py, run on it, does not count a note one relabeller calls wrong. verdict4.py "
           "and its self-test are frozen and are not changed, so this survivor stays and is a known gap of its "
           "self-test.",
    "V12": "Not exercised by the frozen self-test: its answers have trap scores 6 or 9 only, so no answer lies "
           "between 6 and 8 and the two thresholds count the same answers. verdict4-amended.py's self-test has "
           "c4 at 7 against plain at 9 (e2d) and kills the same mutation (A17); in that scenario it also checks "
           "that the unmodified verdict4.py fails exactly gate 7 in every scope. verdict4.py and its self-test are "
           "frozen and are not changed, so this survivor stays and is a known gap of its self-test.",
    "V16": "Unreachable branch: every gate returns finish(c, missing) before adding checks, and adds at least one "
           "check otherwise, so no cell reaches finish() with no checks and nothing missing. It is a defensive "
           "default; the mutant changes no result.",
    "A04": "Equivalent: the noise floor is a maximum of absolute values, so it is never negative, and "
           "'net > sqrt(2) x floor' (which itself requires net > 0) already implies 'net > 0'. The check is kept "
           "because WIN_CRITERIA names both bounds.",
    "A32": "Unreachable branch, as V16: no gate calls finish() with no checks and nothing missing, so the "
           "defensive 'nothing was measured' default never runs.",
}


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_one(target, mutant, timeout):
    """Return a result dict. mutant None = the unmutated script."""
    tmp = tempfile.mkdtemp(prefix="mut4-")
    try:
        for name in set(COPIED) | {target}:
            shutil.copy2(os.path.join(HERE, name), os.path.join(tmp, name))
        path = os.path.join(tmp, target)
        if mutant:
            mid, title, old, new, count = mutant
            with open(path, encoding="utf-8") as f:
                src = f.read()
            n = src.count(old)
            if n != count:
                return {"id": mid, "error": "the text to mutate occurs %d times, expected %d" % (n, count)}
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(src.replace(old, new))
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        t0 = time.time()
        try:
            p = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"], cwd=tmp, env=env,
                               capture_output=True, timeout=timeout)
            code, out = p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")
        except subprocess.TimeoutExpired as e:
            code, out = "timeout", ((e.stdout or b"") + (e.stderr or b"")).decode("utf-8", "replace")
        secs = time.time() - t0
        lines = out.splitlines()
        bad = [ln for ln in lines if ln.startswith("[BAD]")]
        last = next((ln for ln in reversed(lines) if ln.startswith("selftest:")), None)
        tb = [ln for ln in lines if ln.startswith("Traceback") or ln.strip().startswith(("File ", "Error", "Exception"))]
        err_line = next((ln for ln in reversed(lines) if ln and not ln.startswith(("[ok]", "[BAD]", "selftest:"))), "")
        return {"id": mutant[0] if mutant else "baseline", "code": code, "secs": secs, "bad": bad, "last": last,
                "crash": (err_line if (tb or code == "timeout") and not bad else ""), "error": None}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=2400, help="seconds per self-test run")
    ap.add_argument("--only", default="", help="comma-separated mutant ids")
    ap.add_argument("--out", default=os.path.join(HERE, "mutation", "mutation-report.txt"))
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    sets = TARGETS
    watched = sorted(set(sets) | set(COPIED))
    before = {n: sha256(os.path.join(HERE, n)) for n in watched}
    started = datetime.datetime.now()
    rep = ["mutation test of the round-four grading suite (mutation4.py)",
           "started %s; python %s; %d parallel jobs; self-test timeout %d s" % (
               started.isoformat(timespec="seconds"), sys.version.split()[0], a.jobs, a.timeout),
           "originals (never written; sha256 checked before and after):"]
    rep += ["  %-22s %s%s" % (n, before[n], "  (the frozen sha256)" if n == FROZEN and before[n] == FROZEN_SHA256 else
                              "  (NOT the frozen sha256)" if n == FROZEN else "") for n in watched]
    rep.append("mutation4.py sha256 %s" % sha256(os.path.abspath(__file__)))
    if only:
        rep.append("PARTIAL RUN: only %s" % ", ".join(sorted(only)))
    rep.append("method: each mutant replaces one exact piece of text in a copy of the script (in its own temporary "
               "folder, beside unmodified copies of the other scripts) and runs the copy's --selftest; KILLED = the "
               "self-test exits non-zero, SURVIVED = it still passes. A killed mutant that removes a fix shows that the "
               "fix's self-test fails without it.")
    print("\n".join(rep))
    jobs = [(t, None) for t in sets] + [(t, m) for t, ms in sets.items() for m in ms if not only or m[0] in only]
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(run_one, t, m, a.timeout): (t, m) for t, m in jobs}
        for f in concurrent.futures.as_completed(futs):
            t, m = futs[f]
            r = f.result()
            results[(t, m[0] if m else "baseline")] = r
            print("  done %-20s %-8s code=%s %s" % (t, r["id"], r.get("code"), (r.get("last") or r.get("error") or "")),
                  flush=True)
    after = {n: sha256(os.path.join(HERE, n)) for n in watched}
    ok_all = True
    summary = []
    for t, ms in sets.items():
        b = results[(t, "baseline")]
        rep.append("")
        rep.append("=== %s (%d mutants)" % (t, len([m for m in ms if not only or m[0] in only])))
        rep.append("baseline (unmutated copy): exit %s, %s, %.0f s" % (b["code"], b["last"], b["secs"]))
        if b["code"] != 0:
            rep.append("BASELINE FAILS: the mutation results for this script mean nothing")
            ok_all = False
        killed, survived, invalid = [], [], []
        for m in ms:
            if only and m[0] not in only:
                continue
            r = results[(t, m[0])]
            if r.get("error"):
                invalid.append(m[0])
                rep.append("%s INVALID   %s: %s" % (m[0], m[1], r["error"]))
                continue
            if r["code"] != 0:
                killed.append(m[0])
                ev = r["bad"][0][6:] if r["bad"] else ("crash: " + r["crash"] if r["crash"] else "exit %s" % r["code"])
                rep.append("%s KILLED    %s" % (m[0], m[1]))
                rep.append("              %d assertion(s) failed; first: %s" % (len(r["bad"]), ev[:220]))
            else:
                survived.append(m[0])
                rep.append("%s SURVIVED  %s  (%s)" % (m[0], m[1], r["last"]))
                why = EXPLAIN.get(m[0])
                rep.append("              why: " + (why or "NO EXPLANATION RECORDED"))
                if not why:
                    ok_all = False
        n = len(killed) + len(survived)
        line = "summary %s: %d of %d mutants killed; survivors: %s%s" % (
            t, len(killed), n, ", ".join(survived) or "none",
            ("; invalid (text not found): " + ", ".join(invalid)) if invalid else "")
        rep.append(line)
        summary.append(line)
        if invalid:
            ok_all = False
    rep.append("")
    rep += summary
    for n in watched:
        same = before[n] == after[n]
        rep.append("original %s unchanged after the run: %s" % (n, "yes" if same else "NO"))
        ok_all &= same
    rep.append("finished %s (%.0f min)" % (datetime.datetime.now().isoformat(timespec="seconds"),
                                         (datetime.datetime.now() - started).total_seconds() / 60))
    rep.append("RESULT: %s" % ("every survivor explained, every baseline passes" if ok_all else "NOT CLEAN (see above)"))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rep) + "\n")
    print("\n".join(rep[rep.index("") if "" in rep else 0:]))
    print("report written to %s" % a.out)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
