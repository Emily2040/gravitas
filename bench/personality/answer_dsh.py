#!/usr/bin/env python3
"""Answer benchmark questions through DeepSeek Harness headless, one run per question and arm.

Usage: answer_dsh.py QUESTIONS.jsonl ARM [--workers 12] [--rule-dir DIR] [--limit N]

Arms:
  ds-plain       profile gv-plain as shipped (deepseek-flash, DSH's own tools).
  ds-grav        profile gv-grav, Gravitas rule only (claim check off) in the question's
                 language, rule text from --rule-dir (default: the pinned base copy).
  ds-grav:NAME   the same with the rule files in DATA/rules/NAME (a tuning candidate).

Each run starts from its own empty folder, as a user's would. Output per run:
DATA/answers/ARM/QID.{ndjson,err,txt,json}; the .json holds exit code, seconds, usage
totals, tool calls by name and the rule log record (Gravitas arms must show the expected
rule hash; plain must show none).
"""
import argparse
import hashlib
import json
import os
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DATA = Path(os.environ.get("GP_DATA", "W:/AgentData/logs/gravitas-personality"))
GLANG = {"zh": "zh-CN", "en": "en", "ja": "ja", "ko": "ko"}
DSH_CWD = Path(os.environ.get("GP_DSH_CWD", "W:/AgentData/logs/gravitas-dsh-ab3/cwd"))
GRAV_LINK = Path(os.environ.get("GP_GRAV_LINK", "W:/Projects/gravitas-claim-check"))
lock = threading.Lock()


def overlay_for(arm, lang):
    if arm == "ds-plain":
        return None, None
    name = arm.split(":", 1)[1] if ":" in arm else "base"
    rule = DATA / "rules" / name / f"{GLANG[lang]}.md"
    if not rule.exists():
        raise SystemExit(f"missing rule file {rule}")
    # The plugin's prompt section is the rule plus its short DSH tool note, read from the gv-grav
    # link target (dsh/platform/<lang>.rule.md); the rule log hashes that composed text.
    note = (GRAV_LINK / "dsh" / "platform" / f"{GLANG[lang]}.rule.md").read_text(encoding="utf-8")
    text = rule.read_text(encoding="utf-8").rstrip() + "\n\n" + note.strip() + "\n"
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    ov = DATA / "overlays" / f"grav-{name}-{lang}.yml"
    ov.write_text(
        "# Gravitas arm: rule only, claim check off, plugin in the question's language.\n"
        f"- id: dsh-gravitas\n  config:\n    language: {GLANG[lang]}\n    alwaysOnRule: true\n    claimCheck: false\n"
        f"    ruleFile: '{rule.as_posix()}'\n", encoding="utf-8", newline="\n")
    return ov, sha


def summarise(ndjson_path):
    usage = {"input": 0, "cache_read": 0, "output": 0}
    tools, final, steps = {}, "", 0
    for line in open(ndjson_path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t = e.get("type")
        if t == "status" and e.get("phase") == "step_end":
            steps += 1
            u = e.get("usage") or {}
            usage["input"] += u.get("inputTokens", 0)
            usage["cache_read"] += u.get("cacheReadTokens", 0)
            usage["output"] += u.get("outputTokens", 0)
        elif t == "tool_call":
            n = e.get("tool") or e.get("name") or "?"
            tools[n] = tools.get(n, 0) + 1
            if n == "web_search":  # billed per query: count each query in the call
                qs = (e.get("input") or {}).get("queries") or [None]
                tools["web_search_queries"] = tools.get("web_search_queries", 0) + len(qs)
        elif t == "final":
            final = e.get("text") or ""
    return usage, tools, final, steps


def run_one(q, arm, outdir):
    qid, lang = q["id"], q["lang"]
    base = outdir / qid
    if (base.with_suffix(".json")).exists():
        rec = json.loads(base.with_suffix(".json").read_text(encoding="utf-8"))
        if rec.get("exit") == 0 and rec.get("chars", 0) > 0:
            return rec
    ov, sha = overlay_for(arm, lang)
    prof = "gv-plain" if arm == "ds-plain" else "gv-grav"
    # DSH's Windows sandbox needs Full control on the run folder; the one folder Emily granted it
    # is round three's cwd, so each run gets its own gp- subfolder there (round three, 2026-10-25).
    cwd = DSH_CWD / f"gp-{arm.replace(':', '_')}-{qid}"
    cwd.mkdir(parents=True, exist_ok=True)
    rulelog = base.with_suffix(".rule.jsonl")
    if rulelog.exists():
        rulelog.unlink()
    cmd = ["dsh", "--profile", prof] + (["--patch", ov.as_posix()] if ov else []) + ["--json", "-"]
    env = dict(os.environ, GRAVITAS_RULE_LOG=str(rulelog))
    t0 = time.time()
    with open(base.with_suffix(".ndjson"), "w", encoding="utf-8") as out, open(base.with_suffix(".err"), "w", encoding="utf-8") as err:
        try:
            p = subprocess.run(cmd, input=q["q"].encode("utf-8"), stdout=out, stderr=err, cwd=cwd, env=env,
                               timeout=900, shell=(os.name == "nt"))
            code = p.returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    secs = round(time.time() - t0, 1)
    usage, tools, final, steps = summarise(base.with_suffix(".ndjson"))
    base.with_suffix(".txt").write_text(final, encoding="utf-8", newline="\n")
    rule_rec = None
    if rulelog.exists():
        lines = [l for l in rulelog.read_text(encoding="utf-8").splitlines() if l.strip()]
        rule_rec = json.loads(lines[-1]) if lines else None
    rule_ok = (rule_rec is None) if arm == "ds-plain" else (rule_rec is not None and rule_rec.get("sha256") == sha)
    rec = {"qid": qid, "lang": lang, "arm": arm, "exit": code, "secs": secs, "chars": len(final), "steps": steps,
           "usage": usage, "tools": tools, "rule": rule_rec, "rule_expected": sha, "rule_ok": rule_ok}
    base.with_suffix(".json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    with lock:
        print(f"{arm} {qid} {lang} exit={code} secs={secs} chars={len(final)} tools={tools} rule_ok={rule_ok}", flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("questions")
    ap.add_argument("arm")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    qs = [json.loads(l) for l in open(a.questions, encoding="utf-8") if l.strip()]
    if a.limit:
        qs = qs[: a.limit]
    outdir = DATA / "answers" / a.arm.replace(":", "_")
    outdir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.workers) as ex:
        recs = list(ex.map(lambda q: run_one(q, a.arm, outdir), qs))
    bad = [r for r in recs if r["exit"] != 0 or not r["chars"] or not r["rule_ok"]]
    tot = {k: sum(r["usage"][k] for r in recs) for k in ("input", "cache_read", "output")}
    searches = sum(r["tools"].get("web_search_queries", 0) + r["tools"].get("web_fetch", 0) for r in recs)
    print(json.dumps({"arm": a.arm, "runs": len(recs), "bad": len(bad), "usage": tot, "web_calls": searches,
                      "mean_secs": round(sum(r["secs"] for r in recs) / max(1, len(recs)), 1)}))


if __name__ == "__main__":
    main()
