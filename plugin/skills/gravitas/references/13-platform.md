# Module 13 - Platform

## Purpose

This module records verified Antigravity behaviour that will waste work if assumed otherwise. Load it when a task depends on how Antigravity loads customizations, runs subagents, applies permissions or runs headless, and whenever a tool, hook, skill or permission does something unexpected.

Every entry carries the version and date it was checked against, because the platform moves quickly. Between 18 and 23 September 2026 it shipped desktop 2.15.0, 2.15.1, 2.16.0 and 2.17.0 and CLI 1.2.7, 1.2.8 and 1.2.9. Unless an entry says otherwise, it was checked on Windows 11 with desktop 2.17.0 and agy CLI 1.2.9 on 24 September 2026. The CLI, installed through WinGet, updated itself from 1.2.7 to 1.2.9 between two test runs 21 seconds apart and said nothing, so every stamp here comes from the `version:` line in that run's own log. Before relying on an entry, compare its stamp with the changelog at `https://antigravity.google/changelog` and re-run the check if the relevant surface has changed.

## Where Customizations Load From

| Location | Skills | Agents | Rules | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| `~/.gemini/config/skills/`, `agents/`, `AGENTS.md` | Loaded | Loaded, listed by `agy agents` | Loaded | Observed |
| `~/.gemini/config/plugins/<name>/` | Loaded | Loaded, not listed by `agy agents` | Loaded from `rules/AGENTS.md` | Observed with a test plugin: the model named its skill and agent, and obeyed its rule |
| `<repo>/.agents/` | Not loaded | Not loaded | Not tested | Observed; open issue #1052 |

Gravitas installs as a plugin for this reason: one folder carries the skill, the verifier agents and the always-on rule, and `agy plugin disable gravitas` turns all of it off together. `agy plugin list` shows only plugins imported from a marketplace, so a copied plugin does not appear there even when it is loaded.

The workspace row contradicts the documentation. The built-in customization guide and the skills page describe discovery from `<repo>/.agents/`, and the IDE guide says the IDE "automatically discovers and respects" that folder. On the CLI, a skill in `.agents/skills/` and an agent in `.agents/agents/` were not discovered, while `workspaceDirs` in the log named the folder correctly. An earlier check on 19 September 2026 showed hooks in `.agents/` were not loaded either: the log reported `loaded 0 named hooks from 0 hooks.json file(s)`. The desktop app and the IDE were not tested.

## Budgets That Drop Customizations

Skill names and descriptions share a customization budget, and skills that do not fit are dropped. With 133 skills installed, the model listed 3 of them under "Excluded Skills (due to context budget limits)". All 3 were among the 5 longest descriptions installed, at 1,001 to 1,028 characters. That link between length and exclusion is inferred from one observation. Keep descriptions short; this skill's is under 500 characters.

Rules have their own budget of 20,000 tokens, and each rule file is cut at 24,000 bytes on a line boundary; over-budget rules are demoted to file pointers (read: `docs/rules.md` in the built-in `agy-customizations` guide, and the CLI 1.2.7 changelog).

## A Malformed Skill Fails Silently

An unparseable `SKILL.md` is skipped. The error goes to `~/.gemini/antigravity-cli/log/cli-*.log` as `skills.go:201] Failed to parse skill file ...` and nowhere the user will see it. A UTF-8 byte order mark is enough to trigger this, and Windows PowerShell 5.1 `Set-Content` and `Out-File` add one by default. A broken skill does not stop the others loading.

Run `scripts/check_skills.py` after every edit. It checks frontmatter parsing, description presence and length, the byte order mark, dead references, modules over 100 lines, agent tool names, critics with write tools and rule file size.

## Files And Paths

| Behaviour | Evidence |
| :--- | :--- |
| `view_file` resolves a relative path against `~/.gemini/antigravity-cli/scratch/`, not the workspace, for the main agent and for subagents. The folder is shared by every CLI conversation and still held 33 files from tests five days earlier, so a relative path can open a stale file of the same name without any error | Observed on 1.2.9 |
| `view_file` returns 100 lines per call. In one run the agent read the first 100 lines of a 114-line file and moved on | Observed on 1.2.9 |
| Files inside an installed plugin can be read in a headless run without a grant | Observed on 1.2.9 |
| Holding wildcard grants, with a prompt that looked incomplete, the agent read the user's PowerShell history, other conversations' transcripts and running processes' command lines to find the rest | Observed on 1.2.9 with `gemini-3.8-flash-high` |

## Subagents

The tool declarations the model receives changed shape. `invoke_subagent` takes a `Subagents` array whose entries carry `TypeName`, `Role`, `Prompt`, `Model` and `Workspace`; `define_subagent` takes `enable_write_tools`, `enable_mcp_tools` and `enable_subagent_tools` flags; `manage_subagents` lists and kills. Full detail in `07-subagents.md`.

A custom agent whose `tools` list names an unmapped tool may hang, according to the custom subagent documentation. Since CLI 1.2.7, `find_by_name`, `grep_search` and `list_dir` are absent from the default toolset and available only to agents that list them.

Concurrent subagents share the account's model capacity: while two other runs were active, a parent run ended with status `ERROR` on `RESOURCE_EXHAUSTED (code 429)` after its three subagents had finished, so size fan-outs with that in mind. Customizations reach subagents unless the agent file sets `inheritCustomizations: false`; `08-delegation.md` has the measurement.

## Headless Runs

| Behaviour | Evidence |
| :--- | :--- |
| `autoExecutionPolicy: AUTO` has no effect under `agy -p`; a tool without an exact-match grant is auto-denied | Observed on 19 and 24 September 2026; open issue #1054 |
| A `PreToolUse` hook returning `allow` does not allow the call | Observed on 19 September 2026 |
| A `PreToolUse` hook returning `deny` blocks the call, even one with an explicit grant | Observed on 19 September 2026 |
| `overwrite` from a hook is applied and announced to the agent, and permission is checked against the rewritten arguments | Observed on 19 September 2026 |
| A denied tool discards the turn and the run reports `"status": "SUCCESS"` with exit code 0. The largest loss measured was 48 completed steps and 20,595 output tokens | Observed on 1.2.7, and again on 1.2.9; open issue #794 |
| A subagent started from a headless run is denied `read_file` on a workspace file unless `read_file` is granted | Observed on 1.2.9 |
| A parent whose turn ends with a text reply while a subagent is still running can be shut down before the result arrives, with `SUCCESS` | Observed twice on 1.2.9: 5.4 s after a child was denied `read_file`, and after 357 s of an audit, when the log then recorded "Failed to wake idle agent on message: run state not found". Runs that kept polling waited up to 338 s and received every result |
| Agent and model API failures print `AGY_ERROR: {...}` on stderr and exit 3 | Read: 1.2.6 changelog |
| `--json-schema` turns an argument that is neither a readable file nor a JSON object into a string schema, and a non-object root schema always returns HTTP 400 | Observed on 1.2.7 in 42 runs; open issue #1064 |

A security audit's final reply was replaced by "This request was blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related queries." after 13 minutes and 7 subagents (observed on 1.2.9 with `gemini-3.8-flash-high`). Plan headless runs around explicit grants. Policy settings and hook approvals will not carry you, and a `SUCCESS` status is not evidence that the turn's work survived.

## Hooks

- `invocationNum` is zero-indexed, so the opening turn reports 0. The documentation's example shows 3 and does not say.
- Do not quote the command in `hooks.json`. On Windows the executor escapes the quotes before handing the string to `cmd /c`, and the command fails as not recognised. Use unquoted paths without spaces.
- Write `hooks.json` with a JSON serializer. A bash heredoc collapses doubled backslashes in Windows paths and produces invalid escapes.
- The working directory for a hook is the folder that contains `hooks.json`.
- Hooks fail open: invalid JSON, empty output, a non-zero exit and a timeout were each tolerated, and the timeout was enforced. Since desktop 2.4.3, configurations that cannot run are rejected at load time with an error.
- `terminationBehavior: "force_continue"` has no ceiling (open issue #1055). A `Stop` hook can block termination with `decision: "continue"` and receives `executionNum` to bound it. See `10-iteration.md`.

To verify a hook, have its script append to a sentinel file and inject a unique nonce with an instruction to repeat it, then check both. A valid file and a quiet log are not evidence that the hook ran.

## Permissions

Grants are stored as literal command text, sometimes only the first token, which produces entries such as `command(if)` and `command(&)` next to whole multi-kilobyte scripts saved as a single grant. A grant re-matches only a byte-identical command, so the prompt returns and another dead grant is appended. One `~/.gemini/config/config.json` reached 301 KB, 97.5% of it dead grants, with one entry of 36,331 characters. Check its size now and then. `read_url` grants for domains are the ones that earn their place.

Project settings override global ones. Every file in `~/.gemini/config/projects/*.json` can carry its own execution policy, and while a project says otherwise, changing the global setting in the interface has no effect. The desktop app's policy values are `always-proceed`, `request-review`, `strict` and `proceed-in-sandbox`, and file and network sandboxing has been available on Windows since desktop 2.15.1 (read: the built-in `antigravity-guide` skill, its `app.md` reference, and the changelog).

A rule telling the model never to ask for permission cannot work, because the policy is enforced before the model is consulted.

## Tools By Surface

A tool listing from the default agent on agy 1.2.9 contained `ask_question`, `call_mcp_tool`, `define_subagent`, `generate_image`, `invoke_subagent`, `list_resources`, `manage_subagents`, `manage_task`, `read_resource`, `read_url_content`, `replace_file_content`, `run_command`, `schedule`, `search_web`, `send_message`, `view_file` and `write_to_file`, plus tools from enabled MCP servers. There were no browser tools. Browser tools appear in the desktop app when browser integration is on, and one recorded desktop run had none at all, so check before planning. `04-runtime-verification.md` has the fallbacks.

Other surfaces worth knowing: `ask_question` asks the user a structured question in interactive sessions; `/plan` drafts an editable plan before building, governed by the Plan Review Policy setting (desktop 2.17.0); `agy --effort low|medium|high` sets reasoning effort; `agy models` lists the models on the account; `agy --agent <name>` starts a session as a custom agent.

## Scripted Orchestration

When a fan-out has to run over hundreds of items with exact counters, a script is more reliable than any agent's memory. The Google Antigravity Python SDK (`pip install google-antigravity`) starts agents and subagents from code, with `SubagentConfig`, `enabled_tools`, `allowed_subagents`, `max_subagent_depth` and `response_schema` for structured output, according to the SDK plugin's documentation (version 0.0.7). It authenticates with a `GEMINI_API_KEY` and bills to that key rather than to the Antigravity plan. This route has not been tested with this skill, so treat it as documented and unverified.

## Verify Against The Running Platform

Several entries above contradict the documentation, and the CLI updated itself in the middle of the testing that produced them. When platform behaviour matters to a task, test it on the installed version and stamp the result. The evidence hierarchy applies to the platform the same way it applies to the work.
