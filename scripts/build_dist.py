#!/usr/bin/env python3
"""Write dist/<lang>/gravitas, the plugin folders the double-click installers copy.

    python scripts/build_dist.py        # rebuild dist/ in this repository
    python scripts/build_dist.py OUT    # write the same folders into OUT, a new or empty folder

Install Gravitas (Windows).cmd and Install Gravitas (Mac).command run without
Python, so they cannot run install.py. They copy dist/<lang>/gravitas instead.
This script writes those folders with install.py's own prepare() and build(), so
each one holds exactly what `python scripts/install.py <lang>` installs when no
option is given, with the Second Opinion set by install.py's REVIEW_DEFAULT. Each
folder is then validated with its own check_skills.py, as install.py validates
an install.

Every language is validated before anything is written, and dist/ is rebuilt in
dist.new/ and swapped in only when every folder passes, so a failure leaves the
old dist/ whole.

Run it after any change under plugin/ or locales/ and commit dist/ with that
change. tests/scripts/test_build_dist.py fails while dist/ in the checkout
differs from a fresh build, and scripts/release_check.py fails while the commit
does.
"""
import os
import shutil
import sys

sys.dont_write_bytecode = True  # importing install.py would otherwise leave scripts/__pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import install  # noqa: E402

# The folders under dist/, and the languages the double-click installers offer.
LANGS = ("en", "zh-CN", "ja", "ko")
DIST = os.path.join(install.REPO, "dist")


def build_all(out):
    """Write out/<lang>/gravitas for every language. True when every folder validates.

    Each language is prepared, which validates its sources and stops on a fault, before any is built.
    """
    plans = [(lang, install.prepare(lang, install.REVIEW_DEFAULT, False)) for lang in LANGS]
    ok = True
    for lang, (locale, rule, review, status) in plans:
        dest = os.path.join(out, lang, "gravitas")
        install.build(dest, locale, rule, review)
        print("built %s (Second Opinion %s)" % (dest, status))
        ok = install.check_installed(dest) and ok
    return ok


def replace_dist(new):
    """Put the folder new in place of dist/. dist/ is renamed aside first, which fails at once if a file
    in it is open, so there is never a half-deleted dist/."""
    old = DIST + ".old"
    if os.path.lexists(old):
        shutil.rmtree(old)  # left by an earlier run that could not finish deleting it; generated
    try:
        if os.path.isdir(DIST):
            os.rename(DIST, old)
    except OSError as exc:
        sys.exit("could not move dist/ aside (%s). Close any program that has a file in it open and run "
                 "this again. dist/ is unchanged; the new build is in %s" % (exc, new))
    os.rename(new, DIST)
    try:
        shutil.rmtree(old)
    except FileNotFoundError:
        pass
    except OSError as exc:
        print("could not delete %s (%s); delete it by hand" % (old, exc))


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    if len(argv) > 1 or any(a.startswith("-") for a in argv):
        sys.exit("usage: build_dist.py [OUT]")
    out = os.path.abspath(argv[0]) if argv else DIST
    if out == DIST:
        new = DIST + ".new"
        if os.path.lexists(new):
            shutil.rmtree(new)  # left by an earlier run that failed; generated
        if not build_all(new):
            sys.exit("a built folder does not validate; see above. dist/ is unchanged, and the failed "
                     "build is in %s" % new)
        replace_dist(new)
    else:
        if os.path.isdir(out) and os.listdir(out):
            sys.exit("%s is not empty; give a new or empty folder" % out)
        if not build_all(out):
            sys.exit("a built folder does not validate; see above")
    print("dist is ready in %s" % out)


if __name__ == "__main__":
    main(sys.argv[1:])
