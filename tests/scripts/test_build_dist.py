#!/usr/bin/env python3
"""Tests for scripts/build_dist.py and the dist/ folder committed with it.

Run with plain `python tests/scripts/test_build_dist.py`. Each case prints one
PASS or FAIL line; the exit status is 1 if any case fails.

The double-click installers copy dist/<lang>/gravitas and never see plugin/ or
locales/. So the main case rebuilds dist/ into a temporary folder and compares
it byte for byte with the dist/ in this checkout: an edit under plugin/ or
locales/ that was not followed by `python scripts/build_dist.py` fails here.
This checks the working tree; scripts/release_check.py checks that the same
holds for what is committed, which is what a download contains.
The parity cases install with `python scripts/install.py <lang>` into throwaway
home folders and check that each dist folder is exactly what it installs. The
last cases run build_dist.py in a throwaway copy of the repository: editor and
file-manager leftovers never reach dist/, and a source that does not validate,
or a dist/ file held open, leaves the old dist/ whole.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BUILD = os.path.join(REPO, "scripts", "build_dist.py")
INSTALL = os.path.join(REPO, "scripts", "install.py")
DIST = os.path.join(REPO, "dist")
LANGS = ("en", "zh-CN", "ja", "ko")
MARKS = ("<!-- gravitas:second-opinion -->", "<!-- /gravitas:second-opinion -->")

RESULTS = []


def case(name, ok, detail=""):
    RESULTS.append(ok)
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


def run(args, env=None):
    env = dict(os.environ if env is None else env, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")


def tree(root):
    """({relative path: bytes} for every file under root, {relative path} for every folder)."""
    files, dirs = {}, set()
    for d, subdirs, names in os.walk(root):
        for s in subdirs:
            dirs.add(os.path.relpath(os.path.join(d, s), root).replace(os.sep, "/"))
        for n in names:
            p = os.path.join(d, n)
            with open(p, "rb") as fh:
                files[os.path.relpath(p, root).replace(os.sep, "/")] = fh.read()
    return files, dirs


def differences(want, got):
    """One line per file or folder that is missing from got, extra in got, or different."""
    fw, dw = tree(want)
    fg, dg = tree(got)
    out = ["missing " + k for k in sorted(set(fw) - set(fg))]
    out += ["extra " + k for k in sorted(set(fg) - set(fw))]
    out += ["differs " + k for k in sorted(set(fw) & set(fg)) if fw[k] != fg[k]]
    out += ["missing folder " + k for k in sorted(dw - dg)]
    out += ["extra folder " + k for k in sorted(dg - dw)]
    return out


def brief(lines, n=12):
    return "; ".join(lines[:n]) + ("; and %d more" % (len(lines) - n) if len(lines) > n else "")


def review_default():
    with open(INSTALL, encoding="utf-8") as fh:
        m = re.search(r"^REVIEW_DEFAULT = (True|False)\s*$", fh.read(), re.M)
    return None if m is None else m.group(1) == "True"


def copy_repo(root):
    """The parts of the repository build_dist.py reads, and dist/, copied to root."""
    for name in ("plugin", "locales", "scripts", "dist"):
        shutil.copytree(os.path.join(REPO, name), os.path.join(root, name),
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return os.path.join(root, "scripts", "build_dist.py")


def sandbox(tmp):
    # Leftovers an editor, Finder, Explorer or a merge leaves beside the sources.
    root = os.path.join(tmp, "clutter repo")
    build = copy_repo(root)
    clutter = ["plugin/skills/gravitas/SKILL.md~", "plugin/skills/gravitas/references/Thumbs.db",
               "plugin/.DS_Store", "plugin/skills/gravitas/examples/._gates.example.js", "plugin/rules/AGENTS.md.orig",
               "plugin/rules/.AGENTS.md.swp", "plugin/desktop.ini",
               "locales/ja/skills/gravitas/references/__pycache__/x.cpython-310.pyc",
               "locales/ko/skills/gravitas/references/notes.rej"]
    for rel in clutter:
        path = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(b"x")
    out = os.path.join(tmp, "clutter out")
    code, log = run([build, out])
    names = {os.path.basename(k) for k in tree(out)[0]} | {os.path.basename(k) for k in tree(out)[1]}
    leaked = sorted(names & {os.path.basename(c) for c in clutter} | {n for n in names if n == "__pycache__"})
    case("build: editor and file-manager leftovers in plugin/ or locales/ never reach dist/",
         code == 0 and not leaked and not differences(DIST, out), "%s %s" % (leaked, log[-300:]))

    # A locale whose Second Opinion markers do not close: nothing is built, and dist/ stays whole.
    root = os.path.join(tmp, "broken repo")
    build = copy_repo(root)
    rule = os.path.join(root, "locales", "ko", "rules", "AGENTS.md")
    with open(rule, encoding="utf-8", newline="") as fh:
        text = fh.read()
    with open(rule, "w", encoding="utf-8", newline="") as fh:
        fh.write(text.replace(MARKS[1], ""))
    code, log = run([build])
    dist = os.path.join(root, "dist")
    case("build: a locale that does not validate stops the build before dist/ is touched",
         code != 0 and MARKS[1] not in text.replace(MARKS[1], "") and not differences(DIST, dist)
         and not os.path.exists(dist + ".new"), log[-400:])

    if sys.platform != "win32":
        return
    # A dist/ file open in an editor, which on Windows stops dist/ from being renamed.
    root = os.path.join(tmp, "busy repo")
    build = copy_repo(root)
    dist = os.path.join(root, "dist")
    import ctypes
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.CreateFileW.restype = ctypes.c_void_p
    h = k32.CreateFileW(os.path.join(dist, "en", "gravitas", "plugin.json"), 0x80000000, 3, None, 3, 0, None)
    try:
        code, log = run([build])
    finally:
        k32.CloseHandle(ctypes.c_void_p(h))
    case("build: a dist/ file held open stops the swap with a message, and dist/ stays whole",
         code != 0 and "dist/ is unchanged" in log and "Traceback" not in log
         and not differences(DIST, dist), log[-400:])


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    with tempfile.TemporaryDirectory(prefix="gv dist ") as tmp:
        fresh = os.path.join(tmp, "fresh dist")
        code, out = run([BUILD, fresh])
        case("build: build_dist.py writes every language into a new folder",
             code == 0 and all(os.path.isfile(os.path.join(fresh, l, "gravitas", "plugin.json")) for l in LANGS),
             out[-800:])

        diff = differences(fresh, DIST) if os.path.isdir(DIST) else ["dist/ does not exist"]
        case("build: dist/ in this checkout matches a fresh build", not diff,
             brief(diff) + ". Run: python scripts/build_dist.py")

        top = sorted(os.listdir(DIST)) if os.path.isdir(DIST) else []
        case("build: dist/ holds en, zh-CN, ja and ko, each with one gravitas folder",
             top == sorted(LANGS) and all(os.listdir(os.path.join(DIST, l)) == ["gravitas"] for l in top),
             repr(top))

        stray = [k for k in tree(fresh)[0] if "__pycache__" in k or k.endswith(".pyc")]
        case("build: no __pycache__ or .pyc in a built folder", not stray, brief(stray))

        busy = os.path.join(tmp, "busy")
        os.makedirs(busy)
        with open(os.path.join(busy, "keep.txt"), "w") as fh:
            fh.write("x")
        code, out = run([BUILD, busy])
        case("build: refuses an output folder that is not empty, and writes nothing there",
             code != 0 and os.listdir(busy) == ["keep.txt"], out[-400:])

        # install.py into throwaway homes. PYTHONDONTWRITEBYTECODE is cleared, as on a normal
        # machine, so a stray __pycache__ left by the install shows up as a difference.
        for lang in LANGS:
            home = os.path.join(tmp, "home %s 王 é" % lang)
            os.makedirs(home)
            env = dict(os.environ, USERPROFILE=home, HOME=home)
            env.pop("PYTHONDONTWRITEBYTECODE", None)
            code, out = run([INSTALL, lang], env)
            plugin = os.path.join(home, ".gemini", "config", "plugins", "gravitas")
            diff = differences(os.path.join(DIST, lang, "gravitas"), plugin) if code == 0 else [out[-600:]]
            others = sorted(tree(home)[1] - {".gemini", ".gemini/config", ".gemini/config/plugins"}
                            - {k for k in tree(home)[1] if k.startswith(".gemini/config/plugins/gravitas")})
            case("parity: dist/%s/gravitas is what install.py %s installs, and the install leaves "
                 "nothing else in the home folder" % (lang, lang),
                 code == 0 and not diff and not others, brief(diff + ["extra folder " + o for o in others]))

        sandbox(tmp)

    review = review_default()
    case("default: install.py's REVIEW_DEFAULT is readable", review is not None)
    for lang in LANGS:
        root = os.path.join(DIST, lang, "gravitas")
        try:
            with open(os.path.join(root, "rules", "AGENTS.md"), encoding="utf-8") as fh:
                rule = fh.read()
        except OSError as exc:
            case("default: dist/%s has its rule" % lang, False, str(exc))
            continue
        has_reviewer = os.path.exists(os.path.join(root, "agents", "gravitas-reviewer.md"))
        case("default: dist/%s has no Second Opinion marker lines, and the reviewer agent only when "
             "REVIEW_DEFAULT is on" % lang,
             not any(m in rule for m in MARKS) and has_reviewer == bool(review)
             and (review or "gravitas-reviewer" not in rule),
             "reviewer agent present: %s, REVIEW_DEFAULT: %s" % (has_reviewer, review))

    for lang in LANGS[1:]:
        root = os.path.join(DIST, lang, "gravitas")
        src = os.path.join(REPO, "locales", lang)
        try:
            with open(os.path.join(root, "plugin.json"), encoding="utf-8") as fh:
                got = json.load(fh).get("description")
            with open(os.path.join(src, "plugin.json"), encoding="utf-8") as fh:
                want = json.load(fh).get("description")
            with open(os.path.join(root, "README.md"), "rb") as a, open(os.path.join(src, "README.md"), "rb") as b:
                same_readme = a.read() == b.read()
            with open(os.path.join(root, "skills", "gravitas", "SKILL.md"), "rb") as a, \
                    open(os.path.join(src, "skills", "gravitas", "SKILL.md"), "rb") as b:
                same_skill = a.read() == b.read()
        except (OSError, ValueError) as exc:
            case("translated: dist/%s carries its language" % lang, False, str(exc))
            continue
        case("translated: dist/%s carries the %s description, README and SKILL.md" % (lang, lang),
             got == want and same_readme and same_skill)

    failed = RESULTS.count(False)
    print("%d/%d passed" % (len(RESULTS) - failed, len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
