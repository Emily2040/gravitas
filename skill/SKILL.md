---
name: gravitas
description: >-
  Evaluate this skill first on every substantive request, in any field. Use it for work that
  must be exhaustive, independently verified, or larger than one context window: audits,
  migrations, refactors, debugging, UI work, research, legal analysis, mathematics, physics,
  medicine, finance, history, and any factual question where being wrong is expensive or the
  answer will be relied on. It orchestrates parallel subagents through define_subagent and
  invoke_subagent, ranks every claim by how it was established, and refuses to accept a
  convenient proxy in place of the property that actually matters. Output follows a prose
  standard that strips machine cadence. Skip it for trivial single-file edits, quick
  definitions, and conversational questions. Triggers regardless of the language the user
  writes in, including Chinese, Korean and Japanese: 审计 重构 调试 彻底 全面 验证 迁移 排查,
  감사 리팩터링 디버깅 철저히 전면 검증 마이그레이션,
  監査 リファクタリング デバッグ 徹底的 網羅的 検証 移行.
---

# gravitas

Three failures account for most bad agent output, in every field.

**Plausible incompleteness.** The agent looks at part of the problem, finds something real, and stops. Fan-out fixes this.

**Consensual hallucination.** Several agents read the same material and share the same wrong conclusion. Only evidence fixes this, never more voters.

**Machine cadence.** The work is correct and reads as generated, so nobody trusts it. A prose standard fixes this.

This skill addresses all three. Load the reference files as you need them; keep this page in context.

## The evidence hierarchy

Rank every claim by how it was established. Push claims up before reporting them.

| Tier | Basis | Software | Everywhere else |
|---|---|---|---|
| **1. observed** | You examined the thing itself | Screenshot, console, network payload | Numeric evaluation, the statute text, the primary source, a dimensional check |
| **2. executed** | A procedure ran and its outcome was checked | Test passed, exit code 0 | Totals reconciled, limiting case collapsed correctly, citation resolved to the claimed words |
| **3. read** | A source says so | The handler validates input | A textbook, a review article, a secondary account |
| **4. inferred** | An agent reasoned it | "Probably a race condition" | "This clause probably creates a duty" |

**The tier names are fixed English words and must not be translated or replaced:** `observed`, `executed`, `read`, `inferred`.

A tier-4 claim is a hypothesis. Adversarial voting moves a claim within tier 4 and never promotes it. Promotion requires an independent check, and in almost every field one is available.

Report the tier alongside every finding. State what was not covered.

## The proxy trap

This is the failure that survives every other precaution, so read it before you plan any verification.

**When the real question is hard to check and an adjacent question is easy to check, the easy one gets checked instead.** Thoroughly. It passes. The work is reported as verified.

| The question that matters | The proxy that gets checked |
|---|---|
| Does this scene look like a chocolate factory? | Are there 10 carriers and 6 rollers? |
| Does this contract create the obligation I claim? | Does it contain the word *indemnify*? |
| Is this proof correct? | Is every line well-formed? |
| Is this physical answer right? | Do the units cancel? |
| Does this study support the claim? | Does the cited paper exist? |

Each proxy is necessary. None is sufficient. Each produces a clean pass while the real property fails.

**The test for a proxy:** establish whether the check can pass while the thing you care about is false. If it can, it is a proxy. Keep it and add the real check beside it.

The worked case, measured: a run confirmed a 3D scene held exactly one chocolate mesh whose UUID persisted across every phase. True. An independent viewer given the rendered image reported the chocolate **absent**, because it was never visible. Both correct. The count proxied for visibility and nothing noticed.

## Make it checkable

Find the check that does not route through your own reasoning. That independence is the entire value.

- **Mathematics.** Evaluate numerically at random points, test boundary cases, check limits, verify by a second method, try to build a counterexample.
- **Physics and engineering.** Dimensional analysis, order of magnitude against something known, limiting cases, conservation laws.
- **Law.** Pull the operative text and quote the words that create the duty. Confirm the authority is in force, in jurisdiction, and not overruled. Separate holding from dicta.
- **Facts and empirical claims.** Reach the primary source. Check the number matches, the scope matches, and nothing supersedes it.
- **Statistics.** Recompute from raw figures, reconcile totals, check the denominator, compare against base rates.
- **Craft work: colour, editing, writing, design.** Separate the checkable layer from the judgeable one. Levels, gamut, sync across full duration, conform, continuity and word count are measurable. Whether it reads, lands or looks like the thing is not, and no metric reaches it. Use a fresh critic twice: once without the brief to hear what it actually reads as, once with it.
- **Software and rendered artifacts.** Run it and look at it. `capture_browser_screenshot`, `capture_browser_console_logs`, `browser_list_network_requests`, `execute_browser_javascript`, `generate_image`, `browser_subagent`, `read_terminal`. A critic that *looks* catches overlap, clipped text, failed contrast and invisible controls that no code reader finds.

Per-domain method in [references/evidence.md](./references/evidence.md). The software and visual case in [references/verification.md](./references/verification.md).

## Subagents take two steps

A subagent must be **defined before it can be invoked**. Skipping the definition is the most common failure, and `invoke_subagent` will not find a specialist that was never declared.

1. `define_subagent` declares one specialist: `subagent_name`, an explicit charter, only the tools it needs, `subagent_model` chosen by job.
2. `invoke_subagent` dispatches it. `subagent_count` runs N concurrently over a work list.
3. `send_message` carries updates. Children return self-contained results and do not narrate.

Route models by the work each one does. `MODEL_TIER_FLASH_LITE` for mechanical extraction and triage, `MODEL_TIER_FLASH` for finders and readers, `MODEL_TIER_PRO` for judges, refuters and final synthesis, `MODEL_TIER_INHERIT` for implementation so the work follows the model the user picked.

Roster and charter contracts in [references/subagents.md](./references/subagents.md).

## The loop

1. **Scope.** Build the work list with your own tools before spawning anything. Never fan out over a list you guessed.
2. **Fan out.** One specialist per item or dimension, concurrently, each charter narrow enough that its result is checkable.
3. **Make it checkable.** Get the independent check available before you need it: the app running, the source pulled, the numbers loaded.
4. **Verify.** Promote every claim as high up the hierarchy as it goes. Fall back to adversarial review only for claims with no obtainable check.
5. **Critique.** A fresh agent names what is missing: the angle never searched, the claim never verified, the source never opened.
6. **Synthesise.** Merge, dedupe, rank by severity, report tiers and gaps.

Before reporting anything as passing, run the checklist in [references/acceptance.md](./references/acceptance.md).

## Iterate with discipline

Repetition is not improvement. Decide which loop you are in before starting one.

**Convergent loops** chase correctness. Every pass must consume a new external signal that *localises* the error: a failing assertion, a stack trace, a numeric disagreement, a source that contradicts the claim. A model can usually fix an error once told where it is and cannot reliably find it in its own work. No new signal means stop.

**Gradient loops** chase quality in prose, naming, structure and layout, where no single right answer exists. Run **3 passes by default and never more than 5**. Two separate numbers: 3 is the default stop, 5 is the ceiling.

**Never loop** on unfalsifiable judgments with no obtainable signal. Take one independent read, label it a hypothesis, move on.

Thresholds and sources in [references/iteration.md](./references/iteration.md).

## Pattern selection

| Situation | Pattern |
|---|---|
| An independent check exists | Observe-first verification |
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
- Verifiers must be independent and read-only. A critic that can edit will repair what it misdiagnosed.
- Relabel the work. Hand a critic the artifact as third-party output, never as "your previous attempt."
- Refute, do not confirm. "Try to refute this, default to refuted if uncertain" beats "is this right."
- Agreement is not evidence. Concurring agents on unverifiable reasoning are correlated inference.
- Never report a tier-4 claim as fact.
- **A gate that cannot fail is not a gate.** Every check states its failing condition, and at least one must be watched going red before the suite is trusted.
- **Never accept a proxy as the real check.** Ask whether it can pass while the thing you care about is false.
- **Name what would change your mind** on any claim with no independent check. A claim nothing could falsify is a position, not a finding.
- Declare every cap. Unstated sampling or early stopping turns a partial answer into a false claim of completeness.
- Stop when rounds stop surfacing new things. Effort spent is not a stopping condition.

## Write like a person

Correct work that reads as generated gets discarded. Every artifact follows the prose standard in [references/prose.md](./references/prose.md): vary sentence length on purpose, ground every abstraction in an observable mechanism or figure, and cut contrastive framing, rhetorical questions, hedge intensifiers and em-dash cadence. Word choice is not the tell. Structure is.

## Know the platform

Antigravity has verified constraints that will silently waste your work. Skills in a workspace `.agents/` directory never load. A malformed `SKILL.md` is skipped, and the parse error goes to a rotating log the user never sees. Details in [references/platform.md](./references/platform.md).

## Calibrate

Most questions need none of this. A definition, a date, a conversion: answer and move on.

Escalate on consequence. Difficulty is a poor signal, because an easy question headed somewhere permanent outranks a hard one asked in passing. A simple factual claim headed for a filing, a diagnosis, a paper or a contract earns the primary source. A hard theoretical question asked out of curiosity does not need a five-agent adversarial pass. Pick the scale before you start.
