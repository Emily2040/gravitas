#!/usr/bin/env python3
"""Check a 对联: length, 仄起平收, 平仄相对 at the nodes, 重字, embedded characters and the 横批.

    python couplet_check.py 上联 下联 [--hengpi 横批] [--require 知味] [--scheme both]
    python couplet_check.py "知味停车香满座" "闻香下马客盈门" --hengpi "宾至如归" --require 知味

Give the two lines and the 横批 as separate arguments, in simplified characters,
so nothing is guessed from surrounding prose.

Rules:
  - the 上联 and 下联 have the same number of characters
  - the 上联 ends on 仄 and the 下联 ends on 平 (仄起平收)
  - 平仄相对 at positions 2, 4 and 6 (the nodes), where a line has them before its
    last character. Checking the nodes only is the lenient reading; positions
    beyond 6 in a long couplet follow its phrase breaks and are not checked.
  - no character stands at the same position in both lines (同位重字); a 虚词
    such as 之, 而 or 不 there is a note. The other 不规则重字 are notes: a
    character repeated in one line where the other line does not repeat one
    character at those positions, and a character in both lines at different
    positions (异位重字), which some famous couplets carry
  - every character given with --require appears in the 上联 or the 下联
  - the 横批 has 4 characters (a note), or exactly --hengpi-len characters (a problem)

--scheme both (the default) judges tones by 平水韵 and by 中华新韵 and reports a
tone problem only when it fails under both; a failure under one system alone
is a note. --scheme pingshui or --scheme xinyun judges by that system only.
A character missing from a table counts as either tone, so it never fails a
rule; when no system could judge a rule because of one, a PASS names it.

Prints PASS or FAIL with the problems, one per line. Exit 0 on PASS, 1 on FAIL,
2 when the input or the check data cannot be read.
"""
import argparse
import json
import os
import sys

sys.dont_write_bytecode = True  # keep __pycache__ out of the installed plugin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zh_tones as zt  # noqa: E402

NODES = (1, 3, 5)
# 虚词 that 联律 lets stand at the same position in both lines; any other character there is 同位重字
XUCI = set("之乎者也而以于於其与且则乃焉哉矣兮所不无亦的了着地得")


def repeat_findings(up, down):
    """同位重字 as problems, with a 虚词 there as a note, and the other 不规则重字 as notes."""
    probs, notes = [], []
    if len(up) != len(down):
        return probs, notes
    for i, (cu, cd) in enumerate(zip(up, down), 1):
        if cu == cd and cu in XUCI:
            notes.append("position %d: the 虚词 %s is in both lines (同位重字), which 联律 accepts" % (i, cu))
        elif cu == cd:
            probs.append("position %d: %s is in both lines at the same position (同位重字)" % (i, cu))
    for a, b, name, other in ((up, down, "上联", "下联"), (down, up, "下联", "上联")):
        for c in dict.fromkeys(a):
            pos = [i for i, x in enumerate(a) if x == c]
            if len(pos) > 1 and [i for i, x in enumerate(b) if x == b[pos[0]]] != pos:
                notes.append("%s repeats in the %s at positions %s, and the %s does not repeat one character at "
                             "those positions (不规则重字)" % (c, name, ", ".join(str(i + 1) for i in pos), other))
    for c in dict.fromkeys(up):
        pu = [i + 1 for i, x in enumerate(up) if x == c]
        pd = [i + 1 for i, x in enumerate(down) if x == c]
        if pd and not set(pu) & set(pd):
            notes.append("%s is in the 上联 at position %s and in the 下联 at position %s (异位重字)"
                         % (c, ", ".join(map(str, pu)), ", ".join(map(str, pd))))
    if probs:
        notes.append("a 同位重字 the person asked for, or a deliberate device, can stay; say why")
    return probs, notes


def tone_problems(up, down, scheme):
    """Tone problems under one scheme, as (key, message) pairs, the tone marks of both lines, the
    characters each checked rule reads, and the rules this scheme could not judge."""
    tu = [zt.lookup(c, scheme) for c in up]
    td = [zt.lookup(c, scheme) for c in down]
    out = []
    reads = {"end-up": [(up[-1], tu[-1][2])], "end-down": [(down[-1], td[-1][2])]}
    for p in NODES:
        if p < min(len(up), len(down)) - 1:
            reads["node%d" % (p + 1)] = [(up[p], tu[p][2]), (down[p], td[p][2])]
    blind = {key for key, cells in reads.items() if not all(k for _, k in cells)}
    if tu and not zt.can_be_ze(tu[-1][0]):
        out.append(("end-up", "the 上联 ends on %s, which is 平; it must end on 仄" % up[-1]))
    if td and not zt.can_be_ping(td[-1][0]):
        out.append(("end-down", "the 下联 ends on %s, which is 仄; it must end on 平" % down[-1]))
    for p in NODES:
        if p < min(len(up), len(down)) - 1 and not zt.opposite(tu[p][0], td[p][0]):
            out.append(("node%d" % (p + 1), "position %d: %s and %s are not opposite in tone (平仄相对)"
                        % (p + 1, up[p], down[p])))
    marks = ["".join(zt.mark(t, k) for t, _, k in row) for row in (tu, td)]
    return out, marks, reads, blind


def check(up, down, hengpi=None, require="", scheme="both", hengpi_len=None):
    up, down, hengpi, require = zt.han(up), zt.han(down), zt.han(hengpi or ""), zt.han(require or "")
    res = {"scheme": scheme, "up": up, "down": down, "hengpi": hengpi, "tones": {}, "problems": [], "notes": [],
           "unchecked": []}
    p, notes = res["problems"], res["notes"]
    if not up or not down:
        p.append("give both the 上联 and the 下联")
        return res
    if len(up) != len(down):
        p.append("the 上联 has %d characters and the 下联 %d; they must be equal" % (len(up), len(down)))
    schemes = ["pingshui", "xinyun"] if scheme == "both" else [scheme]
    found, reads, blind = {}, {}, {}
    for s in schemes:
        probs, marks, reads, blind[s] = tone_problems(up, down, s)
        res["tones"][zt.SCHEMES[s]] = marks
        for key, msg in probs:
            found.setdefault(key, {})[s] = msg
    # A rule is judged when it fails under every system, or some system passes it knowing every character it reads.
    for key, cells in reads.items():
        failed = found.get(key, {})
        if len(failed) < len(schemes) and not any(s not in failed and key not in blind[s] for s in schemes):
            res["unchecked"].append({"rule": key, "chars": "".join(dict.fromkeys(c for c, _ in cells))})
    for key, by in found.items():
        msg = next(iter(by.values()))
        if len(by) == len(schemes):
            p.append(msg + ("" if scheme != "both" else " (under both 平水韵 and 中华新韵)"))
        else:
            only = zt.SCHEMES[next(iter(by))]
            notes.append("%s, under %s only" % (msg, only))
    rp, rn = repeat_findings(up, down)
    p.extend(rp)
    notes.extend(rn)
    if len(up) > 7:
        notes.append("positions beyond 6 are not checked; in a long couplet the nodes follow the phrase breaks")
    for ch in dict.fromkeys(require):
        if ch not in up + down:
            p.append("%s is not in the 上联 or the 下联" % ch)
    if hengpi:
        if hengpi_len and len(hengpi) != hengpi_len:
            p.append("the 横批 %s has %d characters; %d were asked for" % (hengpi, len(hengpi), hengpi_len))
        elif not hengpi_len and len(hengpi) != 4:
            notes.append("the 横批 %s has %d characters; most have 4" % (hengpi, len(hengpi)))
    for s in schemes:
        missing = "".join(dict.fromkeys(c for c in up + down if not zt.lookup(c, s)[2]))
        if missing:
            notes.append("not in the %s table, so counted as either tone: %s" % (zt.SCHEMES[s], missing))
    return res


def render(res):
    k = len(res["problems"])
    by = "平水韵 and 中华新韵" if res["scheme"] == "both" else zt.SCHEMES[res["scheme"]]
    if not k:
        lines = ["PASS: couplet %s / %s, tones by %s. Length, 仄起平收, the nodes, 同位重字 and the required characters"
                 " hold." % (res["up"], res["down"], by)]
        if res.get("unchecked"):
            where = {"end-up": "the 上联 ending", "end-down": "the 下联 ending"}
            places = ", ".join("%s (%s)" % (where.get(u["rule"], "position " + u["rule"][4:]), u["chars"])
                               for u in res["unchecked"])
            lines = ["PASS: couplet %s / %s, tones by %s, except %s: a character there is not in the table, so"
                     " that tone is unchecked. Length, 仄起平收, the other nodes, 同位重字 and the required"
                     " characters hold." % (res["up"], res["down"], by, places)]
    else:
        lines = ["FAIL: couplet %s / %s, tones by %s, %d problem%s." % (res["up"], res["down"], by, k,
                                                                     "" if k == 1 else "s")]
        lines += ["- " + x for x in res["problems"]]
        for name, (mu, md) in res["tones"].items():
            lines.append("tones by %s: %s / %s (中 = either, ? = not in the table)" % (name, mu, md))
    lines += ["note: " + x for x in res["notes"]]
    return "\n".join(lines)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Check a 对联.")
    ap.add_argument("up", help="the 上联")
    ap.add_argument("down", help="the 下联")
    ap.add_argument("--hengpi", help="the 横批, if there is one")
    ap.add_argument("--hengpi-len", type=int, help="the number of characters the 横批 must have")
    ap.add_argument("--require", default="", help="characters that must appear in the couplet, such as 知味")
    ap.add_argument("--scheme", choices=["both"] + sorted(zt.SCHEMES), default="both")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    a = ap.parse_args(argv)
    if not zt.han(a.up) or not zt.han(a.down):
        print("ERROR: the 上联 and the 下联 must both contain Chinese characters")
        return 2
    res = check(a.up, a.down, a.hengpi, a.require, a.scheme, a.hengpi_len)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else render(res))
    return 1 if res["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
