#!/bin/sh
# usage: freeze.sh <label>   -> freeze-<label>.txt: everything the round runs and grades with; refuses to overwrite one
#        freeze.sh --state   -> the same lines without the label, on stdout (run.sh compares it with freeze-start.txt)
B=/w/AgentData/logs/gravitas-dsh-ab4
W=/w/Projects/gravitas-claim-check
H=/w/AgentData/dsh_home
state() {
  echo "head: $(git -C $W rev-parse HEAD)"
  echo "dirty: $(git -C $W status --porcelain -- dsh dist plugin package.json docs/dsh-ab | wc -l)"
  echo "link: $(powershell.exe -NoProfile -Command "(Get-Item 'W:\\AgentData\\dsh_home\\profiles\\gv-grav\\node_modules\\dsh-gravitas' -Force).Target" | tr -d '\r')"
  echo "dshhome: $(powershell.exe -NoProfile -Command "(Get-Item 'C:\\Users\\emily\\.dsh' -Force).Target" | tr -d '\r')"
  echo "dsh: $(dsh --version 2>/dev/null | head -1 | tr -d '\r')"
  echo "dshpkg: $(npm ls -g --depth=0 @deepseek-ai/dsh 2>/dev/null | grep -o '@deepseek-ai/dsh@[^ ]*')"
  echo "node: $(node --version)"
  # environment the runs inherit that DSH reads (values of DSH_* are hashed, never printed)
  echo "env-dsh: $(env | grep -E '^DSH_' | sort | sha256sum | cut -c1-16) count $(env | grep -cE '^DSH_')"
  echo "agents-dir: $(find ~/.agents -type f 2>/dev/null | sort | xargs -r sha256sum | sha256sum | cut -c1-16) files $(find ~/.agents -type f 2>/dev/null | wc -l)"
  for f in ~/.agents/AGENTS.md $H/AGENTS.md; do [ -e "$f" ] && echo "global-instructions: $(sha256sum "$f")"; done
  ( cd $H/profiles && sha256sum gv-plain/package.json gv-plain/cordis.yml gv-plain/cordis.patch.yml gv-plain/pnpm-workspace.yaml \
      gv-grav/package.json gv-grav/cordis.yml gv-grav/cordis.patch.yml gv-grav/pnpm-workspace.yaml gv-grav/pnpm-lock.yaml )
  ( cd $W && sha256sum dsh/index.js dsh/lib/*.js dsh/platform/*.md dist/*/gravitas/rules/AGENTS.md docs/dsh-ab/WIN_CRITERIA.md )
  ( cd $B && sha256sum run.sh runall.sh freeze.sh schedule.txt tuning-schedule.txt expected-rule-hashes.json \
      rules/change4/*.md overlays/*.yml prompts/*.txt keys/* keypoints/* \
      make_pairs4.py validity4.py verdict4.py build_notes4.py save_labels4.py workflows/*.js \
      $(ls verdict4-*.py verdict4-*.md grader-prompt4.md save_grades4.py judge_codex.sh *schema*.json mutation4.py preverdict4.py 2>/dev/null) )
}
if [ "$1" = "--state" ]; then state; exit 0; fi
[ -n "$1" ] || { echo "usage: freeze.sh <label> | --state"; exit 2; }
out=$B/freeze-$1.txt
[ -e "$out" ] && { echo "REFUSED: $out exists; a freeze record is never overwritten"; exit 3; }
{ echo "label: $1"; echo "time: $(date -Iseconds)"; state; } > $out
cat $out
echo "sha256: $(sha256sum $out | cut -c1-64)"
