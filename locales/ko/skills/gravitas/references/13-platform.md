# 모듈 13 - 플랫폼

## 목적

이 모듈은 다르게 가정하면 작업을 낭비하게 되는, 검증된 Antigravity 동작을 기록합니다. 작업이 Antigravity의 사용자 지정 항목 로드, 서브에이전트 실행, 권한 적용, 헤드리스 실행 방식에 의존할 때, 그리고 도구, 훅, 스킬, 권한이 예상 밖으로 동작할 때 불러옵니다.

플랫폼이 빠르게 바뀌므로 모든 항목에는 확인한 버전과 날짜가 붙어 있습니다. 2026년 9월 18일부터 23일 사이에 데스크톱 2.15.0, 2.15.1, 2.16.0, 2.17.0과 CLI 1.2.7, 1.2.8, 1.2.9가 출시되었습니다. 달리 적지 않았다면 2026년 9월 24일 Windows 11, 데스크톱 2.17.0, agy CLI 1.2.9에서 확인한 것입니다. WinGet으로 설치한 CLI는 21초 간격의 두 시험 실행 사이에 아무 알림 없이 1.2.7에서 1.2.9로 스스로 업데이트했습니다. 그래서 여기 적힌 날인은 모두 해당 실행 자체의 로그에 있는 `version:` 줄에서 가져왔습니다. 항목에 기대기 전에 그 날인을 `https://antigravity.google/changelog`의 변경 기록과 비교하고, 관련 부분이 바뀌었다면 다시 확인합니다.

## 사용자 지정 항목을 불러오는 위치

| 위치 | 스킬 | 에이전트 | 규칙 | 증거 |
| :--- | :--- | :--- | :--- | :--- |
| `~/.gemini/config/skills/`, `agents/`, `AGENTS.md` | 로드됨 | 로드되고 `agy agents`에 표시됨 | 로드됨 | 관찰함 |
| `~/.gemini/config/plugins/<name>/` | 로드됨 | 로드되지만 `agy agents`에는 표시되지 않음 | `rules/AGENTS.md`에서 로드됨 | 시험용 플러그인으로 관찰: 모델이 스킬과 에이전트 이름을 댔고 규칙을 따랐음 |
| `<repo>/.agents/` | `--add-dir`로만 로드됨 | `--add-dir`로만 로드됨 | `rules/`는 어느 쪽에서도 로드되지 않음 | 관찰함, open issue #1036, #1052 |

Gravitas가 플러그인으로 설치되는 이유가 이것입니다. 한 폴더에 스킬, 검증 에이전트, 상시 규칙이 모두 담기고, `agy plugin disable gravitas` 하나로 전부 함께 끌 수 있습니다. `agy plugin list`는 마켓플레이스에서 가져온 플러그인만 보여 주므로, 복사해 넣은 플러그인은 로드되어 있어도 거기 나타나지 않습니다.

워크스페이스 행은 문서와 모순됩니다. 내장 사용자 지정 가이드와 스킬 페이지는 `<repo>/.agents/`에서의 탐색을 설명하고, IDE 가이드는 IDE가 그 폴더를 "automatically discovers and respects"한다고 씁니다. CLI에서는 저장소를 `--add-dir`로 넘기면 `.agents/`의 스킬, 에이전트, 훅이 로드되었고, 그 저장소가 작업 디렉터리이기도 한 경우에도 마찬가지였습니다. 이 플래그 없이 저장소 안에서 실행하면 아무것도 로드되지 않았고, 로그의 `workspaceDirs`는 그 폴더를 가리키면서도 `loaded 0 named hooks`라고 보고했습니다. `.agents/rules/`의 규칙은 어느 경우에도 로드되지 않았습니다. 저장소 자체의 사용자 지정이 중요할 때는 `agy -p "..." --add-dir <repo>`로 실행합니다. 데스크톱 앱과 IDE는 시험하지 않았습니다.

## 사용자 지정 항목을 떨어뜨리는 예산

스킬 이름과 설명은 사용자 지정 예산을 공유하며, 들어가지 못한 스킬은 빠집니다. 스킬 133개가 설치된 상태에서 모델은 그중 3개를 "Excluded Skills (due to context budget limits)" 아래에 나열했습니다. 3개 모두 설치된 스킬 가운데 설명이 가장 긴 5개에 들었고, 길이는 1,001~1,028자였습니다. 길이와 제외 사이의 연관은 관찰 한 번에서 추론한 것입니다. 설명은 짧게 씁니다. 이 스킬의 설명은 500자 미만입니다.

규칙에는 20,000토큰의 별도 예산이 있고, 규칙 파일마다 24,000바이트에서 줄 경계에 맞춰 잘립니다. 예산을 넘은 규칙은 파일 포인터로 강등됩니다(read: 내장 `agy-customizations` 가이드의 `docs/rules.md`, CLI 1.2.7 변경 기록).

## 잘못된 스킬은 조용히 실패한다

해석할 수 없는 `SKILL.md`는 건너뜁니다. 오류는 `~/.gemini/antigravity-cli/log/cli-*.log`에 `skills.go:201] Failed to parse skill file ...`로 기록될 뿐, 사용자가 볼 수 있는 곳에는 나타나지 않습니다. UTF-8 바이트 순서 표시 하나만으로도 이런 일이 생기며, Windows PowerShell 5.1의 `Set-Content`와 `Out-File`은 기본으로 그것을 붙입니다. 망가진 스킬 하나가 다른 스킬의 로드를 막지는 않습니다.

편집할 때마다 `scripts/check_skills.py`를 실행합니다. 프런트매터 해석, 설명의 유무와 길이, 바이트 순서 표시, 끊어진 참조, 100줄이 넘는 모듈, 에이전트 도구 이름, 쓰기 도구를 가진 비평가, 규칙 파일 크기를 확인합니다.

## 파일과 경로

| 동작 | 증거 |
| :--- | :--- |
| `view_file`은 상대 경로를 거부하지만, 헤드리스 실행의 에이전트는 `~/.gemini/antigravity-cli/scratch/`를 자기 작업 디렉터리로 여긴다. 메인 에이전트는 거부당한 뒤 그곳을 뒤졌고, “현재 워크스페이스의” `draft.md`를 쓰라는 말을 들은 서브에이전트는 그곳으로 가는 경로를 직접 만들었다. 이 폴더는 모든 CLI 대화가 함께 쓰며 닷새 전 시험의 파일 33개가 남아 있었고, 둘 다 같은 이름의 오래된 파일을 아무 말 없이 열었다 | 1.2.9에서 관찰 |
| `view_file`은 호출 한 번에 100줄을 돌려준다. 한 실행에서 에이전트는 114줄 파일의 처음 100줄을 읽고 넘어갔다 | 1.2.9에서 관찰 |
| 설치된 플러그인 안의 파일은 헤드리스 실행에서도 권한 없이 읽을 수 있다 | 1.2.9에서 관찰 |
| 와일드카드 권한을 가진 상태에서 프롬프트가 불완전해 보이자, 에이전트는 나머지를 찾으려고 사용자의 PowerShell 기록, 다른 대화의 트랜스크립트, 실행 중인 프로세스의 명령줄을 읽었다 | 1.2.9에서 `gemini-3.8-flash-high`로 관찰 |

## 서브에이전트

모델이 받는 도구 선언의 형태가 바뀌었습니다. `invoke_subagent`는 `TypeName`, `Role`, `Prompt`, `Model`, `Workspace`를 가진 항목들의 `Subagents` 배열을 받고, `define_subagent`는 `enable_write_tools`, `enable_mcp_tools`, `enable_subagent_tools` 플래그를 받으며, `manage_subagents`는 목록 조회와 종료를 합니다. 자세한 내용은 `07-subagents.md`에 있습니다.

사용자 지정 서브에이전트 문서에 따르면, `tools` 목록에 매핑되지 않은 도구 이름이 있는 사용자 지정 에이전트는 멈출 수 있습니다. CLI 1.2.7부터 `find_by_name`, `grep_search`, `list_dir`는 기본 도구 세트에 없으며, 그것들을 나열한 에이전트만 쓸 수 있습니다.

동시에 실행되는 서브에이전트는 계정의 모델 용량을 공유합니다. 다른 두 실행이 돌아가는 동안, 한 부모 실행이 서브에이전트 세 개가 끝난 뒤 `RESOURCE_EXHAUSTED (code 429)`로 `ERROR` 상태로 끝났습니다. 팬아웃 규모는 이를 염두에 두고 정합니다. 에이전트 파일에서 `inheritCustomizations: false`로 두지 않으면 사용자 지정 항목이 서브에이전트에게 전달되며, 측정 결과는 `08-delegation.md`에 있습니다.

## 헤드리스 실행

| 동작 | 증거 |
| :--- | :--- |
| CLI의 정책은 `~/.gemini/antigravity-cli/settings.json`의 `toolPermission`(기본값 `request-review`)에서 오므로, 데스크톱 설정의 `autoExecutionPolicy: AUTO`는 `agy -p`에서 효과가 없다. `toolPermission: "always-proceed"`는 헤드리스에서 권한 없는 명령을 실행하면서도 `deny` 규칙은 지킨다 | 1.2.9에서 관찰, issue #1054 |
| `allow`를 반환하는 `PreToolUse` 훅도, `permissionOverrides`를 단 `ask`도 권한 없는 호출을 허용하지 않는다. `deny`는 권한 있는 호출도 막는다 | 2026년 9월 19일과 24일에 관찰, open issue #1053 |
| `decision: "allow"`와 함께 반환한 `overwrite`는 적용되고 에이전트에게 알려지며, 권한은 바뀐 인수로 확인된다. `decision` 없는 `overwrite`는 거부가 된다 | 2026년 9월 19일과 24일에 관찰 |
| 훅이 명령을 거부한 뒤에도 최종 답이 그 명령이 출력했을 내용을 말할 수 있다. 그런 실행 11번 중 6번은 답이 프롬프트가 요구한 표식 그대로였지만, 기록상 명령은 한 번도 실행되지 않았다 | 1.2.9에서 관찰 |
| 도구가 거부되면 그 턴은 버려지고, 실행은 `"status": "SUCCESS"`와 종료 코드 0을 보고한다. 측정한 최대 손실은 완료된 단계 48개와 출력 토큰 20,595개였다 | 1.2.7에서 관찰, 1.2.9에서 다시 관찰, open issue #794 |
| 헤드리스 실행에서 시작한 서브에이전트는 `read_file`을 허용하지 않으면 워크스페이스 파일 읽기를 거부당한다 | 1.2.9에서 관찰 |
| 서브에이전트가 실행 중일 때 턴을 끝낸 부모는 그 결과를 받지 못한다. 실행은 하위 에이전트가 끝나기를 기다린 뒤 종료되고, 로그에 "Failed to wake idle agent on message: run state not found"를 남기며, 부모의 마지막 답으로 `SUCCESS`를 보고한다 | 1.2.9에서 통제된 실행 2번 중 2번과 감사 한 번에서 관찰, issue #1044. 폴링을 계속한 실행은 최대 338초를 기다려 모든 결과를 받았음 |
| 에이전트와 모델 API 실패는 stderr에 `AGY_ERROR: {...}`를 출력하고 종료 코드 3으로 끝난다 | read: 1.2.6 변경 기록 |
| `--json-schema`는 읽을 수 있는 파일도 JSON 객체도 아닌 인수를 문자열 스키마로 바꾸며, 루트가 객체가 아닌 스키마는 항상 HTTP 400을 반환한다 | 1.2.7에서 42번 실행으로 관찰, 1.2.9에서 다시 관찰, open issue #1064 |

한 보안 감사는 13분 동안 서브에이전트 7개를 돌린 뒤, 최종 답이 "This request was blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related queries."로 바뀌었습니다(1.2.9에서 `gemini-3.8-flash-high`로 관찰). 헤드리스 실행은 명시적 권한이나 `toolPermission`을 기준으로 계획합니다. 훅의 허용은 믿을 수 없으며, `SUCCESS` 상태는 그 턴의 작업이 살아남았다는 증거가 아닙니다.

## 훅

- `invocationNum`은 0부터 세므로 첫 턴은 0을 보고합니다. 문서의 예시는 3을 보여 주며 이 점을 말하지 않습니다.
- `hooks.json`의 명령에서는 무엇도 따옴표로 감싸지 마십시오. Windows에서는 따옴표가 그대로 프로그램에 전달됩니다. 따옴표로 감싼 실행 파일은 "not recognized"가 되고, 따옴표로 감싼 스크립트 경로는 훅 폴더 뒤에 이어 붙습니다(issue #222). 공백 없는 경로를 따옴표 없이 씁니다.
- `hooks.json`은 JSON 직렬화 도구로 씁니다. bash heredoc은 Windows 경로의 이중 백슬래시를 하나로 합쳐 잘못된 이스케이프를 만듭니다.
- 훅의 작업 디렉터리는 `hooks.json`이 있는 폴더입니다.
- 실패한 `PreInvocation` 훅은 건너뜁니다. 잘못된 JSON, 빈 출력, 0이 아닌 종료, 시간 초과가 모두 허용되었습니다(2026년 9월 19일). `PreToolUse` 훅은 실패하면 거부합니다. 잘못된 JSON, `{}`, `decision` 누락, 0이 아닌 종료는 모두 호출을 거부하고, 빈 출력만 통과시킵니다(1.2.9). 시간 초과는 실제로 적용됩니다. 데스크톱 2.4.3부터는 실행할 수 없는 설정이 로드 시점에 오류와 함께 거부됩니다.
- `terminationBehavior: "force_continue"`에는 상한이 없습니다(open issue #1055). 1.2.9에서는 훅이 12번 실행되며 모델 호출 11번을 더 강제했고, 그중 아홉 번은 내용 없는 답, 두 번은 아무도 요청하지 않은 도구 호출이었습니다. `Stop` 훅은 `decision: "continue"`로 종료를 막을 수 있으며, 상한을 두는 데 쓸 `executionNum`을 받습니다. `10-iteration.md`를 보십시오.

훅을 검증하려면 스크립트가 감시용 파일에 내용을 덧붙이게 하고, 고유한 값을 주입해 따라 말하도록 지시한 뒤 둘 다 확인합니다. 올바른 파일과 조용한 로그는 훅이 실행되었다는 증거가 아닙니다.

## 권한

권한은 명령 문자열 그대로, 때로는 첫 단어만 저장되므로 `command(if)`, `command(&)` 같은 항목이 권한 하나로 통째로 저장된 수 KB짜리 스크립트와 나란히 생깁니다. 권한은 바이트 단위로 똑같은 명령에만 다시 일치하므로, 확인 창은 다시 뜨고 쓸모없는 권한이 또 추가됩니다. 한 컴퓨터의 `~/.gemini/config/config.json`은 301 KB에 이르렀고, 그중 97.5%가 쓸모없는 권한이었으며 가장 긴 항목은 36,331자였습니다. 가끔 크기를 확인합니다. 제 몫을 하는 것은 도메인에 대한 `read_url` 권한입니다.

프로젝트 설정이 전역 설정보다 우선합니다. `~/.gemini/config/projects/*.json`의 각 파일은 자체 실행 정책을 가질 수 있고, 프로젝트가 다른 값을 가지고 있는 동안에는 화면에서 전역 설정을 바꿔도 효과가 없습니다. 정책 값은 `always-proceed`, `request-review`, `strict`, `proceed-in-sandbox`이며, Windows에서는 데스크톱 2.15.1부터 파일 및 네트워크 샌드박스를 쓸 수 있습니다(read: 내장 `antigravity-guide` 스킬과 그 `app.md` 참조, 변경 기록).

CLI는 자체 `settings.json`의 `permissions.allow`와 `~/.gemini/config/config.json`의 `globalPermissionGrants.allow` 양쪽에서 권한을 읽습니다. 후자는 로그의 `stored shared config permissions` 줄에서 확인됩니다. Windows에서 `command()` 규칙이 일치하는 것은 똑같은 명령 줄, `command(*)`, 또는 줄 전체를 덮는 `regex:` 규칙(예: `command(regex:git .*)`)뿐입니다. `command(git)`과 `command(git *)`는 인수가 있는 호출에 하나도 일치하지 않습니다(1.2.9에서 관찰, issue #619, #955).

모델에게 절대 권한을 묻지 말라고 지시하는 규칙은 작동할 수 없습니다. 정책은 모델에게 묻기 전에 적용되기 때문입니다.

## 환경별 도구

agy 1.2.9에서 기본 에이전트의 도구 목록에는 `ask_question`, `call_mcp_tool`, `define_subagent`, `generate_image`, `invoke_subagent`, `list_resources`, `manage_subagents`, `manage_task`, `read_resource`, `read_url_content`, `replace_file_content`, `run_command`, `schedule`, `search_web`, `send_message`, `view_file`, `write_to_file`과 활성화된 MCP 서버의 도구가 있었습니다. 브라우저 도구는 없었습니다. 브라우저 도구는 데스크톱 앱에서 브라우저 연동이 켜져 있을 때 나타나지만, 기록된 데스크톱 실행 하나에는 전혀 없었으므로 계획 전에 확인합니다. 대안은 `04-runtime-verification.md`에 있습니다.

알아 둘 만한 기능: `ask_question`은 대화형 세션에서 사용자에게 구조화된 질문을 합니다. `/plan`은 만들기 전에 편집 가능한 계획을 초안으로 작성하며 Plan Review Policy 설정을 따릅니다(데스크톱 2.17.0). `agy --effort low|medium|high`는 추론 강도를 정합니다. `agy models`는 계정에서 쓸 수 있는 모델을 나열합니다. `agy --agent <name>`은 사용자 지정 에이전트로 세션을 시작합니다.

## 스크립트 조율

팬아웃을 수백 개 항목에 대해 정확한 개수로 실행해야 할 때는 어떤 에이전트의 기억보다 스크립트가 더 믿을 만합니다. SDK 플러그인 문서(버전 0.0.7)에 따르면 Google Antigravity Python SDK(`pip install google-antigravity`)는 `SubagentConfig`, `enabled_tools`, `allowed_subagents`, `max_subagent_depth`, 그리고 구조화된 출력을 위한 `response_schema`로 코드에서 에이전트와 서브에이전트를 시작합니다. 인증에는 `GEMINI_API_KEY`를 쓰며, 비용은 Antigravity 요금제가 아니라 그 키에 청구됩니다. 이 경로는 이 스킬과 아직 시험하지 않았으므로 문서화되었지만 검증되지 않은 것으로 다룹니다.

## 실행 중인 플랫폼에서 확인하기

위 항목 중 몇몇은 문서와 모순되며, 그 결과를 얻은 시험 도중에 CLI가 스스로 업데이트되었습니다. 플랫폼 동작이 작업에 중요하다면, 설치된 버전에서 시험하고 결과에 날인합니다. 증거 등급은 작업에 적용되는 것과 똑같이 플랫폼에도 적용됩니다.
