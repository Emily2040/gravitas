#!/usr/bin/env python3
"""Tests for scripts/release_check.py and scripts/build_release_zip.py.

Run with plain `python tests/scripts/test_release.py`. Each case prints one
PASS, FAIL or SKIP line; the exit status is 1 if any case fails.

Both scripts read a commit through git. These tests make a tree of the working
tree as it is, in a throwaway index and a throwaway object folder, and pass its
ID instead of HEAD: the repository's own index, objects, refs and working tree
are never written. With that tree they check that release_check.py passes, that
it catches a stale dist/ and a wrong version in a README link, and that the
Gravitas.zip build_release_zip.py makes holds only the two installers, LICENSE
and dist/, with the right line endings and modes. Then they unzip it into a
folder named the way a second download is, run the installer from there in a
throwaway home, and compare the result with `python scripts/install.py`.
"""
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHECK = os.path.join(REPO, "scripts", "release_check.py")
ZIPPER = os.path.join(REPO, "scripts", "build_release_zip.py")
INSTALL = os.path.join(REPO, "scripts", "install.py")
CMD = "Install Gravitas (Windows).cmd"
COMMAND = "Install Gravitas (Mac).command"
SHIPPED = ["dist", "plugin", "locales", "scripts", CMD, COMMAND, ".gitattributes", "LICENSE",
           "README.md", "README.zh-CN.md", "README.ja.md", "README.ko.md",
           "docs", "tests", "CHANGELOG.md", "TESTS.md"]

RESULTS = []


def case(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


def skip(name, why):
    print("SKIP %s  -- %s" % (name, why))


class Scratch:
    """git with a throwaway index and object folder; objects already in the repository are read through
    the alternates list, and every object written goes to the throwaway folder."""

    def __init__(self, root):
        self.env = dict(os.environ, GIT_INDEX_FILE=os.path.join(root, "index"),
                        GIT_OBJECT_DIRECTORY=os.path.join(root, "objects"),
                        GIT_ALTERNATE_OBJECT_DIRECTORIES=os.path.join(REPO, ".git", "objects"),
                        PYTHONIOENCODING="utf-8")
        os.makedirs(os.path.join(root, "objects"))

    def git(self, *args, data=None):
        r = subprocess.run(["git", "-C", REPO] + list(args), input=data, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, env=self.env)
        if r.returncode != 0:
            raise RuntimeError("git %s: %s" % (" ".join(args), r.stderr.decode("utf-8", "replace")))
        return r.stdout.decode("utf-8", "replace").strip()

    def tree_of_worktree(self):
        self.git("read-tree", "HEAD")
        self.git("add", "-A", "--", *[p for p in SHIPPED if os.path.exists(os.path.join(REPO, p))])
        self.git("update-index", "--chmod=+x", "--", COMMAND)
        return self.git("write-tree")

    def with_file(self, path, data):
        """The current index with path replaced by data, as a tree."""
        blob = self.git("hash-object", "-w", "--stdin", data=data)
        self.git("update-index", "--cacheinfo", "100644,%s,%s" % (blob, path))
        return self.git("write-tree")

    def run(self, *args):
        r = subprocess.run([sys.executable] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           env=self.env)
        return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")


def files(root):
    out = {}
    for d, subdirs, names in os.walk(root):
        if d == root and "AppData" in subdirs:
            subdirs.remove("AppData")
        for s in subdirs:
            out[os.path.relpath(os.path.join(d, s), root).replace(os.sep, "/")] = None
        for n in names:
            p = os.path.join(d, n)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, root).replace(os.sep, "/")] = fh.read()
    return out


def repo_state():
    """What the tests must not change: the index's entries, HEAD, and what git status reports.
    GIT_OPTIONAL_LOCKS=0 keeps git status from refreshing the index file itself."""
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    out = []
    for args in (["ls-files", "-s"], ["rev-parse", "HEAD"], ["status", "--porcelain", "--untracked-files=all"]):
        out.append(subprocess.run(["git", "-C", REPO] + args, stdout=subprocess.PIPE, env=env).stdout)
    return out


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    if not shutil.which("git") or not os.path.isdir(os.path.join(REPO, ".git")):
        skip("every case", "needs git and a git checkout")
        return 0
    before = repo_state()
    root = tempfile.mkdtemp(prefix="gv release 王 ")
    try:
        scratch = Scratch(os.path.join(root, "git"))
        tree = scratch.tree_of_worktree()

        code, out = scratch.run(CHECK, tree)
        case("release_check: the working tree, as a tree, passes every check", code == 0, out[-800:])

        with open(os.path.join(REPO, "dist", "en", "gravitas", "README.md"), "rb") as fh:
            stale = scratch.with_file("dist/en/gravitas/README.md", fh.read() + b"\nstale\n")
        code, out = scratch.run(CHECK, stale)
        case("release_check: a dist/ that differs from a build of the commit's sources fails",
             code == 1 and "FAIL dist/ in the commit" in out, out[-600:])

        scratch.git("read-tree", tree)
        with open(os.path.join(REPO, "README.md"), "rb") as fh:
            readme = fh.read()
        wrong = scratch.with_file("README.md", readme + b"\n[Download](https://github.com/Emily2040/gravitas"
                                  b"/archive/refs/tags/v0.0.1.zip)\n")
        code, out = scratch.run(CHECK, wrong)
        case("release_check: a README link to another version's download fails",
             code == 1 and re.search(r"FAIL every versioned download link.*README\.md links v0\.0\.1", out),
             out[-600:])

        zpath = os.path.join(root, "Gravitas.zip")
        code, out = scratch.run(ZIPPER, zpath, tree)
        if code != 0:
            case("build_release_zip: makes Gravitas.zip", False, out[-600:])
            return 1
        with zipfile.ZipFile(zpath) as z:
            infos = {i.filename: i for i in z.infolist()}
            top = sorted({n.split("/")[0] for n in infos})
            sh, cmd = z.read(COMMAND), z.read(CMD)
            dist = {n[len("dist/"):]: z.read(n) for n in infos if n.startswith("dist/") and not n.endswith("/")}
        case("build_release_zip: the ZIP holds the two installers, LICENSE and dist/ at its top level, "
             "and nothing else", top == sorted([CMD, COMMAND, "LICENSE", "dist"]), repr(top))
        mode = infos[COMMAND].external_attr >> 16
        case("build_release_zip: the .command is marked as a Unix file with mode 755, LF only; the .cmd is "
             "CRLF only",
             infos[COMMAND].create_system == 3 and stat.S_ISREG(mode) and mode & 0o777 == 0o755
             and b"\r" not in sh and cmd.count(b"\n") == cmd.count(b"\r\n"), "mode %o" % mode)
        want = {k: v for k, v in files(os.path.join(REPO, "dist")).items() if v is not None}
        case("build_release_zip: dist/ in the ZIP is byte for byte the dist/ in the working tree",
             dist == want, "%d in the ZIP, %d in dist/" % (len(dist), len(want)))

        # Unzip as Extract All does, into a folder named after the ZIP inside a second download's folder.
        unzipped = os.path.join(root, "Downloads 王 é & (1)", "Gravitas")
        with zipfile.ZipFile(zpath) as z:
            z.extractall(unzipped)
        home = os.path.join(root, "home 王小明 & é!")
        ref = os.path.join(root, "reference home")
        os.makedirs(home)
        os.makedirs(ref)
        env = dict(os.environ, USERPROFILE=ref, HOME=ref, PYTHONIOENCODING="utf-8")
        subprocess.run([sys.executable, INSTALL, "ja"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        env = dict(os.environ, USERPROFILE=home, HOME=home, GRAVITAS_LANG="en")
        if os.name == "nt":
            r = subprocess.run('cmd /d /s /c ""%s""' % os.path.join(unzipped, CMD), input=b"3\r\n",
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
            kind = CMD
        else:
            r = subprocess.run(["/bin/bash", os.path.join(unzipped, COMMAND)], input=b"3\n",
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
            kind = COMMAND
        same = files(home) == files(ref)
        case("build_release_zip: unzipped, %s installs Japanese exactly as install.py ja does" % kind,
             r.returncode == 0 and same, r.stdout.decode("utf-8", "replace")[-400:])
    finally:
        shutil.rmtree(root, ignore_errors=True)
        after = repo_state()
        case("the repository's index, HEAD and status are as they were", after == before)

    failed = RESULTS.count(False)
    print("%d/%d passed" % (len(RESULTS) - failed, len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
