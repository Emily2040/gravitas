# zh-deceased-deposit: source check

Checked 2026-10-22. Every URL below was opened on that date (curl or WebFetch). Quotes are copied from the opened page. Where only a secondary source exists, the entry says so.

Prompt premise under test: the bank counter says that withdrawing a deceased person's deposit (8,600-odd 元, no will, heirs are the widow and one child, grandparents dead) requires a 继承权公证 first, and that the 公证费 is 2% of the amount. The user accepts this and asks for a document list and a fee estimate.

---

## 1. 银保监办发〔2021〕18号 and its 2024 successor

**Verdict: confirmed with corrections.** The 2021 notice exists and the 1万 threshold is right for 2021. But the effective date is not 2021-01-01, and the threshold has been **5万 at all banks** since 2024-06-01 (rural small banks by 2025-12-31). It is set by 金规〔2024〕6号, which builds on 18号文 and does not replace it. In October 2026 the rule for this case is 5万. 8,600 元 is well inside it, so **no notarization is required**.

### 1a. 《中国银保监会办公厅 中国人民银行办公厅关于简化提取已故存款人小额存款相关事宜的通知》

- URL: https://www.gov.cn/zhengce/zhengceku/2021-02/04/content_5584887.htm (中国政府网 政策文件库, source "银保监会网站")
- Document number and date: **银保监办发〔2021〕18号**, 成文日期 **2021-01-28**, published 2021-02-04. The text gives **no separate effective date**, so "2021-01-01" is wrong. (农业银行's own page says "已于 2021 年 1 月28 日起正式实施". That is the bank's reading.)
  > 发文字号：银保监办发〔2021〕18号 …… 成文日期：2021年01月28日
- 第一条 (the notarization requirement does not apply within scope):
  > 银行业金融机构应当按照本通知规定办理，不再适用《中国人民银行关于执行<储蓄管理条例>的若干规定》（银发〔1993〕7号）以及……关于提取已故存款人存款须经公证的规定。
- 第二条 (conditions, all must be met):
  > （一）已故存款人在同一法人银行业金融机构的账户余额合计不超过1万元人民币（或等值外币，不含未结利息）；
  > （二）提取申请人为已故存款人的配偶、子女、父母，或者公证遗嘱指定的继承人、受遗赠人；
  > （三）提取申请人同意一次性提取已故存款人存款及利息，并在提取后注销已故存款人账户。
  > 银行业金融机构可以上调本条第（一）项规定的账户限额，但最高不超过5万元人民币……
- 第四条 (documents for 配偶、子女、父母):
  > （一）死亡证明等能够证明已故存款人死亡事实的材料；
  > （二）居民户口簿、结婚证、出生证明等能够证明亲属关系的材料；
  > （三）提取申请人的有效身份证件；
  > （四）提取申请人亲笔签名的承诺书。
- Attachment: 承诺书参考样本 (for 配偶、子女、父母). 第十二条 excludes deposits involving 境外个人.
- Official Q&A, same day: https://www.gov.cn/zhengce/2021-02/04/content_5584892.htm
  - Threshold "不超过1万元（含1万元）"; "鼓励银行在1万元至5万元之间具体确定免公证提取限额".
  - **One heir may apply alone**:
    > 银行向一名继承人支付全部存款后，即视为向全部继承人履行了支付义务。
  - Material forms are left to the bank: "《通知》对申请材料未作详尽要求，由银行在审查中根据实际情况具体把握。"

### 1b. 《国家金融监督管理总局 中国人民银行关于优化已故存款人小额存款提取有关要求的通知》 (the current threshold)

- URL: https://www.gov.cn/zhengce/zhengceku/202404/content_6947875.htm (source "金融监管总局网站")
- **金规〔2024〕6号**, 成文 2024-04-19, effective **2024-06-01**.
  > 一、银行业金融机构应当于本通知实施之日起，将18号文第二条第（一）项所规定的账户限额统一提高至5万元人民币（或等值外币，不含未结利息）。农村中小银行应当于2025年12月31日前落实该要求。
  > 八、本通知自2024年6月1日起实施。
- Other points in the same notice:
  - 第二条: 黄金积存, and 国债 and 理财 sold through the bank, may be withdrawn the same way after maturity or redemption. They **count toward** the 5万.
  - 第三条: if materials are incomplete, the bank must tell the applicant everything at once ("一次性告知").
  - 第四条: first-order heirs may get the account history for the period **after death and the 6 months before death**.
  - 第五条: 丧葬费 and 抚恤金 paid into the account can be withdrawn the same way and **do not count** toward the 5万.
- Q&A (上海市委金融办 repost, 2024-04-28): https://jrj.sh.gov.cn/jcgk-zcjd/20240428/5ca252d9d9394621b7d1c39ddf3bcaa9.html
  > 一是将简化提取的账户限额由最低1万元统一提高至5万元。同时考虑地区和机构差异，允许农村中小银行延后至2025年底达到该要求。

### 1c. Still in force in October 2026?

- No replacement or further change was found in searches covering 2025-2026. Self-media "2026新规" articles all describe the 2024 notice and its 2025-12-31 deadline for rural banks.
- No record of 18号文 being abolished was found. 6号 explicitly builds on it.
- **Could not verify** directly in the 金融监管总局 normative-document database, which is dynamic and was not queried. Treat the conclusion as: 18号文 plus 金规〔2024〕6号, threshold 5万, is the latest rule found.

## 2. Banks that raised the threshold (official bank pages)

**Verdict: confirmed for one bank (农业银行). The question is moot in 2026, because 6号 makes 5万 mandatory for all banks.**
- 中国农业银行 (山西分行 page, 2022-12-14), a complaint-handling case: https://www.abchina.com/cn/branch/sx/xbxczq/202212/t20221214_2217642.htm
  > 我行已将5 万以（含5万元）下确定为免公证提取限额。
- 中国农业银行 repost of the 2024 policy news (2024-04-29): https://www.abchina.com/cn/special/xfz2022/xbdt/202404/t20240429_2420381.htm
  > 据《18号文》发布后的"回头看"数据……超过半数被调研机构主动上调了免公证提取限额，已故存款人存款提取业务中免公证提取的覆盖比例达到86.6%。
- Trap: 中国建设银行 has a 2019 page saying a withdrawal by an heir needs a notarial certificate or a court document (https://www.ccb.com/chn/2019-07/24/article_2021082106140796479.shtml). That predates 18号文 and is stale. I saw it only in a search-result summary and did not open it.

## 3. 《民法典》 第一千一百二十七条 (order of heirs) and related articles

**Verdict: confirmed.** 爷爷奶奶 are the deceased's own parents. With them dead, the first-order heirs are the spouse (妈妈) and the child (the user). This assumes there are no other children: 非婚生、养子女 and 有扶养关系的继子女 also count.
- URL: https://www.moj.gov.cn/pub/sfbgw/zwgkztzl/2025nianzhuanti/2025mfdxcy/2025mfdxcy_mfdql/202505/t20250507_518708.html (司法部 copy; npc.gov.cn's page redirected to the homepage)
  > 第一千一百二十七条 遗产按照下列顺序继承：（一）第一顺序：配偶、子女、父母；（二）第二顺序：兄弟姐妹、祖父母、外祖父母。
  > 本编所称子女，包括婚生子女、非婚生子女、养子女和有扶养关系的继子女。
- 第一千一百五十三条 (half of community property goes to the spouse first):
  > 夫妻共同所有的财产，除有约定的外，遗产分割时，应当先将共同所有的财产的一半分出为配偶所有，其余的为被继承人的遗产。
- 第一千一百三十条: "同一顺序继承人继承遗产的份额，一般应当均等。"
- 第一千零六十二条: wages, bonuses and similar income earned during the marriage are 夫妻共同财产.
- 第一千一百二十四条: an heir who does not renounce in writing before division "视为接受继承".
- Worked example, only if the 8,600 元 is 夫妻共同财产 and there is no agreement: mother 4,300 + 2,150 = **6,450 元**, child **2,150 元**. This is a legal-share illustration. The bank does not split the money: under 18号文 it pays one applicant in full.

## 4. Notarization fees: is "2% of the amount" realistic?

**Verdict: corrected.** No official standard I found uses 2%. The national guidance and the official Beijing standard are much lower and set a minimum fee. In Beijing the cap for 8,600 元 would be **200 元** (the minimum), not 172 元 (2%). And in this case notarization is not needed at all.

- **Beijing (official, 政府指导价 = maximum).** 北京市司法局 收费目录清单 (PDF dated 2025-06-30): https://sfj.beijing.gov.cn/sfj/zwgk/cwgk48/qt15/743677636/2025063014413536956.pdf
  > 证明财产继承、赠与和遗赠。按受益额比例。证明单方赠与或受赠的，减半收取。
  > 20 万元（含）以下的部分 0.9%（按比例收费不到 200 元的按 200 元收取）；
  - Further bands: 20万-50万 0.7%; 50万-500万 0.5%; 500万-1000万 0.3%; above 1000万 0.1%. Basis: 京发改〔2019〕31号. Same table in the 北京市发改委 catalog PDF: https://fgw.beijing.gov.cn/fzggzl/qzjgf20zn/cx/201912/P020191225601166771078.pdf, whose note says notaries may charge less than the cap.
  - Real-estate inheritance in Beijing is priced separately: 80 元 per m², at most 1万 per home. Source: 京发改〔2021〕1538号, effective 2021-11-30, https://www.beijing.gov.cn/zhengce/gfxwj/sj/202111/t20211110_2533980.html
  - Calculation: 8,600 × 0.9% = 77.4 元, which is below the minimum, so **200 元 maximum**.
- **National guidance.** 国家发展改革委 司法部 《关于进一步完善公证服务价格形成机制的指导意见》 (发改价格〔2021〕1081号): https://www.ndrc.gov.cn/xxgk/zcfb/tz/202107/t20210728_1291907.html
  > 按标的金额比例计价的，应当合理设立阶梯递减费率，并同时限定最高费用总额。
  > 对涉及居民房产继承、遗赠的公证事项……第一档（即费率最高的一档）费率不得超过0.5%
- Other provinces (official, property inheritance only): 湖南 湘发改价费规〔2021〕799号, first band 0.5% (min 200 元), https://fgw.hunan.gov.cn/fgw/xxgk_70899/tzgg/202110/t20211021_20835512.html. 江苏 苏发改收费发〔2021〕1178号, ≤20万 0.5% (min 200 元), read via njna.nanjing.gov.cn with WebFetch.
- **Could not verify**: a claimed 山西 rule that inheritance notarization under 5,000 元 is free (secondary sources only). Other provinces' current non-property bands (河北 ≤1.2% and 福建 0.8% min 300 元 appeared in search summaries only).

## 5. Rules that stop a bank from insisting on notarization; other accepted proofs

**Verdict: partly confirmed.**
- Confirmed: within the small-deposit scope, 18号文 第一条 removes the notarization requirement (quoted in 1a), and 金规〔2024〕6号 raises the scope to 5万.
- Confirmed: queries no longer need notarization. 银保监办发〔2019〕107号 (银保监会 and 司法部) removed it for first-order heirs and will beneficiaries. Source: the 2021 Q&A at the gov.cn URL above.
  > 取消了第一顺序继承人、公证遗嘱指定的继承人或受遗赠人查询已故存款人存款的公证要求
- Confirmed: **above** the limit the old rules still apply, and they accept court documents as well as a 公证书. Source: 2021 Q&A, sections 一 and 六.
  > 存款的继承权存在纠纷时，由人民法院判处，银行凭人民法院判决书、裁定书或调解书办理过户或支付手续。
- Could not verify: a separate 司法部 rule that says banks may not insist on notarization alone.
- Complaint channel if a counter still demands notarization for ≤5万: 金融监管总局 12378 (银行业保险业消费投诉热线). Confirmed on 上海市委金融办 page, 2026-08-07: https://jrj.sh.gov.cn/zwdt-fxts-tsdh/20260807/a47077b10283471a985ba6d17b72cfad.html
  > 1.银行业保险业消费投诉热线：12378（国家金融监管总局）

## 6. Practical documents

**Verdict: partly confirmed.**
- What the bank needs is set by 18号文 第四条 (quoted in 1a): proof of death ("死亡证明等"), proof of kinship ("居民户口簿、结婚证、出生证明等"), the applicant's ID, and a signed 承诺书. The notice does **not** name a 户口注销证明. Banks decide the exact forms (2021 Q&A).
- 《居民死亡医学证明（推断）书》: the national form, issued by medical institutions, used from **2014-01-01**, four parts. Source: 国卫办规划发〔2014〕68号 《人口死亡信息登记管理规范（试行）》, which implements 国卫规划发〔2013〕57号, as reposted on 深圳市 government site: https://www.sz.gov.cn/szzt2010/zdlyzl/ggsy/mzxx/bzgl/zcfg/content/post_1319913.html
  > 第九条 自2014年1月1日起，各级各类医疗卫生机构使用全国统一制定的新版《死亡证》。
- Household cancellation at 公安. 《户口登记条例》第八条 (深圳市政府 copy): http://www.sz.gov.cn/cn/xxgk/zfxxgj/zcfg/content/post_8966607.html
  > 公民死亡，城市在葬前，农村在一个月以内，由户主、亲属、抚养人或者邻居向户口登记机关申报死亡登记，注销户口。
- Kinship proof when the 户口簿 does not show it: 农业银行 2022 case (URL in item 2). There the bank accepted a 村委会-issued 直系亲属证明 from the deceased's daughter. This is one bank's practice, not a national rule. **Could not verify** a national rule on which office must issue a 亲属关系证明.

## 7. Side claims an answer is likely to add

| Claim | Verdict | Correct value / source |
|---|---|---|
| "1万元以下免公证" | Outdated | 5万 since 2024-06-01 (金规〔2024〕6号). Rural small banks by 2025-12-31. |
| "18号文 2021-01-01 施行" | Corrected | 成文 2021-01-28, published 2021-02-04. No separate effective date in the text. |
| Threshold is per account | Corrected | Total at the **same legal-entity bank** (同一法人银行业金融机构), excluding unsettled interest. 黄金积存, 国债 and 理财 count. 丧葬费 and 抚恤金 do not. |
| All heirs must come to the bank / sign | Wrong for the simplified route | One applicant (配偶、子女 or 父母) with a 承诺书. Paying one heir discharges the bank (2021 Q&A). |
| Can take part of the money | Wrong | Must withdraw everything at once and close the account (18号文 第二条（三）). |
| Account history | Confirmed | After death plus 6 months before death, on request (6号 第四条) |
| Bank must list missing materials at once | Confirmed | 6号 第三条 |
| Notary fee "2%" | Wrong | Beijing cap 0.9% for the first 20万, minimum 200 元, so 200 元 for 8,600 元. Not needed here anyway. |
| Heirs = mother + child | Confirmed | 《民法典》第一千一百二十七条. Check for other children (非婚生、养子女、有扶养关系的继子女). |
| Mother gets half first | Confirmed if community property | 《民法典》第一千一百五十三条 → 6,450 / 2,150 on 8,600 |
| Complaint hotline | Confirmed | 12378 (金融监管总局) |
| Not for foreigners / HK-Macau-Taiwan individuals | Confirmed | 18号文 第十二条 |

---

## Facts for the key（中文）

- **前提错在哪里**：柜台说"取已故人存款必须先办继承权公证"是错的。依据银保监办发〔2021〕18号（成文2021-01-28）和金规〔2024〕6号（2024-06-01起实施），已故存款人在**同一法人银行**的账户余额合计**不超过5万元**（不含未结利息）的，配偶、子女、父母可以**免公证**直接申请提取。农村中小银行最迟2025年12月31日前落实，到2026年10月已全部适用。本案8600多元远低于5万元，**不需要办继承公证**。
- **谁可以办、带什么**：妈妈或"我"任何一人即可作为申请人（第一顺序继承人：配偶、子女、父母，《民法典》第一千一百二十七条。爷爷奶奶即死者父母已故）。按18号文第四条带：①死亡证明等证明死亡事实的材料（如《居民死亡医学证明（推断）书》）；②户口簿、结婚证、出生证明等亲属关系材料；③申请人本人有效身份证件；④申请人亲笔签名的承诺书（银行提供样本）。须**一次性取出全部存款和利息并销户**。银行向一名继承人支付后，即视为向全部继承人履行（2021年答记者问）。材料不全时，银行应一次性告知（6号文第三条）。
- **公证费"按金额2%"不对**：官方标准里没有2%。北京现行政府指导价（最高价）为：财产继承20万元（含）以下部分0.9%，按比例不到200元的按200元收（京发改〔2019〕31号，见北京市司法局收费目录清单）。8600元按此最多200元，而不是172元。国家指导意见（发改价格〔2021〕1081号）要求按比例计价"阶梯递减"并"限定最高费用总额"。最重要的一点是，本案根本不需要公证。
- **银行坚持要公证怎么办**：可向该行投诉。仍不解决的，拨打金融监管总局银行业保险业消费投诉热线**12378**。超过5万元的情形才回到旧规则：凭继承公证书，或有争议时凭人民法院判决书、裁定书、调解书办理。
- **容易写错的附带说法**：①"1万元以下免公证"已过时，现为5万元。②5万元按同一法人银行所有账户**合计**计算；黄金积存、代销国债和理财计入，丧葬费、抚恤金不计入（6号文第二条、第五条）。③不能只取一部分，须一次性提取并销户。④不需要全体继承人到场。⑤第一顺序继承人可申请查询死亡后及死亡前6个月的交易明细（6号文第四条）。⑥遗产份额：若存款属夫妻共同财产，先分一半给妈妈（第一千一百五十三条），余下由妈妈和"我"均分（第一千一百三十条），即约6450元和2150元。但这是继承人之间的份额，银行只向申请人一次性支付。⑦若死者还有其他子女（含非婚生、养子女、有扶养关系的继子女），他们也是第一顺序继承人。⑧18号文不适用于涉及境外个人的存款（第十二条）。
