#!/usr/bin/env python3
"""Write round five's run schedules (standard library only).

    python dev/make_schedule5.py           write schedule.txt, schedule.seed.txt, tuning-schedule-1.txt and
                                           tuning-schedule-2.txt in the round-five folder
    python dev/make_schedule5.py --check   write nothing; exit 1 if a written file differs from what it would write

schedule.txt: the 72 held-out runs (12 cases x 3 arms x 2 rounds) as "arm case round" lines, in triplets: one case and
round per triplet, the three arms adjacent, as round four's schedule.txt. The triplet order is a seeded shuffle; the
arm order is rotated from triplet to triplet (a seeded starting order, shifted by one each triplet), so each arm runs
first, second and third in 8 triplets each. schedule.seed.txt holds the seed alone.
tuning-schedule-N.txt: gv-grav-c5 on round four's 12 prompts (W:\\AgentData\\logs\\gravitas-dsh-ab4\\prompts),
round N, pass N.

The held-out case names are the round-five design's list, written here; prompts/ of round five is not read.
"""
import os
import random
import sys

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R4_PROMPTS = os.path.join(os.path.dirname(B), "gravitas-dsh-ab4", "prompts")
SEED = 20261026
ARMS = ["gv-plain", "gv-grav-base", "gv-grav-c5"]
HELD_OUT = sorted([
    "en-debit-card-theft-liability", "en-gift-tax-down-payment", "en-uk-child-benefit-charge",
    "ja-child-allowance-income-cap", "ja-inheritance-registration", "ja-license-lapse",
    "ko-card-installment-defense", "ko-dependent-pension", "ko-duty-free-limit",
    "zh-contract-expiry-compensation", "zh-lease-sale", "zh-passport-remote-apply",
])
TUNING = sorted([
    "en-529-roth", "en-fsa-rollover", "en-medicare-part-b",
    "ja-medical-deduction", "ja-part-time-leave", "ja-wallpaper-restoration",
    "ko-jeonse-protection", "ko-severance-pay", "ko-unemployment-quit",
    "zh-flex-hours", "zh-insurance-gap", "zh-sick-pay",
])


def build():
    listed = sorted(f[:-4] for f in os.listdir(R4_PROMPTS) if f.endswith(".txt"))
    if listed != TUNING:
        raise SystemExit("round four's prompts/ is not the 12 tuning cases: %s" % listed)
    rng = random.Random(SEED)
    triplets = [(c, r) for c in HELD_OUT for r in ("1", "2")]
    rng.shuffle(triplets)
    start = ARMS[:]
    rng.shuffle(start)
    lines = []
    for i, (case, rnd) in enumerate(triplets):
        k = i % 3
        lines += ["%s %s %s" % (a, case, rnd) for a in start[k:] + start[:k]]
    files = {"schedule.txt": "\n".join(lines) + "\n", "schedule.seed.txt": "%d\n" % SEED}
    for n in ("1", "2"):
        files["tuning-schedule-%s.txt" % n] = "".join("gv-grav-c5 %s %s\n" % (c, n) for c in TUNING)
    # checks: 72 runs, every (arm, case, round) once, triplets of one case and round, each arm 8 times per position
    runs = [l.split() for l in lines]
    assert len(runs) == 72 and len({tuple(r) for r in runs}) == 72
    assert {(a, c, r) for a, c, r in runs} == {(a, c, r) for a in ARMS for c in HELD_OUT for r in ("1", "2")}
    for t in range(24):
        trip = runs[3 * t:3 * t + 3]
        assert len({(c, r) for _, c, r in trip}) == 1 and sorted(a for a, _, _ in trip) == sorted(ARMS)
    for pos in range(3):
        for a in ARMS:
            assert sum(1 for t in range(24) if runs[3 * t + pos][0] == a) == 8
    return files


def main():
    files = build()
    if "--check" in sys.argv:
        bad = [p for p, t in files.items() if not os.path.exists(os.path.join(B, p))
               or open(os.path.join(B, p), encoding="utf-8", newline="").read() != t]
        print("differ or missing: %s" % (bad or "none"))
        return 1 if bad else 0
    for p, t in files.items():
        with open(os.path.join(B, p), "w", encoding="utf-8", newline="\n") as f:
            f.write(t)
        print("wrote %s (%d lines)" % (p, t.count("\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
