#!/usr/bin/env python3
"""Tests for plugin/skills/gravitas/scripts/narration_check.py.

Run with plain `python tests/scripts/test_narration_check.py`. Each case prints
one PASS or FAIL line; the exit status is 1 if any case fails.

The bad samples are the shapes found in the runs audited for 1.1: a first-person
check with nothing behind it, a passive one, a verification announced complete,
and a reasoning step that held four of them. The good samples carry the source
in the same sentence, as 01-evidence.md requires.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SCRIPT = os.path.join(REPO, "plugin", "skills", "gravitas", "scripts", "narration_check.py")
sys.path.insert(0, os.path.dirname(SCRIPT))
import narration_check as nc  # noqa: E402

RESULTS = []


def case(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


def run(files, args=()):
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, text in files.items():
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            paths.append(p)
        r = subprocess.run([sys.executable, "-I", SCRIPT] + list(args) + paths, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        return r.returncode, r.stdout.decode("utf-8", "replace")


BAD_STEP = ("I verified the transitions between every shot. I compared both versions frame by frame. "
            "I confirmed the overlay text is identical in each. The timing has been validated against the brief.\n")
GOOD = ("executed (ffprobe -show_frames strip_v1.mp4 -> 24 frames): the strip holds 24 frames.\n"
        "I compared the two sheets with `python diff_cells.py v1.jpg v2.jpg`, which printed 4.8 and 1.2.\n"
        "The render ran with exit code 0.\n"
        "I checked /work/app/src/auth/session.ts:97 and the refresh token is not revoked there.\n"
        "Verification is complete for https://example.org/spec, where section 4 gives the limit.\n")


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    got = [s for _, s in nc.flags(BAD_STEP)]
    case("four narrated checks in one step are all flagged", len(got) == 4, repr(got))
    case("a check with its source in the same sentence is not flagged", not nc.flags(GOOD), repr(nc.flags(GOOD)))
    case("a plain sentence with no check verb is not flagged",
         not nc.flags("The installer copies every script into the plugin folder and exits with status 2 on failure."))
    case("'verified' inside a fenced block or a quoted line is not flagged",
         not nc.flags("```text\nI verified it.\n```\n> I verified it.\n\n<!-- I checked -->\nThe end.\n"))
    case("a passive claim with no source is flagged",
         [s for _, s in nc.flags("The figures were checked twice.")] == ["The figures were checked twice."])
    case("'all tests pass' with no source is flagged, and with the command it is not",
         nc.flags("All tests pass now.") and not nc.flags("All tests pass: `pytest -q` printed 41 passed."))
    case("the line number points at the sentence",
         nc.flags("First line.\n\nSecond line here.\nI verified the output.\n") == [(4, "I verified the output.")],
         repr(nc.flags("First line.\n\nSecond line here.\nI verified the output.\n")))
    case("a list item is checked without its marker",
         [s for _, s in nc.flags("- I measured the gap.\n")] == ["I measured the gap."])
    case("the nominal form, 'inspection of the sheet reveals', is flagged without a source and not with one",
         nc.flags("Frame-by-frame inspection of the initial contact sheet reveals a stationary camera.")
         and not nc.flags("Inspection of `TC_S07_v1_frames_000-023.jpg` reveals a stationary camera."))
    case("a sentence in another language is left alone",
         not nc.flags("私は出力を確認しました。所有数字都核对过了。"))

    code, out = run({"bad.md": BAD_STEP})
    case("command line: a narrated answer prints FAIL first, one FLAG per sentence, and exits 1",
         code == 1 and out.startswith("FAIL 4 narrated checks") and out.count("FLAG ") == 4
         and out.count("bad.md:1: ") == 4, out)
    code, out = run({"good.md": GOOD})
    case("command line: a sourced answer prints PASS first and exits 0",
         code == 0 and out.startswith("PASS") and "FLAG" not in out, out)
    r = subprocess.run([sys.executable, "-I", SCRIPT, os.path.join(tempfile.gettempdir(), "no such file.md")],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    case("command line: a missing file prints ERROR and exits 2",
         r.returncode == 2 and r.stdout.decode("utf-8", "replace").startswith("ERROR"), r.stdout[:200])
    r = subprocess.run([sys.executable, "-I", SCRIPT, "-"], input=BAD_STEP.encode("utf-8"), stdout=subprocess.PIPE)
    case("command line: - reads stdin", r.returncode == 1 and b"FLAG -:1:" in r.stdout, r.stdout[:200])

    failed = RESULTS.count(False)
    print("%d/%d passed" % (len(RESULTS) - failed, len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
