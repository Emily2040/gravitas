# Verifier freeze

Owner: the verifier owner (builds nothing in this benchmark). Gates: `GATES.md`. This file records the freeze and says how it is checked. `verify.py` reads the current freeze commit from the line below; D4 fails as "metric missing" until it is filled in.

Stage-1 freeze commit: recorded in the next commit of this file

## History

- **Stage 1, 2026-10-25:** commit `ec91a8d5e5e3b831693ea470302f09d888fe5671` (recorded in 66b5ed7), after the builder's three fixes in 25d1f9a. Superseded by stage 1b; nothing on held-out had run.
- **Stage 1b, 2026-10-25 (this freeze):** re-freeze before any held-out run, after the second cheapest-pass review (`bench/reviews/CHEAPEST_PASS_2.md`, 6ec2d96) and Emily's approval of lingua-py. The commit is named at the top once made. Decisions on every review item are in GATES.md.

## What changed in stage 1b

- **lingua-language-detector 2.1.1** (Apache-2.0, released 2025-05-27, the current release on 2026-10-25) now identifies the language of every question for **A2 and A5 only**, with `LanguageDetectorBuilder.from_languages(CHINESE, ENGLISH, JAPANESE, KOREAN)` plus two guards it cannot give itself (Traditional script; another Latin-script language). It is pinned by hash in `bench/env/requirements-lingua.txt` (85c1017) and installed in `W:\AgentData\logs\gravitas-personality\venv` (created with `--system-site-packages`; Python 3.10.11, numpy 2.2.6, scipy 1.13.1, scikit-learn 1.7.2). **Run the verifier with `W:\AgentData\logs\gravitas-personality\venv\Scripts\python.exe verify.py`.** Under another Python, or another lingua version, A2 and A5 fail as "metric missing". Answers (N8) and the A9 controls keep the stdlib identifier. On v1, lingua agrees with the label on 1,106 of 1,106 questions.
- **Provenance and order (P1, P2):** every Claude label is checked against its subagent transcript and the frozen first message (`samples.wrapper_text`); the critic against judge_agy's ledger and transcripts; five orderings from the ledger and git. The frozen wrappers reproduce all 12 labeller transcripts that exist today, and P1 passes on today's ql (6 batches) and native (2 batches) labels.
- **Routing and debiasing:** a trait moves to Claude only when Claude is no friendlier; otherwise it is unreliable. DeepSeek's extra favour for Gravitas is subtracted (B6b, B6m) instead of switching judges. B6a is reported only. B5 and K0 use trait-stratified kappa, on plain-against-Gravitas pairs only.
- **Slices and their instruments:** QL covers the whole held-out set (ql2: 270 more questions); N1h and N7h measure hedging in the text; C7 uses the new instrument trait "Challenges the Person" (sets chal-ds-base, chal-ds-cand, chal-gm-base, chal-gm-cand, DeepSeek).
- **Content and format:** N3 and N4 paired with full coverage, N4 per checked claim, N6's half rule, C10 separator lines and italics, C11 count floor, N9 for Korean.
- **The blind critic** runs on Gemini 3.8 Flash (96 runs).
- **Freeze scope:** D4 also diffs `bench/env/requirements-lingua.txt`; stage 2 hashes the DSH profiles, `overlays/lean.yml` and lingua's installed RECORD; D4 checks every DeepSeek judge call's model, candidate agy homes against their base homes, and GRAV_LINK's working tree.
- **Spend:** D5 takes the larger of the usage records and the account balance drop Emily reads.
- **S0, A11 recomputed, A9 per language, D6 from agy's per-run logs, QL at 0.99.**

## Tests at the freeze

- `verify.py --self-test`: all 230 gates fail on an empty metrics object with "metric missing"; each gate goes green and red, and fails as missing when a key is absent, None, NaN, infinite or a bool; the 16 named holes from CHEAPEST_PASS.md fail as missing; B5t refuses the friendlier judge; B6b debiases; N6's half rule.
- `measure_all.py --self-test` (under the venv, so lingua is tested too), `samples.py`, `metrics.py`, `bt.py` self-tests.
- End to end on synthetic data shaped like the real run, with transcripts, both question-label batches, the challenge sets, the Gemini critic, the stage-2 commit and a balance file (`W:\AgentData\logs\gravitas-personality-verify-synth\synth2.py`, folders `s2-*`, reports `s2-*.verify.txt`). A clean run passes 209 of 230: the 21 failures are artefacts of random synthetic text (near-copies, a doubt and hedge pattern the generator puts everywhere, random per-language noise) plus D4 (the synthetic repo has no freeze). Each adversarial run fails exactly the gate meant for it:

| scenario | fails |
|---|---|
| Gravitas challenges people who said nothing wrong | C7, every platform and arm |
| a labeller wrapper with one extra sentence | P1 for every Claude judging set in that batch's unit |
| one ql batch labelled twice | P1.ql |
| cal0 Claude imported after DeepSeek ran | P2 |
| a held-out Korean question pasted into the candidate's ko.md | N9 |
| DeepSeek random on Slop while Claude favours Gravitas on it | B5t.Slop UNRELIABLE, and every gate that uses Slop |
| DeepSeek favours Gravitas by about 0.1 of share | B6b and B6m print DEBIASED and the points move back 56 to 83 Elo |
| gutted answers, a pasted sentence, a rule line in a plain transcript, a second judging run, copied Claude verdicts, DeepSeek random on Truthful, DeepSeek preferring its own answers | as at stage 1 (regression run on the new generator) |

- On the real data, P1 passes for ql and native; every other gate fails as missing until stage 2, as it should.

## Frozen files and their sha256 at the freeze commit

Filled in by the commit after the freeze, from the commit's own blobs.

## What the freeze covers

Every file in `bench/personality` (D4 diffs the whole folder and counts untracked files, VERIFIER_FREEZE.md excepted), `bench/env/requirements-lingua.txt`, and the two documents the verifier reads its lists from: `docs/dsh-ab/WIN_CRITERIA.md` and `docs/dsh-ab/round-three/verdict.py`. The venv itself cannot be committed; its lingua installation is frozen at stage 2 by the sha256 of `lingua_language_detector-2.1.1.dist-info/RECORD` (which lists every installed file's hash), and measure_all refuses any other lingua version.

| file | why it can move a number |
|---|---|
| verify.py, measure_all.py, samples.py, GATES.md | the gates, every measurement, every sample, prompt and labeller wrapper |
| traits.json | the rubric (8 judged definitions and C7's instrument trait, owned by the verifier owner) |
| judge.py | prompt template, scrubbing, order and judge assignment, parser |
| bt.py, metrics.py, calibrate.py, answer_stats.py | the fit the closed form is checked against; text metrics (C5, C10); reports |
| filter_questions.py, gen_questions.py, seeds.json | which questions exist; A11 rebuilds the rating prompt with filter_questions |
| answer_dsh.py, answer_agy.py, answer_raw.py, judge_agy.py, dshbatch.py, dsh/llm-batch.mjs, ledger.py | how answers and verdicts are produced and recorded |
| plan_cost.py, spend.py, GATES_SPEC.md, CHEAPEST_PASS.md | record of the plan and the first review |
| bench/env/requirements-lingua.txt | the language identifier for A2 and A5 |

## How it is checked

D4 requires `git diff <freeze commit> -- bench/personality bench/env/requirements-lingua.txt docs/dsh-ab/WIN_CRITERIA.md docs/dsh-ab/round-three/verdict.py` to be empty apart from this file, and no untracked file in the folder. A later change is a re-freeze, made only between rounds, with the evidence written here. Because this file can be edited, the coordinator keeps the freeze hash separately and compares it with the one `verify.py` prints on its first line.

## Stage 2: freezing the data (I will be messaged to do it)

**What I need, in this order:**

1. The question set v1, made by the frozen `filter_questions.py` with the rating call: `DATA/questions/v1/{all,tuning,heldout}.jsonl`, `report.json`, `DATA/batches/rate-v1.{in,out}.jsonl`.
2. `samples.py build v1` run again with the stage-1b `samples.py` (it adds `ql270.jsonl`; every existing sample file comes out identical, which I check).
3. The A9 controls: `DATA/labels/native_controls.jsonl` and their DeepSeek batch `DATA/batches/controls-*.{in,out}.jsonl` (done).
4. **Emily's DeepSeek account balance in USD**, read just before stage 2 (for D5). She reads it again after the last run and the coordinator commits `bench/freeze/BALANCE_AFTER.json` = `{"usd": <balance>, "read_at": "<time>"}`.
5. GRAV_LINK at the commit every DSH Gravitas run will use, with a clean working tree.
6. The agy homes as they will be used (`home-plain`, `home-grav-<lang>`).
7. No held-out answer launched yet by any arm, and nothing judged on held-out (S0 checks it).

**What I do:**

1. Check every sample against the recipe and stop if any is short or differs.
2. Write `bench/freeze/FREEZE_DATA.json` (outside the frozen folder) with: `set`; `files` = sha256 of the question files, `report.json`, the rating batch, every `samples/*` file, `labels/native_controls.jsonl`, the controls batch, `overlays/lean.yml`, `rules/base/*.md`; `external_files` = sha256 of `W:\AgentData\dsh_home\profiles\gv-plain\` and `gv-grav\` `cordis.patch.yml`, `cordis.yml`, `package.json`, `pnpm-workspace.yaml` and `pnpm-lock.yaml` where present, and of lingua's `RECORD` in the venv; `ledger_prefix` = the line count of `ledger.jsonl` and the sha256 of those lines (the ledger's first N lines joined by newlines, as `measure_all.measure_data_freeze` reads them); `agy_config` = a tree hash of each home's `.gemini/config`; `grav_link_head`; `rules_base`; `pre_existing_judging` = the judging folders that exist then; `deepseek_balance_before_usd`.
3. Commit that file alone. Its commit time is the stage-2 time that S0 and D6 use.

## What the builder must do before and during the first real run

Before any held-out run, in this order:

1. Run `samples.py build v1` again (adds ql270), then stage 2.
2. **ql2:** `samples.py export ql2` (270 prompts) to Claude in batches `DATA/labels/ql2.batchN.prompts.jsonl`, one Sonnet 5.5 subagent per batch whose whole first message is `samples.py wrapper ql2 <n> <input> <output>`, the transcript copied to `DATA/labels/transcripts/` with a `labeller-transcript` ledger line, the raws imported once as `DATA/labels/ql2.jsonl` with one `labels-import` line (name `ql2`). Every Claude label from now on follows the same scheme (P1); never re-run a batch.
3. Tune the candidate on the tuning split with DeepSeek only; never judge the cal15 or cal15b questions with the candidate; keep Claude and Gemini out of tuning.
4. **Confirm the candidate:** commit `bench/confirm/NAME.json` = `{"name": NAME, "rules": {"en.md": sha256, "ja.md": ..., "ko.md": ..., "zh-CN.md": ...}}` before cal0's Claude labels and before any held-out run.
5. **cal0** (`samples.py plan` prints the build command): Claude first (`judge.py export cal0 claude --all`, batches as in step 2 with the "judge" wrapper, one `judge.py import cal0 claude FILE --all`), then DeepSeek (`judge.py run cal0`). Then the critic: `samples.py export critic` writes `judging/cal0/critic.prompts.jsonl`; run `judge_agy.py cal0 critic` (Gemini 3.8 Flash, 96 runs, once). Then `verify.py --only K0`. **Nothing on held-out is judged until K0 passes.** If it fails, stop and send me the numbers (rubric revision, re-freeze, cal1).

Runs:

- DSH: ds-plain, ds-grav, ds-grav:NAME on `samples/heldout.jsonl`; ds-plain-aa, ds-grav-aa on `samples/aa150.jsonl`. Gemini: gm-plain, gm-grav, gm-grav:NAME on `samples/gm150.jsonl`; gm-plain-aa and gm-grav-aa on `samples/gmaa40.jsonl` (80 Argon runs).
- One successful launch per (arm, question); never re-roll a success (N11). Keep GRAV_LINK clean.

Judging (exact commands from `samples.py plan`):

- Every Claude set (hoc-ds-base, hoc-ds-cand, hoc-gm-base, hoc-gm-cand, hoc-xf, swapc) is built, labelled and imported **before** its DeepSeek counterpart (ho-ds-base, ho-ds-cand, ho-gm-base, ho-gm-cand, ho-xf) is run (P2). Each set is built once and judged once per judge.
- The challenge sets (chal-ds-base, chal-ds-cand, chal-gm-base, chal-gm-cand), the A/A sets and the swap sets are DeepSeek only.
- Labels after the runs: `samples.py export n3points`, then `n3marks --name NAME`, `n4 --name NAME` (Claude with web search; the "checker" wrapper), each by the P1 scheme with one `labels-import` line.
- After the last run, Emily reads the DeepSeek balance; commit `bench/freeze/BALANCE_AFTER.json`.
- Then `W:\AgentData\logs\gravitas-personality\venv\Scripts\python.exe verify.py`. The verdict is its exit code and its last line.

## Known today, before any held-out run

- **A9 fails on English today**: the reader picked Emily's English seed over the English draft in 11 of 12 pairs (test accuracy 0.92, outside 3 to 9 of 12). The pooled accuracy (32 of 48) passes. Unless English is redrafted before stage 2 (then ql, ql2 and native must be redone for those questions, under new import names), the final verdict will carry this failure. This is the coordinator's and Emily's call.
- The real-data P1 check passes for ql and native.

## Labelling load

Claude Sonnet 5.5: 2,654 verdicts and labels (312 already done; 2,774 if a rubric revision needs cal1). Gemini 3.8 Flash: 96 (the critic). DeepSeek: 17,776 verdicts for the verifier's sets, about 15 USD, plus the builder's tuning judging. Details in GATES.md.
