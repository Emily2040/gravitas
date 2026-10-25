# DSH A/B round five: "plainly" never means more absolute than what it found

[简体中文](./README.zh-CN.md) · **English**

I wrote this page before any round-five DeepSeek run. It records what was fixed in advance and does not change afterwards. When the tuning and held-out results are in, I add all of them here, losses as plainly as wins.

## Why this change

In round four the current best Gravitas (rule only, check off, gv-grav-base) beat plain 44 to 28 on votes and passed length and completeness, but failed three things: wrong added claims 100 against 78, key points stated wrongly 34 against 18, and slightly more hedging ([round four](../round-four/README.md)).

Three independent diagnosis agents traced every error back to the pages its run had opened ([diagnosis](diagnosis)) and agreed:

- Base checked more than plain (351 searches and fetches against 267), but wrote more flatly than its own evidence: "up to 2½ months" became "through March 15", "December 31 to be safe" became the rule itself, "close to zero" became "0 yen".
- In its reasoning, base quoted rule 4's "settled knowledge plainly" as its licence to stop checking and state things flatly.
- About 30 of base's 50 distinct wrong added claims were details written from memory and never questioned; a rule sentence read at writing time has little reach over those.

## The change

One change (change 5): text added to rule 4, after "the thinly known or pattern-built checked or widened to what they can confirm." In English:

> Plainly never means more absolute than what it found: a limit on a figure, date, deadline or rule that the pages it opened or its own working show (a maximum as "up to", a fact of theirs not yet known as "if") stays in the sentence that states it, in a step too; a date or amount chosen to be safe is given as that choice beside the rule it is safer than, with no new figure or reason; and each limit replaces a flat absolute or a bare "may" or "probably", adding no sentence or branch.

The Chinese, Japanese and Korean rules get the same text ([rules/change5](rules/change5), [design/change5.md](design/change5.md)). It asks for no extra checking, no deletion and no length target, which are where rounds two, three and four failed. Its example limit words (up to, if, 最多, 如果, 最大, まで, なら, 최대, 까지, 라면) are on none of the hedge lists.

How it was chosen: four design agents each proposed one change from a different angle (remove a clause, add one sentence, a plugin mechanism, sources and freshness). Three adversarial critics tested each: would deepseek-flash actually change, what passing gate could break, and could the effect show above noise. One agent then picked. A separate team of agents that never saw the rule (W:\AgentData\research\gravitas-round5) ranked "the condition travels with the claim" first, which is essentially the same change.

Honestly: the design agents put the chance of a full win on the new requests at about 5 to 10%. The per-language vote gates (18 votes per language) and the third hedge list are hard to pass whatever the change; wrong key points are expected to fall from 34 to about 22 to 28 (plain 18), and wrong added claims only partly.

## Tuning, two passes

- Tuning uses round four's 12 requests only: 12 gv-grav-c5 runs per pass, compared with round four's existing plain and base answers (two runs each); no new plain or base runs.
- The decision rule was written before any run ([design/tuning-decision-rule.md](design/tuning-decision-rule.md)): after pass 1 at most one revision (R-a or R-b, both worded in advance); pass 2 decides GO or ABANDON, and ABANDON spends none of the held-out runs.
- Grading: one Claude Opus grader, one answer per session, blind to arm and run, marks every key point against round four's keys and marks 42 "limited key points" as kept, flattened, wrong or absent. The grader is first calibrated on round four's 48 old answers; if calibration fails, the rubric is fixed, never the change.
- The decision is computed by code written by an agent who wrote neither the change nor the rule ([tuning-instrument](tuning-instrument)), reviewed twice.

## Arms and held-out set

- Plain DSH (gv-plain), current best Gravitas (gv-grav-base), and Gravitas with change 5 (gv-grav-c5), all on deepseek-flash with the same headless setup and the plugin in the request's language.
- 12 new held-out requests, 3 each in Chinese, English, Japanese and Korean, each with a baited premise ([prompts](prompts)). Every key was checked against that country's official sources, rechecked by a separate agent, written up with numbered key points and reviewed ([sources](sources), [keys](keys), [keypoints](keypoints)).
- Two runs per arm per request, 72 held-out runs ([schedule.txt](schedule.txt)).

## How it is judged

Exactly as round four: [WIN_CRITERIA.md](../WIN_CRITERIA.md), both the version before the amendments and the amended one, overall and in each of the four languages; three judges (Claude Opus 5.5, Claude Sonnet 5.5, OpenAI gpt-6-astra through Codex CLI). The verdict code is a mechanical port of round four's ([PORT.md](PORT.md), [port-diff.txt](port-diff.txt)): only arm names, paths and the request list changed, every gate and bound is the same, and the self-test counts equal round four's. The Codex judge script's bug is fixed and tested.

## Budget

Emily approved 96 DeepSeek runs (24 tuning, 72 held-out), one rerun per invalid run, stopping to ask past 8, and stopping to ask past 2 invalid runs in a tuning pass. Afterwards 175 runs are used and 325 of the 500 remain. The run script enforces these caps.
