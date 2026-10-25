# zh-new-job-leave: adversarial check of "Facts for the key"

Checked 2026-10-22. I read only `zh-new-job-leave.md`, then reopened the cited sources myself and recomputed every figure in Python (`python -I`, date arithmetic and division).

Limits of this check:
- The WebSearch budget for this turn ran out after the first query, so I could not run a fresh search for 2025-2026 amendments or local rules.
- The MOHRSS 征求意见 page came back empty, the MOJ 立法意见征集 page looped on redirects, and the built-in browser had no free tab.
- Newer-rule checks therefore rest on the official pages listed below only.

Totals: 23 stand, 2 need change, 2 could not be decided.

## Premise (前提错在哪里)

**K1. HR's statement is wrong. The condition is 连续工作满12个月以上 (any employer), not one year at this employer. With no gap, the user qualifies on day one: stands.**
- https://www.gov.cn/zhengce/2022-08/31/content_5711300.htm (实施办法第三条): "职工连续工作满12个月以上的，享受带薪年休假（以下简称年休假）。"
- https://hrss.zs.gov.cn/zcfg/ldgx/content/post_1196498.html (人社厅函〔2009〕149号, 2009-04-15, to 上海市人社局): "既包括职工在同一用人单位连续工作满十二个月以上的情形，也包括职工在不同用人单位连续工作满十二个月以上的情形。"
- Still cited in 2025 by https://rst.hunan.gov.cn/rst/qta/202505/t20250509_33665791.html (2025-05-09): "也包括职工在不同用人单位连续工作满12个月以上的情形"
- Precision note, not a refutation: under the Shanghai court reading (K17b), any gap restarts the 12 months, and then HR's "今年一天都没有" would be correct. Keep "只要前后两份工作是连着的" next to the word "错".

**K2. Service at different employers adds up. Six years falls in the 5-day band: stands.**
- 实施办法第四条 (same URL as K1): "职工在同一或者不同用人单位工作期间……应当计为累计工作时间。"
- https://www.gov.cn/gongbao/content/2008/content_859865.htm (条例第三条): "职工累计工作已满1年不满10年的，年休假5天"

**K3. A new hire's leave for the year is pro rata by remaining calendar days, and any part below one full day is dropped: stands.**
- 实施办法第五条: "按照在本单位剩余日历天数折算确定，折算后不足1整天的部分不享受年休假。" / "（当年度在本单位剩余日历天数÷365天）×职工本人全年应当享受的年休假天数。"

## Figures (正确数字)

**K4. 1 July to 31 December 2026 is 184 days, and 2026 is not a leap year: stands.** Recomputed: (date(2026,12,31) − date(2026,7,1)) + 1 = 184; 2026 % 4 ≠ 0.

**K5. 184 ÷ 365 × 5 = 2.52, so 2 days, paid as normal: stands.** Recomputed 2.5205 → 2 under 第五条.
- 条例第二条: "职工在年休假期间享受与正常工作期间相同的工资收入。"

**K6. Daily wage 15000 ÷ 21.75 = 689.66 yuan, on the basis of 人社部发〔2025〕2号 and 实施办法第十一条: stands.** Recomputed 689.6552.
- https://www.gov.cn/zhengce/zhengceku/202501/content_6995777.htm (人社部发〔2025〕2号, dated 2025-01-01, repeals 劳社部发〔2008〕3号): "日工资：月工资收入÷月计薪天数" / "月计薪天数：（365天-104天）÷12月＝21.75天"
- The notice does not mention 事假. The key does not claim it does.

**K7. Plan A, 3 days of 事假: 2068.97 yuan, or 2068.98 if the daily wage is rounded first: stands.** Recomputed 2068.9655 and 689.66 × 3 = 2068.98.

**K8. Plan B, 5 days of 事假: 3448.28 yuan, or 3448.30 if the daily wage is rounded first: stands.** Recomputed 3448.2759 and 689.66 × 5 = 3448.30.

**K9. The difference is 1379.31 yuan: stands.** Recomputed 15000 × 2 ÷ 21.75 = 1379.3103. With the rounded daily wage the difference is 689.66 × 2 = 1379.32. If an answer uses the rounded figures, it should say 1379.32.

## Side claims (附带说法)

**K10. There is no national formula for 事假 deductions. The employer may withhold pay, according to its rules and the contract: stands.**
- https://know.12348.gov.cn/s/relate/?qid=5c09c82d36aec572cd1be640 (中国法律服务网): "目前我国法律没有明确规定，一般是依据公司规章制度和劳动合同约定"
- https://rst.fujian.gov.cn/wz/cjwt/ldgx/xxxj/202311/t20231113_6295173.htm (2023-08-16): "员工请事假的，用人单位可以不支付其事假期间的工资。"

**K11. 21.75 is the most common daily basis with official backing, and 上海人社局 applies it explicitly to 事假: stands.**
- https://rsj.sh.gov.cn/trdhy_17355/20200617/t0035_1382855.html (2019-05-08, under the subheading "1、事假"; local, 上海市企业工资支付办法): "此处日工资的计算方法是：日工资=假期工资基数÷21.75（月计薪天数）。"
- Suggested addition: the 司法部 site treats 21.75 as the upper limit for a deduction, not just one method among several. Same 12348 URL: "因此扣除事假工资的最高限，是劳动者的月工资÷21.75×事假天数。" This is the site's reading, not a statute. It is useful because a company dividing by fewer days (for example 20.83, or a short month) would deduct more than this.

**K12. Other bases: December 2026 has 23 working days (652.17 per day, 1956.52 for 3 days, 3260.87 for 5), or a 30-day basis (500, 1500, 2500): stands, on arithmetic and the calendar.**
- Recomputed: 1 December 2026 is a Tuesday and the month has 23 weekdays. 15000/23 = 652.1739; ×3 = 1956.5217; ×5 = 3260.8696. 15000/30 = 500.
- Not verified: whether any 调休 workday falls in December 2026. I could not open the 2026 or 2027 国务院办公厅 holiday notices because search was unavailable. Keep the assumption in the wording.

**K13. 事假 is usually deducted for working days only, and whether weekends inside a run count depends on the company. Annual leave excludes statutory holidays and rest days: stands.** The first half is correctly labelled company-specific, and no official text decides it either way. The second half is confirmed.
- 条例第三条第二款: "国家法定休假日、休息日不计入年休假的假期。"

**K14. The employer schedules leave, taking the employee's wishes into account. The user may ask for December and cannot be refused on "未满一年" grounds. Leave stays within the year, and crossing into the next year needs the employee's consent: stands.**
- 条例第五条: "年休假在1个年度内可以集中安排，也可以分段安排，一般不跨年度安排。单位因生产、工作特点确有必要跨年度安排职工年休假的，可以跨1个年度安排。"
- 实施办法第九条: "用人单位确因工作需要不能安排职工年休假或者跨1个年度安排年休假的，应征得职工本人同意。"

**K15. Unused leave is paid at 300%, including normal pay. "本例2天约多付 689.66 × 2 × 2 = 2758.62元": needs change (arithmetic).**
- The rule stands. 实施办法第十条: "按照其日工资收入的300%支付未休年休假工资报酬，其中包含用人单位支付职工正常工作期间的工资收入。"
- The 第十一条 caveat stands too: "在本用人单位工作时间不满12个月的，按实际月份计算月平均工资。"
- The figure is inconsistent: 689.66 × 2 × 2 = 2758.64, while 15000 ÷ 21.75 × 2 × 2 = 2758.62.
- Corrected wording: "本例2天约多付 15000 ÷ 21.75 × 2 × 2 = 2758.62元（日工资先取整为 689.66 × 4 = 2758.64元）。"

**K16. Prior service can be proved with the personnel file, social insurance records, a labour contract or other legally valid proof (149号 point 2): stands.**
- 149号 (zs.gov.cn URL above), second point: the letter says 档案记载、单位缴纳社保费记录、劳动合同或者其他具有法律效力的证明材料 can establish cumulative service. I confirmed this wording on the page.

**K17a. There is no national rule on a gap between leaving one job and starting the next: stands.** The 条例, the 实施办法 and 149号, all reopened, say nothing about gaps.

**K17b. A 2026 浦东法院 case held that a 2-working-day gap broke continuity: stands.**
- https://www.thepaper.cn/newsDetail_forward_33413336 (澎湃号·政务, 2026-06-18, author 曹赟娴): "仍存在2天工作日的间隔，不符合连续工作满12个月以上的情形，应重新计算。"
- Facts checked: the employee left on 2022-09-30 and joined on 2022-10-10, with 8 and 9 October as working days in between. The claim was dismissed and the appeal upheld. The court's 2023 figure checks out: 83 days ÷ 365 × 10 = 2.27, giving 2 days.

**K17c. Chongqing tolerates a gap of up to one month: could not verify.** The rlsbj.cq.gov.cn PDF failed in WebFetch ("Command failed with no output"), and the built-in browser was refused for that host. The claim stays unverified.

**K17d. "深圳据媒体报道要求无缝衔接": needs change (wording and attribution).**
- https://m.mp.oeeee.com/a/BAAFRD0000202601141509115.html (南都, 2026-01-14, reporter 宋承翰). The report attributes the rule to the 深圳市中级人民法院 judicial guideline, not to the media: "深圳市中级人民法院关于审理劳动争议案件的裁判指引一百〇九条规定". The report's word is "无缝对接", not "无缝衔接".
- I could not open the guideline itself.
- Corrected wording: "深圳据南都报道，深圳中院《关于审理劳动争议案件的裁判指引》第一百〇九条要求'无缝对接'（原文未能打开核实）。"

**K17e. Leaving on 30 June and joining on 1 July with no gap gives a safe conclusion; with a gap, it depends on local rules and court practice: stands.** This follows from K1 and K17b.

**K18. Probation does not affect eligibility. The national rules only ask whether 12 months of continuous work are met: stands (inference).** Neither national text mentions 试用期.
- https://hrss.suzhou.gov.cn/jsszhrss/zcwd/202305/f0795a7a9730414aa87c73f6b344cfc0.shtml (2023-05-01): the page asks about a worker on probation and answers only by citing 第三条, 第五条 and 149号: "小李来电咨询，他今年4月进入新单位，目前正处于试用期，是否可以享受带薪年休假？"

**K19. No national text deducts leave taken at the old employer from the new employer's days: stands.**
- 实施办法第五条 bases the quota only on remaining days at the new employer.
- 第十二条 settles the old employer's side and says: "用人单位当年已安排职工年休假的，多于折算应休年休假的天数不再扣回。"

**K20. The 条例第四条 exclusions do not apply here (5 days of 事假, with pay deducted): stands.**
- 条例第四条: "（二）职工请事假累计20天以上且单位按照规定不扣工资的；（三）累计工作满1年不满10年的职工，请病假累计2个月以上的；"

**K21a. A revision of the 条例 is planned (国函〔2026〕66号; MOHRSS, 27 January 2026): stands.**
- https://www.gov.cn/zhengce/content/202607/content_7075216.htm (dated 2026-07-02, published 2026-07-13): "推动修订《职工带薪年休假条例》，严格落实职工带薪休假制度，增强制度执行刚性。"
- https://cn.chinadaily.com.cn/a/202601/27/WS69785b16a310942cc499cfcf.html (2026-01-27): "推动修订《职工带薪年休假条例》，促进用人单位落实职工带薪年休假制度。"

**K21b. No revised text or consultation draft exists as of 2026-10-22: could not decide independently.** Search was unavailable and the MOHRSS and MOJ comment pages could not be read. The gov.cn texts of the 2007 条例 and 2008 实施办法 still load with no repeal notice, and nothing I opened shows new day counts. Keep the key's "未检索到" wording, which is already hedged.

**K22. In 2027 the user has a full year at this employer, so no pro rata applies and the entitlement is 5 days. It rises to 10 days once cumulative service reaches 10 years: stands.**
- 条例第三条: "已满10年不满20年的，年休假10天"

## Outside the key (for the source author)
- Item 6 note: two WebFetch passes over the 南都 article (2026-01-14) found no "200天 / 2.74" worked example, only the formula. Drop that supporting note or recheck it. The 2-day result in K5 does not depend on it.
- Item 5: the Hunan page's question reads "必须在同一单位连续工作满12个月才能休年假吗？", not the wording quoted in the source file. The answer text matches.
