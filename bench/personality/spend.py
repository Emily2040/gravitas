#!/usr/bin/env python3
"""Measured DeepSeek spend for this benchmark so far, from the runs' own usage records.

Usage: spend.py [--cap 50] [--next USD]

Sums every one-shot batch (batches/*.out.jsonl, each id's final result once), every DSH
harness run (answers/ds-*/*.json, token usage plus web search queries and fetches at 0.75 USD
per 1,000), at off-peak prices, or at peak prices for usage recorded during a peak hour when
the record has a time. Prints the total and exits 1 when total + --next would pass --cap, so a
stage can be refused before it starts (Emily's cap for the lean plan: 50 USD, 2026-10-25).
"""
import argparse
import glob
import json
import sys

import dshbatch

WEB_USD = 0.75 / 1000
# agy runs approved by the coordinator: about 1,200 (2026-10-25) plus 500 for Gemini judging.
AGY_APPROVED = 1700


def total():
    D = dshbatch.DATA
    batch_usd, calls = 0.0, 0
    for p in glob.glob(str(D / "batches" / "*.out.jsonl")):
        # Every attempt that returned usage was billed, including ones later retried.
        for l in open(p, encoding="utf-8"):
            if not l.strip():
                continue
            try:
                r = json.loads(l)
            except ValueError:
                continue
            u = r.get("usage")
            if not u:
                continue
            calls += 1
            batch_usd += dshbatch.cost_usd({"input": u.get("inputTokens", 0), "cache_read": u.get("cacheReadTokens", 0),
                                            "output": u.get("outputTokens", 0)})
    harness_usd, runs = 0.0, 0
    for p in glob.glob(str(D / "answers" / "ds-*" / "*.json")):
        r = json.load(open(p, encoding="utf-8"))
        u = r.get("usage") or {}
        runs += 1
        harness_usd += dshbatch.cost_usd({"input": u.get("input", 0), "cache_read": u.get("cache_read", 0), "output": u.get("output", 0)})
        t = r.get("tools") or {}
        harness_usd += WEB_USD * (t.get("web_search_queries", 0) + t.get("web_fetch", 0))
    # Antigravity runs: every agy run writes one conversation database in its home, so the count
    # of those files is the count of runs, probes and failed runs included.
    agy_runs = len(glob.glob(str(D / "agy" / "home-*" / ".gemini" / "antigravity-cli" / "conversations" / "*.db")))
    return {"batch_calls": calls, "batch_usd": round(batch_usd, 3), "harness_runs": runs, "harness_usd": round(harness_usd, 3),
            "total_usd": round(batch_usd + harness_usd, 3), "agy_runs": agy_runs, "agy_approved": AGY_APPROVED}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=float, default=50.0)
    ap.add_argument("--next", type=float, default=0.0, help="estimated cost of the stage about to start")
    a = ap.parse_args()
    t = total()
    t["cap"], t["next"] = a.cap, a.next
    t["ok"] = t["total_usd"] + a.next <= a.cap
    print(json.dumps(t))
    sys.exit(0 if t["ok"] else 1)


if __name__ == "__main__":
    main()
