#!/bin/sh
# usage: runall.sh   runs schedule.txt three at a time (one triplet at a time), appending to run.log
B=/w/AgentData/logs/gravitas-dsh-ab3
xargs -P 3 -L 1 sh -c 'sh '"$B"'/run.sh "$0" "$1" "$2"' < $B/schedule.txt >> $B/run.log 2>&1
echo "runall done" >> $B/run.log
