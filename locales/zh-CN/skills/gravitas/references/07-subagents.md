# 模块 07 - 子代理

## 用途

本模块说明如何得到一个专职代理、截至 2026 年 9 月子代理工具接受哪些参数、本插件附带哪些代理，以及每个角色运行在哪个模型上。在第一次调用 `invoke_subagent` 或 `define_subagent` 之前，与 `08-delegation.md` 一起加载本模块。

## 得到专职代理的三种方式

| 途径 | 做法 | 写权限 | 用于 |
| :--- | :--- | :--- | :--- |
| 附带的代理 | `invoke_subagent`，把 `TypeName` 设为某个 `gravitas-*` 代理 | 由代理文件的 `tools` 列表固定 | 所有观察、评判和评审角色 |
| 临时定义 | 先 `define_subagent`，再用新名字调用 `invoke_subagent` | `enable_write_tools` 为 true 或 false | 本插件没有附带的专职代理 |
| 内置的 `self` | `invoke_subagent`，`TypeName: "self"` | 与父代理相同的工具 | 需要沿用用户所选模型和工具的实现工作。模型在 agy 1.2.9 上列出了它；尚未与本技能一起测试 |

凡是不能写入的角色，优先使用附带的代理。它们的只读属性来自文件中的工具列表，因此不依赖子代理是否遵守指令。

## 工具声明

以下内容读自 2026-09-24 agy 1.2.9 上模型自身收到的工具声明，并与桌面版 2.17.0 的 `language_server.exe` 中的字符串交叉核对。更新之后要重新核对，因为本技能的一个早期版本记载过声明中并不存在的字段。

| 工具 | 参数 |
| :--- | :--- |
| `invoke_subagent` | `Subagents`：一个数组。每个条目都接受必填的 `TypeName`、`Role`（2 到 5 个词的职位名）和 `Prompt`，以及 `Model`（`inherit`、`flash_lite`、`flash`、`pro`；默认 `inherit`）和 `Workspace`（`inherit`、`branch`、`share`；默认 `inherit`） |
| `define_subagent` | `name`、`description`、`system_prompt`、`enable_write_tools`（文件编辑与命令）、`enable_mcp_tools`、`enable_subagent_tools` |
| `manage_subagents` | `Action`：`list`、`kill` 或 `kill_all`，`kill` 需配合 `ConversationIds` |
| `send_message` | `Recipient`（子代理的会话 ID）和 `Message` |

并发来自在同一个 `Subagents` 数组中放入多个条目。每个启动的子代理都有自己的会话 ID 和一个指向其转录记录的 `logAbsoluteUri`，完成时都会回发一条消息。在交互式会话中无需轮询；在无头运行中，要一直进行工具调用，直到所有子代理都完成（见 `08-delegation.md`）。

`invoke_subagent` 的声明要求模型在用户没有指定其他模型时，把 `Model` 默认为 `inherit`。安装本插件，就是对下表路由中各角色提出的这种指定。

## 自定义代理文件

自定义代理是一个带 YAML frontmatter 的 Markdown 文件。frontmatter 配置代理，正文成为它的系统提示词。

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
| `name`、`description` | 身份，以及父代理选择子代理时读到的文字 |
| `tools` | 代理可以调用的工具，其余一律没有 |
| `model` | `inherit`、`flash` 或 `pro` |
| `mainAgent`、`subagent` | 能否被选为主代理，以及能否由 `invoke_subagent` 启动 |
| `commandExecutionPolicy` | shell 策略：`off`、`auto`、`eager` 或 `sandbox` |
| `skills`、`plugins`、`mcpServers`、`rules`、`hooks`、`agents` | 附加到这个代理上的自定义项 |
| `inheritCustomizations`、`inheritMcp` | 代理是否采用用户的技能、规则和插件，以及是否获得用户的 MCP 服务器 |
| `excludeDefaultComponents` | 文档说它会去掉默认的提示词片段和工具；在 agy 1.2.9 上它没有再去掉任何东西（open issue #1015） |

这些键名已在桌面版 2.17.0 的 `language_server.exe` 中作为 YAML 标签得到确认，含义来自自定义子代理文档。`inheritMcp` 不在文档中；它在这里经过了测试。二进制中还有 `enabledTools`、`disabledTools`、`hidden` 和 `background`，未经测试，也没有使用。

`tools` 列表并不是完整的工具集。在 agy 1.2.9 上，一个只列出 `view_file`、并设置了 `inheritCustomizations: false` 的代理，按它自己对声明的陈述，还拥有 `send_message`、`call_mcp_tool`、`list_resources`、`read_resource` 和 `manage_task`。`call_mcp_tool` 可以触及每一个已连接的 MCP 服务器，只有当它们全部只读时，评审者才是只读的。加上 `inheritMcp: false` 去掉了 `call_mcp_tool`；再加 `excludeDefaultComponents: true` 没有任何变化。每个附带的代理都把两个继承开关设为 false。

自定义代理从 `~/.gemini/config/agents/` 和插件内的 `agents/` 中被发现。2026-09-24 在 agy 1.2.9 上，`agy agents` 列出了全局代理，却没有列出插件内的代理，而模型能看到并说出两者的名字。工作区 `.agents/agents/` 中的代理完全没有被 CLI 发现。

两点提醒。文档警告，`tools` 中未映射或拼错的工具名可能导致子代理挂起，所以 `scripts/check_skills.py` 会用一份已知列表核对每个名字。另外，自 agy 1.2.7 起，`find_by_name`、`grep_search` 和 `list_dir` 不再属于默认工具集；自定义代理只有列出它们才能获得。

## 附带的代理名单

| 代理 | 职责 | 工具 | 模型 | 写入 |
| :--- | :--- | :--- | :--- | :--- |
| `gravitas-scout` | 定位文件、路由、符号和来源。只返回路径和行范围 | `list_dir`、`find_by_name`、`grep_search`、`view_file` | flash | 否 |
| `gravitas-reader` | 就一组限定的文件或 URL 回答具体问题，并引用所依据的行 | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content` | flash | 否 |
| `gravitas-finder` | 在给定工作清单上搜寻某一类缺陷，或从某一个角度搜索 | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content`、`search_web` | flash | 否 |
| `gravitas-checker` | 运行一次独立核查：数值求值、测试、重新计算、查询 | `view_file`、`run_command` | flash | 仅限临时文件，由职责规定 |
| `gravitas-refuter` | 尝试反驳一个结论，不确定时默认判为已反驳 | `view_file`、`grep_search`、`read_url_content`、`search_web` | pro | 否 |
| `gravitas-visual-critic` | 以没看过源代码的观看者身份评判截图 | `view_file` | pro | 否 |
| `gravitas-completeness-critic` | 阅读台账，指出从未搜索、打开、运行或核实过的东西 | `view_file`、`list_dir`、`grep_search`、`find_by_name` | pro | 否 |
| `gravitas-prose-editor` | 按文风标准修改草稿并返回修改后的文本 | `view_file` | pro | 否 |

`gravitas-checker` 是唯一带命令行的验证者，所以它的只读属性是职责规定，而不是工具限制。让它的范围保持狭窄，当它的结果承重时要读它的转录记录。

实现工作交给父代理，或交给 `Model: "inherit"` 的 `self`，这样修改文件的工作仍使用用户选定的模型。

## 模型路由

| 工作 | 模型 |
| :--- | :--- |
| 机械抽取、文件分拣、列清单 | `flash_lite` |
| 侦察、阅读、搜寻、核查 | `flash` |
| 反驳、评审、裁判、最终综合 | `pro` |
| 任何会写文件的工作 | `inherit` |

为文件分拣付 `pro` 的价钱是浪费。用 `flash_lite` 跑视觉评审，丢掉的正是这个角色存在的意义：判断力。写入类工作默认 `inherit`，因为悄悄降低用户所选的模型，是用户并没有做出的决定。
