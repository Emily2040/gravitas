# Gravitas

**English** · [简体中文](https://github.com/Emily2040/gravitas/blob/main/README.zh-CN.md) · [日本語](https://github.com/Emily2040/gravitas/blob/main/README.ja.md) · [한국어](https://github.com/Emily2040/gravitas/blob/main/README.ko.md)

This is the copy of the README that the installer placed inside the plugin. The full version, with the test results and the comparison with other skills, is on [GitHub](https://github.com/Emily2040/gravitas), which is private during the beta.

## Part 1: What You Just Installed

Gravitas makes your Antigravity agent prove its work before it tells you it is done.

AI agents can check the easy part of a job, find it fine and report that the whole job is fine. In testing, the most common mistake was an agent saying it had read a source it never opened. Gravitas gives the agent three habits:

1. Say how you know. Every claim carries a label: I looked at it, I ran it, I read it and here is the line, or I worked it out or remembered it.
2. Check the real thing, not the easy thing next to it.
3. Let someone else try to break it. Separate inspector agents look for mistakes and gaps, and they have no tool that edits files.

For example, told that a positive result on a "99% accurate" test for a 1-in-10,000 condition means a 99% chance of having it, and asked to confirm, Gravitas said no: the real figure is about 1 in 102. It showed the working, and gave a command for each calculated number that you can run yourself.

It switches on by itself for work where a wrong answer costs something: audits, debugging, changes across many files, design work, research, law, medicine, mathematics, money and history. Quick questions get quick answers.

A checked answer takes longer and uses more of your plan than a quick one: about 100 seconds for the example above, and about 6 minutes for a full audit of a small project. It cannot make the model smarter or check what nobody can check; when nothing is available to check against, it labels the claim as reasoning. It is a private beta, tested on Windows 11 with Google's Gemini models.

To turn it off, run `agy plugin disable gravitas`, Antigravity's documented command for plugins, and `agy plugin enable gravitas` to turn it back on. To report a problem, use the links on the author's [GitHub profile](https://github.com/Emily2040).

## Part 2: What Is In This Folder

```text
plugin.json                  manifest: the name and description Antigravity lists
rules/AGENTS.md              always-on rule: when to load the skill, and three rules that hold while it is in use
agents/                      eight agents with fixed tool lists
skills/gravitas/SKILL.md     the router; it loads references/00-orchestrator.md
skills/gravitas/references/  fourteen modules, each 100 lines or fewer so one view_file call reads it whole
skills/gravitas/schemas/     the finding and verdict records subagents return
skills/gravitas/scripts/     ledger.py, provenance_check.py, check_skills.py, slopcheck.py
skills/gravitas/examples/    a gate suite that goes red on the scene it was built from
```

How a run goes. The rule is always loaded. On a task that qualifies, the agent opens the skill, which routes it to the orchestrator. The orchestrator answers trivial questions directly. Otherwise it writes a task record, picks a scale (quick, standard, full or exhaustive) with fixed numbers for fan-out, votes and stopping, and names the modules to load. Work lists are built with real tools, specialists fan out with absolute paths and a return schema, load-bearing claims go to independent checks, a completeness critic names what was never checked, and the report ranks findings with their tiers and gaps.

| Tier | What must have happened |
| :--- | :--- |
| `observed` | The artifact itself was inspected, and the label names it |
| `executed` | A tool ran and returned the value, and the label shows the command or query and what it returned |
| `read` | A source was retrieved, and the label gives the URL or path and quotes the line |
| `inferred` | Reasoning or recall; everything whose slot cannot be filled |

None of the agents has a file-editing tool. The checker can run commands and is told never to modify the work under review; the prose editor returns its edited text instead of writing it.

| Agent | Job | Tools |
| :--- | :--- | :--- |
| `gravitas-scout` | Locate files, routes, symbols and sources | `list_dir`, `find_by_name`, `grep_search`, `view_file` |
| `gravitas-reader` | Answer questions about named files or URLs, quoting lines | `view_file`, `grep_search`, `find_by_name`, `list_dir`, `read_url_content` |
| `gravitas-finder` | Hunt one kind of defect across a work list | the reader's tools and `search_web` |
| `gravitas-checker` | Run one independent check | `view_file`, `run_command` |
| `gravitas-refuter` | Try to refute one claim, defaulting to refuted | `view_file`, `grep_search`, `read_url_content`, `search_web` |
| `gravitas-visual-critic` | Judge a screenshot as a viewer who has not seen the source | `view_file` |
| `gravitas-completeness-critic` | Name what was never searched, opened, run or verified | `view_file`, `list_dir`, `grep_search`, `find_by_name` |
| `gravitas-prose-editor` | Edit a draft to the prose standard | `view_file` |

Scripts, run from this folder. `--latest` checks against the most recent conversation, and a conversation's id is the folder name under `~/.gemini/antigravity-cli/brain/`, or `conversation_id` in `agy -p --output-format json` output.

```bash
python skills/gravitas/scripts/check_skills.py          # validate every skill, agent, rule and plugin under ~/.gemini/config
python skills/gravitas/scripts/provenance_check.py <answer> --latest   # check evidence labels against the transcript
python skills/gravitas/scripts/ledger.py --help         # bookkeeping for fan-outs: dedupe, votes, dry rounds
python skills/gravitas/scripts/slopcheck.py <files>     # structural markers of generated prose; --strict fails on any flag
```

What testing showed so far. On the answers from beta 2 testing, the provenance checker held all 6 labels of a law answer whose sources were opened and failed the citations that were never opened. The full audit test case found all three planted defects. There is no clean comparison with Antigravity alone yet; that benchmark is the next piece of work.

Limits. Most of the method is instruction the model is asked to follow; the tool lists and the four scripts are the mechanical parts, and the scripts run when the agent is told to run them. It was tested on agy 1.2.9 on Windows 11. Platform behaviour that affects how you use it is in `skills/gravitas/references/13-platform.md`. Two points matter most: headless `agy -p` runs need explicit permission grants or a `toolPermission` setting in `~/.gemini/antigravity-cli/settings.json`, and the CLI reads a repository's own `.agents/` folder only when the repository is passed with `--add-dir`, which is why this plugin installs globally.

Version 1.0.0-beta.2 · MIT · by [Iamemily2050](https://github.com/Emily2040)
