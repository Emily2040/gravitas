> **语言说明：** 本参考文件目前仅有英文版。核心技能文件 `SKILL.md` 已完整中文化。翻译进行中。

# Platform

Verified Antigravity behaviour that will silently waste work if you assume otherwise. Each item was reproduced on `agy` CLI 1.2.7 and Antigravity Hub 2.15.0 on Windows 11. Several are filed upstream.

---

## Skills only load from the global directory

A skill at `<repo>/.agents/skills/<name>/SKILL.md` never loads. Neither do the alternate spellings `.agent/`, `_agents/`, `_agent/`, nor an explicit `.agents/skills.json` registration. The whole workspace customization root is inert: hooks, rules and plugins as well as skills.

Proof: with a valid `hooks.json` in `<repo>/.agents/` and the global one moved aside, the log reports `hooks_manager.go:53] loaded 0 named hooks from 0 hooks.json file(s)`.

Install to `~/.gemini/config/skills/<name>/` and nowhere else. Project-scoped customization does not work. Do not design workflows that depend on it.

---

## A malformed skill fails silently

An unparseable `SKILL.md` is skipped. The error goes to `~/.gemini/antigravity-cli/log/cli-*.log` as `skills.go:201] Failed to parse skill file ...` and reaches the user nowhere. The skill simply is not there.

A UTF-8 BOM is enough to trigger it. Windows PowerShell 5.1 `Set-Content` and `Out-File` add one by default, so a perfectly valid skill can be rejected over a byte nobody can see in an editor.

Validate after every edit. `scripts/check_skills.py` checks frontmatter parsing, `name` present and matching its directory, `description` present, BOM, dead relative links and a missing `SKILL.md`.

One thing that does work correctly: a broken skill does not break discovery for the others.

---

## `force_continue` has no ceiling

A `PostInvocation` hook returning `{"terminationBehavior": "force_continue"}` drives the loop with no upper bound. Measured across three runs: 3, 8 and 12 continuations, where 12 was a self-imposed test limit rather than a platform one.

The forced turns produce filler. The task is already done, so the model pads.

If you build a hook that blocks termination while tests are red, bound it yourself with a hard pass ceiling. The defensive hook pattern of swallowing exceptions and emitting a default response turns into an infinite loop if that default includes `force_continue`.

---

## Headless permission behaviour differs

Under `agy -p`:

- `autoExecutionPolicy: CASCADE_COMMANDS_AUTO_EXECUTION_AUTO` has no effect. Tool calls without an exact-match grant are auto-denied, because headless cannot prompt.
- A `PreToolUse` hook returning `{"decision": "allow"}` does not allow the call.
- A `PreToolUse` hook returning `{"decision": "deny"}` **does** block, even a command with an explicit grant.
- `overwrite` from a hook response is applied, and announced to the agent as *"A pre-tool hook changed the arguments of this tool call before it ran."*

Hooks restrict. They cannot permit, at least not in headless. Permission is evaluated against the post-`overwrite` arguments, so a hook cannot launder an unapproved command through an approved one.

Plan headless runs around explicit grants. Policy settings and hook approvals will not carry you.

---

## Permission grants accumulate and rarely re-match

Grants are stored as literal command text, sometimes only the first token, which produces entries like `command(if)`, `command($lines)` and `command(&)` alongside the occasional entire multi-kilobyte script saved verbatim as a single grant. A grant re-matches only on a byte-identical command, which almost never recurs, so the prompt returns and another dead grant is appended.

`~/.gemini/config/config.json` reached 301 KB on one machine, 97.5% of it dead grants, with a single entry of 36,331 characters.

Check that file's size periodically. Only `read_url(domain)` grants earn their place, because domains actually repeat.

Related: per-project `autoExecutionPolicy` in `~/.gemini/config/projects/*.json` **overrides** the global setting. Changing it in the UI has no effect while a project file says otherwise.

---

## Verify against the running app, not the docs

Two of the findings above contradict the documented contract. When platform behaviour matters to a task, test it. The documentation describes intent. The same evidence hierarchy the rest of this skill applies to code applies to the platform itself.
