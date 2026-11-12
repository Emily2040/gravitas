#!/usr/bin/env python3
"""Mechanical port of round four's run and grading suite to round five (standard library only).

    python dev/port5.py           write the ported files into the round-five folder and dev/port5-counts.json
    python dev/port5.py --check   write nothing; print, per file, every changed line and the rule that explains it

Each ab4 file is read as bytes, decoded as UTF-8, and passed through the replacement rules below, in order. The rules
are the replacement list of PORT.md and nothing else. Hand edits that are not mechanical (the run.sh lock and tuning
passes, validity5.py --tuning N, the freeze.sh lock record, the judge_codex.sh worker fix) are made afterwards and
are listed separately in PORT.md; check_port5.py tells the two kinds of changed line apart.
"""
import hashlib
import json
import os
import re
import sys

SRC = r"W:\AgentData\logs\gravitas-dsh-ab4"
DST = r"W:\AgentData\logs\gravitas-dsh-ab5"

# ab4 file -> ab5 file
FILES = {
    "run.sh": "run.sh",
    "runall.sh": "runall.sh",
    "freeze.sh": "freeze.sh",
    "validity4.py": "validity5.py",
    "make_pairs4.py": "make_pairs5.py",
    "save_grades4.py": "save_grades5.py",
    "save_labels4.py": "save_labels5.py",
    "build_notes4.py": "build_notes5.py",
    "judge_codex.sh": "judge_codex.sh",
    "verdict4.py": "verdict5.py",
    "verdict4-amended.py": "verdict5-amended.py",
    "mutation4.py": "mutation5.py",
    "workflows/grade4.js": "workflows/grade5.js",
    "workflows/label4.js": "workflows/label5.js",
    "grader-prompt4.md": "grader-prompt5.md",     # copied byte for byte, no rule applied
}
VERBATIM = {"grader-prompt4.md"}

# Round four's held-out cases -> round five's, by position (same language, same place in sorted order), so the
# frozen self-tests build exactly the same synthetic data on the new names. Applied to the verdict scripts only:
# their EXPECTED_CASES list and the self-test scenarios that name a case of it. validity4.py's synthetic case names
# are not tied to any case list and stay as they are.
CASE_MAP = {
    "zh-flex-hours": "zh-contract-expiry-compensation",
    "zh-insurance-gap": "zh-lease-sale",
    "zh-sick-pay": "zh-passport-remote-apply",
    "en-529-roth": "en-debit-card-theft-liability",
    "en-fsa-rollover": "en-gift-tax-down-payment",
    "en-medicare-part-b": "en-uk-child-benefit-charge",
    "ja-medical-deduction": "ja-child-allowance-income-cap",
    "ja-part-time-leave": "ja-inheritance-registration",
    "ja-wallpaper-restoration": "ja-license-lapse",
    "ko-jeonse-protection": "ko-card-installment-defense",
    "ko-severance-pay": "ko-dependent-pension",
    "ko-unemployment-quit": "ko-duty-free-limit",
}
CASE_FILES = {"verdict4.py", "verdict4-amended.py"}

# Text that contains "c4" but is not a c4 identifier or label: verdict4-amended.py's synthetic event streams number
# their tool calls c1..c5 (callId "c4" is the fourth call), and its self-test scenario "(c4)" is item 4 of section (c).
PROTECT = {
    "verdict4-amended.py": ['"callId": "c4"', 'variant("(c4) one codex grade'],
}

FROZEN_OLD = "11cdd365b88df9e20a38ad2514ba50a1e3baac6feea796c1f3220429826792ca"

# (id, what it replaces, pattern, replacement, files it applies to or None for all)
RULES = [
    ("P1", "round folder: gravitas-dsh-ab4 -> gravitas-dsh-ab5",
     re.compile(r"gravitas-dsh-ab4"), "gravitas-dsh-ab5", None),
    ("P2", "worktree: gravitas-claim-check -> gravitas-round5 (and its 'claim-check worktree' label)",
     re.compile(r"gravitas-claim-check|(?<=not the )claim-check(?= worktree)"), "gravitas-round5", None),
    ("P3", "committed copies: docs/dsh-ab/round-four -> docs/dsh-ab/round-five",
     re.compile(r"docs/dsh-ab/round-four"), "docs/dsh-ab/round-five", None),
    ("N1", "script and file names of the ported suite: <name>4 -> <name>5 (validity, make_pairs, save_grades, "
           "save_labels, build_notes, verdict, verdict-amended, mutation, preverdict, grade, label, grader-prompt; "
           "also inside verdict4.json, verdict4_sha256, verdict4_frozen_)",
     re.compile(r"\b(validity|make_pairs|save_grades|save_labels|build_notes|verdict|preverdict|mutation|grade|label"
                r"|grader-prompt)4(?![0-9])"), lambda m: m.group(1) + "5", None),
    ("L1", "round labels: round-four / Round-four / round four / Round four -> five",
     re.compile(r"\b([Rr]ound)([- ])four\b"), lambda m: m.group(1) + m.group(2) + "five", None),
    ("C1", "change 4 -> change 5 (change4, change 4, Change 4)",
     re.compile(r"\b([Cc]hange)( ?)4(?![0-9])"), lambda m: m.group(1) + m.group(2) + "5", None),
    ("C2", "arm, set and c4 identifiers and labels -> c5 (gv-grav-c4, aa-c4, C4, c4, c4_*, *_c4, c4Sentence, ...)",
     re.compile(r"(?<![A-Za-z0-9])([cC])4(?![0-9a-z])"), lambda m: m.group(1) + "5", None),
    ("R1", "run-folder label r4- -> r5- (run.sh's cwd, validity's cwd check, make_pairs' leak pattern)",
     re.compile(r"(?:(?<![A-Za-z0-9])|(?<=\\b))r4-"), "r5-", None),
    ("K1", "EXPECTED_CASES and the self-test scenarios that name its cases -> round five's cases, by position",
     re.compile("|".join(re.escape(k) for k in CASE_MAP)), lambda m: CASE_MAP[m.group()], CASE_FILES),
    ("K2", "the comment above EXPECTED_CASES: round four's list date -> round five's",
     re.compile(r"\(prompts/ as listed on 2026-10-23, before any run\)"),
     "(prompts/ as fixed on 2026-10-25, before any run)", {"verdict4.py"}),
    # T1 runs last, so that no earlier rule (P1, L1) rewrites the text it produces.
    ("T1", "tuning prompt folder: round three's prompts -> W:\\AgentData\\logs\\gravitas-dsh-ab4\\prompts "
           "(variable R3P -> R4P, label 'round three's prompts' -> 'round four's prompts')",
     re.compile(r"R3P=/w/AgentData/logs/gravitas-dsh-ab3/prompts|\$R3P|round three's prompts"),
     lambda m: {"R3P=/w/AgentData/logs/gravitas-dsh-ab3/prompts": "R4P=/w/AgentData/logs/gravitas-dsh-ab4/prompts",
                "$R3P": "$R4P", "round three's prompts": "round four's prompts"}[m.group()], {"run.sh"}),
]


def apply_rules(name, text, counts):
    protected = PROTECT.get(name, [])
    for i, p in enumerate(protected):
        text = text.replace(p, "\x00P%d\x00" % i)
    for rid, _, pat, rep, files in RULES:
        if files is not None and name not in files:
            continue
        text, n = pat.subn(rep, text)
        if n:
            counts[rid] = counts.get(rid, 0) + n
    for i, p in enumerate(protected):
        text = text.replace("\x00P%d\x00" % i, p)
    return text


def port_text(name, text, frozen_new):
    counts = {}
    out = apply_rules(name, text, counts)
    if frozen_new:
        n = out.count(FROZEN_OLD) + out.count(FROZEN_OLD[:8] + "..." + FROZEN_OLD[-5:])
        out = out.replace(FROZEN_OLD, frozen_new).replace(FROZEN_OLD[:8] + "..." + FROZEN_OLD[-5:],
                                                         frozen_new[:8] + "..." + frozen_new[-5:])
        if n:
            counts["S1"] = n
    return out, counts


def main():
    check = "--check" in sys.argv
    all_counts = {}
    order = sorted(FILES, key=lambda f: f in ("verdict4-amended.py", "mutation4.py"))  # verdict5.py first
    frozen_new = None
    for src in order:
        dst = FILES[src]
        raw = open(os.path.join(SRC, src), "rb").read()
        if src in VERBATIM:
            new_raw, counts = raw, {}
        else:
            text = raw.decode("utf-8")
            new, counts = port_text(src, text, frozen_new if src in ("verdict4-amended.py", "mutation4.py") else None)
            new_raw = new.encode("utf-8")
        all_counts[dst] = counts
        if src == "verdict4.py":
            frozen_new = hashlib.sha256(new_raw).hexdigest()
        if not check:
            p = os.path.join(DST, dst)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as f:
                f.write(new_raw)
        print("%-24s <- %-24s %s" % (dst, src, counts or "(byte-identical)"))
    print("verdict5.py sha256 %s" % frozen_new)
    if not check:
        with open(os.path.join(DST, "dev", "port5-counts.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"rules": [[r[0], r[1]] for r in RULES] + [["S1", "frozen sha256 of verdict4.py -> verdict5.py's"]],
                       "counts": all_counts, "verdict5_sha256_after_mechanical_port": frozen_new}, f, indent=1)


if __name__ == "__main__":
    main()
