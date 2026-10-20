# Module 13 - Platform

## Purpose

This module records verified Antigravity behaviour that will waste work if assumed otherwise. Load it when a task depends on how Antigravity loads customizations, runs subagents, applies permissions or runs headless, and whenever a tool, hook, skill or permission does something unexpected.

Every entry carries the version and date it was checked against, because the platform moves quickly. Between 18 and 23 September 2026 it shipped desktop 2.15.0, 2.15.1, 2.16.0 and 2.17.0 and CLI 1.2.7, 1.2.8 and 1.2.9. Unless an entry says otherwise, it was checked on Windows 11 with desktop 2.17.0 and agy CLI 1.2.9 on 24 September 2026. The CLI, installed through WinGet, updated itself from 1.2.7 to 1.2.9 between two test runs 21 seconds apart and said nothing, so every stamp here comes from the `version:` line in that run's own log. It reached 1.2.11 the same way on 26 September 2026, and 1.2.16 by 3 October 2026. Before relying on an entry, compare its stamp with the changelog at `https://antigravity.google/changelog` and re-run the check if the relevant surface has changed.

## Where Customizations Load From

| Location | Skills | Agents | Rules | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| `~/.gemini/config/skills/`, `agents/`, `AGENTS.md` | Loaded | Loaded, listed by `agy agents` | Loaded | Observed |
| `~/.gemini/config/plugins/<name>/` | Loaded | Loaded, not listed by `agy agents` | Loaded from `rules/AGENTS.md` | Observed with a test plugin: the model named its skill and agent, and obeyed its rule |
| `<repo>/.agents/` | Loaded only through `--add-dir` | Loaded only through `--add-dir` | `rules/` not loaded either way | Observed; open issues #1036, #1052 |

Gravitas installs as a plugin for this reason: one folder carries the skill, the verifier agents and the always-on rule, and `agy plugin disable gravitas` turns all of it off together. `agy plugin list` shows only plugins imported from a marketplace, so a copied plugin does not appear there even when it is loaded.

The workspace row contradicts the documentation. The built-in customization guide and the skills page describe discovery from `<repo>/.agents/`, and the IDE guide says the IDE "automatically discovers and respects" that folder. On the CLI, a skill, an agent and a hook in `.agents/` loaded when the repo was passed with `--add-dir`, including when it was also the working directory. Launched from inside the repo without the flag, none of them loaded, although `workspaceDirs` in the log named the folder and the log reported `loaded 0 named hooks`. A rule in `.agents/rules/` did not load either way. When a repo's own customizations matter, run `agy -p "..." --add-dir <repo>`. The desktop app and the IDE were not tested.

## Budgets That Drop Customizations

Skill names and descriptions share a customization budget, and skills that do not fit are dropped. With 133 skills installed, the model listed 3 of them under "Excluded Skills (due to context budget limits)". All 3 were among the 5 longest descriptions installed, at 1,001 to 1,028 characters. That link between length and exclusion is inferred from one observation. Keep descriptions short; this skill's is under 500 characters.

Rules have their own budget of 20,000 tokens, and each rule file is cut at 24,000 bytes on a line boundary; over-budget rules are demoted to file pointers (read: `docs/rules.md` in the built-in `agy-customizations` guide, and the CLI 1.2.7 changelog).

## A Malformed Skill Fails Silently

An unparseable `SKILL.md` is skipped. The error goes to `~/.gemini/antigravity-cli/log/cli-*.log` as `skills.go:201] Failed to parse skill file ...` and nowhere the user will see it. A UTF-8 byte order mark is enough to trigger this, and Windows PowerShell 5.1 `Set-Content` and `Out-File` add one by default. A broken skill does not stop the others loading.

Run `scripts/check_skills.py` after every edit. It checks frontmatter parsing, description presence and length, the byte order mark, dead references, modules over 100 lines, agent tool names, critics with write tools and rule file size.

## Files And Paths

| Behaviour | Evidence |
| :--- | :--- |
| `view_file` rejects a relative path, but agents in a headless run treat `~/.gemini/antigravity-cli/scratch/` as their working directory. The main agent searched it after the rejection, and a subagent told to use `draft.md` "in the current workspace" built a path into it directly. The folder is shared by every CLI conversation and held 33 files from tests five days earlier, and both opened a stale file of the same name without comment | Observed on 1.2.9 |
| `view_file` returns 100 lines per call. In one run the agent read the first 100 lines of a 114-line file and moved on | Observed on 1.2.9 |
| Files inside an installed plugin can be read in a headless run without a grant | Observed on 1.2.9 |
| Holding wildcard grants, with a prompt that looked incomplete, the agent read the user's PowerShell history, other conversations' transcripts and running processes' command lines to find the rest | Observed on 1.2.9 with `gemini-3.8-flash-high` |

## Subagents

The tool declarations the model receives changed shape. `invoke_subagent` takes a `Subagents` array whose entries carry `TypeName`, `Role`, `Prompt`, `Model` (`inherit`, `flash_lite`, `flash` or `pro`) and `Workspace`; `define_subagent` takes `enable_write_tools`, `enable_mcp_tools` and `enable_subagent_tools` flags; `manage_subagents` lists and kills. Full detail in `07-subagents.md`.

A custom agent whose `tools` list names an unmapped tool may hang, according to the custom subagent documentation. Since CLI 1.2.7, `find_by_name`, `grep_search` and `list_dir` are absent from the default toolset and available only to agents that list them. They were still absent on agy 1.3.3 on 10 October 2026, and `view_file` on a folder returns "path is a directory, not a file".

Concurrent subagents share the account's model capacity: while two other runs were active, a parent run ended with status `ERROR` on `RESOURCE_EXHAUSTED (code 429)` after its three subagents had finished, so size fan-outs with that in mind. Customizations reach subagents unless the agent file sets `inheritCustomizations: false`; `08-delegation.md` has the measurement.

## Headless Runs

| Behaviour | Evidence |
| :--- | :--- |
| The CLI takes its policy from `toolPermission` in `~/.gemini/antigravity-cli/settings.json`, `request-review` by default, so `autoExecutionPolicy: AUTO` in the desktop settings has no effect under `agy -p`. `toolPermission: "always-proceed"` runs ungranted commands headless and still honours `deny` rules | Observed on 1.2.9; issue #1054 |
| A `PreToolUse` hook returning `allow`, or `ask` with `permissionOverrides`, does not allow an ungranted call. `deny` blocks even a granted call | Observed on 19 and 24 September 2026; open issue #1053 |
| `overwrite` with `decision: "allow"` is applied and announced to the agent, and permission is checked against the rewritten arguments. `overwrite` without a `decision` is a denial | Observed on 19 and 24 September 2026 |
| When a hook refuses a command, the final reply can state the output the command would have printed. In 6 of 11 such runs the reply was the exact marker the prompt asked for, and the transcript showed the command never ran | Observed on 1.2.9 |
| A denied tool discards the turn and the run reports `"status": "SUCCESS"` with exit code 0. The largest loss measured was 48 completed steps and 20,595 output tokens | Observed on 1.2.7, and again on 1.2.9; open issue #794 |
| At default settings a headless run allows `view_file` and `search_web` without a grant and refuses `run_command` and `read_url_content`. Given a self-contained question in an empty folder, the first call was a shell listing of that folder in 30 of 34 runs with this plugin and 21 of 34 without it, and each lost its reply. A `PreToolUse` hook's deny comes before that permission check, so a hook-refused `dir` left the reply intact | Observed on 1.2.11, 26 and 27 September 2026 |
| `--sandbox --dangerously-skip-permissions` ran commands in the workspace and refused writes outside it, but allowed reads anywhere and network access. Two runs read files two folders above their workspace. On Windows the sandbox runs commands as an AppContainer identity: with the workspace on an exFAT drive, which cannot hold the ACL it needs, the process exits with code 2 at the first `run_command` and emits no result event; keep workspaces on NTFS under the profile | Observed on 1.2.11, 26 September 2026; the exFAT exit on 1.4.2, 20 October 2026, issue #1296 |
| A subagent started from a headless run is denied `read_file` on a workspace file unless `read_file` is granted | Observed on 1.2.9 |
| A parent whose turn ends while a subagent is running, with no timer pending, never receives the result. The run waits for the child, shuts down, logs "Failed to wake idle agent on message: run state not found" and reports `SUCCESS` with the parent's last reply | Observed on 1.2.9 in 2 of 2 controlled runs and one audit; issue #1044. Again on 1.2.16 in 1 run: the reply was only the holding line, no "Failed to wake" line was logged, and the message stayed in the conversation's `messages/undelivered` folder |
| `schedule` returns at once. While a one-shot timer is pending, a headless run stays alive (stderr: `root agent idle; waiting up to 30m0s for 1 background task(s)`) until the timer fires or is cancelled | Observed on 1.2.16, 3 October 2026, with `--sandbox --dangerously-skip-permissions`; the wait pattern is in `08-delegation.md` and is untested at default settings |
| A subagent that finishes without calling `send_message` wakes the parent with a message from sender `system` carrying its last reply, so a `TimerCondition` set to its ID is not cancelled: the 240 s timer ran its full length in 7 of 7 runs and the parent replied twice. A child's own `send_message` carries its ID and cancelled such a timer in 3 of 3 runs. `"any"` was cancelled in 8 of 8 | Observed on 1.2.16, 3 October 2026, with `--sandbox --dangerously-skip-permissions` |
| A turn with neither text nor tool calls is rejected ("model output must contain either output text or tool calls, these cannot both be empty"), so a turn that only waits must say one short line. A headless run prints it, and also prints text written beside a tool call | Observed on 1.2.16 with Gemini 3.8 Flash: the error appeared in 2 of 3 runs told to end the turn silently |
| Agent and model API failures print `AGY_ERROR: {...}` on stderr and exit 3 | Read: 1.2.6 changelog |
| A headless `agy -p` turn ends with `UNAUTHENTICATED (code 401)` at no predictable time: in 12 logged runs the cut came at 18, 28, 42, 53, 58, 61, 138, 208, 265 and 486 minutes, while two runs of 60 and 383 minutes finished clean; once a turn ended instead with `NOT_FOUND (code 404): models/barium-b-agy is not found`. The subagents' work and the files written stayed intact every time; `agy -c` resumed the conversation | Observed on 1.4.0 to 1.4.2, 18 to 20 October 2026, with `--sandbox`. Write every output and the report before the final reply, commit per batch, and plan a resume |

A security audit's final reply was replaced by "This request was blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related queries." after 13 minutes and 7 subagents (observed on 1.2.9 with `gemini-3.8-flash-high`). Plan headless runs around explicit grants or `toolPermission`. Hook approvals will not carry you, and a `SUCCESS` status is not evidence that the turn's work survived.

## Hooks

- `invocationNum` and `executionNum` are zero-indexed. A plugin's own `hooks.json` loads, and the model obeyed an `ephemeralMessage` injected at invocation 0 (1.2.11).
- A `Stop` hook reports a normal finish as `terminationReason: "NO_TOOL_CALL"`, not the documented `model_stop`, and also fires on errors such as a 429 (`"ERROR"`). Returning `continue` appends a second reply after the first, and the JSON `response` joins both; after an error it re-enters a retry loop (1.2.11, 26 September 2026).
- Do not quote anything in a `hooks.json` command. On Windows the quotes reach the program intact: a quoted executable is "not recognized", and a quoted script path is joined onto the hook's folder (issue #222). Use unquoted paths without spaces, and write the file with a JSON serializer, because a bash heredoc collapses doubled backslashes in Windows paths. A hook runs in the folder that contains `hooks.json`.
- A failing `PreInvocation` hook is skipped: invalid JSON, empty output, a non-zero exit and a timeout were each tolerated (19 September 2026). A `PreToolUse` hook fails closed: invalid JSON, `{}`, a missing `decision` and a non-zero exit each deny the call, and only empty output lets it through (1.2.9). Timeouts are enforced. Since desktop 2.4.3, configurations that cannot run are rejected at load time with an error.
- `terminationBehavior: "force_continue"` has no ceiling (open issue #1055): on 1.2.9 the hook ran 12 times and forced 11 more model calls, nine of filler and two calling tools nobody asked for. A `Stop` hook can block termination with `decision: "continue"` and receives `executionNum` to bound it. See `10-iteration.md`.
- To verify a hook, have its script append to a sentinel file and inject a unique nonce with an instruction to repeat it, then check both. A valid file and a quiet log are not evidence that the hook ran.

## Permissions

Grants are stored as literal command text, sometimes only the first token, which produces entries such as `command(if)` and `command(&)` next to whole multi-kilobyte scripts saved as a single grant. A grant re-matches only a byte-identical command, so the prompt returns and another dead grant is appended. One `~/.gemini/config/config.json` reached 301 KB, 97.5% of it dead grants, with one entry of 36,331 characters. Check its size now and then. `read_url` grants for domains are the ones that earn their place.

Project settings override global ones. Every file in `~/.gemini/config/projects/*.json` can carry its own execution policy, and while a project says otherwise, changing the global setting in the interface has no effect. The policy values are `always-proceed`, `request-review`, `strict` and `proceed-in-sandbox`, and file and network sandboxing has been available on Windows since desktop 2.15.1 (read: the built-in `antigravity-guide` skill, its `app.md` reference, and the changelog).

The CLI reads grants from `permissions.allow` in its own `settings.json` and from `globalPermissionGrants.allow` in `~/.gemini/config/config.json`; the log line `stored shared config permissions` shows the second. On Windows a `command()` rule matches only the exact command line, `command(*)`, or a `regex:` rule that covers the whole line, such as `command(regex:git .*)`. `command(git)` and `command(git *)` match no call that has arguments (observed on 1.2.9; issues #619, #955). A rule telling the model never to ask for permission cannot work, because the policy is enforced before the model is consulted.

## Tools By Surface

A tool listing from the default agent on agy 1.2.9 contained `ask_question`, `call_mcp_tool`, `define_subagent`, `generate_image`, `invoke_subagent`, `list_resources`, `manage_subagents`, `manage_task`, `read_resource`, `read_url_content`, `replace_file_content`, `run_command`, `schedule`, `search_web`, `send_message`, `view_file` and `write_to_file`, plus tools from enabled MCP servers. There were no browser tools. Browser tools appear in the desktop app when browser integration is on, and one recorded desktop run had none at all, so check before planning. `04-runtime-verification.md` has the fallbacks.

Other surfaces worth knowing: `ask_question` asks the user a structured question in interactive sessions; `/plan` drafts an editable plan before building, governed by the Plan Review Policy setting (desktop 2.17.0); `agy --effort low|medium|high` sets reasoning effort; `agy models` lists the models on the account; `agy --agent <name>` starts a session as a custom agent.

## Scripted Orchestration

When a fan-out has to run over hundreds of items with exact counters, a script is more reliable than any agent's memory. The Google Antigravity Python SDK (`pip install google-antigravity`) starts agents and subagents from code, with `SubagentConfig`, `enabled_tools`, `allowed_subagents`, `max_subagent_depth` and `response_schema` for structured output, according to the SDK plugin's documentation (version 0.0.7). It authenticates with a `GEMINI_API_KEY` and bills to that key rather than to the Antigravity plan. This route has not been tested with this skill, so treat it as documented and unverified.

## Verify Against The Running Platform

Several entries above contradict the documentation, and the CLI updated itself in the middle of the testing that produced them. When platform behaviour matters to a task, test it on the installed version and stamp the result. The evidence hierarchy applies to the platform the same way it applies to the work.
