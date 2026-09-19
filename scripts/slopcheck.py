#!/usr/bin/env python3
"""Detect the structural AI tells that word-level banned-term scans miss.

Checks the prose rules from AGENTS.md: sentence-length variation, contrastive
framing, rhetorical Q&A, conclusion crutches, plus the em-dash and bold-lead
density that make text read as machine-generated.
"""
import re
import statistics
import sys

BANNED_WORDS = ["delve", "leverage", "foster", "robust", "seamless", "transformative",
                "tapestry", "landscape", "circle back", "unpack", "in short",
                "furthermore", "moreover", "utilize", "crucial", "vital", "realm"]

CONTRASTIVE = [
    r"\bnot\s+(?:just|only|merely|simply)\b[^.]*\bbut\b",
    r"\bisn'?t\s+\w+[^.]{0,40}[-\u2014]\s*it'?s\b",
    r"\bit'?s not\b[^.]{0,40}\bit'?s\b",
    r"[^.]{3,60},\s*not\s+\w+[.,]",
    r"\brather than\s+\w+ing\b",
]

HEDGE = r"\b(genuinely|precisely|deliberately|notably|arguably|effectively|essentially|simply put|worth noting|worth stating)\b"


def strip_code(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    return re.sub(r"`[^`]*`", " ", t)


def sentences(t):
    t = re.sub(r"\s+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if len(s.strip()) > 1]


def report(path):
    raw = open(path, encoding="utf-8").read()
    prose = strip_code(raw)
    lines = raw.split("\n")
    sents = sentences(prose)
    lens = [len(s.split()) for s in sents if len(s.split()) > 2]

    print("== %s ==" % path.split("\\")[-1].split("/")[-1])
    if lens:
        short = sum(1 for n in lens if n <= 8)
        long_ = sum(1 for n in lens if n >= 25)
        print("   sentences %d | mean %.1f | stdev %.1f | short(<=8) %d | long(>=25) %d"
              % (len(lens), statistics.mean(lens), statistics.pstdev(lens), short, long_))
        if statistics.pstdev(lens) < 6:
            print("   FLAG uniform sentence length (stdev %.1f) - reads machine-made" % statistics.pstdev(lens))
        if short == 0:
            print("   FLAG no short anchor sentences (<=8 words)")

    em = prose.count("\u2014")
    per_k = em / max(len(prose.split()) / 1000.0, 0.001)
    print("   em-dashes %d (%.1f per 1000 words)" % (em, per_k))
    if per_k > 6:
        print("   FLAG em-dash density")

    # A definition list (**Term.** explanation) is ordinary technical typography.
    # The template tell is a long bolded lead-in closed by a colon.
    colon_lead = sum(1 for l in lines if re.match(r"^\s*[-*]?\s*\*\*[^*]{12,}:\*\*", l))
    bold_lead = sum(1 for l in lines if re.match(r"^\s*[-*]?\s*\*\*", l))
    bullets = sum(1 for l in lines if re.match(r"^\s*[-*]\s", l))
    print("   bold-lead lines %d (colon-style %d) | bullets %d" % (bold_lead, colon_lead, bullets))
    if bullets and colon_lead / max(bullets, 1) > 0.5:
        print("   FLAG most bullets use a bolded colon lead-in - template cadence")

    for pat in CONTRASTIVE:
        for m in re.finditer(pat, prose, re.I):
            print("   FLAG contrastive: ...%s..." % m.group(0)[:70].strip())

    for m in re.finditer(HEDGE, prose, re.I):
        print("   FLAG hedge/intensifier: %s" % m.group(0))

    low = prose.lower()
    for w in BANNED_WORDS:
        if w in low:
            print("   FLAG banned word: %s x%d" % (w, low.count(w)))

    qa = [s for s in sents if s.endswith("?")]
    for q in qa:
        print("   FLAG rhetorical question: %s" % q[:70])
    print()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
