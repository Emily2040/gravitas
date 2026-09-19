# gravitas

**English** · [简体中文](./README.zh-CN.md) · [日本語](./README.ja.md) · [한국어](./README.ko.md)

An orchestration skill for [Google Antigravity](https://antigravity.google/). It runs work across parallel subagents, ranks every claim by how it was established, refuses to accept a convenient proxy in place of the property that matters, and holds written output to a standard that strips machine cadence.

**It is not a coding skill.** The verification discipline applies to law, mathematics, physics, medicine, statistics, history and ordinary factual questions as directly as it applies to software. What changes by field is which independent check is available. What does not change is that one usually is, and that skipping it is how careful-looking work turns out wrong.

Built and tested against `agy` CLI 1.2.7 and Antigravity Hub 2.15.0.

## Why it exists

Three failure modes account for most weak agent output.

Agents look at part of a problem, find something real, and stop. Several agents read the same source and arrive at the same wrong conclusion together. And the result, even when correct, reads as generated and gets discarded before anyone evaluates it.

Fan-out fixes the first. Evidence fixes the second, and more voters never do. A prose standard fixes the third.

## What makes it specific to Antigravity

Most orchestration advice assumes a text-and-files tool surface, because most harnesses have one. Gemini sees. Antigravity exposes browser screenshots, console capture, network inspection, live JavaScript execution, image generation and a dedicated browser subagent.

That changes verification from an argument into an observation. A critic that looks at a screenshot catches overlapping elements, clipped text, failed contrast, a layout that collapses at 400px and a control that exists in the DOM and is invisible to a human. No code reader finds any of those.

The skill ranks every claim by how it was established:

| Tier | Basis |
|---|---|
| 1. Observed | You looked at the running thing |
| 2. Executed | It ran and the outcome was checked |
| 3. Read | The source says so |
| 4. Inferred | An agent reasoned it |

Tier 4 is a hypothesis. Adversarial voting moves a claim within tier 4 and never promotes it.

## Install

Antigravity never scans a workspace `.agents/` directory, so the global skills directory is the only location that works.

```bash
git clone <this repo> && cd <this repo>
bash scripts/install.sh            # en, or: zh-CN / ja / ko
```

```powershell
git clone <this repo>; cd <this repo>
pwsh scripts/install.ps1           # en, or: zh-CN / ja / ko
```

Both copy `skill/` to `~/.gemini/config/skills/<name>/` and then validate it. Restart Antigravity afterwards.

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
scripts/
├── check_skills.py               validate skills before Antigravity silently skips them
├── slopcheck.py                  measure the structural markers of generated prose
├── install.sh
└── install.ps1
```

## Tooling

**`check_skills.py`** exists because a malformed `SKILL.md` is skipped with no user-visible error. The parse failure reaches a rotating log file and nowhere else, so a skill can stop loading and nothing says so. A UTF-8 BOM is enough to trigger it, and Windows PowerShell adds one by default.

```bash
python scripts/check_skills.py [extra_skills_dir ...]
```

Checks frontmatter parsing, `name` present and matching its directory, `description` present, BOM, dead relative links, missing `SKILL.md`. Exits 1 on any problem.

**`slopcheck.py`** measures what a banned-word list cannot see. Text can contain zero instances of `delve` and `robust` and still be unmistakably generated, because the signature is structural: em-dash density, contrastive framing, uniform sentence length, bolded bullet leads, hedge intensifiers, rhetorical questions.

```bash
python scripts/slopcheck.py <files>
```

Targets: zero em-dashes, zero bold-lead bullets, sentence-length standard deviation above 6, real short anchors present.

## Platform constraints it encodes

Reproduced on 1.2.7 and filed upstream where they are defects.

- Workspace `.agents/` customizations never load. Skills, hooks, rules and plugins alike.
- A malformed skill is skipped silently.
- `force_continue` has no iteration ceiling. Measured at 3, 8 and 12 continuations across three runs.
- In headless mode `autoExecutionPolicy: AUTO` has no effect, and a `PreToolUse` hook returning `decision: "allow"` does not allow. `deny` does block, and `overwrite` is applied.
- Permission grants store literal command text, so they accumulate and rarely re-match. One config reached 301 KB, 97.5% of it dead grants.

Details and workarounds in `skill/references/platform.md`.

## Research behind the loop rules

Iteration is not automatically improvement, and the loop rules follow published results rather than intuition.

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine*. https://dl.acm.org/doi/10.5555/3666122.3668141

## Licence

MIT.
