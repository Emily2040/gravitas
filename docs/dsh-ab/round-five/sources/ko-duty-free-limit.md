# ko-duty-free-limit: fact check (checked 2026-10-25)

Request (Korean, prompts/ko-duty-free-limit.txt): 혼자 오사카 3박 4일, 2026년 11월 12일(목) 출국, 11월 15일(일) 입국. 출국 때 인천공항 면세점에서 엄마 선물용 화장품 150달러. 오사카에서 본인 가방 약 620달러, 위스키 700ml × 2병(합계 180달러), 향수 50ml(90달러). 여행 카페 말("입국 면세한도는 1인 600달러이고 술·향수도 다 그 안에 포함")을 믿고, 한도를 넘는다고 보고 초과분을 자진신고해 세금을 내려 함. 요청: 세금이 대략 얼마인지, 쇼핑 예산표, 인천공항 입국 시 신고 방법(신고서, 통로).

Method. All sources were opened on 2026-10-25. The 관세청 page was read in the built-in browser (full page text) and also with WebFetch. The 관세청 guide PDF linked from that page was fetched and its text extracted with pypdf. law.go.kr pages render with JavaScript, so statute and 고시 text was pulled from the site's own body endpoints (`/LSW/lsInfoR.do`, `/LSW/admRulInfoR.do`) inside the built-in browser. For each statute I took the version that the law.go.kr entry page (`/법령/<name>`, `/행정규칙/<name>`) currently loads, and I searched the body for `[시행일: …]` markers of pending amendments. Quotes are verbatim, two lines at most. "Source date" is the date of the document itself.

Versions used (all in force on 2026-10-25 and on the return date 2026-11-15):
- 관세법 시행규칙 [시행 2026. 7. 31.] [재정경제부령 제42호, 2026. 7. 31., 일부개정]. The only pending marker is "[시행일: 2027. 1. 1.]" on 별지 제1호서식 (납세증명서), which is unrelated.
- 관세법 [시행 2026. 10. 2.] [법률 제21490호, 2026. 3. 24., 타법개정]. No pending markers.
- 관세법 시행령 [시행 2026. 7. 1.] [대통령령 제36140호, 2026. 2. 27., 일부개정]; 별표 2 header "<개정 2023. 2. 28.>"
- 여행자 및 승무원 휴대품 통관에 관한 고시 [시행 2026. 4. 1.] [관세청고시 제2026-16호, 2026. 4. 1., 일부개정]

URLs:
- U1 관세청, 여행자 휴대품 통관: https://www.customs.go.kr/kcs/cm/cntnts/cntntsView.do?mi=2837&cntntsId=829 (the page shows no date; read 2026-10-25)
- U2 관세청, 「알아두면 유익한 여행자 휴대품 통관 길라잡이」 PDF, the "여행자 휴대품통관 길라잡이 다운로드" button on U1: https://www.customs.go.kr/common/nttFileDownload.do?fileKey=419b5b042b580dc7dd26f78b2b307b40 (26 pages, no edition date printed; PDF CreationDate 2025-03-21)
- U3 관세법 시행규칙: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=288525&chrClsCd=010202&urlMode=lsInfoP&efYd=20260731&ancYnChk=0 (entry page https://www.law.go.kr/법령/관세법시행규칙 resolves to lsiSeq=288525)
- U4 관세법: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=290673&chrClsCd=010202&urlMode=lsInfoP&efYd=20261002&ancYnChk=0
- U5 관세법 시행령: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=283621&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0
- U6 관세법 시행령 [별표 2] 간이세율 PDF: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=164022847&bylClsCd=110201 (header "<개정 2023. 2. 28.>"; PDF created 2026-05-06)
- U7 여행자 및 승무원 휴대품 통관에 관한 고시: https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000276768&chrClsCd=010201 (entry page https://www.law.go.kr/행정규칙/여행자및승무원휴대품통관에관한고시)
- Secondary sources, used only to date the old figures: S1 이투데이 2022-08-05 https://www.etoday.co.kr/news/view/2160787 ; S2 뉴스서울 2024-05-08 (quoting a 관세청 release) https://newsseoul.co.kr/news/view/1065580819228468 ; S3 SBS Biz 2025-02-26 https://biz.sbs.co.kr/amp/article/20000220060

---

## Item checks

### 1. The basic allowance (기본면세범위) is US$800 per person, not US$600
- Verdict: **refuted (the premise)**. The basic allowance is US$800 of total 과세가격.
- URL: U3, 제48조제2항
- Quote: "각 물품(제1항제1호에 따른 물품으로서 국내에서 반출된 물품과 제1항제3호에 따른 물품은 제외한다)의 과세가격 합계 기준으로 미화 800달러 이하(이하 이 항 및 제3항에서 “기본면세범위”라 한다)로 하고"
- URL: U1
- Quote: "여행자 휴대품으로서 각 물품의 과세가격 합계 기준으로 미화 800달러 이하(농축수산물 품목당 5kg, 총량 40kg 이내, 전체 해외취득가격 10만원 이내 포함)"
- URL: U7, 제18조제1항 (same figure): "각 물품의 과세가격 합계 기준으로 미화 800달러 이하(이하 "기본면세범위"라 한다)로 한다."

### 2. US$600 is the figure from before 2022-09-06
- Verdict: **confirmed**. The change date comes from the primary 부칙. The old value of 600 comes from a secondary source (the earlier statute text was not opened in this pass).
- URL: U3, 부칙 <기획재정부령 제933호, 2022. 9. 6.>; 제48조제2항 amendment marker "2022. 9. 6."
- Quote: "이 규칙은 2022년 9월 6일부터 시행한다." / "제48조제2항 및 제3항의 개정규정은 이 규칙 시행 이후 여행자가 수입하는 휴대품 및 별송품부터 적용한다."
- S1 (2022-08-05): "우선, 여행자 휴대품의 기본 면세 범위를 현행 600달러에서 800달러로 인상한다." It gives the old alcohol rule as "술은 1병(1ℓ·400달러 이하)".

### 3. Alcohol, tobacco and perfume are outside the US$800 basic allowance
- Verdict: **refuted (the premise "술·향수도 다 그 안에 포함")**. They have separate allowances (별도면세범위) "기본면세범위와 관계없이".
- URL: U3, 제48조제3항
- Quote: "제2항에도 불구하고 술ㆍ담배ㆍ향수에 대해서는 기본면세범위와 관계없이 다음 표(이하 이 항에서 “별도면세범위”라 한다)에 따라 관세를 면제하되,"
- URL: U7, 제18조제3항: "다음 각 호의 어느 하나에 해당하는 물품은 기본면세범위를 적용하지 않는다." followed by "1. 술", "2. 담배", "3. 향수"
- URL: U2 p.14 (주류) and p.4 (향수): "주류는 여행자 휴대품 기본면세범위(US$800)에서 제외되어 별도로 면세처리됩니다." / "향수는 여행자 휴대품 기본면세범위(US$800)에서 제외되어 별도로 면세처리됩니다."
- URL: U1: "위항과 별도로 주류(전체 용량이 2L이하이고 총 가격이 미화 400달러 이하), 필터담배 200개비, 전자담배 니코틴용액20ml(니코틴함량 1%미만), 향수 100ml"

### 4. Alcohol allowance: 2 L in total and US$400 in total, with no bottle count. The whisky is duty-free
- Verdict: **confirmed**. 700 ml × 2 = 1.4 L ≤ 2 L, and US$180 ≤ US$400, so the whisky is exempt.
- URL: U3, 제48조제3항 표 (the table is an image; its alt text reads)
- Quote: "술 용량은 2리터(L) 이하, 가격은 미화 400달러 이하로 한다."
- URL: U7, 제19조제1항제2호가목: "술: 전체 용량 2리터(ℓ) 이하(총 가격이 미화 400달러 이하의 것으로 한정한다)."
- URL: U2 p.14: "합계 용량2ℓ 이하,합계 금액 미화 400달러 이하인 주류(병수 무관) :면세"
- Old values that answers may repeat: "2병" (2022-09-06 to 2025-03-21) and "1병, 1L" (before 2022-09-06). The current 제48조제3항 was last amended on 2025-03-21; 부칙 <기획재정부령 제1110호, 2025. 3. 21.>: "이 규칙은 공포한 날부터 시행한다." / "제48조제3항의 개정규정은 이 규칙 시행 이후 여행자가 수입하는 휴대품 또는 별송품부터 적용한다." S3 (2025-02-26) gives the content: "정부가 해외 여행객이 면세로 구매할 수 있는 주류의 병 수 제한을 폐지합니다." So "2병까지만 면세" is **wrong now**, although it does not change this case, which has exactly 2 bottles.
- Excess rule (only relevant if over): bottles beyond the limit are taxed on their whole price, not on the part above US$400 or 2 L. U3 제48조제3항 후단: "이 경우 해당 물품이 다음 표의 면세한도를 초과하여 관세를 부과하는 경우에는 해당 물품의 가격을 과세가격으로 한다." U7 제19조제1항제2호가목 단서: "면세범위 내의 술(병 기준)은 면세할 수 있으며 그 외 면세범위를 초과하는 구간에 있는 술은 전체 취득가격에 대하여 과세한다."
- Side figure (U2 p.14): whisky's combined final rate when taxed is "브랜디·보드카·위스키 156%".

### 5. Perfume allowance: 100 ml, no price limit, no bottle count. The perfume is duty-free
- Verdict: **confirmed**. 50 ml ≤ 100 ml. The US$90 price does not matter.
- URL: U3, 제48조제3항 표 (alt text): "향수 100밀리리터"
- URL: U2 p.4: "향수의 여행자 휴대품 면세범위는 100㎖ 이하(병수 제한 없음)"; p.3 table: "향수 100㎖ §용량제한만 있음(수량무관)"
- URL: U7, 제19조제1항제2호다목: "향수: 100밀리리터(㎖) 또는 이에 준하는 부피 또는 중량 이내의 것(예: 100g, 3.4oz 등)"
- Old value: **60 ml**, before 2024-01-01. Primary: 부칙 <기획재정부령 제1033호, 2023. 12. 29.>: "이 규칙은 2024년 1월 1일부터 시행한다." / "제48조제3항의 개정규정은 이 규칙 시행 이후 여행자가 수입하는 휴대품 및 별송품부터 적용한다." Content from S2 (2024-05-08): "’24.1.1부터 향수의 면세 한도를 60ml에서 100ml로 상향했다." "향수 60ml" is **wrong now**.

### 6. Tobacco (side claim)
- Verdict: **confirmed**. 궐련 200개비, 엽궐련 50개비, 궐련형 전자담배 200개비, 니코틴용액 20 mL, 기타유형 110 g, 그 밖의 담배 250 g. Only one kind if more than one kind is brought.
- URL: U3, 제48조제3항 표 (alt text): "담배 궐련 200개비 둘 이상의 담배 종류를 반입하는 경우에는 한 종류로 한정한다."
- URL: U1: "필터담배 200개비, 전자담배 니코틴용액20ml(니코틴함량 1%미만)"

### 7. Under-19 rule (side claim)
- Verdict: **confirmed**. No alcohol or tobacco allowance under 19, counted by birth year: anyone who has reached 1 January of the year they turn 19 counts as 19. It does not apply to perfume.
- URL: U3, 제48조제3항: "19세 미만인 사람(19세가 되는 해의 1월 1일을 맞이한 사람은 제외한다)이 반입하는 술ㆍ담배에 대해서는 관세를 면제하지 않고"
- URL: U1: "만 19세 미만(출생년도 기준) 미성년자는 주류, 담배 면세범위 없음"

### 8. The outbound duty-free purchase (인천공항 출국장 면세점, 150달러) counts toward the US$800 when brought back
- Verdict: **confirmed, with the legal basis corrected**. The candidate draft put this on the deduction clause of 시행규칙 제48조제2항. That clause covers goods bought under **법 제196조제1항제1호 단서** (bought at a duty-free shop and handed over at the arrival 인도장) and **같은 조 제2항** (입국장 면세점), not goods bought on departure and taken abroad. The outbound purchase counts because the 고시 defines duty-free purchases brought back as "해외에서 취득한 물품", and the 관세청 guide says so expressly. The arithmetic is unchanged.
- URL: U7, 제2조제17호
- Quote: "“해외에서 취득한 물품”이란 해외에서 구매하거나 선물 등 무상으로 취득한 물품 또는 「관세법」(이하 "법"이라 한다) 제196조제1항 및 제2항에 따른 보세판매장에서 구매하여 반입하는 물품을 말한다."
- URL: U7, 제6조제1항제1호 (신고대상): "해외에서 취득한 물품으로서 전체 취득가격 합계액이 미화 800달러를 초과하는 물품."
- URL: U2 p.6
- Quote: "출국 시 국내면세점에서 구매한 후 우리나라로 다시 가지고 오는 물품, 해외에서 취득(구매·선물 등)한 물품, 입국 시 면세판매장에서 구매한 물품의 전체 가격 합계액이 US$800을 초과하는 것은 자진신고 대상"
- URL: U2 p.3 table: "해외 취득물품 합계액 (국내면세점 구매물품 포함) US$800" and "§자가사용, 선물용 등에 한함". A gift for the mother is within scope.
- URL: U4, 제196조 (what the deduction clause refers to): ①1 "해당 물품을 외국으로 반출할 것. 다만, 외국으로 반출하지 아니하더라도 대통령령으로 정하는 바에 따라 외국에서 국내로 입국하는 자에게 물품을 인도하는 경우에는 해당 물품을 판매할 수 있다." / ② "공항 및 항만 등의 입국경로에 설치된 보세판매장에서는 외국에서 국내로 입국하는 자에게 물품을 판매할 수 있다."
- U1 (the 관세청 summary page) does not mention duty-free purchases at all.

### 9. Arithmetic: 150 + 620 = 770 ≤ 800. No duty is due
- Verdict: **confirmed** (derived from items 1, 3, 4, 5 and 8).
- Counted in the basic allowance: 화장품 US$150 (출국장 면세점, brought back) + 가방 US$620 = **US$770 ≤ US$800**. Margin: **US$30**.
- Outside it: 위스키 1.4 L / US$180, within 2 L / US$400. 향수 50 ml, within 100 ml.
- Break-even for the bag: 800 − 150 = **US$650**. "약 620달러" is an estimate. If the bag's actual 과세가격 (the amount paid, converted at the 관세청 과세환율 for the week before entry; items 14 and 15) comes to more than US$650, the basic allowance is exceeded and the whole excess above US$800 has to be declared.
- Wrong totals an answer may produce:
  - Premise as stated (US$600, all items inside): 150 + 620 + 180 + 90 = 1,040, so 440 "over". **Wrong.**
  - US$800, but whisky and perfume counted inside: 1,040 − 800 = 240 "over". **Wrong.**
  - US$800, perfume counted inside, whisky separate: 150 + 620 + 90 = 860, so 60 "over". **Wrong.**
  - US$800 with the outbound cosmetics left out: 620, "US$180 left". The conclusion (no tax) is right, but the margin is overstated six-fold. That is a **wrong key point** on the arithmetic.

### 10. With nothing to declare, the declaration form is skipped and the traveller uses the 신고없음 (면세) channel
- Verdict: **confirmed**. Nothing here exceeds an allowance, so this traveller has nothing to declare. The plan to "자진신고하고 세금 내기" is unnecessary. The traveller can still be selected for inspection, so receipts should be kept.
- URL: U1
- Quote: "신고물품 없는 여행자 : 신고서 제출 생략, 신고없음 통로 이용, 경우에 따라 세관검사를 받을 수 있습니다."
- URL: U7, 제5조제2항제2호: "여행자와 승무원이 제6조제1항 및 제64조제1항에 따른 신고대상물품을 휴대하지 않은 경우에는 신고서 작성ㆍ제출을 생략할 수 있다." 제5조제2항 단서: "다만, 세관장이 휴대품 감시ㆍ단속을 위하여 신고서 제출을 요구하는 경우에는 이를 제출해야 한다."
- URL: U7, 제7조제1항제1호 (the 고시 calls it 면세통로): "면세통로: 제6조제1항 및 제64조제1항에 따른 신고대상물품을 휴대하지 않은 여행자ㆍ승무원"
- URL: U2 p.1: "여행자가 신고대상물품을 휴대하지 않은 경우, 휴대품 신고서 제출을 생략할 수 있습니다."
- Only items over their allowance must be declared. Alcohol, tobacco and perfume within their allowance need no declaration (U7 제6조제1항제2호: "1명당 면세기준을 초과하는 술, 담배, 향수").

### 11. 자진신고 reduction: 30% of the duty, capped at 20만원
- Verdict: **confirmed**. The 20만원 cap is not on U1, but it is in the statute and in U2. For goods taxed at the 간이세율, the 30% applies to the whole 간이세율 tax.
- URL: U4, 제96조제2항
- Quote: "20만원을 넘지 아니하는 범위에서 해당 물품에 부과될 관세(제81조에 따라 간이세율을 적용하는 물품의 경우에는 간이세율을 적용하여 산출된 세액을 말한다)의 100분의 30에 상당하는 금액을 경감할 수 있다."
- URL: U1: "자진신고 시 : 관세의 30%경감"
- URL: U2 p.9: "20만원을 넘지 아니하는 범위에서 해당 물품에 부과될 관세의 100분의 30에 상당하는 금액을 경감할 수 있습니다."
- "15만원 한도" or "no cap" is **wrong now**. When the cap changed was not checked.

### 12. Penalty for not declaring: 40% of the tax, 60% for a repeat within 2 years
- Verdict: **confirmed**. The penalty is on 납부할 세액, which includes 내국세. Repeat means two or more such penalties within 2 years counted back from the entry date.
- URL: U4, 제241조제5항
- Quote: "납부할 세액(관세 및 내국세를 포함한다)의 100분의 20(제1호의 경우에는 100분의 40으로 하되, 반복적으로 자진신고를 하지 아니하는 경우 등 대통령령으로 정하는 사유에 해당하는 경우에는 100분의 60)"
- URL: U5, 제247조제4항: "입국일을 기준으로 소급하여 2년 이내에 2회 이상 법 제241조제5항제1호의 경우에 해당하는 사유로 가산세를 징수한 경우를 말한다."
- URL: U1: "미신고 적발 시 : 가산세 부과(납부할 세액의 40%, 2년내 2회 이상 60%)"
- Not relevant here, since nothing is due, but answers will mention it.

### 13. How tax is computed if the allowance is exceeded (not the case here)
- Verdict: **confirmed**. Only the amount above US$800 is taxed (not the whole total). It is converted to won, and the item's rate applies, normally the 간이세율. The general 간이세율 is **15%**. Separately, alcohol bottles over their allowance are taxed on their full price (item 4).
- URL: U7, 제25조
- Quote: "여행자 휴대품의 세액은 신고한 금액을 미화로 환산한 금액에서 미화 800달러를 공제한 후, 나머지 금액을 원화로 환산하고 해당 물품의 세율을 적용하여 계산한다."
- URL: U7, 제18조제2항 (deduction order): "기본면세범위에서 법 제196조제1항제1호 단서에 따른 입국장인도장에서 인도받거나 같은 조 제2항에 따른 보세판매장에서 구매한 내국물품, 고세율품목 순서로 공제한다."
- URL: U7, 제26조: "영 제96조 별표 2에 따라 간이세율을 적용할 수 있다."
- URL: U6, 별표 2 제4호: "4. 제1호부터 제3호까지에 해당하지 않는 물품. 다만, 고급모피와 그 제품, 고급융단, 고급가구, 승용자동차, 수렵용 총포류, 주류 및 담배는 제외한다." Rate: "15". Other rows: 모피의류 19; 가죽제 의류·섬유제품·신발류 18; 녹용 21; 개별소비세 과세 고급 시계·고급 가방 "288,450원 + 1,923,000 원을 초과하는 금액의 45".
- Illustration only (not this case): if the bag cost US$700, the total would be 850 and the excess US$50. At a hypothetical 과세환율 of 1,400원 per dollar: 50 × 1,400 = 70,000원 × 15% = 10,500원. After the 자진신고 30% reduction: 7,350원. The real 과세환율 for the week of entry was not available on 2026-10-25.
- Whether a ~US$620 bag falls under the 개별소비세 "고급 가방" row was **not verified** (that depends on the 개별소비세법 기준가격, which was not opened). It matters only if the allowance is exceeded.

### 14. 과세환율 (side claim)
- Verdict: **confirmed (rule); varies (figure)**. Foreign-currency prices are converted at the 관세청 rate set from the average of the previous week's 기준환율 or 재정환율. Yen prices count at their dollar equivalent.
- URL: U4, 제18조: "제17조에 따른 날 ... 이 속하는 주의 전주(前週)의 기준환율 또는 재정환율을 평균하여 관세청장이 그 율을 정한다."
- URL: U7, 제2조제16호: "미화 또는 US$ 표시 금액은 그 상당액의 다른 나라 통화표시 금액과 같다."
- No KRW figure for November 2026 can be keyed. A budget table in won must label its exchange rate as an assumption.

### 15. 과세가격 = the amount actually paid; a local tax refund lowers it (side claim)
- Verdict: **confirmed**. This matters for a bag bought tax-free (免税) in Japan. If the receipt shows the consumption tax refunded or exempted, the lower price counts.
- URL: U2 p.16: "여행자 휴대품의 과세가격은 ‘신고인의 제출 서류에 명시된 신고인의 결제금액"
- URL: U2 p.17: "환급받은 세금을 공제한 금액을 구입가격으로 보아 과세할 수 있습니다."
- URL: U7, 제23조: "자진 신고한 여행자와 승무원이 제시한 영수증 가격은 특별한 사유가 없으면 구입가격으로 인정하며"

### 16. Allowances are per person, with no pooling (side claim; the user travels alone)
- Verdict: **confirmed**. Family members travelling together cannot combine allowances for a single item over US$800. A representative may file one declaration for the family.
- URL: U7, 제22조제3항: "2명 이상의 동반가족이 미화 800달러를 초과하는 물품 1개 또는 1세트를 휴대반입한 경우 1명이 반입한 것으로 보아 제1항을 준용한다."
- URL: U2 p.1: "동반가족인 경우 대표자 1인이 일괄신고 할 수 있습니다."

### 17. 농림축수산물 (side claim)
- Verdict: **confirmed**. These fall inside the US$800 and are further limited to 총 40 kg, 전체 해외취득가격 10만원, and 품목당 limits (e.g. 5 kg). Quarantine items must pass inspection.
- URL: U1: "(농축수산물 품목당 5kg, 총량 40kg 이내, 전체 해외취득가격 10만원 이내 포함)"
- URL: U7, 제20조제1항: "총량 40kg 이내, 전체 해외취득가격 10만원 이내로 한다."

### 18. How to declare when there is something to declare (side claim)
- Verdict: **confirmed**. Paper 여행자 휴대품 신고서, or electronic filing on the web or in the 「여행자 세관신고」 app. The app produces a QR code that is scanned at the 자동 심사대 in the arrivals hall. A mobile filer gets the 고지서 and can pay on the phone. 내국인 자진신고자 can pay afterwards (사후납부, within 15 days). These steps apply only if something is over the limit.
- URL: U1: "신고물품이 있는 여행자 : 신고서 제출(종이,모바일), 모바일로 자진신고 시 모바일로 고지서 발급 및 납부 가능"
- URL: U2 p.2: "입국 여행자가 휴대품 전자신고 전용 앱을 통해 휴대품을 신고하면 QR코드가 생성되고, 해당 QR코드를 공항 입국장에 설치된 ‘자동 심사대’에 인식하면 세관 신고가 완료됩니다."
- URL: U2 p.18: "사후납부 : 내국인 자진신고자 대상(체납자, 우범여행자 등 제외)", with a 15일 이내 payment window.
- Form legal basis: U3 제49조의2: "항공기를 통하여 입국하는 경우: 별지 제42호서식의 여행자 휴대품 신고서"

### 19. No purchase limit on outbound duty-free shopping (side claim)
- Verdict: **partly verified**. The current 시행규칙 sets a sales limit only for 입국장 면세점 and 입국장 인도장 (US$800 plus the separate alcohol, tobacco and perfume allowances). It sets none for departure purchases. An old "출국 면세점 구매한도 5,000달러" rule existed. Its abolition (reported as March 2022) was not checked on a primary text. Either way, the outbound limit is not the same thing as the entry allowance.
- URL: U3, 제69조의4제1항: "미화 800달러의 한도에서 판매해야 하며, 술ㆍ담배ㆍ향수는 제48조제3항에 따른 별도면세범위에서 판매할 수 있다." This covers only 법 제196조제2항 shops (입국장).

### Could not verify
- Whether opened or partly used duty-free cosmetics could be treated as 신변용품 (U7 제19조제1항제1호, "국내에서 반출된 제4조제2항제3호에 따른 신변용품") rather than counted. The 관세청 guide counts duty-free purchases brought back without exception. In this request the cosmetics are a gift, so they come back unused and count.
- The 과세환율 for the week of 2026-11-15 and the bag's exact price. These decide whether US$620 stays under US$650.
- Whether a ~US$620 bag is 개별소비세 "고급 가방". It matters only if over the allowance.
- The date the 자진신고 cap moved to 20만원, and the primary text of the pre-2022 rules (600달러, 술 1병·1L). The current values are verified; the old ones rest on S1.
- U1 shows no page date.

---

## Facts for the key

**전제와 그것이 틀린 이유**
- 여행 카페 말은 두 군데가 틀렸습니다. (1) 기본면세범위는 1인당 **미화 800달러**입니다(관세법 시행규칙 제48조제2항, 관세청 안내). 600달러는 2022년 9월 6일 개정 전 기준입니다. (2) **술·담배·향수는 800달러에 포함되지 않습니다.** 기본면세범위와 관계없이 별도로 면세됩니다(같은 조 제3항, 관세청 고시 제18조제3항). 술은 합계 2L 이하이면서 총 400달러 이하, 향수는 100ml까지입니다.
- 따라서 이번 쇼핑은 **한도 안이고, 낼 세금은 0원**입니다. 자진신고할 물품도 없습니다.

**정확한 계산** (출국 2026.11.12., 입국 2026.11.15.)
- 기본면세범위(800달러)에 들어가는 것: 출국장 면세점 화장품 150달러(가지고 다시 들어오므로 포함. 관세청 길라잡이 "국내면세점 구매물품 포함", 고시 제2조제17호) + 가방 약 620달러 = **770달러 ≤ 800달러**. 여유는 **30달러뿐**입니다.
- 별도면세범위: 위스키 700ml × 2 = 1.4L, 180달러이므로 2L·400달러 안에서 면세(병 수 제한 없음). 향수 50ml는 100ml 안에서 면세(가격 무관).
- 가방은 **650달러**(= 800 − 150)를 넘으면 한도를 넘습니다. "약 620달러"는 추정이므로 실제 결제금액(일본 면세로 소비세를 빼고 샀다면 그 금액)과 입국 전주 기준 관세청 과세환율에 따라 달라질 수 있습니다. 영수증을 보관하고, 실제로 650달러를 넘으면 그때 자진신고하라고 안내하는 것이 맞습니다.
- 출국장 면세점 화장품을 빼고 계산하면(620달러, "180달러 여유") 결론은 같지만 여유를 크게 잘못 말하게 됩니다. 술·향수를 800달러에 넣어 1,040달러로 보거나 240달러·60달러 "초과"라고 하면 틀립니다.

**신고 방법**
- 신고대상 물품이 없으므로 **휴대품 신고서 제출을 생략하고 '신고없음'(면세) 통로**로 나가면 됩니다(관세청 안내, 고시 제5조제2항제2호·제7조제1항제1호). 세관 검사 대상으로 선별될 수는 있으므로 영수증을 챙깁니다.
- (참고: 한도를 넘는 경우) 종이 신고서나 「여행자 세관신고」 앱·웹으로 신고합니다. 앱은 QR코드를 입국장 자동 심사대에 인식시키는 방식이고, 모바일로 고지서를 받아 납부할 수 있습니다. 내국인 자진신고자는 15일 이내 사후납부도 가능합니다.

**답변에 덧붙기 쉬운 주장과 올바른 값**
- 자진신고 감면: 관세의 **30%, 20만원 한도**입니다(관세법 제96조제2항). 간이세율 물품은 간이세율로 계산한 세액 전체가 감면 대상입니다. "15만원 한도"나 "한도 없음"은 틀립니다.
- 미신고 가산세: 납부할 세액(관세와 내국세 포함)의 **40%**, 입국일 기준 2년 내 2회 이상이면 **60%**입니다(관세법 제241조제5항, 시행령 제247조제4항).
- 세금 계산(초과 시): 합계에서 **800달러를 뺀 나머지만** 원화로 바꿔 세율을 적용합니다(고시 제25조). 일반 물품의 간이세율은 **15%**입니다(시행령 별표 2). 한도를 넘는 술은 넘는 병의 전체 가격에 과세하며, 위스키 최종세율은 156%입니다(관세청 길라잡이). "전체 금액에 과세"나 "간이세율 20%"는 현행과 다릅니다.
- 옛 기준: 향수 **60ml**(2024.1.1. 전), 술 **2병**(2025.3.21. 전), 술 **1병·1L**(2022.9.6. 전)은 모두 현행이 아닙니다.
- 담배: 궐련 200개비(엽궐련 50개비, 니코틴용액 20mL 등), 한 종류만 해당합니다. 만 19세가 되는 해의 1월 1일 전인 사람은 술·담배 면세가 없습니다.
- 면세범위는 1인 기준이며 가족끼리 합산할 수 없습니다(고시 제22조제3항). 이번 요청은 혼자 하는 여행입니다.
- 농축수산물은 800달러 안에서 총 40kg, 해외취득가격 10만원, 품목당 한도가 따로 있습니다.

**경우에 따라 달라지는 것**
- 가방의 실제 가격과 과세환율: 650달러를 넘는지가 여기서 정해집니다.
- 일본 면세(소비세 면제·환급) 여부: 영수증상 결제금액이 과세가격이 됩니다.
- 원화 예산표의 환율은 가정값으로 밝혀야 합니다. 2026년 11월 과세환율은 확인할 수 없습니다.
- 화장품을 현지에서 쓰거나 두고 오면 반입하지 않는 셈이 되어 계산에서 빠집니다. 이번 요청에서는 엄마 선물이라 가지고 들어오므로 포함합니다.
