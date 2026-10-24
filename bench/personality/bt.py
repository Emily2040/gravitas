#!/usr/bin/env python3
"""Ratings per trait from pairwise verdicts, after AA-PersonalityBench's method.

- Firth-penalised Bradley-Terry fit per trait: P(i beats j) = sigmoid(t_i - t_j); a tie counts
  as half a win for each side; the penalty is 0.5 * log det of the Fisher information (Firth
  1993), which keeps ratings finite when one system wins every comparison.
- Elo scale: Elo = anchor_elo + (400 / ln 10) * t, so a 400-point gap is 10-to-1 odds; the
  anchor system is fixed at 1000 on every trait.
- 95% intervals from 1,000 bootstrap resamples. The resampling unit is the question (all of a
  question's verdicts move together), which is more conservative than resampling single
  verdicts, because one question's comparisons share answers.
- Index: each member trait's Elo becomes a z-score across the systems rated; the index is the
  mean z (Sycophantic inverted). With only a few systems z-scores are coarse, so the paired
  Elo difference between two named systems is reported beside it.

Usage: bt.py VERDICTS.jsonl --anchor ds-plain [--filter key=value ...] [--boot 1000] [--out FILE]
       bt.py --self-test
"""
import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

SCALE = 400.0 / math.log(10.0)
HERE = Path(__file__).resolve().parent


def fit(systems, rows, anchor):
    """rows: list of (i, j, w) with w = score of i against j (1, 0.5, 0). Returns strengths
    with the anchor at 0, from the Firth-penalised likelihood."""
    k = len(systems)
    ai = systems.index(anchor)
    free = [s for s in range(k) if s != ai]
    if not rows:
        return np.zeros(k)
    I = np.array([r[0] for r in rows]); J = np.array([r[1] for r in rows]); W = np.array([r[2] for r in rows], dtype=float)

    def unpack(x):
        t = np.zeros(k)
        t[free] = x
        return t

    def negpen(x):
        t = unpack(x)
        d = t[I] - t[J]
        p = 1.0 / (1.0 + np.exp(-d))
        ll = np.sum(W * np.log(p + 1e-300) + (1 - W) * np.log(1 - p + 1e-300))
        # Fisher information over the free parameters
        v = p * (1 - p)
        F = np.zeros((k, k))
        np.add.at(F, (I, I), v); np.add.at(F, (J, J), v)
        np.add.at(F, (I, J), -v); np.add.at(F, (J, I), -v)
        Ff = F[np.ix_(free, free)]
        sign, logdet = np.linalg.slogdet(Ff)
        pen = 0.5 * logdet if sign > 0 else -1e6
        return -(ll + pen)

    res = minimize(negpen, np.zeros(len(free)), method="L-BFGS-B")
    return unpack(res.x)


def score(v, sys_a):
    """Score of sys_a in one verdict row (ties half)."""
    if v["winner"] is None:
        return 0.5
    return 1.0 if v["winner"] == sys_a else 0.0


def ratings(verdicts, anchor, boot=1000, seed=20261024):
    """{trait: {system: {elo, lo, hi, n}}} and per-question resampling."""
    by_trait = defaultdict(list)
    for v in verdicts:
        by_trait[v["trait"]].append(v)
    rng = np.random.default_rng(seed)
    out = {}
    for trait, vs in sorted(by_trait.items()):
        systems = sorted({v["left"] for v in vs} | {v["right"] for v in vs})
        if anchor not in systems:
            continue
        idx = {s: i for i, s in enumerate(systems)}
        rows_by_q = defaultdict(list)
        for v in vs:
            rows_by_q[v["qid"]].append((idx[v["left"]], idx[v["right"]], score(v, v["left"])))
        qids = sorted(rows_by_q)
        allrows = [r for q in qids for r in rows_by_q[q]]
        t = fit(systems, allrows, anchor)
        samples = []
        for _ in range(boot):
            pick = rng.integers(0, len(qids), len(qids))
            rows = [r for p in pick for r in rows_by_q[qids[p]]]
            samples.append(fit(systems, rows, anchor))
        S = np.array(samples) if samples else np.zeros((0, len(systems)))
        n = defaultdict(int)
        for v in vs:
            n[v["left"]] += 1; n[v["right"]] += 1
        out[trait] = {"systems": systems, "n_verdicts": len(vs), "n_questions": len(qids), "theta": t.tolist(),
                      "boot": S.tolist(),
                      "elo": {s: {"elo": round(1000 + SCALE * t[i], 1),
                                  "lo": round(1000 + SCALE * float(np.percentile(S[:, i], 2.5)), 1) if boot else None,
                                  "hi": round(1000 + SCALE * float(np.percentile(S[:, i], 97.5)), 1) if boot else None,
                                  "n": n[s]} for s, i in idx.items()}}
    return out


def diff(r, trait, a, b):
    """Elo(a) - Elo(b) on a trait, with its bootstrap 95% interval (same resamples)."""
    R = r[trait]
    ia, ib = R["systems"].index(a), R["systems"].index(b)
    d = SCALE * (R["theta"][ia] - R["theta"][ib])
    S = np.array(R["boot"])
    if len(S) == 0:
        return {"diff": round(d, 1), "lo": None, "hi": None}
    ds = SCALE * (S[:, ia] - S[:, ib])
    return {"diff": round(d, 1), "lo": round(float(np.percentile(ds, 2.5)), 1), "hi": round(float(np.percentile(ds, 97.5)), 1)}


def indexes(r, traits_doc):
    """Mean z-score per index per system (Sycophantic inverted), over systems rated on every member."""
    inv = set(traits_doc["inverted_in_index"])
    out = {}
    for name, members in traits_doc["indexes"].items():
        have = [m for m in members if m in r]
        if not have:
            continue
        systems = sorted(set.intersection(*[set(r[m]["systems"]) for m in have]))
        if len(systems) < 2:
            continue
        zs = defaultdict(list)
        for m in have:
            e = np.array([r[m]["elo"][s]["elo"] for s in systems])
            sd = e.std()
            z = (e - e.mean()) / sd if sd > 0 else np.zeros_like(e)
            if m in inv:
                z = -z
            for s, zz in zip(systems, z):
                zs[s].append(float(zz))
        out[name] = {"members": have, "mean_z": {s: round(sum(v) / len(v), 3) for s, v in zs.items()}}
    return out


def self_test():
    rng = np.random.default_rng(1)
    # three systems with true Elo gaps of +200 and -100 against the anchor
    true = {"anchor": 0.0, "up": 200 / SCALE, "down": -100 / SCALE}
    vs = []
    names = list(true)
    for q in range(400):
        for a, b in (("anchor", "up"), ("anchor", "down"), ("up", "down")):
            p = 1 / (1 + math.exp(-(true[a] - true[b])))
            u = rng.random()
            w = a if u < p * 0.9 else (None if u < p * 0.9 + 0.1 else b)
            vs.append({"qid": f"q{q}", "trait": "T", "left": a, "right": b, "winner": w})
    r = ratings(vs, "anchor", boot=200)
    e = r["T"]["elo"]
    assert abs(e["anchor"]["elo"] - 1000) < 1e-6
    assert 1140 < e["up"]["elo"] < 1260, e
    assert 850 < e["down"]["elo"] < 960, e
    assert e["up"]["lo"] < e["up"]["elo"] < e["up"]["hi"], e
    d = diff(r, "T", "up", "anchor")
    assert d["lo"] > 0, d
    # a clean sweep stays finite under the Firth penalty
    sweep = [{"qid": f"q{q}", "trait": "S", "left": "anchor", "right": "x", "winner": "x"} for q in range(30)]
    rs = ratings(sweep, "anchor", boot=50)
    assert math.isfinite(rs["S"]["elo"]["x"]["elo"]) and rs["S"]["elo"]["x"]["elo"] > 1300, rs["S"]["elo"]
    # ties only: equal ratings
    ties = [{"qid": f"q{q}", "trait": "E", "left": "anchor", "right": "x", "winner": None} for q in range(30)]
    assert abs(ratings(ties, "anchor", boot=0)["E"]["elo"]["x"]["elo"] - 1000) < 1.0
    # no verdicts: no rating at all (a missing trait is absent, never a default)
    assert ratings([], "anchor", boot=10) == {}
    print("bt self-test: ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("verdicts", nargs="?")
    ap.add_argument("--anchor", default="ds-plain")
    ap.add_argument("--filter", action="append", default=[])
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
        return
    vs = [json.loads(l) for l in open(a.verdicts, encoding="utf-8") if l.strip()]
    for f in a.filter:
        k, val = f.split("=", 1)
        vs = [v for v in vs if str(v.get(k)) in val.split("|")]
    r = ratings(vs, a.anchor, boot=a.boot)
    traits_doc = json.load(open(HERE / "traits.json", encoding="utf-8"))
    res = {"anchor": a.anchor, "filters": a.filter, "boot": a.boot, "verdicts": len(vs),
           "traits": {t: {k: v for k, v in R.items() if k not in ("boot", "theta")} for t, R in r.items()},
           "indexes": indexes(r, traits_doc)}
    if a.out:
        Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for t, R in sorted(r.items()):
        print(f"{t:24s} " + "  ".join(f"{s}={R['elo'][s]['elo']:.0f} [{R['elo'][s]['lo']:.0f},{R['elo'][s]['hi']:.0f}]" for s in R["systems"]))


if __name__ == "__main__":
    main()
