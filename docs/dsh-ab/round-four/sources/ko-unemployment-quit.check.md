# Adversarial check: ko-unemployment-quit, "Facts for the key"

Checked 2026-10-24 against primary sources opened in this session. Law texts were read from law.go.kr in the versions current today. The "현행" lookup (https://www.law.go.kr/법령/<name>) returned the same versions the source file cites:
- 고용보험법: lsiSeq 284449, [시행 2026. 9. 18.] 법률 제21473호
- 시행령: 288717, 대통령령 제36588호
- 시행규칙: 288723, 고용노동부령 제479호
- 근로기준법: 285279, [시행 2026. 10. 8.]
- 근로기준법 시행령: 270551
- 임금채권보장법: 283451
- 임금채권보장법 시행령: 285855
- 임금채권보장법 시행규칙: 289001, [시행 2026. 8. 20.]
- 근로자퇴직급여 보장법: 284455
- 근로자퇴직급여 보장법 시행령: 284693

Article bodies were fetched through the same lsiSeq with lsInfoR.do. Quotes are verbatim and short.

Result: 46 facts checked. **43 stand. 3 need change: #4, #6 and #41.** Five items could not be decided; they are listed at the end.

The most important correction: under 고용노동부's published criteria, wages paid in full but late count toward the 2-month test by **adding up the days of delay** (2 months = 60 days, 1 month = 30 days). The number of months that were late does not decide it. "Late in July, August and September" therefore does not by itself prove the 2-month test is met.

---

## 1. 전제와 그것이 틀린 이유

**#1 질문자의 전제("자발적 퇴사라 실업급여 못 받는다")는 틀렸다. Stands.**
제58조 bars benefits only for voluntary quits without a 정당한 사유, and 별표 2 lists 임금체불 as such a reason (see #2 and #3).

**#2 제58조 제2호 다목: a 정당한 사유 under 고용노동부령 lifts the bar. Stands.**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=284449&chrClsCd=010202&urlMode=lsInfoP&efYd=20260918&ancYnChk=0
- Quote: "다. 그 밖에 고용노동부령으로 정하는 정당한 사유에 해당하지 아니하는 사유로 이직한 경우"
- 시행규칙 제101조② (lsiSeq 288723): "“고용노동부령으로 정하는 정당한 사유”란 별표 2를 말한다."

**#3 별표 2 제1호 나목: "임금체불이 있는 경우"가 이직일 전 1년 이내 2개월 이상. Stands.**
- URL (별표 2 PDF, <개정 2024. 7. 1.>, still the annex of the current 시행규칙): https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169481947&bylClsCd=110201
- Quote: "1. 다음 각 목의 어느 하나에 해당하는 사유가 이직일 전 1년 이내에 2개월 이상 발생한 경우 … 나. 임금체불이 있는 경우"
- No 2025-2026 amendment to 제58조 or 별표 2 was found. SBS Biz (2026-08-04) reported a plan to extend benefits to young people who quit voluntarily. It is only a 업무보고 plan: the text of 제58조 in force is unchanged.

**#4 "7·8·9월 석 달 제때 안 나왔으므로 2개월 요건을 넘는다 → 받을 수 있는 경우". Needs change.**

Three late months do not automatically meet the test. 고용노동부's published answers on applying 별표 2 measure full-wage lateness as **total days of delay or non-payment within the year before 이직**, and they give a 10-days-late-each-month example.
- Decisive URL: 고용노동부 빠른인터넷상담. The page shows no date; the ID suggests 2024-07-08. https://www.moel.go.kr/minwon/fastcounsel/fastcounselView.do?inetDcssMngId=202407081113532950110
- Quote: "임금 전액이 체불된 경우에는 이직 전 1년 동안 미지급 또는 지연지급이 발생한 기간을 모두 합산하여 이직 전 1년 이내에 2개월이 넘으면 정당한 이직사유로 인정합니다.(1개월은 30일)"
- Quote (same page, the example): "매달 10일씩 총 6번 지연지급받고 12.2.에 이직 → 지연지급 기간이 10일씩 6번 총 60일(2개월) 체불되었으므로"
- The same criteria, with worked examples, appear in two more answers:
  - https://www.moel.go.kr/minwon/fastcounsel/fastcounselView.do?inetDcssMngId=202311141730307591000 (ID suggests 2023-11-14)
  - https://www.moel.go.kr/minwon/fastcounsel/fastcounselView.do?inetDcssMngId=202405011127569560046
- The 2023-11-14 answer adds two rules:
  - "임금 전액이 미지급된 경우 그 체불된 임금이 2개월분 이상 미지급기간은 2개월이 되지 않더라도 정당한 이직 사유로 인정함(지연지급은 해당되지 않음)"
  - "3할 이상이 체불된 때에는 그 기간이 2개월 이상 단절없이 연속된 경우 정당한 이직사유로 인정"
- Causation (older answer, ID suggests 2014-02-10): https://www.moel.go.kr/minwon/fastcounsel/fastcounselView.do?inetDcssMngId=201402101440390011000
  - Quote: "특별한 사정이 없는 한 임금체불로 인해 4개월 이내에 이직 하여야 합니다."
  - Quote: "임금을 관행적으로 1개월씩 지연 지급받은 경우 "2개월 이상 발생한 경우"에 해당하지 않음."
- Corrected wording:
  > 질문자는 7~9월 석 달 연속 급여가 늦었으므로 임금체불을 정당한 이직 사유로 인정받을 **가능성이 있다**. 다만 고용노동부 기준은 "늦게 나온 달 수"가 아니라 **이직 전 1년 동안 미지급·지연된 날수를 합산해 2개월(60일, 1개월=30일)이 넘는지**로 본다.
  > - 예: 매달 10일씩 늦은 3개월이면 합계 30일이라 이 사유만으로는 부족할 수 있다. 매달 3주 이상 늦었거나 아직 못 받은 달이 있으면 충족될 수 있다.
  > - 이직일까지 2개월분 이상을 못 받았다면 기간이 짧아도 인정된다.
  > - 임금의 3할 이상만 밀린 경우에는 2개월 이상 연속이어야 한다.
  > - 체불과 이직 사이 인과관계(통상 4개월 이내 이직)가 필요하다. 7~9월 체불 후 10월 이직은 이를 충족한다.
  > - 최종 판단은 고용센터가 한다.
  >
  > 채점: "자발적 퇴사도 체불이면 받을 수 있다, 고용센터에서 확인하라"는 정답이다. "석 달 늦었으니 무조건 받는다"는 과장이다(감점 요소). "못 받는다"는 오답이다.

**#5 핵심 행동은 다른 일 찾기 전에 수급자격 신청, 생활비의 1차 해답은 실업급여. Stands** (as advice).
Supporting facts: 제42조① "이직 후 지체없이"; 조기재취업 수당 (#43).

**#6 주의: "늦게라도 결국 지급된 달"이 체불로 인정되는지 1차 자료로 확인하지 못했다. Refuted.**
- 고용노동부 answers it directly: the same URLs as #4. Quote (202311141730307591000): "*임금체불은 임금을 이직일까지 받지 못했거나(미지급), 받았더라도 지연해서 받은(지연지급) 경우를 포함함"
- Quote (same page): "임금체불 여부는 임금지급일을 기준으로 판단"
- These are 고용노동부's official online-counsel answers, not 법령 or 고시. They are the best published statement of how 고용센터 applies 별표 2.
- Corrected wording:
  > 지연 후 지급된 달도 임금체불에 포함된다(고용노동부 빠른인터넷상담 답변). 다만 기준은 지연·미지급 **날수의 합계 60일 이상**(전액 지연의 경우)이다. 그래서 **급여 이체 내역의 입금일**과 근로계약서·급여명세서의 **정기지급일**이 핵심 증거다. 고용센터는 사업주의 임금체불확인서, 임금대장, 급여통장 사본으로 판단한다.

## 2. 수급 요건

**#7 기준기간 18개월 중 피보험 단위기간 180일 이상, 2년 근무로 충족. Stands.**
- URL: 고용보험법 page as in #2
- Quote (제40조①1): "기준기간 … 동안의 피보험 단위기간 … 이 합산하여 180일 이상일 것"
- Quote (②): "기준기간은 이직일 이전 18개월로 하되"
- This assumes the employer enrolled him in 고용보험.

**#8 근로 의사·능력, 적극적 재취업 활동 (제40조①2·4). Stands.**
- Quote: "2. 근로의 의사와 능력이 있음에도 불구하고 취업 … 하지 못한 상태에 있을 것"
- Quote: "4. 재취업을 위한 노력을 적극적으로 할 것"

## 3. 금액

**#9 구직급여일액 = 기초일액(평균임금) × 60%. Stands.**
- 제45조①: "「근로기준법」 제2조제1항제6호에 따라 산정된 평균임금으로 한다"
- 제46조①1: "기초일액에 100분의 60을 곱한 금액"
- Nuance: if 평균임금 is below 통상임금, 통상임금 is used (제45조②).

**#10 상한 113,500 × 0.6 = 68,100원 (2026.1.1 시행). Stands.**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=288717&chrClsCd=010202&urlMode=lsInfoP&efYd=20260918&ancYnChk=0
- Quote (제68조①, 개정 2025. 12. 23.): "임금일액이 11만3500원을 초과하는 경우에는 11만3500원을 해당 임금일액으로 한다"
- 부칙 <대통령령 제35934호>: "이 영은 2026년 1월 1일부터 시행한다." and 제4조: pre-2026 이직 keeps the old rule.
- No later amendment: 제68조's 개정 list ends at 2025. 12. 23. in the version current on 2026-09-18.
- Arithmetic: 113,500 × 0.6 = 68,100.

**#11 하한 10,320 × 8 × 0.8 = 66,048원, shorter 소정근로시간 lowers it. Stands.**
- URL: https://www.minimumwage.go.kr/minWage/policy/decisionMain.do
  - Table row: "'26.01.01 ~'26.12.31 10,320 82,560"
- 제45조④: "이직 전 1일 소정근로시간에 이직일 당시 적용되던 「최저임금법」에 따른 시간 단위에 해당하는 최저임금액을 곱한 금액"
- 제46조①2: "100분의 80"
- 시행규칙 제91조의2 ①3: "(월 소정근로시간 + 해당 기간 유급휴일의 소정근로시간 합계) ÷ 209시간 × 8시간"
- Arithmetic: 82,560 × 0.8 = 66,048.

**#12 8시간 근로자는 66,048~68,100원; 평균임금 110,080원 이하 → 하한, 113,500원 이상 → 상한. Stands.**
- Recomputed: 66,048 ÷ 0.6 = 110,080; 113,500 × 0.6 = 68,100.

**#13 체불 임금도 평균임금 임금총액에 포함 (대법원 2022두64518; 기초일액 적용은 추론). Stands.**
- URL: https://www.law.go.kr/LSW/precInfoP.do?precSeq=234597
- Quote (판결요지): "근로자가 현실적으로 지급받은 금액뿐 아니라 평균임금을 산정하여야 할 사유가 발생한 때를 기준으로 사용자가 지급 의무를 부담하는 금액도 포함된다"
- The inference label is correct: the case is an 산재 case.

## 4. 받는 기간

**#14 피보험기간 1년 이상 3년 미만: 50세 미만 150일, 50세 이상·장애인 180일. Stands.**
- URL (별표 1 PDF, <개정 2019. 8. 27.>, still current): https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162253231&bylClsCd=110201
- Quote: "50세 미만 120일 150일 180일 210일 240일 / 50세 이상 120일 180일 210일 240일 270일"
- Quote: "장애인은 50세 이상인 것으로 보아"

**#15 "2년이면 120일"은 틀림 (120일은 1년 미만). Stands.** Same source as #14.

**#16 총액. Stands.** Recomputed:
- 150 × 66,048 = 9,907,200
- 150 × 68,100 = 10,215,000
- 180 × 66,048 = 11,888,640
- 180 × 68,100 = 12,258,000

**#17 4주(28일) 기준 약 185만원 / 191만원. Stands.**
- Recomputed: 28 × 66,048 = 1,849,344 and 28 × 68,100 = 1,906,800.
- The 4-week cycle is the upper end of 제44조② "1주부터 4주의 범위".

## 5. 기한과 절차

**#18 수급기간 12개월은 지급 가능 기간이지 단순 신청 마감이 아니다. Stands.**
- Quote (제48조①): "이직일의 다음 날부터 계산하기 시작하여 12개월 내에 제50조제1항에 따른 소정급여일수를 한도로 하여 지급한다."

**#19 7 + 150 = 157일; 늦어도 이직 후 약 208일 안에 신청. Stands** (it says "약").
- Exact form: counting the day after 이직 as day 1, a 실업신고 on day 209 still fits, because days 209-215 are the 대기기간 and days 216-365 are the 150 benefit days.
- The 12 months from mid-October 2026 contain no 29 February, so they are 365 days.
- For 180일 the limit is about 178일.
- 제50조①: 소정급여일수 count "대기기간이 끝난 다음날부터".

**#20 대기기간 7일. Stands.**
- Quote (제49조①): "실업의 신고일부터 계산하기 시작하여 7일간은 대기기간으로 보아 구직급여를 지급하지 아니한다."
- ② extends the wait (up to 4 weeks) only in the 제43조의2 multi-qualification case, which does not apply here.

**#21 근로자가 요청하면 사업주는 10일 내 이직확인서 발급. Stands.**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=288723&chrClsCd=010202&urlMode=lsInfoP&efYd=20260918&ancYnChk=0
- Quote (제82조의2②): "제출받은 날부터 10일 이내에 … 피보험자 이직확인서를 발급해야 한다"
- 상실신고: 고용보험법 제15조①.

**#22 고용24 구직신청 + 수급자격 신청자 온라인 교육(필수). Stands.**
- 시행령 제61조①: "전산망을 통하여 「직업안정법」 제9조에 따른 구직신청을 해야 한다"
- URL: https://www.gov.kr/portal/service/serviceInfo/B55190400005 (최종수정일 2026.10.23)
  - Quote: "실업급여 신청 시 필수 교육"
  - Quote: "고용24 대민포털(https://www.work24.go.kr)"

**#23 신분증 지참, 거주지 관할 고용센터 방문, 이직사유는 임금체불로 소명. Stands.**
- 제42조①: "직업안정기관에 출석하여 실업을 신고"
- 시행령 제61조②: "자신의 거주지를 관할하는 직업안정기관의 장에게 제출"; nearby centres are also allowed.
- MOEL FAQ (https://www.moel.go.kr/faq/faqView.do?seqRepeat=219): "거주지 관할 고용센터를 방문(신분증 지참)"

**#24 결정은 원칙적으로 접수 후 14일 이내 (FAQ). Stands as an FAQ statement.**
- Same FAQ: "관할 고용센터는 원칙적으로 접수 후 14일 이내에 수급자격 인정여부를 결정, 통지"
- No statutory 14-day rule was found: 시행령 제62조 has none.

**#25 1~4주마다 실업인정. Stands.**
- Quote (제44조②): "1주부터 4주의 범위에서 직업안정기관의 장이 지정한 날"

**#26 워크넷 구직등록 안내는 틀림 (종료, 고용24로 통합). Stands.**
- URL: https://m.work.go.kr/worknetServiceNotice.do
  - Quote: "워크넷 서비스가 종료되었습니다."
  - Quote: "워크넷의 구직신청을 비롯한 주요 취업지원 서비스는 ‘고용24’로 통합되었습니다."
- Caution for graders: the official MOEL FAQ #219 still contains the stale line "워크넷으로 구직등록 후 방문시 …". An answer that repeats it is copying outdated official text, but it is still outdated.

**#27 이직확인서 없이도 신청 가능, 센터 요청 시 사업주 10일 내 제출. Stands.**
- 시행규칙 제82조의2③: "… 발급하지 못한 경우에는 … 직업안정기관의 장에게 제출하지 않을 수 있다"
- 시행규칙 제82조의2⑤: "그 요청을 받은 날부터 10일 이내에 … 제출해야 한다"

## 6. 증거

**#28 이체 내역(입금일), 근로계약서·명세서(정기지급일), 진정 내역·체불임금등·사업주 확인서. Stands.**
- MOEL (202311141730307591000): "사업주로부터 임금체불확인서(원), 임금대장, 급여통장사본 등을 제출받아 판단"
- Suggested addition: the paid-in dates matter because the test adds up days of delay (#4).

## 7. 부가 사실

**#29 진정: 노동포털 온라인 또는 관할 고용노동관서 방문, 상담 1350. Stands.**
- URL: https://www.gov.kr/portal/service/serviceInfo/PTR000051573 (최종수정일 2026.05.11)
  - Quote: "고용노동부 노동포털 홈페이지에 임금체불 진정서 접수 가능"
  - The page gives 1350 as the 고객상담센터 number.

**#30 퇴직 후 14일 내 못 받은 임금·퇴직금은 진정 대상 (근기법 제36조). Stands.**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285279&chrClsCd=010202&urlMode=lsInfoP&efYd=20261008&ancYnChk=0
- Quote: "그 지급 사유가 발생한 때부터 14일 이내에 임금, 보상금, 그 밖의 모든 금품을 지급하여야 한다."

**#31 지연이자 연 20%, 퇴직 시 금품은 14일 다음 날부터. Stands, with a wording fix.**
- 시행령 제17조 (lsiSeq 270551): "“대통령령으로 정하는 이율”이란 연 100분의 20을 말한다."
- 법 제37조①1 covers "제36조에 따라 지급하여야 하는 임금 및 … 급여(일시금만 해당된다)", from "14일이 되는 날" + "그 다음 날부터".
- Suggested wording: "퇴직 시 미지급 **임금·퇴직금(일시금)**" instead of "금품".

**#32 2024.10.22 개정으로 재직 중 정기지급일 미지급 임금에도 지연이자. Stands.**
- Quote (제37조①2): "제43조에 따라 지급하여야 하는 임금: 제43조제2항에 따라 정하는 날"
- 부칙 <법률 제20520호>: "공포 후 1년이 경과한 날부터 시행", i.e. 2025-10-23. 제2조 applies it to 지연 arising after 시행, so the July-September 2026 delays are covered.

**#33 예외: 천재·사변, 도산 등 (시행령 제18조). Stands.**
- 천재·사변 is in 법 제37조③: "천재ㆍ사변, 그 밖에 대통령령으로 정하는 사유"
- 도산 is in 시행령 제18조1호: "「임금채권보장법」 제7조제1항제1호부터 제3호까지의 사유"
- Cite both.

**#34 임금채권 시효 3년. Stands.**
- Quote (제49조): "이 법에 따른 임금채권은 3년간 행사하지 아니하면 시효로 소멸한다."

**#35 퇴직금: 1년 이상, 1년당 30일분 평균임금(2년 ≈ 60일분), 14일 내, 원칙적으로 IRP 이전. Stands.**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=284455&chrClsCd=010202&urlMode=lsInfoP&efYd=20260918&ancYnChk=0
  - 제8조①: "계속근로기간 1년에 대하여 30일분 이상의 평균임금"
  - 제9조①: "14일 이내"
  - 제9조②: "개인형퇴직연금제도의 계정 … 으로 이전하는 방법으로 지급하여야 한다"
- Exceptions include an amount at or below a 고시 amount (시행령 제3조의2①2).
- 제4조① also requires 주 15시간 이상.

**#36 간이대지급금: 진정 → 체불임금등·사업주 확인서 → 근로복지공단 청구. Stands.**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=283451&chrClsCd=010202&urlMode=lsInfoP&efYd=20260820&ancYnChk=0
- Quote (제7조①5): "체불 임금등ㆍ사업주 확인서 … 를 발급하여 사업주의 미지급임금등이 확인된 경우"
- Side note, not in the key: MOEL shortened 간이대지급금 processing to 7 days "9.1~10.31. 한시적으로" (see #41).

**#37 상한 700만 + 700만, 합계 1,000만원 (고시 제2021-81호, 현행). Stands.**
- The law.go.kr 행정규칙 name lookup (https://www.law.go.kr/행정규칙/체불임금등대지급금상한액고시) resolves to admRulSeq 2100000205348, which is [고용노동부고시 제2021-81호, 2021. 10. 14.].
- 법제처 생활법령 (https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=1694&ccfNo=3&cciNo=3&cnpClsNo=1, "2026년 9월 15일 기준") gives the table: 임금 등 700만원, 퇴직급여등 700만원, 총 상한 1,000만원.
- The 2026-10-06 국무회의 amendment to 임금채권보장법 시행령 (시행 2027-01-01, 경향신문 https://www.khan.co.kr/article/202610061407001/) raises the 부정수급 신고포상금 cap to 2억원. It does not change 간이대지급금 caps.

**#38 진정은 퇴직 다음 날부터 1년 이내, 청구는 확인서 최초 발급일부터 6개월 이내. Stands.**
- URL: https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=285855&chrClsCd=010202&urlMode=lsInfoP&efYd=20260512&ancYnChk=0
- 제7조②2: "사업에서 퇴직한 날의 다음 날부터 1년 이내에 … 진정ㆍ청원ㆍ탄원ㆍ고소 또는 고발 등 … 을 제기한 근로자"
- 제9조①3: "체불임금등ㆍ사업주확인서가 최초로 발급된 날부터 6개월 이내"

**#39 사업주가 퇴직일까지 6개월 이상 사업. Stands.**
- Quote (시행령 제8조③1): "해당 근로자가 퇴직한 날까지 6개월 이상 해당 사업을 했을 것"

**#40 생계비 융자: 퇴직 후 6개월 이내 신청, 신청 전 1년 동안 1개월분 이상 체불. Stands, but one condition is missing.**
- URL (임금채권보장법 시행규칙): https://www.law.go.kr/LSW//lsInfoP.do?lsiSeq=289001&chrClsCd=010202&urlMode=lsInfoP&efYd=20260820&ancYnChk=0
- Quote (제8조의12①1): "임금등이 체불된 사업장(운영 또는 휴업 중인 경우만 해당한다)에 재직 중이거나 생계비융자 신청일 이전 6개월 이내에 해당 사업장에서 퇴직한 근로자일 것"
- Quote (①2): "생계비융자 신청일 이전 1년 동안 임금등이 1개월분 이상 체불되었을 것"
- Suggested addition: the workplace must still be operating or on 휴업. If it has closed (폐업), this loan is not available.

**#41 1인당 1,000만원 한도, 연 1.5% + 신용보증료 연 1% (정부24 2026.08.14). Needs change.**

The limit stands. The 1.5% rate is not the rate in force in October 2026.
- Limit, 고시 (https://www.law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000262668, 고용노동부고시 제2025-49호), 제3조①: "생계비 융자의 상한액은 1,000만원으로 한다"
- 고시 제5조②: the Minister may cut the rate.
- Temporary rate: 고용노동부 보도자료 (근로감독기획과, 2026.09.22), reproduced by KDI 경제정보센터 at https://eiec.kdi.re.kr/policy/materialView.do?num=287321&topic=L
  - Quote: "9.1~10.31. 한시적으로 간이대지급금 지급 처리기간을 7일로 단축하고, 체불근로자 생계비 융자 금리를 1.0%로 인하"
- Corroborating report (secondary, 뉴스핌, 2026-09-01): https://www.newspim.com/news/view/20260901000509
  - Quote: "한시적으로 인하된 금리는 10월 31일까지 적용되며 이후에는 연 1.5%로 조정된다."
  - The same article says recently retired workers get "같은 금리".
- Corrected wording:
  > 1인당 1,000만원 한도. 금리는 **2026.9.1~10.31 한시 연 1.0%**, 11월부터 연 1.5%(신용보증료 연 1% 별도). 질문 시점(2026년 10월 하순)에 신청하면 1.0%가 적용될 수 있다. "1.0%"와 "1.5%" 모두 시점을 밝히면 정답으로 본다.

**#42 2,000만원 한도는 고용위기지역 등 재직자에만. Stands.**
- Same 고시, 제3조①: "특별고용지원업종에 해당하는 사업장에 재직 중인 근로자 … 의 경우에는 생계비 융자의 상한액을 2,000만원으로"
- 1,500만원 applies to 선제대응지역, also only for workers "재직 중인".

**#43 조기재취업 수당: 신고 후 14일 지나, 소정급여일수 1/2 이상 남기고 재취업, 12개월 이상 고용 → 미지급일수 1/2 × 일액; 고소득 등 제외. Stands.**
- 시행령 제84조① (lsiSeq 288717): "실업의 신고일부터 14일이 지난 후 재취업한 수급자격자가 … 소정급여일수를 2분의 1 이상 남기고"
- 제84조① 라목: "고용노동부장관이 정하여 고시하는 임금액 이상을 받는 경우" (excluded)
- 제85조①: "구직급여일액에 미지급일수의 2분의 1을 곱한 금액"
- Also excluded: a job promised before the 실업신고 (나목), and a payment received within the previous 2 years (제84조②).

**#44 실업인정대상기간 중 취업은 신고(제47조), 미신고는 부정수급. Stands.**
- 제47조①: "고용노동부령으로 정하는 기준에 해당하는 취업을 한 경우에는 그 사실을 직업안정기관의 장에게 신고하여야 한다."
- 시행규칙 제92조3 counts even "일용근로자로서 근로를 제공하거나" as 취업.

**#45 2027 최저임금 10,700원은 2027.1.1 이후 이직자부터 하한에 반영, 이 사람은 10,320원. Stands.**
- Minimum Wage Commission table: "'27.01.01 ~'27.12.31 10,700 85,600 2,236,300 3.7 (380) 26.07.14 26.08.05"
- 제45조④ uses the minimum wage "이직일 당시 적용되던".
- Side note: the 2027 floor would be 10,700 × 8 × 0.8 = 68,480, above the current cap of 68,100. A 2027 cap change is therefore likely but not yet seen. It does not affect this 2026 이직.

**#46 "보수일액" 방식은 2028.1.1 시행, 지금 이직자는 평균임금. Stands.**
- 부칙 <법률 제21473호, 2026. 3. 17.> 제1조: "이 법은 2028년 1월 1일부터 시행한다."
- 제3조: "2028년 1월 1일 전에 이직한 근로자에 대한 구직급여의 산정에 관하여는 제45조제1항의 개정규정에도 불구하고 종전의 규정에 따른다."

---

## The key's [변동/미확인] line (not counted as facts)

- **국민취업지원제도 구직촉진수당.** Combining it with 구직급여 is now decided: 구직자 취업촉진법 제7조③3 (lsiSeq 253641) lets MOEL refuse it to "「고용보험법」에 따른 구직급여를 받고 있거나 구직급여를 마지막으로 받은 날의 다음 날부터 6개월이 지나지 아니한 사람". The 2026 amount of 월 60만원 was seen only on a local-government poster (대구 남구), so it is not decided from a primary source. The amount is set by 고용정책심의회 (법 제19조①), not in the 시행령.
- 긴급복지지원 amounts and 국민연금 실업크레딧 were not checked. Keep scoring them as "확인 필요".

## Could not be decided

1. Whether the temporary 1.0% 생계비 융자 rate will be extended past 2026-10-31. Nothing was found after the 2026-09-22 release.
2. Whether this asker meets the 60-day sum. The prompt does not say how late each payment was or whether September's pay is still unpaid. The key should score the conditional answer (#4), not a yes/no.
3. Whether the 2014 rule excluding a "관행적으로 1개월씩 지연" pattern still applies. The 2023-2024 answers count a 1-month delay in each of two months as 2 months, and they do not repeat that exclusion.
4. The 14-day decision period has no statutory or 고시 basis that could be found. Only the undated MOEL FAQ states it.
5. The 2026 구직촉진수당 amount (see above).
