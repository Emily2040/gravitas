"""Build blind packets for round two: one pair per case per round (r1 vs r1, r2 vs r2).

    python make_blind.py        -> blind/packets.md, blind/blind-map.json

A/B order is random per pair (seeded so it can be rebuilt); the map stays out of the packets.
"""
import glob
import json
import os
import random

B = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(20261022)
cases = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(B, "prompts", "*.txt")))
blind_map, parts = {}, []
for rnd in ("r1", "r2"):
    for case in cases:
        texts = {}
        for side in ("gv-plain", "gv-grav"):
            p = os.path.join(B, "raw", "%s.%s.%s.txt" % (case, side, rnd))
            texts[side] = open(p, encoding="utf-8").read().strip()
            if not texts[side]:
                raise SystemExit("empty answer: " + p)
        order = ["gv-plain", "gv-grav"]
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
SEP = "\n\n======== END OF PAIR ========\n\n"
with open(os.path.join(B, "blind", "packets.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(SEP.join(parts) + "\n")
# One file per round, built from the pair list, never by splitting text (answers contain "---").
for rnd in ("r1", "r2"):
    mine = [p for p in parts if p.split("\n", 1)[0].endswith("." + rnd)]
    with open(os.path.join(B, "blind", "packets-%s.md" % rnd), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(SEP.join(mine) + "\n")
with open(os.path.join(B, "blind-map.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(blind_map, fh, indent=1)
print("%d pairs" % len(blind_map))
