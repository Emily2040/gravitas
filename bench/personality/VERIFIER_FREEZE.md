# Verifier freeze

Owner: the verifier owner (builds nothing in this benchmark). Gates: `GATES.md`. This file records the freeze and says how it is checked. `verify.py` reads the current freeze commit from the line below; D4 fails as "metric missing" until it is filled in.

Stage-1 freeze commit: recorded in the next commit of this file

## History

- **Stage 1, 2026-10-25:** commit `ec91a8d5e5e3b831693ea470302f09d888fe5671` (recorded in 66b5ed7), after the builder's three fixes in 25d1f9a. Superseded by stage 1b; nothing on held-out had run.
- **Stage 1b, 2026-10-25:** commit `35518d190e30f5682bacc2008be2a34744d68f4d` (recorded in 09f0653), a re-freeze before any held-out run, after the second cheapest-pass review (`bench/reviews/CHEAPEST_PASS_2.md`, 6ec2d96) and Emily's approval of lingua-py. Decisions on every review item are in GATES.md. Superseded by stage 1c; nothing on held-out had run.
- **Stage 1c, 2026-10-26:** commit `cc42b583d8b8a694944733c1aa6694384c99bd9f`, the D3 amendment, written before the stage-2 freeze and before any held-out result, on the coordinator's instruction. Text and reasons in GATES.md, "D3 amendment". Superseded by stage 1d; nothing on held-out had run.
- **Stage 1d, 2026-10-26:** D5 compared the usage records since the pilots with the balance drop since stage 2, two different spans, so records deleted after stage 2 could hide spend. D5 now takes the larger of the records since the pilots and the records at stage 2 (`deepseek_records_usd_at_stage2`, measured by the verifier's own instrument when the data are frozen) plus the balance drop. Found while writing the stage-2 record, before it was committed. The stage-2 data record (165dcc7) was written against this verifier and needs no change for later stages, which touch no data. Commit `05b278ade19c4e11d88a0b4217a43b06f96c245a`.
- **Stage 1e, 2026-10-26 (this freeze):** the D5 amendment. Emily raised the DeepSeek cap ("Yes that's ok spend more", in answer to a projection of 57-73 USD against 50); the coordinator operates it as 60 USD. New gate D5a (0 to 60 USD, 0 peak launches); the original D5 (50 USD) is reported with its result and marked SUPERSEDED once measured. Made before any held-out run; cal0 had been built and exported, nothing judged. Text in GATES.md, "D5 amendment". The commit is named at the top.

## What changed in stage 1c (the D3 amendment)

- The original D3 needed a confirmed candidate on held-out, so an honest rejection of the one candidate failed it and every candidate gate failed as missing. New gates: **D3a** (exactly one candidate designed and tuned under a recorded decision rule; the verifier recomputes the rule; the held-out outcome is the one it gives) and **D3r** (the rule in the ledger before the candidate's tuning set was built). When D3a passes and measures "not confirmed", the candidate's gates print N/A and the original D3 prints as failing and SUPERSEDED; otherwise nothing is excused. P2's "CONFIRM before cal0's Claude labels" became "the candidate's decision before cal0's Claude labels"; the candidate's orderings and agy-home check moved to P2cand and D4cand. The B5t per-trait minimum is 80 shared comparisons (two Claude set pairs when only base runs). S0 scans every judging folder that existed at stage 2 (`judging_at_stage2`), not only the pilots. 234 gates.
- **The candidate `bottomline` on today's data:** D3a passes; the recomputed decision is NOT CONFIRMED (Admits Uncertainty -33.9 [-59.6, -9.9]; Bottom-Line Summary +54.3 [+28.0, +82.3]), matching analysis/bt-cand-vs-base.json. **D3r fails**: the rule's ledger line (10:22:09) is 51 seconds after `judge-build tune-ds-cand` (10:21:18); the batch had started at 10:21:50 and, by the builder's account, returned its first result at 10:22:04.9, before DECISION.md was written at 10:22:08.99. DECISION.md's header ("written 10:25, before any tune-ds-cand verdict existed") is contradicted by the ledger and the file time. The final report will show D3r failing for this reason.
- Tests: all self-tests pass, including the base-only cases (D3 superseded, candidate gates N/A, a missing candidate metric excused only under base-only, and nothing excused when D3a fails or its decision is missing). Synthetic runs: base-only (69 gates N/A, D3 superseded, D3a and D3r pass, the swap sets work from the base pair, every other outcome as in the clean run); a fake rejection (the candidate passes its own rule but is dropped: D3a fails on outcome and held-out consistency, nothing is excused, 90 gates fail); a late rule (D3r fails, nothing else changes).

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

## Frozen files and their sha256 at the freeze commit (stage 1d)

Computed from the commit's own blobs (`git show <commit>:<path>`); line endings as stored. VERIFIER_FREEZE.md is the one file left out. Earlier stages' tables are in this file's git history.

| file | sha256 |
|---|---|
| `bench/env/requirements-lingua.txt` | `a8296bfa0aae4a0e1386e258f27cd429333ff2c5647e18d1f528a44f57aafea1` |
| `bench/personality/CHEAPEST_PASS.md` | `4fa87e00bede8aa567983a51a6510f52518ae832588afc23775f7dd193a12c6b` |
| `bench/personality/GATES.md` | `42492551a4e6fa603bd30f6f5aa4480da14e0e187786e23525355f8b437cdcdf` |
| `bench/personality/GATES_SPEC.md` | `7d5b2e54aba1b5dbc82ed556bc864ee23a92952d16ee0e298583c8ec6d622c2b` |
| `bench/personality/answer_agy.py` | `8f6042e7a2459e498222816c3535e828390db0e968f8597cdb9f3448dca4217a` |
| `bench/personality/answer_dsh.py` | `86dca4ebbac14705631d37d981352b77b472ac8ff011e3ab27cc5a2709393d06` |
| `bench/personality/answer_raw.py` | `dd3c3952b4701cb55e0da9ee56d0f9948d587761062a2e8415f70f4d3daed571` |
| `bench/personality/answer_stats.py` | `6387d34d15356c0e6cb8ec8e9ed2acdf3521a5208ed46ccb53a9e8b70b2b1387` |
| `bench/personality/bt.py` | `910f03a876a1e93b9ac05bef2d062ee83a73eb9bb65c6a52106de2e83d765862` |
| `bench/personality/calibrate.py` | `d47690a40158955cd88ad54e2c26c246be0521be47bb0f9dcb91fcaa726b5fd8` |
| `bench/personality/dsh/llm-batch.mjs` | `14375526a9d59e56fb1b6793f15ec66d758414afe0ded0cf904aa109c86e2259` |
| `bench/personality/dshbatch.py` | `e61ebf9cff76937a5de7299c7a8af9b3c4a4be1d0fe726b8c9b0606fe06e73f0` |
| `bench/personality/filter_questions.py` | `0795e248691ac229e9fff7f3890da4e9ddfb07a2619629ddb83d6fdbe18647f6` |
| `bench/personality/gen_questions.py` | `2b7d1c61ed5d364c1c06721331a4b9b62de9af466c978c47e4789ae6bfcadf5d` |
| `bench/personality/judge.py` | `14c8322037a125543c65619b2541aecacf16eb9fa56b100a03609e1fdbc4ace2` |
| `bench/personality/judge_agy.py` | `05675825e04b564614fe331f63a25bb1de65aa3b37887f7f0ac546a0780be716` |
| `bench/personality/ledger.py` | `db610d69765b063cbde03644503f7b6714cc4e7410e3fec77f760b79d3acd3e3` |
| `bench/personality/measure_all.py` | `58b9498a1272b5b513d00af1eb511bbcc777968c4dd5fac50c540c02e8566487` |
| `bench/personality/metrics.py` | `7a791cfdb8b1e127ff29946d3f2e0ec1051c604b61f388bdc8a333297971dcfc` |
| `bench/personality/plan_cost.py` | `b9428be79a010d5d8a7538a8069efcdc83643856063321ddc0a9aec57c85fb91` |
| `bench/personality/samples.py` | `761fa984443dfcfd41adb7edb7bdf9b44161dbbda71c151fb5a5d81b00c22ca7` |
| `bench/personality/seeds.json` | `e3f780648541d42fcf8e81b3c20131344bbc49c724dfc9f0ce2da1f1e9afdc92` |
| `bench/personality/spend.py` | `ae553569b7f2ed15941a7c29901777690190b07041ca55295dd7359e6353b5dc` |
| `bench/personality/traits.json` | `8c474cfc7794969b390b07de56be02cb73773dae0daa4770d31c648a6a28c039` |
| `bench/personality/verify.py` | `ef8225ca63c7e248900c7e9a2f9ba880bd3e0a5d492cb99043c0f1e85556c967` |
| `docs/dsh-ab/WIN_CRITERIA.md` | `4121b286662755f55ee73f5d15c1d4025e73640417a0a6f1fbfd44c654a3939e` |
| `docs/dsh-ab/round-three/verdict.py` | `8e85a5655ab957662d1b311e0ee94e105f606d15ee9baddd1ccaa9bbbcac1595` |

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
2. Write `bench/freeze/FREEZE_DATA.json` (outside the frozen folder) with: `set`; `files` = sha256 of the question files, `report.json`, the rating batch, every `samples/*` file, `labels/native_controls.jsonl`, the controls batch, `overlays/lean.yml`, `rules/base/*.md`; `external_files` = sha256 of `W:\AgentData\dsh_home\profiles\gv-plain\` and `gv-grav\` `cordis.patch.yml`, `cordis.yml`, `package.json`, `pnpm-workspace.yaml` and `pnpm-lock.yaml` where present, and of lingua's `RECORD` in the venv; `ledger_prefix` = the line count of `ledger.jsonl` and the sha256 of those lines (the ledger's first N lines joined by newlines, as `measure_all.measure_data_freeze` reads them); `agy_config` = a tree hash of each home's `.gemini/config`; `grav_link_head`; `rules_base`; `pre_existing_judging` = the pilot judging folders (exempt from D3's tuning check); `judging_at_stage2` = every judging folder that exists then (S0 scans them all for held-out questions); `deepseek_balance_before_usd`; `deepseek_records_usd_at_stage2` (the verifier's own spend measure at that moment).
3. Commit that file alone. Its commit time is the stage-2 time that S0 and D6 use.

## What the builder must do before and during the first real run

Before any held-out run, in this order (if the candidate is not confirmed, skip everything about it: no CONFIRM file, no candidate held-out runs, no ho-*-cand, hoc-*-cand or chal-*-cand sets; build swap-ds and swap-gm with the base pair only, `--pairs ds-plain~ds-grav --swap` and `--pairs gm-plain~gm-grav --swap`; export n3marks and n4 without `--name`):

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
