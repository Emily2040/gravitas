#!/usr/bin/env python3
"""Check that a commit is ready to release. Run it before tagging and publishing.

    python scripts/release_check.py        # HEAD, and nothing shipped is left uncommitted
    python scripts/release_check.py REF    # any commit or tree; skips the uncommitted check

A download from GitHub, whether "Source code (zip)" or the Gravitas.zip that
scripts/build_release_zip.py makes, holds what is committed, not what is in the
working tree. tests/scripts/test_build_dist.py compares dist/ with a fresh build
in the working tree. This checks the commit:

1. For HEAD, nothing a download ships has uncommitted or untracked changes: dist,
   plugin, locales, scripts, the three installers, .gitattributes,
   LICENSE, the READMEs, and what the READMEs link to or tell people to run:
   docs, tests, CHANGELOG.md and TESTS.md. A plugin file committed without a
   rebuilt and committed dist/ would reach people who use install.py and not
   people who double-click, and an example left untracked is a dead link on
   GitHub.
2. dist/ in the commit is exactly what scripts/build_dist.py builds from the
   commit's own plugin/ and locales/.
3. In the commit, Install Gravitas (Mac).command and Install Gravitas (Linux).sh
   have mode 100755 and LF line endings, and Install Gravitas (Windows).cmd comes
   out with CRLF line endings,
   as GitHub's own ZIP gives them.
4. Every download link in the READMEs that names a version names the version in
   plugin/plugin.json.

Each check prints PASS or FAIL; the exit status is 1 if any fails.
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CMD = "Install Gravitas (Windows).cmd"
COMMAND = "Install Gravitas (Mac).command"
SH = "Install Gravitas (Linux).sh"
SHIPPED = ["dist", "plugin", "locales", "scripts", CMD, COMMAND, SH, ".gitattributes", "LICENSE",
           "README.md", "README.zh-CN.md", "README.ja.md", "README.ko.md",
           "docs", "tests", "CHANGELOG.md", "TESTS.md"]
# Links that pin a version: a tag's source archive, a release page, or a release asset.
VERSIONED = re.compile(r"github\.com/Emily2040/gravitas/(?:archive/refs/tags/v([^/\s)\"']+?)\.(?:zip|tar\.gz)"
                       r"|releases/(?:tag|download)/v([^/\s)\"']+))")

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


def git(*args, binary=False):
    r = subprocess.run(["git", "-C", REPO, "-c", "core.autocrlf=false", "-c", "core.quotepath=off"] + list(args),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), r.stderr.decode("utf-8", "replace").strip()))
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def archive(ref, dest):
    """Extract the shipped paths of ref into dest, as git archive gives them. Returns {path: bytes}."""
    data = git("archive", "--format=tar", ref, "--", *[p for p in SHIPPED if exists(ref, p)], binary=True)
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for m in tar.getmembers():
            if m.isfile():
                files[m.name] = tar.extractfile(m).read()
                path = os.path.join(dest, *m.name.split("/"))
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(files[m.name])
    return files


def exists(ref, path):
    return bool(git("ls-tree", "--name-only", ref, "--", path).strip())


def tree(root):
    out = {}
    for d, _, names in os.walk(root):
        for n in names:
            p = os.path.join(d, n)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, root).replace(os.sep, "/")] = fh.read()
    return out


def main(argv):
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    if len(argv) > 1 or any(a.startswith("-") for a in argv):
        sys.exit("usage: release_check.py [REF]")
    if not shutil.which("git"):
        sys.exit("git is not installed")
    ref = argv[0] if argv else "HEAD"
    print("checking %s" % ref)

    if not argv:
        status = git("status", "--porcelain", "--untracked-files=all", "--", *SHIPPED)
        lines = [l for l in status.splitlines() if l.strip()]
        check("everything a download ships is committed", not lines,
              "; ".join(lines[:8]) + ("; and %d more" % (len(lines) - 8) if len(lines) > 8 else ""))

    tmp = tempfile.mkdtemp(prefix="gravitas release ")
    try:
        files = archive(ref, os.path.join(tmp, "repo"))
        fresh = os.path.join(tmp, "fresh")
        build = os.path.join(tmp, "repo", "scripts", "build_dist.py")
        if not os.path.isfile(build) or "dist/en/gravitas/plugin.json" not in files:
            check("the commit holds scripts/build_dist.py and dist/", False)
        else:
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
            r = subprocess.run([sys.executable, build, fresh], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               env=env)
            want = tree(fresh) if r.returncode == 0 else {}
            got = {k[len("dist/"):]: v for k, v in files.items() if k.startswith("dist/")}
            diff = (["missing " + k for k in sorted(set(want) - set(got))]
                    + ["extra " + k for k in sorted(set(got) - set(want))]
                    + ["differs " + k for k in sorted(set(want) & set(got)) if want[k] != got[k]])
            check("dist/ in the commit is what build_dist.py builds from the commit's plugin/ and locales/",
                  r.returncode == 0 and not diff,
                  "; ".join(diff[:8]) or r.stdout.decode("utf-8", "replace")[-400:])

        for name in (COMMAND, SH):
            mode = git("ls-tree", ref, "--", name).split(" ")[0]
            sh = files.get(name, b"")
            check("%s has mode 100755 and LF line endings" % name,
                  mode == "100755" and sh.startswith(b"#!/bin/bash\n") and b"\r" not in sh, "mode %r" % mode)
        cmd = files.get(CMD, b"")
        check("%s has CRLF line endings" % CMD,
              bool(cmd) and cmd.count(b"\n") == cmd.count(b"\r\n"), "%d LF, %d CRLF"
              % (cmd.count(b"\n"), cmd.count(b"\r\n")))

        try:
            version = json.loads(files["plugin/plugin.json"].decode("utf-8"))["version"]
        except (KeyError, ValueError) as exc:
            check("plugin/plugin.json has a version", False, repr(exc))
        else:
            wrong = []
            for name, data in sorted(files.items()):
                if re.match(r"^README(\.[A-Za-z-]+)?\.md$", name):
                    for m in VERSIONED.finditer(data.decode("utf-8", "replace")):
                        found = m.group(1) or m.group(2)
                        if found != version:
                            wrong.append("%s links v%s" % (name, found))
            check("every versioned download link in the READMEs names v%s, the version in plugin.json"
                  % version, not wrong, "; ".join(wrong[:8]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = RESULTS.count(False)
    print("%d/%d passed" % (len(RESULTS) - failed, len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
