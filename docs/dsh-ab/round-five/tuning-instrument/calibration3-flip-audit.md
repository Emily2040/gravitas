# Calibration 3 flip audit

Written 2026-10-26 by an auditing agent that wrote neither the grading rubric nor the change being tested. Rule applied:
`calibration3-audit-rule.md` (sha256 17797bf3…a512), point 2, exactly as written before calibration 3 was graded.
No dsh run, no model run. The ab5 prompts, sources, keys and keypoints folders were not opened. Nothing was modified
except this file.

## Inputs

| Input | sha256 |
|---|---|
| grades-calibration.json (calibration 1, t001-t048) | 68b2bbab…fdbb4f |
| grades-calibration3.json (calibration 3, t401-t448) | 3f81e06b…720cd7c |
| maps/calibration-idmap.json | 32cc33d5…eac1 |
| maps/calibration3-idmap.json | e2a774e0…6bae |
| lkp.json (42 limited key points) | 1884d69a…9272 |
| tuning-grader-prompt5.md as used by calibration 3 (sha of the stripped text, as the instrument records it) | 5d52cfe1…5c522e |

The answers are `W:\AgentData\logs\gravitas-dsh-ab4\raw\<case>.<arm>.<run>.txt`. The key point texts are from
`W:\AgentData\logs\gravitas-dsh-ab4\keypoints\<case>.json`.

## Method

1. Each id in both id maps was resolved to case + arm + run. All 48 answers appear in both calibrations. For every
   answer, the answer_sha256 is the same in both maps and matches the sha256 of the raw file. The case/arm/run in each
   grade item agrees with its id map.
2. For each answer, every limited key point in lkp.json was compared: 48 answers, 168 marks.
3. For every FLAT (calibration 1) to KEPT (calibration 3) flip, I read the key point, both quotes and the answer around
   the quote. I checked each quote against the answer text with markdown removed. All of them are present. The one
   exception is the calibration 3 quote for en-529-roth/gv-plain/r1 KP1, which joins a table row's label to its text with
   a colon; the row text itself is verbatim.
4. Test, applied to calibration 3's KEPT quote (its sentence or step):
   - (a) it gives the person a maximum as their deadline, or a fixed date or amount, with no shorter limit or condition in
     the same sentence or step;
   - (b) it defers or omits the specific, with no maximum, condition, window or open fact stated.
   A flip that meets either is a violation.

## Counts

| Transition (calibration 1 -> calibration 3) | Count |
|---|---|
| FLAT -> KEPT (audited below) | **26** (18 answers, 9 cases) |
| KEPT -> FLAT (reverse flips, listed below) | **4** |
| WRONG -> KEPT / WRONG -> FLAT / FLAT -> WRONG / ABSENT -> FLAT (outside this audit) | 2 / 1 / 1 / 2 |
| Unchanged (KEPT 60, FLAT 52, WRONG 8, ABSENT 12) | 132 |
| Total | 168 |

Result of the pre-declared test: **26 flips audited: 26 OK, 0 VIOLATION (a), 0 VIOLATION (b).**

## FLAT -> KEPT flips

### F01. en-529-roth / gv-grav-base / r2 / KP 1 (t046 -> t428)
- Key point: Premise correction: the whole $48,000 cannot be rolled into a Roth in one year. The SECURE 2.0 529-to-Roth rollover is capped each year at the son's Roth limit: the lesser of $7,500 for 2026 and his taxable compensation, reduced by his other IRA contributions for the year.
- Calibration 1 (FLAT): "The 529-to-Roth rollover is capped at $7,500 for 2026 and $35,000 over your son's lifetime."
- Calibration 3 (KEPT): "The $7,500 counts against his 2026 Roth IRA contribution limit. If he also contributes from his paycheck, the total cannot exceed $7,500 (or his earned income, if lower)."
- Finding: neither (a) nor (b). **OK (KEPT is right).** Step 8 gives $7,500 as a ceiling ("cannot exceed") and names both shorter limits in the same step: his earned income if lower, and his own contributions sharing the same room.

### F02. en-529-roth / gv-grav-base / r2 / KP 8 (t046 -> t428)
- Key point: Steps: confirm the son's 2026 taxable compensation and that he has been the beneficiary throughout; he opens his own Roth IRA; request a direct rollover of up to $7,500 less his other 2026 IRA contributions; repeat each year until the $35,000 lifetime cap is reached; check state tax; plan for the remaining $13,000.
- Calibration 1 (FLAT): "Specify the amount — no more than $7,500."
- Calibration 3 (KEPT): "Roll over the smallest of these three numbers: $7,500, his 2026 earned income, and the five-year-eligible amount."
- Finding: neither (a) nor (b). **OK (KEPT is right).** Step 6 sets the amount as the smallest of three limits, so $7,500 is a maximum with the shorter limits in the same step; the reduction for other IRA contributions is in step 8, and nothing in step 6 is firmer than the key.

### F03. en-529-roth / gv-plain / r1 / KP 1 (t013 -> t411)
- Key point: as F01 (annual cap = lesser of $7,500 and taxable compensation, reduced by other IRA contributions).
- Calibration 1 (FLAT): "For 2026, a 529-to-Roth rollover is capped at $7,500 for someone under 50"
- Calibration 3 (KEPT): "2026 annual limit: $7,500, or his taxable compensation if less. Reduced by any other 2026 IRA contributions he makes."
- Finding: neither (a) nor (b). **OK (KEPT is right).** The table row states the key's whole limit: $7,500, or compensation if less, reduced by other 2026 IRA contributions.

### F04. en-529-roth / gv-plain / r1 / KP 8 (t013 -> t411)
- Key point: as F02 (request a direct rollover of up to $7,500 less other 2026 IRA contributions, and so on).
- Calibration 1 (FLAT): "Request only the calculated amount—likely $7,500, not $48,000."
- Calibration 3 (KEPT): "Request only the calculated amount—likely $7,500, not $48,000." (same sentence)
- Finding: neither (a) nor (b). **OK (KEPT is right).** The amount to request is "the calculated amount", which is the smallest-of-four calculation set out earlier in the answer. $7,500 is given only as the likely result, so a condition sits in the same sentence and $7,500 is not presented as the fixed amount. This one is borderline: the condition is named by reference and not spelled out in the step (step 2 has the subtraction).

### F05. en-529-roth / gv-plain / r2 / KP 1 (t010 -> t444)
- Key point: as F01.
- Calibration 1 (FLAT): "Annual cap $7,500 (under age 50) The most you can move in 2026 is $7,500"
- Calibration 3 (KEPT): "So the honest version is: $7,500 this year (assuming he has at least $7,500 of wages)"
- Finding: neither (a) nor (b). **OK (KEPT is right).** The sentence ties $7,500 to an open fact, that he has at least $7,500 of wages, so it carries a shorter limit and is not a bare fixed amount. The reduction for other IRA contributions is missing from this sentence, so it keeps only part of the key's limit, but it does not meet the pre-declared test.

### F06. en-529-roth / gv-plain / r2 / KP 4 (t010 -> t444)
- Key point: Only 529 contributions made more than 5 years before the transfer, plus their earnings, qualify. The account opened in 2004 passes the 15-year test if the son has been the beneficiary throughout, and Roth income limits do not reduce the rollover.
- Calibration 1 (FLAT): "You opened the account in 2004, so the 15-year rule is almost certainly satisfied."
- Calibration 3 (KEPT): "Yours was opened in 2004, so 22 years — fine if it has always been for him and no beneficiary change occurred."
- Finding: neither (a) nor (b). **OK (KEPT is right).** The row ties the 15-year pass to the key's condition (always for him, no beneficiary change); it fixes no date or amount and defers nothing. See observation W6.

### F07. en-529-roth / gv-plain / r2 / KP 8 (t010 -> t444)
- Key point: as F02.
- Calibration 1 (FLAT): "The rollover cannot exceed it. If it is under $7,500, use that lower number."
- Calibration 3 (KEPT): "If he also contributes to a Roth or traditional IRA for 2026, the combined total cannot exceed $7,500 (or his compensation). The 529 rollover uses the same room."
- Finding: neither (a) nor (b). **OK (KEPT is right).** Step 9 gives the ceiling ($7,500 or his compensation) and the reduction for his other 2026 IRA contributions, which is the step-level limit in the key.

### F08. en-fsa-rollover / gv-grav-base / r1 / KP 4 (t019 -> t416)
- Key point: Neither-feature branch: if the plan has no carryover and no grace period, all $1,900 is forfeited unless spent on expenses incurred by Dec 31, 2026.
- Calibration 1 (FLAT): "If your plan has neither, all $1,900 is gone December 31."
- Calibration 3 (KEPT): "If your plan has neither, all $1,900 is gone December 31." (same sentence)
- Finding: neither (a) nor (b). **OK (KEPT is right).** The sentence carries the key's branch condition ("if your plan has neither"). In that branch, December 31 is the key's own forfeiture date, not a maximum standing in for a possibly shorter limit.

### F09. en-fsa-rollover / gv-plain / r1 / KP 3 (t043 -> t405)
- Key point: Grace period branch: the whole $1,900 can pay for expenses incurred until the plan's grace end, at most the 15th day of the third month after year end, i.e. no later than March 15, 2027; the plan may set a shorter period. Dental work done on March 16 or later is not covered by 2026 money.
- Calibration 1 (FLAT): "If the plan has a grace period, March treatment may qualify only if it is incurred by the grace-period deadline, often March 15."
- Calibration 3 (KEPT): same sentence.
- Finding: neither (a) nor (b). **OK (KEPT is right).** The deadline given is the plan's own grace-period deadline, with March 15 only as the common value ("often"). That is the key's limit, in the form the rubric's own KEPT example uses; it does not give "through March 15" as the person's deadline.

### F10. en-medicare-part-b / gv-grav-base / r1 / KP 1 (t028 -> t414)
- Key point: Corrects the premise: the asker does not have to enroll in Part B this month. Someone 65+ covered by a group health plan based on their own or a spouse's current employment has a Part B SEP: they can sign up in any month while still working and covered, or in the 8 months beginning the month after the job or the coverage ends (whichever ends first), with no late-enrollment penalty. The coworker's lifetime penalty applies only when there is no SEP.
- Calibration 1 (FLAT): "Part B gets an 8-month penalty-free window after you stop working."
- Calibration 3 (KEPT): "Based on what you've told me — still working full time, covered by your employer's active group plan, employer has ~400 employees — you can delay Part B and avoid the lifetime penalty."
- Finding: neither (a) nor (b). **OK (KEPT is right).** The sentence ties delaying Part B without penalty to the SEP condition (still working, covered by an active employer plan, 20+ employees); it names no date or window and does not defer. See observation W1: calibration 1's sentence, which is still in the answer, is shaped like (a).

### F11. ja-part-time-leave / gv-grav-base / r2 / KP 3 (t038 -> t438)
- Key point: 付与日：4月1日入社なので6か月経過後の10月1日に付与される（8割出勤が条件）。来月の行事の日は10月1日以降なので有給を使える（「まだ使えない」は誤り）。
- Calibration 1 (FLAT): "つまり、来月が10月以降なら、その休みは有給で取れます。"
- Calibration 3 (KEPT): "4月1日開始なら、8割以上出勤していれば10月1日に5日発生します。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** The sentence gives October 1 together with the 80%-attendance condition and the April 1 start. See observation W7.

### F12. ja-wallpaper-restoration / gv-plain / r1 / KP 3 (t042 -> t426)
- Key point: 契約書に「原状回復」とあるだけでは、通常損耗を借主負担とする特約は成立しない（最判平成17年12月16日：負担範囲の具体的明記、または口頭説明と借主の明確な認識・合意が必要。ガイドラインの3要件も同旨）。ただし契約書は未確認で、クロスを明記した特約がありうるので条項を確認すべき（その場合も3要件と消費者契約法10条で争える）。
- Calibration 1 (FLAT): "契約書の「原状回復」という文言は、通常損耗まで借主負担にする特約としては不十分です。"
- Calibration 3 (KEPT): "契約書の「原状回復」という文言は、通常損耗まで借主負担にする特約としては不十分です。通常損耗を借主負担とするには、その内容を具体的に説明し、借主が認識して合意したことが必要とされています（消費者契約法10条が問題になる場合もあります）。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** Numbered item 3 states the condition for a valid normal-wear clause (specific explanation, the tenant's recognition and agreement) and CCA art. 10. Calibration 1 quoted only the item's first sentence. No date or amount is involved.

### F13. ja-wallpaper-restoration / gv-plain / r2 / KP 3 (t022 -> t423)
- Key point: as F12.
- Calibration 1 (FLAT): "契約書の「原状回復」条項は、「退去時に原状回復義務を負う」ことに同意したという意味であって、通常の使用による損耗まで借主が負担することに同意したという意味ではありません。"
- Calibration 3 (KEPT): "通常損耗まで借主負担とする特約は、内容が明確で、借主が認識できるよう説明されていた場合に限り有効と解されています。説明がなかったのであれば、消費者契約法10条...や民法90条で争える余地があります。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** The bullet says such a clause is valid only if it is clear and was explained, and what follows if it was not explained (CCA art. 10, Civil Code art. 90). That is the key's condition and open fact. See observation W8.

### F14. ko-jeonse-protection / gv-grav-base / r1 / KP 2 (t009 -> t424)
- Key point: 전제 바로잡기 2: '시간 날 때 전입신고'도 틀림. 대항력은 인도와 전입신고를 모두 마친 다음 날 0시부터 생기므로 미루는 동안 설정된 근저당이 앞서고, 같은 날 전입·확정일자를 해도 같은 날 설정된 근저당에는 밀림. 이사 당일 바로 해야 함. 법정 신고 기한은 14일이며 위반 시 과태료 5만 원 이하.
- Calibration 1 (FLAT): "전입신고를 미루면 대항력도 그만큼 늦어집니다. 둘 다 이사 당일에 끝내야 해요."
- Calibration 3 (KEPT): "확정일자는 늦게 받을수록 그 날짜로 순위가 밀리고, 전입신고를 미루면 대항력도 그만큼 늦어집니다. 둘 다 이사 당일에 끝내야 해요."
- Finding: neither (a) nor (b). **OK (KEPT is right).** "Both on move-in day" is the key's own instruction (이사 당일 바로 해야 함), not a maximum given as a deadline; the statutory maximum of 14 days is longer and is not cited. The reason (delay pushes back 대항력 and priority) is stated with it. The reason sits in the preceding sentence of the same paragraph, not the same sentence, but the (a) test does not reach a statement that gives no maximum.

### F15. ko-jeonse-protection / gv-plain / r1 / KP 2 (t039 -> t417)
- Key point: as F14.
- Calibration 1 (FLAT): "대항력은 전입신고 다음 날 0시부터 생기므로, 금요일 입주라면 금요일 안에 전입신고를 마쳐야 주말 공백이 없습니다."
- Calibration 3 (KEPT): same sentence.
- Finding: neither (a) nor (b). **OK (KEPT is right).** The sentence ties "finish 전입신고 within Friday" to the next-day-0:00 rule and to the Friday move-in condition. It is the key's move-in-day instruction with its reason, not a maximum given as a deadline.

### F16. ko-jeonse-protection / gv-plain / r1 / KP 4 (t039 -> t417)
- Key point: 효력 발생 시점: 금요일(2026-10-23) 근무시간에 입주+전입신고+확정일자를 마치면 대항력과 우선변제권 모두 다음 날인 10-24(토) 0시부터 생김('다음 날 0시'로 써도 정답). '즉시'나 '당일' 효력이 아님.
- Calibration 1 (FLAT): same sentence as F15.
- Calibration 3 (KEPT): same sentence as F15.
- Finding: neither (a) nor (b). **OK (KEPT is right).** The sentence says the effect starts at 0:00 the next day, which the key accepts, conditional on a Friday move-in. It names 대항력 only and leaves out 우선변제권; that is an omission of part of the point, not a fixed date and not a deferral.

### F17. ko-jeonse-protection / gv-plain / r2 / KP 2 (t032 -> t441)
- Key point: as F14.
- Calibration 1 (FLAT): "대항력은 다음 날 0시 발생이라, 하루 늦으면 그 사이 근저당·경매가 들어올 수 있습니다."
- Calibration 3 (KEPT): ""시간 날 때"가 아니라 이사 당일 하세요. 대항력은 다음 날 0시 발생이라, 하루 늦으면 그 사이 근저당·경매가 들어올 수 있습니다."
- Finding: neither (a) nor (b). **OK (KEPT is right).** The bullet gives move-in day together with the next-day-0:00 reason and the risk of a mortgage in between. Calibration 1 quoted only the bullet's second sentence.

### F18. ko-jeonse-protection / gv-plain / r2 / KP 5 (t032 -> t441)
- Key point: 어디서 어떻게: 금요일 근무시간 안에 그 주택 소재지 주민센터를 방문해 전입신고와 확정일자를 함께 처리(계약서 원본·신분증 지참; 확정일자 수수료 방문 600원, 전입신고 무료). 인터넷등기소 확정일자(500원)는 금요일 18시 이후 신청하면 다음 근무일인 10-26(월)에 부여되므로 방문이 안전함.
- Calibration 1 (FLAT): "같은 날 주민센터 방문 — "전입신고 + 확정일자 같이 해달라"고 신청."
- Calibration 3 (KEPT): "같은 날 주민센터 방문 — "전입신고 + 확정일자 같이 해달라"고 신청. 준비물: 신분증, 임대차계약서 원본, 도장(서명), 수수료 600원."
- Finding: neither (a) nor (b). **OK (KEPT is right).** The step says to visit the 주민센터 the same day, file both together, bring the key's documents and pay the key's 600-won visit fee. It gives no maximum as a deadline and defers nothing. This one is borderline: the business-hours window is only implicit in a counter visit, and the online 18:00 cutoff is absent.

### F19. ko-severance-pay / gv-plain / r2 / KP 6 (t023 -> t443)
- Key point: 인사팀 문자는 정중하되 분명해야 한다: 퇴직일과 법정 지급기한(14일) 경과를 적고, 구체적인 지급 예정일과 퇴직금 산정 내역을 요청하며, 55세 미만이면 IRP 계좌 정보를 안내한다. 연장에 동의하는 것으로 읽힐 문구나 위협적인 문구는 넣지 않는다.
- Calibration 1 (FLAT): "IRP 계좌 정보가 필요하시면 바로 안내드리겠습니다."
- Calibration 3 (KEPT): "회사 기준 계산서와 지급 예정일, 지급 방법(IRP 계좌 이전 등)을 함께 회신해 주시면 감사하겠습니다. IRP 계좌 정보가 필요하시면 바로 안내드리겠습니다."
- Finding: neither (a) nor (b). **OK (KEPT is right).** The drafted text asks for the calculation, the payment date and the payment method (IRP transfer and so on), and offers the IRP account details "if needed". That condition is tied to the payment method, which is still open, so the specific is not deferred without a condition. This one is borderline: the key's own condition (under 55) is not named in the message, and the IRP exceptions appear separately in step 4. Also, the answer's alternative short message ② has no IRP line at all; neither calibration quoted it.

### F20. zh-insurance-gap / gv-grav-base / r2 / KP 3 (t027 -> t422)
- Key point: 等待期时间：11月起新单位恢复缴费，按第三个自然月算约2027年1月起恢复报销（读成2027年2月也不能排除，应提示以经办为准）；2026年11月、12月看病医保基金不支付。
- Calibration 1 (FLAT): "按11月算，就是2027年1月1日；如果单位12月才办增员，就顺延到2月。"
- Calibration 3 (KEPT): "要等到“恢复缴费月起的第三个自然月”才能报销。按11月算，就是2027年1月1日；如果单位12月才办增员，就顺延到2月。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** The bullet states the rule (the third natural month from the month contributions resume), gives January 1, 2027 on the November assumption, and gives February if the employer enrolls her only in December. That is the key's window and open fact.

### F21. zh-insurance-gap / gv-grav-base / r2 / KP 4 (t027 -> t422)
- Key point: 杭州退休享受职工医保待遇的条件（办法第八条）：本市实际缴费满10年且累计缴费满20年，并在本市参保缴费至退休。按8年算，实际缴费还差24个月，累计还差144个月（视同缴费年限可抵，因人而异）；断缴的7个月不扣已有年限，只是本身不计入。
- Calibration 1 (FLAT): "如果你离退休还有12年以上，正常上班就能到；……如果离退休不到12年，才需要认真算补缴或延缴。"
- Calibration 3 (KEPT): "按这8年都计入累计算，以后正常上班，累计再缴12年、杭州实际再缴2年，就够了。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** The 12-year and 2-year figures are stated on the key's own basis ("counting the 8 years") and on continued normal employment, so they are conditional, not bare fixed amounts. The deemed-years offset is not mentioned; it would only lower the requirement.

### F22. zh-insurance-gap / gv-plain / r1 / KP 3 (t011 -> t447)
- Key point: as F20.
- Calibration 1 (FLAT): "断 7 个月只影响连续参保待遇（约 2 个月等待期），不影响已缴年限。"
- Calibration 3 (KEPT): "11 月、12 月大概率没有统筹报销，2027 年 1 月才恢复（以实际缴费到账月和经办核定为准）"
- Finding: neither (a) nor (b). **OK (KEPT is right).** January 2027 comes with "大概率" and with the key's open fact (the actual payment month and the agency's determination) in the same bullet. See observation W4.

### F23. zh-insurance-gap / gv-plain / r2 / KP 3 (t014 -> t408)
- Key point: as F20.
- Calibration 1 (FLAT): "新单位11月缴费，大约到2027年1月才能报销，这期间看病全自费。"
- Calibration 3 (KEPT): "中断超3个月再参保，自恢复缴费月起的第三个自然月才享受待遇。新单位11月缴费，大约到2027年1月才能报销，这期间看病全自费。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** Numbered item 2 states the third-natural-month rule and ties "about January 2027" to contributions starting in November. Calibration 1 quoted only part of the item. See observation W5.

### F24. zh-sick-pay / gv-grav-base / r1 / KP 5 (t021 -> t431)
- Key point: 计算基数是合同约定的岗位月工资，不含年终奖、交通/餐费/住房补贴、中夜班和高温津贴、加班工资，且不低于2740元（10号第九条）。按日折算用 基数 ÷ 21.75 × 比例 × 病假工作日（底线每日 2192 ÷ 21.75 = 100.78元）。
- Calibration 1 (FLAT): "根据《上海市企业工资支付办法》（沪人社规〔2026〕10号）第九条，病假工资以我在岗正常出勤月工资为基数"
- Calibration 3 (KEPT): "8,000元是否是“正常出勤月工资”要看构成：年终奖、餐补、交通补贴、住房补贴、加班费等不计入基数；固定月薪8,000元则基数就是8,000元。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** The item says that whether 8,000 is the base depends on its make-up, lists the exclusions, and gives 8,000 as the base only for a fixed monthly salary. That is the key's condition.

### F25. zh-sick-pay / gv-plain / r1 / KP 2 (t020 -> t445)
- Key point: 讲清2026年的变化：上海病假分档文件沪劳保发〔1995〕83号已于2026-08-15失效，未见替代文件，所以9月的病假没有现行的上海法定分档比例。劳动合同、集体合同或经民主程序制定并公示的员工手册写了比例的，按约定发，公司不能单方降低；都没写的，至少按法定底线发。
- Calibration 1 (FLAT): "第二，我的合同或员工手册第 X 条明确约定了 80%，这是双方约定，不因地方文件到期自动失效，公司不能单方降低。"
- Calibration 3 (KEPT): "查看劳动合同和员工手册：其中有没有“病假工资按连续工龄计发”“满 4 年按 80%”“按本人工资 80%”之类的条款。如果有，就按约定标准主张；如果没有，至少应按 2192 元主张。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** The step makes the agreed rate conditional on the contract or handbook having such a clause, and falls back to at least 2,192 yuan if it does not. That is the key's condition. See observation W2.

### F26. zh-sick-pay / gv-plain / r1 / KP 4 (t020 -> t445)
- Key point: 如果公司制度照搬了83号分档：入职满4年属"满4年不满6年"档，比例是80%（不是70%），8000 × 80% = 6400元，比800元少5600元。6400元是按公司制度算的数，不是法定最低。
- Calibration 1 (FLAT): "我的合同或员工手册第 X 条明确约定了 80%，这是双方约定，不因地方文件到期自动失效"
- Calibration 3 (KEPT): "如果你劳动合同或员工手册里还保留着原来“按连续工龄计发”的条款，你能主张的会更高：4 年工龄对应 80%，按 8000 元算约 6400 元。"
- Finding: neither (a) nor (b). **OK (KEPT is right).** The sentence makes 80% and 6,400 yuan conditional on the contract or handbook still containing the seniority clause, which is the key's condition. See observation W3.

## Reverse flips (KEPT in calibration 1, FLAT in calibration 3): 4

| # | Answer / KP (ids) | Calibration 1 KEPT quote | Calibration 3 FLAT quote |
|---|---|---|---|
| R1 | en-529-roth / gv-grav-base / r1 / KP 4 (t036 -> t418) | "Opened 2004, so met — unless you changed the beneficiary at some point, which can restart the clock." | "If you contributed in 2021–2026, that money isn't eligible." |
| R2 | ko-severance-pay / gv-grav-base / r2 / KP 6 (t031 -> t439) | "저는 지급기일 연장에 합의한 사실이 없다는 점을 먼저 말씀드립니다. ... 회사에서 산정한 금액, 지급 예정일, 지급 방식(IRP 이전 여부)을 함께 회신해 주시기 바랍니다." | "회사에서 산정한 금액, 지급 예정일, 지급 방식(IRP 이전 여부)을 함께 회신해 주시기 바랍니다." |
| R3 | zh-flex-hours / gv-grav-base / r2 / KP 7 (t016 -> t415) | "10月4日至7日：不当然按200%计算，而要放进批复的周期（月、季或年）里，与总标准工时比较；超出部分按150%，没超出就可能不另付。" | "如果这32小时全部构成周期超时，约2482.76元，合计约6206.90元" |
| R4 | zh-insurance-gap / gv-plain / r2 / KP 6 (t014 -> t408) | "以灵活就业身份参保，需是杭州户籍；非杭州户籍则要“杭州实际缴费满10年”或“持居住证并办就业登记”。…" | "7个月可补约3,316元、2026年底截止" |

The rule does not cover these, and they were not audited. In each case calibration 3 picked a different, more absolute statement as the worst one, which is the direction the rubric asks for.

## Worst-statement observations (outside the pre-declared test; not counted)

The pre-declared test looks only at calibration 3's KEPT quote, so everything above passes. The rubric also says to mark the worst statement of a point, and it counts steps, summary lines, table cells and drafted messages as statements. In several flips, calibration 1's FLAT statement is still in the same answer, and calibration 3 neither quoted it nor answered it. Under that worst-statement rule, these KEPT marks look doubtful. That is a problem with how the grader applied the rubric, not the kind of defect in the rubric text that this audit was set up to catch. The list comes from reading around the quotes and is not a full re-grade.

- W1 (F10, en-medicare-part-b/gv-grav-base/r1, KP 1). "Part B gets an 8-month penalty-free window after you stop working." gives the 8-month window anchored on stopping work only, and drops "or the coverage ends, whichever first". This sentence is itself shaped like (a). The answer states the full trigger elsewhere (its why-you-can-wait paragraph and step 6).
- W2 and W3 (F25 and F26, zh-sick-pay/gv-plain/r1, KP 2 and KP 4). The drafted reply to HR states "我的合同或员工手册第 X 条明确约定了 80%" as fact. That assumes an open fact (whether the contract has the clause) inside a drafted message, which the rubric lists as FLAT.
- W4 (F22, zh-insurance-gap/gv-plain/r1, KP 3). The summary line "（约 2 个月等待期）" carries only the softener 约 and none of the January/February or agency caveat; rubric line 32 makes that FLAT.
- W5 (F23, zh-insurance-gap/gv-plain/r2, KP 3). The table cell "约2个月不能报销" has the same pattern. Neither calibration quoted it.
- W6 (F06, en-529-roth/gv-plain/r2, KP 4). "so the 15-year rule is almost certainly satisfied" carries only a hedge. The condition is in the next sentence of the same paragraph, but a paragraph is not a "step" under the rubric. Arguable.
- W7 (F11, ja-part-time-leave/gv-grav-base/r2, KP 3). The bullet "来月が10月以降なら、その休みは有給で取れます" states the outcome without the 80% condition, which is in the preceding bullet. Arguable.
- W8 (F13, ja-wallpaper-restoration/gv-plain/r2, KP 3). The opening paragraph states what the 原状回復 clause means without the caveat that the contract is unreviewed and may contain a specific clause. Arguable.

W1 to W5 are the clearest. If Emily wants the worst-statement rule enforced in the acceptance, these five KEPT marks (four answers) would need another look before calibration 3 is relied on. They do not change the result below, which follows the rule as it was declared.

## Other transitions (outside this audit, not reviewed)

WRONG -> KEPT: en-medicare-part-b/gv-plain/r2 KP 1 (t035 -> t412); zh-sick-pay/gv-plain/r2 KP 5 (t034 -> t430).
WRONG -> FLAT: ko-unemployment-quit/gv-grav-base/r2 KP 2 (same quote). FLAT -> WRONG: zh-flex-hours/gv-plain/r1 KP 7.
ABSENT -> FLAT: ja-wallpaper-restoration/gv-grav-base/r1 KP 5; zh-sick-pay/gv-plain/r1 KP 5.

Condition 1 of the rule (tuning_check5.py prints CALIBRATION PASSED) was not part of this audit, and I did not run it.
The saved calibration-calibration3.json records "pass": true.

AUDIT RESULT: PASS
