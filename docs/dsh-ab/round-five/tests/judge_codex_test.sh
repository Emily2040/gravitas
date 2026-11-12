#!/usr/bin/env bash
# judge_codex_test.sh: stand-in test of judge_codex.sh's guard and of the worker fix (round five).
#
#   bash tests/judge_codex_test.sh [path/to/judge_codex.sh]     default: ../judge_codex.sh beside this folder
#
# No real Codex call is ever made. Every run below puts a stand-in `codex` first on PATH, and every run in approved
# mode also sets CODEX_APPROVED_STANDIN, so judge_codex.sh's guard (in the parent and in every worker) aborts before
# touching codex unless `command -v codex` is that stand-in. The stand-in answers --version with codex-cli 0.163.0,
# logs each call with its arguments, and writes a valid grade to the -o path.
#
# What it proves:
#  A. a run started with --approved reaches the codex call in every worker (round four's main loop started workers
#     without --approved, the worker's guard refused, and no grade was ever made);
#  B. the same test FAILS on round four's worker start: a copy of judge_codex.sh with only that line put back
#     makes no codex call and exits non-zero (so A is not passing by accident);
#  C. the refusals stay: neither --approved nor CODEX_STANDIN refuses; CODEX_APPROVED_STANDIN without --approved
#     refuses; --approved with CODEX_STANDIN refuses; an approved-path test whose PATH does not resolve codex to the
#     stand-in aborts; none of them calls codex;
#  D. the stand-in test mode (CODEX_STANDIN) still grades every pair.
# Everything is written to a temporary folder under tests/ that is removed at the end. Exit 0 only if every
# assertion holds. Standard tools only (bash, sed, grep, python for save_grades5.py).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROUND="$(dirname "$HERE")"
J="${1:-$ROUND/judge_codex.sh}"
T="$HERE/.tmp-judge-codex-$$"
mkdir -p "$T/tmp"
export TMPDIR="$T/tmp"
trap 'rm -rf "$T"' EXIT
pass=0; fail=0
ok() { if [ "$1" = 0 ]; then pass=$((pass + 1)); echo "[ok]  $2"; else fail=$((fail + 1)); echo "[BAD] $2${3:+  -- $3}"; fi; }

# ---- the stand-in codex (and a second one that must never be reached in test 6)
mkbin() {  # mkbin <dir>
  mkdir -p "$1"
  cat > "$1/codex" <<'EOF'
#!/usr/bin/env bash
here="$(cd "$(dirname "$0")" && pwd)"
if [ "${1:-}" = "--version" ]; then echo "codex-cli 0.163.0"; exit 0; fi
out=""; prev=""
for a in "$@"; do [ "$prev" = "-o" ] && out="$a"; prev="$a"; done
cat > /dev/null
pid="$(printf '%s' "$out" | sed 's#.*[\\/]##; s#\.json$##')"
printf '%s %s\n' "$pid" "$*" >> "$here/calls.log"
side='{"correct": 8, "trap": 9, "honest": 8, "useful": 8, "concise": 7, "added_claim_errors": [], "key_points": {"1": "correct", "2": "vague"}}'
printf '{"pair": "%s", "winner": "A", "margin": "clear", "A": %s, "B": %s, "reasons": "stand-in grade"}\n' \
  "$pid" "$side" "$side" > "$(cygpath -u "$out")"
EOF
  chmod +x "$1/codex"
}
mkbin "$T/bin"
mkbin "$T/other"

# ---- a two-pair round folder
mkround() {  # mkround <dir>
  mkdir -p "$1/blind/packets" "$1/keypoints"
  printf '{"p001": {"set": "main", "case": "zh-x", "round": "r1", "A": "gv-grav-c5", "B": "gv-plain"},\n' > "$1/blind-map.json"
  printf ' "p002": {"set": "main", "case": "zh-x", "round": "r2", "A": "gv-plain", "B": "gv-grav-c5"}}\n' >> "$1/blind-map.json"
  printf '[{"id": "1", "point": "a"}, {"id": "2", "point": "b"}]\n' > "$1/keypoints/zh-x.json"
  for p in p001 p002; do printf '# PAIR %s\n\npacket text\n' "$p" > "$1/blind/packets/$p.md"; done
}
calls() { [ -f "$1/calls.log" ] && grep -c . "$1/calls.log" || echo 0; }
valid_codex() {  # number of valid codex grade entries in the ledger of round folder $1
  [ -f "$1/ledger.jsonl" ] || { echo 0; return; }
  python -c 'import json,sys; print(sum(1 for l in open(sys.argv[1], encoding="utf-8") if l.strip() and json.loads(l).get("judge") == "codex" and json.loads(l).get("valid") is True))' "$(cygpath -w "$1/ledger.jsonl")"
}

# ---- A. approved path, fixed script
mkround "$T/rA"
out=$(env -u CODEX_STANDIN CODEX_APPROVED_STANDIN="$T/bin" PATH="$T/bin:$PATH" B="$T/rA" bash "$J" --approved 2>&1); code=$?
ok $([ "$code" = 0 ] && echo 0 || echo 1) "A: --approved run exits 0" "exit $code: $(printf '%s' "$out" | tail -n 2 | tr '\n' ' ')"
n=$(calls "$T/bin")
ok $([ "$n" = 2 ] && echo 0 || echo 1) "A: every worker started in approved mode reached the codex call (2 of 2 pairs)" "$n calls"
ok $([ "$(valid_codex "$T/rA")" = 2 ] && echo 0 || echo 1) "A: both grades recorded valid in the ledger" "$(valid_codex "$T/rA") valid"
ok $(grep -q 'REAL, approved (approved-path test' "$T/rA/judge-codex.log" && echo 0 || echo 1) "A: the log marks the run approved, as an approved-path test"
ok $([ "$(grep -c 'end exit=0 .* grade valid, in force' "$T/rA/judge-codex.log")" = 2 ] && echo 0 || echo 1) "A: both worker sessions logged end exit=0, valid"
ok $(grep -q -- '--search exec -m gpt-6-astra -c model_reasoning_effort="high" -s read-only --skip-git-repo-check --ephemeral --output-schema ' "$T/bin/calls.log" 2>/dev/null && echo 0 || echo 1) \
   "A: the codex call carries the frozen model, effort, sandbox and flags"
ok $(! printf '%s' "$out" | grep -q REFUSED && echo 0 || echo 1) "A: no worker refused"
rm -f "$T/bin/calls.log"

# ---- B. the same test on round four's worker start (only that line put back) must fail
mkdir -p "$T/old"
cp "$ROUND/save_grades5.py" "$ROUND/grader-prompt5.md" "$T/old/"
sed 's#xargs -P "$JOBS" -I{} bash "$SELF" $WFLAG --one {}#xargs -P "$JOBS" -I{} bash "$SELF" --one {}#' "$J" > "$T/old/judge_codex.sh"
ok $([ "$(diff "$J" "$T/old/judge_codex.sh" | grep -c '^[<>]')" = 2 ] && echo 0 || echo 1) "B: the old copy differs from the fixed script in the worker start line only"
mkround "$T/rB"
out=$(env -u CODEX_STANDIN CODEX_APPROVED_STANDIN="$T/bin" PATH="$T/bin:$PATH" B="$T/rB" bash "$T/old/judge_codex.sh" --approved 2>&1); code=$?
ok $([ "$code" != 0 ] && echo 0 || echo 1) "B: with round four's worker start the approved run fails" "exit $code"
ok $([ "$(calls "$T/bin")" = 0 ] && echo 0 || echo 1) "B: with round four's worker start no worker reaches the codex call" "$(calls "$T/bin") calls"
ok $([ "$(printf '%s' "$out" | grep -c 'REFUSED: real Codex calls')" = 2 ] && echo 0 || echo 1) "B: both workers refused in their own guard"
rm -f "$T/bin/calls.log"

# ---- C. refusals
mkround "$T/rC"
out=$(env -u CODEX_STANDIN -u CODEX_APPROVED_STANDIN PATH="$T/bin:$PATH" B="$T/rC" bash "$J" 2>&1); code=$?
ok $([ "$code" = 3 ] && printf '%s' "$out" | grep -q 'REFUSED: real Codex calls' && echo 0 || echo 1) "C1: neither --approved nor CODEX_STANDIN: refused (exit 3)" "exit $code"
out=$(CODEX_APPROVED_STANDIN="$T/bin" PATH="$T/bin:$PATH" B="$T/rC" bash "$J" 2>&1); code=$?
ok $([ "$code" = 3 ] && printf '%s' "$out" | grep -q 'REFUSED: real Codex calls' && echo 0 || echo 1) "C2: CODEX_APPROVED_STANDIN without --approved: refused (exit 3)" "exit $code"
out=$(CODEX_STANDIN="$T/bin" PATH="$T/bin:$PATH" B="$T/rC" bash "$J" --approved 2>&1); code=$?
ok $([ "$code" = 3 ] && printf '%s' "$out" | grep -q 'pick one' && echo 0 || echo 1) "C3: --approved with CODEX_STANDIN: refused (exit 3)" "exit $code"
out=$(CODEX_APPROVED_STANDIN="$T/bin" PATH="$T/other:$PATH" B="$T/rC" bash "$J" --approved 2>&1); code=$?
ok $([ "$code" = 4 ] && printf '%s' "$out" | grep -q 'ABORT (approved-path test)' && echo 0 || echo 1) "C4: approved-path test with codex resolving elsewhere: aborted (exit 4)" "exit $code"
out=$(PATH="$T/bin:$PATH" B="$T/rC" bash "$J" --one p001 2>&1); code=$?
ok $([ "$code" != 0 ] && echo 0 || echo 1) "C5: a worker started by hand (no RUN_DIR) is refused" "exit $code"
ok $([ "$(calls "$T/bin")" = 0 ] && [ "$(calls "$T/other")" = 0 ] && echo 0 || echo 1) "C: no refused run called any codex" "$(calls "$T/bin") + $(calls "$T/other") calls"
ok $([ ! -e "$T/rC/ledger.jsonl" ] && echo 0 || echo 1) "C: no refused run wrote a grade"

# ---- D. stand-in test mode still grades every pair
mkround "$T/rD"
out=$(env -u CODEX_APPROVED_STANDIN CODEX_STANDIN="$T/bin" PATH="$T/bin:$PATH" B="$T/rD" bash "$J" 2>&1); code=$?
ok $([ "$code" = 0 ] && [ "$(calls "$T/bin")" = 2 ] && [ "$(valid_codex "$T/rD")" = 2 ] && echo 0 || echo 1) \
   "D: CODEX_STANDIN mode grades both pairs (exit 0, 2 calls, 2 valid)" "exit $code, $(calls "$T/bin") calls"
ok $(grep -q 'TEST, stand-in' "$T/rD/judge-codex.log" && echo 0 || echo 1) "D: the log marks the run as a stand-in test"
out=$(env -u CODEX_APPROVED_STANDIN CODEX_STANDIN="$T/bin" PATH="$T/bin:$PATH" B="$T/rD" bash "$J" 2>&1); code=$?
ok $([ "$code" = 0 ] && [ "$(calls "$T/bin")" = 2 ] && echo 0 || echo 1) "D: a second run skips the pairs already graded validly (no new call)" "$(calls "$T/bin") calls"

echo "judge_codex stand-in test: $((pass + fail)) assertions, $fail failed"
[ "$fail" = 0 ]
