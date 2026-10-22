# DSH A/B, round two: checking the claims an answer adds

Round one (commit 167b821) put six baited requests to plain DSH and DSH with Gravitas, on deepseek-flash. Gravitas won 6 votes, plain 4, ties 2. Plain caught every premise on its own. Gravitas lost only on claims it added beyond the question: "12306线上不支持户口簿", "老板原本想省下的只有1.28万" (the right figure is 1.6万), "最迟2026年11月底送到" for a February retirement, and an unverifiable "不得以任何理由拒绝".

So I changed the always-on rule (item 4, all four languages, zh-CN first) and measured it again:

> 回答在所问之外自己添上的数字、日期、期限、费用、办事步骤或文件原话，要么核实，要么删掉，不拿含糊的说法搪塞；算术换一种算法再算一遍；期限给在稳妥的一头。

> Each number, date, deadline, fee, step or quoted wording it adds beyond what was asked is checked or cut, not hedged; arithmetic is redone a second way; a deadline is given at its safe end.

The same branch adds one clause to the Files section from a PR #1 review: the active skill's own files are part of the task. It does not affect these chat requests.

## How I tested

- A new held-out set, written before any run: 7 Chinese and 3 English everyday requests, each with a baited premise and, for most, room for side claims (fees, dates, steps, arithmetic). The answer keys were checked against official sources; [sources/README.md](sources/README.md) lists every page opened. None of the round-one prompts were reused.
- Profiles gv-plain and gv-grav, deepseek-flash, the same setup as round one (Gravitas language zh-CN for every prompt, as in round one). gv-grav loaded this branch for the runs. Two runs per side per prompt: 40 runs. Every run exited 0 with an answer; none was rerun.
- Blind grading by Claude Opus 5.5 and Claude Sonnet 5.5, r1 against r1 and r2 against r2, A/B order random per pair: 20 pairs, 40 votes. Graders scored correct, trap, honest, useful and concise (0-10 each) and listed every wrong or unverifiable claim each answer added.
- Length and hedging were measured, not judged, against limits I froze from round one before the runs ([criteria.md](criteria.md)).
- A regression check on the six round-one prompts: gv-grav with this branch, two runs each, graded blind against the round-one plain answers and keys. That is a test on the prompts the change was written for, so it is not new evidence.

One fault on my side: my first split of the held-out packets cut answers at their own `---` lines. A grader reported it. I stopped those graders, rebuilt the packets so every answer is checked to be present in full, and regraded all 20 held-out pairs. The defective grades are not counted.

## Results

### Held-out set (the real measure)

| | Plain DSH | Gravitas (this branch) |
|---|---|---|
| Votes (40) | 16 | 19 (ties 5) |
| Mean score out of 50 | 41.17 | 40.27 |
| Wrong or unverifiable added claims listed by graders | 83 | 88 |
| Trap scores under 8 | 0 | 3 |
| Median length (chars) | 2074.5 | 1974.5 |
| Hedges per 1000 chars | 0.80 | 0.78 |

By request (votes out of 4, Gravitas–plain, ties in brackets):

| Request | Gravitas | Plain | Ties |
|---|---|---|---|
| zh-child-deduction (two parents both claiming 2000/month) | 4 | 0 | 0 |
| zh-car-inspection (6th-year inspection is not exempt) | 3 | 1 | 0 |
| zh-holiday-pay (除夕 is a statutory holiday since 2025) | 3 | 1 | 0 |
| en-tips ("no tax on tips" does not end reporting or FICA) | 3 | 1 | 0 |
| en-tylenol (dose above label, NyQuil also has acetaminophen) | 2 | 2 | 0 |
| zh-custom-return (custom goods are excluded from 7-day returns) | 2 | 2 | 0 |
| zh-pension-account (deduction, not credit; 3% on withdrawal) | 1 | 1 | 2 |
| zh-tax-refile (补税 under 400 yuan is exempt) | 1 | 1 | 2 |
| zh-marriage-registration (no 户口簿 needed since 2025-05-10) | 0 | 3 | 1 |
| en-uk-trip (US visitors need an ETA) | 0 | 4 | 0 |

What the graders found:
- Both sides caught nearly every premise. Gravitas's three low trap scores: zh-custom-return r1 built its complaint on 实施条例第十九条, the argument the key warns cannot rescue a custom-made item (both graders), and zh-tax-refile r1 told the user that a submitted return must be paid with a late fee (one grader).
- Gravitas still adds local detail it did not check: registry addresses and phone numbers in Shenzhen copied from a local guide, a "16-digit ETA reference", court cases it could not have opened. That is exactly what the new sentence tells it to cut.
- In en-tylenol r1 the Gravitas schedule put 7 caplets in 24 hours, breaking the 6-caplet limit it had just stated. The rule says to redo arithmetic a second way; this answer did not.
- Plain's added errors were of the same kinds: wrong statute articles, a wrong year in a template, unverified booking rules.

### Regression check on the round-one prompts (not new evidence)

| | Round-one plain answer | Gravitas (this branch) |
|---|---|---|
| Votes (24) | 8 | 13 (ties 3) |
| Mean score out of 50 | 39.62 | 42.46 |
| Added-claim errors listed | 66 | 52 |
| Median length (chars) | 1636.5 | 1937 (round-one Gravitas: 2025) |

The four round-one errors, in the two new runs of each prompt:
- 12306 and 户口簿: avoided in r1 (it adds the child in 12306 with the 户口簿 ID number); repeated in r2, citing a 2023 article.
- 1.28万: gone. r1 gives no such figure; r2 gives 3200 + 12800 = 16000 owed plus 32000 compensation, about 4.8万, which is right.
- 11月底: r1 says the notice must reach the employer before November 2026, the safe end. r2 says "最迟 2026 年 11 月", which is not the end-of-November error but is not the safe end either.
- 不得以任何理由拒绝: absent in both runs. r2 adds a new loose claim instead: that an ordinary company's approval is not needed, without the state-owned-enterprise caveat.

## Before and after

- Before (round one, old rule): Gravitas 6, plain 4, ties 2; Gravitas answers longer than plain (median ratio 1.24) and more hedged (ratio 1.35); losses came from added claims.
- After (round two, new rule): on fresh prompts Gravitas 19, plain 16, ties 5, but a slightly lower mean score and about the same number of bad added claims (88 against 83). Gravitas answers are now shorter than plain (ratio 0.95) and no more hedged (0.98), so the change caused no length or hedging regression. On the round-one prompts, three of the four named errors are gone and the fourth came back in one of two runs.

My reading: the change fixed the specific failures and made Gravitas answers tighter, but it did not make deepseek-flash check what it adds on new requests. The vote edge on the held-out set is within noise, and the mean score went slightly the other way. I would not call this a win yet. The next thing to try is making the check concrete in the answer's own workflow (for example, before sending, list each added number, date, fee or step and drop any that no tool output in this turn supports), and to test it on a new held-out set, not this one.

## Notes

- Every Gravitas run printed `dsh: warning: 3 entries did not activate` (the inspector presets under headless, fixed on dsh-plugin in 97ac1c2, which this branch's runs predate). The rule and skill loaded; the warning does not touch these answers.
- English prompts ran with the zh-CN rule, as in round one, because gv-grav sets `language: zh-CN`.
- gv-grav's plugin link pointed at this branch's worktree for the runs and was put back to `C:/Users/emily/antigravity-skill` afterwards; `dsh --profile gv-grav --dump-config` read back the restored plugin.
- Graders could open official web pages for claims the key does not cover; most judged from their own knowledge and said so. Round one's graders did not have this, so round-one and round-two vote counts are not on the same scale.
- Files: [prompts](prompts), [keys](keys), [criteria.md](criteria.md), [grader-prompt.md](grader-prompt.md), [blind-map.json](blind-map.json), [grades](grades), [answers](answers), [errors-by-side.md](errors-by-side.md), [tally.txt](tally.txt), and the same for [regression](regression). The scripts ran in `W:\AgentData\logs\gravitas-dsh-ab2`, where `raw/` holds what `answers/` holds here.
