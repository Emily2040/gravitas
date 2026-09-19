# Patterns

Each pattern states the problem it solves, the structure, and the failure it prevents. Compose them freely.

---

## Observe-first verification

The strongest pattern available here, and the default whenever the work has a rendered or running surface. Run it. Screenshot it, read its console and network traffic, and have an independent critic judge what happened.

Specified in [verification.md](./verification.md).

Prevents correctness theatre, where several agents agree about code none of them ran.

---

## Loop-until-dry

Use it when you do not know how many issues exist. Bugs, security findings, dead code, edge cases.

Spawn a round of finders. Then dedupe against everything seen so far, including findings from rounds that the verifiers later threw out. If the round surfaced nothing new, increment a dry counter, otherwise reset it. Stop after two consecutive dry rounds.

Dedupe against everything seen. Not against what survived verification. Otherwise findings the verifiers already rejected resurface every round and the loop never converges.

Prevents fixed-count loops that stop mid-tail, reporting the easy findings and missing the rest.

---

## Multi-modal sweep

One search angle cannot see everything, and which things it misses depends entirely on the angle, so run several at once.

Run finders concurrently. Each searches differently: by directory, by symbol, by call graph, by recent churn, by test coverage, by error string, by rendered output. Each is blind to what the others surface.

The last one is the differentiator here. A visual sweep of every route finds defects that no text search can express a query for, because the defect is a rendering outcome rather than a string.

Prevents the single-angle blind spot. Grepping for a function name never finds the dynamic dispatch that calls it.

---

## Judge panel

The first plausible answer is rarely the best one when the solution space is wide.

Generate N independent attempts from different starting positions: simplest-thing-that-works, risk-first, performance-first, user-first. Score with fresh judges that authored none of them. Synthesise from the winner. Graft the strongest ideas from the runners-up.

Prevents one-attempt-then-polish, which locks in the first framing and iterates inside it.

---

## Perspective-diverse verify

Some findings can be wrong in more than one way.

Instead of N identical skeptics, give each verifier a distinct lens: correctness, security, performance, does-it-reproduce. Require a majority to clear it.

Prevents redundant verification. Three agents asking the same question get the same blind spot three times and call it consensus.

---

## Completeness critic

Run this before reporting. Always.

A final agent reads the whole run and answers one question: what is missing. Which angle was never searched, which claim never verified, which file never opened, which state never exercised, which route never rendered. Whatever it names becomes the next round.

Prevents confident partial answers, which is the most common way a thorough-looking audit turns out wrong.

---

## Staged escalation

Most items are cheap and a few are expensive, so paying the expensive price uniformly wastes most of the budget.

Run a cheap `FLASH_LITE` pass over everything. Promote only what trips a signal. Log the counts both ways, because a promotion rate near zero or near one means the signal is miscalibrated rather than the work being uniform.

Prevents spending a deep-analysis budget uniformly, which leaves hard cases with the same shallow attention as trivial ones.

---

## Anti-patterns

- **Fanning out over a guessed work list.** Discover it first with your own tools. A fan-out over an imagined list produces systematic, confident blind spots.
- **Self-verification.** An agent asked to check its own finding rationalises it.
- **Confirmation-framed verify.** "Is this correct" invites agreement. "Refute this, default to refuted if uncertain" invites scrutiny.
- **Silent caps.** Sampling, top-N or early stopping that goes unstated turns a partial answer into a false claim of completeness.
- **Depth for its own sake.** `enable_subagent_tools` on every specialist produces a deep, slow, unauditable tree.
- **Skipping the runtime.** Reaching for text analysis when the thing is running and could simply be looked at.
