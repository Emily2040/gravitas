#!/usr/bin/env python3
"""Communication metrics per arm, and paired ratios between two arms, on one question set.

Usage: answer_stats.py QUESTIONS.jsonl ARM [ARM2] [--out FILE]

For each arm: the mean of AA's 21 characteristics over its answers (metrics.py), by
language too. With ARM2 (the plain arm): on questions both arms answered, the median of
per-pair character ratios ARM/ARM2, the share of pairs under 0.6, and ARM/ARM2 ratios of
the mean hedge rates, bold, list items and colons. Missing or empty answers are counted
and left out; they are never filled with a default.
"""
import argparse
import json
import statistics
from collections import defaultdict

import metrics
from judge import answer


def per_arm(qs, arm):
    rows, missing = [], 0
    for q in qs:
        t = answer(arm, q["id"])
        if not t:
            missing += 1
            continue
        rows.append((q, metrics.measure(t, q["lang"])))
    return rows, missing


def means(rows, keys):
    if not rows:
        return {}
    return {k: round(statistics.fmean(m[k] for _, m in rows), 3) for k in keys}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("questions")
    ap.add_argument("arm")
    ap.add_argument("arm2", nargs="?")
    ap.add_argument("--out")
    a = ap.parse_args()
    qs = [json.loads(l) for l in open(a.questions, encoding="utf-8") if l.strip()]
    keys = metrics.AA_METRICS + ["list_items", "bold_lead_items", "hedges_first_per_1k", "hedges_extended_per_1k", "slop_phrases"]
    rep = {"questions": len(qs), "arms": {}}
    for arm in [x for x in (a.arm, a.arm2) if x]:
        rows, missing = per_arm(qs, arm)
        by_lang = defaultdict(list)
        for q, m in rows:
            by_lang[q["lang"]].append((q, m))
        rep["arms"][arm] = {"answered": len(rows), "missing": missing, "mean": means(rows, keys),
                            "by_lang": {l: {"answered": len(r), "mean": means(r, keys)} for l, r in sorted(by_lang.items())}}
    if a.arm2:
        A = {q["id"]: m for q, m in per_arm(qs, a.arm)[0]}
        B = {q["id"]: m for q, m in per_arm(qs, a.arm2)[0]}
        both = [i for i in A if i in B and B[i]["characters"] > 0]
        ratios = [A[i]["characters"] / B[i]["characters"] for i in both]

        def ratio(k):
            b = statistics.fmean(B[i][k] for i in both) if both else 0
            return round(statistics.fmean(A[i][k] for i in both) / b, 3) if both and b > 0 else None
        rep["paired"] = {"pairs": len(both), "median_char_ratio": round(statistics.median(ratios), 3) if ratios else None,
                         "share_under_0_6": round(sum(r < 0.6 for r in ratios) / len(ratios), 3) if ratios else None,
                         "hedges_first_ratio": ratio("hedges_first_per_1k"), "hedges_extended_ratio": ratio("hedges_extended_per_1k"),
                         "bold_ratio": ratio("bold"), "list_items_ratio": ratio("list_items"), "colons_ratio": ratio("colons"),
                         "words_ratio": ratio("words")}
    s = json.dumps(rep, ensure_ascii=False, indent=1)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(s)
    print(s if a.out is None else json.dumps(rep.get("paired", {}), ensure_ascii=False))


if __name__ == "__main__":
    main()
