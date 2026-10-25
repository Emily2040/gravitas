#!/usr/bin/env python3
"""Test validity5.py --tuning N on made-up runs in a temporary folder under tests/ (standard library only).

    python tests/validity_tuning_test.py

validity5.main() is called with b set to the temporary folder, whose freeze.sh is a stub, so the real freeze.sh
(which reads W:\\AgentData\\dsh_home) is never run. Checks: pass N reads tuning-schedule-N.txt and writes
validity-tuning-N.json; --archive-invalid moves pass N's invalid runs to tuning/attempt1/ and writes
rerun-schedule-tuning-N.txt and reruns-tuning-N.json; pass 1 and pass 2 keep separate files; a pass-2 run archived
once is allowed two ledger attempts; the command line refuses --tuning without 1 or 2.
"""
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROUND = os.path.dirname(HERE)
sys.path.insert(0, ROUND)
import validity5 as v  # noqa: E402

res = []


def expect(label, cond, info=""):
    print(("[ok]  " if cond else "[BAD] ") + label + (("  -- " + str(info)) if info and not cond else ""))
    res.append(bool(cond))


T = os.path.join(HERE, ".tmp-validity-tuning-%d" % os.getpid())
try:
    os.makedirs(os.path.join(T, "tuning"))
    shutil.copytree(os.path.join(ROUND, "rules"), os.path.join(T, "rules"))
    shutil.copy(os.path.join(ROUND, "expected-rule-hashes.json"), T)
    with open(os.path.join(T, "freeze.sh"), "w", newline="\n") as f:
        f.write('#!/bin/sh\necho "head: stub"\n')
    with open(os.path.join(T, "freeze-start.txt"), "w", newline="\n") as f:
        f.write("label: start\ntime: now\nhead: stub\n")
    rules, probs = v.expected_rules(T, v.W)
    expect("the copied rule files match expected-rule-hashes.json", not probs, probs)
    fz = __import__("hashlib").sha256(open(os.path.join(T, "freeze-start.txt"), "rb").read()).hexdigest()[:16]
    sha, rf = rules["en"]["gv-grav-c5"]

    def write_run(case, rnd, sid, good=True):
        stem = os.path.join(T, "tuning", "%s.gv-grav-c5.r%s" % (case, rnd))
        cwd = "W:\\AgentData\\logs\\gravitas-dsh-ab3\\cwd\\r5-%s.gv-grav-c5.r%s" % (case, rnd)
        ev = [{"type": "session", "cwd": cwd, "sessionId": sid}, {"type": "final", "text": "answer"}]
        open(stem + ".ndjson", "w", encoding="utf-8").write("\n".join(json.dumps(e) for e in ev) + "\n")
        open(stem + ".txt", "w", encoding="utf-8").write("answer")
        open(stem + ".err", "w", encoding="utf-8").write("")
        open(stem + ".rule.jsonl", "w", encoding="utf-8").write(json.dumps({"language": "en", "ruleFile": rf, "sha256": sha}) + "\n")
        if good:
            open(stem + ".exit", "w", encoding="utf-8").write("0\n")
        with open(os.path.join(T, "run-ledger.tsv"), "a", encoding="utf-8", newline="\n") as f:
            f.write("\t".join(["%s.gv-grav-c5.r%s" % (case, rnd), "/w/x/tuning".replace("/w/x", T.replace("\\", "/")),
                               "1", "2", "0", fz, sid]) + "\n")

    for n in ("1", "2"):
        with open(os.path.join(T, "tuning-schedule-%s.txt" % n), "w", newline="\n") as f:
            f.write("gv-grav-c5 en-a %s\ngv-grav-c5 en-b %s\n" % (n, n))
    write_run("en-a", "1", "s-a1")
    write_run("en-b", "1", "s-b1", good=False)          # no .exit: invalid
    code = v.main(tuning="1", archive=True, b=T, w=v.W)
    rep = json.load(open(os.path.join(T, "validity-tuning-1.json"), encoding="utf-8"))
    expect("pass 1 reads tuning-schedule-1.txt (its 2 runs)", sorted(rep["runs"]) == ["en-a.gv-grav-c5.r1", "en-b.gv-grav-c5.r1"],
           sorted(rep["runs"]))
    expect("pass 1: the run without .exit is invalid, the good one is not",
           rep["invalid"] == ["en-b.gv-grav-c5.r1"] and not rep["runs"]["en-a.gv-grav-c5.r1"]["problems"], rep["runs"])
    expect("pass 1 exits 1 (an invalid run; the round checks also fail on the stub)", code == 1, code)
    expect("pass 1 --archive-invalid moves the invalid run to tuning/attempt1/",
           os.path.exists(os.path.join(T, "tuning", "attempt1", "en-b.gv-grav-c5.r1.ndjson"))
           and not os.path.exists(os.path.join(T, "tuning", "en-b.gv-grav-c5.r1.ndjson")))
    expect("pass 1 writes rerun-schedule-tuning-1.txt", open(os.path.join(T, "rerun-schedule-tuning-1.txt")).read()
           == "gv-grav-c5 en-b 1\n")
    expect("pass 1 writes reruns-tuning-1.json", json.load(open(os.path.join(T, "reruns-tuning-1.json"))) == ["en-b.gv-grav-c5.r1"])
    expect("pass 1 writes no unnumbered tuning files", not any(os.path.exists(os.path.join(T, f)) for f in
           ("validity-tuning.json", "rerun-schedule-tuning.txt", "reruns-tuning.json")))
    # pass 2: en-a fails once, is archived, rerun (a second ledger attempt), and then counts as rerun
    write_run("en-a", "2", "s-a2", good=False)
    write_run("en-b", "2", "s-b2")
    v.main(tuning="2", archive=True, b=T, w=v.W)
    rep2 = json.load(open(os.path.join(T, "validity-tuning-2.json"), encoding="utf-8"))
    expect("pass 2 reads tuning-schedule-2.txt", sorted(rep2["runs"]) == ["en-a.gv-grav-c5.r2", "en-b.gv-grav-c5.r2"], sorted(rep2["runs"]))
    expect("pass 2 keeps its own files (pass 1's report and rerun list unchanged)",
           json.load(open(os.path.join(T, "validity-tuning-1.json"), encoding="utf-8")) == rep
           and open(os.path.join(T, "rerun-schedule-tuning-1.txt")).read() == "gv-grav-c5 en-b 1\n"
           and open(os.path.join(T, "rerun-schedule-tuning-2.txt")).read() == "gv-grav-c5 en-a 2\n")
    write_run("en-a", "2", "s-a2b")                      # the one rerun
    v.main(tuning="2", archive=False, b=T, w=v.W)
    rep2 = json.load(open(os.path.join(T, "validity-tuning-2.json"), encoding="utf-8"))
    expect("pass 2: the rerun run has two ledger attempts allowed and is valid",
           rep2["runs"]["en-a.gv-grav-c5.r2"]["rerun"] is True and not rep2["runs"]["en-a.gv-grav-c5.r2"]["problems"],
           rep2["runs"]["en-a.gv-grav-c5.r2"])
    for argv, label in ((["--tuning"], "--tuning without a pass number"), (["--tuning", "3"], "--tuning 3"),
                        (["--tuning", "--archive-invalid"], "--tuning followed by another flag")):
        p = subprocess.run([sys.executable, "-B", os.path.join(ROUND, "validity5.py")] + argv, capture_output=True, text=True)
        expect("command line refuses %s" % label, p.returncode == 1 and "1 or 2" in p.stderr, (p.returncode, p.stderr))
finally:
    shutil.rmtree(T, ignore_errors=True)
print("validity5 --tuning test: %d assertions, %d failed" % (len(res), res.count(False)))
sys.exit(0 if all(res) else 1)
