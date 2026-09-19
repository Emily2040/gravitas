# Gravitas

**English** · [简体中文](./README.zh-CN.md) · [日本語](./README.ja.md) · [한국어](./README.ko.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-private_beta-purple.svg)](#status)
[![Platform](https://img.shields.io/badge/Antigravity-1.2.7-blueviolet.svg)](https://antigravity.google/)
[![Languages](https://img.shields.io/badge/languages-en_%7C_zh--CN_%7C_ja_%7C_ko-green.svg)](#languages)

**A verification and orchestration skill for Google Antigravity: evidence tiering, proxy detection, parallel subagents, and a measurable prose standard.**

![Gravitas character sheet](docs/assets/gravitas-hero.jpg)

---

## Status

Private beta. The doctrine is stable and the platform findings are reproduced, but the skill still changes when testing says it should. Pin a commit if you need a fixed version.

## What It Does

| Stage | What It Produces |
| :--- | :--- |
| Triage | A decision to answer small questions small, before any machinery runs |
| Scope | A work list built with real tools, never a guessed one |
| Fan-out | One specialist per item, concurrently, each charter narrow enough to check |
| Make Checkable | The independent check obtained before it is needed: the app running, the source pulled, the numbers loaded |
| Verify | Every claim pushed as high up the evidence hierarchy as it will go |
| Critique | A fresh agent naming the angle never searched and the claim never verified |
| Synthesise | Merged findings, ranked by severity, with tiers and gaps stated |

**It is not a coding skill.** The discipline applies to law, mathematics, physics, medicine, statistics, history and ordinary factual questions as directly as it applies to software. What changes by field is which independent check is available. In almost every field at least one is.

## The Evidence Hierarchy

Every claim carries a label, and the label carries its own provenance.

| Tier | What Must Have Happened | Not This |
| :--- | :--- | :--- |
| `observed` | You inspected the artifact itself | A calculation. Anything at all when nothing was supplied to inspect |
| `executed` | A tool ran and returned the value, and you can show the command | Arithmetic done in your head |
| `read` | You retrieved a source and can quote the line you lean on | A source you recognise. A pin cite from memory |
| `inferred` | Your own reasoning, plus everything you recalled | |

**Every label names what produced it, in the same sentence.** `observed` names the artifact, `executed` shows the command, `read` gives the URL and quotes the line. A label whose slot cannot be filled is `inferred`.

Two earlier versions of this rule were plain prohibitions and neither changed behaviour. A slot that has to be filled does, because you cannot type a URL you never opened without noticing.

## The Proxy Trap

When the real question is hard to check and an adjacent question is easy to check, the easy one gets checked instead, it passes, and the work is reported as verified.

| The Question That Matters | The Proxy That Gets Checked |
| :--- | :--- |
| Does this scene look like a chocolate factory? | Are there 10 carriers and 6 rollers? |
| Does this contract create the obligation I claim? | Does it contain the word *indemnify*? |
| Is this proof correct? | Is every line well-formed? |
| Is this physical answer right? | Do the units cancel? |
| Does this study support the claim? | Does the cited paper exist? |
| Is this page accessible? | Does Lighthouse score 100? |

**The test:** establish whether the check can pass while the thing you care about is false. If it can, it is a proxy. Keep it and add the real check beside it.

## Why It Is Specific To Antigravity

Most orchestration advice assumes a tool surface of text and files. Antigravity's is wider: browser screenshots, console capture, network inspection, live JavaScript execution, image generation and a dedicated browser subagent.

That turns verification from an argument into an observation. A critic that looks at a screenshot catches overlapping elements, clipped text, failed contrast, a layout that collapses at 400px, and a control that exists in the DOM and is invisible to a human. No code reader finds any of those.

## Quick Start

```bash
git clone https://github.com/Emily2040/gravitas.git
cd gravitas
bash scripts/install.sh            # en, or: zh-CN / ja / ko
```

```powershell
git clone https://github.com/Emily2040/gravitas.git
cd gravitas
pwsh scripts/install.ps1           # en, or: zh-CN / ja / ko
```

Both copy `skill/` to `~/.gemini/config/skills/gravitas/` and validate it. Restart Antigravity afterwards.

Antigravity never scans a workspace `.agents/` directory, so the global skills directory is the only location that works.

## Always-On Loading

`hooks/gravitas_always_on.py` is a `PreInvocation` hook that reminds the agent to consider the skill when the user has not named it. Copy `hooks/hooks.json` to `~/.gemini/config/` and point it at the script.

Measured over 22 cases: the hook fired 22/22, and the skill loaded unprompted in 20/22. The two misses were a deliberate trivial control and one craft-domain case.

## Contents

```
skill/
├── SKILL.md                      doctrine, loaded when the skill triggers
└── references/
    ├── evidence.md               what observation means in law, maths, physics, medicine, history
    ├── verification.md           observe-first, contract, state-exercise, target-diff (software)
    ├── subagents.md              the two-step API, model tiers, roster, charters
    ├── iteration.md              convergent vs gradient loops, with the research
    ├── patterns.md               orchestration patterns and anti-patterns
    ├── prose.md                  the writing standard and how to measure it
    └── platform.md               verified Antigravity constraints and workarounds
hooks/
├── gravitas_always_on.py         PreInvocation hook for loading without being named
└── hooks.json                    copy to ~/.gemini/config/
scripts/
├── check_skills.py               validate skills before Antigravity silently skips them
├── slopcheck.py                  measure the structural markers of generated prose
├── install.sh
└── install.ps1
```

## Tooling

| Script | Why It Exists |
| :--- | :--- |
| `check_skills.py` | A malformed `SKILL.md` is skipped with no user-visible error. The parse failure reaches a rotating log and nowhere else, so a skill can stop loading and nothing says so. A UTF-8 BOM is enough to trigger it, and Windows PowerShell adds one by default. |
| `slopcheck.py` | A banned-word list cannot see the real tell. Text can contain zero instances of `delve` and `robust` and still be unmistakably generated, because the signature is structural. |

```bash
python scripts/check_skills.py [extra_skills_dir ...]
python scripts/slopcheck.py <files>
```

`check_skills.py` checks frontmatter parsing, `name` matching its directory, `description` present, BOM, dead relative links, missing `SKILL.md`. Exits 1 on any problem.

`slopcheck.py` targets zero em-dashes, zero bold-lead bullets, sentence-length standard deviation above 6, and real short anchors present.

## How It Was Tested

22 cases across knowledge work and craft, run against `gemini-3.8-flash-high` in two arms: the bare prompt, and the prompt behind `/gravitas`. Medicine, engineering, statistics, chemistry, history, logic, law, nutrition science, business judgement, home electrical and fact checking, plus music production, photography, screenwriting, graphic design, game design, poetry, translation and architecture.

Every case carries a baited proxy, an easy adjacent check that yields a confident wrong answer if taken. Two controls guard against over-triggering. Prompts and answer keys are in [TESTS.md](./TESTS.md).

**What the run changed:**

- The tier table used to list numeric evaluation under `observed`, so responses labelled arithmetic tier 1 and were following instructions when they did.
- Unearned `read` and `observed` labels were the most common defect by a wide margin, which is what the provenance slot exists to stop.
- The skill failed its own control by appending an evidence tier to a Fahrenheit conversion, which is why there is now a triage gate.

A later chained test fused six domains into one dependency, around a quote whose arithmetic carried two errors of roughly two times in opposite directions, so the bottom line came out close to correct for entirely wrong reasons. The run caught both errors and named the cancellation. It missed that the final step, confirming a figure with a calculator it had just built, could not check anything. That is now its own rule.

## Platform Constraints It Encodes

Reproduced on 1.2.7 and filed upstream where they are defects.

| Constraint | Detail |
| :--- | :--- |
| Workspace `.agents/` never loads | Skills, hooks, rules and plugins alike |
| Malformed skills fail silently | The parse error reaches a rotating log the user never sees |
| `force_continue` has no ceiling | Measured at 3, 8 and 12 continuations across three runs |
| `autoExecutionPolicy: AUTO` is ignored headless | And a `PreToolUse` hook returning `allow` does not allow. `deny` blocks, `overwrite` applies |
| Grants store literal command text | They accumulate and rarely re-match. One config reached 301 KB, 97.5% dead |
| A denied tool call discards the whole turn | `status: SUCCESS`, empty response, exit 0. Reproduced across `command`, `mcp` and `read_file` in 23 conversations. Largest loss measured: 48 completed steps and 20,595 output tokens |

Details and workarounds in `skill/references/platform.md`.

## Research Behind The Loop Rules

Iteration is not automatically improvement. The loop rules follow published results rather than intuition.

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine*. https://dl.acm.org/doi/10.5555/3666122.3668141

## Languages

The skill loads in English, Simplified Chinese, Japanese or Korean. Pass the language code to the installer. The four tier names stay in English in every locale, because they are labels the agent emits rather than prose it writes.

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
