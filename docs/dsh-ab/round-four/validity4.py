"""Check every round-four run from its own output before anything is graded.

    python validity4.py                  -> held-out runs (schedule.txt, raw/); writes validity.json; exit 1 if any invalid
    python validity4.py --tuning         -> tuning runs (tuning-schedule.txt, tuning/); writes validity-tuning.json
    python validity4.py --archive-invalid  -> also moves each invalid run's files to raw/attempt1/ and writes
                                           rerun-schedule.txt (one rerun per run, never a second; see reruns.json)
    python validity4.py --self-test      -> checks every rule below on made-up runs; exit 1 on any failure

A run is invalid (a harness failure, rerun once before grading) when any of these holds. Every check reads the
run's own files; a missing file fails its check.
  1. exit: <stem>.exit is missing or not 0.
  2. final: <stem>.txt is missing or blank, or the NDJSON has no final event.
  3. cwd: the NDJSON session event's cwd is not this run's own folder (r4-<case>.<arm>.r<n>).
  4. shell: any shell tool result (pwsh, bash, ...) has status "error" (round two's sandbox failure,
     "SetNamedSecurityInfoW failed", came back this way).
  5. network: the run made web calls and every one of them failed with a network error ("fetch failed").
  6. plugin stderr: <stem>.err mentions dsh-gravitas (a plugin warning or error), in any arm.
  7. rule: a Gravitas arm needs <stem>.rule.jsonl with at least one record, and every record must carry the
     request's language, the arm's ruleFile (none for base, rules/change4/<lang>.md for c4) and the sha256 of
     the arm's rule text. The expected sha is recomputed here from the files (rule + DSH rule note, exactly as
     dsh/index.js ruleText joins them) and must also equal expected-rule-hashes.json. The change-4 sentence must
     be in the c4 rule text and not in the base rule text. A plain run must leave no rule log.
  8. ledger: run-ledger.tsv (written by run.sh) must hold exactly one attempt for the run, or two when
     validity4.py archived it for its one rerun (reruns.json); the last attempt's session id must be the one in
     the NDJSON and its freeze hash must be freeze-start.txt's. A run started by hand, or a third attempt, fails.
  9. account: any web result that failed with a sign-in, 401, 429 or quota error, or every web_search failing,
     means the harness, not the arm, shaped the answer.
 10. reach: a non-web tool call whose input names the round's folders (gravitas-dsh-ab4, keypoints, AgentData
     outside the run's own folder), climbs above the run's folder (../ or ..\\), or lists the environment.
Checked for the whole round (exit 1, every run reported): the state freeze.sh records still equals
freeze-start.txt, and the change-4 rule files and expected-rule-hashes.json equal the copies committed at
freeze-start's head under docs/dsh-ab/round-four/.
Reported, graded as is: constrained-language-mode warnings from the shell ("Only core types are supported"),
partial network failures, fetched pages that returned HTTP 4xx or 5xx, any other stderr.
After its one rerun a run that is still invalid is graded as is and its problem is reported; if its final is
blank, that answer loses every pair it is in and its key points count as missing. No run or request is dropped.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

B = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(B))), "Projects", "gravitas-claim-check")
LANG = {"zh": "zh-CN", "en": "en", "ja": "ja", "ko": "ko"}
SHELL = re.compile(r"^(?:pwsh|bash|shell|powershell|terminal)", re.I)
WEB = re.compile(r"^web_", re.I)
CLM = "Only core types are supported"
ACCOUNT = re.compile(r"rejected the account sign-in|HTTP 401|HTTP 429|RESOURCE_EXHAUSTED|quota", re.I)
FETCH_STATUS = re.compile(r"^Fetched \S+ \(HTTP (\d{3})\)")
REACH = re.compile(r"gravitas-dsh-ab4|keypoints|AgentData|\.\.[\\/]|\benv:|printenv|GetEnvironmentVariable|Get-ChildItem\s+-?Path\s+env|\bgci\s+env", re.I)


def rule_text(lang_dir, rule_path, w=W):
    rule = open(rule_path, encoding="utf-8").read()
    note = open(os.path.join(w, "dsh", "platform", "%s.rule.md" % lang_dir), encoding="utf-8").read()
    return "%s\n\n%s\n" % (rule.rstrip(), note.strip())


def expected_rules(b=B, w=W):
    """Per language: {arm: (sha, ruleFile or None, text)} recomputed from the files, plus a list of problems."""
    exp = json.load(open(os.path.join(b, "expected-rule-hashes.json"), encoding="utf-8"))
    out, problems = {}, []
    for short, lang in LANG.items():
        base_path = os.path.join(w, "dist", lang, "gravitas", "rules", "AGENTS.md")
        c4_path = os.path.join(b, "rules", "change4", "%s.md" % lang)
        base = rule_text(lang, base_path, w)
        c4 = rule_text(lang, c4_path, w)
        sh = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()
        out[short] = {"gv-grav-base": (sh(base), None), "gv-grav-c4": (sh(c4), "W:/AgentData/logs/gravitas-dsh-ab4/rules/change4/%s.md" % lang)}
        if sh(base) != exp[short]["base"]:
            problems.append("%s base sha %s != expected-rule-hashes.json" % (short, sh(base)[:12]))
        if sh(c4) != exp[short]["c4"]:
            problems.append("%s c4 sha %s != expected-rule-hashes.json" % (short, sh(c4)[:12]))
        sentence = exp[short]["c4Sentence"]
        if sentence not in c4:
            problems.append("%s c4 sentence missing from the c4 rule" % short)
        if sentence in base:
            problems.append("%s c4 sentence present in the base rule" % short)
    return out, problems


def read_ndjson(path):
    events = []
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    return events


def check_run(stem, arm, case, rnd, rules):
    """Return (problems, notes, info) for one run, from its own files."""
    problems, notes, info = [], [], {}
    lang = case.split("-")[0]
    # 1. exit
    try:
        code = open(stem + ".exit", encoding="utf-8").read().strip()
    except OSError:
        code = None
    info["exit"] = code
    if code is None:
        problems.append("exit missing")
    elif code != "0":
        problems.append("exit %s" % code)
    # 2. final
    final = open(stem + ".txt", encoding="utf-8").read() if os.path.exists(stem + ".txt") else ""
    info["chars"] = len(final.strip())
    if not final.strip():
        problems.append("blank or missing final")
    events = read_ndjson(stem + ".ndjson") if os.path.exists(stem + ".ndjson") else []
    if not events:
        problems.append("ndjson missing or empty")
    if not any(e.get("type") == "final" for e in events):
        problems.append("no final event")
    # 3. cwd
    sess = next((e for e in events if e.get("type") == "session"), None)
    want = "r4-%s.%s.r%s" % (case, arm, rnd)
    cwd = (sess or {}).get("cwd", "")
    if not cwd.replace("/", "\\").rstrip("\\").endswith("\\" + want):
        problems.append("cwd %r is not %s" % (cwd, want))
    # 4-5. tools
    calls = {e.get("callId"): str(e.get("tool", "")) for e in events if e.get("type") == "tool_call"}
    # 10. reach: strip the run's own folder from each non-web call's input, then look for the round's folders
    own = re.compile(r"(?:[A-Za-z]:|/[a-z])?[\\/]+AgentData[\\/]+logs[\\/]+gravitas-dsh-ab3[\\/]+cwd[\\/]+" + re.escape(want), re.I)
    reach = []
    for e in events:
        if e.get("type") == "tool_call" and not WEB.match(str(e.get("tool", ""))):
            text = json.dumps(e.get("input"), ensure_ascii=False).replace("\\\\", "\\")
            text = own.sub("", text)
            m = REACH.search(text)
            if m:
                reach.append("%s: %s" % (e.get("tool"), m.group(0)))
    if reach:
        problems.append("reached outside its folder (%s)" % "; ".join(reach[:3]))
    shell_n = shell_err = web_n = web_net = clm = 0
    search_n = search_err = account = bad_fetch = 0
    for e in events:
        if e.get("type") != "tool_result":
            continue
        tool = calls.get(e.get("callId"), "")
        res = e.get("result") if isinstance(e.get("result"), str) else json.dumps(e.get("result"), ensure_ascii=False)
        if SHELL.match(tool):
            shell_n += 1
            if e.get("status") == "error":
                shell_err += 1
            if CLM in (res or ""):
                clm += 1
        elif WEB.match(tool):
            web_n += 1
            if e.get("status") == "error" and "fetch failed" in (res or ""):
                web_net += 1
            if e.get("status") == "error" and ACCOUNT.search(res or ""):
                account += 1
            if tool == "web_search":
                search_n += 1
                search_err += e.get("status") == "error"
            m = FETCH_STATUS.match(res or "")
            if tool == "web_fetch" and m and not m.group(1).startswith("2"):
                bad_fetch += 1
    info.update(shell=shell_n, shell_errors=shell_err, web=web_n, web_network_errors=web_net,
                web_pages=sum(1 for t in calls.values() if t == "web_fetch"))
    if shell_err:
        problems.append("shell broken (%d of %d shell results are errors)" % (shell_err, shell_n))
    if web_n and web_net == web_n:
        problems.append("network down (all %d web results failed)" % web_n)
    elif web_net:
        notes.append("%d of %d web results failed with a network error" % (web_net, web_n))
    if clm:
        notes.append("%d shell results hit constrained language mode" % clm)
    info.update(web_search=search_n, web_search_errors=search_err, account_errors=account, fetch_non2xx=bad_fetch)
    if account:
        problems.append("account or quota failure in %d web results" % account)
    if search_n and search_err == search_n:
        problems.append("search down (all %d web_search results failed)" % search_n)
    if bad_fetch:
        notes.append("%d fetched pages returned HTTP 4xx/5xx" % bad_fetch)
    # 6. stderr
    err = open(stem + ".err", encoding="utf-8", errors="replace").read() if os.path.exists(stem + ".err") else ""
    if "dsh-gravitas" in err:
        problems.append("plugin message on stderr: %s" % err.strip().splitlines()[0][:120])
    elif err.strip():
        notes.append("stderr: %s" % err.strip().splitlines()[0][:120])
    # 7. rule
    log = stem + ".rule.jsonl"
    recs = []
    if os.path.exists(log):
        for line in open(log, encoding="utf-8"):
            if line.strip():
                try:
                    recs.append(json.loads(line))
                except ValueError:
                    recs.append({})
    info["rule_records"] = len(recs)
    if arm == "gv-plain":
        if recs or os.path.exists(log):
            problems.append("plain run left a rule log")
    elif arm in ("gv-grav-base", "gv-grav-c4"):
        sha, rule_file = rules[lang][arm]
        if not recs:
            problems.append("rule log missing or empty")
        for r in recs:
            if r.get("sha256") != sha:
                problems.append("rule sha %s is not the %s rule" % (str(r.get("sha256"))[:12], arm))
            if r.get("language") != LANG[lang]:
                problems.append("rule language %r, request is %s" % (r.get("language"), LANG[lang]))
            if r.get("ruleFile") != rule_file:
                problems.append("ruleFile %r, %s needs %r" % (r.get("ruleFile"), arm, rule_file))
    else:
        problems.append("unknown arm %s" % arm)
    return sorted(set(problems), key=problems.index), notes, info


def ledger_problems(ledger_rows, stem, od, rerun, sid, fz):
    """Rule 8 for one run: attempts in run-ledger.tsv for (stem, folder), the last one's session id and freeze hash."""
    norm = lambda x: os.path.normcase(os.path.normpath(x.replace("/w/", "W:/", 1) if x.startswith("/w/") else x))
    rows = [r for r in ledger_rows if len(r) >= 7 and r[0] == stem and norm(r[1]) == norm(od)]
    want = 2 if rerun else 1
    out = []
    if len(rows) != want:
        out.append("ledger has %d attempts, %d allowed" % (len(rows), want))
    if rows:
        if rows[-1][6] != (sid or "none"):
            out.append("ledger session %s is not the NDJSON's %s" % (rows[-1][6], sid))
        if rows[-1][5] != fz:
            out.append("ledger freeze hash %s is not freeze-start's %s" % (rows[-1][5], fz))
    return out


def round_problems(b=B, w=W):
    """Whole-round checks: frozen state unchanged; rule files equal the copies committed at freeze-start's head."""
    out = []
    fs = os.path.join(b, "freeze-start.txt")
    if not os.path.exists(fs):
        return ["no freeze-start.txt"]
    start = open(fs, encoding="utf-8").read().splitlines()
    try:
        now = subprocess.run(["sh", os.path.join(b, "freeze.sh"), "--state"], capture_output=True, text=True,
                             encoding="utf-8", timeout=300).stdout.splitlines()
    except Exception as e:  # noqa: BLE001
        now = ["freeze.sh failed: %s" % e]
    if now != start[2:]:
        diff = [l for l in now if l not in start[2:]][:3] + ["(was) " + l for l in start[2:] if l not in now][:3]
        out.append("state changed since freeze-start: %s" % "; ".join(diff))
    head = next((l.split(": ", 1)[1] for l in start if l.startswith("head: ")), None)
    for f in ["rules/change4/%s.md" % lang for lang in LANG.values()] + ["expected-rule-hashes.json"]:
        try:
            committed = subprocess.run(["git", "-C", w, "show", "%s:docs/dsh-ab/round-four/%s" % (head, f)],
                                       capture_output=True, timeout=60).stdout
        except Exception:  # noqa: BLE001
            committed = b""
        local = open(os.path.join(b, f), "rb").read() if os.path.exists(os.path.join(b, f)) else None
        if not committed:
            out.append("%s not committed at freeze-start's head" % f)
        elif local is None or committed.replace(b"\r\n", b"\n") != local.replace(b"\r\n", b"\n"):
            out.append("%s differs from the copy committed at freeze-start's head" % f)
    return out


def main(tuning=False, archive=False, b=B, w=W):
    sched = os.path.join(b, "tuning-schedule.txt" if tuning else "schedule.txt")
    out_dir = os.path.join(b, "tuning" if tuning else "raw")
    runs = [l.split() for l in open(sched, encoding="utf-8") if l.strip()]
    rules, rule_problems = expected_rules(b, w)
    reruns_path = os.path.join(b, "reruns%s.json" % ("-tuning" if tuning else ""))
    reruns = json.load(open(reruns_path, encoding="utf-8")) if os.path.exists(reruns_path) else []
    round_probs = round_problems(b, w)
    report = {"rule_files": rule_problems, "round": round_probs, "invalid": [], "flagged": [], "final_attempt_invalid": [], "runs": {}}
    for p in rule_problems:
        print("RULE FILES: %s" % p)
    for p in round_probs:
        print("ROUND: %s" % p)
    lp = os.path.join(b, "run-ledger.tsv")
    ledger_rows = [l.rstrip("\n").split("\t") for l in open(lp, encoding="utf-8")] if os.path.exists(lp) else []
    fsp = os.path.join(b, "freeze-start.txt")
    fz = hashlib.sha256(open(fsp, "rb").read()).hexdigest()[:16] if os.path.exists(fsp) else "no-freeze-start"
    for arm, case, rnd in runs:
        key = "%s.%s.r%s" % (case, arm, rnd)
        problems, notes, info = check_run(os.path.join(out_dir, key), arm, case, rnd, rules)
        nd = os.path.join(out_dir, key + ".ndjson")
        sid = next((e.get("sessionId") for e in (read_ndjson(nd) if os.path.exists(nd) else []) if e.get("type") == "session"), None)
        problems += ledger_problems(ledger_rows, key, out_dir, key in reruns, sid, fz)
        info.update(problems=problems, notes=notes, rerun=key in reruns)
        report["runs"][key] = info
        if problems:
            (report["final_attempt_invalid"] if key in reruns else report["invalid"]).append(key)
        if notes:
            report["flagged"].append(key)
        print("%-46s %s%s" % (key, ("INVALID%s " % (" after rerun" if key in reruns else "")) + "; ".join(problems) if problems else "ok",
                              "  | " + "; ".join(notes) if notes else ""))
    name = "validity%s.json" % ("-tuning" if tuning else "")
    with open(os.path.join(b, name), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
    if archive and report["invalid"]:
        a_dir = os.path.join(out_dir, "attempt1")
        os.makedirs(a_dir, exist_ok=True)
        lines = []
        for key in report["invalid"]:
            case, arm, r = key.split(".")
            for f in os.listdir(out_dir):
                if f.startswith(key + "."):
                    shutil.move(os.path.join(out_dir, f), os.path.join(a_dir, f))
            lines.append("%s %s %s\n" % (arm, case, r[1:]))
        open(os.path.join(b, "rerun-schedule%s.txt" % ("-tuning" if tuning else "")), "w", encoding="utf-8", newline="\n").writelines(lines)
        with open(reruns_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(sorted(set(reruns) | set(report["invalid"])), fh, indent=1)
        print("archived %d invalid runs to %s; rerun-schedule written" % (len(report["invalid"]), a_dir))
    print("%d runs, %d invalid, %d invalid after their rerun, %d flagged%s%s" % (
        len(runs), len(report["invalid"]), len(report["final_attempt_invalid"]), len(report["flagged"]),
        "; RULE FILE PROBLEMS" if rule_problems else "", "; ROUND PROBLEMS" if round_probs else ""))
    return 1 if (report["invalid"] or rule_problems or round_probs) else 0


def self_test():
    """Made-up runs in a temp folder: one good run per arm, then one break per rule."""
    fails, ran = [], []
    rules, rule_problems = expected_rules()
    if rule_problems:
        fails.append("real rule files: %s" % rule_problems)
    tmp = tempfile.mkdtemp(prefix="v4test-")

    def write_run(arm, case="zh-sick-pay", rnd="1", **over):
        stem = os.path.join(tmp, "%s.%s.r%s" % (case, arm, rnd))
        for ext in (".exit", ".txt", ".ndjson", ".err", ".rule.jsonl"):
            if os.path.exists(stem + ext):
                os.remove(stem + ext)
        lang = case.split("-")[0]
        cwd = over.get("cwd", "W:\\AgentData\\logs\\gravitas-dsh-ab3\\cwd\\r4-%s.%s.r%s" % (case, arm, rnd))
        ev = [{"type": "session", "cwd": cwd}] + over.get("tools", []) + ([{"type": "final", "text": "answer"}] if over.get("final_event", True) else [])
        files = {".exit": over.get("exit", "0\n"), ".txt": over.get("txt", "answer"),
                 ".ndjson": "\n".join(json.dumps(e) for e in ev) + "\n", ".err": over.get("err", "")}
        if arm != "gv-plain" or "rule" in over:
            sha, rf = rules[lang][arm] if arm in rules[lang] else ("x", None)
            rec = over.get("rule", {"language": LANG[lang], "ruleFile": rf, "sha256": sha})
            files[".rule.jsonl"] = "" if rec is None else json.dumps(rec) + "\n"
        for ext, text in files.items():
            if text is not False:
                open(stem + ext, "w", encoding="utf-8").write(text)
        return stem

    def expect(label, arm, want_invalid, needle="", case="zh-sick-pay", **over):
        ran.append(label)
        stem = write_run(arm, case=case, **over)
        problems, notes, _ = check_run(stem, arm, case, "1", rules)
        got = bool(problems)
        if got != want_invalid or (needle and not any(needle in p for p in problems + notes)):
            fails.append("%s: problems=%s notes=%s" % (label, problems, notes))

    sh_call = {"type": "tool_call", "callId": "c1", "tool": "pwsh"}
    web_call = {"type": "tool_call", "callId": "w1", "tool": "web_fetch"}
    for arm in ("gv-plain", "gv-grav-base", "gv-grav-c4"):
        for case in ("zh-sick-pay", "en-529-roth", "ja-medical-deduction", "ko-severance-pay"):
            expect("good %s %s" % (arm, case), arm, False, case=case,
                   tools=[sh_call, {"type": "tool_result", "callId": "c1", "status": "completed", "result": "1"}])
    expect("exit missing", "gv-plain", True, "exit missing", exit=False)
    expect("exit 1", "gv-grav-c4", True, "exit 1", exit="1\n")
    expect("blank final", "gv-plain", True, "blank", txt="  \n")
    expect("final file missing", "gv-plain", True, "blank", txt=False)
    expect("no final event", "gv-grav-base", True, "no final event", final_event=False)
    expect("wrong cwd", "gv-plain", True, "cwd", cwd="W:\\x\\r4-zh-sick-pay.gv-grav-c4.r1")
    expect("missing cwd", "gv-plain", True, "cwd", cwd="")
    expect("shell broken", "gv-grav-c4", True, "shell broken",
           tools=[sh_call, {"type": "tool_result", "callId": "c1", "status": "error", "result": "Error: SetNamedSecurityInfoW failed (Win32 5)"}])
    expect("network down", "gv-plain", True, "network down",
           tools=[web_call, {"type": "tool_result", "callId": "w1", "status": "error", "result": "Error: web fetch failed: TypeError: fetch failed"}])
    expect("partial network is a note", "gv-plain", False, "network error",
           tools=[web_call, {"type": "tool_result", "callId": "w1", "status": "error", "result": "Error: web fetch failed: TypeError: fetch failed"},
                  {"type": "tool_call", "callId": "w2", "tool": "web_search"}, {"type": "tool_result", "callId": "w2", "status": "completed", "result": "ok"}])
    expect("constrained language is a note", "gv-plain", False, "constrained",
           tools=[sh_call, {"type": "tool_result", "callId": "c1", "status": "completed", "result": "[stderr]\nInvalidOperation: Cannot create type. Only core types are supported in this language mode."}])
    expect("plugin stderr", "gv-grav-base", True, "plugin message", err="dsh-gravitas: rule log: EPERM\n")
    expect("plugin stderr in plain", "gv-plain", True, "plugin message", err="dsh-gravitas: something\n")
    expect("other stderr is a note", "gv-plain", False, "stderr", err="something else\n")
    expect("plain with rule log", "gv-plain", True, "plain run left", rule={"language": "zh-CN", "ruleFile": None, "sha256": "x"})
    expect("plain with empty rule log", "gv-plain", True, "plain run left", rule=None)
    expect("grav rule log missing", "gv-grav-c4", True, "rule log missing", rule=None)
    sha_base, _ = rules["zh"]["gv-grav-base"]
    sha_c4, rf_c4 = rules["zh"]["gv-grav-c4"]
    expect("c4 arm ran the base rule", "gv-grav-c4", True, "rule sha", rule={"language": "zh-CN", "ruleFile": rf_c4, "sha256": sha_base})
    expect("base arm ran the c4 rule", "gv-grav-base", True, "rule sha", rule={"language": "zh-CN", "ruleFile": None, "sha256": sha_c4})
    expect("wrong language", "gv-grav-base", True, "rule language", rule={"language": "en", "ruleFile": None, "sha256": sha_base})
    expect("c4 without ruleFile", "gv-grav-c4", True, "ruleFile", rule={"language": "zh-CN", "ruleFile": None, "sha256": sha_c4})
    expect("unknown arm", "gv-grav", True, "unknown arm", rule={"language": "zh-CN", "ruleFile": None, "sha256": sha_base})
    # 9. account and search failures; non-2xx pages are a note
    ws = lambda cid, status, res: [{"type": "tool_call", "callId": cid, "tool": "web_search", "input": {"queries": ["x"]}},
                                   {"type": "tool_result", "callId": cid, "status": status, "result": res}]
    expect("account sign-in rejected", "gv-plain", True, "account or quota",
           tools=ws("s1", "error", "Error: DeepSeek rejected the account sign-in (HTTP 401)") + ws("s2", "completed", "ok"))
    expect("quota exhausted", "gv-grav-c4", True, "account or quota",
           tools=ws("s1", "error", "Error: HTTP 429 too many requests") + ws("s2", "completed", "ok"))
    expect("every search failed", "gv-grav-base", True, "search down",
           tools=ws("s1", "error", "Error: provider error") + ws("s2", "error", "Error: provider error"))
    expect("one search failed is fine", "gv-plain", False, tools=ws("s1", "error", "Error: provider error") + ws("s2", "completed", "ok"))
    expect("403 page is a note", "gv-plain", False, "4xx/5xx",
           tools=[{"type": "tool_call", "callId": "f1", "tool": "web_fetch", "input": {"url": "https://x.example"}},
                  {"type": "tool_result", "callId": "f1", "status": "completed", "result": "Fetched https://x.example (HTTP 403)\n\nbody"}])
    # 10. reach outside the run's own folder
    call = lambda tool, inp: [{"type": "tool_call", "callId": "t1", "tool": tool, "input": inp},
                              {"type": "tool_result", "callId": "t1", "status": "completed", "result": "x"}]
    expect("read a key", "gv-plain", True, "reached outside",
           tools=call("pwsh", {"command": "Get-Content W:\\AgentData\\logs\\gravitas-dsh-ab4\\keys\\zh-sick-pay.md"}))
    expect("read keypoints by relative path", "gv-grav-c4", True, "reached outside",
           tools=call("read", {"path": "..\\..\\..\\gravitas-dsh-ab4\\keypoints\\zh-sick-pay.json"}))
    expect("climb above the folder", "gv-plain", True, "reached outside", tools=call("pwsh", {"command": "Get-ChildItem ../"}))
    expect("list the environment", "gv-grav-base", True, "reached outside", tools=call("pwsh", {"command": "Get-ChildItem env:"}))
    expect("printenv", "gv-plain", True, "reached outside", tools=call("bash", {"command": "printenv"}))
    expect("own folder is fine", "gv-plain", False,
           tools=call("write", {"path": "W:\\AgentData\\logs\\gravitas-dsh-ab3\\cwd\\r4-zh-sick-pay.gv-plain.r1\\calc.py", "content": "1+1"}))
    expect("own folder in /w/ form is fine", "gv-grav-c4", False,
           tools=call("bash", {"command": "cat /w/AgentData/logs/gravitas-dsh-ab3/cwd/r4-zh-sick-pay.gv-grav-c4.r1/calc.py"}))
    expect("another run's folder is not", "gv-plain", True, "reached outside",
           tools=call("read", {"path": "W:\\AgentData\\logs\\gravitas-dsh-ab3\\cwd\\r4-zh-sick-pay.gv-grav-c4.r1\\notes.md"}))
    expect("web search for keys is fine", "gv-plain", False, tools=ws("s1", "completed", "ok") + [
        {"type": "tool_call", "callId": "q", "tool": "web_search", "input": {"queries": ["AgentData keypoints ../"]}},
        {"type": "tool_result", "callId": "q", "status": "completed", "result": "ok"}])
    # 8. ledger
    od = "W:\\AgentData\\logs\\gravitas-dsh-ab4\\raw"
    row = lambda stem="zh-sick-pay.gv-plain.r1", folder="/w/AgentData/logs/gravitas-dsh-ab4/raw", sid="session-a", fz="f" * 16: [stem, folder, "1", "2", "0", fz, sid]
    for label, rows, rerun, sid, needle in [
            ("ledger: no attempt", [], False, "session-a", "0 attempts"),
            ("ledger: two attempts without a rerun", [row(), row(sid="session-b")], False, "session-b", "2 attempts"),
            ("ledger: three attempts with a rerun", [row(), row(), row()], True, "session-a", "3 attempts"),
            ("ledger: session differs", [row(sid="session-x")], False, "session-a", "ledger session"),
            ("ledger: freeze hash differs", [row(fz="0" * 16)], False, "session-a", "freeze hash"),
            ("ledger: another folder's attempt does not count", [row(folder="/w/AgentData/logs/gravitas-dsh-ab4/tuning")], False, "session-a", "0 attempts")]:
        ran.append(label)
        got = ledger_problems(rows, "zh-sick-pay.gv-plain.r1", od, rerun, sid, "f" * 16)
        if not any(needle in g for g in got):
            fails.append("%s: %s" % (label, got))
    for label, rows, rerun, sid in [("ledger: one attempt", [row()], False, "session-a"),
                                    ("ledger: rerun has two", [row(), row(sid="session-b")], True, "session-b")]:
        ran.append(label)
        got = ledger_problems(rows, "zh-sick-pay.gv-plain.r1", od, rerun, sid, "f" * 16)
        if got:
            fails.append("%s: %s" % (label, got))
    # Every check fails on a run with no files at all.
    problems, _, _ = check_run(os.path.join(tmp, "nothing.gv-grav-c4.r1"), "gv-grav-c4", "zh-nothing", "1", rules)
    for needle in ("exit missing", "blank", "ndjson missing", "no final event", "cwd", "rule log missing"):
        ran.append("empty run " + needle)
        if not any(needle in p for p in problems):
            fails.append("empty run: %r not reported (%s)" % (needle, problems))
    problems, _, _ = check_run(os.path.join(tmp, "nothing.gv-plain.r1"), "gv-plain", "zh-nothing", "1", rules)
    for needle in ("exit missing", "blank", "ndjson missing", "no final event", "cwd"):
        ran.append("empty plain run " + needle)
        if not any(needle in p for p in problems):
            fails.append("empty plain run: %r not reported (%s)" % (needle, problems))
    # The rule-file check itself: a changed c4 file or a c4 sentence leaking into base is caught.
    fake_b = os.path.join(tmp, "b")
    shutil.copytree(os.path.join(B, "rules"), os.path.join(fake_b, "rules"))
    shutil.copy(os.path.join(B, "expected-rule-hashes.json"), fake_b)
    with open(os.path.join(fake_b, "rules", "change4", "en.md"), "a", encoding="utf-8") as fh:
        fh.write("\nextra line\n")
    _, probs = expected_rules(fake_b, W)
    ran.append("changed c4 file")
    if not any("en c4 sha" in p for p in probs):
        fails.append("changed c4 rule file not caught: %s" % probs)
    exp = json.load(open(os.path.join(fake_b, "expected-rule-hashes.json"), encoding="utf-8"))
    exp["ja"]["c4Sentence"] = "not in any rule"
    exp["ko"]["c4Sentence"] = "Gravitas"  # a word every rule has: present in base
    json.dump(exp, open(os.path.join(fake_b, "expected-rule-hashes.json"), "w", encoding="utf-8"))
    _, probs = expected_rules(fake_b, W)
    ran.extend(["missing sentence", "sentence in base", "real rule files"])
    if not any("ja c4 sentence missing" in p for p in probs):
        fails.append("missing c4 sentence not caught: %s" % probs)
    if not any("ko c4 sentence present in the base" in p for p in probs):
        fails.append("c4 sentence in base not caught: %s" % probs)
    shutil.rmtree(tmp, ignore_errors=True)
    print("self-test: %d checks, %d failed" % (len(ran), len(fails)))
    for f in fails:
        print("  FAIL " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main(tuning="--tuning" in sys.argv, archive="--archive-invalid" in sys.argv))
