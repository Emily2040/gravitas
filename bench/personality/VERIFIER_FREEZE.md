# Verifier freeze

Owner: the verifier owner (builds nothing in this benchmark). Gates: `GATES.md`. This file records the freeze and says how it is checked. `verify.py` reads the stage-1 commit from the line below; D4 fails as "metric missing" until it is filled in.

Stage-1 freeze commit: recorded in the next commit of this file

## Status (2026-10-25)

**Stage 1 is frozen at the commit named above.** The three builder fixes I asked for landed in 25d1f9a and I checked them before freezing:

1. metrics.py: the zh and en hedge lists are now round three's H_ROUND1 and H_EXTENDED with its two exclusions, and ja and ko are WIN_CRITERIA's lists. I checked that they equal, item for item, the lists the verifier reads from verdict.py and WIN_CRITERIA.md. One difference remains and is accepted: metrics.py counts per 1,000 prose characters (markdown removed), while round three and C6 count per 1,000 characters of the raw final. Only reports (answer_stats.py) use metrics.py's rate; no gate does.
2. judge.py: the template no longer says "more correct overall".
3. judge.py: FOCUS is the 8 judged traits and `--plan focus` returns exactly those 8.

Tests at the freeze:

- `verify.py --self-test`: all 195 gates fail on an empty metrics object with "metric missing"; each gate goes green on a passing case and red on a failing one, and fails as missing when a key is absent, None, NaN, infinite or a bool; the 16 named holes from CHEAPEST_PASS.md fail as missing; zero-plain hedge comparisons and N6 "not measurable" behave.
- `measure_all.py --self-test`: the two-system closed form equals `bt.fit`; the joint bootstrap; the language identifier; kappa; boilerplate; format shape; NaN never stored; round three's hedge and source lists and exclusions; every ja and ko term found verbatim in WIN_CRITERIA.md.
- `samples.py`, `metrics.py` and `bt.py` self-tests.
- End to end on synthetic data shaped like the real run (2,390 answers, every judging set, transcripts, labels, ledger, CONFIRM commit), in `W:\AgentData\logs\gravitas-personality-verify-synth` (generator `synth.py`, reports `*.verify.txt` and `*.freeze-check.txt`). A clean run passes 177 of 195; the 18 failures are artefacts of random synthetic text plus D4 (the synthetic repo has no freeze). Each adversarial run fails exactly the gate meant for it: gutted answers (C5, N3, N5), a held-out phrase in the rule (N9), a pasted sentence (N2), a rule line in a plain transcript (D2), a second judging run (D1.judging), Claude verdicts copied from DeepSeek (B5, B2, K0), DeepSeek random on Truthful (B5t re-sources Truthful to Claude), DeepSeek preferring its own answers (B6a moves the Gemini platform to Claude). The same outcomes hold after the builder's fixes. A full run takes about 40 seconds.
- On the real pilot data (no stage-2 record yet) every gate fails as missing, as it should.

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

## How stage 1 was made, and how it is checked

1. I read the builder's diff (25d1f9a against my commit 5fd1377): it touches only metrics.py and judge.py, as asked.
2. I ran the five self-tests and the synthetic runs again (above), then corrected the lines in GATES.md and this file that described the fixes as pending.
3. That state is the freeze commit named at the top. A later commit records its hash and the sha256 table below and touches this file only.
4. From then on D4 requires `git diff <freeze commit> -- bench/personality docs/dsh-ab/WIN_CRITERIA.md docs/dsh-ab/round-three/verdict.py` to be empty apart from this file, and no untracked file in the folder. A change after that is a re-freeze, made only between rounds, with the evidence written here. Because this file can be edited, the coordinator keeps the freeze hash separately and compares it with the one `verify.py` prints on its first line.

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
