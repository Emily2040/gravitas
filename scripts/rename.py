#!/usr/bin/env python3
"""Rename the skill everywhere: frontmatter, README, installed copy, and the
always-on PreInvocation hook that names it.

    python scripts/rename.py <new-name>
"""
import io
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(os.path.expanduser("~"), ".gemini", "config", "skills")
HOOK = os.path.join(os.path.expanduser("~"), ".gemini", "config", "scripts",
                    "ultracode_always_on.py")


def current_name():
    t = io.open(os.path.join(REPO, "skill", "SKILL.md"), encoding="utf-8").read()
    m = re.search(r"^name:\s*(\S+)\s*$", t, re.M)
    return m.group(1) if m else None


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    new = sys.argv[1].strip()
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", new):
        print("name must be lowercase, digits and hyphens only")
        return 2
    old = current_name()
    if not old:
        print("could not read current name from skill/SKILL.md")
        return 1
    if old == new:
        print("already named", new)
        return 0

    # repo files
    for rel in ["skill/SKILL.md", "README.md"]:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if os.path.exists(p):
            t = io.open(p, encoding="utf-8").read()
            io.open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
            print("  updated", rel)

    # installed copy
    old_dir, new_dir = os.path.join(SKILLS, old), os.path.join(SKILLS, new)
    if os.path.isdir(old_dir):
        if os.path.isdir(new_dir):
            shutil.rmtree(new_dir)
        shutil.move(old_dir, new_dir)
        src = os.path.join(new_dir, "SKILL.md")
        t = io.open(src, encoding="utf-8").read()
        io.open(src, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
        print("  moved installed skill to", new_dir)

    # the always-on hook names the skill in its injected reminder
    if os.path.exists(HOOK):
        t = io.open(HOOK, encoding="utf-8").read()
        if old in t or "ultracode" in t:
            t = t.replace(old, new).replace("ultracode", new)
            io.open(HOOK, "w", encoding="utf-8", newline="\n").write(t)
            print("  updated the always-on hook reminder")

    print("renamed %s -> %s. Restart Antigravity." % (old, new))
    return 0


if __name__ == "__main__":
    sys.exit(main())
