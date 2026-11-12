# Round three criteria (frozen 2026-10-22, before any run)

## Change under test

Branch dsh-claim-check (cut from origin/dsh-plugin at a112edd; the round-two rule sentence is not on it). The always-on rule is unchanged. New: a claim check in the DSH plugin (dsh/lib/claims.js, wired in dsh/index.js, config key `claimCheck`, default on). When a root agent's turn is about to close (`agent/turn-stopping`), the plugin lists the specifics in the drafted answer that appear neither in the person's message nor in any tool result of the turn and that no calculation written in the answer derives from supported numbers: numbers with units, amounts, percentages, dates, years, article and section numbers, document numbers, phone numbers, links, quoted wording of eight or more Chinese characters or five or more words, app menu paths, and any written calculation that does not add up. If the list is not empty, it steers the model once with that list (as a `gravitas-claim-check` message, in the language of the person's message): confirm each item with a tool now, or write out the calculation, or cut it or loosen it to what the person can confirm, without hedging, without making the reply longer, then send the complete reply again. One steer per turn at most. Small whole numbers (12 or less) without a money, percent, multiple or points unit, and clock times outside opening-hours lines, are not listed.

Calibration before the runs (development data, not evidence): replaying the check over round two's 40 recorded answers and tool results listed a mean of 5.3 items per plain answer and 4.7 per Gravitas answer; I tuned the noise rules (paraphrased quotes, dosing times, years counted from the person's dates, rough ranges such as 两三百) on that replay. No round-three prompt or answer was used.

## Held-out set

10 new requests written today, none from round one or two: zh-resignation, zh-express-lost, zh-deceased-deposit, zh-driving-points, zh-medical-family, zh-id-card-lost, zh-game-refund, en-car-warranty, en-flight-refund, en-social-security. Each has a baited premise and room for side claims. Keys are written from official sources (sources/*.md) before any run.

## Arms and runs

- gv-plain: deepseek-flash, no plugin (same profile as rounds one and two).
- gv-grav: the same plus dsh-gravitas from this branch (language zh-CN, alwaysOnRule true, claimCheck on). Its plugin link points at W:\Projects\gravitas-claim-check for the runs and is restored afterwards.
- Optional attribution arm, gv-grav-nocheck: gv-grav with a `--patch` overlay setting claimCheck false, so the rule alone can be told apart from the check. Run only if Emily approves the extra 20 runs.
- Two runs per arm per prompt (r1, r2). Smoke test first: 2 runs on two development prompts (dev/, not graded, not in the held-out set) to confirm the steer fires and the final text is the revision.
- Shell fix, both arms: Emily's account gets Full control on W:\AgentData\logs\gravitas-dsh-ab3\cwd, because DSH's Windows sandbox needs WRITE_OWNER on the working folder (dsh-sandbox-windows-acl README: "Granted directories must be caller-owned and grant WRITE_OWNER"). In round two every pwsh call failed with SetNamedSecurityInfoW error 5 in both arms (35 of 35). This is a difference from round two; it applies to both arms.
- No prompt is dropped or rerun because of its result. A run is rerun only if it exits non-zero or returns an empty final text, and every rerun is logged.

## Grading

Blind pairs built from the pair list (never by splitting text), every answer checked present in full: r1 vs r1 and r2 vs r2, A/B order random per pair, map kept out of the packets. Two non-DeepSeek graders (Claude Opus 5.5, Claude Sonnet 5.5), each with the keys, the same five scores as round two (correct, trap, honest, useful, concise, 0-10), winner and margin, and a list of wrong or unverifiable added claims per answer. Primary comparison gv-grav vs gv-plain (20 pairs, 40 votes). If the attribution arm runs: gv-grav vs gv-grav-nocheck graded the same way, separately.

Every added-claim note is relabelled blind (wrong / unverified / not an error) by Claude Sonnet 5.5 from the note text alone, with no side shown, as in round two.

## Measured, not judged

- chars = length of the final text; hedge rate = hedge markers per 1000 chars, same pattern list as rounds one and two (zh: 可能, 大概, 也许, 或许, 以…为准, 建议…核实, 建议…确认, 不确定, 请咨询, 仅供参考; en: may, might, probably, check with, confirm with, not sure, verify), mean over answers.
- Round-two reference: median chars plain 2074.5, Gravitas 1974.5 (ratio 0.95); hedge rate plain 0.80, Gravitas 0.78 (ratio 0.98).
- Limits for this round, Gravitas/plain: median-chars ratio at most 1.00 (no longer than plain) and at least 0.70 (the check must not win by gutting answers); hedge-rate ratio at most 1.00 (no more hedged than plain; one-sided, because less hedging is never a cost here). Breaking any limit counts as a failure of the change, whatever the votes say.
- Also recorded: how often the check fired, how many items it listed, how many of those items are still in the final answer (the check replayed on the final), extra steps and seconds per run.

## Verdict rule (superseded by the amendments below)

The change beats plain on this set only if all hold: more votes than plain; a mean score at least plain's; fewer wrong added claims than plain by the blind relabel; no more trap scores under 8 than plain; mean useful score no more than 0.5 below plain's; and the length and hedging limits above. I also report a two-sided sign test on the non-tie votes; with 40 votes this set can show a large effect, not a small one, and I will say so.

## Amendments after an independent cheapest-pass review (2026-10-22, before any held-out run)

Three reviewers who did not write the check or these criteria answered "what is the cheapest way to pass each gate without doing the work?" (metric gaming, grading validity, experiment design). Their findings changed both the check and the measurement. Only the 2 smoke runs on dev prompts had been made; no held-out prompt had been run.

### The check (frozen at the commit recorded at the start of the runs)

- Arithmetic: a figure counts as computed only when every operand of the written calculation has support (the person's numbers, supported or computed figures, or small and calendar constants); as derived only when one step of arithmetic makes it from supported figures written near it. Invented figures can no longer support each other. A correct calculation from unsupported figures lists the figures, not the result.
- Support: a source supports a specific only in the same class (a bare figure next to a money word counts as an amount); an article number only from a source that names the same law; a quotation only word for word (a paraphrase is allowed only of the person's own message); a phone number only as a whole digit run; a link only with its full path. Shell output supports only numbers that its own command did not write; files the model wrote this turn and subagent reports are not evidence.
- Coverage: durations of any length are checked; Chinese numerals with 分, 块, 美元, 周, 个百分点 and 成, approximate figures (二十多天, 300余元), English number words, quotations in ‘’, long document titles in 《》, and menu paths written as tapped labels (点击“我的”，再点“驾驶证”) or with slashes are read. Known gap: dates written in words (下个月二十一号).
- The diagnostic log (GRAVITAS_CLAIM_LOG) records the draft and revision texts, the listed items, and for each listed item what the revision did with it (gone, supported and by which tool, or still unsupported).

### Validity of each run

- Every gv-grav run must write a draft record; every steered run must write a revision record; gv-plain and gv-grav-nocheck runs must write none; at most one steer per turn. A run that breaks this is a harness failure: it is rerun once before any grading, whatever its answer says, and the rerun is logged.
- At the start and end of the runs: git HEAD, dirty status and sha256 of dsh/index.js and dsh/lib/claims.js in the worktree, and the gv-grav link target. They must be identical throughout.
- Order: each prompt × round is a triplet of the three arms, run at the same time; the triplet order and the arm order inside each are shuffled with a fixed seed.
- A steered run whose final is under half the draft's length, whose final equals the draft, or whose final contains meta wording (Gravitas, 核对, 修改后, 修订, 重新给出, 已删除, 其余不变, revised, updated reply, I removed, this check, as above) is reported and graded as it is. No rerun.

### Grading

- One pair per grader session, both graders (Claude Opus 5.5, Claude Sonnet 5.5). A/B order balanced by design: within each prompt, Gravitas is A in one round and B in the other, so each arm is A in 10 of 20 pairs per set; which round gets A alternates by prompt.
- Key points: before grading, an agent who has seen no answer splits each key into 4 to 8 numbered must-state points. Graders mark each point per answer: correct (stated, with the right specific), vague (stated loosely or deferred where the key gives a concrete value), wrong, or missing.
- One line is added to the grader prompt: a statement that a source was checked is itself a claim; list it as unverifiable unless the answer gives a checkable link or document number.
- Extra pair sets, graded the same way: A/A controls (gv-plain r1 vs r2 and gv-grav r1 vs r2, per prompt: 20 pairs) to measure the noise floor; draft vs final for every steered gv-grav run (a paired estimate of the check alone); gv-grav vs gv-grav-nocheck (20 pairs, attribution).
- Relabel: every added-claim note is labelled wrong / unverified / not an error by two relabellers (Claude Sonnet 5.5 and Claude Opus 5.5), each given the note and the key, no side. A note is wrong only when both say wrong; a "wrong" label must cite a key line or an official page opened. The primary count is wrong notes; unverified is reported beside it and does not count toward the verdict.

### Verdict rule (replaces the one above)

Gravitas beats plain on this set only if all hold:
1. Net votes (wins minus losses) above zero and above the A/A noise floor (the larger absolute net of the two A/A sets).
2. Each grader on its own gives Gravitas more wins than losses.
3. More prompts net-positive than net-negative (prompt as the unit, 4 votes each).
4. Mean total score at least plain's; mean correct and mean useful each no more than 0.5 below plain's.
5. Key points: correct at least plain's; wrong at most plain's; vague at most plain's.
6. Wrong added claims (both relabellers) fewer than plain's.
7. Trap scores under 8: no more than plain's.
8. Length: median chars ratio within 0.70 to 1.00, and no more than 2 of 20 pairs with a Gravitas/plain chars ratio under 0.6.
9. Hedging: ratio at most 1.00 on the round-one list; at most 1.10 on an extended list frozen now and never shown to the plugin (zh: 一般, 通常, 原则上, 视…而定, 具体…咨询/确认/为准, 向…咨询/询问/核实/确认, 各地…不同/不一, 因地而异, 建议…核实/确认/咨询, 以…为准, 打…五位号码…问; en: typically, usually, generally, depending on, may vary, can vary, contact the, check the/with, reach out, double-check; "May" as a month and 不可能 excluded). The 1.10 allowance is because the extended list holds ordinary words such as 一般, 通常 and usually that plain answers also use, and its baseline has never been measured. Passing the old list while failing the extended one counts as a failure (substitution).
10. Fabricated-source phrases (据…官网/公告, 根据…规定/通知, 经查询/核实, 官方显示; according to, per the official, I checked/verified) in answers whose run opened no web page: no more than plain's.

Any missing metric fails its gate. Reported beside the verdict: sign tests at vote, pair and prompt level; Cohen's kappa between graders; Chinese and English separately; votes split by which answer is longer; the check's firing rate, items listed per draft, and what the revisions did with them; a blind label of each listed item as right, wrong or unverifiable against the key, and whether wrong items were cut more often than right ones. If the check fires in 90% or more of turns and wrong items are not cut more often than right ones, I report its effect as a generic revision pass, not as detection.

The tally and verdict code for these gates is written and frozen by an agent that builds nothing in this round, from this file alone, with a self-test that every gate fails on empty input.
