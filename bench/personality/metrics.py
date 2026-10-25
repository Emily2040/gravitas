#!/usr/bin/env python3
"""Communication characteristics measured from an answer's text, after AA-PersonalityBench.

AA's 21 characteristics (length 5, structure 3, punctuation 8, emphasis 5), counted the
way its methodology page describes, with CJK handling for the Chinese, Japanese and Korean
answers this benchmark adds:

- words: tokens containing a letter or digit; every Han, kana or Hangul character counts
  as one word (AA's rule). For Korean, `native_words` also counts space-separated words.
- characters: prose characters after removing code and URLs.
- sentences: a rule-based splitter that knows common abbreviations and the CJK enders.
- paragraphs: prose paragraphs only (no headings, code, list items or tables).

Extra, not in AA: hedge markers per 1000 characters (the round-one and extended lists from
docs/dsh-ab/WIN_CRITERIA.md), stock slop phrases per language, and the share of list lines
that open with a bold lead.

Usage: metrics.py FILE...   prints one JSON object per file.
       metrics.py --self-test
"""
import json
import re
import sys
import unicodedata

CJK_CHAR = re.compile(r"[぀-ヿㇰ-ㇿ㐀-䶿一-鿿豈-﫿가-힯ᄀ-ᇿ㄰-㆏]")
HAN = re.compile(r"[㐀-䶿一-鿿豈-﫿]")
KANA = re.compile(r"[぀-ヿㇰ-ㇿ]")
HANGUL = re.compile(r"[가-힯ᄀ-ᇿ㄰-㆏]")
LATIN_WORD = re.compile(r"[^\s　-〿＀-￯]*[A-Za-z0-9À-ɏ][^\s　-〿＀-￯]*")
CODE_FENCE = re.compile(r"```.*?(?:```|\Z)", re.S)
INLINE_CODE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"https?://\S+|www\.\S+")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+\S")
LIST_ITEM = re.compile(r"^(\s*)(?:[-*+•・]|\d+[.)、]|[a-zA-Z][.)]|[①-⑳]|[０-９]+[．.、])\s+\S")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
BOLD = re.compile(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1", re.S)
ITALIC = re.compile(r"(?<![*_\w])([*_])(?=[^\s*_])([^*_\n]+?)(?<=[^\s*_])\1(?![*_\w])")
ACRONYM = re.compile(r"\b(?:[A-Z]\.){2,}|\b[A-Z][A-Z0-9]*[A-Z][A-Z0-9]*\b")
CONTRACTION = re.compile(r"\b[A-Za-z]+(?:'|’)(?:t|re|ve|ll|d|m|s)\b", re.I)
POSSESSIVE_HINT = re.compile(r"\b(?:it|he|she|that|there|what|who|where|here|how|let)(?:'|’)s\b", re.I)
ABBREV = {"mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "vs", "etc", "e.g", "i.e", "u.s", "u.k", "no", "fig", "inc", "ltd", "co", "approx", "dept", "est", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec", "a.m", "p.m"}

# Hedge lists from docs/dsh-ab/WIN_CRITERIA.md (round one, extended round three, and the
# Japanese and Korean amendment of 2026-10-23), counted per 1000 characters.
HEDGES = {
    "zh": {"first": ["可能", "也许", "或许", "大概", "建议咨询", "以官方为准", "请以", "具体以"],
           "extended": ["一般来说", "通常", "因地而异", "视情况", "具体情况", "仅供参考", "建议您", "咨询当地"]},
    "en": {"first": ["may ", "might ", "could ", "possibly", "perhaps", "check with", "consult", "verify with"],
           "extended": ["generally", "typically", "usually", "depending on", "it depends", "varies", "in most cases", "contact your"]},
    "ja": {"first": ["かもしれ", "おそらく", "恐らく", "たぶん", "可能性があ", "と思われ", "断言できませ", "ご確認ください", "確認してください"],
           "extended": ["一般的に", "通常は", "場合によ", "地域によ", "自治体によ", "お問い合わせ", "問い合わせて", "相談してください", "目安"]},
    "ko": {"first": ["아마", "일지도", "할지도", "가능성이 있", "확실하지", "확인해 보세요", "확인하시기 바랍니다"],
           "extended": ["일반적으로", "보통은", "경우에 따라", "지역마다", "다를 수 있", "문의하", "상담하"]},
}

# Stock slop phrases: openers, closers and filler a reader recognises as generic. Counted as
# occurrences; reported only, never a gate on its own (a list is gamed by synonyms).
SLOP_PHRASES = {
    "en": ["great question", "good question", "excellent question", "i hope this helps", "hope this helps", "feel free to",
           "let me know if", "happy to help", "in conclusion", "in summary", "to sum up", "it's important to note",
           "it is important to note", "it's worth noting", "it is worth noting", "delve", "tapestry", "navigate the",
           "in today's", "ever-evolving", "game-changer", "unlock", "embark", "a testament to", "plays a crucial role",
           "certainly!", "absolutely!", "of course!", "i'd be happy to", "rest assured"],
    "zh": ["好问题", "这是一个很好的问题", "希望对你有帮助", "希望对您有帮助", "希望这些", "如果你还有", "如果您还有", "欢迎随时",
           "总而言之", "综上所述", "总的来说", "值得注意的是", "需要注意的是", "不可或缺", "至关重要", "赋能", "助力",
           "全方位", "深入探讨", "让我们", "当然可以", "非常好的问题"],
    "ja": ["良い質問", "いい質問", "素晴らしい質問", "お役に立てれば", "参考になれば", "お気軽に", "いかがでしたか",
           "まとめると", "結論として", "総じて", "重要なのは", "注目すべき", "ぜひ", "もちろんです", "喜んで"],
    "ko": ["좋은 질문", "훌륭한 질문", "도움이 되셨길", "도움이 되길", "도움이 되었으면", "언제든지", "편하게 물어",
           "결론적으로", "요약하자면", "종합하면", "중요한 점은", "주목할 만한", "물론입니다", "기꺼이"],
}

EMOJI_RANGES = [(0x1F300, 0x1FAFF), (0x2600, 0x27BF), (0x1F000, 0x1F2FF), (0x1F900, 0x1F9FF), (0x2B00, 0x2BFF), (0x2300, 0x23FF)]
JOINERS = {0x200D, 0xFE0F, 0xFE0E} | set(range(0x1F3FB, 0x1F400)) | set(range(0xE0020, 0xE0080))


def detect_lang(text):
    """zh, ja, ko or en, from the script of the letters (kana means Japanese)."""
    han, kana, hangul = len(HAN.findall(text)), len(KANA.findall(text)), len(HANGUL.findall(text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if hangul > 0.2 * (han + kana + hangul + latin) and hangul >= 5:
        return "ko"
    if kana >= 5 and kana > 0.05 * (han + kana):
        return "ja"
    if han >= 5 and han > 0.3 * latin:
        return "zh"
    return "en"


def is_emoji(cp):
    return any(a <= cp <= b for a, b in EMOJI_RANGES)


def count_emojis(text):
    """Each emoji as a reader sees it: a ZWJ sequence, a flag pair or a modified emoji counts once."""
    n, i, chars = 0, 0, [ord(c) for c in text]
    while i < len(chars):
        cp = chars[i]
        if 0x1F1E6 <= cp <= 0x1F1FF:  # regional indicators pair into one flag
            n += 1
            i += 2 if i + 1 < len(chars) and 0x1F1E6 <= chars[i + 1] <= 0x1F1FF else 1
            continue
        if is_emoji(cp):
            n += 1
            i += 1
            while i < len(chars) and (chars[i] in JOINERS or (chars[i - 1] == 0x200D and is_emoji(chars[i]))):
                i += 1
            continue
        i += 1
    return n


def strip_code(text):
    return INLINE_CODE.sub(" ", CODE_FENCE.sub("\n", text))


def prose_text(text):
    """Text with code, URLs and markdown markers removed, for character and word counts."""
    t = URL.sub(" ", strip_code(text))
    t = re.sub(r"^\s{0,3}#{1,6}\s+", "", t, flags=re.M)
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)
    t = re.sub(r"^(\s*)(?:[-*+•・]|\d+[.)、]|[a-zA-Z][.)]|[①-⑳]|[０-９]+[．.、])\s+", r"\1", t, flags=re.M)
    t = re.sub(r"(\*\*|__|\*|_|~~)", "", t)
    t = re.sub(r"^\s*\|?\s*:?-{3,}.*$", "", t, flags=re.M)
    t = t.replace("|", " ")
    return t


def count_words(t):
    cjk = len(CJK_CHAR.findall(t))
    rest = CJK_CHAR.sub(" ", t)
    return cjk + len(LATIN_WORD.findall(rest))


def sentences(t):
    """Rule-based split: . ! ? and the CJK enders, skipping common abbreviations and decimals."""
    out, cur = [], ""
    i = 0
    while i < len(t):
        ch = t[i]
        cur += ch
        if ch in "。！？!?\n":
            if cur.strip():
                out.append(cur)
            cur = ""
        elif ch == ".":
            prev = re.search(r"([A-Za-z.]+)\.$", cur)
            nxt = t[i + 1] if i + 1 < len(t) else " "
            if prev and prev.group(1).lower() in ABBREV:
                pass
            elif nxt.isdigit() or (prev and len(prev.group(1)) == 1 and prev.group(1).isupper()):
                pass
            elif nxt in " \n\t\"')]”’" or i + 1 == len(t):
                if cur.strip():
                    out.append(cur)
                cur = ""
        i += 1
    if cur.strip():
        out.append(cur)
    return [s for s in out if count_words(s) > 0]


def blocks(text):
    """Classify lines of the code-stripped text into headings, list items, tables, prose."""
    lines = strip_code(text).split("\n")
    kinds = []
    for idx, ln in enumerate(lines):
        if not ln.strip():
            kinds.append("blank")
        elif HEADING.match(ln):
            kinds.append("heading")
        elif TABLE_SEP.match(ln) or (ln.strip().startswith("|") and ln.strip().endswith("|")):
            kinds.append("table")
        elif LIST_ITEM.match(ln):
            kinds.append("list0" if len(LIST_ITEM.match(ln).group(1).replace("\t", "    ")) < 2 else "listN")
        else:
            kinds.append("prose")
    return lines, kinds


def measure(text, lang=None):
    lang = lang or detect_lang(text)
    prose = prose_text(text)
    chars = len(re.sub(r"\s+", " ", prose).strip())
    words = count_words(prose)
    # Sentences count prose and list-item text; headings are labels, not sentences.
    sents = sentences(prose_text(re.sub(r"^\s{0,3}#{1,6}\s+.*$", "", strip_code(text), flags=re.M)))
    lines, kinds = blocks(text)

    # Lists: a top-level list is a run of top-level items, with nested items, blank lines and
    # indented continuation lines allowed inside it; a prose line or heading ends it.
    lists, in_list = 0, False
    for ln, k in zip(lines, kinds):
        if k == "list0":
            if not in_list:
                lists += 1
            in_list = True
        elif k in ("listN", "blank"):
            continue
        elif k == "prose" and in_list and ln.startswith(("  ", "\t")):
            continue
        else:
            in_list = False
    list_items = sum(1 for k in kinds if k in ("list0", "listN"))
    headings = sum(1 for k in kinds if k == "heading")
    tables = sum(1 for i, ln in enumerate(lines) if TABLE_SEP.match(ln) and i > 0 and "|" in lines[i - 1])

    # Paragraphs: runs of prose lines separated by blank lines or other blocks.
    paragraphs, in_para = 0, False
    for k in kinds:
        if k == "prose":
            if not in_para:
                paragraphs += 1
            in_para = True
        else:
            in_para = False

    stripped = strip_code(text)
    bold = len(BOLD.findall(stripped))
    italic = len(ITALIC.findall(BOLD.sub(" ", stripped)))
    bold_lead = sum(1 for ln, k in zip(lines, kinds) if k in ("list0", "listN") and re.match(r"^\s*(?:\S+)\s+(\*\*|__)", ln))

    # Parentheses: closed pairs, nested included, unmatched excluded (ASCII and fullwidth).
    parens, stack = 0, []
    for ch in prose:
        if ch in "(（":
            stack.append(ch)
        elif ch in ")）" and stack:
            stack.pop()
            parens += 1
    quote_marks = len(re.findall(r"[\"“”«»「」『』‘]|(?<!\w)’|’(?!\w)|(?<!\w)'(?=\w)|(?<=[\w.,!?])'(?!\w)", prose))
    em_dashes = prose.count("—")
    ellipses = len(re.findall(r"\.\.\.|…+", prose))
    contractions = len(CONTRACTION.findall(prose)) if lang == "en" else 0

    low = prose.lower()
    hedge = {}
    for which in ("first", "extended"):
        n = sum(low.count(h) for h in HEDGES.get(lang, HEDGES["en"])[which])
        hedge[which] = round(1000.0 * n / chars, 3) if chars else 0.0
    slop_hits = sum(low.count(p) for p in SLOP_PHRASES.get(lang, SLOP_PHRASES["en"]))
    native_words = len(prose.split()) if lang == "ko" else words
    final = text.rstrip()
    return {
        "lang": lang,
        "characters": chars,
        "words": words,
        "native_words": native_words,
        "sentences": len(sents),
        "paragraphs": paragraphs,
        "avg_sentence_words": round(words / len(sents), 2) if sents else 0.0,
        "headings": headings,
        "lists": lists,
        "list_items": list_items,
        "tables": tables,
        "colons": prose.count(":") + prose.count("："),
        "contractions": contractions,
        "exclamations": prose.count("!") + prose.count("！"),
        "questions": prose.count("?") + prose.count("？"),
        "parentheses": parens,
        "em_dashes": em_dashes,
        "quotes": quote_marks // 2,
        "ellipses": ellipses,
        "bold": bold,
        "italics": italic,
        "emojis": count_emojis(text),
        "acronyms": len(ACRONYM.findall(prose)),
        "ends_with_question": 1 if final.endswith(("?", "？")) else 0,
        "bold_lead_items": bold_lead,
        "hedges_first_per_1k": hedge["first"],
        "hedges_extended_per_1k": hedge["extended"],
        "slop_phrases": slop_hits,
    }


AA_METRICS = ["characters", "words", "sentences", "paragraphs", "avg_sentence_words", "headings", "lists", "tables",
              "colons", "contractions", "exclamations", "questions", "parentheses", "em_dashes", "quotes", "ellipses",
              "bold", "italics", "emojis", "acronyms", "ends_with_question"]


def self_test():
    assert len(AA_METRICS) == 21
    en = ("## Answer\n\nGreat question! The **short** answer is yes. Dr. Smith said it's 3.5 times faster (see below).\n\n"
          "- **First** point: one\n- Second point\n  - nested\n\nIn conclusion, I hope this helps... Do you agree?")
    m = measure(en)
    assert m["lang"] == "en", m
    assert m["headings"] == 1 and m["lists"] == 1 and m["list_items"] == 3, m
    assert m["bold"] == 2 and m["bold_lead_items"] == 1, m
    assert m["parentheses"] == 1 and m["ellipses"] == 1 and m["ends_with_question"] == 1, m
    assert m["contractions"] == 1 and m["colons"] == 1, m
    assert m["slop_phrases"] >= 3, m
    assert m["sentences"] == 8, (m["sentences"], sentences(prose_text(en)))
    zh = "北京是中国的首都。人口约2189万（2020年）。\n\n1. 第一点\n2. 第二点\n\n希望对你有帮助！"
    z = measure(zh)
    assert z["lang"] == "zh" and z["lists"] == 1 and z["list_items"] == 2 and z["parentheses"] == 1, z
    assert z["words"] == len(CJK_CHAR.findall(zh)) + 2, z  # 2189 and 2020 count as words
    assert z["slop_phrases"] == 1 and z["exclamations"] == 1, z
    assert measure("東京は日本の首都です。おそらく。")["lang"] == "ja"
    k = measure("서울은 한국의 수도입니다. 아마 맞을 겁니다.")
    assert k["lang"] == "ko" and k["native_words"] == 6 and k["words"] == len(HANGUL.findall("서울은한국의수도입니다아마맞을겁니다")), k
    assert count_emojis("hi \U0001F44D\U0001F3FD and \U0001F468‍\U0001F469‍\U0001F467 \U0001F1EF\U0001F1F5 ❤️") == 4
    assert measure("x = 1\n```py\nprint('a: b')\n```\n")["colons"] == 0
    t = measure("| a | b |\n|---|---|\n| 1 | 2 |\n")
    assert t["tables"] == 1 and t["paragraphs"] == 0, t
    cleaned = prose_text(en + "\n" + zh)
    assert not any(ord(c) < 32 and c not in "\n\t" for c in cleaned), "control character left in prose text"
    assert "  - nested" not in cleaned and "nested" in cleaned, "list markers must go, item text must stay"
    e = measure("")
    assert e["words"] == 0 and e["characters"] == 0 and e["sentences"] == 0
    print("metrics self-test: ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        sys.exit(0)
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            print(json.dumps({"file": path, **measure(f.read())}, ensure_ascii=False))
