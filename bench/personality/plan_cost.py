#!/usr/bin/env python3
"""Run counts and DeepSeek cost for the full benchmark, from the pilots' measured token use.

Usage: plan_cost.py [--out FILE]

Unit costs are measured, never assumed: each comes from a pilot's own usage records on W:
(drafting: gen-pilot2-*/gen-pilot3-*; rating: rate-pilot-rate; judging: judge-pilot; bare
answers: answers-raw-flash-*; harness answers: answers/ds-plain and answers/ds-grav run
records, including their web search queries and fetches, billed at 0.75 USD per 1,000).
Prices are DeepSeek's off-peak list prices (dshbatch.PRICE_OFFPEAK); peak hours cost double.
"""
import argparse
import glob
import json
from pathlib import Path

import dshbatch

D = dshbatch.DATA
WEB_USD = 0.75 / 1000


def batch_unit(pattern):
    tot = {"calls": 0, "input": 0, "cache_read": 0, "output": 0, "errors": 0}
    for p in glob.glob(str(D / "batches" / pattern)):
        t = dshbatch.usage_totals(dshbatch.load(p))
        for k in tot:
            tot[k] += t[k]
    if not tot["calls"]:
        raise SystemExit(f"no pilot usage for {pattern}: metric missing")
    return dshbatch.cost_usd(tot) / tot["calls"], tot["calls"]


def harness_unit(arm, qids=None):
    recs = [json.loads(open(p, encoding="utf-8").read()) for p in glob.glob(str(D / "answers" / arm / "*.json"))]
    recs = [r for r in recs if r.get("exit") == 0 and (qids is None or r["qid"] in qids)]
    if not recs:
        raise SystemExit(f"no pilot runs for {arm}: metric missing")
    usd = 0.0
    for r in recs:
        u = r["usage"]
        usd += dshbatch.cost_usd({"input": u["input"], "cache_read": u["cache_read"], "output": u["output"]})
        usd += WEB_USD * (r["tools"].get("web_search_queries", 0) + r["tools"].get("web_fetch", 0))
    return usd / len(recs), len(recs), sum(r["secs"] for r in recs) / len(recs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--scope", choices=["full", "lean"], default="full")
    a = ap.parse_args()
    u = {}
    u["draft"], n_draft = batch_unit("gen-pilot[23]-*.out.jsonl")
    u["rate"], n_rate = batch_unit("rate-pilot-rate.out.jsonl")
    u["judge"], n_judge = batch_unit("judge-pilot.out.jsonl")
    u["raw"], n_raw = batch_unit("answers-raw-flash-*.out.jsonl")
    u["ds_plain"], n_p, s_p = harness_unit("ds-plain")
    u["ds_grav"], n_g, s_g = harness_unit("ds-grav")

    # The plan. Question set: 30 traits x 2 modes x drafts per cell (zh 12, en 7, ja 6, ko 6),
    # plus 10% top-up drafting; kept: zh 7, en 4, ja 3, ko 3 per cell = 1,020, plus 86 seeds.
    cells = 30 * 2
    drafts = cells * (12 + 7 + 6 + 6)
    draft_calls = round(cells * 4 * 1.10)
    rate_calls = round(drafts * 1.10)
    questions = 1020 + 86
    tuning, heldout = 510 + 86, 510
    T = 17  # traits per comparison set: 10 Gravitas targets, 6 guards, the question's own trait
    plan = {
        "drafting calls": (draft_calls, "draft"),
        "rating calls": (rate_calls, "rate"),
        "ds-plain harness runs (all questions)": (questions, "ds_plain"),
        "ds-grav harness runs (all questions; after round four, gv-grav)": (questions, "ds_grav"),
        "ds-plain A/A rerun (150 held-out)": (150, "ds_plain"),
        "raw-flash bare answers (AA's no-system-prompt condition)": (questions, "raw"),
        "rule screening: 5 candidates x 300 tuning questions, bare model + rule": (5 * 300, "raw"),
        "rule candidates in the harness: 2 x tuning": (2 * tuning, "ds_grav"),
        "final candidate in the harness: held-out": (heldout, "ds_grav"),
        "judge: ds-plain vs ds-grav, all questions": (questions * T, "judge"),
        "judge: ds-plain vs raw-flash, 30% of questions": (round(0.3 * questions) * T, "judge"),
        "judge: Gemini plain vs Gravitas, 300 questions": (300 * T, "judge"),
        "judge: Gemini plain vs DSH plain, 300 questions (self-preference, one scale)": (300 * T, "judge"),
        "judge: A/A noise floor, 150 questions": (150 * T, "judge"),
        "judge: rule screening, 5 x 300": (5 * 300 * T, "judge"),
        "judge: harness candidates, 2 x tuning": (2 * tuning * T, "judge"),
        "judge: final candidate, held-out": (heldout * T, "judge"),
        "judge: remaining 13 traits, 25% of questions, 2 pairs": (13 * round(0.25 * questions) * 2, "judge"),
        "judge: order-swap duplicates for position bias": (1000, "judge"),
    }
    if a.scope == "lean":
        # Emily's lean plan (2026-10-25): judge only the 8 Gravitas-targeted traits, one rule
        # candidate, no bare-model arm or screening, off-peak, at most 50 USD.
        T8 = 8
        plan = {
            "drafting calls": (draft_calls, "draft"),
            "rating calls": (rate_calls, "rate"),
            "ds-plain harness runs (all questions)": (questions, "ds_plain"),
            "ds-grav harness runs (all questions; after round four, gv-grav)": (questions, "ds_grav"),
            "ds-plain-aa rerun (150 held-out)": (150, "ds_plain"),
            "ds-grav-aa rerun (150 held-out; after round four)": (150, "ds_grav"),
            "one rule candidate in the harness: tuning + held-out": (tuning + heldout, "ds_grav"),
            "judge: ds-plain vs ds-grav, all questions, 8 traits": (questions * T8, "judge"),
            "judge: A/A plain and A/A Gravitas, 150 each, 8 traits": (2 * 150 * T8, "judge"),
            "judge: candidate vs ds-plain, tuning + held-out, 8 traits": ((tuning + heldout) * T8, "judge"),
            "judge: Gemini plain vs Gravitas, 300 questions, 8 traits": (300 * T8, "judge"),
            "judge: Gemini candidate vs plain, 300 questions, 8 traits": (300 * T8, "judge"),
            "judge: ds-plain vs gm-plain, 300 questions, 8 traits (self-preference)": (300 * T8, "judge"),
            "judge: order-swap duplicates for position bias": (800, "judge"),
        }
    rows, tot_usd, harness, single = [], 0.0, 0, 0
    for k, (n, unit) in plan.items():
        usd = n * u[unit]
        tot_usd += usd
        if unit.startswith("ds_"):
            harness += n
        else:
            single += n
        rows.append({"item": k, "count": n, "unit": unit, "usd_offpeak": round(usd, 2)})
    rep = {"unit_costs_usd_offpeak": {k: round(v, 5) for k, v in u.items()},
           "unit_basis": {"draft": n_draft, "rate": n_rate, "judge": n_judge, "raw": n_raw, "ds_plain_runs": n_p, "ds_grav_runs": n_g},
           "harness_mean_secs": {"ds_plain": round(s_p, 1), "ds_grav": round(s_g, 1)},
           "plan": rows, "questions": questions, "tuning": tuning, "heldout": heldout,
           "harness_runs": harness, "single_calls": single,
           "total_usd_offpeak": round(tot_usd, 2), "total_usd_if_all_peak": round(2 * tot_usd, 2)}
    s = json.dumps(rep, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(s, encoding="utf-8")
    print(s)


if __name__ == "__main__":
    main()
