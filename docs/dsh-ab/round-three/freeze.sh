#!/bin/sh
# usage: freeze.sh <label>  -> freeze-<label>.txt: what code the runs used (criteria.md, amendments)
B=/w/AgentData/logs/gravitas-dsh-ab3
W=/w/Projects/gravitas-claim-check
out=$B/freeze-$1.txt
{
  echo "label: $1"
  echo "head: $(git -C $W rev-parse HEAD)"
  echo "dirty: $(git -C $W status --porcelain -- dsh package.json | wc -l)"
  sha256sum $W/dsh/index.js $W/dsh/lib/claims.js $W/dsh/lib/provider.js | sed "s|$W/||"
  echo "link: $(powershell.exe -NoProfile -Command "(Get-Item 'W:\\AgentData\\dsh_home\\profiles\\gv-grav\\node_modules\\dsh-gravitas' -Force).Target" | tr -d '\r')"
} > $out
cat $out
