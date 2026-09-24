# How Gravitas Compares: The Evidence

This is the record behind the comparison in the [README](../README.md#compare). On 24 September 2026, research agents searched GitHub from six angles, read 18 projects in depth against the fifteen features below, and then tried to refute every claim of novelty. Each cell below was written by an agent that opened the project's files, and its evidence is quoted or paraphrased from those files. Star counts were read from GitHub the same day. Projects change; if a cell here is out of date, the project's current files win.

✓ implemented as Gravitas defines it, ◐ partial or close, ✗ not found.

## The Fifteen Features

| ID | Feature | Definition |
| :--- | :--- | :--- |
| F1 | Evidence labels | Every claim carries a tier (for example observed, executed, read, inferred), and each label must name what established it: the artifact, the command, or the URL and a quoted line. |
| F2 | Transcript audit | A script compares the labels in a finished answer with the agent's own tool-call transcript, and fails `read` labels on pages never opened (including ones seen only in a search summary) and `executed` labels on commands that never ran. |
| F3 | Proxy test | An explicit rule for spotting checks that can pass while the property that matters is false, applied across fields. |
| F4 | Non-code fields | Verification guidance for law, mathematics, medicine, statistics, history and physics, naming the independent check available in each. |
| F5 | Read-only verifiers | Verifier subagents whose read-only status comes from their tool list, with their context isolated from the user's other customizations. |
| F6 | Vote ledger | Refuters that default to refuted, majority votes, and a script that deduplicates findings across rounds, tallies votes and demotes unsourced records. |
| F7 | Stop rules | A completeness critic and a loop-until-dry stop, with fixed numbers for fan-out, votes and rounds at named scales. |
| F8 | Visual gates | Rendered output judged by a fresh critic who has not seen the source. |
| F9 | Iteration research | Loop rules grounded in published self-correction research. |
| F10 | Prose script | A script that measures structural markers of generated prose before publishing. |
| F11 | Platform findings | Host-platform behaviour verified by experiment, stamped with version and date, and filed upstream. |
| F12 | Triage gate | Trivial requests answered directly, tested with a control case. |
| F13 | Translations | Full line-for-line translations of the skill. |
| F14 | Validator | A script that lints skills, plugins and agents. |
| F15 | Baited tests | A test suite with baited cases and a planted-defect audit case with an answer key. |

## Matrix

| Project | Stars | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 | F14 | F15 |
| :--- | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| [obra/superpowers](https://github.com/obra/superpowers) | 290959 | ◐ | ✗ | ◐ | ✗ | ◐ | ✗ | ◐ | ✗ | ◐ | ✗ | ◐ | ✗ | ✗ | ◐ | ◐ |
| [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | 248564 | ◐ | ◐ | ✗ | ◐ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ | ✗ | ✗ | ◐ |
| [garrytan/gstack](https://github.com/garrytan/gstack) | 134064 | ◐ | ✗ | ✗ | ✗ | ✗ | ◐ | ◐ | ◐ | ◐ | ◐ | ✗ | ◐ | ✗ | ◐ | ◐ |
| [blader/humanizer](https://github.com/blader/humanizer) | 51757 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ | ✗ | ✗ | ✗ | ◐ | ✗ |
| [imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills) | 49352 | ◐ | ◐ | ✗ | ◐ | ✗ | ◐ | ✗ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ✓ |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 36678 | ✗ | ✗ | ◐ | ✗ | ◐ | ◐ | ◐ | ✗ | ◐ | ✗ | ✗ | ◐ | ✗ | ✗ | ◐ |
| [everyinc/compound-engineering-plugin](https://github.com/everyinc/compound-engineering-plugin) | 25243 | ◐ | ✗ | ◐ | ✗ | ◐ | ◐ | ◐ | ✗ | ✗ | ✗ | ◐ | ✓ | ✗ | ◐ | ◐ |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 4703 | ◐ | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ | ✗ | ◐ | ✓ | ✗ | ◐ | ✗ | ◐ | ◐ |
| [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) | 1598 | ◐ | ✗ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ✗ | ◐ | ◐ |
| [vibeeval/vibecosystem](https://github.com/vibeeval/vibecosystem) | 535 | ◐ | ✗ | ◐ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ | ✗ | ◐ | ✗ |
| [dsifry/metaswarm](https://github.com/dsifry/metaswarm) | 419 | ◐ | ✗ | ✗ | ✗ | ◐ | ◐ | ◐ | ◐ | ◐ | ✗ | ✗ | ◐ | ✗ | ◐ | ◐ |
| [socialpranker/deepdive](https://github.com/socialpranker/deepdive) | 377 | ◐ | ◐ | ◐ | ◐ | ✗ | ◐ | ◐ | ✗ | ◐ | ✗ | ✗ | ◐ | ✗ | ◐ | ◐ |
| [udaysharmadev/gravitas](https://github.com/udaysharmadev/gravitas) | 9 | ◐ | ◐ | ✗ | ✗ | ◐ | ✗ | ✗ | ✗ | ◐ | ✗ | ◐ | ◐ | ✗ | ◐ | ◐ |
| [vnmoorthy/groundtruth](https://github.com/vnmoorthy/groundtruth) | 7 | ✗ | ◐ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ | ◐ | ✗ | ✗ | ◐ |
| [aiimagined/godmode](https://github.com/aiimagined/godmode) | 6 | ◐ | ◐ | ◐ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ | ◐ | ◐ | ✗ | ◐ | ✓ |
| [mizcausevic-dev/evidence-labeling-protocol](https://github.com/mizcausevic-dev/evidence-labeling-protocol) | 0 | ◐ | ✗ | ◐ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| [edgebuildlabs/evidence-contracts](https://github.com/edgebuildlabs/evidence-contracts) | 0 | ◐ | ✗ | ◐ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ | ✗ | ✗ | ✗ |
| [aliradid/citation-needed](https://github.com/aliradid/citation-needed) | 0 | ◐ | ✗ | ✗ | ◐ | ✗ | ✗ | ◐ | ✗ | ✗ | ✗ | ✗ | ◐ | ✗ | ◐ | ◐ |

## Project By Project

### [obra/superpowers](https://github.com/obra/superpowers)

Stars 290959. License MIT. Last push 2026-09-22. Platform: Claude Code (primary), plus Codex, Gemini CLI, OpenCode, Kimi, Pi, Hermes, Devin, Muse, Antigravity.

A multi-harness skills pack for Claude Code and other agents (Codex, Gemini, OpenCode, Antigravity, and more). It covers a software-development workflow: brainstorming, then worktrees, plans, subagent-driven development with task reviewers and a capped fix loop, TDD, systematic debugging, and verification-before-completion. A SessionStart hook injects the using-superpowers bootstrap.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | skills/verification-before-completion/SKILL.md says evidence must come before claims. Its 'Common Failures' table ties each claim to a required evidence type, e.g. 'Tests pass' needs 'Test command output: 0 failures'. There are no tier labels, no provenance slots and no downgrade rule. diagnosing-superpowers/SKILL.m... |
| F2 Transcript audit | ✗ | No script compares claims against the tool-call transcript. The diagnosing-superpowers skill has subagents read transcripts, but only to analyse sessions, not to audit evidence labels. |
| F3 Proxy test | ◐ | The verification skill's 'Not Sufficient' column is close to proxy-trap thinking: 'Linter passing' does not prove 'Build succeeds', and 'Tests passing' does not prove 'Requirements met'. It does not name a general doctrine and it covers code only. |
| F4 Non-code fields | ✗ | All guidance is about software (tests, builds, linters, VCS diffs). None of the skill files I opened cover law, mathematics, medicine or other fields. |
| F5 Read-only verifiers | ◐ | skills/subagent-driven-development/task-reviewer-prompt.md dispatches a 'Subagent (general-purpose)' and says in prose 'Your review is read-only on this checkout'. Read-only is an instruction, not a tool list. The repo tree has no agent definitions with restricted tools. |
| F6 Vote ledger | ✗ | There is one reviewer per task and no refuters or voting. The SDD 'ledger' is a text log the orchestrator appends by instruction ('Task <N>: fix round <R>/5 ...'). No script deduplicates findings or tallies votes. |
| F7 Stop rules | ◐ | subagent-driven-development/SKILL.md sets fixed loop numbers: 'Five rounds maximum per task'. Rounds 1-3 resume the implementer, rounds 4-5 use a fresh implementer on a stronger model, and a breaker fires at round 5. There is no completeness critic and no loop-until-dry fan-out. |
| F8 Visual gates | ✗ | Brainstorming has a visual companion server (skills/brainstorming/scripts/server.cjs) for showing mockups to the user. It is not an acceptance gate with a fresh critic. |
| F9 Iteration research | ◐ | The fix loop is capped at 5 rounds, and each round re-runs tests and gets a scoped re-review, which is an external signal. None of the files I opened cite self-correction research. |
| F10 Prose script | ✗ | No prose-scoring script. The scripts/ folder holds only bump-version, lint-shell and codex packaging/sync scripts. |
| F11 Platform findings | ◐ | skills/diagnosing-superpowers files session evidence as GitHub issue bundles (references/github-issues.md, templates/issue.md), but the reports go to superpowers itself, not the host platform. There are per-harness tests such as tests/antigravity/test-antigravity-tools.sh. I found no findings stamped with a version... |
| F12 Triage gate | ✗ | It does the opposite of a triage gate. using-superpowers/SKILL.md line 11 says 'If you think there is even a 1% chance a skill might apply ... you ABSOLUTELY MUST invoke the skill.' The explicit-skill-requests tests check that skills trigger, not that they stay quiet on trivial requests. |
| F13 Translations | ✗ | No translated skill files in the tree. The docs/README.kimi.md and README.opencode.md files are per-harness docs, not translations. |
| F14 Validator | ◐ | There are structure tests (tests/diagnosing-superpowers/test-skill-structure.sh, tests/codex/test-marketplace-manifest.sh, tests/kimi/test-plugin-manifest.sh) and a shell linter (scripts/lint-shell.sh). There is no general lint for skills and agents covering BOMs, description length, dead references or critics with... |
| F15 Baited tests | ◐ | skills/systematic-debugging/test-pressure-1..3.md are baited pressure scenarios, e.g. a production outage costing '$15,000/minute' pushing toward a quick retry fix. writing-skills/testing-skills-with-subagents.md sets out pressure-testing methods. I found no planted-defect audit case with an answer key. Skill-behavi... |

Enforced by code rather than instructions:

- The SessionStart hook (hooks/hooks.json, hooks/session-start) injects the using-superpowers bootstrap on startup, clear and compact
- Helper scripts for the subagent-driven-development workflow (scripts/sdd-workspace, task-brief, review-package) build the diff and brief files that reviewers read
- executing-plans/scripts/task-start and task-done
- Shell tests covering hooks, plugin manifests, version bumps, the codex sync, and skill triggering via headless runs (tests/explicit-skill-requests)
- Everything else is enforced by instruction only: verification-before-completion, reviewer read-only status, the 5-round fix cap, and ledger entries

What it does better than Gravitas:

- Much larger reach and many more harnesses: ports and tests for Claude Code, Codex, Gemini, OpenCode, Kimi, Pi, Hermes, Devin, Muse and Antigravity
- An end-to-end development workflow (brainstorm, then plan, then subagent-driven development, then finish the branch) with concrete per-task review dispatch and a model-escalation fix loop (rounds 4-5 move to a fresher, stronger model), which is well specified
- Detailed rationalization-prevention tables and red-flag lists in each skill
- Pressure-scenario tests built around human-style temptations, plus a documented method for testing skills with subagents
- The diagnosing-superpowers skill: session-transcript forensics with path:line citations, parallel analyst subagents, redaction policy and GitHub issue templates
- Cost awareness: reviewer prompts require an explicit model choice and forbid nested reviewer spawning

### [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent)

Stars 248564. License MIT. Last push 2026-09-24. Platform: Hermes Agent (NousResearch), Python skill for linux/macos/windows.

A research skill bundled with Hermes Agent. A stdlib Python ledger script (sources.py) owns the url-to-[n] citation mapping. It registers sources at retrieval time, renders the Sources block, and verifies drafts: unknown ids, a Sources block that disagrees with the ledger, a minimum coverage level, and an evidence gate. An optional fact-checking mode only accepts a quote that appears verbatim in the saved page text.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | SKILL.md: every sourced claim carries an inline [n] from the ledger, and claims from model knowledge must be marked '[unverified]'. In fact-check mode each source gets a verbatim quote, and `quote` rejects text that is not in the evidence file. That gives two provenance levels (cited-with-quote versus unverified), n... |
| F2 Transcript audit | ◐ | sources.py verify checks the draft's [n] ids against the ledger, and `quote --from page.txt` checks quotes against saved page text. Neither looks at a tool-call transcript. Nothing mechanically confirms that a registered URL was actually fetched: the rule against citing a search snippet ('Citing a search snippet as... |
| F3 Proxy test | ✗ | No proxy-trap doctrine. The nearest thing is the pitfall about using [unverified] as an escape hatch. |
| F4 Non-code fields | ◐ | Fact-Checking Mode names 'medical, legal, financial, safety, disputed claims' and requires a second independent source for disputed facts. It does not name a field-specific check for each domain. |
| F5 Read-only verifiers | ✗ | No verifier subagents. Parallel subagents are mentioned only as a way to share one ledger via --ledger. |
| F6 Vote ledger | ✗ | The ledger deduplicates URLs (normalize_url, idempotent add) but has no refuters, votes or rounds. |
| F7 Stop rules | ✗ | There is a multi-platform sweep table with no fixed numbers and no stopping rule. `verify --min-coverage` is a citation-density gate, not a completeness critic. |
| F8 Visual gates | ✗ | None. |
| F9 Iteration research | ✗ | None. |
| F10 Prose script | ✗ | No prose scorer. verify only warns on more than 3 ids per sentence. |
| F11 Platform findings | ✗ | None. |
| F12 Triage gate | ◐ | SKILL.md 'When to Use' says to skip citations for incidental lookups, casual conversation and creative writing. This is instruction only, with no control-case tests. |
| F13 Translations | ✗ | English only. |
| F14 Validator | ✗ | No validator was found in the files opened (SKILL.md, sources.py, the tests). |
| F15 Baited tests | ◐ | tests/skills/test_grounded_citations_skill.py has unit tests with planted bad inputs, including test_unknown_citation_id_fails, test_sources_block_url_must_match_ledger, test_quote_rejects_paraphrase and test_verify_evidence_gate_requires_quotes. There is no agent-level baited case and no audit answer key. |

Enforced by code rather than instructions:

- sources.py quote: the quote must appear verbatim in the --from evidence text after normalising whitespace, case and markdown, and must be at least 3 words, otherwise SystemExit
- sources.py verify: exits non-zero on citation ids missing from the ledger, a missing Sources block, or a Sources block whose URLs or ids disagree with the ledger
- verify --min-coverage: fails when the share of prose sentences with [n] or [unverified] falls below the threshold
- verify --evidence: fails if any cited source has no attached quote
- verify --strict: turns warnings (such as more than 3 ids per sentence or uncited sources) into failures
- Ids are assigned by the ledger and are stable (URL-normalised, idempotent add, cross-process lockfile)

What it does better than Gravitas:

- Checks quotes against the fetched page text itself, with a markdown-aware matcher, so a paraphrase or misremembered figure cannot be attached as evidence. Gravitas's URL-plus-quoted-line slot is only audited against the transcript.
- The ledger assigns citation numbers, so the model only emits integers it was given. This removes invented URLs by construction, and render generates the Sources block mechanically.
- Declared-provenance coverage metric (--min-coverage) counting both [n] and [unverified], a numeric gate on how much of the prose has declared provenance
- A lockfile lets parallel subagents share one ledger
- Rendering to several output formats (markdown, footnotes, bibtex, evidence block), with idempotent --replace-in for a draft file
- The verify and quote logic has fairly thorough pytest unit coverage

### [garrytan/gstack](https://github.com/garrytan/gstack)

Stars 134064. License MIT. Last push 2026-09-24. Platform: .

Garry Tan's Claude Code skill pack: about 40 slash-command skills written as Markdown templates (office-hours, plan reviews, /review, /qa, /design-review, /ship, /cso and others). They are generated by scripts/gen-skill-docs.ts, drive a real browser (Aside or a bundled one) for QA and screenshots, and ship with a large Bun test and eval suite plus CI workflows.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | review/SKILL.md.tmpl 'Verification of claims' says never write 'likely handled': verify it or flag it as unknown, and a finding must 'cite evidence it IS fine, or flag it as unverified'. Findings carry evidence_paths. There is no tier taxonomy and no provenance slot per label. |
| F2 Transcript audit | ✗ | Nothing in the files I opened compares evidence labels with a tool-call transcript. lib/review-evidence.ts fingerprints evidence_paths so they can be re-read later. It does not audit whether they were read. |
| F3 Proxy test | ✗ | There is no proxy-trap doctrine. The closest thing is the review 'Rationalization prevention' line. |
| F4 Non-code fields | ✗ | All skills are about software, product and design. None covers law, mathematics, medicine or similar fields. |
| F5 Read-only verifiers | ✗ | review/SKILL.md.tmpl allowed-tools includes Edit, Write and Agent. Specialists such as review/specialists/red-team.md are prompt files, not agents with a restricted tool list. agents/ holds only openai.yaml. |
| F6 Vote ledger | ◐ | review/sections/adversarial.md.tmpl runs an adversarial pass (a red-team specialist, plus codex challenge-mode) and persists findings as fingerprint path:line:category records. There are no refuters that default to refuted, no majority vote and no vote-tallying ledger script. |
| F7 Stop rules | ◐ | adversarial.md.tmpl: a pass 'converges only when it completes without edits. Allow at most 3 fix cycles', else persist converged:false. Specialist dispatch is recorded. There is no separate completeness critic and no fan-out numbers per scale. |
| F8 Visual gates | ◐ | design-review/SKILL.md.tmpl takes before/after screenshots and runs `$D verify --mockup ... --screenshot ...` to compare the fix with a generated target mockup. It also computes a design score and an AI slop score. It does not use a fresh critic isolated from the source. |
| F9 Iteration research | ◐ | The 3-fix-cycle cap and the 'converged' flag rely on re-running the diff as an external signal. No research is cited. |
| F10 Prose script | ◐ | The review Step 3.5 runs `bun run slop:diff` (slop-scan, configured by slop-scan.config.json) on changed code. It is advisory and never blocking, and it targets AI code patterns, not prose. |
| F11 Platform findings | ✗ | I found no version-stamped platform experiments filed upstream. |
| F12 Triage gate | ◐ | Some gating exists: the review specialists record {dispatched:false, reason:'scope\|gated'}, and preamble-tier appears in the frontmatter. I saw no triage gate tested with control cases. |
| F13 Translations | ✗ | The skills are English only. |
| F14 Validator | ◐ | scripts/skill-check.ts validates YAML frontmatter, requires non-empty name and description, checks that the openai.yaml fields are present, and checks that generated skills are fresh against their templates. I saw no checks for BOMs, dead references, hang-prone tools or critics with write tools. |
| F15 Baited tests | ◐ | test/ holds hundreds of *.test.ts files, including fixtures such as autoplan-dual-voice-fixture and auto-decide-fixture, plus LLM eval workflows (.github/workflows/evals.yml). I did not find a planted-defect audit case with an answer key. |

Enforced by code rather than instructions:

- freeze/SKILL.md.tmpl PreToolUse hooks on Edit and Write run freeze/bin/check-freeze.sh, which blocks edits outside the allowed directory
- careful/SKILL.md.tmpl PreToolUse hook on Bash runs careful/bin/check-careful.sh to warn on destructive commands
- allowed-tools lists in each skill's frontmatter (for example, freeze allows only Bash, Read and AskUserQuestion)
- scripts/skill-check.ts validates frontmatter and the freshness of generated skills, run in CI (.github/workflows/skill-docs.yml)
- lib/review-evidence.ts computes shared-lib fingerprints, which the review revalidates
- slop-scan via bun run slop:diff (advisory only)

What it does better than Gravitas:

- Real browser-driven QA: /qa and /design-review drive a browser, capture before/after screenshots and console errors for each fix, and classify each fix as verified, best-effort or reverted
- Visual diff of the fix result against a generated target mockup ($D verify --mockup --screenshot)
- Runtime guardrail hooks (freeze, careful) that block or warn on actual tool calls
- Skills are generated from templates and checked for freshness in CI, and the same skills are exported to several hosts (Claude Code, Codex/OpenAI, OpenClaw)
- A far larger automated test and eval suite, with CI workflows for Windows and cross-platform
- End-to-end shipping workflow coverage (plan reviews, ship, land-and-deploy, canary, retro) that goes beyond verification

### [blader/humanizer](https://github.com/blader/humanizer)

Stars 51757. License MIT. Last push 2026-09-06. Platform: Agent-agnostic Markdown skill (skills.sh CLI, Claude Code plugin, Claude Desktop, OpenAI/Codex agents via agents/open....

A single Markdown skill (SKILL.md v3.0.0, max 400 lines) that tells an agent how to rewrite AI-sounding prose. It uses a numbered catalogue of structural and lexical tells based on Wikipedia's "Signs of AI writing", a mark/draft/check/final workflow, voice matching and a no-fabrication rule. It ships as a skills.sh package and a Claude Code plugin, with a package-consistency validator script and a CI workflow.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ✗ | SKILL.md has no evidence labels or provenance slots. It only tells the agent not to add facts: "Do not add a fact, name, number, date, quote, or citation unless it comes from the source or the user." |
| F2 Transcript audit | ✗ | The only script is scripts/validate-package.py, which checks package files. Nothing audits a tool-call transcript. |
| F3 Proxy test | ✗ | There is no proxy-trap doctrine in SKILL.md or README.md. |
| F4 Non-code fields | ✗ | SKILL.md is about prose editing only. It mentions legal/technical text only as a voice register ("Reference, technical, legal, and factual text stays neutral and plain"), not as a way to verify anything. |
| F5 Read-only verifiers | ✗ | agents/openai.yaml is only interface metadata (display_name, short_description, default_prompt). There are no subagents and no tool lists. |
| F6 Vote ledger | ✗ | There are no refuters, votes or ledger script. |
| F7 Stop rules | ✗ | There is no completeness critic or loop-until-dry rule. The workflow is one fixed pass: mark, draft, check, final. |
| F8 Visual gates | ✗ | There is no rendered-output gate. The check step is self-review: "Read it aloud. Ask what still sounds AI-generated." (SKILL.md) |
| F9 Iteration research | ✗ | There is no self-correction research and no pass cap. It has one fixed draft-then-final cycle in SKILL.md 'How to work'. |
| F10 Prose script | ◐ | SKILL.md has a detailed standard for structural prose tells: numbered patterns ranked strongest first, §1-§5 act on one sighting, 'weak alone' patterns need other tells, and a final search for five surviving tells. The standard is applied by the model only. No script scores prose. |
| F11 Platform findings | ✗ | There are no platform experiments or upstream bug reports. The README only states a version floor: "Claude Code 2.1.142 or newer can install the plugin". |
| F12 Triage gate | ✗ | There is no triage gate or control cases. Triggering depends only on the frontmatter description. |
| F13 Translations | ✗ | There are no translation files in the repo (root: SKILL.md, README.md, AGENTS.md, agents/, scripts/, .claude-plugin/, .github/). SKILL.md only says "The formula appears in every language". |
| F14 Validator | ◐ | scripts/validate-package.py lints this one package. It requires YAML frontmatter and rejects the fields version:, compatibility: and allowed-tools:. It checks that versions match across SKILL.md, README and plugin.json, that there is a single root SKILL.md, that patterns are numbered without gaps and match the READM... |
| F15 Baited tests | ✗ | There is no test suite or baited cases. The only automated check is the package validator; .github/workflows/validate.yml is presumed to run it. |

Enforced by code rather than instructions:

- scripts/validate-package.py: YAML frontmatter present; the fields version/compatibility/allowed-tools are banned at the top level
- scripts/validate-package.py: one version across SKILL.md metadata, README changelog and plugin.json
- scripts/validate-package.py: exactly one regular (non-symlink) SKILL.md at the root, and plugin.json skills == ['./']
- scripts/validate-package.py: patterns numbered 1..N without gaps, matching the README tables and the 'The N patterns' heading
- scripts/validate-package.py: SKILL.md has 400 lines or fewer
- All rewriting rules (tells, no fabrication, voice matching, file mode that keeps code unchanged) are instructions only, with no code enforcement

What it does better than Gravitas:

- Explains why the tells occur: the model picks the most probable option, which suits the widest range of readers. Each pattern is framed as a form of that default, which makes the catalogue easier to generalise than a list of banned markers.
- Ranks tells by strength, with explicit thresholds: §1-§5 justify an edit on one sighting, and 'weak alone' patterns need other tells nearby. This is a clear rule for avoiding false positives.
- Has an explicit fidelity check on rewrites: no added or dropped fact, name, number, date, quote, citation, ranking or simultaneity claim. It names the pattern edits (§6, §9, §19) that most often drop them.
- Supports voice matching from a user sample, and the sample overrides the pattern rules (for example, dashes are kept at the writer's rate).
- Has distinct output modes (pasted, file, embedded). File mode edits only prose and leaves code, paths, YAML and link targets unchanged.
- Very wide adoption and simple distribution: about 51.8k stars, one portable Markdown file, installed via skills.sh or the Claude plugin marketplace.

### [imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills)

Stars 49352. License CC BY-NC 4.0 per the README badge (gh licenseInfo reports "Other" / NOASSERTION). Last push 2026-09-24. Platform: Claude Code (plugin marketplace; symlink install also supported).

Claude Code plugin (v3.22.1) with four skills (deep-research, academic-paper, academic-paper-reviewer, academic-pipeline), about 40 agent prompts and a large Python lint/CI layer. It runs a staged pipeline from research to publication, with integrity gates at Stages 2.5 and 4.5, citation-anchor provenance markers, and an opt-in claim-to-source faithfulness audit (ARS_CLAIM_AUDIT=1) that judges each cited claim against the retrieved reference text.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | The labels cover citations, not every claim. Each in-text citation must carry <!--ref:slug--> plus <!--anchor:<kind>:<value>-->, and anchor_kind=none is gate-refused. The audit gives each claim SUPPORTED/UNSUPPORTED/AMBIGUOUS/RETRIEVAL_FAILED and requires 'cite the retrieved excerpt by section/page/quote' (academic-... |
| F2 Transcript audit | ◐ | scripts/claim_audit_pipeline.py runs the audit with dependency-injected retrieve_fn/judge_fn, and RETRIEVAL_FAILED is emitted when retrieval returned nothing ('DO NOT claim to have read a paper the retrieval layer did not actually return'). This checks claims against the retrieved source text. It never checks eviden... |
| F3 Proxy test | ✗ | The only hits for 'proxy trap' or 'Goodhart' are deep-research/references/logical_fallacies.md and eval run logs. There is no cross-domain proxy-trap doctrine. |
| F4 Non-code fields | ◐ | academic-paper/references/domain_evidence_profiles.md, statistical_reporting_standards.md, equator_reporting_guidelines.md, risk_of_bias_agent and a GRIMMER statistical-consistency case cover academic fields, especially medicine and statistics. I found no per-field map of which independent check exists for law, math... |
| F5 Read-only verifiers | ✗ | Only six agent files declare tools, and each one is 'tools: Read, Write, Edit, Grep, Glob' (agents/*.md, deep-research/agents/*.md). Reviewer and audit agents such as devils_advocate_reviewer_agent.md have no tools line, so any read-only behaviour comes from instructions. I saw no context isolation. |
| F6 Vote ledger | ◐ | There is a Devil's Advocate reviewer ('You only challenge', academic-paper-reviewer/agents/devils_advocate_reviewer_agent.md) and a multi-reviewer panel synthesised by an editorial agent. I saw no default-refuted voting and no ledger script that deduplicates findings, tallies votes or counts dry rounds. |
| F7 Stop rules | ✗ | I found no completeness critic and no loop-until-dry rule with fixed fan-out numbers. Revision rounds exist (re_review_mode_protocol.md), but not at named scales. |
| F8 Visual gates | ◐ | academic-paper/references/vlm_figure_verification.md describes an optional VLM critic that checks the rendered figure 'against the paper's data'. The critic sees the source data, so it is not a fresh critic, and the check is enforced only by instructions. |
| F9 Iteration research | ◐ | The README cites Ren et al. 2026 (a survey of self-improving agents) on discovery agents' inability to verify their own work, and the design leans on human-in-the-loop checkpoints and external retrieval. I found no explicit rule set with a pass cap derived from self-correction research. |
| F10 Prose script | ◐ | academic-paper/references/writing_quality_check.md is a checklist of flagged terms and patterns, 'non-blocking prompts for judgment, not ... a pass/fail score'. No script scores the prose. |
| F11 Platform findings | ◐ | The audits/ folder holds dated, model-stamped harness-retirement audits (e.g. harness-retirement-2026-09-opus-5-5.md) and a model bake-off. hooks/run_guard.sh documents Windows platform behaviour (#454). These concern its own issues; I found no upstream bug filings to Claude Code. |
| F12 Triage gate | ◐ | There is mode selection and a mode advisor (academic-pipeline/references/mode_advisor.md, mode_selection_guide.md) and an intake agent. I saw no triage gate tested with trivial control cases, although a clean-control manuscript exists for the reviewer. |
| F13 Translations | ◐ | README.zh-CN/zh-TW/ja-JP/ko-KR/es-ES.md (333-363 lines against 379 for the English README) plus docs/*.zh-TW.md. The SKILL.md files and agents are not translated. |
| F14 Validator | ◐ | scripts/check_skill_description_length.py enforces MAX_LENGTH = 1024; also check_command_frontmatter_name.py, check_agents_mirror_sync.py, check_skill_inventory_parity.py and _skill_lint.py (frontmatter vocabulary), all run in .github/workflows. I saw no BOM check, no check for hanging tool names and no check for cr... |
| F15 Baited tests | ✓ | evals/heldout/reviewer_seeded_defects: synthetic manuscripts with planted defects plus a clean control, and ground-truth manifests (manifests/ms01_quant.defects.json, 11 defects). evals/gold/citation_extraction mixes 30 valid, 16 fabricated and 5 manual-exempt citations. There are about 480 test files and pytest CI. |

Enforced by code rather than instructions:

- PreToolUse hook on Write\|Edit\|MultiEdit\|Bash (hooks/hooks.json -> hooks/run_guard.sh -> scripts/ars_write_scope_guard.py + ars_phase_scope_manifest.json) limits writes to each phase's scope. It fails open to a pass-through when Python is missing.
- Claim audit pipeline and finalizer as executable, tested Python (scripts/claim_audit_pipeline.py, claim_audit_finalizer.py, check_claim_audit_consistency.py), with calibration against a gold set (claim_audit_calibration.py).
- About 100 CI lint scripts run through .github/workflows (spec-consistency, pytest, command-invariants, test-count-monotonic, changelog-covers-merges, tag-version-match, freshness-check). They cover skill description length, frontmatter vocabularies, command...
- Bibliographic integrity signals script (scripts/bibliographic_integrity_signals.py) and API clients (arxiv_client.py, plus Crossref, OpenAlex and Semantic Scholar protocols) for checking that a reference exists.
- Eval threshold gate (scripts/_eval_threshold_gate.py) and the eval-harness workflow.

What it does better than Gravitas:

- Claim-to-source faithfulness against retrieved full text: each cited claim is judged against the actual reference text, with defect stages (source_description, citation_anchor, synthesis_overclaim, negative_constraint_violation). Paywall failures are kept separate from tool failures.
- Per-citation locator anchors (ref slug plus anchor kind/value) attached at write time. A citation with no anchor is refused at a hard formatter gate.
- Calibrated gold sets: 51 citation tuples including fabricated DOIs and arXiv IDs, plus field-norm and RQ-framing gold sets with manifests.
- Much larger CI surface: about 100 check scripts and about 480 test files across many workflows, including test-count-monotonic and changelog coverage.
- Writes during a phase are limited by a runtime PreToolUse hook, not only by instructions.
- Domain depth for academic work: PRISMA and systematic-review protocols, EQUATOR reporting guidelines, risk of bias, IRB decision tree, and scholarly API protocols (Crossref, OpenAlex, Semantic Scholar, arXiv, Chinese literature).

### [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

Stars 36678. License Apache-2.0. Last push 2026-09-24. Platform: Claude Code (plugins: skills, commands, agents, Workflow JS scripts).

Anthropic's official Claude Code plugin marketplace. The three plugins examined are: math-olympiad, a skill that runs parallel solvers, strips their reasoning before fresh-context adversarial verifiers see the proof, holds an asymmetric vote with early exit, and abstains when unsure; code-modernization, with agents and Workflow JS scripts such as harden-scan.js, which uses per-class finders, a code-level dedup, one refuter per finding and a second judge for Critical/High; and code-review, a slash command that runs 5 parallel reviewers, has a Haiku agent score each issue for confidence and filters out anything below 80.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ✗ | There are no evidence tiers with provenance slots. The closest things are code-review.md, which says 'You must cite and link each bug' with a full-SHA line link, and the harden-scan.js schema, which requires source 'repo-relative path:line'. |
| F2 Transcript audit | ✗ | No script checks claims against the tool-call transcript. |
| F3 Proxy test | ◐ | The mechanism is domain-specific and not framed as a proxy-trap doctrine. math-olympiad SKILL.md: 'A correct answer from flawed reasoning is a failure' and 'a pattern that fits n≤10 but fails at n=100 is not a proof'. The agents and harden-scan.js say 'A claim is only real if the executable code exhibits it', and a... |
| F4 Non-code fields | ✗ | Coverage is limited to competition math and code. Nothing covers law, medicine, statistics, history or physics. |
| F5 Read-only verifiers | ◐ | code-modernization/agents/architecture-critic.md and security-auditor.md declare 'tools: Read, Glob, Grep, Bash'. There is no Write or Edit, but Bash can write, so read-only status depends on the instruction 'You are read-only: never create or modify files'. math-olympiad SKILL.md admits 'The Agent tool cannot enfor... |
| F6 Vote ledger | ◐ | math-olympiad has an asymmetric vote with pigeonhole exit: '2 say HOLE FOUND → refuted, stop', '4 say HOLDS → confirmed'. harden-scan.js deduplicates findings in code ('raw findings → deduped'), runs one refuter per finding and adds a second judge for Critical/High, with split verdicts sent to human triage. code-rev... |
| F7 Stop rules | ◐ | Fan-out numbers are fixed: 8-12 attempt agents, 5 verify passes, 'Up to 3 revise cycles', and a per-model tier table (e.g. Opus: 3 solvers, 5 verify passes, abstain after 4 revise fails). code-review uses 5 reviewers. There is no completeness critic and no loop-until-dry rule. |
| F8 Visual gates | ✗ | No rendered-output critic. math-olympiad only compiles LaTeX with scripts/check_latex.sh and compile_pdf.sh. |
| F9 Iteration research | ◐ | SKILL.md cites research: the Yang-Huang structure ('85.7% on IMO') and the Aletheia case study ('50 of 63'). Solver self-refinement is capped: 'Up to 5 rounds', 'Stop: Self-verify passes twice clean'. The external signal is the fresh verifier. It does not cite self-correction-limits literature. |
| F10 Prose script | ✗ | No prose-scoring script. |
| F11 Platform findings | ✗ | No version-stamped platform experiments or upstream bug filings. The only related item is an observed platform limit in SKILL.md: 'The Agent tool cannot enforce tool restriction'. |
| F12 Triage gate | ◐ | code-review.md step 1 has a Haiku agent skip closed, draft, automated or 'very simple and obviously ok' PRs, and step 7 repeats the check. math-olympiad evals/trigger_eval.json lists trigger queries including 10 should_trigger:false controls. These controls test skill activation, not over-triggering of the full mach... |
| F13 Translations | ✗ | English only. |
| F14 Validator | ✗ | The three plugins contain no validator. A repo-wide validator was not examined. |
| F15 Baited tests | ◐ | The only test file found is math-olympiad/skills/math-olympiad/evals/trigger_eval.json, a set of trigger and non-trigger queries. There is no planted-defect audit case with an answer key. |

Enforced by code rather than instructions:

- code-review.md frontmatter allowed-tools limits the command to specific gh subcommands (gh pr diff/view/comment, gh issue view/list, gh search)
- code-modernization agent tool lists (Read, Glob, Grep, Bash) leave out Write and Edit, but Bash still allows writes
- harden-scan.js checks the system name with a regex, deduplicates findings in code, runs the refute and confirm phases as scripted agent() calls with JSON verdict schemas, and computes falsePositiveRate
- harden-scan.js fence() strips untrusted-fence markers from finder output before it goes into judge prompts
- math-olympiad scripts/check_latex.sh and compile_pdf.sh gate PDF output on pdflatex being available
- Everything else is instruction-only, including solver/verifier tool bans (the skill states the Agent tool cannot enforce them), vote thresholds and the code-review score filter

What it does better than Gravitas:

- Stripping reasoning before verification: the math verifier sees only the problem and the cleaned proof, so the solver's thinking trace cannot bias it toward agreement.
- Asymmetric voting with pigeonhole early exit (4 to confirm, 2 to refute) stops launching verifiers once the outcome is decided, which saves calls.
- A named, domain-specific catalogue of attack patterns (e.g. #4 'does this prove RH?', #40 extracting the general lemma and looking for a 2x2 counterexample) instead of a generic 'check logic'.
- Verification is orchestrated by executable Workflow JS (harden-scan.js) with JSON schemas, code-level dedup and a second judge on Critical/High.
- Explicit prompt-injection defences: untrusted-content fencing in code, and a rule that instruction-shaped text in the code under review is reported as a finding.
- Mandatory credential masking in findings output.

### [everyinc/compound-engineering-plugin](https://github.com/everyinc/compound-engineering-plugin)

Stars 25243. License MIT. Last push 2026-09-23. Platform: Claude Code plus 13 other hosts (Cursor, Codex, Antigravity, and others).

A plugin of 36 skills (README) for 14 agent hosts, including Claude Code, Cursor, Codex and Antigravity (.agy/). It runs an engineering loop: brainstorm, plan, work, review, then write the learnings down (ce-compound). Its main verification piece is ce-code-review. That skill sends persona reviewers out in parallel (correctness, security, adversarial, and others), can add a cross-model adversarial peer, runs a script that merges findings deterministically, and ends with an independent validator subagent. It is aimed at code only.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | skills/ce-code-review/references/subagent-template.md: findings use discrete confidence anchors 0/25/50/75/100. A 'Quote-the-line gate' says that at 75+ the first evidence item must be the verbatim line with file:line: 'If you cannot quote the motivating line, you cannot claim 75+ - step down to 50'. The labels are... |
| F2 Transcript audit | ✗ | No script compares claims with the tool-call transcript. findings-mechanics.py only checks that first_evidence is a non-empty string (nonempty_string). It never checks that the quoted line exists or that the file was opened. |
| F3 Proxy test | ◐ | personas/adversarial-reviewer.md has a 'Silent-pass verification mechanism' rule for diffs 'whose failure mode is going green while the real thing is red' (CI gates, coverage/lint gates, test mocks). review-scope.py names silent_pass_classes (tested in ce-code-review-mechanics.test.ts). This covers code and CI only,... |
| F4 Non-code fields | ✗ | Every verifier artifact I opened is about code review. validator-batch-template.md lists protected subjects: memory-safety, concurrency, injection, cryptography and so on. None of them covers law, medicine, mathematics or history. |
| F5 Read-only verifiers | ◐ | validator-batch-template.md says 'inspect ... with read-only tools', but this is an instruction. subagent-template.md even lets reviewers write their own JSON: 'This is the ONE write operation you are permitted to make'. dispatch-reviewers.md: 'Omit the mode parameter ... so the user's configured permission settings... |
| F6 Vote ledger | ◐ | skills/ce-code-review/scripts/findings-mechanics.py is deterministic. It validates the schema, deduplicates exact fingerprints on (file, line, normalised title), demotes findings at 75+ with no first_evidence to 50, suppresses anything below 75, and raises confidence only when 2+ independent reviewers, one of them a... |
| F7 Stop rules | ◐ | Fan-out is sized by a depth gate (lite, focused or full; the fixed numbers are in the adversarial persona: Quick <50 lines, Standard 50-199, Deep 200+). The validator batch has a fixed cap: 'Eight findings is the normal cap', with a budget of 15 minutes and about five tool calls per finding. There is a Plan Requirem... |
| F8 Visual gates | ✗ | The review skills have no perceptual gate that judges rendered output with a fresh critic. ce-test-browser exists, but I did not see a gate there where a critic who never saw the source judges the output. |
| F9 Iteration research | ✗ | The files I opened cite no self-correction research. The budget caps in the validator template are operational and not tied to research. |
| F10 Prose script | ✗ | The tree has no script that scores machine-generated prose. |
| F11 Platform findings | ◐ | docs/plans/*-eval-report.md are dated eval reports on the plugin's own skills, for example 2026-09-09-review-autonomy-live-eval-report.md. docs/solutions/ holds learnings. I found no version-stamped findings about the host platform being filed upstream. |
| F12 Triage gate | ✓ | modes-and-output.md defines a 'Review depth gate' with lite, focused and full paths, plus floors that 'cannot be talked down'. The code side lives in scripts/review-scope.py (hard_block_full, silent_pass_classes). tests/ce-code-review-mechanics.test.ts has control cases, such as 'scope helper leaves a 40-line execut... |
| F13 Translations | ✗ | The tree has no translated skill files. It is ported to 14 hosts instead (.agy, .cursor-plugin, .codex-plugin and others). |
| F14 Validator | ◐ | scripts/release/validate.ts checks that release metadata and agent/skill counts are in sync. There are tests for converters, the Codex skill prompt budget (codex-skill-prompt-budget.test.ts) and bundled-script line endings. ce-compound-refresh has validate-frontmatter.py and validate-doc-claims.py for learning docs.... |
| F15 Baited tests | ◐ | There is a large bun test suite (tests/*.test.ts), including ce-code-review-mechanics.test.ts, which tests the scope helper and merge mechanics. Eval corpora are discussed in docs/solutions/skill-design/authored-eval-corpora-contain-the-happy-path.md. I did not find baited cases or a planted-defect case with an answ... |

Enforced by code rather than instructions:

- findings-mechanics.py: schema and enum validation, exact-fingerprint dedup, a 75+ finding with no first_evidence demoted to 50, suppression below 75, promotion only when independent cross-model reviewers agree, with fast-pass excluded
- review-scope.py: depth-gate facts (hard_block_full floors for migrations and large executables, silent_pass_classes for CI workflow paths), covered by tests/ce-code-review-mechanics.test.ts
- run-log.py: records stage timing and receipts
- scripts/release/validate.ts: release metadata and agent/skill count consistency, run in CI (.github/workflows/ci.yml)
- ce-compound-refresh/scripts/validate-frontmatter.py and validate-doc-claims.py (tested by tests/doc-claims-validator.test.ts)

What it does better than Gravitas:

- Runs on many more hosts: 14, with converters and tests for each (Claude Code, Cursor, Codex, Antigravity .agy, and others). Gravitas targets Antigravity only.
- Evidence is tied to a machine-checkable schema (findings-schema.json plus findings-mechanics.py). Only a script-merged finding with a quoted first_evidence line can reach an actionable confidence level.
- Promotion depends on reviewers being truly independent: agreement between in-process personas, or with the orchestrator's own fast pass, is excluded in code, and only agreement that includes an independence-verified cross-model peer counts.
- The validator follows a protected-subject policy: rejecting a security, data-loss or concurrency finding requires refuting evidence, and uncertain ones return 'unresolved' instead of being dropped.
- The size and risk depth gate is mostly deterministic: review-scope.py floors that cannot be argued down, with many unit tests.
- It saves what was learned from each change as reusable docs (ce-compound), which grows project knowledge over time. Gravitas has no equivalent.

### [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)

Stars 4703. License MIT. Last push 2026-09-24. Platform: Cross-agent (agentskills.io SKILL.md): Claude Code/Cowork plugin, Codex/ChatGPT plugin, Cursor rule, OpenClaw, Hermes....

A portable agentskills.io skill (Claude Code, Cowork plugin, Codex/OpenAI plugin, Cursor rule, Hermes) that audits and rewrites prose to remove AI-writing patterns. It has three modes (rewrite, detect, edit), a two-pass editing ceiling, a 74-category pattern catalogue with a tiered word table, and a dependency-free JS detector with CLI, CI gate, pre-commit hook and GitHub Action. It also ships a preservation validator, a quote normaliser, a house-style checker, a skill router with a graph validator, and a rewrite eval harness.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | SKILL.md requires a Verification block that states which checks "actually ran, whether they were deterministic or model-only". It also says a check that could not run must be labelled model-only and not called verified (lines ~234-240). This is a two-level executed/model-only split with no per-claim labels and no pr... |
| F2 Transcript audit | ✗ | No script compares labels against a tool-call transcript. detector/validate.js compares the original text with the rewrite, not claims with the tool calls that ran. |
| F3 Proxy test | ✗ | No proxy-trap doctrine found. The closest thing is the gate's "never uses the composite 0-100 score" (bin/avoid-ai-writing-gate.js) and the 1A/1B split so wordiness fixes are not read as AI evidence (README). Both are specific to writing. |
| F4 Non-code fields | ✗ | Covers prose only. Its scope is writing contexts (linkedin, blog, docs, investor-email), not verification in other fields. |
| F5 Read-only verifiers | ✗ | There are no subagent definitions with restricted tool lists. skills/preservation-verifier and skills/false-positive-reviewer are ordinary SKILL.md files with routing contracts. Their agents/openai.yaml files are Codex skill metadata. |
| F6 Vote ledger | ✗ | No refuters, votes or dedup ledger. |
| F7 Stop rules | ◐ | SKILL.md sets a fixed stopping rule: at most two editing passes, stop early when "no justified in-scope edit remains", and report a Stop reason. There is no completeness critic and no fan-out. |
| F8 Visual gates | ✗ | No rendered or visual acceptance gate. |
| F9 Iteration research | ◐ | Pass cap: '--iterate never adds passes on top of that ceiling' (SKILL.md), and deterministic checks (detector, validate.js) act as external signals. It cites no self-correction research. |
| F10 Prose script | ✓ | detector/patterns.js scores 74 categories, including structural and rhythm checks. bin/avoid-ai-writing-gate.js fails when findings exceed a threshold (default 6). action.yml and .pre-commit-hooks.yaml run it before merge, and CI runs `npm run self-scan:check` on the repo's own docs (.github/workflows/detector-test.... |
| F11 Platform findings | ✗ | No host-platform findings stamped with version and date and filed upstream. evals/rewrite/reports/automated-stack-...-2026-09-16 are dated model eval runs, not platform bug reports. |
| F12 Triage gate | ◐ | There is a no-op rule: if no justified edit remains, copy the source unchanged and use 0 passes (SKILL.md). evals/rewrite/cases.json has 'clean' control cases with decision 'preserve'. This is about not over-editing, not a triage gate for the machinery. |
| F13 Translations | ✗ | README: rules are "calibrated for English". Other languages are only linked as independently maintained community adaptations. |
| F14 Validator | ◐ | skills/avoid-ai-writing-router/scripts/validate_connections.py "Fails closed on dangling nodes/edges, missing connection contracts, unbounded cycles". Other checks: scripts/validate-openai-plugin.py, check-pattern-count.sh (catalogue count in CI), sync-plugin-skill.sh drift check, verify-release-versions.js. It does... |
| F15 Baited tests | ◐ | Large test suite (patterns/validate/categories tests, fp-measure, detect-parity). evals/rewrite/cases.json has fixtures with claims, protected spans, allowed_edits and review_focus as an answer key (for example 'Do not add exponential backoff'). There are output-contract scenarios too (protected, source_instruction,... |

Enforced by code rather than instructions:

- Pattern detection and scoring: detector/patterns.js (deterministic regex and structural checks)
- Prose gate that fails above a findings threshold: bin/avoid-ai-writing-gate.js, exposed through action.yml and .pre-commit-hooks.yaml
- Rewrite preservation (code blocks, quotes, tables, URLs, numbers, heading count and nesting): detector/validate.js errors
- Quote and apostrophe normalisation against the original: scripts/normalize-quotes.js
- House-style mechanics check (exit 0/1/2): scripts/check-style.js
- Catalogue count matches the README claim (74): scripts/check-pattern-count.sh in CI

What it does better than Gravitas:

- Distribution: ships as an npm detector package, a GitHub Action, a pre-commit hook and an MCP detector. Installs on Claude Code, Cowork, Codex/ChatGPT, Cursor and Hermes, where Gravitas is Antigravity only.
- Its prose detector is far more developed than Gravitas's prose-measuring script: 74 catalogued categories, a 112-entry tiered replacement table, context profiles, and false-positive measurement against HC3/RAID corpora (fp-measure.js, dataset-hc3.js, dataset-raid.js).
- A deterministic preservation validator that checks a rewrite kept protected content (code, quotes, tables, URLs, headings). Gravitas has no equivalent for edits.
- Eval fixtures are licensed and provenance-tagged, with train/development splits and per-case claims and allowed edits, and dated multi-model eval runs are archived in the repo.
- Single-source-of-truth drift controls (.ssot.yaml, sync scripts, promo-drift workflow) keep the plugin, the dist file and the Cursor copies identical to the canonical skill.
- Much larger adoption: about 4.7k stars.

### [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)

Stars 1598. License MIT. Last push 2026-08-24. Platform: Claude Code (.claude/ skills, agents, rules, hooks in settings.json).

A large Claude Code project template for academic researchers in economics and statistics (slides, papers, R/Stata, replication). It ships about 60 skills, 19 agents, 8 hooks and about 20 Python and shell check scripts. Its core loop is to fan out forked reviewers, reduce their JSON findings through a deterministic gate, have a judge check for hallucinated findings, and repeat until two rounds find nothing new. A fresh-context claim-verifier handles Chain-of-Verification.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | .claude/skills/verify-claims/SKILL.md sorts each claim into verdict tiers (supported, contradicted, unverifiable), and every finding must carry `rule`, `evidence` and `failing_case` fields (.claude/references/finding-schema.json, enforced by scripts/validate-findings.py). It has no observed/executed/read/inferred la... |
| F2 Transcript audit | ✗ | No script compares claims against a tool-call transcript. .claude/hooks/claim-reconcile.py only counts passport claims whose source_file mentions a changed file ("The hook only counts declarations by path ,  it never reads a value"). |
| F3 Proxy test | ◐ | .claude/references/research-agent-laws.md law 4: "A green gate is scoped. Capability loss is invisible to output-equality tests." .claude/references/model-versions.md records a case where a claim became false "while the gate stayed green". The vaccinate skill asks "does it pass for the right reason". The idea is the... |
| F4 Non-code fields | ◐ | .claude/references/discipline-cards.md covers social-science disciplines (economics, political science and others) with paper types and journals. .claude/references/theory-proving.md exists. There is no cross-field map of independent checks for law, medicine, history or physics. |
| F5 Read-only verifiers | ◐ | Some agents are read-only by tool list: humanize-auditor.md has `tools: Read, Grep, Glob`; verifier.md has `tools: Read, Grep, Glob, Bash`; claim-verifier.md has `Read, Grep, Glob, WebFetch, WebSearch, Bash`. Bash is a write path, so those two are not strictly read-only. Context isolation comes from `context: fork`... |
| F6 Vote ledger | ◐ | scripts/validate-findings.py deduplicates findings deterministically: `id = sha1(file:line:locus)`, with lens deliberately left out so two lenses finding the same defect produce one finding. adjudicate-review returns CONFIRMED/REFUTED/PARTIAL. It has no refuters that default to refuted, no majority voting, and no sc... |
| F7 Stop rules | ◐ | .claude/rules/orchestrator-protocol.md §4 Loop-until-dry sets fixed numbers: "stop after 2 consecutive dry rounds", `max_rounds` (default 5), about 500k spend cap and a two-strikes escalation. Fan-out sizes are fixed per skill (7 lenses in seven-pass-review, 4 in deep-audit). A post-judge hallucination gate exists,... |
| F8 Visual gates | ◐ | .claude/skills/visual-audit/SKILL.md runs an adversarial layout audit (overflow, alignment) with Edit disallowed. It reads the .qmd/.tex source, and nothing requires a critic who has not seen the source to judge the rendered output. |
| F9 Iteration research | ◐ | claim-verifier.md cites Dhuliawala et al. 2023 (CoVe). Rounds are capped, and "Stop when a confirmation pass returns no new confirmed defect" (adjudicate-review). No self-correction research on external signals is cited. |
| F10 Prose script | ◐ | .claude/skills/humanize/SKILL.md and agents/humanize-auditor.md audit 10 AI-voice categories, including symmetric paragraph shapes and tricolons. The audit is an LLM agent, not a scoring script. The skill itself notes that surface de-AI-ing failed a detector (Pangram). |
| F11 Platform findings | ◐ | .claude/references/model-versions.md is stamped ("verified 2026-08-21"), and run-skill-eval.sh has "verified behaviorally 2026-08-21". No platform bugs are filed upstream. |
| F12 Triage gate | ◐ | orchestrator-protocol.md has a 'Proportionality ,  match the process to the stakes' section. vaccinate/evals/cases/nottrigger-simple-question.md is a control case (fixed vs random effects) that asserts the skill's output does not appear. run-skill-eval.sh itself says nottrigger cases measure content leakage, not tri... |
| F13 Translations | ✗ | No translated skill files appear in the tree. |
| F14 Validator | ◐ | scripts/check-skill-integrity.py checks frontmatter against body tool parity, argument-hint flag parity, anchor resolution and rule-keyword registry completeness. It does not check byte-order marks, description length, tool names that can hang an agent, or critics with write tools. |
| F15 Baited tests | ◐ | .claude/skills/vaccinate seeds known defects into a copy of a real artifact plus a clean control and reports recall and false-positive rate. It has references/defect-library.md and eval cases such as detects-stale-gate.md and requires-clean-control.md. scripts/run-skill-eval.sh compares with-skill and without-skill... |

Enforced by code rather than instructions:

- scripts/validate-findings.py: checks each finding against the JSON schema, computes the sha1 finding ids used for dedup, and blocks synthesis unless it exits 0 (the skill requires exit 0 before synthesis).
- scripts/check-skill-integrity.py: lints skills for tool, flag, anchor and rule parity.
- scripts/check-model-versions.sh, check-staleness.py, check-surface-sync.py, check-derived-counts.py, check-links.py, check-repo-hygiene.py, check-tikz-prevention.py, check-ledger-coverage.py, check-spec-conformance.py: mechanical gates.
- scripts/quality_score.py: hard-gate roll-up of scores.
- Hooks in .claude/settings.json: git-guardrails.py and root-of-trust-guard.py run before tool use (PreToolUse). context-monitor.py, claim-reconcile.py (flags stale numbers after edits), pre-compact.py and post-compact-restore.py handle context and state.
- Tool lists: humanize-auditor has Read/Grep/Glob only, and the humanize and visual-audit skills set `disallowed-tools: [Edit, MultiEdit]`.

What it does better than Gravitas:

- Content-addressed finding ids (sha1 of file:line:locus) make cross-lens and cross-round dedup exact and checkable, and they power a two-strikes rule that escalates the same id when it survives rounds N and N+2.
- A post-judge hallucination gate: any CRITICAL the judge introduces that no lens raised must be re-verified in a fresh claim-verifier fork or marked [JUDGE-HALLUCINATED].
- The /vaccinate skill qualifies a checker before it is trusted, by seeding defects plus a clean control and measuring recall and false-positive rate in a qualification ledger.
- run-skill-eval.sh measures a skill's value against a no-skill baseline in sandboxed fresh sessions.
- Research-reproducibility machinery: numeric-claim passports plus a hook that flags stale manuscript numbers the moment an analysis script or output changes.
- Deep domain tooling for quantitative social science (specification-curve /challenge, replication packages, preregistration, referee simulation) and a model-version staleness checker with expiry dates.

### [vibeeval/vibecosystem](https://github.com/vibeeval/vibecosystem)

Stars 535. License MIT. Last push 2026-08-08. Platform: Claude Code (README also claims Cursor, Codex CLI, OpenCode).

A large Claude Code plugin bundle: the README claims 138 agents, 296 skills and 74 hooks. The assessed skill, skills/factcheck-guard/SKILL.md (the README's v2.1.1 note says it was imported from oh-my-claudecode), requires every factual claim about a codebase to carry a [VERIFIED] (must cite file:line), [INFERRED] (grep or filename only) or [UNCERTAIN] marker. It also sets out a protocol for existence, absence and behaviour claims and a two-pass audit (hypothesise, then read to verify). It is backed by rules/claim-verification.md and a PostToolUse hook, hooks/src/epistemic-reminder.ts, that adds a "grep results are not proof" reminder after Grep and Read calls.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | skills/factcheck-guard/SKILL.md has a three-tier table: [VERIFIED] 'Must cite file:line', [INFERRED] 'Based on grep or file name', [UNCERTAIN] 'Not yet checked'. Only VERIFIED has a provenance slot (file:line). There is no executed/command or URL-plus-quote tier, and no downgrade rule for an unfillable slot beyond '... |
| F2 Transcript audit | ✗ | No script compares markers against the transcript. hooks/src/epistemic-reminder.ts only prints a reminder after Grep or Read ('Update any prior ? INFERRED claims to ✓ VERIFIED if confirmed') and always returns result 'continue'. |
| F3 Proxy test | ◐ | The 'Common False Claim Patterns' table in SKILL.md lists code-only proxy failures: a grep match in a comment, string or test mock; a file named auth.ts not meaning auth is implemented; a type field not meaning it is used. There is no general doctrine and nothing outside code. |
| F4 Non-code fields | ✗ | The skill covers codebase claims only ('Use this skill when making any factual claim about the codebase'). |
| F5 Read-only verifiers | ✗ | The skill defines no read-only verifier subagent. It says that code-reviewer, security-reviewer, architect, sleuth and coroner 'must use this skill', but I did not check those agents' tool lists. |
| F6 Vote ledger | ✗ | No refuters, voting or ledger script in the files assessed. |
| F7 Stop rules | ✗ | The two-pass audit (Pass 1 hypotheses, Pass 2 verify each) has no completeness critic, no loop-until-dry rule and no fixed numbers. The only fixed count is 'minimum 3' alternative search terms for absence claims. |
| F8 Visual gates | ✗ | Not part of this skill. The README lists a separate visual-verdict skill, which I did not assess. |
| F9 Iteration research | ✗ | The only grounding is an unsourced anecdote: 'An 80% false claim rate was observed when agents trusted grep results'. No self-correction research is cited. |
| F10 Prose script | ✗ | Not in this skill. The ai-slop-cleaner skill exists but was out of scope. |
| F11 Platform findings | ✗ | No version-stamped platform experiments or upstream bug reports. |
| F12 Triage gate | ◐ | The trigger is scoped by the frontmatter description ('when making any factual claim about the codebase'). There are no control cases. The hook fires on every Grep and Read and gives a stronger warning only when the pattern matches existence regexes such as /exist/i or /missing/i, or when output_mode is files_with_m... |
| F13 Translations | ✗ | The README is translated into 13 languages (docs/README_ZH.md, README_JA.md, README_KO.md and others), but the skill itself is English only: the skills/factcheck-guard directory contains only SKILL.md. |
| F14 Validator | ◐ | The README shows a GitHub Actions 'Validate' badge (validate.yml). I did not open that workflow, so what it lints is unknown. |
| F15 Baited tests | ✗ | The skill has no tests, baited cases or planted-defect answer key. |

Enforced by code rather than instructions:

- hooks/src/epistemic-reminder.ts (PostToolUse:Grep\|Read) injects a reminder after every Grep or Read. It has a stronger 'GREP RESULTS ARE NOT PROOF' variant for existence-style patterns or files_with_matches mode. The hook only adds a reminder: it never blo...
- The marker requirement, the file:line citation and the ban on showing [UNCERTAIN] to the user are all written instructions in SKILL.md and rules/claim-verification.md. No code checks them.

What it does better than Gravitas:

- It fires a runtime hook on every Grep and Read, so the 'search results are hypotheses' reminder arrives at the moment of the tool call instead of relying on the model remembering the skill.
- It has a specific protocol for absence claims: at least 3 alternative search terms plus reading the likely files directly before claiming [VERIFIED ABSENT]. This is a concrete rule for negative claims about code.
- Its table of code-specific grep false positives (comments, string literals, test mocks, dead branches, type fields that are never set) is practical and easy to apply.

### [dsifry/metaswarm](https://github.com/dsifry/metaswarm)

Stars 419. License MIT. Last push 2026-06-19. Platform: Claude Code plugin (also Codex, Gemini CLI, Cursor, OpenCode adapters).

A software-delivery orchestration framework: 18 agent personas (markdown), a 9-phase workflow (research to PR shepherd), and a 4-phase per-work-unit loop IMPLEMENT, VALIDATE, ADVERSARIAL REVIEW, COMMIT, with parallel plan/design review gates, a BEADS knowledge base and coverage-threshold enforcement. Scoped to code, not general verification.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | skills/orchestrated-execution/SKILL.md: adversarial reviewer must 'Cite file:line evidence for PASS or expected-vs-found for FAIL'. This is a citation requirement, not a tier scheme: no labels and no downgrade rule. |
| F2 Transcript audit | ✗ | No script compares claims against a transcript. The closest thing is the doctrine 'The orchestrator independently runs quality gates. Never trust subagent self-reports' (orchestrated-execution/SKILL.md), which means re-running the tests. |
| F3 Proxy test | ✗ | There is no proxy-trap doctrine. Anti-rationalisation examples such as 'Coverage is close enough at 92%' (orchestrated-execution/SKILL.md) and mock-factory rules in agents/code-review-agent.md are code-only. |
| F4 Non-code fields | ✗ | Everything is software-engineering (rubrics/, agents/). Nothing covers law, maths, medicine and the other non-code fields. |
| F5 Read-only verifiers | ◐ | plan-review-gate/SKILL.md: 'Read-only codebase access. Reviewers can read files, run grep/glob, but cannot modify anything' and 'Fresh instances only'. Read-only is set by the prompt. agents/code-review-agent.md has a prose line '**Tools**: Codebase read, diff analysis, BEADS CLI' and no frontmatter tool list. |
| F6 Vote ledger | ◐ | plan-review-gate spawns 3 independent adversarial reviewers, and 'ALL three must PASS' (unanimity, not a majority vote). There are no refute-by-default refuters and no ledger script for dedup, tallies or dry rounds. |
| F7 Stop rules | ◐ | plan-review-gate has a dedicated Completeness reviewer, with fixed numbers of 3 reviewers and 'Max 3 iterations --> ... escalate'. There is no loop-until-dry rule and no scale-dependent numbers. |
| F8 Visual gates | ◐ | skills/visual-review/SKILL.md takes Playwright screenshots 'so agents can visually inspect their work'. The same agent judges them, so there is no fresh critic that hasn't seen the source, and the gate is not mandatory (auto_activate: false). |
| F9 Iteration research | ◐ | There is an iteration cap: 'Unlimited iterations ... Diminishing returns ... Max 3 iterations, then escalate' (plan-review-gate/SKILL.md). The external signal is fresh reviewers plus real test runs, but no research is cited. |
| F10 Prose script | ✗ | No prose-scoring script exists. |
| F11 Platform findings | ✗ | There are platform references (skills/start/references/*-tools.md) but no version-stamped experiments and no upstream bug filings. |
| F12 Triage gate | ◐ | skills/start/SKILL.md line 179: 'For simple tasks, the standard linear flow (implement → code review → PR) works fine.' This is prose guidance with no control-case tests. |
| F13 Translations | ✗ | English only. The tree has no translated skill files. |
| F14 Validator | ◐ | .github/workflows/ci.yml JSON-parses plugin.json and hooks.json, checks session-start.sh is executable, and runs `node lib/sync-resources.js --check` to keep co-located copies in sync. It does not lint frontmatter, BOMs, description length, tool names or critic write tools. |
| F15 Baited tests | ◐ | The tests/ shell suites (test-session-start.sh, test-ci-template.sh, test-sync-resources.sh, test-installer.sh, codex/gemini tests) test installer and infrastructure behaviour. None has baited cases or a planted-defect audit with an answer key. |

Enforced by code rather than instructions:

- Coverage threshold enforcement: templates/pre-push hook and the orchestrator's validate step read .coverage-thresholds.json and run its enforcement command (blocking)
- Pre-push lint/format checks in templates/pre-push (typecheck and format are softened with '\|\| true')
- CI (.github/workflows/ci.yml): plugin.json/hooks.json JSON validity, hook executability, sync-resources --check, shell test suites
- hooks/hooks.json: SessionStart/PreCompact hook re-injects context (session-start.sh); it does not enforce reviews
- bin/pr-comments-check.sh / pr-comments-filter.sh scripts for PR comment handling
- Reviewer read-only status, fresh instances, the 3-iteration cap and unanimous PASS are all instruction-only

What it does better than Gravitas:

- End-to-end software delivery pipeline (issue to plan to work units to PR shepherd to merge) with explicit Definition-of-Done contracts that reviewers check item by item
- Blocking coverage-threshold enforcement wired into a real git pre-push hook and CI templates, i.e. actual code gates in the user's repo
- Cross-model review via external CLI adapters (skills/external-tools/adapters/codex.sh, gemini.sh), giving model-level independence
- Persistent learning loop: a BEADS JSONL knowledge base (patterns, gotchas, decisions) fed by /self-reflect before each PR
- Multi-host packaging: Claude Code, Codex, Gemini CLI, Cursor and OpenCode, plus an npm CLI installer with tests

### [socialpranker/deepdive](https://github.com/socialpranker/deepdive)

Stars 377. License MIT. Last push 2026-09-20. Platform: Claude Code skill (portable methodology for other LLMs).

A Claude Code research skill (SKILL.md is in Russian, README in English). It runs a 13-phase pipeline defined in phases.yaml: reframing, plan, search by parallel general-purpose subagents, a claims ledger, an evidence filter, a red team, a four-axis verify phase, report export and a decision walkthrough. Each source is saved as sources/NN_slug.md with verbatim quotes, and a large set of Python scripts gate the finished run folder (finish.py, validate_phases.py, check_number_provenance.py, check_number_arithmetic.py, check_citations.py).

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | Claims link to [sNN] source files holding verbatim quotes. references/source_scoring.md adds provenance fields for numbers (origin_kind/origin_url/data_as_of/chain_len) and a fail-closed rule: an unknown origin or chain_len >= 2 bars the number from the memo and from high-confidence claims. Each source records fetch... |
| F2 Transcript audit | ◐ | There is no transcript audit. eval/check_citations.py checks that source URLs resolve (a guard against hallucinated citations). scripts/validate_phases.py checks that each mandatory phase left its artifact in the output folder. Neither compares labels against the tool calls that actually ran. |
| F3 Proxy test | ◐ | No named doctrine. It does recognise specific cases: check_number_provenance.py says 'a content farm with a verbatim quote passes faithfulness perfectly', and it detects 'zombie figures' (one value circulating under different roots). |
| F4 Non-code fields | ◐ | Domain API catalogues (references/api_sources: academic, pubmed, clinicaltrials, EMA, SEC EDGAR, FRED and others) plus 460+ stat sources. These are about sourcing, not per-field verification guidance for law, maths or physics. |
| F5 Read-only verifiers | ✗ | The red team runs as general-purpose subagents (SKILL.md line 126). Explore is used only for scouting ('read-only, только разведка'). No read-only critics defined by tool lists. |
| F6 Vote ledger | ◐ | references/adversarial_pass.md and SKILL.md phase 6 define five hostile roles (Skeptic, Contrarian, Gap-hunter, Executor, Minority advocate), severity triage and one HIGH remediation round, with finder separate from fixer. There is no voting and no dedup/tally ledger script. |
| F7 Stop rules | ◐ | SKILL.md phase 4 has a circuit breaker: stop after two rounds with nothing new. Red-team size is fixed per depth (shallow=R1, medium=R1+R2+R4, deep=all five). Phase 3.7 adds a scout pass of 3-4 Explore agents. There is no separate completeness critic with vote counts. |
| F8 Visual gates | ✗ | The report export (build_report.py) fails on broken links or lost footnotes, but no rendered output is judged by a critic. |
| F9 Iteration research | ◐ | Cites research such as the 'Anthropic Frontier Red Team' note in adversarial_pass.md, and limits remediation to one round. No explicit rule grounded in self-correction research. |
| F10 Prose script | ✗ | No prose-scoring script found in scripts/. |
| F11 Platform findings | ✗ | No version-stamped experiments on the host platform. The weekly catalog-sync workflow validates API endpoints, not agent-platform behaviour. |
| F12 Triage gate | ◐ | Depth modes (shallow 5-7 sources, medium, deep) are chosen and announced up front, and phase 1 downgrades honestly to shallow when there is no decision fork. The mandatory phases depend on depth_gate in phases.yaml. No control-case tests of the triage. |
| F13 Translations | ✗ | SKILL.md is in Russian; the README carries English tables. There are no full parallel translations of the skill. |
| F14 Validator | ◐ | validate.yml runs ruff, pytest and stamp_docs.py --check (fails on doc/count drift), and validate_phases.py self-checks phases.yaml coverage. There is no frontmatter/BOM/tool-name lint for skills or agents. |
| F15 Baited tests | ◐ | Extensive pytest suite (tests/test_verify.py, test_number_provenance.py, test_finish.py and others) with fixtures (tests/fixtures/run_mini), plus eval/ benchmark questions, a rubric and a judge prompt. No baited or planted-defect audit case with an answer key was seen. |

Enforced by code rather than instructions:

- scripts/finish.py: blocking finish gate. It builds sources.csv, checks liveness, runs wiki ingest, number provenance and arithmetic with --strict, then validate_phases.py --strict.
- scripts/validate_phases.py: every phase mandatory for the depth mode must have emitted its artifact.
- scripts/check_number_provenance.py: deterministic fail-closed rule for numbers of unknown provenance, plus detection of circulating 'zombie' figures.
- scripts/check_number_arithmetic.py: recomputes derived numbers in numbers.csv from their formula and inputs.
- eval/check_citations.py: a dead URL on an open-access source fails under --strict.
- scripts/build_report.py: a broken [sNN] link or a lost footnote fails the build.

What it does better than Gravitas:

- Provenance for numbers: origin_kind, chain_len and data_as_of are checked by script, and it detects one figure being passed off as independent sources, which Gravitas lacks.
- Deterministic arithmetic re-check of derived numbers against formula and inputs in numbers.csv.
- URL liveness check for cited sources that expects paywalled access rather than penalising it.
- A phase-completeness gate that fails a run when a mandatory phase left no artifact.
- A cross-run claims wiki that flags conflicts with earlier research before synthesis.
- Large domain source catalogues (29 channels, 460+ stat sources) with weekly automated endpoint validation.

### [udaysharmadev/gravitas](https://github.com/udaysharmadev/gravitas)

Stars 9. License MIT. Last push 2026-09-12. Platform: Google Antigravity (Agent Skills via skills.sh; Native plugin via agy).

A coding-only engineering-discipline Agent Skill ("Core") for Gemini in Google Antigravity, plus an optional Antigravity plugin ("Native"). The plugin's PreToolUse, PostToolUse, PostInvocation and Stop hooks enforce a task contract, action locks, write scope, read-before-write, a hash-chained evidence ledger and a completion gate. The README calls it a "research preview" and says comparative performance has not been measured.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | skills/gravitas/SKILL.md Rule 3: 'Every success claim needs actual command output, cited verbatim'. Its decision records carry 'evidence: read src/auth/session.ts line 23'. There are no observed/executed/read/inferred tier labels and no downgrade rule for a label whose slot cannot be filled. |
| F2 Transcript audit | ◐ | plugins/gravitas-antigravity/scripts/post_tool.py records every tool call into evidence.jsonl, which is hash-chained by evidence_chain.py. stop_gate.py accepts only 'Gravitas-owned executions' (owned_validator_pass: source=='validator', exit_code==0, event_hash) as evidence that an acceptance criterion is covered. S... |
| F3 Proxy test | ✗ | A grep for 'proxy' in SKILL.md, references/verification.md and resources/verification-engine.md found nothing. The closest thing is the anti-rationalization rules in SKILL.md. |
| F4 Non-code fields | ✗ | Coding only. The SKILL.md description says 'software implementation, debugging, refactoring...', and eval/trigger-eval.json expects non-activation on non-engineering prompts. |
| F5 Read-only verifiers | ◐ | plugins/gravitas-antigravity/agents/verifier.md is read-only by instruction only ('You may NOT use: write_to_file, replace_file_content'). It has no frontmatter tool list. Separately, pre_tool.py denies WRITE_TOOLS and mutating shell commands in READ_ONLY_MODES (plan-only, review-only and others), which is code enfo... |
| F6 Vote ledger | ✗ | The verifier is described as 'adversarial', and resources/adversarial-critique.md gives '7 Attack Vectors' for self-critique. There is no voting, no refuters that default to refuted, and no dedup or vote-tally ledger. scripts/ledger_add.py appends evidence records only. |
| F7 Stop rules | ✗ | No completeness critic and no loop-until-dry rule. The only fixed number is stop_gate.py's circuit breaker ('cycle_count >= 3'). |
| F8 Visual gates | ✗ | A grep for screenshot/visual in the verification docs found nothing. There are UI eval tasks (eval/tasks/UI-00x.yaml) but no fresh-critic perceptual gate. |
| F9 Iteration research | ◐ | README cites Huang et al.: 'unaided self-correction can fail ... which is why GRAVITAS privileges external validators'. SKILL.md prefers 'external/deterministic evidence over model self-assessment'. There is a stop-gate cap of 3 cycles, but no explicit research-backed cap on passes. |
| F10 Prose script | ✗ | No prose-scoring script. scripts/check_readme_claims.py checks README claims (file not opened, judged from its name), not machine-prose markers. |
| F11 Platform findings | ◐ | The README links a 'version-aware installation guide' and docs/install-verification.md (not opened), and pre_tool.py handles 'Antigravity 2.x hook payload, with v4-preview compatibility'. I found no evidence of version-stamped experiments filed upstream as bug reports. |
| F12 Triage gate | ◐ | SKILL.md has a Tier 0/1/2 classification ('Trivial / reversible \| Act immediately'), and the README says 'A read-only question should not trigger a committee'. eval/trigger-eval.json has 5 non_activation controls, but its notes say 'False positives on non-engineering tasks are acceptable'. The harness that runs the... |
| F13 Translations | ✗ | The tree has no translated skill files. |
| F14 Validator | ◐ | .github/scripts/validate_skill.py checks only that SKILL.md has frontmatter, name: and description:, and is under 500 lines. It has no BOM, dead-reference, hang-prone tool or critic-write-tool checks. |
| F15 Baited tests | ◐ | tests/test_runtime.py holds adversarial runtime tests such as test_model_supplied_confirmation_cannot_bypass_destructive_prompt, test_chain_verifier_detects_tampering and test_official_hook_telemetry_cannot_complete_a_contract. These are baited hook tests, but there is no planted-defect audit case with an answer key... |

Enforced by code rather than instructions:

- pre_tool.py (PreToolUse hook): action lock denies write tools and mutating shell regex in read-only modes (answer, research, plan-only, review-only, security-review)
- pre_tool.py: allowed_write_scope path-boundary check, read-before-write from the evidence ledger, blocking retries of an already-failed action by fingerprint, force_ask on destructive commands (rm, git reset/clean, drop table) that a model-supplied confirma...
- post_tool.py (PostToolUse hook): logs every tool call to evidence.jsonl with secret redaction; logs failures to failures.jsonl
- evidence_chain.py: SHA-256 hash-linked, append-only evidence ledger with verify_chain tamper detection
- stop_gate.py (Stop hook): blocks completion until every acceptance criterion has a Gravitas-owned validator PASS with exit_code 0, required validators pass, background tasks are idle and known failures are resolved; the 3-cycle circuit breaker never fails open
- validator_runner.py: rejects undeclared criteria and commands (per test names in tests/test_runtime.py; the runner file itself was not opened)

What it does better than Gravitas:

- Runtime enforcement through Antigravity hooks: a Stop-hook completion gate keeps the agent working until each contract acceptance criterion has a validator run with exit code 0. That is enforced by code rather than audited after the fact.
- A hash-chained, tamper-evident evidence ledger (evidence_chain.py) written by hooks, not by the model; the model cannot write completion evidence itself (test_official_hook_telemetry_cannot_complete_a_contract).
- PreToolUse action lock, write-scope and read-before-write enforcement, plus blocking retries of failed actions by fingerprint. Plan-only and review-only modes are blocked from writing by code at the host level.
- A machine-readable task contract (schemas/task-contract.schema.json) that the hooks consume.
- Secret redaction before evidence is persisted.
- An extensive benchmark infrastructure (GravitasBench runner, 30 task specs) that is candid that no results are yet claimed.

### [vnmoorthy/groundtruth](https://github.com/vnmoorthy/groundtruth)

Stars 7. License MIT. Last push 2026-07-20. Platform: Claude Code (Stop hook + skill), Node >=18.

A Node.js Stop hook for Claude Code, with a CLI and a companion skill. On every Stop it parses the session JSONL transcript and regex-detects completion claims in the last assistant turn ("Done.", "fixed", "all tests pass"; 8 frames, 21 exclusions). It then checks whether tool observations in the same turn include a verification artifact, such as a test, typecheck, build or lint command with success output, a curl returning 2xx, or a Read/Grep of a file written in that turn. If a claim in a code-context turn has no such artifact, it returns {"decision":"block","reason":...}. It also includes a retroactive audit CLI (text/JSON/SARIF output) and a memory-file write gate. It is scoped to cod...

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ✗ | There are no per-claim evidence tiers and no provenance slots. Claims are a binary claim/no-claim regex match (src/detector.mjs). The only thing that clears a claim is a 'kind' on the verification side (test\|typecheck\|build\|lint\|http\|grep\|read-written-file\|screenshot), defined in src/verifier.mjs. |
| F2 Transcript audit | ◐ | The mechanical transcript check is real. src/check.mjs checkTurn() combines detectClaims(text) with detectVerifications(observations) parsed from the session JSONL (src/session.mjs), and blocks on a claim with no evidence. However, it matches completion claims against any success artifact in the turn. It does not ma... |
| F3 Proxy test | ✗ | There is no proxy-trap doctrine. README 'Honest limits' only concedes that 'A test that exits 0 but ran no real assertions counts as verified'. |
| F4 Non-code fields | ✗ | The tool is explicitly code-only. SKILL.md Scope: 'This rule applies to code work.' src/code-context.mjs suppresses non-code turns. |
| F5 Read-only verifiers | ✗ | There are no subagents or agent definitions in the tree. Only skills/groundtruth/SKILL.md and src/*.mjs exist. |
| F6 Vote ledger | ✗ | There are no refuters, no voting and no ledger. |
| F7 Stop rules | ✗ | There is no completeness critic and no loop-until-dry rule. The hook blocks at most once: it checks stop_hook_active and 'will never block twice in a row' (SKILL.md). |
| F8 Visual gates | ✗ | There is no perceptual gate. The verifier lists a 'screenshot' kind as acceptable evidence (src/verifier.mjs typedef), but nothing judges the rendered output. |
| F9 Iteration research | ✗ | No self-correction research is cited. The only iteration rule is the single block per stop. |
| F10 Prose script | ✗ | There is no prose-scoring script. |
| F11 Platform findings | ◐ | docs/findings.md: 'npm package @anthropic-ai/claude-code-linux-arm64@2.1.119, binary extracted and grepped directly on 2026-04-24'. This documents the hook surface stamped with version and date. It does not mention filing discrepancies upstream. |
| F12 Triage gate | ◐ | src/code-context.mjs is a scope filter that suppresses gating on non-code turns (check.mjs returns suppressed:'no-code-context'). It has control fixtures: test/fixtures/false-positives.jsonl, non-code-paper-writing.jsonl and community-false-positives.txt. It is a code-context filter, not a triviality gate for heavy... |
| F13 Translations | ✗ | There are no translations. The tree has only English docs. |
| F14 Validator | ✗ | There is no skill, plugin or agent validator. src/doctor.mjs exists, but I did not open it; the README describes status/install checks only. |
| F15 Baited tests | ◐ | The test suite covers the detector with claim fixtures and expected counts: README says 'unverified-claim → 3 findings, terse-closer → 1, checklist → 2, verified-claim → 0'. There are also community true-positive and false-positive fixture files. There is no planted-defect audit case with an answer key for a verifier. |

Enforced by code rather than instructions:

- The Stop hook (src/hook-entry.mjs, src/check.mjs) mechanically blocks the end of a turn when a regex-detected completion claim has no verification artifact among that turn's transcript tool observations.
- Evidence classification is done in code by src/verifier.mjs: 80+ command regexes plus success and failure signal patterns on the output, for example rejecting output that contains '[1-9] failed' or a nonzero exit.
- Read or Grep only counts as evidence when it targets a path written in the same turn (writtenPaths set in src/verifier.mjs).
- A loop guard via stop_hook_active prevents repeated blocks.
- The memory gate CLI (src/memory-gate.mjs) exits nonzero on unverified completion claims in MEMORY.md/NOTES.md content.
- The retroactive audit CLI has --fail-on for CI and SARIF output (src/audit.mjs).

What it does better than Gravitas:

- It enforces live at runtime through a host Stop hook that can actually refuse the end of a turn, rather than auditing labels after an answer is written.
- Its detector was calibrated against a real corpus (1,272 turns across 50 sessions, per the README), and the false-positive counts are published per release.
- It audits past sessions retroactively across all transcripts, with SARIF output and a CI fail-on threshold.
- It has a memory-file write gate that blocks carrying unverified completion claims into persistent memory.
- It is zero-dependency, installs in one line, and has a browser playground for trying it on a JSONL file without installing.

### [aiimagined/godmode](https://github.com/aiimagined/godmode)

Stars 6. License Apache-2.0. Last push 2026-09-23. Platform: Claude Code, Grok, Codex, Antigravity, OpenCode, Copilot, Kiro, Cursor, Gemini CLI, GitHub Action (Python 3.11+).

A zero-dependency Python plugin and CLI for coding agents: Claude Code, Grok, Codex, Antigravity, OpenCode and others. It keeps a local hash-chained archive of the commands the agent ran, what it changed, what it refused and what it claimed. Pre-tool hooks stop risky commands. Claims are graded against cited, re-run evidence. A Stop-gate "done bar" blocks a "complete" while obligations are still open. Thirteen or more integrity monitors look for dishonest green-suite diffs. It ships 19 workflow skills.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | skills/godmode-evidence/SKILL.md: claims carry grades (verified/observed/hypothesis) with citations cmd:/file:<path>#L<n>/seq:<n>. A state-reporting command 'caps at observed no matter what it prints', and a claim with no support is downgraded. These are grades on recorded claims, not an observed/executed/read/infer... |
| F2 Transcript audit | ◐ | Claims go through `godmode claim --verify`, which re-runs the cited cmd: through an attested checker. The Stop gate parks claim-shaped sentences that have no claim record (godmode-evidence step 7). scripts/godmode_runtime/godmode_claimscan.py checks public docs for claims that name no reproduction. Nothing compares... |
| F3 Proxy test | ◐ | The MONITORS dict in scripts/godmode_runtime/godmode_integrity.py (assertion-diff, skip-quarantine, mock-expansion, oracle-tamper, false-green-shape, negative-control and others) detects tests that pass while the property is false. It is limited to code and tests; I found no cross-domain proxy-trap doctrine. |
| F4 Non-code fields | ✗ | The skills I saw (evidence, second-look, triage, skill-forge) are about code and the archive only. I found no guidance for law, medicine or other fields. |
| F5 Read-only verifiers | ✗ | The repo tree has no agents/ directory with tool-listed verifier subagents. skills/*/agents/openai.yaml are interface metadata files. godmode-second-look is a skill that runs in the main agent. |
| F6 Vote ledger | ✗ | There are no refuter agents, no voting and no dedup ledger of findings. The archive is a hash-chained record ledger (godmode_chronicle.py), which is not vote tallying. |
| F7 Stop rules | ✗ | I found no completeness critic and no fan-out or loop-until-dry numbers. The closest thing is the done bar, which lists open obligations (README 'The bar'). |
| F8 Visual gates | ✗ | No visual or perceptual gates found. |
| F9 Iteration research | ✗ | No self-correction research citations found. Skill-forge says 'Revise only from observed failures', with no cap on passes. |
| F10 Prose script | ◐ | godmode_claimscan.py scores public-surface prose for claim-shaped sentences (a number with a unit, or promise verbs) that lack a reproduction. There is also a prose linter for charter rules (tests/test_prose_lint.py, advisory). Neither measures the structural markers of machine-generated prose. |
| F11 Platform findings | ◐ | README Host support: enforcement tiers come from 'live, chronicled interception proof' (HARD/DEGRADED/PARTIAL/SOFT). Claude Code and Grok are live-proven, and the other hosts are declared as unproven. These are experiments on the platform, stamped in the archive. I saw no evidence of bugs filed upstream. |
| F12 Triage gate | ◐ | A skill named godmode-triage exists, but it works the open-asks queue and is not a triage gate against over-triggering. Anti-over-trigger routing is tested by quality/evals/conceptual-question-stays-quiet/graders/no-skill-fired.md and by negative routing examples in each godmode-evals.json. |
| F13 Translations | ✗ | The tree listing has no translation files. |
| F14 Validator | ◐ | tests/test_skill_lint.py -> godmode_forge.lint_skill checks scope (description has a trigger), delivery (backticked terms in the description appear in the body) and safety (hard-fails injection-shaped content). There are also godmode_docslint.py (dead pointers) and `skill validate`. I saw no checks for a BOM, tools... |
| F15 Baited tests | ✓ | README: `godmode scenarios` (29 staged failure and attack shapes, all caught), `godmode grid` (33 attacks on controls), and tests/test_gate_corpus replaying 214 recorded commands. Also integrity monitors such as negative-control, and a large tests/ suite. I did not open the scenario files, so I have not seen an answ... |

Enforced by code rather than instructions:

- PreToolUse/Stop hooks (hooks/godmode_gate_fast.py, hooks/hooks.json) classify commands by risk tier and deny or ask before running them. On Claude Code and Grok this is live-proven.
- The Stop-gate done bar blocks 'everything is complete' while there are open asks, pending plan steps or uncited criteria.
- `claim --verify` re-runs cited cmd: evidence and caps a state-reporting command at 'observed'.
- Integrity monitors (godmode_integrity.py MONITORS) block a diff that has had an assertion removed, a skip added or an oracle tampered with.
- godmode_claimscan.py covers public docs: a number or promise with no reproduction.
- Hash-chained, tamper-evident archive (godmode_chronicle.py).

What it does better than Gravitas:

- Runtime enforcement: real pre-tool hooks deny destructive commands before they run, and this is live-proven on Claude Code. Gravitas relies mostly on doctrine plus an audit after the fact.
- A tamper-evident, hash-chained archive of actions, refusals and claims that persists across sessions and compaction. `godmode resume` rebuilds state from it.
- Evidence is re-executed: cmd: citations are re-run by an attested checker, not just labelled.
- Diff-level anti-cheating monitors for test suites (assertion removal, skip added, oracle tamper, mock expansion) that do not depend on the model's judgment.
- It covers many hosts (Claude Code, Grok, Codex, Antigravity, OpenCode, Copilot, Kiro, CI Action), and each host's tier is computed from live proof, not from the host's name.
- It applies claim discipline to its own README mechanically: claimscan requires a reproduction command on the same line as a claim.

### [mizcausevic-dev/evidence-labeling-protocol](https://github.com/mizcausevic-dev/evidence-labeling-protocol)

Stars 0. License MIT. Last push 2026-08-22. Platform: Claude Code / Claude.ai skill.

A single instruction-only Claude skill (SKILL.md plus README, banner and diagram). It defines five evidence labels (Observed, Executed, Verified, Predicted, Blocked), five hard rules, an output template and a pre-send self-check. It has no scripts, hooks, agents or tests.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | SKILL.md: 'Use exactly one of these for every factual claim'. The template has an Evidence column, and Hard rule 1 says to quote or reference the actual command result. Downgrading is covered: 'If you did not run it, it is Predicted, not passed'. There is no read/URL-plus-quote tier and no required slot structure fo... |
| F2 Transcript audit | ✗ | The repo contains only CODE_OF_CONDUCT.md, CONTRIBUTING.md, LICENSE, README.md, SKILL.md and assets. There is no script. |
| F3 Proxy test | ◐ | SKILL.md Hard rule 2 names one case: 'A scanner that finds nothing because it is broken looks identical to a scanner that finds nothing because there is nothing to find'. It requires a known-positive control and two independent methods. Rule 3 says local or cached copies are not evidence of what is live. This covers... |
| F4 Non-code fields | ✗ | SKILL.md is scoped to 'code behavior, test results, deployments, security findings, or system state'. It does not cover law, mathematics, medicine or other non-code fields. |
| F5 Read-only verifiers | ✗ | There are no agent definitions. |
| F6 Vote ledger | ✗ | No refuters, votes or ledger. |
| F7 Stop rules | ✗ | No completeness critic and no stopping rule. |
| F8 Visual gates | ✗ | No perceptual gate. It mentions 'viewed the screen' only as the meaning of Observed. |
| F9 Iteration research | ✗ | No iteration rules and no research citations. |
| F10 Prose script | ✗ | No prose-scoring script. |
| F11 Platform findings | ✗ | No platform experiments and no upstream bug reports. |
| F12 Triage gate | ✗ | No triage gate. The frontmatter description triggers on any claim about what happened. |
| F13 Translations | ✗ | English only. |
| F14 Validator | ✗ | No validator. |
| F15 Baited tests | ✗ | No tests. The planted known-positive control is advice inside SKILL.md, not a test case. |

What it does better than Gravitas:

- It has a separate Blocked label for 'cannot proceed with current access', and Hard rule 4 requires stating what was not run separately from what passed ('3 of 5 checks executed, 2 blocked'). This makes not-run distinct from failed and from passed.
- It has a Predicted label for results that are expected but not yet run, so a speculative claim still carries a label rather than being left out.
- Hard rule 5: numbers get a source and a date.
- It is a single small file with no dependencies that can be pasted into Claude.ai custom instructions, so it is simpler to adopt than a plugin.
- A BLUF-first output template with a fixed Item / Label / Evidence / Notes table.

### [edgebuildlabs/evidence-contracts](https://github.com/edgebuildlabs/evidence-contracts)

Stars 0. License CC0-1.0. Last push 2026-09-19. Platform: Any agent that reads AGENTS.md/CLAUDE.md/.cursorrules (Claude Code, Codex, Cursor, Gemini CLI).

Instruction-only CC0 contract kit: AGENTS.md (a fixed rule saying every claim of state carries a source and a date or NOT VERIFIED, plus observed/inferred/hypothesis/recommendation labels, the STARTED != COMPLETED != VALIDATED != PASS ladder, a failure-layer classification, doc rules and authorization), with STATE.md and DECISIONS.md templates. The repo holds 5 files (AGENTS.md, DECISIONS.md, LICENSE, README.md, STATE.md). There are no scripts, hooks, agents or tests.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | AGENTS.md: the mark 'travels attached to the claim ,  `path:line (date)` · `command (now)` · `URL (date)` ,  or NOT VERIFIED'. It has observed/inferred/hypothesis/recommendation labels, and an unmarked claim falls to NOT VERIFIED. It has no read/executed split and no quoted-line requirement for URLs. |
| F2 Transcript audit | ✗ | The repo tree holds only 5 markdown/licence files, so no audit script exists. AGENTS.md itself says 'If a script can prove it, write the script', but it ships none. |
| F3 Proxy test | ◐ | AGENTS.md: 'Exit code 0 ... do not prove the mission succeeded'; 'Tests passing is not validation.' This is close to the proxy idea, but it is not named as a doctrine and it covers code only. |
| F4 Non-code fields | ✗ | Coding-agent scope only. No law, medicine or maths guidance in AGENTS.md or README.md. |
| F5 Read-only verifiers | ✗ | No agent definitions. AGENTS.md only says 'self-review is not audit'. |
| F6 Vote ledger | ✗ | Nothing on refuters, votes or a ledger script. DECISIONS.md is an append-only human decision ledger, not a findings deduplicator. |
| F7 Stop rules | ✗ | No completeness critic and no stopping rule. |
| F8 Visual gates | ✗ | Only mentions 'a rendered artifact' as a possible definition of done in AGENTS.md. No fresh-critic gate. |
| F9 Iteration research | ✗ | No iteration rules and no cited research. |
| F10 Prose script | ✗ | No prose-scoring script. 'Prose rots' in AGENTS.md is about volatile values, not machine-prose markers. |
| F11 Platform findings | ✗ | No version-stamped platform experiments. The README claims production use on a VPS but cites no filed bugs. |
| F12 Triage gate | ◐ | AGENTS.md: 'Do not demand deterministic proof for brainstorming, architecture, opinion, or judgment.' This is a scope exemption with no control-case tests. |
| F13 Translations | ✗ | The README links PT/ES versions of the external website only. The contract file itself is not translated in the repo. |
| F14 Validator | ✗ | No validator. |
| F15 Baited tests | ✗ | No tests. |

What it does better than Gravitas:

- Zero-install and portable across tools: one file dropped in as AGENTS.md/CLAUDE.md/.cursorrules works across Claude Code, Codex, Cursor and Gemini CLI, while Gravitas is Antigravity-specific.
- Requires a DATE on every claim of state (`command (now)`, `path:line (date)`), which gives an explicit freshness dimension. Pairs it with 'gather evidence immediately before acting' and records the evidence next to the action.
- Failure-layer triage list (auth, quota, transport, wrong shell, harness, path, permission, sandbox, tool, orchestration, model, product) to check before blaming the model.
- Project-state hygiene templates: STATE.md declares DOCUMENT_CLASS = DATED_SNAPSHOT / IS_CANONICAL_TRUTH = NO, has a size limit and a mandatory 'Not verified' section. DECISIONS.md is append-only, and there is a PROPOSED -> RUNTIME_PROVEN admission state.
- Authorization rule that makes the agent write down what is NOT permitted (the 'negative space').
- Extremely small and readable, and public domain (CC0).

### [aliradid/citation-needed](https://github.com/aliradid/citation-needed)

Stars 0. License MIT. Last push 2026-09-16. Platform: Cross-harness single SKILL.md: Claude Code (plugin + SessionStart hook), Codex, Cursor, Gemini CLI, OpenCode, Kimi, Q....

A fact-checking skill. It pulls atomic factual claims out of a draft, verifies each against live web sources with source tiers (A primary to D not-evidence), and returns a fixed-format evidence ledger with 10 statuses plus an annotated copy. It has Audit and Guard modes, a report linter script (validate_report.py) and a deterministic eval runner with planted-error fixtures.

| Feature | Status | Evidence |
| :--- | :---: | :--- |
| F1 Evidence labels | ◐ | SKILL.md and references/source-tiers.md: each ledger row gets one of 10 statuses (VERIFIED/PARTIAL/UNVERIFIED/CONTRADICTED/...). The Evidence column must hold URLs that came from a tool this session, 'searched:' queries for UNVERIFIED, and a reason for SKIPPED/UNCHECKED. A row without a qualifying source is downgrad... |
| F2 Transcript audit | ✗ | scripts/validate_report.py checks only the report itself: URL counts per status, the 'primary' note, 'searched', fix present, summary counts, verdict and marker consistency. It never reads a tool-call transcript, so it cannot tell whether a URL was actually opened. The 'URL from a tool call' rule is instruction-only... |
| F3 Proxy test | ✗ | No proxy-trap doctrine. The nearest thing is the MISLEADING status ('Literally true but missing context') in SKILL.md, which is about claims, not about checks. |
| F4 Non-code fields | ◐ | SKILL.md ranks legal/medical/financial/safety claims highest. source-tiers.md names primary sources per kind (statutes, court filings, registries, statistics offices, papers, governing bodies). There is no per-field guidance for maths, physics or history, and no independent check is named for each field. |
| F5 Read-only verifiers | ✗ | references/verifier-prompt.md is a prompt template for optional harness subagents ('You have web search and fetch tools'). No agent definition carries a tool list. openai.yaml sets only interface/policy, and gemini.toml is a command prompt. |
| F6 Vote ledger | ✗ | There are no refuters, votes or dedup ledger. Verifier batches of about five claims are merged 'in original claim order' (verifier-prompt.md). |
| F7 Stop rules | ◐ | Fixed numbers exist: 'Up to three searches per claim', 'more than 40 claims ... mark the remainder UNCHECKED (budget)', and verifier batches of 'about five claims' (SKILL.md). There is no completeness critic and no loop-until-dry rule. |
| F8 Visual gates | ✗ | No visual or perceptual gate. |
| F9 Iteration research | ✗ | No self-correction research or iteration rules. Only a per-claim search cap. |
| F10 Prose script | ✗ | No prose-scoring script. validate_report.py lints the report format, not prose style. |
| F11 Platform findings | ✗ | No version-stamped platform experiments or upstream bug filings. There is an issue template .github/ISSUE_TEMPLATE/platform.md, and README says the token cost was 'Measured with claude plugin details', without a version stamp. |
| F12 Triage gate | ◐ | SKILL.md Guard mode 'does not apply to code, chat explanations, brainstorming, fiction' and has a claim-level triage step (SKIPPED for opinion/prediction/first-person/common knowledge). The eval fixtures include 6 opinions as controls ('0/6 opinions wrongly checked'), but there are no request-level control cases for... |
| F13 Translations | ✗ | English only. gemini.toml is a condensed restatement for another harness, not a translation. |
| F14 Validator | ◐ | tests/test_manifests.py checks that all JSON manifests parse, that names match, that versions line up with SKILL.md and CHANGELOG, that the Cursor mirror is identical, and that the frontmatter starts with '---' and has name/description. It does not check BOMs, description length, dead references, hanging tool names... |
| F15 Baited tests | ◐ | evals/fixtures/*.md with *.truth.json answer keys contain planted errors (e.g. tech-history.truth.json p1 'Netscape in 1997' expected CONTRADICTED), true claims and opinions. scripts/run_evals.py scores them deterministically. tests/ holds unit tests for the validator, the hooks and the runner. The key covers plante... |

Enforced by code rather than instructions:

- scripts/validate_report.py: ledger format; each status has the evidence it needs (VERIFIED needs 2 URLs or 1 plus a 'primary' note; UNVERIFIED needs 'searched'; SKIPPED/UNCHECKED need allowed reasons; problem statuses need a fix); summary counts match the r...
- scripts/run_evals.py: deterministic scoring of runs against the truth.json answer keys (no judge model)
- hooks/always-on.mjs: SessionStart injection of the full SKILL.md when a flag file exists (fail-open)
- tests/test_manifests.py: manifest parse, name and version sync, and the Cursor mirror kept byte-identical
- Not enforced by code: 'URL must come from a tool call this session', the source independence rules and the open-the-page rule are instructions only

What it does better than Gravitas:

- A fixed, machine-parseable output contract (summary line, verdict, 5-column ledger, [CN-n STATUS] inline markers) with a linter whose exit code can fail a content-publishing pipeline in CI
- A finer status taxonomy for claims about the world (PARAPHRASED, MISATTRIBUTED, OUTDATED, MISLEADING) and explicit source-independence rules (same wire report or same site counts as one, and wikis are pointers only)
- Published eval numbers from live runs on two harnesses (15/16 planted errors, 0/23 false alarms, 0/6 opinions checked), scored against JSON answer keys with no judge model
- Portability: one SKILL.md with thin installers for about ten harnesses, plus a test that keeps the mirrors in sync
- Cheap context: README reports about 130 tokens per session and about 2,500 when the skill fires

## The Novelty Claims And Their Refuters

Each refuter was told to find prior art for one claim, to open every candidate before citing it, and to default to finding prior art.

### N1, search 0

Claim tested: 

Prior art found: yes.

Verdict: The claim as written is refuted in its core. frizfealer/grounding-attribution (GroundCheck) is a public Claude Code plugin that makes the agent label each claim with a tool-typed citation or 'unverified'. At Stop it audits those labels in the finished answer against the session transcript. It flags a Read citation to a file the session never opened, and a Bash citation whose command never ran ('command-not-found', warn-only by default). That is the read/executed label audit under other names. What it lacks is the web part. Its taxonomy lists WebFetch and WebSearch, but its README says those citations are not auto-checked. So it neither fails a web source that was never fetched nor tells a fetched page from a search-result snippet, and it has no 'observed' label. sudhanshu1402/receipts, claimcheck and groundtruth check free-text claims ('tests pass', 'I read the whole file', 'pushed')...

Strongest claim the search supports: Tools already exist that check per-claim labels and completion claims against the host agent's transcript for local files and shell commands (for example GroundCheck and receipts). As far as a search on 2026-09-24 found, no public agent skill or plugin does the same for web sources: failing a 'read' label whose page was never fetched, or was seen only as a search-result snippet, in the same audit that fails an 'executed' label whose command never ran.

| Project | Closeness | Evidence |
| :--- | :---: | :--- |
| https://github.com/frizfealer/grounding-attribution | close | GroundCheck, a Claude Code plugin (MIT, 0 stars, pushed 2026-06-29). A UserPromptSubmit hook tells Claude to mark every non-trivial claim as VERIFIABLE, with a tool citation such as Read(path:line), Bash(cmd), WebFetch(url) or WebSearch(query), or as unveri... |
| https://github.com/sudhanshu1402/receipts | close | A Claude Code plugin (installed as 'claimcheck') and a CLI (MIT, 0 stars, pushed 2026-09-24). Its README says it 'verifies what an AI coding agent claimed against the tool calls in its own session transcript', from a Stop hook. Opened: README and docs/CHECK... |
| https://github.com/ablanchard-dev/claimcheck | loose | A Claude Code Stop hook (GPL-3.0, 0 stars, pushed 2026-09-23). Opened: README. It reads the final message and tests recognised claims (test counts, 'fixed' after a code edit, pushes, commit SHAs) against tool output from the same turn. Each claim is verifie... |
| https://github.com/vnmoorthy/groundtruth | loose | A Claude Code Stop hook (MIT, 7 stars, pushed 2026-07-20). Opened: README. It blocks a completion claim ('Done.', 'all tests pass') when the same turn has no verifying tool observation, such as a passing test command or a Read/Grep confirming a symbol. It g... |
| https://github.com/EdbertChan/catstack/pull/870 | loose | A PR adding a 'claimed-search-not-run' advisory Stop-time check. Opened with WebFetch, so this description rests on a summary of the PR page. It reads the final message for a backticked code-search command (git log -S/-G/--grep, git blame, gh search) report... |
| https://github.com/mr-ubik/deeper-research | loose | A Claude Code deep-research plugin (Apache-2.0, pushed 2026-09-15). Opened: README and file tree. It archives the full text of every fetched page, grounds claim votes in the archived page, runs a quote-presence gate (skills/run/scripts/check-quotes.py) and... |
| https://github.com/udaysharmadev/gravitas | loose | An Antigravity skill and plugin (9 stars, pushed 2026-09-12). Opened: README. It describes a runtime evidence ledger ('Enforced runtime record') and a completion gate that uses host hooks. It gates completion on a record of evidence. I found no audit of per... |

### N1, search 1

Prior art found: yes.

Verdict: The claim as written does not hold, because its core mechanism already exists. Two public Claude Code Stop hooks, VectorInstitute/backcheck and ablanchard-dev/claimcheck, check claims in the agent's finished answer against the host's own transcript without an LLM, and flag or block a claim that a command ran when no matching tool call or result exists. That is the "executed never ran" half. The "read" half is partly covered by nousresearch/hermes-agent's grounded-citations skill, which rejects quotes that do not appear in fetched page text. Its ledger is filled by the agent, though, not taken from the host transcript. I found nothing that does all of the following together: parse explicit per-claim evidence labels (read/executed/observed); check each label against the host tool-call transcript; and fail a 'read' label whose page was never opened, or was seen only as a search-result su...

Strongest claim the search supports: "Tools such as backcheck and claimcheck already check whether a claim that a command ran is backed by the session transcript. As far as I could find, this is the first public agent skill that audits explicit per-claim evidence labels (read / executed / observed) against the host's actual tool-call transcript. It is also the first I found that fails a 'read' label when the page was never opened or was seen only as a search-result summary."

| Project | Closeness | Evidence |
| :--- | :---: | :--- |
| https://github.com/VectorInstitute/backcheck | close | README: 'reads the session transcript Claude Code already writes and checks the agent's claims against the record of what it actually ran'. Deterministic, zero LLM calls, runs as a Stop hook, and can block with --block. Verdicts are supported/unsupported/co... |
| https://github.com/ablanchard-dev/claimcheck | close | Claude Code Stop hook and plugin. It 'reads the agent's final message, finds the claims it recognises, and confronts each one with the tool output produced in that same turn', and 'checks that the command actually ran, by looking for the tool result that ba... |
| https://github.com/vnmoorthy/groundtruth | loose | Stop hook that blocks a turn ending on a completion claim ('Done.') unless tool observations in the same turn contain a successful verification artifact. It checks the transcript, but only for completion claims. It does not handle per-claim read/executed la... |
| https://github.com/aiimagined/godmode | loose | Keeps a hash-chained record of what the agent ran and changed, and 'grades every "done" against that record instead of against the agent's word'. Work with no record behind it renders as 'declared'. The record is its own ledger, not the host transcript's pe... |
| https://github.com/nousresearch/hermes-agent/blob/main/skills/research/grounded-citations/SKILL.md | close | Research skill with a URL ledger. Verbatim quotes are 'rejected unless they literally appear in the fetched page text', model-knowledge claims are flagged [unverified], and 'verify --evidence fails any draft whose cited sources carry no evidence'. The agent... |
| https://github.com/Pinperepette/grounded | loose | Claude Code hooks that block an Edit on a file the agent never Read, and block identifiers that Grep reported NOT FOUND. It enforces read-before-edit before the tool runs, not an audit of claims in a finished answer. |
| https://github.com/udaysharmadev/gravitas | loose | Antigravity skill plus a Native plugin with 'task-contract, evidence, and completion-gate hooks', reporting 'only what the evidence supports'. It gates completion. I found no audit of per-claim labels against the transcript in the README. |
| https://github.com/pandysp/claude-plugins | loose | The verify-claims skill has the model scan its own response for causal, state, historical, attribution and hedged claims and find proof for each. It works by instruction only, with no mechanical check against the transcript. |
| https://github.com/jimmandas/behavior-evidence | loose | Claude Code plugin whose gate_check.py rejects any claimed run whose trace ID the trace store does not hold ('Every claimed run must have a trace'). That applies to eval runs, not to evidence labels on claims in an answer. |

### N2, search 0

Claim tested: 

Prior art found: yes.

Verdict: No single public package I found combines all seven components, so the combination claim survives. Every individual component has prior art, though, and two packages come close. pedrohcgs/claude-code-my-workflow has a forked claim verifier with a tool list, loop-until-dry critics with a round cap, visual auditors, AI-voice detection and per-claim provenance status in passport.yaml. It lacks a vote-counting deduplication script, a transcript audit of labels and a script-measured prose score. cloudflare/security-audit-skill has fresh adversarial verifiers, coverage critics, deduplicated candidates, a validated ledger and verdict labels, but no prose standard or perceptual gates. The remaining components each appear separately: dinosn/raptor-loop-hunt has a ledger script, deduplication and a fixed K=2 dry-round stop. TheMizeGuy/anti-slop has a script-scored prose standard. vnmoorthy/grou...

Strongest claim the search supports: Each of these practices already exists in public agent skills and plugins, and some packages combine several of them (for example pedrohcgs/claude-code-my-workflow and cloudflare/security-audit-skill), but I have not found a public skill, plugin or agent pack that combines all seven in one package: evidence labels with provenance slots, a transcript audit of those labels, read-only verifiers enforced by tool lists, a vote-counting deduplication ledger script, a completeness critic with fixed stopping numbers, perceptual gates judged by a fresh critic, and a script-measured prose standard.

| Project | Closeness | Evidence |
| :--- | :---: | :--- |
| https://github.com/pedrohcgs/claude-code-my-workflow | close | Opened README and agent files (1598 stars, pushed 2026-08-24). It has a claim-verifier agent with context: fork and an explicit tool list (Read, Grep, Glob, WebFetch, WebSearch, Bash). That list includes Bash, so the tool list alone does not make it read-on... |
| https://github.com/cloudflare/security-audit-skill | close | Opened README (21107 stars, MIT, pushed 2026-09-14). The skill has a coverage-ledger.json with a validator script (validate-coverage-ledger.cjs), 'coverage critics to find gaps', and 'every unique candidate' sent to 'a fresh verifier that tries to disprove... |
| https://github.com/dinosn/raptor-loop-hunt | loose | Opened SKILL.md and the file tree (217 stars). It has a persistent ledger script (scripts/raptor-loop-ledger) whose 'add' refuses invalid executions, and it deduplicates candidates against FINDINGS.md and the judge-rejected set. It has a fixed stopping numb... |
| https://github.com/TheMizeGuy/anti-slop | loose | Opened README. A Claude Code plugin whose zero-dependency Node scanner (slop-scanner.mjs) scores prose for banned words, phrases and patterns deterministically ('Scan score: N/50'). A slop-detector agent adds a second review. This is precedent for a script-... |
| https://github.com/B143KC47/deep-research-skill | loose | Opened README (2 stars). A research skill with an evidence ledger CLI (scripts/research_ledger.py with add-evidence and lint), claim and evidence IDs, confidence labels, and an adaptive stop rule. Precedent for evidence labels with provenance slots plus a l... |
| https://github.com/jacob-balslev/skills | loose | Opened epistemic-grounding/SKILL.md. It defines claim-state labels (verified / source-supported / inferred / asserted / unverified / contradicted) with evidence receipts, plus a Chain-of-Verification procedure. These are instruction-level labels only. |
| https://github.com/vnmoorthy/groundtruth | loose | Confirmed the repo exists: 'A completion-claim gate for Claude Code. Refuses to let the agent say done without evidence.' This is the known precedent for a transcript-based audit of claims. It has none of the other components. |
| https://github.com/anthropics/claude-plugins-official | loose | Confirmed files plugins/claude-security/agents/scan-verifier.md, patch-verifier.md, code-modernization/agents/architecture-critic.md and the code-review plugin. These are verifier and critic agents spread across separate plugins, not one package. |

### N3, search 0

Claim tested: 

Prior art found: yes.

Verdict: The claim as worded is refuted. Suraj1235/open-dynamic-workflows (ODW, 38 stars, MIT) is public and ships an Antigravity plugin bundle and skill through `odw-daemon integrate antigravity`. It also appears in the antigravity-awesome-skills catalogue as an Antigravity skill. Its `verify` primitive runs a panel of adversarial critic agents, and only findings that pass a quorum survive (consensusThreshold, plus a weighted-vote consensus topology). That is adversarial multi-agent verification with voting, available for Antigravity. The author's skill still differs in two ways: - **Read-only verifiers:** ODW's README does not explicitly say its critics are read-only (worker agents get restricted tool lists such as read_file). - **Where the agents run:** on Antigravity, ODW runs its agents in its own external daemon with a separate model key or local Ollama, not as native Antigravity subagen...

Strongest claim the search supports: We found no other public Antigravity skill or plugin that uses Antigravity's own native subagents, restricted to read-only tools, as adversarial verifiers whose verdicts are combined by vote. The closest are Open Dynamic Workflows, which gives Antigravity quorum-voted adversarial critics but runs them in its own external daemon, and Google's built-in /teamwork-preview, which has independent Critic, Challenger and Auditor agents but no voting.

| Project | Closeness | Evidence |
| :--- | :---: | :--- |
| https://github.com/Suraj1235/open-dynamic-workflows | close | I read the raw README (38 stars, created 2026-06-05, last pushed 2026-07-09). It says `odw-daemon integrate antigravity` "installs official-layout Antigravity plugin bundles" at ~/.gemini/config/plugins/odw, ~/.gemini/antigravity-cli/plugins/odw and .agents... |
| https://antigravity.google/docs/teamwork/ | close | This is Google's own built-in /teamwork-preview feature. According to the docs page as I fetched it (through a WebFetch summary), it defines read-only Explorers ("without modifying any source files") plus separate verifier roles: Critic (independent code re... |
| https://antigravity.google/docs/subagents/ | loose | Google's built-in /boost is a "three-tier multi-agent reasoning hierarchy" with "independent verification loops". Custom subagents can be limited to read tools through a `tools` frontmatter list (e.g. view_file, grep_search). The docs describe no voting mec... |
| https://github.com/jm2/OpenCode-Team | loose | I read the README. It describes itself as "A community replica of Google Antigravity's `/teamwork-preview`". It has team/verifier ×N subagents that cannot edit ("permission.edit: deny" plus a runtime guard that refuses write tools for read-only sessions), a... |
| https://github.com/udaysharmadev/Gravitas | loose | I read the README. It is an Antigravity skill plus an agy plugin ("Gravitas Native") with task-contract, evidence and completion-gate hooks, and it scales verification with risk ("A read-only question should not trigger a committee"). It is single-agent evi... |
| https://github.com/kleinric/antigravity-plugin | loose | This is a multi-host plugin that installs in agy itself (`agy plugin install antigravity@sakibsadmanshajib`) and offers code review of uncommitted changes. The README as fetched says nothing about adversarial or multi-reviewer voting. Related Claude-Code-si... |

### N4, search 0

Claim tested: 

Prior art found: yes.

Verdict: The claim as worded does not hold up. Its core test already exists in public agent skills as a general rule. randommonicle/claude-skills (verify-the-effect plus the NORMS.md norm) states almost exactly the same thing: \"A success indicator that can be true while the effect is absent proves nothing\", and \"Never report success from a proxy signal ... assert the actual effect or artifact.\" Its sibling skill prove-it-can-fail asks of every check \"what does this output if the thing it guards is broken?\" rstest's \"Verify Behavior, Not Proxies\" skill and Invoker's prove-it skill say the same for code. What none of these do is apply the test across fields: every one uses only software, CI or ops examples. None gives worked examples for law, medicine, design or research, and none explicitly says to keep the proxy alongside the real check (verify-the-effect says to assert the real effect...

Strongest claim the search supports: Other public agent skills already use the proxy test for code (for example randommonicle/claude-skills: \"a success indicator that can be true while the effect is absent proves nothing\"). As far as a search limited by GitHub rate limits could find, this is the first to state it as one rule across code, law, medicine, design and research, with worked examples in each field and an explicit instruction to keep the proxy and add the real check.

| Project | Closeness | Evidence |
| :--- | :---: | :--- |
| https://github.com/randommonicle/claude-skills/blob/HEAD/verify-the-effect/SKILL.md | close | Opened. Its rule section reads: "A success indicator that can be true while the effect is absent proves nothing. Identify the real intended effect ... and assert that." NORMS.md turns this into an always-on norm: "Never report success from a proxy signal (g... |
| https://github.com/randommonicle/claude-skills/blob/HEAD/prove-it-can-fail/SKILL.md | close | Opened. It asks of every check: "what does this output if the thing it guards is broken?" If the answer is still green, "the check is theatre." It adds rules such as "A check whose two operands share a source is theatre." This is the same question from the... |
| https://github.com/web-infra-dev/rstest/blob/HEAD/.agents/skills/verify/SKILL.md | close | Opened. Its heading is "Verify Behavior, Not Proxies" and it keeps a list of "Forbidden proxies" (typecheck or lint green, build succeeded, a tool accepted your config). A change counts as verified only when the real behavior change has been observed. It is... |
| https://github.com/Neko-Catpital-Labs/Invoker/blob/HEAD/skills/prove-it/SKILL.md | close | Opened. It says: "Never trust a proxy signal ... as evidence for a different claim ,  check the literal thing that was reported broken", and a repro must exercise the reported behavior itself, "not a proxy such as 'a related test passed'". Its example is la... |
| https://github.com/m0n0x41d/haft/blob/HEAD/internal/cli/skill/h-verify/SKILL.md | loose | Opened. The h-verify skill asks: "the measured proxy improved ,  what got worse?" and calls a reflexive answer "the Goodhart failure mode". The h-compare skill says: "Name what each target is a proxy for." Both are about Goodhart in decisions over measured... |
| https://github.com/mohitagw15856/pm-claude-skills/blob/HEAD/skills/metric-gaslighting-detector/SKILL.md | loose | Opened. Its list of metric distortions includes "The vanity proxy ,  measuring what moves instead of what matters" and "Goodhart's ghost". It applies only to business dashboards and KPIs. |
| https://github.com/anthropics/claude-plugins-official/blob/HEAD/plugins/skill-creator/skills/skill-creator/agents/grader.md | loose | Opened. The grader fails evidence that is superficial ("correct filename but empty/wrong content") and asks for discriminating assertions: "it passes when the skill genuinely succeeds and fails when it doesn't." This is the proxy idea applied to eval assert... |

## All 63 Candidates

Found by six searches: Claude Code and Anthropic skills, Antigravity and Gemini CLI, evidence and provenance tools, multi-agent review, anti-slop tools and visual verification. The 18 read in depth are above.

| Project | Stars | Found by | Summary |
| :--- | ---: | :--- | :--- |
| [obra/superpowers](https://github.com/obra/superpowers) | 290805 | claude-skills, multi-agent-review | The most-starred agentic skills pack. Its verification-before-completion skill is the canonical 'evidence before claims' skill: 'NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE', a five-step gate (identify, run, read, verify, cl... |
| [nousresearch/hermes-agent](https://github.com/NousResearch/hermes-agent/tree/main/skills/research/grounded-citations) | 248479 | evidence-provenance | A bundled skill whose stdlib Python ledger script (sources.py) owns the URL-to-id mapping. The agent must register every URL at retrieval time and may cite only the small integer ids the ledger hands back, never a URL from memory. Merged... |
| [anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md) | 177854 | claude-skills, visual-verification | Anthropic's reference skill for testing local web apps with native Python Playwright scripts. It includes a with_server.py helper to manage dev servers, a decision tree for static versus dynamic apps, and a reconnaissance-then-action pat... |
| [garrytan/gstack](https://github.com/garrytan/gstack/blob/main/design-review/SKILL.md) | 134045 | claude-skills, visual-verification | A 23-tool skill pack. Its /design-review skill audits a live site through a scripted browser. Every finding needs at least one screenshot, and before/after screenshots re-verify each fix. A design detector (impeccable) scans the rendered... |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable/blob/main/.claude/skills/impeccable/reference/critique.md) | 70462 | visual-verification | A design skill whose critique command requires two assessments to run as two isolated, parallel sub-agents that must not see each other's output. Assessment A is an LLM design review of source plus the live page in a browser. Assessment... |
| [blader/humanizer](https://github.com/blader/humanizer) | 51711 | anti-slop | The most-starred humanizer skill. It works from 25 numbered patterns taken from Wikipedia's 'Signs of AI writing', in five groups: staging instead of stating, rhythm by rule, inflation and borrowed authority, formatting by rule, and chat... |
| [imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 49320 | evidence-provenance, multi-agent-review | A Claude Code suite for academic work, from research through writing and review to finalising. Stages 2.5 and 4.5 are mandatory integrity gates that run a 7-mode blocking checklist. v3.7.x added trust-chain frontmatter and three-layer ci... |
| [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | 46846 | gemini-antigravity | The largest skill library carrying the Antigravity name (formerly antigravity-awesome-skills; 2,346 top-level SKILL.md files in the tree I listed), with the 'AAS Core' catalog, MCP and validator. It bundles verification-related skills, i... |
| [wshobson/agents](https://github.com/wshobson/agents) | 39914 | multi-agent-review | A multi-harness plugin marketplace: 94 plugins, 202 agents, 183 skills and 105 commands from one Markdown source. The Makefile generates Antigravity plugins. The agent-teams plugin adds /team-review, which runs parallel reviewers across... |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 36672 | claude-skills, multi-agent-review | Anthropic's official plugin directory. Three of its plugins are relevant. math-olympiad strips the solver's thinking and hands the cleaned proof to a fresh-context adversarial verifier with no tools. code-modernization/workflows/extract-... |
| [openai/skills](https://github.com/openai/skills/blob/main/skills/.curated/playwright-interactive/SKILL.md) | 27593 | visual-verification | A curated Codex skill for persistent Playwright sessions against web and Electron apps. Functional QA and visual QA are separate passes. A shared QA inventory maps every user-visible claim to a check and a reviewed screenshot. page.evalu... |
| [voltagent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 25291 | multi-agent-review | A catalog of 161+ Claude Code subagents in 10 categories. The quality-security plugin includes code-reviewer, architect-reviewer, security-auditor, qa-expert, ui-ux-tester and ai-writing-auditor. The README's tool policy says reviewers a... |
| [everyinc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) | 25241 | multi-agent-review | A 36-skill plugin built around the loop brainstorm, plan, work, simplify, review, compound. The ce-code-review guide describes reviewer personas chosen by risk and dispatched in parallel. Synthesis validates each finding, anchors it to t... |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 21000 | multi-agent-review | A six-phase security-audit skill: reconnaissance, coverage-led hunting by isolated hunters, candidate validation, structured output, independent record verification and reporting. A fresh verifier tries to disprove every unique candidate... |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 17537 | anti-slop | A skill file with reference lists of banned phrases (phrases.md), structural clichés (structures.md: binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, false agency, passive voice) and before/after examples.... |
| [wanshuiyin/auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 16583 | multi-agent-review | Markdown-only skills for autonomous ML research in which an executor model drives the work and a different model family (Codex by default) reviews. The audit stack is experiment-audit, result-to-claim, paper-claim-audit and citation-audi... |
| [anthropics/defending-code-reference-harness](https://github.com/anthropics/defending-code-reference-harness) | 7516 | multi-agent-review | A reference vulnerability discovery and remediation harness with the skills /threat-model, /vuln-scan, /triage, /patch, /dnr-hunt and /dnr-respond, plus a pipeline that runs recon, find, verify, report and patch. The README says it is no... |
| [trailofbits/skills](https://github.com/trailofbits/skills/tree/main/plugins/fp-check) | 7221 | claude-skills | Trail of Bits' security skills marketplace, with about 40 plugins including differential-review, variant-analysis, second-opinion and mutation-testing. The fp-check skill verifies a suspected vulnerability to a TRUE POSITIVE or FALSE POS... |
| [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) | 5692 | anti-slop | A Korean humanizer: 10 categories and 85 sub-patterns, with translationese as the main target. A deterministic shim (prepare_monolith_input.py) scores the input first and picks one of three routes. The light route is one call and ends ea... |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 4701 | anti-slop, claude-skills | An audit-and-rewrite skill with 74 pattern categories and a 112-entry tiered word-replacement table. It has three modes: rewrite, detect only, and edit in place. Edit mode refuses source code and config files. The --iterate 1\|2 flag cap... |
| [oneredoak/claude-code-workflows](https://github.com/OneRedOak/claude-code-workflows/blob/main/design-review/design-review-agent.md) | 3891 | claude-skills, visual-verification | A Claude Code design-review subagent and slash command. It works 'Live Environment First' through the Playwright MCP, in seven phases: interaction, responsive screenshots at 1440/768/375, visual polish, WCAG 2.1 AA, robustness, code heal... |
| [nanako0129/sepia](https://github.com/Nanako0129/sepia) | 2814 | anti-slop | A de-AI writing skill with four operations (write, review, refactor, recreate). Fiction goes through three passes: narrative architecture, discourse flow, then surface style. The fiction passes are grounded in StoryScope (arXiv:2604.0313... |
| [neolabhq/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) | 1720 | evidence-provenance | A plugin marketplace for reducing hallucination and bias. It includes reflexion (/reflect, /critique, /memorize), sadd (/do-and-judge, /judge-with-debate, /do-competitively) and an FPF reasoning agent. It ships an Antigravity build with... |
| [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) | 1598 | claude-skills, evidence-provenance | A forkable Claude Code setup for academic work. Its /verify-claims skill runs Chain-of-Verification. It extracts claim-and-citation pairs and hands them to a claim-verifier agent in a forked context that never sees the draft. The verifie... |
| [199-biotechnologies/claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill) | 1141 | evidence-provenance | A deep-research skill with an 8-phase pipeline and four named modes: Quick, Standard, Deep and UltraDeep. It retrieves in parallel, triangulates (3+ sources per major claim), critiques with loop-back to retrieval, and red-teams with mult... |
| [agricidaniel/banana-claude](https://github.com/AgriciDaniel/banana-claude/blob/main/agents/visual-critic.md) | 1057 | visual-verification | An image-generation plugin with an optional visual-critic subagent. The critic's frontmatter grants only the Read tool, with maxTurns 8. It inspects pixels against a frozen brief whose sha256 hash it must verify, and ignores the generato... |
| [sunbigfly/ppt-agent-skills](https://github.com/sunbigfly/ppt-agent-skills/blob/main/references/prompts/step4/tpl-page-review.md) | 900 | visual-verification | A code-driven slide-generation skill. Each slide's HTML is screenshotted and reviewed by a per-page review sub-agent, whose prompt forbids reading the outer SKILL.md or global rules so its context stays isolated. After review, scripts/vi... |
| [sangrokjung/claude-forge](https://github.com/sangrokjung/claude-forge) | 844 | claude-skills | A Claude Code bundle of 16 agents, 33 skills, 14 rules and safety hooks. Version 4.0 added an adversarial verification loop in which the agent that checks a change never wrote it. Its adversarial-reviewer runs in a fresh context, never s... |
| [vibeeval/vibecosystem](https://github.com/vibeeval/vibecosystem/blob/main/skills/factcheck-guard/SKILL.md) | 535 | evidence-provenance | One skill inside a large agent and skill bundle. Every factual claim about the codebase must carry a mandatory confidence marker. [VERIFIED] means the agent read the file and traced the logic, and it must cite file:line. [INFERRED] means... |
| [harshaneel/humanize](https://github.com/harshaneel/humanize) | 495 | anti-slop | Two static rule-based skills. 'humanize' applies nine levers taken from the detection literature (including burstiness enforcement, structural flattening, punctuation normalisation and RLHF voice strip), followed by an audit-revise loop.... |
| [theclaymethod/unslop](https://github.com/theclaymethod/unslop) | 471 | anti-slop | An agent skill with four commands (teach, cleanup, rewrite, mimic). Detection uses three stdlib scanners that output JSON and exit non-zero on a flag. The phrase layer has contextual false-positive gating. The structure layer (structure_... |
| [josstei/maestro-orchestrate](https://github.com/josstei/maestro-orchestrate) | 463 | gemini-antigravity | Multi-agent orchestration with 39 specialists and a 4-phase Standard workflow (Design, Plan, Execute, Complete) with approval gates. Final review blocks on unresolved Critical or Major findings. An Express path handles simple work, and s... |
| [agent-sh/agnix](https://github.com/agent-sh/agnix) | 423 | claude-skills | A Rust linter and language server for agent configuration files. It has 456 rules covering Agent Skills SKILL.md (31 rules), Claude Code CLAUDE.md, hooks, agents and plugins (53), Gemini CLI (9), Cursor, Kiro, Copilot, Cline, MCP and AGE... |
| [dsifry/metaswarm](https://github.com/dsifry/metaswarm) | 419 | gemini-antigravity | Multi-agent orchestration framework with 18 agent personas and 13 skills. Each work unit runs IMPLEMENT → VALIDATE → ADVERSARIAL REVIEW → COMMIT. It has a parallel 5-agent design review gate, a 3-reviewer adversarial plan review, cross-m... |
| [socialpranker/deepdive](https://github.com/Socialpranker/deepdive) | 377 | claude-skills, evidence-provenance | A 13-phase research skill. Every claim links as [sNN] to a source file holding verbatim quotes, recorded in claims.csv and numbers.csv. Verification has four layers: liveness, faithfulness (does the quote entail the claim: SUPPORTED, PAR... |
| [devswha/patina](https://github.com/devswha/patina) | 359 | anti-slop | A deterministic, pattern-based humanizer for Korean, English, Chinese and Japanese, with 189 named patterns. It has audit, score, diff, verify and rewrite modes. `patina --score --offline --exit-on 30` is a deterministic CI gate that nee... |
| [k-dense-ai/science-superpowers](https://github.com/K-Dense-AI/science-superpowers) | 339 | gemini-antigravity | A reimplementation of Superpowers for computational science. It uses pre-registration instead of TDD: hypotheses, predictions and decision rules are locked before outcomes are seen. It has reproducible workspaces, 'verifying-results-befo... |
| [aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | 255 | anti-slop | A humanizer and detector with 55 patterns and 5 voices. An optional zero-dependency Node CLI scores text 0-100 from four measurable signals rather than a pattern count: lexical tell density, trigram repetition, burstiness (sentence-lengt... |
| [dinosn/raptor-loop-hunt](https://github.com/dinosn/raptor-loop-hunt) | 217 | multi-agent-review | A looping, multi-altitude security hunt. Each round generates candidates from raw source with an independent reasoner, judges each one with a separate reasoner prompted to refute it, live-verifies the survivors and records everything in... |
| [eric-tramel/slop-guard](https://github.com/eric-tramel/slop-guard) | 164 | anti-slop | A rule-based prose linter with no LLM judge. It scores text 0-100 using 24 configurable rules backed by 200+ literal and structural heuristics. The rules cover sentence and paragraph rhythm, em-dash and colon overuse, arbitrary mid-sente... |
| [serhiikorniienko/bullshit-detector](https://github.com/SerhiiKorniienko/bullshit-detector) | 148 | evidence-provenance | Fact-checks videos, articles, tweets or PDFs claim by claim. Verdicts are confirmed, plausible, misleading, false or unverifiable, plus a 0–10 BS score. The rule is "no source, no verdict": the skill may not confirm or refute from model... |
| [mohamedabdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop) | 146 | gemini-antigravity | CLI, MCP server and skill that strips AI writing patterns: tricolons, em-dash overuse, hedging, sycophancy openers, repeated '- **Label:**' bullet stacks, title-case headings. It has structural passes, a saved numeric voice profile (sent... |
| [roundpilot/superpowers-antigravity](https://github.com/roundpilot/superpowers-antigravity) | 70 | gemini-antigravity | A native Antigravity 2.0 rebuild of obra/superpowers. It uses invoke_subagent with bundled reviewer agents (code-reviewer, spec-reviewer, re-reviewer), a fresh subagent per task with two-stage review, and a browser-testing skill with 'ev... |
| [ownweights/argus](https://github.com/ownweights/argus) | 43 | visual-verification | An agentic visual UI-testing tool with a bounded six-stage pipeline: Validator, Comprehender, Explorer, Strategist, Executor, Critic. The Critic independently reviews the request, the execution and the evidence before a verdict is accept... |
| [cryptonerdcn/ui-visual-validator-agent](https://github.com/cryptonerdcn/UI-Visual-Validator-Agent/blob/main/ui-visual-validator.md) | 40 | visual-verification | A single Claude Code subagent meant to counter Claude's lenient visual validation and visual hallucinations. It assumes by default that a UI change has NOT succeeded, judges only from screenshots and ignores code hints, verifies position... |
| [wan-huiyan/agent-review-panel](https://github.com/wan-huiyan/agent-review-panel) | 35 | multi-agent-review | 4 to 6 persona reviewers work independently, debate for 1 to 3 rounds and give blind final scores. A completeness-audit agent then looks for what the panel missed, severity verification reads the code for every P0 and P1, and a supreme j... |
| [pjt222/agent-almanac](https://github.com/pjt222/agent-almanac) | 34 | gemini-antigravity | Library of 373 skills, 76 specialist agents and 22 pre-built review teams, with a 'Validate Skills' CI workflow, 30 test scenarios and a translation pipeline. README translation table: zh-CN 343/373 skills, ja 347/373, plus de, es and st... |
| [ncoevoet/claude-review-all](https://github.com/ncoevoet/claude-review-all) | 28 | claude-skills | A /review-all code-review plugin: deterministic gates, ten parallel review agents, then a pass where a hostile verifier re-checks every finding. scripts/dedupe.py merges findings that share a root cause, and a state sweep remembers which... |
| [ilien-dev/quiron](https://github.com/ilien-dev/quiron) | 26 | anti-slop | A humanizer that measures its own work. scripts/aimeter.py measures 23 rates (for example long words, nominalizations, em dashes and lists of three per 1k words) and compares each with a human band: p10-p90 of 167 pre-ChatGPT dev.to post... |
| [electricsheephq/worldos](https://github.com/electricsheephq/WorldOS/blob/main/.claude/skills/visual-critic/SKILL.md) | 23 | visual-verification | A visual feedback loop for game renders. Critic subagents read the render and return text-only findings, so the builder never loads the pixels. A panel of 5-7 independent lens subagents scores the gap to named reference frames. Determini... |
| [osolmaz/ai-smell](https://github.com/osolmaz/ai-smell) | 14 | anti-slop | A stylometric study of AI writing tells. analyze.py and companion scripts strip code, then measure per 1k words: em dashes, semicolons, colons, the sentence-length distribution and fragment share, labeled bullets (a short label, a separa... |
| [udaysharmadev/gravitas](https://github.com/udaysharmadev/Gravitas) | 9 | gemini-antigravity | A different project with the same name: 'Claude-like engineering discipline for Gemini', described as a research preview. Core is a behavioural skill (task contract, read-before-write, external validation, evidence-backed completion). Na... |
| [pablo-aps/prove-it](https://github.com/Pablo-aps/prove-it) | 9 | gemini-antigravity | Adversarial verification skill: 'Don't try to prove it works. Try to prove it doesn't.' It turns a 'done' claim into a falsifiable claim, runs the most decisive checks, and returns PROVEN, FAILED, NOT PROVEN or BLOCKED with the evidence.... |
| [vnmoorthy/groundtruth](https://github.com/vnmoorthy/groundtruth) | 7 | evidence-provenance | A Stop hook that reads the session transcript (transcript_path JSONL) and blocks the turn with {decision:block} when the assistant makes a completion claim ("Done", "tests pass", "fixed") and no tool call in the same turn produced matchi... |
| [aiimagined/godmode](https://github.com/AIimagined/Godmode) | 6 | gemini-antigravity | Keeps a hash-chained local record of what the agent actually ran, changed and refused, and grades every 'done' against that record rather than the agent's word. Work with no backing record is shown as 'declared'. A 'claim --scan' checks... |
| [kigiela/16-eyes](https://github.com/kigiela/16-eyes) | 4 | gemini-antigravity | Security audit pipeline. It profiles the repo and designs tailored 'lenses'. Every finding gets an independent skeptical re-check against the real code, and high-impact findings go to several refuter agents. The output is a markdown repo... |
| [tonydzi/verbatim-citation-gate](https://github.com/tonydzi/verbatim-citation-gate) | 3 | evidence-provenance | A two-stage citation auditor. Stage 1 is deterministic, uses no tokens and costs nothing. It checks that a quoted passage appears contiguously in the cited document. That catches fabricated quotes, "frankenquotes" stitched from real word... |
| [aliradid/citation-needed](https://github.com/aliradid/citation-needed) | 0 | evidence-provenance | Extracts every factual claim from a draft, checks each against live sources and returns an evidence ledger. Statuses are VERIFIED, PARTIAL, UNVERIFIED, CONTRADICTED, OUTDATED, MISATTRIBUTED, PARAPHRASED, MISLEADING, SKIPPED and UNCHECKED... |
| [mizcausevic-dev/evidence-labeling-protocol](https://github.com/mizcausevic-dev/evidence-labeling-protocol) | 0 | evidence-provenance | A behavioural skill that enforces five evidence labels on every claim: Observed (directly inspected), Executed (a command ran and its raw result is available), Verified (checked against a defined pass/fail bar), Predicted (not yet run) a... |
| [j-withmission/design-director](https://github.com/j-withmission/design-director) | 0 | visual-verification | A design-process skill that runs a separate critic which sees only a screenshot and never the code, so the agent is not grading its own work. It has three cost tiers: a Sonnet pairwise spot check that produces no score, a Review loop wit... |
| [classified-ai-core/skill-library](https://github.com/Classified-AI-Core/skill-library/blob/main/skills/design-and-image/screenshot-critique/SKILL.md) | 0 | visual-verification | screenshot-critique spawns one fresh, 'unprimed' sub-agent with fork_context false. It receives only the full screenshots plus 2x-4x crops and a neutral task, never the thread history, implementation details or the defect the main agent... |
| [mr-ubik/deeper-research](https://github.com/mr-ubik/deeper-research) | 0 | multi-agent-review | Extends Claude Code's /deep-research. It archives full page text verbatim, and claims are verified by independent votes grounded in the archived page, with a mechanical check that the quote is present. Every run plants known-false decoy... |
| [edgebuildlabs/evidence-contracts](https://github.com/edgebuildlabs/evidence-contracts) | 0 | gemini-antigravity | A drop-in AGENTS.md contract: 'Every claim of state carries a source and a date ,  or the words NOT VERIFIED.' Marks take the form file:line (date), 'command (now)' or 'URL (date)'. It includes a STARTED ≠ COMPLETED ≠ VALIDATED ≠ PASS la... |

