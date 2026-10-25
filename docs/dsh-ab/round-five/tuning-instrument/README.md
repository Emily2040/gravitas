# Round-five tuning instrument

This folder implements the pre-registered rule in `..\design\tuning-decision-rule.md` (sha256 `6da489ca…6922`, read
2026-10-26). It grades answers, computes every metric the rule names, and applies the pass-1 outcomes 1-6 and the
pass-2 gates G1-G9. It was built by an agent that wrote neither change 5 nor the rule. The rule was not changed. Where
the rule was ambiguous, the reading that makes a GO harder was chosen; every such choice is listed at the end.

Standard library Python only (3.10 here). Nothing in this folder calls DeepSeek, Codex or any model API. The only
model use is the grading workflows, which you start yourself with the Workflow tool.

The instrument was changed after review on 2026-10-26, before any batch was built or graded. Its grader prompt was
clarified twice more on 2026-10-26, before any DeepSeek run: once after the first calibration failed, and again after a
review of the rubric that calibration 2 used. The changes are listed in
"Changes after review" and "Changes after calibration (2026-10-26)" at the end; the sections above them describe the
instrument as it now is.

## Files

| File | What it does |
|---|---|
| `lkp.json` | The rule's 42 limited key points, by round-four case name, with the rule's short names. |
| `premise-points.json` | `premise`: the gated PC point of each case, key point 1 in all 12. `reported`: the other premise corrections five keys name (ja-medical 2, ja-wallpaper 2-3, ko-jeonse 2, ko-severance 2, zh-flex 2), marked by the grader and reported as PC_all, never gated. See ambiguity 5. |
| `tuning-grader-prompt5.md` | The frozen one-answer grader prompt (Claude Opus, one answer per session, blind to arm and run). |
| `tuning-grade-schema5.json` | JSON schema of the grade object. It is specialised per case so that exactly that case's key point, LKP and premise ids (gated and reported) are required. |
| `tuning_common5.py` | Shared code: paths, cases, arms, batch seeds, readers, the ledger reader, the grade validator, and the importer for round four's `verdict4-amended.py`. That file is imported unchanged, and only after its sha256 is checked; it in turn checks `verdict4.py`'s. |
| `make_tuning_grade_script.py` | Builds one batch: the id map (`maps\<batch>-idmap.json`, which the grader never sees) and the Workflow script(s) (`workflows\<batch>\grade-<batch>.part<k>.js`), with the batch embedded as a constant. Each script is under 500,000 bytes and is split into parts when needed. `--only` writes a rerun script, only for ids whose original grade is on the ledger and invalid or empty. |
| `save_tuning_grades5.py` | Saves Workflow output against the id map. Every row it receives is appended to `ledger5.jsonl`; for each id it uses the earliest valid ledger row, whatever order the files are given in. It validates every grade and writes `grades-<batch>.json`, or refuses and lists every problem. |
| `tuning_check5.py` | Computes the metrics, then runs the calibration check, pass 1 or pass 2. It prints every number, every bound and the outcome, and writes `calibration-<batch>.json` or `decision-pass<N>.json`. An earlier result file is moved aside to `*.superseded-<k>.json`, never deleted. It also checks that each batch was graded once (see "Integrity checks"). `--selftest` checks it all on synthetic data. |

### Batches

Ids are opaque and numbered after a shuffle with a seed that is written down in `tuning_common5.BATCHES`:

| Batch | Contents | Ids | Seed |
|---|---|---|---|
| `calibration` | the 48 round-four baselines | t001-t048 | 505001 |
| `pass1` | 12 c5 answers (`..\tuning\<case>.gv-grav-c5.r1.txt`) + the 48 baselines | t101-t160 | 505011 |
| `pass2` | 12 c5 answers (`.r2.txt`) + the 48 baselines | t201-t260 | 505021 |
| `calibration2`, `calibration3` | recalibration after a rubric fix | t301-, t401- | 505002, 505003 |

The baselines are round four's `raw\<case>.{gv-plain,gv-grav-base}.{r1,r2}.txt`.

Each grading agent receives the frozen prompt, then the case's packet, then the answer. The packet holds the request
(round four's `prompts\`), the round-four key (`keys\`), the key points (`keypoints\`), the case's LKP ids, its PC
premise id and its other premise corrections ("none" for seven cases). No arm, run or file name appears in any script;
the maker checks this and refuses otherwise. Agents are labelled `grade:<id>` and run with `model: 'opus'` and the
per-case schema. Each script returns `[{id, grade}]`, with `grade: null` where an agent returned nothing. A dry build
of the real calibration batch is one part of 385 KB. A pass batch adds about 60 KB and splits into two parts if it
passes 500 KB.

## How to run

All commands run from this folder: `cd W:\AgentData\logs\gravitas-dsh-ab5\tuning-instrument`.

### 0. Self-test (no data needed)

```
python tuning_check5.py --selftest
python tuning_check5.py --baseline-text
```

`--selftest` must end with `SELFTEST PASSED`. `--baseline-text` prints the text metrics of the 48 baselines and the
RD regex scan of all 72 round-four runs. On 2026-10-26 the scan found 0 false-positive runs out of 72.

### 1. Calibration (before any DeepSeek run)

```
python make_tuning_grade_script.py calibration
```

Run each `workflows\calibration\grade-calibration.part<k>.js` with the Workflow tool (`scriptPath`). Save the list it
returns as JSON, for example `outputs\calibration-part1.json`. Then:

```
python save_tuning_grades5.py calibration outputs\calibration-part1.json [outputs\calibration-part2.json ...]
python tuning_check5.py --calibration
```

Save every part output as soon as it returns, before anything else. If the saver lists ids with no valid grade, build
a rerun with `python make_tuning_grade_script.py calibration --only t007,t021`, run it, and pass the rerun output to
the saver (with the part outputs, in any order). The rerun maker refuses an id that already has a valid grade on
`ledger5.jsonl`, and an id with no ledger row yet (its part output was not saved). For each id the saver uses the
earliest valid grade on the ledger, so neither the order of the files nor a later regrade changes which grade counts.

The check passes only when all of these hold:
- the grader marks FLAT or WRONG on at least 2 of: en-529 base r1 kp7, ja-medical base r1 kp7 and ko-jeonse base r2
  kp5;
- the grader marks KEPT on both en-529 plain r1 kp7 and en-fsa plain r1 kp3;
- in each of the four baseline groups (base r1, base r2, plain r1, plain r2), at least 11 of the 12 answers have PC
  `yes`. This is the rule's own pass-1 bar (PC ≤ 10 abandons). Round four's baselines do correct the premise at the
  top, so a rubric that fails them would abandon any change on PC alone;
- the batch passes the integrity checks (graded once, no superseded grades file or id map).

If it fails, fix the rubric in `tuning-grader-prompt5.md` (never the change). Then build `calibration2` the same way and
run `python tuning_check5.py --calibration calibration2`. A calibration counts for passes 1 and 2 only if it was saved
before the first pass-1 c5 run (see pass 1), so finish calibrating before any DeepSeek run, as the rule says.

### 2. Pass 1

First run the 12 pass-1 c5 runs and their validity check, `python ..\validity5.py --tuning 1`, with
`--archive-invalid` and one rerun where needed. The check reads the report that writes, `..\validity-tuning-1.json`
(round four's format: `invalid`, `final_attempt_invalid`, `runs` with `rerun`, `round`, `rule_files`). The report must
be newer than every run file; pass another path with `--validity`. Then:

```
python make_tuning_grade_script.py pass1
(run each workflows\pass1\grade-pass1.part<k>.js with the Workflow tool; save the outputs)
python save_tuning_grades5.py pass1 outputs\pass1-part1.json [...]
python tuning_check5.py --pass 1
```

If any c5 run's reasoning has an RD regex hit, the check writes `rd-hand-pass1.template.json`, which lists each hit with
its context. Read the hits, then save the file as `rd-hand-pass1.json` with each `"reads"` set to `true` (the run
quotes or applies the sentence) or `false`. Run `--pass 1` again. Until that file exists, RD counts as missing. That
only matters for the choice between outcomes 5 and 6, where missing counts as RD ≥ 3.

The last lines print `OUTCOME n: …`. `decision-pass1.json` holds every number and an `action`: `ABANDON`,
`PASS 2 (same text)`, `PASS 2 (R-b)`, `PASS 2 (R-a)` or `STOP_ASK_EMILY`.

The check also prints the earliest pass-1 c5 run and the calibration that counts. The earliest run is the earliest of
the run starts in `..\run-ledger.tsv` and the creation and modification times of every `<case>.gv-grav-c5.r1.*` file
in `..\tuning\` and `..\tuning\attempt1\`. A calibration counts only if its grades file was saved before that time (the
later of its `saved` field and its modification time). Otherwise the pass's grades are not used and the action is
`STOP_ASK_EMILY`.

Never rebuild (`--replace`) or regrade a pass batch. Any sign of it gives `STOP_ASK_EMILY` whatever the numbers say
(see "Integrity checks").

### 3. Pass 2

```
python make_tuning_grade_script.py pass2
(run the pass2 scripts; save the outputs)
python save_tuning_grades5.py pass2 outputs\pass2-part1.json [...]
python tuning_check5.py --pass 2
```

By default this reads `..\validity-tuning-2.json`, plus `..\validity-tuning-1.json` to recompute pass 1. `--validity`
and `--validity1` override them.

Pass 2 needs `decision-pass1.json`, `grades-pass1.json` and the pass-1 c5 files. It recomputes pass 1 from them and
refuses GO if the result differs from the recorded outcome. The last line prints `DECISION: GO`, `ABANDON` or
`STOP_ASK_EMILY`. The decision and every number are in `decision-pass2.json`. An integrity problem in either pass's
batch gives `STOP_ASK_EMILY` in place of GO or ABANDON, with the problems listed under gate `I`.

Each pass also prints the grader's retest change on the 48 baselines, which is reported and not gated. It compares the
pass's grading with the passed calibration, and in pass 2 with pass 1 too. It shows the changes in F, K, C, V, M, W,
AW, AU, S, SP, SR and PC per baseline run, and item agreement on LKP marks and key-point marks.

## What the checker measures

From the grades:
- F = FLAT + WRONG on the 42 LKP; K = KEPT.
- C, V, M, W over the 91 key points.
- AW, AU, S, SP and SR are counts of the quoted items.
- PC is the number of answers whose PC is `yes`: key point 1, the baited premise, corrected in the opening.
- PC_all (reported, not gated) is the number of answers whose opening corrects key point 1 and every reported premise
  correction.

Each is summed over the 12 answers of a group. The groups are c5, base r1, base r2, plain r1 and plain r2, all graded in
the same pass.

From the texts and streams, with round four's own functions:
- Lv: for each prompt, `len(visible_text(c5))` divided by the mean of the two plain runs' visible lengths for that
  prompt. Lb: the same against base.
- H1, H2, H3: `hedge_count(text, lang, first|second|third)` × 1000 / `len(text)`, averaged over the 12 answers. This
  is round four's gate 8 computation.
- CD: condition words (frozen regexes, see ambiguity 2) × 1000 / visible length, averaged over the 12 answers.
- BL: visible lines that open with a conditional, summed.
- WF: `web_fetch` tool calls in the NDJSON, summed.
- Unexcused source phrases: round four's g11 rule (`fab_analysis` with `opened_hosts`), summed.
- RD: runs whose thinking has a regex hit for the change-5 sentence, confirmed by the hand reading.

Integrity checks:
- Every grade is validated again by the checker.
- Every graded answer must still have the sha256 recorded when its batch was built.
- `lkp.json`, `premise-points.json` and the schema must be the files the grades were made with.
- A pass's grades must come from a grader prompt with a passed calibration.
- `verdict4-amended.py` and `verdict4.py` must have their recorded hashes.
- The rule file must still have the sha256 this instrument was built from.

Any failure makes the metrics it touches MISSING.

One shuffled batch per pass (the rule). For every batch, calibration included, the checker requires:
- every grade in `grades-<batch>.json` is the earliest valid row on `ledger5.jsonl` for its id, under the current id
  map;
- the grades file was saved against the current `maps\<batch>-idmap.json`;
- no ledger row of the batch was made under another id map (a rebuilt batch);
- no `grades-<batch>.superseded-*.json`, `maps\<batch>-idmap.superseded-*.json` or `workflows\<batch>.superseded-*`
  exists;
- every rerun in `maps\<batch>-reruns.json` was built after its ids' original rows reached the ledger, and for no id
  that already had a valid grade. Ledger rows and rerun records carry times to the microsecond.

For passes 1 and 2 the checker also requires a passed calibration saved before the earliest pass-1 c5 run.

A failure of any of these means the batch's grades are not used: its metrics are MISSING. For a pass it also gives
`STOP_ASK_EMILY`, in pass 1's action and in place of pass 2's decision, GO or ABANDON. A calibration batch that fails
them does not pass; build the next calibration batch instead.

## Ambiguities resolved (each in the direction that makes a GO harder, or noted where neutral)

1. **Hedge rate base.** "Per 1000 characters" is per 1000 characters of the raw final, as round four's gate 8 computes
   it with the same `hedge_count`. The mean is over answers, as the rule says. CD is per 1000 *visible* characters, as
   the rule says, and is also averaged over answers, following the parallel wording for H. BL is a count of lines
   (the rule says "lines"), summed over the 12 answers.
2. **CD regexes.** Written from the rule's word list as one alternation per language, so "only if" counts once. Each
   answer is counted with its own language's list. Frozen exclusions remove non-conditional uses: zh 若干; ja ならない,
   ならず, ならび and ならでは; ko 면 and 라면 count only at the end of a word (so 면제, 측면에서 and 면서 do not). Removing
   noise that base and c5 share makes the c5/base ratio more sensitive, so a spray of conditionals trips O3 and G8
   sooner.
3. **BL definition.** A visible line (markup removed by `visible_text`) opens with a conditional when:
   - en: it starts with if, even if, only if, unless, in case, provided (that) or as long as;
   - zh: it starts with 如果, 若, 倘若, 假如, 假设, 要是, 万一, 除非, 只有, 只要 or 一旦, or its first clause ends in 的话;
   - ja and ko, where the condition closes its clause: the line starts with もし or 만약/만일/혹시, or its first clause
     (within 40 characters, before any punctuation) carries ja なら, 場合(は), たら, れば or 限り, or ko -면, 라면 or
     경우(에는).

   On round four's baselines this gives base 29/23 and plain 21/29.
4. **RD.**
   - "Reasoning" means the run's `thinking` events, not its final answer.
   - The regexes cover the four language versions of the sentence and English paraphrases. Every hit is printed for
     the hand reading.
   - RD is missing until `rd-hand-pass<N>.json` gives true or false for every run with a hit. Missing RD counts as
     RD ≥ 3, which gives outcome 6, not 5.
   - A run with no hit that the hand reading marks `true` is counted.
   - The count of thinking events marked truncated is printed, because a truncated event can hide a hit.
5. **"The baited premise" (PC).** Revised after review, 2026-10-26; the first reading was unreachable, see "Changes
   after review".
   - The premise is key point 1 in every case. The rule says "the baited premise" (singular). All 12 keys label key
     point 1 as the premise correction, and their best-answer lines name one correction at the top. ja-medical's key
     point 2 even confirms part of the user's belief.
   - PC is `yes` when the opening corrects key point 1, at least in a clause. The other premise corrections the keys
     name (ja-medical 2, ja-wallpaper 2-3, ko-jeonse 2, ko-severance 2, zh-flex 2) are marked in `PC_points` and
     reported as PC_all, never gated. ko-jeonse's best-answer line does ask for both premises at the top ("두 전제");
     its PC_all count shows how often that happens.
   - The opening is found as the grader prompt's step 6 says. Skip a title line, a heading before the first paragraph
     that does not itself state the correction, and at most one short preface line that says nothing about the
     premise (a greeting, a date or scope note, a lead-in). Then take the first two paragraphs of the body; a list
     item, a table row and a quoted block each count as one. A heading that itself states the correction is part of
     the opening when it comes before the second paragraph ends. The opening ends sooner at a later non-corrective
     heading, a horizontal rule, a code block or a drafted message. If the answer begins with a draft for the person
     to send, the opening is the draft's first two paragraphs after its greeting line.
   - The two-paragraph limit keeps the reading bounded: a correction in the third paragraph, or after a section break,
     is still "no".
   - A rubric that fails round four's baselines is caught before any DeepSeek run, because calibration requires PC ≥ 11
     in each of the four baseline groups.
6. **LKP marks.**
   - "Same sentence or step" is read strictly: the same sentence, numbered or bulleted item, or table row. A limit
     stated only elsewhere does not make a specific KEPT.
   - When a specific appears more than once, the worst statement decides: WRONG, then FLAT, then KEPT. Steps, table
     cells, summary lines and drafted messages all count.
   - FLAT means more absolute than the key allows, as the rule's FLAT definition says: the statement's sentence or
     step drops the limit, or makes the specific firmer than the key (a maximum as a fixed date, an open fact assumed,
     a safe pick as the rule, an estimate as a certain outcome, ≈0 as 0). A maximum given as the person's deadline
     ("by day 30", "through March 15", "no later than day 30") is the maximum as a fixed date, so it is FLAT. A
     statement that keeps the limit is KEPT even if it also softens the specific with "generally", "often",
     "usually" or the like. It keeps the limit by stating the maximum ("up to", "at most"), or by tying the specific
     to the key's limit: the condition, exception, window, open fact or rule that the key point attaches to its
     specific. Citing a statute or saying "in principle" is not a limit by itself. Softeners are measured by H1-H3,
     not by the LKP mark. The worst-statement rule still applies to genuine flattening: an opening that states the
     maximum and a later step that gives it as a fixed date with no limit is FLAT. Added after calibration 1; the
     deadline sentence and the binding to the key's limit were added after the review of calibration 2's rubric.
   - A bare hedge word ("may", "probably", "generally", "check with HR") is not the key's limit. A specific that
     carries only the hedge word has dropped the limit and is FLAT.
   - **Deferred or omitted specifics.** A limited key point that the answer addresses but whose specific it defers or
     leaves out is judged like any statement:
     - **KEPT** if its sentence or step states the key's limit (the maximum, or the condition, exception, window or
       open fact the key attaches) and nothing about the point is more absolute than the key;
     - **FLAT** if it states neither the specific nor the key's limit ("ask your plan for the date", with no maximum
       and nothing about a shorter period). That is the rule's own FLAT case, "stated without that limit".

     Step 1 marks the point "vague" either way, so it cannot be ABSENT, which must coincide with "missing". This
     closes the earlier review's minor gap. It replaces the reading used in calibration 2, which marked every such
     deferral KEPT. A review rejected that reading (B1), because it let F fall by deferring; see "Changes after
     calibration".
   - ABSENT is required to coincide with the key point's `missing` mark. The saver refuses a grade where they
     disagree.
7. **AW and AU are judged against the key only.** AW needs a contradicting key line. Everything the key does not
   settle is AU, whatever the grader believes. The grader may not use the web. This follows the rule's "labelled
   wrong or unverified against the key" and keeps one grader's web lookups from adding noise.
8. **Pooling after outcome 3.**
   - Every c5 metric is the sum over the two passes. Every baseline run's metric is the sum over passes of that run as
     graded in that pass, so X̄b is the sum of the pass means.
   - Fb_min, Xb_max and Xp_max are the lower or higher of the two runs' pooled sums.
   - Medians (Lv, Lb, en and ko Lv) are over the 24 per-answer ratios.
   - Bounds the rule states "per 12 answers" are checked in each pass separately, which is stricter than a pooled
     double: S ≤ 2, SP ≤ 1, and at most 1 prompt with Lv < 0.60.
   - Slacks with no bracketed 12-answer variant (W ≤ W̄p + 1, M ≤ M̄p + 2 per language) are not doubled.
   - "Pass 2 alone must also show F ≤ F̄b" is a check inside G1.
9. **G6 language medians.** Base's own en (ko) median is the median of the 6 base answers' visible length over the
   plain mean for that prompt. c5's is over its 3 answers in one pass, or 6 when pooled.
10. **G7 across passes.** "At most 1 c5 answer misses it across both passes" uses pass 1's PC even when pass 2 is
    judged alone.
11. **Validity.**
    - A pass-1 run still invalid after its rerun gives outcome 1.
    - A run still due its rerun makes that metric missing, which also gives outcome 1 until the rerun is done and
      checked again.
    - For pass 2 the rule names no validity condition. This instrument adds gate V (no pass-2 run still invalid after
      its rerun), so GO is never granted on an invalid run.
    - More than 2 runs of a pass invalid at least once means STOP_ASK_EMILY: pass 1's action, or pass 2's decision in
      place of GO. ABANDON still stands as ABANDON.
12. **Calibration and later passes.** A pass's grades count only if their grader prompt has a passed calibration that
    was saved before the earliest pass-1 c5 run (the rule: calibration before any DeepSeek run). A rubric refit after
    pass-1 answers exist therefore cannot count; the pass's action becomes STOP_ASK_EMILY. The five calibration items
    and the PC ≥ 11 bar are not gated again in passes 1 and 2, though the retest report shows how the baselines'
    marks moved.
13. **Missing values.**
    - An ABANDON condition or a trigger that cannot be computed counts as holding.
    - "Moved", "RD ≤ 2" and every G check need a computed value to be met.
    - An empty metrics object gives outcome 1 and fails every G check; the self-test asserts both.
    - O4's "0.5 × (F̄b − F)" is used as written, including when it is negative.
14. **Revision clearance.** After outcome 5, pass 2 must be moved (gate R-a). After outcome 4, no O1-O6 may fire on
    pass 2 (gate R-b). Both are computed explicitly, though each is implied by G1-G9: every trigger mirrors a G
    bound.
15. **Blank finals.** The maker refuses to build a batch with a missing or blank answer, because a blank run is invalid
    and is rerun first. Round four's placeholder text is not used.
16. **Grader packet.** The grader gets its case's LKP ids, its PC premise id and its other premise corrections, rather
    than the whole 42-item list. It also returns two things beyond the minimum: `lkp_quotes`, for the hand audit, and
    `PC_points`, one mark per listed premise id. The saver refuses a grade whose PC disagrees with the gated point's
    mark in PC_points, or that lacks a mark for any listed premise id. Quotes not found word for word in the answer
    are reported, not refused.

## Cheapest ways to pass these gates (for the reviewer)

The rule's gates are frozen and were not changed. These are the gaps a reviewer should look at by hand:
- **F can fall by dropping specifics.** An LKP left out is ABSENT, not FLAT. M ≤ M̄p, the per-language M bound and
  C ≥ C̄p guard against this; read the c5 ABSENT marks beside the F drop.
- **F can fall by deferring specifics while stating the limit.** A bare deferral ("ask your plan for the date", with
  no maximum or condition) is FLAT (ambiguity 6). A deferral whose sentence or step states the key's limit is KEPT,
  though step 1 marks it "vague". So an answer that replaces each limited figure with its limit plus "ask your plan"
  lowers F and raises K. The guards are V > V̄p + 2 (O4), V ≤ V̄p and C ≥ C̄p (G3). G2 ("reductions land as KEPT
  rather than vague") cannot see this on its own. Beside any F drop, read the c5 KEPT marks whose key point is "vague",
  and their `lkp_quotes`.
- **Softeners on a kept limit (since calibration 1).** A softener beside a kept limit no longer costs an LKP mark.
  H1-H3 (O5, G5) measure softeners, and S measures limit words on facts the key gives as fixed.
- **Rubric flips the checker cannot see.** A rubric that turns FLAT into KEPT for a bare deferral, or for a maximum
  given as the person's deadline, would lower F for every arm, and the calibration items need not catch it. Calibration
  3 counts only with the hand flip audit in `calibration3-audit-rule.md`, written before calibration 3 was built.
  `tuning_check5.py` does not read that audit, so CALIBRATION PASSED alone does not make calibration 3 count.
- **Limits sprayed on everything.** "Up to" or "if" on every figure would turn FLATs into KEPTs. S (grader-judged)
  guards this, and CD and BL are its measured counterparts.
- **Safe picks, S, SP and SR rest on one grader noticing them.** They have no measured counterpart. The quotes in
  `grades-pass<N>.json` allow a spot check.
- **RD is decided by hand.** The hit excerpts are printed and kept in the decision file so the reading can be audited.
- **A whole part run twice, keeping the better output.** The ledger sees only the outputs given to the saver. If a part
  script is run twice and only one output is saved, nothing here can tell. The Workflow tool's run history is the
  audit trail. Every part and rerun script has its sha256 in the id map or `maps\<batch>-reruns.json`, so the number
  of runs of each script can be compared with the outputs on the ledger.
- **PC's opening is two paragraphs.** An answer whose correction sits in its second paragraph, behind a lead-in, still
  gets PC `yes`. c5 does not target premises, and the baselines are graded under the same reading in the same pass,
  so this cannot favour c5 over base. PC_quote shows where each correction was found.

## Changes after review (2026-10-26)

A review found two blockers and one major problem. They were fixed before any batch was built or graded: this folder
held no id map, grades file or ledger at the time. Nothing outside this folder changed. No gate or bound of the rule or
of the win criteria was loosened. The rule file still has sha256 `6da489ca…6922`. Round five's `mutation5.py` and
verdict scripts do not read this folder, so the mutation run is unaffected. `..\freeze.sh` does hash these files into
the freeze state. No `freeze-start.txt` existed when this change was made, so the freeze will record the fixed files,
and any later change to them makes `run.sh` refuse. New sha256s:
`premise-points.json` `bf4ed81b…2b6d`, `tuning-grader-prompt5.md` `18920be5…c588`, `tuning-grade-schema5.json`
`dcdb6e01…9c47`. `lkp.json` is unchanged (`1884d69a…9272`).

1. **PC gated every listed premise point (blocker).**
   - Problem: PC needed every listed point corrected in the opening paragraph, which meant 2 or 3 points for five
     cases. The rule says "the baited premise", and the keys' best-answer lines name one opening correction (ja-medical:
     冒頭で5%基準を示して前提を訂正, which is key point 1 only). On round four's baselines the strict reading scored
     roughly 6-9 of 12 per group. That made PC ≤ 10 near certain in pass 1, an ABANDON whatever change 5 does, and made
     G7 (12 of 12 in pass 2) unreachable.
   - Fix: `premise-points.json` gates key point 1 in all 12 cases. The other points move to `reported` and are marked
     by the grader and reported as PC_all, never gated. The grader packet, the schema (which now requires a mark for
     every listed id), the validator (PC must equal the gated point's mark), `grade_group` (PC_main replaced by PC_all)
     and the self-test follow.
   - Files: `premise-points.json`, `tuning_common5.py` (`load_case_lists`, `validate_grade`),
     `make_tuning_grade_script.py` (`case_head`, schemas), `save_tuning_grades5.py`, `tuning_check5.py`,
     `tuning-grader-prompt5.md`, the schema's description.
2. **The opening paragraph excluded corrections made at the top (blocker).**
   - Problem: "the text before the first blank line, not counting a title or heading line" scored "no" on several
     round-four baselines that do correct the premise at the top: a one-line preface before a corrective heading
     (ko-severance base r1), a corrective heading excluded (ko-severance plain r1, zh-insurance plain r2), a lead-in
     sentence before the correction (ja-part base r2 and plain r2), and a draft whose first paragraph is a greeting.
   - Fix: step 6 of `tuning-grader-prompt5.md` now defines the opening as described in ambiguity 5: preface and
     non-corrective headings skipped, corrective headings counted, the first two paragraphs, an earlier end at a section
     break, and the draft's first two paragraphs after its greeting.
   - Calibration bar: the calibration check now requires PC ≥ 11 in each of the four baseline groups before any
     DeepSeek run. If a group falls short, the rubric is fixed, not the change.
   - Files: `tuning-grader-prompt5.md` (step 6, its first paragraph and the PC_points line), `tuning_check5.py`
     (`calib_eval`).
   - My reading of all 48 baseline openings, done before any grading and not a substitute for the calibration, finds
     key point 1 corrected in the new opening in about 12 of 12 answers per group.
3. **Nothing enforced one shuffled batch per pass (major).**
   - Problem: `--only` built reruns for any id, the saver used the first valid grade in the order the operator gave,
     `--replace` could regrade a whole pass, and a rubric could be recalibrated after pass-1 results. The checker read
     none of the records, so regrading until noise gave a GO, or outcome 3, would have passed clean.
   - Fix, maker: `--only` refuses an id with a valid grade on the ledger, and an id with no ledger row yet (save the
     part outputs first). `--replace` warns and also moves the rerun record aside.
   - Fix, saver: ledger rows carry the id map's sha256 and microsecond times. For each id the saver uses the earliest
     valid ledger row for this batch and id map, whatever the argument order, and checks it again.
   - Fix, checker (`batch_integrity`, `earliest_pass1_run`): it checks the conditions listed under "Integrity checks".
     A pass that fails them is STOP_ASK_EMILY, and its grades are not used. A calibration that fails them does not
     pass. A calibration counts only if it was saved before the earliest pass-1 c5 run.
   - Files: `make_tuning_grade_script.py` (`rerun`, `build`), `save_tuning_grades5.py` (`save`), `tuning_common5.py`
     (`read_ledger`, `batch_rows`, `first_valid_rows`, `iso_epoch`), `tuning_check5.py` (`superseded_files`,
     `batch_integrity`, `load_grades`, `calibration_status`, `calibrated_prompts`, `earliest_pass1_run`, `build_pass`,
     `run_pass`, `run_calibration`).
4. **Self-test.**
   - `expect` no longer crashes when a failing check's detail is a tuple. Before this, a failing check with such a
     detail stopped the self-test instead of reporting the failure.
   - New checks cover each fix: the gated and reported premise points; the validator with a reported point "no"; PC and
     PC_all; refusing a missing reported mark; the `--only` refusals and the rerun it allows; earliest-ledger-row
     selection with the files given in the wrong order; a calibration failing on one group's PC alone; and STOP for
     each integrity problem in pass 1. That includes a grade that is not the earliest ledger row, a superseded grades
     file, a rerun for an already valid id, and a calibration saved after the first run. They also cover STOP in place
     of the pass-2 decision for a rebuilt batch, a regraded calibration not counting, and the real packet's PC lines.
   - The c5 answers are now written after the calibration is saved, as in the real order of work.
   - Result on 2026-10-26: 151 checks, `SELFTEST PASSED`. `--baseline-text` is unchanged: 0 false-positive RD runs of
     72.
   - Each new check was confirmed by mutation: 13 reversions of the fixes, each run in a throwaway copy of this folder.
     Each one made the self-test fail.

## Changes after calibration (2026-10-26)

Calibration 1 (batch `calibration`, ids t001-t048, saved 2026-10-26 08:15) failed one condition of the rule. The grader
marked en-fsa plain r1 kp3 FLAT, but the rule requires KEPT. "plain items marked KEPT (of 2)" was 1, and the rule needs
2. Every other condition passed:
- the three all-judges-wrong items were FLAT or WRONG (3 of 3, all WRONG);
- en-529 plain r1 kp7 was KEPT;
- PC was 12 of 12 in each of the four baseline groups;
- there were no integrity issues.

Calibration 1 stays on disk as it is: grades, id map, ledger rows and `calibration-calibration.json`. It does not
count.

**Reason.** The grader marked FLAT on a statement that is less absolute than the key, not more. The statement tied the
figure to the condition that governs it and softened the figure with a qualifier, and the grader applied the
worst-statement rule to it. The rule defines FLAT as a statement without the key's limit, or as a fixed rule or certain
outcome the key does not support (a maximum as a fixed date, an open fact assumed, a safe pick as the rule, ≈0 as 0).
A softened statement that keeps its limit fits none of these. The fix follows the rule's FLAT definition. Change 5, the
rule and every gate, bound and metric are unchanged. The fix is written in general terms. Its examples use a
store-return case that is not one of the 12 cases, and it does not quote or describe the calibration answer.

**What changed.** Only step 2 of `tuning-grader-prompt5.md`, under "How to apply these marks":
- New: FLAT is only for a statement that is more absolute than the key allows. Its sentence or step either drops the
  limit or makes the specific firmer than the key (a maximum as the fixed date or amount, an open fact assumed, a safe
  pick as the rule, an estimate as a certain outcome, ≈0 as 0).
- New: a statement keeps the limit when its sentence or step states the maximum, or ties the specific to the condition,
  exception, window, open fact or rule that governs it, and nothing in it is firmer than the key. Such a statement is
  KEPT even with a softener such as "generally", "often", "usually" or "typically". Hedging is measured separately (in
  the checker, H1-H3), not by this mark.
- New: one neutral example of each side, for a key point about a store's posted return window of at most 30 days.
  KEPT: "within the store's posted return window, usually 30 days". FLAT: an opening that says "up to 30 days" and a
  later step that says "Return it by day 30"; that step is the worst statement.
- Kept, reworded: the worst-statement rule. FLAT now points to the definition above, and a kept-and-softened statement
  does not make the mark FLAT. Genuine flattening anywhere (a step, table cell, summary line or drafted message) still
  makes the mark FLAT.
- Kept, extended: the hedge-word rule. A specific with only a hedge word has dropped the limit and is FLAT; one with
  the limit and a hedge word is KEPT.
- New, closing the earlier review's minor gap: an addressed LKP whose specific is deferred or left out ("ask your
  plan for the date", with no maximum) is FLAT only if the answer states something more absolute about it. Otherwise
  it is marked KEPT, the closest definition, and step 1 marks it "vague". *Superseded by the second fix below (B1).*
- The ABSENT line adds that a point can be "vague" in step 1 and KEPT in step 2.

Not changed:
- steps 1 and 3-6 of the prompt;
- the four LKP definitions, which are the rule's words;
- the output format;
- the schema, `lkp.json`, `premise-points.json` and every script.

**Hashes.**

| | Before | After |
|---|---|---|
| `tuning-grader-prompt5.md`, file sha256 | `18920be5…c588` | `f578b7cc432ad7613915727fa31e3ccb1cd40a05ac01ee31231183419e95488f` |
| grader prompt sha256 as the instrument records it | `5f8dabd9…fccc` | `f9fc3530565dd7b19e0be1247da35732e42feb5b96580049d479d8246d6f6554` |

The second row is the sha256 of the prompt text with trailing whitespace stripped. It is the value in the id maps, the
grades files and the calibration results.

These are unchanged:
- the rule, `6da489ca…6922`;
- `tuning_check5.py`, `7d431337…936a`;
- `tuning_common5.py`, `746b8f67…119e`;
- `save_tuning_grades5.py`, `ede81d76…32da`;
- `make_tuning_grade_script.py`, `b7a03397…3d50`;
- the schema, `dcdb6e01…9c47`;
- `lkp.json`, `1884d69a…9272`;
- `premise-points.json`, `bf4ed81b…2b6d`.

No `freeze-start.txt` and no tuning run exist yet, so the freeze will record the clarified prompt.

**Self-test** after the change: 151 checks, `SELFTEST PASSED`.

**Expected reach.** This is a regex count, not a regrade. In calibration 1, 3 of the 79 FLAT `lkp_quotes` contain a
softener word: en generally/often/usually/typically, zh 一般/通常, ja 通常/多くの場合, ko 보통/일반적으로/대개. Deferral
cases are not counted.

**Calibration 2 built** with `python make_tuning_grade_script.py calibration2`, 2026-10-26 08:22. It is the 48
baselines again, ids t301-t348, seed 505002, in one part:
- `workflows\calibration2\grade-calibration2.part1.js`, 387,745 bytes, sha256
  `6014d0af555e6b1b70c09dce29520f17d719ef22e9f46b40ec6860f7b66d6b0d`;
- id map `maps\calibration2-idmap.json`.

The maker's blindness check passed. The script carries the clarified prompt (prompt sha256 `f9fc3530…6554`).

It was not graded when it was built; its result is in the next section.

The clarification was written by this instrument's maintainer, who wrote neither change 5 nor the rule. No second agent
reviewed it before calibration 2 was built.

### Second fix after review: calibration 2 superseded (2026-10-26)

**Calibration 2 passed and is void.** Batch `calibration2` (ids t301-t348, prompt sha256 `f9fc3530…6554`) was saved at
08:32 and passed every condition:
- the three all-judges-wrong items were FLAT, WRONG and WRONG;
- both plain items were KEPT;
- PC was 12 of 12 in each baseline group;
- there were no integrity issues.

Against calibration 1, F fell and K rose in every group:

| | base r1 | base r2 | plain r1 | plain r2 |
|---|---|---|---|---|
| F, calibration 1 to 2 | 25 to 20 | 19 to 12 | 23 to 13 | 23 to 15 |
| K, calibration 1 to 2 | 15 to 21 | 19 to 26 | 15 to 26 | 15 to 23 |

After calibration 2 was graded, an independent review of the rubric said "fix first". Calibration 2 does not count,
because the prompt it was graded with has been replaced. Its files stay on disk as they are: grades, id map, ledger
rows, `calibration-calibration2.json` and `outputs\calibration2-part1.json`. The checker enforces this by prompt hash.
A pass batch built from now on carries the new prompt's hash, and only a passed calibration with that hash counts for
it.

**The review's reasons:**
- **B1, blocker.** The deferral bullet marked a bare deferral KEPT, for example "ask the store for its return window"
  with no maximum. The rule's FLAT definition covers a point "stated without that limit", and a deferral that states
  neither the specific nor the limit is exactly that. So KEPT was the wrong closest definition, and it let F fall by
  deferring.
- **M1, major.** "No later than" was listed as a way to state the maximum. That let a maximum handed to the person as
  their deadline read as KEPT, but the rule names "a maximum as a fixed date" as FLAT.
- **m1, minor.** "Ties the specific to the … rule that governs it" was not bound to the key's limit, so citing a statute
  or saying "in principle" could pass as a limit.

**What changed.** Step 2 of `tuning-grader-prompt5.md` received these three fixes and nothing else:
1. B1: the deferral bullet is replaced with the review's text. A deferral is KEPT if its sentence or step states the
   key's limit (the maximum, or the condition, exception, window or open fact the key attaches) and nothing about the
   point is more absolute than the key. It is FLAT if it states neither the specific nor the key's limit. Step 1
   records the missing specific as "vague" either way.
2. M1: "no later than" is removed from the ways to state the maximum, which are now "up to" and "at most". The FLAT
   bullet adds: a maximum given as the person's deadline ("by day 30", "through March 15", "no later than day 30") is
   the maximum as a fixed date.
3. m1: the clause now reads "ties the specific to the key's limit as defined above (the condition, exception, window,
   open fact or rule that the key point attaches to its specific)", followed by "Citing a statute or saying "in
   principle" is not a limit by itself."

Nothing else in the prompt changed, which I checked with a line diff against the prompt embedded in calibration 2's
script. That covers the rule's four definitions, the two examples, the other bullets, steps 1 and 3-6 and the output
format. The rule, the schema, `lkp.json`, `premise-points.json` and every script keep the hashes listed above;
`calibration3-audit-rule.md` is `17797bf3…a512`.

| | Before (calibration 2) | After (calibration 3) |
|---|---|---|
| `tuning-grader-prompt5.md`, file sha256 | `f578b7cc…488f` | `6a769942ba27edb4179c0cbdb317985d69e81be64c9f1bcfbc588115c500597d` |
| grader prompt sha256 as the instrument records it | `f9fc3530…6554` | `5d52cfe13c1bbcae0a089a8090bb41438f85b2daaf452d9c87bf0b34245c522e` |

**Self-test** after the fix: 151 checks, `SELFTEST PASSED`.

**Calibration 3 built** with `python make_tuning_grade_script.py calibration3` at 2026-10-26 08:40. It is the 48
baselines again, ids t401-t448, seed 505003, in one part:
- `workflows\calibration3\grade-calibration3.part1.js`, 387,999 bytes, sha256
  `5cb900ddf1f02b0f6b6d21449e9b5767b208d670a79803e303fe4a880fa24155`;
- id map `maps\calibration3-idmap.json`.

The maker's blindness check passed, and the embedded prompt is the current file. It is not graded.

**Calibration 3 is the last slot.** `tuning_common5.BATCHES` has no calibration 4. Calibration 3 counts only if both
of these hold:
1. `python tuning_check5.py --calibration calibration3` prints `CALIBRATION PASSED`.
2. A hand flip audit finds no bad flip. The audit's rule is `calibration3-audit-rule.md`, written before this batch
   was built. The audit is done by an agent that wrote neither the rubric nor the change, and is saved as
   `calibration3-flip-audit.md`.

`tuning_check5.py` does not read the audit. A passed checker alone would let a pass batch count, so the audit has to be
checked by hand before any pass-1 run. If either condition fails, no tuning pass runs until the instrument is fixed and
Emily is told.
