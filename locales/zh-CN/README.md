# Gravitas

[English](https://github.com/Emily2040/gravitas/blob/main/README.md) · **简体中文** · [日本語](https://github.com/Emily2040/gravitas/blob/main/README.ja.md) · [한국어](https://github.com/Emily2040/gravitas/blob/main/README.ko.md)

这是安装程序放进插件文件夹里的 README。完整版在 [GitHub](https://github.com/Emily2040/gravitas) 上，里面有多种语言的真实例子、全部测试结果，以及和其他工具的比较。

## 第一部分：你刚装上的是什么

Gravitas 要你的 Antigravity 代理像这件事最在行的那个人那样回答：先查清答案靠的是什么，你哪里想错了，就客气地告诉你。

它在每次对话里加一条简短的规则。规则要代理按你的本意读懂你的话，给出最在行的人会给的东西：改邮件，像个好编辑；查 bug，像个工程师；问用药剂量，像个临床医生。你最先需要什么，它就先给什么。你要依赖的东西，它按你实际使用的方式去检验：步骤走到最后一步，代码真跑一遍，会变的规定就打开官方页面，要精确计数的地方交给脚本去数。每个说法，证据允许多肯定就说多肯定；规定写明是哪个地方、哪个日期的；没法说准的，给出范围和原因。你以为对的东西要是错了，它会客气地指出来，只改错误牵连到的部分，然后照样把你要的东西给你。它按读者来写，用你的语言和当地惯例。技术性文字按简明技术写法来写，中文版规则点名的是阮一峰《中文技术文档的写作规范》，标点和数字分别按 GB/T 15834-2011 和 GB/T 15835-2011。

这一切底下有一条底线：绝不比普通回答差。扎实的普通回答能给的，它全都保留；回复里没有状态行和标签，也不写“正在核查”之类的话。危险信号和求助热线，只出现在临床医生会认为危险还在后头的地方；有人可能身处危险时，它会像受过训练的危机干预咨询师那样跟对方说话。

举个例子：有人请它润色一份春节放假和值班通知，初稿把除夕当成普通休息日，除夕值班只给补休、不发加班费。在 Gemini 3.1 Pro 上，原版 Antigravity 夸初稿“各项说明也很准确”，把这一条原样留了下来。装了 Gravitas 后，它先上网查了现行规定：从 2025 年起，除夕已经是法定节假日，值班要按 300% 付加班费。它先把这一点说清楚，再交出改好的完整通知。

这个例子和下面的数字，测的都是上一版规则（v4）的英文版；中文版规则还没有单独测过。这一版的规则不是在 v4 上修修补补，而是从头推导出来的：v4 明显输给原版 Antigravity 或 `/boost` 的每一个用例，我都逐个剖析了一遍，一共 109 次真实失利，归结为十种机制；新规则前后写了四稿，每一稿都交给一个专门挑错的对手去攻击。它在真实安装的环境里通过了发布前的检查：17 道题里，四种语言的聊天和角色扮演都没有问题；规则底线改了两处以后，每种语言的危机题，回复都被评为比同一模型上的原版 Antigravity 更好。完整的基准测试它还没跑。v4 没赢的地方，是边缘集（历史、深度知识、文字游戏、创意写作）和一部分模型（Codex Astra、Grok 4.5），这次重写瞄准的正是这些地方。

遇到一遍核查不完的工作，比如审计、审查、跨很多文件的修改、研究报告或构建，代理会加载深度工作技能。在那里，它要说清每个结论是怎么知道的，另外几个检查员代理会去找错误和遗漏，它们手里没有任何能改文件的工具。

如果安装时加了 `--review`，第二意见就是开着的：你要依赖、要据此行动或要发出去的回答，会先交给一个在 Gemini 3.1 Pro 上运行的独立审查者，它最多指出三处错误，代理只改这几处，然后你才看到答案。等待期间，会有一行消息说正在把答案再核对一遍。双击安装程序不装它；用终端安装并加上 `--review` 才会装。

开销。在 Gemini 3.8 Flash 上的 60 道日常请求里，用 v4 规则时回答用时的中位数是 35 到 36 秒，不装是 22 到 23 秒，加第二意见是 80 到 81 秒。在 Gemini 3.1 Pro 上，规则只多花几秒。这一版的规则比 v4 长，英文版 1,216 词对 809 词。深度工作要花好几分钟，同时跑好几个代理。

它做不到什么。它不能让模型知道得比本来更多。它的规则是指令，模型可能漏掉，也可能用在不该用的地方。所有基准测试都是在 Windows 11 上用 `agy` 命令行工具跑的；桌面应用没有做基准测试，Mac 安装程序也还没在真正的 Mac 上跑过。

卸载：再双击一次安装程序，选“卸载 Gravitas”，或者在下载的文件夹里运行 `python scripts/install.py --uninstall`。两种方式都会把插件移到你主文件夹里 `.gemini/gravitas-backups` 下一个以日期和时间命名的文件夹。卸载之后，重启 Antigravity，或者新开一个 agy 会话。想关掉又不卸载，运行 `agy plugin disable gravitas`；要重新打开，运行 `agy plugin enable gravitas`。这两条命令成功时什么都不输出，重新安装也不会把它重新打开。要加上或去掉第二意见，就带上 `--review` 或 `--no-review` 再运行一次 `install.py`，并加上语言代码 `zh-CN`。要报告问题，请用我 [GitHub 主页](https://github.com/Emily2040) 上的链接。

## 第二部分：这个文件夹里有什么

```text
plugin.json                  清单文件：Antigravity 显示的名称和描述
rules/AGENTS.md              常驻规则：给这个人最好的回答、底线、装了的话还有第二意见、什么时候加载技能
agents/                      八个工具列表固定的代理；加 --review 安装时还有 gravitas-reviewer
skills/gravitas/SKILL.md     深度工作的路由，它会加载 references/00-orchestrator.md
skills/gravitas/references/  十五个模块，每个不超过 100 行，一次 view_file 就能读完
skills/gravitas/schemas/     子代理返回的发现和裁决记录格式
skills/gravitas/scripts/     ledger.py、provenance_check.py、check_skills.py、slopcheck.py
skills/gravitas/scripts/checks/  六个计数检查，用于诗律、数字和日期，连同所需数据
skills/gravitas/examples/    一套关卡测试，在它取材的那个场景上会亮红灯
```

规则怎么起作用。它开头先定下一种读法，后面每一行都按它来：按用户的本意、在他设定的框架里读他的话；回答的每一部分能不能出现、占多大篇幅，都看它对用户的来意有多大用处。接下来七条，说的是最好的回答该怎么做：给出这条消息该找的那类人中最出色的一位会给的东西，用户最先需要的先给；用户要依赖的东西，按他实际使用的方式去检验，每个说法说到证据允许的准确和肯定程度；意思按框架判断，后果按现实世界判断，所以纠正一个错误时，它牵连到的都重算，没牵连到的不动；每份文字写给它的读者；按所属行当的标准来写。底线是绝不比普通回答差：扎实的普通回答能给的全都保留，只去掉凑字数的话、用不上的过程叙述，以及声称做过却没运行的核查。

规则是怎么写出来的。v4 在基准测试里明显输掉的每一个用例，我都研究了一遍。“明显输掉”是指：判它输的评分模型至少两个、而且过半，判差距明显的至少占全部评分模型的一半。逐个检查的 118 次失利里，9 次是噪声，109 次是真实的失利，分布在 66 道题上。其中 78 次，是 v4 的某一行把模型推向了失利，最常见的是套路固定的句子：有的规定了位置，有的一碰到某个话题就加一节，有的按句子的形式往下砍，不管这样做对眼前这个人有什么影响。28 次，是 v4 没有哪一行能拦住基础模型自己出的错；还有 3 次是测试框架的问题。新规则写了四稿，每一稿都交给一个对手，由它专门编请求来攻破；前三稿分别被 18、20、19 个请求攻破，后一稿把前一稿的这些漏洞都堵上了。

一次运行的过程。规则总是会加载，普通请求就在对话里按规则回答，不用技能。装了第二意见时，代理先写出完整草稿，用请求和草稿启动 `gravitas-reviewer`，设一个 180 秒的 `schedule` 计时器，参数是 `TimerCondition: "any"`，用一行等待提示结束本轮，等审查者的消息到了，只改它指出的问题。深度工作会打开技能，由技能路由到编排器。编排器写一份任务记录，选定规模（quick、standard、full 或 exhaustive），扇出、投票和停止都有固定的数字，并指明要加载哪些模块。工作清单用真实工具建立，专职代理带着绝对路径和返回格式扇出，关键结论交给独立核查，完整性评审者指出从没核查过的东西，报告连同层级和缺口写进文件。回复用平实的话给出结论和发现。

| 层级 | 必须真的发生过 |
| :--- | :--- |
| `observed` | 检查过产物本身，并且标签写明了它 |
| `executed` | 一个工具运行并返回了这个值，标签写出了命令或查询，以及返回了什么 |
| `read` | 取得过来源，标签给出 URL 或路径，并引用原文那一行 |
| `inferred` | 推理或回忆；所有空位填不上的内容 |

层级只用在深度工作的报告里，对话里的回复从不带层级。

所有代理都没有改文件的工具。核查者和审查者可以运行命令，它们被要求绝不改动自己检查的工作；文风编辑者把改好的文字返回，而不是直接写进文件。

| 代理 | 职责 | 工具 |
| :--- | :--- | :--- |
| `gravitas-scout` | 定位文件、路由、符号和来源 | `list_dir`、`find_by_name`、`grep_search`、`view_file` |
| `gravitas-reader` | 就指定的文件或 URL 回答问题，并引用原文 | `view_file`、`grep_search`、`find_by_name`、`list_dir`、`read_url_content` |
| `gravitas-finder` | 在一份工作清单上搜寻某一类缺陷 | 阅读者的工具，外加 `search_web` |
| `gravitas-checker` | 运行一项独立核查 | `view_file`、`run_command` |
| `gravitas-refuter` | 尝试推翻一个结论，默认判为已推翻 | `view_file`、`grep_search`、`read_url_content`、`search_web` |
| `gravitas-visual-critic` | 以没看过源文件的观看者身份评判一张截图 | `view_file` |
| `gravitas-completeness-critic` | 指出从没搜过、打开过、运行过或核实过的东西 | `view_file`、`list_dir`、`grep_search`、`find_by_name` |
| `gravitas-prose-editor` | 按文风标准修改草稿 | `view_file` |
| `gravitas-reviewer`（加 `--review` 时） | 在一份回复草稿里找出最多三处缺陷，从事实错误到格式错误 | `view_file`、`read_url_content`、`search_web`、`run_command` |

下面这些脚本都在这个文件夹里运行。`--latest` 对照最近一次会话核查；会话的 id 就是 `~/.gemini/antigravity-cli/brain/` 下的文件夹名，也可以在 `agy -p --output-format json` 的输出里找到 `conversation_id`。

```bash
python skills/gravitas/scripts/check_skills.py          # 校验 ~/.gemini/config 下的每个技能、代理、规则和插件
python skills/gravitas/scripts/provenance_check.py <回答文件> --latest   # 对照对话记录核查证据标签
python skills/gravitas/scripts/ledger.py --help         # 扇出时记账：去重、计票、没有新发现的轮数
python skills/gravitas/scripts/slopcheck.py <文件>      # 机器腔调的结构特征；加 --strict 时，有一处就判失败
```

`skills/gravitas/scripts/checks/` 里的六个检查，数的是模型会数错、还说得很笃定的东西：`pingze_check.py` 查绝句和律诗，`couplet_check.py` 查对联，`mora_count.py` 查俳句、短歌和川柳，`sijo_check.py` 查韩国平时调（평시조），`num_units.py` 查跨万、亿、億、만、억、lakh、crore 和 million 的金额，`locale_dates.py` 查写给中日韩读者的日期。每个脚本第一行打印 `PASS`、`FAIL` 或 `ERROR`，退出码是 0、1 或 2。什么时候运行哪一个，写在 `skills/gravitas/references/14-checks.md` 里。它们只能通过 `run_command` 运行，而无头运行在默认设置下会拒绝这个工具，这时就按同样的规则手工检查。

测试结果。回答由 Gemini 3.1 Pro 和 Gemini 3.8 Flash 两两盲评，对照书面的标准答案；部分比较还由 Claude Opus 5.5 和 GPT-6 Sol 评。胜率把胜记作 1、平记作 0.5，所以 0.50 表示没有差别；只有在胜率至少 0.55、票数至少 100 票时，才宣称胜出。在 Gemini 3.8 Flash 上，v4 规则在 60 道日常请求上对原版 Antigravity 的胜率是 0.57 和 0.61（各 120 票），在十种语言的 50 道题上是 0.65（150 票），对 `/boost` 是 0.84（180 票）。在 Gemini 3.1 Pro 上，日常请求是 0.58 和 0.55（各 120 票，两个区间都包含 0.50），十种语言是 0.71（150 票），对 `/boost` 是 0.77（120 票）。在 50 道边缘题上，两个 Gemini 评分模型更偏向原版，Flash 上 0.45（100 票），Pro 上 0.42（100 票），而 GPT-6 Sol 偏向 Gravitas，分别是 0.76 和 0.64（各 50 票）。v4 规则的一个便携核心版只由 GPT-6 Sol 评分，每个模型 60 票：Codex 上 GPT-6 Sol 0.66、GPT-6.1 Sol 0.57、GPT-6 Luna 0.57、GPT-6 Astra 0.47，Grok 上 Grok 4.6 0.59、Grok 4.7 build fast 0.54、Grok 4.7 0.52、Grok 4.5 0.42。第二意见按打印出来的全文评，输给了只用规则的版本（0.23 和 0.28，各 180 票），只看最终消息则打平（0.50，168 票；0.47，120 票），所以它默认关闭。一个基于钩子的版本对原版 Antigravity 的胜率是 0.57（180 票），低于同样几个评分模型给只用规则版本的 0.63 和 0.61，所以没有发布。

局限。方法的大部分是要求模型遵守的指令；工具列表、安装程序和各个脚本是机械的部分，而脚本只有在代理被告知要运行时才会运行。它在 Windows 11 上用 agy 1.2.9 到 1.2.16 测过。会影响你使用方式的平台行为，写在 `skills/gravitas/references/13-platform.md` 里。最要紧的有两点：无头的 `agy -p` 运行需要明确授予权限，或者在 `~/.gemini/antigravity-cli/settings.json` 里设置 `toolPermission`；另外，只有用 `--add-dir` 传入仓库时，CLI 才会读取仓库自己的 `.agents/` 文件夹，这也是这个插件采用全局安装的原因。在日文和韩文里，有人可能身处危险、又写得很随意时，回复可能会用礼貌体；原版 Antigravity 也会这样。

版本 1.0.0 · MIT · 作者 [Iamemily2050](https://github.com/Emily2040)
