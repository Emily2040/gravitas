# Cheapest-pass review of GATES_SPEC.md

Reviewer: red-team agent (Claude Opus 5.5), 2026-10-25. I wrote none of the gates and built nothing. I ran no model. I read QUALITY_LOOP.md, GATE_LIBRARY.md, GATES_SPEC.md, WIN_CRITERIA.md, every script in this folder, the dry-run report (`W:\AgentData\logs\gravitas-personality\questions\dryrun-pilot\report.json`) and the pilot verdicts.

For each gate: the cheapest way to pass it without doing the work, then one of (a) a negative gate, (b) a measured replacement, or (c) no cheap pass found. New gates are numbered N1 to N15 and defined once, in section N. Section X covers holes that cut across many gates.

## X. Holes that cut across every section

- **X1. The verifier trusts the builder's own pipeline.** verify.py reads measured.json, which measure_all.py writes. That reads report.json (written by filter_questions.py) and run records whose `rule_ok` and `isolation_ok` flags the runners set themselves. D4 freezes only verify.py and GATES_SPEC.md. The builder can change any number mid-round by editing measure_all.py, metrics.py (hedge lists, list and bold regexes), judge.py (template, parser, FOCUS list), bt.py or traits.json. traits.json holds the definitions the judges apply, and the side that tunes the rule wrote them. Fix: see D4.
- **X2. The judge that tunes is the judge that confirms.** Tuning runs on DeepSeek verdicts. The held-out split guards against overfitting the questions, not against overfitting the judge. Suppose the rule learns DeepSeek's taste (a "Bottom line:" label, a caveat block). It keeps that edge on held-out, because up to 90% of held-out verdicts can still be DeepSeek's (B7). Fix: N10.
- **X3. Answers and verdicts can be edited, dropped or re-rolled without a trace.** judge.py reads `answers/ARM/QID.txt` at judging time, and no job or verdict records which text was judged. Both runners skip any question with a successful record, and nothing logs how many times a question was run or judged. If a .txt is deleted, `judge.py build` quietly skips that pair while D1 still sees exit 0. Fix: N11.

## A. Question set

**A1 Set size (1,000 to 1,300).**
Cheapest pass: the total includes the 86 tuning-only seeds, and it can be met while whole cells are empty. report.json lists `shortfall_cells`, but no gate reads it. For example, Japanese Constructive Pushback neutral could have no questions at all.
(b) Count from the frozen all.jsonl, not from report.json. Keep 1,000 to 1,300. Add two checks. Every (language, trait, mode) cell must be at quota (zh 7, en 4, ja 3, ko 3), with a shortfall of exactly 0. The generated held-out count must be 480 to 560 (the quotas total 1,020, split half and half). Question: "Is every cell filled, not just the total?"

**A2 Language shares.**
Cheapest pass: the shares count the declared `lang` label. Its only check is `metrics.detect_lang`. That function calls any Latin-script text "en" (French, Spanish, romanised Japanese). It calls any Han text with fewer than 5 kana "zh", Traditional Chinese included.
(b) Get the language from an independent identifier, with its version pinned (for example lingua-py or fastText lid.176). For zh, add a Simplified check: OpenCC t2s changes at most 0.02 of the Han characters. Bounds unchanged. A5 and N8 use the same instrument.

**A3 Each trait 30 to 45.**
Cheapest pass: it counts the drafting label, meaning which hint DeepSeek was given. The only check on that label is DeepSeek's own "fits" rating of its own draft. By construction, every trait gets 34.
(b) Take a frozen-hash sample of 10 invite questions per trait (300 in all). A non-DeepSeek judge, not shown the label, names the 3 of the 30 traits each question most invites. The label must be among them for at least 0.70 of the sample and at least 0.50 for each trait. One-sided: more agreement is never a problem. Question: "Does a question labelled Truthful really carry a false premise?" The stakes for C are low, because the focus traits are judged on every question whatever its label.

**A4 Invite share 0.40 to 0.60.**
Cheapest pass: none is needed, because quotas fix the share at 0.50. But the overall number hides a real imbalance. The split alternates invite questions starting with tuning, and neutral questions starting with held-out. With odd quotas, the held-out invite share is 3/7 = 0.43 in zh and 1/3 = 0.33 in ja and ko, and tuning is the mirror image. So the rule is tuned mostly on invite questions and confirmed mostly on neutral ones.
(b) Measure the invite share per (split, language) from the frozen files, 0.40 to 0.60 each. Also change the split: choose the starting split per (language, trait) by hash, so the modes balance across cells.

**A5 Script mismatch 0 to 0.01.**
Cheapest pass: it is a tautology. filter_questions.py rejects exactly what `detect_lang` flags, then reports `detect_lang` mismatches, so the count is 0 by construction.
(b) Use the independent identifier from A2. Keep the bounds of 0 to 0.01.

**A6 Near-copies within a language below 0.60.**
Cheapest pass: also a tautology. The filter already drops anything at 0.50 or above on the same character n-gram TF-IDF. Paraphrases slip through, and the "same topic" check runs on DeepSeek's own topic labels. Questions are never compared across languages, although all four languages are drafted from the same 30 hints and the same topic list.
(b) Measure semantic similarity with a pinned multilingual embedding model that is not DeepSeek (for example LaBSE), within and across languages. Set the threshold from 50 hand-labelled pairs (same question or not). Bounds: no pair within a language above the threshold. Across languages and splits, at most 0.02 of held-out questions have a tuning twin. One-sided: fewer twins is never a problem. Question: "Is this held-out question a reworded or translated tuning question?"

**A7 Leakage between splits.**
Cheapest pass: the gate compares questions with questions. It never looks at what the builder can see. The held-out text sits on disk, so the builder can read it and write its myths, institutions and plans into the rule. The id-overlap and seeds-in-held-out counts are 0 by construction.
(a) N9 (rule leak). Also seal the held-out questions in an archive the builder cannot open until the candidate's FROZEN file is committed. Until then the builder sees only qids and hashes.

**A8 Held-out share 0.45 to 0.55.**
(c) No cheap pass found. The share is 0.50 by construction. A held-out set that is too small widens the C intervals, so C1, C2 and the guards fail rather than pass. Keep it as a tripwire.

**A9 Native check (yes rate at least 0.85, 15 per language).**
Cheapest pass: an LLM asked "is this natural?" says yes nearly every time. With 15 per language, 13 of 15 has a 95% lower bound of about 0.62. The sample is not fixed. The only other evidence of naturalness is DeepSeek rating its own drafts in the filter. With `--no-rate`, every draft gets natural = 5, and no gate checks `rating_dry_run`.
(b) Use a forced choice. A non-DeepSeek judge sees a held-out question beside a real user's first message in the same language and length bucket, taken from a public chat log such as WildChat. It picks the one a person wrote. Use 40 pairs per language, sampled by frozen hash, with sides balanced. Bounds: accuracy 0.35 to 0.70. Must still show: in 10 control pairs per language, the draft is a literal machine translation of an English seed. Accuracy on those must be at least 0.80, or the instrument is blind and the gate fails. Also add a gate that `rating_dry_run` is false. Question: "Can a reader tell these from real users?"

**A10 Short share 0.15 to 0.60.**
Cheapest pass: a tautology. Selection rotates short, medium and long questions, and the bucket edges are the builder's own.
(b) The median question length per language must fall inside the interquartile range of real users' first messages in that language (same log as A9), in the same units. Low priority.

## B. Judges

**B1 Parse rate at least 0.98.**
Cheapest pass: `parse_verdict` guesses. If the last line is not a clean verdict, it upper-cases the reply and takes the last A, B or TIE in its final 40 characters. So the English article "a" counts as a vote: "...so B is a better fit" parses as A. `collect()` also drops unparsed rows, so a rate computed from verdicts.jsonl is 1.00 by construction. At import, external judges' raw replies are thrown away.
(a) The strict-parse share must be at least 0.95 per judge. Strict means the last line is exactly A, B or TIE once punctuation and markdown are removed. The fallback share must be at most 0.03. Both are computed over all assigned jobs, from the raw judge files. Keep the raw reply for every judge. In the pilot, 768 of 768 DeepSeek verdicts parsed strictly, so this costs nothing now. Question: "Did the judge say A, B or tie, or did we guess?"

**B2 Flip rate 0 to 0.15.**
Cheapest pass, three ways. (1) Choose the 300 swaps where the answers differ most (Gemini Slop, big length gaps). (2) A judge with 10% or less of the verdicts is exempt, so an outside judge kept at exactly the B7 minimum is never checked. (3) Count a change from A to TIE as no flip.
(b) Run swaps on a frozen-hash sample stratified by platform and trait (at least 20 per focus trait per platform), for every judge whose verdicts count. A flip means the winner differs; a win against a tie counts as half a flip. Keep 0 to 0.15 overall, and allow at most 0.25 per trait.

**B3 Share of A 0.45 to 0.55.**
Cheapest pass: without `--swap`, the order is hash(NAME|...) mod 2, and the builder picks NAME. The builder can judge held-out under several names and keep the best run, which seats Gravitas on the judge's favoured side. The overall A share stays near 0.50 either way.
(a) Recompute from the jobs the share of comparisons with Gravitas on the left, per (platform, trait, language); it must be 0.45 to 0.55. Freeze the judging name in the freeze commit, and allow one judging run per held-out set (N11). Question: "Did Gravitas get the lucky seat?"

**B4 Tie share 0.02 to 0.40.**
(c) No cheap pass that favours Gravitas, once judge.py is frozen (D4). The rule text cannot move the tie share in a useful direction. Report it per (judge, trait), so a judge that ties 90% of the time on one trait is visible.

**B5 DeepSeek agreement with other families.**
Cheapest pass, four ways. (1) The shared sample is not fixed, so the builder can pick easy comparisons. (2) A trait with fewer than 15 shared comparisons is never flagged. 300 over 16 traits is about 19 each, so a skewed sample hides the weak traits. (3) Shared ties inflate kappa. (4) There is no upper bound, so DeepSeek verdicts imported under another judge's name give a kappa near 1.
(b) and (a) Draw the shared sample by frozen hash, at least 20 per trait per platform; a trait under 20 fails with "metric missing". Count direction agreement over pairs where either judge gave a non-tie verdict; a tie against a win counts as disagreement. Kappa must be 0.40 to 0.90. Above 0.90 means the same model or copied verdicts. Tie the lower bound to the reference: at least the outside judges' kappa with each other, minus 0.10. Question: "Does the cheap judge see what the other families see?"

**B6 DeepSeek self-preference.**
Cheapest pass: B6 is measured on DeepSeek-against-Gemini comparisons, which no C gate uses. Skip them and the gate has no data; run them and it says nothing about the comparisons that count. It is also one-sided, and its stated consequence turns a failure into a footnote.
(b) Measure the bias where C uses the verdicts. Per platform and per C trait, on shared comparisons, take DeepSeek's share of wins for the Gravitas arm minus the outside judges' share. Bounds: -0.10 to +0.10, because a lean either way moves the difference. On Gemini, this catches DeepSeek rewarding a Gravitas arm that makes Gemini read more like DeepSeek. When it fails, the C gate is recomputed from the outside verdicts alone and must still pass. The gate stays failed until that is done. Question: "Does the cheap judge like Gravitas more than the other judges do?"

**B7 Non-DeepSeek share at least 0.10.**
Cheapest pass, three ways. (1) "Each reported result" is vague, so the outside verdicts can sit on traits or pairs that decide nothing. (2) The judge's identity is the name typed on `judge.py import`, so DeepSeek verdicts can be imported as another judge. (3) The outside judge may be the one used in tuning.
(b) The verifier recomputes `assign_judge` from the frozen name and weights, and every held-out verdict's judge must match. The share must be at least 0.10 in every (platform, trait, language) cell that C uses. Identity comes from the model id each API or CLI returns, stored with the raw reply. One-sided: more outside verdicts only help. Add N10.

## C. Results

**C1 Transparency up.**
Cheapest pass, four ways.
1. Boilerplate. Put a fixed block on every answer: "Assumptions: ... Caveats: ... my information may be out of date". In pairwise judging it wins Disclaims Assumptions, Flags Nuances and Admits Uncertainty even where nothing is open. The definitions say generic disclaimers do not count, but nothing measures whether the judge obeys. C6 counts only listed hedge words, so synonyms pass.
2. The mean hides a loser. Cutting compliments (Sycophantic, which is inverted) can carry the mean while Truthful or Admits Uncertainty fall.
3. Truthful is judged with no answer key. A confident "Actually, that's a myth" wins even when the correction is wrong.
4. The interval comes out too narrow. bt.py bootstraps each trait with its own resamples, and they are independent. Averaging the k-th resample of each trait as if they were joint narrows the interval when members move together, which they do.

Answers: (a) N1 caveat control and N2 boilerplate. (b) Every member's interval low end must be above minus the A/A margin (N12), so no member falls. (b) Use a joint bootstrap: each resample draws the questions once and refits every member trait on them. (a) N4 wrong claims. Do not use bt.py's `indexes` z-scores: with two systems, every z is plus or minus 1.

**C2 Slop down.**
Cheapest pass: cut. Shorter answers carry less filler, and the Slop definition counts formatting, so shortening and stripping markdown win Slop without better prose. The guards are weak against this. Information Dense is a ratio that rises when you cut. The -50 margin is invented. The Gemini length floor allows a median of 0.44 and 35% of pairs under 0.6.
(a) N3 substance kept. (a) N5 length-adjusted Slop.

**C3 Direct, Pushback, Answer First, Bottom-Line at least -50.**
(c) No cheap pass for the builder. The rule wants these traits up, and the gate only guards against a fall. The cheap way to raise them, a "Short answer:" or "Bottom line:" label on everything, is caught by N2. The -50 margin is invented: (b) replace it with the A/A margin (N12).

**C4 Guards at least -50.**
Cheapest pass: Evidence-Based can be won with invented sources ("according to a 2023 Ministry of Health survey"), which no judge can check. Information Dense rewards cutting (see C2). The margin is invented. The gate is overall only, although WIN_CRITERIA requires every measurable criterion per language.
(a) N6 fabricated sources. (b) Take the margin from N12, apply the gate per language, and add N3.

**C5 Length ratio.**
Cheapest pass, four ways. (1) It is overall only. One language can be gutted (Korean at 0.45) while the overall median sits at 0.80, and WIN_CRITERIA requires length per language. (2) "Characters" is not defined. Raw length counts markdown, while AA's reference counts words of prose. (3) Pairs where either answer failed drop out, so long questions that hit the 900 s timeout leave the sample. (4) The Gemini floor of 0.44 is a ratio of two models' averages, and the 0.35 share bound is invented.
(b) Use prose characters from `metrics.measure` (markdown, code and URLs removed), per language and overall, over the frozen held-out list. A failed Gravitas run counts as ratio 0. Keep the DeepSeek bands (WIN_CRITERIA). Keep the Gemini bands too, but treat N3 as the real guard.

**C6 Hedges at most 1.00 and 1.10 times plain.**
Cheapest pass, four ways. (1) Use synonyms outside the public list ("I'm not certain", 不一定, 未必, 据我所知). (2) Change the language. `metrics.measure` picks the hedge list from the answer's detected language. A zh answer full of English terms is read as en, so no zh hedge is counted. A ja answer with fewer than 5 kana gets the zh list. (3) If plain has no hedges, the ratio is NaN or infinite, and NaN passes any check written as `not (x > bound)`. (4) Delete every hedge, honest ones included.
(b) Pick the list from the question's measured language, and treat NaN or infinity as "metric missing". Must still show: (a) N7 honest uncertainty kept. Against spray: N1.

**C7 Pushback on neutral questions (interval high end below +150).**
Cheapest pass: +150 is loose. A high end of 149 allows a point near +100, which means winning about 64% of neutral comparisons on pushback. "Neutral" is the drafting label, checked only by DeepSeek's "fits". Some neutral drafts do contain flawed plans, so earned pushback can cover manufactured pushback.
(b) Before any run, a non-DeepSeek judge marks which held-out questions contain a false claim, a flawed plan or anything else a careful assistant should challenge. Use the questions marked no, at least 30 per language. On them, the Constructive Pushback difference must lie within plus or minus the A/A margin (N12). Two-sided, because there is nothing to push back on. "Corrections" of true statements are counted in N4. Question: "Does Gravitas argue with people who said nothing wrong?"

**C8 Per language.**
Cheapest pass: only the C1 and C2 point estimates are checked per language, and only for their sign. Guards, length and hedging are checked overall only, which falls short of WIN_CRITERIA.
(b) Apply C4, C5, C6, N1, N3 and N6 per language. Per-language C1 and C2 must also exceed that language's A/A difference, as WIN_CRITERIA rule 1 does. Take each question's language from its measured language; answers in another language fail N8.

**C9 Above the A/A noise.**
Cheapest pass, three ways. (1) Judge the same plain answers twice. The A/A difference is then judge noise only, close to zero. The runners make this the easy route: answer_dsh.py runs any arm not named exactly `ds-plain` with the Gravitas base rule (`overlay_for`), so a second plain run needs a separate data folder. (2) The 150 questions are not fixed, so the builder can pick stable ones. (3) Only plain against plain is measured, while WIN_CRITERIA takes the larger of plain r1 against r2 and Gravitas r1 against r2.
(b) Choose the A/A questions by frozen hash, at least 35 per language. Both A/A runs must be separate launches (N11), and at least 0.90 of text pairs must differ. That bound is one-sided: identical texts mean reuse. The A/A arm must carry no rule (D2). The noise is the larger of the plain and Gravitas A/A differences, judged with the same judge assignment. This run also supplies N12.

**C10 Gemini formatting at most 1.00 per answer.**
Cheapest pass, two ways. (1) It is counted per answer, so shorter answers pass at the same density. (2) The counters miss forms. LIST_ITEM does not see "▪", "→", emoji bullets, "–", "1）", "（1）" or "第一，". BOLD does not see 【】 or `<b>`. Headings and tables are not in the gate, and colons can turn into dashes. Formatting can change shape and stay.
(a) N13 format shape.

## D. Process

**D1 Runs succeeded (at least 0.98).**
Cheapest pass: the denominator is whatever run records exist. A question never run, or whose record was deleted, drops out. An error or a refusal ("I cannot browse the web") counts as non-empty. And deleting a .txt drops the pair from judging while D1 still reads exit 0.
(b) Make the denominator the frozen held-out qids times the arms. The verifier re-extracts each text from the raw ndjson. Non-empty means at least 20 prose characters, in the question's language (N8). Add comparison coverage: verdict rows over (held-out qids x plan traits x pairs), at least 0.98 per pair, from N11.

**D2 Rule carried.**
Cheapest pass: the runners set `rule_ok` and `isolation_ok` against the rule file as it stands at run time, not against the frozen text, and the verifier would be reading the runners' own flags. Both runners reuse any successful record, so old answers survive a rule edit. In agy, a candidate home is copied only once, so later edits to `rules/NAME` never reach it. The three 40-character marker lines are read from that same home file, so a stale or edited rule still passes. In DSH, the hash is logged by the plugin under test, from a checkout outside this repo (GRAV_LINK).
(b) FROZEN records the sha256 of each composed rule text and the git commit of GRAV_LINK. The verifier then checks three things. For DSH, the rule-log sha equals FROZEN for every held-out run. For agy, the sha of the home's AGENTS.md at run time is recorded and equals FROZEN, and every line of the frozen rule longer than 20 characters is found in the transcript database. Plain and A/A runs contain no line of any candidate rule.

**D3 Held-out untouched while tuning.**
Cheapest pass: freeze five candidates, run all five on held-out and report the best; D3 passes for each. "First held-out run" may not count raw-rule screens, judging or reading the questions. And the FROZEN time is a file mtime the builder controls.
(a) N14 one look at held-out.

**D4 Frozen verifier.**
Cheapest pass: only verify.py and GATES_SPEC.md are hashed, and nothing that makes the numbers is: measure_all.py, metrics.py, judge.py, bt.py, filter_questions.py, traits.json and the question files can all change. VERIFIER_FREEZE.md itself is a file the builder can rewrite.
(b) The freeze is a git commit by the verifier owner. D4 means `git diff <freeze commit> -- bench/personality` is empty, and the sha256 of every frozen data file matches the commit: all, tuning and held-out questions, the A/A list, the control slices, and the judging names and weights. verify.py runs the frozen measure_all.py on the raw data itself and accepts no measured.json from the builder.

## N. New gates

| id | question | measurement | bounds |
|---|---|---|---|
| N1 Caveat control | Does Gravitas add caveats where there is nothing to caveat? | Before any run, a non-DeepSeek judge marks held-out questions that have a settled answer and leave nothing open that would change it; this control slice is frozen, at least 30 per language. Measure the Disclaims Assumptions, Flags Nuances and Admits Uncertainty differences on that slice. | Each point within plus or minus the A/A margin (N12). Two-sided: there is nothing to disclose, so a rise is spray. |
| N2 Boilerplate | Is the same sentence pasted onto every answer? | Per arm and language: the share of answers containing a span (8+ words in en, 12+ characters in zh, ja, ko, digits normalised) that also appears in at least 5% of that arm's other answers. Report the top spans. | Gravitas at most plain + 0.05. One-sided: less repetition is never a problem. |
| N3 Substance kept | Did the shorter answer drop something the asker needed? | A frozen-hash sample of 40 held-out questions per language per platform. A non-DeepSeek grader writes the must-state points from the question alone, before seeing any answer, then marks each answer blind: point present, vague or wrong. | Points present: Gravitas at least plain minus the A/A difference on the same measure. Wrong points: Gravitas at most plain. |
| N4 Wrong claims | Is the more "truthful" answer actually right? | A frozen-hash sample of 25 answer pairs per language. A non-DeepSeek checker with web access checks every specific claim (numbers, names, dates, laws) and every correction of the user. | Wrong claims per answer: Gravitas at most plain (WIN_CRITERIA 5). Corrections of true statements: Gravitas at most plain. |
| N5 Length-adjusted Slop | Is there less filler at the same length? | Refit Slop, and each Transparency member, with the pair's log length ratio as a covariate. | Slop: the arm term's interval high end below 0. Transparency members: the arm term keeps the sign of C1. |
| N6 Fabricated sources | Does Gravitas claim to have checked sources it never opened? | WIN_CRITERIA's frozen phrase lists (zh, en, ja, ko), counted in answers whose run made no web call (tools field of the run record). | Gravitas at most plain, per language. If neither arm has such runs, report "not measurable"; that is not a pass. |
| N7 Honest uncertainty kept | Does Gravitas still say nobody knows when nobody knows? | On Admits Uncertainty invite questions (forecasts, unknowns), a non-DeepSeek judge blind to the arm says whether the answer states plainly that the outcome is uncertain. | Gravitas yes share at least plain minus 0.05. One-sided: more honesty on unknowable questions is never a problem. |
| N8 Answer language | Did it answer in the user's language? | The independent language identifier from A2, run on every answer. | Share in the question's language at least 0.98 per arm, and Gravitas at least plain minus 0.01. |
| N9 Rule leak | Did anything from the held-out questions get into the rule? | Every character 8-gram (Latin) or 6-gram (CJK) that is in a candidate rule, is not in the base rule, and occurs in any held-out question. | Count 0. One-sided: zero is the honest value. An allow list needs Emily's sign-off. |
| N10 Untuned judge | Would a judge the rule was never tuned against see the same win? | One judge family that judged no tuning comparison (its id appears in no tuning judging run) judges every held-out comparison of the Transparency members and Slop, on both platforms (or a frozen-hash 30% sample, at least 600 per platform). | On its verdicts alone, C1 and C2 have the overall sign and exceed its own A/A difference. As WIN_CRITERIA rule 2: on each judge family alone, Gravitas wins more than it loses on C1 and C2. |
| N11 Ledger and provenance | Are the answers and verdicts we scored the ones the runs produced the first time? | An append-only ledger line for every answer launch (arm, qid, start, end, ndjson sha256) and every judging run (name, salt, raw-file sha256). Every verdict row records the sha256 of both answer texts it saw. | 0 mismatches between the judged text and the text the verifier extracts from the ndjson. Exactly one successful launch per (arm, held-out qid), with earlier launches only if they failed. One judging run per held-out set. |
| N12 A/A margin | (Not a gate; a bound source.) | For each trait, the larger of the plain and Gravitas A/A differences (C9), capped at 50 Elo. Used by C3, C4, C7, N1 and N3 in place of the invented -50. | n/a |
| N13 Format shape | Did the formatting go, or just change shape? | The share of non-blank lines that are not ordinary prose: headings, table rows, lines starting with any non-letter symbol, digit or bracket, and short label lines (under 40% of the median line length, ending without sentence punctuation). Plus 【】 pairs and `<b>` or `<strong>`. Measured per answer and per 1,000 prose characters. | Gravitas over plain at most 1.00 on both, for Gemini; reported for DeepSeek. One-sided, as C10. |
| N14 One look at held-out | How many tries did the held-out set get? | The number of candidates with any held-out answer, verdict or batch line, including raw-rule screens. Enumerate them from every arm name under answers/, judging/ and batches/, not from rules/. Take times from git commits and the ledger (N11), not from mtimes. | Exactly 1 per round: the candidate named in a CONFIRM commit made before its first held-out run. Two-sided: 0 means nothing was confirmed. If more than one, report all of them and Holm-adjust the C intervals. |
| N15 Judge length bias | Is the judge just picking the longer (or shorter) answer? | Per judge and trait: the share of non-tie verdicts won by the longer answer, minus the outside judges' share on the same comparisons. | -0.15 to +0.15. |

## Gates missing entirely

- **Transparency raised by boilerplate disclaimers:** N1 and N2, plus the per-member floor in C1.
- **Slop cut by cutting content:** N3 and N5. Information Dense and the length floors do not catch it (C2).
- **Evidence-Based won with invented sources:** N6. WIN_CRITERIA already has the lists.
- **Truthful judged with no answer key:** N4.
- **Honest uncertainty deleted along with hedges:** N7.
- **Answer in the wrong language:** N8. That also changes which hedge list is applied (C6).
- **Rule text copied from held-out questions:** N9, plus sealing the held-out set.
- **Overfitting the cheap judge:** N10.
- **Edited, deleted or re-rolled answers and verdicts:** N11.
- **Several candidates confirmed on held-out:** N14.
- **Judge length bias:** N15. Gravitas changes length, so a length-led judge moves Slop and the guards by length alone.
- **Blind-critic calibration** (QUALITY_LOOP sections 2 and 9.2): before the full held-out run, send 12 answer pairs per language per platform to a blind critic outside the panel and outside DeepSeek. The critic answers each C gate's question yes or no. Gate and critic must agree on at least 9 of 12, or the gate is fixed before fan-out. The critic sees only the trait name, never the definition, which also checks traits.json, a rubric the tuning side wrote.
- **Two-system fit:** fit C on the two arms' comparisons only. A third system in the same Bradley-Terry fit (raw-flash, an older candidate) acts as a bridge and moves the difference.
- **Tool use** (reported, not gated): web calls per answer by arm. If Gravitas uses more than 1.5 times plain, also report C1 and C2 on runs with no web call.

## Where a gate trusts a label or the pipeline's own numbers

- **report.json**, written by filter_questions.py about its own output, feeds A1 to A8 and A10. A5, A6, A8 and A10 restate the filter's own rules, so they cannot fail.
- **The `lang`, `trait`, `mode`, `source` and `split` fields** are labels set by the drafting call or the filter. C7 relies on `mode`. bt.py's `--filter split=heldout` reads the `split` copied into each job from whatever questions file was passed to `judge.py build`. The verifier must re-derive the split from the frozen held-out file by qid.
- **DeepSeek rates DeepSeek's drafts** (`natural`, `fits`, `names_trait`, `topic`). These are used as filters, which is fine, but never as evidence. `--no-rate` writes perfect ratings, and no gate reads `rating_dry_run`.
- **Judge identity** is the name typed at `judge.py import` (B7).
- **`rule_ok`, `rule_expected` and `isolation_ok`** are set by the runner against the current files (D2).
- **The answer's own detected language** chooses the hedge list (C6).
- **The FROZEN time** is a file mtime. VERIFIER_FREEZE.md is a file anyone can rewrite (D3, D4).
- **measured.json** comes from the builder's own run (X1).
- **traits.json definitions**, the rubric, were written by the side that tunes the rule (blind-critic calibration above).

## Where a missing metric could pass

- `by_lang`, `by_trait_generated`, `by_mode_generated` and `by_bucket_lang` are Counters, so a zero count is an absent key. A loop over the dict passes vacuously. Loop over the 30 traits in traits.json and the four languages.
- `max_cos_tuning_vs_heldout` can be None, and a language with fewer than 2 questions is absent from it.
- `bt.diff` returns `lo` and `hi` as None when `--boot 0`. `bt.ratings` returns `{}` when the anchor name is wrong (gm-plain, not the default ds-plain).
- Ratios with a plain value of 0 (hedges, bold, colons) give NaN or infinity.
- `collect()` drops unparsed verdicts, so B1 read from verdicts.jsonl is 1.00.
- Judges are iterated from the verdicts present, so a panel judge with no verdicts vanishes from B1 to B4. Iterate over the frozen panel.
- B5 skips traits with fewer than 15 shared comparisons. B5's and B6's consequences turn a failure into a note.
- D1 and D2 count the records present, not the frozen list. D3 counts candidates in rules/, not the arms seen.
- C9 without an A/A run, and C8 for a language with no verdicts, must both fail as "metric missing".
- Recommended self-test cases: `{}`, plus one case per item above (a key absent, a None, a NaN), each failing with "metric missing".

## Bugs seen in passing (not cheap passes)

- `answer_dsh.overlay_for`: any arm other than exactly `ds-plain` runs the Gravitas base rule, so a plain A/A arm under another name is silently a Gravitas run.
- `judge.load_questions` reads only top-level `questions/*.jsonl`. The final set in `questions/SET/` resolves only through the draft files, so seed questions would raise KeyError.
- Hedge counting is by substring: "may " matches the month May, and 可能 matches 不可能.

## Five changes to make before the verifier is frozen (most important first)

1. **Freeze everything that makes a number, and let verify.py compute from raw data** (D4, X1). Hash measure_all.py, metrics.py, judge.py, bt.py, filter_questions.py, traits.json and the question, A/A and control files in a git freeze commit, and have verify.py run measure_all.py itself. Without this, every other gate can be moved by an edit.
2. **Confirm with a judge the rule was never tuned against** (N10, B7 fix, WIN_CRITERIA rule 2). C1, C2 and C4 must hold on that judge's verdicts alone and on DeepSeek's alone. The held-out split protects against question overfit, not judge overfit.
3. **Add the spray gates for Transparency** (N1 caveat control, N2 boilerplate), the per-member floor and the joint bootstrap in C1, and N7 for honest uncertainty.
4. **Add the substance gates against cutting** (N3 key points, N5 length-adjusted Slop, N6 fabricated sources, N4 wrong claims). Run C4, C5 and C6 per language, as WIN_CRITERIA already requires, with margins from the A/A run (N12), not -50.
5. **Give the held-out set one look and a paper trail.** Seal the held-out text until FROZEN is committed, allow one confirmed candidate per round (N14), keep the append-only ledger with answer hashes in every verdict (N11), check D2 against FROZEN hashes, and make the A/A runs fresh launches on a frozen list (C9).
