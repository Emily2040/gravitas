#!/usr/bin/env python3
"""Run every test script as a person does, and fail on anything a green run would hide.

    python .github/scripts/run_tests.py              # tests/scripts/test_*.py, then the Node suite
    python .github/scripts/run_tests.py --self-test  # the rules below, on made-up results

Each tests/scripts/test_*.py is a plain script that prints PASS, FAIL or SKIP lines and exits 1
when a case fails. Run by hand, a SKIP is a courtesy: the machine has no git, no bash or no
Node. On a CI runner every one of those is installed, so a SKIP there means a check did not
run. A script that skips every case still exits 0, and a job that only reads exit codes would
call that a pass. So this runner fails the job for:

1. no test script found;
2. a script that exits with anything but 0;
3. a script whose last line does not say how many cases passed;
4. a SKIP line, unless the operating system is the reason (ALLOWED below);
5. dsh/test present and Node missing, failing, or reporting no test.

It needs only the standard library and runs on Python 3.8.
"""
import glob
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Skips the operating system decides. Each entry is (where it is allowed, text the SKIP line holds).
# "not-windows" means Linux and macOS.
ALLOWED = [
    ("not-windows", "Windows only"),  # the .cmd installer and its PowerShell hook edit
    # The download mark exists on Windows alone, and there only the .cmd clears it, so the
    # .command and .sh cases skip it under Git Bash. Seen in the first Windows run, 2026-11-12.
    ("windows", "only the .cmd clears the Windows mark"),
    # test_installers.py measures each obstacle before it asserts. On GitHub's Windows Server 2025
    # runner these two do not stop Git Bash, which reads the held file and adds to the denied folder
    # (run 43157361928, 2026-11-12), so the .command and .sh cases built on them skip there. The same
    # cases run on the macOS and Linux jobs, where a skip is not allowed. The third obstacle, a file
    # held open in a folder that is then moved, does stop Git Bash, so its skip is not listed.
    ("windows", "a file held open with no sharing does not stop Git Bash"),
    ("windows", "an icacls rule against adding folders does not stop Git Bash"),
]


def skip_allowed(line, platform):
    group = "windows" if platform.startswith("win") else "not-windows"
    return any(where == group and text in line for where, text in ALLOWED)


def last_line(output):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def judge_scripts(results, platform):
    """Problems in the Python results. results is a list of (name, exit code, output)."""
    problems = []
    if not results:
        return ["no test script found under tests/scripts"]
    for name, code, output in results:
        if code != 0:
            problems.append("%s exited %s" % (name, code))
        if "passed" not in last_line(output):
            problems.append("%s gave no count of passed cases; its last line is %r" % (name, last_line(output)[:80]))
        for line in output.splitlines():
            if line.startswith("SKIP ") and not skip_allowed(line, platform):
                problems.append("%s skipped a check this runner can run: %s" % (name, line.strip()[:160]))
    return problems


def judge_node(present, node_found, code, output):
    """Problems in the Node result. present says whether dsh/test holds test files."""
    if not present:
        return []
    if not node_found:
        return ["dsh/test holds tests and node is not installed"]
    problems = []
    if code != 0:
        problems.append("the Node suite exited %s" % code)
    counts = dict((k, int(v)) for k, v in re.findall(r"^(?:#|ℹ) (tests|pass|fail) (\d+)", output, re.M))
    if "tests" not in counts or "pass" not in counts or "fail" not in counts:
        problems.append("the Node suite printed no tests, pass and fail counts")
    elif counts["tests"] == 0 or counts["fail"] != 0 or counts["pass"] != counts["tests"]:
        problems.append("the Node suite reports %(tests)s tests, %(pass)s passed, %(fail)s failed" % counts)
    return problems


def run(cmd):
    r = subprocess.run(cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode("utf-8", "replace")
    sys.stdout.write(out if out.endswith("\n") or not out else out + "\n")
    sys.stdout.flush()
    return r.returncode, out


def main():
    results = []
    for path in sorted(glob.glob(os.path.join(REPO, "tests", "scripts", "test_*.py"))):
        name = os.path.basename(path)
        print("=== %s" % name)
        code, out = run([sys.executable, path])
        results.append((name, code, out))
    problems = judge_scripts(results, sys.platform)

    node_tests = sorted(glob.glob(os.path.join(REPO, "dsh", "test", "*.test.js")))
    node = shutil.which("node")
    code, out = 0, ""
    if node_tests and node:
        print("=== node --test (%d files)" % len(node_tests))
        code, out = run([node, "--test"] + node_tests)
    elif not node_tests:
        print("=== no dsh/test/*.test.js in this tree; the Node suite does not apply")
    problems += judge_node(bool(node_tests), bool(node), code, out)

    print("\n=== summary (%s, Python %s)" % (sys.platform, sys.version.split()[0]))
    for name, code, out in results:
        print("%-28s exit %s  %s" % (name, code, last_line(out)[:90]))
    if node_tests and node:
        print("%-28s exit %s" % ("node --test", code))
    for p in problems:
        print("FAIL %s" % p)
    print("%d problem(s)" % len(problems))
    return 1 if problems else 0


def self_test():
    ok = "PASS a\n3/3 passed\n"
    cases = [
        ("no script at all fails", judge_scripts([], "linux"), True),
        ("a clean script passes", judge_scripts([("t.py", 0, ok)], "linux"), False),
        ("a non-zero exit fails", judge_scripts([("t.py", 1, ok)], "linux"), True),
        ("empty output fails", judge_scripts([("t.py", 0, "")], "linux"), True),
        ("exit 0 with every case skipped fails",
         judge_scripts([("t.py", 0, "SKIP every case  -- needs git and a git checkout\n")], "darwin"), True),
        ("a skip for a missing tool fails beside real passes",
         judge_scripts([("t.py", 0, "SKIP hook  -- Node is not installed\n" + ok)], "linux"), True),
        ("a Windows-only skip passes on Linux",
         judge_scripts([("t.py", 0, "SKIP cmd: every case  -- x.cmd runs on Windows only\n" + ok)], "linux"), False),
        ("a Windows-only skip passes on macOS",
         judge_scripts([("t.py", 0, "SKIP hook  -- Windows only\n" + ok)], "darwin"), False),
        ("a Windows-only skip fails on Windows",
         judge_scripts([("t.py", 0, "SKIP hook  -- Windows only\n" + ok)], "win32"), True),
        ("the download-mark skip passes on Windows",
         judge_scripts([("t.py", 0, "SKIP sh: files unzipped with the download mark  -- only the .cmd clears "
                                    "the Windows mark; the Mac's own mark is tested on a Mac\n" + ok)], "win32"), False),
        ("the download-mark skip fails on Linux, where it never prints",
         judge_scripts([("t.py", 0, "SKIP sh: files unzipped with the download mark  -- only the .cmd clears "
                                    "the Windows mark; the Mac's own mark is tested on a Mac\n" + ok)], "linux"), True),
        ("an obstacle measured not to stop Git Bash is an allowed skip on Windows",
         judge_scripts([("t.py", 0, "SKIP sh: when a file of the download cannot be read  -- a file held "
                                    "open with no sharing does not stop Git Bash on this machine: with it "
                                    "there, Git Bash could still read the file\n" + ok)], "win32"), False),
        ("an obstacle that does not stop cmd fails on Windows",
         judge_scripts([("t.py", 0, "SKIP cmd: when a file of the download cannot be read  -- a file held "
                                    "open with no sharing does not stop cmd on this machine: with it "
                                    "there, cmd could still read the file\n" + ok)], "win32"), True),
        ("the held-plugin obstacle not stopping Git Bash fails on Windows",
         judge_scripts([("t.py", 0, "SKIP sh: with Antigravity holding the installed plugin  -- a program "
                                    "holding a file of the folder open does not stop Git Bash on this "
                                    "machine: with it there, Git Bash could still move the folder\n" + ok)],
                       "win32"), True),
        ("an obstacle that does not stop bash fails on Linux",
         judge_scripts([("t.py", 0, "SKIP sh: when the plugins folder cannot be added to  -- mode 555 on "
                                    "the folder does not stop bash on this machine: with it there, bash "
                                    "could still add a folder to it\n" + ok)], "linux"), True),
        ("the Mac's download mark not taking fails on macOS",
         judge_scripts([("t.py", 0, "SKIP command: files unzipped with the Mac's download mark are "
                                    "installed without it  -- the mark is not in the way on this machine: "
                                    "0 files and folders of the download took it, and a plain cp -R of "
                                    "them kept it on 0\n" + ok)], "darwin"), True),
        ("no Node tests in the tree passes", judge_node(False, False, 0, ""), False),
        ("Node tests without node fails", judge_node(True, False, 0, ""), True),
        ("a Node run with no counts fails", judge_node(True, True, 0, ""), True),
        ("a Node run with zero tests fails", judge_node(True, True, 0, "# tests 0\n# pass 0\n# fail 0\n"), True),
        ("a Node failure fails", judge_node(True, True, 1, "# tests 2\n# pass 1\n# fail 1\n"), True),
        ("fewer passes than tests fails", judge_node(True, True, 0, "# tests 3\n# pass 2\n# fail 0\n"), True),
        ("a clean Node run passes, in either report style",
         judge_node(True, True, 0, "# tests 2\n# pass 2\n# fail 0\n")
         + judge_node(True, True, 0, "ℹ tests 2\nℹ pass 2\nℹ fail 0\n"), False),
    ]
    failed = 0
    for name, problems, want_problem in cases:
        good = bool(problems) == want_problem
        failed += not good
        print("%s %s%s" % ("PASS" if good else "FAIL", name, "" if good else "  -- got %r" % (problems,)))
    print("%d/%d passed" % (len(cases) - failed, len(cases)))
    return 1 if failed else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.exit(self_test() if sys.argv[1:] == ["--self-test"] else main() if not sys.argv[1:] else
             "usage: run_tests.py [--self-test]")
