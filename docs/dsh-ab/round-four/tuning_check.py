"""Compare the change-4 tuning runs (round-three prompts) with round three's answers to the same prompts.

    python tuning_check.py   -> prints, per prompt, chars for c4 (tuning) vs round-three plain, base (check off), Gravitas

Tuning only: these prompts are not held out, so this decides nothing about the verdict. It checks that the
candidate is shorter without dropping the premise correction before the held-out runs.
"""
import glob
import os
import statistics as st

B = os.path.dirname(os.path.abspath(__file__))
R3 = os.path.join(B, "..", "gravitas-dsh-ab3", "raw")
rows = []
for f in sorted(glob.glob(os.path.join(B, "tuning", "*.gv-grav-c4.r1.txt"))):
    case = os.path.basename(f).split(".")[0]
    c4 = len(open(f, encoding="utf-8").read())
    ref = {arm: len(open(os.path.join(R3, "%s.%s.r1.txt" % (case, arm)), encoding="utf-8").read())
           for arm in ("gv-plain", "gv-grav-nocheck", "gv-grav")}
    rows.append((case, c4, ref))
    print("%-22s c4 %5d | plain %5d (ratio %.2f) | check-off %5d | check-on %5d" % (
        case, c4, ref["gv-plain"], c4 / ref["gv-plain"], ref["gv-grav-nocheck"], ref["gv-grav"]))
if rows:
    print("median ratio c4/plain %.2f; median ratio check-off/plain %.2f" % (
        st.median(r[1] / r[2]["gv-plain"] for r in rows), st.median(r[2]["gv-grav-nocheck"] / r[2]["gv-plain"] for r in rows)))
