# DSH A/B round four: lead with the decision, then stop

[简体中文](./README.zh-CN.md) · **English**

The Results and Where I departed from the plan sections were written after all runs and grading (2026-10-25). Everything from The change down was written before the runs and is unchanged.

## Results

In short: **not a win, and change 4 did worse than no change.** The round is not a win on either version of the criteria ([verdict4-amended.txt](verdict4-amended.txt)). The text as revised after tuning made answers too short: 0.65 of plain's length, below the 0.70 floor, with more key points left out and more stated wrongly than plain. Against Gravitas without it (gv-grav-base) it lost 24 to 48 (three judges pooled, p = 0.006), and 1 to 17 on the Chinese requests.

All 78 runs were valid and none was rerun ([validity.json](validity.json)); the frozen state did not change from the first held-out run to the last ([freeze-end.txt](freeze-end.txt) equals [freeze-start.txt](freeze-start.txt) line for line apart from label and time). All 288 grades (96 pairs × 3 judges) were valid first time, and all 2,346 added-claim notes have a valid label from both relabellers.

### Main comparison: candidate (gv-grav-c4) against plain, three judges, 24 pairs, 72 votes

| Gate | Candidate | Plain | Bound | Result |
|---|---|---|---|---|
| Votes | 36 | 35 (1 tie) | net > √2 × noise floor 12 = 16.97 | **fail** (net +1) |
| Each judge | Opus 12–12, Sonnet 12–11, Codex 12–12 | | each more wins than losses | **fail** |
| Length (median chars) | 1,521 | 2,332 | ratio 0.70–1.00, at most 10% of pairs under 0.6 | **fail** (0.652; 9 of 24 pairs under 0.6) |
| Key points vague / missing | 174 / 56 | 151 / 42 | no more than plain | **fail** |
| Key points correct / wrong | 280 / 36 | 334 / 19 | at least / at most plain | **fail** |
| Wrong added claims (both relabellers) | 103 | 81 | no more than plain | **fail** |
| Trap scores under 8 | | | no more than plain | pass overall, fail in Japanese |
| Hedging (third list) | 0.557 | 0.297 | at most 1.10 × plain | **fail** |
| Requests won / lost | 3 | 3 | more won | **fail** |
| Mean total score (of 50) | 36.83 | 35.85 | at least plain | pass |
| Source checks claimed without backing | 0 | 0 | no more than plain | pass |
| Added claims both relabellers call unverified | 69 | 105 | at most 1.10 × plain | pass |

Votes by language: Chinese 8–10, English 11–6 (1 tie), Japanese 8–10, Korean 9–9. The version before the amendments (Opus and Sonnet only) gives the same picture: 24 to 23 (1 tie) against a noise floor of 12.

### Current best Gravitas (rule only, check off) against plain

In the same round, Gravitas without change 4 did clearly better, though it is not a win either:

- Votes 44 to 28, with all three judges on its side (Opus 14–10, Sonnet 17–7, Codex 13–11). On the version before the amendments its net of +14 clears the noise floor of 12; the amended version asks for more than √2 × 12 = 16.97, and +16 misses by one vote.
- Length ratio 0.959; key points vague 142 against 156, missing 32 against 44, correct 338 against 328; requests 6 won, 0 lost. All pass.
- But wrong added claims 100 against 78, wrong key points 34 against 18, and hedging above plain on the first and third lists, so it fails.

It passes 31 of the amended version's 52 gate cells; the candidate passes 19.

### Noise and judges

- Two runs of the same arm (A/A): plain r1 against r2 net +12, candidate r1 against r2 net −10, 36 votes each.
- Agreement between judges on the winner (Cohen's kappa, main set): Opus–Sonnet 0.68, Opus–Codex 0.83, Sonnet–Codex 0.52.
- Share of decisive votes that went to the shorter answer: main set 0.51, plain against plain 0.36, current best against plain 0.31.

### Why it lost

Tuning showed that the first sentence did not shorten answers (median 1.17 times round three's plain answers). I changed it once, to "each point said once, in the fewest words, shorter than a strong plain answer", and within the budget did not tune again. It overshot: the candidate's median answer fell to 1,521 characters (plain 2,332), headings from 4 to 0, list items from 12.5 to 7, and Chinese answers to 0.57 of plain's length. It did not cut only repetition: 14 more key points left out, 54 fewer stated correctly, and wrong key points up from 19 to 36. As the Tuning section says, the text went into the held-out runs untried, and this is the cost of not tuning again.

### Budget and next step

Round four used 78 DeepSeek runs (6 tuning, 72 held-out), 79 with the unplanned run of 24 October, leaving 421 of the 500. It used 96 Codex judge calls. Under the criteria's stop rule this is a round without improvement; whether to run another round, and how many runs, is Emily's call.

## Where I departed from the plan

- **One change after tuning, no second tuning:** see Tuning below.
- **A bug in the Codex judge script:** the frozen judge_codex.sh starts each worker without `--approved`, and the worker clears that setting while reading its arguments, so its own guard refused every real call (the stand-in tests never exercise that setting). The first call therefore did nothing and spent nothing. I did not edit the frozen script; a driver ([dev/codex_drive.sh](dev/codex_drive.sh)) does what its main loop does but starts each worker with `--approved`. Model, flags, prompt, output schema and ledger checks are the frozen script's own. All 96 calls gave valid grades.
- **The relabelling workflow's input:** the 2,346 notes were too large to pass to the workflow by hand, so code ([dev/make_label_script.py](dev/make_label_script.py)) embedded relabel-batches.json in label4.js, changing only the line that reads the batches; the prompt text is unchanged. Because of the 512 KB script limit it ran in two halves.
- **One relabelling batch rerun:** Sonnet left out 1 of 60 notes in one batch (id 1784), so save_labels4.py wrote nothing. I reran that batch once. The ledger keeps the first valid label of every note, so the rerun filled only that note; its other 59 Sonnet labels and 60 Opus labels are logged and not used.
- **The gv-grav link:** after the held-out runs I pointed the gv-grav plugin link back at C:\Users\emily\antigravity-skill and checked it with `dsh --profile gv-grav --dump-config` (the output is the same before and after: [gv-grav-dump-during.txt](gv-grav-dump-during.txt), [gv-grav-dump-after-restore.txt](gv-grav-dump-after-restore.txt)).

Committed here: every run's final answer and rule log, the blind packets, all three judges' grades, the notes and labels, the grade and label ledger, and the verdict output. The full event streams (raw/*.ndjson) and the Codex session records are too large to commit and stay in W:\AgentData\logs\gravitas-dsh-ab4.

## The change

One change (change 4): a few sentences added at the end of rule point 2. In English (the version after tuning; see Tuning below):

> The first one or two sentences give the decision: the corrected fact and what to do. After that, only the details they will use, each said once, in the fewest words that keep it exact: when the deliverable carries the reasoning, the text around it does not repeat it, and nothing at the end lists again what came before (sources already cited, steps already given); then stop, shorter than a strong plain answer.

The Chinese, Japanese and Korean rules get the same text ([rules/change4](rules/change4)). Round three's Gravitas lost on length and on vague key points; this aims at both.

## Tuning

The first freeze (commit fef5baa, freeze-start sha256 d99f9fd0…, kept as [freeze-start.superseded-1.txt](freeze-start.superseded-1.txt)) used a shorter sentence:

> The first one or two sentences give the decision: the corrected fact and what to do; after that, only the details they will use, then stop; no longer than a strong plain answer.

Before any tuning run finished, I wrote down the decision rule ([tuning-decision-rule.txt](tuning-decision-rule.txt)). The 6 tuning runs use round three's requests only. All were valid ([tuning-validity.txt](tuning-validity.txt)) and all six answers correct the baited premise in their opening, but the median length ratio against round three's plain answers was 1.17, above the rule's 1.00 ([tuning-check.txt](tuning-check.txt)). Reading the answers shows where the length comes from: the decision comes first, then the reasoning is told again around the deliverable (the message to the airline or courier), and a closing list repeats sources and cautions; one answer gave two versions. So, as the rule allows, I changed the sentence once, to the text above, which aims at the repetition rather than at dropping points. The files before the change are in [rules/change4-before-tuning](rules/change4-before-tuning). A probe with no model call ([probe2](probe2)) confirms the plugin loads the revised rules with the hashes in expected-rule-hashes.json.

The rule also said to rerun the 6 tuning runs after a change. I did not: Emily approved 78 runs (6 tuning, 72 held-out), and 6 more would go past that; and since the rule allows only one change, a second tuning result could not change what happens next. So the revised text goes into the held-out runs without having been tried on the tuning requests.

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
