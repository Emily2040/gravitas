"""Build round-three blind packets, one pair per file, from the pair list (never by splitting text).

    python make_pairs.py   -> blind/packets/<pid>.md, blind-map.json, raw/<case>.gv-grav-draft.<round>.txt

Sets (criteria.md, amendments):
  main      gv-plain vs gv-grav, per case and round          (20 pairs)
  attr      gv-grav-nocheck vs gv-grav, per case and round   (20 pairs)
  aa-plain  gv-plain r1 vs gv-plain r2, per case             (10 pairs, noise floor)
  aa-grav   gv-grav r1 vs gv-grav r2, per case               (10 pairs, noise floor)
  draft     the logged draft vs the final, per steered gv-grav run
A/B is balanced by design: within each case Gravitas (or the draft, or r1) is A in one pair and B in
the other, alternating by case. Pair ids are opaque (p001...), assigned in a seeded random order, so
neither the id nor the packet order shows the set or the arms. Every answer is checked to appear in
its packet exactly once and in full.
"""
import glob
import json
import os
import random

B = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(B, "raw")
cases = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(B, "prompts", "*.txt")))
assert len(cases) == 10, cases


def text(case, arm, rnd):
    p = os.path.join(RAW, "%s.%s.%s.txt" % (case, arm, rnd))
    t = open(p, encoding="utf-8").read().strip()
    if not t:
        raise SystemExit("empty answer: " + p)
    return t


# Drafts of steered runs, from the run-time claim log.
drafts = {}
for case in cases:
    for rnd in ("r1", "r2"):
        log = os.path.join(RAW, "%s.gv-grav.%s.claims.jsonl" % (case, rnd))
        if not os.path.exists(log):
            continue
        recs = [json.loads(l) for l in open(log, encoding="utf-8") if l.strip()]
        d = [r for r in recs if r.get("phase") == "draft" and r.get("steered")]
        if d:
            drafts[(case, rnd)] = d[0]["text"].strip()
            with open(os.path.join(RAW, "%s.gv-grav-draft.%s.txt" % (case, rnd)), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(drafts[(case, rnd)] + "\n")

pairs = []  # (set, case, round, (armA, roundA, textA), (armB, roundB, textB))
for i, case in enumerate(cases):
    for j, rnd in enumerate(("r1", "r2")):
        first = (i + j) % 2 == 0  # alternates by case and round, so each side is A in half the pairs
        for set_name, other in (("main", "gv-plain"), ("attr", "gv-grav-nocheck")):
            g = ("gv-grav", rnd, text(case, "gv-grav", rnd))
            o = (other, rnd, text(case, other, rnd))
            pairs.append((set_name, case, rnd) + ((g, o) if first else (o, g)))
        if (case, rnd) in drafts:
            d = ("gv-grav-draft", rnd, drafts[(case, rnd)])
            f = ("gv-grav", rnd, text(case, "gv-grav", rnd))
            pairs.append(("draft", case, rnd) + ((d, f) if first else (f, d)))
    for set_name, arm in (("aa-plain", "gv-plain"), ("aa-grav", "gv-grav")):
        a1 = (arm, "r1", text(case, arm, "r1"))
        a2 = (arm, "r2", text(case, arm, "r2"))
        pairs.append((set_name, case, "r1r2") + ((a1, a2) if i % 2 == 0 else (a2, a1)))

ids = ["p%03d" % (n + 1) for n in range(len(pairs))]
random.Random(20261022 + 33).shuffle(ids)
out = os.path.join(B, "blind", "packets")
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, "*.md")):
    os.remove(f)
blind_map = {}
for pid, (set_name, case, rnd, A, B_) in sorted(zip(ids, pairs)):
    prompt = open(os.path.join(B, "prompts", case + ".txt"), encoding="utf-8").read().strip()
    key = open(os.path.join(B, "keys", case + ".md"), encoding="utf-8").read().strip()
    points = json.load(open(os.path.join(B, "keypoints", case + ".json"), encoding="utf-8"))
    body = "\n\n".join([
        "# PAIR %s" % pid,
        "## Request\n\n````text\n%s\n````" % prompt,
        "## Answer key\n\n%s" % key,
        "## Key points\n\n%s" % "\n".join("%s. %s" % (p["id"], p["point"]) for p in points),
        "## Answer A\n\n````text\n%s\n````" % A[2],
        "## Answer B\n\n````text\n%s\n````" % B_[2],
    ]) + "\n"
    for t in (A[2], B_[2]):
        if body.count(t) != (2 if A[2] == B_[2] else 1):
            raise SystemExit("answer not present exactly once in %s" % pid)
    with open(os.path.join(out, pid + ".md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    entry = {"set": set_name, "case": case, "round": rnd, "A": A[0], "B": B_[0]}
    if set_name.startswith("aa-"):
        entry.update({"A_round": A[1], "B_round": B_[1]})
    blind_map[pid] = entry
with open(os.path.join(B, "blind-map.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(blind_map, fh, indent=1, sort_keys=True)
by_set = {}
for e in blind_map.values():
    by_set[e["set"]] = by_set.get(e["set"], 0) + 1
print("%d pairs: %s; drafts from %d steered runs; every answer present in full" % (len(blind_map), by_set, len(drafts)))
