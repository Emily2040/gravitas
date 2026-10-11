# Module 08 - Delegation

## Purpose

This module covers how to brief a subagent so its result can be checked, how to wait for it, and how to confirm what it actually did before its claims reach the report. Load it with `07-subagents.md`.

## Charter Contract

A charter that produces unusable output costs tokens and yields something that has to be redone. Every `Prompt` states six things.

1. Territory: the files, claims, routes or sources in scope, as absolute paths or full URLs, and nothing else. Overlapping territories produce duplicates, and gaps between them produce silent misses.
2. Question: one question, narrow enough that the answer can be checked.
3. Return shape: for a shipped agent, the JSON its own instructions define. Never name a schema file: its path is relative to a skill folder the child does not know, and a child given one goes looking for it. For an agent made with `define_subagent`, copy the fields of `schemas/finding.schema.json` or `schemas/verdict.schema.json` into its `system_prompt` as one example object, and say there is no file to look for. An agent told only what to look for writes an essay.
4. Evidence: every claim carries its tier and source in the same field, and anything at tier 4 is marked as a hypothesis.
5. Stop condition: when the territory is covered, or after a stated number of items.
6. Blocked behaviour: if a tool is denied or a file is missing, return what exists with status `blocked` and the error text. Working around a denial is forbidden, and the platform's own denial message says the same.

Children return results and do not narrate progress.

Never give a subagent a relative path. On agy 1.2.9 on 2026-09-24, `view_file` resolved a relative path against `~/.gemini/antigravity-cli/scratch/`, a folder shared by every CLI conversation, rather than against the workspace. `gravitas-prose-editor`, told to edit `draft.md` "in the current workspace", edited a different `draft.md` left in that folder by a test five days earlier and returned the edit with no error. `gravitas-refuter` and `gravitas-visual-critic` hit the same folder, found nothing and returned `blocked`, which is the better failure.

Tell every child that its prompt and instructions hold everything it needs. In the audit test, a finder told that its output must match "the Gravitas finding schema" spent most of its 127 steps searching the user's folders for that file, reading git internals and unrelated test output on the way. The shipped agents now carry the whole schema as an example and are told there is nothing to look for. In the re-run, every finder and refuter finished in 4 to 8 steps and opened nothing outside its territory.

A checker that proves a path traversal, an injection or a data exposure targets a harmless canary it created in the temp folder. In the same test, the checker proved a traversal by reading `C:\Windows\win.ini` through the defective function: harmless there, and the wrong habit on a machine with real secrets.

```text
Role: Refuter, session handling
Territory: the claim below and C:/work/app/src/auth/session.ts. Nothing else.
Claim: "logout() leaves the refresh token valid" (C:/work/app/src/auth/session.ts:88-120)
Question: can you show this claim is false?
Return: one JSON object with exactly the fields in your instructions.
Evidence: every statement carries its tier and source, e.g. read (C:/work/app/src/auth/session.ts:97, "...").
Stop: after one verdict.
If a tool is denied, return status "blocked" with the error text.
```

## Delegation Integrity

The parent's own status says nothing about its children, so check each child before synthesis.

1. Record every child in the ledger with its conversation ID and final status: `done`, `failed`, `denied`, `empty` or `killed`.
2. Call `manage_subagents` with `list` to confirm none is still running, and `kill` any that are past the ceiling. Never end a turn while a child runs unless a timer is pending (Waiting For A Subagent, below): without one, a turn that ends with a text reply such as "waiting for the critic" can end the whole run, and a result that arrives afterwards is lost.
3. Report every child that failed, was denied or returned nothing, by name, as a coverage gap in the report file.
4. For every load-bearing claim a child returned, confirm the tool step behind the label in the child's transcript at `logAbsoluteUri`. `scripts/provenance_check.py <child answer> --conversation <child id>` does this for every label at once. The rule is in `02-evidence-traps.md` under Delegated Claims.
5. Carry each claim into the report file with its tier and its author: `read by gravitas-reader (...)`. The reply itself names no agent (`00-orchestrator.md`, Output Assembly).

The silent failure is real on this platform. On agy 1.2.9 on 2026-09-24, a subagent's first `read_file` was denied in a headless run and it produced nothing, while the parent ended 5.4 seconds after starting with `"status": "SUCCESS"` and the reply "I am waiting for its response." With the permission granted, the same kind of run waited 63 seconds for its subagent and reported the subagent's answer. A second early exit had no denial in it: a full audit polled `manage_subagents` for a minute, then ended its turn with "Waiting for the Completeness Critic subagent to complete its evaluation", and the CLI shut the run down 29 seconds later. The critic's result arrived to "Failed to wake idle agent on message: run state not found" in the log.

## Waiting For A Subagent

`schedule` returns at once and does not pause the turn, so waiting means ending the turn with a timer pending. This pattern was verified on agy 1.2.16 on 3 October 2026, headless with `--sandbox --dangerously-skip-permissions`, with the parent on Gemini 3.8 Flash and the subagent on `Model: "pro"`. It is untested at default headless settings, which refuse `run_command` and `read_url_content` (`13-platform.md`), so a child that needs either may return nothing, and then the timer's prompt is what acts. The always-on rule's Second Opinion uses it when the plugin is installed with `--review`.

1. Call `invoke_subagent`.
2. Call `schedule` with `DurationSeconds` set to the longest acceptable wait, `TimerCondition: "any"`, and a `Prompt` that says what to do if nothing arrives.
3. End the turn with one short line, with no other text and no further tool call: a headless run prints text written beside a tool call too, and in 1 of 8 runs the holding line appeared twice that way. On agy 1.2.16 with Gemini 3.8 Flash, a turn with neither text nor tool calls was rejected with "model output must contain either output text or tool calls, these cannot both be empty". A headless run prints the line before the reply, so write it for the person.
4. The child's completion message wakes the parent and cancels the timer. If the timer fires first, act on its prompt.

When a child finishes without calling `send_message`, the wake-up message comes from sender `system`, not from the child's conversation ID, and it carries the child's last reply. A timer keyed to the child's ID is therefore not cancelled by it: in 7 of 7 such runs the 240-second timer ran its full length and the parent replied a second time, once repeating a whole email. A message the child sends itself with `send_message` carries its ID and cancelled a pending timer keyed to that ID in 3 of 3 runs, and no `system` message followed it in 4 of 4. With `"any"`, 8 of 8 runs replied once, 45 to 167 seconds after starting. While a one-shot timer is pending, a headless run stays alive, printing `root agent idle; waiting up to 30m0s for 1 background task(s)` on stderr, until the timer fires or is cancelled. A parent that ended its turn with no timer ended the run instead: its whole reply was the holding line, and the child's result was never delivered. With several children, each message cancels the `"any"` timer, and the declaration allows only one such timer at a time, so set a new one before ending the turn again while others still run; that form follows the declaration and has not yet been tested with this skill.

## Independence

A critic that can write repairs what it misdiagnosed, reports success, and the repair becomes part of the evidence. Every observation and judgement role in the roster has no edit tools for that reason.

Hand critics the artifact as third-party output rather than as "your previous attempt". Models detect errors substantially better in work they believe came from someone else, and relabelling alone improves detection. Never route a verification back to the agent that produced the claim.

Customizations reach subagents unless the agent file turns them off. On agy 1.2.9, `gravitas-reader` found its answer in three steps and then spent 35 seconds loading this skill, because the plugin's always-on rule told it to; the run took 63 seconds. With `inheritCustomizations: false` in the agent file, the same task took 40 seconds and no skill file was opened. Every shipped agent sets it, which also keeps the parent's rules and framing out of the critic's context. None of them has subagent tools.

## Parallel Writers

Two writers on the same files overwrite each other. Partition the work by file, run writers in sequence, or give each one an isolated workspace with `Workspace: "branch"` or `Workspace: "share"`. The isolated modes are described in the tool declaration and have not yet been tested with this skill. Merge through the parent either way.

## Anti-Patterns

- A critic with edit tools, or a checker whose territory includes the work under review.
- Verification by the agent that produced the claim.
- `enable_subagent_tools` on every specialist, which produces a deep, slow tree nobody can audit.
- A charter with no return shape.
- Reading a child's summary and never its transcript on a claim the conclusion rests on.
- Reporting a run as complete while `manage_subagents` would have listed a child as running.
- A `TimerCondition` set to a child's conversation ID, which the `system` completion message does not cancel.
