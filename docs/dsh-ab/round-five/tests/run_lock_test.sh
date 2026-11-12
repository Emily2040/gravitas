#!/usr/bin/env bash
# run_lock_test.sh: test run.sh's lock check, freeze.sh's lock-override record, run.sh's tuning-pass checks and
# rerun cap, and what freeze.sh hashes for tuning (the instrument, the decision rule, round four's files).
#
#   bash tests/run_lock_test.sh
#
# Never touches W:\AgentData\dsh_home: every run.sh call sets RUN_LOCK_TEST to a lock file made here, and freeze.sh
# itself is never run (its lock-override line and its two hash blocks are taken out and run on their own; the
# round-folder block runs in a temporary folder of copies, so round five's held-out files are never read). No run
# reaches dsh: the real run.sh always stops at "no freeze-start.txt" (round five has none, and this test never
# creates one there), and the copy used for the tuning checks has its round folder moved to a temporary folder with
# a stub freeze.sh, and every case there is refused before the run starts. Everything is written under tests/ and
# removed at the end.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROUND="$(dirname "$HERE")"
T="$HERE/.tmp-run-lock-$$"
mkdir -p "$T"
trap 'rm -rf "$T"' EXIT
pass=0; fail=0
ok() { if [ "$1" = 0 ]; then pass=$((pass + 1)); echo "[ok]  $2"; else fail=$((fail + 1)); echo "[BAD] $2${3:+  -- $3}"; fi; }
has() { printf '%s' "$1" | grep -qF -- "$2" && echo 0 || echo 1; }

[ -e "$ROUND/freeze-start.txt" ] && { echo "round five already has freeze-start.txt; this test only runs before the freeze"; exit 2; }
before="$(ls -A "$ROUND" | sort)"

# ---- 1. the lock check in the real run.sh (stops at the next check, "no freeze-start.txt", when the lock is right)
lockrun() {  # lockrun <lock path>; prints run.sh's output and its exit code
  out=$(RUN_LOCK_TEST="$1" sh "$ROUND/run.sh" gv-grav-c5 zh-x 1 2>&1); echo "$out | exit $?"
}
r=$(lockrun "$T/none.LOCK")
ok $(has "$r" "REFUSED: no lock file $T/none.LOCK | exit 3") "lock missing: refused" "$r"
printf '' > "$T/empty.LOCK"
r=$(lockrun "$T/empty.LOCK")
ok $(has "$r" "first line is not 'owner: dsh-round5' | exit 3") "empty lock: refused" "$r"
printf 'owner: dsh-round4\n' > "$T/other.LOCK"
r=$(lockrun "$T/other.LOCK")
ok $(has "$r" "first line is not 'owner: dsh-round5' | exit 3") "lock owned by another session: refused" "$r"
printf 'owner: dsh-round5 \n' > "$T/space.LOCK"
r=$(lockrun "$T/space.LOCK")
ok $(has "$r" "first line is not 'owner: dsh-round5' | exit 3") "first line with a trailing space: refused" "$r"
printf 'owner: dsh-round5x\n' > "$T/longer.LOCK"
r=$(lockrun "$T/longer.LOCK")
ok $(has "$r" "first line is not 'owner: dsh-round5' | exit 3") "first line longer than the owner: refused" "$r"
printf 'note\nowner: dsh-round5\n' > "$T/second.LOCK"
r=$(lockrun "$T/second.LOCK")
ok $(has "$r" "first line is not 'owner: dsh-round5' | exit 3") "owner on the second line only: refused" "$r"
mkdir -p "$T/dir.LOCK"
r=$(lockrun "$T/dir.LOCK")
ok $(has "$r" "REFUSED: no lock file" ) "a folder named like the lock: refused" "$r"
printf 'owner: dsh-round5\n' > "$T/good.LOCK"
r=$(lockrun "$T/good.LOCK")
ok $(has "$r" "REFUSED: no freeze-start.txt | exit 3") "right lock: passes the lock check (stops at the freeze check)" "$r"
printf 'owner: dsh-round5' > "$T/nonl.LOCK"
r=$(lockrun "$T/nonl.LOCK")
ok $(has "$r" "REFUSED: no freeze-start.txt | exit 3") "right lock without a final newline: passes" "$r"
printf 'owner: dsh-round5\r\nsince 2026-10-26\r\n' > "$T/crlf.LOCK"
r=$(lockrun "$T/crlf.LOCK")
ok $(has "$r" "REFUSED: no freeze-start.txt | exit 3") "right lock with CRLF line ends and a second line: passes" "$r"
ok $([ "$(ls -A "$ROUND" | sort)" = "$before" ] && echo 0 || echo 1) "the real run.sh calls left nothing in the round folder"
ok $(grep -q 'RUN_LOCK_TEST.*MUST be unset in' "$ROUND/run.sh" && echo 0 || echo 1) "run.sh's header says RUN_LOCK_TEST must be unset in real runs"

# ---- 2. freeze.sh records whether RUN_LOCK_TEST is set
line="$(grep '^  echo "lock-override: ' "$ROUND/freeze.sh")"
ok $([ -n "$line" ] && echo 0 || echo 1) "freeze.sh has a lock-override line in its state"
ok $(grep -q 'state() {' "$ROUND/freeze.sh" && awk '/^state\(\) \{/,/^\}/' "$ROUND/freeze.sh" | grep -q 'lock-override' && echo 0 || echo 1) "the line is inside state() (so --state and freeze-start both carry it)"
ok $([ "$(env -u RUN_LOCK_TEST sh -c "$line")" = "lock-override: unset" ] && echo 0 || echo 1) "unset -> 'lock-override: unset'"
ok $([ "$(RUN_LOCK_TEST="$T/good.LOCK" sh -c "$line")" = "lock-override: set" ] && echo 0 || echo 1) "set -> 'lock-override: set'"
ok $([ "$(RUN_LOCK_TEST= sh -c "$line")" = "lock-override: set" ] && echo 0 || echo 1) "set but empty -> 'lock-override: set'"

# ---- 3. a copy of run.sh in a temporary round folder: the freeze comparison and the tuning-pass checks
F="$T/round"; mkdir -p "$F/tuning" "$F/prompts"
sed "s#^B=/w/AgentData/logs/gravitas-dsh-ab5\$#B=$F#" "$ROUND/run.sh" > "$F/run.sh"
ok $([ "$(diff "$ROUND/run.sh" "$F/run.sh" | grep -c '^[<>]')" = 2 ] && echo 0 || echo 1) "the copy differs from run.sh in its round folder only"
{ echo '#!/bin/sh'; echo 'echo "head: stub"'; echo 'echo "link: W:\\Projects\\gravitas-round5"'; echo "$line"; } > "$F/freeze.sh"
{ echo "label: start"; echo "time: now"; env -u RUN_LOCK_TEST sh "$F/freeze.sh" --state; } > "$F/freeze-start.txt"
cprun() { out=$(RUN_LOCK_TEST="$T/good.LOCK" sh "$F/run.sh" "$@" 2>&1); echo "$out | exit $?"; }
R4P=/w/AgentData/logs/gravitas-dsh-ab4/prompts
r=$(cprun gv-grav-c5 en-529-roth 1 "$R4P" "$F/tuning")
ok $(has "$r" "state differs from freeze-start") "freeze-start recorded without RUN_LOCK_TEST: a run with it set is refused by the freeze comparison" "$r"
ok $(has "$r" "> lock-override: set") "the refusal shows the lock-override line" "$r"
{ echo "label: start"; echo "time: now"; RUN_LOCK_TEST=x sh "$F/freeze.sh" --state; } > "$F/freeze-start.txt"
r=$(cprun gv-plain en-529-roth 1 "$R4P" "$F/tuning")
ok $(has "$r" "REFUSED: tuning runs gv-grav-c5 only | exit 3") "tuning: gv-plain refused" "$r"
r=$(cprun gv-grav-base en-529-roth 1 "$R4P" "$F/tuning")
ok $(has "$r" "REFUSED: tuning runs gv-grav-c5 only | exit 3") "tuning: gv-grav-base refused" "$r"
r=$(cprun gv-grav-c5 en-529-roth 3 "$R4P" "$F/tuning")
ok $(has "$r" "tuning has passes 1 and 2 only (round 3) | exit 3") "tuning: round 3 refused" "$r"
r=$(cprun gv-grav-c5 en-529-roth 1 "$F/prompts" "$F/tuning")
ok $(has "$r" "tuning runs read round four's prompts only | exit 3") "tuning: another prompt folder refused" "$r"
r=$(cprun gv-grav-c5 en-529-roth 1 /w/AgentData/logs/gravitas-dsh-ab3/prompts "$F/tuning")
ok $(has "$r" "tuning runs read round four's prompts only | exit 3") "tuning: round three's prompt folder refused" "$r"
mkdir -p "$F/raw"; : > "$F/raw/x.ndjson"
r=$(cprun gv-grav-c5 en-529-roth 1 "$R4P" "$F/tuning")
ok $(has "$r" "raw/ already has runs | exit 3") "tuning after a held-out run exists: refused" "$r"
rm -rf "$F/raw"
: > "$F/tuning/en-529-roth.gv-grav-c5.r2.exit"
r=$(cprun gv-grav-c5 en-529-roth 2 "$R4P" "$F/tuning")
ok $(has "$r" "only a run validity5.py archived for its one rerun may run again | exit 3") "tuning pass 2: an existing run is not overwritten" "$r"
mkdir -p "$F/tuning/attempt1"; : > "$F/tuning/attempt1/en-529-roth.gv-grav-c5.r2.ndjson"
echo "gv-grav-c5 en-529-roth 2" > "$F/rerun-schedule-tuning-1.txt"
r=$(cprun gv-grav-c5 en-529-roth 2 "$R4P" "$F/tuning")
ok $(has "$r" "only a run validity5.py archived for its one rerun may run again | exit 3") "tuning pass 2: a rerun listed for pass 1 does not count" "$r"
echo "gv-grav-c5 en-529-roth 2" > "$F/rerun-schedule-tuning-2.txt"
r=$(cprun gv-grav-c5 en-529-roth 2 "$R4P" "$F/tuning")
ok $(has "$r" "exists although it was archived for a rerun; move it to attempt1 first | exit 3") "tuning pass 2: the pass-2 rerun list is the one read" "$r"
rm -f "$F/tuning/en-529-roth.gv-grav-c5.r2.exit" "$F/rerun-schedule-tuning-2.txt"
r=$(cprun gv-grav-c5 en-529-roth 2 "$R4P" "$F/tuning")
ok $(has "$r" "an archived attempt exists but the run is not in rerun-schedule.txt | exit 3") "tuning pass 2: an archived attempt without a pass-2 listing is refused" "$r"
# The rerun cap: more than 2 archived runs in a tuning pass, or more than 8 in the round (tuning and held-out
# together), is refused with "stop and ask Emily". Every case keeps the run's own .exit file, so a case that passes
# the cap is refused by the next check ("move it to attempt1 first"), and a run.sh without the cap starts no run either.
echo "gv-grav-c5 en-529-roth 2" > "$F/rerun-schedule-tuning-2.txt"
: > "$F/tuning/en-529-roth.gv-grav-c5.r2.exit"
: > "$F/tuning/attempt1/en-fsa-rollover.gv-grav-c5.r2.ndjson"
r=$(cprun gv-grav-c5 en-529-roth 2 "$R4P" "$F/tuning")
ok $(has "$r" "move it to attempt1 first | exit 3") "rerun cap: 2 archived runs in tuning pass 2 pass the cap" "$r"
: > "$F/tuning/attempt1/en-medicare-part-b.gv-grav-c5.r2.ndjson"
r=$(cprun gv-grav-c5 en-529-roth 2 "$R4P" "$F/tuning")
ok $(has "$r" "REFUSED: 3 runs of tuning pass 2 archived as invalid, more than 2 in a pass: stop and ask Emily | exit 3") "rerun cap: 3 archived runs in tuning pass 2: refused" "$r"
rm -f "$F/tuning/attempt1/en-medicare-part-b.gv-grav-c5.r2.ndjson"
for k in ja-medical-deduction ja-part-time-leave ja-wallpaper-restoration; do : > "$F/tuning/attempt1/$k.gv-grav-c5.r1.ndjson"; done
r=$(cprun gv-grav-c5 en-529-roth 2 "$R4P" "$F/tuning")
ok $(has "$r" "move it to attempt1 first | exit 3") "rerun cap: pass 1's 3 archived runs do not count against pass 2" "$r"
echo "gv-grav-c5 ja-part-time-leave 1" > "$F/rerun-schedule-tuning-1.txt"
: > "$F/tuning/ja-part-time-leave.gv-grav-c5.r1.exit"
r=$(cprun gv-grav-c5 ja-part-time-leave 1 "$R4P" "$F/tuning")
ok $(has "$r" "REFUSED: 3 runs of tuning pass 1 archived as invalid, more than 2 in a pass: stop and ask Emily | exit 3") "rerun cap: 3 archived runs in tuning pass 1: refused" "$r"
# held-out: 5 archived in tuning/attempt1 so far; 3 more in raw/attempt1 make 8 (allowed), a fourth makes 9 (refused)
mkdir -p "$F/raw/attempt1"; : > "$F/prompts/zh-test-case.txt"
echo "gv-plain zh-test-case 1" > "$F/rerun-schedule.txt"
: > "$F/raw/zh-test-case.gv-plain.r1.exit"
for k in zh-test-case zh-test-b zh-test-c; do : > "$F/raw/attempt1/$k.gv-plain.r1.ndjson"; done
r=$(cprun gv-plain zh-test-case 1 "$F/prompts" "$F/raw")
ok $(has "$r" "move it to attempt1 first | exit 3") "rerun cap: 8 archived runs in the round (5 tuning, 3 held-out) pass the cap" "$r"
: > "$F/raw/attempt1/zh-test-d.gv-plain.r1.ndjson"
r=$(cprun gv-plain zh-test-case 1 "$F/prompts" "$F/raw")
ok $(has "$r" "REFUSED: 9 runs archived for a rerun, past the 8 reruns approved: stop and ask Emily | exit 3") "rerun cap: 9 archived runs in the round (5 tuning, 4 held-out): refused" "$r"
: > "$F/raw/zh-test-e.gv-plain.r1.exit"; : > "$F/prompts/zh-test-e.txt"
r=$(cprun gv-plain zh-test-e 1 "$F/prompts" "$F/raw")
ok $(has "$r" "only a run validity5.py archived for its one rerun may run again | exit 3") "rerun cap: counted for reruns only (a run with no archived attempt meets the usual check)" "$r"
rm -f "$F/tuning/en-529-roth.gv-grav-c5.r2.exit" "$F/tuning/ja-part-time-leave.gv-grav-c5.r1.exit"
ok $([ ! -e "$F/run-ledger.tsv" ] && [ -z "$(ls "$F/tuning" | grep -v attempt1)" ] && [ -z "$(ls "$F/raw" | grep -v -e attempt1 -e '\.exit$')" ] && echo 0 || echo 1) "no refused case started a run or wrote a ledger line"
rm -rf "$F/raw"

# ---- 4. freeze.sh hashes the tuning instrument, the decision rule and round four's files that tuning reads
# Only freeze.sh's two hash blocks are taken out and run: the round-folder block in a temporary folder of copies (so
# it never reads round five's held-out files), and round four's block as it is (it reads round four's folder only).
blk="$(awk '/^  \( cd \$B && sha256sum/,/\) \)$/' "$ROUND/freeze.sh")"
ok $([ -n "$blk" ] && awk '/^state\(\) \{/,/^\}/' "$ROUND/freeze.sh" | grep -qF 'tuning-instrument/tuning_check5.py' && echo 0 || echo 1) "freeze.sh's round-folder hash block is inside state() and names the instrument"
words="$(printf '%s' "$blk" | tr ' \\' '\n\n')"
INSTF="tuning_check5.py tuning_common5.py save_tuning_grades5.py make_tuning_grade_script.py lkp.json premise-points.json tuning-grade-schema5.json tuning-grader-prompt5.md"
for f in $INSTF; do
  ok $(printf '%s\n' "$words" | grep -qx "tuning-instrument/$f" && echo 0 || echo 1) "freeze.sh hashes tuning-instrument/$f"
done
ok $(printf '%s\n' "$words" | grep -qx "design/tuning-decision-rule.md" && echo 0 || echo 1) "freeze.sh hashes design/tuning-decision-rule.md"
ok $(printf '%s\n' "$words" | grep -q '^tuning-instrument/.*[*?[]' && echo 1 || echo 0) "no glob over tuning-instrument/ (grades, decisions and calibrations are written there)"
FZ="$T/fz"; mkdir -p "$FZ/tuning-instrument" "$FZ/design"
for f in $INSTF; do cp "$ROUND/tuning-instrument/$f" "$FZ/tuning-instrument/$f"; done
cp "$ROUND/design/tuning-decision-rule.md" "$FZ/design/"
fzstate() { B="$FZ" sh -c "$blk" 2>/dev/null; }
s1="$(fzstate)"
ok $([ "$(printf '%s\n' "$s1" | grep -c -e ' \*tuning-instrument/' -e ' \*design/tuning-decision-rule.md$')" = 9 ] && echo 0 || echo 1) "the block gives 9 instrument and rule lines" "$s1"
for f in grades-pass1.json decision-pass1.json calibration-calibration.json rd-hand-pass1.json ledger5.jsonl; do echo '{}' > "$FZ/tuning-instrument/$f"; done
ok $([ "$(fzstate)" = "$s1" ] && echo 0 || echo 1) "files tuning writes into tuning-instrument/ leave the state unchanged"
printf '\n# a changed bound\n' >> "$FZ/tuning-instrument/tuning_check5.py"
d="$(diff <(printf '%s\n' "$s1") <(fzstate) | grep '^>' )"
ok $(has "$d" "tuning-instrument/tuning_check5.py") "an edit to tuning_check5.py changes the state (run.sh would refuse)" "$d"
cp "$ROUND/tuning-instrument/tuning_check5.py" "$FZ/tuning-instrument/"
printf ' ' >> "$FZ/tuning-instrument/lkp.json"
d="$(diff <(printf '%s\n' "$s1") <(fzstate) | grep '^>' )"
ok $(has "$d" "tuning-instrument/lkp.json") "an edit to lkp.json changes the state" "$d"
printf '\n' >> "$FZ/design/tuning-decision-rule.md"
d="$(diff <(printf '%s\n' "$s1") <(fzstate) | grep '^>' )"
ok $(has "$d" "design/tuning-decision-rule.md") "an edit to the decision rule changes the state" "$d"
b4="$(awk '/^  \( cd \/w\/AgentData\/logs && sha256sum/,/\)$/' "$ROUND/freeze.sh")"
ok $([ -n "$b4" ] && awk '/^state\(\) \{/,/^\}/' "$ROUND/freeze.sh" | grep -qF 'gravitas-dsh-ab4/prompts/*.txt' && echo 0 || echo 1) "freeze.sh has round four's hash block inside state()"
s4="$(sh -c "$b4" 2>&1)"
ok $([ "$(printf '%s\n' "$s4" | grep -c ' \*gravitas-dsh-ab4/prompts/.*\.txt$')" = 12 ] && echo 0 || echo 1) "round four's 12 prompts are hashed" "$s4"
ok $([ "$(printf '%s\n' "$s4" | grep -c ' \*gravitas-dsh-ab4/keys/.*\.md$')" = 12 ] && [ "$(printf '%s\n' "$s4" | grep -c ' \*gravitas-dsh-ab4/keypoints/.*\.json$')" = 12 ] && echo 0 || echo 1) "round four's 12 keys and 12 key-point files are hashed"
ok $([ "$(printf '%s\n' "$s4" | grep -cE ' \*gravitas-dsh-ab4/raw/[^.]+\.gv-(plain|grav-base)\.r[12]\.(txt|ndjson)$')" = 96 ] && [ "$(printf '%s\n' "$s4" | wc -l)" = 132 ] && echo 0 || echo 1) "the 48 baseline answers (final and stream) are hashed, and nothing else"
miss=""; for c in $(awk '{print $2}' "$ROUND/tuning-schedule-1.txt" "$ROUND/tuning-schedule-2.txt" | sort -u); do
  printf '%s\n' "$s4" | grep -q " \*gravitas-dsh-ab4/prompts/$c\.txt$" || miss="$miss $c"; done
ok $([ -z "$miss" ] && echo 0 || echo 1) "every tuning-schedule case's prompt is among them" "$miss"
ok $(grep -qx 'R4P=/w/AgentData/logs/gravitas-dsh-ab4/prompts' "$ROUND/run.sh" && echo 0 || echo 1) "run.sh's tuning prompt folder is the one hashed"

echo "run.sh lock and tuning test: $((pass + fail)) assertions, $fail failed"
[ "$fail" = 0 ]
