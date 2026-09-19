---
name: deep-work
description: >-
  Evaluate this skill first on every substantive request. Use it for work that must be
  exhaustive, independently verified, or larger than one context window: audits, migrations,
  refactors, debugging, UI and frontend work, research, and anything where being wrong is
  expensive or the result has to actually run. It orchestrates parallel subagents through
  define_subagent and invoke_subagent, verifies claims against observed reality using
  Gemini's native vision rather than against more text, and holds output to a prose standard
  that strips machine cadence. Skip it for trivial single-file edits and conversational
  questions.
---

# Deep Work

Three failures account for most bad agent output.

**Plausible incompleteness.** The agent looks at part of the problem, finds something real, and stops. Fan-out fixes this.

**Consensual hallucination.** Several agents read the same text and share the same wrong conclusion. Only evidence fixes this, never more voters.

**Machine cadence.** The work is correct and reads as generated, so nobody trusts it. A prose standard fixes this.

This skill addresses all three. Load the reference files as you need them; keep this page in context.

## The evidence hierarchy

Rank every claim by how it was established. Push claims up before reporting them.

| Tier | Basis | Example |
|---|---|---|
| **1. Observed** | You looked at the running thing | Screenshot, console log, network payload, rendered DOM |
| **2. Executed** | It ran and the outcome was checked | Test passed, exit code 0, query returned rows |
| **3. Read** | The source says so | The handler validates the input |
| **4. Inferred** | An agent reasoned it | "This is probably a race condition" |

The four words, in order: **observed, executed, read, inferred.** Use those names verbatim when reporting, so a tier is never ambiguous.

A tier-4 claim is a hypothesis. Adversarial voting moves a claim within tier 4 and never promotes it. Promotion requires running something, and on this platform you can almost always run something.

Report the tier alongside every finding. State what was not covered.

## Use the vision

Gemini sees. Most agent harnesses cannot, so most orchestration advice ignores it. That advice is leaving the strongest verification signal on the table.

Reach for these by default on anything with a rendered or running surface:

- `capture_browser_screenshot` gives a critic something to look at. It catches overlap, clipped text, failed contrast, elements rendered off-screen, layouts that collapse at width, a spinner that never resolves, a control present in the DOM and invisible to a human. No code reader finds any of these.
- `capture_browser_console_logs` catches the runtime exception inside a component that rendered correctly.
- `browser_list_network_requests` and `browser_get_network_request` verify the real request and response instead of the assumed contract.
- `execute_browser_javascript` forces empty, error and loading states so they get exercised rather than reasoned about.
- `browser_resize_window` tests breakpoints for real.
- `generate_image` synthesises a target to diff an implementation against, which turns "does it look right" into a checkable comparison.
- `browser_subagent` drives the browser concurrently with code agents and holds ground truth about behaviour.
- `read_terminal` reads what happened instead of assuming the command did its job.

Full method in [references/verification.md](./references/verification.md).

## Subagents take two steps

A subagent must be **defined before it can be invoked**. Skipping the definition is the most common failure, and `invoke_subagent` will not find a specialist that was never declared.

1. `define_subagent` declares one specialist: `subagent_name`, an explicit charter, only the tools it needs, and `subagent_model` chosen by job.
2. `invoke_subagent` dispatches it. `subagent_count` runs N concurrently over a work list.
3. `send_message` carries updates between agents. Children return self-contained results and do not narrate.

Route models by the work each one does. `MODEL_TIER_FLASH_LITE` for mechanical extraction and triage, `MODEL_TIER_FLASH` for finders and readers, `MODEL_TIER_PRO` for judges, refuters, visual critics and final synthesis, `MODEL_TIER_INHERIT` for implementation so the work follows the model the user picked.

Set `enable_subagent_tools: true` only where a specialist subdivides its own charter. A deep tree is slow and hard to audit.

Roster, charters and contracts in [references/subagents.md](./references/subagents.md).

## The loop

1. **Scope.** Build the work list with your own tools before spawning anything. Never fan out over a list you guessed.
2. **Fan out.** One specialist per item or dimension, concurrently, each charter narrow enough that its result is checkable.
3. **Make it observable.** If the work has a runtime surface, get it running now with `restart_dev_server` and `open_browser_url`. Verification depends on this existing.
4. **Verify empirically.** Promote every claim as high up the hierarchy as it goes. Fall back to adversarial text review only for claims with no obtainable signal.
5. **Critique.** A fresh agent names what is missing: the angle never searched, the claim never verified, the state never exercised. That becomes the next round.
6. **Synthesise.** Merge, dedupe, rank by severity, report tiers and gaps.

## Iterate with discipline

Repetition is not improvement. Decide which loop you are in before starting one.

**Convergent loops** chase correctness. Every pass must consume a new external signal that *localises* the error: a failing assertion, a stack trace, a console exception, a screenshot diff, a contradicting network response. A model can usually fix an error once told where it is and cannot reliably find it in its own work. No new signal means stop.

**Gradient loops** chase quality in prose, naming, ergonomics and layout, where no single right answer exists to drift away from. Run **3 passes by default and never more than 5**. Those are two separate numbers: 3 is where you stop by default, 5 is the ceiling you may not cross. Gains concentrate in the first two rounds and reverse past roughly three.

**Never loop** on unfalsifiable judgments with no obtainable signal. Take one independent read, label it a hypothesis, move on.

Thresholds, evidence and sources in [references/iteration.md](./references/iteration.md).

## Pattern selection

| Situation | Pattern |
|---|---|
| A rendered or running surface exists | Observe-first verification |
| Unknown how many issues exist | Loop-until-dry |
| One search angle will miss things | Multi-modal sweep |
| Solution space is wide and open | Judge panel |
| A finding could be wrong several ways | Perspective-diverse verify |
| Suspect something was missed | Completeness critic |
| Cost per item varies wildly | Staged escalation |
| A fix must be driven to green | Convergent loop |
| Output needs polish, not correction | Gradient loop |

Structures in [references/patterns.md](./references/patterns.md).

## Non-negotiables

- Build the work list first. Guessing it produces systematic, confident blind spots.
- Verifiers must be independent and read-only. Define critics without write access so a critic cannot repair what it may have misdiagnosed.
- Relabel the work. Hand a critic the artifact as third-party output, never as "your previous attempt." Detection measurably improves.
- Refute, do not confirm. "Try to refute this, default to refuted if uncertain" beats "is this right."
- Agreement is not evidence. Concurring agents on unverifiable reasoning are correlated inference.
- Never report a tier-4 claim as fact.
- Declare every cap. Unstated sampling or early stopping turns a partial answer into a false claim of completeness.
- Stop when rounds stop surfacing new things. Effort spent is not a stopping condition.

## Write like a person

Correct work that reads as generated gets discarded. Every artifact this skill produces, including issue reports, summaries, commit messages and documentation, follows the prose standard in [references/prose.md](./references/prose.md).

The short version: vary sentence length on purpose, ground every abstraction in an observable mechanism or metric, and cut contrastive framing, rhetorical questions, hedge intensifiers and em-dash cadence. Word choice is not the tell. Structure is.

## Know the platform

Antigravity has verified constraints that will silently waste your work if you ignore them. Skills in a workspace `.agents/` directory never load. A malformed `SKILL.md` is skipped, and the parse error goes to a rotating log file that the user never sees, so the skill is simply absent with no warning anywhere. `force_continue` has no ceiling. Details and workarounds in [references/platform.md](./references/platform.md).

## Calibrate

"Check this quickly" gets two agents and one verification pass. "Audit this properly" gets a wide finder pool, visual and runtime verification wherever a surface exists, three to five vote adversarial refutation on whatever cannot be observed, and a completeness critic. Pick the scale before you start.
