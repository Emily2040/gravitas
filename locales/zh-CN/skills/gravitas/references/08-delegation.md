# 模块 08 - 委托

## 用途

本模块说明如何给子代理布置任务，使其结果可以被核查，以及在它的结论进入报告之前，如何确认它实际做了什么。与 `07-subagents.md` 一起加载。

## 职责约定

一份产出无法使用结果的职责说明，既耗费 token，又得到一个需要重做的东西。每个 `Prompt` 都要写明六件事。

1. 范围：纳入范围的文件、结论、路由或来源，用绝对路径或完整 URL 写明，此外一概不包括。范围重叠会产生重复，范围之间的空隙会造成无声的遗漏。
2. 问题：一个问题，窄到答案可以被核查。
3. 返回形式：符合 `schemas/finding.schema.json` 的发现记录，或一个符合 `schemas/verdict.schema.json` 的裁决。只被告知要找什么的代理，会写出一篇文章。
4. 证据：每个结论在同一字段里带有层级和来源，第 4 层的内容都标为假设。
5. 停止条件：范围覆盖完毕时，或达到指定数量后。
6. 受阻时的做法：如果工具被拒绝或文件缺失，就以 `blocked` 状态返回已有的内容和错误文本。禁止绕过拒绝，平台自己的拒绝消息也这么说。

子代理只返回结果，不叙述进展。

永远不要给子代理相对路径。2026-09-24 在 agy 1.2.9 上，`view_file` 把相对路径解析到了 `~/.gemini/antigravity-cli/scratch/`，一个所有 CLI 会话共用的文件夹，而不是工作区。被要求编辑“当前工作区中”的 `draft.md` 的 `gravitas-prose-editor`，编辑的是五天前一次测试留在那个文件夹里的另一个 `draft.md`，并且没有报任何错就返回了修改结果。`gravitas-refuter` 和 `gravitas-visual-critic` 也落到了同一个文件夹，什么也没找到，返回了 `blocked`，这是更好的失败方式。

告诉每个子代理：它的提示词和指令包含了它需要的一切。在审计测试中，一个被告知输出必须符合“Gravitas finding schema”的搜寻者，把它 127 步中的大部分花在了到用户文件夹里找这个文件上，一路读了 git 内部文件和无关的测试输出。现在附带的代理都把完整的 schema 作为示例带在身上，并被告知没有什么需要去找。在重跑中，每个搜寻者和反驳者都在 4 到 8 步内完成，没有打开范围之外的任何东西。

证明路径穿越、注入或数据泄露的核查者，要以它在临时文件夹中创建的无害诱饵文件为目标。在同一次测试中，核查者通过有缺陷的函数读取 `C:\Windows\win.ini` 来证明路径穿越：在那里无害，但在一台存有真实机密的机器上，这是错误的习惯。

```text
Role: Refuter, session handling
Territory: the claim below and C:/work/app/src/auth/session.ts. Nothing else.
Claim: "logout() leaves the refresh token valid" (C:/work/app/src/auth/session.ts:88-120)
Question: can you show this claim is false?
Return: one JSON object matching schemas/verdict.schema.json.
Evidence: every statement carries its tier and source, e.g. read (src/auth/session.ts:97, "...").
Stop: after one verdict.
If a tool is denied, return status "blocked" with the error text.
```

## 委托的完整性

父代理自身的状态说明不了它的子代理，所以在综合之前逐一检查每个子代理。

1. 在台账中记录每个子代理的会话 ID 和最终状态：`done`、`failed`、`denied`、`empty` 或 `killed`。
2. 用 `list` 调用 `manage_subagents`，确认没有子代理仍在运行，并 `kill` 超过上限的子代理。在无头运行中，要一直进行工具调用，直到所有子代理完成：一轮以“正在等待评审者”之类的文字回复结束，可能会结束整次运行，之后才到的结果就丢失了。
3. 把每一个失败、被拒绝或什么也没返回的子代理，按名字作为覆盖缺口报告出来。
4. 对子代理返回的每个承重结论，在 `logAbsoluteUri` 处的子代理转录记录中确认标签背后的工具步骤。`scripts/provenance_check.py <child answer> --conversation <child id>` 可以一次性对所有标签做这件事。规则见 `02-evidence-traps.md` 中的“委托出去的结论”。
5. 把每个结论连同其层级和作者带进报告：`read by gravitas-reader (...)`。

这种无声的失败在这个平台上是真实存在的。2026-09-24 在 agy 1.2.9 上的一次无头运行中，一个子代理的第一次 `read_file` 被拒绝，什么也没产出，而父代理在启动 5.4 秒后结束，返回 `"status": "SUCCESS"` 和 “I am waiting for its response.”。授予权限后，同类运行为它的子代理等待了 63 秒，并报告了子代理的答案。第二次提前退出与拒绝无关：一次完整审计用 `manage_subagents` 轮询了一分钟，然后以 “Waiting for the Completeness Critic subagent to complete its evaluation” 结束了这一轮，29 秒后 CLI 关闭了这次运行。评审者的结果到达时，日志里记录的是 “Failed to wake idle agent on message: run state not found”。

## 独立性

一个能写入的评审者，会修复它误诊的东西，报告成功，而这次修复就成了证据的一部分。名单中每一个观察和评判角色都没有编辑工具，原因就在于此。

把产物作为第三方输出交给评审者，而不是说成“你之前的尝试”。模型在它们认为出自别人之手的工作中发现错误的能力明显更强，仅仅重新标注就能提高发现率。永远不要把验证交回给产出该结论的代理。

除非代理文件关闭，否则自定义项会传到子代理。在 agy 1.2.9 上，`gravitas-reader` 三步就找到了答案，随后又花了 35 秒加载本技能，因为插件的常驻规则要求它这样做；那次运行用了 63 秒。在代理文件中设置 `inheritCustomizations: false` 后，同样的任务用了 40 秒，没有打开任何技能文件。每个附带的代理都设置了它，这也把父代理的规则和框架挡在了评审者的上下文之外。它们都没有子代理工具。

## 并行写入者

两个写入者写同一批文件会互相覆盖。按文件划分工作，让写入者依次进行，或者用 `Workspace: "branch"` 或 `Workspace: "share"` 给每个写入者一个隔离的工作区。隔离模式在工具声明中有描述，尚未与本技能一起测试。无论哪种方式，都由父代理来合并。

## 反模式

- 带编辑工具的评审者，或范围包含被审工作的核查者。
- 由产出结论的代理来验证。
- 给每个专职代理都开 `enable_subagent_tools`，结果是一棵又深又慢、没人能审计的树。
- 没有返回形式的职责说明。
- 对结论所依赖的主张，只读子代理的摘要而从不读它的转录记录。
- 在 `manage_subagents` 本会列出仍在运行的子代理时，就报告运行已完成。
