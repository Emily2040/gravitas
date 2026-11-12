"""Collect every added-claim note from the grades and every item the check listed, for blind labelling.

    python build_notes.py   -> claim-notes.json, relabel-batches.json, listed-batches.json

claim-notes.json: [{"id", "pid", "side", "grader", "note"}], one row per added_claim_errors entry.
relabel-batches.json: per case, the key and the notes (id and text only, shuffled across sides,
sets and graders), so a relabeller sees no side.
listed-batches.json: per case, the key and every item the check listed in a steered draft, each with
the draft sentence around it (no outcome shown), for a right / wrong / unverified label.
"""
import glob
import json
import os
import random
import re

B = os.path.dirname(os.path.abspath(__file__))
m = json.load(open(os.path.join(B, "blind-map.json"), encoding="utf-8"))
rows = []
for gr in ("opus", "sonnet"):
    for p in sorted(glob.glob(os.path.join(B, "blind", "grades", gr, "*.json"))):
        g = json.load(open(p, encoding="utf-8"))
        pid = os.path.basename(p)[:-5]
        for side in "AB":
            for note in g[side].get("added_claim_errors") or []:
                rows.append({"pid": pid, "side": side, "grader": gr, "note": note})
rng = random.Random(20261022 + 333)
rng.shuffle(rows)
for i, r in enumerate(rows):
    r["id"] = i
with open(os.path.join(B, "claim-notes.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(rows, fh, ensure_ascii=False, indent=1)

key = lambda case: open(os.path.join(B, "keys", case + ".md"), encoding="utf-8").read().strip()
batches = {}
for r in rows:
    batches.setdefault(m[r["pid"]]["case"], []).append({"id": r["id"], "note": r["note"]})
with open(os.path.join(B, "relabel-batches.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump([{"case": c, "key": key(c), "notes": n} for c, n in sorted(batches.items())], fh, ensure_ascii=False, indent=1)

listed = {}
for log in sorted(glob.glob(os.path.join(B, "raw", "*.gv-grav.r?.claims.jsonl"))):
    case, _, rnd = os.path.basename(log).split(".")[:3]
    for rec in (json.loads(l) for l in open(log, encoding="utf-8") if l.strip()):
        if rec["phase"] != "draft" or not rec["steered"]:
            continue
        text = rec["text"]
        for it in rec["flagged"]:
            i = text.find(it["raw"])
            ctx = text[max(0, i - 80): i + len(it["raw"]) + 80] if i >= 0 else ""
            listed.setdefault(case, []).append({"round": rnd, "raw": it["raw"], "cls": it["cls"], "context": re.sub(r"\s+", " ", ctx)})
out = []
for case, items in sorted(listed.items()):
    for j, it in enumerate(items):
        it["n"] = j
    out.append({"case": case, "key": key(case), "items": items})
with open(os.path.join(B, "listed-batches.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("%d notes in %d cases; %d listed items in %d cases" % (len(rows), len(batches), sum(len(b["items"]) for b in out), len(out)))
