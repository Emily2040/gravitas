# Round five: port of round four's run and grading suite

This folder (`W:\AgentData\logs\gravitas-dsh-ab5`) now holds round four's run and grading suite, ported to round five by mechanical text replacement with the smallest possible diff.

- The source is `W:\AgentData\logs\gravitas-dsh-ab4`. Nothing there was changed.
- Every gate, bound and self-test is the same as round four's. The only differences are the replacements listed below and the hand edits that round five's design requires: the run.sh lock and tuning passes, `validity5.py --tuning N`, the freeze.sh lock record, and the judge_codex.sh worker fix.

What was **not** done:

- Nothing was run against DeepSeek, Codex or any other model.
- `W:\AgentData\dsh_home` was not read or touched. All tests point run.sh at a test lock, and freeze.sh's `--state` was never run.
- Nothing was committed and no branch was switched.
- Round five's held-out prompts, sources, keys and key points were not opened. The case names come from the task.

Produced on 2026-10-26.

## 1. Files

### Ported scripts

| Round five file | Source in round four |
|---|---|
| `run.sh` | `run.sh` (mechanical, plus hand edits: lock, tuning passes) |
| `runall.sh` | `runall.sh` |
| `freeze.sh` | `freeze.sh` (mechanical, plus hand edits: lock record, round-five schedules) |
| `validity5.py` | `validity4.py` (mechanical, plus hand edit: `--tuning N`) |
| `make_pairs5.py` | `make_pairs4.py` |
| `save_grades5.py` | `save_grades4.py` |
| `save_labels5.py` | `save_labels4.py` |
| `build_notes5.py` | `build_notes4.py` |
| `judge_codex.sh` | `judge_codex.sh` (mechanical, plus hand edit: the worker fix) |
| `verdict5.py` | `verdict4.py` |
| `verdict5-amended.py` | `verdict4-amended.py` |
| `mutation5.py` | `mutation4.py` |
| `workflows/grade5.js` | `workflows/grade4.js` |
| `workflows/label5.js` | `workflows/label4.js` |
| `grader-prompt5.md` | `grader-prompt4.md`, byte-identical (`cmp` passes) |

### Generated round files

| File | Made from |
|---|---|
| `rules/change5/{en,zh-CN,ja,ko}.md` | `W:\Projects\gravitas-round5\dist\<lang>\gravitas\rules\AGENTS.md`, with the change-5 text inserted (section 3) |
| `overlays/base-{zh,en,ja,ko}.yml` | round four's `overlays/base-*.yml`, comment "Round four" changed to "Round five" |
| `overlays/c5-{zh,en,ja,ko}.yml` | round four's `overlays/c4-*.yml`: the comment names change 5, and `ruleFile` points at `W:/AgentData/logs/gravitas-dsh-ab5/rules/change5/<lang>.md` |
| `expected-rule-hashes.json` | computed as `validity4.py`'s `expected_rules` checks it (section 3) |
| `tuning-schedule-1.txt`, `tuning-schedule-2.txt` | new: 12 lines each, `gv-grav-c5 <case> N`, for round four's 12 prompts |
| `schedule.txt`, `schedule.seed.txt` | new: 72 held-out runs, and the seed (`20261026`) alone |

### Tests and tools

| File | What it is |
|---|---|
| `tests/judge_codex_test.sh` | new: stand-in test of the judge_codex.sh guard and worker fix (section 5) |
| `tests/run_lock_test.sh` | new: test of run.sh's lock check, freeze.sh's lock record, the tuning-pass checks, the rerun cap and what freeze.sh hashes for tuning (the last two added by the review fixes, section 10) |
| `tests/validity_tuning_test.py` | new: test of `validity5.py --tuning N` |
| `dev/port5.py` | the mechanical port: the replacement rules, applied in order |
| `dev/check_port5.py` | classifies every changed line; writes `port-diff.txt` and `dev/port5-classify.json` |
| `dev/make_rules5.py` | writes the rule files, overlays and hashes; `--check` re-verifies them |
| `dev/make_schedule5.py` | writes the four schedule files; `--check` re-verifies them |
| `dev/port5-counts.json` | replacement counts per rule and file |
| `dev/selftest-logs/` | the full output of every self-test and test run |
| `mutation/mutation-report.txt`, `mutation/mutation-run.log` | mutation test output (section 8) |
| `port-diff.txt` | full unified diffs: ab4 file against ab5 file, then the generated files against their sources |

## 2. The replacement list (exact)

`dev/port5.py` applies these rules in this order to the UTF-8 text of each ab4 file. `grader-prompt4.md` is copied byte for byte. Every changed line in the ported files is either produced by these rules, or is one of the hand edits in section 4. `dev/check_port5.py` checks this line by line.

| Id | Replacement | Files |
|---|---|---|
| P1 | `gravitas-dsh-ab4` → `gravitas-dsh-ab5` (the round folder) | all |
| P2 | `gravitas-claim-check` → `gravitas-round5` (the worktree), and run.sh's refusal label "not the claim-check worktree" → "not the gravitas-round5 worktree" | all |
| P3 | `docs/dsh-ab/round-four` → `docs/dsh-ab/round-five` (where validity checks the committed copies) | all |
| N1 | Script and file names of the suite, `<name>4` → `<name>5`. The names are validity, make_pairs, save_grades, save_labels, build_notes, verdict (including verdict4-amended, verdict4.json, verdict4_sha256, verdict4_frozen_, verdict4-selftest-), preverdict, mutation, grade (grade4.js), label (label4.js) and grader-prompt. Regex: `\b(validity\|make_pairs\|save_grades\|save_labels\|build_notes\|verdict\|preverdict\|mutation\|grade\|label\|grader-prompt)4(?![0-9])` | all |
| L1 | `round-four`, `Round-four`, `round four`, `Round four` → five (whole words) | all |
| C1 | `change4`, `change 4`, `Change 4` → 5 | all |
| C2 | The arm, set and c4 identifiers and labels → c5. This covers `gv-grav-c4`, `aa-c4`, `C4`, `c4`, `c4_*`, `*_c4`, `c4Sentence`, `c4-<lang>.yml`. Regex: `(?<![A-Za-z0-9])([cC])4(?![0-9a-z])`. Three strings are protected (see below) | all |
| R1 | The run-folder label `r4-` → `r5-`. It appears in run.sh's cwd `r4-$stem`, validity's cwd check, make_pairs' leak pattern `\br4-`, and the mutants that quote these | all |
| K1 | EXPECTED_CASES, and the self-test scenarios that name its cases, → round five's cases, matched by position (next table) | verdict4.py, verdict4-amended.py |
| K2 | The comment above EXPECTED_CASES: "(prompts/ as listed on 2026-10-23, before any run)" → "(prompts/ as fixed on 2026-10-25, before any run)" | verdict4.py |
| T1 | The tuning prompt folder: `R3P=/w/AgentData/logs/gravitas-dsh-ab3/prompts` → `R4P=/w/AgentData/logs/gravitas-dsh-ab4/prompts`, `$R3P` → `$R4P`, and "round three's prompts" → "round four's prompts". It runs last, so that P1 and L1 cannot rewrite its output | run.sh |
| S1 | Frozen sha256 of verdict4.py (`11cdd365…792ca`, full and abbreviated) → verdict5.py's own sha256, `53ec336e2777202eeaee8a9c6b9e883ca22792fbf5a6afcf9d1654a00cd1419d`. Computed from verdict5.py as written, which no later edit touched. verdict5-amended.py (`FROZEN_SHA256`, docstring) and mutation5.py (`FROZEN_SHA256`) check it | verdict4-amended.py, mutation4.py |

### Case mapping for K1

Each round-four case maps to the round-five case in the same language and the same place in sorted order. The frozen self-tests therefore build exactly the same synthetic data, because they index cases by position.

| Round four | Round five |
|---|---|
| en-529-roth | en-debit-card-theft-liability |
| en-fsa-rollover | en-gift-tax-down-payment |
| en-medicare-part-b | en-uk-child-benefit-charge |
| ja-medical-deduction | ja-child-allowance-income-cap |
| ja-part-time-leave | ja-inheritance-registration |
| ja-wallpaper-restoration | ja-license-lapse |
| ko-jeonse-protection | ko-card-installment-defense |
| ko-severance-pay | ko-dependent-pension |
| ko-unemployment-quit | ko-duty-free-limit |
| zh-flex-hours | zh-contract-expiry-compensation |
| zh-insurance-gap | zh-lease-sale |
| zh-sick-pay | zh-passport-remote-apply |

### Protected from C2

These contain "c4" but are not c4 identifiers:

- In verdict4-amended.py's synthetic event streams, `"callId": "c4"` (twice) is the fourth tool call, numbered c1 to c5. Renaming it would collide with the existing callId `"c5"`.
- In verdict4-amended.py's self-test, the scenario label `"(c4) one codex grade…"` is item 4 of section (c).

### Kept on purpose

These are not in the list, and leaving them changes no behaviour:

- **Module and list names:** the module alias `V4` in verdict5-amended.py and the list name `V4_MUTANTS` in mutation5.py.
- **Temporary-folder prefixes:** `v4test-`, `make-pairs4-selftest-` and `mut4-` (`verdict4-selftest-` changed with N1 because it is the script name), and the synthetic file name `wf4.json` in save_grades5.py's self-test.
- **Seeds:** `random.Random(20261023 + 4)` (pid shuffle, make_pairs5.py) and `random.Random(20261024 + 444)` (note shuffle, build_notes5.py). See open items.
- **Run folder:** the cwd base folder `/w/AgentData/logs/gravitas-dsh-ab3/cwd/`. Only the prefix changes (r4- → r5-), and validity5.py's own-folder pattern still expects ab3/cwd.
- **Synthetic case names:** validity5.py's self-test uses names such as zh-sick-pay and en-529-roth. They are not tied to any case list.
- **Historical remarks:** "round three's longest run took 398" (run.sh), and the round-three hedge-list and FAB-list references in the verdict scripts.
- **Codex flag order:** judge_codex.sh's remark that the flag order is unverified until the first real call. Round four's real calls went through `dev/codex_drive.sh` with the same command line.
- **The phrase "all four languages"** (it means languages, not the round).
- **validity5.py's self-test flag:** it is still `--self-test`, with a hyphen, as round four's.

## 3. Rule files, overlays and expected hashes

### Rule files

`rules/change5/<lang>.md` is the worktree's `dist/<lang>/gravitas/rules/AGENTS.md` with only the change-5 text inserted. `dev/make_rules5.py` takes the text verbatim from `design/change5.md` (section "## Text") and places it where change5.md's "Where" section says: rule item 4, line 13, between the "thinly known" sentence and the "evidence counts" sentence.

| Language | Inserted between | Separator |
|---|---|---|
| en | "…widened to what they can confirm." and "Evidence counts…" | one space, as round four's change-4 files |
| zh-CN | "…确认的程度。" and "证据只有…" | none |
| ja | "…幅を広げます。" and "根拠として…" | none |
| ko | "…넓혀 말합니다." and "근거로…" | one space, as round four's change-4 files |

The script checks four things:

- the insertion point occurs exactly once;
- removing the inserted text gives back the original bytes;
- only line 13 (item 4) changes;
- the inserted text equals change5.md's paragraph.

The diffs against the dist files are in `port-diff.txt`, part 2.

### Overlays

The overlays copy round four's format. `c5-*.yml` uses language = the request's language, `alwaysOnRule: true`, `claimCheck: false`, and `ruleFile: W:/AgentData/logs/gravitas-dsh-ab5/rules/change5/<lang>.md`, with forward slashes.

### Expected hashes

`expected-rule-hashes.json` is computed with validity5.py's own `rule_text()`: the rule plus `W:\Projects\gravitas-round5\dsh\platform\<lang>.rule.md`, joined as `dsh/index.js` does. `c5Sentence` is the first 40 characters of the inserted text.

The base hashes equal round four's base hashes, because the dist rules and platform notes are unchanged.

| Language | base | c5 | c5Sentence |
|---|---|---|---|
| zh | 47f1b94e… | c6027725… | “直接说”不等于说得比查到的更绝对。数字、日期、期限或规定，只要为这次回复打开的 |
| en | 61e4f1bf… | 5a68fe84… | Plainly never means more absolute than w |
| ja | 8206ddda… | f7580248… | 言い切るとは、見つけた以上に断定することではありません。数値、日付、期限、規則に |
| ko | 8f4e720b… | 344277c2… | 얼버무리지 않고 말한다는 것이 찾아낸 것보다 더 단정한다는 뜻은 아닙니다 |

The 40-character sentence survives both revisions allowed after pass 1:

- R-b deletes the parenthetical, which starts after character 40 in every language.
- R-a moves the whole text unchanged.

After a revision, rerun `dev/make_rules5.py` on the revised text, or recompute the c5 hashes, as round four's `dev/revise_c4.py` did.

## 4. Diff summary per script

The counts come from `dev/check_port5.py` (`dev/port5-classify.json`).

- **Mechanical:** a changed line whose ab4 text, put through the rules above on its own, gives exactly the ab5 text.
- **Hand:** every other added, removed or changed line. All of them are listed under the table.

| File | Lines removed | Lines added | Mechanical (rules) | Hand-edit lines |
|---|---|---|---|---|
| run.sh | 12 | 35 | 11 | 25 (13 in the port, 12 from the review fixes, section 10) |
| runall.sh | 1 | 1 | 1 | 0 |
| freeze.sh | 6 | 18 | 5 | 14 (5 in the port, 9 from the review fixes, section 10) |
| validity5.py | 66 | 72 | 58 | 17 |
| make_pairs5.py | 17 | 17 | 17 | 0 |
| save_grades5.py | 22 | 22 | 22 | 0 |
| save_labels5.py | 4 | 4 | 4 | 0 |
| build_notes5.py | 2 | 2 | 2 | 0 |
| judge_codex.sh | 19 | 33 | 15 | 19 |
| verdict5.py | 85 | 85 | 85 | 0 |
| verdict5-amended.py | 188 | 188 | 188 | 0 |
| mutation5.py | 32 | 32 | 32 | 0 |
| workflows/grade5.js | 5 | 5 | 5 | 0 |
| workflows/label5.js | 2 | 2 | 2 | 0 |
| grader-prompt5.md | 0 | 0 | 0 | 0 (byte-identical) |

Every changed line of the ten files without hand edits is explained by the replacement list. The replacement count per rule and file (`dev/port5-counts.json`):

| File | P1 | P2 | P3 | N1 | L1 | C1 | C2 | R1 | K1 | K2 | T1 | S1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| run.sh | 1 | 2 |  | 3 |  | 1 | 3 | 1 |  |  | 4 |  |
| runall.sh | 1 |  |  |  |  |  |  |  |  |  |  |  |
| freeze.sh | 1 | 1 |  | 11 |  | 1 |  |  |  |  |  |  |
| validity5.py | 8 | 1 | 2 | 5 | 1 | 5 | 51 | 7 |  |  |  |  |
| make_pairs5.py | 1 |  |  | 5 | 1 |  | 13 | 3 |  |  |  |  |
| save_grades5.py |  |  |  | 22 |  |  | 2 |  |  |  |  |  |
| save_labels5.py |  |  |  | 4 |  |  |  |  |  |  |  |  |
| build_notes5.py |  |  |  | 1 |  |  | 1 |  |  |  |  |  |
| judge_codex.sh | 2 |  |  | 16 |  |  |  |  |  |  |  |  |
| verdict5.py |  | 1 |  | 9 | 4 |  | 81 |  | 24 | 1 |  |  |
| verdict5-amended.py |  |  |  | 47 | 2 |  | 152 |  | 22 |  |  | 2 |
| mutation5.py |  |  |  | 26 | 2 |  | 12 | 2 |  |  |  | 1 |
| workflows/grade5.js | 1 |  |  | 4 | 1 |  |  |  |  |  |  |  |
| workflows/label5.js |  |  |  | 1 | 1 |  |  |  |  |  |  |  |

### The hand edits

All are required by round five's design or by the task.

**run.sh: 13 lines**

- **Header (6 lines added).** Tuning runs gv-grav-c5 only, in two passes, with rerun lists per pass. The lock rule. `RUN_LOCK_TEST` is for tests only, MUST be unset in real runs, and freeze.sh records whether it is set.
- **Lock check (3 lines added), the first check of all, before the freeze comparison:**

      LOCK=${RUN_LOCK_TEST:-/w/AgentData/dsh_home/profiles/gv-grav.LOCK}
      [ -f "$LOCK" ] || refuse "no lock file $LOCK"
      [ "$(head -n 1 "$LOCK" | sed 's/\r$//')" = "owner: dsh-round5" ] || refuse "lock $LOCK: first line is not 'owner: dsh-round5'"

  The lock is only read; nothing creates or deletes it. A CR before the newline counts as part of the line end, so a lock written with CRLF passes. Any other difference, such as a trailing space, is refused.
- **Tuning branch (2 lines added, 1 changed).** It refuses any arm but gv-grav-c5, because the design runs no new plain or base runs, and any round but 1 or 2. Reruns come from `rerun-schedule-tuning-$r.txt` (one list per pass) instead of `rerun-schedule-tuning.txt`. Held-out runs are unchanged: they read `prompts/` and write `raw/`. Tuning runs read `W:\AgentData\logs\gravitas-dsh-ab4\prompts` (T1) and write `tuning/`, and are refused once `raw/*.ndjson` exists, as in round four.

**freeze.sh: 5 lines**

- One line added in `state()`, after a comment line: `echo "lock-override: $([ -n "${RUN_LOCK_TEST+x}" ] && echo set || echo unset)"`. A variable that is set but empty also prints "set".
  - freeze-start is recorded with the variable unset ("unset"). A run with it set then prints "set", and run.sh's freeze comparison refuses the run.
- The hashed round files: `tuning-schedule.txt` is replaced by `schedule.seed.txt tuning-schedule-1.txt tuning-schedule-2.txt`. The line was split in two, so `expected-rule-hashes.json` moved to the next line.

**validity5.py: 17 lines**

- `--tuning N` checks pass N: `tuning-schedule-N.txt`, `tuning/`, then `validity-tuning-N.json`.
- With `--archive-invalid` it writes `rerun-schedule-tuning-N.txt` and `reruns-tuning-N.json`.
- `main(tuning=None|"1"|"2")`.
- The command line refuses `--tuning` without 1 or 2.
- Docstring lines updated to match.

No check, gate or self-test changed.

**judge_codex.sh: 19 lines.** The worker fix, in section 5.

## 5. The judge_codex.sh fix and its test

### The defect

The main loop started each worker as `judge_codex.sh --one <pid>`. The worker resets `MODE=""` while it parses its arguments, so in a real `--approved` run every worker's guard refused. Stand-in tests never noticed, because `CODEX_STANDIN` is inherited through the environment. Round four worked around it with `dev/codex_drive.sh`.

### The fix

- The main loop now passes `--approved` to each worker when it runs approved:

      WFLAG=""
      if [ "$MODE" = approved ]; then WFLAG="--approved"; fi   # each worker keeps the parent's mode for its own guard
      ... | xargs -P "$JOBS" -I{} bash "$SELF" $WFLAG --one {}

- The refusal when neither `--approved` nor `CODEX_STANDIN` is set is unchanged.
- `--approved` together with `CODEX_STANDIN` is still refused.

### A new test-only variable

`CODEX_APPROVED_STANDIN=<dir>` exists so that the approved path can be tested without any risk of a real call.

- With `--approved`, every guard (in the parent and in each worker) aborts with exit 4 unless `command -v codex` is `<dir>/codex`. Without `--approved` it enables nothing: the run is refused as before.
- It is exported to the workers.
- A run that uses it logs "REAL, approved (approved-path test, stand-in …)".
- The header says it MUST be unset in real runs.
- The `--help` range now covers the longer header (lines 2-30).

### The test: `tests/judge_codex_test.sh` (21 assertions, all pass)

The stand-in `codex` is always first on PATH. It answers `--version` with `codex-cli 0.163.0`, logs its arguments, and writes a valid grade to its `-o` path.

| Part | What it checks |
|---|---|
| A | A `--approved` run of the fixed script, with `CODEX_APPROVED_STANDIN`, grades both pairs: exit 0, two stand-in calls, two valid ledger grades, both workers logged "end exit=0 … valid", no REFUSED. The call carries the frozen model, effort, sandbox and flags. |
| B | A copy of the fixed script with only the worker start line put back to round four's (`bash "$SELF" --one {}`) fails: non-zero exit, no stand-in call, and both workers refuse in their own guard. |
| C | No refused run calls any codex or writes a grade: neither flag (exit 3); `CODEX_APPROVED_STANDIN` without `--approved` (exit 3); `--approved` with `CODEX_STANDIN` (exit 3); an approved-path test whose codex resolves to another stand-in (exit 4); a worker started by hand (refused). |
| D | `CODEX_STANDIN` mode still grades both pairs, and a second run skips the pairs already graded. |

Run against the old worker start (`bash tests/judge_codex_test.sh <copy with the old line>`), the test fails 7 of 21 assertions. All six A assertions about the codex call fail, because no worker reaches it, plus B's own check that the copy differs from the fix. Log: `dev/selftest-logs/judge_codex_test-on-old-worker-start.txt`.

## 6. Run side

- **`tuning-schedule-1.txt` and `tuning-schedule-2.txt`:** `gv-grav-c5 <case> 1` (or `2`) for round four's 12 prompts, in sorted order.
- **`schedule.txt`:** 72 lines, 12 cases × 3 arms × 2 rounds, in 24 triplets. Each triplet is one case and round with the three arms adjacent, as in round four.
  - The triplet order is a seeded shuffle, `random.Random(20261026)`.
  - The arm order is a seeded starting order, rotated by one per triplet, so each arm runs first, second and third in 8 triplets each.
  - `dev/make_schedule5.py` asserts all of this, and that each (arm, case, round) appears exactly once.
  - `schedule.seed.txt` holds `20261026` alone.
  - Round four's schedule was a plain shuffle of arm orders. "Rotated" is read here as balanced rotation.
- **`run.sh`:**
  - tuning runs read `W:\AgentData\logs\gravitas-dsh-ab4\prompts`, write `tuning/`, and are refused once `raw/*.ndjson` exists;
  - held-out runs read `prompts/` and write `raw/`;
  - the lock check is described in section 4;
  - the rerun cap (one rerun per invalid run, stop and ask past 8 in the round, and past 2 in a tuning pass) is described in section 10.
- **`tests/run_lock_test.sh` (60 assertions, all pass; 31 before the review fixes).** It sets `RUN_LOCK_TEST` on every call and never creates a freeze-start in this folder. The rerun-cap and freeze-hash cases added by the review fixes are listed in section 10.
  - **Real run.sh:**
    - Refused: a missing lock, an empty lock, a lock owned by another session, a trailing space, a longer owner, the owner on the second line only, and a folder named like the lock.
    - Passes to the next check ("no freeze-start.txt"): the right lock, with or without a final newline, and with CRLF line ends.
    - These runs leave nothing in the folder.
  - **freeze.sh's lock-override line:** prints unset, set, and set when empty.
  - **A copy of run.sh in a temporary round folder, with a stub freeze.sh:**
    - a freeze-start recorded without the variable refuses a run with it set;
    - tuning refuses plain, base, round 3, another prompt folder, round three's prompts, and an existing raw/ run;
    - pass 2 reads only `rerun-schedule-tuning-2.txt`;
    - no case starts a run.
- **`tests/validity_tuning_test.py` (14 assertions, all pass):**
  - pass N reads `tuning-schedule-N.txt` and writes `validity-tuning-N.json`;
  - archiving moves invalid runs to `tuning/attempt1/` and writes the pass's own rerun files;
  - the two passes keep separate files;
  - a rerun pass-2 run is allowed two ledger attempts;
  - the command line refuses `--tuning`, `--tuning 3` and `--tuning --archive-invalid`.

## 7. Self-tests

Every count equals round four's.

| Script | Command | Result |
|---|---|---|
| validity5.py | `python validity5.py --self-test` | 71 checks, 0 failed (round four: 71) |
| make_pairs5.py | `--selftest` | 8 assertions, 0 failed (8) |
| save_grades5.py | `--selftest` | 35 assertions, 0 failed (35) |
| save_labels5.py | `--selftest` | 11 assertions, 0 failed (11) |
| verdict5.py | `--selftest` | 249 assertions, 0 failed (249) |
| verdict5-amended.py | `--selftest` | 1113 assertions, 0 failed (1113), about 8 minutes |
| judge_codex.sh | `bash tests/judge_codex_test.sh` | 21 assertions, 0 failed (new) |
| run.sh and freeze.sh | `bash tests/run_lock_test.sh` | 60 assertions, 0 failed (new; 31 before the review fixes in section 10) |
| validity5.py --tuning | `python tests/validity_tuning_test.py` | 14 assertions, 0 failed (new) |

Full output is in `dev/selftest-logs/`. `dev/make_rules5.py --check` and `dev/make_schedule5.py --check` both report no difference.

## 8. Mutation test

`mutation5.py --jobs 8` was started in the background on 2026-10-26. It writes `mutation/mutation-report.txt`, and its progress log is `mutation/mutation-run.log`. Temporary files go to `.tmp-mutation/` in this folder. The originals' sha256 before the run is in `mutation/originals-before.sha256`.

The first run (started 00:24) was cut off at 45 of 121 when the session hit its usage limit (mutation/mutation-run.interrupted.log). It was restarted at 07:21 with temporary files in .tmp-mutation and finished at 08:27 (65 min): verdict5.py 24 of 27 killed (survivors V09, V12, V16), verdict5-amended.py 65 of 67 (A04, A32), save_grades5.py 10 of 10, save_labels5.py 7 of 7, make_pairs5.py 5 of 5; every survivor explained, every baseline passes, all originals unchanged after the run (mutation/mutation-report.txt). The same survivors as round four.

After the mutation run, make_pairs5.py's shuffle seed was changed from 20261023 + 4 to 20261026 + 5 (one constant, nothing else), so round five's pid layout differs from round four's blind-map.json, which is readable on disk. make_pairs5.py --selftest still passes (8 assertions). The mutation report's sha256 for make_pairs5.py is the file before this one-constant change.

## 9. Open items, before tuning starts

- **Commit the round's rule copies.** `rules/change5/*.md` and `expected-rule-hashes.json` must be committed under `docs/dsh-ab/round-five/` in `W:\Projects\gravitas-round5` (branch dsh-round5) before freeze-start. Until then, validity5.py's whole-round check fails ("not committed at freeze-start's head"). The design's tuning decision rule, grader prompt, limited-key-point list and `tuning_check5.py` go with them; those are not part of this port.
- **Record freeze-start.** Do it with `sh freeze.sh start`, with `RUN_LOCK_TEST` unset, while gv-grav's plugin link points at `W:\Projects\gravitas-round5`. run.sh refuses unless freeze-start's link line names that worktree, and unless `W:\AgentData\dsh_home\profiles\gv-grav.LOCK` starts with `owner: dsh-round5`. Both are the other session's to set; neither was touched here.
- **If a revision follows pass 1** (R-a or R-b), recompute the change5 files and c5 hashes, commit them, and record a new freeze-start, as round four did (`freeze-start.superseded-1.txt`).
- **Seeds are unchanged:** make_pairs (`20261023 + 4`) and build_notes (`20261024 + 444`). Round five's blind-map shuffle therefore puts the same set, case position and round behind each pid as round four's did. No judge ever sees a map, so the blinding holds. Bumping the seeds is a one-line change per script, outside the replacement list; it is Emily's call.
- **The READMEs are not ported.** `verdict5-amended.py`'s docstring refers to `verdict5-amended-README.md`, and freeze.sh hashes `verdict5-*.md` when present. Round four's READMEs describe round four's data and numbers, so a round-five README needs writing rather than a mechanical port.
- **`judge_codex.sh` still has to be tried with `--approved --limit 1`** before a full grading run, now without `dev/codex_drive.sh`. The fixed worker path is only tested with a stand-in.
- **Record freeze-start after the calibration has passed** (added with the review fixes). freeze.sh now hashes `tuning-instrument/tuning-grader-prompt5.md`, `lkp.json` and the rest of the instrument. A rubric fix during calibration changes the grader prompt, and run.sh then refuses every run until a new freeze-start is recorded. Recording it once calibration has passed avoids a superseded freeze-start.
- **Not done: the optional check in `tuning_check5.py`** (the review's suggestion that `--pass 2` compare its instrument files with the commit at freeze-start's head). The instrument is not committed yet (`docs/dsh-ab/round-five/` does not exist in the worktree), and `tuning_check5.py` belongs to the design rather than to this port. Section 10 lists the gap that remains without it.

## 10. Review fixes (2026-10-26)

A review of this port found two major gaps. Both are fixed in run.sh and freeze.sh, which the mutation run does not read. Neither fix loosens any gate or bound. Both only add refusals or hashed files.

No other files changed: verdict5.py, verdict5-amended.py, save_grades5.py, save_labels5.py, make_pairs5.py, grader-prompt5.md, mutation5.py, validity5.py and the tuning instrument are untouched. The mutation run therefore stays valid.

### 10.1 run.sh: the rerun cap is now enforced

**Finding.** Nothing enforced Emily's approval ("one rerun per invalid run, stop and ask past 8"), or the decision rule's "more than 2 invalid runs in a pass means stop and ask Emily". `validity5.py --archive-invalid` writes a rerun schedule for any number of invalid runs, and run.sh accepted every rerun on it. A quota or network outage (say 20 held-out runs failing on HTTP 429) would have spent 20 more DeepSeek runs without asking.

**Fix.** A check placed just before the existing "run exists" checks, which applies only when the run has an archived attempt (`<outdir>/attempt1/<stem>.ndjson` exists):

    # the rerun cap: every archived attempt is one rerun spent or due, counted over tuning and held-out together
    if [ -e $od/attempt1/$stem.ndjson ]; then
      n=$(ls $B/raw/attempt1/*.ndjson $B/tuning/attempt1/*.ndjson 2>/dev/null | wc -l)
      [ "$n" -le 8 ] || refuse "$n runs archived for a rerun, past the 8 reruns approved: stop and ask Emily"
      if [ "$od" = "$B/tuning" ]; then
        n=$(ls $B/tuning/attempt1/*.r$r.ndjson 2>/dev/null | wc -l)
        [ "$n" -le 2 ] || refuse "$n runs of tuning pass $r archived as invalid, more than 2 in a pass: stop and ask Emily"
      fi
    fi

Three header lines describe it, so the change is 12 added lines in all. How the cap behaves:

- **What counts.** Every file in `attempt1/` is one rerun, spent or due. Tuning and held-out are counted together, because the approval covers the round's 96 runs plus at most 8 reruns.
- **Whole batches.** Once more than 8 runs are archived, every rerun is refused, including the first eight of an oversized batch. Likewise, once more than 2 runs of a tuning pass are archived, every rerun in that pass is refused. Which reruns to spend is then Emily's call. The refusals come one per line in `run.log` when `runall.sh rerun-schedule*.txt` is used.
- **Scope.** First attempts are not affected. Test folders (any other outdir) are not counted.
- **Agreement with tuning_check5.py.** It already reports STOP_ASK_EMILY for more than 2 invalid runs in a pass, so run.sh now stops before that pass's reruns are spent.

**Tests added to `tests/run_lock_test.sh`** (section 3, on the temporary copy of run.sh). Every case keeps the run's own `.exit` file. A case that passes the cap is therefore refused by the next check, and a run.sh without the cap starts no run either.

| Case | Result |
|---|---|
| 2 archived runs in tuning pass 2 | passes the cap |
| 3 archived runs in tuning pass 2 | refused, "stop and ask Emily" |
| pass 1's 3 archived runs, checked for pass 2 | not counted against pass 2 |
| 3 archived runs in tuning pass 1 | refused |
| held-out, 8 archived in the round (5 tuning + 3 held-out) | passes |
| held-out, 9 archived in the round (5 + 4) | refused, "past the 8 reruns approved: stop and ask Emily" |
| a run with no archived attempt | meets the usual "only a run validity5.py archived…" check, not the cap |

**Checked against weakened copies of run.sh:**

- With the cap block removed, the test fails 3 of 60: both per-pass refusals and the 9-run refusal.
- With the round cap raised to 9, it fails 1 of 60 (the 9-run refusal).
- With the pass cap raised to 3, it fails 2 of 60 (both per-pass refusals).

### 10.2 freeze.sh: the tuning instrument, the decision rule and round four's files are now hashed

**Finding.** freeze.sh did not hash the code and data that decide tuning GO or ABANDON: the tuning instrument, or round four's prompts that the tuning runs read. Someone could edit a bound in `tuning_check5.py`, or an entry in `lkp.json` or the grader prompt, after seeing pass 1's grades. `--pass 2` would then print GO, and neither run.sh nor validity5.py would notice.

**Fix.** These files are added by exact name to the round-folder block in `state()`:

- `tuning-instrument/tuning_check5.py`
- `tuning-instrument/tuning_common5.py`
- `tuning-instrument/save_tuning_grades5.py`
- `tuning-instrument/make_tuning_grade_script.py`
- `tuning-instrument/lkp.json`
- `tuning-instrument/premise-points.json`
- `tuning-instrument/tuning-grade-schema5.json`
- `tuning-instrument/tuning-grader-prompt5.md`
- `design/tuning-decision-rule.md`

The names are exact, with no glob, because tuning writes these files into the same folder: `grades-*.json`, `decision-*.json`, `calibration-*.json`, `rd-hand-pass*.json` and `ledger5.jsonl`. The instrument README is documentation and is not hashed.

A new block in `state()` hashes round four's files that tuning reads, 132 lines in all:

    ( cd /w/AgentData/logs && sha256sum gravitas-dsh-ab4/prompts/*.txt gravitas-dsh-ab4/keys/*.md gravitas-dsh-ab4/keypoints/*.json \
        gravitas-dsh-ab4/raw/*.gv-plain.r[12].txt gravitas-dsh-ab4/raw/*.gv-plain.r[12].ndjson \
        gravitas-dsh-ab4/raw/*.gv-grav-base.r[12].txt gravitas-dsh-ab4/raw/*.gv-grav-base.r[12].ndjson )

This departs from the review's suggested line in two ways:

- **The paths carry the folder name** (`gravitas-dsh-ab4/prompts/…`) instead of a bare `prompts/…`. This keeps freeze-start's lines from being mistaken for round five's held-out `prompts/` lines.
- **It also hashes round four's keys, key points and the 48 baseline answers** (finals and streams), besides the prompts. `tuning_common5.py` reads all of them, and they decide GO or ABANDON just as `lkp.json` does. An edit to a key-point file (whose `missing` marks ABSENT must match), or to a baseline final before a batch is built, would otherwise not be noticed. These are extra hashed files only, so the check is stricter, and round four's folder is closed.

`verdict4-amended.py` and `verdict4.py` are not added. `tuning_common5.py` already refuses to import them unless their sha256 matches its constants, and that file is now hashed.

**What this closes.** Every run.sh call compares the state with freeze-start, so an instrument edit made before any later tuning or held-out run is refused. validity5.py's whole-round check reports it as well.

**What remains** (without the optional check in section 9):

- An edit made after the last pass-2 run, before `tuning_check5.py --pass 2` is run, is not refused at that moment. A GO leads to held-out runs, and the first of them refuses on the freeze comparison. Any later validity5.py round check reports it too. An edit that turned GO into ABANDON would run nothing and would go unnoticed, but it would also spend no run.
- After a revision, freeze-start is recorded anew (section 9). An instrument change made then is not refused. It is visible only as a difference between `freeze-start.superseded-N.txt` and the new `freeze-start.txt`, so that diff should be read at each re-freeze.

**Tests added to `tests/run_lock_test.sh`** (new section 4). freeze.sh is still never run. Its two hash blocks are taken out and run on their own:

- **The round-folder block** runs against a temporary folder of copies, so round five's held-out files are never read.
  - It names each of the 8 instrument files and the rule, with no glob over `tuning-instrument/`.
  - It gives 9 lines for them.
  - Files that tuning writes there (grades, decisions, calibrations, RD hand pass, ledger) leave the state unchanged.
  - An edit to `tuning_check5.py`, to `lkp.json` or to the decision rule changes the state.
- **Round four's block** runs as it is (it reads round four's folder only).
  - It gives exactly 132 lines: 12 prompts, 12 keys, 12 key-point files and 96 baseline files.
  - Every case in the tuning schedules has its prompt hashed.
  - run.sh's `R4P` is the folder hashed.

**Checked against weakened copies of freeze.sh:**

- With the added lines removed, the test fails 19 of 60: every new freeze assertion except the no-glob and "files tuning writes" checks (which hold trivially when nothing is hashed) and run.sh's `R4P` check.
- With `lkp.json premise-points.json` replaced by `tuning-instrument/*.json`, it fails 5 of 60. These are the two named files, the no-glob check, the "files tuning writes" check, and the 9-line count (the glob hashes the schema a second time).

### 10.3 Logs and counts

- `dev/selftest-logs/run_lock_test.txt` holds the new 60-assertion output.
- `dev/check_port5.py` was rerun, so `port-diff.txt` and `dev/port5-classify.json` include these edits. Section 4's table shows the new counts for run.sh and freeze.sh. Section 4's list of hand edits describes the port as first written. The lines added here are listed in this section.
