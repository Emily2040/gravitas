# 模块 07：Subagent

## 用途

本模块讲四件事：怎样拿到一个专职 agent；截至 2026 年 10 月，subagent 相关工具接受哪些参数；本插件自带哪些 agent；每个角色跑在哪个模型上。第一次调用 `invoke_subagent` 或 `define_subagent` 之前，先加载本模块，同时加载 `08-delegation.md`。

## 拿到专职 agent 的三种途径

| 途径 | 用法 | 写权限 | 适用场景 |
| :--- | :--- | :--- | :--- |
| 自带 agent | 调用 `invoke_subagent`，把 `TypeName` 设成某个 `gravitas-*` agent | 由 agent 文件里的 `tools` 列表定死 | 所有观察、判断和评审类角色 |
| 临时定义 | 先调 `define_subagent`，再用新名字调 `invoke_subagent` | `enable_write_tools` 设为 true 或 false | 本插件没有自带的专职 agent |
| 内置的 `self` | 调用 `invoke_subagent`，`TypeName: "self"` | 和父 agent 的工具相同 | 需要沿用用户所选模型和工具的实现工作。在 agy 1.2.9 上，模型列出了这个类型；尚未在本技能中测试过 |

凡是不允许写入的角色，优先用自带 agent。它们之所以只读，靠的是文件里的工具列表，而不是 subagent 自觉遵守指令。

## 工具声明

下面的参数是 2026-09-24 在 agy 1.2.9 上从模型自己的工具声明里读出来的，并和桌面版 2.17.0 中 `language_server.exe` 的字符串做过交叉核对。2026-10-03 这天 CLI 从 1.2.15 升到 1.2.16，当天又把除 `define_subagent` 以外的声明重读了一遍，结果一致。每次更新后都要重新核对：本技能早先的一个版本就写进过声明里根本没有的字段。

| 工具 | 参数 |
| :--- | :--- |
| `invoke_subagent` | `Subagents`：一个数组。每个元素都必须带 `TypeName`、`Role`（2 到 5 个词的岗位名称）和 `Prompt`，另有 `Model`（`inherit`、`flash_lite`、`flash`、`pro`，默认 `inherit`）和 `Workspace`（`inherit`、`branch`、`share`，默认 `inherit`） |
| `define_subagent` | `name`、`description`、`system_prompt`、`enable_write_tools`（文件编辑和命令执行）、`enable_mcp_tools`、`enable_subagent_tools` |
| `manage_subagents` | `Action`：`list`、`kill` 或 `kill_all`；用 `kill` 时要带上 `ConversationIds` |
| `send_message` | `Recipient`（subagent 的会话 ID）和 `Message` |
| `schedule` | `DurationSeconds`（一次性计时器）或 `CronExpression`（cron 定时任务），外加 `Prompt`。`TimerCondition` 可取 `never`（默认）、`any`，或某个发送者 ID，收到该发送者的消息就取消计时器。`IsDaemon` 和 `MaxIterations` 用于 cron 任务。调用后立即返回；要取消，用 `manage_task` 带上 `kill` 和任务 ID |

要并发，就在同一个 `Subagents` 数组里放多个元素。每个启动起来的 subagent 都有自己的会话 ID，以及一个指向其对话记录的 `logAbsoluteUri`。subagent 结束时如果没有调用 `send_message`，父 agent 会收到一条发送者为 `system` 的消息，里面带着它的最后一条回复。要等它的结果，就设一个 `TimerCondition: "any"` 的 `schedule` 计时器，然后结束本轮。这么设的原因是：按该 subagent 的 ID 设条件的计时器，不会被这条 `system` 消息取消；不设计时器的话，headless 运行会随本轮一起结束，结果就丢了。验证过的写法见 `08-delegation.md`。

`invoke_subagent` 的声明要求模型：除非用户要求换别的模型，否则 `Model` 默认填 `inherit`。安装本插件，就相当于用户对下面路由表里的这些角色提出了这个要求。

## 自定义 agent 文件

自定义 agent 就是一个带 YAML frontmatter 的 Markdown 文件：frontmatter 负责配置，正文就是它的 system prompt。

```markdown
---
name: "gravitas-refuter"
description: "Attempts to refute one specific claim. Defaults to refuted when uncertain."
tools:
  - view_file
  - grep_search
  - read_url_content
  - search_web
model: "pro"
mainAgent: false
subagent: true
inheritCustomizations: false
inheritMcp: false
---

You are a refuter. ...
```

| 键 | 含义 |
| :--- | :--- |
| `name`、`description` | 身份标识，以及父 agent 挑选 subagent 时读到的说明文字 |
| `tools` | agent 能调用的工具，没列出的一概没有 |
| `model` | `inherit`、`flash` 或 `pro` |
| `mainAgent`、`subagent` | 前者决定它能否被选为主 agent，后者决定 `invoke_subagent` 能否启动它 |
| `commandExecutionPolicy` | shell 执行策略：`off`、`auto`、`eager` 或 `sandbox` |
| `skills`、`plugins`、`mcpServers`、`rules`、`hooks`、`agents` | 挂在这个 agent 上的自定义配置 |
| `inheritCustomizations`、`inheritMcp` | 前者决定 agent 是否沿用用户的技能、规则和插件，后者决定它是否拿到用户的 MCP 服务器 |
| `excludeDefaultComponents` | 文档说它会去掉默认的 prompt 片段和工具；但在 agy 1.2.9 上，它并没有额外去掉任何东西（issue #1015，尚未关闭） |

这些键名已经在桌面版 2.17.0 的 `language_server.exe` 里以 YAML 标签的形式确认过，含义取自自定义 subagent 的文档。`inheritMcp` 不在文档里，是在这里实测过的。二进制里还有 `enabledTools`、`disabledTools`、`hidden` 和 `background`，都没测过，也没用上。

`tools` 列表并不等于全部工具。在 agy 1.2.9 上，一个只列了 `view_file`、并设了 `inheritCustomizations: false` 的 agent，据它自己报告的工具声明，还拥有 `send_message`、`call_mcp_tool`、`list_resources`、`read_resource` 和 `manage_task`。`call_mcp_tool` 能调到每一个已连接的 MCP 服务器，因此只有这些服务器全都是只读的，评审者才算真正只读。加上 `inheritMcp: false` 之后，`call_mcp_tool` 就没了；再叠加 `excludeDefaultComponents: true`，没有任何变化。所有自带 agent 都把这两个继承开关设成了 false。

自定义 agent 的发现位置包括 `~/.gemini/config/agents/` 和插件内的 `agents/`。2026-09-24 在 agy 1.2.9 上，`agy agents` 列出了全局 agent，却没列出插件里的 agent，而模型两个都能看到，也都能叫出名字。放在工作区 `.agents/agents/` 下的 agent，只有用 `--add-dir` 传入该仓库时才会被发现。

有两点要注意。第一，文档警告，`tools` 里如果有未映射或拼错的工具名，subagent 可能会挂起，所以 `scripts/check_skills.py` 会拿一份已知列表逐个核对工具名。第二，从 agy 1.2.7 起，`find_by_name`、`grep_search` 和 `list_dir` 不再属于默认工具集，自定义 agent 必须显式列出才能用。

## 自带 agent 一览

| Agent | 职责 | 工具 | 模型 | 是否写入 |
| :--- | :--- | :--- | :--- | :--- |
| `gravitas-scout` | 定位文件、路由、符号和来源，只返回路径和行号范围 | `list_dir`、`find_by_name`、`grep_search`、`view_file` | flash | 否 |
| `gravitas-reader` | 针对一组限定的文件或 URL 回答具体问题，并引用作为依据的那几行 | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content` | flash | 否 |
| `gravitas-finder` | 在给定的工作清单上，专查一类缺陷，或只从一个角度搜索 | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content`、`search_web` | flash | 否 |
| `gravitas-checker` | 做一项独立核查：数值求值、测试、复算或查询 | `view_file`、`run_command` | flash | 只写临时文件，靠职责约定 |
| `gravitas-refuter` | 尝试推翻一个结论，拿不准时默认判为已推翻 | `view_file`、`grep_search`、`read_url_content`、`search_web` | pro | 否 |
| `gravitas-visual-critic` | 以没看过源码的观看者身份评判截图 | `view_file` | pro | 否 |
| `gravitas-completeness-critic` | 读台账，指出哪些东西从没被搜索、打开、运行或核实过 | `view_file`、`list_dir`、`grep_search`、`find_by_name` | pro | 否 |
| `gravitas-prose-editor` | 按文风标准修改草稿，返回改好的文本 | `view_file` | pro | 否 |
| `gravitas-reviewer` | 为常驻规则的“第二意见”审查回复草稿，最多返回三处缺陷 | `view_file`、`read_url_content`、`search_web`、`run_command` | pro | 否，靠职责约定 |

`gravitas-checker` 和 `gravitas-reviewer` 手里有命令行，所以它们只读是靠职责约定，不是靠工具限制。给核查者划的范围要窄；如果它的结果是关键依据，就去读它的对话记录。审查者服务的是规则里的“第二意见”，不是本技能的扇出；只有规则里带这一节时它才会随之安装，而要装上带这一节的规则，安装时得加 `--review`。实现工作交给父 agent，或者交给 `Model: "inherit"` 的 `self`，这样改文件的工作仍然跑在用户自己选的模型上。

## 模型路由

| 工作 | 模型 |
| :--- | :--- |
| 机械性抽取、文件初筛、列清单 | `flash_lite` |
| 侦察者、阅读者、搜寻者、核查者（scout、reader、finder、checker） | `flash` |
| 反驳者、评审者、裁判，以及最终综合 | `pro` |
| 任何要写文件的工作 | `inherit` |

文件初筛用 `pro`，纯属浪费。让视觉评审跑在 `flash_lite` 上，就把这个角色赖以存在的判断力丢掉了。写文件的工作默认 `inherit`，因为悄悄把用户选的模型降级，等于替用户做了一个他自己没做的决定。
