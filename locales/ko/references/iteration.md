> **언어 안내:** 이 참조 파일은 현재 영어만 제공됩니다. 핵심 `SKILL.md` 는 한국어로 번역되어 있으며, 이 문서는 필요할 때 읽는 상세 자료입니다. 번역은 진행 중입니다.

# Iteration

When repeating improves a result, when it degrades one, and how to tell which loop you are in.

---

## The asymmetry

"Keep going until it is perfect" is the most intuitive agentic loop and the most reliably broken one.

Huang et al. (ICLR 2024) define **intrinsic self-correction** as a model revising its own answer "based solely on its inherent capabilities, without the crutch of external feedback," and find that models "struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction."

The mechanism matters more than the headline. A model can usually repair an error once its location is supplied, and cannot reliably find that location itself. The reasoning that produced the mistake is the reasoning being asked to catch it.

So the loop does not fail from too few passes. It fails because each pass had nothing new to work with.

A follow-up result sharpens it. Models detect errors substantially better in other agents' output than in their own, and relabelling the work as coming from another source improves detection on its own. Independence is not ceremony. It changes what gets caught.

---

## Two loops, opposite rules

### Convergent: there is a right answer

Correctness, bugs, build failures, broken behaviour.

Every pass requires a new external signal, and that signal must supply error location. Valid signals:

- a failing test with its assertion and stack trace
- a compiler or type error with file and line
- a runtime exception from `capture_browser_console_logs`
- a visual diff between two screenshots
- a network response that contradicts the expected contract
- a command exit code with its stderr

If a pass produces no new signal, stop. Another round of a model re-reading its own work is the documented degradation case.

Reflexion works for this reason where naive self-critique fails. It reflects on task feedback held in an episodic memory buffer rather than on impressions, reporting 91% pass@1 on HumanEval against 80% for the GPT-4 baseline. Its framework admits external and internally simulated feedback, and its strongest results come from settings where execution supplies the signal.

Terminate when the signal is clean, or when a pass yields no new signal. Then report honestly, including what still fails.

### Gradient: there is only better

Prose, naming, API ergonomics, layout, code clarity.

Self-refinement works here, because no single correct target exists to drift away from. This is the regime Self-Refine was built for.

Terminate on diminishing returns. The measured shape is consistent: the largest gains land in the first one to two rounds, quality saturates around the third or fourth, and past roughly three iterations gains plateau and can reverse. One reported trajectory runs about 62% to 70% on the first correction, about 75% by the third, saturating near 79% by the fifth.

**Three passes by default, five as a hard ceiling.** If two consecutive passes produce only cosmetic change, stop. You are reshuffling.

### Never loop

Unfalsifiable judgments with no external signal available. "Is this architecture right." "Is this secure," where the path cannot be exercised. Iterating here produces increasingly confident prose and no increase in accuracy. Take one independent opinion, label it a hypothesis with its tier, move on.

---

## Making a loop legitimate

Answer these before starting any correction loop. If you cannot, you do not have a loop. You have a rewrite.

1. **What is the external signal?** Name the artifact: this failing test, this console error, this screenshot pair. "I will review it again" is not a signal.
2. **Does the signal localise the error?** If it says something is wrong and not where, get better instrumentation before iterating. A log line, a narrower test, an assertion. Cheaper than another blind pass.
3. **Who is judging?** Not the agent that produced the work. A fresh subagent, defined read-only, handed the artifact as third-party output.
4. **What is the stop condition?** Signal clean, no new signal, or the pass ceiling. Decide before starting.
5. **What happens on failure?** Report what still fails and why. A loop that exits by quietly dropping the goal is worse than one that never ran.

---

## Anti-patterns

- **Iterate until perfect.** No termination condition, no external signal. Burns budget and degrades the answer.
- **Self-critique framed as self-critique.** Asking an agent to review "your previous output" underperforms handing it the same text as someone else's.
- **Looping without new information.** If pass N+1 sees what pass N saw, the outcome is noise.
- **Treating agreement as verification.** Several agents concurring on unverifiable reasoning is correlated inference. It does not raise the evidence tier.
- **Confusing the loops.** Gradient-style "make it nicer" iteration applied to a correctness bug hides the bug under better prose.
- **Unbounded termination-blocking.** Forcing an agent to continue until tests pass is sound only with a hard pass ceiling. Without one, a broken build becomes an infinite loop.

---

## Sources

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine: Iterative Refinement with Self-Feedback*. https://dl.acm.org/doi/10.5555/3666122.3668141
