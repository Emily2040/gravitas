> **言語について：** この参照ファイルは現在英語のみです。中核の `SKILL.md` は日本語化済みで、ここは必要に応じて読み込む詳細部分です。翻訳は進行中です。

# Verification

How to promote a claim up the evidence hierarchy using Gemini's vision and Antigravity's runtime tools, instead of voting on text.

---

## Observe-first

The default for anything with a rendered or running surface.

Text review answers "does the code look correct." That is the wrong question. The right one is "does the thing do the right thing," and you can go and look.

1. Get it running. `restart_dev_server`, then `open_browser_url`.
2. Capture the baseline before the change: `capture_browser_screenshot` and `capture_browser_console_logs`.
3. Make the change.
4. Capture the same surfaces after.
5. Hand both captures to a fresh `MODEL_TIER_PRO` subagent whose only charter is to describe what differs and judge whether the difference is the intended one. It must not be the agent that made the change.

The visual critic catches a class of defect that is structurally invisible to code review. Overlapping elements. Text clipped by a container. Colour that fails contrast. An element rendered off-screen. A layout that collapses at 400px. A spinner that never resolves. A control that exists in the DOM and cannot be seen by a human.

Read the console every time. A runtime exception inside a component that rendered correctly is the most common thing a screenshot-only check misses.

---

## Contract verification

For any API call, fetch, form submission or request.

Do not read the client, read the handler, and reason about whether they agree. Exercise the path and read the wire.

- `browser_list_network_requests` shows what actually fired, in what order, how many times.
- `browser_get_network_request` shows the real method, headers, payload, status and response body.

This settles what text review can only guess: the double submit, the request that never fires, the field the client sends and the server ignores, the 200 carrying an error body, the retry storm.

---

## State-exercise verification

For any claim about behaviour under specific conditions.

Static review reasons about empty states, error states and loading states, and is frequently wrong, because those paths are the least exercised during development. Drive them instead.

- `execute_browser_javascript` forces state directly.
- `browser_input`, `browser_click_element`, `browser_select_option` walk the real flow.
- `browser_resize_window` tests responsive breakpoints instead of reading media queries.

Screenshot each state and have a critic look at it.

---

## Target-diff verification

When a visual specification exists: a mock, a design, a reference implementation.

Use `generate_image` to synthesise the intended result, or take the provided reference, and give a visual critic both it and a screenshot of the implementation. Ask for a structured list of concrete differences in spacing, weight, alignment, colour and proportion.

This converts "does it look right", which a text agent cannot answer at all, into a checkable comparison.

---

## Images as input, not just output

Gemini reads images natively. Treat any visual the user supplies as first-class evidence rather than context to acknowledge.

A screenshot of a bug is a reproduction, not a description. A design mock is a specification you can diff against. A photo of a whiteboard is an architecture document. A chart is data. When a user pastes an error screenshot, read the error out of it and act. Asking them to retype it wastes the anchor.

Where a task has a visual anchor, pass the anchor. Describing an image in words to a model that could have looked at it discards information for no reason.

---

## Parallel browser and code

When work spans implementation and behaviour.

`browser_subagent` drives the browser while code specialists work concurrently. The browser agent holds ground truth about what the application does. The code agents change what it should do. Reconcile at each round through `send_message`.

Keep the charters strictly separated. A browser agent that starts editing code, or a code agent that starts guessing at rendering, has lost the independence that made the split worth having.

---

## When observation is impossible

Some claims have no runtime surface. Architectural judgments. Security reasoning about paths that cannot be safely triggered. Questions about code that does not run yet.

These stay at tiers 3 and 4, and only here is adversarial text voting the right tool.

- Spawn independent verifiers, each charged to refute, defaulting to refuted when uncertain.
- Where a claim could be wrong in several ways, give each verifier a distinct lens: correctness, security, performance, reproducibility. Diversity catches what redundancy cannot.
- Require a majority to clear it.
- Report the survivor as a hypothesis with its tier, never as an observed fact.

Before accepting that a claim cannot be observed, check whether a cheap harness would make it observable. A scratch script, one test, a single query. Building that harness is almost always cheaper than a five-agent debate about what the code probably does, and it produces an answer rather than a vote.
