#!/usr/bin/env python3
"""Tests for the language checks in plugin/skills/gravitas/scripts/checks/.

Run with plain `python tests/scripts/test_checks.py`. Each case prints one PASS
or FAIL line; the exit status is 1 if any case fails.

Every check is seen going red on a known bad sample and green on a known good
one: 王昌龄《出塞》 and 杜甫《春望》 against the benchmark's 窗/霜 poem, the couplets
the benchmark stored, the 古池 haiku with an 8-mora middle line, 정몽주's 단심가
against a three-line modern poem, and the official number and date examples
the scripts name as their sources. The command-line cases run each script as
the agent would, check the verdict line and the exit status, and check that a
run leaves no __pycache__ inside the plugin. The last cases check the data
files' provenance headers, that the checks import only the standard library,
and that a localized build carries the checks and their data.
"""
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):  # the case names are CJK; a Windows console defaults to cp1252
        _stream.reconfigure(encoding="utf-8", errors="backslashreplace")
HERE =os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHECKS = os.path.join(REPO, "plugin", "skills", "gravitas", "scripts", "checks")
DATA = os.path.join(CHECKS, "data")
SCRIPTS = ["pingze_check.py", "couplet_check.py", "mora_count.py", "sijo_check.py", "num_units.py",
           "locale_dates.py"]
sys.path.insert(0, CHECKS)
sys.path.insert(0, os.path.join(REPO, "scripts"))
import zh_tones as zt  # noqa: E402
import pingze_check as pc  # noqa: E402
import couplet_check as cc  # noqa: E402
import mora_count as mc  # noqa: E402
import sijo_check as sc  # noqa: E402
import num_units as nu  # noqa: E402
import locale_dates as ld  # noqa: E402

RESULTS = []
CHUSAI = "秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度阴山。"
CHUANG_SHUANG = "百丈高楼灯火尽，唯留片影对秋窗。删繁补阙程期促，踏月归时满地霜。"
CHUNWANG = "国破山河在，城春草木深。感时花溅泪，恨别鸟惊心。烽火连三月，家书抵万金。白头搔更短，浑欲不胜簪。"
GUANQUE = "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。"
DANSIM = ["이 몸이|죽고 죽어|일백 번|고쳐 죽어", "백골이|진토되어|넋이라도|있고 없고", "임 향한|일편단심이야|가실 줄이|있으랴"]
SIJO_RED = ["가을밤|창가에서|달빛을|바라보며", "그대를|그리면서|홀로|앉았노라", "그리고 나는|오늘도|너를|생각한다"]


def case(name, fn):
    try:
        ok, detail = fn()
    except (Exception, SystemExit) as exc:  # a crash is a failure, not an abort
        ok, detail = False, "%s: %s" % (type(exc).__name__, exc)
    RESULTS.append(bool(ok))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  -- " + str(detail)))


def run(script, *args):
    """(exit status, stdout) of one check run as a command, the way the agent runs it."""
    env = dict(os.environ)
    env.pop("PYTHONIOENCODING", None)  # the scripts must set UTF-8 output themselves
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    r = subprocess.run([sys.executable, os.path.join(CHECKS, script)] + list(args),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return r.returncode, r.stdout.decode("utf-8") + r.stderr.decode("utf-8", "replace")


def expect(script, args, code, first):
    def fn():
        got, out = run(script, *args)
        return got == code and out.startswith(first), "exit %s, output: %s" % (got, out.strip()[:300])
    return fn


def _raises(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False


# ---------------------------------------------------------------- data

def pingshui_groups():
    counts = {}
    for kind, name, chars in zt._rows("pingshui.tsv"):
        counts[kind] = counts.get(kind, 0) + 1
    want = {"上平声": 15, "下平声": 15, "上声": 29, "去声": 30, "入声": 17}
    return counts == want, "groups per kind: %s" % counts


case("data: pingshui.tsv holds the 106 groups (15 + 15 平, 29 上, 30 去, 17 入)", pingshui_groups)


def header(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return "".join(l for l in fh if l.startswith("#"))


case("data: pingshui.tsv records its source page, revision and licence",
     lambda: (all(s in header("pingshui.tsv") for s in ("zh.wikisource.org/wiki/平水韻", "revision 8264804",
                                                         "PD-old", "CC BY-SA 4.0")), header("pingshui.tsv")[:300]))
case("data: mandarin.tsv records pypinyin as its source and carries the MIT notice",
     lambda: (all(s in header("mandarin.tsv") for s in ("pypinyin 0.55.0", "The MIT License", "mozillazg",
                                                         "Permission is hereby granted")), header("mandarin.tsv")[:300]))


def mandarin_readings_valid():
    bad = [(ch, r) for ch, rs in zt.mandarin().items() for r in rs if not re.fullmatch(r"[a-z]+[1-4]", r)]
    return not bad and len(zt.mandarin()) > 10000, "bad readings %s, %d entries" % (bad[:5], len(zt.mandarin()))


case("data: every Mandarin reading is numbered pinyin with tone 1 to 4", mandarin_readings_valid)
case("data: 窗 is 上平声三江 and 霜 下平声七阳 in 平水韵",
     lambda: (zt.lookup("窗", "pingshui")[1] == ["上平声三江"] and zt.lookup("霜", "pingshui")[1] == ["下平声七阳"],
              (zt.lookup("窗", "pingshui"), zt.lookup("霜", "pingshui"))))
case("data: 国 is 仄 in 平水韵 (入声) and 平 in 中华新韵",
     lambda: (zt.lookup("国", "pingshui")[0] == {zt.ZE} and zt.lookup("国", "xinyun")[0] == {zt.PING},
              (zt.lookup("国", "pingshui"), zt.lookup("国", "xinyun"))))
case("data: the sandhi forms of 一 and 不 do not count (一 平, 不 仄 in 中华新韵)",
     lambda: (zt.lookup("一", "xinyun")[0] == {zt.PING} and zt.lookup("不", "xinyun")[0] == {zt.ZE},
              (zt.lookup("一", "xinyun"), zt.lookup("不", "xinyun"))))


def xinyun_finals():
    want = {"shuang1": "十唐", "ju1": "十二齐", "xue2": "三皆", "zhi1": "十三支", "er2": "十二齐", "gui1": "五微",
            "liu2": "七尤", "lun2": "九文", "xiong2": "十一庚", "yuan2": "八寒", "wo1": "二波", "lve4": "三皆",
            "hua1": "一麻", "kai1": "四开", "hao2": "六豪", "hu2": "十四姑", "yun2": "九文", "qiong2": "十一庚"}
    got = {r: zt.xinyun_group(r) for r in want}
    return got == want, "differs: %s" % {r: g for r, g in got.items() if g != want[r]}


case("data: pinyin finals map to the 14 中华新韵 groups", xinyun_finals)

# ---------------------------------------------------------------- 绝句 and 律诗

case("pingze: 出塞 passes under 平水韵", lambda: (not pc.check(CHUSAI)["problems"], pc.check(CHUSAI)))
case("pingze: 春望 (五言律诗) passes under 平水韵; 恨别鸟惊心 (仄仄仄平平) is not 孤平",
     lambda: (not pc.check(CHUNWANG)["problems"] and pc.check(CHUNWANG)["form"] == "五言律诗", pc.check(CHUNWANG)))
case("pingze: the benchmark's 窗/霜 poem fails 平水韵 on the rhyme group",
     lambda: (any("share no" in p for p in pc.check(CHUANG_SHUANG)["problems"]), pc.check(CHUANG_SHUANG)))
case("pingze: the same poem passes 中华新韵, where 窗 and 霜 are both 十唐",
     lambda: (not pc.check(CHUANG_SHUANG, "xinyun")["problems"], pc.check(CHUANG_SHUANG, "xinyun")))
case("pingze: 登鹳雀楼 passes 平水韵 and fails 中华新韵 on 三平尾, because 一 reads 平 in Mandarin",
     lambda: (not pc.check(GUANQUE)["problems"]
              and pc.check(GUANQUE, "xinyun")["problems"] == ["line 4: the last three characters are all 平 (三平尾)"],
              (pc.check(GUANQUE), pc.check(GUANQUE, "xinyun"))))
case("pingze: 仄平仄仄平 in a rhyme line is 孤平",
     lambda: (pc.check(GUANQUE.replace("黄河", "白河"))["problems"] == ["line 2: only one 平 besides the rhyme word (孤平)"],
              pc.check(GUANQUE.replace("黄河", "白河"))))
case("pingze: 仄仄仄平仄仄平 in a 7-character rhyme line is 孤平",
     lambda: (lambda r: (r["problems"] == ["line 2: only one 平 besides the rhyme word (孤平)"], r))(
         pc.check(CHUSAI.replace("万里长征人", "万里远征客"))))
case("pingze: a three-line poem fails on the line count",
     lambda: (pc.check("床前明月光，疑是地上霜。举头望明月。")["problems"] == ["3 lines; a 绝句 has 4 and a 律诗 has 8"],
              pc.check("床前明月光，疑是地上霜。举头望明月。")))
case("pingze: mixed line lengths fail",
     lambda: ("line lengths" in pc.check("秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度山。")["problems"][0], ""))
case("pingze: a broken 二四分明 is reported with the 拗救 note",
     lambda: (lambda r: (any("二四分明" in p for p in r["problems"]) and any("拗救" in n for n in r["notes"]), r))(
         pc.check(CHUSAI.replace("明月汉", "明风汉"))))
case("pingze: a character missing from the table counts as either tone and is named in a note",
     lambda: (lambda r: (not r["problems"] and any("時" in n for n in r["notes"]), r))(
         pc.check(CHUSAI.replace("秦时", "秦時"))))
case("pingze: a traditional 時 at a read position stays a PASS that names it",
     lambda: (lambda r: (not r["problems"] and r["unchecked"] == "時", r))(pc.check(CHUSAI.replace("秦时", "秦時"))))
case("pingze: an unknown first character of a 7-character line is not reported as unchecked",
     lambda: (lambda r: (not r["problems"] and r["unchecked"] == "", r))(pc.check(CHUSAI.replace("秦时", "龘时"))))
case("pingze: the swapped 出塞 with a traditional character still fails",
     lambda: (lambda r: (bool(r["problems"]), r))(pc.check(
         "万里長征人未还，秦时明月汉时关。不教胡马度阴山，但使龙城飞将在。")))

# ---------------------------------------------------------------- couplets

case("couplet: 知味停车香满座 / 闻香下马客盈门 passes, 横批 宾至如归, 知味 embedded",
     lambda: (not cc.check("知味停车香满座", "闻香下马客盈门", "宾至如归", "知味")["problems"],
              cc.check("知味停车香满座", "闻香下马客盈门", "宾至如归", "知味")))
case("couplet: the lines swapped fail 仄起平收 at both ends",
     lambda: (lambda r: (len(r["problems"]) == 2 and all("must end on" in p for p in r["problems"]), r))(
         cc.check("闻香下马客盈门", "知味停车香满座")))
case("couplet: the stored Gravitas answer 循香驻足方知味 / 落座嗦粉顿生津 fails at position 6 under both systems",
     lambda: (lambda r: (r["problems"] == ["position 6: 知 and 生 are not opposite in tone (平仄相对) "
                                           "(under both 平水韵 and 中华新韵)"], r))(cc.check("循香驻足方知味", "落座嗦粉顿生津")))
case("couplet: a node that fails under 中华新韵 only is a note with --scheme both, a problem with --scheme xinyun",
     lambda: (lambda b, x: (not b["problems"] and any("中华新韵 only" in n for n in b["notes"])
                            and any("position 2" in p for p in x["problems"]), (b, x)))(
         cc.check("家国春光好", "春天喜事多"), cc.check("家国春光好", "春天喜事多", scheme="xinyun")))
case("couplet: unequal lengths fail", lambda: (any("must be equal" in p for p in cc.check(
    "知味停车香满座", "闻香下马客盈")["problems"]), ""))
case("couplet: a required character that is missing fails",
     lambda: (cc.check("知味停车香满座", "闻香下马客盈门", require="鲜")["problems"] == ["鲜 is not in the 上联 or the 下联"], ""))
case("couplet: a 5-character 横批 is a note, and a problem when --hengpi-len 4 is given",
     lambda: (lambda a, b: (not a["problems"] and any("most have 4" in n for n in a["notes"])
                            and any("4 were asked for" in p for p in b["problems"]), (a, b)))(
         cc.check("知味停车香满座", "闻香下马客盈门", "宾至如归天"),
         cc.check("知味停车香满座", "闻香下马客盈门", "宾至如归天", hengpi_len=4)))
case("couplet: 春风送暖花千树 / 春雨润心花万家 fails on 同位重字 at positions 1 and 5",
     lambda: (lambda r: ([x for x in r["problems"] if "同位重字" in x]
                         == ["position 1: 春 is in both lines at the same position (同位重字)",
                             "position 5: 花 is in both lines at the same position (同位重字)"], r))(
         cc.check("春风送暖花千树", "春雨润心花万家")))
case("couplet: 春风送暖花开早 / 春雨滋田麦长高 fails only on 同位重字 at position 1, which the nodes miss",
     lambda: (lambda r: (r["problems"] == ["position 1: 春 is in both lines at the same position (同位重字)"], r))(
         cc.check("春风送暖花开早", "春雨滋田麦长高")))
case("couplet: mirrored repeats (天增岁月人增寿 / 春满乾坤福满门) carry no 重字 problem or note",
     lambda: (lambda r: (not any("重字" in x for x in r["problems"] + r["notes"]), r))(
         cc.check("天增岁月人增寿", "春满乾坤福满门")))
case("couplet: a 虚词 at the same position (之 in 大肚能容 / 开口便笑) is a note, not a problem",
     lambda: (lambda r: (not any("同位重字" in x for x in r["problems"]) and any("虚词 之" in n for n in r["notes"]), r))(
         cc.check("大肚能容容天下难容之事", "开口便笑笑世间可笑之人")))
case("couplet: 知味停车香满座 / 闻香下马客盈门 passes with a 香 异位重字 note",
     lambda: (lambda r: (not r["problems"] and any("异位重字" in n and "香" in n for n in r["notes"]), r))(
         cc.check("知味停车香满座", "闻香下马客盈门")))
case("couplet: traditional 知味停車香滿座 / 聞香下馬客盈門 passes cleanly with --scheme both, names the gaps under pingshui",
     lambda: (lambda b, p: (not b["problems"] and not b["unchecked"] and not p["problems"] and p["unchecked"], (b, p)))(
         cc.check("知味停車香滿座", "聞香下馬客盈門"), cc.check("知味停車香滿座", "聞香下馬客盈門", scheme="pingshui")))

# ---------------------------------------------------------------- haiku, tanka, senryu

WORDS = {"ほっとする": 5, "ボーリングじょう": 7, "ホンコン": 4, "ちょっと": 3, "きょう": 2, "コンピューター": 6,
         "ふるいけや": 5, "かわずとびこむ": 7, "みずのおと": 5}
case("mora: word counts from the koubo.jp examples and small-kana merging",
     lambda: (all(mc.morae(w) == n for w, n in WORDS.items()), {w: mc.morae(w) for w in WORDS}))
case("mora: the 古池 haiku is 5-7-5",
     lambda: (lambda r: (not r["deviations"] and not r["errors"], r))(mc.check("haiku", ["ふるいけや", "かわずとびこむ", "みずのおと"])))
case("mora: an 8-mora middle line is 字余り",
     lambda: (lambda r: (r["deviations"] == ["line 2: かえるがとびこむ has 8 morae, target 7 (字余り)"], r))(
         mc.check("haiku", ["ふるいけや", "かえるがとびこむ", "みずのおと"])))
case("mora: a 4-mora first line is 字足らず",
     lambda: (lambda r: (r["deviations"] == ["line 1: ふるいけ has 4 morae, target 5 (字足らず)"], r))(
         mc.check("senryu", ["ふるいけ", "かわずとびこむ", "みずのおと"])))
case("mora: kanji are refused", lambda: (bool(mc.check("haiku", ["古池や", "かわずとびこむ", "みずのおと"])["errors"]), ""))
case("mora: one argument is split into lines at spaces",
     lambda: (mc.check("haiku", ["ふるいけや かわずとびこむ みずのおと"])["counts"] == [5, 7, 5], ""))
case("mora: a tanka needs 5 lines", lambda: (bool(mc.check("tanka", ["ふるいけや", "かわずとびこむ", "みずのおと"])["errors"]), ""))

# ---------------------------------------------------------------- 시조

case("sijo: 단심가 passes at 45 syllables",
     lambda: (lambda r: (not r["problems"] and r["total"] == 45, r))(sc.check(DANSIM)))
case("sijo: a modern three-line poem fails both 종장 rules",
     lambda: (lambda r: (len(r["problems"]) == 2 and all(p.startswith("종장") for p in r["problems"]), r))(sc.check(SIJO_RED)))
case("sijo: a 2-syllable 종장 first 음보 fails and names the narrower definition; 1 or 4 fail plainly",
     lambda: (lambda r2, r4: (r2["problems"] == ["종장 음보 1 has 2 syllables; the standard form fixes it at 3, and only "
                                                  "the same article's narrower definition allows 2"]
                              and r4["problems"] == ["종장 음보 1 has 4 syllables; it must be 3"], (r2, r4)))(
         sc.check(DANSIM[:2] + ["임은|일편단심이야|가실 줄이|있으랴"]), sc.check(DANSIM[:2] + ["임을향한|일편단심이야|가실 줄이|있으랴"])))
case("sijo: a 장 with 3 음보 fails", lambda: (any("3 음보" in p for p in sc.check(
    ["이 몸이|죽고 죽어|일백 번 고쳐 죽어"] + DANSIM[1:])["problems"]), ""))
case("sijo: one argument with a line per 장 is read as three 장",
     lambda: (sc.check(["\n".join(DANSIM)])["total"] == 45, ""))


def sijo_latin_refused():
    try:
        sc.check(["a|b|c|d"] + DANSIM[1:])
    except ValueError:
        return True, ""
    return False, "no error for Latin text"


case("sijo: Latin text in a 음보 is refused", sijo_latin_refused)

# ---------------------------------------------------------------- numbers

case("num: 5兆100億30万円 (公用文作成の考え方) round-trips",
     lambda: (nu.parse("5兆100億30万円")[0] == 5010000300000
              and nu.east_asian(5010000300000, ("万", "億", "兆")) == "5兆100億30万", ""))
case("num: 12억 3456만 7898 (맞춤법 제44항) round-trips with spacing at each 만 unit",
     lambda: (nu.parse("12억 3456만 7898")[0] == 1234567898 and nu.show(1234567898)["ko"] == "12억 3456만 7898", ""))
case("num: 10亿零817万5288 (GB/T 15835) reads as 1,008,175,288", lambda: (nu.parse("10亿零817万5288")[0] == 1008175288, ""))
case("num: 4万8 is 48,000 and flagged colloquial; 4.8万 is not flagged",
     lambda: (nu.parse("4万8") [0] == 48000 and nu.parse("4万8")[1] and not nu.parse("4.8万")[1], nu.parse("4万8")))
case("num: 零 keeps the next digit in its written place: 2万零8, 1亿零8, 10万零5",
     lambda: ([nu.parse(e) for e in ("2万零8", "1亿零8", "10万零5")] == [(20008, []), (100000008, []), (100005, [])],
              [nu.parse(e) for e in ("2万零8", "1亿零8", "10万零5")]))
case("num: 零 not right after a unit is refused (2零26), 〇 stays refused, 10亿零817万5288 unchanged",
     lambda: (_raises(nu.parse, "2零26") and _raises(nu.parse, "2万〇8") and _raises(nu.parse, "零")
              and nu.parse("10亿零817万5288") == (1008175288, []), ""))
case("num: 3억 5천, 1亿5千, 1億5千, 1억 3천 5백, 1조 5천 read as spoken and flagged",
     lambda: ([nu.parse(e)[0] for e in ("3억 5천", "1亿5千", "1億5千", "1억 3천 5백", "1조 5천")]
              == [350000000, 150000000, 150000000, 135000000, 1500000000000]
              and all(nu.parse(e)[1] for e in ("3억 5천", "1亿5千")),
              [nu.parse(e) for e in ("3억 5천", "1亿5千", "1億5千", "1억 3천 5백", "1조 5천")]))
case("num: 1亿零5千, 3만 5천, 1억 5000, 3억 5천만 5천 read as written, with no note",
     lambda: ([nu.parse(e) for e in ("1亿零5千", "3만 5천", "1억 5000", "3억 5천만 5천")]
              == [(100005000, []), (35000, []), (100005000, []), (350005000, [])],
              [nu.parse(e) for e in ("1亿零5千", "3만 5천", "1억 5000", "3억 5천만 5천")]))
case("num: 128.6万, 3억 2천만, 1.5 crore, 12 lakh, 1,23,45,678 and 1.2 million",
     lambda: ([nu.parse(e)[0] for e in ("128.6万", "3억 2천만", "1.5 crore", "12 lakh", "1,23,45,678", "1.2 million")]
              == [1286000, 320000000, 15000000, 1200000, 12345678, 1200000], ""))
case("num: Indian grouping and exact crore words",
     lambda: (nu.indian(12345678) == "1,23,45,678" and nu.indian_words(12345678) == "1.2345678 crore"
              and nu.indian_words(1500000) == "15 lakh", nu.indian_words(12345678)))
case("num: 금113,560원(금일십일만삼천오백육십원) and 금1,000,000원(금일백만원) (시행규칙 제2조 ②)",
     lambda: (nu.ko_amount(113560) == "금113,560원(금일십일만삼천오백육십원)"
              and nu.ko_amount(1000000) == "금1,000,000원(금일백만원)", nu.ko_amount(113560)))
case("num: capital numerals 12,000, 10,050 and 48,000",
     lambda: ([nu.daxie(n) for n in (12000, 10050, 48000)]
              == ["人民币壹万贰仟元整", "人民币壹万零伍拾元整", "人民币肆万捌仟元整"], [nu.daxie(n) for n in (12000, 10050, 48000)]))
case("num: GB/T 15835 range check flags 13～17万 and 15～30% and keeps 9亿～16亿",
     lambda: (nu.zh_ranges("预计13～17万元，占比15～30%，规模9亿～16亿") == ["13～17万 -> 13万～17万", "15～30% -> 15%～30%"], ""))
case("num: ranges read 至 and 到, keep the writer's connector, add ％ and ‰, skip a zero start",
     lambda: (nu.zh_ranges("预计收入13至17万元，增长15到30%，从0到1亿用户，占比5～8％，2-3‰")
              == ["13至17万 -> 13万至17万", "15到30% -> 15%到30%", "5～8％ -> 5％～8％", "2-3‰ -> 2‰～3‰"],
              nu.zh_ranges("预计收入13至17万元，增长15到30%，从0到1亿用户，占比5～8％，2-3‰")))

# ---------------------------------------------------------------- dates

case("date: 2026-10-04 in zh-CN, ja, 和暦 and ko forms",
     lambda: (lambda s: (s["zh-CN"] == "2026年10月4日（星期日）" and s["ja"] == "2026年10月4日（日）"
                         and s["ja-wareki"] == "令和8年10月4日" and s["ko"] == "2026. 10. 4.(일)", s))(ld.show("2026-10-04")))
case("date: an era's first year is 元年, and a date before 昭和 is refused",
     lambda: (ld.show("2019-05-01")["ja-wareki"] == "令和元年5月1日" and ld.show("1989-01-08")["ja-wareki"] == "平成元年1月8日"
              and _raises(ld.show, "1900-01-01"), ""))
case("date: ko lint flags 2026.9.30 and 2026. 09. 30. and keeps 2026. 9. 30.(수)",
     lambda: (ld.lint("ko", "퇴사일(2026.9.30)로부터") and ld.lint("ko", "2026. 09. 30.")
              and not ld.lint("ko", "2026. 9. 30.(수)까지"), ""))
case("date: ko 2025.10.01 is one date with the missing dot, the leading zero and the spaces named",
     lambda: (lambda h: (len(h) == 1 and "needs a dot" in h[0] and "leading zero" in h[0] and "space" in h[0]
                         and h[0].endswith("(2025. 10. 1.)"), h))(ld.lint("ko", "2025.10.01")))
case("date: ko range 2025.10.01 ~ 2026.09.30 is two dates; 2020.03.~2024.02. is two year-month dates",
     lambda: (len(ld.lint("ko", "2025.10.01 ~ 2026.09.30")) == 2 and len(ld.lint("ko", "2020.03.~2024.02.")) == 2,
              (ld.lint("ko", "2025.10.01 ~ 2026.09.30"), ld.lint("ko", "2020.03.~2024.02."))))
case("date: ko flags 2026.10.4.(일) and 2026. 10.4. once each, keeps 2026. 10. 4.(일), 2026.13.4. and 2001.10.01.5",
     lambda: (len(ld.lint("ko", "2026.10.4.(일)")) == 1 and len(ld.lint("ko", "2026. 10.4.")) == 1
              and not ld.lint("ko", "2026. 10. 4.(일)") and not ld.lint("ko", "2026.13.4.")
              and not ld.lint("ko", "버전 2001.10.01.5") and not ld.lint("ko", "v1.2026.01.02"),
              [ld.lint("ko", x) for x in ("2026.10.4.(일)", "2026. 10.4.", "2026.13.4.", "버전 2001.10.01.5")]))
case("date: ko keeps a no-break space after the dots",
     lambda: (not ld.lint("ko", "2026. 10. 4."), ld.lint("ko", "2026. 10. 4.")))
case("date: ja lint flags 令和7年（2026年） and keeps 令和8年（2026年）",
     lambda: (ld.lint("ja", "令和7年（2026年）") and not ld.lint("ja", "令和8年（2026年）"), ""))
case("date: ja flags 令和1年, 平成１年 and 令和 01年 and keeps 令和元年, 令和10年 and 令和11年",
     lambda: (ld.lint("ja", "令和1年5月1日") and ld.lint("ja", "平成１年") and ld.lint("ja", "令和 01年")
              and not ld.lint("ja", "令和元年（2019年）、令和11年、令和10年"), ""))
case("date: ja flags an era date its era does not cover and keeps the days either side of each change",
     lambda: (all(ld.lint("ja", x) for x in ["平成元年（1989年）1月5日", "令和元年4月1日", "平成31年（2019年）5月10日",
                                              "昭和64年2月1日", "平成35年（2023年）", "1989年（平成元年）1月7日"])
              and not any(ld.lint("ja", x) for x in ["昭和64年（1989年）1月7日", "平成元年1月8日", "平成元年1月",
                                                      "平成31年4月30日", "令和元年（2019年）5月1日", "平成31年度"]),
              [ld.lint("ja", x) for x in ["平成元年（1989年）1月5日", "平成31年（2019年）5月10日", "1989年（平成元年）1月7日"]]))
case("date: ja flags 1月1日 元旦 and １月１日元旦, keeps 令和9年 元旦, 1月1日（元旦） and 11月1日",
     lambda: (ld.lint("ja", "令和9年1月1日 元旦") and ld.lint("ja", "１月１日元旦")
              and not ld.lint("ja", "令和9年 元旦") and not ld.lint("ja", "1月1日（元旦）は休業")
              and not ld.lint("ja", "11月1日元旦"), ""))
case("date: zh lint flags 90年出生 and 26年10月 and keeps 1990年出生, 90年代 and 工作了15年",
     lambda: (len(ld.lint("zh-CN", "90年出生，26年10月")) == 2
              and not ld.lint("zh-CN", "1990年出生，90年代，工作了15年，2026年10月"), ld.lint("zh-CN", "90年出生，26年10月")))


# ---------------------------------------------------------------- command line

case("cli: pingze_check prints PASS and exits 0 on 出塞", expect("pingze_check.py", [CHUSAI], 0, "PASS: 七言绝句 by 平水韵"))
case("cli: pingze_check prints FAIL and exits 1 on the 窗/霜 poem",
     expect("pingze_check.py", [CHUANG_SHUANG], 1, "FAIL: 七言绝句 by 平水韵, 1 problem."))
case("cli: pingze_check --scheme xinyun", expect("pingze_check.py", ["--scheme", "xinyun", CHUANG_SHUANG], 0,
                                                 "PASS: 七言绝句 by 中华新韵"))
case("cli: pingze_check exits 2 on input with no Chinese", expect("pingze_check.py", ["hello"], 2, "ERROR:"))
case("cli: pingze_check names the unchecked character in the PASS line and exits 0",
     expect("pingze_check.py", [CHUSAI.replace("秦时", "秦時")], 0, "PASS: 七言绝句 by 平水韵, except 時:"))


def checks_without_data():
    tmp = tempfile.mkdtemp(prefix="gravitas-test-checks-")
    try:
        copy = os.path.join(tmp, "checks")
        shutil.copytree(CHECKS, copy, ignore=shutil.ignore_patterns("data", "__pycache__"))
        got = []
        for args in (["pingze_check.py", CHUSAI], ["couplet_check.py", "知味停车香满座", "闻香下马客盈门"]):
            r = subprocess.run([sys.executable, os.path.join(copy, args[0])] + args[1:],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            got.append((r.returncode, r.stdout.decode("utf-8", "replace")))
        ok = all(code == 2 and out.startswith("ERROR: cannot read the check data") for code, out in got)
        return ok, "runs: %s" % [(code, out.strip()[:200]) for code, out in got]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


case("cli: with data/ missing, pingze_check and couplet_check print ERROR: cannot read the check data and exit 2",
     checks_without_data)


def pingze_file_and_json():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "poem.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(CHUSAI.replace("，", "\n"))
        code, out = run("pingze_check.py", "--file", path, "--json")
    data = json.loads(out)
    return code == 0 and data["form"] == "七言绝句" and data["problems"] == [], out[:300]


case("cli: pingze_check --file reads a poem with a line per row, and --json parses", pingze_file_and_json)
case("cli: couplet_check FAIL exits 1", expect("couplet_check.py", ["闻香下马客盈门", "知味停车香满座"], 1, "FAIL: couplet"))
case("cli: couplet_check PASS exits 0", expect("couplet_check.py", ["知味停车香满座", "闻香下马客盈门", "--hengpi", "宾至如归",
                                                                   "--require", "知味"], 0, "PASS: couplet"))
case("cli: couplet_check --scheme pingshui on the traditional couplet prints PASS ... except and exits 0",
     expect("couplet_check.py", ["知味停車香滿座", "聞香下馬客盈門", "--scheme", "pingshui"], 0,
            "PASS: couplet 知味停車香滿座 / 聞香下馬客盈門, tones by 平水韵, except"))
case("cli: mora_count PASS", expect("mora_count.py", ["haiku", "ふるいけや", "かわずとびこむ", "みずのおと"], 0,
                                    "PASS: haiku 5-7-5, counted 5-7-5."))
case("cli: mora_count FAIL exits 1", expect("mora_count.py", ["haiku", "ふるいけや", "かえるがとびこむ", "みずのおと"], 1,
                                            "FAIL: haiku 5-7-5, counted 5-8-5."))
case("cli: mora_count exits 2 on kanji", expect("mora_count.py", ["haiku", "古池や", "かわずとびこむ", "みずのおと"], 2, "ERROR:"))
case("cli: sijo_check PASS", expect("sijo_check.py", DANSIM, 0, "PASS: 평시조, 3 장 of 4 음보, 45 syllables"))
case("cli: sijo_check FAIL exits 1", expect("sijo_check.py", SIJO_RED, 1, "FAIL: 평시조, 2 problems"))
case("cli: num_units same PASS", expect("num_units.py", ["same", "1.5 crore", "1500万", "15,000,000"], 0,
                                        "PASS: 1.5 crore, 1500万, 15,000,000 all equal 15,000,000."))
case("cli: num_units same FAIL exits 1", expect("num_units.py", ["same", "12억", "1.2 million"], 1, "FAIL: the values differ."))
case("cli: num_units parse exits 2 on text it cannot read", expect("num_units.py", ["parse", "abc"], 2, "ERROR:"))
case("cli: num_units ranges FAIL exits 1", expect("num_units.py", ["ranges", "增长13～17万元"], 1, "FAIL: GB/T 15835"))
case("cli: num_units daxie", expect("num_units.py", ["daxie", "10050"], 0, "人民币壹万零伍拾元整"))
case("cli: locale_dates lint FAIL exits 1", expect("locale_dates.py", ["lint", "ko", "2026.9.30까지"], 1, "FAIL: 1 date to fix."))
case("cli: locale_dates lint PASS", expect("locale_dates.py", ["lint", "ko", "2026. 9. 30.(수)까지"], 0, "PASS:"))
case("cli: locale_dates lint ja 1月1日 元旦 FAIL", expect("locale_dates.py", ["lint", "ja", "令和9年1月1日 元旦"], 1,
                                                       "FAIL: 1 date to fix."))
case("cli: locale_dates lint ja 元旦 PASS", expect("locale_dates.py", ["lint", "ja", "令和9年 元旦"], 0, "PASS:"))
case("cli: locale_dates show", expect("locale_dates.py", ["show", "2026-10-04"], 0, "zh-CN: 2026年10月4日（星期日）"))
case("cli: locale_dates show exits 2 on a bad date", expect("locale_dates.py", ["show", "2026-13-01"], 2, "ERROR:"))
case("cli: running the checks leaves no __pycache__ in the plugin",
     lambda: (not os.path.exists(os.path.join(CHECKS, "__pycache__")), "found %s" % os.path.join(CHECKS, "__pycache__")))

# ---------------------------------------------------------------- shipping


def stdlib_only():
    stdlib = set(getattr(sys, "stdlib_module_names", ())) or {
        "argparse", "datetime", "decimal", "json", "os", "re", "sys", "unicodedata"}
    bad = {}
    for name in SCRIPTS + ["zh_tones.py"]:
        with open(os.path.join(CHECKS, name), encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        mods = {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        mods |= {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        extra = sorted(mods - stdlib - {"zh_tones"})
        if extra:
            bad[name] = extra
    return not bad, "non-stdlib imports: %s" % bad


case("ship: the checks import only the standard library and zh_tones", stdlib_only)


def documented():
    missing = []
    for name in SCRIPTS:
        with open(os.path.join(CHECKS, name), encoding="utf-8") as fh:
            doc = ast.get_docstring(ast.parse(fh.read())) or ""
        if "python %s" % name not in doc or "Exit" not in doc:
            missing.append(name)
    return not missing, "no usage line or exit statuses in the docstring of %s" % missing


case("ship: every check's docstring gives its usage and exit statuses", documented)


def localized_build_has_checks():
    import install
    tmp = tempfile.mkdtemp(prefix="gravitas-test-checks-")
    try:
        dest = os.path.join(tmp, "gravitas")
        with open(os.path.join(REPO, "locales", "ko", "rules", "AGENTS.md"), encoding="utf-8", newline="") as fh:
            rule, _ = install.second_opinion(fh.read(), False, "ko rule")
        install.build(dest, "ko", rule, False)
        checks = os.path.join(dest, "skills", "gravitas", "scripts", "checks")
        have = sorted(os.listdir(checks)) if os.path.isdir(checks) else []
        r = subprocess.run([sys.executable, os.path.join(checks, "pingze_check.py"), CHUSAI],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ok = (all(n in have for n in SCRIPTS + ["zh_tones.py", "data"]) and r.returncode == 0
              and os.path.isfile(os.path.join(checks, "data", "pingshui.tsv"))
              and os.path.isfile(os.path.join(dest, "skills", "gravitas", "references", "14-checks.md")))
        return ok, "checks folder: %s; run: %s" % (have, r.stdout.decode("utf-8", "replace")[:200])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


case("ship: a Korean build carries the checks, their data and 14-checks.md, and pingze_check runs there",
     localized_build_has_checks)


def check_skills_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "check_skills_for_checks", os.path.join(REPO, "plugin", "skills", "gravitas", "scripts", "check_skills.py"))
    cs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cs)
    return cs


def check_skills_accepts():
    cs = check_skills_module()
    skill = os.path.join(REPO, "plugin", "skills", "gravitas")
    rep = cs.Report(strict=True)
    cs.check_skill(skill, rep, "plugin/skills/gravitas")
    for lang in ("zh-CN", "ja", "ko"):
        cs.check_skill(os.path.join(REPO, "locales", lang, "skills", "gravitas"), rep,
                       "locales/%s/skills/gravitas" % lang, fallback=skill)
    return not rep.problems, "problems: %s" % rep.problems


case("check_skills: the plugin and every locale, with 14-checks.md and scripts/checks/, report no problem",
     check_skills_accepts)


def check_skills_sees_new_paths():
    cs = check_skills_module()
    tmp = tempfile.mkdtemp(prefix="gravitas-test-checks-")
    try:
        skill = os.path.join(tmp, "gravitas")
        shutil.copytree(os.path.join(REPO, "plugin", "skills", "gravitas"), skill,
                        ignore=shutil.ignore_patterns("__pycache__"))
        module = os.path.join(skill, "references", "14-checks.md")
        lf = chr(10)
        with open(module, "a", encoding="utf-8", newline=lf) as fh:
            fh.write(lf + "Run `scripts/checks/missing_check.py` too." + lf + ("x" + lf) * 40)
        rep = cs.Report(strict=True)
        cs.check_skill(skill, rep, "copy")
        msgs = [m for _, m in rep.problems]
        ok = (any("scripts/checks/missing_check.py" in m for m in msgs)
              and any("14-checks.md is" in m and "lines" in m for m in msgs))
        return ok, "problems: %s" % msgs
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


case("check_skills: a dead scripts/checks/ path and a 14-checks.md over 100 lines are both reported",
     check_skills_sees_new_paths)


def agents_in_sync():
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_agents_for_checks",
                                                  os.path.join(REPO, "scripts", "build_agents.py"))
    ba = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ba)
    stale = []
    for a in ba.AGENTS:
        with open(os.path.join(REPO, "plugin", "agents", a["name"] + ".md"), encoding="utf-8", newline="") as fh:
            if fh.read() != ba.render(a):
                stale.append(a["name"])
    return not stale, "regenerate with build_agents.py: %s" % stale


case("build_agents: plugin/agents/*.md still match build_agents.py output with the checks in place", agents_in_sync)

failed = RESULTS.count(False)
print("%d passed, %d failed" % (len(RESULTS) - failed, failed))
sys.exit(1 if failed else 0)
