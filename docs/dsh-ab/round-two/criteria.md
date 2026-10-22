# Round two criteria (frozen 2026-10-22, before any run)

Rule under test: branch dsh-side-claims (one sentence added to item 4 of the always-on rule, all four languages):
every number, date, deadline, fee, step or quoted wording the answer adds beyond what was asked is checked or cut, not hedged; arithmetic is redone a second way; a deadline is given at its safe end.
The same branch also adds one clause to the Files section (from a PR #1 review: the active skill's own files are part of the task, so the agent may read them outside the workspace). It does not touch these chat requests.

Regression check (added at Emily's request, labelled as such, not new evidence): the six round-one prompts rerun on gv-grav twice each with the branch rule, graded blind against the round-one plain answers and keys, and each round-one error marked caught/avoided or repeated.

Arms: gv-plain (deepseek-flash, no plugin) and gv-grav (same, plus dsh-gravitas, language zh-CN, alwaysOnRule true; the plugin link points at the branch worktree for the run). Same profile config as round one. Two runs per side per prompt (r1, r2). No prompt is dropped or rerun because of its result; a run is rerun only if it exits non-zero or returns an empty final text, and every such rerun is logged.

Grading: blind pairs (A/B order randomised per pair, map kept out of the packets), r1 vs r1 and r2 vs r2, two non-DeepSeek graders (Claude Opus 5.5, Claude Sonnet 5.5), each with the keys, same five scores as round one (correct, trap, honest, useful, concise, 0-10) plus winner and margin, plus a count of wrong added claims per answer.

Length and hedging (measured, not judged):
- chars = length of the final text.
- hedge rate = hedge markers per 1000 chars, same pattern list as the round-one measurement (zh: 可能, 大概, 也许, 或许, 以…为准, 建议…核实, 建议…确认, 不确定, 请咨询, 仅供参考; en: may, might, probably, check with, confirm with, not sure, verify).
- Round one baseline: median chars plain 1636.5, Gravitas 2025 (ratio 1.24); hedge rate plain 0.71, Gravitas 0.96 (ratio 1.35).
- Length regression: round-two Gravitas/plain median-chars ratio above 1.24.
- Hedging regression: round-two Gravitas/plain hedge-rate ratio above 1.35.
- Either regression counts as a failure of the rule change, whatever the votes say.
