# One unapproved plain run, 2026-10-24 12:55-12:57 (+11:00)

While testing run.sh's freeze guard I meant to put a stand-in dsh first on PATH, but I wrote the folder
as C:/..., and the colon split the PATH entry, so the real dsh stayed first. The test recorded a
freeze-start and the guard then passed, as it should, and run.sh started a real gv-plain run of the
held-out prompt zh-sick-pay (round 9, out of schedule). I killed it after about 2.5 minutes:
16 model steps finished, 406242 tokens in total (sum of per-step totals), no final answer.

- It counts as one run against the 500-run budget.
- I did not read its answer (there was none) and changed nothing because of it. zh-sick-pay stays in
  the held-out set; dropping it now would be a choice made after seeing a run.
- Nothing from it is graded. The freeze-start the test wrote is kept here as freeze-start.test.txt;
  the real freeze-start is recorded later.
- Fix: the guard test now resolves the stand-in with cygpath -u and refuses to go on unless
  command -v dsh is the stand-in.
