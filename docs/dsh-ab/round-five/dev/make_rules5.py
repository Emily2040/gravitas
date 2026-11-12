#!/usr/bin/env python3
"""Write round five's change-5 rule files, overlays and expected-rule-hashes.json (standard library only).

    python dev/make_rules5.py           write rules/change5/<lang>.md, overlays/{base,c5}-<lang>.yml and
                                        expected-rule-hashes.json in the round-five folder
    python dev/make_rules5.py --check   write nothing; exit 1 if any written file differs from what it would write

The change-5 text of each language is read from design/change5.md (section "## Text", one paragraph per "### <lang>").
It is inserted into a copy of W:\\Projects\\gravitas-round5\\dist\\<lang>\\gravitas\\rules\\AGENTS.md between the two
sentences change5.md names, with the language's own sentence spacing (one space in en and ko, none in zh-CN and ja,
as round four's change-4 files did). Nothing else in the rule changes, which the script checks by removing the
inserted text again and comparing with the original bytes. The hashes are computed with validity5.py's own
rule_text() (rule text plus the DSH platform note, exactly as dsh/index.js ruleText joins them), and c5Sentence is
the first 40 characters of the inserted text.
"""
import hashlib
import json
import os
import re
import sys

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, B)
sys.dont_write_bytecode = True
import validity5 as v  # noqa: E402

# (text before the insertion point, separator, text after it), from change5.md's "Where" section
ANCHORS = {
    "en": ("checked or widened to what they can confirm.", " ", "Evidence counts only if independent"),
    "zh-CN": ("要么把说法放宽到用户自己能去确认的程度。", "", "证据只有同时做到两点才算数"),
    "ja": ("相手が確かめられる程度まで主張の幅を広げます。", "", "根拠として数えるのは"),
    "ko": ("사용자가 확인할 수 있는 정도까지 범위를 넓혀 말합니다.", " ", "근거로 치는 것은"),
}
SHORT = {"zh-CN": "zh", "en": "en", "ja": "ja", "ko": "ko"}
OVERLAY_BASE = """# Round five, current best: rule only, check off, plugin in the request's language.
- id: dsh-gravitas
  config:
    language: {lang}
    alwaysOnRule: true
    claimCheck: false
"""
OVERLAY_C5 = """# Round five, candidate: current best plus change 5 ("plainly" keeps what was found).
- id: dsh-gravitas
  config:
    language: {lang}
    alwaysOnRule: true
    claimCheck: false
    ruleFile: W:/AgentData/logs/gravitas-dsh-ab5/rules/change5/{lang}.md
"""


def change5_texts():
    md = open(os.path.join(B, "design", "change5.md"), encoding="utf-8").read()
    sec = md.split("\n## Text\n", 1)[1].split("\n## ", 1)[0]
    out = {}
    for m in re.finditer(r"^### (\S+)\n(.+?)\n(?=\n|$)", sec, re.M | re.S):
        body = m.group(2).strip()
        if "\n" in body:
            raise SystemExit("change5.md: the %s text is not one paragraph" % m.group(1))
        out[m.group(1)] = body
    if sorted(out) != sorted(ANCHORS):
        raise SystemExit("change5.md: languages %s, expected %s" % (sorted(out), sorted(ANCHORS)))
    return out


def build():
    """{relative path: bytes} of every file this script writes."""
    files, hashes = {}, {}
    texts = change5_texts()
    for lang, (before, sep, after) in ANCHORS.items():
        src = os.path.join(v.W, "dist", lang, "gravitas", "rules", "AGENTS.md")
        raw = open(src, "rb").read()
        rule = raw.decode("utf-8")
        old = before + sep + after
        if rule.count(old) != 1:
            raise SystemExit("%s: the insertion point occurs %d times, expected 1" % (lang, rule.count(old)))
        new = rule.replace(old, before + sep + texts[lang] + sep + after)
        if new.replace(sep + texts[lang], "", 1) != rule or new.count(texts[lang]) != 1:
            raise SystemExit("%s: the new rule differs from the original by more than the inserted text" % lang)
        orig_lines, new_lines = rule.split("\n"), new.split("\n")
        changed = [i + 1 for i, (a, b) in enumerate(zip(orig_lines, new_lines)) if a != b]
        if len(orig_lines) != len(new_lines) or changed != [13] or not new_lines[12].startswith("4. "):
            raise SystemExit("%s: expected exactly line 13 (rule item 4) to change, got %s" % (lang, changed))
        files["rules/change5/%s.md" % lang] = new.encode("utf-8")
        files["overlays/base-%s.yml" % SHORT[lang]] = OVERLAY_BASE.format(lang=lang).encode("utf-8")
        files["overlays/c5-%s.yml" % SHORT[lang]] = OVERLAY_C5.format(lang=lang).encode("utf-8")
        hashes[lang] = (src, texts[lang])
    exp = {}
    for short, lang in v.LANG.items():
        src, text = hashes[lang]
        base_t = v.rule_text(lang, src)
        tmp = os.path.join(B, "dev", ".c5-%s.md" % lang)
        with open(tmp, "wb") as f:
            f.write(files["rules/change5/%s.md" % lang])
        try:
            c5_t = v.rule_text(lang, tmp)
        finally:
            os.remove(tmp)
        sh = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()
        sentence = text[:40]
        if sentence not in c5_t or sentence in base_t:
            raise SystemExit("%s: c5Sentence is not in the c5 rule only" % short)
        exp[short] = {"base": sh(base_t), "c5": sh(c5_t), "c5Sentence": sentence}
    files["expected-rule-hashes.json"] = (json.dumps(exp, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return files


def main():
    files = build()
    if "--check" in sys.argv:
        bad = [p for p, data in files.items()
               if not os.path.exists(os.path.join(B, p)) or open(os.path.join(B, p), "rb").read() != data]
        print("differ or missing: %s" % (bad or "none"))
        return 1 if bad else 0
    for p, data in files.items():
        full = os.path.join(B, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
        print("wrote %s (%d bytes)" % (p, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
