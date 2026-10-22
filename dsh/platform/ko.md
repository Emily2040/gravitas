## DeepSeek Harness에서 쓸 때

이 스킬은 Google Antigravity용으로 쓰였습니다. DeepSeek Harness(DSH)에서도 쓰는 방법은 같고, 도구 이름만 아래 표대로 바꿔 읽으면 됩니다.

| 모듈에 적힌 이름 | DSH에서의 이름 |
| --- | --- |
| `view_file` | `read` |
| `list_dir`, `find_by_name` | `glob` |
| `grep_search` | `grep` |
| `run_command` | Windows에서는 `pwsh`, 그 밖에서는 `bash` |
| `read_url_content`, `search_web` | `web_fetch`, `web_search` |
| `invoke_subagent`로 `gravitas-*` 에이전트 실행 | `gravitas_inspect`에 `agent_preset` 지정(아래 참고) |
| `invoke_subagent`의 `TypeName: "self"` | `subagent` 도구 |
| `define_subagent`, `Workspace: "branch"` | DSH에는 없음 |
| `Model: "flash"` 또는 `"pro"` | `gravitas_inspect`는 부모 에이전트의 모델을 씁니다. 도구가 `provider`와 `model`을 받을 때만 다른 모델을 고르세요 |

### 검사 에이전트 실행

1. 필요한 역할의 역할 파일을 읽습니다. `AGENTS_DIR`에 `gravitas-scout.md`, `gravitas-reader.md`, `gravitas-finder.md`, `gravitas-checker.md`, `gravitas-refuter.md`, `gravitas-visual-critic.md`, `gravitas-completeness-critic.md`, `gravitas-prose-editor.md`가 있습니다.
2. `gravitas_inspect`를 호출하고 세 가지를 넘깁니다.
   - `description`: 3~5단어의 짧은 설명
   - `prompt`: 역할 파일의 헤더 다음 본문, 이어서 작업 내용(확인할 주장, 관련 파일, 답할 질문)
   - `agent_preset`:
     - `gravitas-checker`는 체커 전용입니다. 명령을 실행할 수 있습니다. Antigravity와 마찬가지로, 검토 대상을 바꾸지 않는 것은 도구 제한이 아니라 역할 규칙입니다.
     - 나머지 역할은 모두 `gravitas-inspector`입니다. 파일 읽기, 워크스페이스 검색, 웹 사용은 되지만 파일을 쓰거나 고치는 도구는 없습니다.
3. 호출은 곧바로 검사 에이전트의 ID를 돌려주고, 결과는 나중에 완료 알림으로 옵니다. 서로 독립된 검사는 한꺼번에 시작하고, 알림을 모두 받은 뒤에 판단합니다.

시각 비평 역할은 `read_image`로 이미지를 읽는데, 이미지 입력을 받는 모델 경로에서만 됩니다. 텍스트 전용 경로라면 시각 검사를 하지 않았다고 밝히세요.

### Antigravity와 다른 점

- 모듈 `13-platform.md`는 Antigravity의 버전과 한계를 다룹니다. DSH에서는 일반적인 교훈만 참고하세요.
- 모듈 `15-harness-probing.md`는 그대로 적용됩니다. 기대는 DSH 동작은 믿기 전에 먼저 확인합니다.
- 검사 에이전트에게는 상시 규칙이 전달되지만 스킬은 불러올 수 없습니다. Gravitas 프리셋 두 개 모두 스킬 도구가 없기 때문입니다. 검사 에이전트에게 필요한 모듈 지침은 역할 파일 다음에 이어서 `prompt`에 넣습니다. 검사 에이전트는 먼저 자기 역할 파일을 따릅니다.
- `scripts/provenance_check.py`는 Antigravity 대화 기록만 읽을 수 있고, DSH에서는 검사 에이전트의 도구 단계를 볼 방법도 없습니다. `gravitas_inspect`는 검사 에이전트의 id만 돌려주고, 완료 알림에는 그 답만 들어 있습니다. 그래서 `01-evidence.md`, `02-evidence-traps.md`, `08-delegation.md`의 출처 확인은 DSH에서 손으로 합니다. 자기 답의 각 라벨은 자기가 실제로 한 도구 호출과 하나씩 대조합니다. 검사 에이전트의 핵심 주장에 기대기 전에 그 출처를 직접 열거나 그 명령을 직접 실행합니다. 직접 다시 확인하지 않은 주장은 라벨이 무엇이든 `inferred`입니다.
- 헤드리스 실행(`dsh-headless` 번들)에는 agent-presets 서비스가 없어서 이 규칙과 스킬만 로드되고 `gravitas_inspect`는 없습니다. 이때는 `subagent` 도구로 검사 에이전트를 시작하고, 역할 파일 본문을 작업 내용 앞에 둡니다. 이 도구는 파일을 쓸 수 있으므로, 읽기 전용은 도구 제한이 아니라 역할 규칙입니다.
