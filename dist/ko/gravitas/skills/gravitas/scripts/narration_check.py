#!/usr/bin/env python3
"""List the sentences in an answer that say a check was done and name no source.

Usage: narration_check.py FILE [FILE ...]        (- reads stdin)

The first line is PASS or FAIL, or ERROR when a file cannot be read; the exit
status is 0, 1 or 2. Each FLAG line names the file, the line and the sentence.

The rule it enforces is in 01-evidence.md: a check is a tool event, so a
sentence that says something was verified, compared, measured or confirmed
names the command, the file, the capture or the URL in the same sentence. In
the runs audited for 1.1 the commonest defect was a check that never happened,
written as a done thing ("I verified the transitions", "the output has been
validated") with no tool step behind it. provenance_check.py catches a label
with no retrieval; this catches the sentence that carries no label at all.

A sentence passes when it holds a locator: an evidence label (observed,
executed or read with a bracket), a span in backticks, a URL, a file path, an
exit status, or an arrow from a command to its output. Fenced code, quoted
lines and HTML comments are left out, because they may be someone else's words.
The verbs are English only; a sentence in another language is not checked.
"""
import re
import sys

LABEL = re.compile(r"\b(?:observed|executed|read)`?\*{0,2}\s*\(")
LOCATOR = re.compile(r"`[^`\n]+`|https?://\S+|(?:\b[A-Za-z]:[\\/]|(?<![\w.])/(?=[\w.~-]))[^\s\"'`,;()<>|*]+"
                     r"|\bexit(?: code| status)? \d+\b|->|\bline \d+\b|\bstep \d+\b", re.I)
VERB = r"(?:verif(?:y|ied)|confirm(?:ed)?|check(?:ed)?|double-check(?:ed)?|re-?check(?:ed)?|cross-check(?:ed)?" \
       r"|compar(?:e|ed)|measur(?:e|ed)|inspect(?:ed)?|test(?:ed)?|validat(?:e|ed)|examin(?:e|ed)|review(?:ed)?" \
       r"|ensur(?:e|ed)|made sure|went through|looked (?:at|through|over)|ran|re-?ran)"
NARRATED = [
    re.compile(r"\b(?:I|we)(?:'ve| have| also| then| just| already| carefully| manually)*\s+%s\b" % VERB, re.I),
    re.compile(r"\b(?:has|have|had|was|were|is|are|been|being)\s+(?:also\s+|now\s+|fully\s+|carefully\s+|manually\s+)?"
               r"(?:verified|confirmed|checked|double-checked|re-?checked|cross-checked|compared|measured|inspected"
               r"|tested|validated|examined|reviewed)\b", re.I),
    re.compile(r"\b(?:verification|validation|testing|a? ?(?:quick|full|final) check)\s+(?:is |was |has been )?"
               r"(?:passed|complete|completed|done|successful|finished)\b", re.I),
    re.compile(r"\b(?:all|every|each|both)\s+(?:of the )?(?:checks?|tests?|gates?|cases?|assertions?)\s+(?:now )?"
               r"(?:pass|passed|passes|succeed|succeeded|are green|is green)\b", re.I),
    # the nominal form the audited run used: "frame-by-frame inspection of the sheet reveals ..."
    re.compile(r"\b(?:inspection|examination|comparison|analysis|review|verification|validation|check|measurement)"
               r"(?:\s+of\s+[^,.;]{1,80}?)?\s+(?:reveals|revealed|shows|showed|confirms|confirmed|establishes"
               r"|established|finds|found|verifies|verified|proves|proved)\b", re.I),
]
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?^[ \t]*\1[ \t]*$", re.S | re.M)
COMMENT = re.compile(r"<!--.*?-->", re.S)
QUOTED_LINE = re.compile(r"^[ \t]*>.*$", re.M)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(\[])|\n{2,}")


def blank(m):
    """Replace a match with newlines only, so line numbers stay right."""
    return "\n" * m.group(0).count("\n")


def prose(text):
    text = COMMENT.sub(blank, text)
    text = FENCE.sub(blank, text)
    return QUOTED_LINE.sub("", text)


def sentences(text):
    """(line number, sentence) for every sentence in the prose, Markdown list markers dropped."""
    out = []
    pos = 0
    for m in SENTENCE_END.finditer(text):
        out.append((pos, text[pos:m.start()]))
        pos = m.end()
    out.append((pos, text[pos:]))
    result = []
    for start, s in out:
        s = re.sub(r"^[ \t]*(?:[-*+]|\d+[.)])\s+", "", s.strip())
        s = re.sub(r"\s+", " ", s)
        if s:
            result.append((text.count("\n", 0, start) + 1, s))
    return result


def narrated(sentence):
    """True when the sentence claims a check and names no source."""
    if LABEL.search(sentence) or LOCATOR.search(sentence):
        return False
    return any(p.search(sentence) for p in NARRATED)


def flags(text):
    return [(n, s) for n, s in sentences(prose(text)) if narrated(s)]


def read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    if not argv or any(a.startswith("-") and a != "-" for a in argv):
        print("ERROR usage: narration_check.py FILE [FILE ...]")
        return 2
    found = []
    for path in argv:
        try:
            text = read(path)
        except OSError as exc:
            print("ERROR %s: %s" % (path, exc))
            return 2
        found += [(path, n, s) for n, s in flags(text)]
    print("FAIL %d narrated check%s with no source" % (len(found), "" if len(found) == 1 else "s") if found
          else "PASS no narrated check without a source")
    for path, n, s in found:
        print("FLAG %s:%d: %s" % (path, n, s if len(s) <= 200 else s[:197] + "..."))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
