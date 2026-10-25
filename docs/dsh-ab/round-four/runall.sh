#!/bin/sh
# usage: runall.sh <schedule> [promptdir] [outdir]   three at a time (one triplet), appending to run.log
B=/w/AgentData/logs/gravitas-dsh-ab4
s=$1; pd=${2:-$B/prompts}; od=${3:-$B/raw}
xargs -P 3 -L 1 sh -c 'sh '"$B"'/run.sh "$0" "$1" "$2" '"$pd $od" < $s >> $B/run.log 2>&1
echo "runall $s done" >> $B/run.log
