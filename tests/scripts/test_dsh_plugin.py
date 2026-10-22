#!/usr/bin/env python3
"""Tests for the DeepSeek Harness plugin in dsh/.

Run with plain `python tests/scripts/test_dsh_plugin.py`. Each case prints
one PASS or FAIL line; the exit status is 1 if any case fails.

The plugin is JavaScript, so its behaviour is tested with Node's own test
runner (dsh/test/plugin.test.js): the manifest and patch, every language's
skill, rule and platform note, the presets' tool limits, and config checks.
This script runs that suite when Node.js 22 or later is installed, and checks
here that every file under dsh/ that the plugin needs is listed in
package.json "files", so a packed install cannot miss one.
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RESULTS = []


def case(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


def listed(rel, files):
    for f in files:
        if f.endswith("/") and rel.startswith(f):
            return True
        if "*" in f and re.fullmatch(re.escape(f).replace(r"\*", "[^/]*"), rel):
            return True
        if rel == f:
            return True
    return False


def main():
    with open(os.path.join(REPO, "package.json"), encoding="utf-8") as fh:
        pkg = json.load(fh)
    files = pkg["files"]
    needed = []
    for root, _dirs, names in os.walk(os.path.join(REPO, "dsh")):
        for n in names:
            rel = os.path.relpath(os.path.join(root, n), REPO).replace(os.sep, "/")
            if rel.startswith("dsh/test/"):
                continue
            needed.append(rel)
    missing = [r for r in needed if not listed(r, files)]
    case("package.json files lists every runtime file under dsh/", not missing, ", ".join(missing))
    case("package.json ships dist/, which the plugin reads", "dist/" in files)

    node = shutil.which("node")
    if not node:
        print("SKIP the Node test suite: node is not installed")
    else:
        v = subprocess.run([node, "--version"], stdout=subprocess.PIPE).stdout.decode().strip()
        major = int(v.lstrip("v").split(".")[0]) if v.startswith("v") else 0
        if major < 22:
            print("SKIP the Node test suite: node %s is older than 22" % v)
        else:
            r = subprocess.run([node, "--test", "dsh/test/plugin.test.js"], cwd=REPO,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = r.stdout.decode("utf-8", "replace")
            m = re.search(r"pass (\d+)\D+fail (\d+)", out.replace("ℹ", ""))
            case("the Node suite passes (%s)" % (m and "%s passed, %s failed" % m.groups() or "no summary"),
                 r.returncode == 0, out[-1500:])

    failed = RESULTS.count(False)
    print("%d/%d passed" % (len(RESULTS) - failed, len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
