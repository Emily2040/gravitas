#!/usr/bin/env python3
"""Write the two data files the Chinese verse checks read.

    python scripts/build_check_data.py PINGSHUI_HTML

PINGSHUI_HTML is the zh.wikisource page 平水韻 saved as rendered HTML with
variant=zh-hans (the parser-cache comment at its end names the revision). The
script writes, under plugin/skills/gravitas/scripts/checks/data/:

  pingshui.tsv   the 106 rhyme groups of the 平水韵, one group per line, in
                 the order 上平声, 下平声, 上声, 去声, 入声
  mandarin.tsv   modern Mandarin readings for every character in GB 2312,
                 Big5 level 1 and the 平水韵 table, used for 中华新韵

The checks themselves use the standard library only. This build script needs
pypinyin 0.55.0 for the Mandarin readings, and is not shipped in the plugin.
A reading is kept when it is pypinyin's first reading for the character, or
when at least MIN_PHRASES entries of pypinyin's phrase dictionary use it, so
readings found only in old dictionaries (月 rù, 听 yǐn) do not make a character
count as both tones. The tone-sandhi forms of 一 and 不 are dropped, since
sandhi does not change a character's 平仄. Neutral-tone readings are dropped.
"""
import html
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "plugin", "skills", "gravitas", "scripts", "checks", "data")
CJK = re.compile(r"[一-鿿㐀-䶿\U00020000-\U0002ffff]")
KINDS = ["上平声", "下平声", "上声", "去声", "入声"]
NUMERALS = "一二三四五六七八九十"
MIN_PHRASES = 3
LEXICAL = {"一": ["yi1"], "不": ["bu4"]}

PINGSHUI_HEADER = """\
# 平水韵: the 106 rhyme groups, as printed in 平水新刊韵略 (王文郁, 1229) and 壬子新刊礼部韵略 (刘渊, 1252).
# Source: https://zh.wikisource.org/wiki/平水韻 , page revision {rev}, rendered with variant=zh-hans.
# Licence: the page carries Template:PD-old (公有领域: the author died more than 100 years ago and the
#   work was published before 1 January 1931). Wikisource's footer offers the site's text under
#   CC BY-SA 4.0; should any editorial part of this list be held to be a Wikisource contribution,
#   this file is offered under CC BY-SA 4.0 as well, with attribution to Wikisource contributors.
# Format: kind<TAB>number and name<TAB>characters. kind is 上平声 or 下平声 (平) or 上声, 去声, 入声 (仄).
# The characters are the simplified rendering; a character that appears in several groups belongs to each.
# Written by scripts/build_check_data.py; do not edit by hand.
"""

MANDARIN_HEADER = """\
# Modern Mandarin readings, for judging verse by 中华新韵 (tones 1 and 2 are 平, 3 and 4 are 仄).
# Characters: GB 2312, Big5 level 1, and every character in pingshui.tsv.
# Source: pypinyin {version} (pinyin_dict.json and phrases_dict.json), https://github.com/mozillazg/python-pinyin ,
#   whose single-character data comes from the pinyin-data project (MIT), compiled from the Unicode
#   Unihan database (kTGHZ2013, kXHC1983, kHanyuPinyin, kHanyuPinlu, kMandarin) and other dictionaries.
# Kept: pypinyin's first reading, plus any reading used in at least {min_phrases} phrase-dictionary entries.
#   Tone sandhi of 一 and 不 and neutral-tone readings are dropped. ü is written v.
# Format: character<TAB>readings in numbered pinyin, the most common first.
# Written by scripts/build_check_data.py; do not edit by hand.
#
# pypinyin licence:
# The MIT License (MIT)
# Copyright (c) 2016 mozillazg, 闲耘 <hotoo.cn@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


def numeral(s):
    """一 to 三十 as an int."""
    if s == "十":
        return 10
    if "十" in s:
        a, b = s.split("十")
        return (NUMERALS.index(a) + 1 if a else 1) * 10 + (NUMERALS.index(b) + 1 if b else 0)
    return NUMERALS.index(s) + 1


def pingshui(path):
    text = open(path, encoding="utf-8").read()
    rev = re.search(r"revision id (\d+)", text)
    lines = [l.strip() for l in html.unescape(re.sub(r"<[^>]+>", "\n", text)).split("\n") if l.strip()]
    groups = {}
    i = 0
    while i < len(lines):
        m = re.match(r"^(上平声|下平声|上声|去声|入声)([一二三四五六七八九十]+)$", lines[i])
        if m and i + 2 < len(lines):
            chars = "".join(dict.fromkeys(CJK.findall(lines[i + 2])))
            groups[(KINDS.index(m.group(1)), numeral(m.group(2)))] = (m.group(1), m.group(2) + lines[i + 1], chars)
            i += 3
            continue
        i += 1
    if len(groups) != 106:
        sys.exit("found %d rhyme groups in %s; the 平水韵 has 106" % (len(groups), path))
    return [groups[k] for k in sorted(groups)], rev.group(1) if rev else "unknown"


def numbered(marked):
    """'zhǎng' -> 'zhang3', 'lǜ' -> 'lv4'; a neutral tone gives None."""
    tone = None
    out = []
    for c in unicodedata.normalize("NFD", marked):
        mark = {"̄": "1", "́": "2", "̌": "3", "̀": "4"}.get(c)
        if mark:
            tone = mark
        elif c == "̈":
            out[-1] = "v"
        else:
            out.append(c)
    return "".join(out) + tone if tone else None


def mandarin(chars):
    import pypinyin
    from pypinyin.phrases_dict import phrases_dict
    from pypinyin.pinyin_dict import pinyin_dict
    used = defaultdict(Counter)
    for phrase, readings in phrases_dict.items():
        for ch, r in zip(phrase, readings):
            used[ch][r[0]] += 1
    rows = []
    for ch in sorted(chars):
        if ch in LEXICAL:
            rows.append((ch, LEXICAL[ch]))
            continue
        marked = pinyin_dict.get(ord(ch), "").split(",")
        keep = []
        for n, r in enumerate(marked):
            if r and (n == 0 or used[ch][r] >= MIN_PHRASES):
                num = numbered(r)
                if num and num not in keep:
                    keep.append(num)
        if keep:
            rows.append((ch, keep))
    return rows, pypinyin.__version__


def charset(groups):
    out = set()
    for codec, lead, trail in (("gb2312", range(0xB0, 0xF8), range(0xA1, 0xFF)),
                               ("big5", range(0xA4, 0xC7), list(range(0x40, 0x7F)) + list(range(0xA1, 0xFF)))):
        for a in lead:
            for b in trail:
                try:
                    ch = bytes([a, b]).decode(codec)
                except UnicodeDecodeError:
                    continue
                if CJK.match(ch):
                    out.add(ch)
    for _, _, chars in groups:
        out.update(chars)
    return out


def main(argv):
    if len(argv) != 1:
        sys.exit("usage: build_check_data.py PINGSHUI_HTML")
    groups, rev = pingshui(argv[0])
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "pingshui.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(PINGSHUI_HEADER.format(rev=rev))
        for kind, name, chars in groups:
            fh.write("%s\t%s\t%s\n" % (kind, name, chars))
    rows, version = mandarin(charset(groups))
    with open(os.path.join(OUT, "mandarin.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(MANDARIN_HEADER.format(version=version, min_phrases=MIN_PHRASES))
        for ch, readings in rows:
            fh.write("%s\t%s\n" % (ch, " ".join(readings)))
    print("wrote %d rhyme groups (revision %s) and %d Mandarin entries (pypinyin %s) to %s"
          % (len(groups), rev, len(rows), version, OUT))


if __name__ == "__main__":
    main(sys.argv[1:])
