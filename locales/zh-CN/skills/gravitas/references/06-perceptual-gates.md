# 模块 06 - 感知关卡

## 用途

本模块说明只有观看者才能回答的核查，适用于任何会被人看到的东西：场景、页面、图表、生成的图像、排版后的文档。只要工作有视觉结果，就与 `05-acceptance.md` 一起加载。它所依据的案例就是那里描述的巧克力工厂。

## 截图不等于验证

那次巧克力工厂运行在报告里附了 8 张 PNG。它们所支撑的每一个关卡测量的都是几何：UUID 是否保持、网格数量、夹爪在 `Y = 1.084 m` 处的间隙、循环边界误差小于 0.1 mm。这些全都属实，场景看起来却仍然不对。没有任何环节去问图像看起来对不对。截图被当作“脚本运行过”的证明归档，而不是作为需要评判的图像。

这种失败很诱人，因为它能产出一份满是数字和通过项的文档，感觉比“去看”更严谨。但它回答的是另一个问题。

| | 几何核查 | 感知核查 |
| :--- | :--- | :--- |
| 问题 | 元素是否存在、位置和尺寸是否正确 | 看起来对不对 |
| 方法 | 对场景图或 DOM 做脚本断言 | 由模型看图并作出判断 |
| 能发现 | 缺失节点、错误变换、数量漂移 | 平淡的光照、塑料感材质、难以辨认的造型 |
| 发现不了 | 任何关于外观的问题 | 任何关于精确数值的问题 |

感知核查无法写成脚本。它需要把图像摆在一位新的评审者面前，并问一个关于“读起来像什么”的问题。

## 感知关卡

对任何会被人看到的东西，加上只有观看者才能回答的关卡。把截图和意图交给 `gravitas-visual-critic`，并要求具体的回答。

“这看起来好吗”只会引来附和。下面这些问题的答案才可能是错的：

- 说出每个主要表面看起来是什么材质。简报写的是铜、搪瓷钢和黄铜。你看到的是什么？
- 指出巧克力在哪里。如果在这张图里找不到，就直说。
- 是否有可见的光照方向？说出它。如果光照看起来平淡，就说“平淡”。
- 列出每一个没有纹理、磨损或变化的表面。
- 从未读过简报的人会认出这是一座巧克力工厂吗？他们看到的是什么？

评审者以观看者的身份回答，不读源代码，因为读过代码的评审者描述的是意图，而不是图像。最有用的一个问题是“这看起来是用什么做的”。一个由平面着色基本体构成的场景，无论材质配置怎么写，得到的回答都会是“塑料积木”。

## 在构建之前说出目标

那次运行的计划写得很具体：`#941c33` 覆盆子色搪瓷，粗糙度 0.20，清漆 0.85，3500 K 卤素主光强度 2.8，程序化瓷砖填缝。这些都是真正的验收标准，却没有一条变成关卡。计划描述的是外观，测试集测量的却是位置。

计划中的每一条材质和光照规格，都是一个等着被写出来的感知关卡。如果计划写了清漆 0.85，关卡就问表面看起来是否上了漆。如果计划指定了某个位置的 3500 K 主光，关卡就问观看者能否说出光的方向和冷暖。

## 控制台输出也是关卡

同一个场景请求了在 r186 中已被移除的 `THREE.PCFSoftShadowMap`。渲染器退回到硬阴影，并在控制台里说明了这一点：

```text
THREE.WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead.
```

没有任何东西失败或崩溃。阴影并不是计划要求的样子，而这次运行明明接好了控制台采集，却没人去读。弃用警告是最廉价的缺陷信号。一条点名了代码所调用 API 的警告，在有人排查之前都算失败。

## 一个会变红的实例

`examples/gates.example.js` 是按这些规则编写、并针对上述场景运行的 Playwright 关卡测试集。它得 6 分中的 4 分，并以 1 退出。

```text
PASS  G1  Zero console errors
FAIL  G2  No deprecation warning for an API this code calls
          THREE.WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead.
FAIL  G3  Shadow map enabled and not the hard fallback (type !== 1)
          enabled=true type=1
PASS  G4  Under 90% of materials are untextured
          153/193 materials have no map (79.3%)
PASS  G5  Component counts match the brief
PASS  G6  SELF-TEST: an injected wrong value is detected by G5 logic
```

G6 是规则所要求的自检：它注入一个错误值，并确认比较逻辑能抓住它，因此这套测试已经证明自己能变红。在原来的测试集下，同一个场景报告的是 `ALL TEST GATES PASSED SUCCESSFULLY`。

随后，感知关卡由一个只拿到截图、没有源代码的新代理单独运行（以下为原文引用）：

> **Chocolate: Absent.** The mold cavities are completely white and empty; there is no liquid chocolate, bar, or brown confectionery substance visible anywhere on the line.
>
> **Lighting: Flat.** No directional cast shadows, no specular hot spots.
>
> **What it looks like it is made of:** injection-molded matte toy plastic and raw CAD primitives.

原测试集对同一物体的关卡写的是：“Hero Chocolate Identity Persistence - PASS. Exactly 1 mesh throughout; UUID persists across all phases.” 这个网格存在于场景图中，却在渲染结果里看不见。任何几何关卡都无法弥合这个差距，这正是感知关卡存在的原因。
