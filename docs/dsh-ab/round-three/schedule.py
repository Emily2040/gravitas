"""Write the round-three run schedule: one triplet (the three arms) per prompt x round,
triplet order and arm order shuffled with a fixed seed (criteria.md, amendments).

    python schedule.py   -> schedule.txt, one "arm case round" line per run, triplets adjacent
"""
import glob
import os
import random

B = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(20261022)
cases = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(B, "prompts", "*.txt")))
assert len(cases) == 10
triplets = [(c, r) for c in cases for r in ("1", "2")]
rng.shuffle(triplets)
lines = []
for case, rnd in triplets:
    arms = ["gv-plain", "gv-grav", "gv-grav-nocheck"]
    rng.shuffle(arms)
    lines += ["%s %s %s" % (a, case, rnd) for a in arms]
with open(os.path.join(B, "schedule.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")
print("%d runs in %d triplets" % (len(lines), len(triplets)))
