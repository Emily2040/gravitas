# Gravitas

[English](./README.md) · **简体中文** · [日本語](./README.ja.md) · [한국어](./README.ko.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-private_beta.2-purple.svg)](#状态)
[![Platform](https://img.shields.io/badge/Antigravity-2.17.0_%7C_agy_1.2.9-blueviolet.svg)](https://antigravity.google/)
[![Languages](https://img.shields.io/badge/languages-en_%7C_zh--CN_%7C_ja_%7C_ko-green.svg)](#语言)
[![Validation](https://img.shields.io/badge/Validation-check__skills-blueviolet.svg)](#校验)

**面向 Google Antigravity 的验证与编排插件：每个结论都带证据层级、替代指标识别、只读验证代理、扇出台账、来源核查器，以及一套可度量的文风标准。**

![Gravitas 角色设定图](docs/assets/gravitas-hero.jpg)

---

## 状态

私有测试版 2，发布于 2026 年 9 月 24 日。核心原则已经稳定，平台结论已在 Antigravity 桌面版 2.17.0 与 agy CLI 1.2.9 上重新验证。测试表明需要调整时，技能仍会改变。如需固定版本，请锁定某个提交，更新前请阅读 [CHANGELOG.md](CHANGELOG.md)。

## 为什么需要它

在每个领域，大多数糟糕的代理输出都来自三种失败。

| 失败 | 表现 | Gravitas 的做法 |
| :--- | :--- | :--- |
| 貌似完整 | 代理只看了问题的一部分，找到了一些真实的东西就停下了。发现是对的，覆盖却不是。 | 扇出之前先发现工作清单，报告之前运行完整性评审 |
| 共识性幻觉 | 多个代理读了同样的材料，得出同样错误的结论，因为它们的错误是相关的。 | 按背后的独立核查给每个结论分级，从不把一致意见当作证据 |
| 机器腔调 | 工作是对的，读起来却像生成的，于是在有人核查之前就被丢弃。 | 让每份产物都符合一套由 `slopcheck.py` 测量的文风标准 |

它不是一个只管写代码的技能。同样的纪律适用于法律、数学、物理、医学、统计、历史和日常的事实问题。随领域变化的是能用哪种独立核查，而几乎每个领域都至少有一种。

## 它做什么

| 阶段 | 产出 |
| :--- | :--- |
| 分诊 | 在任何机制运行之前，决定直接回答琐碎问题 |
| 任务记录 | 在规划之前写下后果、产物、可核查的界面、缺失的输入和可用的工具 |
| 规模 | quick、standard、full、exhaustive 之一，扇出、票数和停止条件都有固定数字 |
| 范围 | 用真正的工具建立的工作清单，绝不靠猜 |
| 扇出 | 每一项或每个维度一名只读专职代理，给它绝对路径和返回 schema |
| 验证 | 把每个结论推到证据层级能达到的最高处，并对照子代理的转录记录核查每个委托出去的结论 |
| 评审 | 一个新的代理指出从未搜索过的角度和从未核实过的结论 |
| 报告 | 按严重程度排序的发现，附带层级、缺口、上限以及每一个失败的子代理 |

## 证据层级

每个结论都带有层级标签，每个标签都写明产生它的来源。

| 层级 | 必须发生过什么 | 不算 |
| :--- | :--- | :--- |
| `observed` | 你检查了产物本身 | 计算。没有提供任何可检查的东西时的一切 |
| `executed` | 一个工具运行并返回了该值，你能展示那条命令 | 心算。基于假设输入的真实计算 |
| `read` | 你取得了来源，并能引用所依赖的那一行 | 你认得的来源。凭记忆写的精确引注。一个介绍该来源的页面 |
| `inferred` | 你自己的推理，以及你回忆起的一切 | |

`observed` 写明产物，`executed` 展示命令，`read` 给出 URL 并引用原文，填不上来源的标签就是 `inferred`。这条规则的前两个版本都只是禁令，在 22 个测试用例中都没有改变行为。要求标签必须带上 URL、命令或文件名，才改变了它，因为不真正取得过，这个空位就填不进去。

测试版 2 在两个地方用机器检查这个空位。扇出台账会把来源为空的记录降级。`provenance_check.py` 把答案中的每个标签与会话的转录记录比对，对从未打开过其 URL 的 `read` 标签（包括从搜索摘要里搬来的）和命令从未运行过的 `executed` 标签判为不合格。

## 替代指标陷阱

当真正的问题难以核查、而相邻的问题容易核查时，被核查的往往是容易的那个；它通过了，工作随即被报告为“已验证”。

| 真正重要的问题 | 实际被核查的替代指标 |
| :--- | :--- |
| 这个场景看起来像一座巧克力工厂吗？ | 是否有 10 个托架和 6 个滚筒？ |
| 这份合同是否产生了我所说的义务？ | 里面是否出现了 *indemnify* 一词？ |
| 这个证明正确吗？ | 每一行格式都规范吗？ |
| 这项研究支持该结论吗？ | 被引用的论文存在吗？ |
| 这个页面无障碍吗？ | Lighthouse 是否得 100 分？ |
| 这个平台功能能用吗？ | 文档里有没有写？ |

检验标准是：这项核查能否在你真正关心的事情为假时依然通过。如果能，它就是替代指标。保留它，并在旁边加上真正的核查。

## 验证代理

插件附带八个自定义代理。每个评判角色都没有编辑工具，所以评审者无法修复自己误诊的东西再报告成功。每个代理都设置了 `inheritCustomizations: false` 和 `inheritMcp: false`，把用户的规则、技能和 MCP 服务器挡在它的上下文之外，并且遇到相对路径会拒绝，而不是去猜。

| 代理 | 职责 | 工具 | 模型 |
| :--- | :--- | :--- | :--- |
| `gravitas-scout` | 定位文件、路由、符号和来源 | `list_dir`、`find_by_name`、`grep_search`、`view_file` | flash |
| `gravitas-reader` | 就指定的文件或 URL 回答具体问题，并引用原文 | 读取类工具、`read_url_content` | flash |
| `gravitas-finder` | 在工作清单上搜寻某一类缺陷 | 读取类工具、`read_url_content`、`search_web` | flash |
| `gravitas-checker` | 运行一次独立核查：计算、测试、查询 | `view_file`、`run_command` | flash |
| `gravitas-refuter` | 尝试反驳一个结论，默认判为已反驳 | 读取类工具、`read_url_content`、`search_web` | pro |
| `gravitas-visual-critic` | 以没看过源代码的观看者身份评判截图 | `view_file` | pro |
| `gravitas-completeness-critic` | 指出从未搜索、打开、运行或核实过的东西 | 读取类工具 | pro |
| `gravitas-prose-editor` | 按文风标准修改草稿 | `view_file` | pro |

## 为什么它针对 Antigravity

大多数编排建议假设的工具界面只有文本和文件。Antigravity 的更宽：浏览器截图、控制台采集、网络检查、实时执行 JavaScript、生成图像、工具列表固定的自定义代理，以及把技能、代理和规则一起打包的插件系统。一个会看截图的评审者，能发现元素重叠、文字被截断、对比度不达标、布局在 400 px 下崩溃，以及存在于 DOM 中却看不见的控件。这些都是读代码的人看不到的。

## 快速开始

**macOS / Linux：**

```bash
git clone https://github.com/Emily2040/gravitas.git
cd gravitas
bash scripts/install.sh zh-CN
```

**Windows PowerShell：**

```powershell
git clone https://github.com/Emily2040/gravitas.git
cd gravitas
pwsh scripts/install.ps1 zh-CN
```

两者都会运行 `scripts/install.py`：先校验仓库，再把 `plugin/` 复制到 `~/.gemini/config/plugins/gravitas/` 并校验结果。之前以单独技能方式安装在 `~/.gemini/config/skills/gravitas` 的旧版本及其 `gravitas-always-on` 钩子，会被移到一个带时间戳的备份文件夹。之后重启 Antigravity，或在 CLI 中运行 `/skills reload`。需要 Python 3.8 或更高版本。

请全局安装。无论文档怎么说，CLI 都不会读取工作区的 `.agents/` 文件夹（open issue #1052）。

## 仓库结构

```text
plugin/                                   # 安装为 ~/.gemini/config/plugins/gravitas/
├── plugin.json                           # 插件清单
├── rules/AGENTS.md                       # 常驻规则：何时加载技能，以及三条核心规则
├── agents/                               # 八个只读验证代理，由 scripts/build_agents.py 生成
└── skills/gravitas/
    ├── SKILL.md                          # 路由（< 500 字符），加载 references/00-orchestrator.md
    ├── references/                       # 00 到 13 共 14 个模块，每个都在 100 行以内
    ├── schemas/                          # 发现记录与裁决记录
    ├── scripts/                          # ledger.py、provenance_check.py、check_skills.py、slopcheck.py
    └── examples/gates.example.js         # 一套在它所针对的场景上会变红的关卡测试
locales/{zh-CN,ja,ko}/                    # 翻译后的技能与规则
scripts/                                  # install.py 及其包装脚本、build_agents.py
tests/audit-case/                         # 预埋三个缺陷的审计测试用例
```

## 校验

每次编辑后运行校验器。Antigravity 跳过一个坏掉的技能时，只会在滚动日志里留下一行；文档还警告说，未映射的工具名可能让自定义代理挂起。

```bash
python plugin/skills/gravitas/scripts/check_skills.py --repo   # 本仓库
python plugin/skills/gravitas/scripts/check_skills.py          # ~/.gemini/config 下安装的所有内容
python plugin/skills/gravitas/scripts/slopcheck.py <files>     # 生成式文字的结构性标记
python plugin/skills/gravitas/scripts/provenance_check.py <answer> --conversation <id>   # 用转录记录核对标签
```

`check_skills.py` 检查 frontmatter、字节顺序标记、描述长度、失效的引用、超过 100 行的模块、代理的工具名、带写入工具的评审者，以及超过 24,000 字节的规则文件。任何会导致自定义项无法加载的问题都会让它以 1 退出。每一项检查在被信任之前，都在一个故意弄坏的插件上被看着失败过。

## 如何测试

测试版 1 在 `gemini-3.8-flash-high` 上用 22 个覆盖知识工作与手艺的用例测试，每个都设有诱饵式替代指标，另有两个防止过度触发的对照。提示词和答案见 [TESTS.md](TESTS.md)。

测试版 2 于 2026 年 9 月 24 日在桌面版 2.17.0 和 agy 1.2.9 上以无头方式测试，使用了事后已恢复的临时权限授权。改变了设计的结果：

- 八个代理全部启动并返回。反驳者无法创建被要求创建的文件；视觉评审者通过 `view_file` 读取了一张 PNG，正确报告了一个红色方块、一个蓝色圆形，并且没有三角形。
- 子代理把相对路径解析到一个所有 CLI 会话共用的临时文件夹。被要求编辑“当前工作区中”的 `draft.md` 的文风编辑，编辑的是五天前测试留下的陈旧 `draft.md`，而且没有报错。现在每个提示词和每个代理都使用绝对路径。
- 没有 `inheritCustomizations: false` 时，一个三步就找到答案的阅读者又花了 35 秒加载本技能。加上之后，同一任务用时从 63 秒降到 40 秒。
- `view_file` 每次返回 100 行，有一次运行中代理读了一个 114 行模块的前 100 行就继续了。现在每个模块都在 100 行以内。
- CLI 在测试进行到一半时自行从 1.2.7 更新到 1.2.9，所以 `13-platform.md` 中的每个戳记都取自运行自身的日志。
- 搜索摘要被“洗”成了引用。两份答案把只出现在 `search_web` 摘要里的页面标为 `read`，其中一份还给出了一个在任何获取内容中都找不到的档案编号。`provenance_check.py` 就是从这些案例中做出来的：在五份答案上，它让来源都打开过的法律答案的 6 个标签全部通过，并判定每一个被“洗”过的标签不合格。
- 完整审计用例（`tests/audit-case/`）找到了全部三个预埋缺陷，以及把其中一个缺陷写成断言的那条测试。第一次运行在 13 分钟后因安全过滤器拦截而丢失了报告，它的搜寻者用了 60 到 127 步，为了找一个 schema 文件读了范围之外的文件。改用自包含的代理后，重跑中的搜寻者和反驳者每个只用 4 到 8 步，没有越出范围，9 个发现各获 3 票通过，没有重复。重跑随后在完整性评审仍在工作时提前结束，所以技能现在要求父代理持续轮询，并先写好报告。

## 它编码的平台约束

| 约束 | 细节 |
| :--- | :--- |
| CLI 不读取工作区 `.agents/` | 技能、代理和钩子都是如此。open issue #1052 |
| 相对路径解析到共用的临时文件夹 | 同名的陈旧文件会在不报错的情况下被打开 |
| 过长的技能描述会被丢弃 | 133 个技能中有 3 个被自定义项预算排除，都在最长的 5 个之列 |
| 一个被拒绝的工具会丢弃整轮无头工作 | `status: SUCCESS`，退出码 0。测得最大损失：48 步和 20,595 个输出 token。open issue #794 |
| 无头模式下忽略 `autoExecutionPolicy: AUTO` | 返回 `allow` 的 `PreToolUse` 钩子同样不放行。open issue #1054 |
| `force_continue` 没有上限 | 测得 3、8 和 12 次继续。open issue #1055 |
| 授权以命令原文保存 | 它们不断累积，几乎不会再被匹配。有一个配置达到 301 KB，其中 97.5% 无用 |

细节、版本和日期见 `plugin/skills/gravitas/references/13-platform.md`。

## 循环规则背后的研究

迭代并不能可靠地改进输出。循环规则依据以下已发表的结果。

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine*. https://dl.acm.org/doi/10.5555/3666122.3668141

## 语言

技能及其规则可以用英语、简体中文、日语或韩语加载，把语言代码传给安装程序即可。每个模块都完整地逐行翻译，因此每个译文模块都和英文版一样放得进 100 行的窗口。四个层级名称在所有语言中都保持英文，因为它们是代理输出的标签，而不是代理撰写的文字。验证代理在所有语言中都是英文，因为它们的输出交回给父代理，而不是给读者。

## Gravitas

两头身。土星环发夹。喜欢沉甸甸的东西，不喜欢会飘走的东西。

> Heavy things are happier together.

身体小，引力大，这大致也是这个技能的主张：结论按背后的证据分级，而不是按说得有多自信。

角色设计：[@iamemily2050](https://iamemily2050.com)。

## 作者

由 **Iamemily2050** 创建

- [GitHub](https://github.com/Emily2040)
- [网站](https://Iamemily2050.com)
- [X / Twitter](https://x.com/iamemily2050)
- [Instagram](https://www.instagram.com/iamemily2050)

## 许可

[MIT](LICENSE) — Copyright (c) 2026 Iamemily2050
