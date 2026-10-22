# Source check: zh-resignation (杭州辞职：60天+审批条款、最早离职日、未休年休假折算)

Checked 2026-10-22. Every URL listed as "opened" was opened that day.

Access notes:
- npc.gov.cn fails TLS with WebFetch. Its pages were read with curl over plain http.
- flk.npc.gov.cn (国家法律法规数据库) is a JavaScript app. It returned no law text, so the 劳动合同法 text below comes from the 国家信访局 copy, which names the national database as its source.
- rlsbt.zj.gov.cn (浙江省人社厅) reset every connection. One Zhejiang case analysis there was seen only as a search snippet and is marked that way.
- hangzhou.gov.cn refused both WebFetch and curl.

Premise in the prompt: Hangzhou employee, 2 years at this company, fixed monthly pay 12000, 4 years of total work history. Plans to hand in the resignation on Monday 2026-10-26. The contract says resignation needs 60 days' written application plus company approval, and leaving without approval forfeits that month's pay. The manager refuses and wants him to stay until January. He believes he must serve 60 days and wait for approval. All 5 days of this year's annual leave are unused.

## 1. 劳动合同法第三十七条, and whether approval is needed

- Verdict: **confirmed**. 30 days' written notice is enough (3 days in probation). The employer's consent is not required.
- URL (opened): https://www.gjxfj.gov.cn/2012-12/28/c_139960029.htm (国家信访局. Full text of the 2012 amended law. Page dated 2012-12-28; source line "国家法律法规数据库".)
- Quote, 第三十七条: "劳动者提前三十日以书面形式通知用人单位，可以解除劳动合同。劳动者在试用期内提前三日通知用人单位，可以解除劳动合同。"
- No approval needed. Ministry reply 劳办发〔1995〕324号 (1995-12-19), republished by the 攀枝花市人社局 (page dated 2016-08-03). This is an official local republication, not the ministry's own site.
  - URL (opened): http://rsj.panzhihua.gov.cn/pzhsldrszyzcy/zcwj/1056746.shtml
  - Quote: "劳动者提前三十日以书面形式通知用人单位，解除劳动合同，无需征得用人单位的同意。超过三十日，劳动者向用人单位提出办理解除劳动合同的手续，用人单位应予办理。"
- Supporting pages (opened):
  - https://rsj.sh.gov.cn/tmsztc_17502/20200617/t0035_1379494.html (上海市人社局, 2019-04-26). Quote: "劳动者只要提前三十天向用人单位提出辞职，用人单位就不得不批准。"
  - http://chinajob.mohrss.gov.cn/h5/c/2021-11-01/328835.shtml (中国就业网, 人社部 site, 2021-11-01; reprints a Sichuan court case). Quote: "劳动者只要作出辞职的意思表示，无需得到用人单位的批准或同意，通知期满后劳动关系即告解除。"
  - http://www.npc.gov.cn/zgrdw/npc/zt/2007-08/24/content_1423248.htm (中国人大网, 2007-08-24; reprints a 北京晚报 piece). Quote: "根据《劳动合同法》，劳动者从单位辞职提前30天书面告知即可。"
- Amendment check: the last amendment was 2012-12-28, effective 2013-07-01, and changed only the labour-dispatch articles. Searches found no amendment in 2025 or 2026. This cannot fully exclude an unindexed change.

## 2. Does "60 days + approval" bind an ordinary employee? Any Zhejiang or Hangzhou rule allowing longer notice?

- Verdict: **corrected**. The premise "合同是我自己签的，只能按60天走，还得等领导点头" is wrong.
  - For an ordinary employee, neither the approval requirement nor the 60-day period binds.
  - A clause that excludes the worker's statutory right is void under 劳动合同法第二十六条.
  - No Zhejiang or Hangzhou rule allowing a longer notice period was found.
- URL (opened): https://www.gjxfj.gov.cn/2012-12/28/c_139960029.htm
- Quote, 第二十六条第一款: "下列劳动合同无效或者部分无效：……（二）用人单位免除自己的法定责任、排除劳动者权利的；"
- Local rules that do allow a longer period exist only for employees with trade-secret duties, and none of them is in Zhejiang:
  - **上海市劳动合同条例 第十五条**. The prompt's "第三十七条" is wrong; the provision is 第十五条. Adopted 2001-11-15, effective 2002-05-01; no amendment shown on the page.
    - URL (opened): https://rsj.sh.gov.cn/tsrdfg_17258/20200617/t0035_1388395.html
    - Quote, 第十五条: "对负有保守用人单位商业秘密义务的劳动者,劳动合同当事人可以就劳动者要求解除劳动合同的提前通知期在劳动合同或者保密协议中作出约定,但提前通知期不得超过六个月。"
    - Quote, 第十六条: "劳动合同双方当事人约定竞业限制的,不得再约定解除劳动合同的提前通知期。"
    - Conditions: the employee owes a trade-secret duty; the period is agreed in the contract or a confidentiality agreement; it is at most 6 months; the employer may take 脱密措施 during it; and it cannot be combined with a 竞业限制 clause.
  - **江苏省劳动合同条例 (2013修订) 第二十七条**, quoted in a court article.
    - URL (opened): https://www.jsfy.gov.cn/article/93733.html (无锡市锡山区人民法院, 2022-06-23)
    - Quote: "对负有保密义务的劳动者，用人单位可以与其在劳动合同或者保密协议中，就劳动者要求解除劳动合同的提前通知期以及提前通知期内的岗位调整、劳动报酬作出约定。提前通知期不得超过六个月。"
    - In that case the court voided a clause that effectively exceeded 6 months, and voided a 30万 违约金 clause under 第二十五条.
  - **National 劳部发〔1996〕355号** (脱密期 up to 6 months for staff holding trade secrets): **could not verify**. No official page with the text was found; it was seen only in secondary summaries.
  - **Zhejiang province**: **could not verify any rule**. Searches restricted to zj.gov.cn, zjrd.gov.cn, zjhrss.gov.cn, hangzhou.gov.cn and zjcourt.cn found no provincial 劳动合同条例 and no 浙江高院 or 仲裁院 解答 on longer notice periods. Absence cannot be proven by search.
  - **Hangzhou**: 《杭州市劳动合同条例》 was **repealed in 2010**. hangzhou.gov.cn still hosts the old text (page dated 2019-07-26), so an answer citing it would be wrong.
    - URL (opened): https://hznews.hangzhou.com.cn/xinzheng/yaolan/content/2010-09/09/content_3419455.htm (杭州网, the municipal news portal; secondary, page dated 2010-09-09)
    - Quote: "杭州市第十一届人民代表大会常务委员会第二十二次会议决定，废止《杭州市劳动合同条例》"
- Seen only in a search snippet, not opened (ECONNRESET): a 浙江省人社厅 case analysis dated 2022-01-26 (https://rlsbt.zj.gov.cn/art/2022/1/26/art_1450623_58928153.html). The snippet says the arbitrators treated a "辞职须提前30天提出并经公司批准" rule as a procedure for **negotiated** resignation. **Could not verify.**
- Drafting point (secondary, opened): https://www.jiangyin.gov.cn/doc/2022/02/18/1019404.shtml (江阴市政府, 2022-02-18). Quote: "要写明是辞职的通知书，而不是申请书。" In the case it describes, a letter containing "请批示" was treated as a request for negotiated termination.

## 3. "扣发当月工资" as a penalty

- Verdict: **confirmed**: the penalty clause is unlawful. The employee may still be liable for **proven actual losses** if he leaves in breach of the law. Leaving after a proper 30-day notice is not a breach.
- URL (opened): https://www.gjxfj.gov.cn/2012-12/28/c_139960029.htm
  - Quote, 第二十五条: "除本法第二十二条和第二十三条规定的情形外，用人单位不得与劳动者约定由劳动者承担违约金。"
  - Quote, 第九十条: "劳动者违反本法规定解除劳动合同，或者违反劳动合同中约定的保密义务或者竞业限制，给用人单位造成损失的，应当承担赔偿责任。"
- 工资支付暂行规定 (劳部发〔1994〕489号, in force from 1995-01-01), republished by the 横琴粤澳深度合作区法律事务局.
  - URL (opened): https://www.hengqin.gov.cn/lab/flfg/bmgz/content/post_3729855.html
  - Quote, 第九条: "劳动关系双方依法解除或终止劳动合同时，用人单位应在解除或终止劳动合同时一次付清劳动者工资。"
  - Quote, 第十五条: "用人单位不得克扣劳动者工资。" The permitted deductions are limited to four: 个人所得税; 个人负担的社会保险费用; 法院判决、裁定要求代扣的抚养费、赡养费; and 法律、法规规定可以扣除的其他费用.
  - Quote, 第十六条: "经济损失的赔偿，可从劳动者本人的工资中扣除。但每月扣除的部分不得超过劳动者当月工资的20％。" Under the same article, the employee must still receive at least the local minimum wage.
- Zhejiang rule: 浙江省企业工资支付管理办法 (省政府令第353号, published 2017-03-02, effective 2017-05-01; no amendment shown).
  - URL (opened): https://www.gov.cn/zhengce/2021-12/21/content_5719128.htm
  - 第二十条 lists the permitted deductions (tax, social insurance and housing fund, court-ordered support, "依法由企业代扣的其他款项").
  - Quote, 第三十五条: "企业未按时足额支付工资或者克扣工资的，由人力资源和社会保障部门责令限期改正，拒不改正的，处1万元以上3万元以下的罚款；"
- Loss items if the employee does breach (劳部发〔1995〕223号, 1995-05-10).
  - URL (opened): https://www.gov.cn/zhengce/2022-08/31/content_5711266.htm
  - Quote, 第四条: "劳动者违反规定或劳动合同的约定解除劳动合同，对用人单位造成损失的，劳动者应赔偿用人单位下列损失：" The four items are 招收录用费用, 培训费用, 直接经济损失, and 劳动合同约定的其他赔偿费用.
- Case example (secondary, opened): https://sft.jl.gov.cn/jlspfw/jasf/201904/t20190428_5827866.html (吉林普法网, 2019-04-28). Quote: "公司要求叶某支付未提前三十日通知单位解除劳动合同的违约金，没有法律依据。" The page adds that the employer must prove any claimed loss.

## 4. The 30-day computation (notice delivered 2026-10-26)

- Verdict: **confirmed**: **2026-11-25 is right.**
  - 2026-10-26 is a Monday and is not counted. Day 1 is 10-27.
  - October contributes 5 days (27–31) and November contributes 25 (1–25), so day 30 is **Wednesday 2026-11-25**. It is not a statutory holiday.
  - The period ends at 24:00 on 11-25. That day is the last day of employment. The first free day, when a new job can start, is **11-26**.
- URL (opened): https://www.court.gov.cn/zixun/xiangqing/233181.html (最高人民法院, 民法典 full text)
  - Quote, 第二百零一条: "按照年、月、日计算期间的，开始的当日不计入，自下一日开始计算。"
  - Quote, 第二百零三条: "期间的最后一日是法定休假日的，以法定休假日结束的次日为期间的最后一日。期间的最后一日的截止时间为二十四时；"
- Application to labour notice (opened): http://chinajob.mohrss.gov.cn/h5/c/2021-07-12/313976.shtml (中国就业网, 2021-07-12, reprinting 湖南工人报). Quote: "该'30日'应当从陆某接到辞退通知的第二天开始计算。" The example concerns an employer's notice, but the rule is the same.
- Delivery matters. A written notice takes effect when it reaches the employer (民法典第一百三十七条, same court.gov.cn page): "以非对话方式作出的意思表示，到达相对人时生效。" If the letter is mailed, day 1 is the day after receipt. An email takes effect when it enters the system the employer designated, or otherwise when the employer knows or should know it has arrived.
- The employer may agree to an earlier date. The 2021-11-01 中国就业网 case says that if the employer approves before the 30 days run out, the relationship ends at the approval.
- Arithmetic check: computed with Python, `date(2026,10,26) + 30 days = 2026-11-25`.

## 5. Annual leave: entitlement, proration, and the payment rate

- 职工带薪年休假条例 (国务院令第514号, effective 2008-01-01)
  - Verdict: **confirmed** (5 days for 1 to under 10 years of cumulative work; he has 4 years).
  - URL (opened): https://www.gov.cn/zhengce/2007-12/16/content_2602498.htm
  - Quote, 第三条: "职工累计工作已满1年不满10年的，年休假5天；已满10年不满20年的，年休假10天；已满20年的，年休假15天。"
- 企业职工带薪年休假实施办法 (人社部令第1号, 2008-09-18)
  - Verdict: **confirmed**.
  - URL (opened): https://www.gov.cn/zhengce/2022-08/31/content_5711300.htm
  - Quote, 第十条: "按照其日工资收入的300%支付未休年休假工资报酬，其中包含用人单位支付职工正常工作期间的工资收入。"
  - Quote, 第十一条: "按照职工本人的月工资除以月计薪天数（21.75天）进行折算。……月工资是指职工在用人单位支付其未休年休假工资报酬前12个月剔除加班工资后的月平均工资。"
  - Quote, 第十二条: "（当年度在本单位已过日历天数÷365天）×职工本人全年应当享受的年休假天数-当年度已安排年休假天数。" The same article says: "折算后不足1整天的部分不支付未休年休假工资报酬". It also says that leave already granted beyond the prorated figure is not clawed back.
- Proration for an end date of 2026-11-25
  - Verdict: **confirmed** (arithmetic).
  - Days elapsed, 1 Jan to 25 Nov inclusive: **329**.
  - 329 ÷ 365 × 5 = 4.507, so **4 days** are owed; the fraction is not paid.
  - Robustness: any end date from 2026-10-19 (day 292) to 2026-12-30 gives 4 days. 11-26 (330 days) and 12-25 (359 days) also give 4.
- Payment rate on departure
  - Verdict: **confirmed: the mainstream official reading is an extra 200%.** The 300% in 第十条 includes the normal wage already paid for those working days, so the amount still owed at departure is 200% of the daily wage per day.
  - 河南省高级人民法院 and 河南省人社厅, joint typical cases (issued 2026-04-27, posted 2026-05-20).
    - URL (opened): https://zzrs.zhengzhou.gov.cn/jdal/10059149.jhtml
    - Quote: "除依法应当支付职工正常工作期间的工资收入外，还应当按照职工日工资收入的200%另行支付未休年休假工资，但该200%部分属于福利性补偿，应与劳动报酬相区分"
  - Zhejiang example: an award by the 宁波市北仑区劳动人事争议仲裁院, reported by 浙江工人日报 and reprinted on 中国就业网 (2021-11-09). It is secondary, but it is a Zhejiang award.
    - URL (opened): http://chinajob.mohrss.gov.cn/h5/c/2021-11-09/329686.shtml
    - Quote: "以此计算年休假工资为5885元（8000元÷21.75天×8天×2倍）。" The same award applies the 第十二条 departure proration.
  - 首都之窗 (北京市政府, 2022-07-05). It restates that 300% includes normal wages and does not state "200%" in words.
    - URL (opened): https://www.beijing.gov.cn/hudong/bmwd/jsjbmyyt/jsjblwjf/jsjblwjftqgz/202207/t20220705_2763392.html
- Numbers (fixed 12000, no overtime, so the 12-month average is 12000):

| Item | Value |
|---|---|
| Daily wage | 12000 ÷ 21.75 = 551.72 |
| 4 days × 551.72 × **2** (amount owed at departure) | **4413.79** |
| 4 days × 551.72 × 3 (the full 300%, which includes wages already paid) | 6620.69 |
| Wrong variant: 5 days × 2, no proration | 5517.24 |

- Alternatives the employer may choose: it can schedule the remaining leave during the notice period (条例第五条: the employer arranges leave "统筹安排"). Leave it grants beyond 4 days is not clawed back (第十二条).
- Time limit for claiming this money. The 200% is treated as non-wage compensation, so the one-year limit applies.
  - 鄂州市人社局 12333 reply (2025-06-25). Quote: "劳动关系解除或者终止的，从解除或者终止之日起计算。"
  - URL (opened): https://rsj.ezhou.gov.cn/hdjl/12333zxhf/ldgx/202506/t20250625_710508.html
  - Practice varies by region; some courts treat it as wages.

## 6. Legal basis for 21.75

- Verdict: **confirmed**. 人社部发〔2025〕2号 replaced 劳社部发〔2008〕3号 with the 21.75 value unchanged. 年工作日 is now 248 and 月工作日 20.67, because statutory holidays went from 11 to 13 days.
- URL (opened): https://www.gov.cn/zhengce/zhengceku/202501/content_6995777.htm (中国政府网. 发文字号 人社部发〔2025〕2号; 成文日期 2025-01-01)
  - Quote: "月计薪天数：（365天-104天）÷12月＝21.75天"
  - Quote: "2008年1月3日原劳动和社会保障部发布的《关于职工全年月平均工作时间和工资折算问题的通知》（劳社部发〔2008〕3号）同时废止。"
- Note: the 杭州市人社局 《劳动关系实务操作手册》 (PDF dated 2023-12-28) still cites 劳社部发[2008]3号 and 250 working days. An answer quoting it would have an outdated basis but the right 21.75.
  - URL (opened): https://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web3163/site/attach/0/2312281454591196.pdf

## 7. 劳动合同法第五十条 (termination certificate; transfer within 15 days)

- Verdict: **confirmed**.
- URL (opened): https://www.gjxfj.gov.cn/2012-12/28/c_139960029.htm
  - Quote, 第五十条第一款: "用人单位应当在解除或者终止劳动合同时出具解除或者终止劳动合同的证明，并在十五日内为劳动者办理档案和社会保险关系转移手续。"
  - Quote, 第八十九条: "用人单位违反本法规定未向劳动者出具解除或者终止劳动合同的书面证明，由劳动行政部门责令改正；给劳动者造成损害的，应当承担赔偿责任。"
- Required contents of the certificate. 劳动合同法实施条例 第二十四条, from http://www.npc.gov.cn/npc/c2/c188/201905/t20190522_122802.html (opened via curl): "应当写明劳动合同期限、解除或者终止劳动合同的日期、工作岗位、在本单位的工作年限。"
- 第五十条第二款 requires the employee to hand over his work as agreed ("劳动者应当按照双方约定，办理工作交接"). Handover is an obligation; it is not a condition for resigning.

## 8. Side claims an answer is likely to add

| Claim | Correct value | Verdict | Source |
|---|---|---|---|
| Final pay timing | National rule: pay in full at termination (工资支付暂行规定第九条). Zhejiang: "应当自办理解除或者终止劳动合同手续之日起5日内一次性结清工资" (浙江省企业工资支付管理办法第十九条). The clock starts when the termination formalities are completed, not on the last working day. | confirmed | gov.cn page in §3; hengqin page in §3 |
| Hangzhou handbook wording "自解除或者终止劳动合同之日起5日内" | A paraphrase. The regulation itself says "自办理……手续之日起" | confirmed (minor wording difference) | Hangzhou handbook PDF, p.26 |
| Severance (经济补偿) on voluntary resignation | None. 第四十六条 covers resignations under 第三十八条 (employer fault), not 第三十七条 | confirmed | gjxfj page: "（一）劳动者依照本法第三十八条规定解除劳动合同的；" |
| Arbitration limitation period | One year from when the employee knew or should have known (劳动争议调解仲裁法第二十七条). Wage arrears during employment are not time-barred, but once employment ends the claim must be filed within one year | confirmed | http://www.npc.gov.cn/c2986/c4488/201905/t20190523_48437.html (curl). Quote: "劳动争议申请仲裁的时效期间为一年。仲裁时效期间从当事人知道或者应当知道其权利被侵害之日起计算。" |
| 12333 | 人社 national service hotline (consultation, complaints, reports) | confirmed | http://chinajob.mohrss.gov.cn/c/2025-04-11/430729.shtml ("12333人社咨询服务热线") |
| Written notice: wording | Call it a notice (通知), not an application (申请), and do not write "请批示" | confirmed (secondary: municipal government page reporting a lawyer and a case) | jiangyin.gov.cn page in §2 |
| Written notice: proof of delivery (EMS with tracking, email, a copy signed by HR) | Legal basis: delivery takes effect on arrival (民法典第一百三十七条). No official page recommending EMS specifically was found; that advice is standard practice | basis confirmed; EMS advice could not verify as official guidance | court.gov.cn 民法典 page |
| A 60-day or longer notice period allowed for trade-secret staff | Only by local regulation, in Shanghai (第十五条) and Jiangsu (第二十七条): up to 6 months, agreed, trade-secret duty required. None found for Zhejiang | confirmed for Shanghai and Jiangsu; Zhejiang could not verify (none found) | §2 |
| 杭州市劳动合同条例 still applies | Repealed in 2010 | corrected | §2 |
| Employee owes losses for leaving without notice | Only actual, proven losses (第九十条; 劳部发〔1995〕223号第四条). Not a fixed month's pay | confirmed | §3 |
| Employer may deduct losses from wages | Only under 工资支付暂行规定第十六条: per contract, at most 20% a month, and not below the minimum wage. Not as a penalty | confirmed | hengqin page |
| Unused-leave claim time limit | Regional practice: one year from termination; the 200% treated as non-wage | confirmed as practice; not uniform | ezhou and zhengzhou pages |

## Facts for the key（答案要点）

- **前提错误一："合同签了就只能按60天走"。** 劳动合同法第三十七条规定，提前三十日书面通知即可解除（试用期三日）。合同另写60天、要求批准，属于"排除劳动者权利"（第二十六条），对普通员工不发生效力。原劳动部办公厅劳办发〔1995〕324号明确："无需征得用人单位的同意。"
- **前提错误二："还得等领导点头"。** 辞职是单方通知，不需要批准。领导"不批"、要求干到明年1月，都没有法律依据。辞职信要写成"通知"，不要写"申请""请批示"，以免被认定为协商解除。
- **地方规定：** 只有上海（劳动合同条例第十五条）和江苏（劳动合同条例第二十七条）允许对负有商业秘密保密义务的劳动者约定不超过6个月的提前通知期，而且须事先约定；上海还规定不能与竞业限制并用。浙江省未找到类似规定。《杭州市劳动合同条例》已于2010年废止，引用它就是错的。
- **"扣发当月工资"违法：** 违约金只限服务期（第二十二条）和竞业限制（第二十三条）两种情形（第二十五条）。工资只能依法代扣个税、社保等法定项目（工资支付暂行规定第十五条；浙江省企业工资支付管理办法第二十条），克扣工资可被责令改正，并处1万至3万元罚款（浙江办法第三十五条）。劳动者只有违法解除、给单位造成实际损失时才赔偿（第九十条），而且损失要由单位举证；提前30天通知不属于违法解除。
- **最早离职日：** 10月26日（周一）当面交付或送达的，当日不计入（民法典第二百零一条），第30天是**2026年11月25日（周三）**，不是节假日，当天24时期满。11月25日是最后在职日，11月26日起可入职新单位。邮寄的，从单位收到之次日起算。单位同意的，可以更早离职。
- **未休年假：** 累计工作4年，全年5天（条例第三条）。离职折算：329÷365×5=4.51，取**4天**（实施办法第十二条，不足1天的部分不付）。日工资=12000÷21.75=**551.72元**（月工资为前12个月剔除加班工资后的平均数）。
  - 离职时应补发：4×551.72×2=**4413.79元**。300%里已包含正常工资，额外应付200%：河南高院与河南省人社厅2026年典型案例、宁波北仑仲裁院裁决（按"×2倍"计算）均如此。
  - 4×551.72×3=6620.69元是含已发工资的300%总额，若作为"额外再付"就重复计算了。
  - 单位也可以在通知期内安排休假代替支付。
- **21.75的依据：** 现行为人社部发〔2025〕2号（2025-01-01），劳社部发〔2008〕3号已废止，21.75不变（年工作日改为248天，月工作日20.67天，与计薪无关）。
- **离职手续：** 单位应在解除时出具解除证明，15日内办理档案和社保转移（第五十条）。证明应写明合同期限、解除日期、工作岗位、本单位工作年限（实施条例第二十四条）。工资：国家规定解除时一次付清；浙江规定办理解除手续之日起5日内一次性结清。主动辞职没有经济补偿（第四十六条）。
- **维权：** 12333咨询或投诉；劳动仲裁时效一年（劳动争议调解仲裁法第二十七条），未休年假工资一般从离职之日起算一年。
- **容易写错的地方：**
  - 引用"上海条例第三十七条"（应为第十五条），或说浙江/杭州也允许6个月。
  - 引用已废止的杭州条例，或引用劳社部发〔2008〕3号作为现行依据。
  - 把最早离职日算成11月24日（把交信当天算进去）或12月25日（按60天）。
  - 未休年假不折算、按5天算，或按300%额外支付；用20.67或20.83折算日工资。
  - 说辞职有经济补偿，或说必须交接完毕才能走。
