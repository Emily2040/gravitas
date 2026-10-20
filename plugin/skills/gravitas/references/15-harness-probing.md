# Module 15 - Harness Probing

## Purpose

This module covers how to improve the harness around a model while the work is running: the briefs, gates, checklists, tool rules, model mix and handoff files that decide what an agent does. Load it at standard scale and above, before each round after the first, and whenever a brief or a gate could be written two plausible ways. The weights are fixed. The harness is the part you can change, and it is where most of the quality in a long run comes from.

Every rule in this plugin that changed an outcome (two bounds on a gate, subject in frame before any measure, a check is a tool event, never stop a process you did not start, edits in bounded chunks) was found after a failure. Probing finds the next one before the failure, at the cost of one extra agent per round.

## The Method

Adapted from Google Research's Harness² (Apache-2.0; arXiv 2610.14224), which refines a harness at run time in three steps and keeps what it learns across tasks. Its reported gains from one step are 4.5 to 11.8 points on three work benchmarks. The adaptation here runs inside an Antigravity fan-out.

1. **Propose.** The orchestrator writes two variants of one brief that differ in one dimension only: the order of measures, which reference is emphasised, how the item is decomposed, which model or thinking level runs it, a tool rule, a gate's wording. Both variants are written down before either runs.
2. **Probe.** Two agents run the variants on the same item, with the same seed, inputs, gates, screener and critic. Their outputs and their transcripts are kept side by side in numbered attempt folders.
3. **Compose.** An agent that ran neither probe (the director, or a critic from the roster) reads both results and writes the refined brief, taking the behaviours that produced the better result and naming the evidence that decided: the gate numbers, the critic's lines, the attempt counts. The refined brief replaces the old one for every item of that kind in the next round.

The item to probe is the one that failed worst last round, or the one whose brief changed most. One pair per round is the default; more pairs are a budget decision stated in the report.

## Judging Without Ground Truth

There is no answer key for a scene, a chapter or a design. The comparison is between two runs of the same harness family under the same checks, so what counts is the difference, not the score.

- A difference that the numeric gates and the blind critic agree on is evidence; adopt it.
- A difference that only one of them sees is a hypothesis; probe it again next round before adopting.
- A difference that appears only in the agents' own narration is nothing (`01-evidence.md`): the probe agents' reports are claims, and the composer confirms load-bearing ones against the transcripts.
- Two variants that pass every gate and differ only in the critic's taste are a tie; keep the cheaper one and record that the probe was dry.

## The Improvement Harness

The lessons persist in one file at the workspace root, `HARNESS_LESSONS.md`, which every round's briefs include and the orchestrator reads before proposing. One entry per probe:

```yaml
id: L-012
date: 2026-10-20
item: act 3 car body            # what was probed
dimension: decomposition        # the one thing the variants changed
variant_a: 28 hand-written cross-sections
variant_b: profile curves traced from three orthographic references, lofted, subdivided
evidence: silhouette IoU 0.83 vs 0.91 in three views; smoothness gate 9.4% vs 2.1%; critic named "slab" for A only
adopted: B                       # or tie
now_lives_in: docs/ROUND5_BRIEFS.md, vehicles section; scripts/measure-quality.mjs gate ACT3_BODY_SMOOTHNESS
status: active                   # active | retired (with the later evidence that retired it)
```

A lesson is retired, never deleted, when a later probe contradicts it; the retiring evidence goes in the same entry. The file is the plugin's reflection step made durable: what Argon or any model learned about this project's quirks is written where the next run reads it first, not where it is lost at compaction.

## Scaling Modes

- **Sequential**, the default: one probe pair per round, the composed brief feeds the next round. Cost: one extra agent per round.
- **Parallel**, when budget allows: K pairs on K items in one round, composed together. State K in the report, and remember that concurrent subagents share the account's capacity (`13-platform.md`).
- **Off**: at quick scale, and for any item whose brief has not changed and whose last result passed every gate and the critic.

## Guardrails

- One dimension per probe. A pair that differs in three things teaches nothing.
- Same seed, same inputs, same checks. A probe is a controlled comparison or it is two attempts.
- The composer ran neither probe (`10-iteration.md`: a model catches more in another agent's output than in its own).
- Never probe the gates against the work. Variants change the brief; the gates stay fixed for the round, or the probe measures gaming, not quality (`05-acceptance.md`).
- A probe whose difference is below the gates' resolution two rounds running is dry; stop probing that item and say so.
- Every probe, its outcome and its cost go in the report's Coverage section, with the lesson id.

## Anti-Patterns

- Rewriting a brief after a failure from memory, without a controlled pair, and calling the rewrite a lesson.
- Letting the agent that wrote variant B judge the pair.
- Adopting on narration ("B felt cleaner") rather than on the gates and the blind critic.
- Probing many dimensions at once because agents are cheap.
- Keeping lessons in the conversation, where the next compaction or the next run loses them.

## Sources

- Google Research, *Harness²: recursive agent harnessing for an open world*, github.com/google-research/harness2 (Apache-2.0); paper: https://arxiv.org/abs/2610.14224
- This plugin's own history: the rules added in 1.1.0 to 1.1.2 and the failures that produced them (CHANGELOG).
