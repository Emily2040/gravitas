#!/usr/bin/env python3
"""The Antigravity update-check hook: plugin/hooks.json and the two scripts it runs.

    python tests/scripts/test_update_hook.py           # offline cases only
    python tests/scripts/test_update_hook.py --live    # also one real request to GitHub

Each case runs a script in a scratch plugin folder with a scratch home, as Antigravity runs a
SessionStart hook (in the plugin folder), and checks what it prints: a system message naming
the newer release, or {}. The PowerShell script runs only where PowerShell is installed and
the sh script only where sh is; a case that cannot run is reported as SKIP, never as PASS.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOOKS = os.path.join(REPO, "plugin", "hooks")
results = []


def case(name, ok, detail=""):
    results.append(bool(ok))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok or not detail else "  -- " + detail))


def runners():
    out = []
    ps = shutil.which("powershell") or shutil.which("pwsh")
    if ps and os.name == "nt":
        out.append(("ps1", [ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join("hooks", "update-check.ps1")]))
    else:
        print("SKIP update-check.ps1: no Windows PowerShell here")
    sh = shutil.which("sh")
    if sh:
        out.append(("sh", [sh, os.path.join("hooks", "update-check.sh").replace("\\", "/")]))
    else:
        print("SKIP update-check.sh: no sh here")
    return out


def run(cmd, version, cache=None, off_file=False, env_off=False):
    """Run one hook script; return (stdout, cache-after or None)."""
    root = tempfile.mkdtemp(prefix="gv-hook-")
    plugin, home = os.path.join(root, "gravitas"), os.path.join(root, "home")
    shutil.copytree(HOOKS, os.path.join(plugin, "hooks"))
    with open(os.path.join(plugin, "plugin.json"), "w", encoding="utf-8") as fh:
        json.dump({"name": "gravitas", "version": version}, fh)
    state_dir = os.path.join(home, ".gemini", "gravitas")
    os.makedirs(state_dir)
    if cache is not None:
        with open(os.path.join(state_dir, "update-check.json"), "w", encoding="utf-8") as fh:
            json.dump(cache, fh)
    if off_file:
        open(os.path.join(state_dir, "update-check-off"), "w").close()
    env = dict(os.environ, HOME=home, USERPROFILE=home)
    env.pop("GRAVITAS_UPDATE_CHECK", None)
    if env_off:
        env["GRAVITAS_UPDATE_CHECK"] = "off"
    p = subprocess.run(cmd, cwd=plugin, env=env, capture_output=True, text=True, timeout=60)
    after = os.path.join(state_dir, "update-check.json")
    state = json.load(open(after, encoding="utf-8")) if os.path.exists(after) else None
    shutil.rmtree(root, ignore_errors=True)
    return p.returncode, p.stdout.strip(), state


def notice(out):
    """The system message text, or None when the output is {}; raises on anything else."""
    d = json.loads(out)
    if d == {}:
        return None
    return d["injectSteps"][0]["systemMessage"]["systemMessage"]


def main(argv):
    live = "--live" in argv
    now = int(time.time())
    hooks = json.load(open(os.path.join(REPO, "plugin", "hooks.json"), encoding="utf-8"))
    cmd = hooks["gravitas-update-check"]["SessionStart"][0]["command"]
    case("hooks.json runs update-check.ps1, then update-check.sh, from the plugin folder",
         cmd == "powershell -NoProfile -ExecutionPolicy Bypass -File hooks/update-check.ps1 || sh hooks/update-check.sh")
    case("the hook has a timeout of at most 15 s", 0 < hooks["gravitas-update-check"]["SessionStart"][0]["timeout"] <= 15)
    fresh_newer = {"checkedAt": now - 60, "latest": "9.0.0", "url": "https://github.com/Emily2040/gravitas/releases/tag/v9.0.0"}
    for name, script in runners():
        code, out, state = run(script, "1.3.0", cache=fresh_newer)
        text = notice(out) if code == 0 else None
        case("%s: a cached newer release gives a notice naming both versions and the release page" % name,
             code == 0 and text is not None and "9.0.0" in text and "1.3.0" in text and fresh_newer["url"] in text, out)
        case("%s: the notice says once, after the answer, in the user's language, and not to run the update" % name,
             bool(text) and "once" in text and "after everything else" in text and "user's language" in text and "do not run the update yourself" in text)
        case("%s: the cache was used, not the network (checkedAt unchanged)" % name, state == fresh_newer, str(state))
        for label, v in (("same version", "9.0.0"), ("later version", "9.1.0")):
            code, out, _ = run(script, v, cache=fresh_newer)
            case("%s: no notice for the %s" % (name, label), code == 0 and notice(out) is None, out)
        code, out, _ = run(script, "1.3.0", cache=fresh_newer, off_file=True)
        case("%s: update-check-off file turns it off" % name, code == 0 and out == "{}", out)
        code, out, _ = run(script, "1.3.0", cache=fresh_newer, env_off=True)
        case("%s: GRAVITAS_UPDATE_CHECK=off turns it off" % name, code == 0 and out == "{}", out)
        code, out, _ = run(script, "not-a-version", cache=fresh_newer)
        case("%s: an unreadable plugin version gives {}" % name, code == 0 and out == "{}", out)
        if live:
            code, out, state = run(script, "99.0.0", cache={"checkedAt": "garbage"})
            case("%s: live: a corrupt cache is replaced by a fresh check, and 99.0.0 gets no notice" % name,
                 code == 0 and out == "{}" and state and isinstance(state.get("checkedAt"), int) and state["checkedAt"] >= now, "%s %s" % (out, state))
            t = time.time()
            code, out, state = run(script, "1.0.0", cache=None)
            secs = time.time() - t
            case("%s: live: one real check finds a newer release than 1.0.0 and caches it (%.1fs)" % (name, secs),
                 code == 0 and notice(out) is not None and state and state["checkedAt"] >= now and state["latest"], out[:200])
    print("%d/%d passed" % (sum(results), len(results)))
    return 0 if results and all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
