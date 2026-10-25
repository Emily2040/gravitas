# verdict4.py: round-four verdict

`verdict4.py` checks the eight win criteria of `W:\Projects\gravitas-claim-check\docs\dsh-ab\WIN_CRITERIA.md`, including both amendments (all four languages; Japanese and Korean hedge lists). The candidate is gv-grav-c4 and the control is gv-plain, compared on the main set, overall and separately in zh, en, ja and ko wherever a criterion can be measured per language. For every gate cell it prints the measured values, the bounds and PASS or FAIL. Beside the verdict it reports:

- the same gate table for gv-grav-base vs gv-plain (base set);
- a side-by-side matrix of the two tables;
- the attr-set votes (c4 vs base);
- an `IMPROVEMENT: yes/no` line for WIN_CRITERIA's stop rule.

The last line is always `VERDICT: win` or `VERDICT: not a win (failing: <cells>)`. The script uses Python 3 and the standard library only. Comparisons use exact fractions. It was written by an agent that builds nothing in this round. As frozen, its sha256 is `11cdd365b88df9e20a38ad2514ba50a1e3baac6feea796c1f3220429826792ca`, and the script prints its own hash in every report.

## Run

    python verdict4.py              # evaluates this folder, prints the report, writes verdict4.json here
    python verdict4.py --base DIR   # evaluates DIR instead (verdict4.json goes into DIR)
    python verdict4.py --selftest   # synthetic data in a temporary folder; never reads or writes this folder

When a verdict is computed, the exit code is 0, whatever the verdict says. The self-test exits 0 only if every assertion holds.

## What it reads (paths relative to the evaluated folder)

- `prompts/*.txt`: file names only. They must be exactly the 12 cases frozen in the script: zh-flex-hours, zh-insurance-gap, zh-sick-pay, en-529-roth, en-fsa-rollover, en-medicare-part-b, ja-medical-deduction, ja-part-time-leave, ja-wallpaper-restoration, ko-jeonse-protection, ko-severance-pay, ko-unemployment-quit. A case's language is its prefix.
- `blind-map.json`:
  - main, base and attr: exactly one pair per case and round, `round` r1/r2, arms {gv-grav-c4, gv-plain}, {gv-grav-base, gv-plain} and {gv-grav-c4, gv-grav-base} respectively;
  - aa-plain and aa-c4: exactly one pair per case, both sides the same arm, `A_round`/`B_round` = r1/r2.

  This matches `make_pairs4.py`.
- `blind/grades/{opus,sonnet}/<pid>.json`, in round three's format:
  - `pair` must equal the pid, and `winner` must be A, B or tie;
  - each side has the five integer scores 0-10, `added_claim_errors` (a list of strings) and `key_points` (id -> correct|vague|wrong|missing), with exactly the ids of `keypoints/<case>.json`. A top-level `key_points: {A, B}` is also accepted.

  If any field is invalid, the whole grade counts as malformed.
- `keypoints/<case>.json`: `[{"id", "point"}]`, with at least one point and unique ids.
- `claim-notes.json`, `labels-sonnet.json` and `labels-opus.json`, as in round three. A note counts as wrong only when both relabellers say `wrong` with a non-empty `cite`. A `wrong` with an empty cite is a malformed label. **The base-set notes must be listed and labelled too, or the base table's gate 5 fails as metric missing and the improvement line says no.** attr and aa notes are not used.
- `raw/<case>.<arm>.<round>.txt`: finals for gv-plain, gv-grav-base and gv-grav-c4. An empty or whitespace-only file counts as missing.
- `raw/<case>.<arm>.<round>.ndjson`: event streams, used only in the reported section (web pages opened, tool calls).

## Gates as implemented (one table per comparison; the main table decides the verdict)

Each gate is computed for the scope `overall` (12 cases, 24 pairs) and for each language (3 cases, 6 pairs), except gate 2. That gives 8 overall cells plus 7 x 4 language cells, 36 cells in all.

| Cell | Measured (x = gv-grav-c4, y = gv-plain on the main set) | Pass when |
|---|---|---|
| `g1_votes[scope]` | net = x wins - y wins over the scope's main votes (2 graders per pair); A/A net = r1-side wins - r2-side wins in aa-plain and aa-c4 pairs of the same scope | net > 0 and net > max(abs(aa-plain net), abs(aa-c4 net)) |
| `g2_each_grader[overall]` | opus and sonnet separately, 24 votes each | x wins > y wins for each grader. Overall only; per-language counts are printed but not gated |
| `g3_length[scope]` | chars = length of the final file; median over the scope's finals per arm; ratio per pair (same case and round) | median(x)/median(y) <= 1.00, and count of pairs under 0.6 / pairs <= 0.10, i.e. at most 2 of 24 overall and 0 of 6 per language |
| `g4_vague_key_points[scope]` | key-point marks "vague" over the scope's graded answers (both graders) | x <= y |
| `g5_wrong_added_claims[scope]` | the scope's added-claim notes that both relabellers call wrong with a cite; every note listed once and validly labelled by both | x <= y |
| `g6_correct_wrong_key_points[scope]` | key-point marks "correct" and "wrong" | correct x >= y and wrong x <= y |
| `g7_trap_under_8[scope]` | graded answers with trap < 8 | x <= y |
| `g8_hedging[scope]` | markers per 1000 chars per final, mean over the scope's finals, each final counted with its own language's lists | first list x <= 1.00 * y and second list x <= 1.10 * y |

A missing or malformed input fails exactly the cells that need it, with `metric missing: <what>`:

- a missing grade, label, claim-notes row or final text in one language fails that language's cells and the overall cell;
- a missing blind-map, case list, labels file or malformed claim-notes file fails every cell that uses it.

Nothing missing is ever defaulted to a passing value. `VERDICT: win` needs all 36 main cells to pass.

Hedge lists:

- **zh and en:** round three's `verdict.py` lists, split by the language each pattern is written in. The first list is `H_ROUND1` and the second is `H_EXTENDED`, with its exclusions (不可能 for zh; "May" followed by a day or a year for en).
- **ja and ko:** the literal strings of the 2026-10-23 amendment.

The report also prints round three's combined zh+en lists on the zh and en finals, for comparison with round three. It is not gated.

## Improvement over the previous best (reported, not part of the verdict)

`IMPROVEMENT: yes` requires all of the following:

- gv-grav-c4 passes at least as many of the 36 cells (main table) as gv-grav-base passes in the base table, on the same 12 cases;
- the attr-set net (c4 wins - base wins, 48 votes) is above the aa-c4 noise floor, abs(aa-c4 net) overall;
- no cell in either table is "metric missing", and the attr and aa-c4 votes are complete.

Otherwise the line says `no` and gives the reasons. Cells that c4 gains or loses against the base are listed as information. The base table's gate 1 uses the round's two A/A sets (aa-plain, aa-c4), because there is no aa-base set.

## Self-test

`--selftest` prints one line per assertion and ends with `selftest: 249 assertions, 0 failed`. It covers:

- **Pattern units:** zh and en exclusions; ja and ko markers; each list ignores the other languages' markers; Korean spacing.
- **(a) Empty input:** every one of the 36 main cells, and of the 36 base cells, fails as metric missing. The verdict is `not a win`, the improvement line is `no (metric missing)`, the verdict is the last line, and the results serialise. **(a2)** The same holds with only the case list present.
- **(b) Synthetic clear win:** all 36 main cells pass and the verdict is `VERDICT: win`. In the base table only gate 3 fails (the base answers are longer than plain's), so `IMPROVEMENT: yes` (36 vs 31 cells, attr +48 > floor 4). It also checks the per-language floor, the per-language hedge marker counts, and writing and reading back verdict4.json.
- **(c) One language fails:** ko votes go to plain, so only `g1_votes[ko]` fails and the verdict is `not a win`.
- **(d) One input removed or malformed at a time:** a main grade (ja), a relabel entry (en), a c4 final (zh), an empty plain final (en), an A/A grade (ko), a grade whose key-point ids differ (ko), a `wrong` label without a cite (zh), a claim-notes row (ja), a duplicated main pair (en). Each time, exactly the affected cells fail as metric missing and the other cells still pass. An entry from an unknown set is ignored and reported.
- **(e) Degenerate wins fail on their bounds:**
  - gutted answers (gate 3);
  - one en pair under 0.6: fails en, while 1 of 24 passes overall;
  - hedge substitution (gate 8);
  - net equal to the aa-plain floor, and net equal to the aa-c4 floor (gates 1 and 2);
  - a median ratio of 1.02-1.03 (gate 3);
  - a second-list ratio of about 1.20 and a first-list ratio of about 1.06 (gate 8).

  Equal quality passes "no more than" and "at least".
- **(f) Improvement rule:** attr all ties gives no; attr net equal to the aa-c4 floor gives no; a missing base grade leaves the verdict a win but makes the improvement line no (metric missing); base passing every cell gives yes (36 = 36); c4 failing hedging while base passes everything gives no.

A mutation check (run once, outside this folder) found that 18 of 20 deliberate breakages make the self-test fail. The two that survive have no effect on results: a non-strict default in `pair_votes`, and disabling the missing-metric branch in `finish`. Both are caught by later checks.

## Ambiguities resolved

1. **Per-language length rounding.** I read "no more than 10% of pairs" as count/pairs <= 0.10. That allows 2 of 24 overall and 0 of 6 per language. This is the literal reading and the stricter one; rounding up would allow 1 of 6, which is 17%.
2. **Gate 2 is overall only.** WIN_CRITERIA item 2 says "(overall)", and the amendment's list of per-language criteria omits it. Per-language counts for each grader are printed, not gated.
3. **Per-language noise floor.** The floor is max(abs(aa-plain net), abs(aa-c4 net)) within the language's 3 A/A pairs (6 votes each). The overall floor uses all 12 A/A pairs and is not scaled to the main set's 48 votes, as in WIN_CRITERIA and round three.
4. **"No more than" is <=.** Gate 5 uses <= as WIN_CRITERIA says (round three used <). Gates 4, 6 and 7 use counts over the graded answers of both graders. The denominators are equal by design.
5. **Hedge lists per language.** zh and en use only their own-language patterns from round three's lists, and each exclusion stays with its language. Applying the union to every answer would count Chinese 可能 and 一般 inside Japanese text.
6. **Overall hedging.** The mean is taken over all 24 finals per arm, each final counted with its own language's lists (chosen by case prefix, since this round sets the plugin language to the request language).
7. **ja and ko markers are literal substrings.** A space inside a marker matches any whitespace or none, so 확인해 보세요 and 확인해보세요 both count; Korean auxiliary-verb spacing is optional. Known false-positive risk: 아마 also matches inside 아마존 or 아마추어. It applies to both arms alike. Overlapping patterns each count, as in round three.
8. **A `wrong` label without a cite is malformed** and fails gate 5 as metric missing, as in round three. It is not silently treated as "not wrong", which an arm could otherwise use to drop wrong labels.
9. **Length is measured on the final file as written.** It is `len()` of the UTF-8 text, unstripped, as in round three. Pairs are the same case and round. WIN_CRITERIA sets no lower bound on the median ratio (round three had 0.70), so none is gated. The 0.6 per-pair clause and the key-point gates guard against gutted answers.
10. **The base table uses the round's two A/A sets** for gate 1, because there is no aa-base.
11. **Improvement.** It counts cells (36 per table), not cell-by-cell dominance, and lists the regressions. The attr floor is abs(aa-c4 net) overall. Any metric missing on either side, or incomplete attr or aa-c4 votes, gives "no", so that a missing base input cannot inflate the comparison.
12. **The case list is frozen** to the 12 names in prompts/ on 2026-10-23. A swap fails every gate until the list is re-frozen, deliberately. Key-point files need at least one point; WIN_CRITERIA sets no 4-8 limit.
13. **blind-map entries of an unknown set are ignored and reported**, because they feed no metric. A duplicated or missing pair for a known set fails the affected language's cells. The `round` field of aa entries is not checked, because `A_round`/`B_round` carry the information.
