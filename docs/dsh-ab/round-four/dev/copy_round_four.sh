#!/bin/sh
# Copy everything round four runs and grades with into the worktree, same relative paths, before freeze-start.
# Run again after any change; it mirrors (stale files in the target are removed first).
set -e
B=/w/AgentData/logs/gravitas-dsh-ab4
T=/w/Projects/gravitas-claim-check/docs/dsh-ab/round-four
cd $B
files="run.sh runall.sh freeze.sh schedule.txt tuning-schedule.txt expected-rule-hashes.json tuning_check.py
  rules/change4/*.md rules/change4-before-tuning/* overlays/*.yml prompts/*.txt keys/* keypoints/* sources/* reserve/* probe/* probe2/* tuning/* tuning-decision-rule.txt tuning-check.txt tuning-validity.txt freeze-start.superseded-1.txt
  make_pairs4.py validity4.py verdict4.py verdict4-amended.py build_notes4.py save_labels4.py save_grades4.py
  judge_codex.sh mutation4.py workflows/*.js grader-prompt4.md verdict4-README.md verdict4-amended-README.md
  review/* mutation/mutation-report.txt audit-audit-gravitas.json audit-challenge-gravitas.json
  incidents/2026-10-24-guard-test/NOTE.md incidents/2026-10-24-guard-test/freeze-start.test.txt
  incidents/2026-10-24-guard-test/zh-sick-pay.gv-plain.r9.ndjson incidents/2026-10-24-guard-test/zh-sick-pay.gv-plain.r9.err"
extra=$(ls *schema*.json preverdict4.py 2>/dev/null || true)
for d in rules overlays prompts keys keypoints sources reserve probe probe2 tuning workflows review mutation incidents; do rm -rf "$T/$d"; done
mkdir -p $T
n=0
for f in $files $extra; do
  [ -f "$f" ] || { echo "MISSING $f"; exit 1; }
  mkdir -p "$T/$(dirname $f)"; cp -p "$f" "$T/$f"; n=$((n+1))
done
echo "copied $n files to $T"
# every file freeze.sh hashes from the round folder must be in the copy, byte for byte
( cd $B && sh freeze.sh --state ) | awk 'NF==2 && $1 ~ /^[0-9a-f]{64}$/ {print $2}' | while read f; do
  [ -f "$B/$f" ] || continue
  [ -f "$T/$f" ] && cmp -s "$B/$f" "$T/$f" && continue
  case "$f" in dsh/*|dist/*|docs/*|gv-*) continue ;; esac
  echo "NOT COPIED or differs: $f"
done
