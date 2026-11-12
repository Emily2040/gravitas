#!/bin/sh
# usage: run.sh <arm> <case> <round> [promptdir] [outdir]  -> <outdir>/<case>.<arm>.r<round>.{ndjson,err,txt,exit,rule.jsonl}
# arms: gv-plain; gv-grav-base (rule only, check off); gv-grav-c5 (base + change 5). Gravitas runs in the request's language.
# Refuses to run unless everything freeze.sh records (worktree HEAD, the gv-grav link target, profiles, code, rules,
# overlays, prompts, keys, scripts) still matches freeze-start.txt. Held-out runs read prompts/ and write raw/; tuning
# runs read round four's prompts and write tuning/, and only before any held-out run exists. A run whose files exist
# is never overwritten unless validity5.py archived it for its one rerun. Every attempt is appended to run-ledger.tsv.
# Tuning runs gv-grav-c5 only, in two passes: pass N runs tuning-schedule-N.txt, whose lines carry round N (1 or 2),
# and its reruns come from rerun-schedule-tuning-N.txt (validity5.py --tuning N --archive-invalid).
# Rerun cap (Emily's approval: one rerun per invalid run, stop and ask past 8; the tuning decision rule: more than 2
# invalid runs in a pass means stop and ask): a rerun is refused while raw/attempt1 and tuning/attempt1 together hold
# more than 8 archived runs, and a tuning rerun while its pass has more than 2 in tuning/attempt1.
# Lock: refuses unless W:\AgentData\dsh_home\profiles\gv-grav.LOCK exists and its first line is exactly
# "owner: dsh-round5" (a CR before the newline counts as part of the line end). run.sh only reads the lock; it never
# creates or removes it. RUN_LOCK_TEST points the check at another file and is for tests only: it MUST be unset in
# real runs. freeze.sh records whether it is set, so a real run with it set is refused by the freeze comparison.
B=/w/AgentData/logs/gravitas-dsh-ab5
R4P=/w/AgentData/logs/gravitas-dsh-ab4/prompts
a=$1; c=$2; r=${3:-1}; pd=${4:-$B/prompts}; od=${5:-$B/raw}
stem=$c.$a.r$r
refuse() { echo "$stem REFUSED: $1"; exit 3; }
LOCK=${RUN_LOCK_TEST:-/w/AgentData/dsh_home/profiles/gv-grav.LOCK}
[ -f "$LOCK" ] || refuse "no lock file $LOCK"
[ "$(head -n 1 "$LOCK" | sed 's/\r$//')" = "owner: dsh-round5" ] || refuse "lock $LOCK: first line is not 'owner: dsh-round5'"
[ -f $B/freeze-start.txt ] || refuse "no freeze-start.txt"
tmp=$B/.state.$$
sh $B/freeze.sh --state > $tmp.now
sed 1,2d $B/freeze-start.txt > $tmp.start
if ! cmp -s $tmp.start $tmp.now; then
  echo "$stem REFUSED: state differs from freeze-start:"
  diff $tmp.start $tmp.now | head -20
  rm -f $tmp.now $tmp.start
  exit 3
fi
rm -f $tmp.now $tmp.start
grep -qF 'link: W:\Projects\gravitas-round5' $B/freeze-start.txt || refuse "gv-grav link is not the gravitas-round5 worktree"
# which prompts go to which folder, and limits that only a test may change
case "$od" in
  $B/raw) [ "$pd" = "$B/prompts" ] || refuse "held-out runs read $B/prompts only"; lim=1800
          led=$B/run-ledger.tsv; rs=$B/rerun-schedule.txt ;;
  $B/tuning) [ "$pd" = "$R4P" ] || refuse "tuning runs read round four's prompts only"
             ls $B/raw/*.ndjson > /dev/null 2>&1 && refuse "tuning comes before the held-out runs, and raw/ already has runs"
             [ "$a" = gv-grav-c5 ] || refuse "tuning runs gv-grav-c5 only"
             case "$r" in 1|2) ;; *) refuse "tuning has passes 1 and 2 only (round $r)" ;; esac
             lim=1800; led=$B/run-ledger.tsv; rs=$B/rerun-schedule-tuning-$r.txt ;;
  *) lim=${RUN_LIMIT:-1800}; led=$od/run-ledger.tsv; rs=$od/rerun-schedule.txt ;;  # a test folder keeps its own records
esac
[ -f "$pd/$c.txt" ] || refuse "no prompt $pd/$c.txt"
L=${c%%-*}
case $a in
  gv-plain) prof=gv-plain; extra="" ;;
  gv-grav-base) prof=gv-grav; extra="--patch $B/overlays/base-$L.yml" ;;
  gv-grav-c5) prof=gv-grav; extra="--patch $B/overlays/c5-$L.yml" ;;
  *) echo "unknown arm $a"; exit 2 ;;
esac
out=$od/$stem
# the rerun cap: every archived attempt is one rerun spent or due, counted over tuning and held-out together
if [ -e $od/attempt1/$stem.ndjson ]; then
  n=$(ls $B/raw/attempt1/*.ndjson $B/tuning/attempt1/*.ndjson 2>/dev/null | wc -l)
  [ "$n" -le 8 ] || refuse "$n runs archived for a rerun, past the 8 reruns approved: stop and ask Emily"
  if [ "$od" = "$B/tuning" ]; then
    n=$(ls $B/tuning/attempt1/*.r$r.ndjson 2>/dev/null | wc -l)
    [ "$n" -le 2 ] || refuse "$n runs of tuning pass $r archived as invalid, more than 2 in a pass: stop and ask Emily"
  fi
fi
if [ -e $out.exit ] || [ -e $out.ndjson ]; then
  grep -qx "$a $c $r" $rs 2>/dev/null && [ -e $od/attempt1/$stem.ndjson ] \
    || refuse "$out exists; only a run validity5.py archived for its one rerun may run again"
  refuse "$out exists although it was archived for a rerun; move it to attempt1 first"
fi
if [ -e $od/attempt1/$stem.ndjson ] && ! grep -qx "$a $c $r" $rs 2>/dev/null; then
  refuse "an archived attempt exists but the run is not in rerun-schedule.txt"
fi
d=/w/AgentData/logs/gravitas-dsh-ab3/cwd/r5-$stem; rm -rf "$d"; mkdir -p "$d" $od; cd "$d"
rm -f $out.rule.jsonl $out.timeout
unset DSH_PERMISSION_MODE DSH_TOOLS_MODE
start=$(date +%s)
# set for every arm: plain must leave no rule log (the plugin is not loaded there)
GRAVITAS_RULE_LOG="$(cygpath -w $out.rule.jsonl)" dsh --profile $prof $extra --json - < $pd/$c.txt > $out.ndjson 2> $out.err &
pid=$!
# a hung run is killed with its whole process tree after lim seconds (round three's longest run took 398);
# its exit code is then 124, so validity5.py marks it invalid and it gets its one rerun
# Windows parent links do not follow MSYS process trees, so walk the MSYS table and tree-kill each native process
killtree() {  # parent first, so it cannot go on to its next step; its children are listed before it dies
  kids=$(ps -ef | awk -v p=$1 '$3 == p { print $2 }')
  w=$(cat /proc/$1/winpid 2>/dev/null)
  kill -STOP $1 2>/dev/null
  [ -n "$w" ] && taskkill //T //F //PID $w > /dev/null 2>&1
  kill -9 $1 2>/dev/null
  for ch in $kids; do killtree $ch; done
}
( sleep $lim; if kill -0 $pid 2>/dev/null; then echo "killed after $lim s" > $out.timeout; killtree $pid; fi ) &
wd=$!
wait $pid
code=$?
killtree $wd 2>/dev/null  # also ends its pending sleep
[ -f $out.timeout ] && code=124
end=$(date +%s)
echo "$code" > $out.exit
node -e 'const fs=require("fs");const l=fs.readFileSync(process.argv[1],"utf8").trim().split("\n").map(s=>{try{return JSON.parse(s)}catch{return {}}});const f=l.filter(e=>e.type==="final").pop();fs.writeFileSync(process.argv[2],(f&&f.text)||"")' $out.ndjson $out.txt
sid=$(grep -o '"sessionId":"[^"]*"' $out.ndjson | head -1 | cut -d'"' -f4)
fz=$(sha256sum $B/freeze-start.txt | cut -c1-16)
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$stem" "$od" "$start" "$end" "$code" "$fz" "${sid:-none}" >> $led
echo "$c $a r$r exit=$code secs=$((end-start)) chars=$(wc -m < $out.txt)"
