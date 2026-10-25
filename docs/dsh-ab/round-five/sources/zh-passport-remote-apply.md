# 异地办护照（周口户籍、住深圳、春节去新加坡）: source check

Checked 2026-10-25. All URLs were opened on that date. Most were downloaded with curl and converted to text. The Guangdong service-portal page would not render, so it was tried in a browser and not used. Quotes are verbatim, in the original language, two lines at most. Some NIA pages put stray spaces around numbers and quotation marks, and those spaces are dropped here. "Source date" is the date of the document itself.

Request being keyed (prompts/zh-passport-remote-apply.txt): The user's 户口 is in 河南周口. The user and the mother both live in 深圳, and the user works there. Neither has a passport. Both ID cards are valid, and neither is 登记备案的国家工作人员. They plan a trip of five or six days to Singapore at Spring Festival 2027 ("2027年2月初"). The mother and colleagues say a passport can only be issued at the 户籍地 出入境办 and "异地办不了，这是规定". The user accepts this and plans to take both of them back to 周口 in mid-November (for example leaving Friday 11月13日). The user asks for three things:
- how many days of leave to take,
- the cost of round-trip high-speed rail for two plus two passports,
- how long a passport takes, and whether it will arrive before Spring Festival.

## Item checks

### 1. Since 2019-04-01, ordinary passports are 全国通办: apply at any exit-entry window, same procedure as at the 户籍地
- Verdict: **confirmed**
- URL: https://www.nia.gov.cn/n741440/n741577/c1015032/content.html (国家移民管理局, 政策解读, source date 2019-03-26)
- Quote: "自2019年4月1日起，中华人民共和国普通护照、往来港澳通行证、往来台湾通行证等出入境证件实行“全国通办”，即内地居民可在全国任一出入境管理窗口申请办理上述出入境证件，申办手续与户籍地一致。"
- Quote (same page): "内地居民都能办，即不受户籍地、居住地等条件限制，内地居民均可在异地申办出入境证件"
- The same page states the purpose directly: "今后内地居民不再需要为办证专程往返户籍地". It also names the user's case: "有关公司企业外地员工出国出境不再需要回户籍地办理出入境证件".
- Shenzhen police Q&A (https://ga.sz.gov.cn/JMHD/YWZSK/CRJGL_ZS/content/post_10660148.html, 深圳市公安局, source date 2023-06-20): "内地居民自2023年5月15日起，可以向全国任一公安机关出入境管理窗口申请办理中华人民共和国普通护照，往来港澳通行证及赴香港或澳门探亲、团队旅游、逗留、其他等4类签注，往来台湾通行证。" The 2023-05-15 date is when four kinds of 港澳 endorsements were added. Passports have been 全国通办 since 2019-04-01.

### 2. No 居住证, job, school or kinship proof is needed for an 异地 application
- Verdict: **confirmed**
- URL: https://www.nia.gov.cn/n741435/n907688/n932720/n1008173/n1008190/n1008509/n1008572/c1010770/content.html (国家移民管理局, "4月1日起内地居民申领出入境证件实行“全国通办”", source date 2019-03-27)
- Quote: "群众异地申办上述证件与户籍地申请手续一致，无需再提交居住证、就业、就学、亲属关系证明等材料。"
- URL: http://gat.hubei.gov.cn/bmdt/ztzl/2021n/zcwdpt/xczxzcwd/202112/t20211201_3892935.shtml (湖北省公安厅, 普通护照签发常见问题解答（三）, source date 2021-12-01), Q43
- Quote: "实施“全国通办”，取消了户籍地、居住地等条件的限制，异地申请办理普通护照不需要提交居住证。"
- The same answer appears at https://www.wuzhong.gov.cn/ztzl/zcwdpt/wzsgaj_72080/202311/t20231123_4360840.html (吴忠市人民政府, 2023-11-23).
- Note: the user does not need a 深圳居住证 or social-insurance record. (The user probably has both anyway.)

### 3. The statute text still says 户籍所在地. This is where the premise comes from, and it is not how passports are issued now
- Verdict: **confirmed** that the statute reads this way. It has been **superseded in practice** by 全国通办.
- URL: http://www.npc.gov.cn/c2/c183/c198/201905/t20190522_25538.html (《中华人民共和国护照法》, adopted 2006-04-29, in force 2007-01-01; also on nia.gov.cn c1014017)
- Quote (Art. 5): "由本人向户籍所在地的县级以上地方人民政府公安机关出入境管理机构申请普通护照。"
- Quote (Art. 6): "公民申请普通护照，应当提交本人的居民身份证、户口簿、近期免冠照片以及申请事由的相关材料。"
- The NIA's own current implementing standard drops "户籍所在地". URL: https://www.nia.gov.cn/n741440/n741587/n1316094/n1355872/c1614514/content.html (《普通护照签发（省级）实施规范》, source date 2023-12-01), 八（一）1.(1):
- Quote: "公民因前往外国定居、探亲、学习、就业、旅行、从事商务活动等非公务原因出国的，由本人向县级以上地方人民政府公安机关出入境管理机构申请普通护照。"
- Note: the Shenzhen service guide (item 6) still quotes Art. 5 under 设定依据, and its own 通办范围 is "全国". An answer that cites Art. 5 as proof that the applicant must go back is wrong in practice. If an answer mentions the article at all, it should say that 全国通办 has applied nationwide since 2019. The State Council's new exit-entry regulation (item 19) did not change this.

### 4. Materials for a first adult passport: photo, application form, 居民身份证. No 户口簿, no 居住证. Registered state personnel need unit consent, which does not apply here
- Verdict: **confirmed**
- URL: https://www.nia.gov.cn/n741440/n741587/n1316094/n1355872/c1614514/content.html (实施规范, 2023-12-01), 九（一）1
- Quote: "（3）居民身份证，在居民身份证领取、换领、补领期间，可以提交临时居民身份证；"
- Quote: "（5）登记备案的国家工作人员除提交第（1）（2）（3）项的申请材料外，还应提交本人所属工作单位或者上级主管单位按照人事管理权限审批后出具的同意办理普通护照的意见；"
- The other items are (1) a photo meeting 《出入境证件相片照相指引》 and (2) 中国公民出入境证件申请表. The list has no 户口簿, although Art. 6 of the statute names it. The request says neither person is registered state personnel, so the unit-consent letter does not apply.

### 5. Fee: 120 元 per passport since 2019-07-01 (was 160 元). No surcharge for applying 异地
- Verdict: **confirmed**
- URL: https://www.nia.gov.cn/n741440/n741542/c1057039/content.html (国家移民管理局通知公告, source date 2019-06-24)
- Quote: "自2019年7月1日起，全国公安机关出入境管理部门降低普通护照、往来港澳通行证收费标准，普通护照由每本160元降为每本120元"
- URL: c1614514 (实施规范, 2023-12-01), 十三: "根据《国家发展改革委、财政部关于降低部分行政事业性收费标准的通知》（发改价格〔2019〕914号），普通护照收费标准为120元/本。"
- Shenzhen guide (item 6): "收费标准 120元", basis 发改价格〔2019〕914号.
- Hubei Q&A (item 2 URL), Q45: "不会额外收费，无论您在本地或异地申办普通护照，都执行国家统一的收费标准。"
- Two passports: 2 × 120 = **240 元**. Photo costs are separate (item 16).

### 6. Shenzhen's own service guide: open to non-Guangdong residents, no 居住证 on the list, open Monday to Saturday, 10 working days for non-Guangdong 户籍, mail delivery available
- Verdict: **confirmed**. The page carries no date. Local practice can change: **varies**.
- URL: http://wsbs.sz.gov.cn/shenzhen/project/phoneGuide?code=00754268901001650013440300 (广东省网上办事大厅深圳分厅, 事项 "办理及加注普通护照", 主管部门 深圳市公安局; undated, read 2026-10-25)
- Quote: "服务对象 广东省户籍居民、驻深部队的现役军人及符合条件的非广东省户籍居民" / "通办范围 全国"
- Quote (窗口办理流程, 注): "1.急事急办的，5个工作日内办结 2.非广东省户籍居民10个工作日办结 3.公安机关认为需要调查的，调查时间不计入承诺办结时限"
- Quote: "市局将审批结果报送省厅，省厅2个工作日内制作、签发证件（不计入承诺办理时限）。"
- Quote (every Shenzhen 出入境 hall listed): "办理时间：周一至周六，上午：9:00—12:00，下午：14:00—18:00（法定节假日除外）"
- Quote: "申请人按约定的方式到递交申请的受理点或邮递领取。" The page also shows "物流快递 支持物流快递".
- Quote: "网上预约后，根据预约日期、时间、受理点取号排队，到窗口提交申请材料。"
- The materials listed are: application form, photo receipt, ID card, guardian ID and birth certificate (under 16 only), unit consent letter (registered personnel and military only), military ID, proof of settlement abroad, and the old passport (renewals). **No 居住证 and no 户口簿.**
- The headline "承诺办结时限 5（工作日）" is for Guangdong 户籍. The note gives 10 working days for non-Guangdong 户籍, plus up to 2 working days for provincial production that are not counted.
- Inconsistency: the page also shows "法定办结时限 30（工作日）". The statute says 15 days, extendable to 30 (item 8). This number is not used in the key.

### 7. Promised issue time: 7 working days at the 户籍地; 20 days for a cross-province 异地 application
- Verdict: **confirmed**
- URL: https://www.nia.gov.cn/n741440/n741587/n1316094/n1355872/c1614514/content.html (实施规范, 2023-12-01), 十二（三）承诺审批时限
- Quote: "居民在户籍地公安机关出入境管理机构申请普通护照应当自受理申请材料之日起七个工作日内审批签发并制作普通护照。跨省异地申请普通护照的签发时限为二十日。"
- URL: https://ka.sz.gov.cn/xxgk/qt/gzdt/content/post_11496546.html (深圳市人民政府口岸办公室, "出国游护照三连问，一篇讲清楚", source date 2024-08-14)
- Quote: "向户籍地公安机关出入境管理机构申请普通护照的签发时限为7个工作日。跨省异地申请普通护照的签发时限为20日。"
- Notes:
  - 河南 to 广东 is cross-province, so the 20-day figure applies. Neither source says whether these are working days or calendar days. Item 22 works out both readings.
  - In Shenzhen the stated practice is faster: 10 working days for non-Guangdong 户籍, plus up to 2 working days for production (item 6).
  - **Common wrong values:** "7个工作日" applied to an 异地 application (7 working days is the 户籍地 figure); "15个工作日"; "一个月以上".

### 8. Statutory limit: 15 days, extendable to 30 in special cases
- Verdict: **confirmed**
- URL: http://www.npc.gov.cn/c2/c183/c198/201905/t20190522_25538.html (护照法 Art. 6)
- Quote: "公安机关出入境管理机构应当自收到申请材料之日起十五日内签发普通护照"
- Quote: "在偏远地区或者交通不便的地区或者因特殊情况，不能按期签发护照的，经护照签发机关负责人批准，签发时间可以延长至三十日。"
- The 实施规范 (c1614514, 十二（二）1) repeats this word for word. The 20-day 异地 promise in item 7 is longer than the 15-day base. It is still inside the 30-day maximum.

### 9. Expedited issue (加急): 5 working days, only for listed emergencies. A holiday trip does not qualify
- Verdict: **confirmed**
- URL: c1614514 (实施规范, 2023-12-01), 十二（二）2
- Quote: "出国奔丧、探望危重病人的；前往国入境许可或者签证有效期即将届满的；紧急出国出境参加会议谈判、签订合同；出国留学报到时间临近、行前证件遗失损毁；"
- Quote: "公安机关出入境管理机构应当自收到申请材料之日起五个工作日签发。"
- Leisure travel is not on the list. The last listed ground is a residual one: "省级地方人民政府公安机关出入境管理机构认可的其他紧急事由". Shenzhen's version is "急事急办的，5个工作日内办结" (item 6). The user has about 12 weeks, so no expediting is needed.

### 10. Both applicants must appear in person and give fingerprints
- Verdict: **confirmed**
- URL: https://ka.sz.gov.cn/xxgk/qt/gzdt/content/post_11496546.html (深圳口岸办, 2024-08-14)
- Quote: "申请人提交申请材料并按规定采集指纹信息后，受理机构对符合申请条件、申请材料齐全且符合法定形式的居民将出具《受理申请回执单》"
- Statute: "由本人…申请普通护照" (护照法 Art. 5). The user cannot apply on the mother's behalf. They can book the same slot and go together.

### 11. Online booking, and the national NIA platform
- Verdict: **confirmed**
- URL: c1015032 (NIA, 2019-03-26): the platform launched on 2019-04-01 and "具备证件预约申请、往来港澳台旅游签注办理、证件进度查询…等功能"
- URL: c1010770 (NIA, 2019-03-27): "申请人可以在线预约申请护照…在线填写申请表，预约办证时间和地点。后续再按照预约时间到受理大厅提交申请材料，完成指纹采集、照相、缴费等手续。"
- Shenzhen: see item 6 ("网上预约后，根据预约日期、时间、受理点取号排队"). Third-party guides say booking goes through the 深圳市公安局 website or the 深圳公安 WeChat account. That channel was **not verified**: the Shenzhen booking site (msjw.ga.sz.gov.cn) returned a Tencent Cloud WAF block page on 2026-10-25.

### 12. Collection by mail
- Verdict: **confirmed** for Shenzhen. The postage fee was **not verified**.
- URL: wsbs.sz.gov.cn guide (item 6): "申请人按约定的方式到递交申请的受理点或邮递领取。" / "支持物流快递"

### 13. "全程网办" (online-only) is for renewals and replacements, not for a first passport
- Verdict: **confirmed** (added; a likely wrong side claim)
- URL: https://ga.sz.gov.cn/ZWGK/ZCFG/SZZCFGS/JD_CRJGL/content/post_12460956.html (深圳市公安局 repost of the NIA announcement dated 2024-04-28, measures in force 2024-05-06; page date 2025-10-28)
- Quote: "20个城市16周岁以上户籍居民（国家工作人员和现役军人除外）申请换发补发普通护照、往来港澳通行证、往来台湾通行证，可以通过国家移民管理局政务服务平台网上提交申请"
- Two things rule this out for the user and the mother. They apply for a first passport (首次申请), not a renewal or replacement. They are 户籍居民 of 周口, which is not one of the 20 cities. Shenzhen is on the list, but only for Shenzhen-registered residents.

### 14. Passport validity: 10 years for applicants aged 16 or over
- Verdict: **confirmed**
- URL: npc.gov.cn (护照法 Art. 7): "普通护照的有效期为：护照持有人未满十六周岁的五年，十六周岁以上的十年。"
- A new passport therefore easily meets Singapore's six-month validity rule (item 17).

### 15. Singapore: PRC ordinary-passport holders have been visa-exempt for stays of up to 30 days since 2024-02-09
- Verdict: **confirmed**
- URL: https://www.ica.gov.sg/news-and-publications/newsroom/media-release/mutual-30-day-visa-exemption-arrangement-between-singapore-and-the-people-s-republic-of-china (ICA media release, source date 25 January 2024)
- Quote: "With effect from 9 February 2024, holders of ordinary passports issued by the People’s Republic of China (PRC) will be exempted from visa requirements for a stay of up to 30 days in Singapore."
- URL: https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements (ICA, "Last updated on 25 June 2026"). China is not on the visa-required list. The only PRC entry is "A PRC Travel Document", and the page notes that it means documents other than "ordinary, diplomatic, public affairs or service PRC passports".
- URL: https://sg.china-embassy.gov.cn/lsfw_0/zytz/202408/t20240815_11474255.htm (中国驻新加坡使馆, source date 2024-08-15)
- Quote: "中国公民来新从事旅游、探亲、商务等私人事务，停留不超过30日，持普通护照人员可免签入境。"
- Also at https://wb.beijing.gov.cn/home/wswm/crjxx/qzxx/qztz/202402/t20240205_3557072.html (北京市外办, 2024-01-25): the agreement "将于2024年2月9日（农历除夕）正式生效".
- Wrong values seen in circulation: "需要办新加坡电子签证"; "免签15天". The 15-day figure was China's unilateral entry exemption for Singaporeans from 2023-07-26, the other direction.

### 16. Cumulative cap on visa-free stays (for example "90 days in any 180 days")
- Verdict: **could not verify**. The ICA, Chinese-embassy and Beijing FAO pages checked give only the 30-day single stay. MFA pages (mfa.gov.cn) showed "系统维护" on 2026-10-25. This does not matter for a trip of five or six days. The key should not assert any cumulative cap.

### 17. Singapore entry formalities: passport valid at least 6 months; SG Arrival Card within 3 days before arrival (free)
- Verdict: **confirmed**
- URL: https://www.ica.gov.sg/enter-transit-depart/entering-singapore (ICA, "Last updated on 29 September 2026")
- Quote: "All travellers, except Singapore passport holders, must ensure their passport has a minimum validity of 6 months."
- URL: https://www.ica.gov.sg/enter-transit-depart/entering-singapore/sg-arrival-card (ICA, "Last updated on 18 September 2024")
- Quote: "You are required to submit the SGAC within three (3) days (including the day of arrival) before arrival in Singapore." / "SGAC submission is free of charge."
- The same page advises short-term visitors to carry "sufficient cash and proof of onward travel". The Chinese embassy notice (item 15) repeats "确保护照有效期在6个月以上，在抵达新加坡前3天内填妥电子入境卡".

### 18. Spring Festival 2027 dates, and whether the 2027 holiday schedule is out
- Verdict: **confirmed** for the lunar dates. The 2027 mainland holiday schedule (放假调休安排) was **not published** as of 2026-10-25, judged by search.
- URL: https://www.gov.hk/en/about/abouthk/holiday/2027.htm (GovHK, gazetted list of 2027 general holidays): "Lunar New Year’s Day" is "6 February". So 正月初一 is Saturday 2027-02-06 and 除夕 is Friday 2027-02-05.
- URL: https://www.gov.cn/zhengce/content/202411/content_6986380.htm (国务院令, 发布 2024-11-12, in force 2025-01-01)
- Quote: "（二）春节，放假4天（农历除夕、正月初一至初三）"
- The statutory Spring Festival days in 2027 are therefore 2027-02-05 to 2027-02-08 at least. The full schedule with make-up workdays comes in a 国务院办公厅 notice. The 2025 notice came out on 2024-11-12 and the 2026 notice on 2025-11-04. No 2027 notice was found.

### 19. The new State Council exit-entry regulation (in force 2026-09-15) does not change where to apply
- Verdict: **confirmed** from the official Xinhua release and the ministries' Q&A. The full gov.cn text was **not read**.
- URL: https://www.news.cn/20260731/64967b5190314a548e70e6f2ac3c079a/c.html (新华社, source date 2026-07-31)
- Quote: "国务院总理李强日前签署国务院令，公布《国务院关于出境入境管理的规定》（以下简称《规定》），自2026年9月15日起施行。"
- Quote: "规定出境入境人员申请出境入境、停留居留的事由应当真实、合法，并配合移民管理机构、签证机关核实身份、申请事由"
- The Q&A (https://www.news.cn/20260731/5c1de9dcf080464d850758ef61d6ca5f/c.html) covers four areas: exit safety warnings, truthful application reasons, new exit and entry bans, and registration of intermediaries. None concerns where a passport can be applied for, issue times or fees. 深圳市公安局 confirms the start date in a Q&A of 2026-10-20 (https://ga.sz.gov.cn/JMHD/YWZSK/CRJGL_ZS/content/post_13030954.html): "应自该规定施行之日（2026年9月15日）起90日内办理备案手续".

### 20. No newer NIA measure changes passport applications by mainland residents
- Verdict: **confirmed** (as far as the NIA listings show)
- URL: https://www.nia.gov.cn/n741440/n741542/index.html (通知公告; newest item 2026-10-18). Items from 2025 to 2026 cover recruitment, foreigners' lodging registration, visa-free transit, border passes and intermediary registration. None changes ordinary-passport applications.
- URL: https://www.nia.gov.cn/n741440/n741577/index.html (政策解读; newest items 2026-09-21, 2026-08-20, 2026-07-31). None changes 全国通办, issue times or fees.

### 21. Photos: rules and cost
- Verdict: **varies** (local practice). The cost is **not verified**.
- URL: wsbs.sz.gov.cn guide (item 6), 申请人相片:
- Quote: "1.按照广东省出入境证件数字相片采集回执提交；2.属 60岁（含）以上申请人且在5年内曾成功申办过出入境证件或居民身份证的，可免交《广东省出入境证件数字相片采集回执》。"
- Hubei, for comparison (item 2 URL, Q54): "须在出入境部门内的社会服务照相点采集出入境证件电子照（一年内已采集或仅办理单独签注的可免）。"
- The request does not give the mother's age. If she is 60 or over and has had an ID card or exit-entry document issued in the past 5 years, she may not need the photo receipt in Shenzhen. No official price for the photo receipt was found. Third-party pages say Shenzhen halls have photo points. A claim that photos are "free nationwide" could **not be verified**.

### 22. High-speed rail fare and journey time, 深圳北 to 周口东 (only matters if they went back)
- Verdict: **could not verify on an official source**. 12306's query API returned an empty response to an unauthenticated request. The figures below come from a third-party listing (Ctrip) for trains on 2026-10-26.
- URL: https://trains.ctrip.com/trainbooking/shenzhen-zhoukou/dongche (read 2026-10-25): one direct train, "G2694", 深圳北 11:37 → 周口东 21:16, "9时39分", "二等座 782.5", 一等座 1254.5.
- URL: https://trains.ctrip.com/trainbooking/zhoukou-shenzhen/dongche (read 2026-10-25): "G2693", 周口东 10:17 → 深圳北 20:36, "10时19分", "二等座 822.5".
- One-change itineraries were listed at 687.5 to 765.5 元 second class and take 9 to 11 hours. Fares on some lines float by date, so a mid-November fare may differ. **[varies]**
- Arithmetic: per person round trip 782.5 + 822.5 = 1,605 元. Two people: 2 × 1,605 = **3,210 元** in second class. With two passports: 3,210 + 240 = **3,450 元**. That excludes the local transfer from 周口东 to town, meals, lodging and lost pay. The 12306 station codes are confirmed (station_name.js): 深圳北 IOQ, 周口东 ZKF, 周口 ZKN.
- Journey time: the direct train arrives at 21:16. Applying at the 周口 office would therefore take at least three days (travel, apply, return), unless the timing worked out exactly. Collecting the passports would then mean waiting about 7 working days in 周口, a second trip, or mail delivery. Mail delivery in 周口 was **not verified**.

## Arithmetic for the timeline (request needs it)

Assume they apply in Shenzhen on **Saturday 2026-11-14**. Halls are open Monday to Saturday (item 6), so no leave is needed. Day counts start the next day.

| Basis | Date passports are due | Weekday |
|---|---|---|
| NIA promise, cross-province, 20 days read as calendar days | 2026-12-04 | Fri |
| Same 20 days read as working days | 2026-12-11 | Fri |
| Shenzhen practice: 10 working days for non-Guangdong 户籍 | 2026-11-27 | Fri |
| Plus up to 2 working days for provincial production (not counted in the promise) | 2026-12-01 | Tue |
| Statutory 15 days | 2026-11-29 | Sun |
| Statutory maximum 30 days | 2026-12-14 | Mon |
| For comparison, 户籍地 7 working days, if applied in 周口 on 2026-11-16 (Mon) | 2026-11-25 | Wed |

- 除夕 2027-02-05 is 83 days after 2026-11-14. Under the slowest reading (30 days) the passports are due on 2026-12-14, more than seven weeks before departure. Mail delivery adds a few days.
- **Latest safe application date**, to hold passports by 2027-02-03:
  - 20 working days, with 2027-01-01 a holiday: apply by **Wednesday 2027-01-06**.
  - 20 calendar days: apply by **Thursday 2027-01-14**.
  - Applying in November, as the user plans, leaves a large margin. They could also apply sooner, on any Saturday.
- **Leave:** 0 days if they apply on a Saturday in Shenzhen. A weekday slot at lunchtime would also work. The user's plan to go back to 周口 would take about 3 days of leave and roughly 3,210 元 in rail fares.

## Facts for the key

**The premise and why it is wrong.** "办护照必须回户口所在地，异地办不了" is false. Since **2019-04-01**, ordinary passports have been **全国通办**. A mainland resident can apply at **any** 公安机关出入境管理窗口 in the country, with the same procedure and materials as at the 户籍地. There is no 户籍地 or 居住地 restriction, and **no 居住证** is needed (NIA 2019-03-26 and 2019-03-27; NIA 实施规范 2023-12-01). Both people can apply in **深圳**. They do not need to go back to 周口. The NIA even gives this as the reason for the reform ("不再需要为办证专程往返户籍地"). The premise sounds plausible for two reasons:
- 护照法 Art. 5 (2006) still says "户籍所在地".
- Before 2019, 异地 applications were limited.

Current NIA rules and the Shenzhen service guide accept applicants from other provinces.

**Correct figures:**
- Fee: **120 元/本** (since 2019-07-01; it was 160 元). Two passports: **240 元**. No 异地 surcharge. Photo receipt costs are extra and vary.
- Issue time: the official promise for a cross-province 异地 application is **20 days** (the source does not say whether working or calendar days). The 户籍地 promise is 7 working days. Shenzhen's own guide says **10 working days** for non-Guangdong 户籍, plus up to 2 working days for production. The statutory limit is 15 days, extendable to 30. The key should read: **official limit 20 days, often faster in practice.** Applied in mid-November, the passports arrive by early or mid-December at the latest, well before 除夕 (2027-02-05). Expediting (5 working days) is only for listed emergencies and is not needed.
- Validity: 10 years for applicants aged 16 or over.

**What a correct answer must also say:**
1. Correct the premise plainly and recommend applying in Shenzhen. No leave or return trip is needed. The ~3,210 元 rail fare and about 3 days of leave are saved.
2. Steps: book online (the 深圳市公安局 channel or the NIA platform). Both go **in person** to a Shenzhen 出入境 hall (open Monday to Saturday) with valid **身份证** and a photo receipt meeting the standard. Fill in the application form, give fingerprints and pay 120 元 each. Collect at the hall or choose mail delivery.
3. Materials: ID card, photo receipt and application form. No 户口簿, 居住证 or social-insurance proof. The request rules out the registered-state-personnel unit letter.
4. Timeline: mid-November is fine. The latest prudent date is around early January 2027 (by 2027-01-06 under a 20-working-day reading). It is better to do it now or in November.
5. Singapore: a PRC ordinary passport is **visa-exempt for up to 30 days** (since 2024-02-09). The passport must be valid for at least 6 months, which a new one is. Submit the **SG Arrival Card within 3 days before arrival**; it is free. Carry proof of onward travel.

**If the answer still gives a 周口 plan (it should not be the recommendation):**
- Rail (third-party listing, not 12306): G2694 深圳北→周口东, 二等座 782.5 元, 9h39m. G2693 back, 822.5 元. Two people round trip about **3,210 元**, plus 240 元 for passports, about **3,450 元**. At least 3 days away.
- Applied in 周口, the 户籍地 promise is 7 working days. Collecting means waiting there, making a second trip, or mail delivery (not verified for 周口).

**Side claims an answer is likely to add, with correct values:**
- "异地办护照要7个工作日": **wrong**. 7 working days is the 户籍地 promise. Cross-province 异地 is 20 days (Shenzhen practice: 10 working days for non-Guangdong).
- "护照费160元" or "200元": **wrong**. It has been 120 元 since 2019-07-01.
- "异地办需要居住证、社保或在当地住满半年": **wrong**. No 居住证 or other proof is needed (NIA 2019; Hubei and Wuzhong Q&As).
- "需要带户口本": **wrong** under the current material list (身份证 only). 护照法 Art. 6 still names 户口簿, but the NIA 实施规范 does not.
- "可以在网上全程办理 / 全程网办，不用跑": **wrong** for a first passport. Online-only service is for renewals and replacements by 户籍居民 of 20 pilot cities.
- "可以加急": **wrong for this trip**. Expediting is only for listed emergencies such as 奔丧, a critically ill relative or an expiring visa.
- "可以帮妈妈代办": **wrong**. Each applicant aged 16 or over must apply in person and give fingerprints.
- "新加坡需要签证 / 电子签 / 免签15天": **wrong**. Since 2024-02-09 the exemption is 30 days. A cumulative cap (90/180) was **not verified** and should not be asserted.
- "新加坡入境护照有效期需6个月以上": **correct** (ICA). "抵达前3天内填电子入境卡（SGAC），免费": **correct**.
- "春节是2月6日 / 除夕2月5日": **correct**. The 2027 mainland holiday schedule was not yet published as of 2026-10-25. Statutory Spring Festival holiday is 4 days (除夕 to 初三).
- "新出台的《国务院关于出境入境管理的规定》要求回户籍地": **wrong**. The regulation (in force 2026-09-15) covers truthful application reasons, exit bans, safety warnings and intermediaries, not where to apply.
- Photo cost, whether photos are free, the exact booking channel and postage are local practice: **[varies; not verified]**. In Shenzhen, applicants aged 60 or over with an ID card or exit-entry document issued in the past 5 years may skip the photo receipt.
