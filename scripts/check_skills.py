#!/usr/bin/env python3
"""Validate Antigravity skills, because broken ones fail silently.

Antigravity logs `skills.go:201 Failed to parse skill file ...` and skips the skill,
but surfaces nothing to the user -- the skill is simply absent. This checks the same
things up front.

Usage:  python check_skills.py [extra_skills_dir ...]
Exit:   0 = all good, 1 = at least one problem found.
"""
import os
import re
import sys

GLOBAL = os.path.expanduser(os.path.join("~", ".gemini", "config", "skills"))


def parse_frontmatter(text):
    """Return (dict_or_None, error_string_or_None)."""
    if not text.startswith("---"):
        return None, "no frontmatter (file must start with ---)"
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None, "frontmatter opened but never closed with ---"
    block = m.group(1)
    try:
        import yaml
        data = yaml.safe_load(block)
        if not isinstance(data, dict):
            return None, "frontmatter is not a YAML mapping"
        return data, None
    except ImportError:
        data = {}
        for line in block.split("\n"):
            if ":" in line and not line.startswith((" ", "\t", "-")):
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip().strip('"').strip("'")
        return data, None
    except Exception as exc:
        return None, "YAML parse error: %s" % str(exc).replace("\n", " ")[:120]


def check_dir(root):
    problems, checked = [], 0
    if not os.path.isdir(root):
        return problems, checked, ["directory does not exist: %s" % root]
    notes = []
    for entry in sorted(os.listdir(root)):
        sdir = os.path.join(root, entry)
        if not os.path.isdir(sdir):
            continue
        path = os.path.join(sdir, "SKILL.md")
        if not os.path.exists(path):
            problems.append((entry, "no SKILL.md in the skill directory"))
            continue
        checked += 1
        text = open(path, encoding="utf-8", errors="replace").read()
        if text.startswith("\ufeff"):
            problems.append((entry, "file begins with a UTF-8 BOM, which breaks parsing"))
            continue
        data, err = parse_frontmatter(text)
        if err:
            problems.append((entry, err))
            continue
        name = data.get("name")
        desc = data.get("description")
        if not name:
            problems.append((entry, "frontmatter has no 'name'"))
        elif name != entry:
            problems.append((entry, "frontmatter name %r does not match directory name %r" % (name, entry)))
        if not desc:
            problems.append((entry, "frontmatter has no 'description' (the agent uses it to decide when to load the skill)"))
        elif len(str(desc)) < 30:
            notes.append("%s: description is very short (%d chars); the agent may never trigger it"
                         % (entry, len(str(desc))))
        for _, target in re.findall(r"\[([^\]]+)\]\((\.[^)]+)\)", text):
            if not os.path.exists(os.path.normpath(os.path.join(sdir, target))):
                problems.append((entry, "dead relative link: %s" % target))
    return problems, checked, notes


def main():
    roots = [GLOBAL] + sys.argv[1:]
    total_problems, total_checked, all_notes = [], 0, []
    for root in roots:
        problems, checked, notes = check_dir(root)
        print("== %s ==" % root)
        print("   skills checked: %d" % checked)
        total_checked += checked
        all_notes.extend(notes)
        for entry, msg in problems:
            print("   BROKEN  %-28s %s" % (entry, msg))
            total_problems.append((entry, msg))
        if not problems:
            print("   all valid")
    for n in all_notes:
        print("   note    %s" % n)
    print()
    if total_problems:
        print("FAIL: %d problem(s) across %d skill(s)" % (len(total_problems), total_checked))
        return 1
    print("OK: %d skill(s) valid" % total_checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
