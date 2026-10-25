# zh-flex-hours：对抗性核查（"Facts for the key" 部分）

Checked 2026-10-22 by an independent checker. Only `zh-flex-hours.md` was read from disk. Every URL below was opened on 2026-10-22, by WebFetch, curl, or a read of an already-open built-in browser tab. Quotes are copied from the page, two lines at most.

Limits on this check:
- The WebSearch budget for this turn ran out after one query. Newer-rule checks were therefore done by opening official listing pages directly: the rsj.beijing.gov.cn policy list, the court.gov.cn judicial-interpretation list, and Beijing's 2025 list of abolished documents.
- mohrss.gov.cn served a bot-check script page to curl and WebFetch. I did not try to get past it, and all built-in browser tabs were in use by other agents.

Result: **31 facts. 26 stand, 3 need change (#3, #8, #18), 2 could not be decided (#25, #27).**

---

## 前提及其错误

### 1. 综合工时须经劳动行政部门批准（劳动法第三十九条）: **stands**
- URL: http://www.npc.gov.cn/zgrdw/npc/xinwen/2019-01/07/content_2070261.htm (fetched by curl; the page header shows the 2018-12-29 second amendment)
- Quote: "第三十九条　企业因生产特点不能实行本法第三十六条、第三十八条规定的，经劳动行政部门批准，可以实行其他工作和休息办法。"

### 2. 北京现行规定是京劳社资发〔2003〕157号；第四条要求"经申报、批准"；第十五条规定向注册地区局申报: **stands**
- URL: https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/200804/t20080409_567083.html (page field 有效性: 是)
- Quote (第四条): "企业确因生产经营特点和工作的特殊性不能实行每日工作8小时，每周工作40小时的，经申报、批准可以实行综合计算工时工作制或者不定时工作制。"
- Quote (第十五条): "应向企业营业执照注册地的区、县劳动和社会保障局申报"
- Newer-rule check: Beijing's most recent batch abolition, 京人社发〔2025〕15号 of 2025-11-20 (10 documents), does not include 157号 or 京人社发〔2021〕10号. The attachment lists only 2009–2024 documents on employment subsidies, unemployment and work injury.
  - URL: https://rsj.beijing.gov.cn/xxgk/2024zcwj/202511/t20251120_4288989.html; attachment W020260507399329499115.doc, text extracted locally
  - Quote: "现决定宣布废止失效10件行政规范性文件。"
- The rsj policy list through 2026-10-13 shows no new special-hours rule.

### 3. "第十六条规定，除高级管理人员实行不定时工作制外，均须审批": **needs change**
- Article 16 has two exemptions, not one. The key leaves out the second.
- URL: same 157号 page as #2
- Quote: "企业中的高级管理人员实行不定时工作制，不办理审批手续。国家和本市已规定实行特殊工时制度的企业不再履行审批手续。"
- Corrected wording: 第十六条规定两类情形不再审批：①企业高级管理人员实行不定时工作制；②国家和本市已规定实行特殊工时制度的企业。普通民营物流公司的调度岗位不会因为属于"物流行业"就落入第②类，仍须审批。
- Suggested addition from the same article: an approval for comprehensive hours may be open-ended while the approved posts stay unchanged. An approval granted because production tasks are uneven lasts only 1–3 years, and Article 17 requires re-filing once it expires. Scenario B should therefore also check that the approval covers the 调度 post and is still in date.

### 4. 北京市人社局2019年典型案例：特殊工时"不取决于双方在劳动合同中的约定"；按岗位审批；签字确认不能补正: **stands**
- URL: https://rsj.beijing.gov.cn/bm/ztzl/dxal/201912/t20191206_880144.html (案例一)
- Quote: "对劳动者是否实行特殊工时，不取决于双方在劳动合同中的约定或用人单位的单方告知，而在于劳动者所在的岗位实行特殊工时是否经过人力社保行政部门审批。"
- Note: the case concerned 不定时 hours. The worker's post (工程造价师) was not among the approved posts, and the employer was ordered to pay weekday and rest-day overtime.

### 5. 未经批准按标准工时认定，周末、调休日、法定节假日上班均为加班: **stands**
- URL: 157号 page as #2
- Quote (第三条): "企业应当实行职工每日工作8小时，每周工作40小时的标准工时制度。"
- Together with #4, where the outcome was weekday and rest-day overtime pay ordered on unapproved special hours, this supports the inference. No statute states the sentence directly; the source file already said so.

### 6. 劳部发〔1995〕309号第62条：综合工时下法定节假日仍按第四十四条第（三）项支付: **stands**
- URL: http://www.gd.gov.cn/zwgk/wjk/zcfgk/content/post_2720827.html (广东省政府政策法规库 reprint, document dated 1995-08-04)
- Quote: "工作日正好是法定节假日时，要依照劳动法第四十四条第（三）项的规定支付职工的工资报酬。"
- Current validity on mohrss.gov.cn could not be re-checked (bot-check page). I found nothing showing it was abolished.

### 7. 《北京市工资支付规定》第十六条：综合工时下法定休假日按第十四条第（三）项支付，即不低于300%: **stands**
- URL: https://www.beijing.gov.cn/gongkai/zfxxgk/zc/gz/202112/t20211223_2570952.html. The header lists only the 2007 amendment, and I found no later amendment.
- Quote (第十六条): "安排劳动者在法定休假日工作的，应当按照本规定第十四条第(三)项的规定支付加班工资。"
- Quote (第十四条第三项): "(三)在法定休假日工作的，应当按照不低于日或者小时工资基数的300%支付加班工资。"

### 8. "'国庆上班不算加班'在任何情况下都不成立": **needs change (overstated)**
- In Beijing, an employer with **approved 不定时** hours is excluded from Article 14 altogether, so the 300% rule does not apply to those posts under Beijing rules. The key admits this exception itself further down, so this sentence contradicts it.
- URL: same page as #7
- Quote (第十七条): "用人单位经批准实行不定时工作制度的，不适用本规定第十四条的规定。"
- Corrected wording: 在标准工时制和综合计算工时工作制下（无论是否经过审批），"国庆上班不算加班"都不成立：10月1日至3日至少按300%支付。只有经批准实行不定时工作制的岗位，在北京不适用第十四条，但本案合同写的是综合工时，且公司没有任何审批。

### 9. "合同是我签的"不构成放弃；劳动合同法第二十六条第一款第（二）项: **stands**
- URL: https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/fl/202011/t20201102_394622.html. This is the 2012 amended text, page field 是否有效: 有效, read from an open browser tab. It settles the source's open point: Article 26 is unchanged in the current text.
- Quote: "（二）用人单位免除自己的法定责任、排除劳动者权利的；"

## 2026年国庆的日期划分

### 10. 国办发明电〔2025〕7号：10月1日（周四）至7日（周三）放假调休共7天；9月20日（周日）、10月10日（周六）上班: **stands**
- URL: https://www.gov.cn/zhengce/content/202511/content_7047090.htm (dated 2025-11-04)
- Quote: "七、国庆节：10月1日（周四）至7日（周三）放假调休，共7天。9月20日（周日）、10月10日（周六）上班。"

### 11. 法定节假日为10月1日至3日（《全国年节及纪念日放假办法》第二条，2024年修订，2025年1月1日施行）；10月3日虽是周六仍为法定节假日: **stands**
- URL: https://www.gov.cn/zhengce/content/202411/content_6986380.htm (国令第795号)
- Quote: "（七）国庆节，放假3天（10月1日至3日）。" / "本决定自2025年1月1日起施行。"
- Weekdays recomputed in PowerShell: 2026-10-01 Thu, 10-03 Sat, 10-04 Sun, 10-07 Wed, 09-20 Sun, 10-10 Sat.

### 12. 10月4日至7日为休息日/调休日（200%，可先补休）；4日周日，其余三天是周六法定假日的补假加两天调休: **stands**
- Composition check:
  - 10月3日 (Sat) is a statutory day falling on a weekend, so Article 6 requires a weekday in lieu. That accounts for one of Oct 5–7.
  - The other two weekdays are swapped with 9/20 (Sun) and 10/10 (Sat).
  - That gives 3 + 1 + 3 = 7 days, which matches the notice.
- Quote (放假办法第六条, URL as #11): "全体公民放假的假日，如果适逢周六、周日，应当在工作日补假。"
- The 2x rate for 调休 rest days is corroborated by the 首都之窗 reprint of 北京日报, 2024-11-17: https://www.beijing.gov.cn/fuwu/bmfw/sy/jrts/202411/t20241117_3942681.html
  - Quote: "其他的周末休息日及调休的休息日加班，用人单位就需支付两倍工资。"
- Limit: that article states a general rule, and its example is the 2025 Spring Festival, where no statutory day fell on a weekend. I did not open a 2026-specific official Q&A on whether a 补假 day for a weekend statutory day pays 2x (search budget exhausted). No source I opened says 3x.

### 13. 9月20日、10月10日为正常工作日，上班不是加班: **stands**
- Basis: the same quote from 国办发明电〔2025〕7号 as #10 ("……上班").

## 正确金额与算式

### 14. 日工资 9000 ÷ 21.75 = 413.79；依据人社部发〔2025〕2号；劳社部发〔2008〕3号已废止: **stands**
- URL: https://app.www.gov.cn/govdata/gov/202501/02/523227/article.html (文号 人社部发〔2025〕2号, signed 2025-01-01)
- Quote: "月计薪天数：（365天-104天）÷12月＝21.75天" / "日工资：月工资收入÷月计薪天数"
- Quote: "（劳社部发〔2008〕3号）同时废止。"
- Recomputed: 9000 / 21.75 = 413.793103 → 413.79.

### 15. 情形A金额：3724.14 / 3310.34 / 7034.48（先舍入日工资时为 3724.11 / 3310.32 / 7034.43）: **stands**
- Recomputed in PowerShell:
  - 9000/21.75 × 9 = 3724.1379
  - × 8 = 3310.3448
  - × 17 = 7034.4828
  - With the daily wage rounded first: 413.79 × 9 = 3724.11; × 8 = 3310.32; × 17 = 7034.43
- Rates: Labour Law Art. 44(2) and 44(3), URL as #1. Quote: "（三）法定休假日安排劳动者工作的，支付不低于工资的百分之三百的工资报酬。"

### 16. 4个休息日可用同等时间补休代替200%；法定节假日不能用补休代替；加班费在9000元月工资之外另付: **stands**
- URL: Beijing wage rules, as #7
- Quote (第十四条第二项): "(二)在休息日工作的，应当安排其同等时间的补休，不能安排补休的，按照不低于日或者小时工资基数的200%支付加班工资；"
- The holiday-pay rule is corroborated by the #12 article: "法定节假日加班，用人单位不能以补休来代替加班工资。"
- "Paid on top of the monthly wage" follows from 21.75 counting statutory holidays as paid days (#14 quote: 365-104, so the 13 holidays are not deducted).

### 17. 情形B：10月1日至3日仍为3724.14元；10月4日至7日为正常工作时间无200%；周期超时部分按150%: **stands**
- 309号 Art. 62 (URL as #6): "工作日正好是周休息日的，属于正常工作"
- Beijing wage rules Art. 16 (URL as #7): "劳动者总实际工作时间超过总标准工作时间的部分，视为延长工作时间，应当按照本规定第十四条第(一)项的规定支付加班工资"
- See #3 for the added check that the approval covers this post and is in date.

### 18. "标准总工时按每月20.67天×8小时=165.33小时"（情形B及末条"2025年起制度工作时间"）: **needs change (arithmetic)**
- 20.67 × 8 = **165.36**, not 165.33. The figure 165.33 is 248 × 8 ÷ 12 = 1984 ÷ 12 = 165.333. The notice gives no hour figure at all; it gives only the method.
- URL: as #14
- Quote: "工作小时数的计算：以月、季、年的工作日乘以每日的8小时。" / "月工作日：248天÷12月＝20.67天/月"
- Corrected wording: 标准总工时 = 制度工作日 × 8小时：全年248天 × 8 = 1984小时，每季62天 × 8 = 496小时；按月折算约165.33小时（1984 ÷ 12；若直接用四舍五入后的20.67天 × 8则为165.36小时）。

## 回答可能附带的说法

### 19. "休息日加班公司必须给钱"不完全对：可先补休，不能补休才付200%: **stands**
- Labour Law Art. 44(2), URL as #1: "（二）休息日安排劳动者工作又不能安排补休的，支付不低于工资的百分之二百的工资报酬；"
- Beijing Art. 14(2): see #16.

### 20. 加班费基数：合同约定 → 集体合同 → 正常劳动应得工资；不得低于最低工资（北京工资支付规定第四十四条）: **stands**
- URL: as #7
- Quote: "(一)按照劳动合同约定的劳动者本人工资标准确定；" / "依照前款确定的加班工资基数以及各种假期工资不得低于本市规定的最低工资标准。"

### 21. 北京最低工资2540元/月，自2025年9月1日起: **stands**
- URL: https://rsj.beijing.gov.cn/xxgk/2024zcwj/202507/t20250725_4158456.html (京人社劳发〔2025〕7号)
- Quote: "每月不低于2540元" / "本通知自2025年9月1日起执行。"
- Newer-rule check: the rsj policy list (https://rsj.beijing.gov.cn/xxgk/2024zcwj/) shows no 2026 minimum-wage notice up to its latest entry, dated 2026-10-13.

### 22. 综合工时下每月平均延长工作时间上限36小时（157号第八条）: **stands**
- URL: as #2
- Quote: "企业延长工作时间平均每月不得超过36小时。"

### 23. 北京经批准的不定时不适用第十四条（工资支付规定第十七条），与本案无关: **stands**
- URL and quote: see #8.

### 24. 审批：向注册地区人社局申报；10个工作日；审批表一式三份，工会或职工代表持一份；自贸区告知承诺制只适用于已取得许可、需重新申报的自贸区企业: **stands**
- 157号 Art. 18, URL as #2:
  - "区、县劳动和社会保障局应在接到企业申报材料10个工作日内，提出审批意见"
  - "审批表》一式三份，由区、县劳动和社会保障局、申报企业、企业工会或职工代表各执一份。"
- FTZ notice: https://rsj.beijing.gov.cn/xxgk/2024zcwj/202406/t20240617_3717202.html (京人社发〔2021〕10号, in force 2021-10-01, not abolished, see #2)
  - Quote: "2.已经在本市取得特殊工时行政许可；"
  - The page also limits the notice to FTZ firms and to re-filing under 157号 Art. 17 (name change or expiry).

### 25. "劳动者可要求公司出示审批表或行政许可决定书，也可向区人社局或12333查询": **could not decide**
- This is practical advice, not a rule I could verify. 157号 Art. 18 gives the union or worker representatives a copy of the 审批表, which supports asking them.
- I found no provision that gives an individual worker a right to demand the document from the employer or from the district bureau. 12333 handling was not checked.
- Suggest wording it as advice: "可以要求查看…可以向…咨询".

### 26. 北京157号第六条列举六类可实行综合工时的情形；符合条件仍须批准: **stands**
- URL: as #2
- Quote: "（一）因工作性质需连续作业的；" … "（六）可以定期集中安排休息、休假的。" (six items)

### 27. 503号第五条列举交通、邮电等需连续作业的职工: **could not decide**
- https://www.mohrss.gov.cn/xxgk2020/gzk/gz/202112/t20211228_431561.html returned only a bot-check script to curl and WebFetch, and I did not try to get past it.
- No contrary evidence was found. 309号 Art. 69 (URL as #6) does match the 503号 Art. 7 delegation quoted in the source: "地方企业实行不定时工作制和综合计算工时工作制等其他工作和休息办法的审批办法，由省、自治区、直辖市人民政府劳动行政部门制定"

### 28. 举证：劳动者先证明加班事实；用人单位掌握证据不提供的承担不利后果（法释〔2020〕26号第四十二条）: **stands**
- URL: https://www.court.gov.cn/fabu/xiangqing/282121.html
- Quote: "劳动者主张加班费的，应当就加班事实的存在承担举证责任。但劳动者有证据证明用人单位掌握加班事实存在的证据，用人单位不提供的，由用人单位承担不利后果。"
- Newer-rule check: 劳动争议解释（二）, 法释〔2025〕12号, in force 2025-09-01, repeals only Art. 32(1) of 法释〔2020〕26号. Art. 42 is untouched, and no article of (二) deals with overtime or working-hours systems.
  - URL: https://www.court.gov.cn/fabu/xiangqing/472691.html
- The 2026-08-06 decision amending nine interpretations (法释〔2026〕16号) concerns environmental interpretations only.
  - URL: https://www.court.gov.cn/fabu/xiangqing/508041.html

### 29. 时效：在职追索拖欠劳动报酬不受一年时效限制，离职后一年内；仲裁不收费: **stands**
- URL: http://www.npc.gov.cn/c2986/c4488/201905/t20190523_48437.html (fetched by curl)
- Quote: "劳动关系存续期间因拖欠劳动报酬发生争议的，劳动者申请仲裁不受本条第一款规定的仲裁时效期间的限制；但是，劳动关系终止的，应当自劳动关系终止之日起一年内提出。"
- Quote: "第五十三条 劳动争议仲裁不收费。"
- Optional addition: 解释（二） Art. 20 (URL as #28) says an employer that does not raise a time-bar defence in arbitration cannot raise it later in court.

### 30. 未经审批时全年其他周末上班同样属于休息日加班（补休或200%）: **stands**
- Follows from #5 and from Beijing Art. 14(2) (#16).

### 31. 2025年起制度工作日每月20.67天、全年248天、1984小时；月计薪天数仍为21.75；引用20.83天或劳社部发〔2008〕3号为现行依据的已过时: **stands (except the hour figure, see #18)**
- URL and quotes: see #14 and #18. 248 × 8 = 1984 recomputed.

---

## Summary
- **Need change:**
  - #3: 157号 Art. 16 has a second exemption, for enterprises already put on special hours by national or Beijing rules.
  - #8: "在任何情况下都不成立" is overstated, because Beijing Art. 17 excludes approved 不定时 posts.
  - #18: 20.67 × 8 = 165.36; 165.33 is 1984 ÷ 12.
- **Could not decide:**
  - #25: the worker's right to see the approval and the 12333 route.
  - #27: 503号 Art. 5 text, because mohrss.gov.cn served a bot check.
  - Also not settled: a 2026-specific official statement on the pay rate for the 补假 day (#12; the general rule supports 2x).
- **All money figures recomputed and correct:** 413.79; 3724.14 / 3310.34 / 7034.48; rounded-first 3724.11 / 3310.32 / 7034.43.
