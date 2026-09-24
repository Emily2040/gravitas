# 模块 13 - 平台

## 用途

本模块记录经过验证的 Antigravity 行为，如果想当然地假设别的情况，就会白费工夫。当任务依赖 Antigravity 如何加载自定义项、运行子代理、应用权限或进行无头运行时，以及每当某个工具、钩子、技能或权限的表现出乎意料时，加载本模块。

每一条都带有核查时所针对的版本和日期，因为这个平台变化很快。2026 年 9 月 18 日到 23 日之间，它发布了桌面版 2.15.0、2.15.1、2.16.0 和 2.17.0，以及 CLI 1.2.7、1.2.8 和 1.2.9。除非另有说明，每条都是在 2026 年 9 月 24 日于 Windows 11、桌面版 2.17.0 和 agy CLI 1.2.9 上核查的。通过 WinGet 安装的 CLI 在相隔 21 秒的两次测试运行之间，悄无声息地从 1.2.7 更新到了 1.2.9，所以这里的每个戳记都取自那次运行自身日志中的 `version:` 行。在依赖某一条之前，把它的戳记与 `https://antigravity.google/changelog` 上的更新日志比较，如果相关部分已经变化，就重新核查。

## 自定义项从哪里加载

| 位置 | 技能 | 代理 | 规则 | 证据 |
| :--- | :--- | :--- | :--- | :--- |
| `~/.gemini/config/skills/`、`agents/`、`AGENTS.md` | 加载 | 加载，`agy agents` 会列出 | 加载 | 已观察 |
| `~/.gemini/config/plugins/<name>/` | 加载 | 加载，`agy agents` 不列出 | 从 `rules/AGENTS.md` 加载 | 用测试插件观察：模型说出了它的技能和代理的名字，并遵守了它的规则 |
| `<repo>/.agents/` | 仅通过 `--add-dir` 加载 | 仅通过 `--add-dir` 加载 | `rules/` 两种情况下都不加载 | 已观察；open issue #1036、#1052 |

Gravitas 以插件形式安装正是这个原因：一个文件夹承载技能、验证代理和常驻规则，`agy plugin disable gravitas` 能把它们一起关掉。`agy plugin list` 只显示从市场导入的插件，所以复制进去的插件即使已被加载，也不会出现在那里。

工作区这一行与文档相矛盾。内置的自定义指南和技能页面都描述了从 `<repo>/.agents/` 发现，IDE 指南也说 IDE 会“automatically discovers and respects”那个文件夹。在 CLI 上，只要用 `--add-dir` 传入该仓库，`.agents/` 中的技能、代理和钩子都会加载，即使它同时也是工作目录。不加这个参数、直接在仓库里启动时，它们都不加载，尽管日志中的 `workspaceDirs` 写出了该文件夹，日志也报告 `loaded 0 named hooks`。`.agents/rules/` 中的规则在两种情况下都没有加载。当仓库自带的自定义内容很重要时，运行 `agy -p "..." --add-dir <repo>`。桌面应用和 IDE 未经测试。

## 会丢弃自定义项的预算

技能的名称和描述共用一个自定义项预算，放不下的技能会被丢弃。安装了 133 个技能时，模型把其中 3 个列在了 “Excluded Skills (due to context budget limits)” 之下。这 3 个都属于已安装技能中描述最长的 5 个之列，长度为 1,001 到 1,028 个字符。长度与被排除之间的关联，只是从一次观察中推断出来的。描述要写短；本技能的描述不到 500 个字符。

规则有自己的 20,000 token 预算，每个规则文件在 24,000 字节处按行边界截断；超出预算的规则会被降级为文件指针（read：内置 `agy-customizations` 指南中的 `docs/rules.md`，以及 CLI 1.2.7 更新日志）。

## 格式错误的技能会无声失败

无法解析的 `SKILL.md` 会被跳过。错误只写进 `~/.gemini/antigravity-cli/log/cli-*.log`，形如 `skills.go:201] Failed to parse skill file ...`，用户在任何地方都看不到。一个 UTF-8 字节顺序标记就足以触发这种情况，而 Windows PowerShell 5.1 的 `Set-Content` 和 `Out-File` 默认会加上它。一个坏掉的技能不会阻止其他技能加载。

每次编辑后运行 `scripts/check_skills.py`。它检查 frontmatter 解析、描述是否存在及其长度、字节顺序标记、失效的引用、超过 100 行的模块、代理的工具名、带写入工具的评审者，以及规则文件的大小。

## 文件与路径

| 行为 | 证据 |
| :--- | :--- |
| `view_file` 会拒绝相对路径，但在无头运行中，代理把 `~/.gemini/antigravity-cli/scratch/` 当作自己的工作目录。主代理在被拒绝后去那里搜索，而被要求使用“当前工作区中”的 `draft.md` 的子代理直接拼出了指向那里的路径。这个文件夹由所有 CLI 会话共用，里面还留着五天前测试的 33 个文件，两者都在毫无提示的情况下打开了一个同名的陈旧文件 | 在 1.2.9 上观察到 |
| `view_file` 每次调用返回 100 行。在一次运行中，代理读了一个 114 行文件的前 100 行就继续往下做了 | 在 1.2.9 上观察到 |
| 已安装插件内的文件，在无头运行中无需授权即可读取 | 在 1.2.9 上观察到 |
| 持有通配授权、而提示词看起来不完整时，代理为了找到剩余部分，读取了用户的 PowerShell 历史、其他会话的转录记录以及正在运行的进程的命令行 | 在 1.2.9 上用 `gemini-3.8-flash-high` 观察到 |

## 子代理

模型收到的工具声明改变了形式。`invoke_subagent` 接受一个 `Subagents` 数组，其条目包含 `TypeName`、`Role`、`Prompt`、`Model` 和 `Workspace`；`define_subagent` 接受 `enable_write_tools`、`enable_mcp_tools` 和 `enable_subagent_tools` 开关；`manage_subagents` 用于列出和终止。完整细节见 `07-subagents.md`。

根据自定义子代理文档，`tools` 列表中写了未映射工具的自定义代理可能会挂起。自 CLI 1.2.7 起，`find_by_name`、`grep_search` 和 `list_dir` 不在默认工具集中，只有列出它们的代理才能使用。

并发的子代理共享账户的模型容量：在另外两次运行同时进行时，一次父代理运行在它的三个子代理都完成之后，以 `RESOURCE_EXHAUSTED (code 429)` 为由以 `ERROR` 状态结束，所以规划扇出规模时要考虑这一点。除非代理文件设置 `inheritCustomizations: false`，否则自定义项会传到子代理；测量数据见 `08-delegation.md`。

## 无头运行

| 行为 | 证据 |
| :--- | :--- |
| CLI 的策略来自 `~/.gemini/antigravity-cli/settings.json` 中的 `toolPermission`，默认是 `request-review`，所以桌面设置里的 `autoExecutionPolicy: AUTO` 在 `agy -p` 下不起作用。`toolPermission: "always-proceed"` 能在无头模式下运行未授权的命令，同时仍然遵守 `deny` 规则 | 在 1.2.9 上观察到；issue #1054 |
| 返回 `allow` 的 `PreToolUse` 钩子，或返回带 `permissionOverrides` 的 `ask`，都不会放行未授权的调用。`deny` 连已授权的调用也会阻止 | 于 2026 年 9 月 19 日和 24 日观察到；open issue #1053 |
| 与 `decision: "allow"` 一起返回的 `overwrite` 会被应用并告知代理，权限按改写后的参数检查。没有 `decision` 的 `overwrite` 等于拒绝 | 于 2026 年 9 月 19 日和 24 日观察到 |
| 钩子拒绝一条命令后，最终回复仍可能写出这条命令本该打印的输出。在 11 次这样的运行中有 6 次，回复正是提示词要求的那个标记，而记录显示命令从未运行 | 在 1.2.9 上观察到 |
| 一个工具被拒绝会丢弃这一轮，而运行报告 `"status": "SUCCESS"`，退出码为 0。测得的最大损失是 48 个已完成步骤和 20,595 个输出 token | 在 1.2.7 上观察到，在 1.2.9 上再次观察到；open issue #794 |
| 从无头运行启动的子代理，除非授予了 `read_file`，否则读取工作区文件时会被拒绝 | 在 1.2.9 上观察到 |
| 如果父代理在子代理仍在运行时结束了这一轮，它永远收不到结果。运行会等子代理结束，然后关闭，日志记录 “Failed to wake idle agent on message: run state not found”，并以父代理的最后一条回复报告 `SUCCESS` | 在 1.2.9 上的 2 次受控运行中 2 次观察到，另有一次审计；issue #1044。持续轮询的运行最多等待了 338 秒，并收到了每一个结果 |
| 代理和模型 API 失败时会在 stderr 打印 `AGY_ERROR: {...}` 并以 3 退出 | read：1.2.6 更新日志 |
| `--json-schema` 会把一个既不是可读文件也不是 JSON 对象的参数变成字符串 schema，而根节点不是对象的 schema 总是返回 HTTP 400 | 在 1.2.7 上的 42 次运行中观察到，在 1.2.9 上再次观察到；open issue #1064 |

一次安全审计在进行了 13 分钟、启动了 7 个子代理之后，最终回复被替换成了 “This request was blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related queries.”（在 1.2.9 上用 `gemini-3.8-flash-high` 观察到）。围绕明确的授权或 `toolPermission` 来规划无头运行。钩子的放行靠不住，而 `SUCCESS` 状态也不能证明这一轮的工作保住了。

## 钩子

- `invocationNum` 从零开始计数，所以第一轮报告的是 0。文档中的示例写的是 3，却没有说明这一点。
- `hooks.json` 的命令里不要加任何引号。在 Windows 上引号会原样传给程序：加了引号的可执行文件会“not recognized”，加了引号的脚本路径会被拼接到钩子所在的文件夹后面（issue #222）。使用不带空格、不加引号的路径。
- 用 JSON 序列化器写 `hooks.json`。bash heredoc 会把 Windows 路径中成对的反斜杠合并，产生无效的转义。
- 钩子的工作目录是包含 `hooks.json` 的那个文件夹。
- 失败的 `PreInvocation` 钩子会被跳过：无效的 JSON、空输出、非零退出和超时都被容忍了（2026 年 9 月 19 日）。`PreToolUse` 钩子失败时则拒绝：无效的 JSON、`{}`、缺少 `decision` 和非零退出都会拒绝这次调用，只有空输出会放行（1.2.9）。超时确实生效。自桌面版 2.4.3 起，无法运行的配置会在加载时被拒绝并报错。
- `terminationBehavior: "force_continue"` 没有上限（open issue #1055）：在 1.2.9 上钩子运行了 12 次，强制多出 11 次模型调用，其中九次是空话，两次去调用了没人要求的工具。`Stop` 钩子可以用 `decision: "continue"` 阻止终止，并会收到可用于设限的 `executionNum`。见 `10-iteration.md`。

要验证一个钩子，让它的脚本向一个哨兵文件追加内容，并注入一个唯一随机数、要求代理复述它，然后两者都检查。文件合法、日志安静，都不能证明钩子运行过。

## 权限

授权以命令原文保存，有时只保存第一个词，于是出现 `command(if)`、`command(&)` 这样的条目，旁边还有被整段保存为一条授权的数 KB 脚本。授权只会与逐字节相同的命令再次匹配，所以提示会再次出现，又追加一条无用的授权。有一台机器上的 `~/.gemini/config/config.json` 达到了 301 KB，其中 97.5% 是无用的授权，最长的一条有 36,331 个字符。不时检查一下它的大小。真正值得保留的是针对域名的 `read_url` 授权。

项目设置覆盖全局设置。`~/.gemini/config/projects/*.json` 中的每个文件都可以带有自己的执行策略，只要某个项目另有设置，在界面上修改全局设置就不起作用。策略取值为 `always-proceed`、`request-review`、`strict` 和 `proceed-in-sandbox`，自桌面版 2.15.1 起 Windows 上支持文件和网络沙箱（read：内置 `antigravity-guide` 技能及其 `app.md` 参考，以及更新日志）。

CLI 从它自己的 `settings.json` 中的 `permissions.allow` 和 `~/.gemini/config/config.json` 中的 `globalPermissionGrants.allow` 读取授权；日志行 `stored shared config permissions` 显示的是后者。在 Windows 上，`command()` 规则只匹配完全相同的命令行、`command(*)`，或覆盖整行的 `regex:` 规则，例如 `command(regex:git .*)`。`command(git)` 和 `command(git *)` 匹配不到任何带参数的调用（在 1.2.9 上观察到；issue #619、#955）。

一条告诉模型永远不要请求权限的规则是行不通的，因为策略在咨询模型之前就已经执行了。

## 各界面的工具

在 agy 1.2.9 上，默认代理的工具列表包含 `ask_question`、`call_mcp_tool`、`define_subagent`、`generate_image`、`invoke_subagent`、`list_resources`、`manage_subagents`、`manage_task`、`read_resource`、`read_url_content`、`replace_file_content`、`run_command`、`schedule`、`search_web`、`send_message`、`view_file` 和 `write_to_file`，以及已启用 MCP 服务器提供的工具。没有浏览器工具。浏览器工具在开启浏览器集成时出现在桌面应用中，而有一次记录在案的桌面运行完全没有浏览器工具，所以规划之前要先检查。替代方案见 `04-runtime-verification.md`。

其他值得了解的功能：`ask_question` 在交互式会话中向用户提出结构化问题；`/plan` 在动手之前起草一份可编辑的计划，由 Plan Review Policy 设置控制（桌面版 2.17.0）；`agy --effort low|medium|high` 设置推理强度；`agy models` 列出账户可用的模型；`agy --agent <name>` 以某个自定义代理启动会话。

## 脚本化编排

当一次扇出需要在数百个条目上运行并保持精确计数时，脚本比任何代理的记忆都更可靠。根据 SDK 插件文档（版本 0.0.7），Google Antigravity Python SDK（`pip install google-antigravity`）可以从代码中启动代理和子代理，提供 `SubagentConfig`、`enabled_tools`、`allowed_subagents`、`max_subagent_depth`，以及用于结构化输出的 `response_schema`。它使用 `GEMINI_API_KEY` 认证，费用计在该密钥上，而不是 Antigravity 套餐上。这条途径尚未与本技能一起测试，所以把它当作有文档记载但未经验证。

## 对照运行中的平台核查

上面有几条与文档相矛盾，而且 CLI 在产生这些结论的测试进行到一半时自行更新了。当平台行为对任务很重要时，在已安装的版本上测试它，并给结果加盖戳记。证据层级适用于平台，就像适用于工作本身一样。
