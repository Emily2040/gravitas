#!/usr/bin/env python3
"""Tests for the double-click installers, Install Gravitas (Windows).cmd and Install Gravitas (Mac).command.

Run with plain `python tests/scripts/test_installers.py`. Each case prints one
PASS, FAIL or SKIP line; the exit status is 1 if any case fails.

Everything runs in throwaway folders. The installer and a copy of dist/ go in a
folder whose path holds a space, brackets and non-ASCII letters, the way a
second download unzips, and every run gets a new home folder whose name adds an
ampersand and an exclamation mark. USERPROFILE and HOME point at that folder, so
the real ~/.gemini is never touched. Each result is compared byte for byte with
what `python scripts/install.py <lang>` does in another throwaway home.

The choice goes in through a pipe. Under chcp 65001, cmd's set /p reads only the
first line of a pipe and nothing at all from a redirected file, so every .cmd
case sends one line. At the end of the pipe set /p returns empty, exactly as it
does for Enter alone, so the .cmd takes the default there; a person typing in
the window is asked again after a wrong answer every time. pause returns at
once. The .cmd cases run on Windows. The .command cases run where bash is found:
/bin/bash, or the bash.exe of Git for Windows, since WSL's bash cannot see a
Windows home folder. Git Bash has no osascript, so there the .command reports a
beta 1 hook instead of removing it, as it does on a Mac where osascript fails;
the JavaScript it would run is checked with Node instead, when Node is found.
"""
import ctypes
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CMD_NAME = "Install Gravitas (Windows).cmd"
COMMAND_NAME = "Install Gravitas (Mac).command"
CMD = os.path.join(REPO, CMD_NAME)
COMMAND = os.path.join(REPO, COMMAND_NAME)
INSTALL = os.path.join(REPO, "scripts", "install.py")
DIST = os.path.join(REPO, "dist")
LANGS = ("en", "zh-CN", "ja", "ko")
STAMP = re.compile(r"^\d{8}-\d{6}(-\d+)?$")
# The first line of a successful install, and of a removal, in each language. Both installers share them.
INSTALLED = {"en": "Done. Gravitas is installed in:",
             "zh-CN": "完成，Gravitas 已安装到：",
             "ja": "完了しました。Gravitas を次の場所にインストールしました。",
             "ko": "완료되었습니다. Gravitas가 다음 위치에 설치되었습니다."}
REMOVED = "Done. Gravitas is removed from Antigravity. Its files were moved to:"
# How each installer says to quit Antigravity: from the icon by the clock, or in the menu bar.
QUIT = {"cmd": "Right-click the icon and choose Quit.",
        "command": "click its icon in the menu bar at the top right of the screen and choose Quit"}
MENU = ["1  Install Gravitas in English", "2  安装 Gravitas（简体中文版）",
        "3  日本語版の Gravitas をインストール", "4  한국어판 Gravitas 설치"]
BAD = "Please type a number from 1 to 5."
HOOK_KEY = "gravitas-always-on"
BETA1_HOOKS = ('{\n  "gravitas-always-on": {"PreInvocation": [{"command": "python ~/.gemini/config/scripts/'
               'gravitas_always_on.py", "timeout": 5}]},\n  "mine": {"PostInvocation": [{"command": '
               '"echo caf\u00e9 \u738b"}]}\n}\n').encode("utf-8")

RESULTS = []


def case(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


def skip(name, why):
    print("SKIP %s  -- %s" % (name, why))


def tree(root):
    """{relative path: bytes, or None for a folder} for everything under root.

    A home folder's AppData is left out: Windows PowerShell 5.1, which the .cmd runs for the display
    language, creates AppData\\Roaming under a redirected USERPROFILE. A real profile already has it.
    """
    out = {}
    if not os.path.isdir(root):
        return out
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


def stamped(t):
    """The tree with every backup folder's name replaced by <stamp>, so two homes can be compared."""
    return {re.sub(r"^\.gemini/gravitas-backups/[^/]+", ".gemini/gravitas-backups/<stamp>", k): v
            for k, v in t.items()}


def differences(want, got, normalise=False):
    a, b = tree(want), tree(got)
    if normalise:
        a, b = stamped(a), stamped(b)
    out = ["missing " + k for k in sorted(set(a) - set(b))]
    out += ["extra " + k for k in sorted(set(b) - set(a))]
    out += ["differs " + k for k in sorted(set(a) & set(b)) if a[k] != b[k]]
    return out


def brief(lines, n=10):
    return "; ".join(lines[:n]) + ("; and %d more" % (len(lines) - n) if len(lines) > n else "")


def find_bash():
    if os.name != "nt":
        return "/bin/bash" if os.path.exists("/bin/bash") else shutil.which("bash")
    for base in (os.environ.get("ProgramW6432"), os.environ.get("ProgramFiles"),
                 os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs")):
        if base and os.path.isfile(os.path.join(base, "Git", "bin", "bash.exe")):
            return os.path.join(base, "Git", "bin", "bash.exe")
    return None


def install_py(home, *args):
    env = dict(os.environ, USERPROFILE=home, HOME=home, PYTHONIOENCODING="utf-8")
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    r = subprocess.run([sys.executable, INSTALL] + list(args), stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, env=env)
    return r.returncode, r.stdout.decode("utf-8", "replace")


class Held:
    """A file held open the way another program holds it, for the tests that need one (Windows only).
    share=0 is a virus scanner's exclusive hold; the default is a program that lets others read and
    write but not delete or rename, as a running app does."""

    def __init__(self, path, share=3):
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateFileW.restype = ctypes.c_void_p
        self.k32 = k32
        self.h = k32.CreateFileW(path, 0x80000000, share, None, 3, 0, None)  # GENERIC_READ, OPEN_EXISTING
        if self.h in (None, ctypes.c_void_p(-1).value):
            raise OSError("could not open %s: %d" % (path, ctypes.get_last_error()))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.k32.CloseHandle(ctypes.c_void_p(self.h))


def my_sid():
    r = subprocess.run(["whoami", "/user", "/fo", "csv", "/nh"], stdout=subprocess.PIPE)
    return r.stdout.decode("ascii", "replace").strip().split(",")[-1].strip('"')


class Lab:
    """Throwaway folders: an unzipped download, reference installs, and fresh homes."""

    def __init__(self, root):
        self.root = root
        self.download = self.unzipped("Gravitas (1) 王")
        self.n = 0
        self.ref = {}
        for lang in LANGS:
            home = self.home("ref " + lang)
            code, out = install_py(home, lang)
            if code != 0:
                raise SystemExit("install.py %s failed:\n%s" % (lang, out))
            self.ref[lang] = home

    def unzipped(self, name, langs=LANGS):
        """A folder holding both installers and dist/ for the languages given, as the ZIP unpacks."""
        path = os.path.join(self.root, name)
        for lang in langs:
            shutil.copytree(os.path.join(DIST, lang), os.path.join(path, "dist", lang))
        for f in (CMD, COMMAND):
            shutil.copy2(f, path)
        return path

    def home(self, label="home"):
        self.n += 1
        path = os.path.join(self.root, "%s %d 王小明 & é!" % (label, self.n))
        os.makedirs(path)
        return path

    def command(self, kind, home, ui="en", where=None, env=None):
        """The command line, input encoder and environment for one installer run."""
        where = where or self.download
        env = dict(os.environ if env is None else env, USERPROFILE=home, HOME=home)
        if ui is None:
            env.pop("GRAVITAS_LANG", None)
        else:
            env["GRAVITAS_LANG"] = ui
        if kind == "cmd":
            return 'cmd /d /s /c ""%s""' % os.path.join(where, CMD_NAME), env
        env["LANG"] = "en_US.UTF-8"
        return [BASH, os.path.join(where, COMMAND_NAME)], env

    def run(self, kind, home, answer, ui="en", where=None, raw=False, env=None):
        """Run one installer with the answer piped in. Returns (exit code, output).

        Without raw, a line ending is added to the answer as Enter or Return would."""
        line, env = self.command(kind, home, ui, where, env)
        data = answer if raw else answer + ("\r\n" if kind == "cmd" else "\n")
        r = subprocess.run(line, input=data.encode("utf-8"), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env=env)
        return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")


def plugin(home):
    return os.path.join(home, ".gemini", "config", "plugins", "gravitas")


def shows(out, path, kind):
    """Whether the output names path. Git Bash prints a Windows path in its own form, /c/Users/...
    or /tmp/..., so for the .command only the last four parts are compared."""
    if kind == "cmd" or os.name != "nt":
        return path in out
    return "/".join(path.replace("\\", "/").split("/")[-4:]) in out


def display_language():
    """The language the .cmd's registry fallback reads, as one of LANGS."""
    import winreg
    for key, name in ((r"Control Panel\Desktop", "PreferredUILanguages"),
                      (r"Control Panel\Desktop\MuiCached", "MachinePreferredUILanguages")):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
                value = winreg.QueryValueEx(k, name)[0]
        except OSError:
            continue
        first = (value[0] if isinstance(value, list) and value else str(value)).lower()
        return {"zh": "zh-CN", "ja": "ja", "ko": "ko"}.get(first[:2], "en")
    return "en"


def backups(home):
    root = os.path.join(home, ".gemini", "gravitas-backups")
    return [os.path.join(root, d) for d in sorted(os.listdir(root))] if os.path.isdir(root) else []


def beta1(home, hooks=BETA1_HOOKS):
    """What Gravitas beta 1 left in a home: the bare skill, the hook script, and the hook entry."""
    config = os.path.join(home, ".gemini", "config")
    os.makedirs(os.path.join(config, "skills", "gravitas"))
    with open(os.path.join(config, "skills", "gravitas", "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("---\nname: gravitas\ndescription: beta 1\n---\n")
    os.makedirs(os.path.join(config, "scripts"))
    with open(os.path.join(config, "scripts", "gravitas_always_on.py"), "w", encoding="utf-8") as fh:
        fh.write("print('Load the gravitas skill')\n")
    with open(os.path.join(config, "hooks.json"), "wb") as fh:
        fh.write(hooks)


def python_hook_edit(raw):
    """What install.py writes for a hooks.json, or None when it leaves the file alone."""
    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except ValueError:
        return None
    if not isinstance(data, dict) or HOOK_KEY not in data:
        return None
    del data[HOOK_KEY]
    return (json.dumps(data, indent=2) + "\n").encode("utf-8")


HOOK_FIXTURES = {
    "beta 1 entry beside the person's own hook": BETA1_HOOKS,
    "the only entry": b'{"gravitas-always-on": {}}',
    "a byte order mark": b'\xef\xbb\xbf{"a": 1, "gravitas-always-on": [], "b": "x"}',
    "escapes, non-ASCII, nesting and numbers": json.dumps(
        {"z": {"s": "caf\u00e9 \u738b \U0001F600 \"q\" \\ \n\t\r\b\f \x01 \x7f \u2028",
               "n": [1, -2, 12345678901, True, False, None, [], {}, [[]]],
               "e": {}}, HOOK_KEY: {"x": 1}, "k\u00e9y": "v"}, ensure_ascii=False).encode("utf-8"),
    "the name only inside a string": b'{"other": "mentions gravitas-always-on"}',
    "a file that does not parse": b'{"gravitas-always-on": {}, ',
    "a list, not an object": b'[{"gravitas-always-on": 1}]',
}
# Python writes 1.0 and 1e-07, and keeps every digit of a whole number. JavaScript keeps no difference
# between 1.0 and 1, writes 1e-7, and rounds whole numbers past 2**53. Nobody writes such numbers in
# hooks.json, so only the PowerShell check, which matches Python here too, includes them.
NUMBERS = json.dumps({"f": [1.5, 1.0, 0.1, 1e-07, 2.5e+20, 99999999999999999999], HOOK_KEY: 1}).encode("utf-8")


def static_checks():
    with open(CMD, "rb") as fh:
        cmd = fh.read()
    head = cmd.split(b"chcp 65001")[0]
    case("static: %s has CRLF line endings only, no byte order mark, and only ASCII before chcp 65001"
         % CMD_NAME,
         cmd.count(b"\n") == cmd.count(b"\r\n") and not cmd.startswith(b"\xef\xbb\xbf")
         and b"chcp 65001" in cmd and all(c < 128 for c in head))
    with open(COMMAND, "rb") as fh:
        sh = fh.read()
    case("static: %s starts with #!/bin/bash and has LF line endings, no byte order mark" % COMMAND_NAME,
         sh.startswith(b"#!/bin/bash\n") and b"\r" not in sh)
    cmd_t, sh_t = cmd.decode("utf-8"), sh.decode("utf-8")
    with open(INSTALL, encoding="utf-8") as fh:
        py = fh.read()
    case("static: install.py and both installers back up into ~/.gemini/gravitas-backups, and name the "
         "old skill skills-gravitas",
         '"gravitas-backups"' in py and "skills-gravitas" in py
         and "\\gravitas-backups" in cmd_t and "skills-gravitas" in cmd_t
         and "/gravitas-backups" in sh_t and "skills-gravitas" in sh_t)
    case("static: both installers offer the same four languages",
         all(m in cmd_t and m in sh_t for m in MENU)
         and all(('LANGDIR=%s"' % l in cmd_t or l == "en") and "LANGDIR=%s ;;" % l in sh_t for l in LANGS))
    cmd_blocks = {l: re.search(r"^:text_%s\r?\n(.*?)^exit /b 0" % re.escape(l), cmd_t, re.M | re.S)
                  for l in LANGS}
    for name, text, blocks in (
            ("cmd", cmd_t, cmd_blocks),
            ("command", sh_t, {l: re.search(r"^  %s\)\n(.*?)^    ;;" % re.escape(l), sh_t, re.M | re.S)
                               for l in LANGS})):
        keys = {l: set(re.findall(r"(M_[A-Z0-9]+)=", m.group(1))) if m else set() for l, m in blocks.items()}
        used = set(re.findall(r"(?:call :say |\$|%|\")(M_[A-Z0-9]+)", text))
        case("static: every language in the %s installer sets the same messages, and every message "
             "used is set" % name,
             bool(keys["en"]) and all(keys[l] == keys["en"] for l in LANGS) and used <= keys["en"],
             "; ".join("%s lacks %s" % (l, sorted(keys["en"] - keys[l])) for l in LANGS if keys[l] != keys["en"])
             + (" unset: %s" % sorted(used - keys["en"]) if used - keys["en"] else ""))
    unsafe = [line for m in cmd_blocks.values() if m for line in m.group(1).splitlines()
              if line.startswith('set "') and ('"' in line[5:-1] or "%" in line.replace("%DEF%", ""))]
    case("static: no cmd message holds a straight double quote or a percent sign, which cmd would act on",
         not unsafe, brief(unsafe, 3))
    git = shutil.which("git")
    if not git or subprocess.run([git, "-C", REPO, "rev-parse"], stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL).returncode != 0:
        skip("static: git modes and line endings", "not a git checkout")
        return
    r = subprocess.run([git, "-C", REPO, "ls-files", "-s", "--", COMMAND_NAME], stdout=subprocess.PIPE)
    case("static: %s is in git with mode 100755, so it unzips executable on a Mac" % COMMAND_NAME,
         r.stdout.decode().startswith("100755 "), r.stdout.decode().strip() or "not in the index")
    r = subprocess.run([git, "-C", REPO, "check-attr", "eol", "--", CMD_NAME, COMMAND_NAME], stdout=subprocess.PIPE)
    attrs = r.stdout.decode("utf-8", "replace")
    case("static: .gitattributes gives the .cmd CRLF and the .command LF in every checkout and archive",
         "%s: eol: crlf" % CMD_NAME in attrs and "%s: eol: lf" % COMMAND_NAME in attrs, attrs.strip())


def hook_code_checks(lab):
    """The code that edits hooks.json, run on its own against what install.py writes."""
    if os.name == "nt":
        ps = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "WindowsPowerShell",
                          "v1.0", "powershell.exe")
        bad = []
        for i, (name, raw) in enumerate(list(HOOK_FIXTURES.items()) + [("numbers", NUMBERS)]):
            d = os.path.join(lab.root, "ps hook %d é&" % i)
            os.makedirs(os.path.join(d, "backup"))
            path = os.path.join(d, "hooks.json")
            with open(path, "wb") as fh:
                fh.write(raw)
            env = dict(os.environ, GV_SELF=CMD, GV_HOOKS=path, GV_BACKUP=os.path.join(d, "backup"))
            r = subprocess.run([ps, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command",
                                "$t = [IO.File]::ReadAllText($env:GV_SELF); & ([ScriptBlock]::Create("
                                "$t.Substring($t.LastIndexOf('#GRAVITAS' + '-POWERSHELL'))))"],
                               env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            with open(path, "rb") as fh:
                got = fh.read()
            want = python_hook_edit(raw)
            copy = os.path.join(d, "backup", "hooks.json")
            ok = (r.returncode == 0 and got == want and open(copy, "rb").read() == raw) if want else \
                (r.returncode != 0 and got == raw and not os.path.exists(copy))
            ok = ok and sorted(os.listdir(d)) == ["backup", "hooks.json"]
            if not ok:
                bad.append("%s (exit %d): %r" % (name, r.returncode, got[:200]))
        case("hook: the .cmd's PowerShell writes hooks.json byte for byte as install.py does, keeps a copy, "
             "and leaves a file it cannot handle unchanged (%d files)" % (len(HOOK_FIXTURES) + 1),
             not bad, brief(bad, 3))
    else:
        skip("hook: the .cmd's PowerShell", "Windows only")

    node = shutil.which("node")
    if not node:
        skip("hook: the .command's JavaScript", "Node is not installed")
        return
    with open(COMMAND, encoding="utf-8") as fh:
        js = re.search(r"<<'JS'\n(.*?)\nJS\n", fh.read(), re.S)
    if not js:
        case("hook: the .command holds its JavaScript between <<'JS' and JS", False)
        return
    # Node stands in for the two Foundation calls the script makes; everything else is the script.
    shim = ('const fs = require("fs");\n'
            'const ObjC = { import() {}, unwrap(x) { return x; } };\n'
            'function $(s) { return { writeToFileAtomicallyEncodingError(p) {\n'
            '  fs.writeFileSync(p + ".tmp", s, "utf8"); fs.renameSync(p + ".tmp", p); return true; } }; }\n'
            '$.NSUTF8StringEncoding = 4;\n'
            '$.NSString = { stringWithContentsOfFileEncodingError(p) {\n'
            '  try { return new TextDecoder("utf-8", {fatal: true}).decode(fs.readFileSync(p)); }\n'
            '  catch (e) { return undefined; } } };\n')
    runner = ('\ntry { process.stdout.write(String(run([process.argv[2]]))); }\n'
              'catch (e) { process.stderr.write(String(e)); process.exit(1); }\n')
    prog = os.path.join(lab.root, "hook.js")
    with open(prog, "w", encoding="utf-8") as fh:
        fh.write(shim + js.group(1) + runner)
    bad = []
    for i, (name, raw) in enumerate(HOOK_FIXTURES.items()):
        path = os.path.join(lab.root, "js hook %d é&.json" % i)
        with open(path, "wb") as fh:
            fh.write(raw)
        r = subprocess.run([node, prog, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(path, "rb") as fh:
            got = fh.read()
        want = python_hook_edit(raw)
        said = r.stdout.decode("utf-8", "replace")
        ok = (said == "removed" and got == want) if want else (got == raw and said != "removed")
        if not ok:
            bad.append("%s: said %r, wrote %r" % (name, said, got[:200]))
    case("hook: the .command's JavaScript writes hooks.json byte for byte as install.py does, and leaves "
         "a file it cannot handle unchanged (%d files, run in Node)" % len(HOOK_FIXTURES), not bad, brief(bad, 3))


def behaviour(lab, kind):
    p = "%s:" % kind
    can_edit_hooks = kind == "cmd" or bool(shutil.which("osascript"))

    # Each language, chosen by number, installs what install.py installs, and nothing else.
    for n, lang in enumerate(LANGS, 1):
        home = lab.home()
        code, out = lab.run(kind, home, str(n))
        diff = differences(lab.ref[lang], home)
        case("%s choice %d installs %s: the home folder matches install.py %s byte for byte, and it says "
             "where Gravitas is and how to restart Antigravity" % (p, n, lang, lang),
             code == 0 and not diff and INSTALLED[lang] in out and shows(out, plugin(home), kind)
             and "Quit" in out, brief(diff) or out[-600:])

    # Enter alone takes the default, which GRAVITAS_LANG stands in for the display language.
    for lang in ("ko", "zh-CN"):
        home = lab.home()
        code, out = lab.run(kind, home, "", ui=lang)
        diff = differences(lab.ref[lang], home)
        case("%s Enter alone installs the display language's default (%s), and the prompt is in %s"
             % (p, lang, lang),
             code == 0 and not diff and INSTALLED[lang] in out
             and ("(4번이 선택됩니다)" in out if lang == "ko" else "（会选 2）" in out),
             brief(diff) or out[-600:])
    if kind == "cmd":
        r = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            "[Globalization.CultureInfo]::CurrentUICulture.Name"],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        culture = r.stdout.decode("ascii", "replace").strip()
        want = {"zh": "zh-CN", "ja": "ja", "ko": "ko"}.get(culture[:2].lower(), "en")
        home = lab.home()
        code, out = lab.run(kind, home, "", ui=None)
        diff = differences(lab.ref[want], home)
        case("%s with no GRAVITAS_LANG, Enter alone follows the Windows display language (%s, so %s)"
             % (p, culture or "unknown", want), code == 0 and not diff, brief(diff) or out[-600:])

    # The installed menu text and the first screen.
    home = lab.home()
    code, out = lab.run(kind, home, "1")
    first = out.split("> ")[0]
    case("%s the first screen gives the promise, the menu and how to stop, before any folder path" % p,
         "Nothing else on this" in first and all(m in first for m in MENU) and "close this window" in first
         and ".gemini" not in first, first[-600:])

    # Full-width digits, as a CJK input method types them.
    home = lab.home()
    code, out = lab.run(kind, home, "３")
    case("%s a full-width 3 picks Japanese" % p, code == 0 and not differences(lab.ref["ja"], home),
         out[-400:])

    if kind == "cmd":
        # set /p cannot tell the end of a pipe from Enter alone, so after a wrong answer the pipe's end
        # takes the default. In the window, a wrong answer is asked again every time.
        home = lab.home()
        code, out = lab.run(kind, home, "9")
        case("%s a number outside 1 to 5 is refused once; the end of the pipe then counts as Enter" % p,
             code == 0 and out.count(BAD) == 1 and not differences(lab.ref["en"], home), out[-600:])
    else:
        home = lab.home()
        code, out = lab.run(kind, home, "9\n1")
        case("%s a number outside 1 to 5 asks again" % p,
             code == 0 and out.count(BAD) == 1 and not differences(lab.ref["en"], home), out[-600:])
        home = lab.home()
        code, out = lab.run(kind, home, "x\n7\n4")
        case("%s two wrong answers, then 4, installs Korean" % p,
             code == 0 and out.count(BAD) == 2 and not differences(lab.ref["ko"], home), out[-600:])
        home = lab.home()
        code, out = lab.run(kind, home, "", raw=True)
        case("%s the end of input at the prompt (Control-D) stops, changes nothing and exits 1" % p,
             code == 1 and not tree(home) and "Stopped. Nothing was changed." in out, out[-400:])
        home = lab.home()
        code, out = lab.run(kind, home, "9\n", raw=True)
        case("%s a wrong answer and then the end of input stops without installing" % p,
             code == 1 and not tree(home) and out.count(BAD) == 1, out[-400:])
        home = lab.home()
        code, out = lab.run(kind, home, "3", raw=True)
        case("%s a last answer with no newline after it still counts" % p,
             code == 0 and not differences(lab.ref["ja"], home), out[-400:])

    # Reinstall over an earlier install and a beta 1 skill: both move into one dated backup.
    home = lab.home()
    lab.run(kind, home, "1")
    old_skill = os.path.join(home, ".gemini", "config", "skills", "gravitas")
    os.makedirs(old_skill)
    with open(os.path.join(old_skill, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("---\nname: gravitas\ndescription: beta 1\n---\n")
    code, out = lab.run(kind, home, "3")
    found = backups(home)
    moved = found[0] if len(found) == 1 else ""
    ok = (code == 0 and len(found) == 1 and STAMP.match(os.path.basename(moved))
          and sorted(os.listdir(moved)) == ["gravitas", "skills-gravitas"]
          and not differences(plugin(lab.ref["en"]), os.path.join(moved, "gravitas"))
          and os.path.isfile(os.path.join(moved, "skills-gravitas", "SKILL.md"))
          and not os.path.exists(old_skill)
          and not differences(plugin(lab.ref["ja"]), plugin(home))
          and shows(out, moved, kind) and INSTALLED["ja"] in out)
    case("%s reinstalling moves the old plugin and a beta 1 skill into one gravitas-backups/<date-time> "
         "folder, installs the new language and names the backup" % p, ok,
         "backups: %r; output: %s" % (found, out[-600:]))

    # Remove moves the plugin into a dated backup and says where.
    home = lab.home()
    lab.run(kind, home, "1")
    code, out = lab.run(kind, home, "5")
    found = backups(home)
    moved = os.path.join(found[0], "gravitas") if len(found) == 1 else ""
    case("%s Remove moves the plugin into gravitas-backups/<date-time>/gravitas, says so and says to "
         "restart" % p,
         code == 0 and not os.path.exists(plugin(home)) and len(found) == 1
         and STAMP.match(os.path.basename(found[0]))
         and not differences(plugin(lab.ref["en"]), moved) and shows(out, found[0], kind)
         and REMOVED in out and QUIT[kind] in out,
         "backups: %r; output: %s" % (found, out[-600:]))

    # Remove again: nothing installed, nothing changed.
    code, again = lab.run(kind, home, "5")
    case("%s Remove with nothing installed says so and creates no backup" % p,
         code == 0 and len(backups(home)) == 1 and "nothing to remove" in again, again[-400:])

    # Two installs in the same second still get separate backup folders.
    home = lab.home()
    lab.run(kind, home, "1")
    lab.run(kind, home, "2")
    lab.run(kind, home, "1")
    names = [os.path.basename(b) for b in backups(home)]
    case("%s each run that moves something gets its own backup folder" % p,
         len(names) == 2 and all(STAMP.match(n) for n in names), repr(names))

    # Started away from dist/, as when Explorer runs it straight from the ZIP.
    alone = os.path.join(lab.root, "only the installer %s" % kind)
    os.makedirs(alone, exist_ok=True)
    shutil.copy2(CMD if kind == "cmd" else COMMAND, alone)
    home = lab.home()
    code, out = lab.run(kind, home, "1", where=alone)
    case("%s started without dist/ beside it, it exits 1, changes nothing, says how to unzip and where "
         "to download all of Gravitas" % p,
         code == 1 and not tree(home) and "needs the rest of Gravitas next to it" in out
         and "github.com/Emily2040/gravitas/releases" in out
         and ("Extract all" in out if kind == "cmd" else "Downloads folder" in out), out[-500:])

    # A source download without dist/, and a dist/ missing the chosen language: incomplete.
    source = os.path.join(lab.root, "source only %s" % kind)
    os.makedirs(os.path.join(source, "plugin"), exist_ok=True)
    shutil.copy2(os.path.join(REPO, "plugin", "plugin.json"), os.path.join(source, "plugin"))
    shutil.copy2(CMD if kind == "cmd" else COMMAND, source)
    home = lab.home()
    code, out = lab.run(kind, home, "1", where=source)
    partial = lab.unzipped("no Korean %s" % kind, LANGS[:3])
    home2 = lab.home()
    code2, out2 = lab.run(kind, home2, "4", where=partial)
    case("%s a download without dist/, or without the chosen language, exits 1, changes nothing, says "
         "it is incomplete, in the language chosen, and where to download it again" % p,
         code == 1 and code2 == 1 and not tree(home) and not tree(home2)
         and "This download of Gravitas is incomplete" in out and "빠진 파일이 있어서" in out2
         and "github.com/Emily2040/gravitas/releases" in out2, (out + out2)[-600:])

    # Beta 1 in full beside an installed plugin: the whole home ends as install.py leaves it.
    home = lab.home()
    lab.run(kind, home, "1")
    beta1(home)
    want = lab.home("install.py beta 1")
    install_py(want, "en")
    beta1(want)
    install_py(want, "ko")
    code, out = lab.run(kind, home, "4")
    hooks = os.path.join(home, ".gemini", "config", "hooks.json")
    if can_edit_hooks:
        diff = differences(want, home, normalise=True)
        case("%s over beta 1 (skill, hook script and hook entry) and an earlier install, the whole home "
             "matches install.py's, and it says the hook is gone" % p,
             code == 0 and not diff and "gravitas-always-on" in out and "hooks.json" in out,
             brief(diff) or out[-600:])
    else:
        with open(hooks, "rb") as fh:
            same = fh.read() == BETA1_HOOKS
        script = os.path.join(home, ".gemini", "config", "scripts", "gravitas_always_on.py")
        found = backups(home)
        case("%s over beta 1 without osascript: the skill and old plugin move, the hook entry and its "
             "script stay, and the note names hooks.json" % p,
             code == 0 and same and os.path.isfile(script) and len(found) == 1
             and sorted(os.listdir(found[0])) == ["gravitas", "skills-gravitas"]
             and not differences(plugin(lab.ref["ko"]), plugin(home)) and shows(out, hooks, kind),
             out[-600:])

    # Only beta 1, then Remove: it is installed, so it is removed.
    home = lab.home()
    beta1(home)
    code, out = lab.run(kind, home, "5")
    want = lab.home("install.py beta 1 uninstall")
    beta1(want)
    install_py(want, "--uninstall")
    if can_edit_hooks:
        diff = differences(want, home, normalise=True)
        case("%s Remove with only beta 1 there removes it, and the home matches install.py --uninstall"
             % p, code == 0 and not diff and REMOVED in out and "nothing to remove" not in out,
             brief(diff) or out[-600:])
    else:
        found = backups(home)
        case("%s Remove with only beta 1 there moves its skill, says so, and names hooks.json in the "
             "note" % p,
             code == 0 and len(found) == 1 and os.listdir(found[0]) == ["skills-gravitas"]
             and REMOVED in out and shows(out, os.path.join(home, ".gemini", "config", "hooks.json"), kind),
             out[-600:])

    # A hooks.json that does not parse is left as it is, and so is the hook script.
    home = lab.home()
    beta1(home, b'{"gravitas-always-on": {}, ')
    code, out = lab.run(kind, home, "1")
    with open(os.path.join(home, ".gemini", "config", "hooks.json"), "rb") as fh:
        same = fh.read() == b'{"gravitas-always-on": {}, '
    script = os.path.join(home, ".gemini", "config", "scripts", "gravitas_always_on.py")
    case("%s a hooks.json that does not parse is left unchanged with its hook script, and the note "
         "names it" % p,
         code == 0 and same and os.path.isfile(script) and "could not be removed for you" in out, out[-500:])

    if os.name == "nt":
        failures(lab, kind)


def failures(lab, kind):
    """What a running Antigravity, a virus scanner or a locked-down folder does to an install."""
    p = "%s:" % kind
    # Antigravity running: it holds plugin.json open, so the installed folder cannot be moved.
    home = lab.home()
    lab.run(kind, home, "1")
    with Held(os.path.join(plugin(home), "plugin.json")):
        code, out = lab.run(kind, home, "1")
    stuck = "Antigravity is probably still running" if kind == "cmd" else "This folder could not be moved"
    case("%s with Antigravity holding the installed plugin, it exits 1, says why, and the old plugin and "
         "the rest of the home are as they were" % p,
         code == 1 and stuck in out and "nothing was changed" in out
         and not differences(lab.ref["en"], home), out[-600:])

    # A beta 1 skill moves only after the plugin has; when the plugin cannot move, both stay.
    home = lab.home()
    lab.run(kind, home, "1")
    os.makedirs(os.path.join(home, ".gemini", "config", "skills", "gravitas"))
    before = tree(home)
    with Held(os.path.join(plugin(home), "plugin.json")):
        code, out = lab.run(kind, home, "2")
    case("%s when the plugin cannot move, a beta 1 skill is not moved either" % p,
         code == 1 and tree(home) == before, out[-400:])

    # A virus scanner holding a file of the download: the copy fails before anything is moved.
    scanned = lab.unzipped("scanned %s" % kind)
    home = lab.home()
    lab.run(kind, home, "1")
    with Held(os.path.join(scanned, "dist", "en", "gravitas", "skills", "gravitas", "SKILL.md"), share=0):
        code, out = lab.run(kind, home, "1", where=scanned)
    case("%s when a file of the download cannot be read, it exits 1 and the installed plugin is untouched"
         % p, code == 1 and "Copying Gravitas failed" in out and not differences(lab.ref["en"], home),
         out[-400:])

    # A plugins folder this account cannot add to: found before anything is moved.
    home = lab.home()
    lab.run(kind, home, "1")
    plugins = os.path.dirname(plugin(home))
    sid = my_sid()
    subprocess.run(["icacls", plugins, "/deny", "*%s:(AD)" % sid], stdout=subprocess.DEVNULL)
    try:
        code, out = lab.run(kind, home, "1")
    finally:
        subprocess.run(["icacls", plugins, "/remove:d", "*%s" % sid], stdout=subprocess.DEVNULL)
    case("%s when the plugins folder cannot be added to, it exits 1, names the folder, and the old "
         "plugin is still installed" % p,
         code == 1 and "could not be put into this folder" in out and shows(out, plugins, kind)
         and not differences(lab.ref["en"], home), out[-500:])

    # A ZIP that was not unblocked: every unzipped file carries the download mark.
    marked = lab.unzipped("marked %s" % kind)
    for d, _, names in os.walk(os.path.join(marked, "dist")):
        for n in names:
            with open(os.path.join(d, n) + ":Zone.Identifier", "w") as fh:
                fh.write("[ZoneTransfer]\nZoneId=3\n")
    home = lab.home()
    code, out = lab.run(kind, home, "1", where=marked)
    carrying = []
    for d, _, names in os.walk(plugin(home)):
        for n in names:
            try:
                with open(os.path.join(d, n) + ":Zone.Identifier"):
                    carrying.append(n)
            except OSError:
                pass
    if kind == "cmd":
        case("%s files unzipped with the download mark are installed without it" % p,
             code == 0 and not carrying and not differences(lab.ref["en"], home), brief(carrying))
    else:
        skip("%s files unzipped with the download mark" % p,
             "the macOS mark is an extended attribute, which only a Mac has")

    # Two windows answering at the same moment, over an existing install.
    bad = []
    for trial in range(3):
        home = lab.home()
        lab.run(kind, home, "1")
        procs = []
        for _ in range(2):
            line, env = lab.command(kind, home)
            procs.append(subprocess.Popen(line, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT, env=env))
        threads = [threading.Thread(target=pr.communicate, args=(("1\r\n" if kind == "cmd" else "1\n").encode(),))
                   for pr in procs]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        codes = [pr.returncode for pr in procs]
        stray = [k for k in tree(home) if "gravitas-new" in k or k.startswith(".gemini/config/plugins/gravitas/gravitas")
                 or ".gravitas-test" in k]
        if 0 not in codes or differences(plugin(lab.ref["en"]), plugin(home)) or stray:
            bad.append("trial %d: exits %r, stray %r" % (trial, codes, stray[:3]))
    case("%s two runs at the same moment leave one whole plugin, never one inside another, and no "
         "temporary folder" % p, not bad, brief(bad, 3))


def without_powershell(lab):
    """The .cmd with PowerShell out of reach: it still installs, named and defaulted without it."""
    home = lab.home()
    root = os.path.join(lab.root, "no system root")
    os.makedirs(root, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if k.upper() != "SYSTEMROOT"}
    env["SYSTEMROOT"] = root
    lab.run("cmd", home, "1", env=env)
    code, out = lab.run("cmd", home, "1", env=env)
    names = [os.path.basename(b) for b in backups(home)]
    case("cmd: without PowerShell it still installs, and names the backup folder backup",
         code == 0 and names == ["backup"] and not differences(plugin(lab.ref["en"]), plugin(home))
         and not os.path.isdir(os.path.join(home, "AppData")), "%r %s" % (names, out[-300:]))
    home = lab.home()
    want = display_language()
    code, out = lab.run("cmd", home, "", ui=None, env=env)
    case("cmd: without PowerShell, Enter alone follows the display language in the registry (%s)" % want,
         code == 0 and not differences(lab.ref[want], home), out[-300:])


def shared(lab):
    """install.py and the double-click installers use one backup folder and the same moves."""
    home = lab.home()
    kind = "cmd" if os.name == "nt" else "command"
    lab.run(kind, home, "1")
    code, out = install_py(home, "--uninstall")
    found = backups(home)
    case("shared: install.py --uninstall moves a double-click install into the same "
         "gravitas-backups/<date-time> folder",
         code == 0 and len(found) == 1 and STAMP.match(os.path.basename(found[0]))
         and not differences(plugin(lab.ref["en"]), os.path.join(found[0], "gravitas")), out[-400:])

    home = lab.home()
    install_py(home, "en")
    note = os.path.join(plugin(home), "user-note.txt")
    with open(note, "w") as fh:
        fh.write("mine")
    code, out = install_py(home, "ko")
    found = backups(home)
    kept = os.path.join(found[0], "gravitas", "user-note.txt") if len(found) == 1 else ""
    case("shared: install.py keeps the plugin it replaces in gravitas-backups/<date-time>/gravitas, as the "
         "double-click installers do",
         code == 0 and kept and os.path.isfile(kept) and not differences(plugin(lab.ref["ko"]), plugin(home)),
         out[-400:])


BASH = find_bash()


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    static_checks()
    if not os.path.isfile(os.path.join(DIST, "en", "gravitas", "plugin.json")):
        case("dist/ is built", False, "run: python scripts/build_dist.py")
    else:
        root = tempfile.mkdtemp(prefix="gv installers 王 ")
        try:
            lab = Lab(root)
            hook_code_checks(lab)
            if os.name == "nt":
                behaviour(lab, "cmd")
                without_powershell(lab)
            else:
                skip("cmd: every case", "%s runs on Windows only" % CMD_NAME)
            if BASH:
                behaviour(lab, "command")
            else:
                skip("command: every case", "no bash found")
            shared(lab)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    failed = RESULTS.count(False)
    print("%d/%d passed" % (len(RESULTS) - failed, len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
