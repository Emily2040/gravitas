#!/usr/bin/env python3
"""Tests for plugin/skills/gravitas/scripts/provenance_check.py.

Run with plain `python tests/scripts/test_provenance_check.py`. Every case builds an
Antigravity-style conversation (transcript_full.jsonl plus .system_generated/steps/)
in a temporary directory, runs the checker on an answer, and checks the summary
line, the exit status and the notes. Prints one PASS or FAIL line per case and
exits 1 if any case fails.

Set PROVENANCE_CHECK to another copy of the script to run the same cases against it.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.environ.get("PROVENANCE_CHECK") or os.path.normpath(
    os.path.join(HERE, "..", "..", "plugin", "skills", "gravitas", "scripts", "provenance_check.py"))
SUMMARY = re.compile(r"labels checked: (\d+), holding: (\d+), warnings: (\d+), failing: (\d+)")


class Conv(object):
    """An Antigravity conversation: rows of transcript_full.jsonl and files under steps/."""

    def __init__(self, conv_id="c0ffee00-0000-4000-8000-000000000001"):
        self.id, self.rows, self.files = conv_id, [], {}

    def _row(self, **kw):
        kw.setdefault("status", "DONE")
        kw["step_index"] = len(self.rows)
        self.rows.append(kw)
        return kw["step_index"]

    def user(self, text):
        self._row(type="USER_INPUT", content="<USER_REQUEST>\n%s\n</USER_REQUEST>" % text)

    def calls(self, *calls):
        """Each call is (name, args, result dict). The result dict holds status, content, files."""
        self._row(type="PLANNER_RESPONSE", tool_calls=[{"name": n, "args": a} for n, a, _ in calls])
        for _, _, res in calls:
            i = self._row(type="GENERIC", status=res.get("status", "DONE"), content=res.get("content", ""),
                          **({"error": res["error"]} if "error" in res else {}))
            for name, text in (res.get("files") or {}).items():
                self.files[(i, name)] = text
        self._row(type="EPHEMERAL_MESSAGE", content="ephemeral note")

    def call(self, name, args, **res):
        self.calls((name, args, res))

    def answer(self, text):
        self._row(type="PLANNER_RESPONSE", content=text)

    def write(self, home):
        base = os.path.join(home, ".gemini", "antigravity-cli", "brain", self.id, ".system_generated")
        os.makedirs(os.path.join(base, "logs"), exist_ok=True)
        path = os.path.join(base, "logs", "transcript_full.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for r in self.rows:
                f.write(json.dumps(r) + "\n")
        for (i, name), text in self.files.items():
            d = os.path.join(base, "steps", str(i))
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write(text)
        return path, os.path.join(base, "steps")


def fetch(url, text=None, **res):
    """A read_url_content call whose page is saved to steps/<i>/content.md, as current builds do."""
    return ("read_url_content", {"Url": url},
            dict({"content": "Title: Live Content\n\nThe full content of the article at %s has been saved to: "
                             "STEPDIR\n\nYou can use the view_file tool." % url,
                  "files": {"content.md": text} if text is not None else {}}, **res))


def run(conv, answer, args=None, home=None, encoding="utf-8"):
    tmp = tempfile.mkdtemp(prefix="provtest-")
    try:
        home = home or os.path.join(tmp, "home")
        path, _ = conv.write(home)
        ans = os.path.join(tmp, "answer.md")
        with open(ans, "w", encoding="utf-8") as f:
            f.write(answer)
        env = dict(os.environ, HOME=home, USERPROFILE=home, PYTHONIOENCODING=encoding)
        env.pop("PYTHONUTF8", None)
        cmd = [sys.executable, SCRIPT, ans] + (args if args is not None else ["--transcript", path])
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        out = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n")  # Windows text-mode stdout
        return p.returncode, out, p.stderr.decode("utf-8", "replace")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


CASES = []


def case(name):
    def wrap(fn):
        CASES.append((name, fn))
        return fn
    return wrap


def expect(out, code, holding, warnings, failing, contains=(), absent=()):
    m = SUMMARY.search(out)
    if not m:
        return "no summary line in output"
    got = tuple(int(x) for x in m.groups()[1:])
    problems = []
    if got != (holding, warnings, failing):
        problems.append("holding/warnings/failing = %s, wanted %s" % (got, (holding, warnings, failing)))
    want_code = 1 if failing else 0
    if code != want_code:
        problems.append("exit %d, wanted %d" % (code, want_code))
    problems += ["missing %r" % s for s in contains if s not in out]
    problems += ["unexpected %r" % s for s in absent if s in out]
    return "; ".join(problems)


PAGE = ("The committee met on Tuesday. The committee finally approved the budget for next year "
        "after a long debate about road repairs and library hours.")
OTHER = "Unrelated text about the weather in spring and the migration of birds across the valley."


# ---- 1. URLs match exactly after normalisation -------------------------------------------

@case("url: label citing a page deeper than the one opened fails NOT OPENED")
def _():
    c = Conv()
    c.calls(fetch("https://site.org", PAGE))
    code, out, _ = run(c, "x `read (https://site.org/deep/page)`")
    return expect(out, code, 0, 0, 1, ["NOT OPENED: https://site.org/deep/page"])


@case("url: label citing the parent of an opened page is a warning")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/deep/page", PAGE))
    code, out, _ = run(c, "x `read (https://site.org)`")
    return expect(out, code, 0, 1, 0, ["PARENT PAGE: https://site.org"])


@case("url: sibling sharing a prefix (page vs page2) is not the same page")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/page", PAGE))
    code, out, _ = run(c, "x `read (https://site.org/page2)`")
    return expect(out, code, 0, 0, 1, ["NOT OPENED: https://site.org/page2"])


@case("url: case, trailing slash, fragment, http/https and www. are normalised")
def _():
    c = Conv()
    c.calls(fetch("http://www.Site.org/Page/#top", PAGE))
    code, out, _ = run(c, "x `read (https://site.org/page)` and `observed (https://SITE.org/page/#intro)`")
    return expect(out, code, 2, 0, 0)


@case("url: parentheses inside a URL are kept (old behaviour holds)")
def _():
    c = Conv()
    c.calls(fetch("https://en.wikipedia.org/wiki/Mercury_(planet)", PAGE))
    code, out, _ = run(c, 'x `read (https://en.wikipedia.org/wiki/Mercury_(planet), '
                          '"The committee finally approved the budget for next year")`')
    return expect(out, code, 1, 0, 0)


@case("url: a URL seen only in a search summary is SEARCH-ONLY (old behaviour holds)")
def _():
    c = Conv()
    c.call("search_web", {"query": "budget"},
           content="The search for budget returned the following summary: see https://news.org/budget-2026 ...")
    code, out, _ = run(c, "x `read (https://news.org/budget-2026)`")
    return expect(out, code, 0, 0, 1, ["SEARCH-ONLY: https://news.org/budget-2026"])


@case("url: a label with no URL or path fails NO LOCATOR (old behaviour holds)")
def _():
    c = Conv()
    code, out, _ = run(c, "x `read (Smith, Annual Report, 2019)`")
    return expect(out, code, 0, 0, 1, ["NO LOCATOR"])


# ---- 2. A failed fetch is not an opened page ------------------------------------------------

@case("fetch: read_url_content with status ERROR fails FETCH FAILED")
def _():
    c = Conv()
    c.call("read_url_content", {"Url": "https://site.org/x"}, status="ERROR",
           error="Failed to fetch document content at https://site.org/x: status code 403",
           content="Encountered error in step execution: Failed to fetch document content at https://site.org/x")
    code, out, _ = run(c, "x `read (https://site.org/x)`")
    return expect(out, code, 0, 0, 1, ["FETCH FAILED: https://site.org/x"])


@case("fetch: view_file with status ERROR fails FETCH FAILED")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "C:\\work\\missing.md"}, status="ERROR",
           content="Encountered error in step execution: file not found")
    code, out, _ = run(c, "x `observed (C:\\work\\missing.md)`")
    return expect(out, code, 0, 0, 1, ["FETCH FAILED"])


@case("fetch: calls in one response are paired with their own results, in order")
def _():
    c = Conv()
    c.calls(("read_url_content", {"Url": "https://a.org/one"},
             {"status": "ERROR", "content": "Encountered error in step execution: Failed to fetch document "
                                            "content at https://a.org/one"}),
            ("read_url_content", {"Url": "https://a.org/two"}, {"content": PAGE}))
    code, out, _ = run(c, 'x `read (https://a.org/one)` y `read (https://a.org/two, '
                          '"The committee finally approved the budget for next year")`')
    return expect(out, code, 1, 0, 1, ["FETCH FAILED: https://a.org/one"])


# ---- 3. Quotes are compared with the cited source ------------------------------------------

@case("quote: text found only in the user's own message fails QUOTE NOT IN CITED SOURCE")
def _():
    c = Conv()
    c.user("My friend says the quick brown fox jumps over the lazy dog every single morning.")
    c.calls(fetch("https://site.org/a", OTHER))
    code, out, _ = run(c, 'x `read (https://site.org/a, "the quick brown fox jumps over the lazy dog")`')
    return expect(out, code, 0, 0, 1, ["QUOTE NOT IN CITED SOURCE", "https://site.org/a"])


@case("quote: text from page B cited to page A fails QUOTE NOT IN CITED SOURCE")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/a", OTHER))
    c.calls(fetch("https://site.org/b", PAGE))
    code, out, _ = run(c, 'x `read (https://site.org/a, "The committee finally approved the budget for next year")`')
    return expect(out, code, 0, 0, 1, ["QUOTE NOT IN CITED SOURCE"])


@case("quote: text in the cited page's content.md holds (old behaviour holds)")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/a", PAGE))
    code, out, _ = run(c, 'x `read (https://site.org/a, "The committee finally approved the budget for next year")`')
    return expect(out, code, 1, 0, 0)


@case("quote: text only in steps/<i>/output.txt of the cited fetch holds")
def _():
    c = Conv()
    c.call("read_url_content", {"Url": "https://site.org/big"},
           content="Output too large; the full output is in the step's output.txt",
           files={"output.txt": PAGE})
    code, out, _ = run(c, 'x `read (https://site.org/big, "The committee finally approved the budget for next year")`')
    return expect(out, code, 1, 0, 0)


@case("quote: a quote that is 60-90% present is a REFORMATTED warning (old behaviour holds)")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/a", PAGE))
    code, out, _ = run(c, 'x `read (https://site.org/a, "The committee finally approved the budget for next '
                          'year after a short chat")`')
    return expect(out, code, 0, 1, 0, ["QUOTE REFORMATTED"])


@case("quote: text absent everywhere fails QUOTE NOT FOUND (old behaviour holds)")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/a", PAGE))
    code, out, _ = run(c, 'x `read (https://site.org/a, "the mayor resigned in disgrace over the scandal")`')
    return expect(out, code, 0, 0, 1, ["QUOTE NOT FOUND in anything fetched"])


@case("quote: a quote that appears only in the answer itself is not evidence (old behaviour holds)")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/a", OTHER))
    ans = 'x `read (https://site.org/a, "the mayor resigned in disgrace over the scandal")`'
    c.answer(ans)
    code, out, _ = run(c, ans)
    return expect(out, code, 0, 0, 1, ["QUOTE NOT FOUND"])


@case("quote: view_file line numbers do not break a quote that spans lines")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "C:\\work\\minutes.md"},
           content="File Path: `file:///C:/work/minutes.md`\n1: The committee finally\n2: approved the budget "
                   "for next year")
    code, out, _ = run(c, 'x `read (C:\\work\\minutes.md, "The committee finally approved the budget for next year")`')
    return expect(out, code, 1, 0, 0)


@case("quote: a label citing a fetched page's saved content.md path uses the full page")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/a", PAGE))
    tmp_home = tempfile.mkdtemp(prefix="provtest-home-")
    try:
        steps = os.path.join(tmp_home, ".gemini", "antigravity-cli", "brain", c.id, ".system_generated", "steps")
        saved = os.path.join(steps, "1", "content.md")
        c.rows[1]["content"] = c.rows[1]["content"].replace("STEPDIR", saved)
        code, out, _ = run(c, 'x `read (%s, "The committee finally approved the budget for next year")`' % saved,
                           home=tmp_home)
    finally:
        shutil.rmtree(tmp_home, ignore_errors=True)
    return expect(out, code, 1, 0, 0)


# ---- 4. executed labels compare the whole command ------------------------------------------

@case("executed: same script, different subcommand does not hold")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "python ledger.py add F1"}, content="The command exited with code 0.")
    code, out, _ = run(c, "x `executed (python ledger.py verdict F1 -> refuted)`")
    return expect(out, code, 0, 1, 0, ["PARAPHRASED"])


@case("executed: a run_command with status ERROR (denied) did not run")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "python deploy.py --prod"}, status="ERROR",
           content="Encountered error in step execution: permission check failed for command python deploy.py --prod")
    code, out, _ = run(c, "x `executed (python deploy.py --prod -> deployed)`")
    return expect(out, code, 0, 0, 1, ["NOT RUN", "returned an error"])


@case("executed: quote style and whitespace are ignored")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": 'python -c "print(1+1)"'}, content="2")
    code, out, _ = run(c, "x `executed (python -c 'print(1 + 1)' -> 2)`")
    return expect(out, code, 1, 0, 0)


@case("executed: a script path is reduced to its base name (old behaviour holds)")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": 'python "C:\\work\\scratch\\run.py" --n 3'}, content="42")
    code, out, _ = run(c, "x `executed (python scratch/run.py --n 3 -> 42)`")
    return expect(out, code, 1, 0, 0)


@case("executed: one whole command of a && chain holds (old behaviour holds)")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "cd /d C:\\work && python run.py"}, content="ok")
    code, out, _ = run(c, "x `executed (python run.py -> ok)`")
    return expect(out, code, 1, 0, 0)


@case("executed: the command shown without the arguments that ran is PARAPHRASED")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "python run.py --n 3 --seed 9"}, content="ok")
    code, out, _ = run(c, "x `executed (python run.py -> ok)`")
    return expect(out, code, 0, 1, 0, ["PARAPHRASED"])


@case("executed: a command nothing resembles fails NOT RUN (old behaviour holds)")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "dir"}, content="ok")
    code, out, _ = run(c, "x `executed (python other_tool.py --flag -> 7)`")
    return expect(out, code, 0, 0, 1, ["NOT RUN: no run_command resembles"])


# ---- 5. POSIX and ~/ paths are locators; matching is exact or on a segment boundary --------

@case("path: a POSIX absolute path is a locator and matches view_file")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "/home/user/notes/x.md"}, content="1: hello")
    code, out, _ = run(c, "x `observed (/home/user/notes/x.md)`")
    return expect(out, code, 1, 0, 0)


@case("path: a ~/ path is a locator and matches the expanded home path")
def _():
    tmp_home = tempfile.mkdtemp(prefix="provtest-home-")
    try:
        c = Conv()
        c.call("view_file", {"AbsolutePath": os.path.join(tmp_home, "proj", "a.md")}, content="1: hello")
        code, out, _ = run(c, "x `observed (~/proj/a.md)`", home=tmp_home)
    finally:
        shutil.rmtree(tmp_home, ignore_errors=True)
    return expect(out, code, 1, 0, 0)


@case("path: a POSIX path never opened fails NOT OPENED")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "/home/user/other.md"}, content="1: hello")
    code, out, _ = run(c, "x `observed (/home/user/notes/x.md)`")
    return expect(out, code, 0, 0, 1, ["NOT OPENED: /home/user/notes/x.md"])


@case("path: fractions and and/or are not paths")
def _():
    c = Conv()
    code, out, _ = run(c, "x `read (1/102 of cases and/or 3/4 of the rest)`")
    return expect(out, code, 0, 0, 1, ["NO LOCATOR"], ["NOT OPENED"])


@case("path: the path part of a URL is not a separate path")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/deep/page", PAGE))
    code, out, _ = run(c, "x `read (https://site.org/deep/page)`")
    return expect(out, code, 1, 0, 0, [], ["/deep/page"])


@case("path: a suffix that is not on a segment boundary does not match")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "C:\\work\\myproj\\notes.md"}, content="1: hello")
    code, out, _ = run(c, "x `observed (file:///proj/notes.md)`")
    return expect(out, code, 0, 0, 1, ["NOT OPENED"])


@case("path: a suffix on a segment boundary matches")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "C:\\work\\proj\\notes.md"}, content="1: hello")
    code, out, _ = run(c, "x `observed (/work/proj/notes.md)`")
    return expect(out, code, 1, 0, 0)


@case("path: Windows path with other slashes and case matches (old behaviour holds)")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "C:\\Work\\Notes.md"}, content="1: hello")
    code, out, _ = run(c, "x `observed (c:/work/notes.md)` and `observed (file:///C:/Work/Notes.md)`")
    return expect(out, code, 2, 0, 0)


# ---- command line --------------------------------------------------------------------------

@case("cli: --conversation and --latest find the transcript under ~/.gemini (old behaviour holds)")
def _():
    tmp_home = tempfile.mkdtemp(prefix="provtest-home-")
    try:
        c = Conv("deadbeef-1111-4222-8333-444455556666")
        c.calls(fetch("https://site.org/a", PAGE))
        problems = []
        for args in (["--conversation", c.id], ["--latest"]):
            code, out, _ = run(c, "x `read (https://site.org/a)`", args=args, home=tmp_home)
            p = expect(out, code, 1, 0, 0, [c.id])
            if p:
                problems.append("%s: %s" % (args[0], p))
    finally:
        shutil.rmtree(tmp_home, ignore_errors=True)
    return "; ".join(problems)


@case("cli: non-ASCII label text prints to a stdout that is not UTF-8 without crashing")
def _():
    # PYTHONIOENCODING=ascii stands in for a redirected Windows stdout (cp1252 and the like),
    # on every platform: printing the label below would raise UnicodeEncodeError.
    c = Conv()
    code, out, err = run(c, "x `read (https://no.org/東京 → café)`", encoding="ascii")
    if "UnicodeEncodeError" in err:
        return "UnicodeEncodeError on stdout"
    return expect(out, code, 0, 0, 1, ["NOT OPENED", "東京"])


@case("cli: a missing transcript exits 2")
def _():
    code, out, err = run(Conv(), "x", args=["--transcript", os.path.join(tempfile.gettempdir(), "no-such.jsonl")])
    return "" if code == 2 else "exit %d, wanted 2 (%s)" % (code, (err or out).strip()[-120:])


@case("cli: output keeps the summary line and FAIL/WARN blocks (old behaviour holds)")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/a", PAGE))
    c.call("run_command", {"CommandLine": "python run.py --n 3"}, content="ok")
    code, out, _ = run(c, "x `read (https://site.org/a)` `read (https://no.org/x)` `executed (python run.py -> ok)`")
    problems = [expect(out, code, 1, 1, 1)]
    if not re.search(r"^transcript: .+transcript_full\.jsonl$", out, re.M):
        problems.append("no transcript line")
    if not re.search(r"^FAIL  read \(https://no\.org/x\)\n      NOT OPENED: https://no\.org/x$", out, re.M):
        problems.append("FAIL block format changed")
    if not re.search(r"^WARN  executed \(python run\.py -> ok\)\n      PARAPHRASED", out, re.M):
        problems.append("WARN block format changed")
    return "; ".join(x for x in problems if x)


# ---------------------------------------------------------------- follow-ups from the verifier

@case("follow-up: an ERROR result after a system step between it and the call still fails")
def _():
    c = Conv()
    c._row(type="PLANNER_RESPONSE", tool_calls=[{"name": "read_url_content", "args": {"Url": "https://site.org/a"}}])
    c._row(type="SYSTEM_MESSAGE", content="a system note")
    c._row(type="GENERIC", status="ERROR", content="Encountered error in step execution: Failed to fetch")
    code, out, _ = run(c, "x `read (https://site.org/a)`")
    return expect(out, code, 0, 0, 1, contains=["FETCH FAILED"])


@case("follow-up: a call with no result step did not succeed")
def _():
    c = Conv()
    c._row(type="PLANNER_RESPONSE", tool_calls=[{"name": "run_command", "args": {"CommandLine": "python run.py"}}])
    code, out, _ = run(c, "x `executed (python run.py -> ok)`")
    return expect(out, code, 0, 0, 1)


@case("follow-up: 'saved to' text inside a page body does not mark a path as opened")
def _():
    c = Conv()
    c.calls(fetch("https://site.org/a", "The file has been saved to: C:\\secret\\notes.md and more text here."))
    code, out, _ = run(c, "x `observed (C:\\secret\\notes.md)`")
    return expect(out, code, 0, 0, 1, contains=["NOT OPENED"])


@case("follow-up: an exact command that contains => holds")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "node -e \"[1,2].map(x => x * 2)\""}, content="ok")
    code, out, _ = run(c, "x `executed (node -e \"[1,2].map(x => x * 2)\" -> ok)`")
    return expect(out, code, 1, 0, 0)


@case("follow-up: a flag that differs only in case does not hold")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "ls -r"}, content="ok")
    code, out, _ = run(c, "x `executed (ls -R -> ok)`")
    return expect(out, code, 0, 1, 0)


@case("follow-up: arguments that differ only by a space are different commands")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "python calc.py 100"}, content="ok")
    code, out, _ = run(c, "x `executed (python calc.py 1 00 -> ok)`")
    return "" if "holding: 0" in out else "a different argument list held: " + out


@case("follow-up: one line of a heredoc body is not a command that ran")
def _():
    c = Conv()
    c.call("run_command", {"CommandLine": "python - <<'EOF'\nprint(6 * 7)\nEOF"}, content="42")
    code, out, _ = run(c, "x `executed (print(6 * 7) -> 42)`")
    return "" if "holding: 0" in out else "a heredoc body line held: " + out


@case("follow-up: an absolute one-segment path does not match a file deeper down")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "/home/u/proj/README.md"}, content="1: hello")
    code, out, _ = run(c, "x `observed (/README.md)`")
    return expect(out, code, 0, 0, 1)


@case("follow-up: a made-up quote in Japanese fails, a real one holds")
def _():
    c = Conv()
    c.calls(fetch("https://site.jp/a", "この法律は二千二十年から施行される。罰則は別に定める。"))
    code, out, _ = run(c, "x `read (https://site.jp/a, \"この法律は二千二十年から施行される\")` "
                          "`read (https://site.jp/a, \"この法律は明日から廃止される予定です\")`")
    return expect(out, code, 1, 0, 1)


@case("follow-up: malformed transcript rows are skipped, not crashed on")
def _():
    c = Conv()
    c.call("view_file", {"AbsolutePath": "C:\\work\\a.md"}, content="1: hello")
    c.rows.append("not an object")
    c.rows.append({"type": "PLANNER_RESPONSE", "tool_calls": {"name": "view_file", "args": "oops"}})
    code, out, err = run(c, "x `observed (C:\\work\\a.md)`")
    if "Traceback" in err:
        return "crashed: " + err[-200:]
    return expect(out, code, 1, 0, 0)


@case("follow-up: a default port is the same page")
def _():
    c = Conv()
    c.calls(fetch("https://example.com/page", "Some page text that is long enough."))
    code, out, _ = run(c, "x `read (https://example.com:443/page)`")
    return expect(out, code, 1, 0, 0)


def main():
    print("script: %s" % SCRIPT)
    failed = 0
    for name, fn in CASES:
        try:
            problem = fn()
        except Exception as e:  # a crash in a case is a failure of that case
            problem = "crashed: %r" % e
        print("%s  %s%s" % ("FAIL" if problem else "PASS", name, ("  -- " + problem) if problem else ""))
        failed += bool(problem)
    print("\n%d cases, %d passed, %d failed" % (len(CASES), len(CASES) - failed, failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
