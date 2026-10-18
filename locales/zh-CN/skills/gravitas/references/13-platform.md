# 模块 13：平台

## 用途

这里收录的是已经核实过的 Antigravity 行为；如果想当然地以为它会有别的表现，就会白费功夫。任务若依赖 Antigravity 加载自定义配置、运行 subagent、执行权限规则或以 headless 方式运行的具体方式，就加载本模块；工具、hook、技能或权限出现意料之外的行为时，也要加载。

平台迭代很快，所以每一条都注明了核查时的版本和日期。2026 年 9 月 18 日到 23 日这几天里，桌面版连发了 2.15.0、2.15.1、2.16.0、2.17.0，CLI 也发了 1.2.7、1.2.8、1.2.9。没有特别说明的条目，都是 2026 年 9 月 24 日在 Windows 11 上核查的，环境为桌面版 2.17.0 和 agy CLI 1.2.9。通过 WinGet 安装的 CLI 曾在前后只隔 21 秒的两次测试之间，自己从 1.2.7 升到了 1.2.9，没有任何提示，所以这里的版本戳一律取自当次运行日志里的 `version:` 行。2026 年 9 月 26 日，它又用同样的方式升到 1.2.11，到 2026 年 10 月 3 日已经是 1.2.16。依据某一条行事之前，先拿它的版本戳去对照 `https://antigravity.google/changelog` 上的更新日志；相关部分有变动的，重新核查一遍。

## 自定义配置从哪里加载

| 位置 | 技能 | agent | 规则 | 证据 |
| :--- | :--- | :--- | :--- | :--- |
| `~/.gemini/config/skills/`、`agents/`、`AGENTS.md` | 加载 | 加载，`agy agents` 能列出来 | 加载 | Observed |
| `~/.gemini/config/plugins/<name>/` | 加载 | 加载，但 `agy agents` 列不出来 | 从 `rules/AGENTS.md` 加载 | Observed，用一个测试插件验证：模型说出了插件里技能和 agent 的名字，也遵守了插件的规则 |
| `<repo>/.agents/` | 只有通过 `--add-dir` 才加载 | 只有通过 `--add-dir` 才加载 | `rules/` 两种方式都不加载 | Observed；issue #1036、#1052（未关闭） |

Gravitas 做成插件，就是这个原因：技能、验证 agent 和常驻规则放在同一个文件夹里，执行 `agy plugin disable gravitas` 就能一起关掉。`agy plugin list` 只列出从插件市场导入的插件，直接复制进去的插件即使已经加载，也不会出现在列表里。

工作区这一行和文档对不上。内置的自定义配置指南和技能页面都写着会从 `<repo>/.agents/` 发现自定义配置，IDE 指南也说，IDE 会自动发现并遵循这个文件夹（原文：“automatically discovers and respects”）。CLI 上的实际情况是：用 `--add-dir` 传入仓库时，`.agents/` 里的技能、agent 和 hook 都加载了，仓库同时就是工作目录时也一样。不加这个参数、直接在仓库里启动，三者一个都没加载：日志里的 `workspaceDirs` 明明列出了这个文件夹，日志却报告 `loaded 0 named hooks`。`.agents/rules/` 里的规则，两种方式都没加载。需要用到仓库自带的自定义配置时，运行 `agy -p "..." --add-dir <repo>`。桌面应用和 IDE 没有测过。

## 预算不够，自定义配置会被丢掉

所有技能的名称和描述共用一份自定义配置预算，放不下的技能直接丢掉。装了 133 个技能时，模型把其中 3 个列在“Excluded Skills (due to context budget limits)”下面。这 3 个的描述都在已安装技能中最长的 5 个之列，长度在 1,001 到 1,028 个字符之间。长度和被排除之间的这层关联属于 inferred，依据只有这一次观察。描述要写短，本技能的描述不到 500 个字符。

规则另有一份 20,000 token 的预算，每个规则文件在 24,000 字节处截断，截断点落在行边界上；超出预算的规则会降级成文件指针（read：内置 `agy-customizations` 指南里的 `docs/rules.md`，以及 CLI 1.2.7 的更新日志）。

## 格式错误的技能会静默失败

解析不了的 `SKILL.md` 会被直接跳过。报错只会写进 `~/.gemini/antigravity-cli/log/cli-*.log`，内容是 `skills.go:201] Failed to parse skill file ...`，用户能看到的地方都不会显示。一个 UTF-8 BOM（字节顺序标记）就足以触发，而 Windows PowerShell 5.1 的 `Set-Content` 和 `Out-File` 默认就会写入 BOM。一个技能坏了，不影响其他技能加载。

每次修改后都要运行 `scripts/check_skills.py`。它会检查：frontmatter 能否解析、描述是否存在及其长度、BOM、失效引用、超过 100 行的模块、agent 的工具名、带写入工具的评审 agent，以及规则文件大小。

## 文件与路径

| 行为 | 证据 |
| :--- | :--- |
| `view_file` 不接受相对路径，但 headless 运行时，agent 会把 `~/.gemini/antigravity-cli/scratch/` 当成自己的工作目录。主 agent 被拒之后转去这个目录里搜索；一个 subagent 被要求使用“当前工作区里”（原文：“in the current workspace”）的 `draft.md`，它直接拼出了指向这个目录的路径。所有 CLI 会话共用这个文件夹，里面还留着五天前测试的 33 个文件，结果两者都打开了一个同名的旧文件，而且对此只字未提 | Observed（1.2.9） |
| `view_file` 每次调用只返回 100 行。有一次运行中，agent 读了一个 114 行文件的前 100 行，就接着往下做了 | Observed（1.2.9） |
| headless 运行时，已安装插件里的文件不需要授权就能读取 | Observed（1.2.9） |
| agent 手握通配符授权，又碰上一个看起来没写完的 prompt，为了找出缺的部分，就去读了用户的 PowerShell 历史、其他会话的对话记录，以及正在运行的进程的命令行 | Observed（1.2.9，`gemini-3.8-flash-high`） |

## Subagent

模型收到的工具声明，结构已经变了。`invoke_subagent` 接收一个 `Subagents` 数组，每一项包含 `TypeName`、`Role`、`Prompt`、`Model`（取值为 `inherit`、`flash_lite`、`flash` 或 `pro`）和 `Workspace`；`define_subagent` 接收 `enable_write_tools`、`enable_mcp_tools`、`enable_subagent_tools` 三个开关；`manage_subagents` 负责列出和终止 subagent。详见 `07-subagents.md`。

按自定义 subagent 文档的说法，自定义 agent 的 `tools` 列表里如果写了没有映射的工具，可能会卡住。从 CLI 1.2.7 开始，`find_by_name`、`grep_search` 和 `list_dir` 不在默认工具集里了，只有列出它们的 agent 才能用。

并发的 subagent 共用同一个账号的模型额度。有一次，另有两次运行同时在跑，一个父 agent 的运行在它的三个 subagent 都跑完之后，因 `RESOURCE_EXHAUSTED (code 429)` 以 `ERROR` 状态结束。所以定 fan-out 规模时，要把这一点算进去。除非 agent 文件里设置了 `inheritCustomizations: false`，否则自定义配置会传给 subagent；实测数据见 `08-delegation.md`。

## Headless 运行

| 行为 | 证据 |
| :--- | :--- |
| CLI 的执行策略取自 `~/.gemini/antigravity-cli/settings.json` 里的 `toolPermission`，默认是 `request-review`，所以桌面版设置里的 `autoExecutionPolicy: AUTO` 对 `agy -p` 不起作用。设成 `toolPermission: "always-proceed"` 后，headless 模式下没有授权的命令也能运行，`deny` 规则照样生效 | Observed（1.2.9）；issue #1054 |
| `PreToolUse` hook 返回 `allow`，或者返回带 `permissionOverrides` 的 `ask`，都放行不了没有授权的调用。反过来，`deny` 连已授权的调用也会拦下 | Observed（2026 年 9 月 19 日、24 日）；issue #1053（未关闭） |
| `overwrite` 搭配 `decision: "allow"` 时会生效，并且会告知 agent，权限检查针对的是改写后的参数。只有 `overwrite` 而没有 `decision`，等同于拒绝 | Observed（2026 年 9 月 19 日、24 日） |
| hook 拒绝了某条命令，最终回复里却可能写着这条命令本该打印的输出。这类运行共 11 次，其中 6 次的回复正好是 prompt 要求的那个标记，而对话记录显示命令根本没运行过 | Observed（1.2.9） |
| 一个工具被拒，这一轮就整个作废，运行却报告 `"status": "SUCCESS"`，退出码为 0。实测损失最大的一次，丢掉了 48 个已完成的步骤和 20,595 个输出 token | Observed（1.2.7，1.2.9 上再次出现）；issue #794（未关闭） |
| 默认设置下，headless 运行不需要授权就允许 `view_file` 和 `search_web`，但会拒绝 `run_command` 和 `read_url_content`。在空文件夹里问一个不需要别的信息就能回答的问题，第一个调用就是用 shell 列出这个文件夹：装了本插件时 34 次里有 30 次如此，不装时 34 次里有 21 次；凡是第一个调用是列目录的运行，回复全都丢了。`PreToolUse` hook 的 deny 发生在这道权限检查之前，所以被 hook 拒掉的 `dir` 没有让回复丢失 | Observed（1.2.11，2026 年 9 月 26 日、27 日） |
| `--sandbox --dangerously-skip-permissions` 下，命令在工作区里运行，工作区外的写入会被拒绝，但任何位置都能读，也能联网。有两次运行读到了工作区往上两级目录里的文件 | Observed（1.2.11，2026 年 9 月 26 日） |
| 从 headless 运行里启动的 subagent，如果没有授予 `read_file`，读工作区文件时 `read_file` 会被拒绝 | Observed（1.2.9） |
| subagent 还在运行、又没有待触发的定时器时，父 agent 一旦结束这一轮，就再也收不到结果。运行会等 subagent 结束，然后关闭，在日志里记下“Failed to wake idle agent on message: run state not found”，并以父 agent 的最后一条回复报告 `SUCCESS` | Observed（1.2.9，2 次受控运行 2 次都出现，另有一次审计）；issue #1044。1.2.16 上 1 次运行再次出现：回复只剩那句等待提示，日志里没有“Failed to wake”这一行，消息留在了会话的 `messages/undelivered` 文件夹里 |
| `schedule` 调用后立即返回。一次性定时器还没触发时，headless 运行会一直保持存活（stderr：`root agent idle; waiting up to 30m0s for 1 background task(s)`），直到定时器触发或被取消 | Observed（1.2.16，2026 年 10 月 3 日，使用 `--sandbox --dangerously-skip-permissions`）；等待模式的写法见 `08-delegation.md`，该模式在默认设置下尚未测试 |
| subagent 如果没调用 `send_message` 就结束，唤醒父 agent 的是一条发送者为 `system`、内容为它最后一条回复的消息，所以设为这个 subagent ID 的 `TimerCondition` 不会被取消：7 次运行里，240 秒的定时器 7 次都走满了全程，父 agent 回复了两次。subagent 自己调用 `send_message` 时，消息带着它的 ID，3 次运行里 3 次都取消了这类定时器。设为 `"any"` 的，8 次里 8 次都被取消 | Observed（1.2.16，2026 年 10 月 3 日，使用 `--sandbox --dangerously-skip-permissions`） |
| 既没有文本、也没有工具调用的一轮会被拒绝（“model output must contain either output text or tool calls, these cannot both be empty”），所以哪怕这一轮只是在等待，也必须说一句简短的话。headless 运行会把这句话打印出来，和工具调用写在一起的文本也会打印 | Observed（1.2.16，Gemini 3.8 Flash）：在 3 次被要求静默结束本轮的运行中，有 2 次出现了这个错误 |
| agent 或模型 API 出错时，会在 stderr 打印 `AGY_ERROR: {...}`，并以退出码 3 退出 | Read：1.2.6 更新日志 |
| 无头运行的 `agy -p` 一轮在大约一小时时以 `UNAUTHENTICATED (code 401)` 结束，2 次长时间运行里 2 次都如此（28 分钟和 61 分钟），subagent 的工作和已写入的文件完好；`agy -c` 可以接着这次会话继续 | Observed on 1.4.0，2026 年 10 月 18 日，带 `--sandbox`。要在那之前写好输出和报告，并准备好续跑 |

有一次安全审计跑了 13 分钟、启动了 7 个 subagent，最终回复却被替换成“This request was blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related queries.”（observed，1.2.9，`gemini-3.8-flash-high`）。规划 headless 运行时，要以明确的授权或 `toolPermission` 为准，hook 的放行指望不上；状态显示 `SUCCESS`，也不能说明这一轮的工作成果还在。

## Hook

- `invocationNum` 和 `executionNum` 都从 0 开始计数。插件自带的 `hooks.json` 会被加载，模型也遵从了在 invocation 0（即第一次调用）时注入的 `ephemeralMessage`（1.2.11）。
- `Stop` hook 把正常结束报告为 `terminationReason: "NO_TOOL_CALL"`，而不是文档里写的 `model_stop`；遇到 429 之类的错误时也会触发（`"ERROR"`）。返回 `continue` 会在第一条回复后面再追加一条，JSON 里的 `response` 把两条拼在一起；如果是在出错之后返回 `continue`，则会重新进入重试循环（1.2.11，2026 年 9 月 26 日）。
- `hooks.json` 的命令里，任何东西都不要加引号。在 Windows 上，引号会原封不动地传给程序：带引号的可执行文件会报“not recognized”，带引号的脚本路径会被拼接到 hook 所在文件夹的后面（issue #222）。路径要写成不含空格、不加引号的形式；写这个文件要用 JSON 序列化器，因为 bash heredoc 会把 Windows 路径里成对的反斜杠合并掉。hook 的运行目录是 `hooks.json` 所在的文件夹。
- `PreInvocation` hook 出错时会被跳过：无效 JSON、空输出、非零退出码、超时，每一种都被放过了（2026 年 9 月 19 日）。`PreToolUse` hook 则是失败即拒绝：无效 JSON、`{}`、缺少 `decision`、非零退出码，任何一种都会拒绝这次调用，只有空输出才放行（1.2.9）。超时限制确实生效。从桌面版 2.4.3 开始，无法运行的配置会在加载时直接报错拒绝。
- `terminationBehavior: "force_continue"` 没有上限（issue #1055，未关闭）：在 1.2.9 上，hook 跑了 12 次，硬是多出 11 次模型调用，其中 9 次是凑数的空话，2 次调用了没人要求的工具。`Stop` hook 可以用 `decision: "continue"` 阻止终止，同时会收到 `executionNum`，可以用它来设上限。见 `10-iteration.md`。
- 要验证一个 hook，就让它的脚本往一个哨兵文件里追加内容，同时注入一个唯一的 nonce 并要求原样复述，然后两头都检查。文件格式合法、日志里一片安静，都不能证明 hook 真的运行过。

## 权限

授权是按命令原文存的，有时只存第一个 token，于是会出现 `command(if)`、`command(&)` 这样的条目，旁边还有几 KB 的整段脚本被存成了一条授权。授权只会再次匹配逐字节完全相同的命令，所以确认提示照样弹出，又多出一条用不上的授权。有一个 `~/.gemini/config/config.json` 涨到了 301 KB，其中 97.5% 是这种失效授权，有一条长达 36,331 个字符。隔一段时间就查一下这个文件的大小。真正值得留着的，是按域名授予的 `read_url` 授权。

项目设置优先于全局设置。`~/.gemini/config/projects/*.json` 里的每个文件都可以带自己的执行策略；只要项目里另有设置，在界面上改全局设置就没有效果。策略的取值有 `always-proceed`、`request-review`、`strict` 和 `proceed-in-sandbox`。从桌面版 2.15.1 开始，Windows 上可以使用文件和网络沙箱（read：内置的 `antigravity-guide` 技能、它的 `app.md` 参考文档，以及更新日志）。

CLI 从两处读取授权：它自己 `settings.json` 里的 `permissions.allow`，以及 `~/.gemini/config/config.json` 里的 `globalPermissionGrants.allow`；日志里出现 `stored shared config permissions` 这一行，说明读到了后者。在 Windows 上，`command()` 规则只有三种写法能匹配：照原样写出整条命令行、`command(*)`，或覆盖整行的 `regex:` 规则，例如 `command(regex:git .*)`。`command(git)` 和 `command(git *)` 匹配不到任何带参数的调用（observed，1.2.9；issue #619、#955）。在规则里告诉模型永远不要请求权限，是不起作用的，因为策略在模型参与之前就已经执行了。

## 各端可用的工具

在 agy 1.2.9 上让默认 agent 列出工具，得到的是 `ask_question`、`call_mcp_tool`、`define_subagent`、`generate_image`、`invoke_subagent`、`list_resources`、`manage_subagents`、`manage_task`、`read_resource`、`read_url_content`、`replace_file_content`、`run_command`、`schedule`、`search_web`、`send_message`、`view_file` 和 `write_to_file`，外加已启用的 MCP 服务器提供的工具。里面没有浏览器工具。桌面应用在开启浏览器集成时会出现浏览器工具，而有一次记录在案的桌面版运行里，一个浏览器工具都没有，所以规划之前先确认。替代方案见 `04-runtime-verification.md`。

其他值得了解的入口：`ask_question` 在交互式会话里向用户提结构化问题；`/plan` 在动手构建之前先起草一份可编辑的计划，受 Plan Review Policy 设置控制（桌面版 2.17.0）；`agy --effort low|medium|high` 设置推理强度；`agy models` 列出账号可用的模型；`agy --agent <name>` 以某个自定义 agent 的身份启动会话。

## 用脚本编排

fan-out 要跑几百个条目、还要精确计数时，脚本比任何 agent 的记忆都靠谱。根据 SDK 插件的文档（版本 0.0.7），Google Antigravity Python SDK（`pip install google-antigravity`）可以在代码里启动 agent 和 subagent，提供 `SubagentConfig`、`enabled_tools`、`allowed_subagents`、`max_subagent_depth`，以及用于结构化输出的 `response_schema`。它用 `GEMINI_API_KEY` 认证，费用记在这个 key 上，不走 Antigravity 套餐。这条路还没有和本技能一起测过，只能当作文档里写了、但未经验证的方案。

## 以实际运行的平台为准

上面有好几条与文档矛盾，而且得出这些结论的测试做到一半，CLI 还自己更新了。任务要依赖平台的某个行为时，就在当前安装的版本上实测，并给结果打上版本戳。证据层级怎样用在工作上，就怎样用在平台上。
