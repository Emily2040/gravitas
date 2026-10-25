# ko-severance-pay: adversarial check of "Facts for the key" (checked 2026-10-23/24)

Inputs read: `sources/ko-severance-pay.md`, `prompts/ko-severance-pay.txt`. Nothing else on disk was opened.

Method: every cited source was reopened. law.go.kr pages were read in the built-in browser, because they render with JavaScript. For each statute I took the version that the law.go.kr entry page (`/법령/<name>`) currently loads, and checked it for `[시행일: …]` markers that would flag pending amendments. I ran the 노동포털 퇴직금 calculator myself. I redid every figure independently in Python. I also searched for 2025-2026 amendments and for new annual 고시.

Current versions confirmed (entry page → iframe on 2026-10-24):
- 근로자퇴직급여 보장법 [시행 2026. 9. 18.] [법률 제21475호, 2026. 3. 17.]: lsiSeq=284455. No pending `[시행일:]` markers.
- 같은 법 시행령 [시행 2026. 3. 24.] [대통령령 제36220호]: lsiSeq=284693
- 근로기준법 [시행 2026. 10. 8.] [법률 제21533호, 2026. 4. 7.]: lsiSeq=285279. Pending markers exist for 제13조, 제43조의6, 제44조의4, 제54조, 제60~61조, 제101~108조, 제110·114·116조. None touches 제2조, 제36조, 제37조, 제43조의8 or 제107조.
- 근로기준법 시행령 [시행 2025. 10. 23.] [대통령령 제35436호]: lsiSeq=270551
- 소득세법 [시행 2026. 7. 1.] [법률 제21221호]; 지방세법 [시행 2026. 7. 1.] [법률 제21308호]
- 임금채권보장법 [시행 2026. 8. 20.] [법률 제21376호]; 시행령 [시행 2026. 5. 12.] [대통령령 제36307호]
- 고용노동부고시 제2026-65호 (IRP 이전 예외 금액, 시행 2026. 9. 1.). 체불 임금등 대지급금 상한액 고시: the entry page `/행정규칙/체불임금등대지급금상한액고시` still resolves to 제2021-81호 (admRulSeq=2100000205348), so no newer cap 고시 exists.

Result: 16 facts. **11 stand. 5 need changes**: wording, attribution or minor date arithmetic. **None is refuted on the law or on the money figures.**

---

## 전제와 그것이 틀린 이유

### F1. Company's claim is wrong. 제9조① sets 14 days; an extension needs 특별한 사정 plus 당사자 합의; the law has no "한 달" rule. **STANDS**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=284455&chrClsCd=010202&urlMode=lsInfoP&efYd=20260918&ancYnChk=0 (제9조제1항)
- Quote: "사용자는 근로자가 퇴직한 경우에는 그 지급사유가 발생한 날부터 14일 이내에 퇴직금을 지급하여야 한다. 다만, 특별한 사정이 있는 경우에는 당사자 간의 합의에 따라 지급기일을 연장할 수 있다. <개정 2021. 4. 13.>"
- No amendment in 2025-2026 touches 제9조①. (제9조② was amended 2026. 3. 17.; see F10.)

### F2. Dates: last working day 9/20 (Sun) → 퇴직일 9/21; deadline 10/4~10/5 무렵; on 10/22 more than 2 weeks have passed; "9/21부터 31일째"; the company's "한 달" has passed. **NEEDS CHANGE (minor)**
- Confirmed: 2026-09-20 was a Sunday. The 노동포털 convention is "퇴직일자는 마지막으로 근무한 날의 1일 후 날짜를 기재" (https://labor.moel.go.kr/cmmt/calRtrmnt.do). 10/22 is 17 days after 10/5. 한 달 after 9/20 is 10/20, which has passed.
- Wrong: **"9/21부터 31일째"**. 10/22 − 9/21 = 31 days elapsed. Counting 9/21 as day 1 (the "째" sense), 10/22 is the **32일째**.
- Window too narrow: 2026-10-03 (개천절) is a Saturday and **10/5 (Mon) is a 대체공휴일**. 10/4 is a Sunday. If 민법 제161조 (말일이 토요일·공휴일이면 익일 만료) applies through 민법 제155조, the 14-day period ends on **10/6**. I could not find a 고용노동부 해석 that settles this (see "could not decide"). Either way the deadline had passed well before 10/22.
- Stale anchor: "오늘(10/22)". The check date is 10/23-24; the key should not fix "today".
- Corrected wording: 「마지막 근무일이 9/20(일)이면 퇴직일은 9/21이고, 14일 기한은 10월 초(10/4, 휴일 계산 방식에 따라 늦어도 10/6)입니다. 10/22 기준으로 기한이 2주 넘게 지났고(9/21부터 31일 경과), 회사가 말한 "한 달"(10/20)도 이미 지났습니다.」

---

## 정확한 금액과 계산 과정

### F3. 평균임금 basis: 990만 (110+330+330+220) ÷ 92 = 107,608.70; ×30 = 3,228,261; ×1,158/365 = 10,241,990; matches the 노동포털 calculator. **STANDS**
- I reproduced it on https://labor.moel.go.kr/cmmt/calRtrmnt.do (2026-10-24) with 입사 2023.7.21, 퇴직 2026.9.21 and 기본급 1,100,000 / 3,300,000 / 3,300,000 / 2,200,000. Calculator output: 재직일수 "1158", periods "2026.6.21 ~ 2026.6.30 10 / 7.1~7.31 31 / 8.1~8.31 31 / 9.1~9.20 20", 합계 "92", "1일 평균임금 107,608.7", "퇴직금 10,241,990".
- Independent recomputation: 9,900,000/92 = 107,608.6957; ×30 = 3,228,260.87; ×1158/365 = 10,241,989.3. The calculator multiplies the 1-decimal value 107,608.7 and rounds, which gives 10,241,990. Days 2023-07-21 → 2026-09-21 = 1,158; 2023-07-20 → 2026-09-20 also = 1,158.
- Law: 근로기준법 제2조제1항제6호 "“평균임금”이란 이를 산정하여야 할 사유가 발생한 날 이전 3개월 동안에 그 근로자에게 지급된 임금의 총액을 그 기간의 총일수로 나눈 금액을 말한다." (https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285279&chrClsCd=010202&urlMode=lsInfoP&efYd=20261008&ancYnChk=0); 퇴직급여법 제8조① "계속근로기간 1년에 대하여 30일분 이상의 평균임금".

### F4. 통상임금 floor: 3,300,000 ÷ 209 × 8 = 126,315.79 > 107,608.70 → ×30 × 1,158/365 = 12,022,495; "노동포털 계산기와 법제처 해석(법제처-26-0209)도 같은 방식". **NEEDS CHANGE (attribution only; the numbers stand)**
- Numbers: the calculator with 1일 통상임금 "126,315.79" returns "12,022,495". My recomputation: 126,315.789 × 30 × 1158/365 = 12,022,494.6.
- The rule stands. 근로기준법 제2조② (same URL): "제1항제6호에 따라 산출된 금액이 그 근로자의 통상임금보다 적으면 그 통상임금액을 평균임금으로 한다." Calculator text: "1일 통상임금이 1일 평균임금보다 클 경우 1일 통상임금을 기준으로 퇴직금이 계산됩니다." The calculator's calRet() code switches to comPay when avrPay < comPay.
- The conversion stands, but its source is 근로기준법 시행령 제6조②4·③, not 법제처 (https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=270551&chrClsCd=010202&urlMode=lsInfoP&efYd=20251023&ancYnChk=0): "월급 금액으로 정한 임금은 그 금액을 월의 통상임금 산정 기준시간 수 … 로 나눈 금액" / "③제1항에 따른 통상임금을 일급 금액으로 산정할 때에는 제2항에 따른 시간급 금액에 1일의 소정근로시간 수를 곱하여 계산한다."
- Overstated: "법제처 해석도 같은 방식". 법제처-26-0209 (회신 2026. 5. 26., https://opinion.lawmaking.go.kr/nl4li/lsItptEmp/444368?mode=all) does exist. It holds only that the 통상임금 floor applies to 퇴직금: "「근로기준법」 제2조제2항에 따라 통상임금을 평균임금으로 하여 퇴직금을 산정하여야 합니다." It says nothing about the ÷209×8 method.
- Corrected wording: 「… 1일 통상임금은 3,300,000 ÷ 209 × 8 = 126,315.79원(근로기준법 시행령 제6조)입니다. 평균임금보다 높으므로 통상임금으로 계산합니다(근로기준법 제2조제2항; 퇴직금에도 적용된다는 법제처 해석 법제처-26-0209, 2026.5.26.): 126,315.79 × 30 × 1,158/365 = 약 12,022,495원. 노동포털 계산기 결과도 같습니다.」

### F5. Range 약 1,024만 ~ 1,202만; non-통상 items put it in between; 입사일 shifts it; "질문에 나온 '약 1,020만 원 안팎'은 평균임금만 쓴 하한값". **NEEDS CHANGE**
- The range stands (F3, F4). The "in between" logic stands: if part of the 330만 is non-통상, the 통상임금 falls, and the result runs from 10,241,990 (평균임금 basis) up to 12,022,495.
- Wrong: **"질문에 나온 '약 1,020만 원 안팎'"**. The user's question (prompts/ko-severance-pay.txt) contains no figure. The 1,020만 comes from the checked draft's own item 6. As written, the key would credit the user with a number they never gave.
- Corrected wording: 「정리하면 약 1,024만 원 ~ 1,202만 원입니다. 평균임금만으로 계산한 약 1,024만 원이 하한이고, 330만 원이 전부 통상임금이면 약 1,202만 원입니다. 연장근로수당 같은 비통상 항목이 섞여 있으면 그 사이 값이 되고, 입사일·마지막 근무일이 하루 이틀 다르면 금액도 조금 달라집니다.」

### F6. Add 3/12 of last year's unused-연차 수당; exclude 연차수당 that arises because of retirement (고용노동부 해석). **STANDS**
- URL: https://www.moel.go.kr/minwon/fastcounsel/fastcounselView.do?inetDcssMngId=201707140941334611000
- Quote: "퇴직 전전년도 출근율에 의하여 퇴직 전년도에 발생한 연차유급휴가 중 미사용하고 근로한 일수에 대한 연차유급휴가미사용수당액의 3/12을 퇴직금 산정을 위한 평균임금 산정 기준임금에 포함시킵니다." / retirement-triggered 수당: "평균임금의 정의상 산정사유 발생일 이전에 그 근로자에 대하여 지급된 임금이 아니므로 … 포함되지 않습니다."
- The calculator's worked example applies the same rule ("연차수당 가산액 … × (3개월/12개월)").

---

## 답변에 덧붙기 쉬운 주장과 올바른 값

### F7. Penalty: 제43조, 5년/5천만, from 2026-09-18 (법률 제21475호); old 제44조 3년/3천만 applies before that; 생활법령 is stale; 반의사불벌 kept, with the 명단공개 exception. **STANDS**
- URL: U1 (lsiSeq=284455). 제43조: "다음 각 호의 어느 하나에 해당하는 자는 5년 이하의 징역 또는 5천만원 이하의 벌금에 처한다. 다만, 제1호 및 제2호의 경우(「근로기준법」 제43조의2에 따라 명단 공개된 체불사업주가 명단 공개 기간 중에 제1호 또는 제2호에 해당하는 경우는 제외한다) 피해자의 명시적인 의사에 반하여 공소를 제기할 수 없다. <개정 2021. 4. 13., 2026. 3. 17.>" / "1. 제9조제1항을 위반하여 퇴직금을 지급하지 아니한 자".
- 제44조 now covers only 퇴직연금사업자 violations (제27조④, 제33조③④).
- 부칙 <법률 제21475호, 2026. 3. 17.> 제1조: "이 법은 2026년 7월 1일부터 시행한다. 다만, 제43조와 제44조의 개정규정은 공포 후 6개월이 경과한 날부터 시행한다." That date is 2026-09-18, matching the page header. The 부칙 has no 경과조치 for penalties, so the law in force at the time of the act governs. The deadline here expired in early October, so the new penalty applies.
- Stale secondary sources, confirmed: 생활법령 (https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=999&ccfNo=3&cciNo=2&cnpClsNo=1) says "3년 이하의 징역 또는 3천만원 이하의 벌금에 처해집니다" under 제44조 and is "2026년 9월 15일 기준". Also lagging, though not a 퇴직급여법 page: MOEL's own 노동포털 page (https://labor.moel.go.kr/minwonSysInfo/wagesolway.do) still says "임금체불 사업주는 3년 이하의 징역 또는 3,000만원 이하의 벌금형에 처함". 근로기준법 제107조① has made that 5년/5천만 since 2026-10-08. Graders should expect stale figures even from official portals.
- Optional addition (not needed for the key): 제47조(양벌규정) still reads "제44조부터 제46조까지", so the key correctly avoids claiming a 법인 fine.

### F8. 지연이자 연 20% from the day after the 14th day until payment; about 5,600원/day at 1,024만; "도산이나 금액 다툼 등 시행령 제18조 사유가 있으면 적용되지 않습니다". **NEEDS CHANGE (minor wording)**
- Rate and start date stand. 근로기준법 제37조①: "… 그 다음 날부터 지급하는 날까지의 지연 일수에 대하여 … 대통령령으로 정하는 이율에 따른 지연이자를 지급하여야 한다." / "1. 제36조에 따라 지급하여야 하는 임금 및 「근로자퇴직급여 보장법」 제2조제5호에 따른 급여(일시금만 해당된다): 지급 사유가 발생한 날부터 14일이 되는 날". 시행령 제17조: "“대통령령으로 정하는 이율”이란 연 100분의 20을 말한다. <개정 2025. 4. 8.>"
- Daily amount: 10,241,990 × 0.20 / 365 = 5,612원 (stands). For the upper figure, 12,022,495 → 6,588원.
- Imprecise: the exceptions do not switch interest off for good; they suspend it only while the cause lasts. 제37조③: "제1항은 사용자가 천재ㆍ사변, 그 밖에 대통령령으로 정하는 사유에 따라 임금 지급을 지연하는 경우 그 사유가 존속하는 기간에 대하여는 적용하지 아니한다." The dispute ground is narrower than "금액 다툼". 시행령 제18조3호: "지급이 지연되고 있는 임금 및 퇴직금의 전부 또는 일부의 존부(存否)를 법원이나 노동위원회에서 다투는 것이 적절하다고 인정되는 경우".
- Corrected wording: 「… 연 20%입니다(근로기준법 제37조, 시행령 제17조). 1,024만 원 기준 하루 약 5,600원, 1,202만 원 기준 약 6,600원입니다. 도산, 법령상 자금 제약, 또는 지급의무의 존부를 법원·노동위원회에서 다투는 것이 적절하다고 인정되는 경우(시행령 제18조)에는 그 사유가 존속하는 기간 동안만 지연이자가 적용되지 않습니다.」

### F9. 퇴직소득세: the company withholds it plus 10% 지방소득세; 근속연수 4년; about 9.4만 / 14.1만; no withholding at the time of an IRP transfer. **NEEDS CHANGE (ordering; the numbers stand)**
- Rules confirmed in the current 소득세법 (U5, lsiSeq=280405). 제48조①: 근속연수 "1년 미만의 기간이 있는 경우에는 이를 1년으로 보며". Table: "5년 이하 100만원 × 근속연수"; 환산급여공제 "8백만원 초과 7천만원 이하 8백만원 + (8백만원초과분의60퍼센트)". 제55조① 6% to 1,400만. 제55조②: "1. 해당 과세기간의 퇴직소득과세표준에 제1항의 세율을 적용하여 계산한 금액 2. 제1호의 금액을 12로 나눈 금액에 근속연수를 곱한 금액". 지방세법 제103조의13①: "원천징수하는 소득세 … 의 100분의 10에 해당하는 금액을 … 개인지방소득세로 특별징수".
- Recomputation:
  - 10,241,990 → 환산급여 18,725,970 − 공제 14,435,582 = 과표 4,290,388 → 소득세 85,808 + 지방 8,581 = **94,389원**
  - 12,022,495 → 24,067,485 − 17,640,491 = 6,426,994 → 128,540 + 12,854 = **141,394원**
  - Both match the key.
- Ordering problem: the key opens with "회사가 원천징수하며". Under F10, an IRP transfer is mandatory here (over 300만 and, if under 55, no exception applies). 소득세법 제146조② then says: "… 해당 퇴직소득에 대한 소득세를 연금외수령하기 전까지 원천징수하지 아니한다." / "1. 퇴직일 현재 연금계좌에 있거나 연금계좌로 지급되는 경우". So for this worker the default is no tax at payment. The 9.4만~14.1만 falls due when the money leaves the IRP other than as a pension. Withholding at payment is the exception case, for example a worker aged 55 or over who takes cash.
- Corrected wording: 「퇴직소득세: 55세 미만이면 퇴직금이 IRP로 이전되므로 지급 시점에는 원천징수하지 않고(소득세법 제146조②), IRP에서 연금 외로 찾을 때 과세됩니다. 그때의 세액은 근속연수 4년(1년 미만은 1년) 기준 퇴직소득세에 지방소득세 10%를 더해 1,024만 원이면 약 9.4만 원, 1,202만 원이면 약 14.1만 원입니다(추정). IRP 예외(55세 이상 등)로 현금 지급되면 회사가 이 금액을 원천징수합니다.」

### F10. IRP rule applies to the plain 퇴직금제도 too; payment by transfer to the worker's designated IRP (제9조②); exceptions 55+, ≤300만 (고시 제2026-65호), 사망, 외국인 출국 등. **STANDS**
- 제9조② (U1): "제1항에 따른 퇴직금은 근로자가 지정한 개인형퇴직연금제도의 계정 또는 제23조의8제1항에 따른 계정 … 으로 이전하는 방법으로 지급하여야 한다. 다만, 근로자가 55세 이후에 퇴직하여 급여를 받는 경우 등 대통령령으로 정하는 사유가 있는 경우에는 그러하지 아니하다. <신설 2021. 4. 13., 2026. 3. 17.>" 제9조③: "근로자가 제2항에 따라 개인형퇴직연금제도의 계정등을 지정하지 아니한 경우에는 근로자 명의의 개인형퇴직연금제도의 계정으로 이전한다."
- 시행령 제3조의2① (https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=284693&chrClsCd=010202&urlMode=lsInfoP&efYd=20260324&ancYnChk=0) lists 1. 55세 이후 퇴직, 2. 고시 금액 이하, 3. 사망, 4. 취업 체류자격 외국인 출국, 5. 다른 법령에 따른 공제.
- 고시 제2026-65호 (https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000284960&chrClsCd=010201, read in the document viewer): "“퇴직급여액이 고용노동부장관이 정하는 금액 이하인 경우”란 300만원 이하인 경우를 말한다." Applicability: "이 고시는 시행 후 최초로 급여를 지급할 사유가 발생한 경우부터 적용한다"; "2026년 9월 1일부터 시행". The 9/20 retirement falls under it.
- Optional addition: if the worker names no IRP, the company transfers the money to an IRP in the worker's name (제9조③).

### F11. 진정: online at 노동포털 or at the 관할 지방고용노동관서; 25일 with 2 extensions; 1350. **STANDS**
- URL: https://labor.moel.go.kr/minwonSysInfo/wagesolway.do
- Quotes: "홈페이지 "노동포털"에서 온라인으로 "임금체불 진정"을 제기하거나, 사업장 소재지 관할 고용노동관서 고객지원실을 방문하여 사전 상담 후 진정 또는 고소하실 수 있습니다." / "처리기간은 25일(토요일·공휴일 제외)이며, 2차에 걸쳐 연장 가능" / "1차는 근로감독관의 직권, 2차는 진정인의 동의가 필요합니다." / "고용노동부 고객상담센터 1350".
- Optional precision: the 25 days exclude Saturdays and public holidays.

### F12. 대지급금: a backstop; 진정 → 체불 임금등·사업주 확인서 → 간이대지급금; 진정 within 1 year from the day after retirement; claim within 6 months of the 확인서; caps 퇴직급여 700만, total 1,000만; litigation route with suit within 2 years. **STANDS**
- 임금채권보장법 제7조①5 (https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=283451&chrClsCd=010202&urlMode=lsInfoP&efYd=20260820&ancYnChk=0): "고용노동부장관이 근로자에게 제12조에 따라 체불임금등과 체불사업주 등을 증명하는 서류(이하 “체불 임금등ㆍ사업주 확인서”라 한다)를 발급하여 사업주의 미지급임금등이 확인된 경우". 제7조②2가: "… 최종 3년간의 퇴직급여등".
- 시행령 제7조② (https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285855&chrClsCd=010202&urlMode=lsInfoP&efYd=20260512&ancYnChk=0): "1. … 사업에서 퇴직한 날의 다음 날부터 2년 이내에 … 소송 등 … 을 제기한 근로자" / "2. … 사업에서 퇴직한 날의 다음 날부터 1년 이내에 임금등의 체불을 이유로 해당 사업주에 대한 진정ㆍ청원ㆍ탄원ㆍ고소 또는 고발 등 … 을 제기한 근로자". 시행령 제9조①3: "체불임금등ㆍ사업주확인서가 최초로 발급된 날부터 6개월 이내".
- Caps: 노동포털 (U12): "최대 1,000만원 상한(임금 등 700만원, 퇴직급여 등 700만원)". Cap 고시 제2021-81호 is still the one law.go.kr resolves as current. Searches found no 2025-2026 increase. The 2026 amendments (법 제7조② 2026. 2. 19.; 시행령 2026. 5. 6.: 변제금 rules) changed no amounts.
- Optional precision: the employer must also have run the business at least 6 months up to the retirement date (시행령 제8조③1).

### F13. 시효 3년 (퇴직급여법 제10조). **STANDS**
- U1 제10조: "이 법에 따른 퇴직금을 받을 권리는 3년간 행사하지 아니하면 시효로 인하여 소멸한다."

### F14. 3배 손해배상 (근로기준법 제43조의8) does not apply to 퇴직금. **STANDS**
- U3 제43조의8①1: "명백한 고의로 임금등(「근로자퇴직급여 보장법」 제2조제5호의 급여는 제외한다. 이하 이 조에서 같다)의 전부 또는 일부를 지급하지 아니한 경우" [본조신설 2024. 10. 22.]. No pending amendment marker.

### F15. Other money (last month's pay, unused 연차수당) is also due within 14 days (근로기준법 제36조). **STANDS**
- U3 제36조: "사용자는 근로자가 사망 또는 퇴직한 경우에는 그 지급 사유가 발생한 때부터 14일 이내에 임금, 보상금, 그 밖의 모든 금품을 지급하여야 한다. 다만, 특별한 사정이 있을 경우에는 당사자 사이의 합의에 의하여 기일을 연장할 수 있다."
- Context (not in the key bullet): the penalty is now 제107조① 5년/5천만 with 반의사불벌 in 제107조②. 제109조② was deleted <2026. 4. 7.>. 시행 is "공포 후 6개월" = 2026-10-08 (부칙 <법률 제21533호> 제1조). Item 15 of the source is correct.

### F16. 경우에 따라 달라지는 것: DB/DC; the 통상임금 share of 330만; exact dates; age (55+); 관할 by 사업장 소재지. **STANDS**
- 관할: "사업장 소재지 관할 고용노동관서" (U12). Age: 시행령 제3조의2①1. 통상임금 share: 시행령 제6조①. The DB/DC point fits the structure of 퇴직급여법 (제4조①, DB/DC chapters). It is framed as a condition, not as a figure.

---

## Could not be decided
1. **Does the 14-day period stretch to 10/6?** 10/4 is a Sunday and 10/5 a 대체공휴일 for 개천절; 민법 제161조 applies through 민법 제155조. I found no 고용노동부/법제처 interpretation that applies or rejects 제161조 for 퇴직급여법 제9조 or 근로기준법 제36조·제37조. The deadline lands somewhere from 10/3 to 10/6 depending on the 퇴직일 reading and holiday counting. This does not change any conclusion, because the deadline had passed long before 10/22.
2. **Which money figure applies, 10,241,990 or 12,022,495?** That depends on the payslip (whether all of the 330만 is 통상임금) and the 소정근로시간. Neither is in the request. The key already frames this as a range.
3. **The cap table in 고시 제2021-81호** is an image on law.go.kr and could not be read as text. The caps (700/700/총 1,000만) were confirmed instead from MOEL's 노동포털 page quoted in F12.
