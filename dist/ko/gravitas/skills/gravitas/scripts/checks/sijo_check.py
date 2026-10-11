#!/usr/bin/env python3
"""Count the syllables of a 평시조, 음보 by 음보.

    python sijo_check.py "이 몸이|죽고 죽어|일백 번|고쳐 죽어" "백골이|진토되어|넋이라도|있고 없고" "임 향한|일편단심이야|가실 줄이|있으랴"

Give the three 장 as three arguments (or one argument with a line per 장), and
mark each 음보 with '|' in this check copy. The poem shown to the person keeps
its ordinary spacing. Where the 음보 fall is a reading of the poem, so the model
marks them and the script only counts. Spaces and punctuation inside a 음보 are
not counted; any other non-Hangul text is refused, so write numbers in Hangul.

Rules, from the 한국민족문화대백과사전 article '시조' (revised 2024-10-22):
  problems: not 3 장 of 4 음보 each; a 종장 first 음보 that is not 3 syllables
            ('3음절로 고정'; a 2 is named as the variant only the same article's
            narrower definition allows); a 종장 second 음보 under 5 syllables
  notes:    a 음보 more than 2 syllables away from the base pattern
            (초장 and 중장 3·4·4·4, 종장 3·5·4·3); a total outside 43 to 47
            ('45자 내외')

Prints PASS or FAIL with the problems. Exit 0 on PASS, 1 on FAIL, 2 when the
input cannot be read.
"""
import argparse
import json
import re
import sys
import unicodedata

BASE = [[3, 4, 4, 4], [3, 4, 4, 4], [3, 5, 4, 3]]
JANG = ["초장", "중장", "종장"]
HANGUL = re.compile(r"[가-힣]")


def syllables(foot):
    other = "".join(c for c in foot if not (HANGUL.match(c) or c.isspace()
                                            or unicodedata.category(c).startswith("P")))
    if other:
        raise ValueError("non-Hangul text in a 음보: %s" % other)
    return len(HANGUL.findall(foot))


def check(jang):
    if len(jang) == 1 and "\n" in jang[0]:
        jang = [l for l in jang[0].splitlines() if l.strip()]
    res = {"syllables": [], "total": None, "problems": [], "notes": []}
    if len(jang) != 3:
        res["problems"].append("%d 장; a 평시조 has 3" % len(jang))
        return res
    for i, line in enumerate(jang):
        feet = line.split("|")
        if len(feet) != 4:
            res["problems"].append("%s: %d 음보; mark 4 with |" % (JANG[i], len(feet)))
            continue
        counts = [syllables(f) for f in feet]
        for j, got in enumerate(counts, 1):
            if not got:
                res["problems"].append("%s 음보 %d is empty; mark 4 with |" % (JANG[i], j))
        res["syllables"].append(counts)
        for j, (got, base) in enumerate(zip(counts, BASE[i]), 1):
            if abs(got - base) > 2:
                res["notes"].append("%s 음보 %d: %d syllables, base %d" % (JANG[i], j, got, base))
    if len(res["syllables"]) == 3:
        last = res["syllables"][2]
        if last[0] == 2:
            res["problems"].append("종장 음보 1 has 2 syllables; the standard form fixes it at 3, "
                                   "and only the same article's narrower definition allows 2")
        elif last[0] != 3:
            res["problems"].append("종장 음보 1 has %d syllables; it must be 3" % last[0])
        if last[1] < 5:
            res["problems"].append("종장 음보 2 has %d syllables; it must be 5 or more" % last[1])
        res["total"] = sum(map(sum, res["syllables"]))
        if not 43 <= res["total"] <= 47:
            res["notes"].append("total %d syllables; a 평시조 has about 45" % res["total"])
    return res


def render(res):
    pattern = " / ".join("·".join(map(str, c)) for c in res["syllables"])
    if not res["problems"]:
        out = ["PASS: 평시조, 3 장 of 4 음보, %d syllables (%s)." % (res["total"], pattern)]
    else:
        k = len(res["problems"])
        out = ["FAIL: 평시조, %d problem%s%s." % (k, "" if k == 1 else "s", " (%s)" % pattern if pattern else "")]
        out += ["- " + p for p in res["problems"]]
    out += ["note: " + n for n in res["notes"]]
    return "\n".join(out)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Count the syllables of a 평시조.")
    ap.add_argument("jang", nargs="+", help="the three 장, with each 음보 marked by |")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    a = ap.parse_args(argv)
    try:
        res = check(a.jang)
    except ValueError as exc:
        print("ERROR: %s" % exc)
        return 2
    print(json.dumps(res, ensure_ascii=False) if a.json else render(res))
    return 1 if res["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
