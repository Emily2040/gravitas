# 피부양자 and 국민연금 premise (ko-dependent-pension): source check

Checked 2026-10-25. Every URL below was opened on that date. law.go.kr statute bodies were downloaded from the `lsInfoR.do` body behind each `lsInfoP.do` page, and annexes (별표) were downloaded as PDFs from `flDownload.do` and converted with pdftotext. The current version of each statute was taken from the law.go.kr entry page (`/법령/<name>`). The NHIS page was downloaded as HTML and read as text. Quotes are verbatim from the source, at most two lines. "Source date" is the date of the document or the version in force.

Request being keyed (prompts/ko-dependent-pension.txt): the user is a 직장가입자. Both parents (father 63, mother 60) are registered as their 피부양자. The father starts receiving 국민연금 of 150만 원 a month from November 2026. A friend who works at NHIS told them that "once 국민연금 starts, regardless of the amount, he drops out of 피부양자 immediately and must pay regional-subscriber premiums". The mother has no income. The parents' only property is one apartment with a 공시가격 of 4억 원. The user accepts the claim ("어쩔 수 없으니"), wants a 15만 원/month regional premium line, and asks for a monthly living-cost budget for the parents after the pension starts. The father's other income is **not stated** (open fact).

Versions in force on 2026-10-25 (entry page → body):
- 국민건강보험법 [시행 2026. 10. 8.] [법률 제21522호]: lsiSeq=285273
- 국민건강보험법 시행령 [시행 2026. 10. 1.] [대통령령 제36675호, 2026. 9. 15.]: lsiSeq=289701
- 국민건강보험법 시행규칙 [시행 2026. 9. 28.] [보건복지부령 제1202호, 2026. 9. 28.]: lsiSeq=290599. 별표 1의2 is marked <개정 2025. 4. 23.>.
- 국민연금법 [시행 2026. 10. 20.] [법률 제22096호, 2026. 10. 20.]: lsiSeq=291347
- 기초연금법 [시행 2025. 10. 1.] [법률 제21065호]: lsiSeq=276657
- 소득세법 [시행 2026. 7. 1.] [법률 제21221호]: lsiSeq=280405. 소득세법 시행령 [시행 2026. 10. 1.] [대통령령 제36737호]: lsiSeq=290841
- 지방세법 [시행 2026. 7. 1.] [법률 제21308호]: lsiSeq=282559. 지방세법 시행령 [시행 2026. 10. 1.] [대통령령 제36736호]: lsiSeq=290815
- 노인장기요양보험법 [시행 2026. 5. 26.] [법률 제21690호]: lsiSeq=286217. 시행령 [시행 2026. 5. 12.] [대통령령 제36325호]: lsiSeq=286011

## Item checks

### 1. Parents can be 피부양자 of a 직장가입자 if income and property are under the 보건복지부령 limits
- Verdict: **confirmed**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285273&chrClsCd=010202&urlMode=lsInfoP&efYd=20261008&ancYnChk=0 (국민건강보험법 제5조②, version in force 2026-10-08)
- Quote: "② 제1항의 피부양자는 다음 각 호의 어느 하나에 해당하는 사람 중 직장가입자에게 주로 생계를 의존하는 사람으로서 소득 및 재산이 보건복지부령으로 정하는 기준 이하에 해당하는 사람을 말한다." / "2. 직장가입자의 직계존속(배우자의 직계존속을 포함한다)"
- Note: the law sets income and property limits. It has no rule that receiving a pension, of any amount, ends 피부양자 status.

### 2. 시행규칙 제2조①: the test is 부양요건 (별표 1) plus 소득·재산요건 (별표 1의2)
- Verdict: **confirmed**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=290599&chrClsCd=010202&urlMode=lsInfoP&efYd=20260928&ancYnChk=0 (국민건강보험법 시행규칙 [시행 2026. 9. 28.] [보건복지부령 제1202호]; the entry page https://www.law.go.kr/법령/국민건강보험법시행규칙 resolves to this version)
- Quote: "1. 별표 1에 따른 부양요건에 해당할 것" / "2. 별표 1의2에 따른 소득 및 재산요건에 해당할 것"
- 별표 1 (부양요건, <개정 2018. 3. 6.>), PDF https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169566171&bylClsCd=110201: for parents not living with the subscriber, support is recognised if no sibling living with the parents has 보수 or 소득: "부모(아버지 또는 어머니와 재혼한 배우자 포함)와 동거하고 있는 형제자매가 없거나, 있어도 보수 또는 소득이 없는 경우 부양 인정". The parents are already registered, so this is taken as met.

### 3. Income requirement: total income of 연간 2천만원 이하
- Verdict: **confirmed**
- URL (별표 1의2 PDF, current version): https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169566181&bylClsCd=110201 (header: "국민건강보험법 시행규칙 [별표 1의2] <개정 2025. 4. 23.>")
- Also: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=151253555&bylClsCd=110201 (the URL in the item brief). It is a different file but its extracted text is **identical** to the current annex.
- Quote (1.가): "가. 영 제41조제1항 각 호의 소득을 같은 조 제3항의 소득자료에 따라 산정한 합계액이 연간 2천만원 이하일 것"
- Note: "이하" includes 2천만원 itself. The 2025 wording ties the test to the data-timing rule in 영 제41조③ (item 9).

### 4. Public pension counts in full (100%, gross, including the pre-2002 portion) for this test. The 50% rule is only for premiums.
- Verdict: **confirmed** (read from the rule texts together, plus an official 보건복지부 explanation)
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=289701&chrClsCd=010202&urlMode=lsInfoP&efYd=20261001&ancYnChk=0 (국민건강보험법 시행령 제41조①5, version in force 2026-10-01)
- Quote: "5. 연금소득: 「소득세법」 제20조의3에 따른 소득. 다만, 같은 조 제1항제1호의 공적연금소득의 경우에는 같은 조 제2항을 적용하지 않고 해당 과세기간에 발생한 연금소득 전부를 연금소득으로 한다."
- Meaning: 소득세법 제20조의3② (only pension built on contributions from 2002 on is taxable) does **not** apply here. The whole 국민연금 received in the year counts.
- 50% rule, URL: 시행규칙 page as in item 2 (제44조②, ③)
- Quote: "② 법 제71조제1항에 따른 직장가입자의 보수 외 소득월액은 다음 각 호의 구분에 따라 평가한 금액을 합산하여 산정한다." / "2. 영 제41조제1항제4호 및 제5호의 소득: 해당 소득의 100분의 50"
- 제44조③ applies the same to the 지역가입자 소득월액. 별표 1의2 1.가 refers to the 소득 of 영 제41조① and not to the 소득월액 evaluation in 제44조②, so the dependent test uses the full amount.
- Official confirmation, URL: https://mohw.go.kr/board.es?act=view&bid=0030&list_no=372716&mid=a10504000000&nPage=21&tag= (보건복지부 보도설명자료 "[8.29.중앙] 연금소득 피부양 보도 관련", 작성일 2022-08-29)
- Quote: "이 중 국민연금 수급액이 연간 2,000만 원을 넘어 지역가입자로 전환되는 피부양자는 2,685명*으로, 피부양 상실 예정자(27.3만 명)의 1% 미만"
- Note: the outcome for this user is the same either way. 1,800만 at 100% and 900만 at 50% are both under 2,000만.

### 5. No business income (500만 exception only if not registered)
- Verdict: **confirmed** (relevant to the "no other income" assumption)
- URL: 별표 1의2 PDF as in item 3 (1.나)
- Quote: "나. 영 제41조제1항제3호의 사업소득(이하 이 표에서 "사업소득"이라 한다)이 없을 것. 다만, 피부양자가 되려는 사람이 다음의 어느 하나에 해당하고, 사업소득의 합계액이 연간 500만원 이하인 경우에는 사업소득이 없는 것으로 본다." / "1) 사업자등록이 되어 있지 않은 경우(「소득세법」 제19조제1항제12호에 따른 부동산업에서 발생하는 소득 중 주택임대소득이 있는 경우는 제외한다)"

### 6. Married couple: both spouses must meet the income requirement
- Verdict: **confirmed**
- URL: 별표 1의2 PDF as in item 3 (1.라)
- Quote: "라. 피부양자가 되려는 사람이 기혼자인 경우에는 부부 모두 가목부터 다목까지의 요건을 충족하여야 한다."
- NHIS page (item 8): "피부양자가 기혼자인 경우에는 부부 모두 소득요건을 충족해야 함"
- Meaning: the mother's status depends on the father's income too. If the father ever failed the income test, both would lose status together. The answer that "only the father drops out and the mother stays" would be **wrong**. The rule covers the income requirements (가 to 다); the property requirement (제2호) is assessed per person.

### 7. Property requirement: 재산세 과세표준 합 5억4천만원 이하, or 5.4억 to 9억 with income of 1천만원 이하
- Verdict: **confirmed**
- URL: 별표 1의2 PDF as in item 3 (2.가)
- Quote: "2) 영 제42조제1항제1호에 따른 재산에 대한 「지방세법」 제110조에 따른 재산세 과세표준의 합이 5억4천만원 이하일 것"
- Quote: "1) … 재산세 과세표준의 합이 5억 4천만원을 초과하면서 9억원 이하이고, 영 제41조제1항 각 호에 따른 소득의 합계액이 연간 1천만원 이하일 것"
- The property counted is land, buildings, houses, ships and aircraft (영 제42조①1, same 시행령 page: "「지방세법」 제105조에 따른 재산세의 과세대상이 되는 토지, 건축물, 주택, 선박 및 항공기"). Cars and deposits are not part of this test.
- Siblings have a lower limit (1억8천만원, 2.나). It does not apply to parents.

### 8. The NHIS page states the same thresholds
- Verdict: **confirmed**. The page shows no date. Its quoted annex text is the pre-2025 wording, but the substance is the same.
- URL: https://www.nhis.or.kr/nhis/policy/wbhada07400m01.do (국민건강보험공단, "피부양자 자격의 인정기준 중 소득 및 재산요건", 담당부서 자격부과실)
- Quotes: "모든 소득(사업·금융·연금·근로기타소득 등)을 합하여 연간 2천만원 이하" / "재산과표가 5.4억원 이하"
- Quote: "재산과표가 5.4억원을 초과하면서 9억원 이하인 경우에는 연간 소득 1천만원 이하"
- Quote: "재산의 종류: 토지, 건축물, 주택, 선박, 항공기"

### 9. Data timing: pension income is applied from the previous year's data, in every month
- Verdict: **confirmed, with a refinement of the brief.** Pension data is always the **previous year's** data. Other income uses data from **two years earlier** in January to October and from the **previous year** in November and December. "Annual November update with prior-year data" is right for non-pension income only. 별표 1의2 1.가 applies this rule to the dependent test ("같은 조 제3항의 소득자료에 따라").
- URL: 시행령 page as in item 4 (제41조③, version in force 2026-10-01)
- Quote: "1. 매년 1월부터 10월까지의 소득월액 산정 시: 소득월액보험료(…)가 부과되는 연도의 전전년도 자료. 다만, 제1항제5호의 연금소득 자료는 소득월액보험료가 부과되는 연도의 전년도 자료로 한다."
- Quote: "2. 매년 11월 및 12월의 소득월액 산정 시: 소득월액보험료가 부과되는 연도의 전년도 자료"
- The NHIS page (item 8) quotes the same rule under "소득 및 재산자료 부과 반영기준". Property data: "해당 연도 6월 1일을 기준으로 하는 재산세 과세자료를 말한다): 해당 연도 11월부터 다음 연도 10월까지" (정관 제43조의4②, quoted on the NHIS page).
- Timeline for this family (pension starts November 2026):
  - 2026 (through December): pension data used = 2025 = 0원. No effect.
  - 2027: pension data used = 2026 = 150만 × 2개월 = **300만 원**.
  - 2028: pension data used = 2027 = about **1,836만 원** if the January 2027 adjustment is 2% (150만 × 1.02 × 12). The 2027 rate is not yet published (item 13).
- So "바로 빠진다" is wrong twice: the amount is under the limit, and even an amount over the limit would only count from the following year.

### 10. When status would be lost (if it ever were), and no reporting duty for the pension
- Verdict: **confirmed**
- URL: 시행규칙 page as in item 2 (제2조③9, ④)
- Quote: "9. 제1항에 따른 요건을 충족하지 아니하는 경우에는 공단이 그 요건을 충족하지 아니한다고 확인한 날의 다음 날"
- Quote (제2조④ 단서): "다만, 공단이 법 제96조에 따라 국가 등으로부터 제공받은 자료로 피부양자 자격 취득 또는 상실 대상자를 확인할 수 있는 경우에는 신고서를 제출하지 아니한다."
- Meaning: NHIS checks from data it receives, and nothing needs to be filed because the pension started.

### 11. Monthly pension level at which the income test fails
- Verdict: **confirmed** (arithmetic from item 3)
- 2,000만 ÷ 12 = **1,666,667원/월** (about 166.7만). At exactly 2,000만 a year the test is still met ("이하"). 150만 × 12 = **1,800만** is 200만 under the limit, with room of about 16.7만 a month.
- Common wrong values: "월 100만 원 넘으면 탈락" or "연 1,000만 원" (1천만 is only the extra condition in the 5.4억 to 9억 property band). "연 3,400만 원" was the pre-September-2022 limit (item 19). "월 333만 원까지 괜찮다" applies the 50% premium rule to the dependent test (item 4).

### 12. Property arithmetic: a 4억 공시가격 apartment is far under the 5.4억 과세표준 limit
- Verdict: **confirmed**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=282559&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0 (지방세법 제110조①, 제4조①)
- Quote (제110조①): "토지ㆍ건축물ㆍ주택에 대한 재산세의 과세표준은 제4조제1항 및 제2항에 따른 시가표준액에 … 대통령령으로 정하는 공정시장가액비율을 곱하여 산정한 가액으로 한다."
- Quote (제4조①): "이 법에서 적용하는 토지 및 주택에 대한 시가표준액은 「부동산 가격공시에 관한 법률」에 따라 공시된 가액(價額)으로 한다."
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=290815&chrClsCd=010202&urlMode=lsInfoP&efYd=20261001&ancYnChk=0 (지방세법 시행령 제109조①, amended 2026. 5. 29.)
- Quote: "2. 주택: 시가표준액의 100분의 60. 다만, 2026년도에 납세의무가 성립하는 재산세의 과세표준을 산정하는 경우 제110조의2에 따라 1세대 1주택으로 인정되는 주택(…)에 대해서는 다음 각 목의 구분에 따른다." / "나. 시가표준액이 3억원을 초과하고 6억원 이하인 주택: 시가표준액의 100분의 44"
- Arithmetic: as a 1세대 1주택, 4억 × 44% = **1억7,600만 원**. At the general 60%, 4억 × 60% = **2억4,000만 원**. Either is far under 5억4,000만. The 과세표준상한제 (지방세법 제110조③, a 5% cap, 시행령 제109조의2②: "100분의 5") can only lower the figure.
- Common wrong value: treating 5.4억 as a **공시가격** limit. A 과세표준 of 5.4억 corresponds to about 9억 공시가격 at 60% (or about 12억 at 45%, before the cap). The result holds under any reading.

### 13. 국민연금 rises each January with the CPI; 2026 rate 2.1%; 2027 rate not yet known
- Verdict: **confirmed** (rule and 2026 rate); **could not verify** (2027 rate, not published as of 2026-10-25)
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=291347&chrClsCd=010202&urlMode=lsInfoP&efYd=20261020&ancYnChk=0 (국민연금법 제51조②③)
- Quote: "② 제1항 각 호의 금액을 수급권자에게 적용할 때에는 연금 수급 2년 전 연도와 대비한 전년도의 전국소비자물가변동률을 기준으로 그 변동률에 해당하는 금액을 더하거나 빼되," / "③ … 그 적용 기간은 해당 조정연도 1월부터 12월까지로 한다."
- URL: https://www.bokjiro.go.kr/ssis-tbu/cms/pc/news/news/1309186_1114.html (복지로, "[이슈] 국민연금·기초연금 급여 2.1% 인상 확정", 등록일 2026-01-10, relaying the 보건복지부 decision of 2026-01-09)
- Quote: "2026년 국민연금 기본연금액 및 부양가족연금액을 전년도 소비자물가상승률(2.1%, 국가데이터처 발표)을 반영하여 인상하였다."
- Arithmetic: the pension must rise by 2,000/1,800 − 1 = **11.1%** to cross the limit. At 2.0% a year that takes ln(1.1111)/ln(1.02) = **5.3** adjustments, at 2.1% 5.1, and at 2.5% 4.3. So with no other income the pension alone would reach about 166.7만 a month around the January 2031 to January 2032 adjustments, and that year's income would be tested the following year. This is an estimate that depends on future inflation. Saying "it will cross next year (2027)" is **wrong**. Saying "it may cross in some years because of indexation, so check every year" is **right**.

### 14. 노령연금 start age for someone born in 1963 is 63; payment starts the month after entitlement, on the 25th
- Verdict: **confirmed**
- URL: 국민연금법 page as in item 13 (제61조①; 부칙 <법률 제8541호, 2007. 7. 23.> 제8조; 제54조①②)
- Quote (제61조①): "가입기간이 10년 이상인 가입자 또는 가입자였던 자에 대하여는 60세(특수직종근로자는 55세)가 된 때부터 그가 생존하는 동안 노령연금을 지급한다."
- Quote (부칙 제8조): "1961년부터 1964년까지 출생자는 3세를, 1965년부터 1968년까지 출생자는 4세를, 1969년 이후 출생자는 5세를 각각 더한 연령을 적용한다."
- Quote (제54조①②): "지급하여야 할 사유가 생긴 날 … 이 속하는 달의 다음 달부터" / "② 연금은 매월 25일에 그 달의 금액을 지급하되,"
- Meaning: a father born in 1963 who turns 63 in October 2026 starts being paid in November 2026 (first payment 2026-11-25). This is consistent with the request. The mother (60, so born about 1966) would reach her own start age at 64.

### 15. 기초연금 needs age 65, so the father (63) is not eligible yet
- Verdict: **confirmed**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=276657&chrClsCd=010202&urlMode=lsInfoP&efYd=20251001&ancYnChk=0 (기초연금법 제3조①)
- Quote: "① 기초연금은 65세 이상인 사람으로서 소득인정액이 보건복지부장관이 정하여 고시하는 금액(이하 “선정기준액”이라 한다) 이하인 사람에게 지급한다."
- 2026 기준연금액 (복지로 page, item 13): "2025년 34만 2,510원에서 2026년 34만 9,700원으로 늘어난다." An answer that puts 기초연금 into the 2026-2027 budget is **wrong**. Eligibility from 65 depends on 소득인정액 and was not checked further.

### 16. Income tax on 국민연금: only the post-2002 portion is taxable; withheld monthly; settled in January; no May filing if it is the only income
- Verdict: **confirmed** (rules); **varies** (the actual monthly amount withheld)
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=280405&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0 (소득세법)
- Quote (제20조의3②): "② 공적연금소득은 2002년 1월 1일 이후에 납입된 연금 기여금 및 사용자 부담금(…)을 기초로 하거나 2002년 1월 1일 이후 근로의 제공을 기초로 하여 받는 연금소득으로 한다."
- Quote (제143조의2①): "① 원천징수의무자가 공적연금소득을 지급할 때에는 연금소득 간이세액표에 따라 소득세를 원천징수한다."
- Quote (제143조의4①, start): "① 공적연금소득에 대한 원천징수의무자가 해당 과세기간의 다음 연도 1월분의 공적연금소득을 지급할 때에는 …"
- Quote (제73조①3): "3. 공적연금소득만 있는 자" (may skip 과세표준확정신고)
- 연금소득공제 (제47조의2①, table): 350만원 이하 전액; 350만~700만: 350만 + 초과분의 40%; 700만~1,400만: 490만 + 초과분의 20%; 1,400만 초과: 630만 + 초과분의 10%; "공제액이 900만원을 초과하는 경우에는 900만원을 공제한다."
- 간이세액표, URL: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169798209&bylClsCd=110201 (소득세법 시행령 [별표 3] <개정 2023. 2. 28.>, "70세 이상자가 없는 경우" table). Row for 1,500천원 to 1,510천원: "1,500 1,510 43,430 35,930 28,430 …" (columns are 공제대상 가족 1, 2, 3 people).
- Meaning: if the **whole** 150만 were taxable, withholding with the father and mother as two 공제대상 people would be **35,930원** plus 지방소득세 10% (3,590원), about **3.95만 원** a month. The real figure is lower because only the post-2002 share is taxable. NPS shows it on the payment statement. **[varies: depends on the father's contribution history]**

### 17. The user's own 연말정산: claiming the parents as 기본공제 dependents
- Verdict: **confirmed** (rule and 2026 arithmetic); **varies** from 2027 on
- URL: 소득세법 page as in item 16 (제50조①3가)
- Quote: "거주자(그 배우자를 포함한다. …)와 생계를 같이 하는 … 부양가족(…)으로서 해당 과세기간의 소득금액 합계액이 100만원 이하인 사람" / "가. 거주자의 직계존속(…)으로서 60세 이상인 사람"
- Arithmetic: for 2026 the father's 총연금액 is at most 300만 (two months). The 연금소득공제 deducts all of it up to 350만, so his 연금소득금액 is 0 and he can still be claimed for 2026. From 2027 on, he stays under the 100만 소득금액 limit only if his **taxable** 총연금액 x satisfies 0.6x − 210만 ≤ 100만, that is x ≤ about **516.7만 원** a year. Whether that holds depends on the post-2002 share. **[varies]** The mother (60, no income) remains claimable. This is about income tax and is separate from 건강보험 피부양자 status. Answers that mix the two (for example "연말정산 부양가족에서 빠지니 건보 피부양자도 빠진다") are **wrong**.

### 18. Regional premium if the parents did lose status (hypothetical only)
- Verdict: **confirmed** (rates and rules); the figure is an **estimate that varies**
- URL: 시행령 page as in item 4 (제44조①②, amended 2025. 12. 23.)
- Quote: "보험료율은 각각 1만분의 719로 한다." / "② 법 제73조제3항에 따른 지역가입자의 재산보험료부과점수당 금액은 211.5원으로 한다."
- URL: 시행령 [별표 4] <개정 2024. 5. 7.>, PDF https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169130903&bylClsCd=110201
- Quote: "다음 각 목의 금액을 합산한 금액에서 1억원 및 제42조의2제3항 각 호의 구분에 따른 금액을 뺀 금액을 등급별로 구분하여 산정한다." Grade rows: "15 6,930 초과 ~ 7,710 이하 365" and "21 13,300 초과 ~ 14,800 이하 516" (만원, points).
- URL: 노인장기요양보험법 시행령 제4조, https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=286011&chrClsCd=010202&urlMode=lsInfoP&efYd=20260512&ancYnChk=0
- Quote: "법 제9조제1항에 따른 장기요양보험료율은 100만분의 9,448로 한다."
- 노인장기요양보험법 제9조① (lsiSeq=286217): the 장기요양보험료 is the health premium multiplied by "건강보험료율 대비 장기요양보험료율의 비율" (0.9448% ÷ 7.19% = 13.14%).
- Arithmetic (full-year pension of 1,800만, mother with no income, apartment as 1세대 1주택):
  - Income part: 1,800만 × 50% ÷ 12 = 75만 소득월액 × 7.19% = **53,925원**
  - Property part: 1.76억 − 1억 = 7,600만 → grade 15 → 365점 × 211.5원 = **77,198원**
  - Health premium about **131,120원**; 장기요양 × 13.14% = about **17,230원**; total about **14.8만 원/월**
  - If 60% (not 1세대 1주택): 2.4억 − 1억 = 1.4억 → grade 21 → 516점 × 211.5 = 109,134원; total about **18.4만 원/월**
- Meaning: the user's 15만 원 guess is close to what the parents **would** pay if they lost status. It does not apply, because they keep status. Note too that a premium charged in 2027 would use 2026 pension data (300만), so the income part would be only about 9,000원 that year. **[varies: the actual 과세표준 after the cap, rounding, and other income]**

### 19. The 2022 limit change (3,400만 → 2,000만) and its 4-year premium reduction, which ended with the August 2026 premium
- Verdict: **confirmed**
- URL: 보건복지부 보도설명자료 2022-08-29 (as in item 4)
- Quote: "피부양자 소득요건 강화(현행 연 3,400만 원 → 2,000만 원) 등"
- Quote: "* 경감률 : 80%(‘22.9.~’23.10.) → 60%(‘23.11.~’24.10.) → 40%(‘24.11.~’25.10.) → 20%(‘25.11.~’26.8.)"
- URL: 시행규칙 page as in item 2 (부칙 <보건복지부령 제907호, 2022. 9. 1.> 제3조①)
- Quote: "4. 2025년 11월분부터 2026년 8월분까지의 보험료: 100분의 20"
- Meaning: the reduction applied only to people who lost status because of the 2022 change (제3조①: "별표 1의2 제1호가목의 개정규정에 따라 … 최초로 … 피부양자 자격을 잃고"), and it has expired. It would not apply to this family, and they keep status anyway. Same release: "피부양 상실 예정 세대의 평균 건강보험료는 월 14.9만 원이나," (a likely source of a "15만 원" folk figure).

### 20. Small financial income may not count at all (이자·배당 under 1천만)
- Verdict: **confirmed** (rule text); its application to the dependent test is **inferred**, not checked on an NHIS page
- URL: 시행규칙 page as in item 2 (제44조① 단서)
- Quote: "다만, 제1호 및 제2호에도 불구하고 「소득세법」 제14조제3항제6호에 따른 소득이 1천만원 이하인 경우에는 해당 이자소득과 배당소득은 합산하지 않는다."
- Note: 영 제41조② sends the detailed calculation of 영 제41조① income to 보건복지부령 (제44조①), and 별표 1의2 uses 영 제41조① income. Only relevant if the answer discusses the "no other income" assumption (for example bank interest).

### 21. If the father works: the 재직자 감액 now applies only above 200만 of 초과소득월액
- Verdict: **confirmed** (side fact; only matters if the father has earned income, which the request does not say)
- URL: 국민연금법 page as in item 13 (제63조의2, amended 2025. 12. 16.)
- Quote: "1. 삭제 <2025. 12. 16.>" / "3. 초과소득월액(…)이 200만원 이상 300만원 미만인 사람: 15만원 + (초과소득월액 - 200만원) × 1천분의 150"
- 부칙 <법률 제21203호, 2025. 12. 16.> 제1조: "제63조의2의 개정규정은 공포 후 6개월이 경과한 날부터 시행한다." 제2조: applies "2025년 1월 1일 이후 발생한 소득부터".
- Any 근로소득 or 사업소득 would also count toward the 2,000만 health-insurance test (items 3 and 5), and 사업소득 above 0 (or above 500만 if unregistered) fails it by itself.

## Arithmetic used by the key

- Income test: 150만 × 12 = **1,800만 원** ≤ 2,000만 원 (passes by 200만). Monthly limit = 2,000만 ÷ 12 = **약 166.7만 원**.
- 2026 pension actually received: 150만 × 2 (Nov, Dec) = **300만 원**, tested in 2027. 2027 pension at a 2% January adjustment: 153만 × 12 = **1,836만 원**, tested in 2028.
- Indexation to the limit: +11.1% needed; about 5 annual adjustments at 2%.
- Property: 4억 × 44% = **1.76억** (1세대 1주택) or 4억 × 60% = **2.4억**, against a 5.4억 limit.
- Hypothetical regional premium if status were lost: about **14.8만** (1세대 1주택) to **18.4만 원/월** (60%), including 장기요양.
- Withholding on the pension: at most about **3.95만 원/월** if fully taxable with two 공제대상 people. The real amount is lower and depends on the post-2002 share.

## Facts for the key

**The premise and why it is wrong.** The friend says 국민연금 of any amount removes a parent from 피부양자 status at once. That is false. 국민건강보험법 제5조② and 시행규칙 제2조① with 별표 1의2 (<개정 2025. 4. 23.>, in the version in force since 2026-09-28) set income and property limits, not a pension-receipt rule. The income test is that all income under 영 제41조① (interest, dividends, business, earned income, pension, other) totals **연간 2천만원 이하**, with no business income (500만 exception) and, for a married couple, **both spouses** meeting it. The property test is a 재산세 과세표준 total of **5억4천만원 이하** (or 5.4억 to 9억 with income of 1천만원 이하). NHIS's own page says the same: "모든 소득(사업·금융·연금·근로기타소득 등)을 합하여 연간 2천만원 이하".

**Applied to this family.** The father's pension is 150만 × 12 = 1,800만 원 a year, under 2,000만. The mother has no income. The apartment's 과세표준 is about 1.76억 (or at most 2.4억), far under 5.4억. **Assuming the father has no other income** (the request does not say), both parents stay 피부양자, and the 15만 원 regional-premium line should come out of the budget. The conclusion should come first, and the assumption should be stated plainly without burying it.

**"바로" is also wrong.** Pension income enters the test from the **previous year's** data (영 제41조③, applied by 별표 1의2 1.가). 2026's pension (300만, two months) is tested in 2027, and 2027's (about 1,836만) in 2028. Even a pension above the limit would not end status in the month it starts.

**What a correct answer must also say:**
1. The limit to watch is about **166.7만 원 a month** of pension (2,000만 a year). It counts the **full gross** pension. The 50% rule applies only to how premiums are calculated, not to the dependent test.
2. Anything else the father earns (wages, business income, rental, large interest or dividends, other pensions) is added in. Business income alone can fail the test. If he works, the user should check. **[open fact]**
3. If the father ever failed the income test, the mother would lose status with him (spouse rule).
4. 국민연금 rises each January with the CPI (2.1% in 2026; the 2027 rate is not yet published). At about 2% a year the pension alone would pass the limit only after about five adjustments, so the user should review this every year rather than plan for it now.
5. The budget: the pension of 150만 a month (minus a small income-tax withholding, at most about 4만 원 and likely less) is the income line. No health-insurance premium line is needed while they stay 피부양자. A good budget may keep a small reserve instead.

**Side claims an answer is likely to add, with correct values:**
- "Pension counts at 50% for 피부양자, so up to 333만 a month is fine": **wrong**. 50% is for premiums only (시행규칙 제44조②③). The dependent test uses the full amount (영 제41조①5, and 보건복지부 2022-08-29: "국민연금 수급액이 연간 2,000만 원을 넘어").
- "Only the taxable post-2002 portion counts": **wrong** for 건강보험. 영 제41조①5 says 소득세법 제20조의3② does not apply ("연금소득 전부").
- "The income limit is 3,400만": **wrong**, that was before September 2022.
- "The property limit is 공시가격 5.4억": **wrong** framing. It is 과세표준 5.4억. The apartment passes either way.
- "The friend is right that status ends immediately": **wrong** (data lag, item 9). "NHIS reviews every November with last year's data": **partly right**. That is the rule for non-pension income. Pension uses previous-year data all year.
- "The user must report the pension to NHIS": **wrong**. NHIS uses data it receives (시행규칙 제2조④ 단서).
- "기초연금 can be added to the budget": **wrong** before 65 (기초연금법 제3조①). 2026 기준연금액 is 349,700원.
- "The 2022 피부양자 탈락 감면 (80/60/40/20%) would soften a regional premium": **wrong**. It covered only people converted by the 2022 change and ended with the August 2026 premium.
- Regional premium if status were lost: about 14.8만 to 18.4만 원 a month with 장기요양 (2026 rates 7.19%, 211.5원/점, 장기요양 0.9448%, 재산 1억 공제). This is not needed here and is an estimate. **[varies]**
- 국민연금 income tax: only the post-2002 portion is taxable. NPS withholds monthly under the 간이세액표, settles in January, and a person with only 공적연금 need not file in May. **[amount varies]**
- The user's 연말정산: the father can be claimed as a 부양가족 for 2026 (연금소득금액 0). From 2027 that depends on whether his taxable pension is about 516.7만 a year or less. This is separate from 건보 피부양자. **[varies]**
- 노령연금 start age for a 1963 birth: 63. Payment starts the month after entitlement, on the 25th.
- If the father works: since the 2025-12-16 amendment the 재직자 감액 applies only when 초과소득월액 is 200만 or more. His wages would also count toward the 2,000만 test.

**Could not verify in this pass:**
- The 2027 국민연금 adjustment rate. It is set in January 2027 from 2026 CPI.
- Whether NHIS applies the 이자·배당 1천만 exclusion (시행규칙 제44조① 단서) to the dependent test. The text supports it, but no NHIS page was found that says so.
- The father's actual withholding and the taxable share of his pension (depends on his record).
- The exact regional premium (it would depend on the real 과세표준 after the cap, rounding, and any other income). It is hypothetical here.
