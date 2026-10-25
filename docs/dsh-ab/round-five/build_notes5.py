"""Collect every added-claim note from all three judges' grades, for blind relabelling.

    python build_notes5.py   -> claim-notes.json, relabel-batches.json

claim-notes.json: [{"id", "pid", "side", "grader", "note"}], one row per added_claim_errors entry of every grade
in blind/grades/{opus,sonnet,codex}, every set (main, base, attr, aa-plain, aa-c5), so no set the verdict reads
can be short of labels.
relabel-batches.json: per case, the key and the notes (id and text only), shuffled across sides, sets and judges,
in batches of at most 60, so a relabeller never sees a side, an arm or a judge.
Exit 1 if any pair in blind-map.json lacks a grade from any judge (relabel only once grading is complete).
"""
import json
import os
import random
import sys

B = os.path.dirname(os.path.abspath(__file__))
JUDGES = ("opus", "sonnet", "codex")
BATCH = 60
m = json.load(open(os.path.join(B, "blind-map.json"), encoding="utf-8"))
rows, missing = [], []
for gr in JUDGES:
    for pid in sorted(m):
        p = os.path.join(B, "blind", "grades", gr, pid + ".json")
        if not os.path.exists(p):
            missing.append("%s %s" % (gr, pid))
            continue
        g = json.load(open(p, encoding="utf-8"))
        for side in "AB":
            for note in g[side].get("added_claim_errors") or []:
                rows.append({"pid": pid, "side": side, "grader": gr, "note": note})
if missing:
    print("grades missing, not building notes: %d (first %s)" % (len(missing), missing[:5]))
    sys.exit(1)
rng = random.Random(20261024 + 444)
rng.shuffle(rows)
for i, r in enumerate(rows):
    r["id"] = i
with open(os.path.join(B, "claim-notes.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(rows, fh, ensure_ascii=False, indent=1)

key = lambda case: open(os.path.join(B, "keys", case + ".md"), encoding="utf-8").read().strip()
by_case = {}
for r in rows:
    by_case.setdefault(m[r["pid"]]["case"], []).append({"id": r["id"], "note": r["note"]})
batches = []
for case, notes in sorted(by_case.items()):
    for j in range(0, len(notes), BATCH):
        batches.append({"file": "relabel-%s-%02d" % (case, j // BATCH), "case": case, "key": key(case), "notes": notes[j:j + BATCH]})
with open(os.path.join(B, "relabel-batches.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(batches, fh, ensure_ascii=False, indent=1)
print("%d notes from %d grades in %d cases, %d batches" % (len(rows), len(m) * len(JUDGES), len(by_case), len(batches)))
