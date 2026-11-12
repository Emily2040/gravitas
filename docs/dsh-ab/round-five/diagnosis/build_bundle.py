"""Round five diagnosis: where gv-grav-base lost to gv-plain in round four (base set), unblinded, for designing the
next change. Writes wrong-claims.md, wrong-keypoints.md, hedges.md and summary.json beside this script.
Reads W:\\AgentData\\logs\\gravitas-dsh-ab4 only; changes nothing there."""
import collections
import importlib.util
import json
import os
import re

A4 = r"W:\AgentData\logs\gravitas-dsh-ab4"
OUT = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), os.path.join(A4, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V4 = load("verdict4")
VA = load("verdict4-amended")
J = lambda p: json.load(open(os.path.join(A4, p), encoding="utf-8"))
bm = J("blind-map.json")
notes = {n["id"]: n for n in J("claim-notes.json")}
lab = {r: {x["id"]: x for x in J("labels-%s.json" % r)} for r in ("opus", "sonnet")}
ARMS = ("gv-grav-base", "gv-plain")
base_pids = sorted(p for p, e in bm.items() if e["set"] == "base")

# 1. added claims both relabellers call wrong, per case and arm
wrong = collections.defaultdict(list)
unver = collections.Counter()
for nid, n in notes.items():
    e = bm[n["pid"]]
    if e["set"] != "base":
        continue
    arm = e[n["side"]]
    lo, ls = lab["opus"][nid], lab["sonnet"][nid]
    if lo["label"] == "wrong" and ls["label"] == "wrong":
        wrong[(e["case"], arm)].append((n["grader"], n["note"], lo["cite"] or ls["cite"]))
    if lo["label"] == "unverified" and ls["label"] == "unverified":
        unver[arm] += 1
cases = sorted({bm[p]["case"] for p in base_pids})
with open(os.path.join(OUT, "wrong-claims.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# Added claims both relabellers called wrong, round four base set (gv-grav-base vs gv-plain)\n\n")
    f.write("Each note is one judge's note on one answer; the same claim can appear up to three times (three judges).\n\n")
    for c in cases:
        f.write("## %s\n\n" % c)
        for arm in ARMS:
            rows = wrong[(c, arm)]
            f.write("### %s: %d notes\n\n" % (arm, len(rows)))
            for g, note, cite in rows:
                f.write("- [%s] %s\n  - relabeller cite: %s\n" % (g, note.replace("\n", " "), cite.replace("\n", " ")))
            f.write("\n")

# 2. key points marked wrong (and missing/vague counts), per case, arm and judge
kpw = collections.defaultdict(list)
kpcount = collections.Counter()
for p in base_pids:
    e = bm[p]
    kps = {k["id"]: k["point"] for k in json.load(open(os.path.join(A4, "keypoints", e["case"] + ".json"), encoding="utf-8"))}
    for judge in ("opus", "sonnet", "codex"):
        g = json.load(open(os.path.join(A4, "blind", "grades", judge, p + ".json"), encoding="utf-8"))
        for side in "AB":
            arm = e[side]
            for kid, mark in g[side]["key_points"].items():
                kpcount[(arm, mark)] += 1
                if mark == "wrong":
                    kpw[(e["case"], arm)].append((judge, e[side + "_round"] if e.get(side + "_round") else e["round"], kid, kps.get(kid, "?"), g["reasons"]))
with open(os.path.join(OUT, "wrong-keypoints.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# Key points a judge marked wrong, round four base set\n\n")
    for c in cases:
        f.write("## %s\n\n" % c)
        for arm in ARMS:
            rows = kpw[(c, arm)]
            f.write("### %s: %d marks\n\n" % (arm, len(rows)))
            for judge, rnd, kid, point, reasons in rows:
                f.write("- [%s, %s] point %s: %s\n  - judge's reasons for the pair: %s\n" % (judge, rnd, kid, point.replace("\n", " "), reasons.replace("\n", " ")))
            f.write("\n")

# 3. hedge markers (first and third lists) in every base and plain final, with context
hedge = collections.Counter()
with open(os.path.join(OUT, "hedges.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# Hedge markers in round four finals, first and third lists, with 30 characters either side\n\n")
    for c in cases:
        lang = c.split("-")[0]
        f.write("## %s\n\n" % c)
        for arm in ARMS:
            for r in ("r1", "r2"):
                t = open(os.path.join(A4, "raw", "%s.%s.%s.txt" % (c, arm, r)), encoding="utf-8").read()
                hits = []
                for which, pats in (("first", V4.HEDGE[lang]["first"]), ("third", VA.H3[lang])):
                    for pat in pats:
                        for m in re.finditer(pat, t, flags=re.I):
                            if lang == "zh" and m.group().startswith("可能") and m.start() > 0 and t[m.start() - 1] == "不":
                                continue
                            hits.append((which, t[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
                hedge[(arm, "first")] += sum(1 for h in hits if h[0] == "first")
                hedge[(arm, "third")] += sum(1 for h in hits if h[0] == "third")
                f.write("### %s %s (%d chars, %d markers)\n\n" % (arm, r, len(t), len(hits)))
                for which, ctx in hits:
                    f.write("- (%s) ...%s...\n" % (which, ctx))
                f.write("\n")

summary = {
    "wrong_added_claims_by_case": {c: {a: len(wrong[(c, a)]) for a in ARMS} for c in cases},
    "wrong_added_claims_total": {a: sum(len(wrong[(c, a)]) for c in cases) for a in ARMS},
    "unverified_by_both": dict(unver),
    "key_point_marks": {"%s %s" % k: v for k, v in sorted(kpcount.items())},
    "wrong_key_points_by_case": {c: {a: len(kpw[(c, a)]) for a in ARMS} for c in cases},
    "hedge_markers": {"%s %s" % k: v for k, v in sorted(hedge.items())},
}
json.dump(summary, open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
