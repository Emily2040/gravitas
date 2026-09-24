# 모듈 07 - 서브에이전트

## 목적

이 모듈은 전문 에이전트를 얻는 방법, 2026년 9월 기준 서브에이전트 도구가 받는 매개변수, 이 플러그인에 포함된 에이전트, 그리고 역할마다 쓰는 모델을 다룹니다. 처음 `invoke_subagent`나 `define_subagent`를 호출하기 전에 `08-delegation.md`와 함께 불러옵니다.

## 전문 에이전트를 얻는 세 가지 방법

| 경로 | 방법 | 쓰기 권한 | 용도 |
| :--- | :--- | :--- | :--- |
| 포함된 에이전트 | `TypeName`을 `gravitas-*` 에이전트로 정해 `invoke_subagent` | 에이전트 파일의 `tools` 목록으로 고정 | 모든 관찰, 판단, 비평 역할 |
| 즉석 정의 | `define_subagent` 후 새 이름으로 `invoke_subagent` | `enable_write_tools`가 true 또는 false | 이 플러그인에 없는 전문 에이전트 |
| 내장 `self` | `TypeName: "self"`로 `invoke_subagent` | 부모와 같은 도구 | 사용자가 고른 모델과 도구를 따라야 하는 구현. agy 1.2.9에서 모델이 목록에 올렸으며 이 스킬과는 아직 시험하지 않음 |

써서는 안 되는 역할에는 포함된 에이전트를 우선합니다. 읽기 전용이라는 성질은 파일의 도구 목록에서 오므로, 서브에이전트가 지시를 따르는지와 무관합니다.

## 도구 선언

2026-09-24 agy 1.2.9에서 모델 자신이 받은 도구 선언을 읽어 내고, 데스크톱 2.17.0의 `language_server.exe` 문자열과 대조한 것입니다. 이 스킬의 이전 버전은 선언에 없는 필드를 적었으므로, 업데이트 뒤에는 다시 확인하십시오.

| 도구 | 매개변수 |
| :--- | :--- |
| `invoke_subagent` | `Subagents`: 배열. 각 항목은 필수인 `TypeName`, `Role`(2~5단어 직함), `Prompt`와 함께 `Model`(`inherit`, `flash_lite`, `flash`, `pro`, 기본값 `inherit`), `Workspace`(`inherit`, `branch`, `share`, 기본값 `inherit`)를 받습니다 |
| `define_subagent` | `name`, `description`, `system_prompt`, `enable_write_tools`(파일 편집과 명령), `enable_mcp_tools`, `enable_subagent_tools` |
| `manage_subagents` | `Action`: `list`, `kill`, `kill_all`. `kill`에는 `ConversationIds`를 붙입니다 |
| `send_message` | `Recipient`(서브에이전트 대화 ID)와 `Message` |

동시 실행은 하나의 `Subagents` 배열에 여러 항목을 넣어서 얻습니다. 시작된 서브에이전트마다 고유한 대화 ID와 그 트랜스크립트를 가리키는 `logAbsoluteUri`가 생기고, 끝나면 메시지를 돌려보냅니다. 대화형 세션에서는 폴링할 필요가 없고, 헤드리스 실행에서는 모든 하위 에이전트가 끝날 때까지 도구 호출을 계속합니다(`08-delegation.md`).

`invoke_subagent` 선언은 사용자가 다른 모델을 요청하지 않는 한 `Model`을 `inherit`로 두라고 모델에 지시합니다. 이 플러그인을 설치하는 것이 아래 라우팅 표의 역할들에 대한 바로 그 요청입니다.

## 사용자 지정 에이전트 파일

사용자 지정 에이전트는 YAML 프런트매터가 있는 Markdown 파일입니다. 프런트매터가 에이전트를 설정하고 본문은 시스템 프롬프트가 됩니다.

```markdown
---
name: "gravitas-refuter"
description: "Attempts to refute one specific claim. Defaults to refuted when uncertain."
tools:
  - view_file
  - grep_search
  - read_url_content
  - search_web
model: "pro"
mainAgent: false
subagent: true
inheritCustomizations: false
inheritMcp: false
---

You are a refuter. ...
```

| 키 | 의미 |
| :--- | :--- |
| `name`, `description` | 정체, 그리고 부모가 서브에이전트를 고를 때 읽는 글 |
| `tools` | 에이전트가 부를 수 있는 도구. 나머지는 없음 |
| `model` | `inherit`, `flash`, `pro` |
| `mainAgent`, `subagent` | 메인 에이전트로 고를 수 있는지, `invoke_subagent`로 시작할 수 있는지 |
| `commandExecutionPolicy` | 셸 정책: `off`, `auto`, `eager`, `sandbox` |
| `skills`, `plugins`, `mcpServers`, `rules`, `hooks`, `agents` | 이 에이전트에 붙이는 사용자 지정 항목 |
| `inheritCustomizations`, `inheritMcp` | 사용자의 스킬, 규칙, 플러그인을 물려받는지, 사용자의 MCP 서버를 받는지 |
| `excludeDefaultComponents` | 기본 프롬프트 부분과 도구를 뺀다고 문서화되어 있지만, agy 1.2.9에서는 더 빼는 것이 없었음(open issue #1015) |

키 이름은 데스크톱 2.17.0의 `language_server.exe`에서 YAML 태그로 확인했고, 의미는 사용자 지정 서브에이전트 문서에서 가져왔습니다. `inheritMcp`는 문서에 없으며 여기서 시험했습니다. 바이너리에는 `enabledTools`, `disabledTools`, `hidden`, `background`도 있지만 시험하지 않았고 쓰지 않습니다.

`tools` 목록이 도구 세트의 전부는 아닙니다. agy 1.2.9에서 `view_file`만 나열하고 `inheritCustomizations: false`로 둔 에이전트도, 자기 선언에 대한 스스로의 설명에 따르면 `send_message`, `call_mcp_tool`, `list_resources`, `read_resource`, `manage_task`를 가지고 있었습니다. `call_mcp_tool`은 연결된 모든 MCP 서버에 닿으므로, 비평가가 읽기 전용인 것은 그 서버들이 모두 읽기 전용일 때뿐입니다. `inheritMcp: false`를 더하자 `call_mcp_tool`이 사라졌고, 거기에 `excludeDefaultComponents: true`를 더해도 달라진 것이 없었습니다. 포함된 모든 에이전트는 두 상속 플래그를 모두 false로 둡니다.

사용자 지정 에이전트는 `~/.gemini/config/agents/`와 플러그인 안의 `agents/`에서 발견됩니다. 2026-09-24 agy 1.2.9에서 `agy agents`는 전역 에이전트는 보여 주었지만 플러그인 안의 것은 보여 주지 않았고, 모델은 둘 다 보고 이름을 댈 수 있었습니다. 워크스페이스 `.agents/agents/`의 에이전트는 CLI가 전혀 발견하지 못했습니다.

주의할 점이 두 가지 있습니다. 문서는 `tools`에 매핑되지 않았거나 철자가 틀린 도구 이름이 있으면 서브에이전트가 멈출 수 있다고 경고하므로, `scripts/check_skills.py`가 모든 이름을 알려진 목록과 대조합니다. 또 agy 1.2.7부터 `find_by_name`, `grep_search`, `list_dir`는 기본 도구 세트에서 빠졌으며, 사용자 지정 에이전트는 목록에 적었을 때만 쓸 수 있습니다.

## 포함된 명단

| 에이전트 | 역할 | 도구 | 모델 | 쓰기 |
| :--- | :--- | :--- | :--- | :--- |
| `gravitas-scout` | 파일, 경로, 심볼, 출처를 찾는다. 경로와 줄 범위만 반환 | `list_dir`, `find_by_name`, `grep_search`, `view_file` | flash | 없음 |
| `gravitas-reader` | 한정된 파일이나 URL에 대한 구체적 질문에 답하고 근거한 줄을 인용 | `view_file`, `grep_search`, `find_by_name`, `list_dir`, `read_url_content` | flash | 없음 |
| `gravitas-finder` | 주어진 작업 목록에서 한 종류의 결함을 찾거나 한 각도에서 탐색 | `view_file`, `grep_search`, `find_by_name`, `list_dir`, `read_url_content`, `search_web` | flash | 없음 |
| `gravitas-checker` | 독립적인 검증 하나를 실행: 수치 평가, 테스트, 재계산, 쿼리 | `view_file`, `run_command` | flash | 역할 규정상 임시 파일만 |
| `gravitas-refuter` | 주장 하나의 반박을 시도하고, 확신이 없으면 반박된 것으로 판정 | `view_file`, `grep_search`, `read_url_content`, `search_web` | pro | 없음 |
| `gravitas-visual-critic` | 소스를 보지 않은 관찰자로서 캡처를 판단 | `view_file` | pro | 없음 |
| `gravitas-completeness-critic` | 원장을 읽고 한 번도 탐색, 열람, 실행, 검증되지 않은 것을 지목 | `view_file`, `list_dir`, `grep_search`, `find_by_name` | pro | 없음 |
| `gravitas-prose-editor` | 초안을 문체 기준에 맞게 고쳐 수정된 글을 반환 | `view_file` | pro | 없음 |

`gravitas-checker`는 명령줄을 가진 유일한 검증자이므로, 읽기 전용이라는 성질은 도구 제한이 아니라 역할 규정입니다. 범위를 좁게 유지하고, 그 결과가 결론을 떠받칠 때는 트랜스크립트를 읽습니다.

구현은 부모에게 맡기거나 `Model: "inherit"`인 `self`에 맡깁니다. 그러면 파일을 바꾸는 작업에는 사용자가 고른 모델이 쓰입니다.

## 모델 배정

| 작업 | 모델 |
| :--- | :--- |
| 기계적 추출, 파일 분류, 목록 작성 | `flash_lite` |
| 정찰, 읽기, 탐색, 검증 | `flash` |
| 반박, 비평, 심사, 최종 종합 | `pro` |
| 파일을 쓰는 모든 작업 | `inherit` |

파일 분류에 `pro` 비용을 치르는 것은 낭비입니다. 시각 비평을 `flash_lite`로 돌리면 그 역할이 존재하는 이유인 판단력을 버리게 됩니다. 쓰는 역할의 기본값이 `inherit`인 이유는, 사용자가 고른 모델을 조용히 낮추는 것은 사용자가 내리지 않은 결정이기 때문입니다.
