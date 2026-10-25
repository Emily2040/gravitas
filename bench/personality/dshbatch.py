#!/usr/bin/env python3
"""Run many independent DeepSeek calls inside one DeepSeek Harness boot.

Each request is a one-shot call with no history, sent through DSH's own signed-in route
(profile gv-plain with the lean overlay and the llm-batch plugin; the saved profile is not
changed). Results are appended as they finish, so a cut run resumes where it stopped.
"""
import json
import os
import subprocess
import time
from pathlib import Path

DATA = Path(os.environ.get("GP_DATA", "W:/AgentData/logs/gravitas-personality"))
HERE = Path(__file__).resolve().parent
PLUGIN = (HERE / "dsh" / "llm-batch.mjs").as_posix()
LEAN = (DATA / "overlays" / "lean.yml").as_posix()


def _yaml_str(s):
    return "'" + str(s).replace("'", "''") + "'"


def is_peak(t=None):
    """DeepSeek peak hours: 01:00-04:00 and 06:00-10:00 UTC, Monday to Friday (api-docs pricing
    page, read 2026-10-24). Chinese public holidays are off-peak too; not modelled (errs safe)."""
    g = time.gmtime(t if t is not None else time.time())
    return g.tm_wday < 5 and (1 <= g.tm_hour < 4 or 6 <= g.tm_hour < 10)


def wait_offpeak():
    """Emily's lean plan runs off-peak only: hold until the peak window ends."""
    waited = 0
    while is_peak():
        if waited == 0:
            print("[dshbatch] DeepSeek peak hours: waiting for off-peak", flush=True)
        time.sleep(60)
        waited += 60
    return waited


def run(name, requests, concurrency=24, model="deepseek-flash", temperature=None, max_tokens=None, timeout_s=7200):
    """Run requests [{id, user, system?}] as batch `name`; return {id: result} for every id."""
    wait_offpeak()
    bdir = DATA / "batches"
    bdir.mkdir(parents=True, exist_ok=True)
    src, out = bdir / f"{name}.in.jsonl", bdir / f"{name}.out.jsonl"
    ids = [r["id"] for r in requests]
    assert len(ids) == len(set(ids)), f"{name}: duplicate request ids"
    with open(src, "w", encoding="utf-8", newline="\n") as f:
        for r in requests:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    cfg = [f"in: {_yaml_str(src.as_posix())}", f"out: {_yaml_str(out.as_posix())}",
           f"concurrency: {int(concurrency)}", f"model: {_yaml_str(model)}"]
    if temperature is not None:
        cfg.append(f"temperature: {float(temperature)}")
    if max_tokens is not None:
        cfg.append(f"maxTokens: {int(max_tokens)}")
    overlay = bdir / f"{name}.overlay.yml"
    overlay.write_text(
        "- id: headless-runner\n  disabled: true\n- insert:\n    - id: gravitas-llm-batch\n"
        f"      name: {_yaml_str(PLUGIN)}\n      config:\n" + "".join(f"        {c}\n" for c in cfg),
        encoding="utf-8", newline="\n")
    cwd = DATA / "cwd" / f"batch-{name}"
    cwd.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    for attempt in range(3):
        with open(bdir / f"{name}.stderr.txt", "a", encoding="utf-8") as err:
            proc = subprocess.run(["dsh", "--profile", "gv-plain", "--patch", LEAN, "--patch", overlay.as_posix()],
                                  cwd=cwd, stdout=subprocess.DEVNULL, stderr=err, timeout=timeout_s, shell=(os.name == "nt"))
        got = load(out)
        missing = [i for i in ids if i not in got or got[i].get("error")]
        if not missing:
            break
    got = load(out)
    print(f"[dshbatch] {name}: {sum(1 for i in ids if i in got and not got[i].get('error'))}/{len(ids)} ok in {time.time() - t0:.0f}s (exit {proc.returncode})")
    return {i: got.get(i, {"id": i, "error": "missing"}) for i in ids}


def load(out):
    """Latest result per id from an out.jsonl (a later success replaces an earlier error)."""
    got = {}
    if not Path(out).exists():
        return got
    for line in open(out, encoding="utf-8"):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r["id"] not in got or not r.get("error"):
            got[r["id"]] = r
    return got


def usage_totals(results):
    """Sum token usage over results; reasoning is billed as output."""
    t = {"calls": 0, "input": 0, "cache_read": 0, "output": 0, "errors": 0}
    for r in results.values():
        if r.get("error"):
            t["errors"] += 1
            continue
        u = r.get("usage") or {}
        t["calls"] += 1
        t["input"] += u.get("inputTokens", 0)
        t["cache_read"] += u.get("cacheReadTokens", 0)
        t["output"] += u.get("outputTokens", 0)
    return t


# DeepSeek list prices for deepseek-flash, USD per 1M tokens, from api-docs.deepseek.com
# (read 2026-10-24): off-peak cache hit 0.003, miss 0.15, output 0.60; peak is double
# (01:00-04:00 and 06:00-10:00 UTC, Monday to Friday). Search and fetch: 0.75 per 1,000.
PRICE_OFFPEAK = {"cache_read": 0.003, "input": 0.15, "output": 0.60}


def cost_usd(t, peak=False):
    k = 2.0 if peak else 1.0
    return k * (t["cache_read"] * PRICE_OFFPEAK["cache_read"] + t["input"] * PRICE_OFFPEAK["input"]
                + t["output"] * PRICE_OFFPEAK["output"]) / 1e6
