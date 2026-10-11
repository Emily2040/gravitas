# Module 10 - Iteration

## Purpose

This module covers when repeating a pass improves a result, when it degrades one, and how to tell which loop you are in. Load it before starting any correction or refinement loop.

## The Asymmetry

"Keep going until it is perfect" is the most intuitive agent loop and the most reliably broken one.

Huang et al. (ICLR 2024) define intrinsic self-correction as a model revising its own answer "based solely on its inherent capabilities, without the crutch of external feedback," and find that models "struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction."

The mechanism matters more than the headline. A model can usually repair an error once its location is supplied, and cannot reliably find that location itself, because the reasoning that produced the mistake is the reasoning being asked to catch it. A loop fails because each pass has nothing new to work with, not because it ran too few passes.

A follow-up result sharpens this. Models detect errors substantially better in other agents' output than in their own, and relabelling the work as coming from another source improves detection by itself. Independence changes what gets caught, which is why the critics in this plugin never see work framed as their own.

## Convergent Loops

Use a convergent loop when there is a right answer: correctness, bugs, build failures, broken behaviour, a figure that has to reconcile.

Every pass consumes a new external signal, and that signal has to say where the error is. Valid signals:

- a failing test with its assertion and stack trace,
- a compiler or type error with file and line,
- a runtime exception from the console,
- a visual difference between two captures,
- a network response that contradicts the expected contract,
- a command's exit code with its stderr,
- a numeric disagreement between two independent methods,
- a source that contradicts the claim, quoted.

If a pass produces no new signal, stop. Another round of a model rereading its own work is the documented degradation case.

Reflexion works where naive self-critique fails for this reason: it reflects on task feedback held in an episodic memory buffer rather than on impressions. It reports 91% pass@1 on HumanEval against 80% for the GPT-4 baseline, and its strongest results come from settings where execution supplies the signal.

Stop when the signal is clean or when a pass yields no new signal, and report what still fails.

## Gradient Loops

Use a gradient loop when there is only better: prose, naming, API ergonomics, layout, code clarity. Self-refinement works here because no single correct target exists to drift away from, which is the regime Self-Refine was built for.

The measured shape is consistent. The largest gains land in the first one or two rounds, quality saturates around the third or fourth, and past roughly three iterations gains plateau and can reverse. One reported trajectory runs from about 62% to 70% after the first correction, about 75% by the third, and saturates near 79% by the fifth.

Run 3 passes by default and never more than 5. If two consecutive passes produce only cosmetic change, stop, because the loop has started reshuffling.

## Never Loop

Some judgements have no external signal available: whether an architecture is right, whether a system is secure when the path cannot be exercised. Iterating on these produces increasingly confident prose and no increase in accuracy. Take one independent opinion, label it a hypothesis with its tier, and move on.

## Making A Loop Legitimate

Answer these before starting a correction loop. If you cannot, what you have is a rewrite.

1. What is the external signal? Name the artifact: this failing test, this console error, this capture pair. "I will review it again" is not a signal.
2. Does the signal localise the error? If it says something is wrong and not where, add instrumentation before iterating: a log line, a narrower test, an assertion. That costs less than another blind pass.
3. Who judges? Not the agent that produced the work. A read-only critic from the roster, handed the artifact as third-party output.
4. What is the stop condition? Signal clean, no new signal, or the pass ceiling, decided before starting.
5. What happens on failure? Report what still fails and why. A loop that exits by quietly dropping the goal is worse than one that never ran.

## Loops Driven By Hooks

Antigravity can hold an agent in its loop from outside. A `PostInvocation` hook can return `terminationBehavior: "force_continue"` or `"terminate"`, and a `Stop` hook receives `executionNum`, `terminationReason` and `fullyIdle` and can return `decision: "continue"` with a `reason` that is injected as a system message (read: the built-in `agy-customizations` guide, `docs/hooks.md`, desktop 2.17.0).

`force_continue` has no platform ceiling. Measured across three runs it produced 3, 8 and 12 continuations, where 12 was the test's own limit, and the forced turns were filler because the task was already done. This is filed as issue #1055 on `google-antigravity/antigravity-cli`. Any hook that blocks termination while tests are red needs its own counter, keyed on `executionNum` or `invocationNum`, and a hard ceiling. A defensive hook that catches exceptions and emits a default response turns into an infinite loop if that default continues.

## Anti-Patterns

- Iterating until perfect, with no stop condition and no external signal.
- Asking an agent to review "your previous output" instead of handing it the same text as someone else's.
- Looping without new information, where pass N+1 sees what pass N saw.
- Treating agreement as verification. Agents concurring on unverifiable reasoning is correlated inference and does not raise the tier.
- Confusing the loops. Gradient iteration applied to a correctness bug hides the bug under better prose.
- Termination blocking without a ceiling.

## Sources

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine: Iterative Refinement with Self-Feedback*. https://dl.acm.org/doi/10.5555/3666122.3668141
