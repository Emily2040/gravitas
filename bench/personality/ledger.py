#!/usr/bin/env python3
"""Append-only ledger of every answer launch and judging step (gate N11).

Each line: {"time", "kind", ...}. Lines are only ever appended; nothing in the benchmark
rewrites or deletes this file. The verifier counts launches per (arm, qid) and judging runs
per set from it, and compares the text hashes it records with the texts it re-extracts.
"""
import hashlib
import json
import os
import time
from pathlib import Path

DATA = Path(os.environ.get("GP_DATA", "W:/AgentData/logs/gravitas-personality"))
LEDGER = DATA / "ledger.jsonl"


def sha256_text(t):
    return hashlib.sha256((t or "").encode("utf-8")).hexdigest()


def sha256_file(p):
    p = Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def append(kind, **fields):
    rec = {"time": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "kind": kind, **fields}
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec
