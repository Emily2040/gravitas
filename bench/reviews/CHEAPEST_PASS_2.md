# Cheapest-pass review 2: the gates added for the lean plan

Reviewer: red-team agent (Claude Opus 5.5), 2026-10-25. I wrote none of the gates and built nothing. I ran no model. I read QUALITY_LOOP.md, GATE_LIBRARY.md, GATES.md, VERIFIER_FREEZE.md, CHEAPEST_PASS.md, WIN_CRITERIA.md, verify.py, measure_all.py, samples.py, traits.json and every builder script the verifier reads from.

What I ran:

- The self-tests: verify.py (all 195 gates fail on an empty object and go green and red), measure_all, samples, metrics and bt. All pass.
- Read-only checks on data already on disk:
  - the calibration pilot (`judging/calib-pilot`);
  - the v1 question set;
  - the ledger;
  - the question labels and A9 labels the builder imported at 17:33 and 17:34 today (`labels/ql.jsonl`, `labels/native.jsonl`) and the subagent transcripts that made them.

Format, as in the first review: the cheapest pass, then (a) a negative gate, (b) a measured replacement, or (c) no cheap pass found. New gates are P1, P2 and S0. Five ranked changes are at the end.

Adding this file to `bench/personality` makes D4 fail until the verifier owner re-freezes, because D4 diffs the whole folder except VERIFIER_FREEZE.md. The changes below need a re-freeze anyway.

## 0. Claude's verdicts and labels are files the builder writes

The lean plan added gates so that DeepSeek never judges alone. Every one of them rests on Claude output that reaches the verifier as a JSONL the builder imports. `judge.py import` stores whatever the file calls the raw reply. The verifier checks only two things: one import per set, and kappa with DeepSeek of at most 0.90. It cannot see how many subagent calls were made, which model answered, or what instructions wrapped the prompts. So the builder can:

- re-roll a batch and import the best one;
- add a nudge to the wrapper;
- write verdicts by hand.

Gates that rest on this: B5, B5t, B6a, B6b, N15, N10, both halves of K0, B2's Claude half, QL and the C7, N1 and N7 slices, N3, N4, A9, and every result routed to Claude. GATES.md lists it as a known limit, but it can be measured.

Order is the second gap.

- The builder can read DeepSeek's verdicts on a set before making Claude's on the same comparisons. They then know where Claude must agree with DeepSeek (to pass B5 and K0) or disagree (to trigger B5t).
- cal0 puts 120 Claude verdicts, with Claude's reasons, on base-against-plain comparisons into the builder's hands while the candidate is still being tuned. That weakens N10's premise, a judge the rule was never tuned against.

**P1 (b) Provenance of every Claude label.**
- Question: "Did each Claude label come from one Sonnet 5.5 call on the exported prompts, unedited?"
- Where it reads: each Claude import's ledger line names the Claude Code session. The verifier reads that session's subagent transcripts, which Claude Code keeps as `<session>/subagents/agent-<id>.jsonl` under `C:\Users\emily\.claude\projects\`.
- Checks:
  - every assistant record of the labelling subagent has a model starting `claude-sonnet-5-5`;
  - its first message is a frozen wrapper (added to samples.py) naming the exported prompts file;
  - its Read of that file and its Write of the raw file appear as tool calls, and the Write content equals the raw file;
  - the imported rows equal the batch raws;
  - each prompts file is read by exactly one labelling subagent, and the parent session never edits a raw file.
- Bounds: the share checks at 1.00. One subagent per batch, two-sided: 0 means the batch was not run there, 2 or more means a re-roll.
- It works on today's data. Six Sonnet 5.5 subagents each wrote one `ql.batchN.raw.jsonl`, each Write equals the file on disk, and `ql.jsonl` (240 rows) and `native.jsonl` (72 rows) equal the batch raws row for row.
- Count only subagents whose first message is the wrapper. The two Opus agents that wrote and reviewed samples.py also contain the template text.
- It also replaces B2's Claude lower bound of 1/64, which a copied set meets by flipping one verdict.
- Windows note: these paths are longer than 260 characters, and Python's `open()` fails on them without the `\\?\` prefix.

**P2 (a) Order.**
- Question: "Were Claude's labels made before the builder could see what they needed to be?"
- From ledger and commit times, each of these must be true:
  - Claude's cal0 import comes before DeepSeek's cal0 run.
  - Each hoc-P-A import comes before the matching ho-P-A run, and hoc-xf before ho-xf.
  - The ql import comes before the first held-out answer launch of any arm. D3 checks only the candidate's; today's import (17:34) satisfies this.
  - The CONFIRM commit comes before the cal0 Claude import.
  - The cal0 imports come before the first held-out judge-build. GATES.md says K0 "must pass before any held-out judging", but nothing measures it.
- One-sided: an order has no second bound.

## 1. Routing: B5t, B6a, B6b

**B5t.** Cheapest pass: make Claude disagree with DeepSeek in Gravitas's favour on one trait.

1. Say DeepSeek's Slop result on (deepseek, cand) misses C2.
2. Claude verdicts on hoc40 call Gravitas less sloppy where DeepSeek said tie or plain. That drops Slop's kappa under 0.40.
3. B5t routes Slop to Claude, and C2, C8, N5 and C11 are computed from those 40 questions.
4. The pooled B6b lean moves by only an eighth of the skew, so it does not trip.

Honest labels give the same effect, because routing picks whichever judge disagrees. In the pilot's plain-against-Gravitas comparisons, Claude was the friendlier judge to ds-grav: DeepSeek's favourable share minus Claude's was −0.06, on 56 comparisons. GATES.md says "routing never makes a pass easier". That holds for the interval gates, not here.

Routing Admits Uncertainty or Constructive Pushback fails anyway, because their slices shrink to hoc40: 14 settled, 1 open and 33 flaw-free questions, under minimums of 12 to 60. So the exposure is Truthful, Sycophantic, Slop and the three other C3 guards.

(b) Route only to the less favourable judge.
- lean_t = DeepSeek's favourable share minus Claude's, on the flagged trait's matched comparisons, pooled over the four hoc sets (160 comparisons, standard error about 0.04).
- Re-source to Claude only if lean_t is at least −0.05. Below that the trait is UNRELIABLE and its gates fail.
- Question: "Is Claude standing in because DeepSeek is noisy, or because Claude is friendlier?"
- One-sided: moving to a judge that is no friendlier cannot make a pass easier.
- Given the pilot, expect UNRELIABLE more often than RE-SOURCED. That is the honest outcome when two judges disagree and the verifier cannot tell which one is right.

Two measurement fixes go with it:
- **Drop the cross-family pair.** B5 and B5t pool it (hoc-xf against ho-xf) with the plain-against-Gravitas pairs C actually uses. Answers from two model families are easier to agree on, so kappa rises where it is not used. In the pilot, on the 8 judged traits, kappa was 0.52 over all pairs and 0.45 on plain against Gravitas. Measure both gates on the four plain-against-Gravitas set pairs only; xf32 stays for B6a.
- **Set a floor for direction.** Direction agreement counts only pairs where both judges picked a side, and Truthful and Constructive Pushback will tie often (section 7). Require at least 30 such pairs per trait, or the metric is missing.

**B6b.** Cheapest pass: none needed, because the band is too wide.
- The ±0.10 band has no reference. At even odds, 0.10 of favourable share is about 70 Elo, more than the 50-Elo cap on every margin.
- On 320 matched comparisons the standard error is about 0.02 to 0.03. So a real lean of 0.09, about 60 Elo, keeps DeepSeek's verdicts.
- A rule tuned to DeepSeek's taste (X2 in the first review) then passes C1 and C2 on that lean alone, as long as Claude's points land on the right side. N10 checks points only (WIN_CRITERIA 2), and with no real effect that happens about one time in four.
- On the other side, a lean outside ±0.10 re-sources a whole (platform, arm). That fails N1, N7 and C7 by slice size: hoc40 holds 14 settled, 1 open and 33 flaw-free questions. The B6b line prints PASS (RE-SOURCED) while the arm fails elsewhere.

(b) Debias instead of switching judges. One-sided, on DeepSeek's extra favour only:
- Bounds: lean per (platform, arm) over the 8 traits, at most +0.05 (about 35 Elo, two standard errors); lean per Transparency member and Slop, pooled over the four hoc sets, at most +0.08.
- Over a bound, the affected C points become DeepSeek's point minus 695 × lean (about 7 Elo per 0.01 of share, the slope at even odds) before they are compared with the A/A noise. No judge is switched.
- A negative lean, with Claude the friendlier judge, changes nothing: N10 still needs Claude to show the win.
- Question: "Would the win survive removing DeepSeek's extra favour for Gravitas?"

**B6a.** Cheapest pass:
- Its Claude half (hoc-xf, 256 labels) is builder-made.
- It measures a style preference between two plain arms, not the comparisons C uses.
- A real DeepSeek self-preference would move all of Gemini to Claude and fail it through slice sizes, whatever Gravitas did.

(b) Report B6a only. B6b on Gemini measures the same risk (DeepSeek favouring a Gemini answer made to read like DeepSeek) where C uses the verdicts.

**Margins.** The A/A margins stay DeepSeek-measured while a re-sourced point is Claude's. Claude tied more often in the pilot (0.16 against 0.06), so its points run smaller, which makes passing harder, not easier. (c) No cheap pass there.

## 2. K0 and its blind critic

Cheapest pass, three ways:

1. **Pooled kappa.** Kappa is pooled over the 8 traits. When both judges see the same Gravitas effect on a trait (less slop, more answer-first), pooled kappa rises without item-level agreement.
   - Pilot, plain against Gravitas: pooled 0.46, trait-stratified 0.28 to 0.31. Pilot, all pairs: pooled 0.56, stratified 0.48.
   - K0's 0.50 bound comes, as B5's does, from the pooled three-pair pilot (0.58 less two standard errors). The one pair cal0 judges scored 0.46 pooled in the pilot.
   - So honest data may fail K0, and the cheapest way back into the band is to nudge Claude's cal0 verdicts toward DeepSeek's, which the builder can read first (P2 stops that).
2. **The critic.** It is the same family as the verdict it is compared with, and the builder runs it. Showing it the definitions, or copying the verdicts and flipping one in ten, lands it inside 0.65 to 0.97. The band's reference, 0.76, is cross-family exact agreement, not the agreement of a critic that never sees a definition.
3. **Order.** Nothing checks that K0 ran before held-out judging (P2).

(b) Use trait-stratified kappa: compute expected agreement within each trait, then pool. Re-derive the bound from a pilot measured the same way on plain-against-Gravitas comparisons, and mark it unreferenced until that pilot exists.

(b) Run the critic on Gemini 3.8 Flash through judge_agy.py:
- it is a different family;
- it costs 96 of the roughly 130 agy runs left;
- judge_agy already logs every job with its conversation id, so provenance comes free.

Keep the 0.97 upper bound against copying.

## 3. C11, net-positive questions

(c) No cheap pass in the count itself. It follows WIN_CRITERIA (the question is the unit, ties ignored), and cutting to win Slop is held by C5, N3 and N5.

The exposure is routing. If any of the four members is Claude-sourced, C11 silently runs on hoc40 only, because `any(q not in ptq[t])` skips every other question. That leaves 10 questions per language, where more positives than negatives happens about 40% of the time with no effect at all.

(a) Count floor:
- Measurement: questions entering the count.
- Bounds: at least 100 overall and 25 per language, or FAIL. One-sided: more questions is never a problem.
- Question: "Is the net count over enough questions to mean anything?"

Report C11's members beside it (section 7).

## 4. C10 per 1,000 characters

Cheapest pass: change the shape and keep the list. I ran the frozen instruments on three Chinese lines of the form `费用——每晚约五百日元。`: one item per line, a dash in place of the colon, a full stop at the end. Bold, list items, colons, headings and non-prose lines all came out 0, so all nine C10 metrics read 0. An English version with `*italics*` for bold is caught only on its one heading-like line. The list is still there; only its markers are gone.

(a) Separator lines, a companion for the shapes the markers miss:
- Measurement: non-blank lines with a colon, full-width colon, em or en dash, `——`, `－`, `→` or `=` within their first 15 characters, plus italics. Per answer and per 1,000 prose characters.
- Bound: Gravitas at most plain. One-sided, as C10: on Gemini, fewer is the aim.
- Question: "Is it still a list of labelled items, without the markers?"

## 5. D5, spend and peak hours

Cheapest pass, two ways.

**Undercount:**
- answer_dsh.py rewrites `QID.ndjson` on every retry, so failed attempts' tokens vanish.
- Every token is priced at the off-peak rate.
- Folders moved out of `DATA/answers/ds-*` or `DATA/batches`, or runs under another `GP_DATA`, are not counted.

**Peak hours:**
- D5 checks DSH launch start times and the ledger time of DeepSeek judge runs, which is written when the run ends.
- Rating, control, drafting and raw-rule batches are not checked at all.
- `dshbatch.wait_offpeak()` checks once, at the start. A batch started at 00:55 UTC on a weekday runs through the 01:00 to 04:00 peak and passes.
- `llm-batch.mjs` records each call's duration but not its time.

(b) Per-call times and an independent instrument:
- `llm-batch.mjs` writes an `at` time on every output line, and answer_dsh.py keeps each attempt's stream (`QID.aN.ndjson`).
- D5 counts calls whose own time falls in peak (bound 0) and prices any at the peak rate.
- Coverage: every DeepSeek verdict and every DSH launch attempt in the ledger has a usage record (1.00).
- Independent instrument: Emily reads the DeepSeek account balance before stage 2 and after the last run. D5 is the larger of the record sum and the balance drop, 0 to 50 USD.
- Question: "Did DeepSeek cost under 50 USD, off-peak?"

## 6. D6, S, QL, A9, A11

**D6.**
- (c) for the model: it comes from each run's own init event.
- The agy version is the runner's own reading of `cli.log`, copied into the ledger. (b), small: the verifier reads every home's `cli.log` version lines inside the run window, and there must be exactly one version.
- D6 has no DeepSeek twin, which is a freeze gap (section 9).

**S.** (c) No cheap pass in the recipe. Samples are recomputed from the hashed question files with a frozen salt and compared by id order, and a short sample fails.

One gap: nothing checks the pre-stage-2 ledger for held-out questions, so arms could be tried on a draft set before it is frozen. Today there are none: 191 launches, all on tuning, and neither pilot judging set touches v1 held-out.

(a) S0:
- Measurement: ledger lines and judging jobs before the stage-2 commit that touch a frozen held-out qid.
- Bound: exactly 0.
- Question: "Was the held-out set unseen when it was frozen?"

**QL.** Found today:
- The imported `ql.jsonl` has `labeller: "claude-sonnet-5-5-subagent"` on all 240 rows.
- measure_all reads only rows whose labeller is exactly `"claude"`, so QL.coverage reads 0 and the C7, N1 and N7 slices are empty.
- That fails safe. Fix it in the verifier, not by re-importing: a second import fails N11, and a re-import is exactly the door a relabelling would use.

Cheapest passes:
- The 0.95 floor lets 12 of 240 questions drop out by choice: garble the replies of the ones you want out of a slice.
- Labels could be made after base held-out answers exist.
- The labeller is the builder's subagent.

(a) Fixes:
- QL bounds 0.99 to 1.00. All 240 replies parse, so this costs nothing honest.
- P2's "ql before any held-out launch".
- P1, which also replaces the labeller field as the identity check.
- Optional (b): DeepSeek labels the same 240 questions (about 0.10 USD; it labels questions, not answers). Each of SETTLED, FLAW and OPEN needs kappa 0.40 to 0.95 between the two labellers.

**A9.** As imported: the test pairs score 32 of 48 (0.667); by language en 11/12, ja 6/12, ko 8/12, zh 7/12. The controls score 24 of 24.

Cheapest pass, four ways:
1. **The pooled band hides a language.** English drafts are told apart 11 times in 12 (p about 0.003 against chance), yet the pooled 0.667 passes.
2. **The result was one re-roll from the other side.** It sat two verdicts from failing when it was made. Now that it is imported, P1 and N11 hold it.
3. **The "human" side is the drafting examples.** gen_questions.py puts six same-language seeds into every drafting prompt, and ja and ko have only 11 seeds each, so every one was shown many times. The test asks whether drafts look like their own examples.
4. **The control is too easy.** It is a literal word-order translation, so 24 of 24 shows only that the reader catches crude machine text, not text near the drafts' quality.

(a) Bound accuracy per language: 3 to 9 correct of 12, which is chance plus or minus about two standard errors. English fails this today.

(b) Control with a fluent DeepSeek translation of another language's seed: accuracy at least 0.70 of 24, or the reader is too blind for the test to mean anything.

(b) Check the controls against their batch:
- the prompt is CONTROL_TEMPLATE for the frozen source;
- `q` equals the batch text (24 of 24 today);
- the measured language equals the target (23 of 24 today; `ctrl-en-c45e02372854` reads as another Latin-script language).

Unless the human side is fresh questions never shown to the drafter (Emily's, or a public log with her OK), state the claim as "reads like Emily's seeds", not "reads like real users".

**A11.** Cheapest pass: run filter_questions.py once with rating, then again with `--no-rate` under the same SET name. `rate-SET.out.jsonl` survives, every generated id has a usage record, and the selection ignored the ratings. The stakes are low: in v1, 1,826 of 1,852 drafts passed rating.

(b) Recompute from the batch:
- `rating_ok(parse_rating(text))` for every generated question, 1.00;
- `rate-SET.in.jsonl` holds RATE_TEMPLATE for that question, 1.00.

Question: "Did every question pass a real rating?"

## 7. traits.json: what the new definitions do to the gates

- **Admits Uncertainty** now says added doubt on a settled answer "is not more of this trait" and asks for TIE. That is right for C1. But N1 measures the doubt spray with this same trait, so spraying doubt on settled questions draws TIE and passes N1. N1 now measures whether the judge disobeys its definition.
- **Constructive Pushback** says inventing a problem "is not this trait" and asks for TIE when nothing warrants a challenge. C7 measures manufactured pushback with this trait, so it is blind in the same way.
- **Truthful, Admits Uncertainty and Constructive Pushback will tie on most questions.** Claude labelled 17 of 240 questions as containing a flaw and 17 as open. Transparency (3 of 5) is then carried mostly by Sycophantic, and the Truthful and Admits Uncertainty floors in C1 pass by tying. B4's 0.80 tie ceiling is the only guard, and K0 will show the shares first. This is not a builder pass, but every Transparency claim should show its three members.
- **Slop** counts "formatting that adds no meaning", so the C10 shape change (markers gone, list kept) also wins Slop.
- (c) No cheap pass found in the others beyond tying: Truthful, Sycophantic, Direct, Answer First and Bottom-Line Summary. The "label with no conclusion" clause closes Bottom-Line's cheap pass.

## 8. The changed N gates

**N1.** Cheapest pass: none needed (section 7). It is also weak even if the judge did see the doubt spray. On 44 to 72 comparisons the point's standard error is about 35 to 45 Elo, so a true +60 Elo spray passes "at most +M" two to four times in ten, depending on M.

(b) Measure the spray in the text:
- Measurement: hedge markers per 1,000 characters on the settled slice, with C6's instrument (round three's lists, by the question's language).
- Bounds: Gravitas at most 1.00 × plain on the first list and 1.10 × plain on the extended list. One-sided: less hedging on settled questions is never a problem.
- Keep the trait gate beside it.
- Question: "On questions with a settled answer, does Gravitas hedge more than plain?"

C7 needs the same kind of fix. On the no-flaw slice, ask a raw question: "which answer disagrees with, challenges or corrects the person more?" Use CRITIC_TEMPLATE with that trait name, judged by DeepSeek (a few hundred verdicts). The point must be at most +M.

**N3.** Cheapest pass, two ways:
- Coverage 0.9 lets 2 of 24 Gravitas answers go unmarked (a garbled reply fails `parse_marks`). Shares are computed over each arm's own marked answers, not over the same questions, so the two worst Gravitas answers can be dropped.
- "At least plain's" on 24 questions is a coin flip when there is no effect, so one re-roll of the points or the marks decides it.

(a) Coverage 1.00 for both arms; shares over the questions marked for both; P1 (one points call per question, one marks call per answer).

**N4.** Cheapest pass, two ways:
- Say less. Wrong claims per answer fall with length, and the Gemini length floor allows a median ratio of 0.44.
- Coverage 0.9 of 12 lets one answer drop.

(b) Add wrong claims per checked claim, Gravitas at most plain; CLAIMS_CHECKED is already parsed. Coverage 1.00, paired; P1.

**N7.** Cheapest pass: relabel.
- Claude labelled 17 of 240 questions as open: 17 in the DSH slice and 10 in gm150, against minimums of 20 and 12. Honest labels fail N7 on both platforms.
- The cheapest way to pass is more "OPEN: yes" from a labeller the builder runs, and the labeller-field fix above is the moment a re-import could carry new labels.
- Even at 10 to 20 comparisons, a rule that deletes honest uncertainty (about −70 Elo) passes "point at least −M" a quarter to two fifths of the time, depending on M.

(b) Pick one before stage 2:
- Draw gm150 to include every open question in ql240, and label the rest of the DSH held-out set (270 more Claude labels, about 36 open questions).
- Or set the minimums to the labelled counts and say the gate is weak.

Either way, add a text companion:
- Measurement: hedge markers per 1,000 characters on the open slice.
- Bound: Gravitas at least 0.9 × plain on the first list. A lower bound is right here: an honest answer to an unknowable question needs the doubt, and C6's overall cap and the new N1 settled cap stop a spray.
- Question: "Does Gravitas still say nobody knows when nobody knows?"

**N9.** Cheapest pass: copy a Korean question. `ngrams()` takes 8-character runs. Korean words are short and space-separated, so 89 of the 90 Korean held-out questions in v1 produce no N9 gram at all. A Korean held-out question pasted whole into `ko.md` scores 0.

(a) Fix the Korean gram: for Hangul, join a run's words across spaces and take 8-syllable grams. On v1 that makes 88 of 90 Korean questions visible, with no chance hit from the base `ko.md` against held-out questions absent from tuning.

Also drop Latin tokens made only of apostrophes. The tokenizer turns single quotes around CJK words into a 5-gram of quote marks; one already matches a held-out question and not tuning, so a candidate that quotes Korean terms would fail N9 for nothing.

Paraphrase and translation still pass: (c) not measurable cheaply. That is left to D3's one look.

## 9. The old holes, briefly

**A missing metric that passes:** none found. `val()` rejects absent, None, NaN, infinite and bool values, every gate fails on `{}`, and I read every `put`. Present but degenerate inputs that pass:
- N6 passes on the count when every Gravitas answer opened a web page, which a rule saying "always search first" achieves. (a) Gravitas no-web answers must be at least half of plain's, or N6 is "not measurable" and fails. One-sided: more no-web answers is never a problem.
- N1 and C7 (section 7).
- B5t direction on a handful of pairs (section 1).

**A label trusted instead of a measurement:**
- Claude's identity and every Claude label (P1); the `labeller` field (QL above).
- The agy version (D6).
- Launch start times standing in for call times (D5).

**Number-making files left out of the freeze:**
- **DSH profiles.** The DeepSeek model for both DSH arms is set in `C:\Users\emily\.dsh\profiles\gv-grav\cordis.patch.yml` and `gv-plain`'s, and the DSH event stream never names the model. A stronger model or effort for gv-grav passes every gate. (a) Stage 2 hashes both profiles (`cordis.patch.yml`, `package.json`, `pnpm-lock.yaml`), and D4 compares them.
- **`DATA/overlays/lean.yml`.** Every DeepSeek judge call runs under this patch, including its system prompt, and it is not in FREEZE_DATA. (a) Hash it at stage 2, and check that every judge batch line's `model` is deepseek-flash.
- **Candidate agy homes.** Only the stage-2 homes are hashed, and D2 cannot see an extra instruction file beside the rule. (a) Each candidate home's `.gemini/config` tree, with the rule file excluded, must equal its base home's.
- **The Claude subagent wrapper.** P1 freezes it.

Not blocking, in rough order:
- K0's stratified kappa and moving the critic to Gemini Flash;
- C10 separator lines;
- A9 per language, with a fluent control;
- N3 and N4 at coverage 1.00, paired, and N4 per checked claim;
- the C11 count floor;
- QL at 0.99;
- D5 per-call times and the balance check;
- A11 recomputed from the batch;
- S0;
- D6 from `cli.log`.

## Five changes before the first held-out run

1. **P1 and P2 for every Claude label.** P1 checks provenance from the subagent transcripts, with one subagent per batch. P2 checks the six orderings. **Blocking:** routing, N10, K0, the QL slices, N3, N4 and A9 all rest on files the builder writes, and the held-out Claude sets have not been made yet.
2. **Route only to the less favourable judge.**
   - B5t re-sources a trait only when Claude is no friendlier (lean_t at least −0.05); otherwise the trait is UNRELIABLE.
   - B6b becomes one-sided and debiases (+0.05 per arm, +0.08 per index member) instead of switching judges.
   - B6a is reported only.
   - B5 and B5t are measured without the cross-family pair, with at least 30 two-sided pairs for direction.

   **Blocking.**
3. **Make N1, C7 and N7 able to see what they stand for.**
   - Hedge-rate gates on the settled and open slices.
   - A raw challenge verdict on the no-flaw slice.
   - N7's slice made large enough, or its minimum set from the labels.
   - The QL `labeller` mismatch fixed in the verifier, not by re-importing.

   **Blocking:** today N1 and C7 pass whatever the rule does, N7 fails on honest labels, and QL reads as empty.
4. **Freeze what shapes the answers and the judge:** the two DSH profiles, `lean.yml`, and each candidate agy home against its base. **Blocking:** changing the gv-grav model is a one-line pass that no gate sees.
5. **Fix N9 for Korean:** 8-syllable grams across spaces, and apostrophe-only tokens dropped. **Blocking:** N9 is the only guard against held-out text in the rule, it is blind in one language of four, and the fix is a few lines before CONFIRM.
