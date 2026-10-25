#!/usr/bin/env python3
"""Answer benchmark questions through the Antigravity CLI (agy) headless, one run per
question and arm, each from its own empty workspace.

Usage: answer_agy.py QUESTIONS.jsonl ARM [--model gemini-4-argon-low] [--workers 3]

Arms run in throwaway homes on W:, so Emily's own ~/.gemini config is never read or changed
(agy signs in the same way from any home). Any other arm name is refused.
  gm-plain       home-plain: Antigravity as shipped, no plugins, rules or instructions.
  gm-plain-aa    the same, a separate launch for the A/A noise floor.
  gm-grav        home-grav-<lang>: the same plus Gravitas installed by scripts/install.py
                 in the question's language, Second Opinion off.
  gm-grav-aa     the same, a separate launch for the A/A noise floor.
  gm-grav:NAME   home-grav-NAME-<lang>: a copy of that home whose rule file is DATA/rules/NAME/
                 <lang>.md, re-copied before any run whose home copy differs; refused unless
                 DATA/rules/NAME/FROZEN exists.

Isolation is proved from each run's own transcript (the conversation database agy writes
into the home): the plain arms must contain no line of the Gravitas rule and none of Emily's
personal rules; a Gravitas arm must contain every line of its own rule longer than 20
characters, and none of Emily's personal rules. The sha256 of the rule file in the home at
run time is recorded with every run.

Limits from the coordinator (2026-10-25): at most 3 agy processes at once; on the first 429 or
quota error every worker stops, waits 15 minutes, and the run resumes at half the parallelism.
"""
import argparse
import glob
import hashlib
import re
import ledger
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


BUILD_LOGS = DATA / "agy" / "build_logs.txt"  # one glob per line: the build legs' run logs (read only)


def builds_hit_quota(window_s=900):
    """True if any build leg's log, written in the last 15 minutes, shows a quota or 429 error.
    The coordinator's rule (2026-10-25): builds come first, so judge and answer runs pause then."""
    if not BUILD_LOGS.exists():
        return False
    now = time.time()
    for pat in [l.strip() for l in BUILD_LOGS.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]:
        for p in glob.glob(pat, recursive=True):
            try:
                if now - os.path.getmtime(p) > window_s:
                    continue
                with open(p, "rb") as f:
                    f.seek(max(0, os.path.getsize(p) - 200_000))
                    tail = f.read().decode("utf-8", "replace")
            except OSError:
                continue
            for line in tail.splitlines():
                if quota_error_line(line, is_err_file=p.endswith("_err.txt")):
                    return True
    return False


def quota_error_line(line, is_err_file=False):
    """A quota or 429 error, not a 401 (agy's hourly token refresh) and not a number such as a
    token count of 4291: the line must be an error line (AGY_ERROR, an "error" JSON key, or any
    line of an _err.txt file) and name 429 as a whole number, RESOURCE_EXHAUSTED or quota."""
    if not (is_err_file or "AGY_ERROR" in line or '"error' in line.lower()):
        return False
    if "UNAUTHENTICATED" in line or re.search(r"\b401\b", line):
        return False
    return bool(re.search(r"(?<![\d.])429(?![\d.])", line) or "RESOURCE_EXHAUSTED" in line or re.search(r"quota", line, re.I))


def wait_for_builds():
    paused = False
    while builds_hit_quota():
        if not paused:
            print("a build leg hit a quota or 429 error: pausing agy runs until it recovers", flush=True)
            paused = True
        time.sleep(300)


def parse_arm(arm):
    """(is_plain, candidate name or None) for a known arm; anything else stops the run."""
    if arm in ("gm-plain", "gm-plain-aa"):
        return True, None
    if arm in ("gm-grav", "gm-grav-aa"):
        return False, None
    if arm.startswith("gm-grav:") and len(arm) > 8:
        name = arm.split(":", 1)[1]
        if not (DATA / "rules" / name / "FROZEN").exists():
            raise SystemExit(f"rule candidate {name} has no FROZEN file; freeze it before any run")
        return False, name
    raise SystemExit(f"unknown arm {arm!r}")


def home_for(arm, lang):
    plain, name = parse_arm(arm)
    if plain:
        return AGY / "home-plain", None
    if name is None:
        h = AGY / f"home-grav-{GLANG[lang]}"
    else:
        h = AGY / f"home-grav-{name}-{GLANG[lang]}"
        if not h.exists():
            shutil.copytree(AGY / f"home-grav-{GLANG[lang]}" / ".gemini" / "config", h / ".gemini" / "config")
        src = DATA / "rules" / name / f"{GLANG[lang]}.md"
        dst = h / ".gemini/config/plugins/gravitas/rules/AGENTS.md"
        if hashlib.sha256(src.read_bytes()).hexdigest() != hashlib.sha256(dst.read_bytes()).hexdigest():
            shutil.copyfile(src, dst)
            ledger.append("agy-home-rule-recopied", home=str(h), rule=str(src), sha256=ledger.sha256_file(src))
    rule = h / ".gemini/config/plugins/gravitas/rules/AGENTS.md"
    return h, rule


def rule_lines(rule_text):
    """Every substantial line of a rule (over 20 characters, comments and blank lines skipped)."""
    return [x.strip() for x in rule_text.splitlines() if len(x.strip()) > 20 and not x.strip().startswith("<!--")]


def agy_version(home):
    log = home / ".gemini" / "antigravity-cli" / "cli.log"
    if not log.exists():
        return None
    found = re.findall(r"version: (\d+\.\d+\.\d+)", log.read_text(encoding="utf-8", errors="replace"))
    return found[-1] if found else None


def markers(rule_text):
    """Three marker lines from the rule: its first, a middle and its last substantial line."""
    lines = [x.strip() for x in rule_text.splitlines() if len(x.strip()) > 20 and not x.startswith("<!--")]
    return [lines[0][:40], lines[len(lines) // 2][:40], lines[-1][:40]]


def grav_markers(lang):
    return markers((AGY / f"home-grav-{GLANG[lang]}" / ".gemini/config/plugins/gravitas/rules/AGENTS.md").read_text(encoding="utf-8"))


def run_one(q, arm, model, outdir):
    if stop.is_set():
        return None
    wait_for_builds()
    qid, lang = q["id"], q["lang"]
    base = outdir / qid
    js = base.with_suffix(".json")
    home, rule = home_for(arm, lang)
    rule_sha = ledger.sha256_file(rule) if rule is not None else None
    attempt = 1
    if js.exists():
        rec = json.loads(js.read_text(encoding="utf-8"))
        # Reuse only a successful, isolated run made with the same rule file as now.
        if rec.get("status") == "SUCCESS" and rec.get("chars", 0) > 0 and rec.get("isolation_ok") and rec.get("home_rule_sha256") == rule_sha:
            return rec
        attempt = rec.get("attempt", 1) + 1
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
    plain, _ = parse_arm(arm)
    if db and db.exists():
        data = db.read_bytes()
        base_lines = rule_lines((AGY / f"home-grav-{GLANG[lang]}" / ".gemini/config/plugins/gravitas/rules/AGENTS.md").read_text(encoding="utf-8"))
        iso["base_rule_lines_found"] = sum(1 for m in base_lines if m.encode("utf-8") in data)
        iso["emily_markers_found"] = sum(1 for m in EMILY_MARKERS if m.encode("utf-8") in data)
        if rule is not None:
            own = rule_lines(rule.read_text(encoding="utf-8"))
            iso["own_rule_lines"] = len(own)
            iso["own_rule_lines_found"] = sum(1 for m in own if m.encode("utf-8") in data)
    if plain:
        iso_ok = iso.get("base_rule_lines_found") == 0 and iso.get("emily_markers_found") == 0
    else:
        iso_ok = (iso.get("own_rule_lines", 0) > 0 and iso.get("own_rule_lines_found") == iso.get("own_rule_lines")
                  and iso.get("emily_markers_found") == 0)
    base.with_suffix(".txt").write_text(text, encoding="utf-8", newline="\n")
    rec = {"qid": qid, "lang": lang, "arm": arm, "attempt": attempt, "model": model, "agy_version": agy_version(home),
           "exit": code, "status": status, "secs": secs, "chars": len(text), "usage": usage, "steps": tools,
           "conversation_id": cid, "home_rule_sha256": rule_sha, "isolation": iso, "isolation_ok": iso_ok, "quota_error": quota}
    js.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    ledger.append("answer-launch", platform="agy", arm=arm, qid=qid, attempt=attempt, start=round(t0, 1), secs=secs, status=status,
                  model=model, agy_version=rec["agy_version"], ndjson_sha256=ledger.sha256_file(base.with_suffix(".ndjson")),
                  text_sha256=ledger.sha256_text(text), home_rule_sha256=rule_sha, isolation_ok=iso_ok, conversation_id=cid)
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
    parse_arm(a.arm)
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
