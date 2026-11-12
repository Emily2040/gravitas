# zh-express-lost: source check

Checked 2026-10-22. Every URL below was opened on that date (curl or WebFetch). Quotes are copied from the opened page. Statutes are quoted from official government copies. Where only a secondary source exists, the entry says so.

Prompt premise under test: the courier's customer service says that under 《邮政法》, a lost parcel without 保价 can only be compensated at 3 times the freight (18 元 × 3 = 54 元), and the user accepts this as "法律这么规定".

---

## 1. 《邮政法》 第四十五条, 第四十七条, 第五十九条: what the 3x cap covers

**Verdict: corrected.** The 3x cap is in 第四十七条, but it covers only 给据邮件 sent by a 邮政企业 within 邮政普遍服务. 第五十九条 extends only 第四十五条第二款 to 快件, and that paragraph sends compensation to civil law. The 3x cap is never extended to 快件. "邮政法规定没保价的快递只能赔3倍运费" is wrong for a private express company.

- URL: https://www.spb.gov.cn/gjyzj/c100009/c100012/201504/a19db232da254cfe9f9f79701f278abd.shtml (国家邮政局 copy of the current text)
- Current version: adopted 1986, revised 2009-04-24, amended 2012-10-26 and 2015-04-24. No later amendment appears in the header.
  > 根据2015年4月24日第十二届全国人民代表大会常务委员会第十四次会议《关于修改〈中华人民共和国义务教育法〉等五部法律的决定》第二次修正
- 第四十五条:
  > 邮政普遍服务业务范围内的邮件和汇款的损失赔偿，适用本章规定。
  > 邮政普遍服务业务范围以外的邮件的损失赔偿，适用有关民事法律的规定。
- 第四十七条第一款第（二）项 (the 3x cap):
  > (二)未保价的给据邮件丢失、损毁或者内件短少的，按照实际损失赔偿，但最高赔偿额不超过所收取资费的三倍；
- 第四十七条第三款 (the cap is lost even for the postal enterprise in these cases):
  > 邮政企业因故意或者重大过失造成给据邮件损失，或者未履行前款规定义务的，无权援用本条第一款的规定限制赔偿责任。
- 第五十九条 (last clause):
  > 第四十五条第二款关于邮件的损失赔偿的规定，适用于快件的损失赔偿。
- 第八十四条 definitions (邮件 and 快件 are different things):
  > 邮件，是指邮政企业寄递的信件、包裹、汇款通知、报刊和其他印刷品等。
  > 快件，是指快递企业递送的信件、包裹、印刷品等。
- 第十五条 (scope of 普遍服务, run by 邮政企业 only):
  > 邮政企业应当对信件、单件重量不超过五千克的印刷品、单件重量不超过十千克的包裹的寄递以及邮政汇兑提供邮政普遍服务。

A court said the same thing (广州市花都区人民法院, official court site, see item 5):
> 非邮政企业从事的快递业务并非邮政普遍服务业务，不能直接适用我国《中华人民共和国邮政法》中关于限额赔偿的规定。

## 2. 《快递市场管理办法》 (交通运输部令2023年第22号)

**Verdict: confirmed (order number and dates); corrected (content).** The 办法 has **no** article that sets compensation for lost 未保价 parcels. It requires the company to tell senders the 保价 rules, to publish its 损失赔偿 rules, and not to set unfair terms. The 未保价 rule is in 《快递暂行条例》 (see 2a).

- URL: https://xxgk.mot.gov.cn/jigou/fgs/202401/P020240104504317085126.pdf (交通运输部 PDF; text extracted with pdftotext)
- Order and dates:
  > 中华人民共和国交通运输部令 2023 年第 22 号
  > 《快递市场管理办法》已于 2023 年 12 月 8 日经第 28 次部务会议通过，现予公布，自 2024 年 3 月 1 日起施行。
- 第二十六条（一）（二） (no unfair terms; duty to tell the sender the 保价 rules):
  > （一）……不得设定不公平、不合理的交易条件，不得强制交易；
  > （二）提醒寄件人在提供快递运单信息前，认真阅读快递服务合同条款……告知相关保价规则和保险服务项目；
- 第二十二条 (publish 损失赔偿 rules): "……资费标准、快件查询、损失赔偿、投诉处理等服务事项。"
- 第三十条 (complaint, then 申诉 to the postal regulator):
  > 用户对投诉处理结果不满意或者投诉没有得到及时处理的，可以提出快递服务质量申诉。
- A text search of the whole 办法 finds "赔偿" only in 第二十二条 and "保价" only in 第二十六条. No later amendment of the 办法 was found (search, 2026-10-22).

## 2a. 《快递暂行条例》 (added: this is where the 未保价 rule is)

**Verdict: confirmed, with a numbering correction.** The rule is "未保价 → 民事法律". Since the 2025 revision (in force 2025-06-01) it is **第二十八条**. It was 第二十七条 before. Answers that cite "第二十七条" are using the old numbering.

- Current text (third revision, 2026-08-08): https://www.mee.gov.cn/ywgz/fgbz/xzfg/202610/t20261009_1175902.shtml
  > 根据2025年4月13日《国务院关于修改〈快递暂行条例〉的决定》第二次修订 根据2026年8月8日《国务院关于修改和废止部分行政法规的决定》第三次修订
  > 第二十八条 快件延误、丢失、损毁或者内件短少的，对保价的快件，应当按照经营快递业务的企业与寄件人约定的保价规则确定赔偿责任；对未保价的快件，依照民事法律的有关规定确定赔偿责任。
- 第二十二条 (duty to tell the sender; the company may ask for 保价 on valuables):
  > 经营快递业务的企业在寄件人填写快递运单前，应当提醒其阅读快递服务合同条款……告知相关保价规则和保险服务项目。
  > 寄件人交寄贵重物品的，应当事先声明；经营快递业务的企业可以要求寄件人对贵重物品予以保价。
- 2025 decision, 国务院令第806号, in force 2025-06-01: https://www.mee.gov.cn/zcwj/gwywj/202504/t20250422_1117316.shtml
  > ……现予公布，自2025年6月1日起施行。
- 2026 decision, 国务院令第843号, in force 2026-08-15. It changes only 第五十六条第一款 (the names of environmental laws), not 第二十八条/第二十九条: https://www.mee.gov.cn/zcwj/gwywj/202608/t20260814_1164034.shtml
- Old numbering, 2018 text: https://www.gov.cn/zhengce/content/2018-03/27/content_5277801.htm. It has "第二十七条 快件延误、丢失……对未保价的快件，依照民事法律的有关规定确定赔偿责任。" and "第二十八条 ……应当自接到投诉之日起7日内予以处理并告知用户。"

## 3. GB/T 27917 《快递服务》

**Verdict: partly confirmed, partly could not verify.**
- Confirmed: the current Part 3 is **GB/T 27917.3-2023** 《快递服务 第3部分：服务环节》. It is a **推荐性** national standard with status 现行. It was issued 2023-12-28, took effect 2024-04-01, and wholly replaces GB/T 27917.3-2011.
  - URL: https://std.samr.gov.cn/gb/search/gbDetailed?id=0DF2F72AE2BC403DE06397BE0A0A87C4 (全国标准信息公共服务平台)
    > 国家标准 推荐性 现行 …… 发布于 2023-12-28 实施于 2024-04-01 …… 代替了以下标准 GB/T 27917.3-2011 （全部代替）
  - 国家邮政局 news, 2024-01-25: https://www.spb.gov.cn/gjyzj/c100015/c100016/202401/f9d065b4b3a148b2948ee97c6a594eb6.shtml ("新版《快递服务》国家标准将于4月1日实施"). It lists the main changes (terms, delivery time limits, worker rights, data security) and says nothing about compensation.
- Could not verify: the wording of the **2023** annex on 未保价 compensation. The full text was not available in readable form.
- Verified for the superseded **2011** edition only (国家邮政局 辽宁局 copy, posted 2023-10-18): https://ln.spb.gov.cn/lnsyzglj/c202495/202310/3533159e016e4e7794e88e53d9593804.shtml. Annex A (规范性附录) says that for a lost parcel the 服务费 is waived and:
  > b ）对于没有购买保价的快件，按照《中华人民共和国邮政法》、《中华人民共和国合同法》 等相关法律规定赔偿；
  - The 2011 edition also had A.1 赔付对象 "寄件人或寄件人指定的受益人", a 24 h claim acknowledgment, 30 calendar days for claim handling (domestic), payment within 7 working days after agreement, and a parcel "彻底延误（丢失）" after the promised time + 7 calendar days. **These are 2011 values. Whether the 2023 edition keeps them was not verified.**
- In neither edition is there a national-standard rule that a lost 未保价 parcel gets "3 times the freight".

## 4. 《民法典》 第四百九十六条, 第四百九十七条, 第五百零六条, 第八百三十二条, 第八百三十三条

**Verdict: confirmed.** (npc.gov.cn's 民法典 page redirected to the site homepage. Text taken from the 司法部 copy.)
- URL: https://www.moj.gov.cn/pub/sfbgw/zwgkztzl/2025nianzhuanti/2025mfdxcy/2025mfdxcy_mfdql/202505/t20250507_518708.html
- 第四百九十六条第二款:
  > 提供格式条款的一方未履行提示或者说明义务，致使对方没有注意或者理解与其有重大利害关系的条款的，对方可以主张该条款不成为合同的内容。
- 第四百九十七条（二）:
  > （二）提供格式条款一方不合理地免除或者减轻其责任、加重对方责任、限制对方主要权利；
- 第五百零六条:
  > 合同中的下列免责条款无效：……（二）因故意或者重大过失造成对方财产损失的。
- 第八百三十二条:
  > 承运人对运输过程中货物的毁损、灭失承担赔偿责任。但是，承运人证明货物的毁损、灭失是因不可抗力、货物本身的自然性质或者合理损耗以及托运人、收货人的过错造成的，不承担赔偿责任。
- 第八百三十三条:
  > 货物的毁损、灭失的赔偿额，当事人有约定的，按照其约定；没有约定或者约定不明确，依据本法第五百一十条的规定仍不能确定的，按照交付或者应当交付时货物到达地的市场价格计算。法律、行政法规对赔偿额的计算方法和赔偿限额另有规定的，依照其规定。
- Related, also confirmed on the same page:
  - 第五百九十二条第二款 (reduction for the sender's own fault): "当事人一方违约造成对方损失，对方对损失的发生有过错的，可以减少相应的损失赔偿额。"
  - 第一百八十八条: "向人民法院请求保护民事权利的诉讼时效期间为三年。"
- Related, 最高法 合同编通则解释 (法释〔2023〕13号, in force 2023-12-05) 第十条第三款. URL: https://www.court.gov.cn/fabu/xiangqing/419382.html
  > 提供格式条款的一方对其已经尽到提示义务或者说明义务承担举证责任。对于通过互联网等信息网络订立的电子合同，提供格式条款的一方仅以采取了设置勾选、弹窗等方式为由主张其已经履行提示义务或者说明义务的，人民法院不予支持……
- Related, 《消费者权益保护法》 第二十六条第二、三款 (2013 text, 北京市市场监管局 copy; no later amendment seen in its header). URL: https://scjgj.beijing.gov.cn/cxfw/flfgcxfw/xfzqybhl/202006/t20200618_1928074.html
  > 经营者不得以格式条款、通知、声明、店堂告示等方式，作出排除或者限制消费者权利、减轻或者免除经营者责任……
  > 格式条款、通知、声明、店堂告示等含有前款所列内容的，其内容无效。

## 5. Court practice on lost 未保价 parcels

**Verdict: confirmed that outcomes vary. Courts do not apply a statutory "3x freight" cap to express companies.** A limit clause binds only if it was properly highlighted and explained. Even then it gives way to 故意/重大过失. Courts often reduce the award when the sender did not declare the value or insure (过失相抵). I found no 最高法 公报案例 or 典型案例 on exactly this point. The 人民法院案例库 entries below were read through secondary sites, because rmfyalk.court.gov.cn needs a login.

a) **广州市花都区人民法院, phone accessories, 未保价, clause "最高赔偿不超过300元/票". Actual loss awarded: 30,964 元. Upheld on appeal by 广州中院.** Official court site, posted 2018. This was decided under the old 合同法, and the same rule is now in 民法典 496.
- URL: https://www.gzhdcourt.gov.cn/ssfw/jdal/2018/10/29103131595.html
  > Y速递公司亦未提供其它证据证明其已采取合理方式对该条款向李先生进行说明，故根据《中华人民共和国合同法》第四十条的规定，该条款无效。Y速递公司应按照李先生的实际损失进行赔付。
- Evidence the court accepted:
  > 淘宝交易聊天截图、备货截图、进货单、微信聊天记录、支付宝转账记录及淘宝订货记录等证据已经形成完整证据链

b) **河南省新野县人民法院, published 2026-09-21. 未保价 parcel lost, clause "未保价最高赔1000元" (运费九倍, 封顶一千). The clause was not part of the contract. Fault split 60/40, award 13,002.43 元.** Official court site.
- URL: https://xyxfy.hncourt.gov.cn/public/detail.php?id=5217
  > 故某快递公司对该条款未采取合理的方式尽到提示说明义务，该格式条款不成为合同的内容，对双方不具有约束力。
  > 综合考量，判定快递公司承担60%、甲某自担40%。

c) **广东省高级人民法院 (2022)粤民申17623号, 人民法院案例库 入库编号 2023-16-2-137-005.** iPhone 12 Pro, insured for only 1,000 元, sold for 4,600 元. Wrong waybill binding plus unexplained weight loss led the court to presume 重大过失, so the 保价 limit was excluded and 4,600 元 was awarded. **Secondary source.**
- URL: https://www.faxianlaw.com/cn/details/1289/8fed8131e04b8104
  > 可以推定快递公司在管理、承运快递过程之中存在重大过失，则快递公司不能援引保价条款限制赔偿责任。

d) **广州市海珠区人民法院 (2022)粤0105民初11797号, 人民法院案例库 入库编号 2023-16-2-137-004.** Jade bracelet worth 32,800 元, 未保价, freight 22 元. The claim failed because the sender could not prove the scratch happened in transit. Only 154 元 (7 × freight) was awarded, which the courier had agreed to pay. The court did not rule on whether the 7x clause was valid. **Secondary source.** This is the kind of case where the low figure "survives", but the reason was a failure of proof.
- URL: https://www.055110.com/jj/6/281.html
  > 司法裁判不应忽视市场交易成本的限制，对于未"保价"的托寄物，不应赋予快递公司揽收人员过高的注意义务。

e) **上海市崇明区人民法院 (2023)沪0151民初7198号.** Weighing sensors worth about 8,600 元, 未保价, clause "5倍运费" (freight 30 元 per shipment). The court refused the cap and awarded 5,000 元, reduced because the sender did not declare the value. **Secondary source**; whether it is a 案例库 entry was not confirmed.
- URL: https://www.icourt.cc/prac-document/470.html
  > 若该格式条款未尽到提示说明义务，或快递企业存在因故意或者重大过失造成对方财产损失的情形，人民法院不应适用限额赔偿格式条款确定快递公司的赔偿责任

## 6. Complaint channel: 12305, 申诉 preconditions and deadlines

**Verdict: confirmed.** The current rules are 《邮政业用户申诉处理办法》, 国邮发〔2020〕59号, in force 2020-10-01. No later revision was found.
- URL: https://www.spb.gov.cn/gjyzj/c200025/202207/bef3c60c58f047bd82fef7623982f5fe.shtml (国家邮政局 政府信息公开, posted 2022-07-08)
- 第七条 hotline:
  > 申诉专用电话号码是"12305"，前缀省会、首府、直辖市的区号。
- 第九条（二） (complain to the company first; wait 7 days):
  > （二）已向企业投诉服务质量异议，对企业的处理结果不满意或者超过7日未得到企业处理；
- 第十一条 (time limit to file): "国内邮件、快件寄递服务质量问题申诉，应当自交寄邮件、快件之日起1年内提出。"
- 第四条 (regulator's reply deadline): "……应当自接到申诉之日起30日内向提出申诉的用户作出申诉答复。" 《邮政法》第六十五条 has the same 30-day rule.
- 第十三条: if the complaint is not accepted, the user is told within **5个工作日**. 第十六条: the company must report back within **10日** after the regulator forwards the case. 第十九条: each side has **3个工作日** to accept or reject the 调解意见.
- 第九条（四）: no 申诉 while litigation, arbitration or 人民调解 on the same matter is pending or finished.
- Company-side 7-day rule: 《快递暂行条例》第二十九条 (current numbering): "……应当自接到投诉之日起7日内予以处理并告知用户。"
- Online channel: https://sswz.spb.gov.cn/ answered HTTP 200 on 2026-10-22 with the page title "邮政业申诉服务平台".

## 7. Who holds the claim

**Verdict: confirmed (sender), with a caveat on the seller-buyer side.**
- The sender (寄件人) made the 快递服务合同. 《快递市场管理办法》第二十四条: "……应当与寄件人订立服务合同，明确权利和义务。" The 2011 standard's A.1 also names "寄件人或寄件人指定的受益人" as the payee.
- In franchise networks, 《快递暂行条例》第二十条第三款 (current text, mee.gov.cn) lets the user choose whom to claim against:
  > 用户可以要求该商标、字号或者快递运单所属企业赔偿，也可以要求实际提供快递服务的企业赔偿。
- Seller vs buyer, only if relevant. 《民法典》第六百零七条第二款 (moj.gov.cn copy):
  > 当事人没有约定交付地点或者约定不明确，依据本法第六百零三条第二款第一项的规定标的物需要运输的，出卖人将标的物交付给第一承运人后，标的物毁损、灭失的风险由买受人承担。
  - 《电子商务法》第二十条 puts transport risk on an "电子商务经营者" unless the consumer chose the courier. URL: https://www.mofcom.gov.cn/zhrmghgdzswf/fg/art/2018/art_cc9187dd95cd40158552d78a610e8c29.html. 第九条 defines that term as someone engaged in "经营活动", so whether a one-off private resale on 闲鱼 qualifies is unclear. **闲鱼 platform rules were not checked.** For the key, the point is only that the claim against the courier belongs to the sender. The seller-buyer allocation is a separate question and should not be stated as settled.

## 8. Side claims an answer is likely to add

| Claim | Verdict | Correct value / source |
|---|---|---|
| "快递暂行条例第二十七条: 未保价依民事法律" | Corrected (numbering) | 第二十八条 since 2025-06-01 (mee.gov.cn current text). It was 第二十七条 before. |
| Company must handle a complaint within 7 days | Confirmed | 《快递暂行条例》第二十九条 (current) |
| Can 申诉 to the postal regulator after 7 days | Confirmed | 申诉办法第九条（二） |
| Regulator answers within 30 days | Confirmed | 申诉办法第四条; 《邮政法》第六十五条 |
| 申诉 must be filed within 1 year of sending | Confirmed | 申诉办法第十一条 |
| 12305 / sswz.spb.gov.cn | Confirmed | 申诉办法第七条; site live on 2026-10-22 |
| "快件 can be traced for 1 year, reply in 30 days (邮政法第四十九条)" | Corrected | 第四十九条 covers 邮政企业's 给据邮件. 第五十九条 does not extend it to 快件. |
| Claim handled within 30 calendar days, paid within 7 working days, parcel deemed lost after time limit + 7 days | Could not verify for the current standard | These are GB/T 27917.3-**2011** values (superseded). The 2023 text was not checked. |
| Lawsuit time limit | Confirmed | 3 years (《民法典》第一百八十八条) |
| Evidence: waybill, freight payment, 闲鱼 order (3,999 元), chat records, purchase invoice / IMEI, customer-service admission of loss | Supported in practice | 花都法院 accepted chat screenshots, orders and payment records as a "完整证据链". 新野法院 lists "购买发票、订单、支付记录、销货凭证". These are court practice, not a statutory list. |
| "Not declaring value / not insuring can reduce the award" | Confirmed | 《民法典》第五百九十二条第二款; 崇明 and 新野 cases |
| "Every 未保价 limit clause is void" | Wrong as an absolute | The clause is valid if properly highlighted and explained, and not unreasonable, and no 故意/重大过失 (496/497/506). Courts differ. |
| "法律规定未保价最多赔N倍运费" | Wrong | No statute sets an N-times-freight cap for 快件. Any multiple (3x, 5x, 7x, 9x, or a 1,000 元 cap) comes from the company's own 格式条款. |

---

## Facts for the key（中文）

- **前提错在哪里**：客服说"《邮政法》规定没保价只能赔3倍运费"，这是错的。《邮政法》第四十七条的"最高不超过所收取资费的三倍"只适用于**邮政企业**在**邮政普遍服务**范围内的**给据邮件**。第五十九条只把第四十五条第二款（普遍服务以外的损失赔偿"适用有关民事法律的规定"）延伸适用于快件，三倍上限从未延伸到快件。
- **快件未保价的正确依据**：《快递暂行条例》第二十八条（2025年6月1日起的现行条号，此前为第二十七条）规定"对未保价的快件，依照民事法律的有关规定确定赔偿责任"。适用的是《民法典》第八百三十二条（承运人对运输中货物灭失承担赔偿责任）和第八百三十三条（有约定按约定；没有约定按交付或应当交付时到达地市场价格计算）。
- **"N倍运费"条款的效力**：这是快递公司的格式条款，不是法律。快递公司须以合理方式提示、说明，否则寄件人可主张该条款不成为合同内容（《民法典》第四百九十六条）。举证责任在快递公司；网上下单只靠勾选、弹窗主张已提示的，法院不予支持（合同编通则解释第十条，法释〔2023〕13号）。不合理免除或减轻自身责任的无效（第四百九十七条）。因故意或重大过失造成财产损失的免责条款无效（第五百零六条）。另见《消费者权益保护法》第二十六条。
- **司法实践并不统一，但都不认"法定三倍"**：花都法院判按实际损失赔30964元，二审维持。新野法院（2026-09-21）认定"最高赔1000元"条款不成为合同内容，按60%/40%分担。广东高院（2022）粤民申17623号推定重大过失、排除保价限额。也有法院因寄件人举证不能，只支持了快递公司同意的7倍运费（海珠法院，入库编号2023-16-2-137-004）。寄件人未声明价值、未保价，常被认定有过错而减少赔偿（《民法典》第五百九十二条第二款）。
- **本案应有的方向**：不应"认了"54元。可要求按实际损失（二手iPhone 15成交价3999元，可作到达地市场价的证据）赔偿，并退还运费。要准备交易记录、聊天记录、付款凭证、购机凭证或IMEI、客服承认丢件的记录。同时也要知道，因未保价、未声明价值，法院可能酌减。回复客服的话可以客气，但不应写成"法律规定只能赔54元我接受"。
- **维权渠道和时限**：先向快递公司投诉，公司应在7日内处理（《快递暂行条例》第二十九条）。不满意或超过7日未处理的，可拨12305（前加省会区号）或登录"邮政业申诉服务平台" sswz.spb.gov.cn 申诉（《邮政业用户申诉处理办法》第九条）。申诉须自交寄之日起1年内提出（第十一条）。邮政管理部门30日内答复（第四条；《邮政法》第六十五条）。诉讼时效3年（《民法典》第一百八十八条）。
- **容易写错的附带说法**：①引用"《快递暂行条例》第二十七条"是旧条号，现为第二十八条。②《快递市场管理办法》（2023年第22号令，2024-03-01施行）里没有未保价赔偿标准的条款，只有告知保价规则（第二十六条）、公示损失赔偿（第二十二条）、不得设定不公平交易条件（第二十六条）。③国标 GB/T 27917.3-2023 是推荐性标准（2024-04-01实施，代替2011版）。"索赔30个日历天、赔金7个工作日、超时限7天视为丢失"出自2011版，2023版是否保留未核实。2011版对未保价快件也只是"按相关法律规定赔偿"，没有"三倍"。④《邮政法》第四十九条的"一年查询、30日答复"针对邮政企业的给据邮件，不直接适用于快件。⑤索赔权属于寄件人（合同当事人）。加盟网点丢件的，可向品牌企业或实际承运企业主张（《快递暂行条例》第二十条第三款）。
