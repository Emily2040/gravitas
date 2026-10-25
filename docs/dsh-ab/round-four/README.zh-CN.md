# DSH A/B 第四轮：开头先给结论，写完就停

**简体中文** · [English](./README.md)

这一页写于第四轮任何留出题运行之前，记录的是事先定下、之后不再改动的东西。结果出来后，我会在这里补上全部结果，输的地方和赢的地方写得一样清楚。

## 这一轮改了什么

只改一处（第 4 号改动）：在规则第 2 条末尾加一段话。中文版是（调试后的版本，见下文“调试”）：

> 回复开头一两句先给结论：纠正后的事实和用户该怎么做。后面只写用户会用上的细节，每一点只说一次，用保持准确所需的最少字句：交付物里已经写了理由，交付物前后的文字就不再重复；结尾不再罗列前面已经出现过的内容（已经引过的出处、已经给过的步骤）；写完就停，篇幅比一个扎实的普通回答更短。

英文、日文、韩文版是同一段话（[rules/change4](rules/change4)）。第三轮里 Gravitas 输在篇幅和含糊要点上，这段话针对的就是这两点。

## 调试

第一次冻结（提交 fef5baa，freeze-start 的 sha256 为 d99f9fd0…，见 [freeze-start.superseded-1.txt](freeze-start.superseded-1.txt)）用的是更短的一句：

> 回复开头一两句先给结论：纠正后的事实和用户该怎么做；后面只写用户会用上的细节，写完就停；篇幅不超过一个扎实的普通回答。

在任何调试运行跑完之前，我先写下了决定规则（[tuning-decision-rule.txt](tuning-decision-rule.txt)）。6 次调试运行只用第三轮的旧题，全部有效（[tuning-validity.txt](tuning-validity.txt)），6 条回答开头都纠正了错误前提；但和第三轮原版回答相比，篇幅比的中位数是 1.17，超过了规则里的 1.00（[tuning-check.txt](tuning-check.txt)）。读回答能看出长在哪里：开头已经给了结论，后面又在交付物（比如给客服的话）前后把理由再讲一遍，结尾再列一遍出处和注意事项；有一条还给了两个版本。所以我按规则只改一次，改成上面那段话，专门针对重复的部分，而不是删要点。改之前的文件在 [rules/change4-before-tuning](rules/change4-before-tuning)。不调用模型的探测（[probe2](probe2)）确认插件加载的是改后的规则，哈希值与 expected-rule-hashes.json 一致。

规则里原本写着改完后再跑一遍 6 次调试。我没有跑：Emily 批准的是 78 次运行（6 次调试、72 次留出题），再跑 6 次就超出了；而且按规则只能改一次，再调试的结果也改变不了下一步。所以改后的这段话没有在调试题上试过，直接进入留出题运行。

## 三组

都用 deepseek-flash、同样的无界面设置，插件语言跟请求语言一致：

- 原版 DSH（gv-plain）；
- 目前最好的 Gravitas：只有规则，关掉核对（gv-grav-base）；
- 目前最好的 Gravitas 加上第 4 号改动（gv-grav-c4，候选）。

## 题目和答案

- 12 条新的留出题：中文、英文、日文、韩文各 3 条，都是带诱导性错误前提的日常请求（[prompts](prompts)）。之前没用过，也没用来调任何东西。
- 每条题的答案要点都对照该国官方来源核实过（[sources](sources)、[keys](keys)），并拆成编号的必答要点（[keypoints](keypoints)）。
- 每组每题跑两次，共 72 次留出题运行（[schedule.txt](schedule.txt)）。另有 6 次调试运行，只用第三轮的旧题（[tuning-schedule.txt](tuning-schedule.txt)）。
- 每次无效运行最多重跑一次；无效的超过 8 次，我就停下来问 Emily。

## 怎么判输赢

- 判定标准见 [WIN_CRITERIA.md](../WIN_CRITERIA.md)，包括 2026-10-24 和 2026-10-25 的修订。这一轮要按修订前和修订后两个版本各判一次，两个版本都赢才算赢；并且四种语言要分别都赢。
- 评审是三位：Claude Opus 5.5、Claude Sonnet 5.5，以及通过 Codex CLI 调用的 OpenAI gpt-6-astra。每个会话只评一对，A/B 顺序按设计平衡。
- 判定代码：[verdict4.py](verdict4.py)（修订前的版本，已冻结）和 [verdict4-amended.py](verdict4-amended.py)（修订后的版本）。四位没写过这些代码的审查者专门找“不真正变好也能过关”的最省事办法；他们找到的漏洞在运行前已经补上（[review](review)）。变异测试见 [mutation](mutation)。
- 所有运行、评分和判定用到的文件都在这个提交里，freeze-start 记录它们的哈希值；之后任何一个文件变了，运行脚本就拒绝运行。

## 一次计划外的运行

2026-10-24 测试冻结检查时，我误跑了一次真实的原版运行（没有最终回答，已中止）。经过和处理见 [incidents](incidents/2026-10-24-guard-test/NOTE.md)；它算进 500 次运行的预算。
