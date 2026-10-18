# 모듈 13 - 플랫폼

## 목적

이 모듈에는 직접 확인한 Antigravity의 실제 동작 가운데, 다르게 짐작하고 진행했다가는 작업을 헛되이 날리게 되는 것들을 모아 두었습니다. 작업 결과가 Antigravity의 커스터마이징 로드 방식, 서브에이전트 실행 방식, 권한 적용 방식, 헤드리스 실행 방식에 따라 달라진다면 이 모듈을 불러옵니다. 도구, 훅, 스킬, 권한이 예상과 다르게 동작할 때도 언제든 불러옵니다.

플랫폼이 워낙 빠르게 바뀌기 때문에 항목마다 어느 버전에서 언제 확인했는지를 함께 적었습니다. 2026년 9월 18일부터 23일 사이에만 데스크톱 2.15.0, 2.15.1, 2.16.0, 2.17.0과 CLI 1.2.7, 1.2.8, 1.2.9가 나왔습니다. 따로 적지 않은 항목은 2026년 9월 24일 Windows 11에서 데스크톱 2.17.0과 agy CLI 1.2.9로 확인한 것입니다. WinGet으로 설치한 CLI는 21초 간격으로 돌린 두 테스트 실행 사이에 아무 알림 없이 1.2.7에서 1.2.9로 스스로 업데이트되었습니다. 그래서 이 문서의 버전 표기는 모두 해당 실행의 로그에 찍힌 `version:` 줄에서 가져왔습니다. CLI는 같은 방식으로 2026년 9월 26일에 1.2.11이 되었고, 2026년 10월 3일 시점에는 1.2.16까지 올라가 있었습니다. 어떤 항목을 근거로 삼기 전에는 거기 적힌 버전·날짜를 `https://antigravity.google/changelog`의 변경 로그와 비교하고, 관련된 부분이 바뀌었다면 다시 확인합니다.

## 커스터마이징을 불러오는 위치

| 위치 | 스킬 | 에이전트 | 규칙 | 근거 |
| :--- | :--- | :--- | :--- | :--- |
| `~/.gemini/config/skills/`, `agents/`, `AGENTS.md` | 로드됨 | 로드되며 `agy agents` 목록에도 나옴 | 로드됨 | Observed |
| `~/.gemini/config/plugins/<name>/` | 로드됨 | 로드되지만 `agy agents` 목록에는 안 나옴 | `rules/AGENTS.md`에서 로드됨 | Observed. 테스트용 플러그인으로 확인: 모델이 그 플러그인의 스킬과 에이전트 이름을 댔고 규칙도 따름 |
| `<repo>/.agents/` | `--add-dir`로 넘겼을 때만 로드됨 | `--add-dir`로 넘겼을 때만 로드됨 | `rules/`는 어느 쪽이든 로드되지 않음 | Observed. 미해결 이슈 #1036, #1052 |

Gravitas를 플러그인으로 설치하는 것도 이 때문입니다. 스킬, 검증 에이전트, 상시 규칙이 한 폴더에 모두 들어 있고, `agy plugin disable gravitas` 한 번이면 전부 함께 꺼집니다. 다만 `agy plugin list`에는 마켓플레이스에서 가져온 플러그인만 나오므로, 폴더째 복사해 넣은 플러그인은 로드된 상태여도 이 목록에 보이지 않습니다.

워크스페이스 행의 결과는 공식 문서와 어긋납니다. 내장 커스터마이징 가이드와 스킬 페이지는 `<repo>/.agents/`에서 항목을 찾는다고 설명하고, IDE 가이드에는 IDE가 이 폴더를 자동으로 찾아 반영한다("automatically discovers and respects")고 적혀 있습니다. CLI에서는 저장소를 `--add-dir`로 넘기면 `.agents/`에 둔 스킬, 에이전트, 훅이 로드되었고, 그 저장소가 작업 디렉터리를 겸할 때도 마찬가지였습니다. 반면 플래그 없이 저장소 안에서 실행하면 하나도 로드되지 않았습니다. 로그의 `workspaceDirs`에 그 폴더가 들어 있었는데도 `loaded 0 named hooks`가 찍혔습니다. `.agents/rules/`에 둔 규칙은 어느 방식으로도 로드되지 않았습니다. 저장소에 딸린 커스터마이징이 필요하다면 `agy -p "..." --add-dir <repo>`로 실행합니다. 데스크톱 앱과 IDE에서는 테스트하지 않았습니다.

## 예산을 넘으면 커스터마이징이 빠진다

스킬 이름과 설명은 하나의 커스터마이징 예산을 나눠 쓰고, 예산에 들어가지 못한 스킬은 빠집니다. 스킬 133개를 설치한 상태에서 모델은 그중 3개를 "Excluded Skills (due to context budget limits)" 아래에 나열했습니다. 3개 모두 설치된 스킬 가운데 설명이 가장 긴 5개 안에 들었고, 설명 길이는 1,001~1,028자였습니다. 다만 설명 길이와 제외 사이의 연관성은 관찰 한 번에 기댄 추론(inferred)입니다. 설명은 짧게 씁니다. 이 스킬의 설명은 500자가 안 됩니다.

규칙에는 20,000토큰의 예산이 따로 있고, 규칙 파일은 하나당 24,000바이트에서 줄 경계에 맞춰 잘립니다. 예산을 넘긴 규칙은 파일 포인터로 강등됩니다(read: 내장 `agy-customizations` 가이드의 `docs/rules.md`, CLI 1.2.7 변경 로그).

## 형식이 잘못된 스킬은 소리 없이 실패한다

파싱할 수 없는 `SKILL.md`는 그냥 건너뜁니다. 오류는 `~/.gemini/antigravity-cli/log/cli-*.log`에 `skills.go:201] Failed to parse skill file ...`로 남을 뿐, 사용자 눈에 띄는 곳에는 어디에도 나타나지 않습니다. UTF-8 BOM(바이트 순서 표시) 하나만 붙어 있어도 이렇게 되는데, Windows PowerShell 5.1의 `Set-Content`와 `Out-File`은 기본값으로 BOM을 붙입니다. 망가진 스킬이 하나 있어도 나머지 스킬은 정상적으로 로드됩니다.

수정할 때마다 `scripts/check_skills.py`를 실행합니다. 이 스크립트는 프런트매터 파싱, 설명의 유무와 길이, BOM, 깨진 참조, 100줄이 넘는 모듈, 에이전트의 도구 이름, 파일 쓰기 도구를 가진 검증 에이전트, 규칙 파일 크기를 검사합니다.

## 파일과 경로

| 동작 | 근거 |
| :--- | :--- |
| `view_file`은 상대 경로를 받지 않는데도, 헤드리스 실행의 에이전트는 `~/.gemini/antigravity-cli/scratch/`를 자기 작업 디렉터리로 여깁니다. 메인 에이전트는 상대 경로가 거부되자 이 폴더를 뒤졌고, 현재 워크스페이스("in the current workspace")에 있는 `draft.md`를 사용하라는 지시를 받은 서브에이전트는 곧바로 이 폴더 안을 가리키는 경로를 만들었습니다. 이 폴더는 모든 CLI 대화가 함께 쓰는 곳이고, 닷새 전 테스트에서 남은 파일 33개가 그대로 있었습니다. 두 에이전트 모두 이름이 같은 묵은 파일을 열면서 아무 말도 하지 않았습니다 | Observed (1.2.9) |
| `view_file`은 한 번 호출에 100줄씩 돌려줍니다. 어떤 실행에서는 에이전트가 114줄짜리 파일의 앞 100줄만 읽고 그대로 넘어갔습니다 | Observed (1.2.9) |
| 설치된 플러그인 안의 파일은 헤드리스 실행에서도 허용(grant) 없이 읽을 수 있습니다 | Observed (1.2.9) |
| 와일드카드 허용 항목이 있는 상태에서 미완성으로 보이는 프롬프트를 받자, 에이전트는 나머지 내용을 찾으려고 사용자의 PowerShell 기록, 다른 대화의 트랜스크립트, 실행 중인 프로세스의 명령줄까지 읽었습니다 | Observed (1.2.9, `gemini-3.8-flash-high`) |

## 서브에이전트

모델에 전달되는 도구 선언의 형태가 바뀌었습니다. `invoke_subagent`는 `Subagents` 배열을 받고, 배열의 각 항목에는 `TypeName`, `Role`, `Prompt`, `Model`(`inherit`, `flash_lite`, `flash`, `pro` 중 하나), `Workspace`가 들어갑니다. `define_subagent`는 `enable_write_tools`, `enable_mcp_tools`, `enable_subagent_tools` 플래그를 받고, `manage_subagents`로는 서브에이전트 목록을 보거나 종료할 수 있습니다. 자세한 내용은 `07-subagents.md`에 있습니다.

커스텀 서브에이전트 문서에 따르면, `tools` 목록에 매핑되지 않은 도구 이름이 들어 있는 커스텀 에이전트는 멈춰 버릴 수 있습니다. CLI 1.2.7부터는 `find_by_name`, `grep_search`, `list_dir`가 기본 도구 세트에서 빠져서, 이 도구들을 목록에 직접 적은 에이전트만 쓸 수 있습니다.

동시에 도는 서브에이전트들은 계정의 모델 용량을 나눠 씁니다. 다른 실행 두 개가 돌아가는 사이, 어떤 부모 실행은 서브에이전트 세 개가 모두 끝난 뒤에 `RESOURCE_EXHAUSTED (code 429)`로 `ERROR` 상태가 되어 끝났습니다. 팬아웃 규모는 이 점을 감안해서 정합니다. 에이전트 파일에 `inheritCustomizations: false`를 지정하지 않는 한 커스터마이징은 서브에이전트에도 그대로 전달됩니다. 측정 결과는 `08-delegation.md`에 있습니다.

## 헤드리스 실행

| 동작 | 근거 |
| :--- | :--- |
| CLI는 정책을 `~/.gemini/antigravity-cli/settings.json`의 `toolPermission`(기본값 `request-review`)에서 가져옵니다. 따라서 데스크톱 설정에서 `autoExecutionPolicy: AUTO`로 지정해 두어도 `agy -p`에서는 아무 효과가 없습니다. `toolPermission: "always-proceed"`로 두면 헤드리스에서도 허용되지 않은 명령을 실행하며, 그러면서도 `deny` 규칙은 지킵니다 | Observed (1.2.9). 이슈 #1054 |
| `PreToolUse` 훅이 `allow`를 반환하든, `permissionOverrides`를 붙여 `ask`를 반환하든 허용되지 않은 호출은 통과시키지 못합니다. 반대로 `deny`는 허용된 호출까지 막습니다 | Observed (2026년 9월 19일, 24일). 미해결 이슈 #1053 |
| `decision: "allow"`와 함께 쓴 `overwrite`는 실제로 적용되고 에이전트에게도 그 사실이 알려지며, 권한 확인은 고쳐 쓴 인수를 기준으로 이루어집니다. `decision` 없이 쓴 `overwrite`는 거부로 처리됩니다 | Observed (2026년 9월 19일, 24일) |
| 훅이 명령을 거부했더라도, 최종 답변에는 그 명령이 출력했을 법한 결과가 적혀 있을 수 있습니다. 이런 실행 11번 중 6번은 답변이 프롬프트가 요구한 마커와 정확히 일치했지만, 트랜스크립트를 보면 명령은 한 번도 실행되지 않았습니다 | Observed (1.2.9) |
| 도구가 거부되면 그 턴의 작업은 통째로 버려지는데도, 실행 결과는 `"status": "SUCCESS"`에 종료 코드 0으로 보고됩니다. 측정된 가장 큰 손실은 완료된 단계 48개, 출력 토큰 20,595개였습니다 | Observed (1.2.7, 1.2.9에서 재확인). 미해결 이슈 #794 |
| 기본 설정의 헤드리스 실행은 `view_file`과 `search_web`은 허용 없이 쓰게 해 주지만, `run_command`와 `read_url_content`는 거부합니다. 빈 폴더에서 그 자체로 답할 수 있는 질문을 주었더니, 첫 호출로 그 폴더의 파일 목록을 셸로 조회한 경우가 이 플러그인이 있을 때 34번 중 30번, 없을 때 34번 중 21번이었고, 그런 실행은 하나같이 답변을 잃었습니다. `PreToolUse` 훅의 거부는 이 권한 확인보다 먼저 일어나므로, 훅이 `dir`을 거부한 경우에는 답변이 온전히 남았습니다 | Observed (1.2.11, 2026년 9월 26일·27일) |
| `--sandbox --dangerously-skip-permissions`는 워크스페이스 안에서 명령을 실행하고 워크스페이스 밖으로의 쓰기는 거부했지만, 읽기는 위치를 가리지 않고 허용했고 네트워크 접근도 허용했습니다. 실제로 두 실행이 자기 워크스페이스보다 두 단계 위 폴더에 있는 파일을 읽었습니다 | Observed (1.2.11, 2026년 9월 26일) |
| 헤드리스 실행에서 띄운 서브에이전트는 `read_file` 허용이 없으면 워크스페이스 파일에 대한 `read_file` 호출이 거부됩니다 | Observed (1.2.9) |
| 서브에이전트가 아직 실행 중인데 대기 중인 타이머도 없이 부모의 턴이 끝나면, 부모는 그 결과를 끝내 받지 못합니다. 실행은 자식 에이전트가 끝나기를 기다렸다가 종료되고, 로그에 "Failed to wake idle agent on message: run state not found"를 남긴 뒤 부모의 마지막 답변과 함께 `SUCCESS`를 보고합니다 | Observed (1.2.9, 통제된 실행 2번 중 2번과 감사 1번). 이슈 #1044. 1.2.16에서도 실행 1번에서 다시 나타남: 답변은 대기 안내 문장 한 줄뿐이었고, "Failed to wake" 줄은 로그에 없었으며, 메시지는 대화의 `messages/undelivered` 폴더에 그대로 남아 있었음 |
| `schedule`은 호출 즉시 반환됩니다. 일회성 타이머가 대기 중이면 헤드리스 실행은 타이머가 울리거나 취소될 때까지 종료되지 않고 살아 있습니다(stderr: `root agent idle; waiting up to 30m0s for 1 background task(s)`) | Observed (1.2.16, 2026년 10월 3일, `--sandbox --dangerously-skip-permissions` 사용). 대기 패턴은 `08-delegation.md`에 있으며, 기본 설정에서는 테스트하지 않음 |
| `send_message`를 호출하지 않고 끝난 서브에이전트는 자신의 마지막 답변을 발신자 `system` 명의의 메시지에 실어 부모를 깨웁니다. 그래서 그 서브에이전트의 ID를 지정한 `TimerCondition`은 취소되지 않습니다. 240초 타이머가 7번 중 7번 모두 끝까지 돌았고, 부모는 답변을 두 번 했습니다. 반면 자식 에이전트가 직접 보낸 `send_message`에는 자기 ID가 담기며, 이런 타이머를 3번 중 3번 모두 취소했습니다. `"any"`로 지정한 타이머는 8번 중 8번 모두 취소되었습니다 | Observed (1.2.16, 2026년 10월 3일, `--sandbox --dangerously-skip-permissions` 사용) |
| 텍스트도 도구 호출도 없는 턴은 거부되므로("model output must contain either output text or tool calls, these cannot both be empty"), 기다리기만 하는 턴이라도 짧게 한 줄은 말해야 합니다. 헤드리스 실행은 이 한 줄을 출력하고, 도구 호출과 함께 쓴 텍스트도 출력합니다 | Observed (1.2.16, Gemini 3.8 Flash): 턴을 조용히 끝내라고 지시한 실행 3번 중 2번에서 이 오류가 나옴 |
| 에이전트나 모델 API에서 실패가 나면 stderr에 `AGY_ERROR: {...}`를 출력하고 종료 코드 3으로 끝납니다 | Read: 1.2.6 변경 로그 |
| 헤드리스 `agy -p` 턴이 약 한 시간 시점에 `UNAUTHENTICATED (code 401)`로 끝났다. 긴 실행 2회 가운데 2회(28분, 61분)였고, 서브에이전트의 작업과 써 둔 파일은 온전했다. `agy -c`로 대화를 이어 갈 수 있었다 | Observed on 1.4.0, 2026년 10월 18일, `--sandbox` 사용. 출력과 보고서는 그 전에 쓰고, 이어 가기를 계획해 둔다 |

13분 동안 서브에이전트 7개를 돌린 어떤 보안 감사에서는 최종 답변이 "This request was blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related queries."라는 문구로 통째로 바뀌었습니다(observed: 1.2.9, `gemini-3.8-flash-high`). 헤드리스 실행은 명시적인 허용이나 `toolPermission`을 전제로 계획합니다. 훅의 승인에 기대서는 통과할 수 없고, `SUCCESS` 상태가 떴다고 해서 그 턴의 작업이 살아남았다는 증거가 되지는 않습니다.

## 훅

- `invocationNum`과 `executionNum`은 0부터 셉니다. 플러그인에 들어 있는 `hooks.json`도 로드되며, 호출 0번에서 주입한 `ephemeralMessage`를 모델이 그대로 따랐습니다(1.2.11).
- `Stop` 훅은 정상 종료를 문서에 나온 `model_stop`이 아니라 `terminationReason: "NO_TOOL_CALL"`로 알려 주며, 429 같은 오류(`"ERROR"`)가 났을 때도 실행됩니다. 이 훅이 `continue`를 반환하면 첫 번째 답변 뒤에 두 번째 답변이 덧붙고, JSON의 `response`에는 두 답변이 이어 붙은 채로 담깁니다. 오류가 난 뒤라면 재시도 루프에 다시 들어갑니다(1.2.11, 2026년 9월 26일).
- `hooks.json`의 명령에는 어떤 것도 따옴표로 감싸지 마십시오. Windows에서는 따옴표가 벗겨지지 않고 그대로 프로그램에 넘어갑니다. 그래서 따옴표로 감싼 실행 파일은 "not recognized" 오류가 나고, 따옴표로 감싼 스크립트 경로는 훅 폴더 경로 뒤에 덧붙여집니다(이슈 #222). 경로는 공백 없는 것으로 골라 따옴표 없이 쓰고, 파일은 JSON 직렬화 도구로 만듭니다. bash heredoc으로 쓰면 Windows 경로의 이중 백슬래시가 하나로 줄어들기 때문입니다. 훅은 `hooks.json`이 들어 있는 폴더에서 실행됩니다.
- `PreInvocation` 훅은 실패하면 그냥 건너뜁니다. 잘못된 JSON, 빈 출력, 0이 아닌 종료 코드, 타임아웃 모두 문제없이 넘어갔습니다(2026년 9월 19일). 반면 `PreToolUse` 훅은 실패하면 막는 쪽(fail closed)으로 동작합니다. 잘못된 JSON, `{}`, `decision` 누락, 0이 아닌 종료 코드는 모두 호출을 거부하고, 빈 출력일 때만 통과합니다(1.2.9). 타임아웃은 실제로 적용됩니다. 데스크톱 2.4.3부터는 실행할 수 없는 설정이 로드 시점에 오류와 함께 거부됩니다.
- `terminationBehavior: "force_continue"`에는 상한이 없습니다(미해결 이슈 #1055). 1.2.9에서 이 훅은 12번 실행되며 모델 호출을 11번 더 강제했는데, 그중 9번은 의미 없는 채움 답변이었고 2번은 아무도 요청하지 않은 도구를 호출했습니다. `Stop` 훅은 `decision: "continue"`로 종료를 막을 수 있으며, 횟수를 제한하는 데 쓸 수 있도록 `executionNum`을 전달받습니다. `10-iteration.md`를 참고합니다.
- 훅이 실제로 실행되는지 확인하려면 두 가지 장치를 함께 씁니다. 훅 스크립트가 센티널 파일에 내용을 덧붙이게 하고, 고유한 논스(nonce)와 함께 그 값을 그대로 되풀이하라는 지시를 주입하게 합니다. 그런 다음 두 결과를 모두 확인합니다. 파일이 유효하고 로그에 별다른 기록이 없다고 해서 훅이 실행되었다는 증거가 되지는 않습니다.

## 권한

허용(grant) 항목은 명령 문자열 그대로 저장되는데, 때로는 첫 토큰만 저장되기도 합니다. 그래서 `command(if)`나 `command(&)` 같은 항목이 생기는가 하면, 그 옆에는 몇 KB짜리 스크립트 전체가 허용 항목 하나로 통째로 저장되기도 합니다. 허용 항목은 바이트 하나까지 똑같은 명령에만 다시 적용되므로, 확인 창이 또 뜨고 쓸모없는 허용 항목이 하나 더 쌓입니다. 어떤 `~/.gemini/config/config.json`은 301 KB까지 불어났는데, 그중 97.5%가 쓸모없는 허용 항목이었고 36,331자짜리 항목도 하나 있었습니다. 이 파일의 크기는 가끔 확인합니다. 제 몫을 하는 것은 도메인 단위의 `read_url` 허용 항목입니다.

프로젝트 설정이 전역 설정보다 우선합니다. `~/.gemini/config/projects/*.json`의 파일마다 실행 정책을 따로 가질 수 있어서, 프로젝트 쪽에 다른 값이 지정되어 있는 동안에는 UI에서 전역 설정을 아무리 바꿔도 효과가 없습니다. 정책 값은 `always-proceed`, `request-review`, `strict`, `proceed-in-sandbox`이며, Windows에서는 데스크톱 2.15.1부터 파일·네트워크 샌드박스를 쓸 수 있습니다(read: 내장 `antigravity-guide` 스킬과 그 `app.md` 참조 문서, 변경 로그).

CLI는 허용 항목을 두 군데에서 읽습니다. 하나는 CLI 자체 `settings.json`의 `permissions.allow`이고, 다른 하나는 `~/.gemini/config/config.json`의 `globalPermissionGrants.allow`입니다. 두 번째 것을 읽었다는 사실은 로그의 `stored shared config permissions` 줄로 확인됩니다. Windows에서 `command()` 규칙이 일치하는 경우는 명령줄 전체와 정확히 같은 규칙, `command(*)`, 그리고 `command(regex:git .*)`처럼 줄 전체를 덮는 `regex:` 규칙뿐입니다. `command(git)`이나 `command(git *)`는 인수가 붙은 호출과는 하나도 일치하지 않습니다(observed: 1.2.9, 이슈 #619, #955). 모델에게 권한을 절대 묻지 말라고 지시하는 규칙은 효과를 낼 수 없습니다. 정책은 모델이 관여하기도 전에 적용되기 때문입니다.

## 실행 환경별 도구

agy 1.2.9의 기본 에이전트에서 뽑은 도구 목록에는 `ask_question`, `call_mcp_tool`, `define_subagent`, `generate_image`, `invoke_subagent`, `list_resources`, `manage_subagents`, `manage_task`, `read_resource`, `read_url_content`, `replace_file_content`, `run_command`, `schedule`, `search_web`, `send_message`, `view_file`, `write_to_file`이 있었고, 여기에 활성화된 MCP 서버의 도구가 더해졌습니다. 브라우저 도구는 없었습니다. 브라우저 도구는 데스크톱 앱에서 브라우저 연동을 켜면 나타나지만, 기록에 남은 데스크톱 실행 하나에는 그마저도 전혀 없었습니다. 그러니 계획을 세우기 전에 먼저 확인합니다. 대안은 `04-runtime-verification.md`에 있습니다.

그 밖에 알아 둘 만한 기능도 있습니다. `ask_question`은 대화형 세션에서 사용자에게 구조화된 질문을 던집니다. `/plan`은 실제로 만들기 전에 편집 가능한 계획 초안을 작성하며, Plan Review Policy 설정의 적용을 받습니다(데스크톱 2.17.0). `agy --effort low|medium|high`는 추론 강도를 정하고, `agy models`는 계정에서 쓸 수 있는 모델 목록을 보여 주며, `agy --agent <name>`은 커스텀 에이전트로 세션을 시작합니다.

## 스크립트로 오케스트레이션하기

수백 개 항목에 팬아웃을 돌리면서 개수를 정확히 세어야 한다면, 어떤 에이전트의 기억보다도 스크립트가 믿을 만합니다. SDK 플러그인 문서(버전 0.0.7)에 따르면 Google Antigravity Python SDK(`pip install google-antigravity`)를 쓰면 코드에서 에이전트와 서브에이전트를 띄울 수 있고, `SubagentConfig`, `enabled_tools`, `allowed_subagents`, `max_subagent_depth`, 그리고 구조화된 출력용 `response_schema`를 쓸 수 있습니다. 인증은 `GEMINI_API_KEY`로 하며, 비용도 Antigravity 요금제가 아니라 이 키로 청구됩니다. 이 방법은 이 스킬과 함께 테스트해 보지 않았으므로, 문서에는 나와 있지만 검증되지 않은 것으로 취급합니다.

## 실행 중인 플랫폼에서 직접 확인하기

위 항목 가운데 여럿이 공식 문서와 어긋나고, 이 결과를 얻은 테스트 도중에 CLI가 스스로 업데이트되기까지 했습니다. 플랫폼 동작이 작업에 영향을 준다면 설치된 버전에서 직접 테스트하고, 결과에 버전과 날짜를 적어 둡니다. 증거 등급 체계는 작업 결과물에 적용하는 것과 똑같이 플랫폼에도 적용됩니다.
