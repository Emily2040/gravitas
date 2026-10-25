#!/usr/bin/env python3
"""Answer benchmark questions through the Antigravity CLI (agy) headless, one run per
question and arm, each from its own empty workspace.

Usage: answer_agy.py QUESTIONS.jsonl ARM [--model gemini-4-argon-low] [--workers 3]

Arms run in throwaway homes on W:, so Emily's own ~/.gemini config is never read or changed
(agy signs in the same way from any home):
  gm-plain       home-plain: Antigravity as shipped, no plugins, rules or instructions.
  gm-grav        home-grav-<lang>: the same plus Gravitas installed by scripts/install.py
                 in the question's language, Second Opinion off.
  gm-grav:NAME   home-grav-NAME-<lang>: a copy of that home with the rule file replaced by
                 DATA/rules/NAME/<lang>.md (a tuning candidate).

Isolation is proved from each run's own transcript (the conversation database agy writes
into the home): the plain arm must contain none of the Gravitas rule's marker lines, nor
Emily's global rules; a Gravitas arm must contain all of its rule's marker lines.

Limits from the coordinator (2026-10-25): at most 3 agy processes at once; on the first 429 or
quota error every worker stops, waits 15 minutes, and the run resumes at half the parallelism.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DATA = Path(os.environ.get("GP_DATA", "W:/AgentData/logs/gravitas-personality"))
AGY = DATA / "agy"
GLANG = {"zh": "zh-CN", "en": "en", "ja": "ja", "ko": "ko"}
EMILY_MARKERS = ["EMILY QUALITY LOOP", "# Reasoning method", "argon-baseline"]
QUOTA = ("429", "RESOURCE_EXHAUSTED", "quota", "Quota", "rate limit", "Rate limit")
lock = threading.Lock()
stop = threading.Event()


def home_for(arm, lang):
    if arm == "gm-plain":
        return AGY / "home-plain", None
    if arm == "gm-grav":
        h = AGY / f"home-grav-{GLANG[lang]}"
    else:
        name = arm.split(":", 1)[1]
        h = AGY / f"home-grav-{name}-{GLANG[lang]}"
        if not h.exists():
            shutil.copytree(AGY / f"home-grav-{GLANG[lang]}" / ".gemini" / "config", h / ".gemini" / "config")
            shutil.copyfile(DATA / "rules" / name / f"{GLANG[lang]}.md", h / ".gemini/config/plugins/gravitas/rules/AGENTS.md")
    rule = h / ".gemini/config/plugins/gravitas/rules/AGENTS.md"
    return h, rule


def markers(rule_text):
    """Three marker lines from the rule: its first, a middle and its last substantial line."""
    lines = [x.strip() for x in rule_text.splitlines() if len(x.strip()) > 20 and not x.startswith("<!--")]
    return [lines[0][:40], lines[len(lines) // 2][:40], lines[-1][:40]]


def grav_markers(lang):
    return markers((AGY / f"home-grav-{GLANG[lang]}" / ".gemini/config/plugins/gravitas/rules/AGENTS.md").read_text(encoding="utf-8"))


def run_one(q, arm, model, outdir):
    if stop.is_set():
        return None
    qid, lang = q["id"], q["lang"]
    base = outdir / qid
    js = base.with_suffix(".json")
    if js.exists():
        rec = json.loads(js.read_text(encoding="utf-8"))
        if rec.get("status") == "SUCCESS" and rec.get("chars", 0) > 0 and rec.get("isolation_ok"):
            return rec
    home, rule = home_for(arm, lang)
    ws = AGY / "ws" / f"{arm.replace(':', '_')}-{qid}"
    if ws.exists():
        shutil.rmtree(ws)
    ws.mkdir(parents=True)
    env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
    cmd = ["agy", "-p", q["q"], "--model", model, "--sandbox", "--output-format", "stream-json"]
    t0 = time.time()
    with open(base.with_suffix(".ndjson"), "w", encoding="utf-8") as out, open(base.with_suffix(".err"), "w", encoding="utf-8") as err:
        try:
            p = subprocess.run(cmd, stdout=out, stderr=err, cwd=ws, env=env, timeout=900)
            code = p.returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    secs = round(time.time() - t0, 1)
    cid, status, text, usage, tools = None, None, "", None, {}
    for line in open(base.with_suffix(".ndjson"), encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("event") == "init":
            cid = e.get("conversation_id")
        elif e.get("event") == "result":
            r = e["result"]
            status, text, usage = r.get("status"), (r.get("response") or "").strip(), r.get("usage")
        elif e.get("event") == "step_update":
            st = e["step_update"].get("step_type")
            if st and st not in ("user_input", "agent_response") and e["step_update"].get("state") == "DONE":
                tools[st] = tools.get(st, 0) + 1
    errtext = base.with_suffix(".err").read_text(encoding="utf-8", errors="replace")
    quota = any(k in errtext for k in QUOTA) or (status not in (None, "SUCCESS") and any(k in json.dumps(status) for k in QUOTA))
    # Isolation from the run's own transcript.
    iso = {}
    db = home / ".gemini" / "antigravity-cli" / "conversations" / f"{cid}.db" if cid else None
    if db and db.exists():
        data = db.read_bytes()
        gm = grav_markers(lang)
        iso["grav_markers_found"] = sum(1 for m in gm if m.encode("utf-8") in data)
        iso["emily_markers_found"] = sum(1 for m in EMILY_MARKERS if m.encode("utf-8") in data)
        if rule is not None:
            own = markers(rule.read_text(encoding="utf-8"))
            iso["own_rule_markers_found"] = sum(1 for m in own if m.encode("utf-8") in data)
    if arm == "gm-plain":
        iso_ok = iso.get("grav_markers_found") == 0 and iso.get("emily_markers_found") == 0
    else:
        iso_ok = iso.get("own_rule_markers_found") == 3 and iso.get("emily_markers_found") == 0
    base.with_suffix(".txt").write_text(text, encoding="utf-8", newline="\n")
    rec = {"qid": qid, "lang": lang, "arm": arm, "model": model, "exit": code, "status": status, "secs": secs,
           "chars": len(text), "usage": usage, "steps": tools, "conversation_id": cid, "isolation": iso,
           "isolation_ok": iso_ok, "quota_error": quota}
    js.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    with lock:
        print(f"{arm} {qid} {lang} status={status} secs={secs} chars={len(text)} steps={tools} iso_ok={iso_ok}"
              + (" QUOTA" if quota else ""), flush=True)
    if quota:
        stop.set()
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("questions")
    ap.add_argument("arm")
    ap.add_argument("--model", default="gemini-4-argon-low")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    if a.workers > 3:
        sys.exit("at most 3 agy processes at once (coordinator's limit)")
    qs = [json.loads(l) for l in open(a.questions, encoding="utf-8") if l.strip()]
    outdir = DATA / "answers" / a.arm.replace(":", "_")
    outdir.mkdir(parents=True, exist_ok=True)
    workers = a.workers
    while True:
        stop.clear()
        with ThreadPoolExecutor(workers) as ex:
            recs = list(ex.map(lambda q: run_one(q, a.arm, a.model, outdir), qs))
        if not stop.is_set():
            break
        workers = max(1, workers // 2)
        print(f"quota or 429 error: waiting 15 minutes, then resuming with {workers} at a time", flush=True)
        time.sleep(900)
    recs = [r for r in recs if r]
    ok = [r for r in recs if r["status"] == "SUCCESS" and r["chars"] > 0 and r["isolation_ok"]]
    print(json.dumps({"arm": a.arm, "model": a.model, "runs": len(recs), "ok": len(ok),
                      "mean_secs": round(sum(r["secs"] for r in recs) / max(1, len(recs)), 1),
                      "median_chars": sorted(r["chars"] for r in recs)[len(recs) // 2] if recs else 0}))


if __name__ == "__main__":
    main()
