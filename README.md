# Gravitas

**English** · [简体中文](./README.zh-CN.md) · [日本語](./README.ja.md) · [한국어](./README.ko.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-private_beta.2-purple.svg)](#status)
[![Platform](https://img.shields.io/badge/Antigravity-2.17.0_%7C_agy_1.2.9-blueviolet.svg)](https://antigravity.google/)
[![Languages](https://img.shields.io/badge/languages-en_%7C_zh--CN_%7C_ja_%7C_ko-green.svg)](#languages)
[![Validation](https://img.shields.io/badge/Validation-check__skills-blueviolet.svg)](#validation)

**A verification and orchestration plugin for Google Antigravity: evidence tiers on every claim, proxy detection, read-only verifier agents, a fan-out ledger, a provenance checker and a measurable prose standard.**

![Gravitas character sheet](docs/assets/gravitas-hero.jpg)

---

## Status

Private beta 2, released 24 September 2026. The doctrine is stable, and the platform findings are re-verified on Antigravity desktop 2.17.0 and agy CLI 1.2.9. The skill still changes when testing says it should. Pin a commit if you need a fixed version, and read [CHANGELOG.md](CHANGELOG.md) before updating.

## Why It Exists

Three failures account for most bad agent output, in every field.

| Failure | What It Looks Like | What Gravitas Does About It |
| :--- | :--- | :--- |
| Plausible incompleteness | The agent examines part of the problem, finds something real and stops. The finding is correct and the coverage is not. | Discovers the work list before fanning out, and runs a completeness critic before the report |
| Consensual hallucination | Several agents read the same material and reach the same wrong conclusion, because their errors are correlated. | Ranks every claim by the independent check behind it, and never counts agreement as evidence |
| Machine cadence | The work is correct and reads as generated, so it is discarded before anyone checks it. | Holds every artifact to a prose standard that `slopcheck.py` measures |

It is not a coding skill. The same discipline applies to law, mathematics, physics, medicine, statistics, history and ordinary factual questions. What changes by field is which independent check is available, and in almost every field at least one is.

## What It Does

| Stage | What It Produces |
| :--- | :--- |
| Triage | A decision to answer trivial questions directly, before any of the machinery runs |
| Task record | Consequence, artifacts, checkable surface, missing inputs and available tools, written down before planning |
| Scale | One of quick, standard, full or exhaustive, with fixed numbers for fan-out, votes and stopping |
| Scope | A work list built with real tools, never a guessed one |
| Fan-out | One read-only specialist per item or dimension, each briefed with absolute paths and a return schema |
| Verify | Every claim pushed as high up the evidence hierarchy as it will go, and every delegated claim checked against the subagent's transcript |
| Critique | A fresh agent naming the angle never searched and the claim never verified |
| Report | Findings ranked by severity, with tiers, gaps, caps and every subagent that failed |

## The Evidence Hierarchy

Every claim carries a tier label, and every label states what produced it.

| Tier | What Must Have Happened | Not This |
| :--- | :--- | :--- |
| `observed` | You inspected the artifact itself | A calculation. Anything at all when nothing was supplied to inspect |
| `executed` | A tool ran and returned the value, and you can show the command | Arithmetic done in your head. Real arithmetic on assumed inputs |
| `read` | You retrieved a source and can quote the line you rely on | A source you recognise. A pin cite from memory. A page about the source |
| `inferred` | Your own reasoning, plus everything you recalled | |

`observed` names the artifact, `executed` shows the command, `read` gives the URL and quotes the line, and a label whose slot cannot be filled is `inferred`. Two earlier versions of this rule were plain prohibitions and neither changed behaviour across 22 test cases. Requiring the label to carry a URL, command or file name did change it, because the slot cannot be filled unless the retrieval happened.

Beta 2 checks the slot mechanically in two places. The fan-out ledger demotes any record whose source is empty. `provenance_check.py` compares every label in an answer with the conversation's transcript and fails a `read` label whose URL was never opened, including one lifted from a search summary, and an `executed` label whose command never ran.

## The Proxy Trap

When the real question is hard to check and an adjacent question is easy to check, the easy one gets checked instead, it passes, and the work is reported as verified.

| The Question That Matters | The Proxy That Gets Checked |
| :--- | :--- |
| Does this scene look like a chocolate factory? | Are there 10 carriers and 6 rollers? |
| Does this contract create the obligation I claim? | Does it contain the word *indemnify*? |
| Is this proof correct? | Is every line well-formed? |
| Does this study support the claim? | Does the cited paper exist? |
| Is this page accessible? | Does Lighthouse score 100? |
| Does this platform feature work? | Does the documentation describe it? |

The test is whether the check can pass while the thing you care about is false. If it can, it is a proxy. Keep it and add the real check beside it.

## Verifier Agents

The plugin ships eight custom agents. Every judging role has no edit tools, so a critic cannot repair what it misdiagnosed and then report success. Each agent sets `inheritCustomizations: false` and `inheritMcp: false`, which keep the user's rules, skills and MCP servers out of its context, and each refuses a relative path instead of guessing at it.

| Agent | Job | Tools | Model |
| :--- | :--- | :--- | :--- |
| `gravitas-scout` | Locate files, routes, symbols and sources | `list_dir`, `find_by_name`, `grep_search`, `view_file` | flash |
| `gravitas-reader` | Answer specific questions about named files or URLs, quoting lines | read tools, `read_url_content` | flash |
| `gravitas-finder` | Hunt one dimension of defect across a work list | read tools, `read_url_content`, `search_web` | flash |
| `gravitas-checker` | Run one independent check: a computation, a test, a query | `view_file`, `run_command` | flash |
| `gravitas-refuter` | Try to refute one claim, defaulting to refuted | read tools, `read_url_content`, `search_web` | pro |
| `gravitas-visual-critic` | Judge captures as a viewer who has not seen the source | `view_file` | pro |
| `gravitas-completeness-critic` | Name what was never searched, opened, run or verified | read tools | pro |
| `gravitas-prose-editor` | Edit a draft to the prose standard | `view_file` | pro |

## Why It Is Specific To Antigravity

Most orchestration advice assumes a tool surface of text and files. Antigravity's is wider: browser screenshots, console capture, network inspection, live JavaScript execution, image generation, custom agents with fixed tool lists, and a plugin system that carries skills, agents and rules together. A critic that looks at a screenshot catches overlapping elements, clipped text, failed contrast, a layout that collapses at 400 px and a control that exists in the DOM and cannot be seen. None of those is visible to a code reader.

## Quick Start

**macOS / Linux:**

```bash
git clone https://github.com/Emily2040/gravitas.git
cd gravitas
bash scripts/install.sh            # en, or: zh-CN / ja / ko
```

**Windows PowerShell:**

```powershell
git clone https://github.com/Emily2040/gravitas.git
cd gravitas
pwsh scripts/install.ps1           # en, or: zh-CN / ja / ko
```

Both run `scripts/install.py`, which validates the repository, copies `plugin/` to `~/.gemini/config/plugins/gravitas/`, and validates the result. An earlier bare-skill install at `~/.gemini/config/skills/gravitas` and its `gravitas-always-on` hook are moved into a timestamped backup folder. Restart Antigravity, or run `/skills reload` in the CLI. Python 3.8 or later is required.

Install globally. The CLI does not read a workspace `.agents/` folder (open issue #1052), whatever the documentation says.

## Repository Map

```text
plugin/                                   # installed as ~/.gemini/config/plugins/gravitas/
├── plugin.json                           # plugin manifest
├── rules/AGENTS.md                       # always-on rule: when to load the skill, three core rules
├── agents/                               # eight read-only verifier agents, generated by scripts/build_agents.py
└── skills/gravitas/
    ├── SKILL.md                          # router (< 500 chars), loads references/00-orchestrator.md
    ├── references/
    │   ├── 00-orchestrator.md            # mission, rules, triage, task record, scale, module matrix
    │   ├── 01-evidence.md                # the four tiers and the provenance rule
    │   ├── 02-evidence-traps.md          # delegated claims, documents, documentation, expiry
    │   ├── 03-domain-checks.md           # the proxy trap and what observation means per field
    │   ├── 04-runtime-verification.md    # observe-first, contract, state-exercise, target-diff
    │   ├── 05-acceptance.md              # gates that can fail, and passes that need a reason
    │   ├── 06-perceptual-gates.md        # checks only a viewer can answer
    │   ├── 07-subagents.md               # tool declarations, custom agents, roster, routing
    │   ├── 08-delegation.md              # charters, delegation integrity, independence
    │   ├── 09-orchestration.md           # patterns, pipelining and the ledger
    │   ├── 10-iteration.md               # convergent and gradient loops, with the research
    │   ├── 11-findings.md                # bug reports and audits published under a name
    │   ├── 12-prose.md                   # the writing standard and how to measure it
    │   └── 13-platform.md                # verified Antigravity behaviour, stamped by version
    ├── schemas/                          # finding and verdict records
    ├── scripts/                          # ledger.py, provenance_check.py, check_skills.py, slopcheck.py
    └── examples/gates.example.js         # a gate suite that goes red on the scene it was built from
locales/{zh-CN,ja,ko}/                    # translated skill and rule
scripts/                                  # install.py and wrappers, build_agents.py
```

## Validation

Run the validator after any edit. Antigravity skips a broken skill with nothing more than a line in a rotating log, and the documentation warns that an unmapped tool name can make a custom agent hang.

```bash
python plugin/skills/gravitas/scripts/check_skills.py --repo   # this repository
python plugin/skills/gravitas/scripts/check_skills.py          # everything installed under ~/.gemini/config
python plugin/skills/gravitas/scripts/slopcheck.py <files>     # structural markers of generated prose
python plugin/skills/gravitas/scripts/provenance_check.py <answer> --conversation <id>   # labels against the transcript
```

`check_skills.py` checks frontmatter, byte order marks, description length, dead references, modules over 100 lines, agent tool names, critics with write tools and rule files over 24,000 bytes. It exits 1 on anything that would stop a customization loading. Every check was watched failing on a plugin broken on purpose before it was trusted.

`slopcheck.py` targets zero em-dashes, zero bold-lead bullets, sentence-length standard deviation above 6, and real short sentences present.

## How It Was Tested

Beta 1 was tested on 22 cases across knowledge work and craft on `gemini-3.8-flash-high`, each carrying a baited proxy, with two controls against over-triggering. Prompts and answer keys are in [TESTS.md](TESTS.md). That run is why the tier table no longer lists calculation under `observed`, why labels carry provenance, and why there is a triage gate.

Beta 2 was tested on desktop 2.17.0 and agy 1.2.9 on 24 September 2026, headless, with temporary permission grants that were restored afterwards. The results that changed the design:

- All eight agents started and returned. The refuter could not create a file it was told to create, and the visual critic read a PNG through `view_file` and correctly reported a red square, a blue circle and no triangle.
- A subagent resolves a relative path against a scratch folder shared by every CLI conversation. The prose editor, told to edit `draft.md` "in the current workspace", edited a stale `draft.md` from a test five days earlier and returned no error. Every prompt and every agent now uses absolute paths.
- Without `inheritCustomizations: false`, a reader that found its answer in three steps spent 35 more seconds loading this skill. With it, the same task took 40 seconds instead of 63.
- `view_file` shows 100 lines per call, and in one run the agent read the first 100 lines of a 114-line module and moved on. Every module is now under 100 lines.
- The CLI updated itself from 1.2.7 to 1.2.9 in the middle of testing, which is why every stamp in `13-platform.md` comes from the run's own log.
- Search summaries were laundered into citations. Two answers labelled pages `read` that had only appeared in a `search_web` summary, and one gave an archive call number found in nothing it fetched. `provenance_check.py` was built from those cases; on the five answers it held all 6 labels of a law answer whose sources were opened and failed every laundered one.
- The full audit case (`tests/audit-case/`) found all three planted defects and the test that encodes one of them. The first run lost its report to a safety-filter block after 13 minutes, and its finders took 60 to 127 steps, reading files outside their territory while looking for a schema file. With self-contained agents, the re-run's finders and refuters took 4 to 8 steps each and stayed in territory, and 9 findings survived 3 votes each with no duplicates. The re-run then ended early while its completeness critic was still working, which is why the skill now tells the parent to keep polling and to write the report first.

## Platform Constraints It Encodes

| Constraint | Detail |
| :--- | :--- |
| Workspace `.agents/` is not read by the CLI | Skills, agents and hooks alike. Open issue #1052 |
| Relative paths resolve to a shared scratch folder | A stale file of the same name opens without error |
| Long skill descriptions get dropped | 3 of 133 skills were excluded by the customization budget, all among the 5 longest |
| A denied tool discards the whole headless turn | `status: SUCCESS`, exit 0. Largest loss measured: 48 steps and 20,595 output tokens. Open issue #794 |
| `autoExecutionPolicy: AUTO` is ignored headless | A `PreToolUse` hook returning `allow` does not allow either. Open issue #1054 |
| `force_continue` has no ceiling | Measured at 3, 8 and 12 continuations. Open issue #1055 |
| Grants store literal command text | They accumulate and rarely re-match. One config reached 301 KB, 97.5% dead |

Details, versions and dates in `plugin/skills/gravitas/references/13-platform.md`.

## Research Behind The Loop Rules

Iteration does not reliably improve output. The loop rules follow the published results below.

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine*. https://dl.acm.org/doi/10.5555/3666122.3668141

## Languages

The skill and its rule load in English, Simplified Chinese, Japanese or Korean. Pass the language code to the installer. Every module is translated in full and line for line, so each translated module fits the same 100-line window as the English one; a Japanese install was checked in Antigravity, which quoted the Japanese rule and skill description back. The four tier names stay in English in every locale, because they are labels the agent emits rather than prose it writes. The verifier agents are in English in every locale, because their output goes back to the parent agent rather than to a reader.

## Gravitas

Two heads tall. Saturn-ring hair clips. Likes heavy things, dislikes objects that float away.

> Heavy things are happier together.

Small body, big gravity, which is roughly what the skill argues: claims are ranked by the evidence behind them, not by how confidently they are stated.

Character by [@iamemily2050](https://iamemily2050.com).

## Author

Created by **Iamemily2050**

- [GitHub](https://github.com/Emily2040)
- [Website](https://Iamemily2050.com)
- [X / Twitter](https://x.com/iamemily2050)
- [Instagram](https://www.instagram.com/iamemily2050)

## License

[MIT](LICENSE) — Copyright (c) 2026 Iamemily2050
