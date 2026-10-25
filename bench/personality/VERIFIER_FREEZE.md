# Verifier freeze

Owner: the verifier owner (builds nothing in this benchmark). Gates: `GATES.md`. This file records the freeze and says how it is checked. `verify.py` reads the stage-1 commit from the line below; D4 fails as "metric missing" until it is filled in.

Stage-1 freeze commit: `ec91a8d5e5e3b831693ea470302f09d888fe5671`

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

## Frozen files and their sha256 at the freeze commit

Computed from the commit's own blobs (`git show <commit>:<path>`); line endings as stored. VERIFIER_FREEZE.md is the one file left out.

| file | sha256 |
|---|---|
| `bench/personality/CHEAPEST_PASS.md` | `4fa87e00bede8aa567983a51a6510f52518ae832588afc23775f7dd193a12c6b` |
| `bench/personality/GATES.md` | `177b3209a4d602a7ce6e4fe561027a1bc0106826dc8014288e15459cce11e0db` |
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
| `bench/personality/measure_all.py` | `b8378bdf87e3e646a3e20d2330496f3329acf332ca63d939717c6c4625c28f8e` |
| `bench/personality/metrics.py` | `7a791cfdb8b1e127ff29946d3f2e0ec1051c604b61f388bdc8a333297971dcfc` |
| `bench/personality/plan_cost.py` | `b9428be79a010d5d8a7538a8069efcdc83643856063321ddc0a9aec57c85fb91` |
| `bench/personality/samples.py` | `4177c6ac6933efea01a35d600cea61a4a2f5873cc9a5fdb1bb6ad13e7290b809` |
| `bench/personality/seeds.json` | `e3f780648541d42fcf8e81b3c20131344bbc49c724dfc9f0ce2da1f1e9afdc92` |
| `bench/personality/spend.py` | `ae553569b7f2ed15941a7c29901777690190b07041ca55295dd7359e6353b5dc` |
| `bench/personality/traits.json` | `a1b5b39259555f0d1536236581a0377890ab9dec07849931105e47531e90ba48` |
| `bench/personality/verify.py` | `09d0018914bfbd3537e654cad3fa63b426f3e38c43b70b77c5e83324d90b7139` |
| `docs/dsh-ab/WIN_CRITERIA.md` | `4121b286662755f55ee73f5d15c1d4025e73640417a0a6f1fbfd44c654a3939e` |
| `docs/dsh-ab/round-three/verdict.py` | `8e85a5655ab957662d1b311e0ee94e105f606d15ee9baddd1ccaa9bbbcac1595` |

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
