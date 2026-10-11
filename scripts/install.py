#!/usr/bin/env python3
"""Install Gravitas as an Antigravity plugin.

    python scripts/install.py              # English
    python scripts/install.py zh-CN        # 简体中文
    python scripts/install.py ja           # 日本語
    python scripts/install.py ko           # 한국어
    python scripts/install.py --review     # with the Second Opinion (off by default)
    python scripts/install.py --no-review  # without it, even if REVIEW_DEFAULT changes
    python scripts/install.py --uninstall

The plugin goes to ~/.gemini/config/plugins/gravitas/. The CLI reads a workspace
.agents/ folder only when the repo is passed with --add-dir, so the global location
is the one that works from every directory.

The rule's Second Opinion section (an independent review of answers people rely
on, by the gravitas-reviewer agent) sits in rules/AGENTS.md between the lines
<!-- gravitas:second-opinion --> and <!-- /gravitas:second-opinion -->. With the
review on, the installer removes only those two lines. With --no-review it removes
the section and both lines from the installed rule and does not install
agents/gravitas-reviewer.md. REVIEW_DEFAULT below decides which applies when
neither --review nor --no-review is given. A translated rule that has no marked
section installs with the review off and says so; --review then stops the install.
A rule that still names gravitas-reviewer while the review is off also stops it.
Both stops happen before anything is changed.

Earlier versions installed a bare skill at ~/.gemini/config/skills/gravitas and a
PreInvocation hook named gravitas-always-on. Both are moved into a timestamped
backup folder, on install and on uninstall, because the plugin's rule replaces the
hook and a second copy of the skill would compete with the plugin's. An unreleased
development build also left a hooks.json inside the plugin folder, which goes to the
backup with the old plugin folder, and a log folder at ~/.gemini/gravitas, which is
moved to the same backup. This release installs no hooks.

Backup folders are named for the date and time, YYYYMMDD-HHMMSS, inside
~/.gemini/gravitas-backups/. The double-click installers at the repository root
(Install Gravitas (Windows).cmd and Install Gravitas (Mac).command) use the same
folder, and move things the same way: nothing is deleted.

The new plugin is built inside the backup folder first and validated there with
its own check_skills.py. Only then is the installed plugin moved into the backup
and the new one moved into its place, so a failed build or check leaves the
installed plugin as it was. A fault exits 1; faults in other installed plugins are
not this installer's to fix.

build() writes the plugin folder for one language. scripts/build_dist.py calls it
to write dist/<lang>/gravitas, the folders the double-click installers copy, so an
install by either route is the same files.
"""
import errno
import datetime
import importlib.util
import json
import os
import shutil
import subprocess
import sys

# Whether the Second Opinion is installed when neither --review nor --no-review is given.
# Off: in the decision test of 3 October 2026 the review did not beat the rule alone on Gemini 3.8 Flash, and its
# holding line cost points in headless output, at about twice the time per answer. --review turns it on.
REVIEW_DEFAULT = False

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
CONFIG = os.path.join(HOME, ".gemini", "config")
DEST = os.path.join(CONFIG, "plugins", "gravitas")
CHECK = os.path.join(REPO, "plugin", "skills", "gravitas", "scripts", "check_skills.py")
LANGS = {"en": None, "zh": "zh-CN", "zh-CN": "zh-CN", "ja": "ja", "ko": "ko"}
REVIEWER = "gravitas-reviewer"
MARK_OPEN = "<!-- gravitas:second-opinion -->"
MARK_CLOSE = "<!-- /gravitas:second-opinion -->"
# Every backup goes in a dated folder here, from this script and from the double-click installers.
BACKUPS = os.path.join(HOME, ".gemini", "gravitas-backups")
# Where the development build's hooks kept their logs. Nothing in this release writes here.
HOOK_STATE = os.path.join(HOME, ".gemini", "gravitas")
HOOK_STATE_FILES = {"errors.log", "turns.jsonl", "turns.jsonl.lock"}
# Editor and file-manager leftovers that must never reach dist/ or an install.
CLUTTER = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "._*", "Thumbs.db", "desktop.ini",
                                 "*~", "*.swp", "*.orig", "*.rej")


def second_opinion(text, review, where):
    """The rule text with the marked Second Opinion section kept (review on) or removed (review off),
    and whether the text had a marked section at all.

    The marker lines go either way. Removing the section can leave two blank lines where it stood,
    and they are joined into one. Unbalanced markers stop the install before anything is changed.
    """
    out, inside, removed, found = [], False, False, False
    for line in text.splitlines(True):
        mark = line.strip()
        if mark == MARK_OPEN:
            if inside:
                sys.exit("%s: %s appears twice without %s; nothing was installed" % (where, MARK_OPEN, MARK_CLOSE))
            inside = found = True
            continue
        if mark == MARK_CLOSE:
            if not inside:
                sys.exit("%s: %s has no opening line; nothing was installed" % (where, MARK_CLOSE))
            inside, removed = False, not review
            continue
        if inside and not review:
            continue
        if removed and not mark and out and not out[-1].strip():
            continue
        removed = False
        out.append(line)
    if inside:
        sys.exit("%s: %s is never closed; nothing was installed" % (where, MARK_OPEN))
    return "".join(out), found


def backup_dir():
    """A new, empty backup folder; a second run in the same second gets its own."""
    base = os.path.join(BACKUPS, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    path, n = base, 1
    while True:
        try:
            os.makedirs(path)
            return path
        except FileExistsError:
            n += 1
            path = "%s-%d" % (base, n)


def drop_if_empty(backup):
    """Remove a backup folder nothing was moved into, then the backups folder if that left it empty."""
    for path in (backup, BACKUPS):
        try:
            os.rmdir(path)
        except OSError:  # not empty, so it stays
            return


def rename(src, dst):
    """Move src to dst, which must not exist. Within one drive this is a rename, which either happens
    whole or not at all; shutil.move's fallback, a copy and then a delete, could stop halfway on a
    file Antigravity holds open. A different drive gets that fallback, since a rename cannot work.
    If it stops halfway, the files it deleted from a folder are copied back from dst and the copy at
    dst is removed, so src is whole again when the error is raised."""
    if os.path.lexists(dst):
        raise FileExistsError(errno.EEXIST, "already exists", dst)
    try:
        os.rename(src, dst)
    except OSError as exc:
        if exc.errno != errno.EXDEV and getattr(exc, "winerror", None) != 17:  # 17: not the same device
            raise
        try:
            shutil.move(src, dst)
        except OSError:
            if os.path.isdir(src) and os.path.isdir(dst):
                for root, _, files in os.walk(dst):
                    back = os.path.join(src, os.path.relpath(root, dst))
                    os.makedirs(back, exist_ok=True)
                    for name in files:
                        if not os.path.lexists(os.path.join(back, name)):
                            shutil.copy2(os.path.join(root, name), os.path.join(back, name))
                shutil.rmtree(dst, ignore_errors=True)
            raise


def move_aside(path, backup, label, name=None):
    if os.path.lexists(path):
        rename(path, os.path.join(backup, name or os.path.basename(path)))
        print("  moved %s to %s" % (label, backup))
        return True
    return False


def retire_hook_state(backup):
    """The log folder of an unreleased build with hooks. Its hooks.json was inside the plugin folder,
    so it goes to the backup with the old plugin."""
    if os.path.isdir(HOOK_STATE):
        if set(os.listdir(HOOK_STATE)) <= HOOK_STATE_FILES:
            move_aside(HOOK_STATE, backup, "the development hooks' log folder", "gravitas-hook-state")
        else:
            print("  left %s in place: it holds files the development hooks did not write" % HOOK_STATE)


def read_legacy_hooks():
    """~/.gemini/config/hooks.json, parsed before anything is moved.

    None when it is absent or unreadable; an unreadable file is reported and left alone, and the
    rest of the install goes ahead.
    """
    path = os.path.join(CONFIG, "hooks.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        print("  %s does not parse (%s); left unchanged. Remove any gravitas-always-on entry by hand."
              % (path, exc))
        return None
    if not isinstance(data, dict):
        print("  %s is not a JSON object; left unchanged. Remove any gravitas-always-on entry by hand." % path)
        return None
    return data


def migrate_legacy(backup, hooks_data):
    """Move beta 1's skill and hook script into the backup and take its hook out of hooks.json.
    True when any of them was there. A hooks.json that could not be read keeps its entry, so the
    script the entry runs stays too, as the double-click installers leave it."""
    found = move_aside(os.path.join(CONFIG, "skills", "gravitas"), backup, "the old skill install",
                       "skills-gravitas")
    hooks = os.path.join(CONFIG, "hooks.json")
    if hooks_data is not None and "gravitas-always-on" in hooks_data:
        shutil.copy2(hooks, os.path.join(backup, "hooks.json"))
        del hooks_data["gravitas-always-on"]
        with open(hooks, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(hooks_data, fh, indent=2)
            fh.write("\n")
        print("  removed the gravitas-always-on hook from hooks.json (copy in the backup)")
        found = True
    if hooks_data is not None or not os.path.exists(hooks):
        found = move_aside(os.path.join(CONFIG, "scripts", "gravitas_always_on.py"), backup,
                           "the old hook script") or found
    return found


def check_installed(dest=DEST):
    """Validate the installed plugin with its own copy of check_skills.py. True when nothing is broken."""
    path = os.path.join(dest, "skills", "gravitas", "scripts", "check_skills.py")
    # Loading the checker would otherwise leave a __pycache__ folder inside the plugin it checks.
    saved, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec = importlib.util.spec_from_file_location("gravitas_installed_check", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        rep = mod.Report()
        mod.check_plugin(dest, rep)
    except Exception as exc:  # a checker that cannot run has not validated anything
        print("  the installed check_skills.py did not run: %r" % exc)
        return False
    finally:
        sys.dont_write_bytecode = saved
    c = rep.counts
    print("checked %d skill(s), %d agent(s), %d rule file(s), %d plugin(s)"
          % (c["skills"], c["agents"], c["rules"], c["plugins"]))
    for where, msg in rep.problems:
        print("  BROKEN  %-40s %s" % (where, msg))
    for where, msg in rep.notes:
        print("  note    %-40s %s" % (where, msg))
    print("FAIL: %d problem(s)" % len(rep.problems) if rep.problems else "OK")
    return not rep.problems


def prepare(lang_arg, review, explicit):
    """Validate the repository and settle what to install, before anything is changed.

    Returns (locale, rule, review, status): locale is None for English, rule is the text of the rule
    to install, review says whether the Second Opinion goes in, and status is how to report it.
    """
    if lang_arg not in LANGS:
        sys.exit("unknown language %r; use en, zh-CN, ja or ko" % lang_arg)
    locale = LANGS[lang_arg]
    lang = locale or "en"
    if subprocess.call([sys.executable, CHECK, "--repo", "--locales", locale or "none"]) != 0:
        sys.exit("the repository does not validate; nothing was installed")
    src = os.path.join(REPO, "locales", locale) if locale else None
    rule_src = os.path.join(src or os.path.join(REPO, "plugin"), "rules", "AGENTS.md")
    where = os.path.relpath(rule_src, REPO)
    with open(rule_src, encoding="utf-8", newline="") as fh:
        rule, marked = second_opinion(fh.read(), review, where)
    status = "on" if review else "off"
    if review and not marked:
        if explicit:
            sys.exit("%s has no Second Opinion section, so --review cannot apply; nothing was installed" % where)
        review, status = False, "not available in %s yet" % lang
    if not review and REVIEWER in rule:
        sys.exit("%s still names %s with the review off; check its %s lines. Nothing was installed"
                 % (where, REVIEWER, MARK_OPEN))
    if review and not os.path.isfile(os.path.join(REPO, "plugin", "agents", REVIEWER + ".md")):
        sys.exit("plugin/agents/%s.md is missing and the rule calls it; nothing was installed" % REVIEWER)
    return locale, rule, review, status


def build(dest, locale, rule, review):
    """Write the plugin folder for one language to dest, which must not exist yet.

    install() writes it to ~/.gemini/config/plugins/gravitas, and scripts/build_dist.py writes it to
    dist/<lang>/gravitas for the double-click installers.
    """
    shutil.copytree(os.path.join(REPO, "plugin"), dest, ignore=CLUTTER)
    if locale:
        src = os.path.join(REPO, "locales", locale)
        skill = os.path.join(dest, "skills", "gravitas")
        shutil.rmtree(skill)
        shutil.copytree(os.path.join(src, "skills", "gravitas"), skill, ignore=CLUTTER)
        for name in ("examples", "schemas", "scripts"):
            if not os.path.exists(os.path.join(skill, name)):
                shutil.copytree(os.path.join(REPO, "plugin", "skills", "gravitas", name),
                                os.path.join(skill, name), ignore=CLUTTER)
        # what Antigravity lists for the plugin, and the README beside it, in the installed language
        shutil.copy2(os.path.join(src, "README.md"), os.path.join(dest, "README.md"))
        with open(os.path.join(dest, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        with open(os.path.join(src, "plugin.json"), encoding="utf-8") as fh:
            manifest.update(json.load(fh))
        with open(os.path.join(dest, "plugin.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    with open(os.path.join(dest, "rules", "AGENTS.md"), "w", encoding="utf-8", newline="") as fh:
        fh.write(rule)
    if not review:
        reviewer = os.path.join(dest, "agents", REVIEWER + ".md")
        if os.path.exists(reviewer):
            os.remove(reviewer)


def install(lang_arg, review, explicit):
    locale, rule, review, status = prepare(lang_arg, review, explicit)
    hooks_data = read_legacy_hooks()

    backup = backup_dir()
    staging = os.path.join(backup, "new")
    new = os.path.join(staging, "gravitas")
    build(new, locale, rule, review)
    if not check_installed(new):
        shutil.rmtree(staging)
        drop_if_empty(backup)
        sys.exit("the built plugin does not validate; see above. Nothing was installed")

    try:
        moved = move_aside(DEST, backup, "the previous install")  # the dev build's hooks.json goes with it
    except OSError as exc:
        shutil.rmtree(staging)
        drop_if_empty(backup)
        sys.exit("could not move the installed plugin out of the way (%s). If Antigravity is running, quit "
                 "it and run the installer again. Nothing was changed" % exc)
    try:
        os.makedirs(os.path.dirname(DEST), exist_ok=True)
        rename(new, DEST)
    except OSError as exc:
        shutil.rmtree(staging, ignore_errors=True)
        if moved:
            try:
                rename(os.path.join(backup, "gravitas"), DEST)
            except OSError:
                sys.exit("could not put the new plugin in place (%s), and could not put the previous install "
                         "back; it is in %s" % (exc, os.path.join(backup, "gravitas")))
        drop_if_empty(backup)
        sys.exit("could not put the new plugin in place (%s). Nothing was changed" % exc)
    os.rmdir(staging)
    print("installed Gravitas (%s, Second Opinion %s) to %s" % (locale or "en", status, DEST))

    retire_hook_state(backup)
    migrate_legacy(backup, hooks_data)
    drop_if_empty(backup)
    print("Restart Antigravity, or start a new agy session, to pick up the change.")


def uninstall():
    hooks_data = read_legacy_hooks()
    backup = backup_dir()
    try:
        found = move_aside(DEST, backup, "the plugin")
    except OSError as exc:
        drop_if_empty(backup)
        sys.exit("could not move the installed plugin (%s). If Antigravity is running, quit it and run "
                 "the uninstall again. Nothing was changed" % exc)
    retire_hook_state(backup)
    found = migrate_legacy(backup, hooks_data) or found
    if not found:
        print("no Gravitas install found in %s" % CONFIG)
    drop_if_empty(backup)


def main(argv):
    # A piped stdout uses the ANSI code page on Windows, which cannot print every home folder's name.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    flags = [a for a in argv if a.startswith("-")]
    langs = [a for a in argv if not a.startswith("-")]
    usage = "usage: install.py [en|zh-CN|ja|ko] [--review | --no-review] | --uninstall"
    if "-h" in flags or "--help" in flags:
        print(usage)
        if __doc__:
            print(__doc__.split("\n\n")[1])
        return
    unknown = sorted(set(flags) - {"--uninstall", "--review", "--no-review"})
    if unknown or len(langs) > 1 or {"--review", "--no-review"} <= set(flags):
        sys.exit(usage)
    if "--uninstall" in flags:
        uninstall()
    else:
        review = False if "--no-review" in flags else True if "--review" in flags else REVIEW_DEFAULT
        install(langs[0] if langs else "en", review, "--review" in flags)


if __name__ == "__main__":
    main(sys.argv[1:])
