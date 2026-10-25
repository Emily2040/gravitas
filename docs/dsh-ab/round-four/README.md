# DSH A/B round four: lead with the decision, then stop

[简体中文](./README.zh-CN.md) · **English**

I wrote this page before any round-four held-out run. It records what was fixed in advance and does not change afterwards. When the results are in, I add all of them here, losses as plainly as wins.

## The change

One change (change 4): one sentence added at the end of rule point 2. In English:

> The first one or two sentences give the decision: the corrected fact and what to do; after that, only the details they will use, then stop; no longer than a strong plain answer.

The Chinese, Japanese and Korean rules get the same sentence ([rules/change4](rules/change4)). Round three's Gravitas lost on length and on vague key points; this sentence aims at both.

## Arms

All on deepseek-flash, the same headless setup, the plugin in the request's language:

- plain DSH (gv-plain);
- current best Gravitas: rule only, check off (gv-grav-base);
- current best plus change 4 (gv-grav-c4, the candidate).

## Requests and keys

- 12 new held-out requests, 3 each in Chinese, English, Japanese and Korean, everyday requests with a baited premise ([prompts](prompts)). Never used before and never used to tune anything.
- Each key is checked against that country's official sources ([sources](sources), [keys](keys)) and split into numbered must-state points ([keypoints](keypoints)).
- Two runs per arm per request, 72 held-out runs ([schedule.txt](schedule.txt)), plus 6 tuning runs on round three's requests only ([tuning-schedule.txt](tuning-schedule.txt)).
- Each invalid run gets one rerun; past 8 invalid runs I stop and ask Emily.

## How it is judged

- The criteria are [WIN_CRITERIA.md](../WIN_CRITERIA.md) with the amendments of 2026-10-24 and 2026-10-25. The round is judged on the version before the amendments and on the amended version, and counts as a win only if it wins on both, and in each of the four languages.
- Three judges: Claude Opus 5.5, Claude Sonnet 5.5, and OpenAI gpt-6-astra through Codex CLI, one pair per session, A/B order balanced by design.
- Verdict code: [verdict4.py](verdict4.py) (the version before the amendments, frozen) and [verdict4-amended.py](verdict4-amended.py). Four reviewers who wrote none of it looked for the cheapest way to pass each gate without better answers; the holes they found were closed before any run ([review](review)). Mutation tests are in [mutation](mutation).
- Every file the runs, grading and verdict use is in this commit, and freeze-start records its hash; if any of them changes afterwards, the run script refuses to run.

## One unplanned run

On 2026-10-24, while testing the freeze guard, I started one real plain run by mistake (no final answer; I stopped it). What happened and what I changed is in [incidents](incidents/2026-10-24-guard-test/NOTE.md). It counts against the 500-run budget.
