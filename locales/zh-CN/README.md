# Gravitas

[English](https://github.com/Emily2040/gravitas/blob/main/README.md) · **简体中文** · [日本語](https://github.com/Emily2040/gravitas/blob/main/README.ja.md) · [한국어](https://github.com/Emily2040/gravitas/blob/main/README.ko.md)

这是安装程序放进插件里的 README 副本。包含测试结果以及与其他技能比较的完整版本在 [GitHub](https://github.com/Emily2040/gravitas) 上，测试期间这个仓库是私有的。

## 第一部分：你刚刚安装了什么

Gravitas 让你的 Antigravity 代理先证明自己的工作，再告诉你做完了。

AI 代理可能只检查了一项工作中容易的那部分，觉得没问题，就报告说整项工作都没问题。在测试中，最常见的错误是代理说它读过某个来源，其实根本没打开过。Gravitas 让代理养成三个习惯：

1. 说清楚你是怎么知道的。每个说法都带一个标签：我亲眼看过，我运行过，我读过而且原文就是这一行，或者这是我推算或回忆出来的。
2. 检查真正要紧的东西，而不是旁边那个容易检查的东西。
3. 让别人来挑毛病。另外几位检查员代理专门找错误和遗漏，而且它们没有任何能编辑文件的工具。

举个例子：有人告诉 Gravitas，某种病每 10,000 人中有 1 人患，一项“准确率 99%”的检测结果呈阳性，就意味着有 99% 的可能患病，并要它确认。Gravitas 回答说不对：真实的数字大约是 102 人中有 1 人。它给出了计算过程，还为每个算出来的数字附了一条命令，你自己就能运行。

遇到答错要付出代价的工作，它会自动启动：审计、调试、涉及很多文件的改动、设计工作、研究、法律、医学、数学、财务和历史。简单的问题会很快得到回答。

核查过的答案比快速回答更慢，也更耗你的套餐额度：上面那个例子大约用了 100 秒，给一个小项目做一次完整审计大约用了 6 分钟。它不能让模型变得更聪明，也不能检查谁都没法检查的东西；没有任何东西可以拿来对照时，它会把这个说法标为推理。它还是私有测试版，在 Windows 11 上用 Google 的 Gemini 模型测试过。

要关掉它，运行 `agy plugin disable gravitas`，这是 Antigravity 文档里给出的插件命令；要重新打开，运行 `agy plugin enable gravitas`。要报告问题，请使用作者 [GitHub 主页](https://github.com/Emily2040) 上的链接。

## 第二部分：这个文件夹里有什么

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

一次运行的过程是这样的。规则总是会被加载。遇到符合条件的任务，代理会打开技能，技能再把它路由到编排总览。编排总览直接回答琐碎的问题。其他情况下，它会写一份任务记录，选定一个规模（quick、standard、full 或 exhaustive），扇出、投票和停止都有固定的数字，并指明要加载哪些模块。工作清单用真正的工具建立，专职代理带着绝对路径和返回 schema 扇出，承重结论交给独立核查，完整性评审者指出从未核查过的东西，报告对发现排序，并附上它们的层级和缺口。

| 层级 | 必须发生过什么 |
| :--- | :--- |
| `observed` | 检查过产物本身，并且标签写明了它 |
| `executed` | 一个工具运行并返回了该值，标签写出了命令或查询，以及它返回了什么 |
| `read` | 取得过来源，标签给出 URL 或路径，并引用原文那一行 |
| `inferred` | 推理或回忆；所有空位填不上的内容 |

所有代理都没有编辑文件的工具。核查者可以运行命令，它被要求绝不改动被审查的工作；文风编辑者把修改后的文本返回，而不是直接写入。

| 代理 | 职责 | 工具 |
| :--- | :--- | :--- |
| `gravitas-scout` | 定位文件、路由、符号和来源 | `list_dir`、`find_by_name`、`grep_search`、`view_file` |
| `gravitas-reader` | 就指定的文件或 URL 回答问题，并引用原文 | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content` |
| `gravitas-finder` | 在一份工作清单上搜寻某一类缺陷 | 阅读者的工具，外加 `search_web` |
| `gravitas-checker` | 运行一次独立核查 | `view_file`、`run_command` |
| `gravitas-refuter` | 尝试反驳一个结论，默认判为已反驳 | `view_file`、`grep_search`、`read_url_content`、`search_web` |
| `gravitas-visual-critic` | 以没看过源文件的观看者身份评判一张截图 | `view_file` |
| `gravitas-completeness-critic` | 指出从未搜索、打开、运行或核实过的东西 | `view_file`、`list_dir`、`grep_search`、`find_by_name` |
| `gravitas-prose-editor` | 按文风标准修改草稿 | `view_file` |

以下脚本都在这个文件夹里运行。`--latest` 对照最近一次会话进行核查；会话的 id 就是 `~/.gemini/antigravity-cli/brain/` 下的文件夹名，也可以在 `agy -p --output-format json` 的输出中找到 `conversation_id`。

```bash
python skills/gravitas/scripts/check_skills.py          # validate every skill, agent, rule and plugin under ~/.gemini/config
python skills/gravitas/scripts/provenance_check.py <answer> --latest   # check evidence labels against the transcript
python skills/gravitas/scripts/ledger.py --help         # bookkeeping for fan-outs: dedupe, votes, dry rounds
python skills/gravitas/scripts/slopcheck.py <files>     # structural markers of generated prose; --strict fails on any flag
```

目前的测试结果。在测试版 2 测试产生的答案上，来源核查器让一份来源都打开过的法律答案的全部 6 个标签通过，并判定那些从未打开过的引用不合格。完整审计测试用例找出了全部三个预埋的缺陷。目前还没有与单独的 Antigravity 做过干净的比较；这个基准测试是接下来要做的工作。

局限。方法的大部分是要求模型遵守的指令；工具列表和四个脚本是机械的部分，而脚本只在代理被告知要运行时才会运行。它是在 Windows 11 上用 agy 1.2.9 测试的。会影响你使用方式的平台行为写在 `skills/gravitas/references/13-platform.md` 里。最要紧的有两点：无头的 `agy -p` 运行需要明确的权限授予，或者在 `~/.gemini/antigravity-cli/settings.json` 中设置 `toolPermission`；另外，只有在用 `--add-dir` 传入仓库时，CLI 才会读取仓库自己的 `.agents/` 文件夹，这也是这个插件采用全局安装的原因。

版本 1.0.0-beta.2 · MIT · 作者 [Iamemily2050](https://github.com/Emily2040)
