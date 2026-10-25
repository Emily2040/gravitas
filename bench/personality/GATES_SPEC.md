# Gate spec for the Gravitas personality and slop benchmark

This file says what the verifier checks and where every bound comes from. The verifier (`verify.py`) is written and frozen by an agent that builds nothing in this benchmark. It reads one file, `measured.json`, which `measure_all.py` computes from the data on W: (answers, transcripts, verdicts, question set). The verifier never reads a label an item declares about itself: languages come from the script of the text, rule loading from each run's own log or transcript, and wins from judge verdicts.

Rules from `C:\Users\emily\AgentRules\QUALITY_LOOP.md` that apply:
- A missing metric fails its gate with the message "metric missing". There is never a `?? passingValue` fallback.
- `verify.py --self-test` runs every gate on `{}` and asserts that every gate fails. It also runs one red and one green case per gate.
- Two bounds on every number, unless the gate is one-sided on purpose and the reason is written beside it.
- Each gate names the question a person would ask that it stands for.
- The verifier does not change during a round. Changes happen between rounds, with the evidence written down.

Reference numbers used for bounds:
- AA-PersonalityBench (artificialanalysis.ai, October 2026): 30 questions per trait; average words per answer Gemini 4 Argon 790, GPT-6 Astra 352, Claude Sonnet 5.5 450; Gemini has the most lists (3.9), colons (14.5) and bold (17.2) per answer; Gemini's Transparency index is at the 18th percentile.
- `docs/dsh-ab/WIN_CRITERIA.md` (Emily's frozen DSH win criteria): length ratio of medians at most 1.00 and at least 0.70; at most 10% of pairs below 0.6 of plain's length; hedge markers at most 1.00 times plain on the first list and 1.10 times on the extended list; the win must hold in each of zh, en, ja and ko; an A/A noise floor is measured every round.
- My pilot (2026-10-24, 8 questions, DeepSeek judge, both orders): 100% of verdicts parsed; the two orders agreed on 84% of comparisons and flipped on 10%; "A" won 51.4% of non-tie verdicts; ties were 10.8%.

## A. Question set: is this a fair, native, multilingual test that was never tuned on?

Inputs: `measured.json["questions"]`, from `questions/<set>/report.json` and a native check by a judge that is not DeepSeek.

| id | question it stands for | measurement | bounds |
|---|---|---|---|
| A1 | Is the set as large as asked? | `total` | 1,000 to 1,300 |
| A2 | Is Chinese the main language without crowding out the others? | share of `by_lang` | zh 0.35 to 0.50 and the largest; en, ja and ko each 0.13 to 0.30 |
| A3 | Does every trait get about as many questions as in AA? | `by_trait_generated` (DeepSeek-drafted only) | each of the 30 traits 30 to 45 |
| A4 | Are there both inviting and neutral questions, like AA? | `by_mode_generated` invite share | 0.40 to 0.60 |
| A5 | Is each question in the language it claims? | `script_lang_mismatch` (measured from the text) | 0 to 0.01 of `total` |
| A6 | Are there near-copies inside a language? | `max_cos_within_lang` per language | each below 0.60 (and present for all four languages) |
| A7 | Could held-out questions have leaked into tuning? | `id_overlap_tuning_heldout`, `public_or_seed_in_heldout`, `max_cos_tuning_vs_heldout` | 0, 0, each below 0.60 |
| A8 | Is the held-out split big enough to confirm on? | `by_split_generated["heldout"]` / generated | 0.45 to 0.55 |
| A9 | Do the questions read as native, not translated, to a reader who did not write them? | `native_check`: a non-DeepSeek judge's yes rate on a sample | sample at least 15 per language; yes rate at least 0.85 per language (one-sided: more natural is never a problem) |
| A10 | Is there a mix of short and long questions in each language (AA's examples are short; the drafts skewed long)? | `by_bucket_lang` share of `short` | 0.15 to 0.60 per language |

## B. Judges: can the verdicts be trusted?

Inputs: `measured.json["judges"]`, `["calibration"]`, `["self_preference"]`.

| id | question | measurement | bounds |
|---|---|---|---|
| B1 | Does each judge give a usable verdict? | parsed / requested, per judge | at least 0.98 (one-sided: a parse rate cannot be too high) |
| B2 | Does the judge give the same verdict when the answer order is swapped? | flips / swapped comparisons, on at least 300 swapped comparisons per judge used for more than 10% of verdicts | flip rate 0.00 to 0.15 |
| B3 | Does the judge favour the first answer? | share of "A" among non-tie verdicts | 0.45 to 0.55 |
| B4 | Is the judge discriminating (neither always tying nor never)? | tie share | 0.02 to 0.40 |
| B5 | Does the cheap DeepSeek judge agree with judges from other model families on the same comparisons? | Cohen's kappa (A, B, tie) and direction agreement on non-tie pairs, DeepSeek against the non-DeepSeek verdicts on a shared sample of at least 300 comparisons spread over the 16 traits in `judge.py`'s focus plan | kappa at least 0.40 and direction agreement at least 0.75. If a single trait has kappa below 0.20 on at least 15 shared comparisons, its DeepSeek verdicts are flagged and the result for that trait counts only from non-DeepSeek judges. |
| B6 | Does DeepSeek prefer DeepSeek-written answers? | on comparisons of a DeepSeek answer against a Gemini answer judged by both families: (DeepSeek judge's share for the DeepSeek answer) minus (non-DeepSeek judges' share) | at most 0.10. If this is exceeded, cross-family results are reported from non-DeepSeek judges only, and the gate is marked so. |
| B7 | Is the panel mixed, as asked? | share of non-DeepSeek verdicts among the held-out verdicts behind each reported result | at least 0.10 |

## C. Results: does Gravitas beat plain on the held-out split, on each platform?

Inputs: `measured.json["results"][platform]`, platform `deepseek` (ds-plain vs ds-grav or a candidate) and `gemini` (gm-plain vs gm-grav or a candidate). Differences are Elo(Gravitas arm) minus Elo(plain arm) from `bt.py` (Firth-penalised Bradley-Terry, ties as half, question-clustered bootstrap, 1,000 resamples, 95% intervals), on held-out verdicts only.

| id | question | measurement | bounds |
|---|---|---|---|
| C1 | Is Gravitas more transparent? | Transparency difference: mean of the member traits' differences, Sycophantic's sign flipped, with its bootstrap interval | point above 0 and interval low end above 0 |
| C2 | Does Gravitas have less slop? | Slop difference | point below 0 and interval high end below 0 |
| C3 | Is it at least as direct and willing to push back? | Direct, Constructive Pushback, Answer First, Bottom-Line Summary differences | each interval low end above -50 |
| C4 | Does cutting slop keep the substance? (guards) | Information Dense, Evidence-Based, Actionable Guidance, Pragmatic, Natural Sounding, Emotionally Intelligent differences | each interval low end above -50 |
| C5 | Is the answer shorter or no longer, without being gutted? | median over pairs of (Gravitas characters / plain characters); share of pairs below 0.6 | DeepSeek: median 0.70 to 1.00 and the share at most 0.10 (WIN_CRITERIA). Gemini: median 0.44 to 1.00 (0.44 is GPT-6 Astra's 352 words over Gemini's 790 in AA, the shortest frontier model AA lists) and the share at most 0.35 |
| C6 | Is "admits uncertainty" honest rather than hedging sprayed on? | hedge markers per 1,000 characters, Gravitas / plain, first and extended lists | first at most 1.00, extended at most 1.10 (WIN_CRITERIA), and present for both |
| C7 | Is pushback earned, not manufactured? | Constructive Pushback difference on neutral-mode questions only | interval high end below +150 (a Gravitas arm that disagrees with ordinary questions is gaming C3) |
| C8 | Does the win hold in each language? | C1 and C2 point estimates per language (zh, en, ja, ko) | same sign as the overall gate in all four (intervals reported, not gated, because per-language samples are small) |
| C9 | Is the difference bigger than the noise? | A/A: plain run twice on the same 150 held-out questions, judged the same way; the absolute Transparency and Slop differences between the two plain runs | each C1/C2 difference larger in size than the A/A difference for the same quantity |
| C10 | For Gemini, does Gravitas cut the formatting AA measures most? | bold, list items and colons per answer, Gravitas / plain | each at most 1.00 (one-sided: less formatting is the aim on Gemini; C4 guards the content) |

## D. Process: was it run the way the result says?

| id | question | measurement | bounds |
|---|---|---|---|
| D1 | Did every counted answer actually run? | per arm: share of runs with exit 0 (DSH) or status SUCCESS (agy) and non-empty text | at least 0.98 |
| D2 | Did the Gravitas arm carry its rule, and plain carry none? | DSH: the rule log hash equals the expected hash; agy: the transcript holds all three marker lines of its own rule and none of Emily's personal rules; plain: no rule log, no marker lines | 1.00 of counted runs |
| D3 | Was the held-out split untouched while tuning? | for each candidate, its first held-out run comes after its rule file's freeze time (`rules/<name>/FROZEN` written before any held-out run) | true for every candidate |
| D4 | Is this the verifier that was frozen? | sha256 of `verify.py` and `GATES_SPEC.md` equal to `VERIFIER_FREEZE.md` | equal |
