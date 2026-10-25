#!/usr/bin/env bash
# judge_codex.sh: grade every packet in blind/packets/ with the third judge, OpenAI gpt-6-astra at high reasoning
# effort through Codex CLI 0.163.0 (WIN_CRITERIA amendment of 2026-10-24), one pair per session, at most 3 at a time.
#
#   judge_codex.sh --approved [--limit N]          REAL: every call spends Emily's OpenAI quota; run only with her
#                                                  approval. Try --limit 1 first and check the grade it writes.
#   CODEX_STANDIN=<dir> judge_codex.sh [--limit N] TEST: refuses to start unless `command -v codex` is <dir>/codex
#                                                  (give <dir> in /c/... form, from cygpath -u; never C:/...)
#   CODEX_APPROVED_STANDIN=<dir> judge_codex.sh --approved [--limit N]
#                                                  TEST of the approved path (tests/judge_codex_test.sh only): runs as
#                                                  REAL, but every guard also aborts unless `command -v codex` is
#                                                  <dir>/codex. It MUST be unset in real runs.
#   B=<folder> ...                                 the round folder (default /w/AgentData/logs/gravitas-dsh-ab5)
#
# The main run starts each worker as `judge_codex.sh [--approved] --one <pid>`, passing --approved when it runs
# approved, so the worker's guard sees the parent's mode (round four's workers dropped it and refused every real call).
# With neither --approved nor CODEX_STANDIN it refuses. Pairs that already have a valid codex grade in the ledger
# (save_grades5.py --todo) are skipped, so a rerun grades only what is missing or malformed. Each session gets
# grader-prompt5.md with the packet inline on stdin, a strict output schema built for that pair
# (save_grades5.py --schema: the pid, the case's key-point ids, the score and mark values), and writes its last
# message to blind/grades/codex/<pid>.json:
#   codex --search exec -m gpt-6-astra -c model_reasoning_effort="high" -s read-only --skip-git-repo-check
#              --ephemeral --output-schema <schema> -o blind/grades/codex/<pid>.json -
# run from an empty temporary folder. --search (a top-level flag in `codex --help`, absent from `codex exec --help`)
# gives the judge live web search, as the grader prompt allows; the sandbox stays read-only. The flag order is
# unverified until the first real `--approved --limit 1` call. Every start and end is logged to judge-codex.log in
# the round folder; the session's exact prompt, stdout and stderr go to judge-codex-runs/<pid>.{prompt.txt,out,err}.
# After each session the grade is logged in ledger.jsonl (save_grades5.py --record, which also checks that the prompt
# was grader-prompt5.md plus these delivery lines and the current packet); the first valid ledger grade of a pair is
# the one used (amendment 2026-10-25). Exit 0 only if every pair in blind-map.json then has a valid codex grade.
set -u

SELF="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
TOOLS="$(dirname "$SELF")"            # grader-prompt5.md and save_grades5.py live beside this script
B="${B:-/w/AgentData/logs/gravitas-dsh-ab5}"
MODEL="gpt-6-astra"
CODEX_VERSION="codex-cli 0.163.0"
JOBS=3
export B TOOLS

log() {   # one line per event; a mkdir lock keeps the three workers' lines whole (gives up waiting after 10 s)
  line="$(date '+%Y-%m-%dT%H:%M:%S%z') $*"
  i=0
  while ! mkdir "$B/.judge-codex.log.lock" 2>/dev/null; do
    i=$((i + 1)); [ "$i" -gt 100 ] && break; sleep 0.1
  done
  printf '%s\n' "$line" >> "$B/judge-codex.log"
  [ "$i" -gt 100 ] || rmdir "$B/.judge-codex.log.lock" 2>/dev/null
}
die() { echo "judge_codex.sh: $*" >&2; exit "${2:-2}"; }
winpath() { cygpath -w "$1"; }

# The guard runs first in the parent and again in every worker shell, before codex is touched in any way.
guard() {
  if [ -n "${CODEX_STANDIN:-}" ]; then
    [ "${MODE:-}" = approved ] && die "REFUSED: --approved and CODEX_STANDIN together; pick one" 3
    want="${CODEX_STANDIN%/}/codex"
    got="$(command -v codex 2>/dev/null || true)"
    if [ "$got" != "$want" ]; then
      die "ABORT (test mode): codex resolves to '$got', not the stand-in '$want'; nothing was run" 4
    fi
  elif [ "${MODE:-}" != approved ]; then
    die "REFUSED: real Codex calls spend Emily's OpenAI quota. Pass --approved only with her approval, or set CODEX_STANDIN for a test." 3
  elif [ -n "${CODEX_APPROVED_STANDIN:-}" ]; then   # the approved path under test: never the real codex
    want="${CODEX_APPROVED_STANDIN%/}/codex"
    got="$(command -v codex 2>/dev/null || true)"
    if [ "$got" != "$want" ]; then
      die "ABORT (approved-path test): codex resolves to '$got', not the stand-in '$want'; nothing was run" 4
    fi
  fi
}

one() {   # grade one pair; runs in a worker shell started by xargs
  pid="$1"
  guard
  packet="$B/blind/packets/$pid.md"
  out="$B/blind/grades/codex/$pid.json"
  schema="$RUN_DIR/$pid.schema.json"
  prompt="$B/judge-codex-runs/$pid.prompt.txt"
  [ -f "$packet" ] || { log "$pid SKIP no packet"; return 1; }
  mkdir -p "$B/blind/grades/codex" "$B/judge-codex-runs"
  if ! python "$TOOLS/save_grades5.py" --base "$(winpath "$B")" --schema "$pid" "$(winpath "$schema")" > "$RUN_DIR/$pid.schema.log" 2>&1; then
    log "$pid FAIL could not build the output schema: $(head -1 "$RUN_DIR/$pid.schema.log")"
    return 1
  fi
  {
    cat "$TOOLS/grader-prompt5.md"
    printf '\nPacket: given in full below, between the lines BEGIN PACKET and END PACKET. Do not open any file on disk.\n'
    printf 'Output: your whole final reply is the JSON object described above, with "pair" set to "%s", and nothing before or after it.\n\n' "$pid"
    printf 'BEGIN PACKET\n'
    cat "$packet"
    printf '\nEND PACKET\n'
  } > "$prompt"
  log "$pid start"
  t0=$(date +%s)
  ( cd "$EMPTY_DIR" && codex --search exec -m "$MODEL" -c 'model_reasoning_effort="high"' -s read-only --skip-git-repo-check \
      --ephemeral --output-schema "$(winpath "$schema")" -o "$(winpath "$out")" - \
      < "$prompt" > "$B/judge-codex-runs/$pid.out" 2> "$B/judge-codex-runs/$pid.err" )
  code=$?
  t1=$(date +%s)
  python "$TOOLS/save_grades5.py" --base "$(winpath "$B")" --record codex "$pid" > "$RUN_DIR/$pid.record" 2>&1
  if python "$TOOLS/save_grades5.py" --base "$(winpath "$B")" --check codex "$pid" > "$RUN_DIR/$pid.check" 2>&1; then
    v="valid, in force"
  else
    v="INVALID ($(head -1 "$RUN_DIR/$pid.record"); $(head -1 "$RUN_DIR/$pid.check"))"
  fi
  log "$pid end exit=$code secs=$((t1 - t0)) grade $v"
  [ "$v" = "valid, in force" ]
}

MODE=""
LIMIT=""
WORKER=""
while [ $# -gt 0 ]; do
  case "$1" in
    --approved) MODE=approved ;;
    --limit) shift; LIMIT="${1:-}" ;;
    --one) shift; WORKER="${1:-}" ;;
    -h|--help) sed -n '2,30p' "$SELF"; exit 0 ;;
    *) die "unknown argument $1" ;;
  esac
  shift
done
export MODE

if [ -n "$WORKER" ]; then
  [ -n "${RUN_DIR:-}" ] && [ -n "${EMPTY_DIR:-}" ] || die "--one is internal (started by the main run)"
  one "$WORKER"
  exit $?
fi

guard
[ -d "$B/blind/packets" ] || die "no $B/blind/packets"
[ -f "$B/blind-map.json" ] || die "no $B/blind-map.json"
[ -f "$TOOLS/grader-prompt5.md" ] || die "no $TOOLS/grader-prompt5.md"
case "$LIMIT" in ''|*[!0-9]*) [ -z "$LIMIT" ] || die "--limit needs a number" ;; esac
ver="$(codex --version 2>/dev/null | head -1 | tr -d '\r')"
[ "$ver" = "$CODEX_VERSION" ] || die "codex --version is '$ver', not '$CODEX_VERSION' (WIN_CRITERIA names that version)" 5

RUN_DIR="$(mktemp -d)"
EMPTY_DIR="$RUN_DIR/empty"
mkdir -p "$EMPTY_DIR"
export RUN_DIR EMPTY_DIR CODEX_STANDIN="${CODEX_STANDIN:-}" CODEX_APPROVED_STANDIN="${CODEX_APPROVED_STANDIN:-}"
trap 'rm -rf "$RUN_DIR"' EXIT

todo="$(python "$TOOLS/save_grades5.py" --base "$(winpath "$B")" --todo codex)" || die "save_grades5.py --todo failed"
total=$(ls "$B/blind/packets" | grep -c '\.md$')
n_todo=$(printf '%s\n' "$todo" | grep -c .)
if [ -n "$LIMIT" ]; then todo="$(printf '%s\n' "$todo" | grep . | head -n "$LIMIT")"; fi
n_run=$(printf '%s\n' "$todo" | grep -c .)
log "run start ($([ -n "${CODEX_STANDIN:-}" ] && echo "TEST, stand-in $CODEX_STANDIN" || echo "REAL, approved${CODEX_APPROVED_STANDIN:+ (approved-path test, stand-in $CODEX_APPROVED_STANDIN)}")):$total packets, $((total - n_todo)) already graded validly and skipped, $n_run to grade now${LIMIT:+ (limit $LIMIT)}; model $MODEL, effort high, live web search on (--search), $ver, at most $JOBS at a time"
echo "grading $n_run pairs ($((total - n_todo)) of $total already valid)"
if [ "$n_run" -gt 0 ]; then
  WFLAG=""
  if [ "$MODE" = approved ]; then WFLAG="--approved"; fi   # each worker keeps the parent's mode for its own guard
  printf '%s\n' "$todo" | grep . | xargs -P "$JOBS" -I{} bash "$SELF" $WFLAG --one {}
fi
python "$TOOLS/save_grades5.py" --base "$(winpath "$B")" --judge codex > "$RUN_DIR/final.check" 2>&1
status=$?
log "run end: $(tail -1 "$RUN_DIR/final.check")"
cat "$RUN_DIR/final.check"
exit $status
