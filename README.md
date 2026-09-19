# gravitas

**English** · [简体中文](./README.zh-CN.md) · [日本語](./README.ja.md) · [한국어](./README.ko.md)

<p align="center">
  <img src="assets/gravitas.jpg" width="640"
       alt="Gravitas, the project mascot: a two-heads-tall character with Saturn-ring hair clips and a moon-and-star hoodie, standing on a macaron">
</p>

> **Private beta.** The doctrine is stable and the platform findings are reproduced, but the
> skill is still being tested against new domains and changes when testing says it should.
> Pin a commit if you need a fixed version.

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

| Tier | What must have happened | Not this |
|---|---|---|
| 1. Observed | You inspected the artifact itself | A calculation. Anything at all when nothing was supplied to inspect |
| 2. Executed | A tool ran and returned the value, and you can show the command | Arithmetic done in your head |
| 3. Read | You retrieved a source and can quote the line you lean on | A source you recognise. A pin cite from memory |
| 4. Inferred | Your own reasoning, plus everything you recalled | |

Tier 4 is a hypothesis. Adversarial voting moves a claim within tier 4 and never promotes it.

**Every label names what produced it, in the same sentence.** `observed` names the artifact,
`executed` shows the command, `read` gives the URL and quotes the line. A label whose slot you
cannot fill is `inferred`. Two earlier versions of this rule were prohibitions and neither
changed behaviour; a slot that has to be filled does, because you cannot type a URL you never
opened without noticing.

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
hooks/
├── gravitas_always_on.py         PreInvocation hook so the skill is considered without being named
└── hooks.json                    copy to ~/.gemini/config/ and point it at the script
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

## How it was tested

Twenty-two cases across knowledge work and craft, run against `gemini-3.8-flash-high` in two
arms: the bare prompt, and the prompt behind `/gravitas`. Medicine, engineering, statistics,
chemistry, history, logic, law, nutrition science, business judgement, home electrical and fact
checking, plus music production, photography, screenwriting, graphic design, game design,
poetry, translation and architecture. Every case carries a baited proxy, an easy adjacent check
that yields a confident wrong answer if taken. Two controls guard against over-triggering.

The prompts and answer keys are in [TESTS.md](./TESTS.md).

What the run changed. The tier table used to list numeric evaluation under `observed`, so
responses labelled arithmetic tier 1 and were following instructions when they did. Unearned
`read` and `observed` labels were the most common defect by a wide margin, which is what the
provenance slot above exists to stop. The skill also failed its own control by appending an
evidence tier to a Fahrenheit conversion, which is why there is now a triage gate before any
of the machinery.

A later chained test fused six domains into one dependency, around a quote whose arithmetic
carried two errors of roughly two times in opposite directions, so the bottom line came out
close to correct for entirely wrong reasons. The run caught both errors and named the
cancellation. It missed that the final step, confirming a figure with a calculator it had just
built, could not check anything, which is now its own rule.

## Platform constraints it encodes

Reproduced on 1.2.7 and filed upstream where they are defects.

- Workspace `.agents/` customizations never load. Skills, hooks, rules and plugins alike.
- A malformed skill is skipped silently.
- `force_continue` has no iteration ceiling. Measured at 3, 8 and 12 continuations across three runs.
- In headless mode `autoExecutionPolicy: AUTO` has no effect, and a `PreToolUse` hook returning `decision: "allow"` does not allow. `deny` does block, and `overwrite` is applied.
- Permission grants store literal command text, so they accumulate and rarely re-match. One config reached 301 KB, 97.5% of it dead grants.
- A denied tool call discards the entire turn, returning `status: SUCCESS`, an empty response and exit 0. Reproduced across `command`, `mcp` and `read_file` denials in 23 conversations. The largest loss measured was 48 completed steps and 20,595 output tokens.

Details and workarounds in `skill/references/platform.md`.

## Research behind the loop rules

Iteration is not automatically improvement, and the loop rules follow published results rather than intuition.

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine*. https://dl.acm.org/doi/10.5555/3666122.3668141

## Gravitas

The mascot, drawn by [@iamemily2050](https://github.com/Emily2040). Two heads tall, Saturn-ring
hair clips, likes heavy things, dislikes objects that float away.

> Heavy things are happier together.

Small body, big gravity, which is roughly what the skill argues. The weight of a claim comes
from what holds it down, not from how confidently it was stated.

## Licence

MIT.
