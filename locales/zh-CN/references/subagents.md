> **语言说明：** 本参考文件目前仅有英文版。核心技能文件 `SKILL.md` 已完整中文化，这里是按需加载的深度细节。翻译进行中。

# Subagents

The API, the roster, and the contracts that keep a fan-out auditable.

---

## The two-step API

A subagent must be declared before it can be dispatched. The runtime is explicit about this: *"Subagent %q defined successfully. It can now be invoked via invoke_subagent"*, and *"at least one subagent spec is required."*

**`define_subagent`** declares one specialist.

- `subagent_name` identifies it for later invocation.
- The charter states what it does and what it returns. Narrow enough that the result is checkable.
- Tools are granted per specialist. Grant only what the charter needs.
- `subagent_model` selects the tier.
- `enable_subagent_tools` lets that specialist delegate further. Leave it off unless the charter actually subdivides.

**`invoke_subagent`** dispatches. `subagent_count` runs N copies concurrently across a work list.

**`send_message`** carries updates between agents. Children return self-contained, reviewable results. They do not narrate progress.

---

## Model tiers

| Tier | Use for |
|---|---|
| `MODEL_TIER_FLASH_LITE` | Mechanical extraction, file triage, breadth sweeps |
| `MODEL_TIER_FLASH` | Finders, readers, browser observers |
| `MODEL_TIER_PRO` | Judges, refuters, visual critics, final synthesis |
| `MODEL_TIER_INHERIT` | Implementation, so work follows the model the user selected |

Paying PRO rates for file triage is waste. Running a visual critic on FLASH_LITE is false economy. `INHERIT` is the correct default for anything that writes code, because silently downgrading the user's chosen model is a decision they did not make.

---

## Agent modes

The runtime exposes `AGENT_MODE_MAIN_AGENT_ONLY`, `SUBAGENT_ONLY`, `SUBAGENT_PRIMARILY`, `BOTH_AGENTS`, `PLANNING`, `EXECUTION` and `VERIFICATION`. `BOTH_AGENTS` is what makes a browser observer and a code implementer run side by side. `VERIFICATION` marks a pass whose only job is to check, which is worth setting explicitly so the transcript shows where verification happened.

---

## Starter roster

A menu, not a mandate. Define only what a task needs. The two columns that matter are write access and tier.

| Specialist | Charter | Write | Tier |
|---|---|---|---|
| `scout` | Locate relevant files, routes, symbols. Return paths and line ranges only. | no | FLASH_LITE |
| `reader` | Read a bounded set of files and answer specific questions about them. | no | FLASH |
| `finder` | Hunt one dimension of defect across the work list. | no | FLASH |
| `browser-observer` | Drive the running app. Capture screenshots, console, network. | no | FLASH |
| `visual-critic` | Compare captures. Judge whether the difference is the intended one. | no | PRO |
| `contract-checker` | Exercise a request path and report the real wire traffic. | no | FLASH |
| `refuter` | Attempt to refute one specific claim. Default to refuted if uncertain. | no | PRO |
| `implementer` | Make a scoped change. The only role with write access. | yes | INHERIT |
| `completeness-critic` | Name what was never searched, verified, opened or exercised. | no | PRO |
| `prose-editor` | Apply the prose standard to a draft. Returns the edited text. | no | PRO |

Two rules hold this together. Only `implementer` writes, which is what makes every observation and judgment role worth trusting. And `INHERIT` is the implementation default.

`scout → implement → verify` is the smallest useful composition and covers most single-defect work.

---

## Charter contracts

A charter that produces unusable output is worse than no fan-out, because it costs tokens and yields something that has to be redone. Four rules.

State the return shape. "Return a list of objects with file, line, claim, evidence-tier." An agent told only what to look for will write an essay.

Bound the territory. Name the files, routes or dimension. Overlapping charters produce duplicate findings that then need deduping, and gaps between charters produce silent misses.

Forbid narration. Children return results to the parent. A child that writes progress commentary is spending tokens on something nobody reads.

Name the evidence requirement. "Every claim must carry its tier, and anything at tier 4 must be labelled a hypothesis." Without this, agents return confident prose.

---

## Independence

A critic that can write is not a critic. It will repair what it misdiagnosed and report success.

Define every observation and judgment role with no write access. Hand critics the artifact as third-party output rather than as "your previous attempt", because error detection measurably improves when the work is not framed as the agent's own. And never route a verification back to the agent that produced the claim.
