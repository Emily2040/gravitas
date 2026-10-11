# 模块 08：委派

## 用途

本模块讲三件事：怎么给 subagent 写任务书，让它交回的结果能够核查；怎么等它跑完；以及在它的论断写进报告之前，怎么确认它实际做了什么。需要和 `07-subagents.md` 一起加载。

## 任务书规范

任务书写得不好，交回来的东西用不上，token 白花了，活还得重做。每个 `Prompt` 都必须写清下面六项。

1. 范围（Territory）：要处理的文件、论断、路由或来源，一律写绝对路径或完整 URL，除此之外什么都不列。范围之间有重叠，结果就会重复；范围之间有空档，就会漏掉东西，而且没人察觉。
2. 问题（Question）：只问一个问题，问得足够窄，答案才能核查。
3. 返回格式（Return shape）：如果是插件自带的 agent，就用它自己的指令里规定的 JSON。绝不要写出 schema 文件名：那个路径是相对于技能文件夹的，subagent 并不知道这个文件夹在哪儿，拿到文件名就会到处去找。用 `define_subagent` 创建的 agent，要把 `schemas/finding.schema.json` 或 `schemas/verdict.schema.json` 里的字段写成一个示例对象，抄进它的 `system_prompt`，并告诉它没有任何文件需要去找。只告诉 agent 要找什么，它交回来的就是一篇作文。
4. 证据（Evidence）：每条论断都在同一个字段里写明层级和来源；凡是第 4 级的内容，一律标为假设。
5. 停止条件（Stop condition）：范围覆盖完就停，或者处理完规定数量的条目就停。
6. 受阻时怎么办（Blocked behaviour）：工具调用被拒绝或文件不存在时，把已有的内容交回来，状态写 `blocked`，并附上原始报错信息。被拒之后严禁另想办法绕过去，平台自己的拒绝提示里也是这么写的。

subagent 只交结果，不汇报进度。

绝不能给 subagent 相对路径。2026-09-24 在 agy 1.2.9 上，`view_file` 解析相对路径时，基准目录不是工作区，而是 `~/.gemini/antigravity-cli/scratch/`，这是所有 CLI 会话共用的文件夹。`gravitas-prose-editor` 收到的指令是编辑“当前工作区里”（原文“in the current workspace”）的 `draft.md`，结果它改的却是五天前一次测试遗留在那个文件夹里的另一个 `draft.md`，没报任何错误，就把改动交了回来。`gravitas-refuter` 和 `gravitas-visual-critic` 的相对路径也被解析到了同一个文件夹，什么都没找到，返回了 `blocked`；相比之下，这种失败方式反而更好。

要明确告诉每个 subagent：它需要的一切都已经写在 prompt 和指令里了。在审计测试中，有个搜寻者被告知输出必须符合“the Gravitas finding schema”，结果它 127 步里的大部分都花在了翻遍用户的各个文件夹找这个文件上，一路上还读了 git 内部文件和不相干的测试输出。现在插件自带的 agent 都把完整的 schema 作为示例直接写在里面，并明确告诉它们不用再去找任何东西。重跑时，每个搜寻者和反驳者都在 4 到 8 步内完成，范围以外的东西一个都没打开。

负责证明路径穿越、注入或数据泄露的核查者，要拿它自己在临时文件夹里创建的无害诱饵文件（canary）当目标。同一次测试里，核查者是通过那个有缺陷的函数读取 `C:\Windows\win.ini` 来证明路径穿越的：放在那台机器上无害，但换到存有真实机密的机器上，这就是个坏习惯。

```text
Role: Refuter, session handling
Territory: the claim below and C:/work/app/src/auth/session.ts. Nothing else.
Claim: "logout() leaves the refresh token valid" (C:/work/app/src/auth/session.ts:88-120)
Question: can you show this claim is false?
Return: one JSON object with exactly the fields in your instructions.
Evidence: every statement carries its tier and source, e.g. read (C:/work/app/src/auth/session.ts:97, "...").
Stop: after one verdict.
If a tool is denied, return status "blocked" with the error text.
```

## 核查委派结果

主 agent 自己的状态反映不了 subagent 的情况，所以汇总之前，每个 subagent 都要逐一检查。

1. 每个 subagent 都记进台账，写明会话 ID 和最终状态：`done`、`failed`、`denied`、`empty` 或 `killed`。
2. 调用 `manage_subagents` 的 `list` 操作，确认已经没有还在运行的 subagent，超过上限的直接 `kill` 掉。只要还有 subagent 在跑，就绝不能结束本轮，除非挂着一个还没触发的计时器（见下文“等待 subagent”）。没有计时器时，本轮如果以一句文字回复收尾（比如“正在等评审者”），整次运行可能就此结束，之后才到的结果也就丢了。
3. 凡是失败、被拒或什么都没返回的 subagent，都要在报告文件里点名列出，作为覆盖缺口。
4. subagent 返回的每条支撑结论的论断，都要去 `logAbsoluteUri` 指向的 subagent 对话记录里，确认标签背后确实有对应的工具步骤。`scripts/provenance_check.py <child answer> --conversation <child id>` 可以一次核对所有标签。规则见 `02-evidence-traps.md` 的“委托得来的结论”一节。
5. 每条论断写进报告文件时，都要带上层级和作者：`read by gravitas-reader (...)`。回复本身不出现任何 agent 的名字（见 `00-orchestrator.md` 的“输出组装”一节）。

这种悄无声息的失败，在这个平台上确实会发生。2026-09-24 在 agy 1.2.9 上的一次 headless 运行中，subagent 的第一次 `read_file` 就被拒绝，什么都没产出；主 agent 却在启动 5.4 秒后就结束了，返回 `"status": "SUCCESS"`，回复是“I am waiting for its response.”。授予权限之后，同类运行等了 subagent 63 秒，并报告了 subagent 的答案。第二次提前退出跟权限拒绝无关：一次完整审计先用 `manage_subagents` 轮询了一分钟，然后以“Waiting for the Completeness Critic subagent to complete its evaluation”结束了本轮，29 秒后 CLI 就把这次运行关掉了。评审者的结果后来送到时，日志里记下的是“Failed to wake idle agent on message: run state not found”。

## 等待 subagent

`schedule` 调用后立刻返回，并不会让本轮停下来等，所以“等待”的做法是：先挂上一个计时器，再结束本轮。这个做法于 2026 年 10 月 3 日在 agy 1.2.16 上验证过，条件是 headless 运行、带 `--sandbox --dangerously-skip-permissions`，主 agent 用 Gemini 3.8 Flash，subagent 用 `Model: "pro"`。默认的 headless 设置下还没测过；默认设置会拒绝 `run_command` 和 `read_url_content`（见 `13-platform.md`），所以需要其中任何一个工具的 subagent 可能什么都不返回，这时起作用的就是计时器的 prompt。插件安装时带了 `--review` 的话，常驻规则里的“第二意见”（Second Opinion）用的就是这个做法。

1. 调用 `invoke_subagent`。
2. 调用 `schedule`：`DurationSeconds` 设为能接受的最长等待时间，设置 `TimerCondition: "any"`，再写一个 `Prompt`，说明到时什么都没等到该怎么办。
3. 用简短的一句话结束本轮，不写别的文字，也不再调用任何工具。原因是 headless 运行也会把和工具调用写在一起的文字打印出来，8 次运行里有 1 次，等待提示就这样出现了两遍。在 agy 1.2.16 上用 Gemini 3.8 Flash 时，既没有文字也没有工具调用的一轮会被拒绝，报错“model output must contain either output text or tool calls, these cannot both be empty”。headless 运行会在回复之前先打印这句等待提示，所以要写成给人看的话。
4. subagent 的完成消息会唤醒主 agent，同时取消计时器。如果计时器先触发，就按它的 prompt 去做。

subagent 没调用 `send_message` 就结束时，唤醒消息的发送者是 `system`，而不是 subagent 的会话 ID，消息里带的是 subagent 的最后一条回复。所以，绑定 subagent ID 的计时器不会被这条消息取消：这种情况跑了 7 次，240 秒的计时器每次都走满全程，主 agent 都多回复了一次，其中有一次连整封邮件都重复了一遍。subagent 自己用 `send_message` 发出的消息带着它的 ID，在 3 次运行中全都取消了绑定该 ID 的待触发计时器；这条消息之后也没有再出现 `system` 消息，4 次运行都是如此。用 `"any"` 时，8 次运行全都只回复了一次，时间在启动后 45 到 167 秒之间。

一次性计时器待触发期间，headless 运行会一直保持存活，在 stderr 上打印 `root agent idle; waiting up to 30m0s for 1 background task(s)`，直到计时器触发或被取消。主 agent 没挂计时器就结束本轮时，整次运行随之结束：它的回复从头到尾只有那句等待提示，subagent 的结果始终没有送达。

有多个 subagent 时，每条消息都会取消 `"any"` 计时器，而工具声明规定同一时间只能有一个这样的计时器，所以只要还有别的 subagent 在跑，再次结束本轮之前就要重新设一个。这种用法是按工具声明写的，还没有配合本技能测试过。

## 保持独立

评审者如果有写权限，就会去修复自己误诊的问题，然后报告成功，这次修复本身也就成了证据的一部分。正因如此，角色清单里所有负责观察和评判的角色都没有编辑工具。

把产物交给评审者时，要说成是第三方的输出，而不是“你之前的尝试”。模型审查自认为出自别人之手的工作时，找错的能力明显更强，光是换个标签就能提高检出率。验证工作绝不能交回给提出该论断的那个 agent。

除非在 agent 文件里关掉，否则自定义配置会一路传到 subagent。在 agy 1.2.9 上，`gravitas-reader` 三步就找到了答案，接着又花 35 秒加载本技能，因为插件的常驻规则要求它这么做；那次运行一共用了 63 秒。在 agent 文件里设置 `inheritCustomizations: false` 后，同样的任务用了 40 秒，也没有打开任何技能文件。插件自带的每个 agent 都设了这一项，这样还能把主 agent 的规则和它给问题定的调子挡在评审者的上下文之外。这些 agent 都没有 subagent 工具。

## 并行写入

两个写入者改同一批文件，会互相覆盖。可以按文件拆分任务，可以让写入者依次执行，也可以用 `Workspace: "branch"` 或 `Workspace: "share"` 给每个写入者一个隔离的工作区。隔离模式的说明在工具声明里，还没有配合本技能测试过。不管用哪种办法，最后都由主 agent 来合并。

## 反模式

- 评审者带编辑工具，或者核查者的范围里包含了被审查的工作。
- 由提出论断的 agent 自己来验证。
- 给每个专职 agent 都开 `enable_subagent_tools`，结果是一棵又深又慢、谁也审计不了的树。
- 任务书里没写返回格式。
- 对结论所依赖的论断，只看 subagent 的摘要，从不看它的对话记录。
- 还有 subagent 在运行（`manage_subagents` 一查就能列出来），却报告运行已经完成。
- 把 `TimerCondition` 设成 subagent 的会话 ID；`system` 发出的完成消息取消不了这种计时器。
