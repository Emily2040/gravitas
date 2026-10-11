#!/usr/bin/env python3
"""Write a date the way each locale's standard writes it, and lint the dates in a text.

    python locale_dates.py show 2026-10-04
    python locale_dates.py lint ko "퇴사일(2026.9.30)로부터 14일"
    python locale_dates.py lint ja "令和7年（2026年）10月"
    python locale_dates.py lint zh-CN "26年10月发布"

Forms printed by show:
  zh-CN  2026年10月4日（星期日）    GB/T 15835-2011 5.1.2: the year in full, no zero padding
  ja     2026年10月4日（日）         and the era form 令和8年10月4日, with 元年 for an era's first year
  ko     2026. 10. 4.(일)          한글 맞춤법 문장 부호: a dot after the year, the month and the day,
                                   and the weekday in brackets right after the last dot
Era start dates: 令和 2019-05-01, 平成 1989-01-08, 昭和 1926-12-25. Earlier dates are refused.

Lint rules (flags for the writer to fix, not grades):
  ko     a dotted date without the dot after the day (2026.9.30), with a zero-padded month or day
         (2026. 09. 30.), or with no space after the year or the month dot (2026.10.4.); one line per date
  ja     an era year next to a Western year that does not match it (令和7年（2026年））; 1年 for an era's
         first year, which prose writes 元年 (令和1年); an era date its era does not cover (平成元年1月5日
         is 昭和64年1月5日; 平成35年 never came); 1月1日 written before 元旦, which already means it
  zh-CN  a two-digit year before a month (26年10月) or before 出生, 毕业, 入学 or 入职 (90年出生).
         A bare 15年 is left alone, because it is usually a length of time.

Prints PASS or FAIL for lint. Exit 0 on PASS or after show, 1 on FAIL, 2 when the input cannot be read.
"""
import argparse
import datetime as dt
import json
import re
import sys

ERAS = [("令和", dt.date(2019, 5, 1)), ("平成", dt.date(1989, 1, 8)), ("昭和", dt.date(1926, 12, 25))]
ERA_START = {name: start.year for name, start in ERAS}
ERA_END = {ERAS[i][0]: ERAS[i - 1][1] - dt.timedelta(days=1) for i in range(1, len(ERAS))}
ERA_DATE = re.compile(r"(令和|平成|昭和)(元|\d{1,2})年(?:[（(]\s*\d{4}\s*年?\s*[)）]|[)）])?"
                      r"(?:(\d{1,2})月(?:(\d{1,2})日)?)?")
KO_DATE = re.compile(r"(?<![\d.])(\d{4})\.(\s?)(\d{1,2})\.(?:(\s?)(\d{1,2})(\.)?)?(?![.\d])")
WEEKDAY = {"zh-CN": "一二三四五六日", "ja": "月火水木金土日", "ko": "월화수목금토일"}
LANGS = {"zh": "zh-CN", "zh-CN": "zh-CN", "ja": "ja", "ko": "ko"}


def wareki(d):
    for name, start in ERAS:
        if d >= start:
            y = d.year - start.year + 1
            return "%s%s年%d月%d日" % (name, "元" if y == 1 else y, d.month, d.day)
    raise ValueError("%s is before 昭和; give a later date" % d.isoformat())


def outside_era(era, ey, month, day):
    """Say why an era date names a day its era does not cover, or return None.

    A month without a day is flagged only when the whole month falls outside the era."""
    start = dict(ERAS)[era]
    end = ERA_END.get(era)
    year = start.year + (1 if ey == "元" else int(ey)) - 1
    if end and year > end.year:
        return "%s ended on %s, in %s%d年" % (era, end.isoformat(), era, end.year - start.year + 1)
    if not month:
        if year < start.year:  # 令和0年
            return "%s began on %s, in %s元年" % (era, start.isoformat(), era)
        return None
    try:
        first = dt.date(year, int(month), int(day) if day else 1)
        last = first if day else dt.date(year + int(month) // 12, int(month) % 12 + 1, 1) - dt.timedelta(days=1)
    except ValueError:
        return None
    if last < start:
        why = "%s began on %s" % (era, start.isoformat())
    elif end and first > end:
        why = "%s ended on %s" % (era, end.isoformat())
    else:
        return None
    if day and first >= ERAS[-1][1]:
        return "%s; that day is %s" % (why, wareki(first))
    return why


def show(iso):
    try:
        d = dt.date.fromisoformat(iso)
    except ValueError:
        raise ValueError("%r is not an ISO date such as 2026-10-04" % iso)
    w = d.weekday()
    return {"zh-CN": "%d年%d月%d日（星期%s）" % (d.year, d.month, d.day, WEEKDAY["zh-CN"][w]),
            "ja": "%d年%d月%d日（%s）" % (d.year, d.month, d.day, WEEKDAY["ja"][w]),
            "ja-wareki": wareki(d),
            "ko": "%d. %d. %d.(%s)" % (d.year, d.month, d.day, WEEKDAY["ko"][w]),
            "iso": d.isoformat()}


def lint(lang, text):
    hits = []
    if lang == "ko":
        for m in KO_DATE.finditer(text):  # one line per date, naming every fault in it
            y, sp1, mo, sp2, d, dot = m.groups()
            if not 1 <= int(mo) <= 12 or (d is not None and not 1 <= int(d) <= 31):
                continue
            fix = []
            if d is not None and not dot:
                fix.append("needs a dot after the day")
            if any(p and len(p) > 1 and p[0] == "0" for p in (mo, d)):
                fix.append("no leading zero in the month or the day")
            if d is not None and (not sp1 or not sp2):
                fix.append("write a space after the year and the month dots, as the 문장 부호 examples do")
            if fix:
                form = "%s. %d." % (y, int(mo)) + ("" if d is None else " %d." % int(d))
                hits.append("%s: %s (%s)" % (m.group(0), "; ".join(fix), form))
    elif lang == "ja":
        # one year glossed by the other, in brackets or after a slash; a range or a list
        # (令和元年〜2026年, 2020年から令和8年) names two different years
        pat = (r"(令和|平成|昭和)(元|\d{1,2})年\s*[（(/／]\s*(?:西暦)?\s*(\d{4})年"
               r"|(\d{4})年\s*[（(/／]\s*(令和|平成|昭和)(元|\d{1,2})年")
        for m in re.finditer(pat, text):
            era = m.group(1) or m.group(5)
            ey = m.group(2) or m.group(6)
            west = int(m.group(3) or m.group(4))
            n = 1 if ey == "元" else int(ey)
            if ERA_START[era] + n - 1 != west:
                hits.append("%s: %s%s年 is %d, not %d" % (m.group(0), era, ey, ERA_START[era] + n - 1, west))
        for m in re.finditer(r"(令和|平成|昭和)\s?[0０]?[1１]年", text):
            hits.append("%s: prose writes %s元年 for an era's first year; keep the numeral only where"
                        " the reader needs one, as in a form field or a quote" % (m.group(0), m.group(1)))
        for m in ERA_DATE.finditer(text):
            hit = outside_era(*m.groups())
            if hit:
                hits.append("%s: %s" % (m.group(0), hit))
        for m in re.finditer(r"(?<![0-9０-９十])[1１一]月[1１一]日[ 　]*元旦", text):
            hits.append("%s: 元旦 already means the morning of January 1; drop the month and day (令和9年 元旦)"
                        % m.group(0))
    elif lang == "zh-CN":
        for m in re.finditer(r"(?<![\d年])(\d{2})年(?=\d{1,2}月|出生|毕业|入学|入职)", text):
            hits.append("%s: write the year in full, with four digits (GB/T 15835 5.1.2)" % m.group(0))
    return hits


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="print the result as JSON")
    ap = argparse.ArgumentParser(description="Locale date forms and date lint for zh-CN, ja and ko.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show", parents=[common], help="print one ISO date in every locale form").add_argument("iso")
    lp = sub.add_parser("lint", parents=[common], help="flag misformatted dates in a text")
    lp.add_argument("lang", choices=sorted(LANGS))
    lp.add_argument("text")
    a = ap.parse_args(argv)
    if a.cmd == "show":
        try:
            forms = show(a.iso)
        except ValueError as exc:
            print("ERROR: %s" % exc)
            return 2
        print(json.dumps(forms, ensure_ascii=False) if a.json else "\n".join("%s: %s" % kv for kv in forms.items()))
        return 0
    hits = lint(LANGS[a.lang], a.text)
    if a.json:
        print(json.dumps(hits, ensure_ascii=False))
    elif hits:
        print("FAIL: %d date%s to fix." % (len(hits), "" if len(hits) == 1 else "s"))
        print("\n".join("- " + h for h in hits))
    else:
        print("PASS: no date breaks the %s rules this script checks." % LANGS[a.lang])
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
