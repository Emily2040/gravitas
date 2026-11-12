# ko-jeonse-protection: adversarial check of "Facts for the key"

Checked 2026-10-24 (task date 2026-10-23). Read only `sources/ko-jeonse-protection.md` and `prompts/ko-jeonse-protection.txt` on disk.
Method: re-opened every cited source; searched law.go.kr with "예정법령포함" switched on for each statute (promulgated-but-not-yet-in-force versions); searched for 2025-2026 amendments, policy announcements and updated figures; recomputed every number.
Quotes are verbatim and kept to two lines or less.

Numbering: the "Facts for the key" bullets are numbered A1-A5 (전제), B1-B5 (수치와 계산), C1-C5 (이사 당일 순서), D1-D10 (덧붙기 쉬운 주장). That makes 25 facts.

## Result

- **Stands: 19.** A1, A2, A3, A5, B1, B2, B4, B5, C1, C3, C4, C5, D3, D4, D5, D6, D7, D8, D9. A3 and D4 can drop their "not verified" caveats, because this check verified them.
- **Refuted / needs change: 4.**
  - D1: the amendment push is real and dated. The current rule itself stands.
  - D2: the key names only one online route to 확정일자; there is a second.
  - A4: "사실상 유일한 순위 보호 장치" is overstated.
  - B3: the 2023-02-21 transitional rule is worded too loosely.
- **Could not be decided: 2.**
  - C2: no official source says the balance must go to an account in the registered owner's name. The rest of C2 stands.
  - D10: 주민센터 opening hours.
  - The wording of the 표준계약서 clause in D9 is also still undecided. D9 itself only claims that the clause exists, and that stands.

## Statute status checked (all on law.go.kr, 예정법령포함 on)

| Law | In force now | Pending version? |
|---|---|---|
| 주택임대차보호법 | [시행 2026. 1. 2.] 법률 제21065호 | none listed |
| 주택임대차보호법 시행령 | [시행 2026. 7. 1.] 대통령령 제36423호 | none listed. Amounts last changed 2023. 2. 21. |
| 확정일자 규칙 (법무부령 / 대법원규칙) | 2022. 2. 7. / 2021. 6. 10. | none listed |
| 등기사항증명서 등 수수료규칙 | [시행 2025. 8. 1.] | none listed |
| 부동산 거래신고 등에 관한 법률 | [시행 2024. 5. 17.] | 법률 제21900호 (시행 2026. 12. 9.) and 제21815호 (시행 2026. 12. 17. / 2027. 6. 17.). Neither touches 제6조의2-제6조의5 or 제28조⑤3 (read in the 2026. 12. 9. version). |
| 부동산거래신고법 시행령 | [시행 2026. 10. 1.] | none listed |
| 부동산거래신고법 시행규칙 | [시행 2026. 2. 10.] | none listed |
| 주민등록법 | [시행 2025. 7. 22.] | none listed. 시행령 제36282호 takes effect 2026. 10. 29., but its 개정이유 covers only 세대원 등재순위, foreign names and fingerprints, not 제16조 or 제40조. |
| 국세징수법 / 시행령 | [시행 2026. 10. 2.] / [시행 2026. 10. 1.] | none listed |
| 지방세징수법 / 시행령 | [시행 2026. 10. 2.] / [시행 2026. 2. 5.] | none listed |

---

## A. 전제와 그것이 틀린 이유

### A1. 부동산 말("전입신고만 하면 … 신경 안 써도 된다")은 틀림 — **stands**
This follows from A2 to A5 below.

### A2. 전입신고+입주로 생기는 것은 대항력(제3조①). 집주인이 바뀌어도 새 집주인에게 요구 가능 — **stands**
- URL: https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=276291&chrClsCd=010202&urlMode=lsInfoP&efYd=20260102&ancYnChk=0
- 제3조①: "임차인(賃借人)이 주택의 인도(引渡)와 주민등록을 마친 때에는 그 다음 날부터 제삼자에 대하여 효력이 생긴다."
- 제3조④: "임차주택의 양수인(讓受人)(그 밖에 임대할 권리를 승계한 자를 포함한다)은 임대인(賃貸人)의 지위를 승계한 것으로 본다."

### A3. 우선변제권 = 대항요건 + 확정일자(제3조의2②). 확정일자가 없으면 배당 순위 보호도 없음 — **stands** (the caveat can now be removed)
- 제3조의2② (same URL): "…대항요건(對抗要件)과 임대차계약증서…상의 확정일자(確定日字)를 갖춘 임차인은 … 우선하여 보증금을 변제(辨濟)받을 권리가 있다."
- The key says the rule "앞선 근저당이 있으면 대항 불가" was not checked against a source. This check verified it: 대법원 2025. 4. 15. 선고 2024다326398, https://www.law.go.kr/LSW/precInfoP.do?mode=0&precSeq=605771
  - 판결요지[2]: "경매로 인하여 소멸하는 저당권보다 뒤에 등기되었거나 대항력을 갖춘 임차권은 선순위 저당권과 함께 소멸하는 이상 … 임차인은 매수인에 대하여 임차권의 효력을 주장할 수 없다."
- Suggested wording in place of the caveat: "임차인보다 먼저 등기된 근저당이 경매로 소멸하면 그보다 늦은 임차권도 함께 소멸해 매수인에게 대항할 수 없습니다(대법원 2024다326398)."

### A4. 2억 원은 소액임차인 기준 초과 → 최우선변제 없음; "확정일자가 사실상 유일한 순위 보호 장치" — **needs change (minor)**
- The 최우선변제 part stands (see D7).
- "사실상 유일" is overstated. A 민법 제621조 임대차등기 also gives 대항력 and 우선변제권, but only with the landlord's cooperation. Same URL as A2:
  - 제3조의4①: "「민법」 제621조에 따른 주택임대차등기의 효력에 관하여는 제3조의3제5항 및 제6항을 준용한다."
  - 제3조의4②: "임차인이 대항력이나 우선변제권을 갖추고 「민법」 제621조제1항에 따라 임대인의 협력을 얻어 임대차등기를 신청하는 경우…"
- 전세권설정등기 is another registered alternative, but its article was not opened in this check. HUG requires an existing 전세권 to be cancelled or transferred before it issues a 반환보증 (HUG page, see D8): "전세권이 설정된 경우 말소 또는 공사로 전세권을 이전할 것".
- Corrected wording: "2억 원은 서울 소액임차인 기준(1억 6,500만 원 이하)을 넘어 최우선변제는 해당되지 않습니다. 임대인 협조 없이 임차인 혼자 갖출 수 있는 순위 보호 장치는 사실상 확정일자뿐입니다(민법 제621조 임대차등기도 순위를 주지만 임대인의 협력이 필요합니다)."

### A5. "시간 날 때 전입신고"도 틀림: 다음 날 0시, 같은 날 근저당에 밀림(97다22393), 14일·과태료 5만 원 이하 — **stands**
- 대법원 1997. 12. 12. 선고 97다22393, https://www.law.go.kr/LSW/precInfoP.do?precSeq=196635
  - Holding: "확정일자를 입주 및 주민등록일과 같은 날 또는 그 이전에 갖춘 경우에는 우선변제적 효력은 대항력과 마찬가지로 인도와 주민등록을 마친 다음날을 기준으로 발생한다."
  - Facts: on 1994. 9. 16. the tenant moved in, filed 전입신고 and got 확정일자. The bank registered its 근저당 the same day, and the bank ranked first.
- 14일 and 5만원: see D3.

## B. 정확한 수치와 계산

### B1. 금요일 = 2026-10-23. 근무시간에 입주+전입+확정일자 → 대항력·우선변제권 모두 2026-10-24(토) 0시 — **stands**
- Recomputed: 2026-01-01 is a Thursday; day-of-year 296 gives offset 295; 295 mod 7 = 1, so 2026-10-23 is a Friday.
- 대법원 1999. 5. 25. 선고 99다9981, https://www.law.go.kr/LSW/precInfoP.do?precSeq=195095
  - "그 '익일부터' 제3자에 대하여 효력이 생긴다고 함은 익일 오전 영시부터…"
- 97다22393 (A5) gives the same date for 우선변제 when 확정일자 is obtained on the same day.

### B2. 인터넷등기소 확정일자: 금 18시 이후 → 2026-10-26(월). 16시 이후도 다음 근무일 가능. 확정일자는 이사 전에도 가능 — **stands**
- 대법원규칙 (current, [시행 2021. 6. 10.]), https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=232367&chrClsCd=010202&urlMode=lsInfoP&efYd=20210610&ancYnChk=0
  - 제8조① 단서: "다만, 평일 16시 이후에 확정일자 부여의 신청이 접수된 경우에는 다음 근무일에 이를 부여할 수 있다."
  - 제8조③: "전자확정일자 부여의 신청이 평일 18시 이후에 접수되거나, 토요일 또는 공휴일에 접수된 경우에는 다음 근무일에 확정일자를 부여한다."
- 2026-10-26 is a Monday. October 2026 public holidays are 10/3 and 10/9, so it is a working day.
- HUG, https://www.khug.or.kr/jeonse/web/s03/s030301.jsp: "확정일자는 이사 전에도 임대차 계약서만 있다면 받을 수 있어요."

### B3. 최우선변제 계산 / 5,500만·1/2 한도 / "2023-02-21 이전에 설정된 담보물권이 있으면 종전 기준" — **needs change (wording only)**
- Arithmetic checks out: 2억 − 1억 6,500만 = 3,500만 over the threshold, so 최우선변제 does not apply.
- 시행령 [시행 2026. 7. 1.], https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=287183&chrClsCd=010202&urlMode=lsInfoP&efYd=20260701&ancYnChk=0
  - 제10조①1: "서울특별시: 5천500만원"
  - 제10조②: "…주택가액의 2분의 1에 해당하는 금액까지만 우선변제권이 있다."
  - 제11조1: "서울특별시: 1억6천500만원"
- The transitional rule is relative and keyed to the 시행일 (the 공포일, 2023-02-21). It applies only against creditors who took their security before that date.
  - 부칙 제2조 (대통령령 제33254호): "이 영 시행 전에 임차주택에 대하여 담보물권을 취득한 자에 대해서는 종전의 규정에 따른다."
- Corrected wording: "2023-02-21 **전**에 그 집에 담보물권(근저당 등)을 취득한 사람에 **대해서는** 더 낮은 종전 기준이 적용됩니다."
- No 2025-2026 change to the amounts was found. A 2025 국정기획위원회 proposal would move the reference point from 담보물권 취득 to 계약 시점, but it is not in the text in force (news only, e.g. https://v.daum.net/v/20250825070216088).

### B4. 임대차 신고: 2억 > 6천만 → 대상(서울 전 자치구), 계약일(가계약금 입금일)부터 30일, 전입신고 때 계약서 제출 → 신고 의제 + 확정일자 의제 — **stands**
- 시행령 제4조의3 [시행 2026. 10. 1.], https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=290839&chrClsCd=010202&urlMode=lsInfoP&efYd=20261001&ancYnChk=0
  - "보증금이 6천만원을 초과하거나 월 차임이 30만원을 초과하는 주택 임대차 계약"
  - ② covers every "구(자치구를 말한다)".
- 법 제6조의5①③: same text in the current version and in the 2026. 12. 9. pending version (https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=289317&chrClsCd=010202&urlMode=lsInfoP&efYd=20261209&ancYnChk=0)
  - ③: "…확정일자를 부여한 것으로 본다(임대차계약서가 제출된 경우로 한정한다)."
- A rule the key does not cite: the deeming at 전입신고 itself needs the contract. 시행규칙 제6조의6 [시행 2026. 2. 10.], https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=283339&chrClsCd=010202&urlMode=lsInfoP&efYd=20260210&ancYnChk=0
  - "…전입신고를 하는 경우로서 법 제6조의5제1항에 따라 주택 임대차 계약의 신고를 한 것으로 보는 경우 주택 임대차 계약서 … 를 제출해야 한다."
- easylaw (2026-09-30 기준), https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=629&ccfNo=2&cciNo=2&cnpClsNo=5: "(가)계약금 입금일을 기준으로 30일 이내 신고해야 합니다."

### B5. 수수료: 확정일자 600원(4장 초과 시 4장마다 100원), 인터넷등기소 500원, 전입신고 무료, 등기부 인터넷 열람 700원, 인터넷·무인 발급 1,000원, 창구 1,200원 — **stands**
- 법무부령 제8조①1, https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=240291&chrClsCd=010202&urlMode=lsInfoP&efYd=20220207&ancYnChk=0
  - "확정일자 부여 수수료: 1건마다 600원(계약증서가 4장을 초과할 경우 초과 4장마다 100원 추가)"
- 대법원규칙 제13조①3 (URL in B2): "인터넷등기소를 이용하여 전자확정일자 부여의 신청 또는 정보의 제공을 요청한 경우 수수료는 각 500원으로 하고"
- 수수료규칙 [시행 2025. 8. 1.], https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=272961&chrClsCd=010202&urlMode=lsInfoP&efYd=20250801&ancYnChk=0
  - 제2조①: "1통에 대하여 20장까지는 1,200원"
  - 제2조②: "무인발급기나 인터넷에 의한 등기사항증명서의 발급수수료는 1통에 대하여 1,000원"
  - 제3조②: "인터넷을 통한 … 열람에 대한 수수료는 … 700원". Counter viewing (제3조①) is 1,200원.
- 정부24 전입신고, https://www.gov.kr/mw/AA020InfoCappView.do?HighCtgCD=&CappBizCD=13100000016 (최근 내용 변경일 2025-12-09): "수수료 없음"
- Fee exemptions exist for 기초생활수급자 and others when applying in person (법무부령 제8조③; 대법원규칙 제13조②). These do not apply to 인터넷등기소 applications.

## C. 이사 당일 순서

### C1. 잔금 전에 등기부 열람, 달라졌으면 잔금 중단 — **stands** (official guidance, not a statute)
- HUG s030301 (URL in B2): "내가 전입신고를 하고 대항력을 갖게 되기 전까지는 등기부등본을 통해 권리변동상황이 발생하는지 살펴봐야 해요."

### C2. 잔금은 등기부상 소유자 명의 계좌로, 열쇠 받아 실제 입주 — **could not be decided** for the account part
- The 점유 (moving in) part stands: 인도 is an element of 제3조①.
- No official page says the balance must go to an account in the registered owner's name. Checked: HUG s030202, s030301 and s030303; MOLIT 2025-09-18 체크리스트 press release (https://www.korea.kr/briefing/pressReleaseView.do?newsId=156713334), whose checklist is in an attachment that was not opened.
- HUG s030202 only says the person in front of you, the contract signatory and the registered owner must be the same: "내 눈앞에 있는 사람과, 계약서에 도장 찍는 임대인과 등기부등본에 적힌 주택의 소유자가 모두 동일 인물이 맞는지 확인해야 해요"
- Keep the account step as advice, not as a cited rule.

### C3. 같은 날 근무시간 안에 주택 소재지 관할 주민센터에서 전입신고+확정일자(계약서 원본+신분증), 계약서 제출로 임대차 신고도 처리 — **stands**
- 제3조의6① (URL in A2): "확정일자는 주택 소재지의 읍ㆍ면사무소, 동 주민센터 … 등기소 또는 「공증인법」에 따른 공증인 … 이 부여한다."
- 주민등록법 제16조①: the 전입신고 goes to "신거주지의 시장ㆍ군수 또는 구청장". See D3 for the URL.
- 시행규칙 제6조의6 (B4): the contract must be submitted for the 신고 to be deemed.

### C4. 다음 날(다음 근무일) 등기부 재열람 — **stands** (advice; consistent with HUG s030301 and 97다22393)

### C5. 보증금 반환 때까지 거주·주민등록 유지, HUG 반환보증 검토(전입+확정일자가 조건) — **stands**
- easylaw (95다44597) as cited. Stronger and newer authority: 2024다326398 판결요지[1] (URL in A3):
  - "대항요건은 대항력 취득 시에만 갖추면 충분한 것이 아니라 대항력을 유지하기 위하여서도 계속 존속하고 있어야 한다."
  - The same judgment holds that a later 임차권등기 does not revive a lost 대항력 retroactively.
- HUG condition: see D8.

## D. 답변에 덧붙기 쉬운 주장과 정확한 값

### D1. 대항력: "전입신고 즉시"는 틀림, 현행 다음 날 0시, "개정 추진설은 확인되지 않음" — **needs change** (the push is confirmed; the current rule stands)
- The current rule stands. 제3조① still reads "그 다음 날부터". law.go.kr lists no promulgated or pending amendment to 주택임대차보호법 with 예정법령포함 switched on, as checked 2026-10-24.
- The push is real and dated. korea.kr 정책뉴스, 2026-03-10, 관계부처 합동 「전세사기 방지 대책」, https://www.korea.kr/news/policyNewsView.do?newsId=148960599
  - "전입신고 '다음날 0시'에 발생하던 대항력 효력을 이사를 마친 임차인의 '전입신고 처리 시' 발생하도록 개선한다."
- Bills: 김희정 의원 (reported as filed 2025-07) and 이종배 의원 (2026-04-16), both per news, e.g. https://www.heraldk.com/article/2026031523550133769 and https://m.news.nate.com/view/20260416n29453. No report of passage was found.
- Corrected wording: "대항력 발생시점: '전입신고 즉시'는 현행법상 틀림. 현행은 인도+전입신고 다음 날 0시(제3조①, 99다9981). 정부가 2026-03-10 '전입신고 처리 시' 발생으로 바꾸는 대책을 발표했고 개정안도 발의됐지만, 2026-10-24 현재 공포된 개정(시행예정 포함)은 없어 이번 이사에는 현행 규칙이 적용됨."

### D2. 확정일자 600원/500원. 정부24에서 확정일자를 받는다는 말은 틀림: 정부24는 전입신고만, 온라인 확정일자는 대법원 인터넷등기소 — **needs change** (the online route list is incomplete)
- The fees stand (B5). That 정부24 handles only 전입신고 stands (gov.kr page in B5; its process runs "즉시(근무시간 내 3시간)").
- There is a second online route. HUG s030301 (URL in B2):
  - "확정일자는 담당 행정복지센터(구 주민센터)나 등기소, 또는 대법원 인터넷 등기소를 통해 받을 수 있어요."
  - "…임대차계약을 신고하면서 임대차계약서를 제출하면 확정일자가 자동으로 부여돼요."
  - The same page links 부동산거래관리시스템 (rtms.molit.go.kr). easylaw (B4) says the 신고 can be filed there: "온라인으로도 신고 가능합니다".
  - 법 제6조의5③ ties the deemed 확정일자 to "신고의 접수를 완료한 때".
- Corrected wording: "…정부24에서 확정일자를 받는다는 말은 틀림(정부24는 전입신고만). 온라인 확정일자는 대법원 인터넷등기소(500원), 또는 부동산거래관리시스템에서 임대차 신고를 하며 계약서를 제출하는 방법(확정일자 의제)이 있음. 온라인은 접수·처리 시점에 따라 날짜가 다음 근무일로 밀릴 수 있어 금요일에는 주민센터 방문이 안전."
- Not decided: when an RTMS filing submitted after hours counts as "접수 완료" for the deemed 확정일자. No official statement was found.

### D3. 전입신고 기한 14일, 지연 과태료 5만 원 이하 — **stands**
- 주민등록법 [시행 2025. 7. 22.], found via law.go.kr search "주민등록법". The cited lsiSeq=268555 page is the same version.
  - 제16조①: "신거주지에 전입한 날부터 14일 이내에 신거주지의 시장ㆍ군수 또는 구청장에게 전입신고(轉入申告)를 하여야 한다."
  - 제40조④: "정당한 사유 없이 … 제16조제1항 … 에 따른 신고 또는 신청을 기간 내에 하지 아니한 자에게는 5만원 이하의 과태료를 부과한다."

### D4. 임대차 신고 과태료: 상한 100만 원, 국토부 2025-04-28 발표로 지연 최대 30만 원(2025-06-01 이후 계약부터), "하한 2만 원과 거짓신고 100만 원은 출처 미확인" — **stands** (now verified; drop the caveat)
- 법 제28조⑤3 (current and the 2026. 12. 9. pending version): "제6조의2 또는 제6조의3에 따른 신고를 하지 아니하거나(공동신고를 거부한 자를 포함한다) 그 신고를 거짓으로 한 자" → "100만원 이하".
- 시행령 [시행 2026. 10. 1.] 별표 3 「과태료의 부과기준」, 마목 (법 제28조제5항 관련). Read in the law.go.kr viewer reached from the 시행령 page URL in B4.
  - Late or missing filing: by delay band × 계약금액. "신고하지 않은 기간이 3개월 이하인 경우 / 계약금액이 1억원 미만인 경우 2만원". Rows run up to "2년을 초과하는 경우 또는 공동신고를 거부한 경우 / 5억원 이상 30만원".
  - "바) 거짓으로 신고한 경우 100만원".
- For this lease (2억, in the 1억 이상 3억 미만 band): 3만원 if up to 3 months late, 8만 for 3-6 months, 10만 for 6-12 months, 13만 for 1-2 years, 15만 beyond 2 years.
- MOLIT press release, https://www.molit.go.kr/USR/NEWS/m_71/dtl.jsp?lcmspage=1&id=95090898 (등록일 2025-04-28). Subtitle: "과태료 계도기간 5월 31일 종료… '6월 1일 이후' 계약부터 부과 / 지연신고 시 과태료 기준 최대 100만원에서 30만원으로 인하"
- Corrected wording: "임대차 신고 과태료: 법정 상한 100만 원 이하. 시행령 별표 3: 지연·미신고 2만~30만 원(기간·계약금액별, 이 계약은 3개월 이내 지연 시 3만 원), 거짓 신고 100만 원. 2025-06-01 이후 계약부터 부과."

### D5. 미납 국세·지방세 열람: 보증금 1천만 원 초과면 동의 없이, 임대차 기간 시작일까지만 — **stands**
- 국세징수법 제109조② [시행 2026. 10. 2.]: "…보증금이 대통령령으로 정하는 금액을 초과하는 자는 임대차 기간이 시작하는 날까지 임대인의 동의 없이도 제1항에 따른 신청을 할 수 있다."
- 시행령 제97조② [시행 2026. 10. 1.], https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=283487&chrClsCd=010202&urlMode=lsInfoP&efYd=20261001&ancYnChk=0: "“대통령령으로 정하는 금액”이란 1천만원을 말한다."
- 지방세징수법 제6조③ [시행 2026. 10. 2.]: "…보증금이 대통령령으로 정하는 금액을 초과하는 경우 임차인은 임대차기간이 시작되는 날까지 임대인의 동의 없이 제1항에 따른 열람신청을 할 수 있다."
  - The source md quoted this paragraph truncated and dropped the threshold clause.
- 지방세징수법 시행령 제8조② [시행 2026. 2. 5.], https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=283265&chrClsCd=010202&urlMode=lsInfoP&efYd=20260205&ancYnChk=0: "법 제6조제3항 전단에서 “대통령령으로 정하는 금액”이란 1천만원을 말한다."
- Extra: under 국세징수법 제109조① 후단, the 국세 열람 can be requested at any 세무서, not only the competent one. Under ② 후단 the landlord is notified.

### D6. 제3조의7은 2023-04-18 공포일부터 시행 — **stands**
- 부칙 <법률 제19356호, 2023. 4. 18.> 제1조 (URL in A2): "이 법은 공포 후 3개월이 경과한 날부터 시행한다. 다만, 제3조의7의 개정규정은 공포한 날부터 시행한다. <개정 2023. 7. 11.>"
- What the 2023-07-11 amendment (법률 제19520호) changed, per its 개정문: "부칙 제1조 본문 중 "6개월"을 "3개월"로 한다." The 제3조의7 proviso was untouched.
- 부칙 제3조: the article applies to leases signed after it took effect.

### D7. 최우선변제 서울 1억 6,500만 / 5,500만, 지역별 1억 4,500만/4,800만, 8,500만/2,800만, 7,500만/2,500만 — **stands**
- 시행령 제10조①·제11조 (URL in B3) match all four tiers.
- Not relevant to Seoul: 대통령령 제36423호 (시행 2026. 7. 1.) is titled 「전남광주통합특별시 설치를 위한 특별법 시행령」. It did not change the "광역시" wording in 제10조·제11조, and how the merged 광주 area is classed was not checked.

### D8. HUG 전세보증금반환보증 (수도권 7억 이하, 신청기한, 가입조건, 한도·140%, 2억÷1.26≈1억 5,873만, 보증료 46.8만/60.4만/73.6만) — **stands**
- https://www.khug.or.kr/hug/web/ig/dr/igdr000001.jsp (read 2026-10-24)
  - "수도권 7억원 그외 지역 5억원 이하"
  - "전세계약서 상 잔금지급일과 전입신고일 중 늦은 날로부터 전세계약기간의 1/2 경과하기 전"
  - "주택가격 x 담보인정비율(90%) – 선순위채권 등"
  - "신청하려는 주택에 거주하면서 전입신고와 확정일자를 받았을 것"
  - 연립·다세대 ①: "국토교통부장관이 공시하는 공동주택가격의 140%에 해당하는 금액"
  - 감정평가: "임차인 또는 임대인이 감정평가를 받은 경우에는 위 산정기준표에도 불구하고 주택가격 산정 시 최우선 적용". The appraisal must be no more than 6 months old.
  - Fee: "보증료 : 보증금액 * 보증료율 * 전세계약기간/365". For 1억원 초과 ~ 2억원 이하 / 기타: 70% 이하 연 0.117%, 80% 이하 연 0.151%, 80% 초과 연 0.184%.
- Recomputed:
  - 0.9 × 1.4 = 1.26; 2억 ÷ 1.26 = 158,730,159원, about 1억 5,873만. Correct.
  - 2억 × 0.117% × 2 = 468,000; × 0.151% × 2 = 604,000; × 0.184% × 2 = 736,000. Correct.
  - A 730-day lease makes the factor exactly 2; a 731-day lease adds about 0.1%.
- Additions the key leaves out, all from the same page:
  - Surcharge: "선순위채권금액이 주택가액의 50%를 초과하는 경우, 산출된 보증료의 10%를 할증".
  - Relevant for a 빌라: "건축물대장상 위반건축물로 기재되어 있지 않을 것(아파트 제외)".
  - Also required: 계약기간 1년 이상, no other household's 전입 on the 전입세대확인서, and building and land both owned by the landlord.
  - Discounts: 사회배려계층 40-60%; 전자계약 3%.
- Pending change: HUG's CEO said on 2026-10-15 (국정감사) that the ratio will be lowered stepwise to 80%, with no date set (news: https://www.kukinews.com/article/view/kuk202610150166). The product page still shows 90%. Keep the "[변경될 수 있음]" tag.

### D9. 표준계약서 담보권 설정 금지 특약: 2022년 개정 표준계약서에 신설됨, 정확한 문구는 미확인 — **stands**; the wording remains **undecided**
- https://www.moj.go.kr/bbs/moj/118/564974/artclView.do (2022.11.21): "계약체결 후 입주 전 임대인의 담보권 설정금지 특약 신설". The form itself was not opened.
- There is a later 2023 revision: https://www.moj.go.kr/bbs/moj/118/569781/artclView.do (2023.04.18). It adds a 해제 특약 for when the landlord's information is false: "임대인이 제시한 정보가 사실과 다를 경우 임차인의 계약 해제 특약 신설". The page does not say whether the 2022 담보권 clause was kept; it presumably was, but this was not verified.

### D10. 주민센터 운영시간 / 야간 업무 — **could not be decided** (not checked; varies by 동)

---

## Other findings (not in the key)
- 2026-03-10 대책: HUG 안심전세 App is to show 등기·확정일자·전입세대·체납 정보 from September 2026, with landlord consent: "올해 9월부터 임대인 동의 방식의 대국민 서비스를 제공할 예정이다." (korea.kr, same URL as D1). Whether the service launched was not checked.
- Not checked: online 정부24 전입신고 filed after hours, and whether it counts from the submission or the processing date. This was item 11 in the source md, and the key does not rely on it.
