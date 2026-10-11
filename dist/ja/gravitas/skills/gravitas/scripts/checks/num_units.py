#!/usr/bin/env python3
"""Convert and check large numbers across 万/亿 (zh), 万/億/兆 (ja), 만/억/조 (ko),
lakh/crore (en-IN) and thousand/million/billion (en).

    python num_units.py parse "4万8"                  # the value, and every locale form
    python num_units.py same "1.5 crore" "1500万"     # PASS when all expressions are equal
    python num_units.py show 1234567898              # every locale form of an integer
    python num_units.py daxie 12000                  # 人民币壹万贰仟元整
    python num_units.py ko-amount 113560             # 금113,560원(금일십일만삼천오백육십원)
    python num_units.py ranges "增长13～17万元"      # GB/T 15835 range check

Expressions are digits with units: "4万8", "128.6万", "12억 3456만 7898",
"3억 2천만", "5兆100億30万円", "1.5 crore", "12 lakh", "1,23,45,678",
"1.2 million". Currency signs and words are ignored. A bare digit after a large
unit ("4万8") is read as the next lower place, 48,000, and flagged as colloquial.
After 零 the next digits stay in their written place: 4万零8 is 40,008, and 零 is
read only right after a unit. A 千/천, 百/백 or 十/십 tail after 亿, 億, 억, 兆 or 조
with no 万/만 ("3억 5천") is read as spoken, 350,000,000, and flagged with the
reading as written; 零 before the tail keeps the written reading.
Chinese numerals written as words (两万, 三千) are not read.

Sources for the forms:
  - 公用文作成の考え方 (2022): 5兆100億30万円
  - 한글 맞춤법 제44항: 12억 3456만 7898
  - 행정업무의 운영 및 혁신에 관한 규정 시행규칙 제2조 ②: 금113,560원(금일십일만삼천오백육십원)
  - GB/T 15835-2011 5.1.3 and 5.3: 9亿～16亿, not 9～16亿; 10亿零817万5288
  - 支付结算办法 第13条: capital numerals. The 元整, 角 and 分 suffix rules come from its
    appendix, which was not checked, so treat daxie output as standard practice.
Lakh (10^5) and crore (10^7) are standard Indian numbering.

Exit 0 on success or PASS, 1 on FAIL (same, ranges), 2 when an expression cannot be read.
"""
import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation

BIG = {"万亿": 10**12, "萬億": 10**12, "万": 10**4, "萬": 10**4, "만": 10**4, "亿": 10**8, "億": 10**8, "억": 10**8,
       "兆": 10**12, "조": 10**12, "lakh": 10**5, "crore": 10**7,
       "thousand": 10**3, "million": 10**6, "billion": 10**9, "trillion": 10**12}
DROPPED = {"亿": "万", "億": "万", "억": "만", "万亿": "亿", "萬億": "億", "兆": "億", "조": "억"}  # the unit speech leaves off after each
SMALL = {"千": 1000, "천": 1000, "百": 100, "백": 100, "十": 10, "십": 10}
NUM = r"\d[\d,]*(?:\.\d+)?"
TOKEN = re.compile(r"(%s)?([千천百백十십]?)(万亿|萬億|万|萬|만|亿|億|억|兆|조|lakh|crore|thousand|million|billion|trillion)?" % NUM)
RANGE = re.compile(r"(\d+(?:\.\d+)?)\s*([～~\u2014\u2013-]|至|到)\s*(\d+(?:\.\d+)?)\s*(万亿|万|亿|%|％|‰)")


def parse(expr):
    """(integer value, notes) for an expression such as '4万8' or '1.5 crore'. ValueError if unreadable."""
    s = expr.strip().lower().replace(" ", "").replace("　", "")
    s = re.sub(r"lakhs", "lakh", s)
    s = re.sub(r"crores", "crore", s)
    s = re.sub(r"[元円원₹$¥￥]|rupees?|rs\.?|inr|won|yuan|yen|rmb", "", s)
    if not s:
        raise ValueError("nothing to read in %r" % expr)
    notes, total, pos, last_unit = [], Decimal(0), 0, None
    big_name, tail, tail_small, gap, after_unit = None, Decimal(0), False, False, False  # after the last large unit
    while pos < len(s):
        if s[pos] == "零":  # 10亿零817万, 4万零8: a skipped place, so what follows is read as written
            if not after_unit:
                raise ValueError("cannot read %r in %r" % (s[pos:], expr))
            gap, pos = True, pos + 1
            continue
        m = TOKEN.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError("cannot read %r in %r" % (s[pos:], expr))
        num, small, big = m.groups()
        try:
            coef = Decimal(num.replace(",", "")) if num else Decimal(1)
        except InvalidOperation:
            raise ValueError("cannot read %r in %r" % (num, expr))
        if small:
            coef *= SMALL[small]
        if big:
            total += coef * BIG[big]
            last_unit = BIG[big]
            big_name, tail, tail_small, gap = big, Decimal(0), False, False
        elif num and last_unit and not small and not gap and len(num) == 1 and m.end() == len(s):
            part = coef * last_unit // 10
            total += part
            notes.append("'%s' after the unit read as %s (colloquial; write it in full)" % (num, format(int(part), ",")))
        else:
            total += coef
            tail += coef
            tail_small = tail_small or bool(small)
        after_unit = bool(small or big)
        pos = m.end()
    if big_name in DROPPED and tail_small and not gap and tail < 10**4:
        strict = total
        total += tail * (BIG[big_name] // 10**4 - 1)  # "3억 5천" is said for 3억 5천만
        notes.append("the tail after %s read as %s, as spoken with %s left off; as written it is %s, "
                     "so write %s or the digits to be sure" % (big_name, format(int(total), ","), DROPPED[big_name],
                                                              format(int(strict), ","), DROPPED[big_name]))
    if total != total.to_integral_value():
        notes.append("not a whole number; rounded down")
    return int(total), notes


def east_asian(n, units, sep=""):
    """Four-digit groups with 万/億/兆-type units, skipping empty groups: 5兆100億30万."""
    parts = []
    for unit, size in ((units[2], 10**12), (units[1], 10**8), (units[0], 10**4)):
        q, n = divmod(n, size)
        if q:
            parts.append("%d%s" % (q, unit))
    if n:
        parts.append(str(n))
    return sep.join(parts) or "0"


def indian(n):
    s = str(n)
    if len(s) <= 3:
        return s
    head = re.sub(r"(\d)(?=(\d{2})+$)", r"\1,", s[:-3])
    return "%s,%s" % (head, s[-3:])


def indian_words(n):
    for name, size in (("crore", 10**7), ("lakh", 10**5)):
        if n >= size:
            v = (Decimal(n) / size).normalize()
            return "%s %s" % (format(v, "f"), name)
    return str(n)


def show(n):
    return {"en": format(n, ","), "en-IN": "%s (%s)" % (indian(n), indian_words(n)),
            "zh-CN": east_asian(n, ("万", "亿", "万亿")), "ja": east_asian(n, ("万", "億", "兆")),
            "ko": east_asian(n, ("만", "억", "조"), sep=" ")}


def daxie(n):
    """人民币 capital numerals for a whole number of yuan: 10050 -> 人民币壹万零伍拾元整."""
    digits, units, bigs = "零壹贰叁肆伍陆柒捌玖", ["仟", "佰", "拾", ""], ["", "万", "亿", "万亿"]
    if n >= 10**16:
        raise ValueError("give a whole number below 10^16; daxie writes amounts up to 万亿")
    groups = []
    while n:
        n, g = divmod(n, 10000)
        groups.append(g)
    out, need_zero = [], False
    for gi in range(len(groups) - 1, -1, -1):
        g = groups[gi]
        if g == 0:
            need_zero = True
            continue
        if need_zero or (out and g < 1000):
            out.append("零")
        need_zero, started, zero_pending = False, False, False
        for i, ch in enumerate("%04d" % g):
            v = int(ch)
            if v == 0:
                zero_pending = started
                continue
            if zero_pending:
                out.append("零")
                zero_pending = False
            out.append(digits[v] + units[i])
            started = True
        out.append(bigs[gi])
    return "人民币%s元整" % ("".join(out).replace("零零", "零") or "零")


def ko_amount(n):
    """금113,560원(금일십일만삼천오백육십원). 일 is kept before 십, 백 and 천, as the 시행규칙 example writes it."""
    d, u = "영일이삼사오육칠팔구", ["천", "백", "십", ""]

    def group(g):
        return "".join(d[int(c)] + u[i] for i, c in enumerate("%04d" % g) if c != "0")
    out, m = [], n
    for unit, size in (("조", 10**12), ("억", 10**8), ("만", 10**4)):
        g, m = divmod(m, size)
        if g:
            out.append(group(g) + unit)
    if m:
        out.append(group(m))
    return "금%s원(금%s원)" % (format(n, ","), "".join(out) or "영")


def zh_ranges(text):
    """GB/T 15835 5.1.3: keep 万, 亿, % and ‰ on both ends of a range joined by ～, —, 至 or 到.
    Ordinary units (kg, 元) may be dropped. The fix keeps 至 or 到 as written; a range from 0 is skipped."""
    out = []
    for m in RANGE.finditer(text):
        a, sep, b, unit = m.groups()
        if float(a) == 0:  # 从0到1亿 reads the same either way
            continue
        out.append("%s -> %s%s%s%s%s" % (m.group(0), a, unit, sep if sep in "至到" else "～", b, unit))
    return out


def forms_text(n):
    return "\n".join("  %s: %s" % kv for kv in show(n).items())


def run(a):
    """Print the result of one subcommand and return the exit status."""
    if a.cmd == "parse":
        v, notes = parse(a.expr)
        if a.json:
            print(json.dumps({"value": v, "notes": notes, "forms": show(v)}, ensure_ascii=False))
            return 0
        print("%s = %s" % (a.expr, format(v, ",")))
        print(forms_text(v))
        for x in notes:
            print("note: " + x)
        return 0
    if a.cmd == "same":
        vals = [(e,) + parse(e) for e in a.exprs]
        ok = len({v for _, v, _ in vals}) == 1
        if a.json:
            print(json.dumps({"same": ok, "values": {e: v for e, v, _ in vals}}, ensure_ascii=False))
            return 0 if ok else 1
        if ok:
            print("PASS: %s all equal %s." % (", ".join(a.exprs), format(vals[0][1], ",")))
        else:
            print("FAIL: the values differ.")
            for e, v, _ in vals:
                print("- %s = %s" % (e, format(v, ",")))
        for e, _, notes in vals:
            for x in notes:
                print("note: %s: %s" % (e, x))
        return 0 if ok else 1
    if a.cmd == "ranges":
        hits = zh_ranges(a.text)
        if a.json:
            print(json.dumps(hits, ensure_ascii=False))
        elif hits:
            print("FAIL: GB/T 15835 keeps 万, 亿, % and ‰ on both ends of a range.")
            for h in hits:
                print("- " + h)
        else:
            print("PASS: no range drops 万, 亿, % or ‰ from its first value.")
        return 1 if hits else 0
    if a.n < 0:
        raise ValueError("give a whole number of 0 or more")
    if a.cmd == "show":
        print(json.dumps(show(a.n), ensure_ascii=False) if a.json else format(a.n, ",") + "\n" + forms_text(a.n))
    else:
        text = daxie(a.n) if a.cmd == "daxie" else ko_amount(a.n)
        print(json.dumps({a.cmd: text}, ensure_ascii=False) if a.json else text)
    return 0


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="print the result as JSON")
    ap = argparse.ArgumentParser(description="Convert and check large numbers across locales.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("parse", parents=[common], help="read an expression and print every locale form").add_argument("expr")
    sub.add_parser("same", parents=[common], help="PASS when all expressions have the same value").add_argument(
        "exprs", nargs="+")
    for name in ("show", "daxie", "ko-amount"):
        sub.add_parser(name, parents=[common]).add_argument("n", type=int)
    sub.add_parser("ranges", parents=[common], help="GB/T 15835 range check on a text").add_argument("text")
    a = ap.parse_args(argv)
    try:
        return run(a)
    except ValueError as exc:
        print("ERROR: %s" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
