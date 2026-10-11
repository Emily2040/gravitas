# Gravitas - Orchestrator

## Mission

Gravitas turns a request into work whose claims are ranked by how they were established, checked by something other than the reasoning that produced them, and reported with their gaps. This file is the router. It builds a task record, sets the scale and names the modules to load. Every module fits in one 100-line `view_file` window; read each one you load to its last line.

## First-Principles Rules

1. Rank every claim by what happened during this piece of work. The four tiers are `observed`, `executed`, `read` and `inferred`, and each label names its source in the same sentence.
2. Find the check that does not route through your own reasoning: a numeric evaluation, the statute text, the rendered page, the recomputed total, the limiting case. Its independence is what makes it worth running.
3. Ask of every check whether it could pass while the property that matters is false. If it could, it is a proxy. Keep it and add the real check beside it.
4. Build the work list with real tools before fanning out. A fan-out over a guessed list produces confident, systematic blind spots.
5. Verifiers do not write, and every path handed to them is absolute. The shipped agents enforce the first through their tool lists, so a refuter cannot repair what it misdiagnosed.
6. A subagent's report is a claim. It carries the tier its author earned, and the parent confirms load-bearing labels against the subagent's transcript before repeating them.
7. Declare every cap: sampling, top-N, early stopping, and every subagent that failed, was denied a tool or returned nothing.
8. A check is only as current as the thing it checked. Stamp platform, library, legal and data claims with the version or date they were verified against.
9. Stop a loop when it stops producing new signal. Effort spent is not a stopping condition.
10. Write for the person who reads the result, in the voice of the person who signs it.

## Triage Gate

Questions, advice, calculations, recommendations and short writing are answered under the always-on rule, in the main conversation (its In this conversation section), and never reach this file. If one did, answer it under the rule. This file is for work with many parts: an audit, a review, a change across many files, a research report, a build. On 26 September 2026, seven single questions run through this machinery took a median of 494 seconds against 19 without the plugin, and blind graders preferred the plain answer in five of them: labels, bookkeeping and progress notes buried the substance, and one reply held no answer at all.

Consequence sets how strong each check must be: anything bound for a filing, a diagnosis, a paper or a contract needs the primary source. The amount of work sets the scale: fan out only when there are more items than one agent can check well.

## Task Record

Build this record before loading deep modules. Keep it in working notes or the plan artifact, not in the reply.

```yaml
deliverable: answer | review | audit | fix | build | research | report | writing
consequence: passing | relied-on | permanent | published-under-a-name | safety
domains: []            # software, law, medicine, statistics, colour, ...
artifacts_present: []  # none, text, files, repo, running-app, images, documents, audio, data
checkable_surface: []  # what can be run, rendered, retrieved, recomputed or measured here
missing_inputs: []     # inputs the answer depends on that were not supplied
tools_available: []    # browser tools, run_command, search_web, subagents: confirm, do not assume
scale: quick | standard | full | exhaustive
```

A missing input that decides the answer is handled in the order the always-on rule's item 6 sets (`01-evidence.md`): inferred where the request shows it, and said so in the sentence that depends on it; otherwise what holds whatever its value, and the answer for each value when the values are few, come before the deciding question, asked with `ask_question` when the session is interactive. A question alone is right only when nothing useful holds without the input, such as a review of a document never attached or a build failure with no log. When the request itself looks truncated or incomplete, ask or stop and say what is missing; never search shell history, other conversations or running processes for it. Fill `artifacts_present` from the request: look inside the workspace only when the request names files, a folder or a project, and never outside it unless the person names the path. On 26 September 2026 two runs given a self-contained question walked up from an empty workspace and read a benchmark's answer keys. Confirm `tools_available` before planning verification. The agy CLI has no browser tools, and in a headless run a denied command discards the whole turn while reporting success, so a check that needs `run_command` there needs a grant first (`13-platform.md`).

## Scale

Pick the scale from `consequence`, state it, with the reason, in the report's Coverage section, and change it only when a check fails in a way the plan did not expect. The report states any departure from these defaults.

| Scale | Use When | Fan-Out | Verification | Critic | Stop Rule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| quick | The deep task turns out to be one or two claims | None | Items 3 and 4 of the always-on rule's opening list | None | After the check |
| standard | Someone will rely on a deliverable with several parts | 2 to 4 finders or readers | 1 refuter per load-bearing claim, plus any runnable check | One pass before the report | 1 dry round |
| full | Audits, migrations, and anything bound for a filing, diagnosis, paper, contract or public tracker | 4 to 8 finders, each on a different search angle | 3 refuters or 3 lens verifiers per finding, majority to survive | Every round | 2 dry rounds, 5 rounds maximum |
| exhaustive | The user asks for everything, or the work is safety-relevant | One finder per item of the discovered work list | Lens panel plus every runnable check | Every round, plus a final judge | 2 dry rounds, ceiling declared up front |

## Module Loading Matrix

| Module | Load When |
| :--- | :--- |
| `01-evidence.md` | Always, above quick scale |
| `02-evidence-traps.md` | Subagents, user-supplied files, platform documentation, or an instrument you built are involved |
| `03-domain-checks.md` | The claim sits outside software, or the independent check is not obvious |
| `04-runtime-verification.md` | The work has a running or rendered surface |
| `05-acceptance.md` | Before reporting anything as passing, and whenever you write a test, gate or checklist |
| `06-perceptual-gates.md` | A person will look at the result: a scene, page, chart, image or layout |
| `07-subagents.md`, `08-delegation.md` | Before the first `invoke_subagent` or `define_subagent` call |
| `09-orchestration.md` | Standard scale and above, to pick a pattern and set up the ledger |
| `10-iteration.md` | Before starting any correction or refinement loop |
| `11-findings.md` | The deliverable is a bug report, audit, review or anything published under a person's name |
| `12-prose.md` | Every artifact a person will read |
| `13-platform.md` | The task depends on Antigravity behaviour, or a tool, hook, skill or permission does something unexpected |
| `14-checks.md` | The work holds Chinese regulated verse or couplets, a haiku, tanka, senryu or sijo, amounts converted across 万, 億, 만, lakh or crore, or dates for zh-CN, ja or ko readers |

## Phases

Run multi-phase work as separate fan-outs and read each result before planning the next phase, because the scout results usually change the work list.

1. Discover the work list with real tools, inside what the request names: files, routes, statutes, papers, ledger lines, claims. For files on the agy CLI, send `gravitas-scout` (`09-orchestration.md`).
2. When the territory is large, send readers over its parts and merge their answers into a map.
3. Get the independent check ready before it is needed: the app running, the source pulled, the data loaded, the harness validated against a known answer.
4. Fan out one specialist per item or dimension, with a charter narrow enough that its result can be checked.
5. Verify each finding as it arrives. Wait for the whole set only for deduplication, an early exit on zero, or a comparison across findings.
6. Have a completeness critic read the ledger and name what was never searched, opened, run or verified. What it names becomes the next round.
7. Merge, deduplicate, rank by severity, and report tiers, gaps and failed subagents.

## Output Assembly

The always-on rule's limits on a reply hold here too. The reply never contains raw subagent output, progress or status lines, tier labels, coverage or scale sections, agent names, transcript or cache paths, or search-redirect links; the one status line allowed is the single holding line a wait needs (`08-delegation.md`). Never end a turn while a subagent is running unless a `schedule` timer is pending. At standard scale and above, the refuters and the critic take the place of the rule's Second Opinion, so do not also start `gravitas-reviewer` on the report. At quick scale the reply follows the always-on rule alone.

At standard scale and above, write the report to a file in the workspace or artifact folder, mapped to these sections in this order, dropping any that are empty. The reply gives the verdict and the findings that matter in plain words and names that file. For machine-readable output, emit records that match `schemas/finding.schema.json`. Run `scripts/provenance_check.py` on the report and fix every `FAIL` before replying (`01-evidence.md`). Write the report before the final reply and before waiting on the last subagent, because a final turn can be lost after the work is done: a 13-minute audit with 7 subagents ended in a safety-filter block instead of its report, and only its ledger file survived.

1. The answer or verdict in one or two sentences, with its tier.
2. Findings ranked by severity, each with its tier and provenance in the same sentence.
3. Missing inputs and how the answer changes with them.
4. Coverage: the scale used, what was checked, what was not, every cap, and every subagent that failed, was denied a tool or returned nothing.
5. What would change the conclusion, for any claim with no independent check.

Name the file, the line, the command, the number, the version and the date. Replace "verified" with what was run and what it returned, and "the tests pass" with which tests, how many, and which one was watched failing first.
