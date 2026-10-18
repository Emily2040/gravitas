# Gravitas

**English** · [简体中文](https://github.com/Emily2040/gravitas/blob/main/README.zh-CN.md) · [日本語](https://github.com/Emily2040/gravitas/blob/main/README.ja.md) · [한국어](https://github.com/Emily2040/gravitas/blob/main/README.ko.md)

This is the copy of the README that the installer placed inside the plugin. The full version, with real examples in several languages, every test result and the comparison with other tools, is on [GitHub](https://github.com/Emily2040/gravitas).

## Part 1: What You Just Installed

Gravitas asks your Antigravity agent to answer the way the best person for your request would, to check what the answer depends on, and to tell you kindly when something you assumed is wrong.

It adds a short rule to every conversation. The rule asks the agent to read your words as you meant them, and to give what the best person for this request would give: a good editor for an email, an engineer for a bug, a clinician for a dosing question. It leads with what you need first. It tests what you will rely on the way you will use it: it follows steps to the end, runs code, opens the official page for a rule that changes, and counts with a script where a count matters. It states each claim as surely as the evidence allows, names the place and date a rule depends on, and gives a range with its reasons where it cannot be exact. When something you assumed is wrong, it says so kindly, corrects only as far as the error reaches, and still gives you what you came for. It writes for whoever will read the piece, in your language and its conventions, and takes technical writing about 80% of the way to ASD-STE100 Simplified Technical English, or to your language's own plain technical style.

Under all of it sits a floor: never worse than a plain answer. The reply keeps everything a strong plain answer would give, and holds no status lines, labels or notes about checks in progress. Warning signs and helplines appear where a clinician would read danger still ahead, and someone who may be in danger is answered the way a trained crisis counsellor would speak to them.

For example, asked "git: how do I undo my last commit but keep the changes staged?", plain Antigravity on Gemini 3.8 Flash gave the right command. With Gravitas it gave the same command and one more sentence: if the commit is already on a shared server, undoing it takes a force push, which "can disrupt collaborators".

That example and the older numbers below were measured on the previous rule (v4). This release's rule was rebuilt from a first-principles study of v4's clear losses to plain Antigravity or `/boost`: 109 real losses, ten mechanisms, and four drafts attacked by an adversary. It passed a release check from a real install. That check ran 17 cases: chat and role play were fine in all four languages, and after two fixes to the part of the rule that covers someone who may be in danger, the crisis case in each language was judged better than plain Antigravity on the same model. It has not yet had the full benchmark. The edge set (history, deep knowledge, wordplay, creative) and some models (Codex Astra, Grok 4.5) were where v4 did not win, and they are what the rebuild targets.

For work one pass cannot check, such as an audit, a review, a change across many files, a research report or a build, the agent loads the deep-work skill. There it says how it knows each claim, and separate inspector agents, which have no tool that edits files, look for mistakes and gaps.

If you installed with `--review`, the Second Opinion is on: an answer you will rely on, act on or send goes to an independent reviewer on Gemini 3.1 Pro, which names at most three mistakes, and the agent fixes only those before you see the answer. While you wait, a one-line message says the answer is being checked once more. The double-click installer does not install it; the terminal install with `--review` does.

What it costs. On Gemini 3.8 Flash, on 60 everyday requests, a median answer took 35 to 36 seconds with the v4 rule against 22 to 23 without it, and 80 to 81 seconds with the Second Opinion. On Gemini 3.1 Pro the rule added a few seconds. This release's rule is longer than v4's, 1,216 words against 809, and these figures do not cover it. Deep work takes minutes and runs several agents at once.

What it cannot do. It cannot make the model know more than it does. Its rules are instructions, and the model can miss them or apply them where they do not belong. Every benchmark run used the `agy` command-line tool on Windows 11; the desktop app was not benchmarked, and the Mac installer has not been run on a real Mac.

To remove it, double-click the installer again and choose Remove Gravitas, or run `python scripts/install.py --uninstall` from the downloaded folder. Either moves the plugin into a folder named for the date and time inside `.gemini/gravitas-backups` in your home folder. To turn it off without removing it, run `agy plugin disable gravitas`, and `agy plugin enable gravitas` to turn it back on; neither prints anything when it works, and reinstalling does not turn it back on. To add or remove the Second Opinion, run `install.py` again with `--review` or `--no-review`, plus your language code if you installed one. To report a problem, use the links on my [GitHub profile](https://github.com/Emily2040).

## Part 2: What Is In This Folder

```text
plugin.json                  manifest: the name and description Antigravity lists
rules/AGENTS.md              always-on rule: the best answer for this person, the floor, the Second Opinion if installed, when to load the skill
agents/                      eight agents with fixed tool lists, and gravitas-reviewer if installed with --review
skills/gravitas/SKILL.md     the router for deep work; it loads references/00-orchestrator.md
skills/gravitas/references/  fifteen modules, each 100 lines or fewer so one view_file call reads it whole
skills/gravitas/schemas/     the finding and verdict records subagents return
skills/gravitas/scripts/     ledger.py, provenance_check.py, check_skills.py, slopcheck.py
skills/gravitas/scripts/checks/  six counting checks for verse, numbers and dates, with their data
skills/gravitas/examples/    a gate suite that goes red on the scene it was built from
```

How the rule works. It opens with one reading that governs every line: the person's words as meant, in the frame they set, with every part of the answer sized by what it does for what they came for. Seven lines then say what the best answer does. It gives what the best person the message calls on would give, and leads with what the person needs first. It tests what they rely on as they will use it, and states each claim as exactly and surely as the evidence allows. It judges meaning by the frame and action by the world, so a correction reruns everything the error carried and goes no further. It writes each piece for its reader, and writes to the practice's standard. The floor, never worse than plain, keeps all a strong plain answer gives and removes only padding, unusable narration and claims of checks that never ran.

How the rule was built. I studied every clear loss of v4 in the benchmark. A clear loss is a comparison judged by two or more graders, where most of them preferred the other answer and at least half of all the graders said it was clearly better. Of the 118 clear losses, examined one by one, 9 were noise and 109 were real, in 66 cases. In 78 a v4 line pushed the model into the loss, most often a line with a fixed shape: one that set a position, fired a section on a topic or cut by the form of a sentence, whatever its effect on the person. In 28, v4 had no line that would have caught the failure, and 3 were faults in the test harness. The new rule went through four drafts, and each was attacked by an adversary with requests built to break it; the first three broke on 18, 20 and 19 requests, and each next draft removed those breaks. A second outside review of the design and a second proofread followed, and every claim was checked against the files before anything changed. Of the review's 132 design claims, 43 held up. They led to crisis replies sized to what the person said, politeness and forms of address that follow the reader, three rule lines made clearer, and fixes to the checkers. Of the proofread's 178 findings, 87 were fixed.

How a run goes. The rule is always loaded, and an ordinary request is answered under it in the conversation, without the skill. With the Second Opinion installed, the agent writes the whole draft, starts `gravitas-reviewer` with the request and the draft, sets a 180-second `schedule` timer with `TimerCondition: "any"`, ends its turn on one holding line, and fixes only what the reviewer names when its message arrives. Deep work opens the skill, which routes it to the orchestrator. The orchestrator writes a task record, picks a scale (quick, standard, full or exhaustive) with fixed numbers for fan-out, votes and stopping, and names the modules to load. Work lists are built with real tools, specialists fan out with absolute paths and a return schema, load-bearing claims go to independent checks, a completeness critic names what was never checked, and the report, with its tiers and gaps, goes to a file. The reply gives the verdict and the findings in plain words.

| Tier | What must have happened |
| :--- | :--- |
| `observed` | The artifact itself was inspected, and the label names it |
| `executed` | A tool ran and returned the value, and the label shows the command or query and what it returned |
| `read` | A source was retrieved, and the label gives the URL or path and quotes the line |
| `inferred` | Reasoning or recall; everything whose slot cannot be filled |

The tiers belong to deep-work reports. A reply in the conversation never carries them.

None of the agents has a file-editing tool. The checker and the reviewer can run commands and are told never to modify the work they check; the prose editor returns its edited text instead of writing it.

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
| `gravitas-reviewer` (with `--review`) | Return at most three defects in a draft reply, from wrong facts to wrong format | `view_file`, `read_url_content`, `search_web`, `run_command` |

Scripts, run from this folder. `--latest` checks against the most recent conversation, and a conversation's id is the folder name under `~/.gemini/antigravity-cli/brain/`, or `conversation_id` in `agy -p --output-format json` output.

```bash
python skills/gravitas/scripts/check_skills.py          # validate every skill, agent, rule and plugin under ~/.gemini/config
python skills/gravitas/scripts/provenance_check.py <answer> --latest   # check evidence labels against the transcript
python skills/gravitas/scripts/ledger.py --help         # bookkeeping for fan-outs: dedupe, votes, dry rounds
python skills/gravitas/scripts/slopcheck.py <files>     # structural markers of generated prose; --strict fails on any flag
```

The six checks in `skills/gravitas/scripts/checks/` count what a model miscounts while sounding sure: `pingze_check.py` for 绝句 and 律诗, `couplet_check.py` for 对联, `mora_count.py` for haiku, tanka and senryu, `sijo_check.py` for 평시조, `num_units.py` for amounts across 万, 亿, 億, 만, 억, lakh, crore and million, and `locale_dates.py` for dates written for Chinese, Japanese and Korean readers. Each prints `PASS`, `FAIL` or `ERROR` on its first line and exits 0, 1 or 2. `skills/gravitas/references/14-checks.md` says when to run each one. They run only through `run_command`, which a headless run at default settings refuses, and then the same rules are applied by hand.

What testing showed. Answers were graded blind in pairs against written answer keys, by Gemini 3.1 Pro and Gemini 3.8 Flash and, on some comparisons, Claude Opus 5.5 and GPT-6 Sol. The win share counts a win as one and a tie as half, so 0.50 means no difference, and a win is claimed only at 0.55 or more over at least 100 votes. On Gemini 3.8 Flash the v4 rule beat plain Antigravity at 0.57 and 0.61 on 60 everyday requests (120 votes each) and at 0.65 on 50 requests in ten languages (150 votes), and beat `/boost` at 0.84 (180 votes). On Gemini 3.1 Pro it scored 0.58 and 0.55 on the everyday requests (120 votes each, both intervals including 0.50), 0.71 on the ten-language requests (150 votes) and 0.77 against `/boost` (120 votes). On 50 edge requests the two Gemini graders preferred plain Antigravity, 0.45 over 100 votes on Flash and 0.42 over 100 on Pro, while GPT-6 Sol preferred Gravitas, 0.76 and 0.64 over 50 votes each. A portable core of the v4 rule, graded by GPT-6 Sol only over 60 votes each, scored 0.66 on Codex GPT-6 Sol, 0.57 on GPT-6.1 Sol, 0.57 on GPT-6 Luna and 0.47 on GPT-6 Astra, and 0.59 on Grok 4.6, 0.54 on Grok 4.7 build fast, 0.52 on Grok 4.7 and 0.42 on Grok 4.5. The Second Opinion lost to the rule alone as printed (0.23 and 0.28 over 180 votes each) and tied on the final message (0.50 over 168 votes and 0.47 over 120), which is why it is off by default. A hook-based version scored 0.57 against plain Antigravity over 180 votes, below the rule alone at 0.63 and 0.61 under the same graders, and it is not shipped.

Limits. Most of the method is instruction the model is asked to follow; the tool lists, the installers and the scripts are the mechanical parts, and the scripts run when the agent is told to run them. It was tested on agy 1.2.9 to 1.2.16 on Windows 11. Platform behaviour that affects how you use it is in `skills/gravitas/references/13-platform.md`. Two points matter most: headless `agy -p` runs need explicit permission grants or a `toolPermission` setting in `~/.gemini/antigravity-cli/settings.json`, and the CLI reads a repository's own `.agents/` folder only when the repository is passed with `--add-dir`, which is why this plugin installs globally. The native Chinese, Japanese and Korean rules have not been benchmarked. In Japanese and Korean, the reply to someone who may be in danger can answer a person who wrote casually in a polite register; plain Antigravity does the same.

Version 1.1.1 · MIT · by [Iamemily2050](https://github.com/Emily2040)
