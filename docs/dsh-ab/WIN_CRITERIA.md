# What counts as Gravitas beating plain DeepSeek Harness

Frozen on 2026-10-22, after round three's grades and before any round-four run. Every later round is judged on exactly these criteria. If one of them turns out to be wrong, I write down why, and the next round is judged on both the old and the new version; a round only counts as a win if it wins on the old version too.

## The test

- Arms: plain DSH (profile gv-plain) against DSH with the dsh-gravitas plugin (gv-grav), both on deepseek-flash, the same headless setup, two runs per arm per request.
- A fresh held-out set every round: everyday requests (see the four-language amendment below for the minimum per language) with a baited premise and room for side claims, never used before and never used to tune anything. Each answer key is checked against official sources and written, with its numbered must-state points, before that round's runs.
- Any tuning happens on a separate tuning set, never on a held-out set.
- One change per round, named before the runs.
- Blind grading by two non-DeepSeek graders, one pair per session, A/B order balanced by design; added-claim notes relabelled blind by two relabellers against the key.
- The noise floor is measured again every round: plain r1 against plain r2 and Gravitas r1 against Gravitas r2, graded the same way.

## A win needs all of these, overall and in Chinese and in English separately

1. Votes: Gravitas wins minus plain wins is above zero and above that round's noise floor (the larger absolute net of the two A/A sets; per language, the A/A net within that language).
2. Each grader on its own gives Gravitas more wins than losses (overall).
3. Length: the median Gravitas answer is no longer than the median plain answer (ratio at most 1.00), and no more than 10% of pairs have a Gravitas answer under 0.6 of plain's length.
4. Vague key points: no more than plain's.
5. Wrong added claims (both relabellers say wrong, with a cite): no more than plain's.
6. Correct key points: at least plain's; wrong key points: no more than plain's.
7. Trap scores under 8: no more than plain's.
8. Hedging: no more than plain on the round-one hedge list, and at most 1.10 times plain on the extended list from round three.

A missing metric fails its gate. A round that passes everything overall but fails in one language is not a win.

## When to stop and ask

I stop and report to Emily if three rounds in a row bring no improvement on these criteria, or before the runs pass the budget she set (see the amendment below), so she can decide on more spend. Each round's run count is told to her before it starts.

## Amendment, 2026-10-22, before any round-four run: all four languages

Emily asked that Japanese and Korean be tested beside Chinese and English. From round four on:
- every held-out set has at least two requests (three where the budget allows) in each of Chinese, English, Japanese and Korean, with keys checked against official sources of that country;
- each request runs with the plugin's language set to the request's language (zh-CN, en, ja or ko), except in a round that tests the language setting itself;
- a win must hold overall and in each of the four languages separately, on every criterion above that can be measured per language (votes and that language's A/A net, length, vague key points, wrong added claims, correct and wrong key points, trap scores, hedging). A round that wins overall but fails in one language is not a win. Results are reported per language.

Why: Gravitas ships in four languages, and round three tested only two. A win in two languages says nothing about the other two.

The spend for the rounds after round three is up to 500 new DeepSeek runs (Emily, 2026-10-22), counted from round four.

## Where results go

Each round is written up in docs/dsh-ab/round-N with every result, losses as plainly as wins.
