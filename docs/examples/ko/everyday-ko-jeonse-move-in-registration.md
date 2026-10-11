# Gravitas가 더 못했던 경우: 전세 잔금일의 전입신고

이 사례는 Gravitas가 도움이 되지 않았고, 오히려 더 못했던 경우입니다.

## 질문 (원문 그대로)

````text
다음 달에 전세로 이사 가는데 하나만 확인 좀 해주세요.
보증금 3억이고 잔금 치르고 입주하는 날이 10월 16일 금요일이에요. 확정일자는 계약서 쓴 날 주민센터 가서 미리 받아놨고요.
전입신고는 이사하고 14일 안에만 하면 된다고 해서, 주말에 짐 정리 좀 하고 그 다음 주 수요일(21일)에 반차 내고 주민센터 가서 하려고 하는데요. 이렇게 해도 별 문제 없죠?
````

## 사용한 모델과 채점 결과

- **답변 모델:** Gemini 3.1 Pro (high), Google Antigravity
  - 기본 Antigravity: Gravitas 없이, Google 기본 플러그인 10개만 설치된 상태
  - Gravitas: 같은 모델에 Gravitas의 이전 기본 규칙(v4)만 적용, 두 번째 의견(`--review`)은 끈 상태. 이번 릴리스의 규칙은 이 테스트 뒤에 새로 만들었습니다.
- **채점 방식:** 어느 답이 Gravitas인지 모르는 블라인드 쌍 비교. 미리 검증해 둔 정답 기준표를 보고 판정합니다.
- **판정:**

  - **Gemini 3.1 Pro (high) 채점자:** 기본 Antigravity 쪽, 분명한 차이(clear). 점수(10점 만점, Gravitas 대 기본): 정확성 10 대 10, 함정 대응 5 대 10, 유용성 8 대 10, 정직성 10 대 10, 간결성 10 대 9
  - **Gemini 3.8 Flash (high) 채점자:** 기본 Antigravity 쪽, 분명한 차이(clear). 점수(10점 만점, Gravitas 대 기본): 정확성 8 대 10, 함정 대응 6 대 10, 유용성 7 대 10, 정직성 10 대 10, 간결성 10 대 9

- **같은 질문의 다른 실행:** 여기 실은 Gravitas 답은 Gemini 3.1 Pro로 두 번째 돌린 실행에서 나왔습니다. 같은 규칙으로 모두 네 번 비교했습니다. Gravitas는 세 번 졌고(Pro 두 번, Flash 한 번), 이긴 한 번(Flash)도 두 채점자 모두 근소한 차이(slight)였습니다.

<details>
<summary>채점자 판정 이유 원문 (영어, Answer A = 기본 Antigravity, Answer B = Gravitas)</summary>

**Gemini 3.1 Pro (high)**

> Both answers correctly advise the user against delaying the registration and clarify the misconception regarding the 14-day rule. However, Answer A fully addresses the prompt's trap by explicitly explaining that the user's early 확정일자 does not provide protection on its own without the 대항력 gained from 전입신고. Answer B ignores the early 확정일자 entirely. Answer A also provides excellent practical advice on the timing required for online processing.

**Gemini 3.8 Flash (high)**

> Answer A thoroughly resolves the user's situation by explaining that an early 확정일자 alone offers no protection without 대항요건(전입신고+인도), and by noting the essential Friday 18:00 working-hours cutoff for online 정부24 filing. In contrast, Answer B completely overlooks the user's explicit mention of having already obtained a 확정일자, omitting the legal mechanism of 우선변제권. Answer A also directly addresses the user's practical concern about taking a half-day off by outlining the mobile filing process.

</details>

## 기본 Antigravity 답변 (전문)

````text
**큰일 납니다! 절대 21일로 미루지 마시고 잔금을 치르는 당일인 10월 16일(금)에 반드시 전입신고를 하셔야 합니다.**

말씀하신 대로 전입신고의 법정 기한은 이사 후 14일 이내가 맞습니다. 하지만 전세 보증금 3억 원을 안전하게 지키기 위해서는 이야기가 완전히 달라집니다. 그 이유는 다음과 같습니다.

**1. 보증금을 지키는 '대항력'과 '우선변제권'의 발생 시기**
세입자가 집이 경매로 넘어가더라도 보증금을 지킬 수 있는 권리를 얻으려면 **대항력(실제 거주 + 전입신고)**과 **확정일자**, 이 두 가지가 모두 필요합니다. 
질문자님은 확정일자는 미리 받아두셨지만, 대항력은 전입신고를 한 **'다음 날 0시'**부터 효력이 발생합니다.

*   **질문자님의 계획대로라면:** 21일(수)에 전입신고를 하시면, 보증금을 보호받는 법적 효력은 **22일(목) 0시**부터 생깁니다.
*   **발생하는 치명적인 위험:** 잔금을 치른 16일(금)부터 21일(수) 사이의 5일이라는 공백 기간 동안, 만약 집주인이 해당 집을 담보로 은행에서 대출을 받는다면 은행의 근저당권이 질문자님의 보증금보다 '선순위'가 되어버립니다. 최악의 경우 집이 경매에 넘어가면 보증금을 온전히 돌려받지 못할 수 있습니다.

**2. 평일에 반차를 낼 필요 없이 스마트폰으로 가능합니다!**
전입신고 때문에 굳이 수요일에 반차를 내고 주민센터에 방문하실 필요가 없습니다. 

잔금을 치르고 이사하시는 10월 16일 당일에, 주민센터 방문 없이 **PC나 스마트폰으로 '정부24(www.gov.kr)' 홈페이지나 앱에 접속하여 온라인으로 바로 전입신고**를 하실 수 있습니다. (공동인증서, 금융인증서, 간편인증 등으로 쉽게 로그인 가능합니다.)

**요약 및 행동 지침:**
*   10월 16일 금요일, 잔금을 집주인에게 입금하신 직후에 바로 스마트폰이나 PC를 이용해 **정부24에서 전입신고를 완료**하세요. 
*   이사를 주말에 하시더라도 잔금을 치르는 날 전입신고를 마쳐야 주말 동안 안심하실 수 있습니다. (온라인 전입신고의 경우 평일 근무시간 내에 신청해야 당일 처리가 되므로, 금요일 오후 6시 이전에 신청을 완료하셔야 합니다.)
````

## Gravitas 답변 (전문)

````text
전입신고를 21일로 미루시면 보증금 3억 원을 잃을 위험이 있습니다. 반드시 잔금을 치르고 입주하는 10월 16일 당일에 하셔야 합니다.

이사 후 14일 이내에 전입신고를 해야 한다는 것은 과태료를 피하기 위한 행정상 기한일 뿐, 보증금을 지키기 위한 기준이 아닙니다. 주택임대차보호법상 세입자의 보증금을 보호하는 권리(대항력)는 이사를 하고 전입신고를 마친 '다음 날 0시'부터 효력이 생깁니다.

21일에 전입신고를 하시면 22일 0시부터 권리가 생깁니다. 만약 집주인이 16일부터 21일 사이에 그 집을 담보로 은행 대출을 받으면, 은행의 근저당권은 등기 당일부터 효력이 발생하므로 질문자님의 보증금보다 순위가 앞서게 됩니다. 이 경우 집이 경매로 넘어가면 보증금을 온전히 돌려받지 못할 수 있습니다.

16일 잔금을 입금하자마자 바로 전입신고를 진행하시기 바랍니다. 주민센터에 갈 시간을 내기 어려우시다면, 당일 인터넷 '정부24' 웹사이트나 스마트폰 앱을 통해서도 전입신고를 마칠 수 있습니다.
````

## 해설

### 두 답이 모두 맞힌 것

핵심 결론은 둘 다 맞았습니다. "14일 안에"는 신고 기한일 뿐 보증금을 지키는 기준이 아니고, 보증금을 지키는 대항력은 전입신고 다음 날 0시에 생기므로, 21일까지 미루지 말고 잔금을 치르는 16일 당일에 하라는 것입니다. 그 사이 집주인이 집을 담보로 대출을 받으면 은행 근저당이 앞설 수 있다는 위험, 주민센터에 가지 않고 정부24로도 신고할 수 있다는 점도 두 답 모두 알려 줬습니다. 14일 기한이 과태료를 피하기 위한 행정상 기한이라는 설명은 Gravitas 쪽에만 있었습니다.

### Gravitas가 빠뜨린 것

Gravitas는 기본 Antigravity 답의 절반 정도 길이로 줄이면서, 질문하신 분에게 꼭 필요한 두 가지를 빠뜨렸습니다.

첫째, 질문하신 분은 "확정일자는 계약서 쓴 날 주민센터 가서 미리 받아놨고요"라고 했습니다. 확정일자를 먼저 받아 두었으니 괜찮지 않겠느냐는 기대가 깔린 말입니다. 기본 Antigravity는 "질문자님은 확정일자는 미리 받아두셨지만, 대항력은 전입신고를 한 **'다음 날 0시'**부터 효력이 발생합니다"라고 이 부분을 직접 짚었습니다. Gravitas는 확정일자를 한 번도 언급하지 않았습니다.

둘째, 기본 Antigravity는 "온라인 전입신고의 경우 평일 근무시간 내에 신청해야 당일 처리가 되므로, 금요일 오후 6시 이전에 신청을 완료하셔야 합니다"라고 시간 조건까지 알려 줬습니다. Gravitas는 "잔금을 입금하자마자 바로" 신고하라고는 했지만, "당일 인터넷 '정부24' 웹사이트나 스마트폰 앱을 통해서도 전입신고를 마칠 수 있습니다"에서 멈췄습니다. 근무시간이 지나 신청하면 그날 처리되지 않는다는 말이 없어서, 이삿짐을 다 들인 뒤 금요일 밤에 신청해도 된다고 받아들일 여지가 남습니다. 다만 기본 Antigravity가 말한 "오후 6시 이전"도 안전한 기준은 아닙니다. 정부24 안내에 따르면 근무시간 안에 낸 신청도 오후 3시를 넘기면 다음 근무일에 처리될 수 있습니다. 금요일 오후 늦게 신청했다가 월요일(19일)에 처리되면 대항력은 화요일(20일) 0시에야 생기므로, 16일 당일에 처리되게 하려면 오후 3시 전에 신청하는 것이 안전합니다.

두 채점자 모두 바로 이 두 가지를 이유로 기본 Antigravity 쪽을 골랐습니다.

### 왜 이렇게 됐나

v4 규칙에는 군더더기를 줄이라는 줄이 있습니다. 같은 줄은 행동에 필요한 단계, 숫자, 주의 사항은 자르지 말라고도 하지만, 이 답은 그 선을 넘었습니다.

> Give the reply the length its content needs: cut padding, repetition, preamble and decoration, never the steps, figures or caveats the person needs to act on it.

질문하신 분이 직접 꺼낸 사실(미리 받은 확정일자)을 답 안에서 정리해 주라는 줄도 지켜지지 않았습니다.

> When they made several claims, settle each one in the flow of the answer, without labels or verdict headings, and never tell them they are wrong about something that holds.

Gravitas의 세 가지 원칙(어떤 일인지 알아보기, 바깥의 사실로 확인하기, 사람에게 맞추기)으로 보면 **사람에게 맞추기**에서 실패한 사례입니다. Gemini 3.1 Pro는 원래 군더더기가 많지 않은 모델이라, 군더더기를 줄이라는 지시가 내용까지 깎아 낸 것으로 보입니다. 앞선 실험에서도 Pro에서는 짧게 쓰다가 필요한 내용을 빼서 지는 경우가 있었습니다.

### 묻는 사람에게 왜 중요한가

보증금 3억 원이 걸린 질문입니다. 결론은 맞았지만, 확정일자를 미리 받았으니 괜찮겠다는 생각이 왜 틀렸는지가 답에서 빠졌고, 언제까지 신청해야 그날 처리되는지도 빠졌습니다. 짧고 단호한 답이 늘 더 좋은 답은 아닙니다. 이 경우에는 Gravitas 없이 받은 답이 더 쓸모 있었습니다.
