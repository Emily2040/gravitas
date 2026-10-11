# Module 02 - Evidence Traps

## Purpose

This module covers the places where a correct-looking label still overstates what happened: claims a subagent made, documents the user supplied, documentation, checks that have expired, instruments built from the claim they test, and errors that cancel. Load it with `01-evidence.md` whenever the work uses subagents, supplied files, platform documentation or a tool you built.

## Delegated Claims

A subagent's report is text that another model wrote, and its labels are claims about what that subagent did. A delegated claim carries at most the tier its author earned, and the parent records it in the report file as the subagent's: `read by gravitas-reader (<url>, "<quoted line>")`. The reply names no agent (`00-orchestrator.md`, Output Assembly).

For every load-bearing claim, confirm the label against the subagent's own record. `invoke_subagent` returns a `logAbsoluteUri` for each subagent it starts, pointing at that subagent's transcript. That transcript is part of this task, so the always-on rule's limit on reading outside the workspace and other conversations does not cover it. The limit still covers every conversation this task did not start. Open it and find the tool step behind the label: a `read_url_content` or `view_file` step for `read`, a `run_command` step with the stated command for `executed`, a `view_file` of the artifact for `observed`. If the step is not there, the claim is `inferred`, whatever the label says. `scripts/provenance_check.py <child answer> --conversation <child id>` checks every label in a child's answer this way at once.

The failure this prevents has already happened on this platform. In a test on 24 September 2026 with agy CLI 1.2.9, a subagent's first tool call was refused ("permission check failed for read_file ... user denied permission"), and it produced no answer. The parent's run ended 5.4 seconds after it started, with `"status": "SUCCESS"` and the reply "I have invoked the `gv-reader` subagent with the requested task. I am waiting for its response." Nothing in the parent's output said the subagent had failed. Only the subagent's transcript showed it.

## Documents The User Supplies

A PDF, a spreadsheet, a Word or PowerPoint file, an image or a recording that the user attached is an artifact, and reading it is observation. Antigravity reads PDFs, Office files and audio natively in the desktop app (changelog entries 2.1.4, 2.16.0 and 2.10.0).

Keep two claims apart. What the document says is `observed`, with the file name and the page, cell, slide or timestamp. Whether what it says is true is a separate claim with its own tier. `observed (supply-agreement.pdf, p. 4, cl. 9.2)`: the supplier indemnifies the buyer for third-party IP claims. Whether that clause is enforceable in the buyer's jurisdiction needs the statute or case law, and until something is retrieved it is `inferred`.

## Documentation Describes Intent

A documentation page establishes what the page says. What the software does needs `executed` or `observed`.

On 24 September 2026, the built-in customization guide and the skills documentation both described workspace discovery from `<repo>/.agents/`, and the IDE guide said the IDE "automatically discovers and respects" it. On agy CLI 1.2.9 the same day, a skill in `.agents/skills/` and a custom agent in `.agents/agents/` were not discovered, while the same agent file in `~/.gemini/config/agents/` was listed by `agy agents` straight away. Workspace discovery in the CLI is tracked as open issue #1052 on `google-antigravity/antigravity-cli`.

Strings found inside a binary are weaker still. An earlier version of this skill documented `subagent_count` and `subagent_model` as `invoke_subagent` parameters, taken from strings in `language_server.exe`. The tool declaration the model receives, read out on 24 September 2026, takes a `Subagents` array whose entries carry `TypeName`, `Role`, `Prompt`, `Model` and `Workspace`, and has neither field. A string in a binary shows only that the name exists somewhere in the program.

## Verification Expires

A check is valid for the version, dataset, jurisdiction and date it ran against. Between 18 and 23 September 2026 Antigravity shipped desktop releases 2.15.0, 2.15.1, 2.16.0 and 2.17.0 and CLI releases 1.2.7, 1.2.8 and 1.2.9 (read: `https://antigravity.google/changelog`). The CLI on the test machine installed one of those releases by itself in the middle of this skill's own testing.

Stamp every version-sensitive claim where it is made: `executed on agy 1.2.9, 2026-09-24`. Take the version from the run itself, not from a check made earlier. On 24 September 2026 the CLI updated itself from 1.2.7 to 1.2.9 between two runs 21 seconds apart, so `agy --version` at the start of the session was wrong for every test after it; the CLI log records `version:` at the top of each run. Before relying on a stamped claim, compare the stamp with the latest release of the thing it describes, and re-run the check if it has changed since.

## Instruments You Built

An instrument built from a claim cannot test that claim. A request to build a calculator, a model, a script or a harness and then use it to confirm a figure routes the check back through the assumptions just encoded, so it agrees, and the agreement reads as verification because a tool was involved and a number came out.

Caught in a chained test: given a solar quote whose arithmetic carried two large errors, an agent was asked to build a payback calculator and then confirm the user's figure with it. It found both errors and modelled each one separately. It never said that the final step as written could not have checked anything. Had it complied, the calculator would have encoded the errors and certified them.

Validate an instrument against something outside it before trusting its output: a worked case with a known answer, a published figure, a second independent method. Name what you validated against. An unvalidated instrument reports its inputs back with more decimal places.

## Errors That Cancel

In the same test, understated generation and overstated tariff value were each wrong by roughly a factor of 2 in opposite directions, so the final payback landed within 3% of the correct figure. Checking only the answer confirms it, and checking each link finds both errors. When a result matches a claim, check the steps that produced it before stopping.

## When Nothing Is Observable

Some claims have no independent check at all: interpretive questions, contested law, ethics, prediction, judgements about intent. This is a larger share of work outside software, so the handling matters more.

1. Take independent opinions with distinct lenses. Three agents asking the same question share one blind spot.
2. State the claim as a hypothesis and label its tier.
3. Name what would change your mind. A claim that nothing could falsify is a position rather than a finding, and is reported as one.
4. Give the strongest version of the opposing reading before concluding. If you cannot state it well, you have not understood the question.
5. Report the disagreement. Averaging two incompatible readings produces a third that nobody holds, and two well-argued incompatible readings is the real answer when that is the situation.
