# zh-insurance-gap: source check

- Checked: 2026-10-22
- Request: 杭州，2026年3月离职，4月至10月共7个月未交职工医保，11月新单位重新参保；此前连续交职工医保8年。问"断缴超过3个月以前年限全部清零、退休要重新交满"是否属实，能否补救、补多少钱。
- Method: primary official pages opened directly. The Zhejiang provincial hosts (ybj.zj.gov.cn, mpa.zj.gov.cn, minyi.zjzwfw.gov.cn) reset every connection from here, and the built-in browser was denied on them, so the provincial texts are marked "could not verify". The operative local rule (杭州 2026 办法 and 实施细则) was read in full from the official gazette PDF. Search budget ran out before the official Hangzhou 2026 数据通告 page itself could be found; its figures come from the 杭州网 reprint and are checked by arithmetic.

## A. National level

### A1. 国办发〔2024〕38号 contains a 职工医保 中断缴费 / 补缴 / "3个月" rule — **corrected**
- URL: https://www.gov.cn/zhengce/zhengceku/202408/content_6965742.htm (成文 2024-07-26, 发布 2024-08-01); cross-checked at http://www.nhsa.gov.cn/art/2024/8/1/art_104_13427.html and https://guangdong.chinatax.gov.cn/gdsw/zjfg/2024-08/02/content_1bdd19f524f7401898464cd28fbf3369.shtml
- Finding: the document has no sentence that contains 职工医保 together with 中断, 断保, 补缴 or 转. Its waiting periods and its "3个月" apply to 居民医保. The gov.cn text carries the note "本文有删减"; three official copies were checked and none has such a clause.
- Quote: 「自2025年起，除新生儿等特殊群体外，对未在居民医保集中参保期内参保或未连续参保的人员，设置参保后固定待遇等待期3个月；」

### A2. 38号文 居民医保 waiting periods — **confirmed**
- URL: http://www.nhsa.gov.cn/art/2024/8/1/art_104_13427.html (2024-08-01)
- Quote: 「其中，未连续参保的，每多断保1年，原则上在固定待遇等待期基础上增加变动待遇等待期1个月，」「参保人员可通过缴费修复变动待遇等待期，每多缴纳1年可减少1个月变动待遇等待期，」
- Also: 「连续断缴4年及以上的，修复后固定待遇等待期和变动待遇等待期之和原则上不少于6个月。」「等待期具体标准由各省份根据自身情况确定。」

### A3. 38号文 连续参保激励 (the only "重新计算" in the document) — **confirmed, 居民医保 only**
- URL: https://www.gov.cn/zhengce/zhengceku/202408/content_6965742.htm (2024-07-26)
- Quote: 「对连续参加居民医保满4年的参保人员，之后每连续参保1年，可适当提高大病保险最高支付限额。」「断保之后再次参保的，连续参保年数重新计算。」
- Also: 「原则上每次提高限额均不低于1000元，累计提高总额不超过所在统筹地区大病保险原封顶线的20%。」

### A4. 38号文: 失业保险金 pays 职工医保 (added) — **confirmed**
- URL: https://www.gov.cn/zhengce/zhengceku/202408/content_6965742.htm (2024-07-26)
- Quote: 「落实从失业保险基金中支付领取失业保险金人员的职工医保（含生育保险）费政策，并确保与参保职工同等享受医疗保险、生育保险待遇。」

### A5. National 3-month rule is in 医保办发〔2021〕43号, Art. 11 (cross-region transfer and 职工/居民 switching) — **confirmed (added)**
- URL: https://www.gov.cn/zhengce/zhengceku/2021-11/28/content_5653856.htm (印发 2021-11-01, 施行 2021-12-01)
- Quote: 「在转移接续前中断缴费3个月（含）以内的，可按转入地规定办理职工基本医疗保险费补缴手续，补缴后不设待遇享受等待期，」「中断缴费3个月以上的，基本医疗保险待遇按各统筹地区规定执行，原则上待遇享受等待期不超过6个月。」
- Para 2 (switching schemes) applies the same rule only to people who 「已连续2年（含2年）以上参加基本医疗保险的」. Scope note: this article governs transfers between pooling areas and switches between schemes; a gap inside Hangzhou is governed by the Hangzhou rule (C3).

### A6. 43号 Art. 12: 缴费年限累计计算 — **confirmed**
- URL: https://www.gov.cn/zhengce/zhengceku/2021-11/28/content_5653856.htm (2021-11-01)
- Quote: 「参加职工基本医疗保险的个人，基本医疗保险关系转移接续时，基本医疗保险缴费年限累计计算。」「达到法定退休年龄时，享受退休人员基本医疗保险待遇的缴费年限按照各地规定执行。」

### A7. 社会保险法 第二十七条: retirement test is cumulative years — **confirmed**
- URL: https://www.gov.cn/guoqing/2021-10/29/content_5647616.htm (law of 2010-10-28, amended 2018-12-29)
- Quote: 「参加职工基本医疗保险的个人，达到法定退休年龄时累计缴费达到国家规定年限的，退休后不再缴纳基本医疗保险费，按照国家规定享受基本医疗保险待遇；未达到国家规定年限的，可以缴费至国家规定年限。」

### A8. 社会保险法 第四十五条、第四十八条: 失业保险金 and 职工医保 during it (added) — **confirmed**
- URL: https://www.gov.cn/guoqing/2021-10/29/content_5647616.htm
- Quote (45): 「（一）失业前用人单位和本人已经缴纳失业保险费满一年的；（二）非因本人意愿中断就业的；（三）已经进行失业登记，并有求职要求的。」
- Quote (48): 「失业人员应当缴纳的基本医疗保险费从失业保险基金中支付，个人不缴纳基本医疗保险费。」

### A9. NHSA official explanation of 38号文: waiting period is a 居民医保 measure — **confirmed**
- URL: https://paper.people.com.cn/rmrbwap/html/2024-08/22/nw.D110000renmrb_20240822_6-03.htm (人民日报 2024-08-22, 国家医疗保障局有关司局负责人)
- Quote: 「医保待遇等待期是指参保人员因未按照政策规定及时参保缴费，导致无法立即享受医保待遇，需要等待一段时间才能享受，」
- The article does not mention 职工医保.

## B. Zhejiang provincial level

### B1. 浙江九部门《关于健全基本医疗保险参保长效机制的实施意见》(reported as 浙医保联发〔2024〕19号, 2025-03-27, reported effective 2025-04-01) — **could not verify**
- URL tried: http://ybj.zj.gov.cn/art/2025/3/27/art_1229113757_2548108.html and its 解读 http://ybj.zj.gov.cn/art/2025/3/27/art_1229667819_2548102.html (connection reset; browser denied)
- A search-engine summary says it exempts 「职工医保参保中断3个月内转入」 people from the fixed waiting period. Not read from the original; do not rely on it.

### B2. 《浙江省医疗保障条例》(2021) 灵活就业 中断 → "第三个自然月" — **could not verify**
- URL tried: https://mpa.zj.gov.cn/art/2021/8/12/art_1229563479_2348289.html and http://ybj.zj.gov.cn/art/2021/8/19/art_1229560915_2323375.html (connection reset)
- The Hangzhou 实施细则 (C3) uses the same "第三个自然月" wording and is the operative local text.

### B3. 浙江医保省级统筹 (2026) — **confirmed that it exists; no change to the years rule found**
- URL: https://hznews.hangzhou.com.cn/kejiao/content/2026-01/05/content_9156179.htm (杭州网 2026-01-05)
- Quote: 「先行实施职工医保基金省级统筹调剂，设立基础调剂金，纳入省级财政专户管理，单独核算，专款专用。」
- The article says nothing about 断缴, 等待期 or 最低缴费年限.

### B4. A single Zhejiang-wide 职工医保 retirement minimum — **could not verify**
- Only the Hangzhou rule was read. Other Zhejiang cities have their own 办法 (for example 嘉兴 嘉政发〔2024〕22号), so treat the 10/20-year figure as Hangzhou-only.

## C. Hangzhou (operative rule)

Primary source for C1–C10, C12–C16: 杭州市人民政府《关于印发杭州市基本医疗保障办法的通知》杭政函〔2025〕88号, signed 2025-09-30, gazette PDF https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/10/15/20251015_ec3d3e35772bc2a066570411d334c03f.pdf (30 pages, read in full; 办法 + 附件《实施细则》).

### C1. Current rule, effective date, what it replaces — **confirmed**
- Quote (办法 三十二): 「本办法自2026年1月1日起施行」「《杭州市人民政府关于印发杭州市基本医疗保障办法的通知》（杭政〔2020〕56号）同时废止。」

### C2. Benefits stop the month after a month goes unpaid — **confirmed**
- Quote (实施细则 一(二)): 「参保人员应连续缴纳职工医保费至享受职工医保退休待遇为止。参保人员当月未缴费的，次月起暂停享受职工医保待遇。」

### C3. Gap over 3 months = 中断参保; waiting period on return; nothing paid during gap or wait — **confirmed** (the "3个月" threshold in the premise is right; the consequence is a waiting period, not a reset)
- Quote (实施细则 一(三)): 「未在规定时间内办理参保缴费手续或连续中断缴费三个月（不含）以上的，视为中断参保。」
- Quote (一(三)1): 「中断参保后重新办理参保手续并恢复正常缴费的，自恢复缴费月起的第三个自然月开始享受职工医保待遇，在中断参保期间和待遇等待期内发生的医疗费用，医保基金不予支付。」
- Compare normal start (一(二)): 「在办理缴费手续后的次月起享受职工医保待遇。」
- Reading: payment resumed in 2026-11 → Nov (1st), Dec (2nd), Jan (3rd) → benefits from 2027-01; the normal start without a gap would be 2026-12. The text gives no worked example; the reading 2027-02 cannot be ruled out. Confirm with the 医保经办.

### C4. "断缴超过3个月，以前交的年限全部清零" — **corrected**
- No clause in the 办法 or 实施细则 clears earlier years; years are defined as sums (C6), the national rule says 累计计算 (A6), and the law tests 累计缴费 (A7). The only "重新计算" in these sources is the 居民医保 大病保险 continuity bonus (A3, C16).

### C5. Retirement test in Hangzhou: cumulative, 本市实际 ≥10 years and 累计 ≥20 years — **confirmed** (premise "退休要重新交满" corrected)
- Quote (办法 八): 「本市职工医保实际缴费年限满十年（含），且职工医保累计缴费年限满二十年（含）的，应在本市医保经办机构办理医保退休资格确认手续后，按规定享受职工医保退休待遇。」
- The same sentence opens 「职工医保参保人员在本市连续参保缴费至按月领取基本养老金或法定退休年龄时」: the person must be insured in Hangzhou up to retirement, but the years themselves are counted cumulatively.

### C6. What counts as 实际 / 累计 years — **confirmed**
- Quote (实施细则 一(五)): 「2.在本市参加职工医保的实际缴费年限；」 (one of four parts, 「但不重复计算」)
- Quote (一(六)): 「2.职工医保视同缴费年限。」「3.2002年12月31日前符合国家和省有关规定的连续工龄。」 also count toward 累计.

### C7. Shortfall at retirement: lump sum or monthly continuation, 8.9% — **confirmed**
- Quote (实施细则 一(七)): 「选择退休一次性缴纳的参保人员，缴费基数为办理补缴时的上年度省平工资，缴费费率为8.9%，退休一次性缴纳的医保费不予划入个人账户。」
- 2026 figures (see C11 source): 一次性 「743.60元/月」 = 99722×8.9%÷12 + 48÷12; 按月延缴 「443.75元/月」 = 4986×8.9%.

### C8. Back-payment (补缴) is possible; rules — **confirmed**
- Quote (实施细则 一(四)2): 「以灵活就业人员身份补缴的，按办理补缴时灵活就业人员的缴费标准执行，补缴起始时间不得早于办理补缴手续当年。」
- Quote (一(四)3): 「补缴年限记录为实际缴费年限；补缴时段内发生的医疗费用，医保基金不予支付。」
- Employer-route back-payment cannot reach before the employer covered the person: 「补缴起始时间不得早于本人所在用人单位纳入职工医保参保范围的时间。」 So the new employer cannot cover April–October.
- Consequence: the April–October 2026 months can be back-paid as 灵活就业 only while the application is made in 2026.

### C9. Back-paying the gap removes the waiting period in Hangzhou — **could not verify**
- The 实施细则 is silent on this; the only national "no waiting period after 补缴" rule is limited to gaps of 3 months or less (A5). Also unconfirmed: whether the 经办 treats an unemployed person's gap as 「应保未保期间」 eligible for 灵活就业 back-payment. Ask the 杭州医保经办.

### C10. Who may join as 灵活就业 in Hangzhou — **confirmed**
- Quote (办法 六): 「1.本市户籍人员；2.本市职工医保实际缴费年限已累计满十年，或持本市核发的有效期内《浙江省居住证》（以下简称《居住证》）并在本市办理就业登记的非本市户籍人员；」
- With 8 years, a non-Hangzhou-户籍 person does not meet the 10-year route and needs the 居住证 + 就业登记 route.

### C11. 灵活就业 contribution standard and 2026 amount — **confirmed** (rule from gazette; figures from a reprint of the official notice)
- Rule quote (办法 七5): 「灵活就业人员以上年度省平工资的60%为缴费基数，按9.5%的比例按月缴纳职工医保（含生育保险）费。」
- Figures URL: https://hznews.hangzhou.com.cn/chengshi/content/2026-01/11/content_9160281.htm (杭州网 2026-01-11, reprinting 《关于公布2026年杭州市基本医疗保障有关数据的通告》 dated 2025-12-23, effective 2026-01-01)
- Quote: 「99722元（2023年浙江省非私营和私营单位就业人员加权平均工资）×60%÷12月＝4986元/月」「月缴费标准为473.67元」
- Arithmetic: 99722×0.6÷12 = 4986.1 → 4986; 4986×9.5% = 473.67.

### C12. 个人账户 during the gap — **confirmed**
- Quote (实施细则 一(十二)): 「有以下情形之一的，停止划入及使用个人账户资金：1.未按规定缴纳或停止缴纳职工医保费的；」
- Quote (一(十一)4): 「个人账户结余资金未办理转移或清算手续的，再次参加本市职工医保后，可按规定继续使用。」

### C13. 居民医保 as a stop-gap in Hangzhou — **confirmed**
- Quote (办法 十3): 「其他居民医保：十八周岁以上的本市户籍人员」 (non-户籍 adults cannot join Hangzhou 居民医保)
- 2026 individual share (实施细则 二(十五)): 一档 770元/年, 二档 670元/年.
- Quote (二(十八)): 「未在集中参保期内参保缴费的居民，缴费未中断的，设置参保后固定待遇等待期三个月；」

### C14. 生育津贴 requires 6 months' continuous payment (the one place "连续" bites) — **confirmed**
- Quote (办法 二十二): 「申领津贴时已在本市连续缴纳职工医保（含生育保险）费满六个月。」

### C15. Employee contribution rates — **confirmed**
- Quote (办法 七1): 「用人单位的缴费比例为9.5%（其中生育保险缴费比例为0.6%，下同），职工个人的缴费比例为2%」

### C16. Hangzhou 居民医保 continuity bonus (resets after a break) — **confirmed, 居民医保 only**
- Quote (实施细则 三(二十七)): 「对自2025年起连续参加居民医保满四年的参保人员，之后每连续参保一年，提高大病保险最高支付限额5000元。」「断保之后再次参保的，连续参保年数重新计算。」 (cap 「不超过12万元」)

### C17. 失业代缴 in Hangzhou — **confirmed**
- Quote (办法 七6): 「失业人员在领取失业保险金期间，应缴纳的职工医保（含生育保险）费由失业保险基金支付」
- Whether a claim made now can cover past months: not checked.

## Facts for the key

**前提及其错误**
- 前提："断缴超过3个月，以前交的年限就全部清零，退休要重新交满"——错误。
- 依据：社会保险法第二十七条按"累计缴费"判断退休医保；医保办发〔2021〕43号第十二条规定缴费年限"累计计算"；杭州现行办法（杭政函〔2025〕88号，2026年1月1日施行）把年限定义为各段实际缴费和视同缴费的合计，没有任何清零条款。
- "3个月"确实是杭州的分界线，但超过3个月的后果是"中断参保"、重新缴费后有待遇等待期，断缴期间和等待期内看病医保不报；已缴的8年不受影响。
- 国办发〔2024〕38号没有职工医保断缴、补缴的条款；其中3个月固定等待期、每断1年加1个月，以及"断保后连续参保年数重新计算"，针对的都是居民医保（后者只影响大病保险的奖励额度）。

**正确数字和算法（假设8年都在杭州缴纳、3月已缴、11月新单位正常缴费）**
- 已缴：8年 = 96个月，全部保留。
- 杭州退休享受职工医保待遇的条件：本市实际缴费满10年（120个月），且累计缴费满20年（240个月，可含视同缴费年限和2002年底前连续工龄），并且在本市参保到退休。
  - 实际缴费还差：120 − 96 = 24个月。
  - 累计还差：240 − 96 = 144个月（12年），视同缴费年限可抵（因人而异）。
  - 断缴的7个月不会扣减已有年限，只是这7个月本身不计入（除非补缴）。
- 断缴月份：2026年4月至10月 = 7个月 > 3个月 → 中断参保。
- 恢复后何时报销：11月恢复缴费，"自恢复缴费月起的第三个自然月"开始享受 → 按最自然的读法为2027年1月（11月、12月、1月）。2026年11月、12月看病统筹基金不报。不中断时本应12月起享受。文件没有举例，另一种读法是2月，以经办答复为准。
- 补缴断缴期（以灵活就业身份）：
  - 2026年标准473.67元/月（4986元基数×9.5%，4986 = 99722×60%÷12）。
  - 7个月：473.67 × 7 = 3,315.69元。个人应缴的大病保险费从补划的个人账户中扣，不另外交现金。
  - 期限：补缴起始时间不得早于办理当年，所以要补2026年的月份，必须在2026年12月31日前办。
  - 效果：7个月记为实际缴费年限；补缴月份内的医疗费不报；能否免掉等待期没有核实到，须问杭州医保经办。
  - 资格：本市户籍；或本市实际缴费满10年（8年不够）；或持杭州《居住证》并在杭州办理就业登记。
  - 新单位不能替她补4–10月：单位补缴不得早于该单位为她参保的时间。
- 不补的代价：
  - 只有到退休时累计不满20年才需要补。若以后再工作满12年（或有视同年限），这7个月根本不影响退休医保。
  - 若到时不足，按2026年标准一次性缴纳为743.60元/月（99722×8.9%÷12 + 48÷12），7个月约 743.60 × 7 = 5,205.20元。这笔钱不进个人账户，且标准随省平工资每年调整。也可选按月延缴（2026年443.75元/月）。

**回答可能顺带提到的说法及正确值**
- "职工医保断缴3个月清零是38号文规定的"：错，38号文没有职工医保断缴条款。
- "断缴超过3个月要等6个月才能报销"：杭州为恢复缴费月起第三个自然月开始享受（约多等1个月）。全国43号文只说"原则上不超过6个月"，具体由统筹地区规定。【因地而异】
- "3个月内补缴待遇不中断、可追溯报销"：全国43号文第十一条只对跨统筹区转移接续或职工/居民切换、中断3个月（含）以内并补缴的情形这样规定；切换参保还要求已连续参保2年以上。她已断7个月，不适用。【因地而异】
- "断缴后个人账户清零"：错。杭州断缴期间停止划入和使用个人账户，余额保留，重新参保后可继续使用。【因地而异】
- "退休医保要交满25/30年、或必须连续缴费"：杭州是本市实际10年 + 累计20年，累计计算，不要求连续；浙江其他城市和外省规定不同。【因地而异】
- 灵活就业职工医保费率：杭州9.5%（含生育0.6%），基数为上年度省平工资60%，2026年473.67元/月。持低保边缘证者减半为236.84元/月。【杭州，按年调整】
- 在职缴费比例：杭州单位9.5%（含生育0.6%）、个人2%。【杭州】
- 生育津贴：申领时须在杭州连续缴纳职工医保满6个月，断缴会影响这一项。【杭州】
- 居民医保兜底：杭州"其他居民医保"只限本市户籍成年人。2026年个人缴费一档770元、二档670元/年，非集中参保期参保有3个月等待期。她11月已入职，没有必要。【杭州，按年调整】
- 失业保险金：若离职非本人意愿、失业保险缴满1年并办理失业登记，领金期间职工医保由失业保险基金代缴，个人不缴。是否可追溯到4月起未核实。【个案】
- 居民医保连续参保奖励（杭州：自2025年起连续满4年后每年+5000元大病限额，零报销+5000元，合计不超过12万元，断保后重新计算）：只适用于居民医保，与她的职工医保年限无关。【杭州】
- 未能核实的：浙江省级落实38号文的实施意见原文、《浙江省医疗保障条例》相关条文（官网无法访问）；杭州补缴断缴期能否免除等待期；无业期间能否按"应保未保"以灵活就业身份补缴。
