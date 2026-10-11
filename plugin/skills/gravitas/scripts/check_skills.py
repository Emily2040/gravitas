#!/usr/bin/env python3
"""Validate Antigravity skills, custom agents, rules and plugins.

Antigravity skips a broken skill with nothing more than a line in a rotating log
(`skills.go:201 Failed to parse skill file ...`), and the documentation warns that
an unmapped tool name in a custom agent's `tools` list may make the agent hang.
This checks for both, and for the other faults that fail quietly.

Usage:
  python check_skills.py              # everything installed under ~/.gemini/config
  python check_skills.py --repo       # the plugin and locales in a Gravitas repository checkout
  python check_skills.py --repo --locales ja   # the plugin and one locale (or: none, all)
  python check_skills.py DIR [DIR...] # extra skills folders or plugin folders

Faults that stop something loading are reported as BROKEN and set exit 1. Dead
references inside other authors' skills are notes, except under --repo, where
they are BROKEN because they are ours to fix.

Exit: 0 when nothing is broken, 1 when at least one problem was found.
"""
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
CONFIG = os.path.join(HOME, ".gemini", "config")


def find_repo():
    """The repository root is the nearest ancestor holding plugin/plugin.json."""
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.exists(os.path.join(d, "plugin", "plugin.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent

# Tool names seen in the default agent's own tool list on agy 1.2.9 (2026-09-24),
# plus the three the 1.2.7 changelog says remain available when listed explicitly.
CONFIRMED_TOOLS = {
    "ask_question", "call_mcp_tool", "define_subagent", "generate_image", "invoke_subagent",
    "list_resources", "manage_subagents", "manage_task", "read_resource", "read_url_content",
    "replace_file_content", "run_command", "schedule", "search_web", "send_message",
    "view_file", "write_to_file", "find_by_name", "grep_search", "list_dir",
}
# Step types present in language_server.exe that may be tool names on some surfaces
# (the desktop browser tools in particular). Unconfirmed as `tools` entries.
POSSIBLE_TOOLS = {
    "open_browser_url", "capture_browser_screenshot", "capture_browser_console_logs",
    "browser_list_network_requests", "browser_get_network_request", "execute_browser_javascript",
    "browser_click_element", "browser_input", "browser_select_option", "browser_resize_window",
    "browser_scroll", "browser_press_key", "read_browser_page", "browser_subagent",
    "restart_dev_server", "read_terminal", "command_status", "send_command_input",
    "view_file_outline", "view_code_item", "view_content_chunk", "list_browser_pages",
}
AGENT_KEYS = {
    "name", "description", "tools", "model", "mainAgent", "subagent", "skills", "plugins",
    "rules", "hooks", "agents", "mcpServers", "inheritCustomizations", "inheritMcp",
    "excludeDefaultComponents", "commandExecutionPolicy", "hidden", "background",
    "enabledTools", "disabledTools",
}
AGENT_MODELS = {"inherit", "flash", "pro"}
# Tools that change files. A verifier holding one can edit the work it judges.
WRITE_TOOLS = {"write_to_file", "replace_file_content", "multi_replace_file_content"}
COMMAND_TOOLS = {"run_command"}   # critics may not hold these either; gravitas-checker may
# Name fragments that mark an agent as a verifier, which must hold no WRITE_TOOLS.
VERIFIER_ROLES = ("critic", "refuter", "reader", "finder", "scout", "reviewer", "verifier", "checker")
READ_ONLY_RE = re.compile(r"(?<!not )\bread[-‐‑_ ]?only\b")
RULE_FILE_LIMIT = 24000      # bytes, per docs/rules.md
VIEW_WINDOW = 100            # lines view_file returns per call (observed, agy 1.2.9)
LONG_DESCRIPTION = 800       # characters; three 1,000+ character descriptions were dropped


def parse_frontmatter(text):
    """Return (mapping or None, error or None)."""
    if not text.startswith("---"):
        return None, "no frontmatter (the file must start with ---)"
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None, "frontmatter opened but never closed with ---"
    block = m.group(1)
    try:
        import yaml
    except ImportError:
        yaml = None
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
        except Exception as exc:
            return None, "YAML parse error: %s" % str(exc).replace("\n", " ")[:120]
        if not isinstance(data, dict):
            return None, "frontmatter is not a YAML mapping"
        return data, None
    data, key = {}, None
    for line in block.split("\n"):
        if re.match(r"^\s+-\s+", line) and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(line.split("-", 1)[1].strip().strip('"').strip("'"))
        elif ":" in line and not line.startswith((" ", "\t")):
            key, v = line.split(":", 1)
            key, v = key.strip(), v.strip()
            # as YAML reads them: [] is an empty list, true and false are booleans, digits a number
            if v in ("", "[]"):
                data[key] = []
            elif v in ("true", "false"):
                data[key] = v == "true"
            elif re.match(r"^-?[0-9]+$", v):
                data[key] = int(v)
            else:
                data[key] = v.strip('"').strip("'")
    return data, None


def read(path):
    raw = open(path, "rb").read()
    return raw, raw.decode("utf-8", errors="replace")


class Report:
    def __init__(self, strict=False):
        self.strict = strict
        self.problems, self.notes, self.counts = [], [], {"skills": 0, "agents": 0, "rules": 0, "plugins": 0}

    def bad(self, where, msg):
        self.problems.append((where, msg))

    def note(self, where, msg):
        self.notes.append((where, msg))

    def content(self, where, msg):
        """Broken references break our own repo; elsewhere they are the author's to fix."""
        (self.bad if self.strict else self.note)(where, msg)


def check_skill(sdir, rep, label=None, fallback=None):
    """fallback: a second skill folder that supplies shared scripts, schemas and examples."""
    entry = os.path.basename(sdir.rstrip("\\/"))
    where = label or entry
    path = os.path.join(sdir, "SKILL.md")
    if not os.path.exists(path):
        (rep.content if label and "/skills/" in label else rep.bad)(where, "no SKILL.md in the skill folder")
        return
    rep.counts["skills"] += 1
    raw, text = read(path)
    if raw.startswith(b"\xef\xbb\xbf"):
        rep.bad(where, "SKILL.md begins with a UTF-8 BOM, which breaks parsing")
        return
    data, err = parse_frontmatter(text)
    if err:
        rep.bad(where, err)
        return
    name, desc = data.get("name"), data.get("description")
    if not desc:
        rep.bad(where, "no 'description'; the agent uses it to decide when to load the skill")
    elif len(str(desc)) < 30:
        rep.note(where, "description is %d characters; the agent may never trigger it" % len(str(desc)))
    elif len(str(desc)) > LONG_DESCRIPTION:
        rep.note(where, "description is %d characters; long descriptions were the ones dropped by "
                        "the customization budget" % len(str(desc)))
    for root, _, files in os.walk(sdir):
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            _, t = read(p)
            for target in re.findall(r"\]\((\.{1,2}/[^)#\s]+)\)", t):
                if not os.path.exists(os.path.normpath(os.path.join(root, target))):
                    rep.content(where, "dead relative link in %s: %s" % (os.path.relpath(p, sdir), target))
            lines = t.count("\n")
            if os.path.basename(root) == "references" and lines > VIEW_WINDOW:
                rep.content(where, "%s is %d lines; view_file shows %d lines per call and the rest may go unread"
                            % (f, lines, VIEW_WINDOW))
            for target in re.findall(r"`(\d\d-[\w-]+\.md)`", t):
                if not os.path.exists(os.path.join(sdir, "references", target)):
                    rep.content(where, "%s names module %s, which does not exist" % (os.path.relpath(p, sdir), target))
            for target in re.findall(r"`((?:references|schemas|scripts|examples)/[\w./-]+)`", t):
                if "<" in target or "*" in target:
                    continue
                if not os.path.exists(os.path.join(sdir, target)) and not (
                        fallback and os.path.exists(os.path.join(fallback, target))):
                    rep.content(where, "%s names %s, which does not exist" % (os.path.relpath(p, sdir), target))


def check_agent(path, rep, label=None):
    base = os.path.basename(path)
    expected = os.path.basename(os.path.dirname(path)) if base == "agent.md" else base[:-3]
    where = label or ("agent " + expected)
    rep.counts["agents"] += 1
    raw, text = read(path)
    if raw.startswith(b"\xef\xbb\xbf"):
        rep.bad(where, "begins with a UTF-8 BOM")
        return
    data, err = parse_frontmatter(text)
    if err:
        rep.bad(where, err)
        return
    for k in data:
        if k not in AGENT_KEYS:
            rep.note(where, "unknown frontmatter key %r" % k)
    if data.get("name") != expected:
        rep.bad(where, "name %r does not match file name %r" % (data.get("name"), expected))
    if not data.get("description"):
        rep.bad(where, "no 'description'; the parent uses it to choose a subagent")
    model = data.get("model")
    if model and str(model) not in AGENT_MODELS:
        rep.note(where, "model %r is not one of %s" % (model, ", ".join(sorted(AGENT_MODELS))))
    tools = as_list(data.get("tools"), "tools", where, rep)
    for t in tools:
        t = str(t)
        if t in CONFIRMED_TOOLS:
            continue
        if t.startswith("mcp_"):
            rep.note(where, "MCP tool %r is only valid while its server is connected" % t)
        elif t in POSSIBLE_TOOLS:
            rep.note(where, "tool %r exists as a step type but is not confirmed as a `tools` name; "
                            "test the agent before relying on it" % t)
        else:
            rep.bad(where, "unknown tool %r; an unmapped tool name may make the agent hang" % t)
    # A verifier's independence rests on its tool list, not on its instructions.
    held = set(map(str, tools)) | set(map(str, as_list(data.get("enabledTools"), "enabledTools", where, rep)))
    writes = sorted(held & WRITE_TOOLS)
    name_parts = set(re.split(r"[-_.\s]+", expected.lower()))
    desc_l = str(data.get("description") or "").lower()
    read_only = bool(READ_ONLY_RE.search(desc_l))
    if "critic" in name_parts and (writes or held & COMMAND_TOOLS):
        rep.bad(where, "a critic with write or command tools is not independent")
    elif writes and (name_parts & set(VERIFIER_ROLES) or read_only):
        rep.bad(where, "a read-only or verifier agent holds file-writing tool(s) %s and is not independent"
                % ", ".join(writes))
    elif read_only and held & COMMAND_TOOLS:
        rep.note(where, "described as read-only but holds %s, so read-only is an instruction, not a tool limit"
                 % ", ".join(sorted(held & COMMAND_TOOLS)))


def as_list(value, key, where, rep):
    """A frontmatter tool field as a list of names; anything else is reported, not crashed on."""
    if value is None or value == []:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return list(value)
    rep.bad(where, "%s must be a list of tool names, not %r" % (key, value))
    return []


def check_rules(path, rep, where):
    rep.counts["rules"] += 1
    raw, _ = read(path)
    if raw.startswith(b"\xef\xbb\xbf"):
        rep.bad(where, "rule file begins with a UTF-8 BOM")
    if len(raw) > RULE_FILE_LIMIT:
        rep.bad(where, "rule file is %d bytes; Antigravity cuts rule files at %d" % (len(raw), RULE_FILE_LIMIT))


def check_plugin(pdir, rep):
    name = os.path.basename(pdir.rstrip("\\/"))
    rep.counts["plugins"] += 1
    manifest = os.path.join(pdir, "plugin.json")
    try:
        json.load(open(manifest, encoding="utf-8"))
    except Exception as exc:
        rep.bad("plugin " + name, "plugin.json does not parse: %s" % exc)
    skills = os.path.join(pdir, "skills")
    if os.path.isdir(skills):
        for e in sorted(os.listdir(skills)):
            if os.path.isdir(os.path.join(skills, e)):
                check_skill(os.path.join(skills, e), rep, "%s/skills/%s" % (name, e))
    agents = os.path.join(pdir, "agents")
    if os.path.isdir(agents):
        for e in sorted(os.listdir(agents)):
            p = os.path.join(agents, e)
            if e.endswith(".md"):
                check_agent(p, rep, "%s/agents/%s" % (name, e))
            elif os.path.isfile(os.path.join(p, "agent.md")):
                check_agent(os.path.join(p, "agent.md"), rep, "%s/agents/%s" % (name, e))
    rules = os.path.join(pdir, "rules")
    if os.path.isdir(rules):
        for e in sorted(os.listdir(rules)):
            if e.endswith(".md"):
                check_rules(os.path.join(rules, e), rep, "%s/rules/%s" % (name, e))
    hooks = os.path.join(pdir, "hooks.json")
    if os.path.exists(hooks):
        try:
            json.load(open(hooks, encoding="utf-8"))
        except Exception as exc:
            rep.bad("plugin " + name, "hooks.json does not parse: %s" % exc)


def check_path(path, rep):
    if not os.path.isdir(path):
        rep.bad(path, "folder does not exist")
    elif os.path.exists(os.path.join(path, "plugin.json")):
        check_plugin(path, rep)
    elif os.path.exists(os.path.join(path, "SKILL.md")):
        check_skill(path, rep)
    else:
        for e in sorted(os.listdir(path)):
            sub = os.path.join(path, e)
            if os.path.isdir(sub) and os.path.exists(os.path.join(sub, "plugin.json")):
                check_plugin(sub, rep)
            elif os.path.isdir(sub):
                check_skill(sub, rep)


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    repo = find_repo() if argv[:1] == ["--repo"] else None
    rep = Report(strict=repo is not None)
    if argv[:1] == ["--repo"]:
        if repo is None:
            print("--repo must be run from inside a Gravitas repository checkout")
            return 2
        check_plugin(os.path.join(repo, "plugin"), rep)
        if not os.path.exists(os.path.join(repo, "plugin", "README.md")):
            rep.bad("plugin", "README.md is missing; it is what a user finds in the installed folder")
        locales = os.path.join(repo, "locales")
        i = argv.index("--locales") if "--locales" in argv else -1
        if i >= 0 and i + 1 >= len(argv):
            print("--locales needs a value: a locale code, none or all")
            return 2
        only = argv[i + 1] if i >= 0 else "all"
        if only not in ("none", "all") and not os.path.isdir(os.path.join(locales, only)):
            rep.bad("locales/%s" % only, "folder does not exist")
        elif os.path.isdir(locales) and only != "none":
            for lang in sorted(os.listdir(locales)):
                if only != "all" and lang != only:
                    continue
                sk = os.path.join(locales, lang, "skills", "gravitas")
                if os.path.isdir(sk):
                    check_skill(sk, rep, "locales/%s/skills/gravitas" % lang,
                                fallback=os.path.join(repo, "plugin", "skills", "gravitas"))
                rules = os.path.join(locales, lang, "rules", "AGENTS.md")
                if os.path.exists(rules):
                    check_rules(rules, rep, "locales/%s/rules/AGENTS.md" % lang)
                # the installer copies these two into the installed plugin
                if not os.path.exists(os.path.join(locales, lang, "README.md")):
                    rep.bad("locales/%s" % lang, "README.md is missing")
                overlay = os.path.join(locales, lang, "plugin.json")
                try:
                    data = json.load(open(overlay, encoding="utf-8"))
                    if not isinstance(data.get("description"), str) or not data["description"].strip():
                        rep.bad("locales/%s/plugin.json" % lang, "needs a non-empty description")
                except Exception as exc:
                    rep.bad("locales/%s/plugin.json" % lang, "missing or does not parse: %s" % exc)
        targets = []
    else:
        targets = [os.path.join(CONFIG, "skills"), os.path.join(CONFIG, "plugins")] + argv
        agents = os.path.join(CONFIG, "agents")
        if os.path.isdir(agents):
            for e in sorted(os.listdir(agents)):
                if e.endswith(".md"):
                    check_agent(os.path.join(agents, e), rep)
        for rules in (os.path.join(CONFIG, "AGENTS.md"), os.path.join(CONFIG, "GEMINI.md")):
            if os.path.exists(rules):
                check_rules(rules, rep, os.path.basename(rules))
    for t in targets:
        if os.path.isdir(t):
            check_path(t, rep)
        elif t in argv:
            rep.bad(t, "folder does not exist")

    c = rep.counts
    print("checked %d skill(s), %d agent(s), %d rule file(s), %d plugin(s)"
          % (c["skills"], c["agents"], c["rules"], c["plugins"]))
    for where, msg in rep.problems:
        print("  BROKEN  %-40s %s" % (where, msg))
    for where, msg in rep.notes:
        print("  note    %-40s %s" % (where, msg))
    if rep.problems:
        print("FAIL: %d problem(s)" % len(rep.problems))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
