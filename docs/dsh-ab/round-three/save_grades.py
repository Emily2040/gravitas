"""Save blind grades returned by the grading workflow, and check that every pair has both.

    python save_grades.py <workflow-output-file> [...]   -> blind/grades/<grader>/<pid>.json

The workflow returns a JSON array of {"pid", "grader", "grade"}. Grades are validated against the
grader prompt's format (scores integers 0-10, winner and margin in their sets, one key-point mark per
point of the case). Prints every pair that is missing or malformed; exit 1 if any.
"""
import json
import os
import sys

B = os.path.dirname(os.path.abspath(__file__))
GRADERS = ("opus", "sonnet")
m = json.load(open(os.path.join(B, "blind-map.json"), encoding="utf-8"))


def results(path):
    data = json.load(open(path, encoding="utf-8"))  # the workflow output: {"summary", ..., "result": [...]}
    return data["result"] if isinstance(data, dict) else data


def problems(pid, g):
    pts = [p["id"] for p in json.load(open(os.path.join(B, "keypoints", m[pid]["case"] + ".json"), encoding="utf-8"))]
    out = []
    if g.get("pair") != pid:
        out.append("pair id %r" % g.get("pair"))
    if g.get("winner") not in ("A", "B", "tie"):
        out.append("winner")
    if g.get("margin") not in ("slight", "clear", "decisive"):
        out.append("margin")
    for side in "AB":
        s = g.get(side) or {}
        for d in ("correct", "trap", "honest", "useful", "concise"):
            if not isinstance(s.get(d), int) or not 0 <= s[d] <= 10:
                out.append("%s.%s" % (side, d))
        if not isinstance(s.get("added_claim_errors"), list):
            out.append("%s.added_claim_errors" % side)
        kp = s.get("key_points") or {}
        if sorted(kp) != sorted(pts) or any(v not in ("correct", "vague", "wrong", "missing") for v in kp.values()):
            out.append("%s.key_points" % side)
    return out


for path in sys.argv[1:]:
    for r in results(path):
        if not r or not r.get("grade"):
            continue
        d = os.path.join(B, "blind", "grades", r["grader"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, r["pid"] + ".json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(r["grade"], fh, ensure_ascii=False, indent=1)

bad = []
for pid in sorted(m):
    for gr in GRADERS:
        p = os.path.join(B, "blind", "grades", gr, pid + ".json")
        if not os.path.exists(p):
            bad.append((pid, gr, "missing"))
            continue
        pr = problems(pid, json.load(open(p, encoding="utf-8")))
        if pr:
            bad.append((pid, gr, ", ".join(pr)))
for pid, gr, why in bad:
    print("%s %s: %s" % (pid, gr, why))
print("%d pairs x %d graders, %d missing or malformed" % (len(m), len(GRADERS), len(bad)))
sys.exit(1 if bad else 0)
