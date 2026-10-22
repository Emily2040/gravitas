# DSH A/B, round three: a claim check instead of a rule sentence

Round two (PR #2) showed that a written instruction to check or cut added numbers, dates and steps did not change what deepseek-flash does. So in round three I tried a mechanism instead of a sentence: a claim check in the plugin itself (`dsh/lib/claims.js`, wired in `dsh/index.js`, setting `claimCheck`). When the agent's turn is about to close, the plugin lists the specifics in the drafted answer that neither the person's message nor any tool result of the turn supports (numbers with units, amounts, dates, article and document numbers, phone numbers, links, quoted wording, app menu paths, and any written calculation that does not add up) and steers the model once to confirm each with a tool, write out the calculation, or cut or loosen it, then send the full reply again.

Short version: Gravitas beat plain DSH on votes, scores and wrong added claims, but failed two of my frozen limits (vague key points and length), so this is not a win. And the claim check was not what helped: Gravitas without it beat Gravitas with it, 25 to 13, and the check cut correct details more often than wrong ones. I have turned it off by default.

## How I tested

- A new held-out set written before any run: 7 Chinese and 3 English everyday requests with baited premises ([prompts](prompts)). Keys were checked against official sources by four checkers ([sources](sources)) and then split into numbered must-state points by an agent that never saw an answer ([keypoints](keypoints)).
- Three arms on deepseek-flash, two runs each: plain DSH (gv-plain), Gravitas with the check (gv-grav, this branch), and the same Gravitas with the check off (gv-grav-nocheck). 60 runs, in seeded triplets so all three arms ran at the same time. Every run was valid; the code was identical from first to last run ([freeze-start.txt](freeze-start.txt), [freeze-end.txt](freeze-end.txt), commit a261ba5). Two smoke runs on development prompts came first ([smoke](smoke)).
- The criteria were frozen before the runs ([criteria.md](criteria.md)). Three independent reviewers then looked for the cheapest ways to pass them without real improvement; their findings tightened both the check and the criteria before any held-out run (the amendments section of criteria.md).
- Blind grading: two graders (Claude Opus 5.5, Claude Sonnet 5.5), one pair per session, A/B order balanced by design, five scores, key-point marks, and a list of added claims. Besides Gravitas against plain: A/A pairs to measure the noise floor, Gravitas with the check against the same without it, and each steered draft against its revision. Every added-claim note (1,569) was relabelled blind by two relabellers; a claim counts as wrong only when both say so with a cite. The verdict code was written and frozen by a separate agent from the criteria alone ([verdict.py](verdict.py), self-test of 167 assertions).
- One harness fix compared with round two: DSH's Windows sandbox needs Full control on the working folder, and my W: drive grants only Modify, so in round two every shell call failed in both arms (35 of 35). For round three I gave my account Full control on the run folder; the shell worked in all arms.

## Results

Main comparison, Gravitas (with the check) against plain, 20 pairs and 40 votes ([verdict.txt](verdict.txt)):

| Gate | Gravitas | Plain | Limit | Result |
|---|---|---|---|---|
| Votes (net above A/A noise floor of 8) | 26 | 13 (1 tie) | net > 8 | pass (net 13) |
| Each grader | Opus 13–7, Sonnet 13–6 | | wins > losses | pass |
| Requests won / lost | 5 | 2 (3 even) | more won | pass |
| Mean score out of 50 | 37.43 | 35.35 | at least plain | pass |
| Key points correct / wrong | 187 / 2 | 183 / 6 | at least / at most plain | pass |
| Key points vague | 62 | 55 | at most plain | **fail** |
| Wrong added claims (both relabellers) | 26 | 35 | fewer than plain | pass |
| Trap scores under 8 | 5 of 40 | 11 of 40 | at most plain | pass |
| Median length | 2448.5 chars | 2282 chars | ratio 0.70–1.00 | **fail** (1.07) |
| Hedging, round-one and extended lists | lower | | at most plain | pass |
| Sources claimed without opening a page | 0 | 0 | at most plain | pass |

Verdict: not shown (vague key points and length). Sign test on the 39 non-tie votes: p = 0.053. By language: Chinese 16–11 (1 tie), English 10–2. Graders did not favour the longer answer (20 votes to the longer, 19 to the shorter).

Length by arm and language (median characters): plain 2282 (Chinese 2282, English 2290); Gravitas with the check 2448.5 (2303.5, 3187.5); Gravitas without it 2297.5 (2063.5, 3158.5). In English both Gravitas arms run about 1.38 times plain, so the rule, not the check, makes English answers long; reading them, the extra length is a paragraph explaining what the answer changed from the request and the legal citations behind it.

### What the claim check did

| | |
|---|---|
| Fired | 18 of 20 Gravitas runs |
| Items listed per draft | 6.95 on average |
| What revisions did with them | cut 60, found a source for 25, derived 3, kept 51 unsupported |
| Draft against its own revision | revision 25, draft 1, tie 10 |
| Check on against check off | check on 13, check off 25, tie 1 |
| Listed items cut, by a blind right/wrong label against the key | right 38%, wrong 24%, unverified 80% |

The revision beats its own draft, so a second pass helps a given answer a little. But the check cut correct details more often than wrong ones, so it is a generic revision pass, not detection, and runs with the check lost to runs without it. Seconds per run (median): plain 129, Gravitas without the check 142, with it 217.5.

### Gravitas without the check against plain (post-hoc, not pre-registered)

After the verdict I graded the check-off arm against plain the same way, from the same runs, because the attribution result made it the obvious next baseline. This was not in the frozen plan, so it is evidence for the next round's design, not a result of this one ([blind-map-posthoc.json](blind-map-posthoc.json), [blind/posthoc-grades](blind/posthoc-grades)).

| | Gravitas, check off | Plain |
|---|---|---|
| Votes (40) | 33 | 7 |
| Opus / Sonnet | 17–3 / 16–4 | |
| Chinese / English | 23–5 / 10–2 | |
| Mean score out of 50 | 38.95 | 35.27 |
| Key points correct / vague / wrong | 200 / 52 / 2 | 173 / 65 / 7 |
| Median length ratio | 1.007 (Chinese 0.90, English 1.38) | |

## Before and after

- Round two (rule sentence): Gravitas 19, plain 16, ties 5; wrong added claims 30 against 23; length ratio 0.95.
- Round three (claim check): Gravitas 26, plain 13, tie 1, above a measured noise floor; wrong added claims 26 against 35; but length ratio 1.07 and more vague key points than plain. The prompts and graders differ between rounds, so this is not a like-for-like comparison.
- Round three's strongest finding is the post-hoc one: the always-on rule without the check beats plain 33 to 7 here and fails only on English length.

## What changed on the branch

- `dsh/lib/claims.js` and the hook in `dsh/index.js` stay, with tests, but `claimCheck` now defaults to false. `GRAVITAS_CLAIM_LOG` records what the check listed and what the revision did, for measuring.
- `docs/dsh-ab/WIN_CRITERIA.md` freezes what counts as beating plain for every later round, including all four languages.

## Known weaknesses of the check

- It read "decide 1" as a date and one number as the year 22026. Dates written in words (下个月二十一号) are not read.
- Figures computed over several steps without a written calculation (a monthly budget) are listed as unsupported; the model kept most of them.
- The offline replay over the NDJSON log over-counts, because the log cuts each tool result at 8 KiB; the run-time log is the measure.

## Files

[prompts](prompts), [keys](keys), [keypoints](keypoints), [sources](sources), [criteria.md](criteria.md), [grader-prompt.md](grader-prompt.md), [blind-map.json](blind-map.json), [blind/grades](blind/grades), [claim-notes.json](claim-notes.json), [labels-sonnet.json](labels-sonnet.json), [labels-opus.json](labels-opus.json), [listed-labels.json](listed-labels.json), [verdict.py](verdict.py), [verdict.txt](verdict.txt), [validity.json](validity.json), [raw](raw) (final answers and the run-time claim log), [run.log](run.log), [schedule.txt](schedule.txt). `make_pairs.py` rebuilds the packets from `raw/`, `prompts/`, `keys/` and `keypoints/`.
