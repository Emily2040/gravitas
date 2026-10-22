#!/bin/sh
# usage: run.sh <arm> <case> <round> [promptdir]  -> raw/<case>.<arm>.r<round>.{ndjson,err,txt}
# arms: gv-plain, gv-grav, gv-grav-nocheck (gv-grav with nocheck.patch.yml)
B=/w/AgentData/logs/gravitas-dsh-ab3
a=$1; c=$2; r=${3:-1}; pd=${4:-$B/prompts}
case $a in
  gv-grav-nocheck) prof=gv-grav; extra="--patch $B/nocheck.patch.yml" ;;
  *) prof=$a; extra="" ;;
esac
d=$B/cwd/$c.$a.r$r; mkdir -p $d; cd $d
out=$B/raw/$c.$a.r$r
start=$(date +%s)
GRAVITAS_CLAIM_LOG="W:/AgentData/logs/gravitas-dsh-ab3/raw/$c.$a.r$r.claims.jsonl" dsh --profile $prof $extra --json - < $pd/$c.txt > $out.ndjson 2> $out.err
code=$?
end=$(date +%s)
node -e 'const fs=require("fs");const l=fs.readFileSync(process.argv[1],"utf8").trim().split("\n").map(s=>{try{return JSON.parse(s)}catch{return {}}});const f=l.filter(e=>e.type==="final").pop();fs.writeFileSync(process.argv[2],(f&&f.text)||"")' $out.ndjson $out.txt
echo "$c $a r$r exit=$code secs=$((end-start)) chars=$(wc -m < $out.txt)"
