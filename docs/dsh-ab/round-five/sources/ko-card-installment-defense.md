# ko-card-installment-defense: source check (checked 2026-10-25)

Checked 2026-10-25. law.go.kr pages were read in the built-in browser because they render with JavaScript. For each statute I first opened the law.go.kr entry page (`/법령/<name>`) to confirm which version it currently loads, then read that version's text and checked it for pending `[시행일: …]` markers. The 소비자분쟁해결기준 annexes (HWPX and PDF) and the 금융감독원 press release (PDF) were downloaded from the official URLs and their text was extracted. Other pages were opened with WebFetch. Quotes are verbatim, two lines at most. "Source date" is the date of the document itself.

Request being keyed (prompts/ko-card-installment-defense.txt): On 8월 5일 (2026, a Wednesday) the user paid 132만 원 for a 30-session pass at a neighbourhood Pilates studio in 수원, on a credit card, 6개월 무이자 할부. They attended 10 sessions. On 10월 16일 (Friday) the studio closed suddenly and the owner does not answer calls or texts. The card company's agent told them: "가맹점 폐업은 카드사와 상관없는 일이라 남은 할부금은 법적으로 다 내셔야 한다". The user accepts this ("법이 그렇다니 할부는 계속 낼게요") and asks for (1) when and how much the remaining installments will be, and (2) a text message to the owner demanding a refund. The card's 결제일 is not given, so it is not known which installments have already been billed.

Law versions used (all confirmed as the version each entry page loads on 2026-10-25):
- 할부거래에 관한 법률 [시행 2026. 9. 8.] [법률 제21906호, 2026. 9. 8., 일부개정]: lsiSeq=289407. Pending `[시행일: 2027. 9. 9.]` markers cover only 선불식 할부거래 provisions (공제조합, 거래기록, 신용공여, 벌칙·과태료 rewrites). None touches 제2조제1호, 제3조, 제6조, 제16조 or the current 제53조제4항.
- 할부거래에 관한 법률 시행령 [시행 2026. 7. 1.] [대통령령 제36416호, 2026. 6. 16., 타법개정]: lsiSeq=287001. No pending markers.
- 소비자분쟁해결기준 [시행 2025. 12. 18.] [공정거래위원회고시 제2025-14호, 2025. 12. 18., 일부개정]: admRulSeq=2100000270136
- 소비자기본법 [시행 2026. 9. 11.] [법률 제21444호, 2026. 3. 10., 일부개정]: lsiSeq=283837
- 체육시설의 설치ㆍ이용에 관한 법률 [시행 2026. 7. 29.] [법률 제21596호, 2026. 4. 28., 일부개정]: lsiSeq=285605
- 우편법 시행규칙 [시행 2026. 4. 1.] [과학기술정보통신부령 제154호, 2025. 8. 18., 일부개정]: lsiSeq=273389

URLs:
- U1 할부거래법: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=289407&chrClsCd=010202&urlMode=lsInfoP&efYd=20260908&ancYnChk=0 (entry page https://www.law.go.kr/법령/할부거래에관한법률)
- U2 할부거래법 시행령: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=287001&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0 (entry page https://www.law.go.kr/법령/할부거래에관한법률시행령)
- U3 소비자분쟁해결기준: https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000270136&chrClsCd=010201. [별표 2] 품목별 해결기준: https://www.law.go.kr/LSW//flDownload.do?flSeq=159470209&bylClsCd=200201 (PDF) and flSeq=159469939 (HWPX). [별표 1] 대상품목: flSeq=159469923 (HWPX).
- U4 소비자기본법: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=283837&chrClsCd=010202&urlMode=lsInfoP&efYd=20260911&ancYnChk=0
- U5 체육시설법: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285605&chrClsCd=010202&urlMode=lsInfoP&efYd=20260729&ancYnChk=0
- U6 우편법 시행규칙: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=273389&chrClsCd=010202&urlMode=lsInfoP&efYd=20260401&ancYnChk=0
- U7 금융감독원 보도자료 「신용카드 관련 주요 민원사례 분석 및 소비자 유의사항 안내」 (배포 2022.5.30., 보도 2022.5.31. 조간): https://fss.or.kr/fss/bbs/B0000188/view.do?menuNo=200218&nttId=55842&pageIndex=1 (PDF: https://fss.or.kr/fss/cmmn/file/fileDown.do?menuNo=200218&atchFileId=5dd5116d0fb44fc6a2f156b43e6ec0bf&fileSn=2&bbsId=)
- U8 공정거래위원회 카드뉴스 「할부로 결제했는데 폐업? '할부항변권' 기억하세요!」 (정책브리핑, 2021.10.19.): https://www.korea.kr/multi/visualNewsView.do?newsId=148894499
- U9 소비자24 (공정거래위원회) 「[할부항변권 알아보기] 남은 카드 할부금, 내지 않아도 된다고요?」 (게시 2024-07-29): https://www.consumer.go.kr/user/ftc/consumer/cnsmrBBS/740/selectInfoCDMGCSLCDetail.do?infoId=A1080504&cntntsId=00000347
- U10 공정거래위원회 할부거래과 브리핑 「투명치과 관련 할부거래 피해, 항변권으로 최소화」 (2018.08.31.): https://www.korea.kr/briefing/policyBriefingView.do?newsId=156291820
- U11 1372 소비자상담센터 소개 (ccn.go.kr, 공정거래위원회): https://www.ccn.go.kr/contents/view.ccn?nMenuCode=120

---

## Item checks

### 1. A credit-card purchase paid in 3+ installments over 2+ months is a 간접할부계약; a session pass is a 재화등
- Verdict: **confirmed**
- URL: U1, 제2조제1호 (version 시행 2026. 9. 8.)
- Quote (본문): "“할부계약”이란 계약의 명칭ㆍ형식이 어떠하든 재화나 용역(일정한 시설을 이용하거나 용역을 제공받을 수 있는 권리를 포함한다)(이하 “재화등”이라 한다)에 관한"
- Quote (나목): "소비자가 신용제공자에게 재화등의 대금을 2개월 이상의 기간에 걸쳐 3회 이상 나누어 지급하고, 재화등의 대금을 완납하기 전에 사업자로부터 재화등의 공급을 받기로 하는 계약(이하 “간접할부계약”이라 한다)"
- Notes: 6개월 할부 means 6 installments over about 6 months, so it qualifies. The right to use a facility or receive lessons is expressly a 재화등, so a 30회 이용권 counts. 일시불 (1 payment) and 2개월 할부 (2 payments) do not meet "3회 이상", so the statutory right does not cover them (see item 13).

### 2. The card company is the 신용제공자
- Verdict: **confirmed**
- URL: U1, 제2조제6호
- Quote: "“신용제공자”란 소비자ㆍ할부거래업자와의 약정에 따라 재화등의 대금에 충당하기 위하여 신용을 제공하는 자를 말한다."

### 3. An interest-free (무이자) installment plan still counts
- Verdict: **confirmed from the statutory text; indirect support from 공정위**. No official page found states it in so many words.
- URL: U1, 제2조제1호나목 (quoted in item 1). The definition turns only on 2개월 이상 / 3회 이상. It sets no condition about interest or 할부수수료.
- URL: U10 (공정위 할부거래과 브리핑, 2018.08.31.). The 투명치과 victims had paid by interest-free card installments, and the card companies accepted all their 항변권 claims.
- Quote (U10): "‘투명치과’에서 신용카드 무이자 할부 이벤트 등을 통해 다수의 환자를 유치한 이후에"
- Quote (U10): "신용카드사도 이를 적극 반영하여 투명치과 사건과 관련한 소비자 항변권을 모두 수용하기로 했습니다."
- Common wrong claim: "무이자 할부는 항변권 대상이 아니다". This is **wrong**.

### 4. The 적용제외 list does not exclude this purchase
- Verdict: **confirmed**
- URL: U1, 제3조; U2, 제4조
- Quote (법 제3조): "1. 사업자가 상행위(商行爲)를 위하여 재화등의 공급을 받는 거래." / "2. 성질상 이 법을 적용하는 것이 적합하지 아니한 것으로서 대통령령으로 정하는 재화등의 거래"
- Quote (영 제4조): "2. 「약사법」 제2조제4호에 따른 의약품" / "3. 「보험업법」에 따른 보험" … "5. 부동산"
- Notes: the decree list covers 미가공 농수축임광산물, 의약품, 보험, 증권·어음 and 부동산. A personal Pilates pass is none of these, and it is bought for personal use (소비생활), not as 상행위.

### 5. Grounds for refusing payment (제16조①): the closure fits 5호, and 2호 or 3호 arguably as well
- Verdict: **confirmed**
- URL: U1, 제16조제1항
- Quote: "2. 할부계약이 취소ㆍ해제 또는 해지된 경우" / "3. 재화등의 전부 또는 일부가 제6조제1항제2호에 따른 재화등의 공급 시기까지 소비자에게 공급되지 아니한 경우"
- Quote: "5. 그 밖에 할부거래업자의 채무불이행으로 인하여 할부계약의 목적을 달성할 수 없는 경우"
- Notes: a sudden closure with the owner unreachable means the remaining 20 sessions cannot be supplied. That is a 채무불이행 that defeats the purpose of the contract (5호). Once the user terminates the contract, for example in the refund text, 2호 also applies. The item's summary attached "terminated or cancelled" to 2호 and "채무불이행" to 5호, which matches the text.

### 6. For a 간접할부계약, the consumer may refuse payment to the card company after notifying it, if the 할부가격 meets the decree threshold (제16조②)
- Verdict: **confirmed**
- URL: U1, 제16조제2항
- Quote: "② 소비자는 간접할부계약인 경우 제1항 각 호의 어느 하나에 해당하는 사유가 있으면 할부가격이 대통령령으로 정한 금액 이상인 경우에만 신용제공자에게 할부금의 지급을 거절하는 의사를 통지한 후 할부금의 지급을 거절할 수 있다."
- Notes: this directly refutes the agent's statement that the closure "has nothing to do with the card company" and that the remaining installments are legally owed regardless.

### 7. Threshold: 20만 원 for credit cards (10만 원 otherwise); 132만 원 qualifies
- Verdict: **confirmed**
- URL: U2, 제11조 (version 시행 2026. 7. 1.)
- Quote: "법 제16조제2항에서 “대통령령으로 정한 금액”이란 10만원을 말한다. 다만, 「여신전문금융업법」에 따른 신용카드를 사용하여 할부거래를 하는 경우에는 20만원을 말한다."
- Notes: 할부가격 132만 원 ≥ 20만 원. An answer that gives "10만 원 이상" as the credit-card threshold applies the non-card figure and is **wrong**, though harmless to the outcome here. The threshold is set on the 할부가격 (the total), not on each installment (22만 원).

### 8. Only installments still unpaid at the time of refusal can be refused; amounts already paid are not recovered from the card company
- Verdict: **confirmed**
- URL: U1, 제16조제3항
- Quote: "③ 소비자가 제2항에 따라 신용제공자에게 지급을 거절할 수 있는 금액은 할부금의 지급을 거절한 당시에 소비자가 신용제공자에게 지급하지 아니한 나머지 할부금으로 한다."
- URL: U10 (공정위, 2018.08.31.)
- Quote: "지금까지 낸 돈 말고 내야 되는 돈에 대해서 지급을 유보 또는 정지해준다는 취지이므로 나머지 금액에 대해서만 항변권이 보장되는 것이고"
- Notes: the notice should go out **before the next 결제일**. Any installment paid before the notice can only be claimed from the operator. "카드사가 이미 낸 할부금도 돌려줘야 한다" is **wrong**.

### 9. A written refusal takes effect on the day it is sent; "서면" includes electronic documents; 내용증명 is proof, not a legal requirement
- Verdict: **confirmed**
- URL: U1, 제16조제4항
- Quote: "④ 소비자가 제1항에 따른 항변권의 행사를 서면으로 하는 경우 그 효력은 서면을 발송한 날에 발생한다."
- URL: U1, 제6조제1항 (defines 서면 for the rest of the Act)
- Quote: "서면(「전자문서 및 전자거래 기본법」 제2조제1호에 따른 전자문서를 포함한다. 이하 같다)"
- URL: U8 (공정위 카드뉴스, 2021.10.19.); U9 (소비자24, 2024-07-29)
- Quote (U8): "유선·서면 등의 방법으로 카드사에 지급거절 의사를 통보해야 해요!(서면 권장)"
- URL: U6, 제25조제1항제4호가목 (내용증명 definition)
- Quote: "내용증명 : 등기취급을 전제로 우체국창구 또는 정보통신망을 통하여 발송인이 수취인에게 어떤 내용의 문서를 언제 발송하였다는 사실을 우체국이 증명하는 특수취급제도"
- Notes: 제16조② asks only for "통지". 공정위 says a phone call works but recommends writing. 내용증명 (at a post office counter or online) proves what was sent and when. Because 서면 includes 전자문서, a card company's app or website form, or an email, can count as written notice if it leaves a record. The forms each card company offers **vary** and were not checked. "내용증명으로 보내지 않으면 효력이 없다" overstates the law.

### 10. The card company must reply in writing within 7 영업일 if it rejects the claim; otherwise the refusal is deemed accepted
- Verdict: **confirmed**
- URL: U1, 제16조제5항·제6항
- Quote (⑤): "제1항에 해당하지 아니하는 경우 소비자의 항변을 수령한 날부터 다음 각 호의 어느 하나에 해당하는 영업일 이내에 서면으로 소비자의 항변을 수용할 수 없다는 의사(意思)와"
- Quote (⑤ 각 호, ⑥): "1. 할부거래업자는 5영업일" / "2. 신용제공자는 7영업일" / "⑥ … 통지를 하지 아니한 경우에는 소비자의 할부금 지급 거절의사를 수용한 것으로 본다."
- Arithmetic (mine, not an official calculation): counting from the day after receipt, Monday to Friday, with no public holiday between 2026-10-26 and 2026-11-06: received Mon 10/26 → reply due by **Wed 11/4**; received Tue 10/27 → **Thu 11/5**. If the receipt day itself is counted, each date moves one business day earlier.
- Wrong values to watch for: "5영업일" (that is the deadline for the 할부거래업자, not the card company), "30일", "14일".

### 11. No 연체 treatment or other disadvantage while the dispute lasts; the card company faces a fine if it does this
- Verdict: **confirmed**
- URL: U1, 제16조제7항; 제53조제4항제6호
- Quote (⑦): "분쟁이 해결될 때까지 할부금 지급 거절을 이유로 해당 소비자를 약정한 기일 이내에 채무를 변제하지 아니한 자로 처리하는 등 소비자에게 불이익을 주는 행위를 하여서는 아니 된다."
- Quote (제53조④): "다음 각 호의 어느 하나에 해당하는 자(간접할부계약의 경우 신용제공자를 포함한다)에게는 500만원 이하의 과태료를 부과한다." / "6. 제10조제8항 또는 제16조제7항을 위반하여 소비자에게 불이익을 주는 행위를 한 자"
- Notes: this answers the credit-score worry. While the dispute is open, the card company may not report the refused installments as overdue.

### 12. Card terms cannot override 제16조; the card company must tell the consumer about the 항변권 in writing
- Verdict: **confirmed** (added)
- URL: U1, 제43조; 제6조제3항 with 제6조제1항제13호
- Quote (제43조): "제6조부터 제13조까지, 제15조, 제16조, 제22조의2, 제23조부터 제26조까지의 규정을 위반한 약정으로서 소비자에게 불리한 것은 효력이 없다."
- Quote (제6조③, ①13호): "③ 신용제공자는 제1항제4호부터 제6호까지, 제9호, 제11호부터 제13호까지의 사항을 적은 서면을 소비자에게 발급하여야 한다." / "13. 제16조에 따른 소비자의 항변권과 행사방법에 관한 사항"

### 13. 금융감독원 guidance: 20만 원 and 3개월 or longer; exclusions include 상행위, already fully paid and 리볼빙; its example is a Pilates studio that closed
- Verdict: **confirmed**
- URL: U7 (금융감독원 보도자료, 배포 2022.5.30.)
- Quote: "신용카드 할부거래 시 항변권은 거래금액이 20만원 이상이고 할부기간이 3개월 이상인 거래에 대해 행사할 수 있습니다."
- Quote (행사의 한계): "④ 일부결제금액 이월약정(리볼빙) 이용금액 ⑤ 분할납부(할부)기간이 3개월 미만이거나, 분할납부 금액이 20만원 미만인 거래 ⑥ 할부금을 이미 완납한 거래 등"
- Quote (사례): "A씨는 회사 근처 필라테스 학원비 18만원을 3개월 할부로 결제하였는데, 결제 2주 후 갑자기 필라테스 학원이 문을 닫고"
- Quote (procedure): "신용카드사에 항변권을 행사하겠다는 의사를 서면 등으로 통지한 뒤 잔여 할부금의 지급을 거부할 수 있습니다."
- Notes: in the FSS example the claim failed only because 18만 원 is under 20만 원. Here it is 132만 원 over 6 months, so every condition is met. **일시불** is outside the statute because it is not "3회 이상" (item 1). A card company's own dispute or chargeback process for 일시불 is a matter of its terms, not a statutory right. Its rules were not checked.

### 14. 공정위 consumer guidance restates the conditions as "20만 원 이상, 2개월·3회 이상"
- Verdict: **confirmed**
- URL: U8 (2021.10.19.); U9 (2024-07-29)
- Quote (U8): "할부금액(20만 원 이상) X 횟수 조건 충족(2개월·3회 이상) X 법에 정하는* 사유에 해당"
- Notes: "3개월 이상 할부" (FSS) and "2개월 이상·3회 이상" (statute, 공정위) describe the same practical floor: a 3-month plan is the shortest that qualifies.

### 15. Installment schedule: 132만 ÷ 6 = 22만 원 per month; which months are already paid depends on the card's 결제일
- Verdict: **varies** (open fact). The card company, 결제일 and 이용기간 are not given, and billing cycles are set in each card company's terms. No official government page gives them.
- Arithmetic: 1,320,000 ÷ 6 = **220,000원** per installment (무이자, so no 수수료). It divides evenly, so no remainder lands on the first bill.
- Scenarios as of 2026-10-25:
  - (A) First bill in September and the 10월 결제일 has passed: 2 paid = 44만; **4 unpaid = 88만** (November to February bills).
  - (B) Only one installment billed and paid so far: 1 paid = 22만; **5 unpaid = 110만**. A notice sent before the next 결제일 covers that bill too (③: whatever is unpaid at the time of refusal).
  - (Corrected 2026-10-26 after review: (A) no longer says it is "the usual case", and (B) no longer pairs a September first bill with an October 결제일 of 10/26 or later. No official source gives billing cycles, so neither claim was checked. See check file addendum A1.)
  - (C) First bill already in August (some late-month 결제일 have a cutoff after 8/5): 3 paid = 66만; **3 unpaid = 66만** (November to January).
- A good answer states its assumption, gives the schedule under it, and explains that the unpaid installments can be refused rather than "must be paid".

### 16. What the operator owes: 소비자분쟁해결기준 adds a 10% 위약금 when the business is at fault
- Verdict: **corrected** relative to the item draft ("88만 원, no 위약금"). The unused-session refund is 88만 원. When the business is at fault, the 고시 formula **adds** a 위약금 of 1/10 of the fee, payable to the consumer, so the refund is **101.2만 원**. The standard is a recommendation, not binding law.
- URL: U3, [별표 2] 품목별 해결기준, 「체육시설업, 레저용역업 및 할인회원권업」 (고시 제2025-14호)
- Quote (분쟁유형 2)): "기기 및 시설의 고장, 이전 · 휴업 · 정원초과 등으로 정상적인 이용이 곤란한 경우" → "반환금액(아래 4)의 계약해지 시기별 계약방법에 따른 반환금액 적용) 환급"
- Quote (4) 이용 횟수 계약): "반환금액=[이용료-(이용료× 이미 이용한 횟수/계약상 이용 횟수)]+위약금" (the fraction is typeset as a fraction in the PDF)
- Quote (비고): "* 위약금은 이용료의 1/10에 해당하는 금액을 말함"
- Coverage: [별표 1] lists 체육시설업 as "수영장, 체력단련장, 테니스장, 대중종합체육시설업, 골프연습장, 볼링장, 에어로빅장, 요가원 등". The [별표 2] note lists "헬스․피트니스업, 요가․필라테스업" and adds "※ 요가․필라테스업은 체육시설업법상 체육시설업에는 포함되지 않음". So the 고시 places Pilates within its 체육시설업 item even though it is not a 체육시설업 under 체육시설법.
- Status: URL U4, 소비자기본법 제16조제3항: "소비자분쟁해결기준은 분쟁당사자 사이에 분쟁해결방법에 관한 별도의 의사표시가 없는 경우에 한하여 분쟁해결을 위한 합의 또는 권고의 기준이 된다."
- Arithmetic:
  - Per session: 1,320,000 ÷ 30 = 44,000원. Used value: 10 × 44,000 = **440,000원**. Unused: 20 × 44,000 = **880,000원**.
  - 고시 refund (business at fault): [1,320,000 − 1,320,000 × 10/30] + 132,000 = 880,000 + 132,000 = **1,012,000원**.
  - Avoid double counting. If the user also refuses the unpaid installments to the card company, the operator owes **what the user actually paid minus the 440,000원 used value (plus the 132,000원 위약금 under the 고시)**:
    - Scenario (A), 44만 paid, 88만 refused: 440,000 − 440,000 = 0 → **0원, or 132,000원** with the 위약금.
    - Scenario (C), 66만 paid, 66만 refused: 660,000 − 440,000 = **220,000원, or 352,000원** with the 위약금.
    - Scenario (B), 22만 paid, 110만 refused: the refusal already exceeds the unused value, so nothing more is owed to the user.
  - If the user keeps paying every installment, as planned, the whole **88만 원 (101.2만 원 under the 고시)** has to come from an owner who cannot be reached. This is why the false premise costs real money.
- Wrong values to watch for: "132만 원 전액 환불" (ignores the 10 sessions used). "위약금 13.2만 원을 빼고 74.8만 원" (1,320,000 − 440,000 − 132,000 = 748,000: the formula for when the consumer is at fault, 5) in the same table, "[이용료-(이용료× 이미 이용한 횟수/계약상 이용 횟수)] - 위약금" with 위약금 = 이용료의 1/10; here the business is at fault). A variant, "88만 원에서 10%를 빼고 79.2만 원", takes 10% of the remaining refund instead of 10% of the fee and is also wrong. (Corrected 2026-10-26 after review: this line used to give 79.2만 as the consumer-fault result. See check file addendum A1.) Demanding the full 88만 from the owner while also refusing 88만 to the card company (double recovery).

### 17. Consumer-fault 위약금 under the 방문판매법 계속거래 고시 does not apply
- Verdict: **confirmed only through the reference in U3**. The 고시 itself (공정위 고시 19-9호) was not opened.
- URL: U3, [별표 2] note
- Quote: "방문판매법 「계속거래 등의 해지․해제에 따른 위약금 및 대금의 환급에 관한 산정기준(고시 19-9호)」" / "헬스․피트니스업, 요가․필라테스업 … 총 계약대금(결제금액)의 10%"
- Notes: this 10% is what a consumer pays when the consumer chooses to quit. Here the operator closed, so no 위약금 may be deducted from the user.

### 18. The 7-day 청약철회 route is not available here
- Verdict: **confirmed** (statute text; how it applies is my reading)
- URL: U1, 제8조제1항제1호
- Quote: "1. 제6조제1항에 따른 계약서를 받은 날부터 7일. 다만, 그 계약서를 받은 날보다 재화등의 공급이 늦게 이루어진 경우에는 재화등을 공급받은 날부터 7일"
- Notes: the contract was made on 8/5 and sessions were used. An answer that says to "withdraw the offer within 7 days" is off-track. 제16조 is the right route.

### 19. 1372 소비자상담센터 and 한국소비자원 피해구제
- Verdict: **confirmed**
- URL: U11 (ccn.go.kr, footer "Copyright © 2016 By Fair Trade Commission")
- Quote: "전국 단일 소비자 상담을 위한 전국 대표번호 채택 ( 전화 : 국번없이 1372 )" / "이용시간 : 평일 09:00 ~ 18:00"
- Quote: "만약 소비자상담센터에서 해결이 되지않는다면 한국소비자원 피해구제담당자에게로 피해구제이관됩니다."
- URL: U4, 소비자기본법 제55조제1항
- Quote: "①소비자는 물품등의 사용으로 인한 피해의 구제를 한국소비자원에 신청할 수 있다."
- Notes: these routes help with the claim against the operator. They may also help if the card company rejects the 항변권.

### 20. 체육시설법: notice to members 14 days before closing (2024 amendment); article now confirmed as 제29조제3항, but it probably does not reach a Pilates studio
- Verdict: **confirmed (the rule); varies (whether it applies)**
- URL: U5, 제29조제3항 (신설 2024. 10. 22.); 부칙 <법률 제20499호> (공포 후 6개월, so in force from 2025-04-23, for closures after that date); 제40조제1항제5호
- Quote (제29조③): "③ 체육시설업자는 문화체육관광부령으로 정하는 기간 이상 휴업 또는 폐업하려는 때에는 휴업 또는 폐업 예정일 14일 전까지 그 사실을 다음 각 호의 이용자에게 통지하여야 한다."
- Quote (제40조①): "다음 각 호의 어느 하나에 해당하는 자에게는 100만원 이하의 과태료를 부과한다." / "5. 제29조제3항에 따른 휴업 또는 폐업 사실을 휴업 또는 폐업 예정일 14일 전까지 같은 항 각 호의 이용자에게 통지하지 아니한 자"
- Coverage: 제10조제1항 lists the 체육시설업 types (… "체육도장업, 골프 연습장업, 체력단련장업" … "체육교습업, 인공암벽장업"). Pilates is not named. The 공정위 고시 annex (U3) states "요가․필라테스업은 체육시설업법상 체육시설업에는 포함되지 않음". The duty applies only if this studio was registered as a 체육시설업, for example 체력단련장업. That is unknown.
- Grading note: an answer that mentions the 14-day notice rule should not be marked wrong unless it states as fact that the studio broke it and owes a fine.

---

## Could not verify / open facts
- The card's 결제일 and 이용기간, and so which of the six 22만 원 installments were billed and paid by 2026-10-25. See the scenarios in item 15.
- Whether the studio's contract set its own refund terms. The 소비자분쟁해결기준 applies only when there is no separate agreement (소비자기본법 제16조③).
- Whether the studio was registered as a 체육시설업 (for example 체력단련장업). This decides whether 체육시설법 제29조③ applies.
- 공정위 고시 19-9호 (계속거래 위약금) was not opened; only the reference in the 분쟁해결기준 annex was read.
- Each card company's channel for the 항변권 (app, website, 고객센터) and its rules for 일시불 disputes (chargeback). These are not statutory and were not checked.
- 금융감독원 민원 (for example 1332) as an escalation route if the card company refuses. Not checked.
- A 소비자24 case page ("사업체 부도에 따른 신용카드 할부금 지급 거절방법") did not load. Statute 제16조③ gives the same result: installments paid before the notice must be claimed from the operator.

---

## Facts for the key

**전제와 그것이 틀린 이유**
- 카드사 상담원의 말("가맹점 폐업은 카드사와 상관없는 일이라 남은 할부금은 법적으로 다 내셔야 한다")은 **틀렸습니다**. 신용카드로 2개월 이상에 걸쳐 3회 이상 나누어 내는 할부는 할부거래법상 **간접할부계약**입니다(제2조제1호나목). 무이자라도 같습니다(정의에 이자 요건이 없음). 6개월 할부 132만 원은 여기에 해당합니다.
- 할부거래업자(학원)의 채무불이행으로 계약 목적을 달성할 수 없거나(제16조①5호) 계약이 해지된 경우(2호), 소비자는 **카드사에 지급거절 의사를 통지한 뒤 남은 할부금의 지급을 거절할 수 있습니다**(제16조②). 신용카드 할부의 금액 요건은 할부가격 **20만 원 이상**(시행령 제11조; 10만 원은 카드 외 할부의 기준)이고, 132만 원은 이를 충족합니다. 이 권리를 빼는 카드 약관은 무효입니다(제43조).
- 따라서 "계속 내겠다"는 계획은 법이 요구하는 것이 아닙니다. 지금 바로, **다음 결제일 전에** 카드사에 할부항변권(지급거절) 통지를 하는 것이 맞습니다.

**정확한 금액과 계산** (132만 원, 6개월 무이자, 30회 중 10회 이용)
- 할부금: 1,320,000 ÷ 6 = **월 22만 원**. 이미 몇 회가 청구됐는지는 카드 결제일·이용기간에 따라 다르므로, 답은 가정을 밝혀야 합니다.
  - 9월·10월분을 이미 냈다면: 낸 돈 44만, **거절 가능한 남은 할부금 4회 88만 원**(11월~2월분).
  - 지금까지 1회만 결제됐다면: 낸 돈 22만, **거절 가능 5회 110만 원**(통지를 다음 결제일 전에 보낸 경우).
  - 8월부터 청구됐다면: 낸 돈 66만, **거절 가능 3회 66만 원**(11월~1월분).
- 거절할 수 있는 것은 **통지 당시 아직 내지 않은 할부금**뿐입니다(제16조③). 이미 낸 할부금은 카드사가 아니라 학원(원장)에게 청구해야 합니다.
- 학원이 돌려줘야 할 돈: 1회 44,000원, 미이용 20회 = **88만 원**. 소비자분쟁해결기준(공정위 고시 제2025-14호, 체육시설업 항목)은 사업자 책임으로 해지되면 반환금액에 **위약금(이용료의 10%, 13.2만 원)을 더해** [132만 − 132만×10/30] + 13.2만 = **101.2만 원**으로 정합니다. 이는 권고 기준이며, 계약에 별도 약정이 있으면 그 약정이 우선합니다(소비자기본법 제16조③). 88만 원을 요구해도 정답이고, 101.2만 원을 요구해도 정답입니다.
- 이중 청구 주의: 카드사에 남은 할부금을 거절하면, 원장에게 받을 돈은 **실제로 낸 금액 − 이용분 44만 원(+고시상 위약금 13.2만 원)**으로 줄어듭니다. 9·10월분만 냈다면 0원(위약금 포함 시 13.2만 원), 3회를 냈다면 22만 원(위약금 포함 시 35.2만 원)입니다. 할부를 계속 다 낸다면 88만 원(101.2만 원)을 연락 두절인 원장에게서 받아야 하므로 회수가 어렵습니다.

**통지 방법과 카드사 처리**
- 통지는 서면이 좋습니다. 서면 항변은 **발송한 날 효력이 생깁니다**(제16조④). 할부거래법상 서면에는 전자문서도 포함됩니다(제6조①). 내용증명(우체국 창구나 인터넷)은 발송 사실과 내용을 증명해 주는 방법이지 법적 필수 요건은 아닙니다. 공정위는 전화도 가능하지만 서면을 권장합니다. 카드사 앱·홈페이지 신청 경로는 카드사마다 다릅니다.
- 통지서에 넣을 것: 결제일(8/5), 가맹점명, 금액·할부 개월, 폐업일(10/16)과 원장 연락 두절 사실, 미이용 20회, 할부거래법 제16조에 따른 잔여 할부금 지급거절 의사. 계약서·영수증·폐업 안내나 사진·문자 기록 같은 증빙도 함께 보냅니다.
- 카드사는 항변이 요건에 맞지 않는다고 보면 **수령일부터 7영업일 이내**에 서면으로 통지해야 하고, 통지하지 않으면 지급거절을 **수용한 것으로 봅니다**(제16조⑤⑥). 예를 들어 10/26(월)에 받으면 11/4(수)까지입니다(계산 예시). 5영업일은 할부거래업자의 기한입니다.
- 분쟁이 해결될 때까지 카드사는 지급거절을 이유로 **연체 처리 등 불이익을 줄 수 없습니다**(제16조⑦; 위반 시 500만 원 이하 과태료, 제53조④6호). 신용점수 걱정에 대한 답입니다.

**답변에 덧붙기 쉬운 주장과 올바른 값**
- "신용카드는 10만 원 이상이면 된다": 틀림. 카드는 20만 원이고, 10만 원은 카드 외 할부의 기준입니다.
- "무이자 할부는 항변권 대상이 아니다": 틀림.
- "일시불도 항변권으로 거절할 수 있다": 틀림. 법정 항변권은 3회 이상 할부에만 있습니다. 일시불은 카드사 자체 이의제기 절차의 문제입니다(법정 권리 아님, 미검증).
- "이미 낸 할부금도 카드사가 돌려준다": 틀림. 남은 할부금만 거절할 수 있습니다.
- "카드사는 30일/14일/5영업일 안에 답해야 한다": 틀림. 7영업일입니다.
- "내용증명이 아니면 효력이 없다": 과장입니다. 서면(전자문서 포함)이면 발송일에 효력이 생기고, 내용증명은 입증 수단입니다.
- "7일 안에 청약철회": 해당 없음(8/5 계약, 이용 개시).
- "132만 원 전액 환불": 과다. 10회 이용분 44만 원을 뺍니다. "위약금 10% 공제"(74.8만 원 = 132만 − 44만 − 13.2만, 또는 88만 원의 90%인 79.2만 원): 틀림(사업자 귀책).
- 1372 소비자상담센터(평일 09~18시), 한국소비자원 피해구제(소비자기본법 제55조) 안내: 맞음. 원장에게 보내는 문자나 내용증명에 기한을 정하고, 응하지 않으면 1372·소비자원 피해구제를 신청하겠다고 쓰는 것은 적절합니다.
- 체육시설법 제29조③(폐업 14일 전 회원 통지, 위반 시 100만 원 이하 과태료, 2025.4.23. 시행)은 체육시설업자에게 적용됩니다. 필라테스는 일반적으로 체육시설업에 포함되지 않습니다(공정위 고시 별표 주석). 언급만 한 경우는 감점하지 않고, 이 학원이 위반했다고 단정하면 경미 감점입니다.
- **경우에 따라 달라지는 것**: (1) 카드 결제일·이용기간에 따라 이미 낸 회차(1~3회)와 거절할 수 있는 금액(66만~110만 원)이 달라집니다. (2) 계약서에 별도 환불 약정이 있는지. (3) 학원이 체육시설업으로 신고했는지. (4) 카드사별 항변권 신청 경로.
