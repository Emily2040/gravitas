#!/usr/bin/env python3
"""Tests for check_skills.py's verifier-tool rule and the refuter's verdict schema.

Run with plain Python (no pytest):

    python tests/scripts/test_check_skills.py

Prints one PASS or FAIL line per case and exits 1 if any case fails.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHECK = os.path.join(ROOT, "plugin", "skills", "gravitas", "scripts", "check_skills.py")
BUILD = os.path.join(ROOT, "scripts", "build_agents.py")
SCHEMA = os.path.join(ROOT, "plugin", "skills", "gravitas", "schemas", "verdict.schema.json")
AGENTS_DIR = os.path.join(ROOT, "plugin", "agents")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cs = load("check_skills_under_test", CHECK)
ba = load("build_agents_under_test", BUILD)

RESULTS = []
TMP = tempfile.mkdtemp(prefix="gravitas-test-check-skills-")


def case(name, fn):
    try:
        ok, detail = fn()
    except Exception as exc:  # a crash is a failure, not an abort
        ok, detail = False, "%s: %s" % (type(exc).__name__, exc)
    RESULTS.append(ok)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  -- " + detail))


# ---------------------------------------------------------------- defect 1

def write_agent(name, tools, description="Does a job.", enabled=None):
    d = os.path.join(TMP, "agents-%d" % len(os.listdir(TMP)))
    os.makedirs(d)
    lines = ["---", 'name: "%s"' % name, 'description: "%s"' % description, "tools:"]
    lines += ["  - %s" % t for t in tools]
    if enabled:
        lines += ["enabledTools:"] + ["  - %s" % t for t in enabled]
    lines += ['model: "flash"', "---", "", "Body.", ""]
    path = os.path.join(d, name + ".md")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    return path


INDEPENDENCE = re.compile(r"not independent")


def independence_problems(path):
    rep = cs.Report(strict=True)
    cs.check_agent(path, rep)
    return [m for _, m in rep.problems if INDEPENDENCE.search(m)]


def expect_broken(name, tools, **kw):
    def fn():
        probs = independence_problems(write_agent(name, tools, **kw))
        return bool(probs), "no independence problem reported for %s with %s" % (name, tools)
    return fn


def expect_clean(name, tools, **kw):
    def fn():
        probs = independence_problems(write_agent(name, tools, **kw))
        return not probs, "unexpected: %s" % probs
    return fn


for role in ("refuter", "reader", "finder", "scout"):
    case("defect1: gravitas-%s holding write_to_file is BROKEN" % role,
         expect_broken("gravitas-" + role, ["view_file", "write_to_file"]))
case("defect1: gravitas-reviewer holding replace_file_content is BROKEN",
     expect_broken("gravitas-reviewer", ["view_file", "replace_file_content"]))
case("defect1: gravitas-verifier holding multi_replace_file_content is BROKEN",
     expect_broken("gravitas-verifier", ["view_file", "multi_replace_file_content"]))
case("defect1: agent described as Read-only (any name) holding write_to_file is BROKEN",
     expect_broken("gravitas-summariser", ["view_file", "write_to_file"],
                   description="Summarises a report. Read-only."))
case("defect1: 'read only' spelling in description is also caught",
     expect_broken("helper", ["replace_file_content"], description="A read only helper."))
case("defect1: gravitas-checker holding write_to_file is BROKEN",
     expect_broken("gravitas-checker", ["view_file", "run_command", "write_to_file"]))
case("defect1: write tool granted via enabledTools on a refuter is BROKEN",
     expect_broken("gravitas-refuter", ["view_file"], enabled=["write_to_file"]))
case("defect1: role match is case-insensitive (Gravitas-Finder)",
     expect_broken("Gravitas-Finder", ["write_to_file"]))

case("kept: gravitas-checker may hold run_command",
     expect_clean("gravitas-checker", ["view_file", "run_command"]))
case("kept: a critic holding run_command is BROKEN",
     expect_broken("gravitas-visual-critic", ["view_file", "run_command"]))
case("kept: a critic holding write_to_file is BROKEN",
     expect_broken("gravitas-completeness-critic", ["view_file", "write_to_file"]))
case("kept: a refuter holding only read tools is clean",
     expect_clean("gravitas-refuter", ["view_file", "grep_search", "read_url_content", "search_web"]))
case("kept: a non-verifier builder agent may hold write tools",
     expect_clean("gravitas-builder", ["view_file", "write_to_file", "run_command"],
                  description="Builds the site from the plan."))
case("kept: a non-critic verifier may hold run_command without write tools",
     expect_clean("gravitas-reviewer", ["view_file", "run_command"]))


def critic_message_unchanged():
    rep = cs.Report(strict=True)
    cs.check_agent(write_agent("gravitas-visual-critic", ["view_file", "run_command"]), rep)
    msgs = [m for _, m in rep.problems]
    return msgs == ["a critic with write or command tools is not independent"], "got %s" % msgs


case("kept: critic message text unchanged and reported once", critic_message_unchanged)


def shipped_agents_clean():
    bad = {}
    for e in sorted(os.listdir(AGENTS_DIR)):
        if e.endswith(".md"):
            probs = independence_problems(os.path.join(AGENTS_DIR, e))
            if probs:
                bad[e] = probs
    return not bad, "shipped agents flagged: %s" % bad


case("kept: every shipped agent in plugin/agents passes the rule", shipped_agents_clean)


def cli_reports_broken():
    pdir = os.path.join(TMP, "cliplugin")
    os.makedirs(os.path.join(pdir, "agents"))
    with open(os.path.join(pdir, "plugin.json"), "w", encoding="utf-8") as fh:
        json.dump({"name": "cliplugin"}, fh)
    shutil.copy(write_agent("gravitas-scout", ["list_dir", "write_to_file"]),
                os.path.join(pdir, "agents", "gravitas-scout.md"))
    env = dict(os.environ, HOME=TMP, USERPROFILE=TMP)  # keep ~/.gemini/config out of it
    p = subprocess.run([sys.executable, CHECK, pdir], capture_output=True, text=True, env=env)
    lines = [l for l in p.stdout.splitlines() if "BROKEN" in l and "gravitas-scout" in l]
    ok = p.returncode == 1 and lines and re.match(r"^  BROKEN  \S", lines[0]) and "FAIL:" in p.stdout
    return bool(ok), "exit %s, stdout: %s" % (p.returncode, p.stdout)


case("cli: check_skills.py DIR exits 1 with a BROKEN line for a writing scout", cli_reports_broken)


# ---------------------------------------------------------------- defect 2

def validate(obj, schema):
    """The subset of JSON Schema that verdict.schema.json uses."""
    errs = []
    if not isinstance(obj, dict):
        return ["not an object"]
    for k in schema.get("required", []):
        if k not in obj:
            errs.append("missing required %r" % k)
    props = schema.get("properties", {})
    for k, v in obj.items():
        if k not in props:
            if schema.get("additionalProperties") is False:
                errs.append("additional property %r" % k)
            continue
        p = props[k]
        if "enum" in p and v not in p["enum"]:
            errs.append("%r=%r not in %s" % (k, v, p["enum"]))
        if p.get("type") == "string" and not isinstance(v, str):
            errs.append("%r is not a string" % k)
    return errs


with open(SCHEMA, encoding="utf-8") as fh:
    VERDICT = json.load(fh)
REFUTER = [a for a in ba.AGENTS if a["name"] == "gravitas-refuter"][0]


def inline_example(agent):
    m = re.search(r"```json\n(.*?)\n```", agent["body"], re.S)
    return json.loads(m.group(1))


def schema_has_status_and_error():
    props = VERDICT["properties"]
    ok = (sorted(props.get("status", {}).get("enum", [])) == ["blocked", "done"]
          and props.get("error", {}).get("type") == "string"
          and VERDICT.get("additionalProperties") is False)
    return ok, "status=%s error=%s" % (props.get("status"), props.get("error"))


case("defect2: verdict.schema.json declares status (done|blocked) and error (string)",
     schema_has_status_and_error)


def refuter_inline_has_status():
    ex = inline_example(REFUTER)
    return ex.get("status") == "done" and "error" in ex, "refuter example: %s" % ex


case("defect2: refuter's inline example carries status and error", refuter_inline_has_status)


def refuter_inline_valid():
    errs = validate(inline_example(REFUTER), VERDICT)
    return not errs, "; ".join(errs)


case("kept: refuter's inline example validates against verdict.schema.json", refuter_inline_valid)


def blocked_verdict_valid():
    blocked = {"status": "blocked", "key": "k1", "refuted": "blocked", "tier": "inferred",
               "reason": "The prompt gave a relative path.", "error": "relative path: src/a.py"}
    errs = validate(blocked, VERDICT)
    return not errs, "; ".join(errs)


case("defect2: a refuter following the shared blocked instructions passes the schema",
     blocked_verdict_valid)


def inline_keys_match_schema():
    ex = set(inline_example(REFUTER))
    props = set(VERDICT["properties"])
    return ex == props, "inline-only %s, schema-only %s" % (sorted(ex - props), sorted(props - ex))


case("kept: refuter's inline fields and the schema's fields are the same set", inline_keys_match_schema)


def every_evidence_agent_has_status_error():
    missing = []
    for a in ba.AGENTS:
        if a.get("evidence", True):
            ex = inline_example(a)
            if "status" not in ex or "error" not in ex:
                missing.append(a["name"])
    return not missing, "missing status/error: %s" % missing


case("defect2: every agent given the shared blocked rule shows status and error", every_evidence_agent_has_status_error)


def generated_files_in_sync():
    stale = []
    for a in ba.AGENTS:
        path = os.path.join(AGENTS_DIR, a["name"] + ".md")
        with open(path, encoding="utf-8", newline="") as fh:
            if fh.read() != ba.render(a):
                stale.append(a["name"])
    return not stale, "regenerate with build_agents.py: %s" % stale


case("kept: plugin/agents/*.md match build_agents.py output", generated_files_in_sync)


def generated_refuter_has_status():
    with open(os.path.join(AGENTS_DIR, "gravitas-refuter.md"), encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    ex = json.loads(m.group(1))
    return ex.get("status") == "done" and not validate(ex, VERDICT), "generated example: %s" % ex


case("defect2: generated gravitas-refuter.md example has status and validates", generated_refuter_has_status)


def old_verdict_still_valid():
    old = {"key": "k1", "refuted": "no", "lens": "correctness", "tier": "read",
           "source": "a.py:3", "reason": "The call is there.", "error": ""}
    errs = validate(old, VERDICT)
    return not errs, "; ".join(errs)


case("kept: a verdict without status is still valid (status is optional)", old_verdict_still_valid)


def unknown_field_rejected():
    errs = validate({"key": "k", "refuted": "yes", "tier": "read", "reason": "r", "extra": 1}, VERDICT)
    return any("additional property 'extra'" in e for e in errs), "errors: %s" % errs


case("kept: the schema still rejects unknown fields", unknown_field_rejected)


def bad_status_rejected():
    errs = validate({"key": "k", "refuted": "yes", "tier": "read", "reason": "r", "status": "SUCCESS"}, VERDICT)
    return any("status" in e for e in errs), "errors: %s" % errs


case("kept: status outside done|blocked is rejected", bad_status_rejected)


# ---------------------------------------------------------------- follow-ups from the verifier

def write_raw_agent(name, frontmatter_lines):
    d = os.path.join(TMP, "raw-%d" % len(os.listdir(TMP)))
    os.makedirs(d)
    path = os.path.join(d, name + ".md")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(["---", 'name: "%s"' % name, 'description: "Does a job."']
                           + frontmatter_lines + ['model: "flash"', "---", "", "Body.", ""]))
    return path


def odd_type_reported(field, value):
    def fn():
        rep = cs.Report(strict=True)
        cs.check_agent(write_raw_agent("gravitas-scout", ["tools:", "  - view_file", "%s: %s" % (field, value)]), rep)
        msgs = [m for _, m in rep.problems]
        return any("must be a list" in m for m in msgs), "problems: %s" % msgs
    return fn


case("follow-up: enabledTools: true is reported, not a crash", odd_type_reported("enabledTools", "true"))
case("follow-up: enabledTools: 5 is reported, not a crash", odd_type_reported("enabledTools", "5"))


def tools_scalar_reported():
    rep = cs.Report(strict=True)
    cs.check_agent(write_raw_agent("gravitas-reader", ["tools: 5"]), rep)
    msgs = [m for _, m in rep.problems]
    return any("must be a list" in m for m in msgs), "problems: %s" % msgs


case("follow-up: tools: 5 is reported, not a crash", tools_scalar_reported)
case("follow-up: a role word inside another word (proofreader) is not a verifier",
     expect_clean("proofreader", ["view_file", "write_to_file"], description="Fixes typos in drafts."))
case("follow-up: 'Not read-only' in a description does not mark the agent read-only",
     expect_clean("gravitas-builder", ["view_file", "write_to_file"],
                  description="Not read-only: it edits files."))
case("follow-up: a non-breaking hyphen in read-only is still caught",
     expect_broken("helper", ["write_to_file"], description="A read‑only helper."))


def read_only_command_noted():
    rep = cs.Report(strict=True)
    cs.check_agent(write_agent("gravitas-summariser", ["view_file", "run_command"],
                               description="Summarises a report. Read-only."), rep)
    notes = [m for _, m in rep.notes]
    return any("read-only is an instruction" in m for m in notes), "notes: %s" % notes


case("follow-up: a read-only agent holding run_command gets a note", read_only_command_noted)


shutil.rmtree(TMP, ignore_errors=True)
failed = RESULTS.count(False)
print("%d passed, %d failed" % (len(RESULTS) - failed, failed))
sys.exit(1 if failed else 0)
