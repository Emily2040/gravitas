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
    raw = open(path, encoding="utf-8").read()
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
            print("   FLAG uniform sentence length (stdev %.1f) - reads machine-made" % statistics.pstdev(lens))
        if short == 0:
            print("   FLAG no short anchor sentences (<=%d %s)" % (short_at, unit))

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

    # Contrastive framing, hedge intensifiers and the banned-word list are
    # English constructions. Running them over CJK reports nothing and means
    # nothing, so say so rather than implying the text passed those checks.
    if cjk:
        print("   note: contrastive/hedge/vocabulary checks are English-only and were skipped")
    else:
        for pat in CONTRASTIVE:
            for m in re.finditer(pat, prose, re.I):
                print("   FLAG contrastive: ...%s..." % m.group(0)[:70].strip())

        for m in re.finditer(HEDGE, prose, re.I):
            print("   FLAG hedge/intensifier: %s" % m.group(0))

        low = prose.lower()
        for w in BANNED_WORDS:
            if w in low:
                print("   FLAG banned word: %s x%d" % (w, low.count(w)))

    # A question that opens a numbered or bulleted item is a checklist prompt
    # for the reader, not the ask-and-immediately-answer-yourself pattern.
    checklist = set()
    for l in lines:
        m = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", l)
        if m:
            checklist.add(re.sub(r"[*`]", "", m.group(1)).strip())
    qa = [s for s in sents if s.endswith("?") or s.endswith("？")]
    for q in qa:
        bare = re.sub(r"[*`]", "", q).strip()
        if any(item.startswith(bare[:30]) for item in checklist if bare[:30]):
            continue
        print("   FLAG rhetorical question: %s" % q[:70])
    print()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
