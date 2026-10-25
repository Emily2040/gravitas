# zh-new-job-leave: source check

Request: worked 6 years, joined the current employer on 1 July (2026), wants a few days in December; HR says "入职满一年才有年假，你今年一天都没有"; asks for a 事假 message and the deduction for 5 days of 事假 at 15,000 yuan/month.

Checked on 2026-10-22. All pages below were opened that day unless marked otherwise. Quotes are in the original language, two lines at most.

## Items

### 1. 职工带薪年休假条例 第二条 (eligibility, pay during leave)
- Verdict: **confirmed**
- URL: https://www.gov.cn/gongbao/content/2008/content_859865.htm (国务院公报 2008年第2号; 国务院令第514号, 2007-12-14公布, 2008-01-01施行)
- Quote: "……的职工连续工作1年以上的，享受带薪年休假（以下简称年休假）。单位应当保证职工享受年休假。职工在年休假期间享受与正常工作期间相同的工资收入。"

### 2. 职工带薪年休假条例 第三条 (days by cumulative service; weekends and holidays excluded)
- Verdict: **confirmed**
- URL: same as item 1
- Quote: "职工累计工作已满1年不满10年的，年休假5天；已满10年不满20年的，年休假10天；已满20年的，年休假15天。" / "国家法定休假日、休息日不计入年休假的假期。"

### 3. 企业职工带薪年休假实施办法 第三条 (连续工作满12个月以上)
- Verdict: **confirmed**
- URL: https://www.gov.cn/zhengce/2022-08/31/content_5711300.htm (人力资源社会保障部令第1号, 2008-09-18公布施行; source line on page: 人力资源社会保障部网站)
- Quote: "职工连续工作满12个月以上的，享受带薪年休假（以下简称年休假）。"
- Related, same page, 第四条 (cumulative service counts across employers): "职工在同一或者不同用人单位工作期间……应当计为累计工作时间。"

### 4. 企业职工带薪年休假实施办法 第五条 (new hire, pro rata by remaining calendar days, fraction below one day dropped)
- Verdict: **confirmed** (exact wording is "不足1整天", not "不足1天")
- URL: same as item 3
- Quote: "职工新进用人单位且符合本办法第三条规定的，当年度年休假天数，按照在本单位剩余日历天数折算确定，折算后不足1整天的部分不享受年休假。" / "（当年度在本单位剩余日历天数÷365天）×职工本人全年应当享受的年休假天数。"

### 5. 人社厅函〔2009〕149号 (连续工作满12个月 includes different employers)
- Verdict: **confirmed**. Original text read from a government reprint (中山市人社局), not from mohrss.gov.cn; the MOHRSS search index lists the letter with the same title and date 2009.04.15. 湖南省人社厅 (2025-05-09) and 苏州市人社局 (2023-05-01) Q&As cite it as current.
- URL: https://hrss.zs.gov.cn/zcfg/ldgx/content/post_1196498.html (letter dated 2009-04-15, addressed to 上海市人力资源和社会保障局)
- Quote: "第三条中的'职工连续工作满十二个月以上'，既包括职工在同一用人单位连续工作满十二个月以上的情形，也包括职工在不同用人单位连续工作满十二个月以上的情形。"
- Second point of the same letter (proof of service): "职工的累积工作时间可以根据档案记载、单位缴纳社保费记录、劳动合同或者其他具有法律效力的证明材料确定。"
- Supporting: https://rst.hunan.gov.cn/rst/qta/202505/t20250509_33665791.html (Q: "我刚跳槽到新单位,需要连续工作满12个月才能休年休假吗?"; answer repeats the 149号 wording).

### 6. 7月1日至12月31日 = 184天; 184÷365×5 = 2.52, 取2天
- Verdict: **confirmed** (arithmetic checked: 31+31+30+31+30+31 = 184; 2026 is not a leap year, so the divisor 365 is exact; 920÷365 = 2.5205; the fraction is dropped under 第五条, giving 2 days)
- URL: rule from item 4 (https://www.gov.cn/zhengce/2022-08/31/content_5711300.htm); computation done locally.
- Quote: "折算后不足1整天的部分不享受年休假。"
- Note: a MOHRSS WeChat explanation reported by 南都 (2026-01-14, https://m.mp.oeeee.com/a/BAAFRD0000202601141509115.html, secondary) uses the same method (200 days remaining, 5×200÷365 ≈ 2.74, 2 days).

### 7. 事假扣款没有国家统一公式
- Verdict: **confirmed**
- URL: https://know.12348.gov.cn/s/relate/?qid=5c09c82d36aec572cd1be640 (中国法律服务网, 司法部)
- Quote: "目前我国法律没有明确规定，一般是依据公司规章制度和劳动合同约定"
- Supporting, 福建省人社厅 Q&A (2023-08-16), https://rst.fujian.gov.cn/wz/cjwt/ldgx/xxxj/202311/t20231113_6295173.htm: "员工请事假的，用人单位可以不支付其事假期间的工资。"
- Supporting, 上海市人社局 热点回应 (2019-05-08), https://rsj.sh.gov.cn/trdhy_17355/20200617/t0035_1382855.html: "此处日工资的计算方法是：日工资=假期工资基数÷21.75（月计薪天数）。" (Shanghai, under 上海市企业工资支付办法; local, not national.)

### 8. 人社部发〔2025〕2号: 日工资 = 月工资 ÷ 21.75
- Verdict: **confirmed**, with a scope note: the notice sets the general daily-wage conversion. It does not mention 事假 and does not make a 事假 deduction mandatory. It is dated 2025-01-01 and repeals 劳社部发〔2008〕3号. The 21.75 figure also appears in 实施办法第十一条 for unused leave pay.
- URL: https://www.gov.cn/zhengce/zhengceku/202501/content_6995777.htm
- Quote: "日工资：月工资收入÷月计薪天数" / "月计薪天数：（365天-104天）÷12月＝21.75天"

### 9. 15000÷21.75 = 689.66; 5天 3448.28; 先休2天年假再请3天事假 2068.97
- Verdict: **confirmed** (arithmetic): 15000÷21.75 = 689.6552; ×5 = 3448.2759 → 3448.28; ×3 = 2068.9655 → 2068.97; ×2 = 1379.31.
- Rounding note: rounding the daily wage first (689.66×5 = 3448.30; ×3 = 2068.98) gives a few fen more. Both are acceptable, but say which one you used.
- URL: basis from item 8; computation done locally.

### 10. 离职间隔是否影响"连续工作"的认定
- Verdict: **could not verify a national rule**. 条例, 实施办法 and 149号 say nothing about gaps. Practice differs by place:
  - **Shanghai court practice: confirmed** (court's official account). 上海浦东法院 case published 2026-06-18 on 澎湃号·政务 (author 曹赟娴). The employee left on 2022-09-30 and joined on 2022-10-10; two working days fell between them. The court held that continuity was broken and the 12 months restarted. The claim was dismissed and upheld on appeal. URL: https://www.thepaper.cn/newsDetail_forward_33413336. Quote: "仍存在2天工作日的间隔，不符合连续工作满12个月以上的情形，应重新计算。"
  - **Chongqing: could not verify.** A one-month gap tolerance is reported in 渝劳社办发〔2008〕268号 on rlsbj.cq.gov.cn, but the host refused connections from curl, PowerShell and the built-in browser. The wording is known only from search snippets: "不得间断超过一个月以上。超过的，其连续工作时间重新计算". URL tried: https://rlsbj.cq.gov.cn/zwgk_182/zfxxgkml/zcwj_145360/jfxzgfxwj/200902/W020230214613025972669.pdf
  - **Shenzhen "无缝衔接": could not verify.** The only source is a secondary media report (南都 2026-01-14, link in item 6). The hrss.sz.gov.cn case page returned 404.

### 11. (added) 条例 is under revision but unchanged as of 2026-10-22
- Verdict: **confirmed** that a revision is planned. No revised text or consultation draft turned up in searches of gov.cn, MOHRSS, MOJ or the news on 2026-10-22, so the 2007 条例 and 2008 实施办法 still apply.
- URL: https://www.gov.cn/zhengce/content/202607/content_7075216.htm (国务院关于《扩大消费"十五五"规划》的批复, 国函〔2026〕66号, published 2026-07; plan section （二十八）)
- Quote: "推动修订《职工带薪年休假条例》，严格落实职工带薪休假制度，增强制度执行刚性。"
- Also: MOHRSS press conference on 2026-01-27 (China Daily, https://cn.chinadaily.com.cn/a/202601/27/WS69785b16a310942cc499cfcf.html): "推动修订《职工带薪年休假条例》，促进用人单位落实职工带薪年休假制度。"

### 12. (added) Scheduling is the employer's job, the leave normally stays in the year, and unused days are paid at 300%
- Verdict: **confirmed**
- URL: https://www.gov.cn/gongbao/content/2008/content_859865.htm (条例第五条); https://www.gov.cn/zhengce/2022-08/31/content_5711300.htm (实施办法第九、十、十一条)
- Quote (条例第五条): "单位根据生产、工作的具体情况，并考虑职工本人意愿，统筹安排职工年休假。" / "年休假在1个年度内可以集中安排，也可以分段安排，一般不跨年度安排。"
- Quote (实施办法第十条): "按照其日工资收入的300%支付未休年休假工资报酬，其中包含用人单位支付职工正常工作期间的工资收入。"
- 实施办法第十一条: the daily wage for unused leave is the monthly wage (12-month average excluding overtime, or the actual months if under 12) ÷ 21.75. 第十条第二款: if the employer arranges the leave and the employee declines it in writing for personal reasons, only normal pay is owed.

### 13. (added) Exclusions that could cancel the year's leave (条例第四条)
- Verdict: **confirmed**. None appears to apply to this user (the 事假 would be deducted, and it is under 20 days).
- URL: item 1
- Quote: "（二）职工请事假累计20天以上且单位按照规定不扣工资的；（三）累计工作满1年不满10年的职工，请病假累计2个月以上的；"

### 14. (added) Probation does not exclude annual leave
- Verdict: **confirmed** as far as the national texts go. Neither the 条例 nor the 实施办法 mentions 试用期; the condition is 连续工作满12个月 (item 3). The 苏州市人社局 Q&A "试用期员工可以享受带薪年休假吗？" (2023-05-01) answers by citing 第三条, 第五条 and 149号. It gives no separate probation rule.
- URL: https://hrss.suzhou.gov.cn/jsszhrss/zcwd/202305/f0795a7a9730414aa87c73f6b344cfc0.shtml
- Quote: "小李来电咨询，他今年4月进入新单位，目前正处于试用期，是否可以享受带薪年休假？"

### 15. (added) Leave taken at the previous employer earlier in the year
- Verdict: **could not verify** any national rule that offsets it against the new employer's pro-rata days. 实施办法第五条 bases the new employer's quota only on remaining days at the new employer. 第十二条 governs the old employer's settlement on leaving. Some commentary says the old employer's leave should be netted off, but I found no official text. Answers should not state an offset as law.
- URL: item 3

### 16. (added) Arbitration example: prior service counts at a new employer
- Verdict: **confirmed** (MOHRSS 中国就业网 reprint of a 河北工人报 report on a 石家庄 arbitration award)
- URL: https://chinajob.mohrss.gov.cn/c/2021-10-11/326547.shtml (2021-10-11)
- Quote: "张某于2016年参加工作，入职某美容机构处前，其已连续工作1年以上，符合享受带薪年休假的条件。"

### 17. (added) December 2026 working days, for a "monthly working days" deduction basis
- Verdict: **confirmed** by calendar. 2026-12-01 is a Tuesday, and December 2026 has 23 weekdays. This assumes no 调休 workday in December 2026; the 2027 holiday schedule was not checked.
- Computation done locally (PowerShell date arithmetic).

## Facts for the key

**前提错在哪里**
- 人事说"入职满一年才有年假，你今年一天都没有"，这是错的；用户据此认为"新公司只能请事假"，也是错的。法定条件是"连续工作满12个月以上"（实施办法第三条），不是"在本单位满一年"。人社厅函〔2009〕149号明确，这个条件既包括同一用人单位，也包括不同用人单位。用户已工作6年，7月1日跳槽入职；只要前后两份工作是连着的，入职当天就已满足条件。
- 年休假天数按累计工作时间确定，不同单位的工作时间合并计算（实施办法第四条）。累计6年，属于"满1年不满10年"一档，全年应休5天（条例第三条）。
- 新进用人单位当年按剩余日历天数折算，不足1整天的部分不享受（实施办法第五条）。

**正确数字**
- 2026年7月1日至12月31日：31+31+30+31+30+31 = 184天（2026年不是闰年）。
- 今年在新单位的年假：184 ÷ 365 × 5 = 2.52，取2天。年假期间工资照发，与正常工作期间相同（条例第二条），不扣钱。
- 日工资常用口径：15000 ÷ 21.75 = 689.66元（21.75见人社部发〔2025〕2号、实施办法第十一条）。
- 方案A，先休2天年假，再请3天事假：扣 15000 × 3 ÷ 21.75 = 2068.97元。先把日工资取整再乘，是 689.66 × 3 = 2068.98元。
- 方案B，按人事说法5天全请事假：扣 15000 × 5 ÷ 21.75 = 3448.28元。日工资先取整则为 3448.30元。
- 两者差 1379.31元，即2天年假的工资。

**答案中常会加上的附带说法及正确值**
- 事假怎么扣，国家没有统一公式。事假期间单位可以不发工资，具体按公司规章制度或劳动合同（中国法律服务网；福建省人社厅）。21.75是最常见、也有官方依据的日工资口径，上海人社局明确用于事假。【因地、因公司制度而异】有的公司按当月应出勤天数（2026年12月为23个工作日：15000÷23 = 652.17元/天，3天1956.52元，5天3260.87元），有的按30天（500元/天，3天1500元，5天2500元）。答案应提醒用户以公司制度为准，不能把21.75说成法定扣法。
- 事假一般只扣工作日。连续请假中间夹着周末算不算，看公司制度。【因公司而异】年休假不计入法定节假日和休息日（条例第三条第二款）。
- 年假由单位统筹安排，考虑本人意愿（条例第五条、实施办法第九条）。用户可以申请12月休，具体日期需要单位安排，单位无权以"未满一年"为由不给。年假原则上当年休完，单位确有必要的，经职工同意可跨1个年度。
- 单位当年不安排、职工又没有书面放弃的，应休未休的年假按日工资的300%支付，其中包含正常工资（实施办法第十条）。本例2天约多付 689.66 × 2 × 2 = 2758.62元。注意第十一条的月工资取剔除加班工资后的月平均工资，不满12个月按实际月份算，结果可能与15000/月略有出入。
- 怎么证明以前的工作年限：档案记载、单位缴纳社保费记录、劳动合同或其他有法律效力的证明（149号第二点）。建议用户向人事提供社保缴费记录或原单位离职证明，并引用实施办法第三、四、五条和149号。
- 离职与入职之间有空档怎么办，国家层面没有规定。【因地而异】上海浦东法院2026年公布的案例中，空档仅2个工作日，即被认定"不符合连续工作满12个月以上的情形，应重新计算"。重庆有"间断不超过一个月"的地方口径，深圳据媒体报道要求无缝衔接，这两条均未能打开原文核实。答案应提示：如果6月30日离职、7月1日入职、中间没有空档，结论稳妥；有空档的，要看当地规定和裁判口径。
- 试用期不影响年假资格，国家规定只看连续工作是否满12个月。
- 今年在原单位已休的年假是否要从新单位的2天里扣，国家文本没有这样的规定，不应作为定论。
- 条例第四条规定的不享受情形与本例无关：事假累计20天以上且单位不扣工资，或病假累计2个月以上（满1年不满10年一档）。只请5天事假且扣工资，不影响今年和明年的年假。
- 条例正在修订：国函〔2026〕66号规划写明"推动修订"，人社部2026年1月27日也有表态。截至2026-10-22，未检索到修订文本或征求意见稿，现行2007年条例和2008年实施办法仍然适用。答案不应引用任何"2026新规"天数。
- 明年（2027年）：全年在本单位，不再折算，按累计工龄应休5天。累计工龄满10年后为10天。
