#!/usr/bin/env python3
"""Run a judge's share of comparisons through the Antigravity CLI, one run per comparison.

Usage: judge_agy.py NAME JUDGE [--model gemini-3.8-flash-high] [--workers 3]

Reads DATA/judging/NAME/JUDGE.prompts.jsonl (from `judge.py export`), writes
DATA/judging/NAME/JUDGE.raw.jsonl ({job, verdict: raw text}); then `judge.py import NAME
JUDGE <that file>` parses the verdicts. Runs from the clean throwaway home (home-plain), so
neither Gravitas nor Emily's own rules reach the judge, each comparison from its own empty
workspace, with the prompt on stdin. Same limits as answer_agy.py: at most 3 at once; on a
429 or quota error, stop, wait 15 minutes, resume at half the parallelism.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from answer_agy import AGY, DATA, EMILY_MARKERS, QUOTA, grav_markers

lock = threading.Lock()
stop = threading.Event()


def one(p, model, out_path, done):
    if stop.is_set() or p["job"] in done:
        return
    home = AGY / "home-plain"
    ws = AGY / "ws" / f"judge-{abs(hash(p['job'])) % 10**10}"
    if ws.exists():
        shutil.rmtree(ws)
    ws.mkdir(parents=True)
    msg = json.dumps({"event": "user", "message": {"role": "user", "content": p["prompt"]}}, ensure_ascii=False) + "\n"
    env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
    t0 = time.time()
    try:
        r = subprocess.run(["agy", "--input-format", "stream-json", "--output-format", "stream-json", "--model", model, "-p="],
                           input=msg.encode("utf-8"), capture_output=True, cwd=ws, env=env, timeout=600)
        out, err = r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        out, err = "", "timeout"
    text, status, cid = "", None, None
    for line in out.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("event") == "init":
            cid = e.get("conversation_id")
        if e.get("event") == "result":
            status, text = e["result"].get("status"), e["result"].get("response") or ""
    iso = None
    db = home / ".gemini" / "antigravity-cli" / "conversations" / f"{cid}.db" if cid else None
    if db and db.exists():
        data = db.read_bytes()
        iso = all(m.encode("utf-8") not in data for m in EMILY_MARKERS + grav_markers("en") + grav_markers("zh"))
    quota = any(k in err for k in QUOTA)
    rec = {"job": p["job"], "verdict": text, "status": status, "secs": round(time.time() - t0, 1), "judge_clean": iso, "model": model}
    with lock:
        if status == "SUCCESS" and iso:
            with open(out_path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"{p['job'][:60]} status={status} secs={rec['secs']} clean={iso} -> {text.strip()[-12:]!r}" + (" QUOTA" if quota else ""), flush=True)
    if quota:
        stop.set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("judge")
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    if a.workers > 3:
        sys.exit("at most 3 agy processes at once (coordinator's limit)")
    d = DATA / "judging" / a.name
    prompts = [json.loads(l) for l in open(d / f"{a.judge}.prompts.jsonl", encoding="utf-8") if l.strip()]
    out_path = d / f"{a.judge}.raw.jsonl"
    workers = a.workers
    while True:
        done = set()
        if out_path.exists():
            done = {json.loads(l)["job"] for l in open(out_path, encoding="utf-8") if l.strip()}
        stop.clear()
        with ThreadPoolExecutor(workers) as ex:
            list(ex.map(lambda p: one(p, a.model, out_path, done), prompts))
        if not stop.is_set():
            break
        workers = max(1, workers // 2)
        print(f"quota or 429 error: waiting 15 minutes, then resuming with {workers} at a time", flush=True)
        time.sleep(900)
    n = sum(1 for _ in open(out_path, encoding="utf-8")) if out_path.exists() else 0
    print(json.dumps({"judge": a.judge, "model": a.model, "prompts": len(prompts), "answered_clean": n}))


if __name__ == "__main__":
    main()
