# 모듈 06 - 지각 게이트

## 목적

이 모듈은 보는 사람만 답할 수 있는 검증을 다룹니다. 대상은 사람이 보게 될 모든 것, 즉 장면, 페이지, 차트, 생성 이미지, 조판된 문서입니다. 작업에 시각적 결과가 있으면 `05-acceptance.md`와 함께 불러옵니다. 이 모듈의 바탕이 된 사례는 그곳에 설명된 초콜릿 공장입니다.

## 스크린샷은 검증이 아니다

초콜릿 공장 실행은 보고서에 PNG 8장을 첨부했습니다. 그것들이 뒷받침한 게이트는 모두 기하를 측정했습니다. UUID 유지, 메시 수, `Y = 1.084 m`에서의 그리퍼 간격, 0.1 mm 미만의 사이클 경계 오차였습니다. 모두 사실이었고, 그런데도 장면은 이상해 보였습니다. 이미지가 제대로 보이는지 묻는 것은 아무것도 없었습니다. 스크린샷은 판단할 이미지가 아니라 스크립트가 실행되었다는 증거로 철해졌습니다.

이 실패가 매력적인 이유는 숫자와 통과로 가득한 문서가 만들어지고, 직접 보는 것보다 더 엄밀하게 느껴지기 때문입니다. 하지만 그것은 다른 질문에 답합니다.

| | 기하 검증 | 지각 검증 |
| :--- | :--- | :--- |
| 질문 | 요소가 있고, 위치와 크기가 맞는가 | 제대로 보이는가 |
| 방법 | 장면 그래프나 DOM에 대한 스크립트 단언 | 모델이 이미지를 보고 판단 |
| 잡아내는 것 | 누락된 노드, 잘못된 변환, 개수 변화 | 밋밋한 조명, 플라스틱 같은 재질, 알아볼 수 없는 형태 |
| 잡아내지 못하는 것 | 외관에 관한 모든 것 | 정확한 값에 관한 모든 것 |

지각 검증은 스크립트로 만들 수 없습니다. 새로운 비평가 앞에 이미지를 놓고, 그것이 어떻게 보이는지 묻는 질문이 필요합니다.

## 지각 게이트

사람이 보게 될 모든 것에는 보는 사람만 답할 수 있는 게이트를 추가합니다. `gravitas-visual-critic`에 캡처와 의도를 주고 구체적인 답을 요구합니다.

“보기 좋은가”는 동의를 부를 뿐입니다. 다음 질문들은 틀릴 수 있는 답을 끌어냅니다.

- 주요 표면 각각이 어떤 재질로 보이는지 말해 주십시오. 브리프에는 구리, 법랑 강철, 황동이라고 되어 있습니다. 무엇이 보입니까?
- 초콜릿을 가리켜 주십시오. 이 이미지에서 찾을 수 없다면 그렇다고 말해 주십시오.
- 보이는 빛의 방향이 있습니까? 그 방향을 말해 주십시오. 조명이 밋밋해 보이면 밋밋하다고 말해 주십시오.
- 질감, 마모, 변화가 없는 표면을 모두 나열해 주십시오.
- 브리프를 읽어 본 적 없는 사람이 이것을 초콜릿 공장으로 알아보겠습니까? 대신 무엇이 보입니까?

비평가는 보는 사람으로서 답하며 소스를 읽지 않습니다. 코드를 읽은 비평가는 이미지가 아니라 의도를 묘사하기 때문입니다. 가장 유용한 질문 하나는 “이것은 무엇으로 만들어진 것처럼 보이는가”입니다. 플랫 셰이딩된 기본 도형으로 만든 장면은 재질 설정이 무엇이라 주장하든 “플라스틱 블록”이라는 답을 받습니다.

## 만들기 전에 목표를 명시하기

그 실행의 계획은 구체적이었습니다. 거칠기 0.20, 클리어코트 0.85의 `#941c33` 라즈베리색 법랑, 강도 2.8의 3500 K 할로겐 키 라이트, 절차적 타일 줄눈. 이것들은 진짜 인수 기준이었지만 하나도 게이트가 되지 않았습니다. 계획은 외관을 묘사했고, 테스트 모음은 위치를 측정했습니다.

계획에 적힌 재질과 조명 사양은 모두 작성되기를 기다리는 지각 게이트입니다. 계획에 클리어코트 0.85라고 되어 있으면, 게이트는 표면이 칠해진 것처럼 보이는지 묻습니다. 특정 위치의 3500 K 키 라이트를 지정했다면, 게이트는 보는 사람이 빛의 방향과 따뜻함을 알아볼 수 있는지 묻습니다.

## 콘솔 출력도 게이트다

같은 장면은 r186에서 제거된 `THREE.PCFSoftShadowMap`을 요청했습니다. 렌더러는 하드 섀도로 대체했고, 그 사실을 콘솔에 남겼습니다.

```text
THREE.WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead.
```

아무것도 실패하거나 멈추지 않았습니다. 그림자는 계획이 요구한 것이 아니었고, 그 실행은 콘솔 수집을 연결해 두고도 읽지 않았습니다. 사용 중단 경고는 얻을 수 있는 가장 싼 결함 신호입니다. 코드가 호출하는 API를 지목하는 경고는 누군가 분류하기 전까지 실패로 다룹니다.

## 빨간불이 켜지는 실제 예

`examples/gates.example.js`는 이 규칙에 따라 작성되어 위 장면을 대상으로 실행된 Playwright 게이트 모음입니다. 6개 중 4개를 통과하고 종료 코드 1로 끝납니다.

```text
PASS  G1  Zero console errors
FAIL  G2  No deprecation warning for an API this code calls
          THREE.WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead.
FAIL  G3  Shadow map enabled and not the hard fallback (type !== 1)
          enabled=true type=1
PASS  G4  Under 90% of materials are untextured
          153/193 materials have no map (79.3%)
PASS  G5  Component counts match the brief
PASS  G6  SELF-TEST: an injected wrong value is detected by G5 logic
```

G6는 규칙이 요구하는 자체 시험입니다. 잘못된 값을 주입하고 비교가 그것을 잡아내는지 확인하므로, 이 모음은 빨간불이 켜질 수 있음을 보여 주었습니다. 원래의 모음에서는 같은 장면이 `ALL TEST GATES PASSED SUCCESSFULLY`라고 보고했습니다.

그다음 지각 게이트를 따로 실행했습니다. 스크린샷만 받고 소스는 받지 않은 새 에이전트가 수행했습니다(아래는 원문 인용).

> **Chocolate: Absent.** The mold cavities are completely white and empty; there is no liquid chocolate, bar, or brown confectionery substance visible anywhere on the line.
>
> **Lighting: Flat.** No directional cast shadows, no specular hot spots.
>
> **What it looks like it is made of:** injection-molded matte toy plastic and raw CAD primitives.

원래 모음이 같은 대상에 둔 게이트는 이렇게 적혀 있었습니다. “Hero Chocolate Identity Persistence - PASS. Exactly 1 mesh throughout; UUID persists across all phases.” 메시는 장면 그래프에 존재하지만 렌더링에서는 보이지 않습니다. 어떤 기하 게이트도 이 간극을 메울 수 없으며, 그래서 지각 게이트가 존재합니다.
