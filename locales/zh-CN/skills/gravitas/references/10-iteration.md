# 模块 10：迭代

## 用途

同一件事再做一轮，有时能把结果改好，有时反而改坏。本模块讲清楚这两种情况分别在什么时候出现，以及怎么判断自己正处在哪一种循环里。开始任何纠错或打磨循环之前，先加载本模块。

## 不对称

“一直改，改到完美为止”是最符合直觉的 agent 循环，偏偏也是最靠不住的一种。

Huang 等人（ICLR 2024）把内在自我纠错（intrinsic self-correction）定义为：模型只靠自身能力、不借助外部反馈来修改自己的答案（原文：“based solely on its inherent capabilities, without the crutch of external feedback”）。他们发现，没有外部反馈时，模型很难纠正自己的回答，有时纠正之后表现反而下降（原文：“struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction”）。

比结论更要紧的是背后的机制。只要告诉模型错在哪里，它通常能修好；但让它自己去找错在哪，就靠不住了，因为犯错的是这套推理，被要求去抓错的还是这套推理。所以循环失败，不是因为轮数跑得不够，而是因为每一轮都拿不到新东西。

后续一项研究把这一点说得更透：模型在别的 agent 的输出里找错，明显比在自己的输出里找得好；而且只要把同一份工作说成是别处来的，单凭这一点，检出率就会上升。是否独立，会改变能抓到哪些错误。本插件里的评审者看到的工作，从来不会被说成是它自己做的，原因就在这里。

## 收敛型循环

有标准答案的时候，用收敛型循环：正确性、bug、构建失败、行为异常、必须对得上的数字。

每一轮都必须拿到一个新的外部信号作为输入，而且这个信号必须指出错在哪里。下面这些算有效信号：

- 失败的测试，附断言和调用栈；
- 编译错误或类型错误，附文件和行号；
- 控制台里的运行时异常；
- 两张截图之间的视觉差异；
- 与预期契约对不上的网络响应；
- 命令的退出码，以及它的 stderr；
- 两种独立方法算出来的数值不一致；
- 与结论相矛盾的来源，并附原文引用。

如果某一轮没有产生新信号，就停。让模型把自己的东西再读一遍，正是文献里记录的那种退化情形。

Reflexion 能在朴素自我批评失效的地方起作用，道理也在这里：它反思的是存放在情景记忆缓冲区（episodic memory buffer）里的任务反馈，而不是印象。论文报告，Reflexion 在 HumanEval 上的 pass@1 为 91%，GPT-4 基线为 80%；它最好的成绩出自由执行结果提供信号的场景。

信号不再报错了，或者某一轮没有产生新信号，就停下来，并报告还有哪些没通过。

## 梯度型循环

没有对错、只有好坏的时候，用梯度型循环：文字、命名、API 好不好用、布局、代码清晰度。自我打磨在这里管用，因为本来就没有一个唯一正确的目标可以偏离，Self-Refine 正是为这类场景设计的。

实测出来的曲线形状很一致：收益大头在前一两轮；到第三、四轮左右，质量基本饱和；超过大约三轮，收益走平，甚至可能倒退。有一份报告给出的轨迹是：第一次纠正后从约 62% 升到 70%，第三轮约 75%，到第五轮在 79% 附近饱和。

默认跑 3 轮，绝不超过 5 轮。如果连续两轮都只是表面改动，就停，因为循环已经开始来回倒腾了。

## 绝不该循环的情况

有些判断根本拿不到外部信号：架构对不对；某条路径没法实际跑起来的时候，系统安不安全。在这类问题上反复迭代，只会得到越来越笃定的文字，准确度一点也不会提高。找一个独立意见，标成假设并注明层级，然后继续往下走。

## 怎样的循环才算数

开始纠错循环之前，先回答下面几个问题。答不上来，你手里的就只是一次重写。

1. 外部信号是什么？把那个产物点出来：这个失败的测试、这条控制台报错、这一对截图。“我再审一遍”不算信号。
2. 信号能定位错误吗？如果它只说有问题、不说在哪，先插桩再迭代：一行日志、一个范围更小的测试、一个断言。这比再盲跑一轮便宜。
3. 谁来评判？不能是产出这份工作的 agent。要从角色清单里找一个只读评审者，把产物当作第三方的输出交给它。
4. 停止条件是什么？是信号不再报错、没有新信号，还是到了轮数上限，开始之前就要定好。
5. 失败了怎么办？报告哪些还没通过、为什么没通过。悄悄放弃目标就退出的循环，比根本没跑过还糟。

## 由 hook 驱动的循环

Antigravity 可以从外部把 agent 按在循环里。`PostInvocation` hook 可以返回 `terminationBehavior: "force_continue"` 或 `"terminate"`；`Stop` hook 会收到 `executionNum`、`terminationReason` 和 `fullyIdle`，可以返回 `decision: "continue"`，并带上一个 `reason`，这个 `reason` 会作为系统消息注入（read: 内置的 `agy-customizations` 指南，`docs/hooks.md`，桌面版 2.17.0）。

`force_continue` 在平台层面没有上限。三次实测分别续跑了 3、8、12 次，其中 12 是测试自己设的上限；被强制续出来的轮次全是空转，因为任务早就完成了。这个问题已在 `google-antigravity/antigravity-cli` 提为 issue #1055。凡是在测试还没变绿时阻止终止的 hook，都必须自带计数器（按 `executionNum` 或 `invocationNum` 计）和一个硬上限。带防御逻辑的 hook 如果捕获异常后输出一个默认响应，而这个默认响应是“继续”，它就会变成死循环。

## 反模式

- 没有停止条件、没有外部信号，一味“迭代到完美”。
- 让 agent 审查“你之前的输出”，而不是把同一段文本当作别人写的交给它。
- 没有新信息还在循环，第 N+1 轮看到的和第 N 轮一样。
- 把意见一致当成验证。几个 agent 在无法验证的推理上达成一致，是彼此相关、并不独立的推断（correlated inference），不能提升层级。
- 把两种循环搞混。拿梯度型迭代去对付正确性 bug，只会把 bug 埋在更漂亮的文字底下。
- 阻止终止却不设上限。

## 来源

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine: Iterative Refinement with Self-Feedback*. https://dl.acm.org/doi/10.5555/3666122.3668141
