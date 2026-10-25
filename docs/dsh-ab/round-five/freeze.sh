#!/bin/sh
# usage: freeze.sh <label>   -> freeze-<label>.txt: everything the round runs and grades with; refuses to overwrite one
#        freeze.sh --state   -> the same lines without the label, on stdout (run.sh compares it with freeze-start.txt)
B=/w/AgentData/logs/gravitas-dsh-ab5
W=/w/Projects/gravitas-round5
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
  # run.sh's test-only lock override: it must be unset in real runs, so a set value makes the state differ from freeze-start
  echo "lock-override: $([ -n "${RUN_LOCK_TEST+x}" ] && echo set || echo unset)"
  echo "agents-dir: $(find ~/.agents -type f 2>/dev/null | sort | xargs -r sha256sum | sha256sum | cut -c1-16) files $(find ~/.agents -type f 2>/dev/null | wc -l)"
  for f in ~/.agents/AGENTS.md $H/AGENTS.md; do [ -e "$f" ] && echo "global-instructions: $(sha256sum "$f")"; done
  ( cd $H/profiles && sha256sum gv-plain/package.json gv-plain/cordis.yml gv-plain/cordis.patch.yml gv-plain/pnpm-workspace.yaml \
      gv-grav/package.json gv-grav/cordis.yml gv-grav/cordis.patch.yml gv-grav/pnpm-workspace.yaml gv-grav/pnpm-lock.yaml )
  ( cd $W && sha256sum dsh/index.js dsh/lib/*.js dsh/platform/*.md dist/*/gravitas/rules/AGENTS.md docs/dsh-ab/WIN_CRITERIA.md )
  ( cd $B && sha256sum run.sh runall.sh freeze.sh schedule.txt schedule.seed.txt tuning-schedule-1.txt tuning-schedule-2.txt \
      expected-rule-hashes.json \
      rules/change5/*.md overlays/*.yml prompts/*.txt keys/* keypoints/* \
      make_pairs5.py validity5.py verdict5.py build_notes5.py save_labels5.py workflows/*.js \
      tuning-instrument/tuning_check5.py tuning-instrument/tuning_common5.py tuning-instrument/save_tuning_grades5.py \
      tuning-instrument/make_tuning_grade_script.py tuning-instrument/lkp.json tuning-instrument/premise-points.json \
      tuning-instrument/tuning-grade-schema5.json tuning-instrument/tuning-grader-prompt5.md design/tuning-decision-rule.md \
      $(ls verdict5-*.py verdict5-*.md grader-prompt5.md save_grades5.py judge_codex.sh *schema*.json mutation5.py preverdict5.py 2>/dev/null) )
  # round four's files that tuning reads: the prompts the tuning runs get, and the keys, key points and the 48 baseline
  # answers (finals and streams) the tuning grades and tuning_check5.py read. Named with the round folder, so these lines
  # cannot be mistaken for round five's prompts/, keys/ and keypoints/.
  ( cd /w/AgentData/logs && sha256sum gravitas-dsh-ab4/prompts/*.txt gravitas-dsh-ab4/keys/*.md gravitas-dsh-ab4/keypoints/*.json \
      gravitas-dsh-ab4/raw/*.gv-plain.r[12].txt gravitas-dsh-ab4/raw/*.gv-plain.r[12].ndjson \
      gravitas-dsh-ab4/raw/*.gv-grav-base.r[12].txt gravitas-dsh-ab4/raw/*.gv-grav-base.r[12].ndjson )
}
if [ "$1" = "--state" ]; then state; exit 0; fi
[ -n "$1" ] || { echo "usage: freeze.sh <label> | --state"; exit 2; }
out=$B/freeze-$1.txt
[ -e "$out" ] && { echo "REFUSED: $out exists; a freeze record is never overwritten"; exit 3; }
{ echo "label: $1"; echo "time: $(date -Iseconds)"; state; } > $out
cat $out
echo "sha256: $(sha256sum $out | cut -c1-64)"
