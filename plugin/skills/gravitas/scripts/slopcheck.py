#!/usr/bin/env python3
"""Detect the structural AI tells that word-level banned-term scans miss.

Checks the prose rules from AGENTS.md: sentence-length variation, contrastive
framing, rhetorical Q&A, conclusion crutches ("in conclusion", "to sum up",
a sentence opening "Ultimately,"), plus em-dashes and bold-lead density that
make text read as machine-generated.

Usage: slopcheck.py [--strict] FILE [FILE ...]

Without --strict the exit status is 0 whatever is found, so agents that
already call it keep working. With --strict it exits 1 when any FLAG line
was printed, so a build can fail on it.
"""
import argparse
import re
import statistics
import sys

BANNED_WORDS = ["delve", "leverage", "foster", "robust", "seamless", "transformative",
                "tapestry", "landscape", "circle back", "unpack", "in short",
                "furthermore", "moreover", "utilize", "crucial", "vital", "realm"]

# Phrases that announce a summary instead of ending on a fact. Matched on word
# boundaries anywhere in the text; "Ultimately," is handled separately because
# it is only a crutch when it opens a sentence.
CONCLUSION_CRUTCHES = ["in conclusion", "in summary", "to sum up", "to summarize",
                       "to summarise", "all in all", "at the end of the day"]

CONTRASTIVE = [
    r"\bnot\s+(?:just|only|merely|simply)\b[^.]*\bbut\b",
    r"\bisn'?t\s+\w+[^.]{0,40}[-\u2014]\s*it'?s\b",
    r"\bit'?s not\b[^.]{0,40}\bit'?s\b",
    r"[^.]{3,60},\s*not\s+\w+[.,]",
    r"\brather than\s+\w+ing\b",
]

HEDGE = r"\b(genuinely|precisely|deliberately|notably|arguably|effectively|essentially|simply put|worth noting|worth stating)\b"


def phrase_pattern(phrase, inflect=False):
    """Word-boundary regex for a banned word or phrase.

    Multi-word phrases tolerate any run of whitespace between words. Single
    words optionally accept inflections and the common derived endings
    (leverages, leveraging, seamlessly, robustness, crucially), so the boundary
    keeps what the old substring match caught, while "vital" no longer fires on
    "vitality" and "foster" no longer fires on "fosterage".
    """
    words = [re.escape(w) for w in phrase.split()]
    body = r"\s+".join(words)
    if inflect and len(words) == 1:
        alts = [body + r"(?:s|es|d|ed|ing|ly|ness|ally|ingly)?"]
        if phrase.endswith("e"):
            alts.append(re.escape(phrase[:-1]) + r"ing")
        body = "(?:%s)" % "|".join(alts)
    return re.compile(r"\b%s\b" % body, re.I)


BANNED_RES = [(w, phrase_pattern(w, inflect=True)) for w in BANNED_WORDS]
CRUTCH_RES = [(w, phrase_pattern(w)) for w in CONCLUSION_CRUTCHES]
# "Ultimately," at the start of a line (after any list, heading or quote
# marker) or after a sentence-ending mark.
ULTIMATELY_RE = re.compile(
    r"(?:^[ \t]*(?:[-*+][ \t]+|\d+[.)][ \t]+|#+[ \t]+)?|[.!?][\"')\]\u201d\u2019]*\s+)"
    r"[*_]*ultimately[*_]*\s*,", re.I | re.M)

def count_ultimately(prose):
    """Sentence-opening "Ultimately,". A line that starts with it counts only when it
    also starts a sentence: after a blank line, a list or heading marker, or a line
    that ended one. A hard-wrapped line in mid-sentence does not."""
    n = 0
    lines = prose.split("\n")
    for m in ULTIMATELY_RE.finditer(prose):
        if prose[m.start()] in ".!?" or m.group(0).lstrip()[:1] in "-*+#" or m.group(0).lstrip()[:1].isdigit():
            n += 1
            continue
        row = prose.count("\n", 0, m.start())
        prev = next((l.strip() for l in reversed(lines[:row]) if l.strip()), "")
        if not prev or row == 0 or re.search(r"[.!?:][\"')\]\u201d\u2019*_]*$", prev) \
                or not lines[row - 1].strip():
            n += 1
    return n


FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def strip_fences(t):
    """Remove fenced code blocks, backtick or tilde. Returns (text, line number of
    a fence still open at the end, or None). The lines after an unclosed fence are
    kept as prose, so one stray fence cannot hide the rest of the file."""
    out = []
    fence = None
    opened_at = None
    held = []
    for n, l in enumerate(t.splitlines(), 1):
        m = FENCE_RE.match(l)
        if fence is None:
            # A backtick fence's info string cannot contain a backtick, so
            # ```x``` on one line is inline code rather than an opening fence.
            if m and not (m.group(1)[0] == "`" and "`" in l.strip()[len(m.group(1)):]):
                fence, opened_at, held = m.group(1), n, []
                out.append("")
                continue
            out.append(l)
        else:
            # A fence closes on a line of the same character, at least as long.
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) \
                    and not l.strip()[len(m.group(1)):].strip():
                fence, held = None, []
            else:
                held.append(l)
            out.append("")
    if fence is not None:
        out = out[:len(out) - len(held)] + held
        return chr(10).join(out), opened_at
    return chr(10).join(out), None


def strip_code(t):
    t, _ = strip_fences(t)
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"`[^`]*`", " ", t)
    # Table rows and blockquotes are tabular or quoted material. A question
    # inside either is data or someone else's words, so it says nothing about
    # this text's own cadence.
    keep = [l for l in t.splitlines()
            if not l.lstrip().startswith("|") and not l.lstrip().startswith(">")]
    return chr(10).join(keep)


# Quoted spans stay inside one paragraph: a stray quote mark must not swallow
# the rest of the document.
_PARA = r"(?:[^{close}\n]|\n(?![ \t]*\n)){{1,400}}?"
# A straight quote mark is ambiguous (12" is an inch mark, '90s an elision), so a
# straight-quoted span may not run past the end of a sentence.
_SENT = r"(?:(?![.!?][\"')\]]*\s+[A-Z])[^{close}\n]|\n(?![ \t]*\n)){{1,200}}?"
QUOTED = [
    re.compile(r'(?<!\d)"' + _SENT.format(close='"') + r'"'),
    re.compile("\u201c" + _PARA.format(close="\u201d") + "\u201d"),
    # Curly single quotes double as apostrophes (it\u2019s), so a closing mark
    # must not be followed by a letter.
    re.compile("\u2018(?:[^\u2019\n]|\u2019(?=\\w)){1,400}?\u2019(?!\\w)"),
    # Straight single quotes: opener not preceded by a letter (so "users'"
    # cannot open), closer not followed by one (so "don't" cannot close).
    re.compile(r"(?<![\w'])'(?=\S)(?:(?![.!?]\s+[A-Z])[^'\n]|'(?=\w)){1,200}?(?<=\S)'(?!\w)"),
]


def strip_quotes(t):
    """Replace quoted spans with a placeholder so a quoted question (a user
    prompt, a model reply, someone else's words) is not read as the writer's."""
    for pat in QUOTED:
        t = pat.sub('"[quote]"', t)
    return t


CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]")


def is_cjk(t):
    """True when the text is substantially Chinese, Japanese or Korean."""
    letters = [c for c in t if c.isalpha()]
    if not letters:
        return False
    return sum(1 for c in letters if CJK.match(c)) / len(letters) > 0.3


def sentences(t):
    t = re.sub(r"\s+", " ", t)
    # CJK terminates sentences with fullwidth marks and does not space-separate,
    # so splitting on [.!?] alone reads a whole document as one sentence.
    parts = re.split(r"(?<=[.!?。！？])\s*", t)
    return [s.strip() for s in parts if len(s.strip()) > 1]


def units(s):
    """Word count for alphabetic scripts, character count for CJK."""
    return len(s) if is_cjk(s) else len(s.split())


def report(path):
    """Print the report for one file and return the number of FLAG lines."""
    flags = [0]

    def flag(msg):
        print("   FLAG " + msg)
        flags[0] += 1

    raw = open(path, encoding="utf-8-sig").read()
    _, unclosed = strip_fences(raw)
    prose = strip_code(raw)
    lines = raw.split("\n")
    sents = sentences(prose)
    cjk = is_cjk(prose)
    lens = [units(s) for s in sents if units(s) > 2]
    # CJK packs far more meaning per character, so the thresholds scale.
    short_at, long_at, unit = (24, 70, "chars") if cjk else (8, 25, "words")

    norm = path.replace("\\", "/")
    label = "/".join([p for p in norm.split("/") if p][-2:])
    print("== %s ==%s" % (label, "  [CJK]" if cjk else ""))
    if lens:
        short = sum(1 for n in lens if n <= short_at)
        long_ = sum(1 for n in lens if n >= long_at)
        print("   sentences %d | mean %.1f | stdev %.1f | short(<=%d) %d | long(>=%d) %d  (%s)"
              % (len(lens), statistics.mean(lens), statistics.pstdev(lens),
                 short_at, short, long_at, long_, unit))
        floor = 14 if cjk else 6
        if statistics.pstdev(lens) < floor:
            flag("uniform sentence length (stdev %.1f) - reads machine-made" % statistics.pstdev(lens))
        if short == 0:
            flag("no short anchor sentences (<=%d %s)" % (short_at, unit))

    # The prose standard's target is zero em-dashes, so any one is flagged.
    # The rate stays in the report for comparing drafts.
    em = prose.count("\u2014") + len(re.findall(r"&mdash;|&#8212;|&#x2014;", prose, re.I))
    per_k = em / max(len(prose.split()) / 1000.0, 0.001)
    print("   em-dashes %d (%.1f per 1000 words)" % (em, per_k))
    if em:
        flag("em-dashes present (%d) - target is zero" % em)
    if unclosed:
        flag("unclosed code fence at line %d; the text after it was checked as prose" % unclosed)

    # A definition list (**Term.** explanation) is ordinary technical typography.
    # The template tell is a long bolded lead-in closed by a colon.
    colon_lead = sum(1 for l in lines if re.match(r"^\s*[-*]?\s*\*\*[^*]{12,}:\*\*", l))
    bold_lead = sum(1 for l in lines if re.match(r"^\s*[-*]?\s*\*\*", l))
    bullets = sum(1 for l in lines if re.match(r"^\s*[-*]\s", l))
    print("   bold-lead lines %d (colon-style %d) | bullets %d" % (bold_lead, colon_lead, bullets))
    if bullets and colon_lead / max(bullets, 1) > 0.5:
        flag("most bullets use a bolded colon lead-in - template cadence")

    # Contrastive framing, hedge intensifiers, the banned-word list and the
    # conclusion crutches are English constructions. Running them over CJK
    # reports nothing and means nothing, so say so rather than implying the
    # text passed those checks.
    if cjk:
        print("   note: contrastive/hedge/vocabulary checks are English-only and were skipped")
    else:
        for pat in CONTRASTIVE:
            for m in re.finditer(pat, prose, re.I):
                flag("contrastive: ...%s..." % m.group(0)[:70].strip())

        for m in re.finditer(HEDGE, prose, re.I):
            flag("hedge/intensifier: %s" % m.group(0))

        for w, pat in BANNED_RES:
            n = len(pat.findall(prose))
            if n:
                flag("banned word: %s x%d" % (w, n))

        for w, pat in CRUTCH_RES:
            n = len(pat.findall(prose))
            if n:
                flag("conclusion crutch: %s x%d" % (w, n))
        n = count_ultimately(prose)
        if n:
            flag("conclusion crutch: ultimately, x%d" % n)

    # A question that opens a numbered or bulleted item is a checklist prompt
    # for the reader, not the ask-and-immediately-answer-yourself pattern.
    checklist = set()
    for l in lines:
        m = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", l)
        if m:
            checklist.add(re.sub(r"[*`]", "", strip_quotes(m.group(1))).strip())
    # Questions inside quotation marks are someone else's words. Blockquotes
    # and fenced code were already removed by strip_code.
    qa = [s for s in sentences(strip_quotes(prose)) if s.endswith("?") or s.endswith("？")]
    originals = [s for s in sentences(prose) if s.endswith("?") or s.endswith("？")]
    for q in qa:
        # Whitespace is collapsed before splitting, so a "-" or "+" bullet that
        # follows prose arrives as "- Is it...?"; drop the marker before comparing.
        bare = re.sub(r"^[-+]\s+", "", re.sub(r"[*`]", "", q).strip())
        if any(item.startswith(bare[:30]) for item in checklist if bare[:30]):
            continue
        head = q.split('"[quote]"')[0][:25]
        shown = next((s for s in originals if head and s.startswith(head)), q)
        flag("rhetorical question: %s" % shown[:70])
    print()
    return flags[0]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Report structural markers of machine-generated prose.")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when any FLAG line is printed (default: always exit 0)")
    ap.add_argument("files", nargs="*", help="Markdown or text files to check")
    args = ap.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:  # a Windows pipe is cp1252, which cannot print CJK text
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    total, unreadable = 0, 0
    for p in args.files:
        try:
            total += report(p)
        except (OSError, UnicodeDecodeError) as e:
            unreadable += 1
            print("ERROR %s: %s" % (p, getattr(e, "strerror", None) or e), file=sys.stderr)
    if unreadable:
        return 2
    return 1 if args.strict and total else 0


if __name__ == "__main__":
    sys.exit(main())
