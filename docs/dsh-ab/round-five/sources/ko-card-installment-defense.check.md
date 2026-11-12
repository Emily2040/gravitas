# Adversarial check: ko-card-installment-defense.md, items and "Facts for the key"

Checked 2026-10-25 to 2026-10-26 (the local date changed to 2026-10-26 during the check) by an agent that did not write the source file. On disk I read only `prompts/ko-card-installment-defense.txt` and `sources/ko-card-installment-defense.md`. Every URL below was opened on those dates. For law.go.kr I first fetched each entry page (`/법령/<name>` or `/행정규칙/<name>`) to see which version it loads. I then fetched that version's text from the body endpoint that the `lsInfoP.do` page itself calls (`lsInfoR.do`, same `lsiSeq` and `efYd`). For 할부거래법 I also read the page in the built-in browser, which shows pending text inline. The 소비자분쟁해결기준 annexes, the 고시 제2019-9호 annex and the 금융감독원 PDF were downloaded from the official URLs and their text extracted (HWPX XML, PDF with pypdf, HWP 5.0 with a small reader). Other pages were fetched directly. Quotes are verbatim, two lines at most. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: no change was found, in force or promulgated, that would change a fact or make the premise true. (1) The 할부거래법 entry page still loads [시행 2026. 9. 8.] [법률 제21906호] (lsiSeq=289407). Its amendment list (`lsRvsDocListP.do?lsId=000355`) shows nothing after 법률 제21906호 (2026. 9. 8.). I opened the pending version that takes effect 2027. 9. 9. (same lsiSeq, efYd=20270909). Its 제16조 is identical to the current text, line for line. 제2조제1호·제6호, 제3조, 제6조제1항·제3항, 제6조제1항제13호, 제8조제1항 and 제43조 are also identical. The 2027 changes add definitions to 제2조 (5의2 선수금, 10 신용공여) and rewrite 선불식 provisions. They also re-enact 제53조, which moves the 500만원 과태료 paragraph from ④ to ⑤ without changing its content (see item 11). (2) The 시행령 entry page loads [시행 2026. 7. 1.] [대통령령 제36416호]. Its amendment list shows nothing newer, and the text has no pending markers. (3) The 소비자분쟁해결기준 history (`admRulHstListR.do`) lists 고시 제2025-14호 (시행 2025. 12. 18.) as the newest. The annex files used are attached to that version. (4) 소비자기본법: the newest is 법률 제21444호 (시행 2026. 9. 11.). (5) 체육시설법: one amendment is pending, 법률 제21750호 (2026. 6. 2., 시행 2026. 12. 3.). It only adds 제8조제3항 (opening hours and booking for public facilities) and does not touch 제10조, 제29조 or 제40조. (6) 고시 제2019-9호 (계속거래 위약금) is still the newest version of that 고시. (7) I scanned the 공정거래위원회 press list for 2026-09-01 to 2026-10-23 (84 items). The only 할부 items concern 선불식 할부거래 (a revised 지침 on 10-23, a quarterly disclosure on 10-20, a meeting on 09-30). Nothing concerns 간접할부 or the 항변권. The 금융감독원 press list for 2026-09-16 to 2026-10-25 has no 할부항변권 item. Not covered: bills pending in the 국회, 입법예고 of decree changes, and news. See the tooling note.

Tooling note: the shared WebSearch budget was already used up when this check began, and my first query was refused. I ran no open web search. Every check above used direct fetches of known official URLs and the official sites' own version-history and press-list pages.

## The premise

**P1. The card agent's statement ("가맹점 폐업은 카드사와 상관없는 일이라 남은 할부금은 법적으로 다 내셔야 한다") is false. A 6-month credit-card installment purchase of 132만 원 qualifies for the 할부항변권 against the card company.**
Status: **stands** (the premise is false and the correction stands)
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=289407&chrClsCd=010202&urlMode=lsInfoP&efYd=20260908&ancYnChk=0 (할부거래법, 제16조제2항)
- Quote: "② 소비자는 간접할부계약인 경우 제1항 각 호의 어느 하나에 해당하는 사유가 있으면 할부가격이 대통령령으로 정한 금액 이상인 경우에만 신용제공자에게 할부금의 지급을 거절하는 의사를 통지한 후 할부금의 지급을 거절할 수 있다."
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=287001&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0 (시행령 제11조)
- Quote: "다만, 「여신전문금융업법」에 따른 신용카드를 사용하여 할부거래를 하는 경우에는 20만원을 말한다."
- All conditions hold on the facts given: 6 payments over about 6 months (제2조제1호나목), 132만 원 ≥ 20만 원, personal use and not an excluded item (item 4), and a closure that defeats the contract (item 5). The premise would be true only if every installment had already been paid (제16조③). That is impossible here, since a 6-month plan from 8/5 runs into early 2027.

## Item checks (numbered as in the source)

**1. A credit-card purchase paid in 3+ installments over 2+ months is a 간접할부계약; a session pass is a 재화등.**
Status: **stands**
- URL: U1 above, 제2조제1호
- Quote: "1. “할부계약”이란 계약의 명칭ㆍ형식이 어떠하든 재화나 용역(일정한 시설을 이용하거나 용역을 제공받을 수 있는 권리를 포함한다)(이하 “재화등”이라 한다)에 관한"
- Quote (나목): "나. 소비자가 신용제공자에게 재화등의 대금을 2개월 이상의 기간에 걸쳐 3회 이상 나누어 지급하고, 재화등의 대금을 완납하기 전에 사업자로부터 재화등의 공급을 받기로 하는 계약(이하 “간접할부계약”이라 한다)"

**2. The card company is the 신용제공자.**
Status: **stands**
- URL: U1, 제2조제6호
- Quote: "6. “신용제공자”란 소비자ㆍ할부거래업자와의 약정에 따라 재화등의 대금에 충당하기 위하여 신용을 제공하는 자를 말한다."

**3. An interest-free (무이자) plan still counts.**
Status: **stands** (from the statutory definition, which has no interest condition; 공정위 support is indirect)
- URL: U1, 제2조제1호나목 (quoted in item 1)
- URL: https://www.korea.kr/briefing/policyBriefingView.do?newsId=156291820 (공정위 할부거래과 브리핑, 2018.08.31.)
- Quote: "‘투명치과’에서 신용카드 무이자 할부 이벤트 등을 통해 다수의 환자를 유치한 이후에"
- Quote: "신용카드사도 이를 적극 반영하여 투명치과 사건과 관련한 소비자 항변권을 모두 수용하기로 했습니다."
- Optional precision: the briefing says the clinic drew patients "through interest-free installment events and the like". It does not say every victim paid that way. The source's "The 투명치과 victims had paid by interest-free card installments" slightly overstates the quote. The conclusion rests on the statutory text and is unaffected.

**4. The 적용제외 list does not exclude this purchase.**
Status: **stands**
- URL: U1, 제3조
- Quote: "1. 사업자가 상행위(商行爲)를 위하여 재화등의 공급을 받는 거래." / "2. 성질상 이 법을 적용하는 것이 적합하지 아니한 것으로서 대통령령으로 정하는 재화등의 거래"
- URL: U2 (시행령), 제4조
- Quote: "2. 「약사법」 제2조제4호에 따른 의약품" / "3. 「보험업법」에 따른 보험" … "5. 부동산"
- The decree list is 1 미가공 농수축임광산물, 2 의약품, 3 보험, 4 증권·어음, 5 부동산. A Pilates pass is none of these.

**5. Grounds (제16조①): the closure fits 5호, and 2호 once the contract is terminated (3호 arguably).**
Status: **stands**
- URL: U1, 제16조제1항
- Quote: "2. 할부계약이 취소ㆍ해제 또는 해지된 경우" / "3. 재화등의 전부 또는 일부가 제6조제1항제2호에 따른 재화등의 공급 시기까지 소비자에게 공급되지 아니한 경우"
- Quote: "5. 그 밖에 할부거래업자의 채무불이행으로 인하여 할부계약의 목적을 달성할 수 없는 경우"

**6. For a 간접할부계약, the consumer may refuse payment to the card company after notifying it (제16조②).**
Status: **stands**
- URL: U1, 제16조제2항 (quoted under P1)

**7. Threshold: 20만 원 for credit cards (10만 원 otherwise); set on the 할부가격, not on each installment.**
Status: **stands**
- URL: U2, 제11조
- Quote: "법 제16조제2항에서 “대통령령으로 정한 금액”이란 10만원을 말한다. 다만, 「여신전문금융업법」에 따른 신용카드를 사용하여 할부거래를 하는 경우에는 20만원을 말한다."
- 제16조② ties the threshold to "할부가격", the total price. 132만 원 ≥ 20만 원.

**8. Only installments unpaid at the time of refusal can be refused; amounts already paid are not recovered from the card company.**
Status: **stands**
- URL: U1, 제16조제3항
- Quote: "③ 소비자가 제2항에 따라 신용제공자에게 지급을 거절할 수 있는 금액은 할부금의 지급을 거절한 당시에 소비자가 신용제공자에게 지급하지 아니한 나머지 할부금으로 한다."
- URL: U10 (2018.08.31. briefing)
- Quote: "지금까지 낸 돈 말고 내야 되는 돈에 대해서 지급을 유보 또는 정지해준다는 취지이므로 나머지 금액에 대해서만 항변권이 보장되는 것이고"

**9. A written refusal takes effect on the day it is sent; 서면 includes 전자문서; 내용증명 is proof, not a requirement.**
Status: **stands**
- URL: U1, 제16조제4항
- Quote: "④ 소비자가 제1항에 따른 항변권의 행사를 서면으로 하는 경우 그 효력은 서면을 발송한 날에 발생한다."
- URL: U1, 제6조제1항
- Quote: "서면(「전자문서 및 전자거래 기본법」 제2조제1호에 따른 전자문서를 포함한다. 이하 같다)"
- URL: https://www.korea.kr/multi/visualNewsView.do?newsId=148894499 (공정거래위원회 카드뉴스, 2021.10.19.)
- Quote: "유선·서면 등의 방법으로 카드사에 지급거절 의사를 통보해야 해요!(서면 권장)"
- URL: https://www.consumer.go.kr/user/ftc/consumer/cnsmrBBS/740/selectInfoCDMGCSLCDetail.do?infoId=A1080504&cntntsId=00000347 (소비자24, 생산기관 공정거래위원회 특수거래정책과, 게시일 2024-07-29)
- Quote: "유선, 서면 등의 방법으로 카드사에 지급거절 의사를 통보해야 해요!(서면 권장)"
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=273389&chrClsCd=010202&urlMode=lsInfoP&efYd=20260401&ancYnChk=0 (우편법 시행규칙 제25조제1항제4호가목; the entry page loads this version)
- Quote: "가. 내용증명 : 등기취급을 전제로 우체국창구 또는 정보통신망을 통하여 발송인이 수취인에게 어떤 내용의 문서를 언제 발송하였다는 사실을 우체국이 증명하는 특수취급제도"
- The newer 부령 제155호 (2025. 9. 30.) amends only 제12조 (delivery standards). It does not affect this definition.

**10. The card company must reply in writing within 7 영업일 if it rejects; otherwise the refusal is deemed accepted.**
Status: **stands**
- URL: U1, 제16조제5항·제6항
- Quote (⑤): "제1항에 해당하지 아니하는 경우 소비자의 항변을 수령한 날부터 다음 각 호의 어느 하나에 해당하는 영업일 이내에 서면으로 소비자의 항변을 수용할 수 없다는 의사(意思)와"
- Quote: "1. 할부거래업자는 5영업일" / "2. 신용제공자는 7영업일" / "⑥ 할부거래업자 또는 신용제공자가 제5항에 따른 통지를 하지 아니한 경우에는 소비자의 할부금 지급 거절의사를 수용한 것으로 본다."
- Recomputed: 2026-10-26 is a Monday. Counting 7 weekdays from the next day gives Wed 2026-11-04. From Tue 10-27 it gives Thu 11-05. 관공서의 공휴일에 관한 규정 제2조 (시행 2026. 5. 11. version, https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285779&chrClsCd=010202&urlMode=lsInfoP&efYd=20260511&ancYnChk=0) lists no fixed holiday between 10-26 and 11-06 (추석 2026 is 9월). A government-designated temporary holiday ("11. 그 밖에 정부에서 수시 지정하는 날") could not be ruled out without search. The date stays an example.

**11. No 연체 treatment while the dispute lasts; a fine of up to 500만원 applies, including to the card company.**
Status: **stands**, with one optional addition
- URL: U1, 제16조제7항
- Quote: "분쟁이 해결될 때까지 할부금 지급 거절을 이유로 해당 소비자를 약정한 기일 이내에 채무를 변제하지 아니한 자로 처리하는 등 소비자에게 불이익을 주는 행위를 하여서는 아니 된다."
- URL: U1, 제53조제4항 (current text)
- Quote: "④ 다음 각 호의 어느 하나에 해당하는 자(간접할부계약의 경우 신용제공자를 포함한다)에게는 500만원 이하의 과태료를 부과한다." / "6. 제10조제8항 또는 제16조제7항을 위반하여 소비자에게 불이익을 주는 행위를 한 자"
- Addition: from 2027. 9. 9. the same provision becomes 제53조제5항제6호 (법률 제21906호, pending text: "⑤ 다음 각 호의 어느 하나에 해당하는 자(간접할부계약의 경우 신용제공자를 포함한다)에게는 500만원 이하의 과태료를 부과한다. <개정 2026. 9. 8.>"). Content and amount are unchanged. The source's law-version line says no pending marker touches "the current 제53조제4항". Strictly, the pending rewrite renumbers it. That makes no difference as of today.

**12. Card terms cannot override 제16조; the card company must give the consumer a written notice of the 항변권.**
Status: **stands**
- URL: U1, 제43조; 제6조제3항 and 제6조제1항제13호
- Quote: "제6조부터 제13조까지, 제15조, 제16조, 제22조의2, 제23조부터 제26조까지의 규정을 위반한 약정으로서 소비자에게 불리한 것은 효력이 없다."
- Quote: "③ 신용제공자는 제1항제4호부터 제6호까지, 제9호, 제11호부터 제13호까지의 사항을 적은 서면을 소비자에게 발급하여야 한다." / "13. 제16조에 따른 소비자의 항변권과 행사방법에 관한 사항"

**13. 금융감독원 guidance: 20만 원 and 3개월 or longer; exclusions include 상행위, already fully paid, 리볼빙; its example is a closed Pilates studio.**
Status: **stands**
- URL: https://fss.or.kr/fss/bbs/B0000188/view.do?menuNo=200218&nttId=55842&pageIndex=1. The page dates the release 2022-05-30. The PDF attachment (fileSn=2) reads "보도 2022.5.31.(화) 조간 배포 2022.5.30.(월)".
- Quote: "신용카드 할부거래 시 항변권은 거래금액이 20만원 이상이고 할부기간이 3개월 이상인 거래에 대해 행사할 수 있습니다."
- Quote: "④ 일부결제금액 이월약정(리볼빙) 이용금액 ⑤ 분할납부(할부)기간이 3개월 미만이거나, 분할납부 금액이 20만원 미만인 거래 ⑥ 할부금을 이미 완납한 거래 등"
- Quote: "A씨는 회사 근처 필라테스 학원비 18만원을 3개월 할부로 결제하였는데, 결제 2주 후 갑자기 필라테스 학원이 문을 닫고"
- Quote: "신용카드사에 항변권을 행사하겠다는 의사를 서면 등으로 통지한 뒤 잔여 할부금의 지급을 거부할 수 있습니다." (The extracted PDF text runs some words together. The wording matches.)

**14. 공정위 consumer guidance restates the conditions as 20만 원 이상, 2개월·3회 이상.**
Status: **stands**
- URL: U8 (2021.10.19.)
- Quote: "할부금액(20만 원 이상) X 횟수 조건 충족(2개월·3회 이상) X 법에 정하는* 사유에 해당"
- URL: U9 (2024-07-29)
- Quote: "할부금액(20만원 이상), 횟수 조건 충족(2개월, 3회 이상), 법에 정하는 사유에 해당(할부거래법 제16조 제1항 각호)"

**15. Schedule: 132만 ÷ 6 = 22만 원 per month; which months are paid depends on the 결제일.**
Status: **stands** (arithmetic; the billing facts stay open)
- Recomputed: 1,320,000 ÷ 6 = 220,000. Scenarios: (A) 2 paid = 44만, 4 unpaid = 88만. (B) 1 paid = 22만, 5 unpaid = 110만. (C) 3 paid = 66만, 3 unpaid = 66만. These are consistent with 제16조③ (item 8). 8/5 is a Wednesday and 10/16 a Friday, as the source says.
- No official source gives card billing cycles. That stays "varies".

**16. What the operator owes: [별표 2] 체육시설업 adds a 위약금 of 1/10 when the business is at fault: [132만 − 132만×10/30] + 13.2만 = 101.2만 원; the standard is a recommendation.**
Status: **stands** for the figure and the status of the standard. **The quote needs completing** (see below).
- URL: https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000270136&chrClsCd=010201 ([시행 2025. 12. 18.] [공정거래위원회고시 제2025-14호]). [별표 2] PDF: https://www.law.go.kr/LSW//flDownload.do?flSeq=159470209&bylClsCd=200201. HWPX: flSeq=159469939. Both are listed on that version's body page.
- Quote (2), complete): "2)기기 및 시설의 고장, 이전 · 휴업 · 정원초과 등으로 정상적인 이용이 곤란한 경우" → "ㅇ반환금액(아래 4)의 계약해지 시기별 계약방법에 따른 반환금액 적용) 환급 또는 동급의 타 시설물로 이용 대체"
- Quote (4), 이용개시일 이후, 이용 횟수): "4) 위 1) 2) 이외 사업자의 책임있는 사유로 인한 계약해제" … "ㆍ반환금액=[이용료-(이용료× 이미 이용한 횟수/계약상 이용 횟수)]+위약금" (typeset as a fraction)
- Quote (비고): "* 위약금은 이용료의 1/10에 해당하는 금액을 말함"
- Coverage. [별표 1] (flSeq=159469923): "수영장, 체력단련장, 테니스장, 대중종합체육시설업, 골프연습장, 볼링장, 에어로빅장, 요가원 등". [별표 2]: "헬스․피트니스업, 요가․필라테스업" / "※ 요가․필라테스업은 체육시설업법상 체육시설업에는 포함되지 않음(법령 내용 다음 페이지 참고)".
- Status. URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=283837&chrClsCd=010202&urlMode=lsInfoP&efYd=20260911&ancYnChk=0 (소비자기본법 제16조제3항): "③제2항의 규정에 따른 소비자분쟁해결기준은 분쟁당사자 사이에 분쟁해결방법에 관한 별도의 의사표시가 없는 경우에 한하여 분쟁해결을 위한 합의 또는 권고의 기준이 된다."
- Recomputed: 1,320,000 − 440,000 + 132,000 = 1,012,000. The double-counting scenarios (0 or 13.2만; 22만 or 35.2만; nothing in B) check out.
- Needed change: the source's quote of 분쟁유형 2) stops at "환급". The standard goes on: "또는 동급의 타 시설물로 이용 대체". So for 이전·휴업 cases the business may offer an equivalent facility instead of a refund. A sudden permanent closure is not literally 이전·휴업. It fits 4) ("위 1) 2) 이외 사업자의 책임있는 사유로 인한 계약해제"). That clause has no substitution option and the same formula, so 101.2만 원 stands either way. Suggested key wording: "사업자 책임 해지(4)) 기준: [132만 − 132만×10/30] + 13.2만 = 101.2만 원 (이전·휴업 유형 2)이면 동급 시설 대체도 가능하나, 폐업·연락두절이면 환급이 현실적인 해결)".

**17. The consumer-fault 위약금 (방문판매법 계속거래 고시 19-9호, 요가·필라테스 10%) does not apply because the operator is at fault.**
Status: **stands**, now verified directly (the source had it only through the reference in U3)
- URL: https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000183832&chrClsCd=010201 ([시행 2019. 11. 19.] [공정거래위원회고시 제2019-9호]; the entry page `/행정규칙/계속거래등의해지ㆍ해제에따른위약금및대금의환급에관한산정기준` loads this version and its history shows nothing newer)
- Quote (제4조①): "① 계약이 사업자의 귀책사유 없이 해지 또는 해제된 경우 사업자는 소비자에게 위약금을 청구할 수 있다. 이때 위약금은 별표의 금액을 초과하지 못한다."
- URL: [별표] 위약금, https://www.law.go.kr/LSW/flDownload.do?flSeq=50614915&bylClsCd=200201 (HWP)
- Quote (row): "헬스․ 피트니스업 요가․ 필라테스업" / "총계약대금의 10%"
- Needed change: drop "공정위 고시 19-9호 … was not opened" from the source's could-not-verify list.

**18. The 7-day 청약철회 route is not available here.**
Status: **stands**
- URL: U1, 제8조제1항제1호
- Quote: "1. 제6조제1항에 따른 계약서를 받은 날부터 7일. 다만, 그 계약서를 받은 날보다 재화등의 공급이 늦게 이루어진 경우에는 재화등을 공급받은 날부터 7일"

**19. 1372 소비자상담센터 and 한국소비자원 피해구제.**
Status: **stands**
- URL: https://www.ccn.go.kr/contents/view.ccn?nMenuCode=120 (footer "Copyright © 2016 By Fair Trade Commission All Rights Reserved.")
- Quote: "전국 단일 소비자 상담을 위한 전국 대표번호 채택 ( 전화 : 국번없이 1372 )" / "이용시간 : 평일 09:00 ~ 18:00"
- Quote: "만약 소비자상담센터에서 해결이 되지않는다면 한국소비자원 피해구제담당자에게로 피해구제이관됩니다." This sentence is the alt text of the process diagram image (`/images/new2016/1372_center.gif`), not body text.
- URL: U4, 소비자기본법 제55조제1항
- Quote: "①소비자는 물품등의 사용으로 인한 피해의 구제를 한국소비자원에 신청할 수 있다."

**20. 체육시설법 제29조③: 14-day notice to members before closing (in force for closures from 2025-04-23); probably does not reach a Pilates studio.**
Status: **stands**, with one optional addition
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285605&chrClsCd=010202&urlMode=lsInfoP&efYd=20260729&ancYnChk=0 ([시행 2026. 7. 29.] [법률 제21596호]; the entry page loads this version)
- Quote (제29조③): "③ 체육시설업자는 문화체육관광부령으로 정하는 기간 이상 휴업 또는 폐업하려는 때에는 휴업 또는 폐업 예정일 14일 전까지 그 사실을 다음 각 호의 이용자에게 통지하여야 한다."
- Quote (제40조①): "①다음 각 호의 어느 하나에 해당하는 자에게는 100만원 이하의 과태료를 부과한다." / "5. 제29조제3항에 따른 휴업 또는 폐업 사실을 휴업 또는 폐업 예정일 14일 전까지 같은 항 각 호의 이용자에게 통지하지 아니한 자"
- Quote (부칙 <법률 제20499호, 2024. 10. 22.>): "제2조(체육시설업자의 휴업ㆍ폐업 통지에 관한 적용례) 제29조의 개정규정은 이 법 시행 이후 체육시설업자가 휴업하거나 폐업하는 경우부터 적용한다." The amendment list shows "[시행 2025. 4. 23.] [법률 제20499호, 2024. 10. 22., 일부개정]".
- Quote (제10조①2호): "2. 신고 체육시설업 : 요트장업, 조정장업, 카누장업, 빙상장업, 승마장업, 종합 체육시설업, 수영장업, 체육도장업, 골프 연습장업, 체력단련장업," … "체육교습업, 인공암벽장업". Pilates is not named.
- Addition: the same paragraph has a proviso the source does not quote: "다만, 다음 각 호의 이용자의 연락처를 알 수 없는 경우 등 정당한 사유가 있는 경우에는 통지에 갈음하는 조치를 할 수 있다." This is one more reason not to assert a violation. The pending 법률 제21750호 (시행 2026. 12. 3.) changes only 제8조.

## Facts for the key

- **전제와 그것이 틀린 이유**: **stands**. 제2조제1호나목, 제16조①5호·2호, 제16조②, 시행령 제11조 (20만 원) and 제43조 are all confirmed on the versions in force on 2026-10-25/26. 제16조 is identical in the pending 2027-09-09 text.
- **할부금 22만 원과 시나리오 A/B/C (88만·110만·66만 거절 가능)**: **stands** (arithmetic; 결제일 unknown).
- **거절 가능 범위 = 통지 당시 미납 할부금 (제16조③)**: **stands**.
- **학원 반환 88만 원 / 고시상 101.2만 원; 권고 기준; 별도 약정 우선**: **stands**. Replace the one-line description of the 고시 with the wording suggested in item 16. 2) also allows "동급의 타 시설물로 이용 대체". A permanent closure fits 4), which uses the same formula.
- **이중 청구 주의 (0원 또는 13.2만 원; 22만 원 또는 35.2만 원)**: **stands**.
- **통지 방법 (서면, 발송일 효력, 전자문서 포함, 내용증명은 입증 수단, 공정위는 전화 가능·서면 권장)**: **stands**.
- **7영업일, 미통지 시 수용 간주, 5영업일은 할부거래업자 기한; 예시 10/26(월) → 11/4(수)**: **stands**. 10/26 is a Monday. It is now the current date.
- **분쟁 중 연체 처리 금지, 500만 원 이하 과태료 (제53조④6호)**: **stands**. Optional: "2027. 9. 9.부터는 같은 내용이 제53조⑤6호".
- **덧붙기 쉬운 오답 목록** (10만 원, 무이자 제외, 일시불, 이미 낸 돈 환급, 30일/14일/5영업일, 내용증명 필수, 7일 청약철회, 132만 전액, 위약금 10% 공제): **stands**. The last item is now backed directly by 고시 제2019-9호 제4조① (item 17).
- **1372 (평일 09~18시), 한국소비자원 피해구제 (제55조)**: **stands**.
- **체육시설법 제29조③ (14일 전 통지, 100만 원 이하 과태료, 2025.4.23. 시행), 필라테스는 일반적으로 체육시설업 아님**: **stands**. Optional: add the 정당한 사유 proviso (item 20).
- **경우에 따라 달라지는 것 (1)~(4)**: **stands**.

## Not decided in this pass
- Bills pending in the 국회 and any 입법예고 to amend 할부거래법 제16조 or 시행령 제11조. No open web search was possible (tooling note). Neither would change the law in force today.
- Temporary public holidays designated by the government between 2026-10-26 and 2026-11-06. These affect only the example date in item 10.
- Each card company's 항변권 channel and its 일시불 dispute rules. These are not statutory, and the source also left them open.

---

## Addendum A1 (2026-10-26, after a review of the key): the consumer-fault formula, 분쟁유형 5)

Added by the agent that fixed the key after the review. It is not part of the adversarial check above.

**A1-1. On these facts the consumer-fault refund under [별표 2] 체육시설업 (분쟁유형 5)) is 74.8만 원, not 79.2만 원.**
Status: **refuted/needs change** (the key, the key points and source item 16 gave 79.2만 as the consumer-fault value). Now corrected in all three.
- URL: [별표 2] 품목별 해결기준, 공정거래위원회고시 제2025-14호 (시행 2025. 12. 18.). PDF: https://www.law.go.kr/LSW//flDownload.do?flSeq=159470209&bylClsCd=200201. HWPX: flSeq=159469939. Both are listed on https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000270136&chrClsCd=010201.
- How it was read: from the copies of these two files that law.go.kr served on 2026-10-25 at 12:57:46 GMT (PDF) and 12:58:03 GMT (HWPX), with Content-Disposition "[별표 2] 품목별 해결기준(소비자분쟁해결기준)". These are the same files item 16 used. A fresh fetch on 2026-10-26 was blocked by a tool limit, so the files were not downloaded again. The PDF text and the HWPX text agree.
- Quote (분쟁유형): "5) 소비자의 책임있는 사유로 인한 계약해제"
- Quote (이용개시일 이후, 계약내용이 이용 횟수로 정해진 경우): "ㆍ반환금액=[이용료-(이용료× 이미 이용한 횟수/계약상 이용 횟수)] - 위약금" (typeset as a fraction, as in item 16)
- Quote (비고, also in item 16): "* 위약금은 이용료의 1/10에 해당하는 금액을 말함"
- Arithmetic: 이용료 1,320,000원. Used share 10/30 = 440,000원. 위약금 1/10 = 132,000원. Under 5): 1,320,000 − 440,000 − 132,000 = **748,000원 (74.8만)**. The 고시 제2019-9호 cap (item 17, "총계약대금의 10%") is also 132,000원, so deducting it from the 880,000원 refund gives the same 748,000원. 79.2만 = 880,000 × 0.9 = 792,000 takes 10% of the remaining refund, not 10% of the fee. It matches neither text.
- Effect: the business-at-fault refund of 101.2만 (4)) and the 88만 unused-session figure do not change. Only the trap value moves. The key now names 74.8만 as the consumer-fault wrong value and keeps 79.2만 as a second wrong variant.

**A1-2. Scenario B (billing) and the "usual case" label.**
Status: no new official fact. Item 15 above already says no official source gives card billing cycles. The source called scenario A "the usual case" and paired a September first bill with an October 결제일 of 10/26 or later (scenario B). Neither claim was checked. The reviewer noted, from general knowledge and without a source, that a late-month 결제일 usually bills purchases made up to about mid-month in the same month, which would put an 8/5 purchase in an August bill (scenario C). That was not checked on an official page either. The key, the key points and the source now state B as "지금까지 1회만 결제" with no dates, and the "usual case" / "흔한 경우" labels are gone. The arithmetic (22만 × number of installments; 88만, 110만, 66만 refusable) does not change and still stands.

Files changed with this addendum: keys/ko-card-installment-defense.md (change list items 6 and 7, scenarios A and B, the 79.2만 trap line, the 감점 line), keypoints/ko-card-installment-defense.json (points 3 and 6), sources/ko-card-installment-defense.md (item 15 scenarios, item 16 wrong-values line, the "Facts for the key" scenario lines and wrong-claim line). The request text did not change.

## Addendum A2 (2026-10-26, after a second review of the key): scenario (C) needs the October 결제일 to have passed

Added by the agent that fixed the key after the review. It is not part of the adversarial check above. No new official fact.

**A2-1. "First bill in August" gives 3 paid only once the October 결제일 has passed.**
Status: **needs change** in the wording of (C); the arithmetic in item 15 stands. Now corrected in the key and key point 3.
- Item 15 checked only "3 paid = 66만, 3 unpaid = 66만". It did not check that a first bill in August means 3 are already paid. With six monthly bills from August (8월, 9월, 10월, 11월, 12월, 1월), 3 are paid only after the October 결제일. Today is 2026-10-26 (Monday, item 10 / Facts for the key), so a card billed from August whose October 결제일 is still ahead has paid 2.
- Recomputed: 8월부터 청구, 10월 결제일 전: 2 paid = 440,000원; 4 unpaid = 880,000원 (10월~1월 bills). Under 제16조③ (item 8, stands) all four can be refused if the notice goes out before the October 결제일. Double-recovery for this case: 440,000 − 440,000 = 0원, or 132,000원 with the 위약금, the same as scenario (A) (item 16, stands).
- Which 결제일 the user's card has stays open (item 15: no official source gives billing cycles). The key does not say which case is common.

Files changed with this addendum: keys/ko-card-installment-defense.md (scenario (C) now reads "첫 청구가 8월이고 10월 결제일도 지났다면", with the 44만 paid / 88만 refusable sub-case and a no-mark-down note; the double-recovery line adds that sub-case), keypoints/ko-card-installment-defense.json (point 3, same change). The request text did not change. sources/ko-card-installment-defense.md item 15 (C) and its Korean summary line still state (C) without the October condition; they were outside this fix.
