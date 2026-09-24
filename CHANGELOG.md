# Changelog

All notable changes to this project are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- The README is rewritten in two parts in all four languages: Part 1 explains what Gravitas does for someone with no technical background, with a real example, costs, risks, limits and a step-by-step install; Part 2 gives the architecture, the evidence, the test results and a comparison with Antigravity's own `/boost` and `/teamwork-preview` and with 18 public skills.
- `docs/comparison.md`: the evidence behind the comparison, from research on 24 September 2026. It holds fifteen features, 18 projects read in depth with the evidence for every cell, the four novelty claims and the refuters that narrowed three of them, and all 63 candidates found.
- `plugin/README.md` ships inside the installed plugin, and a translated install writes the translated README and plugin description, the text Antigravity lists for the plugin. `check_skills.py --repo` fails when a translation lacks either.
- 171 tests for the four scripts in `tests/scripts/`, runnable with plain Python, and `scripts/readme_parity.py`, which checks that each translated README keeps the English structure.

### Fixed
- `provenance_check.py` pairs every tool call with its own result, so a failed fetch or a denied command no longer counts as opened or run; checks a quote against the source the label cites; matches URLs and paths exactly, with a parent page as a warning; compares the whole command, keeping case and argument spacing; reads `steps/<n>/output.txt`; recognises POSIX paths; and survives malformed rows, CJK quotes and Windows pipes. Its verdicts on the seven real test answers are unchanged.
- `ledger.py` reports never-voted findings at quick scale as unverified; records blocked and demoted votes without counting them; holds votes to the same provenance rule as findings; requires a `read` source to quote content, not a path; flags nearby duplicates instead of silently dropping them unless the wording is near-identical; validates records against the schemas; and handles blocked finder envelopes and files with a byte order mark.
- `slopcheck.py` gains `--strict`, which exits 1 on any flag; matches banned words on word boundaries while still catching derived forms; flags any em-dash, conclusion crutches and an unclosed code fence; skips quoted, blockquoted and fenced questions; and survives Windows pipes and missing files.
- `check_skills.py` bars file-writing tools from every verifier role, not only critics, and reports malformed tool fields instead of crashing. The refuter's verdict schema gains `status` and `error`.
- Module corrections in all four languages: the chocolate-factory suite had 8 gates, not 9; the automated-accessibility figure now cites the 2017 UK government tool audit and Deque's 2021 study; `restart_dev_server` is marked as unconfirmed; the triage module records the retest that fixed the control case. `TESTS.md` gives the Gaussian integral as 0.886227, and the English `SKILL.md` compatibility line names agy 1.2.9.

### Changed
- The README states that the beta 1 comparison was not clean: the always-on hook was installed for the bare-prompt arm, which opened the skill in 21 of 22 runs. A clean with-and-without benchmark is the next piece of work.
- The plugin description is written for people choosing a plugin rather than for engineers.

## [1.0.0-beta.2] - 2026-09-24

### Added
- Plugin packaging under `plugin/`: the skill, eight verifier agents and an always-on rule install as one folder at `~/.gemini/config/plugins/gravitas/`, and `agy plugin disable gravitas` turns all of it off.
- Eight custom agents (`gravitas-scout`, `-reader`, `-finder`, `-checker`, `-refuter`, `-visual-critic`, `-completeness-critic`, `-prose-editor`). Critics have no edit tools, so read-only verification comes from the tool list instead of an instruction. Each sets `inheritCustomizations: false` and `inheritMcp: false`, carries its return schema inline and refuses relative paths, and all but the prose editor are told not to search the machine for context.
- `scripts/ledger.py`: deterministic bookkeeping for fan-outs. It deduplicates against every finding ever seen, merges same-location duplicates at a word overlap of 0.25 (calibrated on a real audit), flags possible duplicates for `merge`, tallies votes by scale, counts dry rounds, and demotes any `observed`, `executed` or `read` record that has no source.
- `scripts/provenance_check.py`: compares every evidence label in an answer with the conversation's transcript, and fails `read` labels on pages never opened (including ones seen only in a search summary), quotes absent from anything fetched, and `executed` labels whose command never ran.
- `schemas/finding.schema.json` and `schemas/verdict.schema.json` for the records subagents return.
- New modules: `02-evidence-traps.md` (delegated claims, supplied documents, documentation, expiry, instruments you built), `06-perceptual-gates.md`, `08-delegation.md`, and `11-findings.md` (bug reports and audits published under a person's name).
- A scale table with concrete fan-out, vote and stop numbers for quick, standard, full and exhaustive work.
- Rules from this release's own testing: absolute paths only; ask or stop when a request looks incomplete; take version stamps from the run's own log; a search summary is not a page; an `executed` label shows the command that ran; checkers prove exploits against a canary; in a headless run, keep polling until every subagent is done and write the report first.
- `tests/audit-case/`: a three-file package with three planted defects and a test that encodes one of them, with an answer key in `TESTS.md`.
- Full Simplified Chinese, Japanese and Korean translations of all 14 modules, the router and the rule. Beta 1 translated only `SKILL.md`.
- `CHANGELOG.md`.

### Changed
- `SKILL.md` is now a router under 500 characters that loads `references/00-orchestrator.md`, matching the layout of the author's other skills. The doctrine moved into 14 numbered modules, each 100 lines or fewer so it fits in one `view_file` window.
- The subagent reference now documents the tool declarations as the model receives them on agy 1.2.9: `invoke_subagent` takes a `Subagents` array with `TypeName`, `Role`, `Prompt`, `Model` and `Workspace`. The old `subagent_count` and `subagent_model` fields are gone.
- The platform module is re-tested on agy 1.2.9, checked against documentation and binary strings from desktop 2.17.0, with every entry stamped with the version and date it was checked.
- `check_skills.py` now validates plugins, agents and rules: tool names that could hang an agent, critics with write tools, rule files over 24,000 bytes, modules over 100 lines and references to modules that do not exist. It ships inside the skill with `slopcheck.py`.
- The skill description is under 500 characters, because the longest descriptions were the ones Antigravity dropped from its customization budget.
- The installer is one Python script behind `install.sh` and `install.ps1`, and it moves a previous bare-skill install and its hook into a timestamped backup.

### Fixed
- Re-tested on agy 1.2.9 on 24 September 2026, which corrected four platform claims. A workspace `.agents/` folder does load when the repo is passed with `--add-dir`. "Hooks fail open" held only for `PreInvocation`; a failing `PreToolUse` hook denies the call. `view_file` rejects relative paths, and the stale-file hazard comes from agents treating the shared scratch folder as their workspace. The CLI's headless policy comes from `toolPermission` and grants in its own `settings.json` as well as `config.json`, and on Windows a `command()` rule needs the exact line or `regex:`.
- `13-platform.md` records three more behaviours from the same testing: a subagent's result never reaches a parent that has already ended its turn, a hook refusal can be followed by a reply stating output that was never produced, and `overwrite` needs a `decision`.

### Removed
- The `PreInvocation` hook and `hooks/`. The plugin's `rules/AGENTS.md` replaces it without needing Python on the path.
- `scripts/rename.py`, which only served the rename from `ultracode`.

## [1.0.0-beta.1] - 2026-09-20

### Added
- First private beta: evidence tiers with provenance slots, the proxy trap, per-domain checks, acceptance gates, iteration rules, the prose standard and verified platform constraints.
- Simplified Chinese, Japanese and Korean translations.
- The Gravitas character.
