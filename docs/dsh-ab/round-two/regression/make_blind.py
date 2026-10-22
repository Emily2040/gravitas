"""Regression packets: each round-one prompt, the branch rule on gv-grav (r1, r2) against the round-one
plain answer (gravitas-dsh-ab/raw/<case>.gv-plain.r1.txt), with the round-one key.

    python make_blind.py   -> blind/packets.md, blind-map.json

This is a regression check on prompts the rule was written to fix, not new evidence.
"""
import glob
import json
import os
import random

B = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.join(B, "..", "..", "gravitas-dsh-ab")
rng = random.Random(202610221)
cases = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(B, "prompts", "*.txt")))
blind_map, parts = {}, []
for rnd in ("r1", "r2"):
    for case in cases:
        texts = {
            "plain-round1": open(os.path.join(R1, "raw", "%s.gv-plain.r1.txt" % case), encoding="utf-8").read().strip(),
            "grav-branch": open(os.path.join(B, "raw", "%s.gv-grav.%s.txt" % (case, rnd)), encoding="utf-8").read().strip(),
        }
        for k, v in texts.items():
            if not v:
                raise SystemExit("empty answer: %s %s %s" % (case, rnd, k))
        order = ["plain-round1", "grav-branch"]
        rng.shuffle(order)
        pid = "%s.%s" % (case, rnd)
        blind_map[pid] = {"A": order[0], "B": order[1]}
        prompt = open(os.path.join(B, "prompts", case + ".txt"), encoding="utf-8").read().strip()
        key = open(os.path.join(B, "keys", case + ".md"), encoding="utf-8").read().strip()
        parts.append("\n\n".join([
            "# PAIR %s" % pid,
            "## Request\n\n````text\n%s\n````" % prompt,
            "## Answer key\n\n%s" % key,
            "## Answer A\n\n````text\n%s\n````" % texts[order[0]],
            "## Answer B\n\n````text\n%s\n````" % texts[order[1]],
        ]))
os.makedirs(os.path.join(B, "blind"), exist_ok=True)
with open(os.path.join(B, "blind", "packets.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n\n---\n\n".join(parts) + "\n")
with open(os.path.join(B, "blind-map.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(blind_map, fh, indent=1)
print("%d pairs" % len(blind_map))
