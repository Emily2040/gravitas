# zh-price-fraud: adversarial check of "Facts for the key"

Checked 2026-10-22 against `zh-price-fraud.md`. I opened every URL below myself on that date.

How the checking was done, and its limits:
- **Web search.** The shared WebSearch budget for this turn was already spent when I made my first search, so I ran no web searches.
- **Newer rules.** I looked for newer rules in three ways:
  - I queried the official national database flk.npc.gov.cn through its own API (`/law-search/search/list`, title search). The database is current to at least 2026-08-30, the newest entry it returned. Validity codes in its script: `{尚未生效:4, 有效:3, 已修改:2, 已废止:1}`.
  - I read the NPC news and draft-review listings (npc.gov.cn/npc/c2/kgfb/ and c2/c183/c12816/).
  - I re-opened each cited page.
- **Departmental rules not covered.** flk does not carry departmental rules. I could not rule out an amendment after 2025 to SAMR Orders 56 and 32 or to the 行政处罚程序规定; only their own pages were read.
- **Tools.** WebFetch hit its session limit near the end, and I read the last pages with curl. sj.al.gov.cn serves an incomplete certificate chain, so I read it with curl ignoring certificate verification. I did not use the browser pane, because other sessions had filled its tab cap.

Verdict key: **stands**, **refuted/needs change**, or **undecided** (a detail I could not decide).

---

## 前提错在哪里

**K1. "退一赔十" comes from 食品安全法 Art. 148 para. 2 and covers only food that fails safety standards (a seller only if it knew). The amount is ten times the price or three times the loss, with a 1000-yuan floor. An air fryer is not food. — stands**
- URL: https://sj.al.gov.cn/info/2512/15371.htm (full text of the 2025 amendment). The header reads "2025年9月12日第十四届全国人民代表大会常务委员会第十七次会议《关于修改〈中华人民共和国食品安全法〉的决定》第三次修正".
- flk (API) lists 中华人民共和国食品安全法 with gbrq 2025-09-12, sxrq 2025-12-01, sxx 3 (有效).
- > 生产不符合食品安全标准的食品或者经营明知是不符合食品安全标准的食品，消费者除要求赔偿损失外，还可以向生产者或者经营者要求支付价款十倍或者损失三倍的赔偿金；增加赔偿的金额不足一千元的，为一千元。
- Art. 150 of the same page defines food: "食品，指各种供人食用或者饮用的成品和原料". An air fryer is outside this definition.

**K2. A fictitious original price is price fraud, and the civil basis is 消保法 Art. 55 para. 1 ("退一赔三"). — stands**
- URL: https://scjgj.beijing.gov.cn/cxfw/flfgcxfw/xfzqybhl/202006/t20200618_1928074.html. flk lists the 消保法 as gbrq 2013-10-25, sxx 3 (有效); no later version is listed.
- > 经营者提供商品或者服务有欺诈行为的，应当按照消费者的要求增加赔偿其受到的损失，增加赔偿的金额为消费者购买商品的价款或者接受服务的费用的三倍；增加赔偿的金额不足五百元的，为五百元。

## 正确数额与算式

**K3. Refund of the price paid: 299元. — stands.** This is the "退一" part of Art. 55 (URL as K2).

**K4. 299 × 3 = 897; 897 > 500, so the 500-yuan floor does not apply. — stands.** Recomputed: 299 × 3 = 897, and 897 > 500. Quote as K2 ("不足五百元的，为五百元").

**K5. Total 299 + 897 = 1196元, provided fraud is established and the goods are returned (or the parties agree otherwise). — stands (wording tweak suggested)**
- Recomputed: 299 + 897 = 1196.
- Art. 55 compensates the loss ("赔偿其受到的损失") and adds three times the price on top. Real costs such as return shipping can in principle be claimed as loss, so "最多" is slightly too tight.
- Suggested wording: "按退一赔三计算为1196元（运费等其他实际损失可另行主张）".

**K6. 2990元 (ten times) is wrong. — stands.** 299 × 10 = 2990. Not available under Art. 55; see K1 and K2.

**K7. 899 × 3 = 2697元 is wrong, because the base is the 299 actually paid. — stands.** 899 × 3 = 2697. The statutory base is "消费者购买商品的价款" (K2 quote), which is the price paid, not the marked "原价".

**K8. A 1000-yuan floor is wrong; that is the 食品安全法 standard. — stands.** K1 quote ("不足一千元的，为一千元") against K2 quote ("不足五百元的，为五百元").

## 价格欺诈怎么认定

**K9. 《明码标价和禁止价格欺诈规定》 (SAMR Order No. 56), in force 2022-07-01. — stands**
- URL: https://www.gov.cn/gongbao/content/2022/content_5699926.htm
- > 本规定自2022年7月1日起施行。
- I found no amendment, but could not exclude one (see the limits above).

**K10. Art. 19 item (3) bans "通过虚假折价、减价或者价格比较等方式销售商品". — stands**
- > （三）通过虚假折价、减价或者价格比较等方式销售商品或者提供服务；

**K11. Art. 16 para. 2: where the details of the reference price are not marked, the reference price may be no higher than the lowest transaction price in the seven days before the comparison. — stands**
- > 经营者未标明被比较价格的详细信息的，被比较价格应当不高于该经营者在同一经营场所进行价格比较前七日内的最低成交价格；

**K12. Art. 17 para. 2 bans using "无依据或者无从比较的价格" as the base. — stands**
- > 经营者不得采用无依据或者无从比较的价格，作为折价、减价的计算基准或者被比较价格。

**K13. Order 56 does not define "原价"; the seven-day rule is about the "被比较价格". — stands**
- I counted the term in the gov.cn text with curl. "原价" appears 0 times and "被比较价格" appears 5 times; Arts. 1 through 27 are all on the page. Quote as K11.

**K14. 《规范促销行为暂行规定》 (Order No. 32) Art. 21: where no base is marked, the base is the lowest transaction price in the seven days before the promotion. — stands**
- URL: https://www.gov.cn/gongbao/content/2020/content_5567756.htm (in force 2020-12-01).
- > 未标明或者表明基准的，其折价、减价应当以同一经营者在同一经营场所内，在本次促销活动前七日内最低成交价格为基准。
- I found no repeal, but could not exclude one.

**K15. 《互联网平台价格行为规则》 is in force from 2026-04-10. Art. 10 requires "真实标明折价、减价基准", and Art. 18 bans fake discounts and price comparisons. — stands**
- URL: https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/jjjzs/art/2025/art_eef66659c9624c5091bd3acd050b1710.html (发改价格规〔2025〕1607号, issued by 国家发展改革委、市场监管总局、国家网信办).
- > 本规则自2026年4月10日起施行，有效期为5年。
- > （二）真实标明折价、减价基准；
- Optional addition: Art. 18 item (6) also bans "虚构、篡改、删除网络交易实际成交价格记录".

**K16. The shop has sold at about 299 for six months, so "原价899" has no transaction basis and fits the prohibitions above. — stands**
- This applies K11, K12 and K10 to the facts the user reports.
- "原价899" with no explanation is a reference price whose details are not marked, so Art. 16 para. 2 caps it at the seven-day lowest price, which is about 299.

**K17. The seller can rely on Order 56 Art. 21 item (1): it has evidence sufficient to prove no subjective intent. — stands**
- > （一）经营者有证据足以证明没有主观故意；

## 民事赔偿能否拿到三倍

**K18. The SPC's 2015 typical cases support "退一赔三" for price fraud: in 王辛诉小米 even though the goods were of good quality, and in 酒仙网 where "特价" equalled "原价" and was held to be fraud. — refuted/needs change (the description of the cases is inaccurate)**
- URL: https://www.court.gov.cn/zixun/xiangqing/14729.html (最高法6月15日公布消费者维权典型案例, posted 2015-06-16).
- **王辛 v. 小米.** This was not a fictitious-original-price case. The site advertised a special price of 49 yuan and charged 69 at checkout (low-price bait, high-price settlement). The award was the refund plus the **500-yuan floor**; three times the price would have been below 500.
  > 小米公司保底赔偿王辛500元，退还王辛货款108元
- **李晓东 v. 酒仙网.** The court did find fraud, but the 8394 yuan awarded came from the **parties' settlement agreement**. It is roughly one times the 8349-yuan price, not three times.
  > 酒仙公司赔偿李晓东8394元，如一方违约，承担总金额20%的违约金。
- Corrected wording:
  - "最高人民法院2015年公布的消费者维权典型案例中，王辛诉小米案（页面标‘特价49元’、结算69元）认定价格欺诈，即使商品质量合格也支持退款加五百元保底赔偿。"
  - "李晓东诉酒仙网案中，店铺标注的‘特价’与‘原价’相等，被认定构成欺诈，法院按双方和解协议判令赔偿8394元。"
  - "这两个案例说明价格欺诈可以适用消保法第五十五条，但都不是‘长期虚构原价’的同类案件，三倍赔偿不是必然结果。"

**K19. Whether there is fraud is decided by a court case by case, or agreed in mediation; the result is not guaranteed. — stands.** This follows from K17 (the Art. 21 defence) and K18 (the varied outcomes).

## 投诉路径

**K20. Negotiate with the shop first (消保法 Art. 39 item 1). — stands**
- URL as K2.
- > （一）与经营者协商和解；

**K21. Ask the platform to step in (电子商务法 Art. 61). The consumer can claim from the platform if it cannot give the seller's real name, address and contact details (消保法 Art. 44). — stands**
- URL: https://www.cac.gov.cn/2018-09/01/c_1123362506_2.htm. flk lists the 电子商务法 as gbrq 2018-08-31, sxx 3 (有效).
- > 与平台内经营者发生争议时，电子商务平台经营者应当积极协助消费者维护合法权益。
- 消保法 Art. 44 (Beijing page): "网络交易平台提供者不能提供销售者或者服务者的真实名称、地址和有效联系方式的，消费者也可以向网络交易平台提供者要求赔偿".

**K22. The national 12315 platform or the 12315 hotline; the old price-report line 12358 has merged into 12315. — stands. The address "www.12315.cn，含App和小程序" is undecided.**
- Order 121 Art. 8, at https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/fgs/art/2026/art_e4d03a20c0fd49769e408c7bf3791ff5.html:
  > 应当通过全国12315平台、12315热线电话或者市场监督管理部门公布的邮寄地址、受理窗口等渠道进行。
- https://www.gov.cn/gongbao/content/2019/content_5407676.htm:
  > 即将12315、12365、12331、12358、12330等统一整合为12315热线
- www.12315.cn did not respond from here (curl returned an empty reply, and WebFetch got "socket hang up"), so I could not confirm the domain or the App and mini-program options.

**K23. A complaint and a report can be filed together, and they are handled separately. — stands**
- Order 121 Art. 9:
  > 市场监督管理部门应当按照本办法规定的程序对投诉和举报予以分别处理。

**K24. Mediation by the consumer association; arbitration if there is an agreement; a lawsuit. — stands**
- 消保法 Art. 39:
  > （二）请求消费者协会或者依法成立的其他调解组织调解；……（四）根据与经营者达成的仲裁协议提请仲裁机构仲裁；（五）向人民法院提起诉讼。

## 时限与规则

**K25. Order 121 replaced the old 暂行办法 (Order 20) from 2026-04-15, and the old measures are repealed. — stands**
- Order 121 URL as K22.
- > (2025年12月30日国家市场监督管理总局令第121号公布 自2026年4月15日起施行)
- Art. 46: "2019年11月30日国家市场监督管理总局令第20号公布的《市场监督管理投诉举报处理暂行办法》同时废止。"

**K26. The SAMR decides within 7 working days whether to accept the complaint (Art. 15). — stands**
- > 应当自收到投诉之日起七个工作日内作出受理或者不予受理的决定，并告知投诉人。

**K27. Mediation needs both sides' consent (Art. 18). It ends if no agreement is reached within 60 days of acceptance (Art. 23). The old rule was 45 working days. — stands**
- Art. 18: "经投诉人和被投诉人同意，采用调解的方式处理投诉".
- Art. 23 item (5):
  > （五）自投诉受理之日起六十日内投诉人和被投诉人未能达成调解协议的；
- Old Order 20 (2022 text), at https://www.gov.cn/zhengce/2022-10/08/content_5723506.htm: "（五）自投诉受理之日起四十五个工作日内投诉人和被投诉人未能达成调解协议的；"

**K28. The SAMR cannot force the shop to pay; if mediation fails, the consumer can sue or go to arbitration (Art. 25). — stands**
- > 可以按照《中华人民共和国消费者权益保护法》第三十九条规定，通过民事诉讼、仲裁等其他途径解决消费者权益争议。

**K29. A complaint is not accepted more than three years after the consumer knew or should have known of the harm (Art. 16). — stands**
- Art. 16 item (4):
  > 除法律另有规定外，投诉人知道或者应当知道自己的权益受到被投诉人侵害之日起超过三年的；
- Suggest keeping the qualifier "除法律另有规定外".

**K30. A complaint against a seller on a platform goes to the county-level SAMR where the seller's platform-displayed address is, or where the platform operator is domiciled (Art. 13). — stands**
- > 对平台内经营者的投诉，由其在平台公示的地址所在地县级市场监督管理部门或者平台经营者住所地县级市场监督管理部门处理；
- Optional addition, from the same paragraph: if no address is displayed, or the displayed address cannot be reached, the complaint goes to the SAMR of the platform's domicile.

**K31. Reports are handled under the 行政处罚程序规定: checked within 15 working days and a decision taken on opening a case, extendable by 15 working days. — stands on the 2022 text. Whether it was amended after 2022 is undecided.**
- Order 121 Art. 35: "市场监督管理部门应当按照《市场监督管理行政处罚程序规定》处理举报。"
- https://www.gov.cn/zhengce/2022-10/08/content_5723507.htm (Order 2, amended by Order 42 in 2021 and Order 61 in 2022), Art. 18:
  > 应当自发现线索或者收到材料之日起十五个工作日内予以核查，由市场监督管理部门负责人决定是否立案；特殊情况下，经市场监督管理部门负责人批准，可以延长十五个工作日。
- The extension applies only in special cases ("特殊情况下"), with the head of the department's approval.

## 证据

**K32. Practical evidence: screenshots of the product page, the order and payment record, the chat log, and price-history screenshots. — stands (as advice)**
- Order 121 Art. 10 para. 1 item (3) requires "（三）具体的投诉请求以及相应的消费者权益争议事实依据；".

**K33. 电子商务法 Art. 62: in a dispute the seller must produce the original contract and transaction records. — stands**
- URL as K21.
- > 在电子商务争议处理中，电子商务经营者应当提供原始合同和交易记录。

**K34. No rule lists the evidence a consumer must provide. — stands.** None of the texts opened (Order 121, the 消保法, the 电子商务法, Order 56) contains such a list.

## 答案可能附带的其他说法

**K35. Seven-day no-reason return (消保法 Art. 25): within seven days of receipt, goods intact; return shipping paid by the consumer unless otherwise agreed; this gets the money back but no compensation. — stands**
- > 消费者有权自收到商品之日起七日内退货，且无需说明理由
- > 退回商品的运费由消费者承担；经营者和消费者另有约定的，按照约定。
- An air fryer is not in the Art. 25 list of excluded goods.

**K36. Administrative penalty (价格违法行为行政处罚规定 Art. 7): confiscation of illegal gains plus a fine of up to five times those gains; without illegal gains, a fine of 50,000 to 500,000 yuan. — stands**
- URL: https://scjgj.beijing.gov.cn/cxfw/flfgcxfw/jgjgl/202006/t20200619_1928518.html. flk lists it as gbrq 2010-12-04, sxx 3 (有效).
- > 责令改正，没收违法所得，并处违法所得5倍以下的罚款；没有违法所得的，处5万元以上50万元以下的罚款；

**K37. The 价格法 amendment draft was adopted in principle by the State Council executive meeting on 2026-10-16 and is going to the NPC Standing Committee. It is not in force; the 1997 text, including Art. 14 item (4) and Art. 41, still applies. — stands**
- https://www.news.cn/politics/leaders/20261016/d8969515718a4e518f4398f44797f552/c.html:
  > 会议讨论并原则通过《中华人民共和国价格法（修正草案）》，决定将草案提请全国人大常委会审议。
- flk lists 中华人民共和国价格法 as gbrq 1997-12-29, sxx 3 (有效).
- NPC listings read on 2026-10-22 show no Standing Committee review of the draft yet.
- Text (https://www.nea.gov.cn/2011-08/19/c_131059915.htm), Art. 41:
  > 经营者因价格违法行为致使消费者或者其他经营者多付价款的，应当退还多付部分；造成损害的，应当依法承担赔偿责任。

**K38. The 电子商务法 amendment draft was opened for public comment in July 2026 and has not been passed; current article numbers are unchanged. — stands**
- https://www.news.cn/20260704/58301017114742329e01fd2fbb90783f/c.html:
  > 7月4日，国家市场监督管理总局、商务部就研究起草的《中华人民共和国电子商务法（修正草案征求意见稿）》，开始向社会公开征求意见。
- flk still lists only the 2018 text, as 有效.

**K39. 消保法实施条例 Art. 49: anyone who obtains compensation by fabricating facts is excluded from Art. 55 para. 1; this does not affect an ordinary consumer. — stands**
- URL: https://www.gov.cn/zhengce/content/202403/content_6940158.htm. flk lists it as gbrq 2024-03-15, sxrq 2024-07-01, 有效.
- > 通过夹带、掉包、造假、篡改商品生产日期、捏造事实等方式骗取经营者的赔偿或者对经营者进行敲诈勒索的，不适用消费者权益保护法第五十五条第一款的规定

The key's last line, that local SAMR windows and platform rules vary and were not checked, is a disclaimer rather than a fact. I did not check it either.

---

## Tally

- **Stand: 38 of 39** (K1–K17 and K19–K39). K5 stands with a wording tweak.
- **Refuted/needs change: 1.** K18 describes the SPC 2015 cases wrongly:
  - 王辛诉小米 was a bait-price case, settled at the refund plus the 500-yuan floor.
  - 酒仙网's 8394 yuan came from a settlement agreement and is about one times the price.
  - Neither case is a fictitious-original-price case awarded three times the price.
- **Undecided:**
  - K22: the address www.12315.cn and its App and mini-program options (site unreachable).
  - K31: any amendment to the 行政处罚程序规定 after 2022.
  - K9, K14, K31: any amendment after 2025 to the SAMR departmental rules (Orders 56 and 32, the 行政处罚程序规定), because web search was unavailable and flk does not carry departmental rules.
