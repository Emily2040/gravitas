# 모듈 08 - 위임

## 목적

이 모듈은 결과를 확인할 수 있도록 서브에이전트에게 과제를 주는 방법과, 그 주장이 보고서에 들어가기 전에 실제로 무엇을 했는지 확인하는 방법을 다룹니다. `07-subagents.md`와 함께 불러옵니다.

## 역할 약정

쓸모없는 결과를 내는 지시는 토큰을 쓰고도 다시 해야 할 것을 남깁니다. 모든 `Prompt`에는 여섯 가지를 적습니다.

1. 범위: 대상이 되는 파일, 주장, 경로, 출처를 절대 경로나 전체 URL로 적고, 그 밖의 것은 넣지 않습니다. 범위가 겹치면 중복이 생기고, 범위 사이의 틈은 조용한 누락을 만듭니다.
2. 질문: 답을 확인할 수 있을 만큼 좁은 질문 하나.
3. 반환 형태: `schemas/finding.schema.json`에 맞는 발견 기록, 또는 `schemas/verdict.schema.json`에 맞는 판정 하나. 무엇을 찾을지만 들은 에이전트는 에세이를 씁니다.
4. 증거: 모든 주장은 같은 필드에 등급과 출처를 담고, 4등급인 것은 가설로 표시합니다.
5. 멈춤 조건: 범위를 다 다뤘을 때, 또는 정한 개수에 이르렀을 때.
6. 막혔을 때의 동작: 도구가 거부되거나 파일이 없으면, 있는 것을 `blocked` 상태와 오류 문구와 함께 반환합니다. 거부를 우회하는 것은 금지이며, 플랫폼 자체의 거부 메시지도 같은 말을 합니다.

하위 에이전트는 결과를 반환할 뿐 진행 상황을 서술하지 않습니다.

서브에이전트에게 절대 상대 경로를 주지 마십시오. 2026-09-24 agy 1.2.9에서 `view_file`은 상대 경로를 워크스페이스가 아니라 모든 CLI 대화가 함께 쓰는 폴더인 `~/.gemini/antigravity-cli/scratch/`를 기준으로 해석했습니다. “현재 워크스페이스의” `draft.md`를 편집하라는 말을 들은 `gravitas-prose-editor`는 닷새 전 시험이 그 폴더에 남긴 다른 `draft.md`를 편집했고, 아무 오류 없이 결과를 돌려주었습니다. `gravitas-refuter`와 `gravitas-visual-critic`도 같은 폴더에 닿아 아무것도 찾지 못하고 `blocked`를 반환했는데, 이쪽이 더 나은 실패입니다.

모든 하위 에이전트에게 필요한 것은 전부 프롬프트와 지시 안에 있다고 알려 줍니다. 감사 시험에서 출력이 “the Gravitas finding schema”에 맞아야 한다는 말을 들은 탐색자는 127단계의 대부분을 그 파일을 찾아 사용자 폴더를 뒤지는 데 썼고, 그 과정에서 git 내부 파일과 무관한 시험 출력까지 읽었습니다. 이제 포함된 에이전트들은 스키마 전체를 예시로 지니고 있으며, 찾아볼 것이 없다는 말을 듣습니다. 다시 실행했을 때 모든 탐색자와 반박자는 4~8단계 안에 끝났고 범위 밖의 것은 하나도 열지 않았습니다.

경로 조작, 주입, 데이터 노출을 증명하는 검증자는 임시 폴더에 직접 만든 무해한 카나리아 파일을 대상으로 삼습니다. 같은 시험에서 검증자는 결함 있는 함수를 통해 `C:\Windows\win.ini`를 읽어 경로 조작을 증명했습니다. 거기서는 무해했지만, 진짜 비밀이 있는 컴퓨터에서는 잘못된 습관입니다.

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

## 위임의 무결성

부모 자신의 상태는 하위 에이전트에 대해 아무것도 말해 주지 않으므로, 종합하기 전에 하위 에이전트를 하나씩 확인합니다.

1. 모든 하위 에이전트를 대화 ID와 최종 상태(`done`, `failed`, `denied`, `empty`, `killed`)와 함께 원장에 기록합니다.
2. `manage_subagents`를 `list`로 호출해 아직 실행 중인 것이 없는지 확인하고, 상한을 넘은 것은 `kill`합니다. 헤드리스 실행에서는 모든 하위 에이전트가 끝날 때까지 도구 호출을 계속합니다. “비평가를 기다리는 중” 같은 텍스트 답으로 턴을 끝내면 실행 전체가 끝날 수 있고, 그 뒤에 도착한 결과는 사라집니다.
3. 실패했거나, 거부되었거나, 아무것도 반환하지 않은 하위 에이전트는 이름을 밝혀 범위의 공백으로 보고합니다.
4. 하위 에이전트가 돌려준 결론을 떠받치는 주장마다, `logAbsoluteUri`에 있는 그 트랜스크립트에서 표시 뒤의 도구 단계를 확인합니다. `scripts/provenance_check.py <child answer> --conversation <child id>`가 모든 표시에 대해 이것을 한 번에 합니다. 규칙은 `02-evidence-traps.md`의 “위임한 주장”에 있습니다.
5. 각 주장을 등급과 작성자와 함께 보고서에 옮깁니다: `read by gravitas-reader (...)`.

조용한 실패는 이 플랫폼에서 실제로 일어납니다. 2026-09-24 agy 1.2.9의 헤드리스 실행에서 서브에이전트의 첫 `read_file`이 거부되어 아무것도 나오지 않았는데, 부모는 시작 5.4초 만에 `"status": "SUCCESS"`와 "I am waiting for its response."를 남기고 끝났습니다. 권한을 주자 같은 종류의 실행은 서브에이전트를 63초 기다렸고 그 답을 보고했습니다. 두 번째 조기 종료에는 거부가 없었습니다. 전체 규모 감사가 `manage_subagents`로 1분 동안 폴링한 뒤 "Waiting for the Completeness Critic subagent to complete its evaluation"으로 턴을 끝냈고, CLI는 29초 뒤 실행을 닫았습니다. 비평가의 결과가 도착했을 때 로그에는 "Failed to wake idle agent on message: run state not found"가 기록되었습니다.

## 독립성

쓸 수 있는 비평가는 잘못 진단한 것을 고치고 성공을 보고하며, 그 수리가 증거의 일부가 됩니다. 명단의 모든 관찰, 판단 역할에 편집 도구가 없는 이유입니다.

결과물은 “당신의 이전 시도”가 아니라 제3자의 출력으로 비평가에게 건넵니다. 모델은 남이 한 것이라고 믿는 작업에서 오류를 훨씬 잘 찾아내며, 표시만 바꿔도 탐지가 좋아집니다. 검증을 주장을 만든 에이전트에게 되돌려 보내지 마십시오.

에이전트 파일에서 끄지 않으면 사용자 지정 항목이 서브에이전트에게 전달됩니다. agy 1.2.9에서 `gravitas-reader`는 3단계 만에 답을 찾은 뒤, 플러그인의 상시 규칙이 시키는 대로 35초 동안 이 스킬을 불러왔고, 실행은 63초가 걸렸습니다. 에이전트 파일에 `inheritCustomizations: false`를 넣자 같은 작업이 40초에 끝났고 스킬 파일은 하나도 열리지 않았습니다. 포함된 모든 에이전트가 이를 설정하며, 이것은 부모의 규칙과 틀을 비평가의 컨텍스트 밖에 두는 역할도 합니다. 그 어느 것도 서브에이전트 도구를 갖지 않습니다.

## 병렬 작성자

같은 파일에 두 작성자가 쓰면 서로 덮어씁니다. 작업을 파일별로 나누거나, 작성자를 차례로 실행하거나, `Workspace: "branch"` 또는 `Workspace: "share"`로 각자에게 격리된 워크스페이스를 줍니다. 격리 모드는 도구 선언에 설명되어 있지만 이 스킬과는 아직 시험하지 않았습니다. 어느 쪽이든 부모를 통해 합칩니다.

## 안티패턴

- 편집 도구를 가진 비평가, 또는 검토 대상 작업을 범위에 포함한 검증자.
- 주장을 만든 에이전트가 하는 검증.
- 모든 전문 에이전트에 `enable_subagent_tools`를 켜서 아무도 감사할 수 없는 깊고 느린 트리를 만드는 것.
- 반환 형태가 없는 지시.
- 결론이 기대는 주장에 대해 하위 에이전트의 요약만 읽고 트랜스크립트는 읽지 않는 것.
- `manage_subagents`라면 실행 중인 하위 에이전트를 보여 주었을 상황에서 실행이 끝났다고 보고하는 것.
