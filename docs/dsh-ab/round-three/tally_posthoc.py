"""Recount round three's figures that verdict.py does not print, from the files in this folder.

    python tally_posthoc.py [--events DIR]

DIR holds the runs' NDJSON event streams (<case>.<arm>.<round>.ndjson). They are not in the repo, because they
carry fetched web pages; on my machine they are in W:\AgentData\logs\gravitas-dsh-ab3aw. Without them the
web-page and source-claim figures are printed as not measurable, never counted.

- attr: Gravitas with the check (gv-grav) against the same without it (gv-grav-nocheck), from blind/grades.
- draft: each steered draft against its own revision, from blind/grades.
- post-hoc: Gravitas without the check against plain, from blind-map-posthoc.json and blind/posthoc-grades.
  Graded after the verdict and not pre-registered. Its added-claim notes were not relabelled, so the
  wrong-claim gate is not measured for it.
- g10 (sources claimed without opening a page) for the main set: how many runs qualified at all.
Hedge and source-claim patterns, the web-page rule and the sign test are imported from verdict.py.
"""
import json
import os
import statistics as st
from collections import Counter

import sys

import verdict as V

HERE = os.path.dirname(os.path.abspath(__file__))
EVENTS = sys.argv[sys.argv.index("--events") + 1] if "--events" in sys.argv else os.path.join(HERE, "raw")
DIMS = ("correct", "trap", "honest", "useful", "concise")


def grades(map_file, grade_dir, set_name):
    m = json.load(open(os.path.join(HERE, map_file), encoding="utf-8"))
    out = []
    for pid, e in sorted(m.items()):
        if e.get("set") != set_name:
            continue
        for g in V.GRADERS:
            path = os.path.join(HERE, "blind", grade_dir, g, pid + ".json")
            out.append((pid, e, g, json.load(open(path, encoding="utf-8"))))
    return out


def text(case, arm, rnd):
    return open(os.path.join(HERE, "raw", "%s.%s.%s.txt" % (case, arm, rnd)), encoding="utf-8").read()


def votes(rows, x, y):
    c, by_grader, by_lang, by_case = Counter(), {}, {}, {}
    for pid, e, g, gr in rows:
        w = "tie" if gr["winner"] == "tie" else e[gr["winner"]]
        c[w] += 1
        by_grader.setdefault(g, Counter())[w] += 1
        by_lang.setdefault(e["case"].split("-")[0], Counter())[w] += 1
        by_case.setdefault(e["case"], Counter())[w] += 1
    print("  votes: %s %d, %s %d, tie %d (sign test p = %.3f)" % (x, c[x], y, c[y], c["tie"], V.sign_test(c[x], c[y])))
    for g, cc in sorted(by_grader.items()):
        print("    %-6s %d-%d (tie %d)" % (g, cc[x], cc[y], cc["tie"]))
    for lang, cc in sorted(by_lang.items(), reverse=True):
        print("    %-6s %d-%d (tie %d)" % (lang, cc[x], cc[y], cc["tie"]))
    won = sum(1 for cc in by_case.values() if cc[x] > cc[y])
    lost = sum(1 for cc in by_case.values() if cc[x] < cc[y])
    print("    requests won/lost/even: %d/%d/%d" % (won, lost, len(by_case) - won - lost))
    return c


def per_answer(rows, x, y):
    sc = {x: [], y: []}
    kp = {x: Counter(), y: Counter()}
    trap = Counter()
    notes = Counter()
    for pid, e, g, gr in rows:
        for side in "AB":
            arm = e[side]
            sc[arm].append(gr[side])
            kp[arm].update(gr[side]["key_points"].values())
            trap[arm] += gr[side]["trap"] < 8
            notes[arm] += len(gr[side].get("added_claim_errors") or [])
    for arm in (x, y):
        tot = st.mean(sum(s[d] for d in DIMS) for s in sc[arm])
        print("  %-16s mean total %.2f/50, correct %.2f, useful %.2f | key points correct %d vague %d wrong %d missing %d"
              " | trap<8 %d of %d | added-claim notes %d (not relabelled)" % (
                  arm, tot, st.mean(s["correct"] for s in sc[arm]), st.mean(s["useful"] for s in sc[arm]),
                  kp[arm]["correct"], kp[arm]["vague"], kp[arm]["wrong"], kp[arm]["missing"], trap[arm], len(sc[arm]), notes[arm]))


def finals(rows, x, y):
    seen = {x: {}, y: {}}
    for pid, e, g, gr in rows:
        for side in "AB":
            rnd = e.get(side + "_round", e.get("round"))
            seen[e[side]][(e["case"], rnd)] = text(e["case"], e[side], rnd)
    return seen


def lengths(seen, x, y):
    for scope in ("all", "zh", "en"):
        pick = lambda arm: [len(t) for (case, r), t in seen[arm].items() if scope == "all" or case.startswith(scope + "-")]
        mx, my = st.median(pick(x)), st.median(pick(y))
        print("  median chars %-3s %s %.1f, %s %.1f, ratio %.3f" % (scope, x, mx, y, my, mx / my))
    under = sum(1 for k in seen[x] if len(seen[x][k]) < 0.6 * len(seen[y][k]))
    print("  pairs (same case and round) with %s under 0.6 of %s: %d of %d" % (x, y, under, len(seen[x])))


def hedging_and_sources(seen, x, y):
    for arm in (x, y):
        per1k = lambda pats, excl: st.mean(1000 * V.count_patterns(t, pats, excl) / max(1, len(t)) for t in seen[arm].values())
        events = {k: V.parse_ndjson(os.path.join(EVENTS, "%s.%s.%s.ndjson" % (k[0], arm, k[1])))[0] for k in seen[arm]}
        missing = sum(1 for ev in events.values() if not ev)
        if missing:
            web = "web pages: not measurable (%d of %d event streams missing; pass --events)" % (missing, len(events))
        else:
            no_web = [k for k, ev in events.items() if not V.web_opened(ev)]
            fab = sum(V.count_patterns(seen[arm][k], V.FAB, False) for k in no_web)
            web = "runs with no web page %d of %d, source-claim phrases in them %d" % (len(no_web), len(events), fab)
        print("  %-16s hedges per 1000 chars: round-one list %.3f, extended %.3f | %s" % (
            arm, per1k(V.H_ROUND1, True), per1k(V.H_EXTENDED, True), web))


if __name__ == "__main__":
    print("== attr: check on (gv-grav) against check off (gv-grav-nocheck), pre-registered")
    votes(grades("blind-map.json", "grades", "attr"), V.GRAV, V.NOCHECK)
    print("== draft: revision (gv-grav) against its own draft, pre-registered")
    votes(grades("blind-map.json", "grades", "draft"), V.GRAV, V.DRAFT)
    print("== post-hoc: check off (gv-grav-nocheck) against plain, graded after the verdict, not pre-registered")
    rows = grades("blind-map-posthoc.json", "posthoc-grades", "posthoc-nocheck-vs-plain")
    votes(rows, V.NOCHECK, V.PLAIN)
    per_answer(rows, V.NOCHECK, V.PLAIN)
    seen = finals(rows, V.NOCHECK, V.PLAIN)
    lengths(seen, V.NOCHECK, V.PLAIN)
    hedging_and_sources(seen, V.NOCHECK, V.PLAIN)
    print("== g10 on the main set: which runs could count at all")
    hedging_and_sources(finals(grades("blind-map.json", "grades", "main"), V.GRAV, V.PLAIN), V.GRAV, V.PLAIN)
