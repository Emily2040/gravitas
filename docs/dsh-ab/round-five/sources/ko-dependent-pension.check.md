# Adversarial check: ko-dependent-pension.md, items 1 to 21 and "Facts for the key"

Checked 2026-10-25 to 2026-10-26 by an agent that did not write the source file. On disk I read only `prompts/ko-dependent-pension.txt`, `sources/ko-dependent-pension.md` and, for format, round four's `en-fsa-rollover.check.md`. Every URL below was opened in this check. law.go.kr statute bodies were downloaded from the `lsInfoR.do` body behind each `lsInfoP.do` page (same `lsiSeq` and `efYd`), annexes were downloaded as PDFs from `flDownload.do` and converted with pdftotext, and the NHIS, 보건복지부 and 복지로 pages were downloaded as HTML and read as text. Quotes are verbatim, two lines at most, with "…" for cuts. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: no change to the 피부양자 income or property rules, and no announced change, was found up to 2026-10-26. (1) The law.go.kr entry page of every statute the source cites still resolves to the version the source lists: 국민건강보험법 lsiSeq=285273 [시행 2026. 10. 8.], 시행령 289701 [시행 2026. 10. 1.], 시행규칙 290599 [시행 2026. 9. 28.] [보건복지부령 제1202호], 국민연금법 291347 [시행 2026. 10. 20.], 기초연금법 276657, 소득세법 280405, 소득세법 시행령 290841, 지방세법 282559, 지방세법 시행령 290815, 노인장기요양보험법 286217, 시행령 286011. (2) I listed every promulgated but not yet effective version through the law.go.kr open API (`https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=XML&nw=2&query=<법령명>`). 국민건강보험법 시행규칙, 노인장기요양보험법 시행령 and 지방세법 시행령 have **none**, so 별표 1의2, the 0.9448% rate and the 2026 공정시장가액비율 have no pending change. Pending versions exist for 국민건강보험법 (법률 제21235호, 시행 2026-12-24; 제21687호, 시행 2026-11-27 and 2027-01-01), its 시행령 (제36675호 parts, 2026-12-24 and 2027-01-01), 국민연금법 (제21689호, 제21931호, 제22096호, 제21473호), 기초연금법 (제22097호), 노인장기요양보험법 (제21690호, 2026-11-27), 소득세법 and 지방세법 (2027-01-01 parts). I downloaded each future version and compared it article by article with the version in force. None changes 법 제5조 or 제69조 to 제73조, 영 제32조, 제41조, 제41조의2, 제42조 or 제44조, 국민연금법 제51조, 제54조, 제61조 or 제63조의2, 기초연금법 제3조①, 소득세법 제20조의3, 제47조의2, 제50조, 제73조, 제143조의2 or 제143조의4, or 지방세법 제4조 or 제110조. The only touched article the source relies on is 노인장기요양보험법 제9조① (rounding of the ratio, item 18), which does not change any figure. (3) The 2027 건강보험료율 was set on 2026-09-08: frozen at 7.19%, with 211.5원 per property point (item 18). (4) I scanned the 보건복지부 press-release list (`https://www.mohw.go.kr/board.es?mid=a10503010100&bid=0027&nPage=1` to `nPage=16`, 2026-08-04 to 2026-10-23). It has no release on 피부양자 criteria, on 부과체계 changes, or on the 2027 장기요양보험료율. (5) Web searches before the budget ran out found no official notice of a change to the 피부양자 criteria. Results were blogs restating the 2,000만 / 5.4억 rules, and a 2026 search confirmed the 2022 reduction (80/60/40/20%) ended in August 2026. (6) The 2027 국민연금 adjustment is not published. It is set in January 2027 from 2026 CPI.

Tooling note: the shared WebSearch budget ran out partway through this check. All later checks used direct fetches of official primary URLs and the law.go.kr open API.

## The rules (items 1 to 10)

**1. Parents can be 피부양자 of a 직장가입자 if income and property are under the 보건복지부령 limits. The law has no pension-receipt rule.**
Status: **stands**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285273&chrClsCd=010202&urlMode=lsInfoP&efYd=20261008&ancYnChk=0 (국민건강보험법 [시행 2026. 10. 8.] [법률 제21522호], 제5조②)
- Quote: "② 제1항의 피부양자는 다음 각 호의 어느 하나에 해당하는 사람 중 직장가입자에게 주로 생계를 의존하는 사람으로서 소득 및 재산이 보건복지부령으로 정하는 기준 이하에 해당하는 사람을 말한다." / "2. 직장가입자의 직계존속(배우자의 직계존속을 포함한다)"
- Pending amendments 제21235호 and 제21687호 leave 제5조 unchanged.

**2. 시행규칙 제2조①: the test is 부양요건 (별표 1) plus 소득·재산요건 (별표 1의2).**
Status: **stands**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=290599&chrClsCd=010202&urlMode=lsInfoP&efYd=20260928&ancYnChk=0 (국민건강보험법 시행규칙 [시행 2026. 9. 28.] [보건복지부령 제1202호])
- Quote: "1. 별표 1에 따른 부양요건에 해당할 것" / "2. 별표 1의2에 따른 소득 및 재산요건에 해당할 것"
- 별표 1 PDF (<개정 2018. 3. 6.>): https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169566171&bylClsCd=110201 (the PDF linked from the current 시행규칙 body). Row 2.가, 비동거 시: "부모(아버지 또는 어머니와 재혼한 배우자 포함)와 동거하고 있는 형제자매가 없거나, 있어도 보수 또는 소득이 없는 경우 부양 인정"

**3. Income requirement: total income of 연간 2천만원 이하.**
Status: **stands**
- URL: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169566181&bylClsCd=110201 (별표 1의2 PDF linked from the current body; header "국민건강보험법 시행규칙 [별표 1의2] <개정 2025. 4. 23.>")
- Quote (1.가): "가. 영 제41조제1항 각 호의 소득을 같은 조 제3항의 소득자료에 따라 산정한 합계액이 연간 2천만원 이하일 것"
- The brief's URL https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=151253555&bylClsCd=110201 is a different file. Its extracted text is identical line for line, header included (checked with diff).

**4. Public pension counts in full (gross, including the pre-2002 part) for the dependent test. The 50% rule is only for premiums.**
Status: **stands**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=289701&chrClsCd=010202&urlMode=lsInfoP&efYd=20261001&ancYnChk=0 (국민건강보험법 시행령 [시행 2026. 10. 1.] [대통령령 제36675호], 제41조①5)
- Quote: "5. 연금소득: 「소득세법」 제20조의3에 따른 소득. 다만, 같은 조 제1항제1호의 공적연금소득의 경우에는 같은 조 제2항을 적용하지 않고 해당 과세기간에 발생한 연금소득 전부를 연금소득으로 한다."
- 50% rule, 시행규칙 page as in item 2 (제44조②): "② 법 제71조제1항에 따른 직장가입자의 보수 외 소득월액은 다음 각 호의 구분에 따라 평가한 금액을 합산하여 산정한다." / "2. 영 제41조제1항제4호 및 제5호의 소득: 해당 소득의 100분의 50". 제44조③ applies 제2항 전단 to the 지역가입자 소득월액. 시행규칙 제44조①5 counts the pension as "「소득세법」 제20조의3제1항 각 호에 따른 소득의 금액의 합계액", the gross amount before 연금소득공제.
- URL: https://mohw.go.kr/board.es?act=view&bid=0030&list_no=372716&mid=a10504000000&nPage=21&tag= (보건복지부 보도설명자료 "[8.29.중앙] 연금소득 피부양 보도 관련", 작성일: 2022-08-29 11:54)
- Quote: "이 중 국민연금 수급액이 연간 2,000만 원을 넘어 지역가입자로 전환되는 피부양자는 2,685명*으로, 피부양 상실 예정자(27.3만 명)의 1% 미만"

**5. Business income must be zero (500만 exception only when not registered, and not for 주택임대소득).**
Status: **stands**
- URL: 별표 1의2 PDF as in item 3 (1.나)
- Quote: "나. 영 제41조제1항제3호의 사업소득(이하 이 표에서 "사업소득"이라 한다)이 없을 것. 다만, … 사업소득의 합계액이 연간 500만원 이하인 경우에는 사업소득이 없는 것으로 본다." / "1) 사업자등록이 되어 있지 않은 경우(「소득세법」 제19조제1항제12호에 따른 부동산업에서 발생하는 소득 중 주택임대소득이 있는 경우는 제외한다)"

**6. Married couple: both spouses must meet the income requirement.**
Status: **stands**
- URL: 별표 1의2 PDF as in item 3 (1.라)
- Quote: "라. 피부양자가 되려는 사람이 기혼자인 경우에는 부부 모두 가목부터 다목까지의 요건을 충족하여야 한다."
- URL: https://www.nhis.or.kr/nhis/policy/wbhada07400m01.do
- Quote: "피부양자가 기혼자인 경우에는 부부 모두 소득요건을 충족해야 함"
- The source's reading that 라목 covers only the income items (가 to 다) matches the annex layout: 라목 sits under 제1호 (income), and 제2호 (property) has no spouse clause.

**7. Property requirement: 재산세 과세표준 합 5억4천만원 이하, or over 5.4억 up to 9억 with income of 1천만원 이하. Siblings 1.8억.**
Status: **stands**
- URL: 별표 1의2 PDF as in item 3 (2.가, 2.나)
- Quote: "2) 영 제42조제1항제1호에 따른 재산에 대한 「지방세법」 제110조에 따른 재산세 과세표준의 합이 5억4천만원 이하일 것"
- Quote: "1) … 재산세 과세표준의 합이 5억 4천만원을 초과하면서 9억원 이하이고, 영 제41조제1항 각 호에 따른 소득의 합계액이 연간 1천만원 이하일 것"
- 2.가 applies to "별표 1의 제1호부터 제9호까지". Parents are 별표 1 row 2, so 2.가 applies. Siblings (row 10) get 2.나: "1억8천만원 이하".
- 영 제42조①1, 시행령 page as in item 4: "「지방세법」 제105조에 따른 재산세의 과세대상이 되는 토지, 건축물, 주택, 선박 및 항공기"

**8. The NHIS page states the same thresholds.**
Status: **stands**
- URL: https://www.nhis.or.kr/nhis/policy/wbhada07400m01.do (담당부서 "자격부과실"; no date on the page)
- Quotes: "모든 소득(사업·금융·연금·근로기타소득 등)을 합하여 연간 2천만원 이하" / "재산과표가 5.4억원 이하"
- Quote: "재산과표가 5.4억원을 초과하면서 9억원 이하인 경우에는 연간 소득 1천만원 이하" / "재산의 종류: 토지, 건축물, 주택, 선박, 항공기"
- The page still quotes the pre-2025 annex wording ("영 제41조제1항 각 호에 따른 소득의 합계액이 연간 2천만원 이하일 것", with the old "영 제42조제3항제1호"). The substance is the same, as the source says.

**9. Data timing: pension income uses the previous year's data in every month. Other income uses data from two years earlier in January to October and the previous year in November and December.**
Status: **stands**
- URL: 시행령 page as in item 4 (제41조③)
- Quote: "1. 매년 1월부터 10월까지의 소득월액 산정 시: 소득월액보험료(…)가 부과되는 연도의 전전년도 자료. 다만, 제1항제5호의 연금소득 자료는 소득월액보험료가 부과되는 연도의 전년도 자료로 한다."
- Quote: "2. 매년 11월 및 12월의 소득월액 산정 시: 소득월액보험료가 부과되는 연도의 전년도 자료"
- 별표 1의2 1.가 ties the dependent test to this rule ("같은 조 제3항의 소득자료에 따라", item 3). The NHIS page (item 8) quotes the same rule and, from 정관 제43조의4②, the property data window: "해당 연도 6월 1일을 기준으로 하는 재산세 과세자료를 말한다): 해당 연도 11월부터 다음 연도 10월까지".
- Recomputed timeline: 2026 data = 150만 × 2 = 300만 (tested in 2027). 2027 data at a 2% adjustment = 153만 × 12 = 1,836만 (tested in 2028). "해당 과세기간에 발생한 연금소득 전부" (item 4) supports using the amount actually received in the year, not an annualised figure. Neither year reaches 2,000만.

**10. Status would end the day after NHIS confirms the failure, and no report is needed for the pension.**
Status: **stands**, with one optional precision
- URL: 시행규칙 page as in item 2 (제2조③9, ④ 단서)
- Quote: "9. 제1항에 따른 요건을 충족하지 아니하는 경우에는 공단이 그 요건을 충족하지 아니한다고 확인한 날의 다음 날"
- Quote: "다만, 공단이 법 제96조에 따라 국가 등으로부터 제공받은 자료로 피부양자 자격 취득 또는 상실 대상자를 확인할 수 있는 경우에는 신고서를 제출하지 아니한다."
- Precision: 제2조③ also has 제10호 and 제11호 (<개정 2023. 9. 11., 2024. 5. 13.>), which the source does not mention. They end status at the end of the month (or the following month) in which 사업소득 or 근로소득 arose, but only for people who used the income-adjustment route of 영 제41조의2 ("영 제41조제1항제3호 및 제4호의 소득(이하 “사업소득등”이라 한다)"). They do not apply to pension income, so the pension conclusion is unchanged. Relevant only if the key discusses a working father.

## Applying the rules to this family (items 11 to 15)

**11. The pension level at which the income test fails is 2,000만 ÷ 12 = 1,666,667원 a month. 150만 × 12 = 1,800만 passes by 200만.**
Status: **stands**
- Recomputed from item 3 ("연간 2천만원 이하"): 20,000,000 ÷ 12 = 1,666,666.7. 1,500,000 × 12 = 18,000,000.
- The wrong values the source lists (월 100만, 연 1,000만, 연 3,400만, 월 333만) are correctly explained by items 7, 19 and 4.

**12. A 4억 공시가격 apartment gives a 과세표준 of 1.76억 (1세대 1주택, 44%) or 2.4억 (60%), far under 5.4억.**
Status: **stands**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=282559&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0 (지방세법 [시행 2026. 7. 1.] [법률 제21308호], 제110조①, 제4조①)
- Quote (제110조①): "토지ㆍ건축물ㆍ주택에 대한 재산세의 과세표준은 제4조제1항 및 제2항에 따른 시가표준액에 … 대통령령으로 정하는 공정시장가액비율을 곱하여 산정한 가액으로 한다."
- Quote (제4조①): "이 법에서 적용하는 토지 및 주택에 대한 시가표준액은 「부동산 가격공시에 관한 법률」에 따라 공시된 가액(價額)으로 한다."
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=290815&chrClsCd=010202&urlMode=lsInfoP&efYd=20261001&ancYnChk=0 (지방세법 시행령 [시행 2026. 10. 1.] [대통령령 제36736호], 제109조①, <… 2026. 5. 29.>)
- Quote: "2. 주택: 시가표준액의 100분의 60. 다만, 2026년도에 납세의무가 성립하는 재산세의 과세표준을 산정하는 경우 제110조의2에 따라 1세대 1주택으로 인정되는 주택(…)에 대해서는 다음 각 목의 구분에 따른다." / "나. 시가표준액이 3억원을 초과하고 6억원 이하인 주택: 시가표준액의 100분의 44"
- Cap: 시행령 제109조의2②: "법 제110조제3항의 계산식에서 “대통령령으로 정하는 비율”이란 100분의 5를 말한다."
- Recomputed: 4억 × 0.44 = 1.76억. 4억 × 0.60 = 2.4억. The 1세대 1주택 ratio is written for 2026 only. Even at 60% the result passes, so 2027 cannot change the outcome.

**13. 국민연금 is adjusted each January by CPI. The 2026 rate was 2.1%. The 2027 rate is not yet known.**
Status: **stands** (rule and 2026 rate). The 2027 rate is still unpublished as of 2026-10-26.
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=291347&chrClsCd=010202&urlMode=lsInfoP&efYd=20261020&ancYnChk=0 (국민연금법 [시행 2026. 10. 20.] [법률 제22096호], 제51조②)
- Quote: "② 제1항 각 호의 금액을 수급권자에게 적용할 때에는 연금 수급 2년 전 연도와 대비한 전년도의 전국소비자물가변동률을 기준으로 그 변동률에 해당하는 금액을 더하거나 빼되,"
- URL: https://www.bokjiro.go.kr/ssis-tbu/cms/pc/news/news/1309186_1114.html (복지로, "[이슈] 국민연금·기초연금 급여 2.1% 인상 확정", "등록일 : 2026-01-10")
- Quote: "2026년 국민연금 기본연금액 및 부양가족연금액을 전년도 소비자물가상승률(2.1%, 국가데이터처 발표)을 반영하여 인상하였다."
- Recomputed: ln(2000/1800) ÷ ln(1.02) = 5.32, ÷ ln(1.021) = 5.07, ÷ ln(1.025) = 4.27. 150만 × 1.02^5 = 165.6만 and 150만 × 1.021^5 = 166.4만, both still under 166.7만. So the pension alone first exceeds the limit at the January 2031 (2.5%) to January 2032 (2.0 to 2.1%) adjustment, as the source says. The pending 국민연금법 amendments (제21689호, 제21931호, 제22096호, 제21473호) leave 제51조 unchanged.

**14. For a 1963 birth the 노령연금 starts at 63. Payment starts the month after entitlement, on the 25th.**
Status: **stands**
- URL: 국민연금법 page as in item 13
- Quote (제61조①): "가입기간이 10년 이상인 가입자 또는 가입자였던 자에 대하여는 60세(특수직종근로자는 55세)가 된 때부터 그가 생존하는 동안 노령연금을 지급한다."
- Quote (부칙 <법률 제8541호, 2007. 7. 23.> 제8조): "… 1961년부터 1964년까지 출생자는 3세를, 1965년부터 1968년까지 출생자는 4세를, 1969년 이후 출생자는 5세를 각각 더한 연령을 적용한다."
- Quote (제54조①②): "지급하여야 할 사유가 생긴 날(…)이 속하는 달의 다음 달부터" / "② 연금은 매월 25일에 그 달의 금액을 지급하되, 지급일이 토요일이나 공휴일이면 그 전날에 지급한다."

**15. 기초연금 needs age 65, so the father (63) is not eligible. The 2026 기준연금액 is 349,700원.**
Status: **stands**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=276657&chrClsCd=010202&urlMode=lsInfoP&efYd=20251001&ancYnChk=0 (기초연금법 [시행 2025. 10. 1.] [법률 제21065호], 제3조①)
- Quote: "① 기초연금은 65세 이상인 사람으로서 소득인정액이 보건복지부장관이 정하여 고시하는 금액(이하 “선정기준액”이라 한다) 이하인 사람에게 지급한다."
- 복지로 page as in item 13: "2025년 34만 2,510원에서 2026년 34만 9,700원으로 늘어난다."
- The pending 기초연금법 제22097호 (시행 2027-01-21) keeps 제3조① ("65세 이상") unchanged.

## Side facts (items 16 to 21)

**16. Income tax on 국민연금: only the post-2002 part is taxable. NPS withholds monthly by the 간이세액표, settles in January, and a person with only 공적연금 need not file in May. If the whole 150만 were taxable, the withholding for two 공제대상 people would be 35,930원 plus 3,590원 지방소득세.**
Status: **stands**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=280405&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0 (소득세법 [시행 2026. 7. 1.] [법률 제21221호])
- Quote (제20조의3②): "② 공적연금소득은 2002년 1월 1일 이후에 납입된 연금 기여금 및 사용자 부담금(…)을 기초로 하거나 2002년 1월 1일 이후 근로의 제공을 기초로 하여 받는 연금소득으로 한다."
- Quote (제143조의2①; title "연금소득에 대한 원천징수시기 및 방법"): "① 원천징수의무자가 공적연금소득을 지급할 때에는 연금소득 간이세액표에 따라 소득세를 원천징수한다."
- Quote (제143조의4①): "① 공적연금소득에 대한 원천징수의무자가 해당 과세기간의 다음 연도 1월분의 공적연금소득을 지급할 때에는 …"
- Quote (제73조①3): "3. 공적연금소득만 있는 자"
- 연금소득공제 (제47조의2①): the table is an image. Its alt text on the same page reads "350만원 이하 총연금액", "350만원 초과 700만원 이하 … 350만원 + (350만원을초과하는금액의100분의40)", "700만원 초과 1400만원 이하 … 490만원 + (700만원을초과하는금액의100분의20)", "1400만원 초과 … 630만원 + (1400만원을초과하는금액의100분의10)", and the article text says "공제액이 900만원을 초과하는 경우에는 900만원을 공제한다."
- 간이세액표 URL: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169798209&bylClsCd=110201 (소득세법 시행령 [별표 3] <개정 2023. 2. 28.>, first table "(70세 이상자가 없는 경우)")
- Quote: "1,500 1,510 43,430 35,930 28,430 20,930 13,430 5,930 0"
- Recomputed: 35,930 + 3,593 → about 3.95만 원 a month at most.

**17. The user's 연말정산: the father can be claimed for 2026 (연금소득금액 0). From 2027 he stays claimable only while his taxable 총연금액 is about 516.7만 or less. This is separate from 건보 피부양자.**
Status: **stands**
- URL: 소득세법 page as in item 16 (제50조①3가)
- Quote: "3. 거주자(그 배우자를 포함한다. 이하 이 호에서 같다)와 생계를 같이 하는 다음 각 목의 어느 하나에 해당하는 부양가족(…)으로서 해당 과세기간의 소득금액 합계액이 100만원 이하인 사람" / "가. 거주자의 직계존속(…)으로서 60세 이상인 사람"
- Recomputed from the 제47조의2 table: 300만 is under 350만, so 연금소득금액 = 0. In the 350만 to 700만 band, 소득금액 = 0.6x − 210만 ≤ 100만 gives x ≤ 516.7만. Pending 소득세법 changes for 2027 leave 제20조의3, 제47조의2 and 제50조 unchanged.

**18. Hypothetical regional premium if the parents lost status: about 14.8만 (1세대 1주택) to 18.4만 원/월 (60%), with 장기요양.**
Status: **refuted/needs change** (one sub-claim only; the main figures stand)
- URL: 시행령 page as in item 4 (제44조①②, <… 2025. 12. 23.>)
- Quote: "… 지역가입자의 보험료율은 각각 1만분의 719로 한다." / "② 법 제73조제3항에 따른 지역가입자의 재산보험료부과점수당 금액은 211.5원으로 한다."
- URL: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169130903&bylClsCd=110201 (시행령 [별표 4] <개정 2024. 5. 7.>, linked from the current body)
- Quote: "다음 각 목의 금액을 합산한 금액에서 1억원 및 제42조의2제3항 각 호의 구분에 따른 금액을 뺀 금액을 등급별로 구분하여 산정한다." Rows: "15 6,930 초과 ~ 7,710 이하 365" / "21 13,300 초과 ~ 14,800 이하 516"
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=286011&chrClsCd=010202&urlMode=lsInfoP&efYd=20260512&ancYnChk=0 (노인장기요양보험법 시행령 제4조)
- Quote: "법 제9조제1항에 따른 장기요양보험료율은 100만분의 9,448로 한다."
- Recomputed: 1,800만 × 50% ÷ 12 × 7.19% = 53,925. 365 × 211.5 = 77,197.5. Sum 131,123 × (1 + 0.9448/7.19) = 148,353, so about 14.8만. 60% case: (53,925 + 109,134) × 1.13141 = 184,486, so about 18.4만. Both stand.
- 2027 update. URL: https://www.mohw.go.kr/board.es?mid=a10503010100&bid=0027&act=view&list_no=1491824&tag=&nPage=1 (보건복지부 보도자료, 작성일: 2026-09-08 13:45)
- Quote: "□ 2027년도 건강보험료율을 동결하여 올해와 동일한 7.19%로 결정하였다. 또한 지역가입자의 재산보험료부과점수당 금액도 올해와 동일한 211.5원으로 결정하였다."
- So the hypothetical holds for 2027 too, except the 장기요양보험료율, for which no 2027 decision was found. 노인장기요양보험법 제9조① as amended by 법률 제21690호 (시행 2026-11-27) adds "(소수점 이하 다섯째자리에서 반올림한다)" to the ratio. 0.9448/7.19 rounds to 0.1314, so the figures do not change.
- **What needs changing:** the source says a premium charged in 2027 on 2026 pension data (300만) would have an income part of "only about 9,000원". 300만 × 50% ÷ 12 = 12.5만 소득월액, which is under the 28만 floor in 시행규칙 제44조③ 단서 (시행규칙 page as in item 2):
- Quote: "다만, 지역가입자의 소득월액이 28만원 이하인 경우에는 영 제32조제2호나목에 따른 월별 보험료액의 하한액을 영 제44조제1항에 따른 보험료율로 나누어 얻은 값을 해당 지역가입자의 소득월액으로 한다."
- Corrected wording: "A premium charged in 2027 would use 2026 pension data (300만). That gives a 소득월액 of 12.5만, under the 28만 floor, so the income part would be the 지역가입자 월별 보험료 하한액 set by 보건복지부 고시 (영 제32조제2호나목), not about 9,000원. [figure not fetched in this check]" This sits inside a hypothetical that does not apply to the family, so it changes no conclusion.

**19. The 2022 limit change (3,400만 → 2,000만) and its 4-year premium reduction, which ended with the August 2026 premium.**
Status: **stands**
- URL: 보건복지부 2022-08-29 release as in item 4
- Quote: "피부양자 소득요건 강화(현행 연 3,400만 원 → 2,000만 원) 등"
- Quote: "* 경감률 : 80%(‘22.9.~’23.10.) → 60%(‘23.11.~’24.10.) → 40%(‘24.11.~’25.10.) → 20%(‘25.11.~’26.8.)"
- Same release: "피부양 상실 예정 세대의 평균 건강보험료는 월 14.9만 원이나,"
- URL: 시행규칙 page as in item 2 (부칙 <보건복지부령 제907호, 2022. 9. 1.> 제3조①)
- Quote: "4. 2025년 11월분부터 2026년 8월분까지의 보험료: 100분의 20"
- Scope, same 제3조①: "별표 1의2 제1호가목의 개정규정에 따라 피부양자 자격의 인정기준 중 소득요건을 갖추지 못하게 되어 최초로 직장가입자의 피부양자 자격을 잃고"

**20. 이자·배당 of 1천만원 or less are not added (시행규칙 제44조① 단서). Its use in the dependent test is inferred.**
Status: **stands** (rule text). The application to the dependent test is still inferred, as the source says.
- URL: 시행규칙 page as in item 2 (제44조①)
- Quote: "다만, 제1호 및 제2호에도 불구하고 「소득세법」 제14조제3항제6호에 따른 소득이 1천만원 이하인 경우에는 해당 이자소득과 배당소득은 합산하지 않는다."
- Link: 영 제41조② ("제1항 각 호의 소득의 구체적인 산정방법은 보건복지부령으로 정한다.") sends the calculation to 제44조①, and 별표 1의2 1.가 uses 영 제41조① income. No NHIS page found that applies it to dependents.

**21. If the father works: the 재직자 감액 now applies only from 200만 of 초과소득월액.**
Status: **stands**
- URL: 국민연금법 page as in item 13 (제63조의2)
- Quote: "1. 삭제 <2025. 12. 16.>" / "3. 초과소득월액(…)이 200만원 이상 300만원 미만인 사람: 15만원 + (초과소득월액 - 200만원) × 1천분의 150"
- 부칙 <법률 제21203호, 2025. 12. 16.>: "다만, 제63조의2의 개정규정은 공포 후 6개월이 경과한 날부터 시행한다." / "제63조의2의 개정규정은 2025년 1월 1일 이후 발생한 소득부터 적용한다."

## "Facts for the key"

**The premise is false and the correction stands.** No rule removes a 피부양자 because a pension starts, whatever its amount (items 1 to 3, 8). The test is 연간 2천만원 of total income, with the full gross pension counted (item 4), both spouses meeting it (item 6), and 과세표준 5.4억 for property (item 7). Status: **stands**.

**Applied to this family:** 1,800만 a year is under 2,000만. The mother has no income. 과세표준 1.76억 or 2.4억 is under 5.4억. Assuming no other income for the father, both parents stay 피부양자, and the 15만 원 line should come out of the budget. Status: **stands** (items 11, 12). The open fact (the father's other income) is correctly flagged.

**"바로" is also wrong:** pension data are the previous year's (item 9). Status: **stands**.

**What a correct answer must also say (1 to 5):** 166.7만 monthly line, full gross (items 4, 11); other income adds in, business income can fail the test alone (items 3, 5, 21); spouse rule (item 6); CPI indexation and an annual review, about five adjustments away (item 13); budget with pension income, withholding at most about 4만, no premium line (items 16, 18). Status: **stands**, all five.

**Side claims:** each wrong/right label in the source's list matches the items above: 50% rule (item 4), post-2002 portion (item 4), 3,400만 (item 19), 공시가격 5.4억 framing (items 7, 12), "immediately" and "November review" (item 9), reporting duty (item 10), 기초연금 (item 15), 2022 reduction (item 19), regional premium range (item 18), income tax (item 16), 연말정산 (item 17), start age (item 14), 재직자 감액 (item 21). Status: **stands**. If the key repeats the "about 9,000원" 2027 income-part figure from item 18, it should use the corrected wording above.

## Not decided in this pass
- The 2027 국민연금 adjustment rate (set in January 2027 from 2026 CPI).
- The 2027 장기요양보험료율. No decision was found in the 보건복지부 press list through 2026-10-23. The 2027 health rate (7.19%) and point value (211.5원) are decided.
- The exact 2026 지역가입자 월별 보험료 하한액 (보건복지부 고시) needed for the corrected item 18 sub-claim.
- Whether NHIS applies the 이자·배당 1천만 exclusion to dependents (item 20). The text supports it, but no NHIS page says so.
- The father's actual withholding and taxable share (depends on his record).
