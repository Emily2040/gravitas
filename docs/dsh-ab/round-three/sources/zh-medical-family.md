# Source check: zh-medical-family (职工医保个人账户给父母用, 居民医保"两病")

Checked 2026-10-22. Every URL below was opened that day. The nhsa.gov.cn pages and their attached .txt files were read in the desktop browser pane. ybj.ah.gov.cn (安徽省医保局) returned 403 "GeoBL" to both WebFetch and the browser, so no Anhui provincial document could be opened.

Premise in the prompt: the user is a Suzhou employee in 职工医保 with 8000+元 in his personal account (个人账户). His mother is 62, in 城乡居民医保 in Anhui, and pays about 200元 a month out of pocket for blood-pressure drugs at a pharmacy. He believes the account is for his own use only and that using it for family is 违规套保. He asks for the annual cost and how much 居民医保 pays.

## 1. 国办发〔2021〕14号: who the personal account may pay for

- Verdict: **confirmed**. Since 2021 the account may pay for the holder's spouse, parents and children, including at 定点零售药店.
- URL: https://www.gov.cn/zhengce/content/2021-04/22/content_5601280.htm (中国政府网; dated 2021-04-13, published 2021-04-22)
- Quote: "可以用于支付参保人员本人及其配偶、父母、子女在定点医疗机构就医发生的由个人负担的医疗费用，以及在定点零售药店购买药品、医疗器械、医用耗材发生的由个人负担的费用。"
- Also quoted:
  - "探索个人账户用于配偶、父母、子女参加城乡居民基本医疗保险等的个人缴费。"
  - "个人账户不得用于公共卫生费用、体育健身或养生保健消费等不属于基本医疗保险保障范围的支出。"

## 2. 国办发〔2024〕38号: the circle widened to 近亲属

- Verdict: **confirmed**.
- URL: https://www.gov.cn/gongbao/2024/issue_11526/202408/content_6969189.html (国务院公报; dated 2024-07-26)
- Quote: "支持职工医保个人账户用于支付参保人员近亲属参加居民医保的个人缴费及已参保的近亲属在定点医药机构就医购药发生的个人自付医药费用。"

## 3. Cross-province 共济 between a Jiangsu employee and an Anhui parent, as of October 2026

- Verdict: **confirmed**. It works. The check's framing as a "长三角 pilot" is **corrected**: this is a national mechanism.

**Timeline**
- **2024-12**: national pilot launched. Suzhou and Huainan were in the first 31 areas (统筹区).
  - URL: https://www.nhsa.gov.cn/art/2024/12/4/art_14_14979.html (国家医保局, 2024-12-04)
  - Quote: "江苏省（苏州市）、安徽省（淮南市）……共31个地区（统筹区）已开通个人账户跨省共济使用。"
- **By 2025-03-14**: Suzhou and all 16 Anhui cities had opened the 医保钱包 (medical insurance wallet).
  - URL: https://www.nhsa.gov.cn/art/2025/3/15/art_14_16006.html (2025-03-15)
  - Quote: "河北、河南、安徽、西藏、四川、湖北、山东7省级医保部门在全省（自治区）域范围内全面开通医保钱包"
- **National rules**: 医保发〔2025〕35号, signed 2025-12-24, published 2026-01-09.
  - URL: https://www.nhsa.gov.cn/art/2026/1/9/art_104_19293.html (the attached .txt was read)
  - Quote: "被共济人为基本医疗保险（包括职工基本医疗保险和城乡居民基本医疗保险）的参保对象。"
  - Also quoted: "个人医保钱包实行虚拟额度管理……不得将医保基金实际拨入个人医保钱包。"
  - 解读: https://www.nhsa.gov.cn/art/2026/1/9/art_105_19295.html. Quote: "将职工基本医疗保险个人账户共济范围从省内拓展至全国。"
- **Operating rules**: 医保办发〔2026〕8号, signed 2026-06-02, published 2026-06-05.
  - URL: https://www.nhsa.gov.cn/art/2026/6/5/art_104_20858.html (the attached .txt was read)
  - Quote, 第七条: "近亲属包括配偶、父母、子女、兄弟姐妹、祖父母、外祖父母、孙子女及外孙子女。"
  - Quote, 第九条: "建立共济关系时共济人应签署承诺书……"
  - Quote, 第十三条: "各省可结合实际情况设定共济额度转出频次和限额"
  - Quote, 第十一条: "被共济人不得将获得的共济额度再共济给第三人。"
- **医保钱包2.0** has run in every province since 2026-10-16.
  - URL: https://www.news.cn/politics/20261019/13d1459e234147dea4812ba8b66e5dde/c.html (新华社, 2026-10-19)
  - Quote: "并自2026年10月16日起在全国各省份及新疆生产建设兵团全部上线运行。"

**Current state (国家医保局 Q&A, 2026-10-21)**
- URL: https://www.nhsa.gov.cn/art/2026/10/21/art_14_23191.html
- This describes the user's exact case: "已实现功能1：A省职工医保参保人甲可以将个人账户共济额度给B省居民医保参保的母亲乙。"
- Use at pharmacies: "已基本实现功能2：乙可以用该额度在B省的定点医疗机构就医、在定点零售药店购药。这个功能的实现，还有赖于B省定点医药机构的配合。"
- Paying the mother's 居民医保 premium from the 额度 works so far only in 天津、江苏、江西、湖南、广东、海南、云南 and the 兵团, as of 10-20. **Anhui is not yet included**; the other regions are "预计11月份陆续实现". In this case the premium is paid in the mother's province, Anhui.
- Using the 额度 outside the mother's province, for example in Suzhou, is "预计2026年底前陆续实现".
- Some areas keep a minimum balance in the employee's own account (安全保障基线), for example "有些地区设置共济人只能将2000元个账金额以上的部分共济出去". **Could not verify** whether Suzhou or Jiangsu sets one, or at what level.

## 4. How to bind a family member

- Verdict: **confirmed**.
- URL: https://www.nhsa.gov.cn/art/2026/10/21/art_14_23191.html
- Quote: "通过国家医保服务平台APP及支付宝小程序，点击进入“医保钱包”专区，签署个人承诺书，即可完成与近亲属建立共济关系和设立共济额度等操作。"
- Offline: "共济人携带有效身份证件前往参保地医保经办服务窗口".
- Use the national app, not a provincial one: "一些省份的医保APP目前暂时无法支持操作医保钱包的跨省个账共济，故建议大家用国家医保服务平台APP".
- The mother does not need a smartphone. The son enters her name and ID number, then shows her 医保码 through his "亲情账户" at the counter.
- **Could not verify** whether Jiangsu's or Suzhou's own channels support the cross-province step. NHSA advises using the national app.

## 5. What is actually 违规

- Verdict: **confirmed**. The violation is lending your card or code for someone to use in your name (冒名使用), reselling drugs, or taking cash back. Setting up a 共济 relationship is the legal route.
- URL: https://www.gov.cn/zhengce/zhengceku/2021-02/19/content_5587668.htm (《医疗保障基金使用监督管理条例》, 国令第735号, effective 2021-05-01)
- Quote, 第十七条: "参保人员应当持本人医疗保障凭证就医、购药……妥善保管本人医疗保障凭证，防止他人冒名使用。"
- Quote, 第四十一条: "属于参保人员的，暂停其医疗费用联网结算3个月至12个月：（一）将本人的医疗保障凭证交由他人冒名使用；"
- 第十九条 also bans "转卖药品，接受返还现金、实物或者获得其他非法利益".
- When the purpose is to defraud the fund, a further fine of 2 to 5 times the amount applies (第四十一条第二款; seen in search results, not quoted directly here).
- In short: the user buying his mother's drugs with his own card or code, as if they were for him, is the risky act. Giving her a 共济额度 that she spends under her own 医保码 is the allowed act.

## 6. National "两病" rule for 城乡居民 (医保发〔2019〕54号)

- Verdict: **confirmed**. The policy-scope payment ratio is "要达到50％以上". It is tied to **二级及以下定点基层医疗机构**; pharmacies are not mentioned. Drugs must be on the national catalogue (目录). Each province sets its own payment policy.
- URL: https://www.nhsa.gov.cn/art/2019/10/10/art_37_1842.html (国家医保局 et al., 2019-10-10)
- Quote: "以二级及以下定点基层医疗机构为依托，对“两病”参保患者门诊发生的降血压、降血糖药品费用由统筹基金支付，政策范围内支付比例要达到50％以上。"
- Quote: "各省（区、市）要在摸清“两病”门诊用药人数、用药数量和金额等实际情况的基础上合理设定支付政策。"

## 7. Anhui's actual "两病" rule

- Verdict: **could not verify** the current province-wide figures.
- The provincial basis is 皖医保发〔2019〕33号. It is cited by the city document below; the provincial text could not be opened (ybj.ah.gov.cn geo-blocked).
- City example 1, **宣城** (政策解读, page metadata 2020-04-09):
  - URL: https://ylbz.xuancheng.gov.cn/OpennessContent/download/1847883.html
  - No deductible (起付线), 55% reimbursement, annual limit 450元 for hypertension.
  - Only at "二级及以下定点基层医疗机构".
  - Eligible patients are those diagnosed by a 定点医疗机构 who do not meet the 门诊常见慢性病 standard.
  - Quote: "报销比例为55%" and "高血压报销限额为450元/人"
- City example 2, **广德** (明白纸, 2023-08-01): the separate 门诊常见慢性病 route, for patients whose hypertension is 鉴定 (assessed) as a chronic condition.
  - URL: https://www.guangde.gov.cn/OpennessContent/download/2938125.html
  - Quote: "常见慢性病起付线200元/年,省内报销比例为60%，省外报销比例为50%，报销限额：2500元/年"
  - Qualifying requires a 鉴定, and the criteria vary by city.
- The mother's city in Anhui is not given. Ratios, limits and the list of eligible facilities **vary by city** and may have changed since these pages were published.

## The right answer

- **Annual drug cost**: 200 × 12 = **2400元**.
- **The premise is wrong.**
  - Since 2021 the account may pay for parents (国办发〔2021〕14号), and since 2024 for all 近亲属 (国办发〔2024〕38号).
  - Cross-province 共济 started in Suzhou and Huainan in 2024-12. All of Anhui was open by 2025-03. It has been national since 医保发〔2025〕35号, and 医保钱包2.0 has run in every province since 2026-10-16.
  - Doing it through 共济 is legal. 冒名使用 his card is the violation.
- **What he can do**:
  - In the 国家医保服务平台 App (or the 支付宝 mini program, or a counter), open 医保钱包, sign the 承诺书, add his mother, and set a 共济额度.
  - She then pays the self-pay part at 定点 clinics and pharmacies in her Anhui area. Pharmacy acceptance is "基本实现" and depends on the pharmacy.
  - Possible limits: a minimum balance kept in his account in some areas (example 2000元); provinces set frequency and amount caps; she cannot pay her 居民医保 premium from it in Anhui until about November 2026.
- **How much 居民医保 pays**: a correct answer **cannot give one fixed figure**.
  - Nationally, 两病 drugs are paid at 50% or more of the policy-scope cost, but at 基层定点医疗机构, for catalogue drugs, within local annual limits.
  - Buying at an ordinary pharmacy out of pocket, as she does now, typically gets no 居民医保 reimbursement. Whether any Anhui city covers pharmacies under 两病 could not be verified.
  - Illustration with 宣城's 2020 figures: 2400 × 55% = 1320元, capped at **450元 a year**.
  - If her hypertension qualifies as a 门诊常见慢性病 (广德 2023 example): (2400 − 200) × 60% = 1320元, within the 2500元 limit.
  - Both are local examples only. She should register or get assessed at her local 医保 office or 基层卫生院 and use catalogue drugs (集采 drugs are much cheaper; prices not verified here).
  - The remaining self-pay part can then come from the son's 共济额度.

## Side claims an answer is likely to add

| Claim | Correct value | Status | Varies by place? |
|---|---|---|---|
| "个人账户只能本人用" | wrong since 2021 (spouse, parents, children); 近亲属 since 2024 | corrected | no |
| "给家人用就是违规套保" | wrong if done through 共济; 冒名使用 the card is the violation (暂停联网结算 3–12 months) | corrected | no |
| "跨省不行 / 只有长三角试点" | wrong: national; Suzhou and all of Anhui open since 2025-03; 2.0 nationwide since 2026-10-16 | corrected | no |
| Who counts as 近亲属 | spouse, parents, children, siblings, grandparents on both sides, grandchildren on both sides | confirmed (医保办发〔2026〕8号 第七条) | no |
| 被共济人 may be in 城乡居民医保 | yes | confirmed | no |
| "钱转到妈妈卡上 / 可以取现" | wrong: a virtual 额度 (虚拟额度) only; no cash; cannot be passed on | confirmed | no |
| How to set up | 国家医保服务平台 App / 支付宝小程序 / counter; 医保钱包; sign 承诺书 | confirmed | provincial apps may not support it |
| Mother needs a smartphone | no; the son uses 亲情账户 to show her 医保码 | confirmed | no |
| 额度 usable at Anhui pharmacies | "已基本实现", depends on the pharmacy | confirmed (with caveat) | yes |
| Pay mother's 居民医保 premium from the 额度 | not yet in Anhui (live in 7 provinces + 兵团 as of 10-20; others "预计11月") | confirmed | yes |
| Use the 额度 when she visits Suzhou | not yet; "预计2026年底前" | confirmed | no |
| Minimum balance kept in his account | some areas, e.g. 2000元; Suzhou's level unknown | partly verified | yes |
| "每天3笔、每笔2000元" | figure from 1.0-era media; under 2.0 provinces set the caps (规程 第十三条) | could not verify for 2.0 | yes |
| 两病 payment ratio | at least 50% nationally (医保发〔2019〕54号) | confirmed | yes (local ratio and limit) |
| Anhui 两病 ratio and limit | 宣城 2020: 55%, no deductible, 450元/year (hypertension), 基层 facilities only | local example; current provincial figure could not verify | yes |
| Must use 定点 / 基层 facility and catalogue drugs | yes for 两病 (二级及以下定点基层医疗机构, 目录内) | confirmed nationally | yes |
| 门诊慢性病 route for hypertension | exists; needs 鉴定; 广德 2023: 起付线 200, 60%, limit 2500 | local example | yes |
| "居民医保一年能报1200元 (50% of 2400)" | wrong as a flat figure: local limits apply and pharmacy self-pay is usually not covered | corrected | yes |
| NHSA fraud reporting line | 010-89061396, 010-89061397 (footer of nhsa.gov.cn pages) | confirmed | no |
| 12393 医保服务热线 | not checked | could not verify | n/a |

## Facts for the key（答案要点）

- 前提错误："个人账户只能本人用，给家人用就是违规套保"是错的。
  - 国办发〔2021〕14号起，个人账户可以支付本人及配偶、父母、子女在定点医疗机构和定点零售药店的个人负担费用。
  - 国办发〔2024〕38号把范围扩大到近亲属。
  - 跨省共济：2024年12月在苏州、淮南等首批31个统筹区试点，2025年3月14日前安徽全省16市和苏州都已开通医保钱包。医保发〔2025〕35号把共济范围推向全国，医保钱包2.0自2026年10月16日起在全国上线。
  - 真正违规的是把本人医保卡或医保码交给他人冒名使用（《医疗保障基金使用监督管理条例》第四十一条，暂停联网结算3至12个月），以及转卖药品、套现。
- 正确做法：
  - 在国家医保服务平台App（或支付宝小程序、参保地窗口）进入"医保钱包"，签署承诺书，与母亲建立共济关系并设定共济额度。
  - 母亲在安徽参保地的定点医疗机构和药店用自己的医保码结算，药店能否用要看机构是否配合（"已基本实现"）。
  - 共济额度是虚拟额度，不能取现，也不能再转给第三人。
  - 截至10月20日，用共济额度缴纳居民医保费在安徽尚未开通（预计11月），在省外就医购药预计2026年底前实现。部分地区要求个人账户保留基线，例如2000元。
- 药费：200元 × 12个月 = 2400元/年。
- 居民医保能报多少：不能给出一个确定数字。
  - 国家规定"两病"门诊降压药在二级及以下定点基层医疗机构、目录内药品，政策范围内支付比例达到50%以上，具体比例和限额由各地定。
  - 现在在普通药店自费买药，一般报不了。
  - 安徽各市不同。宣城2020年的例子：不设起付线，报销55%，高血压限额450元/年，2400元最多报450元。
  - 如果经鉴定纳入门诊常见慢性病（广德2023年的例子：起付线200元，报销60%，限额2500元），可以报约1320元。
  - 应当让母亲到参保地医保部门或基层卫生院做"两病"登记或慢病鉴定，并使用目录内药品，自付部分再用共济额度支付。
- 容易写错的地方：
  - 说只能自费。
  - 说跨省不能共济，或说只有长三角试点。
  - 近亲属只写配偶、父母、子女。
  - 说钱能转到银行卡或提现。
  - 直接写"居民医保报50%、一年报1200元"，忽略限额和就医机构的限制。
  - 断言安徽现在已经能用共济额度缴纳居民医保。
  - 把"每天3笔、每笔2000元"当作现行全国统一规定。
