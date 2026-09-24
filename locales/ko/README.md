# Gravitas

[English](https://github.com/Emily2040/gravitas/blob/main/README.md) · [简体中文](https://github.com/Emily2040/gravitas/blob/main/README.zh-CN.md) · [日本語](https://github.com/Emily2040/gravitas/blob/main/README.ja.md) · **한국어**

이 파일은 설치 프로그램이 플러그인 안에 넣어 둔 README 사본입니다. 시험 결과와 다른 스킬과의 비교까지 담은 전체 버전은 [GitHub](https://github.com/Emily2040/gravitas)에 있으며, 베타 기간에는 비공개입니다.

## 1부: 방금 설치한 것

Gravitas는 Antigravity 에이전트가 끝났다고 말하기 전에 먼저 자기 작업을 증명하게 합니다.

AI 에이전트는 일의 쉬운 부분만 확인하고, 거기에 문제가 없으니 일 전체가 괜찮다고 보고할 수 있습니다. 시험에서 가장 흔한 실수는 에이전트가 열어 보지도 않은 자료를 읽었다고 말하는 것이었습니다. Gravitas는 에이전트에게 세 가지 습관을 줍니다.

1. 어떻게 아는지 말하기. 모든 주장에 표시가 붙습니다. 직접 봤다, 직접 실행했다, 읽었고 해당 줄은 이것이다, 또는 추론했거나 기억해 냈다.
2. 옆에 있는 쉬운 것 말고 진짜를 확인하기.
3. 다른 누군가가 깨뜨려 보게 하기. 별도의 검사 에이전트가 실수와 빈틈을 찾으며, 이들에게는 파일을 편집하는 도구가 없습니다.

예를 들어, 10,000명 중 1명꼴로 생기는 질환을 “정확도 99%”인 검사로 검사해 양성이 나오면 그 질환이 있을 확률이 99%라고 말하고 맞는지 확인해 달라고 했을 때, Gravitas는 아니라고 답했습니다. 실제 수치는 약 102명 중 1명입니다. 계산 과정을 보여 주었고, 계산한 숫자마다 여러분이 직접 실행해 볼 수 있는 명령을 붙였습니다.

틀리면 대가가 따르는 작업에서는 저절로 켜집니다. 감사, 디버깅, 여러 파일에 걸친 변경, 디자인 작업, 리서치, 법률, 의학, 수학, 금전, 역사입니다. 빠른 질문에는 빠르게 답합니다.

확인을 거친 답은 빠른 답보다 오래 걸리고 요금제 사용량도 더 씁니다. 위의 예는 약 100초, 작은 프로젝트의 전체 감사는 약 6분이 걸렸습니다. 모델을 더 똑똑하게 만들 수는 없고, 아무도 확인할 수 없는 것을 확인할 수도 없습니다. 대조할 것이 없으면 그 주장을 추론으로 표시합니다. 비공개 베타이며, Windows 11에서 Google의 Gemini 모델로 시험했습니다.

끄려면 Antigravity가 플러그인용으로 문서화한 명령인 `agy plugin disable gravitas`를 실행하고, 다시 켜려면 `agy plugin enable gravitas`를 실행하세요. 문제를 알리려면 작성자의 [GitHub 프로필](https://github.com/Emily2040)에 있는 링크를 쓰세요.

## 2부: 이 폴더에 든 것

```text
plugin.json                  manifest: the name and description Antigravity lists
rules/AGENTS.md              always-on rule: when to load the skill, and three rules that hold while it is in use
agents/                      eight agents with fixed tool lists
skills/gravitas/SKILL.md     the router; it loads references/00-orchestrator.md
skills/gravitas/references/  fourteen modules, each 100 lines or fewer so one view_file call reads it whole
skills/gravitas/schemas/     the finding and verdict records subagents return
skills/gravitas/scripts/     ledger.py, provenance_check.py, check_skills.py, slopcheck.py
skills/gravitas/examples/    a gate suite that goes red on the scene it was built from
```

실행은 이렇게 진행됩니다. 규칙은 항상 로드되어 있습니다. 해당하는 작업이면 에이전트가 스킬을 열고, 스킬은 오케스트레이터로 안내합니다. 오케스트레이터는 사소한 질문에는 바로 답합니다. 그렇지 않으면 작업 기록을 쓰고, 팬아웃, 투표, 멈춤 조건의 수치가 정해진 규모(quick, standard, full, exhaustive) 하나를 고르고, 불러올 모듈을 지정합니다. 작업 목록은 실제 도구로 만듭니다. 전문 에이전트는 절대 경로와 반환 스키마를 받아 팬아웃하고, 결론을 떠받치는 주장은 독립 검증으로 가며, 완결성 비평가는 한 번도 확인하지 않은 것을 지목합니다. 마지막으로 보고서가 발견을 등급, 빈틈과 함께 순위대로 정리합니다.

| 등급 | 반드시 일어났어야 하는 일 |
| :--- | :--- |
| `observed` | 결과물 자체를 살펴보았고, 표시가 그 결과물을 밝힌다 |
| `executed` | 도구가 실행되어 값을 반환했고, 표시가 명령이나 쿼리와 그 반환값을 보여 준다 |
| `read` | 출처를 가져왔고, 표시가 URL이나 경로를 적고 해당 줄을 인용한다 |
| `inferred` | 추론이나 기억. 칸을 채울 수 없는 모든 것 |

어떤 에이전트에도 파일 편집 도구는 없습니다. checker 에이전트는 명령을 실행할 수 있지만 검토 중인 작업을 절대 수정하지 말라는 지시를 받고, 문체 편집 에이전트는 고친 글을 파일에 쓰지 않고 돌려줍니다.

| 에이전트 | 역할 | 도구 |
| :--- | :--- | :--- |
| `gravitas-scout` | 파일, 경로, 심볼, 출처를 찾는다 | `list_dir`, `find_by_name`, `grep_search`, `view_file` |
| `gravitas-reader` | 이름을 댄 파일이나 URL에 관한 질문에 답하고 해당 줄을 인용한다 | `view_file`, `grep_search`, `find_by_name`, `list_dir`, `read_url_content` |
| `gravitas-finder` | 작업 목록 전체에서 한 종류의 결함을 찾는다 | 읽기 담당의 도구와 `search_web` |
| `gravitas-checker` | 독립 검증 하나를 실행한다 | `view_file`, `run_command` |
| `gravitas-refuter` | 주장 하나의 반박을 시도하며, 기본 판정은 반박됨 | `view_file`, `grep_search`, `read_url_content`, `search_web` |
| `gravitas-visual-critic` | 소스를 보지 않은 관찰자로서 스크린샷을 판단한다 | `view_file` |
| `gravitas-completeness-critic` | 한 번도 탐색, 열람, 실행, 검증되지 않은 것을 지목한다 | `view_file`, `list_dir`, `grep_search`, `find_by_name` |
| `gravitas-prose-editor` | 초안을 문체 기준에 맞게 고친다 | `view_file` |

스크립트는 이 폴더에서 실행합니다. `--latest`는 가장 최근 대화를 기준으로 확인합니다. 대화 ID는 `~/.gemini/antigravity-cli/brain/` 아래의 폴더 이름이거나, `agy -p --output-format json` 출력의 `conversation_id`입니다.

```bash
python skills/gravitas/scripts/check_skills.py          # validate every skill, agent, rule and plugin under ~/.gemini/config
python skills/gravitas/scripts/provenance_check.py <answer> --latest   # check evidence labels against the transcript
python skills/gravitas/scripts/ledger.py --help         # bookkeeping for fan-outs: dedupe, votes, dry rounds
python skills/gravitas/scripts/slopcheck.py <files>     # structural markers of generated prose; --strict fails on any flag
```

지금까지의 시험 결과는 이렇습니다. 베타 2 시험에서 나온 답변에 대해, 출처 검사기는 출처를 연 법률 답변의 표시 6개를 모두 통과시켰고 한 번도 열지 않은 인용은 불합격시켰습니다. 전체 감사 시험 사례는 심어 둔 결함 3개를 모두 찾았습니다. Antigravity 단독과의 깔끔한 비교는 아직 없으며, 그 벤치마크가 다음 작업입니다.

한계도 있습니다. 방법의 대부분은 모델에게 따르라고 요구하는 지시입니다. 도구 목록과 스크립트 4개가 기계적인 부분이고, 스크립트는 에이전트가 실행하라는 지시를 받을 때 실행됩니다. Windows 11의 agy 1.2.9에서 시험했습니다. 사용 방식에 영향을 주는 플랫폼 동작은 `skills/gravitas/references/13-platform.md`에 있습니다. 가장 중요한 것은 두 가지입니다. 헤드리스 `agy -p` 실행에는 명시적인 권한 부여나 `~/.gemini/antigravity-cli/settings.json`의 `toolPermission` 설정이 필요합니다. 그리고 CLI는 저장소를 `--add-dir`로 넘겼을 때만 저장소 자체의 `.agents/` 폴더를 읽는데, 이 플러그인이 전역으로 설치되는 것도 그 때문입니다.

버전 1.0.0-beta.2 · MIT · 만든 사람 [Iamemily2050](https://github.com/Emily2040)
