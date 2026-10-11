# Module 07 - Subagents

## Purpose

This module covers how to get a specialist, what the subagent tools take as of October 2026, which agents this plugin ships, and which model each role runs on. Load it before the first `invoke_subagent` or `define_subagent` call, together with `08-delegation.md`.

## Three Ways To Get A Specialist

| Route | How | Write Access | Use For |
| :--- | :--- | :--- | :--- |
| Shipped agent | `invoke_subagent` with `TypeName` set to a `gravitas-*` agent | Fixed by the agent file's `tools` list | Every observation, judgement and critique role |
| Ad-hoc definition | `define_subagent`, then `invoke_subagent` with the new name | `enable_write_tools` true or false | A specialist this plugin does not ship |
| Built-in `self` | `invoke_subagent` with `TypeName: "self"` | The parent's tools | Implementation that should follow the user's model and tools. Listed by the model on agy 1.2.9; not yet tested with this skill |

Prefer the shipped agents for any role that must not write. Their read-only status comes from the tool list in the file, so it does not depend on the subagent following an instruction.

## The Tool Declarations

Read out from the model's own tool declarations on agy 1.2.9 on 2026-09-24, and cross-checked against strings in `language_server.exe` from desktop 2.17.0. All but `define_subagent` were read again on 2026-10-03, the day the CLI moved from 1.2.15 to 1.2.16, and matched. Re-check them after an update, because an earlier version of this skill documented fields that the declarations do not contain.

| Tool | Parameters |
| :--- | :--- |
| `invoke_subagent` | `Subagents`: an array. Each entry takes `TypeName`, `Role` (a 2 to 5 word job title) and `Prompt`, all required, plus `Model` (`inherit`, `flash_lite`, `flash`, `pro`; default `inherit`) and `Workspace` (`inherit`, `branch`, `share`; default `inherit`) |
| `define_subagent` | `name`, `description`, `system_prompt`, `enable_write_tools` (file edits and commands), `enable_mcp_tools`, `enable_subagent_tools` |
| `manage_subagents` | `Action`: `list`, `kill` or `kill_all`, with `ConversationIds` for `kill` |
| `send_message` | `Recipient` (a subagent conversation ID) and `Message` |
| `schedule` | `DurationSeconds` for a one-shot timer or `CronExpression` for a cron, and `Prompt`. `TimerCondition`: `never` (default), `any`, or a sender ID whose message cancels the timer. `IsDaemon` and `MaxIterations` apply to crons. Returns at once; `manage_task` with `kill` and the task ID cancels it |

Concurrency comes from putting several entries in one `Subagents` array. Each started subagent gets its own conversation ID and a `logAbsoluteUri` pointing at its transcript, and when it finishes without calling `send_message`, a message from sender `system` carries its last reply. To wait for it, set a `schedule` timer with `TimerCondition: "any"` and end the turn: a timer keyed to the subagent's ID is not cancelled by that `system` message, and without a timer a headless run ends with the turn and the result is lost. `08-delegation.md` has the verified pattern.

The `invoke_subagent` declaration tells the model to default `Model` to `inherit` unless the user asks for a different model. Installing this plugin is that request for the roles in the routing table below.

## Custom Agent Files

A custom agent is a Markdown file with YAML frontmatter. The frontmatter configures the agent and the body becomes its system prompt.

```markdown
---
name: "gravitas-refuter"
description: "Attempts to refute one specific claim. Defaults to refuted when uncertain."
tools:
  - view_file
  - grep_search
  - read_url_content
  - search_web
model: "pro"
mainAgent: false
subagent: true
inheritCustomizations: false
inheritMcp: false
---

You are a refuter. ...
```

| Key | Meaning |
| :--- | :--- |
| `name`, `description` | Identity, and the text the parent reads when choosing a subagent |
| `tools` | The tools the agent may call. Everything else is absent |
| `model` | `inherit`, `flash` or `pro` |
| `mainAgent`, `subagent` | Whether the agent can be picked as the main agent, and whether `invoke_subagent` can start it |
| `commandExecutionPolicy` | Shell policy: `off`, `auto`, `eager` or `sandbox` |
| `skills`, `plugins`, `mcpServers`, `rules`, `hooks`, `agents` | Customizations attached to this agent |
| `inheritCustomizations`, `inheritMcp` | Whether the agent adopts the user's skills, rules and plugins, and whether it gets the user's MCP servers |
| `excludeDefaultComponents` | Documented as dropping default prompt sections and tools; on agy 1.2.9 it removed nothing further (open issue #1015) |

The key names were confirmed as YAML tags in `language_server.exe` from desktop 2.17.0, and the meanings come from the custom subagent documentation. `inheritMcp` is not in the documentation; it was tested here. The binary also contains `enabledTools`, `disabledTools`, `hidden` and `background`, which are untested and unused.

The `tools` list is not the whole toolset. On agy 1.2.9, an agent listing only `view_file` and setting `inheritCustomizations: false` also had `send_message`, `call_mcp_tool`, `list_resources`, `read_resource` and `manage_task`, by its own account of its declarations. `call_mcp_tool` reaches every connected MCP server, and a critic is read-only only if all of them are. Adding `inheritMcp: false` removed `call_mcp_tool`; adding `excludeDefaultComponents: true` on top changed nothing. Every shipped agent sets both inheritance flags to false.

Custom agents are discovered from `~/.gemini/config/agents/` and from `agents/` inside a plugin. On agy 1.2.9 on 2026-09-24, `agy agents` listed a global agent and did not list one inside a plugin, while the model could see and name both. Agents in a workspace `.agents/agents/` were discovered only when the repo was passed with `--add-dir`.

Two cautions. The documentation warns that an unmapped or misspelled tool name in `tools` may cause the subagent to hang, so `scripts/check_skills.py` checks every name against a known list. And since agy 1.2.7, `find_by_name`, `grep_search` and `list_dir` are no longer in the default toolset; a custom agent gets them only by listing them.

## The Shipped Roster

| Agent | Charter | Tools | Model | Writes |
| :--- | :--- | :--- | :--- | :--- |
| `gravitas-scout` | Locate files, routes, symbols and sources. Return paths and line ranges only | `list_dir`, `find_by_name`, `grep_search`, `view_file` | flash | No |
| `gravitas-reader` | Answer specific questions about a bounded set of files or URLs, quoting the lines relied on | `view_file`, `grep_search`, `find_by_name`, `list_dir`, `read_url_content` | flash | No |
| `gravitas-finder` | Hunt one dimension of defect, or search one angle, across a given work list | `view_file`, `grep_search`, `find_by_name`, `list_dir`, `read_url_content`, `search_web` | flash | No |
| `gravitas-checker` | Run one independent check: a numeric evaluation, a test, a recomputation, a query | `view_file`, `run_command` | flash | Scratch files only, by charter |
| `gravitas-refuter` | Try to refute one claim, defaulting to refuted when uncertain | `view_file`, `grep_search`, `read_url_content`, `search_web` | pro | No |
| `gravitas-visual-critic` | Judge captures as a viewer who has not seen the source | `view_file` | pro | No |
| `gravitas-completeness-critic` | Read the ledger and name what was never searched, opened, run or verified | `view_file`, `list_dir`, `grep_search`, `find_by_name` | pro | No |
| `gravitas-prose-editor` | Apply the prose standard to a draft and return the edited text | `view_file` | pro | No |
| `gravitas-reviewer` | Review a draft reply for the always-on rule's Second Opinion and return at most three defects | `view_file`, `read_url_content`, `search_web`, `run_command` | pro | No, by charter |

`gravitas-checker` and `gravitas-reviewer` hold a command line, so their read-only status is a charter rule rather than a tool restriction. Keep the checker's territory narrow and read its transcript when its result is load-bearing. The reviewer serves the rule's Second Opinion, not this skill's fan-outs, and is installed only with a rule that has that section, which takes `--review` at install. Implementation goes to the parent or to `self` with `Model: "inherit"`, which keeps the user's chosen model on the work that changes files.

## Model Routing

| Work | Model |
| :--- | :--- |
| Mechanical extraction, file triage, listing | `flash_lite` |
| Scouts, readers, finders, checkers | `flash` |
| Refuters, critics, judges, final synthesis | `pro` |
| Anything that writes files | `inherit` |

Paying for `pro` on file triage is waste. Running a visual critic on `flash_lite` discards the judgement the role exists for. `inherit` is the default for writers because silently downgrading the user's chosen model is a decision the user did not make.
