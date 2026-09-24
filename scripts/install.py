#!/usr/bin/env python3
"""Install Gravitas as an Antigravity plugin.

    python scripts/install.py              # English
    python scripts/install.py zh-CN        # 简体中文
    python scripts/install.py ja           # 日本語
    python scripts/install.py ko           # 한국어
    python scripts/install.py --uninstall

The plugin goes to ~/.gemini/config/plugins/gravitas/. Workspace .agents/ folders
are not read by the CLI, so the global location is the one that works.

Earlier versions installed a bare skill at ~/.gemini/config/skills/gravitas and a
PreInvocation hook named gravitas-always-on. Both are moved into a timestamped
backup folder, because the plugin's rule replaces the hook and a second copy of the
skill would compete with the plugin's.
"""
import datetime
import json
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(os.path.expanduser("~"), ".gemini", "config")
DEST = os.path.join(CONFIG, "plugins", "gravitas")
CHECK = os.path.join(REPO, "plugin", "skills", "gravitas", "scripts", "check_skills.py")
LANGS = {"en": None, "zh": "zh-CN", "zh-CN": "zh-CN", "ja": "ja", "ko": "ko"}


def backup_dir():
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(CONFIG, "_backup_gravitas_" + stamp)
    os.makedirs(path, exist_ok=True)
    return path


def move_aside(path, backup, label):
    if os.path.exists(path):
        shutil.move(path, os.path.join(backup, os.path.basename(path)))
        print("  moved %s to %s" % (label, backup))
        return True
    return False


def migrate_legacy(backup):
    moved = move_aside(os.path.join(CONFIG, "skills", "gravitas"), backup, "the old skill install")
    moved |= move_aside(os.path.join(CONFIG, "scripts", "gravitas_always_on.py"), backup,
                        "the old hook script")
    hooks = os.path.join(CONFIG, "hooks.json")
    if os.path.exists(hooks):
        with open(hooks, encoding="utf-8") as fh:
            data = json.load(fh)
        if "gravitas-always-on" in data:
            shutil.copy2(hooks, os.path.join(backup, "hooks.json"))
            del data["gravitas-always-on"]
            with open(hooks, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(data, fh, indent=2)
                fh.write("\n")
            print("  removed the gravitas-always-on hook from hooks.json (copy in the backup)")
            moved = True
    return moved


def install(lang_arg):
    if lang_arg not in LANGS:
        sys.exit("unknown language %r; use en, zh-CN, ja or ko" % lang_arg)
    locale = LANGS[lang_arg]
    if subprocess.call([sys.executable, CHECK, "--repo", "--locales", locale or "none"]) != 0:
        sys.exit("the repository does not validate; nothing was installed")

    backup = backup_dir()
    if os.path.isdir(DEST):
        shutil.rmtree(DEST)  # a previous install of this plugin; the repository is its source
    shutil.copytree(os.path.join(REPO, "plugin"), DEST,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if locale:
        src = os.path.join(REPO, "locales", locale)
        skill = os.path.join(DEST, "skills", "gravitas")
        shutil.rmtree(skill)
        shutil.copytree(os.path.join(src, "skills", "gravitas"), skill)
        for name in ("examples", "schemas", "scripts"):
            if not os.path.exists(os.path.join(skill, name)):
                shutil.copytree(os.path.join(REPO, "plugin", "skills", "gravitas", name),
                                os.path.join(skill, name),
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copy2(os.path.join(src, "rules", "AGENTS.md"), os.path.join(DEST, "rules", "AGENTS.md"))
    print("installed Gravitas (%s) to %s" % (locale or "en", DEST))

    migrate_legacy(backup)
    if not os.listdir(backup):
        os.rmdir(backup)
    subprocess.call([sys.executable, os.path.join(DEST, "skills", "gravitas", "scripts", "check_skills.py")])
    print("Restart Antigravity, or run /skills reload in the CLI, to pick up the change.")


def uninstall():
    backup = backup_dir()
    if not move_aside(DEST, backup, "the plugin"):
        print("no plugin install found at %s" % DEST)
        os.rmdir(backup)


def main(argv):
    if argv[:1] == ["--uninstall"]:
        uninstall()
    else:
        install(argv[0] if argv else "en")


if __name__ == "__main__":
    main(sys.argv[1:])
