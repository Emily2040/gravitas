"""Tone and rhyme lookups for Chinese verse, shared by pingze_check.py and couplet_check.py.

Two systems, and a poem is judged by one of them at a time:

  pingshui  平水韵, the 106 rhyme groups of classical verse (data/pingshui.tsv).
            上平声 and 下平声 are 平; 上声, 去声 and 入声 are 仄. 入声 characters
            such as 国, 白, 一, 十 are 仄 here even though Mandarin reads them 平.
  xinyun    中华新韵 (中华诗词学会, 2005), from modern Mandarin readings
            (data/mandarin.tsv): tones 1 and 2 are 平, tones 3 and 4 are 仄, and
            rhyme follows the 14 groups below.

A character with readings of both tones counts as either tone (中), so it never
breaks a rule by itself. A character missing from a table also counts as either
tone, so it can never cause a FAIL; the checks name it in a note, and a PASS that
rests on it names it in its first line. Both tables use simplified characters,
and pingshui.tsv often keeps a classical variant (翦, not 剪).

Standard library only. The data files record their sources and licences in
their header lines.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CJK = re.compile(r"[一-鿿㐀-䶿豈-﫿\U00020000-\U0002ffff]")
PING, ZE = "平", "仄"
EITHER = frozenset((PING, ZE))
SCHEMES = {"pingshui": "平水韵", "xinyun": "中华新韵"}

# 中华新韵 (2005): group name and the finals in it. ü is written v.
XINYUN_GROUPS = [
    ("一麻", ["a", "ia", "ua"]),
    ("二波", ["o", "e", "uo"]),
    ("三皆", ["ie", "ve"]),
    ("四开", ["ai", "uai"]),
    ("五微", ["ei", "uei"]),
    ("六豪", ["ao", "iao"]),
    ("七尤", ["ou", "iou"]),
    ("八寒", ["an", "ian", "uan", "van"]),
    ("九文", ["en", "in", "uen", "vn"]),
    ("十唐", ["ang", "iang", "uang"]),
    ("十一庚", ["eng", "ing", "ong", "iong", "ueng"]),
    ("十二齐", ["i", "v", "er"]),
    ("十三支", ["-i"]),
    ("十四姑", ["u"]),
]
FINAL_GROUP = {f: g for g, finals in XINYUN_GROUPS for f in finals}
INITIALS = ("zh", "ch", "sh", "b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "h", "j", "q", "x", "r", "z", "c", "s")
Y_W = {"yi": "i", "ya": "ia", "yo": "o", "ye": "ie", "yai": "iai", "yao": "iao", "you": "iou", "yan": "ian",
       "yin": "in", "yang": "iang", "ying": "ing", "yong": "iong", "yu": "v", "yue": "ve", "yuan": "van",
       "yun": "vn", "wu": "u", "wa": "ua", "wo": "uo", "wai": "uai", "wei": "uei", "wan": "uan", "wen": "uen",
       "wang": "uang", "weng": "ueng"}

_TABLES = {}


def _rows(name):
    path = os.path.join(DATA, name)
    try:
        fh = open(path, encoding="utf-8")
    except OSError as exc:
        print("ERROR: cannot read the check data %s (%s). Reinstall Gravitas to restore"
              " scripts/checks/data/, or check by hand and say the script did not run." % (path, exc.strerror))
        raise SystemExit(2)
    with fh:
        for line in fh:
            line = line.rstrip("\r\n")
            if line and not line.startswith("#"):
                yield line.split("\t")


def pingshui():
    """{character: [(tone, group), ...]}, for example 窗 -> [('平', '上平声三江')]."""
    if "pingshui" not in _TABLES:
        table = {}
        for kind, name, chars in _rows("pingshui.tsv"):
            tone = PING if kind in ("上平声", "下平声") else ZE
            for ch in chars:
                table.setdefault(ch, []).append((tone, kind + name))
        _TABLES["pingshui"] = table
    return _TABLES["pingshui"]


def mandarin():
    """{character: ['zhang3', 'chang2', ...]}, the most common reading first."""
    if "mandarin" not in _TABLES:
        _TABLES["mandarin"] = {ch: readings.split() for ch, readings in _rows("mandarin.tsv")}
    return _TABLES["mandarin"]


def final(syllable):
    """The final of a toneless pinyin syllable: 'zhuang' -> 'uang', 'ju' -> 'v', 'shi' -> '-i'."""
    s = syllable
    if s in ("zhi", "chi", "shi", "ri", "zi", "ci", "si"):
        return "-i"
    if s in Y_W:
        return Y_W[s]
    for ini in INITIALS:
        if s.startswith(ini) and len(s) > len(ini):
            rest = s[len(ini):]
            if ini in ("j", "q", "x") and rest.startswith("u"):
                rest = "v" + rest[1:]
            return {"ui": "uei", "iu": "iou", "un": "uen"}.get(rest, rest)
    return s


def xinyun_group(reading):
    """The 中华新韵 group of a numbered reading such as 'shuang1', or '?' when it has none."""
    return FINAL_GROUP.get(final(reading.rstrip("12345")), "?")


def lookup(ch, scheme):
    """(tones, rhyme groups of its 平 readings, known) for one character under one scheme."""
    if scheme == "pingshui":
        entries = pingshui().get(ch)
        if not entries:
            return EITHER, [], False
        return (frozenset(t for t, _ in entries),
                sorted({g for t, g in entries if t == PING}), True)
    readings = mandarin().get(ch)
    if not readings:
        return EITHER, [], False
    tones = frozenset(PING if r[-1] in "12" else ZE for r in readings)
    return tones, sorted({xinyun_group(r) for r in readings if r[-1] in "12"} - {"?"}), True


def mark(tones, known=True):
    """One character for a tone: 平, 仄, 中 (either) or ? (not in the table)."""
    if not known:
        return "?"
    return "中" if tones == EITHER else next(iter(tones))


def can_be_ping(tones):
    return PING in tones


def can_be_ze(tones):
    return ZE in tones


def opposite(a, b):
    """True when the two positions can carry opposite tones."""
    return (PING in a and ZE in b) or (ZE in a and PING in b)


def same(a, b):
    return bool(a & b)


def han(text):
    """Only the Han characters of a string."""
    return "".join(CJK.findall(text))
