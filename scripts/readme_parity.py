#!/usr/bin/env python3
"""Check that every README gives the same facts, each in its own language.

    python scripts/readme_parity.py

The zh-CN, ja and ko READMEs are written for their own readers, not translated
line by line, so their headings, order, examples and wording may all differ
from the English README. What may not differ are the facts a reader acts on.
For each pair, README.<lang>.md against README.md and locales/<lang>/README.md
against plugin/README.md, this checks:

1. Installer file names: the same set of "Install Gravitas (Windows).cmd",
   "Install Gravitas (Mac).command", "Install Gravitas (Linux).sh", Gravitas.zip,
   install.py, install.sh and
   install.ps1, wherever they appear.
2. Code-block commands: the same set of command lines in fenced blocks tagged
   bash, sh, shell, zsh, console, powershell, pwsh, ps1, cmd or bat. Comments,
   prompts and spacing are dropped, and every <placeholder> counts as the same,
   since comments and placeholder names are written in the reader's language.
   In a console block only the lines after a prompt are commands.
3. Headline numbers: the same set of win shares and vote counts. A win share is
   a two-digit decimal from 0.00 to 0.99 anywhere outside code blocks and HTML
   comments, so intervals count too. A vote count is a whole number in the
   votes column of a table (a header that says votes, 票 or 표), or a number
   of 10 or more written as a vote count ("120 votes", "0.52 over 120",
   "120票", "120표") on a line that also holds a win share. Each README's own
   examples carry their own vote counts on lines without a win share, and
   those are not headline numbers. Smaller counts in running text are left
   out too, because English writes them as words ("two votes short") where
   Chinese, Japanese and Korean write digits ("あと 2 票").

And for every README, English included:

4. Every relative link resolves, with the spelling GitHub needs, case and all:
   a file or folder that exists, and a #fragment that matches a heading's
   GitHub id or an explicit id in the target. A README inside the plugin is
   read as installed, so its links resolve in the plugin folder: first the
   locale's own files, then plugin/, and never outside it.
5. The language-switch line: one line naming English, 简体中文, 日本語 and
   한국어, with the file's own language in bold and the other three linked to
   their README. Inside the plugin there is only one README, so those links
   must be full URLs.

Prints OK or FAIL for each file, with the problems under it. Exits 1 when any
file fails. --root DIR checks another checkout, as the tests do.
"""
import io
import os
import re
import sys
import unicodedata
from urllib.parse import unquote

LANGS = ("zh-CN", "ja", "ko")
LABELS = {"en": "English", "zh-CN": "简体中文", "ja": "日本語", "ko": "한국어"}
ROOT_README = {"en": "README.md", "zh-CN": "README.zh-CN.md", "ja": "README.ja.md", "ko": "README.ko.md"}

FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})([^\n]*)\n(.*?)^[ \t]*\1[ \t]*$", re.S | re.M)
COMMENT = re.compile(r"<!--.*?-->", re.S)
INLINE_CODE = re.compile(r"`[^`\n]+`")
INSTALLER = re.compile(r"Install Gravitas \((?:Windows|Mac|Linux)\)\.(?:cmd|command|sh)|Gravitas\.zip|\binstall\.(?:py|sh|ps1)\b")
SHELLS = {"bash", "sh", "shell", "zsh", "console", "shell-session", "powershell", "pwsh", "ps1", "ps",
          "cmd", "bat", "batch"}
PROMPTED = {"console", "shell-session"}
PROMPT = re.compile(r"^(?:\$|>|%|PS[^>\n]*>)\s+")
SHARE = re.compile(r"(?<![\d.,])0\.\d{2}(?!\d)")
VOTES = re.compile(r"(\d[\d,]*)\s*(?:votes?\b|票|표(?![준본시현기]))", re.I)
OVER = re.compile(r"(?<![\d.,])0\.\d{2}\)?\s+over\s+(\d{1,3}(?:,\d{3})+|\d+)(?!\d|\.\d)")
MIN_PROSE_VOTES = 10
VOTE_HEADER = re.compile(r"(?i)\bvotes?\b|票|투표|^\s*표\s*(?:수)?\s*$")
INTEGER = re.compile(r"(?<![\d.])\d{1,3}(?:,\d{3})+(?!\d|\.\d)|(?<![\d.,])\d+(?!\d|\.\d)")
LINK = re.compile(r"\]\(\s*(<[^>\n]*>|(?:[^()\s]|\([^()\s]*\))+)")
HTML_LINK = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
REF_DEF = re.compile(r"^[ \t]{0,3}\[(?!\^)[^\]\n]+\]:\s*(\S+)", re.M)
HEADING = re.compile(r"^[ \t]{0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$", re.M)
EXPLICIT_ID = re.compile(r"""<[^>]*\b(?:id|name)\s*=\s*["']([^"']+)["']""", re.I)
SCHEME = re.compile(r"^(?:[A-Za-z][A-Za-z0-9+.-]*:|//)")


def read(path):
    with io.open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def prose(text):
    """The text without fenced code blocks or HTML comments."""
    return FENCE.sub("", COMMENT.sub("", text))


# ---------------------------------------------------------------- facts

def installers(text):
    return set(INSTALLER.findall(unquote(COMMENT.sub("", text))))


def commands(text):
    out = set()
    for m in FENCE.finditer(COMMENT.sub("", text)):
        info = m.group(2).strip().split()
        lang = info[0].lower().strip("{}.") if info else ""
        if lang not in SHELLS:
            continue
        for line in m.group(3).splitlines():
            line = line.strip()
            if lang in PROMPTED:
                if not PROMPT.match(line):
                    continue
            if not line or line.startswith(("#", "::")) or re.match(r"(?i)rem(\s|$)", line):
                continue
            line = PROMPT.sub("", line)
            line = re.sub(r"\s+#.*$", "", line)
            line = re.sub(r"<[^<>\n]+>", "<>", line)
            line = " ".join(line.split())
            if line:
                out.add(line)
    return out


def integers(s):
    return [n.replace(",", "") for n in INTEGER.findall(s)]


def cells(row):
    row = row.strip().replace("\\|", "\0")
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [c.replace("\0", "|").strip() for c in row.split("|")]


def headline_numbers(text):
    """{('share', '0.57'), ('votes', '120'), ...}; see the module docstring for what counts."""
    lines = prose(text).splitlines()
    out = set()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            header = cells(line)
            vote_cols = [k for k, c in enumerate(header) if VOTE_HEADER.search(c)]
            out.update(("share", s) for s in SHARE.findall(line))
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                row = cells(lines[i])
                for k in vote_cols:
                    if k < len(row):
                        out.update(("votes", n) for n in integers(SHARE.sub(" ", row[k])))
                out.update(row_numbers(lines[i]))
                i += 1
            continue
        out.update(row_numbers(line))
        i += 1
    return out


def row_numbers(line):
    shares = SHARE.findall(line)
    out = {("share", s) for s in shares}
    if shares:
        for n in VOTES.findall(line) + OVER.findall(line):
            n = n.strip(",").replace(",", "")
            if n and int(n) >= MIN_PROSE_VOTES:
                out.add(("votes", n))
    return out


def fmt(items):
    """Names and commands as they are; numbers as "share 0.57" or "votes 120", in order."""
    def key(x):
        return (x[0], float(x[1]), "") if isinstance(x, tuple) else ("", 0.0, x)
    return "; ".join("%s %s" % x if isinstance(x, tuple) else x for x in sorted(items, key=key))


def compare_facts(en_text, tr_text):
    problems = []
    for name, get in (("installer file names", installers), ("code-block commands", commands),
                      ("headline numbers", headline_numbers)):
        a, b = get(en_text), get(tr_text)
        missing, extra = a - b, b - a
        if missing:
            problems.append("%s in the English README but not here: %s" % (name, fmt(missing)))
        if extra:
            problems.append("%s here but not in the English README: %s" % (name, fmt(extra)))
    return problems


# ---------------------------------------------------------------- links

def slug(heading):
    """The id GitHub gives a heading: lower case, punctuation and symbols removed, spaces to hyphens."""
    t = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t).strip().lower()
    kept = []
    for c in t:
        cat = unicodedata.category(c)
        if c in "- " or cat[0] in "LMN" or cat == "Pc":
            kept.append(c)
    return "".join(kept).replace(" ", "-")


def anchors(text):
    text = prose(text)
    found, seen = set(EXPLICIT_ID.findall(text)), {}
    for m in HEADING.finditer(text):
        base = slug(m.group(2))
        n = seen.get(base, 0)
        seen[base] = n + 1
        found.add(base if n == 0 else "%s-%d" % (base, n))
    return found


def exists_exact(base, rel):
    """True when rel names a file or folder under base, spelled exactly as on disk."""
    cur = base
    for part in rel.replace("\\", "/").split("/"):
        if part in ("", "."):
            continue
        try:
            names = os.listdir(cur)
        except OSError:
            return False
        if part not in names:
            return False
        cur = os.path.join(cur, part)
    return True


def link_targets(text):
    text = INLINE_CODE.sub("", prose(text))
    out = [m.group(1) for m in LINK.finditer(text)]
    out += HTML_LINK.findall(text) + REF_DEF.findall(text)
    return [t[1:-1] if t.startswith("<") and t.endswith(">") else t for t in out]


def link_problems(text, bases, in_plugin):
    """bases: folders a relative link may resolve in, first match wins; the file sits at the top of each."""
    problems = []
    own = anchors(text)
    for target in link_targets(text):
        if SCHEME.match(target):
            continue
        where, _, frag = target.partition("#")
        where = unquote(where.split("?")[0])
        if not where:
            if frag and unquote(frag) not in own:
                problems.append("link %s: no heading or id %r in this file" % (target, unquote(frag)))
            continue
        hit = None
        for base in bases:
            full = os.path.normpath(os.path.join(base, where.lstrip("/") if where.startswith("/") else where))
            rel = os.path.relpath(full, base)
            if rel == ".." or rel.startswith(".." + os.sep):
                continue
            if exists_exact(base, rel):
                hit = full
                break
        if hit is None:
            problems.append("link %s: %s does not exist%s"
                            % (target, where, " in the plugin as installed" if in_plugin else ""))
            continue
        if frag and hit.lower().endswith(".md") and os.path.isfile(hit):
            if unquote(frag) not in anchors(read(hit)):
                problems.append("link %s: no heading or id %r in %s" % (target, unquote(frag), where))
    return problems


# ---------------------------------------------------------------- language switch

def switch_problems(text, lang, in_plugin):
    labels = list(LABELS.values())
    for line in prose(text).splitlines():
        if not all(l in line for l in labels) or line.count("](") < 2:
            continue
        problems = []
        own = LABELS[lang]
        if not any(f % own in line for f in ("**%s**", "<b>%s</b>", "<strong>%s</strong>")):
            problems.append("language switch: %s, this file's language, is not in bold" % own)
        for other, label in LABELS.items():
            if other == lang:
                continue
            m = re.search(r"\[%s\]\(([^)\s]+)\)" % re.escape(label), line)
            if not m:
                problems.append("language switch: %s is not linked" % label)
                continue
            target, want = m.group(1).split("#")[0], ROOT_README[other]
            if in_plugin and not re.match(r"^https?://", target):
                problems.append("language switch: %s links %s; inside the plugin it needs the full URL of %s"
                                % (label, target, want))
            elif not (target in (want, "./" + want) or target.endswith("/" + want)):
                problems.append("language switch: %s links %s, not %s" % (label, target, want))
        return problems
    return ["no language-switch line naming %s, with the others linked" % ", ".join(labels)]


# ---------------------------------------------------------------- run

def check_file(root, rel, lang, in_plugin, en_rel=None):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return ["missing"]
    text = read(path)
    problems = []
    if en_rel:
        en_path = os.path.join(root, en_rel)
        if os.path.isfile(en_path):
            problems += compare_facts(read(en_path), text)
        else:
            problems.append("%s is missing, so there is nothing to compare with" % en_rel)
    if in_plugin:
        bases = [os.path.dirname(path)] + ([os.path.join(root, "plugin")] if lang != "en" else [])
    else:
        bases = [root]
    problems += link_problems(text, bases, in_plugin)
    problems += switch_problems(text, lang, in_plugin)
    return problems


def main(argv):
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if argv[:1] == ["--root"] and len(argv) == 2:
        root = os.path.abspath(argv[1])
    elif argv:
        sys.exit("usage: readme_parity.py [--root DIR]")
    plan = [("README.md", "en", False, None), (os.path.join("plugin", "README.md"), "en", True, None)]
    for lang in LANGS:
        plan.append((ROOT_README[lang], lang, False, "README.md"))
        plan.append((os.path.join("locales", lang, "README.md"), lang, True, os.path.join("plugin", "README.md")))
    bad = 0
    for rel, lang, in_plugin, en_rel in plan:
        problems = check_file(root, rel, lang, in_plugin, en_rel)
        print("%-24s %s" % (rel.replace(os.sep, "/"), "FAIL" if problems else "OK"))
        for p in problems:
            print("    " + p)
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
