# zh-insurance-gap: adversarial check of "Facts for the key"

- Checked: 2026-10-22, against `zh-insurance-gap.md` (only file read on disk).
- How the sources were opened:
  - Hangzhou gazette PDF (杭政函〔2025〕88号): fetched from the official URL and the text layer extracted with pypdf. The PDF has 42 pages (办法 pp.1-10, 实施细则 pp.11-42), not the 30 pages the source file states. I read the whole text.
  - gov.cn pages (38号文, 43号文, 社会保险法) and the 杭州网 reprint of the 2026 数据通告: fetched directly and read as text.
  - ybj.hangzhou.gov.cn, www.hangzhou.gov.cn and ybj.zj.gov.cn timed out from here.
  - The fetch tool hit its session limit after the first page. The shared web-search budget was already used up, so I ran no searches.
  - So the search for 2025-2026 national or provincial changes is incomplete (see "Could not decide").

Key URLs used below:
- [HZ] https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/10/15/20251015_ec3d3e35772bc2a066570411d334c03f.pdf (杭政函〔2025〕88号, 2025-09-30; 办法 + 附件《实施细则》)
- [HZ-DATA] https://hznews.hangzhou.com.cn/chengshi/content/2026-01/11/content_9160281.htm (杭州网 2026-01-11, full reprint of 《关于公布2026年杭州市基本医疗保障有关数据的通告》)
- [GB38] https://www.gov.cn/zhengce/zhengceku/202408/content_6965742.htm (国办发〔2024〕38号, 成文 2024-07-26, 发布 2024-08-01)
- [YB43] https://www.gov.cn/zhengce/zhengceku/2021-11/28/content_5653856.htm (医保办发〔2021〕43号, 成文 2021-11-01, 实施 2021-12-01)
- [SIL] https://www.gov.cn/guoqing/2021-10/29/content_5647616.htm (社会保险法, 2010 通过, 2018-12-29 修正)

## Verdicts

### 前提及其错误

**F1. 前提"断缴超过3个月，以前年限清零，退休要重新交满"错误 — stands**
- [HZ] Neither the 办法 nor the 实施细则 has any clause that clears 职工医保 years. In the full text, 清零 appears once and 重新计算 appears once, both in the 居民医保 大病保险 incentive clause (实施细则 二十七):
  「参保人员发生大病报销并使用奖励额度后，累计零报销激励额度清零。断保之后再次参保的，连续参保年数重新计算。」

**F2. 依据：社保法27条按累计缴费；43号文12条"累计计算"；杭州办法2026-01-01施行，年限为各段合计，无清零条款 — stands (add a scope note for 43号文)**
- [SIL] 第二十七条: 「参加职工基本医疗保险的个人，达到法定退休年龄时累计缴费达到国家规定年限的，退休后不再缴纳基本医疗保险费，」
- [YB43] 第十二条: 「参加职工基本医疗保险的个人，基本医疗保险关系转移接续时，基本医疗保险缴费年限累计计算。」 The article is written for transfers between pooling areas. It still supports the point, but cite it as "转移接续时累计计算".
- [HZ] 办法 三十二: 「本办法自 2026年 1 月 1 日起施行」. 实施细则 一(六) lists 实际, 视同 and 2002年底前连续工龄 years 「但不重复计算」.

**F3. 杭州以"3个月"为界；超过即中断参保，恢复后有等待期，断缴期和等待期看病不报；8年不受影响 — stands**
- [HZ] 实施细则 一(三): 「未在规定时间内办理参保缴费手续或连续中断缴费三个月（不含）以上的，视为中断参保。」
- Precision: the threshold is "more than three months" (三个月不含). A gap of exactly three months is not 中断参保.

**F4. 38号文没有职工医保断缴/补缴条款；3个月固定等待期、每断1年加1个月、"连续参保年数重新计算"都针对居民医保 — stands**
- [GB38] The page's only 职工医保 sentences cover 失业代缴, 个人账户共济 and 就业地参保. All the 等待期 and 重新计算 language sits in the 居民医保 paragraphs:
  「自2025年起，除新生儿等特殊群体外，对未在居民医保集中参保期内参保或未连续参保的人员，设置参保后固定待遇等待期3个月；」
- Caveat (unchanged from the source): the gov.cn copy ends 「（本文有删减）」.

### 正确数字和算法

**F5. 已缴8年 = 96个月，全部保留 — stands** (8×12 = 96; see F1)

**F6. 杭州退休条件：本市实际满10年 + 累计满20年（可含视同、2002年底前连续工龄），并在本市参保到退休 — stands**
- [HZ] 办法 八: 「职工医保参保人员在本市连续参保缴费至按月领取基本养老金或法定退休年龄时，本市职工医保实际缴费年限满十年（含），且职工医保累计缴费年限满二十年（含）的，」

**F7. 实际还差 120−96 = 24个月；累计还差 240−96 = 144个月 — stands** (arithmetic checked, under the stated assumption that all 8 years were paid in Hangzhou)

**F8. 断缴7个月不扣减已有年限，只是本身不计入（除非补缴） — stands** (F1; 实施细则 一(四)3 「补缴年限记录为实际缴费年限」)

**F9. 2026年4–10月 = 7个月 > 3个月 → 中断参保 — stands** (count checked; this assumes March 2026 was paid by the old employer)

**F10. 11月恢复缴费 → 按"第三个自然月"读法2027年1月起享受；11、12月"统筹基金不报"；不中断本应12月起 — needs change (wording)**
- [HZ] 实施细则 一(三)1: 「自恢复缴费月起的第三个自然月开始享受职工医保待遇，在中断参保期间和待遇等待期内发生的医疗费用，医保基金不予支付。」
- [HZ] 办法 二十七 defines 医保基金 to include personal-account money: 「…大病保险基金和医疗救助基金等专项基金，以及个人账户资金。」
- The text bars 医保基金, not just 统筹基金. Corrected wording: 「2026年11月、12月（等待期）看病，医保基金不予支付（杭州办法所称医保基金包括个人账户资金），等待期内能否刷个人账户以经办答复为准。」
- The January reading and the normal start in December stand: 一(二) 「在办理缴费手续后的次月起享受职工医保待遇」. The February reading remains open (see Could not decide).

**F11. 灵活就业补缴标准2026年473.67元/月（4986×9.5%，4986 = 99722×60%÷12） — stands**
- [HZ-DATA] 「99722元（2023年浙江省非私营和私营单位就业人员加权平均工资）×60%÷12月＝4986元/月；月缴费标准为473.67元」
- [HZ] 实施细则 一(四)2: 「按办理补缴时灵活就业人员的缴费标准执行」
- Recomputed: 99722×0.6/12 = 4986.10 → 4986; 4986×0.095 = 473.67.

**F12. 7个月 473.67×7 = 3,315.69元；个人大病保险费从补划个人账户中扣，不另交现金 — stands, minor addition**
- Arithmetic checked: 3,315.69.
- [HZ] 实施细则 一(四)4: 「按规定补划个人账户资金并扣减应由个人补缴的大病保险费和长期护理保险（以下简称长护险）费。」
- Corrected wording: 「个人应缴的大病保险费和长护险费从补划的个人账户资金中扣减，不另交现金。」

**F13. 补缴起始时间不得早于办理当年 → 补2026年的月份须在2026年12月31日前办 — stands**
- [HZ] 实施细则 一(四)2: 「补缴起始时间不得早于办理补缴手续当年。」

**F14. 效果：记为实际缴费年限；补缴月份医疗费不报；能否免等待期未核实 — stands**
- [HZ] 实施细则 一(四)3: 「补缴年限记录为实际缴费年限；补缴时段内发生的医疗费用，医保基金不予支付。」
- Adversarial note: 一(三)1 has no exception for 补缴. The only clause that restores benefits after 补缴 is 一(三)2, and it covers 用人单位欠缴 only. So the text gives no basis for a waiver, but it does not forbid one either. Leave this as 未核实.

**F15. 灵活就业资格：本市户籍；或本市实际满10年（8年不够）；或持杭州《居住证》并在杭州办就业登记 — stands**
- [HZ] 办法 六: 「2.本市职工医保实际缴费年限已累计满十年，或持本市核发的有效期内《浙江省居住证》（以下简称《居住证》）并在本市办理就业登记的非本市户籍人员；」
- This is consistent with [GB38], which orders only 超大城市 to drop 户籍 limits and 特大城市 to apply 持居住证参保.

**F16. 新单位不能替她补4–10月："单位补缴不得早于该单位为她参保的时间" — refuted (the conclusion holds, the stated rule is misread)**
- [HZ] 实施细则 一(四)1: 「补缴起始时间不得早于本人所在用人单位纳入职工医保参保范围的时间。」
- This clause limits back-payment to the date the employer itself came into coverage. It is not the date the employer insured her.
- The real basis is the opening of 一(四): 「参保人员应保未保期间的职工医保（含生育保险）费，可申请按应保未保期间不同身份对应的缴费标准补缴」. From April to October she was not the new company's employee, so there is no 职工-identity period for that company to back-pay.
- Corrected wording: 「新单位不能替她补4–10月：补缴按"应保未保期间"的实际身份办理，4–10月她不是新单位职工，不能以新单位职工身份补缴；只能考虑以灵活就业身份补缴。」

**F17. 不补的代价：只有到退休时累计不满20年才需要补；再工作满12年（或有视同年限）则7个月不影响 — needs change (incomplete)**
- [HZ] 办法 八 sets two tests (本市实际满10年 and 累计满20年), and the text after them is 「医保缴费年限未达到上述规定年限要求的，可办理医保退休一次性缴纳或按月延续缴纳」.
- Corrected wording: 「只有到退休时本市实际缴费不满10年或累计不满20年才需要补；她再在杭州缴满12年（或有视同年限抵扣、且本市实际满10年），这7个月就不影响退休医保。」

**F18. 一次性缴纳2026年743.60元/月（99722×8.9%÷12 + 48÷12），7个月约5,205.20元，不进个人账户，每年调整；按月延缴443.75元/月 — stands**
- [HZ-DATA] 「其补缴标准为743.60元/月，即：99722元×8.9%÷12月（职工医保费）+48元÷12月（大病保险费）=743.60元/月；」「其缴费标准为443.75元/月」
- [HZ] 实施细则 一(七): 「退休一次性缴纳的医保费不予划入个人账户。」 The 48元 is the 职工 大病保险 individual share, per 实施细则 二十四: 「个人缴纳 48元」.
- Recomputed: 99722×0.089/12 = 739.605; +4 = 743.605 → 743.60; ×7 = 5,205.20. 4986×0.089 = 443.754 → 443.75.
- Annual adjustment: 实施细则 八十一 says the next year's 征缴基数 are published 「在每年年底前」.

### 回答可能顺带提到的说法

**F19. "职工医保断缴3个月清零是38号文规定的"：错 — stands** (see F4)

**F20. "断缴超过3个月要等6个月"：杭州为第三个自然月（约多等1个月）；43号文"原则上不超过6个月" — stands**
- [YB43] 第十一条: 「中断缴费3个月以上的，基本医疗保险待遇按各统筹地区规定执行，原则上待遇享受等待期不超过6个月。」
- Normal start is December and the gapped start is January, which is one month extra.

**F21. "3个月内补缴待遇不中断、可追溯"：43号文只对转移接续或职工/居民切换、中断≤3个月的情形，切换还要求连续参保2年以上；她断7个月不适用 — stands**
- [YB43] 第十一条: 「补缴后不设待遇享受等待期，缴费当月即可在转入地按规定享受待遇，中断期间的待遇可按规定追溯享受。」 The second paragraph begins 「参保人员已连续2年（含2年）以上参加基本医疗保险的」.
- Optional strengthening: Hangzhou's own 实施细则 一(四)3 bars payment for medical costs in back-paid months (see F14), so no retroactive reimbursement applies here in any case.

**F22. "断缴后个人账户清零"：错；断缴期间停止划入和使用，余额保留，重新参保后可继续使用 — stands**
- [HZ] 一(十二): 「1.未按规定缴纳或停止缴纳职工医保费的；」. 一(十一)4: 「个人账户结余资金未办理转移或清算手续的，再次参加本市职工医保后，可按规定继续使用。」
- See F10 for use during the waiting period.

**F23. "退休要交满25/30年或必须连续缴费"：杭州本市实际10年 + 累计20年，累计计算，"不要求连续" — needs change (overclaim)**
- [HZ] 办法 八 opens 「职工医保参保人员在本市连续参保缴费至按月领取基本养老金或法定退休年龄时」.
- [HZ] 实施细则 一(二): 「参保人员应连续缴纳职工医保费至享受职工医保退休待遇为止。」
- The text does require continuous contribution up to retirement. What it does not do is erase earlier years after a gap: the consequences of a gap are suspension and a waiting period (一(二), 一(三)).
- Corrected wording: 「杭州是本市实际10年＋累计20年，年限累计计算，过去的断档不会抹掉已缴年限；但办法要求在杭州持续参保缴费直到退休，断缴期间待遇暂停、恢复后有等待期。浙江其他城市和外省规定不同。」

**F24. 灵活就业9.5%（含生育0.6%），基数为上年度省平工资60%，2026年473.67元/月；低保边缘证者236.84元/月 — stands**
- [HZ] 办法 七5: 「灵活就业人员以上年度省平工资的 60%为缴费基数，按9.5%的比例按月缴纳职工医保（含生育保险）费。」
- [HZ-DATA] 「其中持有本市民政部门核发的有效期内《最低生活保障边缘家庭证》的人员为236.84元/月。」 Recomputed: 473.67/2 = 236.835 → 236.84.

**F25. 在职：单位9.5%（含生育0.6%）、个人2% — stands**
- [HZ] 办法 七1: 「用人单位的缴费比例为9.5%（其中生育保险缴费比例为0.6%，下同），职工个人的缴费比例为2%」

**F26. 生育津贴须在杭州连续缴纳满6个月 — stands**
- [HZ] 办法 二十二: 「申领津贴时已在本市连续缴纳职工医保（含生育保险）费满六个月。」
- The same article also requires 生育时「在本市职工医保待遇期内」, so births during the 2026-11/12 waiting period would not qualify.

**F27. 居民医保兜底：杭州"其他居民医保"限本市户籍成年人；2026年一档770、二档670元/年；非集中期参保3个月等待期 — stands**
- [HZ] 办法 十3: 「其他居民医保：十八周岁以上的本市户籍人员」
- [HZ] 实施细则 十五: 「个人缴纳770元」「个人缴纳670元」
- [HZ] 实施细则 十八: 「未在集中参保期内参保缴费的居民，缴费未中断的，设置参保后固定待遇等待期三个月；」

**F28. 失业保险金：非本人意愿离职、缴满1年、办失业登记，领金期间职工医保由失业保险基金代缴；"能否追溯到4月起未核实" — stands; the open point is now decided**
- [SIL] 第四十五条 sets the three conditions, and 第四十八条 says 「个人不缴纳基本医疗保险费」.
- [SIL] 第五十条: 「失业保险金领取期限自办理失业登记之日起计算。」
- Corrected wording: 「失业代缴只覆盖领取失业保险金期间，而领取期限自办理失业登记之日起计算；4月起没有办登记的月份不能追溯代缴。她11月已入职，现在办登记基本没有意义。」

**F29. 居民医保连续参保奖励（自2025年起满4年后每年+5000元，零报销+5000元，合计≤12万元，断保后重新计算），只适用于居民医保 — stands**
- [HZ] 实施细则 二十七: 「对自 2025年起连续参加居民医保满四年的参保人员，之后每连续参保一年，提高大病保险最高支付限额5000元。」 It continues with the 零报销 incentive, 「两项激励累计提高总额度不超过12万元」 and 「断保之后再次参保的，连续参保年数重新计算」.

**F30. 未能核实清单 — stands, update the list**
- Remove 失业代缴追溯 (decided in F28).
- Keep the rest. Add that [HZ] 办法 三十二 says 「国家、省另有规定的，从其规定」, so an unread provincial text could override the Hangzhou rule.

## Tally

- Stands as written: 23 (F1-F9, F11, F13-F15, F18-F22, F24-F27, F29).
- Stands, wording update only: 3 (F12 add 长护险费; F28 open point decided; F30 list update).
- Refuted / needs change: 4.
  - F16: the stated rule is misread; the conclusion survives.
  - F10: 医保基金, not just 统筹基金.
  - F17: missing the 本市实际10年 condition.
  - F23: "不要求连续" contradicts 办法 八 and 一(二).

## Could not decide

- 第三个自然月: January (Nov=1) versus February. The text gives no worked example, and the Hangzhou bureau site was unreachable.
- Whether back-paying the gap as 灵活就业 removes the waiting period. The text is silent; the only waiver is the employer-arrears case in 一(三)2.
- Whether an unemployed, unregistered gap counts as 「应保未保期间」 eligible for 灵活就业 补缴. 灵活就业 participation is voluntary (办法 六 「可自主选择」), so the 经办 may refuse.
- Newer overriding rules. I could not check:
  - the Zhejiang provincial 实施意见 (2025) and 《浙江省医疗保障条例》 (ybj.zj.gov.cn timed out);
  - any 2025-2026 national law, for example whether a 医疗保障法 has been enacted;
  - whether 社会保险法 has been amended after 2018 (no search budget).
  The gov.cn 社会保险法 text read here shows the 2018 amendment as its latest.
- The official 数据通告 itself (date 2025-12-23, issuing page). The figures were read only from the 杭州网 full reprint; they match the gazette formulas exactly.
