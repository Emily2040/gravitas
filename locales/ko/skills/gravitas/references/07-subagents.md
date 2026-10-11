# 모듈 07 - 서브에이전트

## 목적

전문 에이전트를 투입하는 방법, 2026년 10월 기준 서브에이전트 도구의 매개변수, 이 플러그인이 기본 제공하는 에이전트, 역할별로 쓰는 모델을 정리한 모듈입니다. `invoke_subagent`나 `define_subagent`를 처음 호출하기 전에 `08-delegation.md`와 함께 불러옵니다.

## 전문 에이전트를 쓰는 세 가지 방법

| 경로 | 방법 | 쓰기 권한 | 용도 |
| :--- | :--- | :--- | :--- |
| 기본 제공 에이전트 | `TypeName`을 `gravitas-*` 에이전트로 지정해 `invoke_subagent` 호출 | 에이전트 파일의 `tools` 목록으로 고정 | 관찰, 판단, 비평을 맡는 모든 역할 |
| 즉석 정의 | `define_subagent`로 정의한 뒤, 새로 만든 이름으로 `invoke_subagent` 호출 | `enable_write_tools`를 true 또는 false로 지정 | 이 플러그인이 기본 제공하지 않는 전문 역할 |
| 내장 `self` | `TypeName: "self"`로 `invoke_subagent` 호출 | 부모 에이전트와 같은 도구 | 사용자가 고른 모델과 도구로 진행해야 하는 구현 작업. agy 1.2.9에서는 모델이 나열한 목록에 들어 있었지만, 이 스킬로는 아직 테스트하지 않음 |

쓰기 작업을 맡기면 안 되는 역할에는 기본 제공 에이전트를 우선 쓰십시오. 이들이 읽기 전용인 것은 파일에 적힌 도구 목록 덕분이므로, 서브에이전트가 지시를 따르느냐와는 상관이 없습니다.

## 도구 선언

아래 내용은 2026-09-24에 agy 1.2.9에서 모델 자신이 받은 도구 선언을 그대로 읽어 낸 것이고, 데스크톱 2.17.0의 `language_server.exe`에 들어 있는 문자열과도 대조했습니다. CLI가 1.2.15에서 1.2.16으로 올라간 2026-10-03에는 `define_subagent`를 뺀 나머지를 다시 읽어 보았고, 내용이 일치했습니다. 이 스킬의 이전 버전에는 실제 선언에 없는 필드가 적혀 있었으니, 업데이트 후에는 다시 확인하십시오.

| 도구 | 매개변수 |
| :--- | :--- |
| `invoke_subagent` | `Subagents`: 배열입니다. 각 항목에는 필수 값인 `TypeName`, `Role`(2~5단어로 된 직무명), `Prompt`가 들어가고, 여기에 `Model`(`inherit`, `flash_lite`, `flash`, `pro` 중 하나, 기본값 `inherit`)과 `Workspace`(`inherit`, `branch`, `share` 중 하나, 기본값 `inherit`)를 더할 수 있습니다 |
| `define_subagent` | `name`, `description`, `system_prompt`, `enable_write_tools`(파일 편집과 명령 실행), `enable_mcp_tools`, `enable_subagent_tools` |
| `manage_subagents` | `Action`: `list`, `kill`, `kill_all` 중 하나. `kill`일 때는 `ConversationIds`를 함께 넘깁니다 |
| `send_message` | `Recipient`(서브에이전트의 대화 ID)와 `Message` |
| `schedule` | 일회성 타이머는 `DurationSeconds`로, 크론은 `CronExpression`으로 지정하고 `Prompt`를 함께 넘깁니다. `TimerCondition`은 `never`(기본값), `any`, 또는 발신자 ID 중 하나이며, 발신자 ID를 주면 그 발신자의 메시지가 왔을 때 타이머가 취소됩니다. `IsDaemon`과 `MaxIterations`는 크론에 적용됩니다. 호출하면 바로 반환되며, 취소하려면 `manage_task`에 `kill`과 작업 ID를 넘깁니다 |

여러 서브에이전트를 동시에 돌리려면 `Subagents` 배열 하나에 항목을 여러 개 넣으면 됩니다. 서브에이전트는 시작될 때마다 자기만의 대화 ID와 자기 트랜스크립트를 가리키는 `logAbsoluteUri`를 받습니다. 서브에이전트가 `send_message`를 호출하지 않고 끝나면, 마지막 응답은 발신자가 `system`인 메시지에 실려 옵니다. 이 응답을 기다리려면 `TimerCondition: "any"`로 `schedule` 타이머를 걸어 두고 턴을 끝냅니다. 서브에이전트 ID를 조건으로 건 타이머는 이 `system` 메시지로는 취소되지 않고, 타이머가 없으면 헤드리스 실행은 턴과 함께 끝나 버려 결과를 잃기 때문입니다. 검증된 패턴은 `08-delegation.md`에 있습니다.

`invoke_subagent` 선언에는 사용자가 다른 모델을 요청하지 않는 한 `Model`을 `inherit`로 두라는 지시가 들어 있습니다. 아래 모델 배정 표에 나온 역할에 대해서는, 이 플러그인을 설치한 것 자체가 바로 그 요청에 해당합니다.

## 커스텀 에이전트 파일

커스텀 에이전트는 YAML 프런트매터가 달린 Markdown 파일입니다. 프런트매터에서 에이전트를 설정하고, 본문은 해당 에이전트의 시스템 프롬프트가 됩니다.

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
| `name`, `description` | 에이전트를 식별하는 값이자, 부모가 서브에이전트를 고를 때 읽는 텍스트 |
| `tools` | 에이전트가 호출할 수 있는 도구. 목록에 없는 도구는 아예 주어지지 않음 |
| `model` | `inherit`, `flash`, `pro` 중 하나 |
| `mainAgent`, `subagent` | 메인 에이전트로 선택될 수 있는지, `invoke_subagent`로 시작할 수 있는지 |
| `commandExecutionPolicy` | 셸 명령 실행 정책: `off`, `auto`, `eager`, `sandbox` |
| `skills`, `plugins`, `mcpServers`, `rules`, `hooks`, `agents` | 이 에이전트에 붙이는 커스터마이징 항목 |
| `inheritCustomizations`, `inheritMcp` | 각각 사용자의 스킬, 규칙, 플러그인을 물려받을지, 사용자의 MCP 서버를 받을지 |
| `excludeDefaultComponents` | 문서에는 기본 프롬프트 섹션과 도구를 제외한다고 되어 있지만, agy 1.2.9에서는 추가로 빠지는 것이 없었음(미해결 이슈 #1015) |

키 이름은 데스크톱 2.17.0의 `language_server.exe`에서 YAML 태그로 확인했고, 각 키의 의미는 커스텀 서브에이전트 문서를 따랐습니다. `inheritMcp`는 문서에 없는 키로, 이 스킬에서 직접 테스트했습니다. 바이너리에는 `enabledTools`, `disabledTools`, `hidden`, `background`도 들어 있지만, 테스트하지 않았고 사용하지도 않습니다.

`tools` 목록이 곧 전체 도구 세트는 아닙니다. agy 1.2.9에서 `view_file`만 나열하고 `inheritCustomizations: false`로 설정한 에이전트도, 그 에이전트가 직접 보고한 도구 선언을 보면 `send_message`, `call_mcp_tool`, `list_resources`, `read_resource`, `manage_task`를 쓸 수 있었습니다. `call_mcp_tool`은 연결된 MCP 서버 전부에 접근하므로, 그 서버가 모두 읽기 전용일 때만 비평 에이전트도 읽기 전용이 됩니다. `inheritMcp: false`를 추가하자 `call_mcp_tool`이 사라졌고, 여기에 `excludeDefaultComponents: true`까지 더해도 달라진 것은 없었습니다. 기본 제공 에이전트는 모두 두 상속 플래그를 false로 설정합니다.

커스텀 에이전트는 `~/.gemini/config/agents/`와 플러그인 내부의 `agents/`에서 인식됩니다. 2026-09-24에 agy 1.2.9로 확인했을 때 `agy agents`는 전역 에이전트는 목록에 보여 주었지만 플러그인 내부의 에이전트는 보여 주지 않았습니다. 반면 모델은 둘 다 인식했고 이름까지 댈 수 있었습니다. 워크스페이스의 `.agents/agents/`에 둔 에이전트는 저장소를 `--add-dir`로 넘겼을 때만 인식되었습니다.

주의할 점이 두 가지 있습니다. 첫째, 문서는 `tools`에 매핑되지 않았거나 철자가 틀린 도구 이름이 있으면 서브에이전트가 멈출(hang) 수 있다고 경고합니다. 그래서 `scripts/check_skills.py`가 모든 도구 이름을 알려진 목록과 대조합니다. 둘째, agy 1.2.7부터 `find_by_name`, `grep_search`, `list_dir`가 기본 도구 세트에서 빠졌습니다. 커스텀 에이전트가 이 도구를 쓰려면 목록에 직접 적어야 합니다.

## 기본 제공 에이전트 목록

| 에이전트 | 역할 규정 | 도구 | 모델 | 쓰기 |
| :--- | :--- | :--- | :--- | :--- |
| `gravitas-scout` | 파일, 라우트, 심볼, 출처의 위치를 찾고, 경로와 줄 범위만 반환 | `list_dir`, `find_by_name`, `grep_search`, `view_file` | flash | 불가 |
| `gravitas-reader` | 범위가 정해진 파일이나 URL에 관한 구체적인 질문에 답하고, 근거로 삼은 줄을 인용 | `view_file`, `grep_search`, `find_by_name`, `list_dir`, `read_url_content` | flash | 불가 |
| `gravitas-finder` | 주어진 작업 목록 전체에서 결함 유형 하나만 파고들거나, 한 가지 관점으로만 검색 | `view_file`, `grep_search`, `find_by_name`, `list_dir`, `read_url_content`, `search_web` | flash | 불가 |
| `gravitas-checker` | 독립적인 검증 한 건 실행: 수치 평가, 테스트, 재계산, 쿼리 | `view_file`, `run_command` | flash | 임시 파일만(역할 규정상) |
| `gravitas-refuter` | 주장 하나를 반박해 보고, 확신이 서지 않으면 반박된 것으로 판정 | `view_file`, `grep_search`, `read_url_content`, `search_web` | pro | 불가 |
| `gravitas-visual-critic` | 소스를 본 적 없는 사람의 눈으로 캡처를 평가 | `view_file` | pro | 불가 |
| `gravitas-completeness-critic` | 원장(ledger)을 읽고, 한 번도 검색하거나 열어 보거나 실행하거나 검증하지 않은 항목을 짚어 냄 | `view_file`, `list_dir`, `grep_search`, `find_by_name` | pro | 불가 |
| `gravitas-prose-editor` | 초안에 문체 기준을 적용하고 고친 글을 반환 | `view_file` | pro | 불가 |
| `gravitas-reviewer` | 상시 규칙의 두 번째 의견(Second Opinion)을 위해 답변 초안을 검토하고, 결함을 최대 세 개까지 반환 | `view_file`, `read_url_content`, `search_web`, `run_command` | pro | 불가(역할 규정상) |

`gravitas-checker`와 `gravitas-reviewer`는 명령줄을 쓸 수 있습니다. 따라서 이 둘이 읽기 전용인 것은 도구로 막혀 있어서가 아니라 역할 규정이 그렇게 정해 두었기 때문입니다. checker에게 맡기는 범위는 좁게 잡고, 결론이 그 결과에 기대고 있다면 트랜스크립트를 직접 읽습니다. reviewer는 이 스킬의 팬아웃용이 아니라 상시 규칙의 "두 번째 의견(Second Opinion)" 섹션용 에이전트이며, 이 섹션이 있는 규칙과 함께일 때만 설치됩니다. 그런 규칙은 설치할 때 `--review`를 붙여야 들어갑니다. 구현 작업은 부모 에이전트가 직접 하거나 `Model: "inherit"`로 지정한 `self`에 맡깁니다. 그래야 파일을 바꾸는 작업에 사용자가 고른 모델이 그대로 쓰입니다.

## 모델 배정

| 작업 | 모델 |
| :--- | :--- |
| 기계적인 추출, 파일 분류, 목록 작성 | `flash_lite` |
| scout, reader, finder, checker | `flash` |
| 반박자(refuter), 비평가(critic), 판정자(judge), 최종 종합 | `pro` |
| 파일을 쓰는 모든 작업 | `inherit` |

파일 분류에 `pro`를 쓰는 것은 비용 낭비입니다. 반대로 visual critic을 `flash_lite`로 돌리면 이 역할의 존재 이유인 판단력을 내버리는 셈입니다. 쓰기 작업의 기본값이 `inherit`인 이유는, 사용자가 고른 모델을 아무 말 없이 낮추면 사용자가 내린 적 없는 결정을 대신 내리는 꼴이 되기 때문입니다.
