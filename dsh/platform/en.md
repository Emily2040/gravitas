## On DeepSeek Harness

This skill was written for Google Antigravity. On DeepSeek Harness (DSH) it works the same way, with these substitutions.

| In the modules | On DSH |
| --- | --- |
| `view_file` | `read` |
| `list_dir`, `find_by_name` | `glob` |
| `grep_search` | `grep` |
| `run_command` | `pwsh` on Windows, `bash` elsewhere |
| `read_url_content`, `search_web` | `web_fetch`, `web_search` |
| `invoke_subagent` with a `gravitas-*` agent | `gravitas_inspect` with `agent_preset` (below) |
| `invoke_subagent` with `TypeName: "self"` | the `subagent` tool |
| `define_subagent`, `Workspace: "branch"` | not available |
| `Model: "flash"` or `"pro"` | `gravitas_inspect` takes the parent's model; choose another only if the tool offers `provider` and `model` |

### Starting an inspector

1. Read the role file for the role you need: `AGENTS_DIR` holds `gravitas-scout.md`, `gravitas-reader.md`, `gravitas-finder.md`, `gravitas-checker.md`, `gravitas-refuter.md`, `gravitas-visual-critic.md`, `gravitas-completeness-critic.md` and `gravitas-prose-editor.md`.
2. Call `gravitas_inspect` with `description` (3 to 5 words), `prompt` (the role file's text after its header, then the task: the claim, the files, the questions) and `agent_preset`:
   - `gravitas-checker` for the checker. It can run shell commands; like the Antigravity checker, its read-only status is a charter rule, not a tool restriction.
   - `gravitas-inspector` for every other role. It can read, search the workspace and use the web, and has no tool that writes or edits files.
3. The call returns at once with the inspector's id; its answer arrives later as a completion notice. Start independent inspectors together, then wait for their notices before you judge.

The visual critic reads images with `read_image`, which works only on a model route that accepts image input. On a text-only route, state that the visual check was not run.

### What differs from Antigravity

- Module `13-platform.md` describes Antigravity's versions and limits. On DSH, read it for its general lessons only.
- Module `15-harness-probing.md` applies as written: probe any DSH behaviour you rely on before trusting it.
- Inspectors inherit the parent's skills and global rules, including this one. They follow their role file first.
