#!/usr/bin/env python3
"""Make Gravitas.zip, the download for people who have never installed anything.

    python scripts/build_release_zip.py OUT.zip          # from HEAD
    python scripts/build_release_zip.py OUT.zip REF      # from any commit or tree

The ZIP holds, at its top level and nothing else: Install Gravitas (Windows).cmd,
Install Gravitas (Mac).command, LICENSE and dist/. Everything comes from REF
through git archive, so it is exactly what is committed, with the line endings
.gitattributes gives: CRLF for the .cmd, LF for the rest. The .command keeps mode
755 and the ZIP marks its entries as made on Unix, so Archive Utility unzips it
ready to run. Windows' Extract All and the Mac's Archive Utility both unzip it
into one folder named after the ZIP, so the person opens that folder and finds
the two installers, with no other folder to open first.

Run scripts/release_check.py first, then attach the file to the GitHub release
under the name Gravitas.zip. When that release is marked Latest, this link always
downloads the newest one:

    https://github.com/Emily2040/gravitas/releases/latest/download/Gravitas.zip
"""
import io
import os
import stat
import subprocess
import sys
import tarfile
import time
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENTS = ["Install Gravitas (Windows).cmd", "Install Gravitas (Mac).command", "LICENSE", "dist"]


def entries(ref):
    """(name, mode, mtime, bytes or None for a folder) for every path in CONTENTS at ref."""
    r = subprocess.run(["git", "-C", REPO, "-c", "core.autocrlf=false", "archive", "--format=tar", ref, "--"]
                       + CONTENTS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        sys.exit("git archive %s failed: %s" % (ref, r.stderr.decode("utf-8", "replace").strip()))
    out = []
    with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tar:
        for m in tar.getmembers():
            if m.isdir():
                out.append((m.name.rstrip("/") + "/", m.mode, m.mtime, None))
            elif m.isfile():
                out.append((m.name, m.mode, m.mtime, tar.extractfile(m).read()))
    return out


def write_zip(path, items):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, mode, mtime, data in items:
            info = zipfile.ZipInfo(name, date_time=max(time.gmtime(mtime)[:6], (1980, 1, 1, 0, 0, 0)))
            info.create_system = 3  # Unix, so the permission bits below are read
            if data is None:
                info.external_attr = ((stat.S_IFDIR | 0o755) << 16) | 0x10
                z.writestr(info, b"")
            else:
                info.external_attr = (stat.S_IFREG | (0o755 if mode & 0o111 else 0o644)) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, data)


def main(argv):
    if not argv or len(argv) > 2 or any(a.startswith("-") for a in argv):
        sys.exit("usage: build_release_zip.py OUT.zip [REF]")
    out = os.path.abspath(argv[0])
    ref = argv[1] if len(argv) > 1 else "HEAD"
    items = entries(ref)
    names = {n for n, _, _, _ in items}
    missing = [c for c in CONTENTS if c not in names and c + "/" not in names]
    if missing:
        sys.exit("%s does not hold %s; nothing was written" % (ref, ", ".join(missing)))
    write_zip(out, items)
    print("wrote %s from %s: %d files" % (out, ref, sum(1 for i in items if i[3] is not None)))


if __name__ == "__main__":
    main(sys.argv[1:])
