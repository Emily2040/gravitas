# DSH A/B 第四轮：开头先给结论，写完就停

**简体中文** · [English](./README.md)

这一页写于第四轮任何留出题运行之前，记录的是事先定下、之后不再改动的东西。结果出来后，我会在这里补上全部结果，输的地方和赢的地方写得一样清楚。

## 这一轮改了什么

只改一处（第 4 号改动）：在规则第 2 条末尾加一句。中文版是：

> 回复开头一两句先给结论：纠正后的事实和用户该怎么做；后面只写用户会用上的细节，写完就停；篇幅不超过一个扎实的普通回答。

英文、日文、韩文版是同一句话（[rules/change4](rules/change4)）。第三轮里 Gravitas 输在篇幅和含糊要点上，这句话针对的就是这两点。

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
