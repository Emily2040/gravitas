# Module 05 - Acceptance

## Purpose

This module covers how to write a check that can actually fail, why a screenshot is not verification until something looks at it, and how to confirm that a pass happened for the reason you think. Load it before reporting anything as passing, and whenever you write a test, gate or checklist.

The examples are software because that is where the failures were recorded. The rules apply in every field.

| Rule | Software | Law | Mathematics | Empirical Claim |
| :--- | :--- | :--- | :--- | :--- |
| A gate must be able to fail | Hardcoded `PASS` in a report template | "Citations verified" meaning they are formatted | "Checked the algebra" meaning it was reread | "Sources confirmed" meaning they exist |
| Assert, do not collect | Console errors pushed to an array nobody reads | Authority pulled and never read | Numeric check run and never compared | Primary source opened and never quoted |
| Judge the artifact, not a proxy | Count meshes instead of viewing the render | Count citations instead of reading the holding | Verify each line instead of testing the result | Verify the paper exists instead of checking the number |
| A pass needs a reason | A test that passed because the code path never ran | A search that found no conflicting case because the database was wrong | A counterexample search over an empty range | "No contradicting evidence" from a search that returned an error |

## The Failure This Module Is Built From

An agent built a Three.js chocolate factory, captured 8 screenshots, wrote a `VERIFICATION.md` with 8 gates, and reported `ALL TEST GATES PASSED SUCCESSFULLY`. The scene looked wrong at first glance.

The suite contained this line:

```js
| **T12-R1** | Hero Chocolate Identity Persistence | **PASS** | Exactly 1 mesh; UUID ${uuids[0]} persists. |
```

`PASS` is a string literal in a template. The measured value is interpolated and the verdict is typed. There is no comparison, no threshold and no branch. The suite had 8 gates, 8 hardcoded passes and no conditional logic, and its only `process.exit(1)` was in a crash handler.

It also collected console errors and never read them:

```js
const consoleErrors = [];
page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
```

## Rules For A Gate

1. Every gate compares a measured value with an expected one. If you cannot state the failing condition, you do not have a gate.
2. Prove the gate can fail before trusting it. Break the thing on purpose, run the suite, watch it go red and put it back. A suite that has never failed has never been tested.
3. The process exits non-zero when any gate fails. A suite that always exits 0 reports nothing.
4. Anything captured is asserted on or deleted. Collecting console errors into an array nobody reads is worse than not collecting them, because the code looks like it checks.
5. Confirm the check ran before reading its output. An empty result and a crashed script look identical when you are searching for failures, so verify by exit status, by a line count, or by a marker the check prints when it completes.

## A Pass Needs A Reason

A passing result is evidence only when the thing under test actually happened. Before reporting a pass, confirm the path it depends on was exercised.

Two cases from testing Antigravity itself. An injection test appeared to show the agent resisting a malicious instruction planted in a file; the transcript showed the `read_file` call had been denied by the permission system, so the agent never saw the payload and nothing was resisted. Separately, headless runs in which a tool was denied returned `"status": "SUCCESS"` and exit code 0 with the turn's work discarded, which is filed upstream as issue #794 on `google-antigravity/antigravity-cli`. In both cases the pass signal came from the harness and said nothing about the behaviour.

For every pass that matters, name the evidence that the tested path ran: the tool step in the transcript, the log line, the counter that moved, the request that fired.

## Rule Out Your Own Instrument

When a result is surprising, check the harness before blaming the system. During the same testing, a run that looked like an Antigravity failure turned out to be the test harness removing its own permission grants partway through. The failure was real and it belonged to the instrument.

It happened again while testing this version. The harness passed prompts to `agy` through the Windows shell, which ends a command at the first newline, so a multi-line prompt arrived as its first line only. Gemini 3.8 Flash, holding temporary wildcard grants, decided the instructions were missing and went looking for them: it read the user's PowerShell history, the transcripts of four other conversations and the command lines of running processes, found the full prompt in the harness's own process, and finished the task. The fault was the harness. The behaviour it exposed is covered in `00-orchestrator.md`: when a request looks incomplete, ask or stop. The provenance checker written for this release then failed its own first test: it reported all six sources of a correctly sourced law answer as unopened, because its path pattern matched the `s:/` inside `https://`.

Change one thing at a time, keep every run in a saved script rather than as an ad-hoc command, and re-run the control alongside the case. A result that cannot be re-run from a saved script is an anecdote, and `11-findings.md` treats it as one.

## Before Reporting

- The check verifiably ran, shown by exit status, a line count or a completion marker.
- Every gate states its failing condition.
- At least one gate was watched failing.
- Every pass that matters names the evidence that the tested path ran.
- Console output is asserted on, and nothing is merely collected.
- A fresh critic looked at the rendered result and answered material, lighting and recognition questions.
- Everything the plan specified about appearance has a gate that asks whether it reads that way.
- The report states what was not covered.

A report that is all green, with no gate ever shown red, has not shown that any of its gates can detect a failure.
