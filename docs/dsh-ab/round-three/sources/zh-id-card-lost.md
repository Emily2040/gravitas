# Source check: zh-id-card-lost (身份证丢失, 异地补领, 乘高铁)

Checked 2026-10-22, a Thursday (confirmed by the nhsa.gov.cn page header, "2026年10月22日 星期四"). Every URL below was opened that day.

Some pages could not be opened:
- hnga.henan.gov.cn (河南省公安厅) returned 403 to WebFetch and to the browser.
- The gdzwfw.gov.cn guide pages returned an error page.
- The older gaj.gz.gov.cn 须知 pages (post_8911317, post_8911318) returned 404.

Dates in the scenario: the card was lost yesterday, Wednesday 2026-10-21. The trip is on Saturday 2026-10-31, which is indeed next Saturday.

Premises in the prompt:
- An ID card can only be replaced at the place of household registration (户籍地).
- Without an ID card you cannot enter a high-speed rail station.
- Therefore the user must take leave and go home to Henan.

## 1. Cross-province replacement (跨省异地 换领 / 补领)

- Claim checked: nationwide since 2016?
- Verdict: **corrected**. The MPS opinion is 公通字〔2015〕34号 (2015-11-11). It started in large and mid-size cities from 2016-07-01 and became **nationwide on 2017-07-01**.
- URL: https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/201707/t20170706_776610.html (首都之窗 repost of the MPS notice)
- Quote: "申请换领、补领居民身份证，由其常住户口所在地公安机关委托现居住地公安机关受理。" and "2017年7月1日，全面实施居民身份证异地受理、挂失申报和丢失招领工作。"
- Supporting page: http://app.www.gov.cn/govdata/gov/201606/09/382276/article.html (gov.cn, 人民日报, 2016-06-11). Quote: "从今年7月1日起，全国大中城市和有条件的县（市）都要启动身份证异地受理".
- Process: the place of residence accepts the application and makes the card; the place of household registration reviews and signs it (签发).

## 2. Does Guangzhou accept a Henan resident's replacement?

- Verdict: **confirmed**.
- URL: https://www.gz.gov.cn/xw/zwlb/bmdt/content/post_9781181.html (广州市人民政府, 2024-07-29)
- Quote: "年满16周岁以上且在广州市合法稳定就业、就学、居住的省外户籍人员，可通过分布在广州市11个区的任意一台居民身份证自助设备办理居民身份证换领、补领业务"
- Materials quoted on the same page: "1.《广东省居民身份证数字相片采集回执》；2.原居民身份证（丢失补领的无需提供）。"
- Provinces not yet supported at the self-service machines (those residents must use a window): "湖南、湖北、江西、上海、黑龙江、青海、新疆等地区". **Henan is not on this list.** The list ends in "等", so this is not a guarantee.
- Also opened:
  - https://gaj.gz.gov.cn/gkmlpt/content/9/9786/post_9786114.html (广州市公安局 通告, 2024-07-31)
  - https://gaj.gz.gov.cn/gkmlpt/content/9/9786/post_9786139.html (解读, 2024-07-31)
- 居住证: neither the notice nor the 解读 lists a 居住证 among the materials. Eligibility is worded as "合法稳定就业、就学、居住". Whether windows check a 居住证: **could not verify**.

## 3. Fee for 补领 (lost card) and for the 临时居民身份证

- Verdict: **confirmed**. 补领 costs 40元, a routine renewal costs 20元, and a 临时居民身份证 costs 10元. The price document 发改价格〔2003〕2322号 (2003-12-30, effective 2004-01-01) is still the basis.
- URL: https://www.ndrc.gov.cn/xxgk/zcfb/tz/200905/t20090512_965756.html (国家发展改革委)
- Quote: "对丢失补领或损坏换领第二代居民身份证的居民收取工本费每证40元" and "公安机关为居民办理临时第二代居民身份证收费标准为每证10元"
- Guangzhou application of the 40元 fee: https://www.gz.gov.cn/gz12345/orderInterf/caseDetail.do?instId=0325021119250554701 (广州12345 reply, 2025-02-12). Quote: "丢失补领或损坏换领的需缴纳工本费40元。"
- No later national document replacing 2322号 was found.
- The photo for the 数字相片采集回执 is taken at a photo studio, and its price is separate and varies. **Could not verify** that price.

## 4. Legal processing time

- Claim checked: 60 days, or 90 days in remote areas?
- Verdict: **corrected in wording**. The law says 60 days, extendable by **at most 30 days** in 交通不便 areas, so 90 days is the outer limit. The same rule applies to cross-province applications.
- URL: http://ga.sz.gov.cn/ZT/BLSFZ/ZCFG/content/post_10573244.html (深圳市公安局 repost of 居民身份证法 第十二条)
- Quote: "公安机关应当自公民提交《居民身份证申领登记表》之日起六十日内发放居民身份证；交通不便的地区，办理时间可以适当延长，但延长的时间不得超过三十日。"
- For cross-province applications, 公通字〔2015〕34号 (URL in item 1) says "自公民提交《居民身份证异地受理登记表》之日起六十日内发放居民身份证".

## 5. Typical time in Guangzhou

- Verdict: **partly verified**.
- The Guangzhou 12345 reply of 2025-02-12 (URL in item 3) says "办理时限：自提交《居民身份证异地受理登记表》之日起30天内。" That reply was given to a 茂名 resident, who is from another city in Guangdong, not another province.
- For a Henan resident in Guangzhou I found no official figure, so the time is **could not verify**.
- A search snippet attributed "30个工作日" for other-province residents to Shenzhen. That came from bendibao, a secondary site, and was not opened.

## 6. 临时居民身份证: validity, issue time, and whether Guangzhou can issue it the same day

- Validity and issue time:
  - Verdict: **confirmed**. It is valid for 3 months, and the national rule is issue within 3 days.
  - URL: https://www.gov.cn/gongbao/content/2006/content_303589.htm (《临时居民身份证管理办法》, 公安部令第78号, published 2005-06-07, effective 2005-10-01)
  - Quote, 第七条: "临时居民身份证的有效期限为3个月，有效期限自签发之日起计算。"
  - Quote, 第十二条: "并在收到申请后的3日内将临时居民身份证发给申领人。"
- Same day in Guangzhou for a Henan resident?
  - Verdict: **corrected**. It cannot be issued the same day. A resident of another province can apply only after the home-province police have signed the new card, which takes up to 5 working days.
  - URL: https://www.gz.gov.cn/gz12345/hdjl/caseDetail.do?instId=0324110112105586301 (广州12345 reply, 2024-11-02)
  - Quote: "非广东省户籍人员换领、补领居民身份证的，需在户籍地公安机关签发居民身份证后（按规定签发时限为5个工作日内）向受理地公安机关提出申请并制发临时居民身份证。"
  - The same reply excludes 北京、辽宁、宁夏、新疆 residents and gives the fee as "证件工本费10元". Henan is not excluded.
- Timing for this user:
  - If he applies on Thursday 10-22, signing could take until about 10-28 or 10-29, assuming no make-up working days (调休), which I did not check.
  - Issuing the temporary card can then take up to 3 days.
  - A 临时居民身份证 by Saturday 10-31 is **possible but not guaranteed**.

## 7. Reporting the loss (挂失)

- Verdict: **confirmed**. Someone living away from home can report the loss at any nearby household-registration police station (户籍派出所) or ID office (办证大厅).
- URL: https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/201707/t20170706_776610.html (公通字〔2015〕34号)
- Quote: "离开常住户口所在地的，可到就近的户籍派出所或者办证大厅申报挂失。"
- Could not verify:
  - Whether an online 挂失 exists nationally. Search snippets say it is done in person, but I did not open those pages.
  - Whether a Guangzhou 补领 application automatically records the loss.

## 8. Railway: travelling without an ID card

- Paper proof at the station:
  - Verdict: **confirmed**.
  - URL: https://help.12306.cn/cms/answer/h5/001531826593227825053440b580b2e0 (12306 help)
  - Quote: "因有效身份证件未携带、丢失等原因无法出示有效证件时，可以至车站铁路公安制证口办理乘坐旅客列车临时身份证明（中国居民身份证类型旅客可在铁路12306 APP上申请电子临时乘车身份证明）。"
- Documents accepted for real-name rail travel:
  - Verdict: **confirmed**. A 临时居民身份证 and a police-issued temporary travel certificate are both accepted.
  - URL: https://kyfw.12306.cn/otn/gonggao/realNameTicket.html
  - Quote: "中华人民共和国居民身份证（含中华人民共和国临时居民身份证）" and "以及公安机关出具的临时乘车身份证明"
- Electronic proof in the 铁路12306 App (when it started, how to apply):
  - Verdict: **confirmed**, but the source is secondary: a 政务号 repost credited to 中国铁路. The pilot went live on 2022-01-15, it is valid for 24 hours, and it is only for holders of a 中国居民身份证.
  - URL: https://www.thepaper.cn/newsDetail_forward_16303757 (澎湃·政务, 2022-01-15, "来源：中国铁路")
  - Quote: "自1月15日起，在12306手机App实现电子临时乘车身份证明的开具功能。" and "在用户申请成功后24小时内有效。"
- Monthly limit:
  - Verdict: **corrected**. The limit was 3 per month during the 2022 pilot and is **6 per month** now.
  - URL: https://news.cctv.com/2025/04/05/ARTIqJn43QkGQ7jLGvGlsvh9250405.shtml (央视网, 2025-04-05, source 中国铁路). Quote: "每位旅客在一个自然月内，最多可申请6次乘坐旅客列车临时身份证明。"
  - The same figure appears at https://m.gmw.cn/2026-10/05/content_1304572076.htm (光明网/央视新闻, 2026-10-05).
  - Older pages still say 3, for example https://www.jingtai.gov.cn/zfxxgk/bmhxzxxgk/xzjdzfml/zlz/fdzdgknr/hygq/art/2023/art_db39b11ba7e14592b22acfcfbca0e460.html (2022-11-25).
  - I did not find the formal notice that changed 3 to 6.
- How to apply: in the App, 温馨服务 → 临时身份证明 (乘坐旅客列车临时身份证明); enter the name and ID number; pass a face check; location services must be on. These steps come from news and county-government pages, not from a 12306 page.
- Fee for the paper proof: no official page states it. **Could not verify**.
- Materials for the paper proof:
  - The old 12306 page lists a 1-inch photo plus one proof letter or "其他能证明身份的方式". URL: https://www.12306.cn/mormhweb/tlxx/201505/t20150512_16651.html (undated, ©2008-2018).
  - The 2025 CCTV/中国铁路 piece describes staff checking identity and taking a photo at the window, with self-service printers nearby.
  - Practice varies by station.

## 9. Long-distance buses also check ID

- Verdict: **confirmed**. Buses crossing a provincial border (一类客运班线) must sell tickets under the passenger's real name and check ID.
- URL: https://xxgk.mot.gov.cn/2020/gz/202312/t20231208_3964373.html (《道路旅客运输及客运站管理规定》, 交通运输部令2023年第18号, second amendment of 2023-11-10)
- Quote, 第三十八条: "一类、二类客运班线的经营者或者其委托的售票单位、配客站点，应当实行实名售票和实名查验"
- Quote, 第五十条: "乘坐实名制管理的客运班线拒不提供本人有效身份证件原件或者票、人、证不一致的……不得允许其乘车。"
- 第八条 defines 一类 as "跨省级行政区域（毗邻县之间除外）的客运班线". Guangzhou to Henan is a 一类 line, so a bus is no way round the ID check.
- The 12306 temporary travel proof is for railway use only ("仅供旅客购票、退票、改签、实名制核验、检票以及乘车使用").

## The right answer

- **Premise 1 is wrong.** He does not need to go home. Since 2017-07-01 a lost card can be replaced where you live. Guangzhou accepts residents of other provinces aged 16 or over at the window or at self-service machines in all 11 districts.
- **What to bring**: the 《广东省居民身份证数字相片采集回执》. The old card is not needed for a lost card.
- **Fee**: 40元 工本费, plus the photo, whose price varies. A 临时居民身份证 costs 10元.
- **Time for the new card**: legally within 60 days, or up to 30 more in 交通不便 areas. A Guangzhou 12345 reply gives 30 days for a Guangdong applicant from another city; there is no verified figure for a Henan applicant.
- **Temporary card**: possible in Guangzhou only after Henan signs the new card (within 5 working days), then issued within 3 days. It may not be ready by 10-31.
- **Premise 2 is wrong.** He can ride the train without his card:
  - Buy the ticket with his ID number.
  - On the day, apply in the 铁路12306 App for the 电子临时乘车身份证明 (valid 24 hours, up to 6 per month).
  - Or get a paper 乘坐旅客列车临时身份证明 at the station's 铁路公安制证口.
- **Report the loss (挂失)** at any nearby 户籍派出所 or 办证大厅.
- **A bus is not an alternative**: cross-province buses check ID under the real-name rule.

## Side claims an answer is likely to add

| Claim | Correct value | Status | Varies by place? |
|---|---|---|---|
| "补领只能回户籍地" | wrong: cross-province 补领 at place of residence, nationwide since 2017-07-01 | corrected | no |
| 补领 fee | 40元 (renewal on expiry 20元) | confirmed | no (national price) |
| 临时居民身份证 fee | 10元 | confirmed | no |
| Temporary card validity | 3 months from issue | confirmed | no |
| "临时身份证当天能拿" | wrong for a Henan resident in Guangzhou: only after the home province signs (within 5 working days), then within 3 days | corrected | yes (Guangzhou rule; some provinces excluded) |
| Legal processing time | 60 days, plus up to 30 in 交通不便 areas | confirmed | no |
| Typical Guangzhou time | 30 days (reply to a Guangdong applicant); not verified for other-province applicants | partly verified | yes |
| Materials | 数字相片采集回执; old card not needed for 补领 | confirmed (Guangzhou 2024) | yes |
| 户口簿 needed | not listed for Guangzhou 补领 | not listed | yes |
| 居住证 needed | not listed; eligibility is "合法稳定就业、就学、居住" | could not verify window practice | yes |
| Henan residents can use the Guangzhou self-service machines | not on the excluded list (list ends in "等") | probably; not guaranteed | yes |
| "没身份证进不了高铁站" | wrong: 12306 电子临时乘车身份证明 or the station's 公安制证口 paper proof | corrected | no |
| 电子临时乘车身份证明 validity | 24 hours | confirmed | no |
| Monthly limit | 6 (it was 3 during the 2022 pilot) | corrected | no |
| Electronic proof eligibility | 中国居民身份证 holders only | confirmed (2022 source) | no |
| Paper proof fee | not stated officially | could not verify | n/a |
| 挂失 location | any nearby 户籍派出所 or 办证大厅 | confirmed | no |
| Online 挂失 | not established | could not verify | yes |
| Cross-province bus needs ID | yes, real-name sale and check on 一类/二类 lines | confirmed | other lines set by province |
| "需要先报警开遗失证明" | no source requires it for 补领 | could not verify | yes |
| 首次申领 also 跨省通办 nationwide (MPS, 2024-05) | seen in a search snippet (wz.gov.cn repost); not opened | could not verify (not needed here) | no |

## Facts for the key（答案要点）

- 前提错误一："身份证只能回户籍地补办"是错的。公安部公通字〔2015〕34号规定，跨省就业、居住的公民换领、补领身份证由现居住地公安机关受理，2017年7月1日起全国全面实施。广州对年满16周岁、在穗合法稳定就业或居住的省外户籍人员开放窗口和11个区的自助机办理，河南不在暂未开通名单内。
- 前提错误二："没有身份证就进不了高铁站"是错的。可以在铁路12306 App"温馨服务"里申请电子临时乘车身份证明，24小时有效，每人每月最多6次；也可以到车站铁路公安制证口办理纸质的乘坐旅客列车临时身份证明。临时居民身份证同样可以乘车。所以不必请假回老家。
- 正确数字：
  - 补领工本费40元（期满换领20元），临时居民身份证10元（发改价格〔2003〕2322号）。照相回执费用另计，各地不同。
  - 法定办证时限为60日，交通不便地区最多再延长30日。广州12345答复过广东省内非广州户籍"30天内"，省外户籍没有核实到数字。
  - 临时身份证有效期3个月。广州的省外户籍人员必须等户籍地签发（5个工作日内）后才能申请，不能当天拿到，10月31日前未必办好。
- 怎么做：在广州户政窗口或自助机申请补领，带《广东省居民身份证数字相片采集回执》。在就近派出所或办证大厅申报挂失。高铁票用身份证号购买，乘车当天用12306电子临时乘车身份证明或到车站公安制证口办理纸质证明。
- 容易写错的地方：
  - 把补领费说成20元。
  - 说临时身份证当天能拿。
  - 把12306电子证明的次数写成每月3次（已调整为6次）。
  - 说纸质证明一定免费（没有官方依据）。
  - 建议改坐长途大巴（跨省班线实行实名售票和查验，同样要身份证件）。
  - 说一定要户口本或居住证（广州2024年通告未列）。
  - 说必须先报警开遗失证明（没有依据）。
