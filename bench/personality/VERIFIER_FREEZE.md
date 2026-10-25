# Verifier freeze

Owner: the verifier owner (builds nothing in this benchmark). Gates: `GATES.md`. This file records the freeze and says how it is checked. `verify.py` reads the stage-1 commit from the line below; D4 fails as "metric missing" until it is filled in.

Stage-1 freeze commit: none yet (blocked, see below)

## Status (2026-10-25)

**Stage 1 is blocked on two builder fixes.** Everything on the verifier side is written, committed and tested; the freeze is one commit once the fixes land. The brief says to leave the freeze until builder fixes are done, and both files are number-making, so they cannot change after the freeze.

What was tested before this commit:

- `verify.py --self-test`: all 195 gates fail on an empty metrics object with "metric missing"; each gate goes green on a passing case and red on a failing one, and fails as missing when a key is absent, None, NaN, infinite or a bool; the 16 named holes from CHEAPEST_PASS.md fail as missing; zero-plain hedge comparisons and N6 "not measurable" behave.
- `measure_all.py --self-test`: the two-system closed form equals `bt.fit`; the joint bootstrap; the language identifier; kappa; boilerplate; format shape; NaN never stored; round three's hedge and source lists and exclusions; every ja and ko term found verbatim in WIN_CRITERIA.md.
- `samples.py --self-test`, `metrics.py --self-test`, `bt.py --self-test`.
- End to end on synthetic data shaped like the real run (2,390 answers, every judging set, transcripts, labels, ledger, CONFIRM commit), in `W:\AgentData\logs\gravitas-personality-verify-synth` (generator `synth.py`, reports `*.verify.txt`). A clean run passes 177 of 195; the 18 failures are artefacts of random synthetic text plus D4 (no freeze yet). Each adversarial run fails exactly the gate meant for it: gutted answers (C5, N3, N5), a held-out phrase in the rule (N9), a pasted sentence (N2), a rule line in a plain transcript (D2), a second judging run (D1.judging), Claude verdicts copied from DeepSeek (B5, B2, K0), DeepSeek random on Truthful (B5t re-sources Truthful to Claude), DeepSeek preferring its own answers (B6a moves the Gemini platform to Claude). A full run takes about 40 seconds.
- On the real pilot data (no stage-2 record yet) every gate fails as missing, as it should.

## Builder fixes needed

Blocking (number-making files):

1. **metrics.py, hedge lists.** The docstring says the hedge lists are WIN_CRITERIA's round-one and extended lists. For zh and en they are not: WIN_CRITERIA 8 means round three's `H_ROUND1` (tally.py's list: 可能, 大概, 也许, 或许, 以…为准, 建议…核实/确认, 不确定, 请咨询, 仅供参考, may, might, probably, check with, confirm with, not sure, verify) and `H_EXTENDED` (criteria item 9), with 不可能 and "May" as a month excluded, as in `docs/dsh-ab/round-three/verdict.py`. metrics.py has, for example, "could", "possibly", "perhaps", "consult" and lacks "probably", "not sure", 不确定, 请咨询. The verifier no longer reads these numbers (C6 reads the lists from verdict.py itself), but `answer_stats.py` reports them, so tuning against them would steer the candidate by a different list from the one C6 gates. Fix: use round three's lists and exclusions in `metrics.HEDGES` (or relabel the fields as not WIN_CRITERIA's).
2. **judge.py, JUDGE_TEMPLATE.** "You are rating how strongly the trait appears, not which answer is better, more correct overall or more helpful" contradicts Truthful, whose trait is being correct. It is the likeliest cause of the pilot's low Truthful agreement (kappa 0.0, 0.22 and 0.55 for the three judge pairs). Fix: drop "more correct overall" from that sentence (for example: "not which answer is better or more helpful overall"). The new Truthful definition already says "for this trait, being correct is the trait itself", but two contradicting sentences in one prompt make a noisy judge. This changes verdicts, so it must land before cal0.

Recommended, not blocking:

3. **judge.py, FOCUS and GUARD.** They still describe the 16-trait plan, so `--plan focus` would judge 16 or 17 traits. Either set FOCUS to the 8 judged traits and GUARD to an empty list, or always pass the explicit plan printed by `samples.py plan`. D1.judging fails any set built with other traits.

## What stage 1 freezes

Every file in `bench/personality` (D4 diffs the whole folder and counts untracked files, VERIFIER_FREEZE.md excepted), and the two documents the verifier reads its lists from, already committed: `docs/dsh-ab/WIN_CRITERIA.md` and `docs/dsh-ab/round-three/verdict.py`.

| file | why it can move a number |
|---|---|
| verify.py, measure_all.py, samples.py, GATES.md | the gates, every measurement, every sample and prompt |
| traits.json | the rubric judges apply (8 definitions owned by the verifier owner) |
| judge.py | prompt template, scrubbing, order and judge assignment, parser |
| bt.py, metrics.py, calibrate.py, answer_stats.py | the fit the closed form is checked against; text metrics (C5, C10); reports |
| filter_questions.py, gen_questions.py, seeds.json | which questions exist and how they are split |
| answer_dsh.py, answer_agy.py, answer_raw.py, judge_agy.py, dshbatch.py, dsh/llm-batch.mjs, ledger.py | how answers and verdicts are produced and recorded |
| plan_cost.py, spend.py, GATES_SPEC.md, CHEAPEST_PASS.md | record of the plan and the review |

## Stage-1 procedure (when the fixes are committed)

1. Read the builder's diff since this commit; confirm it touches only the fixes.
2. Run the five self-tests and the synthetic end-to-end run again.
3. Record here: `Stage-1 freeze commit: <the commit holding the fixed state>`, plus the sha256 of every file in the table, and commit this file alone (Emily's voice, no attribution line).
4. From then on D4 requires `git diff <freeze commit> -- bench/personality docs/dsh-ab/WIN_CRITERIA.md docs/dsh-ab/round-three/verdict.py` to be empty apart from this file, and no untracked file in the folder. Any change after that is a re-freeze, made only between rounds with the evidence written here.

## Stage 2: freezing the data (I will be messaged to do it)

**What I need, in this order:**

1. The question set, made by the frozen `filter_questions.py` **with the rating call** (not `--no-rate`), and its name SET (`DATA/questions/SET/{all,tuning,heldout}.jsonl`, `report.json`, and `DATA/batches/rate-SET.out.jsonl`).
2. The A9 controls: the builder runs `samples.py export controls` (24 prompts), sends them through DeepSeek, and saves `DATA/labels/native_controls.jsonl` as `{id, lang, q}` (the reply as `q`), with one ledger line `labels-import`, name `native_controls`.
3. GRAV_LINK (`W:/Projects/gravitas-claim-check`) at the commit every DSH Gravitas run will use, with a clean working tree.
4. The agy homes as they will be used (`home-plain`, `home-grav-<lang>`); candidate homes are created later and are checked through CONFIRM and D2 instead.
5. No held-out answer launched yet by any arm, and nothing judged on held-out.

**What I do:**

1. `samples.py build SET`; read `DATA/samples/index.json` and stop if any sample is short.
2. Write `bench/freeze/FREEZE_DATA.json` (outside the frozen folder) with: `set`; `files` = sha256 of `questions/SET/{all,tuning,heldout}.jsonl`, `questions/SET/report.json`, `batches/rate-SET.out.jsonl`, every `samples/*.jsonl` and `samples/index.json`, `labels/native_controls.jsonl`, `rules/base/*.md`; `ledger_prefix` = the line count of `ledger.jsonl` and the sha256 of those lines; `agy_config` = a tree hash of each home's `.gemini/config`; `grav_link_head`; `rules_base` = sha256 per language; `pre_existing_judging` = the judging folders that exist (the pilots).
3. Commit that file alone and give the commit here. From then on the same D4 gate checks every one of those hashes, and the judging set names, recipes and weights are the ones in `samples.py` (frozen at stage 1).

## What the builder must do before and during the first real run

Before any held-out run:

- Fixes 1 and 2 (and 3 if wanted), then tell the coordinator so stage 1 can be frozen.
- Run `filter_questions.py` with rating; then stage 2.
- Run ds-plain and ds-grav on the tuning split, then **cal0** (`samples.py plan` prints the command; DeepSeek with `judge.py run`; Claude with `judge.py export cal0 claude --all`, one import with `--all`; Gemini Flash on the same 120 only if the agy runs allow), and the blind critic (`samples.py export critic`, saved as `judging/cal0/critic.jsonl` `{job, raw}`, one `labels-import` line, name `critic`). Run `verify.py --only K0`. **Do not judge anything on held-out until K0 passes.** If it fails, stop and send me the numbers (rubric revision, re-freeze, cal1).
- Keep Claude and Gemini Flash out of every tuning judging set (D3 checks it). The candidate's tuning judging uses DeepSeek only and never the cal15 or cal15b questions.
- Question labels: `samples.py export ql` to Claude, saved as `labels/ql.jsonl` `{qid, labeller: "claude", raw}`, one `labels-import` line (name `ql`), before the candidate's first held-out launch.
- Confirm the candidate: commit `bench/confirm/NAME.json` = `{"name": NAME, "rules": {"en.md": sha256, "ja.md": ..., "ko.md": ..., "zh-CN.md": ...}}` (sha256 of `DATA/rules/NAME/*.md`) **before** its first held-out launch or held-out judging build. One candidate only.

Runs:

- DSH: ds-plain, ds-grav, ds-grav:NAME on `samples/heldout.jsonl`; ds-plain-aa, ds-grav-aa on `samples/aa150.jsonl`. Gemini: gm-plain, gm-grav, gm-grav:NAME on `samples/gm150.jsonl`; **gm-plain-aa and gm-grav-aa on `samples/gmaa40.jsonl` (80 Argon runs, not in the lean plan's list but needed for C1, C2 and C8 on Gemini)**.
- One successful launch per (arm, question); a failed launch may be retried, a successful one never re-rolled (N11).

Judging (the exact commands come from `samples.py plan`):

- Build each frozen set once, under its frozen name, with the 8-trait plan, after all its answers exist. DeepSeek sets: `judge.py run NAME` once. Claude sets: `judge.py export NAME claude`, 40 per subagent call, raw reply kept per job, `judge.py import NAME claude FILE` once.
- Labels after the runs: `samples.py export n3points` then `n3marks --name NAME`, `n4 --name NAME` (Claude with web search), `native`; each saved under `DATA/labels/` with its raw replies and one `labels-import` ledger line.
- Then `verify.py`. The verdict is its exit code and its last line.

## Still needed from someone who did not write these gates

QUALITY_LOOP asks that an agent who did not write the gates answer, before any build, what the cheapest pass of each gate is. The draft had that review (CHEAPEST_PASS.md); the gates added for the lean plan have not: the routing gates B5t, B6a and B6b, K0, C11, C10's per-1,000 form, D5, D6, S, QL and A11, and the changed N1, N3, N4, N7 and N9. I could not run a second agent in this task. The coordinator should have one review those before the first held-out run; any answer that finds a cheap pass becomes a negative gate in a re-freeze before the run.

## Labelling load

Claude Sonnet 5.5: 2,480 verdicts (2,696 if a rubric revision needs cal1). Gemini 3.8 Flash: none required; 120 optional on cal0. DeepSeek: 16,456 verdicts for the verifier's sets, about 14 USD, plus the builder's tuning judging. Details in GATES.md.
