# Changelog

All notable changes to this project are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [1.0.0-beta.2] - 2026-09-24

### Added
- Plugin packaging under `plugin/`: the skill, eight verifier agents and an always-on rule install as one folder at `~/.gemini/config/plugins/gravitas/`, and `agy plugin disable gravitas` turns all of it off.
- Eight custom agents (`gravitas-scout`, `-reader`, `-finder`, `-checker`, `-refuter`, `-visual-critic`, `-completeness-critic`, `-prose-editor`). Critics have no edit tools, so read-only verification comes from the tool list instead of an instruction. Each sets `inheritCustomizations: false` and `inheritMcp: false`, carries its return schema inline, refuses relative paths, and is told not to search the machine for context.
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
- `SKILL.md` is now a router under 500 characters that loads `references/00-orchestrator.md`, matching the layout of the author's other skills. The doctrine moved into 14 numbered modules, each under 100 lines so it fits in one `view_file` window.
- The subagent reference now documents the tool declarations as the model receives them on agy 1.2.9: `invoke_subagent` takes a `Subagents` array with `TypeName`, `Role`, `Prompt`, `Model` and `Workspace`. The old `subagent_count` and `subagent_model` fields are gone.
- The platform module is re-verified on desktop 2.17.0 and agy 1.2.9, with every entry stamped with the version and date it was checked.
- `check_skills.py` now validates plugins, agents and rules: tool names that could hang an agent, critics with write tools, rule files over 24,000 bytes, modules over 100 lines and references to modules that do not exist. It ships inside the skill with `slopcheck.py`.
- The skill description is under 500 characters, because the longest descriptions were the ones Antigravity dropped from its customization budget.
- The installer is one Python script behind `install.sh` and `install.ps1`, and it moves a previous bare-skill install and its hook into a timestamped backup.

### Removed
- The `PreInvocation` hook and `hooks/`. The plugin's `rules/AGENTS.md` replaces it without needing Python on the path.
- `scripts/rename.py`, which only served the rename from `ultracode`.

## [1.0.0-beta.1] - 2026-09-20

### Added
- First private beta: evidence tiers with provenance slots, the proxy trap, per-domain checks, acceptance gates, iteration rules, the prose standard and verified platform constraints.
- Simplified Chinese, Japanese and Korean translations.
- The Gravitas character.
