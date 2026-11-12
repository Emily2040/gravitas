# Adversarial check: ko-duty-free-limit.md, "Facts for the key"

Checked 2026-10-25 by an agent that did not write the source file. Some fetches ran just after local midnight, on 2026-10-26. On disk I read only `prompts/ko-duty-free-limit.txt` and `sources/ko-duty-free-limit.md`, plus round four's `en-fsa-rollover.check.md` for the format. I opened every URL below myself, in one of these ways:
- The 관세청 page: WebFetch and curl.
- law.go.kr statutes and the 고시: I loaded each entry page (`/법령/<name>`, `/행정규칙/<name>`) in the built-in browser, then read the version it loads through the site's body endpoints (`/LSW/lsInfoR.do`, `/LSW/admRulInfoR.do`).
- The amendment-text lists (`/LSW/lsRvsDocListP.do`): curl.
- The two PDFs: downloaded from the given URLs, with text extracted by pypdf.

Quotes are verbatim, two lines at most. "p." means the page number printed in the PDF. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search. I found no change to the Korean rules that would alter a fact or make the premise true:
- **Entry pages.** Each one still loads the version the source names:
  - 관세법 시행규칙 [시행 2026. 7. 31.] [재정경제부령 제42호] (lsiSeq=288525)
  - 관세법 [시행 2026. 10. 2.] [법률 제21490호] (lsiSeq=290673)
  - 관세법 시행령 [시행 2026. 7. 1.] [대통령령 제36140호] (lsiSeq=283621)
  - 여행자 및 승무원 휴대품 통관에 관한 고시 [시행 2026. 4. 1.] [관세청고시 제2026-16호] (admRulSeq=2100000276768)
- **시행규칙.** The amendment-text list has nothing newer than 제42호, which only replaces 별표 1의2. In 2026 only one ordinance touched 제48조: 재정경제부령 제12호 (2026. 3. 20., 시행 2026. 4. 1.).
  - It added 제48조제1항제4호, "영 제213조제3항 단서에 따라 회수되지 않은 물품일 것". That clause covers departure duty-free goods that could not be taken abroad, for example because a flight was cancelled. It left 제2항 and 제3항 unchanged.
  - Its 부칙 is the source of the one pending date: "별지 제1호서식의 개정규정: 2027년 1월 1일".
- **관세법.** The newest entry is 법률 제21858호 (2026. 8. 11., in force the same day). It only amends 제255조의5 (수출입안전관리우수업체 공인 취소) and 제328조. 제21490호 (공소청법, 타법개정) only changes 제116조의4. 제21208호 (시행 2026. 1. 1.) adds equipment and body searches of travellers (제265조) and does not touch 제96조 or 제241조제5항.
- **News.** 한국세정신문, 2026-06-04 (https://www.taxtimes.co.kr/news/article.html?no=275396): "면세업계가 여행객 면세 한도 확대, 특허수수료 인하, 규제 완화 등을 정부에 건의했다." The same article gives the current rule: "기본면세(800달러)에 품목별 별도면세(술 400달러·2L, 담배 200개비, 향수100ml)". The government only said it would review the requests. I found no 2026 announcement that raises US$800 or changes the separate allowances.

One newer rule does change a fact. **Japan's tax-free system switches to a refund method for purchases made from 2026-11-01.** All of this trip's Osaka shopping (Nov 12 to 15) falls under it. See F15.

Tooling note: the shared WebSearch budget ran out partway through, and WebFetch hit a session limit near the end. The last fetches were curl requests to known primary URLs. As a result, I could not open the 재정경제부 text of the 2026 세법개정안 to rule out a proposed allowance change. Even if it holds one, a 관세법 change cannot take effect before the National Assembly passes it. An allowance change made by ministerial ordinance (시행규칙) can take effect on promulgation, as the 2025-03-21 change did. **Re-check 시행규칙 제48조 on grading day.**

## Versions and sources

**F0. Versions used, U1–U7 and S1–S3 (source lines 7–21).**
Status: **stands**
- All four law versions match what the entry pages load (see above). The 시행규칙's only pending marker is confirmed. U6 (별표 2 PDF, flSeq=164022847) is the PDF linked from the current 시행령. Its header reads "■ 관세법 시행령 [별표 2] <개정 2023. 2. 28.>", and its PDF CreationDate is 2026-05-06.
- U2 is still the "여행자 휴대품통관 길라잡이 PDF파일 다운로드" link on U1 (fileKey=419b5b042b580dc7dd26f78b2b307b40). It has 26 pages and a PDF CreationDate of 2025-03-21. The server's file name confirms the edition: `Content-Disposition: attachment; filename="250321_한 여행자휴대품통관 길라잡이.pdf"`.
- U1 shows no page date. The only date-like string on it is an image file name.

## The premise

**F1. The basic allowance is US$800 per person, not US$600.**
Status: **stands** (premise refuted)
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=288525&chrClsCd=010202&urlMode=lsInfoP&efYd=20260731&ancYnChk=0 (시행규칙 제48조제2항)
- Quote: "각 물품(제1항제1호에 따른 물품으로서 국내에서 반출된 물품과 제1항제3호에 따른 물품은 제외한다)의 과세가격 합계 기준으로 미화 800달러 이하(이하 이 항 및 제3항에서 “기본면세범위”라 한다)로 하고"
- URL: https://www.customs.go.kr/kcs/cm/cntnts/cntntsView.do?mi=2837&cntntsId=829
- Quote: "여행자 휴대품으로서 각 물품의 과세가격 합계 기준으로 미화 800달러 이하(농축수산물 품목당 5kg, 총량 40kg 이내, 전체 해외취득가격 10만원 이내 포함)"
- URL: https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000276768&chrClsCd=010201 (고시 제18조제1항)
- Quote: "각 물품의 과세가격 합계 기준으로 미화 800달러 이하(이하 \"기본면세범위\"라 한다)로 한다."

**F2. US$600 is the figure from before 2022-09-06.**
Status: **stands**, and it is now confirmed from the primary text. The source took the old value 600 from S1. The amending ordinance itself states it.
- URL: https://www.law.go.kr/LSW/lsRvsDocListP.do?lsId=006392&chrClsCd=010202&lsRvsGubun=all (제정·개정문, 기획재정부령 제933호, 2022. 9. 6.)
- Quote: "제48조제2항 본문 중 \"600달러\"를 \"800달러\"로 하고, 같은 조 제3항의 표중 술란을 다음과 같이 한다."
- Same ordinance, 부칙: "이 규칙은 2022년 9월 6일부터 시행한다." / "제48조제2항 및 제3항의 개정규정은 이 규칙 시행 이후 여행자가 수입하는 휴대품 및 별송품부터 적용한다."
- S1, https://www.etoday.co.kr/news/view/2160787 (2022-08-05). Both quotes in the source are verbatim: "우선, 여행자 휴대품의 기본 면세 범위를 현행 600달러에서 800달러로 인상한다." / "술은 1병(1ℓ·400달러 이하), 담배는 200개비(1보루), 향수는 60㎖이다."

**F3. Alcohol, tobacco and perfume are outside the US$800 allowance.**
Status: **stands** (premise refuted)
- URL: U3 (시행규칙 제48조제3항)
- Quote: "제2항에도 불구하고 술ㆍ담배ㆍ향수에 대해서는 기본면세범위와 관계없이 다음 표(이하 이 항에서 “별도면세범위”라 한다)에 따라 관세를 면제하되,"
- URL: U7 (고시 제18조제3항): "다음 각 호의 어느 하나에 해당하는 물품은 기본면세범위를 적용하지 않는다." It is followed by "1. 술", "2. 담배" and "3. 향수".
- URL: https://www.customs.go.kr/common/nttFileDownload.do?fileKey=419b5b042b580dc7dd26f78b2b307b40 (U2 p.14 and p.4)
- Quote: "주류는 여행자 휴대품 기본면세범위(US$800)에서 제외되어 별도로 면세처리됩니다." / "향수는 여행자 휴대품 기본면세범위(US$800)에서 제외되어 별도로 면세처리됩니다."
- URL: U1: "위항과 별도로 주류(전체 용량이 2L이하이고 총 가격이 미화 400달러 이하), 필터담배 200개비, 전자담배 니코틴용액20ml(니코틴함량 1%미만), 향수 100ml"

## The allowances that decide this case

**F4. Alcohol: 2 L and US$400 in total, with no bottle count. The whisky (1.4 L, US$180) is duty-free.**
Status: **stands**, with one optional addition
- URL: U3, 제48조제3항 표. The table is an image; I read its alt text from the page HTML.
- Quote: "술 용량은 2리터(L) 이하, 가격은 미화 400달러 이하로 한다."
- URL: U7 (고시 제19조제1항제2호가목): "술: 전체 용량 2리터(ℓ) 이하(총 가격이 미화 400달러 이하의 것으로 한정한다)."
- URL: U2 p.14: "합계 용량2ℓ 이하,합계 금액 미화 400달러 이하인 주류(병수 무관) :면세"
- Old "2병" rule, from a government source better than S3. URL: https://www.korea.kr/news/policyNewsView.do?newsId=148940039 (기획재정부, 2025-02-26)
- Quote: "여행자 휴대 면세주류 제한을 최대 2병, 최대 2리터(400달러 이하)에서 병 수 제한은 폐지하고 최대 2리터(400달러 이하)로 한다."
- Change date. 제정·개정문, 기획재정부령 제1110호: "제48조제3항의 표를 다음과 같이 한다." 부칙: "이 규칙은 공포한 날부터 시행한다." (2025. 3. 21.). S3 (https://biz.sbs.co.kr/amp/article/20000220060, 2025-02-26) is quoted verbatim in the source.
- Excess rule. 시행규칙 제48조제3항 후단: "이 경우 해당 물품이 다음 표의 면세한도를 초과하여 관세를 부과하는 경우에는 해당 물품의 가격을 과세가격으로 한다." 고시 제19조제1항제2호가목 단서 is quoted verbatim in the source. U2 p.14: "브랜디·보드카·위스키 156%".
- Optional addition: the 2 L / US$400 allowance does not apply to every traveller. 고시 제19조제2항: "우범여행자 및 쿠리어가 반입하는 술은 1ℓ 이하로서 미화 60달러 이하의 것 1병만 면세한다." An ordinary tourist is neither, so this case does not change.

**F5. Perfume: 100 ml, no price limit, no bottle count. The 50 ml perfume is duty-free.**
Status: **stands**
- URL: U3, table alt text: "향수 100밀리리터"
- URL: U2 p.4: "향수의 여행자 휴대품 면세범위는 100㎖ 이하(병수 제한 없음)". U2 p.3 table: "향수 100㎖ §용량제한만 있음(수량무관)"
- URL: U7 (고시 제19조제1항제2호다목): "향수: 100밀리리터(㎖) 또는 이에 준하는 부피 또는 중량 이내의 것(예: 100g, 3.4oz 등)"
- Old 60 ml. 제정·개정문, 기획재정부령 제1033호 (2023. 12. 29.): "제48조제3항의 표 중 향수란을 다음과 같이 한다." 부칙: "이 규칙은 2024년 1월 1일부터 시행한다."
- S2 (https://newsseoul.co.kr/news/view/1065580819228468, 2024-05-08): "’24.1.1부터 향수의 면세 한도를 60ml에서 100ml로 상향했다." S1 (2022) also gives "향수는 60㎖이다".

**F6. Tobacco (side claim).**
Status: **stands**
- URL: U3, table alt text: "담배 궐련 200개비 둘 이상의 담배 종류를 반입하는 경우에는 한 종류로 한정한다." The other rows are 엽궐련 50개비, 궐련형 200개비, 니코틴용액 20밀리리터(mL), 기타유형 110그램 and 그 밖의 담배 250그램.
- URL: U2 p.4: "수량기준으로 가격제한 없음" / "한 종류만 해당"

**F7. Under-19 rule (side claim).**
Status: **stands**
- URL: U3 (제48조제3항): "19세 미만인 사람(19세가 되는 해의 1월 1일을 맞이한 사람은 제외한다)이 반입하는 술ㆍ담배에 대해서는 관세를 면제하지 않고"
- URL: U1: "만 19세 미만(출생년도 기준) 미성년자는 주류, 담배 면세범위 없음"

## The arithmetic

**F8. The cosmetics bought at the Incheon departure duty-free shop (US$150) count toward the US$800 when brought back. The legal basis is the 고시 definition, not the deduction clause.**
Status: **stands**. The source's correction of the legal basis is right. The deduction clause of 제48조제2항 still names only 법 제196조제1항제1호 단서 and 같은 조 제2항.
- URL: U3 (제48조제2항): "법 제196조제1항제1호 단서 및 같은 조 제2항에 따라 구매한 내국물품이 포함되어 있을 경우에는 기본면세범위에서 해당 내국물품의 구매가격을 공제한 금액으로 한다."
- URL: U7 (고시 제2조제17호)
- Quote: "\"해외에서 취득한 물품\"이란 해외에서 구매하거나 선물 등 무상으로 취득한 물품 또는 「관세법」(이하 \"법\"이라 한다) 제196조제1항 및 제2항에 따른 보세판매장에서 구매하여 반입하는 물품을 말한다."
- URL: U7 (고시 제6조제1항제1호): "해외에서 취득한 물품으로서 전체 취득가격 합계액이 미화 800달러를 초과하는 물품."
- URL: U2 p.6: "출국 시 국내면세점에서 구매한 후 우리나라로 다시 가지고 오는 물품, 해외에서 취득(구매·선물 등)한 물품, 입국 시 면세판매장에서 구매한 물품의 전체 가격 합계액이 US$800을 초과하는 것은 자진신고 대상"
- URL: U2 p.3 table: "해외 취득물품 합계액 (국내면세점 구매물품 포함) US$800" with "§자가사용, 선물용 등에 한함"
- Further official support, from Incheon airport customs. URL: https://www.customs.go.kr/incheon_airport/cm/cntnts/cntntsView.do?mi=12546&cntntsId=6689
- Quote: "국내 면세점 물품포함(입국장면세점 구매물품 포함)"
- URL: U4 (관세법 제196조). The quotes in the source for ① 1호 and ② are verbatim.

**F9. 150 + 620 = 770 ≤ 800, so no duty is due. The margin is US$30 and the bag breaks even at US$650.**
Status: **stands** (recomputed)
- 150 + 620 = 770. 800 − 770 = 30. 800 − 150 = 650.
- The wrong totals are right as listed. 150 + 620 + 180 + 90 = 1,040, which is 440 over 600 and 240 over 800. 150 + 620 + 90 = 860, which is 60 over. Leaving out the cosmetics gives 620, so "180 left", and 180 / 30 = 6, a six-fold overstatement.
- The figure that goes into this sum for the bag is now affected by F15. If "약 620달러" is the price before Japanese consumption tax, the amount paid in November 2026 will be higher.

## Declaring and paying

**F10. With nothing to declare, the traveller skips the form and uses the 신고없음 (면세) channel.**
Status: **stands**
- URL: U1: "신고물품 없는 여행자 : 신고서 제출 생략, 신고없음 통로 이용, 경우에 따라 세관검사를 받을 수 있습니다."
- URL: U7 (고시 제5조제2항제2호): "여행자와 승무원이 제6조제1항 및 제64조제1항에 따른 신고대상물품을 휴대하지 않은 경우에는 신고서 작성ㆍ제출을 생략할 수 있다." 단서: "다만, 세관장이 휴대품 감시ㆍ단속을 위하여 신고서 제출을 요구하는 경우에는 이를 제출해야 한다."
- URL: U7 (고시 제7조제1항제1호): "면세통로: 제6조제1항 및 제64조제1항에 따른 신고대상물품을 휴대하지 않은 여행자ㆍ승무원". The same article also has "3. 전자신고통로: 휴대품 전자신고하는 여행자ㆍ승무원".
- URL: U2 p.1: "여행자가 신고대상물품을 휴대하지 않은 경우, 휴대품 신고서 제출을 생략할 수 있습니다."
- URL: U7 (고시 제6조제1항제2호): "1명당 면세기준을 초과하는 술, 담배, 향수"

**F11. The 자진신고 reduction is 30% of the duty, capped at 20만원.**
Status: **stands**. One open point from the source is now settled: the cap rose from 15만원 to 20만원 on 2023-01-01.
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=290673&chrClsCd=010202&urlMode=lsInfoP&efYd=20261002&ancYnChk=0 (관세법 제96조제2항)
- Quote: "20만원을 넘지 아니하는 범위에서 해당 물품에 부과될 관세(제81조에 따라 간이세율을 적용하는 물품의 경우에는 간이세율을 적용하여 산출된 세액을 말한다)의 100분의 30에 상당하는 금액을 경감할 수 있다."
- When it changed. URL: https://www.law.go.kr/LSW/lsRvsDocListP.do?lsId=001556&chrClsCd=010202&lsRvsGubun=all (법률 제19186호, 2022. 12. 31., 시행 2023. 1. 1.). 제96조 is not among the 부칙 제1조 exceptions.
- Quote: "제96조제2항 중 \"15만원\"을 \"20만원\"으로 한다." / 부칙 제6조: "제96조제2항의 개정규정은 이 법 시행 이후 여행자가 반입하는 휴대품 또는 별송품부터 적용한다."
- URL: U2 p.9 (quoted verbatim in the source). Incheon customs page: "자진신고 : 관세의 30%(20만원 한도) 감면"

**F12. The penalty for not declaring is 40% of the tax, or 60% for a repeat within 2 years.**
Status: **stands**
- URL: U4 (제241조제5항)
- Quote: "납부할 세액(관세 및 내국세를 포함한다)의 100분의 20(제1호의 경우에는 100분의 40으로 하되, 반복적으로 자진신고를 하지 아니하는 경우 등 대통령령으로 정하는 사유에 해당하는 경우에는 100분의 60)"
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=283621&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0 (시행령 제247조제4항)
- Quote: "입국일을 기준으로 소급하여 2년 이내에 2회 이상 법 제241조제5항제1호의 경우에 해당하는 사유로 가산세를 징수한 경우를 말한다."
- URL: U1: "미신고 적발 시 : 가산세 부과(납부할 세액의 40%, 2년내 2회 이상 60%)"

**F13. If the allowance were exceeded, only the part above US$800 is taxed, normally at the 15% 간이세율.**
Status: **stands**. One open point from the source is now settled: a ~US$620 bag is not a 개별소비세 "고급 가방".
- URL: U7 (고시 제25조): "여행자 휴대품의 세액은 신고한 금액을 미화로 환산한 금액에서 미화 800달러를 공제한 후, 나머지 금액을 원화로 환산하고 해당 물품의 세율을 적용하여 계산한다."
- URL: U7 (고시 제18조제2항): "기본면세범위에서 법 제196조제1항제1호 단서에 따른 입국장인도장에서 인도받거나 같은 조 제2항에 따른 보세판매장에서 구매한 내국물품, 고세율품목 순서로 공제한다."
- URL: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=164022847&bylClsCd=110201 (별표 2): "4. 제1호부터 제3호까지에 해당하지 않는 물품. 다만, 고급모피와 그 제품, 고급융단, 고급가구, 승용자동차, 수렵용 총포류, 주류 및 담배는 제외한다." Rate: "15". The other rows match the source: 19, 18, 21, and "288,450원 + 1,923,000 원을 초과하는 금액의 45".
- Settled point. URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=290819&chrClsCd=010202&urlMode=lsInfoP&efYd=20260930&ancYnChk=0 (개별소비세법 시행령 제4조, [시행 2026. 9. 30.])
- Quote: "2. 법 제1조제2항제2호가목4)부터 6)까지의 물품: 1개당 200만원." Item 6) is "고급 가방" (개별소비세법 제1조제2항제2호가목6)). At any plausible rate, US$620 is far below 200만원, so row 1다 of 별표 2 does not apply. I did not check whether a particular bag falls under row 3 (which requires a base tariff of at least 10%) or row 4 (15%). That matters only if the allowance is exceeded.
- The illustration (50 × 1,400 = 70,000원 × 15% = 10,500원, less 30% = 7,350원) is arithmetically right and correctly labelled hypothetical.

**F14. 과세환율 (side claim).**
Status: **stands**
- URL: U4 (제18조): "제17조에 따른 날(보세건설장에 반입된 물품의 경우에는 수입신고를 한 날을 말한다)이 속하는 주의 전주(前週)의 기준환율 또는 재정환율을 평균하여 관세청장이 그 율을 정한다."
- URL: U7 (고시 제2조제16호): "미화 또는 US$ 표시 금액은 그 상당액의 다른 나라 통화표시 금액과 같다."

**F15. "과세가격 = the amount actually paid; a local tax refund lowers it", together with the key's wording "일본 면세로 소비세를 빼고 샀다면 그 금액".**
Status: **refuted/needs change**. The Korean rule stands. What changed is how Japanese tax-free purchases work, which also changes how the source applies the rule.
- The Korean rule is unchanged. URL: U2 p.16: "여행자 휴대품의 과세가격은 ‘신고인의 제출 서류에 명시된 신고인의 결제금액". U2 p.17: "환급받은 금액을 확인할 수 있는 경우 환급받은 세금을 공제한 금액을 구입가격으로 보아 과세할 수 있습니다." U7 (고시 제23조) is quoted verbatim in the source.
- The newer Japanese rule. URL: https://www.mlit.go.jp/kankocho/tax-free/page01_000001_00021.html (観光庁, 旅行者向け特設ページ)
- Quote: "2026年11月１日購入分からは、制度改正により、出国時に空海港（税関）で物品を国外に持ち出すことが確認された後に消費税相当額を返金する「リファンド方式」に移行します。"
- Same page: "購入者は、免税店にて 税込価格（課税）で免税対象物品を購入 することとなります。" / "返金は各免税店又は委託を受けた返金事業者から行います。"
- URL: https://www.nta.go.jp/publication/pamph/shohi/menzei/201805/format/002.htm (国税庁): "令和７年度税制改正により、令和８年11月１日から「リファンド方式」が実施されます。"
- Rate. URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6303.htm: "標準税率10パーセントと軽減税率8パーセントの複数税率になっています。"
- Why it matters. Every Osaka purchase on this trip (Nov 12 to 15) is made under the refund method. The shop charges the tax-inclusive price, and the refund comes only after the departure customs check, from the shop or a refund operator, on that operator's timetable. There is no longer a "bought without the tax" price at the till. The refunded tax is deducted in Korea only if the refund can be shown ("확인할 수 있는 경우 … 할 수 있습니다").
- Consequence. If "약 620달러" is the price before tax, the amount paid is about 620 × 1.10 = US$682. Then 150 + 682 = US$832, which is over US$800 unless the refund is documented. If 620 already includes tax, the conclusion holds with more room.
- Corrected wording for the key (replaces "일본 면세로 소비세를 빼고 샀다면 그 금액" and the bullet "일본 면세(소비세 면제·환급) 여부: 영수증상 결제금액이 과세가격이 됩니다"):
  > 일본은 2026년 11월 1일 구매분부터 면세 방식이 '리펀드 방식'으로 바뀌어, 매장에서는 소비세를 포함한 가격으로 결제하고 출국할 때 공항 세관 확인을 거친 뒤 소비세 상당액을 돌려받습니다(환급은 매장이나 위탁 환급업체가 합니다). 한국 세관은 환급받은 금액이 영수증 등으로 확인될 때 그만큼 뺀 금액을 구입가격으로 볼 수 있습니다. '약 620달러'가 세금 전 가격이라면 실제 결제액은 약 682달러이고, 환급이 확인되지 않으면 150 + 682 = 832달러로 800달러를 넘을 수 있습니다. 결제 영수증과 환급 내역을 함께 챙기고, 가방 금액이 650달러를 넘는지 그 기준으로 확인하라고 안내해야 합니다. [경우에 따라 다름]

**F16. Allowances are per person, with no pooling (side claim).**
Status: **stands**
- URL: U7 (고시 제22조제3항): "2명 이상의 동반가족이 미화 800달러를 초과하는 물품 1개 또는 1세트를 휴대반입한 경우 1명이 반입한 것으로 보아 제1항을 준용한다."
- URL: U2 p.1: "동반가족인 경우 대표자 1인이 일괄신고 할 수 있습니다."

**F17. 농림축수산물 (side claim).**
Status: **stands**
- URL: U7 (고시 제20조제1항): "총량 40kg 이내, 전체 해외취득가격 10만원 이내로 한다."
- URL: U2 p.5: "농림축수산물 및 한약재의 면세통관범위는 총량 40kg 이내, 전체 해외취득가격 10만원 이내로 합니다."

**F18. How to declare when there is something to declare (side claim).**
Status: **stands**
- URL: U1: "신고물품이 있는 여행자 : 신고서 제출(종이,모바일), 모바일로 자진신고 시 모바일로 고지서 발급 및 납부 가능"
- URL: U2 p.2 (the QR code and 자동 심사대 quote is verbatim). U2 p.18: "사후납부 : 내국인 자진신고자 대상(체납자, 우범여행자 등 제외)", with "15일 이내".
- URL: U3 (제49조의2, now marked "<개정 2026. 1. 2.>" for the ministry rename): "항공기를 통하여 입국하는 경우: 별지 제42호서식의 여행자 휴대품 신고서"
- Incheon customs page: "'여행자 세관신고' 앱 또는 웹'으로 신고 가능"

**F19. No purchase limit on outbound duty-free shopping (side claim).**
Status: **stands** as hedged ("partly verified")
- URL: U3 (제69조의4제1항): "미화 800달러의 한도에서 판매해야 하며, 술ㆍ담배ㆍ향수는 제48조제3항에 따른 별도면세범위에서 판매할 수 있다." This applies only to 법 제196조제2항 shops (입국장 면세점). The 2022-09-06 ordinance changed it from 600 to 800 ("제69조의4제1항 및 제3항 중 \"600달러\"를 각각 \"800달러\"로 한다").
- I did not check the abolition of the old 5,000달러 outbound limit either.

## Summary for the key

- The premise is false on both counts. The basic allowance is US$800, not 600, and alcohol, tobacco and perfume are outside it. The correction stands on the law in force on 2026-10-25 and on the return date, 2026-11-15, unless the 시행규칙 is amended before then. Nothing pending was found.
- F1–F14 and F16–F19 stand. F2, F11 and F13 now rest on more primary evidence than the source had.
- **F15 needs change.** Japan's refund method (purchases from 2026-11-01) replaces the "bought without the tax" price that the key relies on. The answer should tell the traveller to keep both the receipt and the refund record, and to judge the US$650 threshold on the amount actually paid. If "약 620달러" is a pre-tax price, the trip can exceed US$800 (150 + 682 = 832).

## Not decided in this pass
- Whether the 2026 세법개정안 proposes any change to the traveller allowances. The search budget ran out before I could open the 재정경제부 release. Nothing was in force or pending on law.go.kr as of 2026-10-25.
- Whether the user's "약 620달러" includes Japanese consumption tax, and when a given Osaka shop's refund operator pays out.
- The 과세환율 for the week before 2026-11-15.
- Which 간이세율 row (3나 or 4) applies to the user's particular bag. It matters only if the allowance is exceeded.
- The primary text abolishing the old 출국 면세점 5,000달러 limit.
