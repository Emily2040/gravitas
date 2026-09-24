#!/usr/bin/env python3
"""Tests for plugin/skills/gravitas/scripts/slopcheck.py.

Run with plain `python tests/scripts/test_slopcheck.py`. Each case prints one
PASS or FAIL line; the exit status is 1 if any case fails. Set SLOPCHECK to a
different script path to run the same cases against another copy (for
example the pre-fix version).
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SCRIPT = os.environ.get("SLOPCHECK") or os.path.join(
    REPO, "plugin", "skills", "gravitas", "scripts", "slopcheck.py")

# A paragraph that trips nothing: varied sentence lengths, short anchors, no
# em-dash, no banned vocabulary, no questions.
CLEAN = (
    "Load the file first. The installer copies every script into the plugin "
    "directory, checks that Python 3.8 or later is on the path, and then writes "
    "a manifest that records the version and the time of the install so that a "
    "later run can compare the two values. It exits with status 2 on failure. "
    "Logs go to the temp folder.\n"
)

RESULTS = []


def run(files, args=()):
    """Write files into a temp dir, run the script on them, return (code, out)."""
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, text in files.items():
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            paths.append(p)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, SCRIPT] + list(args) + paths,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        out = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
        out = out.replace(chr(13) + chr(10), chr(10))
        return r.returncode, out


def flag_lines(out):
    return [l.strip() for l in out.splitlines() if l.strip().startswith("FLAG")]


def case(name, ok, detail=""):
    RESULTS.append(ok)
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


def check(name, text, want=(), avoid=(), args=()):
    """Run on one file; every regex in want must match a FLAG line, none in avoid."""
    code, out = run({"doc.md": text}, args)
    flags = flag_lines(out)
    missing = [w for w in want if not any(re.search(w, f) for f in flags)]
    present = [a for a in avoid if any(re.search(a, f) for f in flags)]
    ok = code == 0 and not missing and not present and "Traceback" not in out
    detail = "exit %d; missing %s; unexpected %s; flags %s" % (code, missing, present, flags)
    case(name, ok, detail)


def main():
    # Baseline: the clean fixture really is clean.
    code, out = run({"clean.md": CLEAN})
    case("baseline: clean fixture prints no FLAG and exits 0",
         code == 0 and not flag_lines(out), out)

    # ---- Defect 1: --strict ------------------------------------------------
    code, out = run({"doc.md": CLEAN + "This is vital.\n"}, ["--strict"])
    case("strict: exits 1 when a FLAG is printed",
         code == 1 and "FLAG banned word: vital" in out and "Traceback" not in out, out)

    code, out = run({"clean.md": CLEAN}, ["--strict"])
    case("strict: exits 0 when nothing is flagged",
         code == 0 and "== " in out and not flag_lines(out), "exit %d\n%s" % (code, out))

    code, out = run({"a.md": CLEAN, "b.md": CLEAN + "We delve in.\n"}, ["--strict"])
    case("strict: exits 1 when any one of several files is flagged",
         code == 1 and out.count("== ") == 2 and "Traceback" not in out, out)

    code, out = run({"doc.md": CLEAN + "This is vital.\n"})
    case("default: exits 0 even with FLAG lines (compatibility)",
         code == 0 and "FLAG banned word: vital" in out, out)

    r = subprocess.run([sys.executable, SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    case("default: no arguments prints nothing and exits 0",
         r.returncode == 0 and not r.stdout.strip(), r.stdout + r.stderr)

    # ---- Defect 2: word boundaries ----------------------------------------
    check("banned: 'vitality' does not fire 'vital'", CLEAN + "Their vitality shows.\n",
          avoid=[r"banned word: vital\b"])
    check("banned: 'in shortage' does not fire 'in short'", CLEAN + "Staff are in shortage.\n",
          avoid=[r"banned word: in short\b"])
    check("banned: 'fosterage' and 'realmente' do not fire", CLEAN + "Fosterage ends. Es realmente.\n",
          avoid=[r"banned word: foster\b", r"banned word: realm\b"])
    check("banned: bare 'vital' still fires with a count", CLEAN + "It is vital. Vital, too.\n",
          want=[r"banned word: vital x2$"])
    check("banned: inflections still fire (leveraged, leveraging, utilizes)",
          CLEAN + "We leveraged it. We are leveraging it. It utilizes it.\n",
          want=[r"banned word: leverage x2$", r"banned word: utilize x1$"])
    check("banned: multi-word phrase across a line break", CLEAN + "We will circle\nback.\n",
          want=[r"banned word: circle back x1$"])

    # ---- Defect 3: any em-dash ---------------------------------------------
    long_text = CLEAN * 6 + "The build takes four minutes — longer on Windows.\n"
    code, out = run({"doc.md": long_text})
    rate = re.search(r"em-dashes 1 \((\d+\.\d) per 1000 words\)", out)
    case("em-dash: a single dash at under 6 per 1,000 words is flagged",
         code == 0 and rate is not None and float(rate.group(1)) < 6
         and any("em-dash" in f for f in flag_lines(out)), out)
    case("em-dash: the rate line is still printed", rate is not None, out)
    check("em-dash: none present, no em-dash FLAG", CLEAN, avoid=[r"em-dash"])
    check("em-dash: a dash inside fenced code is ignored",
          CLEAN + "```\na — b\n```\n", avoid=[r"em-dash"])

    # ---- Defect 4: conclusion crutches ------------------------------------
    check("crutch: 'In conclusion,' fires", CLEAN + "In conclusion, it works.\n",
          want=[r"conclusion crutch: in conclusion x1$"])
    check("crutch: 'to sum up', 'in summary', 'all in all', 'at the end of the day' fire",
          CLEAN + "To sum up, it works. In summary it is fine. All in all, good. "
          "At the end of the day, ship it.\n",
          want=[r"crutch: to sum up", r"crutch: in summary", r"crutch: all in all",
                r"crutch: at the end of the day"])
    check("crutch: sentence-opening 'Ultimately,' fires",
          CLEAN + "Ultimately, the fix was a flag. It shipped. Ultimately, we moved on.\n",
          want=[r"conclusion crutch: ultimately, x2$"])
    check("crutch: 'ultimately' mid-sentence does not fire",
          CLEAN + "The value ultimately depends on the cache.\n",
          avoid=[r"ultimately"])
    check("crutch: word boundaries hold ('in conclusions')",
          CLEAN + "They erred in conclusions drawn.\n",
          avoid=[r"crutch"])

    # ---- Defect 5: questions in quotations, blockquotes, fences -------------
    check("question: inside straight double quotes is ignored",
          CLEAN + 'He asked "why does it fail?" and we checked the logs.\n',
          avoid=[r"rhetorical question"])
    check("question: a whole quoted prompt is ignored",
          CLEAN + 'The user typed "Can you fix the build?" into the chat.\n',
          avoid=[r"rhetorical question"])
    check("question: inside curly double quotes is ignored",
          CLEAN + "The model replied “Should I retry?” and stopped.\n",
          avoid=[r"rhetorical question"])
    check("question: inside single quotes is ignored",
          CLEAN + "She wrote 'is it cached?' in the ticket.\n",
          avoid=[r"rhetorical question"])
    check("question: quote spanning a wrapped line is ignored",
          CLEAN + 'The prompt was "Why does the\ninstaller fail?" and nothing else.\n',
          avoid=[r"rhetorical question"])
    check("question: inside a tilde fence is ignored",
          CLEAN + "~~~\nWhat is this?\n~~~\n",
          avoid=[r"rhetorical question"])
    check("question: inside a backtick fence is ignored",
          CLEAN + "```text\nIs this code?\n```\n",
          avoid=[r"rhetorical question"])
    check("fence: an unclosed fence is flagged and the text after it is still checked",
          CLEAN + "```\nWhy does this matter? Because the cache is cold.\n",
          want=[r"unclosed code fence at line", r"rhetorical question: Why does this matter"])
    check("words: derived forms still fire (seamlessly, robustness, crucially)",
          CLEAN + "It works seamlessly. Its robustness is crucially important.\n",
          want=[r"banned word: seamless", r"banned word: robust", r"banned word: crucial"])
    check("quotes: an inch mark does not open a quote that hides a question",
          CLEAN + 'The panel is 12" wide. Why does it sag? Because the frame is thin. It holds 3 kg.\n',
          want=[r"rhetorical question: Why does it sag"])
    check("crutch: a hard-wrapped line starting with ultimately, is not a crutch",
          CLEAN + "The migration will move the tables and the indexes and\nultimately, the views.\n",
          avoid=[r"conclusion crutch: ultimately"])
    check("crutch: a sentence opening Ultimately, still fires",
          CLEAN + "The tables moved. Ultimately, the views did too.\n",
          want=[r"conclusion crutch: ultimately"])
    check("em-dash: an HTML entity counts",
          CLEAN + "One thing &mdash; then another.\n",
          want=[r"em-dashes present \(1\)"])
    check("question: on a blockquote line is ignored",
          CLEAN + "> Why does it fail?\n",
          avoid=[r"rhetorical question"])
    check("question: an unquoted question answered by the writer still fires",
          CLEAN + "Why does this matter? Because the cache is cold.\n",
          want=[r"rhetorical question: Why does this matter\?"])
    check("question: apostrophes do not hide a real question",
          CLEAN + "It's the users' call. Why doesn't it work? It's broken.\n",
          want=[r"rhetorical question: Why doesn't it work\?"])
    check("question: a question after a closed quote still fires",
          CLEAN + 'He said "done." Is it done? Not yet.\n',
          want=[r"rhetorical question: .*Is it done\?"])
    check("question: checklist items are still exempt, including quoted terms",
          CLEAN + "- Is the cache warm?\n- Does the \"fast\" option work?\n",
          avoid=[r"rhetorical question"])

    # ---- Old behaviour that must hold -------------------------------------
    code, out = run({"doc.md": CLEAN})
    case("output: header, sentences, em-dash and bold-lead lines unchanged",
         re.search(r"^== [^\n]*doc\.md ==$", out, re.M) is not None
         and re.search(r"^   sentences \d+ \| mean [\d.]+ \| stdev [\d.]+ \| short\(<=8\) \d+ "
                       r"\| long\(>=25\) \d+  \(words\)$", out, re.M) is not None
         and re.search(r"^   em-dashes 0 \(0\.0 per 1000 words\)$", out, re.M) is not None
         and re.search(r"^   bold-lead lines 0 \(colon-style 0\) \| bullets 0$", out, re.M) is not None,
         out)
    check("old: contrastive framing still fires",
          CLEAN + "It's not a bug, it's a docs issue.\n", want=[r"^FLAG contrastive:"])
    check("old: hedge intensifier still fires",
          CLEAN + "This is genuinely fast.\n", want=[r"^FLAG hedge/intensifier: genuinely$"])
    check("old: uniform sentence length still fires",
          "One two three four five six seven eight nine ten. " * 6 + "\n",
          want=[r"uniform sentence length", r"no short anchor sentences"])
    check("old: bolded colon lead-ins still fire",
          CLEAN + "- **A long bolded lead in:** text\n- **Another long lead here:** text\n",
          want=[r"bolded colon lead-in"])

    cjk = ("这是一个测试文档。"
           "它包含很多中文句子，"
           "用来检查脚本的行为。"
           "脚本应该跳过英文检查。 "
           "vital in conclusion genuinely\n")
    code, out = run({"zh.md": cjk})
    case("cjk: skips contrastive/hedge/vocabulary/crutch checks and says so",
         code == 0 and "[CJK]" in out
         and "note: contrastive/hedge/vocabulary checks are English-only and were skipped" in out
         and not any(k in out for k in ("banned word", "hedge/intensifier", "crutch", "contrastive:")),
         out)

    failed = RESULTS.count(False)
    print("%d/%d passed" % (len(RESULTS) - failed, len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
