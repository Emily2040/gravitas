#!/usr/bin/env python3
"""Check the tones and rhyme of a 绝句 or 律诗 (近体诗) against one rhyme system.

    python pingze_check.py "秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度阴山。"
    python pingze_check.py --scheme xinyun "..."     # 中华新韵 instead of 平水韵
    python pingze_check.py --file poem.txt [--json]

Pass the poem in simplified characters, with the lines split by punctuation or
new lines. --scheme pingshui (平水韵, the default) or xinyun (中华新韵); judge by
the one the person asked for, and say in the reply which one the poem follows.

Hard rules, each a problem:
  - 4 lines (绝句) or 8 (律诗), every line 5 or 7 characters
  - 二四分明, and 四六分明 in 7-character lines
  - 对 inside each couplet and 粘 between couplets, at position 2
  - lines 2, 4, 6 and 8 end on 平 and share one 平声 rhyme group; line 1 may
    rhyme, and when it ends on 平 it must
  - lines 3, 5 and 7 end on 仄
  - 三平尾, and 孤平 (仄平仄仄平, or 仄仄仄平仄仄平) in a line that ends on 平
A character with both tones counts as either. Notes, which never fail a poem:
characters missing from the table, and 重字 across lines. A PASS names, in its
first line, any missing character that a rule reads, since that rule went unchecked.

Not modelled: 拗救. A deliberate 拗 at position 2, 4 or 6 is reported even when
a 救 offsets it, so read such a problem before rewriting a line. 仄韵 poems and
排律 are out of scope.

Prints PASS or FAIL with the problems, one per line. Exit 0 on PASS, 1 on FAIL,
2 when the input or the check data cannot be read.
"""
import argparse
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # keep __pycache__ out of the installed plugin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zh_tones as zt  # noqa: E402

SPLIT = re.compile(r"[，。！？；、,.!?;:：\s]+")


def poem_lines(text):
    return [l for l in (zt.han(part) for part in SPLIT.split(text)) if l]


def form_name(n, width):
    return "%s言%s" % ("五" if width == 5 else "七", "绝句" if n == 4 else "律诗")


def check(text, scheme="pingshui"):
    """A dict with the form, the tone marks per line, the problems and the notes."""
    lines = poem_lines(text)
    out = {"scheme": zt.SCHEMES[scheme], "form": "", "lines": lines, "tones": [], "problems": [], "notes": [],
           "unchecked": ""}
    n = len(lines)
    if n not in (4, 8):
        out["problems"].append("%d line%s; a 绝句 has 4 and a 律诗 has 8" % (n, "" if n == 1 else "s"))
        return out
    width = len(lines[0])
    if width not in (5, 7) or any(len(l) != width for l in lines):
        out["problems"].append("line lengths %s; every line must have 5 characters, or every line 7"
                               % "/".join(str(len(l)) for l in lines))
        return out
    out["form"] = form_name(n, width)
    info = [[zt.lookup(c, scheme) for c in l] for l in lines]
    tones = [[t for t, _, _ in row] for row in info]
    out["tones"] = ["".join(zt.mark(t, k) for t, _, k in row) for row in info]
    p = out["problems"]

    for i, row in enumerate(tones, 1):
        if not zt.opposite(row[1], row[3]):
            p.append("line %d: positions 2 and 4 must differ in tone (二四分明)" % i)
        if width == 7 and not zt.opposite(row[3], row[5]):
            p.append("line %d: positions 4 and 6 must differ in tone (四六分明)" % i)
    for a in range(0, n, 2):
        if not zt.opposite(tones[a][1], tones[a + 1][1]):
            p.append("lines %d and %d: position 2 must be opposite in tone (失对)" % (a + 1, a + 2))
    for a in range(1, n - 1, 2):
        if not zt.same(tones[a][1], tones[a + 1][1]):
            p.append("lines %d and %d: position 2 must match in tone (失粘)" % (a + 1, a + 2))

    rhyme_idx = list(range(1, n, 2))
    groups, unknown = [], []
    for i in rhyme_idx:
        t, g, known = info[i][-1]
        ch = lines[i][-1]
        if not zt.can_be_ping(t):
            p.append("line %d: rhyme word %s is 仄; it must be 平" % (i + 1, ch))
        elif known:
            groups.append((ch, set(g)))
        else:
            unknown.append(ch)
    common = set.intersection(*[g for _, g in groups]) if groups else set()
    if len(groups) > 1 and not common:
        p.append("rhyme words share no %s 平声 group: %s" % (out["scheme"], ", ".join(
            "%s (%s)" % (ch, " or ".join(sorted(g)) or "none") for ch, g in groups)))
    if unknown:
        out["notes"].append("rhyme of %s not checked: not in the %s table" % ("".join(unknown), out["scheme"]))
    t1, g1, k1 = info[0][-1]
    if k1 and t1 == {zt.PING} and common and not set(g1) & common:
        p.append("line 1 ends on 平 (%s) but does not rhyme with the other rhyme words" % lines[0][-1])
    for i in range(2, n, 2):
        if not zt.can_be_ze(tones[i][-1]):
            p.append("line %d: a line that does not rhyme must end on 仄, and %s is 平" % (i + 1, lines[i][-1]))

    for i, row in enumerate(info):
        if all(k and t == {zt.PING} for t, _, k in row[-3:]):
            p.append("line %d: the last three characters are all 平 (三平尾)" % (i + 1))
        # 孤平 is judged on the last five characters a b c d e of a line ending on 平: when d is 仄
        # (the 平平仄仄平 pattern), a, b and c must hold at least two 平. 仄仄仄平平 is not 孤平.
        last5 = [t for t, _, _ in row[-5:]]
        if (i in rhyme_idx or (i == 0 and t1 == {zt.PING})) and zt.can_be_ping(last5[4]) and last5[3] == {zt.ZE} \
                and sum(zt.can_be_ping(t) for t in last5[:3]) <= 1:
            p.append("line %d: only one 平 besides the rhyme word (孤平)" % (i + 1))

    seen = {}
    for i, l in enumerate(lines, 1):
        for c in l:
            seen.setdefault(c, set()).add(i)
    repeats = ["%s (lines %s)" % (c, ", ".join(map(str, sorted(v)))) for c, v in seen.items() if len(v) > 1]
    if repeats:
        out["notes"].append("重字 across lines: " + "; ".join(repeats))
    missing = "".join(dict.fromkeys(c for l, row in zip(lines, info) for c, (_, _, k) in zip(l, row) if not k))
    # No rule here reads the first character of a 7-character line, so it cannot hide a fault.
    out["unchecked"] = "".join(dict.fromkeys(c for l, row in zip(lines, info) for j, (c, (_, _, k))
                                             in enumerate(zip(l, row)) if not k and not (width == 7 and j == 0)))
    if missing:
        out["notes"].append("not in the %s table, so counted as either tone: %s%s" % (
            out["scheme"], missing, "; write the check copy in simplified characters" if scheme == "pingshui" else ""))
    if any(("position" in x or "孤平" in x) for x in p):
        out["notes"].append("拗救 is not modelled: if a broken position is a deliberate 拗 with its 救, keep it")
    return out


def render(res):
    name = res["form"] or "poem"
    if not res["problems"]:
        head = "PASS: %s by %s. Line count, 二四六分明, 粘对, rhyme, 孤平 and 三平尾 all hold." % (name, res["scheme"])
        body = []
        if res.get("unchecked"):
            them = "it" if len(res["unchecked"]) == 1 else "them"
            head = ("PASS: %s by %s, except %s: the table lacks %s, so the tones and rhyme that rest on %s are"
                    " unchecked. Line count, 二四六分明, 粘对, rhyme, 孤平 and 三平尾 hold for every other character."
                    % (name, res["scheme"], res["unchecked"], them, them))
            body = ["tones (中 = either, ? = not in the table):"]
            body += ["  %s  %s" % (l, t) for l, t in zip(res["lines"], res["tones"])]
    else:
        k = len(res["problems"])
        head = "FAIL: %s by %s, %d problem%s." % (name, res["scheme"], k, "" if k == 1 else "s")
        body = ["- " + x for x in res["problems"]]
        if res["tones"]:
            body.append("tones (中 = either, ? = not in the table):")
            body += ["  %s  %s" % (l, t) for l, t in zip(res["lines"], res["tones"])]
    body += ["note: " + x for x in res["notes"]]
    return "\n".join([head] + body)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Check a 绝句 or 律诗 against 平水韵 or 中华新韵.")
    ap.add_argument("poem", nargs="?", help="the poem text")
    ap.add_argument("--file", help="read the poem from a UTF-8 file instead")
    ap.add_argument("--scheme", choices=sorted(zt.SCHEMES), default="pingshui")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    a = ap.parse_args(argv)
    if bool(a.poem) == bool(a.file):
        ap.error("give the poem or --file, not both")
    try:
        text = a.poem if a.poem else open(a.file, encoding="utf-8-sig").read()
    except UnicodeDecodeError as exc:
        print("ERROR: %s is not UTF-8 text; save it as UTF-8 and run again (%s)" % (a.file, exc))
        return 2
    except OSError as exc:
        print("ERROR: cannot read %s: %s" % (a.file, exc))
        return 2
    if not poem_lines(text):
        print("ERROR: no Chinese characters in the input")
        return 2
    res = check(text, a.scheme)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else render(res))
    return 1 if res["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
