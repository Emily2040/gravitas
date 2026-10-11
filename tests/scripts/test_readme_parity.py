#!/usr/bin/env python3
"""Tests for scripts/readme_parity.py.

Run with plain `python tests/scripts/test_readme_parity.py`. Each case prints
one PASS or FAIL line; the exit status is 1 if any case fails.

The cases build a small checkout in a temporary folder: an English README and
three native READMEs that order their sections differently, use their own
headings, comments and placeholder names, and carry example vote counts of
their own, plus the plugin README and its three locale copies. That checkout
must pass. Then each case changes one fact in a fresh copy (a win share, a
vote count, an installer name, a command, a link, a heading id, the language
switch) and checks that the script fails on it and names it. The last case
runs the script on this repository to make sure real READMEs parse, without
judging their content. Nothing in the repository is written.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SCRIPT = os.path.join(REPO, "scripts", "readme_parity.py")

spec = importlib.util.spec_from_file_location("readme_parity", SCRIPT)
rp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rp)

RESULTS = []


def case(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


FENCE = "```"
GH = "https://github.com/Emily2040/gravitas/blob/main/"

EN = """# Gravitas

**English** · [简体中文](./README.zh-CN.md) · [日本語](./README.ja.md) · [한국어](./README.ko.md)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

<a id="install"></a>

## Install

Download Gravitas.zip, open it, and double-click `Install Gravitas (Windows).cmd` or `Install Gravitas (Mac).command`.

{f}bash
python scripts/install.py ja --review   # Japanese, with the Second Opinion
python scripts/install.py <lang>
{f}

## Real Examples

Both graders preferred plain Antigravity in all four runs, 8 votes out of 8. [The request and both answers](docs/examples/en/case.md)

## Results

| set | model | votes | win share | interval |
|---|---|---|---|---|
| blind | Flash | 120 | 0.57 | 0.48-0.66 |
| world | Pro | 100 | 0.71 | 0.61-0.79 |

Codex GPT-6 Sol 0.66 and Grok 4.5 0.42, graded by GPT-6 Sol only, 60 votes each. Run 2 scored 0.45 over 120, two votes short of nothing.

See [Install](#install), [Results](#results) and [the method](docs/comparison.md#method).
""".format(f=FENCE)


def native(lang, label_bold, h_results, h_install, h_examples, comment, placeholder, vote):
    labels = [("English", "./README.md"), ("简体中文", "./README.zh-CN.md"), ("日本語", "./README.ja.md"),
              ("한국어", "./README.ko.md")]
    switch = " · ".join("**%s**" % l if l == label_bold else "[%s](%s)" % (l, t) for l, t in labels)
    return """# Gravitas

{switch}

## {r}

Codex GPT-6 Sol 0.66, Grok 4.5 0.42 (GPT-6 Sol, 60{v}). 120{v}, 0.45; 2{v}.

| set | model | {v} | share | interval |
|---|---|---|---|---|
| world | Pro | 100 | 0.71 | 0.61-0.79 |
| blind | Flash | 120 | 0.57 | 0.48-0.66 |

## {i}

Gravitas.zip, `Install Gravitas (Windows).cmd`, `Install Gravitas (Mac).command`.

{f}bash
python scripts/install.py ja --review   # {c}
python scripts/install.py {p}
{f}

## {e}

64{v}, 29{v}. [x](docs/examples/{lang}/case.md)

[{i}](#{is_}) [{r}](#{rs}) [m](docs/comparison.md#method)
""".format(switch=switch, r=h_results, i=h_install, e=h_examples, c=comment, p=placeholder, v=vote, f=FENCE,
           lang=lang, is_=rp.slug(h_install), rs=rp.slug(h_results))


JA = native("ja", "日本語", "結果", "インストール", "実例", "日本語、セカンドオピニオン付き", "<言語>", " 票")
ZH = native("zh-CN", "简体中文", "结果", "安装", "真实例子", "日语，带第二意见", "<语言>", "票")
KO = native("ko", "한국어", "결과와 방법", "설치", "실제 사례", "일본어, 두 번째 의견 포함", "<언어>", "표")


def plugin_readme(bold):
    labels = [("English", "README.md"), ("简体中文", "README.zh-CN.md"), ("日本語", "README.ja.md"),
              ("한국어", "README.ko.md")]
    switch = " · ".join("**%s**" % l if l == bold else "[%s](%s%s)" % (l, GH, t) for l, t in labels)
    return """# Gravitas

{switch}

[rules](rules/AGENTS.md) · [agents](agents/) · [reviewer](agents/gravitas-reviewer.md#role)

{f}bash
python skills/gravitas/scripts/check_skills.py   # {bold}
{f}
""".format(switch=switch, f=FENCE, bold=bold)


FILES = {
    "README.md": EN,
    "README.ja.md": JA,
    "README.zh-CN.md": ZH,
    "README.ko.md": KO,
    "LICENSE": "MIT\n",
    "docs/comparison.md": "# Comparison\n\n## Method\n\nText.\n",
    "docs/examples/en/case.md": "# Case\n",
    "docs/examples/ja/case.md": "# Case\n",
    "docs/examples/zh-CN/case.md": "# Case\n",
    "docs/examples/ko/case.md": "# Case\n",
    "plugin/README.md": plugin_readme("English"),
    "plugin/rules/AGENTS.md": "# Gravitas\n",
    "plugin/agents/gravitas-reviewer.md": "# Reviewer\n\n## Role\n",
    "locales/ja/README.md": plugin_readme("日本語"),
    "locales/ja/rules/AGENTS.md": "# Gravitas\n",
    "locales/zh-CN/README.md": plugin_readme("简体中文"),
    "locales/zh-CN/rules/AGENTS.md": "# Gravitas\n",
    "locales/ko/README.md": plugin_readme("한국어"),
}


def build(root, changes=None):
    """Write the fixture checkout into root; changes maps a path to (old, new) or to None to leave it out."""
    if os.path.exists(root):
        shutil.rmtree(root)
    for rel, text in FILES.items():
        change = (changes or {}).get(rel, ())
        if change is None:
            continue
        if change:
            old, new = change
            if old not in text:
                raise AssertionError("fixture %s has no %r" % (rel, old))
            text = text.replace(old, new, 1)
        path = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)


def run(root):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, SCRIPT, "--root", root], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       env=env)
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")


def fails_on(tmp, name, file, changes, *needles, also=()):
    """The changed checkout fails on file, naming every needle, and every other file except those in also passes."""
    root = os.path.join(tmp, "case")
    build(root, changes)
    code, out = run(root)
    block = section(out, file)
    ok = code == 1 and block.startswith(file.ljust(24) + " FAIL") and all(n in block for n in needles)
    others = [l for l in out.splitlines() if l and not l.startswith(" ")
              and not any(l.startswith(f + " ") for f in (file,) + tuple(also))]
    ok = ok and len(others) == 7 - len(also) and all(l.endswith(" OK") for l in others)
    case(name, ok, out[-700:])


def section(out, file):
    lines, keep = [], False
    for l in out.splitlines():
        if not l.startswith(" "):
            keep = l.startswith(file + " ")
        if keep:
            lines.append(l)
    return "\n".join(lines)


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    # Pure functions first.
    case("slug: an English heading gets GitHub's id",
         rp.slug("Part 1: What Gravitas Does For You") == "part-1-what-gravitas-does-for-you")
    case("slug: code, punctuation and CJK are handled as GitHub does",
         rp.slug("`check_skills.py` 的用法") == "check_skillspy-的用法"
         and rp.slug("Install Gravitas (Windows).cmd") == "install-gravitas-windowscmd"
         and rp.slug("결과와 방법") == "결과와-방법", repr(rp.slug("`check_skills.py` 的用法")))
    case("anchors: a repeated heading gets -1, a closing # run is dropped, and <a id> counts",
         rp.anchors("# A\n## A\n## Learn C# ##\n<a id=\"x\"></a>\n```\n# not a heading\n```\n")
         == {"a", "a-1", "learn-c", "x"}, repr(rp.anchors("# A\n## A\n## Learn C# ##\n<a id=\"x\"></a>\n")))
    nums = rp.headline_numbers(EN)
    case("headline numbers: shares, intervals and vote counts from a table and from text",
         {("share", "0.57"), ("share", "0.48"), ("share", "0.66"), ("share", "0.42"), ("votes", "120"),
          ("votes", "100"), ("votes", "60")} <= nums, repr(sorted(nums)))
    case("headline numbers: an example's 8 votes, on a line with no win share, is not one",
         ("votes", "8") not in nums)
    case("headline numbers: '0.45 over 120' counts 120 as votes, and a share is not read as a vote count",
         ("votes", "120") in rp.headline_numbers("Run 2 scored 0.45 over 120.\n")
         and rp.headline_numbers("a share over 0.55\n") == {("share", "0.55")},
         repr(rp.headline_numbers("a share over 0.55\n")))
    case("commands: comments and placeholder names do not count, the command does",
         rp.commands(EN) == rp.commands(JA) == {"python scripts/install.py ja --review", "python scripts/install.py <>"},
         repr(rp.commands(JA)))
    case("commands: in a console block only the prompted lines are commands",
         rp.commands("```console\n$ python scripts/install.py\nInstalled.\n```\n") == {"python scripts/install.py"})

    tmp = tempfile.mkdtemp(prefix="gv parity 王 ")
    try:
        root = os.path.join(tmp, "case")
        build(root)
        code, out = run(root)
        case("a checkout whose native READMEs reorder, rename and add example votes passes", code == 0
             and out.count(" OK\n") == 8, out[-900:])

        fails_on(tmp, "a win share missing from a native README fails and is named", "README.ja.md",
                 {"README.ja.md": ("Grok 4.5 0.42 ", "Grok 4.5 ")}, "share 0.42",
                 "in the English README but not here")
        fails_on(tmp, "a wrong vote count in a native README's table fails and is named", "README.zh-CN.md",
                 {"README.zh-CN.md": ("| world | Pro | 100 |", "| world | Pro | 10 |")}, "votes 10",
                 "here but not in the English README")
        fails_on(tmp, "a renamed installer fails", "README.ko.md",
                 {"README.ko.md": ("`Install Gravitas (Mac).command`", "`Install Gravitas.command`")},
                 "Install Gravitas (Mac).command")
        fails_on(tmp, "a changed command fails", "README.ja.md",
                 {"README.ja.md": ("install.py ja --review", "install.py ja")}, "python scripts/install.py ja --review")
        fails_on(tmp, "a link to a file that does not exist fails", "README.ja.md",
                 {"README.ja.md": ("docs/examples/ja/case.md", "docs/examples/ja/gone.md")}, "gone.md does not exist")
        fails_on(tmp, "a link spelled with the wrong case fails, as it would on GitHub", "README.ko.md",
                 {"README.ko.md": ("docs/examples/ko/case.md", "Docs/examples/ko/case.md")}, "does not exist")
        fails_on(tmp, "a link to a heading that does not exist fails", "README.ja.md",
                 {"README.ja.md": ("[結果](#結果)", "[結果](#結果2)")}, "no heading or id '結果2'")
        fails_on(tmp, "a link to a missing heading in another file fails", "README.md",
                 {"README.md": ("comparison.md#method", "comparison.md#methods")}, "no heading or id 'methods'")
        fails_on(tmp, "a README without the language-switch line fails", "README.zh-CN.md",
                 {"README.zh-CN.md": ("**简体中文** · ", "")}, "no language-switch line")
        fails_on(tmp, "a switch line without its own language in bold fails", "README.ja.md",
                 {"README.ja.md": ("**日本語**", "日本語")}, "日本語, this file's language, is not in bold")
        fails_on(tmp, "a switch line linking the wrong README fails", "README.ko.md",
                 {"README.ko.md": ("[日本語](./README.ja.md)", "[日本語](./README.zh-CN.md)")},
                 "日本語 links ./README.zh-CN.md, not README.ja.md")
        fails_on(tmp, "a README inside the plugin that links another language by a relative path fails",
                 "locales/ja/README.md",
                 {"locales/ja/README.md": ("(%sREADME.md)" % GH, "(./README.md)")}, "needs the full URL")
        fails_on(tmp, "a link out of the plugin folder fails, since it is not there once installed",
                 "plugin/README.md", {"plugin/README.md": ("[rules](rules/AGENTS.md)", "[rules](../LICENSE)")},
                 "does not exist in the plugin as installed")
        fails_on(tmp, "a locale's link that resolves in neither its folder nor plugin/ fails",
                 "locales/ko/README.md",
                 {"locales/ko/README.md": ("[rules](rules/AGENTS.md)", "[rules](rules/RULES.md)")},
                 "rules/RULES.md does not exist")
        fails_on(tmp, "a missing native README fails, and so does every switch line that links it",
                 "README.ko.md", {"README.ko.md": None}, "missing",
                 also=("README.md", "README.ja.md", "README.zh-CN.md"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = r.stdout.decode("utf-8", "replace")
    heads = [l for l in out.splitlines() if l and not l.startswith(" ")]
    case("this repository's READMEs parse: one OK or FAIL line for each of the 8, and no traceback",
         r.returncode in (0, 1) and len(heads) == 8 and all(l.endswith((" OK", " FAIL")) for l in heads)
         and "Traceback" not in out, out[-600:])

    failed = RESULTS.count(False)
    print("%d/%d passed" % (len(RESULTS) - failed, len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
