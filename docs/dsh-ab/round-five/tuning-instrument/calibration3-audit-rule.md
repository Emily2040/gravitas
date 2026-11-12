# Calibration 3 acceptance: flip audit (written 2026-10-26, before calibration 3 is built or graded)

Calibration 2 passed, but a review found that the rubric it used (sha256 f9fc3530…) marked a deferred specific KEPT
and listed "no later than" as stating a maximum. The rubric is being fixed again and calibration 3 is the last
calibration slot. Calibration 3 counts only if both hold:

1. tuning_check5.py --calibration calibration3 prints CALIBRATION PASSED.
2. A hand audit, by an agent that wrote neither the rubric nor the change, of every limited key point that calibration 1
   marked FLAT and calibration 3 marks KEPT (same answer, same key point; matched through the two id maps), finds no flip
   where calibration 3's KEPT quote
   - gives the person a maximum as their deadline or a fixed date or amount ("by day 30", "through March 15",
     "no later than April 15"), with no shorter-limit or condition in the same sentence or step; or
   - defers or omits the specific with no maximum, condition, window or open fact stated ("ask your plan for the date").
   Any such flip means the rubric is wrong. Then no tuning pass runs until the instrument is fixed and Emily is told.

The audit lists every flip with both quotes and its finding, and is saved as calibration3-flip-audit.md beside this file.
