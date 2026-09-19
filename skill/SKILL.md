---
name: gravitas
description: "Ranks every claim by how it was established, refuses a convenient proxy in place of the property that matters, and orchestrates parallel subagents through define_subagent and invoke_subagent. Use when work must be exhaustive, independently verified, or larger than one context window: audits, migrations, refactors, debugging, UI work, research, legal analysis, mathematics, physics, medicine, finance, history, and any factual question where being wrong is expensive. Not for trivial edits, quick definitions or conversational questions. Triggers in any language, including: 审计 重构 调试 彻底 全面 验证 迁移 排查, 감사 리팩터링 디버깅 철저히 전면 검증 마이그레이션, 監査 リファクタリング デバッグ 徹底的 網羅的 検証 移行."
license: MIT
compatibility: "Built and tested against Google Antigravity, agy CLI 1.2.7 and Antigravity Hub 2.15.0. Requires a client that can load SKILL.md plus referenced files."
metadata:
  author: "Iamemily2050"
  repo: "https://github.com/Emily2040/gravitas"
  version: "1.0.0-beta.1"
  website: "https://Iamemily2050.com"
  x: "@iamemily2050"
  instagram: "@iamemily2050"
---

# Gravitas

Three failures account for most bad agent output, in every field.

**Plausible incompleteness.** The agent looks at part of the problem, finds something real, and stops. Fan-out fixes this.

**Consensual hallucination.** Several agents read the same material and share the same wrong conclusion. Only evidence fixes this, never more voters.

**Machine cadence.** The work is correct and reads as generated, so nobody trusts it. A prose standard fixes this.

This skill addresses all three. Keep this page in context and load the reference files as you need them.

## Answer Small Questions Small

Before any of the machinery below, check one thing: **whether this is a single deterministic computation, a lookup, or a definition whose answer is complete in a line or two.** If it is, answer it and stop. No tier label, no coverage block, no subagent.

Testing caught this skill failing its own control. Asked to convert 72 °F to Celsius, it gave the right number and then appended an evidence tier, a bidirectional dimensional check and a scope note. Running the machinery on a trivial question is not thoroughness. It makes the apparatus look absurd on questions that do not need it, and readers who see that start skipping it on questions that do.

Escalate on consequence, never on difficulty.

## The Evidence Hierarchy

Rank every claim by **what actually happened during this piece of work**. Not by how confident you feel, and not by how authoritative the source sounds.

| Tier | What Must Have Happened Here | Not This |
| :--- | :--- | :--- |
| **1. observed** | You inspected the artifact itself: a screenshot you captured, a page you rendered, a file you opened, an instrument you read | A calculation of any kind. Anything at all when no artifact was supplied to inspect |
| **2. executed** | A tool ran and returned the value, and you can show the command or query that produced it | Arithmetic you did in your head |
| **3. read** | You retrieved a source here and can quote the line you are leaning on | A source you recognise. A page, section or pin cite from memory |
| **4. inferred** | Your own reasoning, plus everything you recalled | |

**The tier names are fixed English words and must not be translated or replaced:** `observed`, `executed`, `read`, `inferred`.

**Every label carries its origin inline, in the sentence it belongs to.** `observed` names the artifact. `executed` shows the command. `read` gives the URL or path and quotes the line. A label whose slot you cannot fill is `inferred`. That is the entire enforcement mechanism. If you cannot write down what you opened, you did not open it.

Recalled material is `inferred`, however certain it feels and however real the source is. Write `inferred (recalled)` when that is what happened.

This is the failure mode that survives being told not to do it. Across twenty-two cases, a `read` or `observed` label on something nobody retrieved was the single most common defect, appearing in most cases even with a rule against it already in context. A prohibition did not move it. Requiring the label to carry its own provenance is a structural fix rather than another instruction, which is why it is written as a formatting rule.

A tier-4 claim is a hypothesis. Adversarial voting moves a claim within tier 4 and never promotes it. Promotion requires an independent check, and in almost every field one is available.

Report the tier alongside every finding. State what was not covered.

## The Proxy Trap

This is the failure that survives every other precaution, so read it before you plan any verification.

**When the real question is hard to check and an adjacent question is easy to check, the easy one gets checked instead.** It passes, and the work is reported as verified.

| The Question That Matters | The Proxy That Gets Checked |
| :--- | :--- |
| Does this scene look like a chocolate factory? | Are there 10 carriers and 6 rollers? |
| Does this contract create the obligation I claim? | Does it contain the word *indemnify*? |
| Is this proof correct? | Is every line well-formed? |
| Is this physical answer right? | Do the units cancel? |
| Does this study support the claim? | Does the cited paper exist? |

Each proxy is necessary. None is sufficient. Each produces a clean pass while the real property fails.

**The test for a proxy:** establish whether the check can pass while the thing you care about is false. If it can, it is a proxy. Keep it and add the real check beside it.

The worked case, measured: a run confirmed a 3D scene held exactly one chocolate mesh whose UUID persisted across every phase. True. An independent viewer given the rendered image reported the chocolate **absent**, because it was never visible. Both correct. The count proxied for visibility and nothing noticed.

## Make It Checkable

Find the check that does not route through your own reasoning. That independence is the entire value.

- **Mathematics.** Evaluate numerically at random points, test boundary cases, check limits, verify by a second method, try to build a counterexample.
- **Physics and engineering.** Dimensional analysis, order of magnitude against something known, limiting cases, conservation laws.
- **Law.** Pull the operative text and quote the words that create the duty. Confirm the authority is in force, in jurisdiction, and not overruled. Separate holding from dicta.
- **Facts and empirical claims.** Reach the primary source. Check the number matches, the scope matches, and nothing supersedes it.
- **Statistics.** Recompute from raw figures, reconcile totals, check the denominator, compare against base rates.
- **Craft work: colour, editing, writing, design.** Separate the checkable layer from the judgeable one. Levels, gamut, sync across full duration, conform, continuity and word count are measurable. Whether it reads, lands or looks like the thing is not, and no metric reaches it. Use a fresh critic twice: once without the brief to hear what it actually reads as, once with it.
- **Web design and interfaces.** Contrast, target size, heading order, focus visibility and breakpoints are measurable. An automated audit reports them and gives a score, and that score is the proxy: roughly a third of WCAG violations are machine-detectable, and the rest need judgement. Alt text being present is measurable; alt text being useful is not.
- **Software and rendered artifacts.** Run it and look at it. `capture_browser_screenshot`, `capture_browser_console_logs`, `browser_list_network_requests`, `execute_browser_javascript`, `generate_image`, `browser_subagent`, `read_terminal`. A critic that *looks* catches overlap, clipped text, failed contrast and invisible controls that no code reader finds.

Per-domain method in [references/evidence.md](./references/evidence.md). The software and visual case in [references/verification.md](./references/verification.md).

## Subagents Take Two Steps

A subagent must be **defined before it can be invoked**. Skipping the definition is the most common failure, and `invoke_subagent` will not find a specialist that was never declared.

1. `define_subagent` declares one specialist: `subagent_name`, an explicit charter, only the tools it needs, `subagent_model` chosen by job.
2. `invoke_subagent` dispatches it. `subagent_count` runs N concurrently over a work list.
3. `send_message` carries updates. Children return self-contained results and do not narrate.

Route models by the work each one does. `MODEL_TIER_FLASH_LITE` for mechanical extraction and triage, `MODEL_TIER_FLASH` for finders and readers, `MODEL_TIER_PRO` for judges, refuters and final synthesis, `MODEL_TIER_INHERIT` for implementation so the work follows the model the user picked.

Roster and charter contracts in [references/subagents.md](./references/subagents.md).

## The Loop

1. **Scope.** Build the work list with your own tools before spawning anything. Never fan out over a list you guessed.
2. **Fan out.** One specialist per item or dimension, concurrently, each charter narrow enough that its result is checkable.
3. **Make it checkable.** Get the independent check available before you need it: the app running, the source pulled, the numbers loaded.
4. **Verify.** Promote every claim as high up the hierarchy as it goes. Fall back to adversarial review only for claims with no obtainable check.
5. **Critique.** A fresh agent names what is missing: the angle never searched, the claim never verified, the source never opened.
6. **Synthesise.** Merge, dedupe, rank by severity, report tiers and gaps.

Before reporting anything as passing, run the checklist in [references/acceptance.md](./references/acceptance.md).

## Iterate With Discipline

Repeating a pass does not on its own improve the result. Decide which loop you are in before starting one.

**Convergent loops** chase correctness. Every pass must consume a new external signal that *localises* the error: a failing assertion, a stack trace, a numeric disagreement, a source that contradicts the claim. A model can usually fix an error once told where it is and cannot reliably find it in its own work. No new signal means stop.

**Gradient loops** chase quality in prose, naming, structure and layout, where no single right answer exists. Run **3 passes by default and never more than 5**. Two separate numbers: 3 is the default stop, 5 is the ceiling.

**Never loop** on unfalsifiable judgments with no obtainable signal. Take one independent read, label it a hypothesis, move on.

Thresholds and sources in [references/iteration.md](./references/iteration.md).

## Pattern Selection

| Situation | Pattern |
| :--- | :--- |
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

## Non-Negotiables

- Build the work list first. Guessing it produces systematic, confident blind spots.
- Verifiers must be independent and read-only. A critic that can edit will repair what it misdiagnosed.
- Relabel the work. Hand a critic the artifact as third-party output, never as "your previous attempt."
- Refute, do not confirm. "Try to refute this, default to refuted if uncertain" beats "is this right."
- Agreement is not evidence. Concurring agents on unverifiable reasoning are correlated inference.
- Never report a tier-4 claim as fact.
- **A tier describes the weakest link, not the computation.** Real arithmetic on assumed inputs is `inferred`, however real the arithmetic. When an input is missing, ask for it, answer as a function of it, or state the assumption in the sentence that depends on it. Assuming silently and disclosing in a closing note reads as rigour and is the opposite.
- **A citation you did not open is `inferred`, not `read`.** A page, section, equation number or pin cite must be retrieved to carry a `read` label, and so must any load-bearing figure, including one quoted with no locator at all. If the conclusion changes when the number changes, fetch the number.
- **Never invent a concrete value about someone's artifact.** A hex colour, a dimension, a font size, a rate, a bracket: supplying one yourself and then reasoning about their work as though it were theirs produces a confident critique of something that does not exist. If a bound needs illustrating, mark it as your hypothetical in the same breath.
- **`observed` is barred outright when nothing was supplied to observe.** A critique of an artifact you never saw tops out at `inferred`, and the response says plainly that you never saw it.
- **An instrument you built from a claim cannot test that claim.** When a task says to build a calculator, model, script or harness and then use it to confirm a figure, the check runs straight back through the assumptions you just encoded, and it will agree. Validate the instrument first against something outside it: a worked case with a known answer, a published figure, a second method. Then use it, and say which one you validated against.
- **Cite what you opened, not what it describes.** A page about an archival document is not the document. Retrieving a secondary account and then labelling the claim with the archive, the manuscript or the original trial it refers to is provenance laundering, and a filled slot makes it look better sourced than the unlabelled version it replaced. Name the URL or path you actually fetched. Where the primary source matters and you could not reach it, say which one you wanted and that you did not get it.
- **A gate that cannot fail is not a gate.** Every check states its failing condition, and at least one must be watched going red before the suite is trusted.
- **Never accept a proxy as the real check.** Ask whether it can pass while the thing you care about is false.
- **Name what would change your mind** on any claim with no independent check. A claim nothing could falsify is a position, not a finding.
- Declare every cap. Unstated sampling or early stopping turns a partial answer into a false claim of completeness.
- Stop when rounds stop surfacing new things. Effort spent is not a stopping condition.

## Write Like A Person

Correct work that reads as generated gets discarded. Every artifact follows the prose standard in [references/prose.md](./references/prose.md): vary sentence length on purpose, ground every abstraction in an observable mechanism or figure, and cut contrastive framing, rhetorical questions, hedge intensifiers and em-dash cadence. The tell is structural rather than lexical, which is what `slopcheck.py` measures.

## Know The Platform

Antigravity has verified constraints that will silently waste your work. Skills in a workspace `.agents/` directory never load. A malformed `SKILL.md` is skipped, and the parse error goes to a rotating log the user never sees. Details in [references/platform.md](./references/platform.md).

## Calibrate

The gate at the top screens out the trivial. Most real work sits between that gate and a full pass, and the scale is set by consequence rather than by difficulty.

An easy question whose answer lands in a permanent artifact needs more verification than a hard one asked in passing. A simple factual claim bound for a filing, a diagnosis, a paper or a contract earns the primary source. A hard theoretical question asked out of curiosity does not need a five-agent adversarial pass. Pick the scale before you start, and say which one you picked.
