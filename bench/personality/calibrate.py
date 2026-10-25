#!/usr/bin/env python3
"""Agreement between judges on the same comparisons (same job id = same question, trait,
answers and order).

Usage: calibrate.py JUDGE_FILE [JUDGE_FILE ...] [--out FILE]
  Each JUDGE_FILE is a judge.py verdict file ({job, judge, verdict}); the judge name comes
  from its "judge" field.

Reports per judge: verdicts, tie share, share of "A" among non-tie verdicts. Per judge pair:
shared comparisons, Cohen's kappa over the three labels (A, B, TIE), direction agreement on
comparisons where both judges picked a side, and kappa per trait (traits with at least 5
shared comparisons). The trait is read from the job id (qid|trait|left|right|rep).
"""
import argparse
import itertools
import json
from collections import Counter, defaultdict

LABELS = ("A", "B", "TIE")


def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[l] * cb[l] for l in LABELS) / (n * n)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def load(path):
    out, name = {}, None
    for l in open(path, encoding="utf-8"):
        if not l.strip():
            continue
        r = json.loads(l)
        if r.get("verdict") in LABELS:
            out[r["job"]] = r["verdict"]
            name = r.get("judge") or name
    return name, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out")
    a = ap.parse_args()
    judges = dict(load(p) for p in a.files)
    rep = {"judges": {}, "pairs": {}}
    for j, v in judges.items():
        vals = list(v.values())
        nt = [x for x in vals if x != "TIE"]
        rep["judges"][j] = {"n": len(vals), "tie_share": round(vals.count("TIE") / len(vals), 3) if vals else None,
                            "a_share_nontie": round(nt.count("A") / len(nt), 3) if nt else None}
    for j1, j2 in itertools.combinations(sorted(judges), 2):
        shared = sorted(set(judges[j1]) & set(judges[j2]))
        pairs = [(judges[j1][k], judges[j2][k]) for k in shared]
        both = [(x, y) for x, y in pairs if x != "TIE" and y != "TIE"]
        per = defaultdict(list)
        for k, p in zip(shared, pairs):
            per[k.split("|")[1]].append(p)
        rep["pairs"][f"{j1}~{j2}"] = {
            "shared": len(shared), "kappa": kappa(pairs), "exact_agreement": round(sum(x == y for x, y in pairs) / len(pairs), 3) if pairs else None,
            "direction_n": len(both), "direction_agreement": round(sum(x == y for x, y in both) / len(both), 3) if both else None,
            "per_trait_kappa": {t: {"n": len(ps), "kappa": kappa(ps)} for t, ps in sorted(per.items()) if len(ps) >= 5},
        }
    s = json.dumps(rep, ensure_ascii=False, indent=1)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(s)
    print(s)


if __name__ == "__main__":
    main()
