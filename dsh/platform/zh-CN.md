## 在 DeepSeek Harness 上使用

本技能最初为 Google Antigravity 编写。在 DeepSeek Harness（DSH）上，用法相同，只需按下表替换工具名。

| 模块里写的 | 在 DSH 上用 |
| --- | --- |
| `view_file` | `read` |
| `list_dir`、`find_by_name` | `glob` |
| `grep_search` | `grep` |
| `run_command` | Windows 上用 `pwsh`，其他系统用 `bash` |
| `read_url_content`、`search_web` | `web_fetch`、`web_search` |
| 用 `invoke_subagent` 启动 `gravitas-*` 智能体 | 用 `gravitas_inspect`，并填写 `agent_preset`（见下文） |
| `invoke_subagent` 且 `TypeName: "self"` | `subagent` 工具 |
| `define_subagent`、`Workspace: "branch"` | DSH 上没有 |
| `Model: "flash"` 或 `"pro"` | `gravitas_inspect` 默认沿用父智能体的模型；只有工具提供 `provider` 和 `model` 参数时，才另选模型 |

### 启动检查员

1. 先读所需角色的角色文件。`AGENTS_DIR` 下有：`gravitas-scout.md`、`gravitas-reader.md`、`gravitas-finder.md`、`gravitas-checker.md`、`gravitas-refuter.md`、`gravitas-visual-critic.md`、`gravitas-completeness-critic.md` 和 `gravitas-prose-editor.md`。
2. 调用 `gravitas_inspect`，填写三项：
   - `description`：三到五个词的任务简述；
   - `prompt`：先放角色文件头部之后的正文，再写任务本身（要核实的说法、相关文件、要回答的问题）；
   - `agent_preset`：
     - `gravitas-checker` 只用于核验员（checker）。它可以运行命令；和 Antigravity 上一样，它"不改动被审查的工作"是一条职责规定，而不是工具层面的限制。
     - 其他角色一律用 `gravitas-inspector`。它能读文件、搜索工作区、上网查资料，没有任何写入或修改文件的工具。
3. 调用会立即返回检查员的编号，结果稍后以"完成通知"送达。彼此独立的检查员应同时启动，等收齐通知后再下判断。

视觉评审员用 `read_image` 看图，只有当前模型路由支持图像输入时才能用。如果路由只支持文本，就说明"视觉检查未执行"。

### 与 Antigravity 的不同

- 模块 `13-platform.md` 讲的是 Antigravity 的版本和限制。在 DSH 上，只取其中的通用经验。
- 模块 `15-harness-probing.md` 照常适用：凡是要依赖的 DSH 行为，先探测、后信任。
- 检查员会继承父智能体的技能和全局规则（包括本规则），但首先遵守自己的角色文件。
