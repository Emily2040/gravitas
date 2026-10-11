#!/usr/bin/env python3
"""Count the morae (音) of a haiku, tanka or senryu from a kana reading of each line.

    python mora_count.py haiku "ふるいけや" "かわずとびこむ" "みずのおと"
    python mora_count.py tanka L1 L2 L3 L4 L5
    python mora_count.py senryu "ふるいけや かわずとびこむ みずのおと"   # one argument, lines split by spaces
    python mora_count.py count ちょっと ボーリングじょう                  # count single words

Pass the reading, not the poem: hiragana or katakana only. A kanji's reading
needs a dictionary (今日 is きょう or こんにち), so this script refuses kanji
and the model supplies the reading it intends.

Counting: every kana is one mora, and so are っ, ッ, ん, ン and ー. Small
ゃ ゅ ょ ぁ ぃ ぅ ぇ ぉ ゎ and their katakana forms join the kana before them, so
きょ is one mora. ほっとする is 5, ボーリングじょう is 7, ホンコン is 4.

Targets: haiku and senryu 5-7-5, tanka 5-7-5-7-7. A line over or under its
target is 字余り or 字足らず. 破調 is a legitimate choice, so a deviation means
"fix it unless it is intended", not "wrong". The script does not judge 季語 or
切れ字.

Prints PASS or FAIL with each deviation. Exit 0 on PASS, 1 on a deviation,
2 when a line is not kana or the line count is wrong.
"""
import argparse
import json
import re
import sys

FORMS = {"haiku": [5, 7, 5], "senryu": [5, 7, 5], "tanka": [5, 7, 5, 7, 7]}
SMALL = set("ゃゅょぁぃぅぇぉゎャュョァィゥェォヮ")
KANA = re.compile(r"[ぁ-ゖゝゞァ-ヺーヽヾ]")
IGNORED = re.compile(r"[\s　、。・「」『』（）()！？!?,.…〜~]")


def morae(reading):
    """The number of morae in a kana string. ValueError when anything else is left in it."""
    s = IGNORED.sub("", reading)
    other = "".join(c for c in s if not KANA.match(c))
    if other:
        raise ValueError("not kana: %s" % other)
    return sum(1 for c in s if c not in SMALL)


def check(form, lines):
    target = FORMS[form]
    if len(lines) == 1 and len(target) > 1:
        lines = [l for l in re.split(r"[\s　/／|]+", lines[0]) if l]
    res = {"form": form, "target": target, "lines": lines, "counts": [], "deviations": [], "errors": []}
    if len(lines) != len(target):
        res["errors"].append("%d line%s; a %s has %d" % (len(lines), "" if len(lines) == 1 else "s", form,
                                                          len(target)))
        return res
    for i, (line, want) in enumerate(zip(lines, target), 1):
        try:
            n = morae(line)
        except ValueError as exc:
            res["errors"].append("line %d: %s; pass a hiragana or katakana reading" % (i, exc))
            continue
        res["counts"].append(n)
        if n != want:
            res["deviations"].append("line %d: %s has %d morae, target %d (%s)"
                                     % (i, line, n, want, "字余り" if n > want else "字足らず"))
    return res


def render(res):
    pattern = "-".join(map(str, res["target"]))
    if res["errors"]:
        return "\n".join(["ERROR: %s" % e for e in res["errors"]])
    counted = "-".join(map(str, res["counts"]))
    if not res["deviations"]:
        return "PASS: %s %s, counted %s." % (res["form"], pattern, counted)
    out = ["FAIL: %s %s, counted %s." % (res["form"], pattern, counted)]
    out += ["- " + d for d in res["deviations"]]
    out.append("note: 破調 is allowed when it is intended; otherwise rewrite the line to its target.")
    return "\n".join(out)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Count morae in a haiku, tanka or senryu reading.")
    ap.add_argument("form", choices=sorted(FORMS) + ["count"])
    ap.add_argument("lines", nargs="+", help="the kana reading of each line, or words to count")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    a = ap.parse_args(argv)
    if a.form == "count":
        try:
            counts = {w: morae(w) for w in a.lines}
        except ValueError as exc:
            print("ERROR: %s; pass a hiragana or katakana reading" % exc)
            return 2
        print(json.dumps(counts, ensure_ascii=False) if a.json else
              "\n".join("%s: %d morae" % (w, n) for w, n in counts.items()))
        return 0
    res = check(a.form, a.lines)
    print(json.dumps(res, ensure_ascii=False) if a.json else render(res))
    return 2 if res["errors"] else 1 if res["deviations"] else 0


if __name__ == "__main__":
    sys.exit(main())
