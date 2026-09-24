#!/usr/bin/env python3
"""Check that each translated README keeps the English README's structure.

    python scripts/readme_parity.py

Compares README.md with README.<lang>.md, and plugin/README.md with
locales/<lang>/README.md: heading levels, table shapes, HTML anchors, code
blocks, link targets and the numbers in table rows. A translation may change
every word and none of these. Exits 1 when any pair differs.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("zh-CN", "ja", "ko")


def shape(text):
    lines = text.splitlines()
    fences = re.findall(r"^```[^\n]*\n.*?^```", text, re.S | re.M)
    tables, cur = [], None
    for l in lines:
        if l.startswith("|"):
            cells = len(l.strip().strip("|").split("|"))
            if cur is None:
                cur = [cells, 0]
                tables.append(cur)
            cur[1] += 1
        else:
            cur = None
    return {
        "heading levels": [len(m) for m in re.findall(r"^(#{1,6}) ", text, re.M)],
        "anchors": re.findall(r'<a id="([^"]+)"></a>', text),
        "code blocks": [f.strip() for f in fences],
        "tables (columns, rows)": [tuple(t) for t in tables],
        "link targets": sorted(re.findall(r"\]\(([^)\s]+)\)", text)),
        "numbers in table rows": sorted(n.rstrip(",.") for n in re.findall(r"\d[\d,.]*", " ".join(l for l in lines if l.startswith("|")))),
    }


def compare(en_path, tr_path):
    if not os.path.exists(tr_path):
        return ["missing"]
    en = shape(io.open(en_path, encoding="utf-8").read())
    tr = shape(io.open(tr_path, encoding="utf-8").read())
    problems = []
    for key in en:
        a, b = en[key], tr[key]
        if key == "link targets":
            # the language switcher links differ by design: each file links the other three
            a = [x for x in a if not re.match(r"^(\./)?README(\.[\w-]+)?\.md$", x) and "/README." not in x]
            b = [x for x in b if not re.match(r"^(\./)?README(\.[\w-]+)?\.md$", x) and "/README." not in x]
        if key == "numbers in table rows":
            # every English number must survive; a translation may write "one" as 1
            left = list(b)
            missing = [n for n in a if not (n in left and not left.remove(n))]
            if missing:
                problems.append("numbers in table rows missing from the translation: %s" % missing[:8])
            continue
        if a != b:
            if isinstance(a, list) and len(a) == len(b):
                diffs = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y][:3]
                problems.append("%s differ at %s" % (key, diffs))
            else:
                missing = [x for x in a if x not in b][:5]
                extra = [x for x in b if x not in a][:5]
                problems.append("%s: English has %d, translation %d; missing %s; extra %s"
                                % (key, len(a), len(b), missing, extra))
    return problems


def main():
    bad = 0
    for lang in LANGS:
        pairs = [(os.path.join(ROOT, "README.md"), os.path.join(ROOT, "README.%s.md" % lang)),
                 (os.path.join(ROOT, "plugin", "README.md"), os.path.join(ROOT, "locales", lang, "README.md"))]
        for en, tr in pairs:
            problems = compare(en, tr)
            name = os.path.relpath(tr, ROOT)
            print("%-28s %s" % (name, "OK" if not problems else "DIFFERS"))
            for p in problems:
                print("    " + p)
            bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
