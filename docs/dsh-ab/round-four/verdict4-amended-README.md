# verdict4-amended.py: round-four verdict with the amendments of 2026-10-24 and 2026-10-25

`verdict4-amended.py` decides round four under `W:\Projects\gravitas-claim-check\docs\dsh-ab\WIN_CRITERIA.md`, including its amendments of 2026-10-24 ("gates restored, a mixed judge panel") and 2026-10-25 ("what the cheapest-pass review found"). The 2026-10-24 amendment says the round "is judged on this version and on the version before this amendment; it counts as a win only if it wins on both". The 2026-10-25 amendment changes only the amended version. The script computes both versions:

- **As frozen.** `verdict4.py` is imported unchanged, but only after its sha256 matches the frozen value. It runs on a temporary copy of the folder that holds the opus and sonnet grades only, as "the version before this amendment is judged with the Opus and Sonnet grades only, exactly as it was written".
- **Amended.** Three judges (opus, sonnet, codex; all votes count; gate 2 for each judge) on 52 cells. These are the eight original gates, the restored ones (length floor, request-level wins, mean scores, fabricated sources) and the 2026-10-25 changes:
  - missing key points in gate 4;
  - per-pair and visible-text length checks;
  - a third hedge list;
  - a gate on unverifiable claims;
  - fabricated sources counted in every run, with excuses for citations and opened hosts;
  - a sqrt(2) noise floor;
  - integrity checks (answer hashes, the grade and label ledger, the run validity report) that fail as metric missing.

The output ends with these six lines:

    IMPROVEMENT (as frozen, opus+sonnet): yes|no (...)
    IMPROVEMENT (amended, three judges): yes|no (...)
    IMPROVEMENT: yes|no (...)                       yes only if both versions say yes
    VERDICT (as frozen, opus+sonnet): win | not a win (failing: ...)
    VERDICT (amended, three judges): win | not a win (failing: ...)
    ROUND VERDICT: win | not a win (as frozen: ...; amended: ...; it counts as a win only if it wins on both)

The script uses Python 3 and the standard library only. Comparisons are exact: fractions, and an integer test for the sqrt(2) floor. The first lines of the output print the script's own sha256 and the sha256 of verdict4.py. When a verdict is computed, the exit code is 0, whatever the verdict says. I wrote and froze it; I build nothing else in this round.

**Frozen sha256 of verdict4-amended.py: `5cf3316b8fbb55b50688ca94f2fc2840f339b4b66f50981aa6078959fc715c14`.** verdict4.py: `11cdd365b88df9e20a38ad2514ba50a1e3baac6feea796c1f3220429826792ca` (unchanged). `freeze.sh --state` hashes this script, this README, grader-prompt4.md, save_grades4.py, judge_codex.sh and mutation4.py, so once freeze-start.txt is recorded, any edit to them stops run.sh.

## Run

    python verdict4-amended.py              # evaluates this folder, prints, writes verdict4-amended.json here
    python verdict4-amended.py --base DIR   # evaluates DIR (the JSON goes into DIR)
    python verdict4-amended.py --no-json    # prints only; writes nothing anywhere
    python verdict4-amended.py --selftest   # synthetic data in a temporary folder

The self-test exits 0 only if every assertion holds. It reads only this script and verdict4.py from this folder, never the round's data, and writes only to a temporary folder.

## What it reads (relative to the evaluated folder)

Everything `verdict4.py` reads, in the same formats (see `verdict4-README.md`), plus:

- **`blind/grades/codex/<pid>.json`.** Every judge's file is parsed by verdict4.py's own `parse_grade`.
- **`claim-notes.json`** with rows from all three judges, as written by `build_notes4.py`. The relabellers stay sonnet and opus.
- **`raw/<case>.<arm>.<round>.ndjson`.** Gate input: which hosts did a completed `web_fetch` open with HTTP 2xx?
- **`blind-map.json`'s `A_sha256` and `B_sha256`** (make_pairs4.py), checked against `raw/`.
- **`blind/packets/<pid>.md`.** Its sha256 is compared with the ledger.
- **`ledger.jsonl`.** The append-only ledger of every grade and label received (save_grades4.py, save_labels4.py).
- **`validity.json`** (validity4.py): it must exist, be newer than every file directly in `raw/`, and list no run under `invalid`.

Readers are reused from verdict4.py: `load_cases`, `load_map`, `load_keypoints`, `parse_grade`, `load_labels`, `parse_ndjson`, the hedge lists, `literal` and `count_markers`. That keeps input validation the same in both versions.

## The version before the amendments

`run_frozen()` checks the sha256 of `verdict4.py` and imports it. It copies what verdict4.py reads into a temporary folder: `prompts/`, `keypoints/`, `raw/`, `blind/grades/opus/`, `blind/grades/sonnet/`, `blind-map.json`, both labels files, and `claim-notes.json` without its codex rows. verdict4.py rejects a note from any other grader, so its gate 5 would otherwise fail everywhere. It then calls verdict4.py's `evaluate()` and `render()`, and prints that report with each line prefixed `  | `.

A hash mismatch, a missing file or a crash inside verdict4.py makes the frozen verdict "not computed", which counts as not a win. verdict4.py writes nothing in this path, and no `__pycache__` is written.

## Gates as implemented (amended version)

x = gv-grav-c4 and y = gv-plain on the main set. The base table (gv-grav-base vs gv-plain on the base set) uses the same 52 cells. A gate is checked overall (12 cases, 24 pairs) and per language (3 cases, 6 pairs), except gates 2 and 12, which are overall only.

| Cell | Measured | Pass when | Source |
|---|---|---|---|
| `g1_votes` | net = x wins - y wins, all three judges' votes. A/A net = r1-side wins - r2-side wins. Ties per set reported | net > 0 and net > sqrt(2) x max(abs(aa-plain net), abs(aa-c4 net)) of the same scope | criterion 1; sqrt(2): 2026-10-25 |
| `g2_each_judge` | opus, sonnet and codex separately | x wins > y wins for each judge. Overall only | criterion 2; 2026-10-24 |
| `g3_length` | chars per final, on raw text and on visible text. Visible text drops blank lines, table rule lines and horizontal rules; removes leading `#`, list markers, `**` pairs and table pipes; and collapses whitespace | On each of the two texts: 0.70 <= pooled median ratio <= 1.00; 0.70 <= median of the per-pair ratios <= 1.00; pairs under 0.6 / pairs <= 0.10 | criterion 3; floor: 2026-10-24; per-pair and visible: 2026-10-25 |
| `g4_vague_key_points` | key-point marks "vague" and "missing" (3 judges) | vague x <= y and missing x <= y. The A/A vague floor is reported beside it | criterion 4; missing: 2026-10-25 |
| `g5_wrong_added_claims` | notes from all three judges that both relabellers call `wrong` with a cite. Every note must be listed once and labelled by both | x <= y. Wrong per 1000 chars reported | criterion 5 |
| `g6_correct_wrong_key_points` | marks "correct" and "wrong" | correct x >= y and wrong x <= y | criterion 6 |
| `g7_trap_under_8` | answers with trap < 8 | x <= y | criterion 7 |
| `g8_hedging` | markers per 1000 chars, mean over finals, each final with its own language's lists | first list x <= 1.00 y; second x <= 1.10 y; third x <= 1.10 y overall only (reported in the language cells) | criterion 8; third list: 2026-10-25 |
| `g9_requests` | per request, its 6 votes summed (+1, -1, 0) | net-positive requests > net-negative requests | 2026-10-24 |
| `g10_mean_scores` | means over graded answers | total x >= y; correct and useful x >= y - 0.5 | 2026-10-24 |
| `g11_fabricated_sources` | source-claim phrases in every final of every run. Each is excused, or not (see below) | unexcused x <= unexcused y. Always measurable | 2026-10-24, redefined 2026-10-25 |
| `g12_unverified_claims` | notes from all three judges that both relabellers call `unverified` | x <= 1.10 y overall. Per language it is reported beside the A/A difference of the same count (r1 side - r2 side) | 2026-10-25 |

**Fabricated sources.** The phrases are applied whole to every final, with `re.I`:

- zh and en: round three's list;
- ja and ko: the amendment's regular expressions, exactly as written.

A phrase is **excused** in either of two cases:

- **A citation within 25 characters.** "Within" is measured as the gap between the two spans. The citations recognised are:
  - `第N条` (N in digits or CJK numerals), `N条` (digits), `제N조`, `〔YYYY〕N号`;
  - Publication/Pub. N, section/sec. N, §N, N U.S.C., IRC N, No. N;
  - a URL (`http(s)://…`, `www.…`).
- **A named opened host.** The final names a host that a completed `web_fetch` of the same run opened with HTTP 2xx. The tool result must start "Fetched <url> (HTTP 2xx)". The host counts with and without a leading `www.`.

Phrases, citation excuses, host excuses and unexcused phrases are printed per arm.

### Integrity: all of these fail as metric missing

- **The validity report** is missing, unreadable, not newer than a file in `raw/`, or lists a run under `invalid`. Every amended cell fails, both tables.
- **An answer does not match its stored sha256.** The stored hash is `A_sha256`/`B_sha256`; the recomputed one comes from the final, read as UTF-8 and stripped, or from the placeholder "(no answer: the run produced no final text)" when the final is blank. A missing stored hash also counts. The grades of every pair that holds that answer fail, and so do the text gates for that (case, arm, round).
- **The ledger check fails.** For a grade, it fails when any of these holds:
  - the ledger is missing or unreadable;
  - the (pid, judge) has no valid ledger entry;
  - the grade file differs from its first valid ledger grade after the last replace record;
  - the packet's current sha256 differs from the one recorded with that grade.

  For a label, it fails when the labels file entry differs from the first valid ledger label for its (id, relabeller). That label then counts as missing in gates 5 and 12.

Re-grade counts appear under "reported beside". They are given per set and by the arm the first valid grade picked, together with re-label counts per relabeller.

`VERDICT (amended, three judges): win` needs all 52 main cells to pass. NOT MEASURABLE no longer exists: the 2026-10-25 amendment makes g11 always measurable. `VERDICT (as frozen, ...)` is verdict4.py's own verdict on its 36 cells. `ROUND VERDICT: win` needs both versions to be wins.

## Reported beside the gates (not gated)

- **Integrity:** the validity report (with runs graded as is after their rerun, flagged runs and rule-file problems), answer-hash mismatches, and re-grades and re-labels from the ledger.
- **Inputs:** valid grade files per judge, claim-notes rows per judge, blind-map issues.
- **Sign tests** per set and scope, with per-judge win-loss-tie counts.
- **A/A noise** per scope: votes, ties and vague marks.
- **The share of decisive votes that went to the shorter answer** (2026-10-25), per judge and per set, for main, base, attr, aa-plain and aa-c4. In the A/A sets any length preference is pure bias. A vote between answers of equal length, or with a final missing, is left out.
- **Pairwise Cohen's kappa** between judges.
- **Format metrics:** medians of characters, English words, list items, bold spans and headings, per arm and language.
- **Event streams:** runs that opened a page with HTTP 2xx, and runs that only searched.
- **Beside gate 4:** the A/A vague floor.
- **Beside gate 5:** wrong claims per 1000 chars.
- **Beside gate 11:** unexcused phrases per 1000 chars.
- **Beside gate 12:** per language, and the A/A difference.

## IMPROVEMENT (WIN_CRITERIA's stop rule)

- **As frozen:** verdict4.py's own rule, on opus and sonnet.
- **Amended:** yes only when all of these hold:
  - no cell in either table is metric missing, and the attr and aa-c4 votes are complete;
  - c4 passes at least as many of the 52 cells as base;
  - the attr net is above sqrt(2) x abs(aa-c4 net). The sqrt(2) is there because the attr set has twice the pairs of aa-c4, as in gate 1.
- **`IMPROVEMENT: yes`** only if both versions say yes.

## Self-test

`--selftest` ends with `selftest: 1113 assertions, 0 failed`. Every 2026-10-25 route has a scenario that fails without its fix. The mutation test shows that: removing each fix makes the self-test fail. The scenarios:

- **Units:**
  - every source-claim pattern;
  - the excuse rule: an article inside the phrase, 25 characters away (excused), 26 away (not excused), a publication number, 제N조, 第N条, N条, 〔YYYY〕N号, a URL, a named host the run opened, and a named host it did not open;
  - opened hosts: HTTP 200 counts; HTTP 403, a failed fetch and a web_search do not;
  - visible text;
  - the third hedge list, including the Korean spacing;
  - format metrics.
- **(a) Empty input:** all 52 + 52 cells fail as metric missing, both verdicts are not a win, and the final six lines are in order. **(a2)** The same with only the case list present.
- **(b) Clear win:** all 52 cells pass; base fails gate 3 only; the frozen version wins; IMPROVEMENT yes (52 vs 47, attr +72 > sqrt(2) x 4). Measured values are checked:
  - g1: net 72 against a floor of 8 (scaled 11.31); ties main 0, aa-plain 20, aa-c4 24;
  - g3 on raw and visible text;
  - g4: vague 72 vs 144, missing 0 vs 0, A/A vague floor 36;
  - g5: codex's notes counted;
  - g8: the third list gated overall only;
  - g11: all 24 runs counted;
  - g12: 72 vs 72 unverified;
  - shorter-answer shares: main 1.0 per judge, aa-plain 12 of 16, aa-c4 1/3;
  - integrity clean;
  - the JSON written and read back.
- **(c) Missing grades:** all codex grades removed; all opus grades removed; one codex main grade; one codex grade with wrong key-point ids; one codex A/A grade; one relabel of a codex note; one codex claim-notes row. Each fails exactly its cells.
- **(d) Judges and the floor:**
  - codex alone prefers plain: only g2 fails;
  - codex 12 vs 12: only g2 fails;
  - net equal to the floor: g1 and g2 fail;
  - **(d4)** net between the floor and sqrt(2) x floor in every scope (8 vs 6 per language, 32 vs 24 overall): g1 fails.
- **(e) Degenerate wins:**
  - gutted answers (0.63): only the four floor checks fail;
  - all net votes from one request; tied requests;
  - total below plain; trap 7 vs 9;
  - relabellers disagree; one and three short pairs;
  - hedge substitution; second list at 1.13-1.15x; first list at 1.06x;
  - more wrong key points;
  - **(e2l)** vague points turned into missing ones (plain c,c,v,v,v vs c4 c,c,m,m,m): g4 fails on the missing check, while the frozen version passes;
  - **(e2m)** the uneven cut (0.61 on the short and long requests, 0.98 on the middle one): pooled ratio about 0.98; only the per-pair median checks fail;
  - **(e2n)** markup only (c4 has more words but drops plain's bullets and bold): raw ratio 0.81; only the visible ceiling checks fail;
  - **(e2o)** off-list hedging: only the third-list check fails, overall;
  - **(e2p)** unverifiable claims 82 vs 72 fails; **(e2q)** 79 vs 72 passes;
  - useful 1.0 below fails and 0.5 below passes; more source phrases; equal grading; ko votes to plain.
- **(f) Fabricated sources:**
  - **(f1)** c4 opens a page (HTTP 200) every run and claims sources naming no opened host: fails;
  - **(f2)** each final names the opened host: excused;
  - **(f3)** the fetch returned 403: not excused;
  - **(f4)** each phrase sits next to a citation: excused; **(f4b)** 30 characters away: not excused;
  - **(f5, f6)** a missing or unreadable event stream: metric missing.
- **(g) The versions disagree:** amended win with a frozen loss; verdict4.py altered; a simulated crash in verdict4.py.
- **(h) Exact length bounds:** 0.70 passes, 0.699 fails, 1.00 passes, 1.001 fails.
- **(i) Improvement:**
  - **(i1)** attr net +32 against a floor of 24 (above it, but not above sqrt(2) x 24): no;
  - a missing codex base grade: no (metric missing);
  - base passing everything: yes (52 = 52);
  - c4 failing hedging: no (47 < 52).
- **(j) Integrity:**
  - **(j1)** a final edited after packaging: its pairs' grade cells and its language's text cells fail;
  - **(j2-j4)** validity.json missing, older than a run file, or listing an invalid run: every cell fails;
  - **(j5)** a grade file replaced by a different valid grade; **(j5b)** with the re-grade logged later: still fails (the first valid grade is the one used); **(j5c)** a logged replace with its reason: passes and is counted;
  - **(j6)** a label changed after it was received;
  - **(j7)** no ledger: every grade cell fails;
  - **(j8)** a packet edited after grading;
  - **(j9)** a blind-map without answer hashes;
  - **(j10)** a plain final blank after its rerun, packaged as the placeholder: its grades stand, its text gates fail, and the frozen version fails its text gates.

## Mutation test

`mutation4.py` copies each script into a temporary folder, beside unmodified copies of the others. It applies one deliberate breakage at a time and runs that copy's own self-test. A mutant that removes one of the 2026-10-25 fixes is the evidence that the fix's self-test fails without it. The full output is in `mutation/mutation-report.txt`: final run 2026-10-25, against the sha256 above, with every original unchanged after the run.

- **verdict4-amended.py: 65 of 67 killed.** Every 2026-10-25 fix has a mutant that removes it, and all are killed:
  - the missing check, the per-pair median, visible text, the third list, the unverified gate, sqrt(2);
  - the excuse window, the HTTP 2xx rule, the old "no page" rule;
  - the answer-hash, ledger, first-valid, replace-record, packet-hash, validity-freshness, invalid-run, missing-validity, label-ledger and placeholder checks.

  Survivors:
  - **A04** removes "net > 0" from gate 1. It is equivalent: the floor is never negative, and the sqrt(2) test itself requires net > 0.
  - **A32** makes a cell with nothing measured pass. That branch is unreachable: no gate finishes with no checks and nothing missing.
  - An earlier run also left **A65** (a blank final's placeholder not recognised). The self-test computed the synthetic answer hashes with the same function it was testing. The synthetic hashes are now computed separately, as make_pairs4.py does, and the rerun kills A65.
- **verdict4.py (frozen; its own 249-assertion self-test): 24 of 27 killed.** Survivors:
  - **V09** (all relabellers becomes any) is equivalent on its data, where the relabellers always agree.
  - **V12** (trap threshold 6) is not exercised: no trap score falls between 6 and 8.
  - **V16** is the unreachable branch.

  V09 and V12 are gaps in the frozen self-test, which cannot change. The amended self-test covers both gates in (e2e) and (e2d), and also checks the unmodified verdict4.py's verdict there.
- **save_grades4.py: 10 of 10 killed** (routes a and b). **save_labels4.py: 7 of 7** (routes b and c). **make_pairs4.py: 5 of 5** (route d).

## Companion files

- **`grader-prompt4.md`:** round three's grader prompt for four languages. The same text goes to all three judges; only the delivery lines after it differ.
- **`workflows/grade4.js`:** returns, with each row, the exact `prompt` it sent and the `packetPath` (2026-10-25, route a).
  - The prompt is the grader prompt with trailing whitespace removed, plus the frozen delivery lines.
  - Tested end to end with stub agents in node (no model): its 14 rows were saved by save_grades4.py, and a row with an edited prompt was refused.
- **`save_grades4.py`:**
  - validates and saves the Claude grades, and records the codex grades (`--record`, called by judge_codex.sh);
  - **route (a):** refuses a row whose prompt is not grader-prompt4.md plus the frozen delivery lines, or whose packet is not `blind/packets/<pid>.md`; refuses a codex session whose prompt is not grader-prompt4.md plus judge_codex.sh's delivery lines and the current packet;
  - **route (b):** appends every grade received to the ledger with its packet's hash. The grade used is the first valid one after the last replace record. `--replace REASON` and `--retire JUDGE PID REASON` log the reason. It prints re-grade counts per set and by the first valid grade's arm, and `--restore` puts the first valid grades back;
  - self-test: 35 assertions.
- **`save_labels4.py`** (routes b and c):
  - appends every label received to the ledger. The label used is the first valid one, and labels-*.json are written from the ledger;
  - writes nothing when there is a problem. Problems are an unreadable output, an id that is not a note, two different labels for one id in the outputs given, or a note left without a valid label. An empty batch that a later file fills is not a problem;
  - self-test: 11 assertions.
- **`make_pairs4.py`** (route d):
  - stores `A_sha256` and `B_sha256` for every entry;
  - refuses an answer matching `gv-(plain|grav)|gravitas-dsh|AgentData|\br4-`;
  - packages a final still blank after its rerun (it is in reruns.json) as the placeholder; a blank final not yet rerun still stops the build;
  - self-test: 8 assertions.
- **`judge_codex.sh`:**
  - runs `codex --search exec -m gpt-6-astra -c model_reasoning_effort="high" -s read-only --skip-git-repo-check --ephemeral --output-schema <schema> -o blind/grades/codex/<pid>.json -` from an empty folder, at most 3 at a time;
  - keeps each session's exact prompt in `judge-codex-runs/<pid>.prompt.txt`, records each grade in the ledger, and skips pairs that already have a valid ledger grade;
  - refuses unless `--approved` (a real run, Emily's quota) or a `CODEX_STANDIN` that `command -v codex` resolves to;
  - tested only with a stand-in (41 assertions). The `--search` flag order is unverified until the first real `--approved --limit 1` call.
- **`mutation4.py`:** the mutation test above.

## Ambiguities resolved

1. **"As frozen, with the Opus and Sonnet grades only"** is run on a filtered temporary copy (see above). verdict4.py itself is imported unchanged after its hash check.
2. **Gates 2 and 12 are overall only.** Criterion 2 says "(overall)". The 2026-10-25 amendment gates unverifiable claims "overall", and reports them per language.
3. **The restored gates apply overall and per language**, except where an amendment says "overall".
4. **Length.** Every g3 check must pass on raw text and on visible text, each with both the pooled and the per-pair medians.
   - Visible lines are joined with one newline.
   - A plain final with no visible text fails as metric missing.
   - A list marker is a bullet followed by a blank, or a number followed by `.`, `、` or `)` (and full-width forms), so a line starting with `**bold**` keeps its text.
   - Table rule lines and horizontal rules are lines made only of `|`, `:`, dashes, `=`, `_` and `*`, with at least three dashes, `=`, `_` or `*`.
5. **Missing key points** are compared as counts of "missing" marks: x <= y, every scope.
6. **The third hedge list is used exactly as written.** The zh and en entries are regular expressions; the ja and ko entries are literal strings in which a space matches any whitespace or none, as verdict4.py reads the other ja and ko lists. The rate is markers per 1000 chars, mean over finals, gated at 1.10 overall only.
7. **Unverifiable claims:** notes that both relabellers call `unverified`, from all three judges. The bound is x <= 1.10 y, exact. The A/A difference is the unverified-by-both count on the r1 side minus the r2 side.
8. **"Within 25 characters"** means the gap between the phrase's span and the citation's span is at most 25. A citation overlapping the phrase also excuses it.
   - Citations are checked first, then hosts.
   - A named opened host excuses every phrase in that final, as the amendment words it ("when the final names a host"), not only a phrase near the host.
   - "Opened with HTTP 2xx" is read from the tool result's first line, "Fetched <url> (HTTP nnn)". A completed result whose code is not 2xx opens nothing.
9. **The sqrt(2) floor** is tested exactly as net > 0 and net² > 2 x floor². The same scaling is used for the attr floor in IMPROVEMENT.
10. **Shorter-answer share** uses raw character counts. Ties and equal lengths are left out, and so is a vote with a final missing.
11. **Integrity failures are scoped to what they touch.**
    - Validity problems fail every cell.
    - A hash mismatch fails that answer's pairs' grades and its text cells.
    - A ledger mismatch fails that grade or label.
    - "Newer than every run file" means a later modification time than every file directly in `raw/`; `raw/attempt1/` is left out.
    - The validity report's `rule_files` problems and `final_attempt_invalid` runs are reported, not gated, because the amendment names only runs still due a rerun.
12. **The ledger reference** is the first valid entry after the last replace record. Without a replace record that is "the first valid one". A replace record needs a reason (`--replace REASON`, `--retire ... REASON`), and is counted in the re-grade report.
13. **"Re-grade counts per set and arm"** are (pair, judge) slots with more than one entry or a replace record. They are counted per set and split by the arm the first valid grade picked, so re-grades aimed at pairs one arm won show up.
14. **The placeholder for a blank final.** Its hash is accepted as matching an empty final, so the pair's grades stand. The text gates still fail as metric missing for an empty final, as in both versions. validity4.py's docstring says such an answer "loses every pair it is in and its key points count as missing", and the judges grade the placeholder accordingly.
15. **An earlier resolution that still stands:** "opened a web page" means a completed web_fetch. The new rule needs HTTP 2xx, and only to excuse a phrase, so a web_search never excuses anything.

## What in the criteria I think is wrong or not measurable

- **The host excuse is broad.** One named host that the run opened with 2xx excuses every source-claim phrase in that final, including phrases about other sources. That is the amendment's wording, but an answer that fetches one official page and names it can claim "according to …" about anything else. A stricter rule would excuse only a phrase within 25 characters of the named host.
- **Citations excuse by position, not by truth.** Any article or document number within 25 characters excuses a phrase, even a made-up one. Gate 5 (wrong claims) and the key points are what catch an invented article.
- **`\b` and CJK.** The English patterns (`\baccording to\b`) do not match right after a CJK character, because CJK characters are word characters to `\b`. An English phrase glued to Chinese text is missed. This matters only for mixed-language answers.
- **Per-language cells stay coarse.** There are 3 requests and 18 votes per language, and gate 3 per language allows no short pair (0 of 6). The sqrt(2) floor per language is about 2.8 x the A/A net of 9 votes.
- **The mean-total gate has no tolerance.**
- **The integrity checks prove consistency, not honesty.** They catch a grade, label, packet or final changed after the fact. They cannot catch an operator who runs everything again from scratch and writes a fresh ledger. The frozen hashes in freeze-start.txt, committed and sent to Emily before the first run (the run side), and a freeze-end diff are what close that.
- **The Codex output schema and the `--search` flag order** have not been tried against the real CLI, because no calls were allowed. Run `judge_codex.sh --approved --limit 1` first.
