#!/usr/bin/env bash
# usage: codex_drive.sh <limit>   grade up to <limit> pairs that have no valid codex grade, 3 at a time
# judge_codex.sh's main loop starts each worker as `judge_codex.sh --one <pid>`, and the worker resets MODE while
# reading its arguments, so its guard refuses every real call (stand-in tests never exercise MODE). This driver does
# what the main loop does, unchanged, but starts each worker as `judge_codex.sh --approved --one <pid>`; the worker
# code (prompt, model, flags, schema, ledger record and check) is the frozen script's own. Emily approved ~96 calls.
set -u
B=/w/AgentData/logs/gravitas-dsh-ab4
lim=${1:?limit}
ver="$(codex --version 2>/dev/null | head -1 | tr -d '\r')"
[ "$ver" = "codex-cli 0.163.0" ] || { echo "codex --version is '$ver'"; exit 5; }
RUN_DIR=$B/dev/codex-run/$(date +%Y%m%d-%H%M%S); EMPTY_DIR=$RUN_DIR/empty; mkdir -p "$EMPTY_DIR"
export RUN_DIR EMPTY_DIR
todo="$(python $B/save_grades4.py --base "$(cygpath -w $B)" --todo codex)" || { echo "todo failed"; exit 2; }
todo="$(printf '%s\n' "$todo" | grep . | head -n "$lim")"
echo "$(date '+%Y-%m-%dT%H:%M:%S%z') driver start (REAL, approved; dev/codex_drive.sh): $(printf '%s\n' "$todo" | grep -c .) to grade, $ver" >> $B/judge-codex.log
printf '%s\n' "$todo" | grep . | xargs -P 3 -I{} bash $B/judge_codex.sh --approved --one {}
python $B/save_grades4.py --base "$(cygpath -w $B)" --judge codex > "$RUN_DIR/final.check" 2>&1
echo "$(date '+%Y-%m-%dT%H:%M:%S%z') driver end: $(tail -1 "$RUN_DIR/final.check")" >> $B/judge-codex.log
tail -1 "$RUN_DIR/final.check"
