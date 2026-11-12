# verdict.py: round-three verdict

`verdict.py` applies the amended verdict rule in `criteria.md` (items 1-10) as ten named gates. For each gate it prints the measured values, the bounds and PASS or FAIL. It then prints the items criteria.md reports beside the verdict, and ends with one line: `VERDICT: beats plain` (every gate passes) or `VERDICT: not shown (failing: ...)`. It uses Python 3 and the standard library only. Comparisons use exact fractions.

## Run

    python verdict.py              # evaluates the folder the script is in, writes verdict.json next to it
    python verdict.py --selftest   # synthetic data in a temporary folder; never reads or writes the real folders

The exit code is 0 whenever a verdict was computed, whatever it says. The self-test exits 0 only if every assertion holds.

## What it reads (paths relative to this folder)

- `prompts/*.txt`: file names only, to get the case list. They must be exactly the 10 held-out cases named in criteria.md.
- `blind-map.json`. The main set must have one pair per case and round (gv-grav vs gv-plain). aa-plain and aa-grav must have one pair per case, with `A_round`/`B_round` = r1/r2. attr and draft are reported only.
- `blind/grades/{opus,sonnet}/<pid>.json`: one object, or an array holding exactly one object. It needs `pair` equal to the pid, `winner` A|B|tie, and A and B objects. Each of A and B has the five integer scores 0-10, `added_claim_errors` (a list of strings) and `key_points` (id -> correct|vague|wrong|missing). A top-level `key_points: {A: ..., B: ...}` is also accepted. If any field is invalid, including key-point ids that differ from `keypoints/<case>.json`, the whole grade counts as malformed, and every gate that uses grades (1-7) fails as "metric missing".
- `keypoints/<case>.json`: `[{"id", "point"}]`, 4 to 8 points with unique ids.
- `claim-notes.json`, `labels-sonnet.json`, `labels-opus.json`. Every main-set `added_claim_errors` entry must appear exactly once in claim-notes, and both relabellers must label it. A note missing a label from either one fails gate 6, and so does a `wrong` label with an empty `cite`.
- `raw/<case>.<arm>.<round>.txt` (finals), `.ndjson` (did the run open a web page?) and `raw/<case>.gv-grav.<round>.claims.jsonl` (check telemetry). `raw/<case>.gv-grav-draft.<round>.txt` is optional.
- Optional: `listed-labels.json` (cut rate of wrong vs right listed items) and `run.log` (seconds per run). These are reported only.

## Self-test

`--selftest` prints one line per assertion and a final count. It checks:

- the pattern units;
- **(a)** on an empty folder, and on a folder holding only the case list, every gate FAILS as "metric missing";
- **(b)** on a synthetic dataset where Gravitas clearly wins, every gate PASSES and the verdict line is `VERDICT: beats plain`;
- **(c)** the same dataset with one input removed or malformed, one at a time: a main-set grade file, a relabel entry, an A/A grade, a final text, an event stream, a key-point id, the cite of a "wrong" label. Exactly the affected gates fail as "metric missing" and the rest still pass;
- **(d)** degenerate wins fail on their bounds: gutted answers (gate 8), hedge substitution (gate 9), plain winning (gates 1-3), and a net equal to the A/A noise floor (gate 1).
