# Adversarial check: zh-contract-expiry-compensation.md

Checked 2026-10-26 (system date; the task brief says 2026-10-25) by an agent that did not write the source file. On disk I read only `prompts/zh-contract-expiry-compensation.txt`, `sources/zh-contract-expiry-compensation.md`, and round four's `en-fsa-rollover.check.md` for the format. I downloaded every URL below myself on that date and extracted its text. Quotes are verbatim, in the original language, two lines at most. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: I found no rule, amendment, figure or announcement in force by 2026-10-25 that makes the premise true. Expiry of a fixed-term contract that the employer declines to renew still triggers economic compensation. Here is what I checked:
- **Labour Contract Law.** The NPC's 现行有效法律目录 (cut-off 2026-08-28, the close of the 24th NPCSC session) still lists 劳动合同法 as "2007 年通过，2012 年修正". The 74th chairpersons' meeting (2026-10-22) set the 25th session for 2026-11-02 to 11-06. Its agenda contains no stand-alone labour bill. It does include a State Council package, "突发事件应对法等15部法律的修正案草案". That notice does not list the 15 laws, so I cannot rule out that 劳动合同法 is one of them. Nothing from that package can be in force by 2026-10-25.
- **SPC judicial interpretations.** The court.gov.cn listing (pages 1 and 2, back to 2024-01) has one labour-contract item: 劳动争议解释（二） (法释〔2025〕12号, in force 2025-09-01). It does not touch Art. 46(5) or 47. It adds detail to items 20 and 21 below.
- **Jiangsu provincial regulations.** I scanned all 25 pages of the jsrd.gov.cn listing, plus every 2025–2026 package amendment and repeal decision. None amends or repeals 江苏省劳动合同条例. 江苏省工资支付条例 received its 3rd amendment on 2026-05-27. Its Art. 19 (final wages within two working days) is unchanged, and it adds a fact to item 12.
- **Suzhou HR Q&As.** A 2026-01-28 Suzhou HR Q&A confirms the 2660 unemployment-benefit cap from 2026-01-01. It also gives a published floor of 1812, which differs from the source's derived 1891.50 (item 15). A 2024-01-29 Suzhou HR Q&A states the expiry-compensation rule outright (item 2).

One hazard for graders: the Jiangsu People's Congress site's own entry for 江苏省劳动合同条例 still shows the **2003** text, including the deleted 30-day notice in Art. 37 (item 9). An answer that cites it is citing a stale page.

Tooling note: the shared WebSearch budget ran out on my first query. From then on I made no search-engine queries. I downloaded known official URLs directly and browsed official listing pages (NPC, SPC, jsrd.gov.cn, Suzhou HR). I did not check a national revision of 失业保险条例 in this pass, because the gov.cn regulation list is JavaScript-only.

## The premise

**F1 (source item 1). Contract expiry is a ground for termination (劳动合同法 Art. 44(1)).**
Status: **stands**
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html (北京市司法局 copy, 发布时间 2008-03-14)
- Quote: "第四十四条 有下列情形之一的，劳动合同终止：" / "（一）劳动合同期满的；"

**F2 (source item 2, headline 1). Expiry termination of a fixed-term contract requires economic compensation unless the employer offered same-or-better terms and the worker refused. So the premise "到期不续签公司不用给任何补偿" is false.**
Status: **stands** (premise refuted)
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html
- Quote: "（五）除用人单位维持或者提高劳动合同约定条件续订劳动合同，劳动者不同意续订的情形外，依照本法第四十四条第一项规定终止固定期限劳动合同的；"
- Current text: https://www.sz.gov.cn/cn/xxgk/zfxxgj/zcfg/content/post_8965212.html (深圳市政府, 发布日期 2017-04-12). Header: "根据2012年12月28日《全国人民代表大会常务委员会关于修改〈中华人民共和国劳动合同法〉的决定》修订". Art. 46(5) is identical.
- No later amendment: http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf (现行有效法律目录, "截至 2026 年 8 月 28 日"). Quote: "中华人民共和国劳动合同法（2007 年通过，2012 年修正）"
- Suzhou's own HR bureau says the same: http://hrss.suzhou.gov.cn/jsszhrss/zcwd/202401/6798fec4eb164ca3b4ad4346ea60d22d.shtml (苏州市人社局, 2024-01-29, item 12 "劳动合同终止的，用人单位是否支付经济补偿？")
- Quote: "除用人单位维持或者提高劳动合同约定条件续订劳动合同，劳动者不同意续订劳动合同的情形外，用人单位依照本法第四十四条第一项规定终止固定期限劳动合同的；" … "用人单位应当向劳动者支付经济补偿。"
- Worked example on the same facts: https://rsj.beijing.gov.cn/bm/ztzl/dxal/201912/t20191206_880166.html (北京市人社局 typical case, 日期 2017-03-03). Quote: "该劳动合同到期后，甲公司决定不再与张某续订劳动合同，并通过银行转账方式向张某支付了终止劳动合同的经济补偿金18168元。"
- Not re-opened: the content of the 2012 amendment decision. It does not matter, because Art. 46(5) reads the same in the 2012-amended copy.

## Amount

**F3 (item 3). One month's wage per full year. N = 3.**
Status: **stands**
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html
- Quote: "第四十七条 经济补偿按劳动者在本单位工作的年限，每满一年支付一个月工资的标准向劳动者支付。"
- Recomputed: 2023-11-01 to 2026-10-31 is exactly 3 years. The half-month and round-up rules do not apply.

**F4 (item 4). "Monthly wage" means the average 应得工资 over the 12 months before termination, including bonuses and allowances.**
Status: **stands**
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html. Quote: "本条所称月工资是指劳动者在劳动合同解除或者终止前十二个月的平均工资。"
- URL: https://www.gov.cn/zwgk/2008-09/19/content_1099470.htm (国务院令第535号, dated 二○○八年九月十八日). The same text is at https://glj.jiangsu.gov.cn/art/2012/9/10/art_79128_9525489.html (发布日期 2012-09-10).
- Quote: "劳动合同法第四十七条规定的经济补偿的月工资按照劳动者应得工资计算，包括计时工资或者计件工资以及奖金、津贴和补贴等货币性收入。"
- URL: https://hrss.suzhou.gov.cn/jsszhrss/zxfgk/201902/398d5ed9f5ee4090929ed33c2dacc7ee.shtml (江苏省劳动合同条例, 2013 revision, posted 2019-02-27). Art. 33 quote: "计发经济补偿的月工资标准为劳动者在劳动合同解除或者终止前十二个月的月平均工资，月平均工资低于当地最低工资标准的，按照最低工资标准确定。"

**F5 (item 5). The base is gross (应得), not take-home pay.**
Status: **stands**
- URL: https://rsj.beijing.gov.cn/bm/ztzl/dxal/201912/t20191206_880166.html
- Quote: "故劳动者经济补偿金的计算标准应以月应得工资而非月实得工资为计算标准。" / "劳动人事争议仲裁委员会经审理，裁决支持了张某的仲裁请求。"

**F6 (item 6, headline 2). The January bonus: 39000 if counted when paid, 36500 under Jiangsu allocation, 36000 as the floor.**
Status: **stands** (correctly marked as varying)
- URL: https://guantao.com/page3092 (观韬 law firm, 2019-01-11, quoting 苏劳人仲委[2017]1号 Part 2 item 10)
- Quote: "劳动者在解除或终止劳动合同前十二个月内的加班工资、年终奖、季度奖应当作为计算平均工资内容。但年终奖、季度奖应当分摊计算至相应的月份，" / "分摊计算后，如果不在劳动合同解除或终止前十二个月内的，不宜作为计发数额。"
- I could not find an official copy of 苏劳人仲委〔2017〕1号 either. The source's "could not verify" flag stays.
- Recomputed: (10000 + 2000) × 12 + 12000 = 156000. 156000 ÷ 12 = 13000, and × 3 = 39000. Under allocation, 144000 + 2000 = 146000. 146000 ÷ 12 = 12166.67, and × 3 = 36500. Leaving the bonus out, 12000 × 3 = 36000.

**F7 (item 7). The 3× average-wage cap and the 12-year cap are not triggered.**
Status: **stands**
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html. Quote: "劳动者月工资高于用人单位所在直辖市、设区的市级人民政府公布的本地区上年度职工月平均工资三倍的，向其支付经济补偿的标准按职工月平均工资三倍的数额支付"
- http://tjj.suzhou.gov.cn/sztjj/rdwd/202606/026a862b9d5e4acfae7e7d4d06d9d15d.shtml (发布日期 2026-06-25): "答：2025年度苏州市城镇非私营单位在岗职工年平均工资为148364元。"
- http://tjj.suzhou.gov.cn/sztjj/rdwd/202606/5c41527977254069a812a7f991ea2447.shtml (2026-06-25): "答：2025年度苏州市城镇非私营单位从业人员年平均工资为146353元。"
- http://tjj.suzhou.gov.cn/sztjj/rdwd/202606/310c055f541f4589a51e9285d54aafbc.shtml (2026-06-25): "答：2025年度苏州市城镇私营单位从业人员年平均工资为88358元。"
- Recomputed: 148364 ÷ 12 × 3 = 37091.00. 146353 ÷ 12 × 3 = 36588.25. 88358 ÷ 12 × 3 = 22089.50. All are above 13000.

**F8 (item 8). Suzhou minimum wage is 2660 a month from 2026-01-01.**
Status: **stands**
- URL: https://www.suzhou.gov.cn/szsrmzf/bmwj/202512/ffb74aa45eda4d88bebe00c2c59999b0.shtml (苏人保〔2025〕8号, 成文日期 2025-12-31)
- Quote: "苏州市区、张家港市、常熟市、太仓市、昆山市均执行江苏省一类地区月最低工资标准，由原2490元/月调整为2660元/月。" / "三、调整后的最低工资标准从2026年1月1日起执行。"
- No later change found. The 2026-01-28 Suzhou HR Q&A (F15) repeats the same figure.

## Side claims that answers may add

**F9 (item 9, headline 3). Jiangsu's "30 days' written notice before expiry" (old Art. 37) was deleted in 2013. Suzhou has no per-day damages. The per-day rule is Beijing's.**
Status: **stands**, with one caution added for graders
- Old text: https://policy.mofcom.gov.cn/claw/clawContent.shtml?id=57944 (时效状态 "已被修改", 发布日期 2003-10-25). Quote: "第三十七条 劳动合同期限届满前，用人单位应当提前三十日将终止或者续订劳动合同意向以书面形式通知劳动者，到期办理终止或者续订劳动合同手续。"
- Current text: https://policy.mofcom.gov.cn/claw/clawContent.shtml?id=18075 ("江苏省劳动合同条例(2013修订)", 时效状态 "现行有效", 实施日期 2013-05-01) and the Suzhou HR copy (F4). Quote (current Art. 37): "第三十七条 劳务派遣单位应当与被派遣劳动者订立二年以上的固定期限劳动合同。"
- I read Chapter 4 (Arts. 31–35) of the 2013 text myself. It has no expiry-notice duty and no per-day damages. The only 30-day notices left are in Art. 18: "用人单位应当在第二次劳动合同期满三十日前，书面告知劳动者可以订立无固定期限劳动合同。"
- 2013 outline: http://jshrss.jiangsu.gov.cn/art/2013/3/21/art_77279_9074968.html (2013-03-21). Quote: "应当提前三十天书面告知劳动者其订立无固定期限条件的权利"
- No amendment in 2025–2026: I checked all seven 2025–2026 package amendment and repeal decisions on https://www.jsrd.gov.cn/qwfb/sjfg/, and none names the regulation. The only package text that mentions 劳动合同 (t20250609_1221333) amends the union-law implementing measures. Gap: I did not open the pre-2025 package decisions. For that period I rely on MOFCOM's "现行有效".
- Caution: the Jiangsu People's Congress site's own entry, https://www.jsrd.gov.cn/qwfb/sjfg/200812/t20081231_1221013.shtml (dated 2008-12-31, no status label), still shows the 2003 text: "第三十七条 劳动合同期限届满前，用人单位应当提前三十日将终止或者续订劳动合同意向以书面形式通知劳动者". The 2013 revision is not in that listing. An answer citing this page for a 30-day notice is still wrong.
- Beijing: https://www.beijing.gov.cn/gongkai/zfxxgk/zc/gz/202201/t20220126_2600689.html ("根据2021年12月30日北京市人民政府第302号令修改"). Quote: "第四十七条 用人单位违反本规定第四十条规定，终止劳动合同未提前30日通知劳动者的，以劳动者上月日平均工资为标准，每延迟1日支付劳动者1日工资的赔偿金。"
- Recomputed for the wrong-claim check: notice was due 2026-10-01 and given on 2026-10-23, so it was 22 days late, with 8 days left before expiry.

**F10 (item 10). No 代通知金 and no N+1 on expiry.**
Status: **stands**
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html. Quote: "第四十条 有下列情形之一的，用人单位提前三十日以书面形式通知劳动者本人或者额外支付劳动者一个月工资后，可以解除劳动合同："

**F11 (item 11). Not 2N. Unpaid compensation is dealt with under Art. 85.**
Status: **stands**
- URL: https://www.sz.gov.cn/cn/xxgk/zfxxgj/zcfg/content/post_8965212.html
- Quote: "第八十七条 用人单位违反本法规定解除或者终止劳动合同的，应当依照本法第四十七条规定的经济补偿标准的二倍向劳动者支付赔偿金。"
- Quote: "（四）解除或者终止劳动合同，未依照本法规定向劳动者支付经济补偿的。" / "逾期不支付的，责令用人单位按应付金额百分之五十以上百分之一百以下的标准向劳动者加付赔偿金："

**F12 (item 12). Certificate on termination, file and social-insurance transfer within 15 days (by 2026-11-15), compensation paid when the handover is done, and the employer's 7-day unemployment filing.**
Status: **stands**, with one addition for the HR message
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html. Quote: "第五十条 用人单位应当在解除或者终止劳动合同时出具解除或者终止劳动合同的证明，并在十五日内为劳动者办理档案和社会保险关系转移手续。" / "用人单位依照本法有关规定应当向劳动者支付经济补偿的，在办结工作交接时支付。"
- Jiangsu Art. 35 (Suzhou copy, F4): "解除或者终止劳动合同时，劳动者应当归还用人单位的财物、技术资料等，并根据用人单位规章制度、双方约定办理工作交接手续。"
- Art. 89 (Shenzhen copy): "由劳动行政部门责令改正；给劳动者造成损害的，应当承担赔偿责任。"
- 7-day filing: https://www.gov.cn/zhengce/202407/content_6963391.htm. Quote: "应将失业人员的名单自终止或者解除劳动合同之日起7日内报受理其失业保险业务的经办机构备案，并按要求提供终止或解除劳动合同证明等有关材料。"
- **Addition (final wages):** https://www.jsrd.gov.cn/qwfb/sjfg/202606/t20260603_1335323.shtml (江苏省工资支付条例, "根据2026年5月27日…第三次修正"). Quote: "第十九条 用人单位与劳动者依法解除或者终止劳动关系的，应当在劳动关系解除或者终止之日起两个工作日内一次性付清劳动者工资。双方另有约定的除外。" The 2026 amendment (https://www.jsrd.gov.cn/qwfb/sjfg/202606/t20260603_1335326.shtml, part 五) changed Arts. 2, 6, 29 and 30 but not Art. 19. 2026-10-31 is a Saturday, so October wages are due by Tuesday 2026-11-03 unless otherwise agreed. Suggested key wording: "10月工资应在终止之日起两个工作日内付清（江苏省工资支付条例第十九条），即约2026年11月3日前。"

## Unemployment benefit

**F13 (item 13). Expiry termination counts as involuntary job loss, so the user qualifies after one year of contributions plus registration.**
Status: **stands**
- URL: https://www.gov.cn/zhengce/202407/content_6963391.htm (third revision "根据2024年6月14日…第三次修订"). Quote: "其中，非因本人意愿中断就业的是指下列人员：" / "（一）终止劳动合同的；"
- Same page, 条例 Art. 14: "（一）按照规定参加失业保险，所在单位和本人已按照规定履行缴费义务满1年的；" / "（三）已办理失业登记，并有求职要求的。"
- URL: http://hrss.suzhou.gov.cn/jsszhrss/zcwd/202408/8ddf1bab677f499bbffd2a1d7e76a00f.shtml (2024-08-27). Quote: "“非因本人意愿中断就业”，主要包括以下情形：劳动合同期满或用人单位主体资格消亡终止劳动合同；"
- The 2026 Suzhou Q&A (F15, Q6) treats a near-identical case as eligible: "沈女士与单位劳动合同到期后不续签需申请失业金".

**F14 (item 14, headline 4). In Jiangsu, benefits run 2 months per full year of contributions, up to 24 months. With 3 years that is 6 months, not "最长12个月".**
Status: **stands**
- URL: http://www.js.gov.cn/art/2025/1/21/art_64797_11476234.html (省政府令第188号, "自2025年3月1日起施行")
- Quote: "失业人员失业前用人单位和本人按照规定累计缴费时间每满1年领取2个月失业保险金，领取失业保险金的期限最长为24个月。"
- National ceiling: http://www.huangshi.gov.cn/zwct/sb567/syjlq/202210/t20221012_948156.html. Quote: "累计缴费时间满1年不足5年的，领取失业保险金的期限最长为12个月;"
- Note on dating: the Suzhou Q&A of 2024-08-27 already described the same practice, "累计缴费每满一年享受2个月，以此类推，最长不超过24个月". So 2025-03-01 is when the rule entered the provincial government rule. The practice predates it. The figure the key uses (6 months) is unaffected.
- Note: the same 2025 text says "重新就业后，再次失业的，缴费时间重新计算". Pooling earlier Jiangsu contributions assumes the user has not drawn benefits since then.
- Not checked in this pass: any national revision of 失业保险条例.

**F15 (item 15). Benefit = 45% of the 12-month average contribution base, capped at the minimum wage, so 2660 a month for this user. Floor 1.5 × 1261 = 1891.50.**
Status: **refuted/needs change** (floor only; the cap stands and is now confirmed officially)
- Formula: https://jshrss.jiangsu.gov.cn/art/2024/10/11/art_89373_11382452.html (reply 2024-09-06). Quote: "缴费不满10年的，按照失业人员失业前12个月月平均缴费基数的45%确定；" / "失业保险金最高不得超过当地最低工资标准，最低不得低于当地城市居民最低生活保障标准的1.5倍。"
- **Official Suzhou 2026 figures:** http://hrss.suzhou.gov.cn/jsszhrss/zcwd/202601/5db431743ec7476aa90e1c6ede0fc91e.shtml (苏州市人社局 "12333热点第47期", 2026-01-28)
- Quote: "根据《关于调整苏州市失业保险金标准的通知》（苏人保就〔2025〕11号），自2026年1月1日起，失业保险金最高标准从2490元/月提高到2660元/月，失业保险金最低标准仍为1812元/月。"
- 低保: https://www.suzhou.gov.cn/szsrmzf/zwgg/202607/cc2b11cac2e346bebfad748539e1ae8d.shtml (2026-07-03). Quote: "最低生活保障标准由1208元/月提高到1261元/月。" / "新的低保、特困生活救助标准自2026年7月1日起执行。"
- Correction: the published floor is **1812** (= 1.5 × the old 低保 of 1208). The source's 1891.50 applies the rule to the 低保 that took effect on 2026-07-01. I found no notice raising the published floor. Suggested wording: "最低标准按已公布的1812元/月（苏人保就〔2025〕11号）；2026-07-01低保提高后是否相应上调，未见公告。" This does not change the user's figure: any base above 5911.11 hits the 2660 cap.
- The "Could not verify: a separately published Suzhou 2026 unemployment-benefit table" entry should be dropped. The 2660 cap is published (above).
- 2026 contribution base: https://www.suzhou.gov.cn/szsrmzf/mszx/202610/66f00381bed6498b9fbb9493287bd6fb.shtml (2026-10-08). Quote: "全省职工基本养老保险缴费工资基数上限标准按25127元执行，下限标准按5025元执行。"
- Medical insurance paid by the fund: Suzhou Q&A (F13). Quote: "失业保险基金为失业人员代缴职工基本医疗保险费、生育保险费，享受相关的待遇，个人无需缴费。" The 2025 Jiangsu decision says the same: "个人不缴纳基本医疗保险（含生育保险）费".
- Recomputed: 2660 ÷ 0.45 = 5911.11. 3 × 2660 = 7980. 6 × 2660 = 15960.

**F16 (item 16). The rule text says claim within 60 days, but Suzhou may not refuse a late claim. Payment runs from the registration date.**
Status: **stands**
- URL: https://www.gov.cn/zhengce/202407/content_6963391.htm. Quote: "第六条 失业人员应在终止或者解除劳动合同之日起60日内到受理其单位失业保险业务的经办机构申领失业保险金。" / "经审核合格者，从其办理失业登记之日起计发失业保险金。"
- Suzhou Q&A (F13). Quote: "参保人员失业后，申领失业保险金没有时间限制。（详见《人力资源社会保障部办公厅关于进一步推进失业保险金“畅通领、安全办”的通知》（人社厅发〔2020〕24号：不得以超过60日申领期限为由拒发失业保险金）"

## Other money points

**F17 (item 17). Untaken annual leave is paid out on a prorated basis at an extra 200% per day.**
Status: **stands**
- URL: https://www.gov.cn/gongbao/content/2009/content_1265995.htm (人社部令第1号)
- Quote (Art. 12): "前款规定的折算方法为：（当年度在本单位已过日历天数÷365天）×职工本人全年应当享受的年休假天数-当年度已安排年休假天数。" Also: "但折算后不足1整天的部分不支付未休年休假工资报酬。"
- Quote (Art. 10): "按照其日工资收入的300%支付未休年休假工资报酬，其中包含用人单位支付职工正常工作期间的工资收入。"
- Quote (Art. 11): "前款所称月工资是指职工在用人单位支付其未休年休假工资报酬前12个月剔除加班工资后的月平均工资。"
- URL: https://www.gov.cn/gongbao/content/2008/content_859865.htm. Quote: "第三条 职工累计工作已满1年不满10年的，年休假5天；已满10年不满20年的，年休假10天；已满20年的，年休假15天。"
- Recomputed: 2026-01-01 to 10-31 is 304 days. 5 × 304/365 = 4.16, so 4 days. 13000 ÷ 21.75 = 597.70, and × 2 = 1195.40 a day. × 4 = 4781.61. On the no-bonus base: 551.72 a day, 1103.45 extra a day, 4413.79 for 4 days.

**F18 (item 18). Income tax on expiry compensation is disputed.**
Status: **stands**
- URL: https://www.gov.cn/zhengce/zhengceku/2018-12/31/content_5440172.htm (财税〔2018〕164号, 成文日期 2018年12月27日). Quote: "（一）个人与用人单位解除劳动关系取得一次性补偿收入（包括用人单位发放的经济补偿金、生活补助费和其他补助费），在当地上年职工平均工资３倍数额以内的部分，免征个人所得税；"
- Same notice: "八、除上述衔接事项外，其他个人所得税优惠政策继续按照原文件规定执行。" Section 五 has no sunset date. The 2021-12-31 dates appear only in sections 一 and 二.
- URL: http://zhejiang.chinatax.gov.cn/art/2023/2/8/art_25980_1298.html (浙江财税12366, 答复时间 2020-07-21). Quote: "因此，劳动合同到期后，不再续聘所发放的补偿金不属于财税〔2018〕164号文规定的解除合同的一次性补偿金，应在发放当月合并工资薪金计税。"
- URL: https://jiangsu.chinatax.gov.cn/art/2024/7/19/art_16876_4261.html (答复时间 2024-07-18). This reply concerns a Suzhou dismissal ("辞退一名工作1年的员工") and only restates 164号. It does not address expiry.
- Recomputed: 3 × 88358 = 265074. 3 × 146353 = 439059. 3 × 148364 = 445092.

**F19 (item 19). Arbitration has a one-year limit and no fee. A 39000 claim is above the finality threshold of 31920.**
Status: **stands**
- URL: https://chinajob.mohrss.gov.cn/h5/c/2022-07-15/356212.shtml (主席令八十号, page 2022.07.15)
- Quote: "第二十七条 劳动争议申请仲裁的时效期间为一年。仲裁时效期间从当事人知道或者应当知道其权利被侵害之日起计算。" / "第五十三条 劳动争议仲裁不收费。"
- Quote: "（一）追索劳动报酬、工伤医疗费、经济补偿或者赔偿金，不超过当地月最低工资标准十二个月金额的争议；"
- Recomputed: 12 × 2660 = 31920.
- Related new rule, no change to the key: 劳动争议解释（二） Art. 20 bars raising a limitation defence for the first time in court, unless based on new evidence.

**F20 (item 20). This is a first fixed-term contract, so there is no right to an open-ended renewal.**
Status: **stands**, with one optional addition
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html. Quote: "（三）连续订立二次固定期限劳动合同，且劳动者没有本法第三十九条和第四十条第一项、第二项规定的情形，续订劳动合同的。"
- Addition: https://www.court.gov.cn/fabu/xiangqing/472691.html (法释〔2025〕12号, 发布时间 2025-08-01, in force 2025-09-01). Art. 10 lists the situations treated as "连续订立二次". Among them: "（一）用人单位与劳动者协商延长劳动合同期限累计达到一年以上，延长期限届满的；" and "（三）…用人单位变换劳动合同订立主体，但继续对劳动者进行劳动管理，合同期限届满的；". None fits a single 3-year contract with no extension and no change of employing entity. The source's conclusion holds.

**F21 (item 21). The contract is extended if an Art. 42 situation exists at expiry (Art. 45).**
Status: **stands**, with one optional addition
- URL: https://sfj.beijing.gov.cn/sfj/sfdt/fzxc74/387021/index.html. Quote: "第四十五条 劳动合同期满，有本法第四十二条规定情形之一的，劳动合同应当续延至相应的情形消失时终止。"
- Addition: 解释（二） Art. 8 (same URL as F20) adds an unexpired service period and an unexpired union-committee term: "（二）劳动合同法实施条例第十七条规定的服务期尚未到期的；" / "（三）工会法第十九条规定的任期未届满的。" The request contains no such facts.

**F22 (item 22). A pro-rata 2026 year-end bonus is uncertain.**
Status: **stands**
- URL: https://www.court.gov.cn/fabu/xiangqing/364671.html (指导案例183号, 发布时间 2022-07-06)
- Quote: "但劳动合同的解除非因劳动者单方过失或主动辞职所导致，且劳动者已经完成年度工作任务，用人单位不能证明劳动者的工作业绩及表现不符合年终奖发放标准，年终奖发放前离职的劳动者主张用人单位支付年终奖的，人民法院应予支持。"
- The case involved a completed year. A user leaving after 10 months fits "check the company's rules", not "you will get 10/12".

## Facts for the key: summary

- Key 1–8 (premise, N = 3, base, 39000 / 36500 / 36000, caps, payment timing): **stand**.
- Key 9 (HR message): **stands**. Add the two-working-day rule for final wages and the date 2026-11-03 (F12).
- Key 10 (budget figures): **stands**. 2660 a month, 7980 for 3 months.
- Key 11 (Jiangsu 6 months, the "5850" figure wrong): **stands**. Optional: say the 2-months-per-year practice predates 2025-03-01 (F14).
- Key 12–19: **stand**. Optional additions from 解释（二） in F20 and F21.
- "因人因地而异": **stands**.
- Could-not-verify list: drop the "Suzhou 2026 benefit table" entry (F15). Keep the 苏劳人仲委〔2017〕1号 entry and the cap-figure entry. Add: "公布的失业保险金最低标准1812元/月是否随2026-07-01低保上调而调整，未见公告。"

## Not decided in this pass
- An official copy of 苏劳人仲委〔2017〕1号. Only the law firm's quotation was found.
- Which of the 15 laws are in the State Council amendment package set for the NPCSC session of 2026-11-02 to 11-06. Nothing from it can be in force by 2026-10-25.
- Any national revision of 失业保险条例.
- Jiangsu package amendments before 2025, which I did not open one by one. MOFCOM/北大法宝 lists the 2013 revision as "现行有效".
