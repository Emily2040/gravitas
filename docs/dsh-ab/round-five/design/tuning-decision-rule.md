# Round five tuning decision rule (pre-registered; written by the design workflow, 2026-10-25)

Write and commit this rule before pass 1's first run. Commit with it the frozen grader prompt, the limited-key-point list below, and tuning_check5.py. An agent that wrote neither the change nor the rule computes the decision.

RUNS
- Pass 1: 12 gv-grav-c5 runs, one per round-four prompt, with the plugin in the prompt's language.
- Pass 2: 12 more runs, of either the same text or the one revision.
- No new gv-plain or gv-grav-base runs. Baselines are round four's existing answers on the same 12 prompts: base r1, base r2, plain r1, plain r2.
- An invalid run gets one rerun. More than 2 invalid runs in a pass means stop and ask Emily.

INSTRUMENT
Grader: Claude Opus 5.5, one answer per session, blind to arm and run. It sees the prompt, the round-four key, keypoints\<case>.json, the limited-key-point list, and the answer.

Calibration, before any DeepSeek run:
- Grade the 48 baseline answers once.
- The grader must mark FLAT or WRONG on at least 2 of the 3 items all three judges marked wrong: en-529 base r1 kp7, ja-medical base r1 kp7, ko-jeonse base r2 kp5.
- It must mark KEPT on en-529 plain r1 kp7 and en-fsa plain r1 kp3.
- Otherwise fix the rubric (not the change) and recalibrate.

Each pass grades one shuffled batch of 60 answers: the 12 c5 answers plus the same 48 baselines graded again. Compare c5 only with baselines graded in the same pass. Report the grader's retest change on the 48.

LIMITED KEY POINTS (LKP): 42 key points whose truth depends on a maximum, condition, exception, open fact, date window, or a rule versus a safe pick.
- en-529: 1, 4, 7, 8
- en-fsa: 2, 3, 4, 5
- en-medicare: 1, 5, 6, 7
- ja-medical: 1, 2, 4, 7
- ja-part: 3, 5, 6
- ja-wallpaper: 3, 4, 5
- ko-jeonse: 2, 4, 5
- ko-severance: 2, 4, 6
- ko-unemployment: 2, 4, 5
- zh-flex: 3, 6, 7
- zh-insurance: 3, 4, 5, 6
- zh-sick: 2, 4, 5, 6

The grader marks each LKP in each answer as one of:
- KEPT: the specific is stated with the key's limit in the same sentence or step.
- FLAT: stated without that limit, or as a fixed rule or certain outcome the key does not support (a maximum as a fixed date, an open fact assumed, a safe pick as the rule, ≈0 as 0).
- WRONG: contradicts the key in another way.
- ABSENT: not addressed.

METRICS PER 12 ANSWERS
From the grader:
- F = FLAT + WRONG on LKP; K = KEPT on LKP.
- C, V, M, W = correct, vague, missing and wrong over all 91 key points.
- AW and AU = added specifics labelled wrong or unverified against the key.
- S = limit words the grader finds attached to facts the key gives as fixed.
- SP = safe-pick sentences that add a figure or reason not in the key.
- SR = safe-pick sentences with no actual rule beside them.
- PC = answers that correct the baited premise in their opening paragraph.

From tuning_check5.py, which imports visible_text and hedge_count from verdict4-amended.py:
- Lv = per-prompt visible length divided by the mean of plain r1 and r2 for that prompt. Lb = the same against base.
- H1, H2, H3 = hedge-list rates per 1000 characters, mean over answers.
- CD = condition-word density per 1000 visible characters, from frozen regexes: up to / at most / only if / unless / if; 最多 / 不超过 / 只有…才 / 除非 / 如果 / 若; 最大 / まで / なら / 限り; 최대 / 까지 / 라면 / 면.
- BL = lines that open with a conditional.
- WF = web_fetch calls.
- RD = runs whose reasoning quotes or applies the new sentence (regex hits, read by hand).

Notation: X̄b and X̄p are the base and plain means of r1 and r2. Xb_min and Xb_max are the lower and higher base run; Xp_max is the higher plain run.

PASS 1: check in this order; exactly one outcome applies
1. ABANDON now (no pass 2) if any of:
   - PC ≤ 10;
   - a run is still invalid after its rerun;
   - median Lv < 0.70;
   - M ≥ M̄b + 6.
2. "Moved" means F ≤ Fb_min − 1. Overshoot triggers:
   - O1: median Lv > 1.00 and median Lb > 1.05.
   - O2: S ≥ 3.
   - O3: CD > 1.5 × CD̄b, or BL > 1.5 × BL̄b.
   - O4: K − K̄b < 0.5 × (F̄b − F), or V > V̄p + 2, or M > M̄p.
   - O5: H1 > H1b_max, or H2 > H2b_max, or H3 > H3b_max.
   - O6: AU > 1.10 × AUp_max, or SP ≥ 2, or SR ≥ 1.
3. Moved and no trigger: no revision. Pass 2 reruns the same text as a replicate.
4. Moved and any trigger: revision R-b (delete the parenthetical in all four languages). Pass 2 runs R-b.
5. Not moved, no trigger, and RD ≤ 2 (the sentence was not read): revision R-a (move the unchanged text to the end of item 7). Pass 2 runs R-a.
6. Not moved, and any trigger or RD ≥ 3 (read but ineffective, or harmful without effect): ABANDON.

PASS 2 decides GO or ABANDON
Scope:
- After outcome 3, pool both passes. Each c5 total is the sum over passes; each baseline is the sum over passes of that pass's mean; Fb_min is the lower of the two base runs' sums. Pass 2 alone must also show F ≤ F̄b.
- After outcome 4 or 5, judge pass 2 alone, which must also clear the trigger that caused the revision. For R-a, clearing the trigger means moved; for R-b, no O1 to O6.

GO needs all of G1 to G9 (24-answer pooled bound, with the 12-answer bound in brackets):
- G1: F ≤ F̄p (F ≤ F̄p + 1), and F ≤ Fb_min − 2 (F ≤ Fb_min − 1).
- G2: K − K̄b ≥ 0.5 × (F̄b − F).
- G3: C ≥ C̄p and C ≥ C̄b − 4 (C ≥ C̄b − 2); M ≤ M̄p; V ≤ V̄p; W ≤ W̄p + 1.
- G4: AW ≤ AW̄p (AW ≤ AWp_max); AU ≤ 1.10 × AŪp (AU ≤ 1.10 × AUp_max).
- G5: H1 ≤ 1.05 × H̄1p and H1 ≤ H̄1b; H2 ≤ max(H̄2b, 1.10 × H̄2p); H3 ≤ H̄3b.
- G6: median Lv between 0.80 and 1.00; median Lb ≤ 1.04; at most 1 prompt per 12 with Lv < 0.60; the en and ko median Lv each no more than base's own en and ko median plus 0.03.
- G7: every pass-2 answer corrects the premise, and at most 1 c5 answer misses it across both passes.
- G8: S ≤ 2 per 12 answers; SP ≤ 1 per 12 answers; SR = 0; CD ≤ 1.5 × CD̄b; BL ≤ 1.5 × BL̄b; unexcused source phrases (g11 rule) ≤ the base mean; WF ≥ 0.75 × WF̄b.
- G9: in each language, F ≤ F̄b, and M ≤ M̄p + 2.

If any of G1 to G9 fails: ABANDON. Report to Emily with every number, and spend no held-out runs on this change.

On GO: freeze (commit the c5 files and hashes, write freeze-start), give Emily the run count again, then run the 72 held-out runs. That is 12 new keyed prompts, 3 per language, × gv-plain, gv-grav-base and gv-grav-c5 × 2 runs, judged on both versions of WIN_CRITERIA.

Total DeepSeek runs: 24 + 72 = 96, leaving 325 of 421. Tuning alone uses 12 or 24.

## Abandon if

Abandon before any held-out run in any of these cases:
- **Pass 1:**
  - two or more c5 answers fail to correct the baited premise;
  - a tuning run is still invalid after its rerun;
  - the median visible length is below 0.70 of plain;
  - missing key points are at least base's mean plus 6;
  - the sentence did not move the target (flattened-or-wrong limited key points not at least 1 below both base runs) and either it was read (at least 3 of 12 runs quote or apply it) or any overshoot trigger fired. The triggers are length, spraying, conditional density, blur, any hedge list above base's higher run, unverified added claims, or safe-pick sentences adding figures or reasons.
- **Pass 2:** any of G1 to G9 fails. G1 to G9 cover:
  - the target (at or below plain's mean, and below both base runs by at least 2 pooled, or 1 if only pass 2 counts);
  - reductions landing as kept rather than vague;
  - correct, missing, vague and wrong key points against plain;
  - wrong and unverified added claims against plain;
  - the three hedge lists;
  - length between 0.80 and 1.00 of plain and no more than 1.04 of base;
  - premise corrections;
  - the guards against spraying, safe picks, conditionals, sources and fetching;
  - per-language checks on the target and on missing key points.
- **Revision:** a revision does not clear the trigger that caused it.

Either way, report to Emily and spend none of the 72 held-out runs.
