# Gravitas

[English](./README.md) · [简体中文](./README.zh-CN.md) · [日本語](./README.ja.md) · **한국어**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-private_beta.2-purple.svg)](#상태)
[![Platform](https://img.shields.io/badge/Antigravity-2.17.0_%7C_agy_1.2.9-blueviolet.svg)](https://antigravity.google/)
[![Languages](https://img.shields.io/badge/languages-en_%7C_zh--CN_%7C_ja_%7C_ko-green.svg)](#언어)
[![Validation](https://img.shields.io/badge/Validation-check__skills-blueviolet.svg)](#검증)

**Google Antigravity를 위한 검증 및 조율 플러그인: 모든 주장에 붙는 증거 등급, 대리 지표 탐지, 읽기 전용 검증 에이전트, 팬아웃 원장, 출처 검사기, 그리고 측정 가능한 문체 기준.**

![Gravitas 캐릭터 시트](docs/assets/gravitas-hero.jpg)

---

## 상태

비공개 베타 2, 2026년 9월 24일 출시. 원칙은 안정되었고, 플랫폼에 관한 결론은 Antigravity 데스크톱 2.17.0과 agy CLI 1.2.9에서 다시 검증했습니다. 시험 결과가 요구하면 스킬은 지금도 바뀝니다. 고정된 버전이 필요하면 커밋을 지정하고, 업데이트 전에 [CHANGELOG.md](CHANGELOG.md)를 읽으십시오.

## 왜 필요한가

어느 분야에서든 질 나쁜 에이전트 출력의 대부분은 세 가지 실패에서 나옵니다.

| 실패 | 나타나는 모습 | Gravitas가 하는 일 |
| :--- | :--- | :--- |
| 그럴듯한 불완전함 | 에이전트가 문제의 일부를 살펴보고, 진짜인 무언가를 찾고, 멈춘다. 발견은 맞고 범위는 그렇지 않다. | 팬아웃 전에 작업 목록을 찾고, 보고 전에 완결성 비평을 실행한다 |
| 합의된 환각 | 여러 에이전트가 같은 자료를 읽고 같은 틀린 결론에 이른다. 오류가 서로 상관되어 있기 때문이다. | 모든 주장을 그 뒤의 독립 검증으로 등급을 매기고, 동의를 증거로 세지 않는다 |
| 기계적인 말투 | 작업은 맞는데 생성된 것처럼 읽혀서, 누가 확인하기도 전에 버려진다. | 모든 결과물을 `slopcheck.py`가 측정하는 문체 기준에 맞춘다 |

이것은 코딩 전용 스킬이 아닙니다. 같은 규율이 법률, 수학, 물리, 의학, 통계, 역사, 그리고 일상적인 사실 질문에도 적용됩니다. 분야에 따라 달라지는 것은 쓸 수 있는 독립 검증의 종류이며, 거의 모든 분야에 적어도 하나는 있습니다.

## 하는 일

| 단계 | 만들어 내는 것 |
| :--- | :--- |
| 분류 | 어떤 장치도 돌리기 전에 사소한 질문에는 바로 답한다는 결정 |
| 작업 기록 | 계획 전에 적어 두는 결과의 무게, 결과물, 검증 가능한 표면, 빠진 입력, 쓸 수 있는 도구 |
| 규모 | quick, standard, full, exhaustive 중 하나이며, 팬아웃, 표, 멈춤의 수가 정해져 있다 |
| 범위 | 추측이 아니라 실제 도구로 만든 작업 목록 |
| 팬아웃 | 항목이나 차원마다 읽기 전용 전문 에이전트 하나. 절대 경로와 반환 스키마를 준다 |
| 검증 | 모든 주장을 증거 등급에서 갈 수 있는 가장 높은 곳까지 올리고, 위임한 모든 주장을 서브에이전트의 트랜스크립트와 대조한다 |
| 비평 | 새 에이전트가 한 번도 탐색하지 않은 각도와 검증하지 않은 주장을 지목한다 |
| 보고 | 심각도순 발견에 등급, 빈틈, 상한, 실패한 모든 서브에이전트를 붙인다 |

## 증거 등급

모든 주장에는 등급 표시가 붙고, 모든 표시는 그것을 만든 것을 밝힙니다.

| 등급 | 반드시 일어났어야 하는 일 | 해당하지 않는 것 |
| :--- | :--- | :--- |
| `observed` | 결과물 자체를 살펴보았다 | 계산. 살펴볼 것이 제공되지 않았을 때의 모든 것 |
| `executed` | 도구가 실행되어 값을 반환했고, 그 명령을 보여 줄 수 있다 | 암산. 가정한 입력에 대한 실제 계산 |
| `read` | 출처를 가져왔고 의존하는 줄을 인용할 수 있다 | 알아보는 출처. 기억으로 쓴 정확한 인용 위치. 출처에 관한 페이지 |
| `inferred` | 자신의 추론과 기억해 낸 모든 것 | |

`observed`는 결과물을, `executed`는 명령을 보여 주고, `read`는 URL을 대고 줄을 인용하며, 칸을 채울 수 없는 표시는 `inferred`입니다. 이 규칙의 이전 두 버전은 단순한 금지였고, 테스트 사례 22개에서 둘 다 동작을 바꾸지 못했습니다. 표시에 URL, 명령, 파일 이름을 반드시 넣게 하자 달라졌습니다. 실제로 가져오지 않았다면 그 칸을 채울 수 없기 때문입니다.

베타 2는 이 칸을 두 곳에서 기계적으로 확인합니다. 팬아웃 원장은 출처가 빈 기록을 강등합니다. `provenance_check.py`는 답변의 모든 표시를 대화의 트랜스크립트와 대조하여, URL을 한 번도 열지 않은 `read` 표시(검색 요약에서 가져온 것 포함)와 명령이 한 번도 실행되지 않은 `executed` 표시를 불합격시킵니다.

## 대리 지표의 함정

진짜 질문은 확인하기 어렵고 바로 옆의 질문은 확인하기 쉬울 때, 확인되는 것은 쉬운 쪽입니다. 그것이 통과하고, 작업은 “검증됨”으로 보고됩니다.

| 정말 중요한 질문 | 실제로 확인되는 대리 지표 |
| :--- | :--- |
| 이 장면이 초콜릿 공장처럼 보이는가 | 캐리어 10개와 롤러 6개가 있는가 |
| 이 계약이 내가 주장하는 의무를 만드는가 | *indemnify*라는 단어가 있는가 |
| 이 증명은 옳은가 | 모든 줄의 형식이 올바른가 |
| 이 연구가 주장을 뒷받침하는가 | 인용된 논문이 존재하는가 |
| 이 페이지는 접근성이 있는가 | Lighthouse 점수가 100인가 |
| 이 플랫폼 기능이 작동하는가 | 문서에 적혀 있는가 |

판별법은, 정말 신경 쓰는 것이 거짓일 때도 그 검증이 통과할 수 있는지입니다. 통과할 수 있다면 대리 지표입니다. 그대로 두되 옆에 진짜 검증을 추가합니다.

## 검증 에이전트

플러그인에는 사용자 지정 에이전트 여덟 개가 들어 있습니다. 판단하는 역할은 모두 편집 도구가 없으므로, 비평가가 잘못 진단한 것을 고치고 성공을 보고할 수 없습니다. 각 에이전트는 `inheritCustomizations: false`와 `inheritMcp: false`를 설정해 사용자의 규칙, 스킬, MCP 서버를 컨텍스트 밖에 두며, 상대 경로는 추측하지 않고 거부합니다.

| 에이전트 | 하는 일 | 도구 | 모델 |
| :--- | :--- | :--- | :--- |
| `gravitas-scout` | 파일, 경로, 심볼, 출처를 찾는다 | `list_dir`, `find_by_name`, `grep_search`, `view_file` | flash |
| `gravitas-reader` | 지정한 파일이나 URL에 대한 구체적 질문에 답하고 줄을 인용한다 | 읽기 도구, `read_url_content` | flash |
| `gravitas-finder` | 작업 목록에서 한 종류의 결함을 찾는다 | 읽기 도구, `read_url_content`, `search_web` | flash |
| `gravitas-checker` | 독립 검증 하나를 실행한다: 계산, 테스트, 쿼리 | `view_file`, `run_command` | flash |
| `gravitas-refuter` | 주장 하나의 반박을 시도하고, 기본값은 반박됨 | 읽기 도구, `read_url_content`, `search_web` | pro |
| `gravitas-visual-critic` | 소스를 보지 않은 관찰자로서 캡처를 판단한다 | `view_file` | pro |
| `gravitas-completeness-critic` | 한 번도 탐색, 열람, 실행, 검증되지 않은 것을 지목한다 | 읽기 도구 | pro |
| `gravitas-prose-editor` | 초안을 문체 기준에 맞게 고친다 | `view_file` | pro |

## 왜 Antigravity 전용인가

조율에 관한 조언 대부분은 텍스트와 파일뿐인 도구 환경을 가정합니다. Antigravity의 환경은 더 넓습니다. 브라우저 스크린샷, 콘솔 수집, 네트워크 검사, 실시간 JavaScript 실행, 이미지 생성, 도구 목록이 고정된 사용자 지정 에이전트, 그리고 스킬, 에이전트, 규칙을 함께 담는 플러그인 체계가 있습니다. 스크린샷을 보는 비평가는 겹친 요소, 잘린 텍스트, 부족한 명암비, 400 px에서 무너지는 레이아웃, DOM에는 있지만 보이지 않는 컨트롤을 잡아냅니다. 코드를 읽는 사람에게는 어느 것도 보이지 않습니다.

## 빠른 시작

**macOS / Linux:**

```bash
git clone https://github.com/Emily2040/gravitas.git
cd gravitas
bash scripts/install.sh ko
```

**Windows PowerShell:**

```powershell
git clone https://github.com/Emily2040/gravitas.git
cd gravitas
pwsh scripts/install.ps1 ko
```

둘 다 `scripts/install.py`를 실행합니다. 저장소를 검증하고, `plugin/`을 `~/.gemini/config/plugins/gravitas/`로 복사하고, 결과를 검증합니다. 예전에 스킬 단독으로 `~/.gemini/config/skills/gravitas`에 설치한 버전과 그 `gravitas-always-on` 훅은 날짜가 붙은 백업 폴더로 옮겨집니다. 그다음 Antigravity를 다시 시작하거나 CLI에서 `/skills reload`를 실행합니다. Python 3.8 이상이 필요합니다.

전역으로 설치하십시오. 문서가 뭐라고 하든 CLI는 워크스페이스의 `.agents/` 폴더를 읽지 않습니다(open issue #1052).

## 저장소 구성

```text
plugin/                                   # ~/.gemini/config/plugins/gravitas/ 로 설치
├── plugin.json                           # 플러그인 매니페스트
├── rules/AGENTS.md                       # 상시 규칙: 스킬을 불러올 때와 세 가지 핵심 규칙
├── agents/                               # 읽기 전용 검증 에이전트 8개, scripts/build_agents.py 가 생성
└── skills/gravitas/
    ├── SKILL.md                          # 라우터(500자 미만), references/00-orchestrator.md 를 불러옴
    ├── references/                       # 00~13 모듈 14개, 모두 100줄 미만
    ├── schemas/                          # 발견 기록과 판정 기록
    ├── scripts/                          # ledger.py, provenance_check.py, check_skills.py, slopcheck.py
    └── examples/gates.example.js         # 바탕이 된 장면에서 빨간불이 켜지는 게이트 모음
locales/{zh-CN,ja,ko}/                    # 번역된 스킬과 규칙
scripts/                                  # install.py 와 래퍼, build_agents.py
tests/audit-case/                         # 결함 세 개를 심은 감사 시험 사례
```

## 검증

편집할 때마다 검증 도구를 실행합니다. Antigravity는 망가진 스킬을 순환 로그에 한 줄 남기는 것으로만 건너뛰며, 문서는 매핑되지 않은 도구 이름이 사용자 지정 에이전트를 멈추게 할 수 있다고 경고합니다.

```bash
python plugin/skills/gravitas/scripts/check_skills.py --repo   # 이 저장소
python plugin/skills/gravitas/scripts/check_skills.py          # ~/.gemini/config 아래 설치된 모든 것
python plugin/skills/gravitas/scripts/slopcheck.py <files>     # 생성된 글의 구조적 표지
python plugin/skills/gravitas/scripts/provenance_check.py <answer> --conversation <id>   # 표시를 트랜스크립트와 대조
```

`check_skills.py`는 프런트매터, 바이트 순서 표시, 설명 길이, 끊어진 참조, 100줄이 넘는 모듈, 에이전트 도구 이름, 쓰기 도구를 가진 비평가, 24,000바이트가 넘는 규칙 파일을 확인합니다. 사용자 지정 항목의 로드를 막을 문제가 있으면 종료 코드 1을 반환합니다. 모든 검사는 믿기 전에, 일부러 망가뜨린 플러그인에서 실패하는 것을 지켜보았습니다.

## 시험 방법

베타 1은 지식 작업과 공예에 걸친 사례 22개로 `gemini-3.8-flash-high`에서 시험했습니다. 모든 사례에 미끼로서의 대리 지표가 있고, 과잉 작동을 막는 대조군이 두 개 있습니다. 프롬프트와 정답은 [TESTS.md](TESTS.md)에 있습니다.

베타 2는 2026년 9월 24일 데스크톱 2.17.0과 agy 1.2.9에서 헤드리스로 시험했으며, 임시 권한 부여를 쓰고 나중에 되돌렸습니다. 설계를 바꾼 결과는 다음과 같습니다.

- 에이전트 여덟 개가 모두 시작해 결과를 돌려주었습니다. 반박자는 만들라는 파일을 만들지 못했고, 시각 비평가는 `view_file`로 PNG를 읽고 빨간 사각형, 파란 원, 그리고 삼각형은 없다고 정확히 보고했습니다.
- 서브에이전트는 상대 경로를 모든 CLI 대화가 함께 쓰는 임시 폴더를 기준으로 해석합니다. “현재 워크스페이스의” `draft.md`를 편집하라는 말을 들은 문체 편집자는 닷새 전 시험의 오래된 `draft.md`를 편집했고, 오류도 내지 않았습니다. 이제 모든 프롬프트와 모든 에이전트는 절대 경로를 씁니다.
- `inheritCustomizations: false`가 없으면, 3단계 만에 답을 찾은 읽기 담당이 35초를 더 들여 이 스킬을 불러왔습니다. 넣자 같은 작업이 63초에서 40초로 줄었습니다.
- `view_file`은 호출 한 번에 100줄을 돌려주며, 한 실행에서 에이전트는 114줄 모듈의 처음 100줄을 읽고 넘어갔습니다. 이제 모든 모듈은 100줄 미만입니다.
- 시험 도중 CLI가 1.2.7에서 1.2.9로 스스로 업데이트되었습니다. 그래서 `13-platform.md`의 날인은 모두 해당 실행 자체의 로그에서 가져왔습니다.
- 검색 요약이 인용으로 세탁되었습니다. 두 답변이 `search_web` 요약에만 나온 페이지를 `read`로 표시했고, 하나는 가져온 어떤 내용에도 없는 문서 번호를 댔습니다. `provenance_check.py`는 이 사례들에서 만들어졌습니다. 다섯 답변에 대해, 출처를 모두 연 법률 답변의 표시 6개는 모두 통과시켰고 세탁된 것은 모두 불합격시켰습니다.
- 전체 규모 감사 사례(`tests/audit-case/`)는 심어 둔 결함 세 개와, 그중 하나를 담은 테스트를 모두 찾았습니다. 첫 실행은 13분 뒤 안전 필터 차단으로 보고서를 잃었고, 탐색자들은 스키마 파일을 찾느라 범위 밖 파일을 읽으며 60~127단계를 썼습니다. 스스로 완결된 에이전트로 바꾼 재실행에서는 탐색자와 반박자가 각각 4~8단계로 범위 안에 머물렀고, 발견 9개가 각각 3표로 중복 없이 살아남았습니다. 재실행은 그 뒤 완결성 비평가가 아직 일하는 중에 일찍 끝났기 때문에, 이제 스킬은 부모에게 폴링을 계속하고 보고서를 먼저 쓰라고 지시합니다.

## 담고 있는 플랫폼 제약

| 제약 | 세부 |
| :--- | :--- |
| CLI는 워크스페이스 `.agents/`를 읽지 않는다 | 스킬, 에이전트, 훅 모두. open issue #1052 |
| 상대 경로가 공유 임시 폴더를 기준으로 해석된다 | 같은 이름의 오래된 파일이 오류 없이 열린다 |
| 긴 스킬 설명은 빠진다 | 스킬 133개 중 3개가 사용자 지정 예산에서 제외되었고, 모두 가장 긴 5개에 들었다 |
| 거부된 도구 하나가 헤드리스 턴 전체를 버린다 | `status: SUCCESS`, 종료 코드 0. 측정한 최대 손실: 48단계와 출력 토큰 20,595개. open issue #794 |
| 헤드리스에서는 `autoExecutionPolicy: AUTO`가 무시된다 | `allow`를 반환하는 `PreToolUse` 훅도 허용하지 않는다. open issue #1054 |
| `force_continue`에 상한이 없다 | 3회, 8회, 12회의 계속을 측정. open issue #1055 |
| 권한이 명령 문자열 그대로 저장된다 | 쌓여 가고 거의 다시 일치하지 않는다. 한 설정은 301 KB에 이르렀고 97.5%가 쓸모없었다 |

세부, 버전, 날짜는 `plugin/skills/gravitas/references/13-platform.md`에 있습니다.

## 루프 규칙의 근거가 된 연구

반복은 출력을 확실히 개선하지 않습니다. 루프 규칙은 아래 공개된 결과를 따릅니다.

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- *The Self-Correction Illusion: LLMs Correct Others but Not Themselves*. https://arxiv.org/pdf/2606.05976
- Shinn et al., *Reflexion*. https://arxiv.org/abs/2303.11366
- Madaan et al., *Self-Refine*. https://dl.acm.org/doi/10.5555/3666122.3668141

## 언어

스킬과 규칙은 영어, 중국어 간체, 일본어, 한국어로 불러올 수 있습니다. 설치 프로그램에 언어 코드를 넘기면 됩니다. 모든 모듈을 한 줄씩 빠짐없이 번역했으므로, 번역된 모듈도 영어판과 똑같이 100줄 창에 들어갑니다. 네 가지 등급 이름은 모든 언어에서 영어로 유지합니다. 글로 쓰는 것이 아니라 에이전트가 내보내는 표시이기 때문입니다. 검증 에이전트는 모든 언어에서 영어입니다. 그 출력은 독자가 아니라 부모 에이전트에게 돌아가기 때문입니다.

## Gravitas

2등신. 토성 고리 머리핀. 무거운 것을 좋아하고, 둥둥 떠내려가는 것은 싫어함.

> Heavy things are happier together.

작은 몸, 큰 중력. 대략 이 스킬이 주장하는 바이기도 합니다. 주장은 얼마나 자신 있게 말했는지가 아니라 뒤에 있는 증거로 순위가 매겨집니다.

캐릭터: [@iamemily2050](https://iamemily2050.com).

## 만든 사람

**Iamemily2050**이 만들었습니다

- [GitHub](https://github.com/Emily2040)
- [웹사이트](https://Iamemily2050.com)
- [X / Twitter](https://x.com/iamemily2050)
- [Instagram](https://www.instagram.com/iamemily2050)

## 라이선스

[MIT](LICENSE) — Copyright (c) 2026 Iamemily2050
