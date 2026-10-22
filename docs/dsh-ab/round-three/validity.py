"""Check every round-three run against the validity rules in criteria.md (amendments).

    python validity.py   -> prints a report, writes validity.json; exit 1 if any run is invalid

Invalid (harness failure, rerun once before grading): missing or empty final text, non-zero exit,
a gv-grav run with no draft record, a steered gv-grav run with no revision record, more than one
steer in a turn, or any claim-log record from gv-plain or gv-grav-nocheck.
Reported, graded as is: steered runs whose final is under half the draft, equals the draft, or
carries meta wording; meta wording in any final answer.
"""
import json
import os
import re
import sys

B = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(B, "raw")
META = re.compile(r"Gravitas|核对|修改后|修订|重新给出|已删除|其余不变|revised|updated reply|I removed|this check|as above", re.I)

runs = [l.split() for l in open(os.path.join(B, "schedule.txt"), encoding="utf-8") if l.strip()]
exits = {}
for line in open(os.path.join(B, "run.log"), encoding="utf-8"):
    m = re.match(r"(\S+) (\S+) r(\d) exit=(\d+)", line)
    if m:
        exits[(m.group(2), m.group(1), m.group(3))] = int(m.group(4))  # last attempt wins

report = {"invalid": [], "flagged": [], "runs": {}}
for arm, case, rnd in runs:
    stem = os.path.join(RAW, "%s.%s.r%s" % (case, arm, rnd))
    info = {"exit": exits.get((arm, case, rnd))}
    problems, notes = [], []
    final = open(stem + ".txt", encoding="utf-8").read().strip() if os.path.exists(stem + ".txt") else ""
    info["chars"] = len(final)
    if info["exit"] != 0:
        problems.append("exit %s" % info["exit"])
    if not final:
        problems.append("empty final")
    log = stem + ".claims.jsonl"
    recs = [json.loads(l) for l in open(log, encoding="utf-8") if l.strip()] if os.path.exists(log) else []
    if arm == "gv-grav":
        drafts = [r for r in recs if r["phase"] == "draft"]
        revs = [r for r in recs if r["phase"] == "revision"]
        steered = [r for r in drafts if r["steered"]]
        info.update(drafts=len(drafts), steered=len(steered), revisions=len(revs),
                    listed=[len(r["flagged"]) for r in drafts], left=[len(r["flagged"]) for r in revs])
        if not drafts:
            problems.append("no draft record")
        if len(steered) > len({r["turn"] for r in steered}):
            problems.append("more than one steer in a turn")
        if steered and not revs:
            problems.append("steered without a revision record")
        if steered:
            draft = steered[0]["text"].strip()
            if final == draft:
                notes.append("final equals the draft")
            elif len(final) < 0.5 * len(draft):
                notes.append("final under half the draft (%d of %d chars)" % (len(final), len(draft)))
    elif recs:
        problems.append("claim-log records from %s" % arm)
    if META.search(final):
        notes.append("meta wording: %s" % META.search(final).group(0))
    info["problems"], info["notes"] = problems, notes
    key = "%s.%s.r%s" % (case, arm, rnd)
    report["runs"][key] = info
    if problems:
        report["invalid"].append(key)
    if notes:
        report["flagged"].append(key)
    print("%-42s %s%s%s" % (key, "INVALID " + "; ".join(problems) if problems else "ok",
                            "  | " + "; ".join(notes) if notes else "",
                            "  | listed %s left %s" % (info.get("listed"), info.get("left")) if arm == "gv-grav" else ""))
with open(os.path.join(B, "validity.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(report, fh, indent=1, ensure_ascii=False)
print("%d runs, %d invalid, %d flagged" % (len(runs), len(report["invalid"]), len(report["flagged"])))
sys.exit(1 if report["invalid"] else 0)
