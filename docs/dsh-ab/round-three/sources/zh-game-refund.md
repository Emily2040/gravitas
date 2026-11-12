# Source check: zh-game-refund (11岁孩子用家长手机和身份证实名账号充值6480元)

Checked 2026-10-22. Every URL listed as "opened" was opened that day.

Access notes:
- court.gov.cn, gov.cn, nppa.gov.cn, cac.gov.cn, kf.qq.com and support.apple.com were read with WebFetch.
- Two court pages were read with curl: 南京秦淮 had an expired certificate, and 滨州中院 refused connections. The 滨州 case was never read.
- chinacourt.org did not resolve and was not read.

Premise in the prompt: the son is 11. Last month he made more than ten top-ups totalling 6480 yuan in a mobile game, using the parent's phone and the parent's WeChat Pay. The game account is real-name verified with the parent's ID card. Customer service said that "按规定就是成年人充值，不予退款". The parent accepts this ("我也认了") and wants a message asking for a partial refund, plus settings to stop it happening again.

## 1. 最高法《指导意见（二）》: document number and the article on minors' game spending

- Verdict: **confirmed**. The document number is 法发〔2020〕17号, dated 2020-05-15 and posted 2020-05-19. The relevant article is **第9条**, under the heading "一、关于合同案件的审理".
- URL (opened): https://www.court.gov.cn/zixun/xiangqing/230181.html
- Quote, 第9条: "限制民事行为能力人未经其监护人同意，参与网络付费游戏或者网络直播平台'打赏'等方式支出与其年龄、智力不相适应的款项，监护人请求网络服务提供者返还该款项的，人民法院应予支持。"
- Current status: no repeal decision was found. Whether it is still in force **could not be verified**.
- Newer document that answers should know about: 最高人民法院办公厅《人民法院审理涉未成年人民事案件工作指引》, 法办〔2026〕76号. It was issued 2026-01-31 and announced 2026-03-18; 第27条 covers game top-ups and live-stream tips.
  - URL (opened): https://www.court.gov.cn/zixun/xiangqing/495081.html
  - Quote, 第27条第二款: "当事人针对无效合同诉请返还财产或者折价补偿的，应当予以支持；当事人诉请赔偿损失的，应当根据未成年人的年龄、智力、缔约过程、监护人履行监护职责情况等因素，认定各方当事人的过错及相应责任。"
  - The first paragraph tells courts to "综合判断缔约行为与未成年人的年龄、智力是否相适应，准确认定合同效力". The 指引 has no article on burden of proof or on accounts real-name verified to an adult.

## 2. 民法典第十九条 and 第一百四十五条

- Verdict: **confirmed**. An 11-year-old is a 限制民事行为能力人 (aged 8 or over).
- URL (opened): https://www.court.gov.cn/zixun/xiangqing/233181.html (最高人民法院, 民法典 full text)
- Quote, 第十九条: "八周岁以上的未成年人为限制民事行为能力人，实施民事法律行为由其法定代理人代理或者经其法定代理人同意、追认；但是，可以独立实施纯获利益的民事法律行为或者与其年龄、智力相适应的民事法律行为。"
- Quote, 第一百四十五条第一款: "限制民事行为能力人实施的纯获利益的民事法律行为或者与其年龄、智力、精神健康状况相适应的民事法律行为有效；实施的其他民事法律行为经法定代理人同意或者追认后有效。"
- Also relevant, from the same page:
  - 第一百五十七条 (return of property, fault sharing): "有过错的一方应当赔偿对方由此所受到的损失；各方都有过错的，应当各自承担相应的责任。" Courts cite this when they cut a refund because the parent was at fault.
  - 第一百八十八条 (limitation period): "向人民法院请求保护民事权利的诉讼时效期间为三年。"

## 3. Burden of proof when the account is real-name verified to the parent; "实名是成年人就一律不退"

- Verdict: **corrected**. No law or judicial rule says an adult real-name account bars a refund.
  - The real-name record is evidence. It is not decisive.
  - The parent bears the burden of showing that the child made the payments. Courts accept circumstantial evidence on the civil "高度可能性" standard.
  - Where the parent kept the phone, ID or payment password poorly, refunds are often partial (60%–80% in the cases below). Where the evidence points to an adult, the claim fails.
- 南京市秦淮区人民法院, 2023-11-15. The child, then 7, used his grandfather's phone. 4398 yuan; the court ordered an 80% refund.
  - URL (opened via curl): http://www.njqhfy.gov.cn/njxxweb_publishing/www/qhfyww/ggdy_2_mb_a2023112712912.html
  - Quote: "案涉游戏虽然是实名制，但并无人脸识别功能，无法排除未成年人借用成年人账号登录并充值的可能性，故本院依法认定案涉充值行为均系原告所为。"
  - Evidence factors in the judgment: "结合充值行为发生时间、充值成功率以及原告法定代理人事后投诉行为". Outcome: "4398元×80%=3518.4元".
- 芜湖鸠江区法院, reported 2025-09-11 (安徽长安网). The parent lost.
  - URL (opened): http://www.ahcaw.gov.cn/ahcaw/content/2025-09/11/content_9254010.htm
  - The game company showed the activity times did not fit a child's schedule, and the chat covered "买房、网店、育儿" topics.
  - Quote: "原告的现有证据无法证明案涉充值行为是孩子所为" and "判决驳回原告全部诉请".
- 灵宝市人民法院, 2024-09-18, on the 河南高院 site. The child registered with a classmate's ID and paid through the parents' WeChat. Mediated outcome: 60% refunded.
  - URL (opened): https://www.hncourt.gov.cn/public/detail.php?id=198662
  - Quote: "未能妥善保管自己的电子设备及银行卡密码，也应当对小晴游戏充值的民事行为承担相应的责任。" and "游戏公司返还小晴父母3186元，即充值款项的60%。"
- 最高法网络消费典型案例, 2023-03-15. A fifth-grader born in 2011 used her father's phone and Alipay in April 2022; 5949.87 yuan in about 20 minutes; the father refused to ratify, and the court ordered the claimed amount refunded.
  - URL (opened): https://www.court.gov.cn/zixun/xiangqing/393481.html
  - Quote: "该行为明显已经超出与其年龄、智力相适宜的程度，现原告对张小某的行为不予追认，被告应当将该款项退还原告"
- 陕西省市场监管局 reply, 陕市监函〔2025〕351号 (2025-06-09). It confirms that regulators help with refunds where a minor used an adult account, and that companies often stall by citing "证据不足".
  - URL (opened): https://snamr.shaanxi.gov.cn/zfxxgk/zfxxgkzl/fdzdgk/jyta/202506/t20250609_3529413.html
  - Quote: "对于未成年人用成年人账号进行的充值操作，协助配合相关部门做好退费等工作。"
- Not verified: search snippets mention a Beijing case where the platform bore 90% for lacking 人脸识别 checks, a 高密 50/50 split, and a 横琴 30% case. None of these pages was opened.

## 4. 国家新闻出版署 notices: top-up limits and play-time limits; are they current in 2026?

- 2019 notice: **confirmed**. 国新出发〔2019〕34号, signed 2019-10-25, effective 2019-11-01.
  - URL (opened): https://www.nppa.gov.cn/xxgk/fdzdgknr/zcfg_210/gfxwj_215/201911/t20191119_4695.html (nppa.gov.cn, 政府信息公开 → 规范性文件)
  - Quote: "8周岁以上未满16周岁的用户，单次充值金额不得超过50元人民币，每月充值金额累计不得超过200元人民币；"
  - Under 8: "网络游戏企业不得为未满8周岁的用户提供游戏付费服务。" Ages 16 to 18: at most 100 yuan per top-up and 400 a month.
  - Real-name registration: "所有网络游戏用户均须使用有效身份信息方可进行游戏账号注册。"
- 2021 notice: **confirmed**. 国新出发〔2021〕14号, dated 2021-08-30.
  - URL (opened): https://www.gov.cn/zhengce/zhengceku/2021-09/01/content_5634661.htm
  - Quote: "所有网络游戏企业仅可在周五、周六、周日和法定节假日每日20时至21时向未成年人提供1小时网络游戏服务"
  - Precedence: "国新出发〔2019〕34号相关规定与本通知不一致的，以本通知为准". The 2021 notice sets **no** top-up amounts, so the 2019 amounts are not displaced.
- Current in 2026: **could not fully verify**. Searches found no notice repealing or replacing either one. The 2023-12 draft 《网络游戏管理办法（草案征求意见稿）》 was found only in secondary sources, with no sign it was adopted. The 2019 notice is still listed among the NPPA's 规范性文件.
- Applied to this case: the child is 11, which is the 50/200 band. The limits apply only if the account is identified as a minor's. Here the account is the parent's, so the platform's system would treat him as an adult. That is why evidence is the deciding issue.

## 5. 未成年人保护法 and 未成年人网络保护条例

- 未成年人保护法 (2020修订, effective 2021-06-01; amended again in 2024): **confirmed**.
  - The page shows the 2024 amendment but not its date. The 2024-04-26 date I know of **could not be verified**. Articles 74 and 75 read as below.
  - URL (opened): https://www.nxjy.gov.cn/ztml/fzzfjs/202405/t20240511_4535913.html (泾源县政府, full text "2024年修正")
  - Quote, 第七十四条第二款: "网络游戏、网络直播、网络音视频、网络社交等网络服务提供者应当针对未成年人使用其服务设置相应的时间管理、权限管理、消费管理等功能。"
  - Quote, 第七十五条第二款: "国家建立统一的未成年人网络游戏电子身份认证系统。网络游戏服务提供者应当要求未成年人以真实身份信息注册并登录网络游戏。"
  - 第七十五条 also bans service to minors "每日二十二时至次日八时".
- 未成年人网络保护条例 (国务院令第766号, published 2023-10-16, effective 2024-01-01): **confirmed**.
  - URL (opened): https://www.cac.gov.cn/2023-10/24/c_1699806932316206.htm
  - Quote, 第四十四条: "应当采取措施，合理限制不同年龄阶段未成年人在使用其服务中的单次消费数额和单日累计消费数额，不得向未成年人提供与其民事行为能力不符的付费服务。"
  - Quote, 第四十六条: "网络游戏服务提供者应当通过统一的未成年人网络游戏电子身份认证系统等必要手段验证未成年人用户真实身份信息。"
  - 第四十三条 requires a minors' mode and guardian tools: "为监护人履行监护职责提供时间管理、权限管理、消费管理等功能".
- Also relevant: 消费者权益保护法实施条例 (国令第778号, effective 2024-07-01): **confirmed**.
  - URL (opened): https://www.gov.cn/zhengce/zhengceku/202403/content_6940159.htm
  - Quote, 第十六条: "经营者提供网络游戏服务的，……针对未成年人设置相应的时间管理、权限管理、消费管理等功能，在注册、登录等环节严格进行用户核验，依法保护未成年人身心健康。"
- None of these texts requires face recognition at every payment. Some courts nevertheless count its absence against the platform (see the 南京秦淮 case).

## 6. Practical controls (only what an official page confirms)

| Control | Steps / facts | Verdict | URL (opened) |
|---|---|---|---|
| WeChat: turn off fingerprint payment | "点击【我】->【服务】（微信版本低于8.0.18为【支付】）->【钱包】->【消费者保护】->【安全保障】->【安全锁】->【指纹支付开关】根据页面提示进行关闭即可。" | confirmed | https://kf.qq.com/touch/sappfaq/130807me2YZf150515QzyYFb.html |
| WeChat: turn off face payment | No official path found. The 微信支付用户服务协议 treats fingerprint and face payment alike (no password needed within a limit) | could not verify the path | — |
| WeChat: turn off 免密支付 / 自动续费 | "【我】->【服务】->【钱包】->底部【支付设置】->【自动续费】/【Apple服务扣费】/【免密支付】，找到需要关闭自动扣费的项目，点击关闭服务即可。" | confirmed | https://kf.qq.com/touch/faq/190315vm22U7190315Zb2eye.html |
| WeChat: change or reset the payment password | 忘记支付密码: 我 → 服务 → 钱包 → 支付设置 → 忘记支付密码 (seen in a kf.qq.com search snippet; page not opened). Not keeping the password where the child can see it is common sense, not an official instruction | path could not verify | — |
| WeChat Pay: dispute an order | "在微信支付账单详情页，用户可点击'对订单有疑惑'选择问题并提交咨询单"; "用户对商家服务不满意时，可随时升级投诉商家" | confirmed | https://kf.qq.com/faq/210603MVnyYB210603BveqYZ.html |
| WeChat 小游戏 minor-payment channel ("…"→反馈与投诉→支付问题→未成年支付; developer must reply within 5 working days) | Seen only in WeChat developer-community snippets. Applies only to 小游戏, not to app games | could not verify | — |
| WeChat 青少年模式 | Protects the **child's own** WeChat account. It does not help when the child uses the parent's phone and account | not relied on (snippet only) | — |
| iPhone / iPad: block in-app purchases | New path (page dated 2026-09-19): "轻点'App 和网站'，然后轻点 App Store。" then "轻点'App 内购买项目'并选择'阻止'。" Older iOS used 内容和隐私访问限制 → iTunes 与 App Store 购买项目 → App 内购买项目 → 不允许. **It blocks Apple-billed purchases only.** A top-up paid through WeChat Pay, as here, is not an Apple in-app purchase. That inference is mine and suggests Android or a non-App Store channel | confirmed (Apple page); the scope point is an inference | https://support.apple.com/zh-cn/102470 |
| Huawei: 健康使用设备 / 未成年人模式 with a 6-digit PIN | "健康使用手机模式仅对华为自有应用（如华为视频、音乐、主题、云空间），和接入了鸿蒙生态的应用有效。" It may not cover third-party games or WeChat Pay | confirmed, with that limit | https://consumer.huawei.com/cn/support/content/zh-cn16010475/ |
| Tencent 成长守护平台 | Spending limits or a one-click spending ban, time limits, per-game bans. **Tencent games only**, tied to the child's game account | confirmed | https://jiazhang.qq.com/special/feature/index.html |
| Tencent minor-refund channel (腾讯未成年人家长服务平台 mini program) | "本平台是腾讯官方受理未成年人退费的唯一渠道。" Only Tencent games and apps; the guardian must apply; originals of 户口页, birth or guardianship proof and payer details; refund goes to the original account. No deadline is stated | confirmed; relevant only if the game is Tencent's (the prompt does not say) | https://youyou.qq.com/h5/refund_guide.html ; https://kf.qq.com/touch/sappfaq/210917FFVfmU210917QzYjUj.html |
| Android generic / Google Play family controls | Not checked. Google Play is not the usual channel in mainland China | could not verify | — |

## 7. Side claims an answer is likely to add

| Claim | Correct value | Verdict | Source |
|---|---|---|---|
| A deadline for refund requests ("must apply within X days") | No statutory deadline was found. Lawsuits fall under the general 3-year limitation period (民法典第一百八十八条). Tencent's refund page states no deadline, though it closes applications if materials are never supplied | confirmed (no deadline found; 3-year limitation confirmed) | court.gov.cn 民法典; youyou.qq.com |
| 12315 | Market regulators accept minors' game top-up complaints and help with refunds; their reach over out-of-province companies is limited. Under the consumer-protection regulation a complaint needs real identity, a named respondent, a specific request and facts, and regulators handle it within 7 working days | confirmed | Shaanxi reply in §3; gov.cn 实施条例 第二十六条 and 第四十六条 |
| Some localities route game top-up complaints to the culture authority instead of 12315 | Seen in a 潜江 search snippet only | could not verify | — |
| Evidence to prepare | Courts weighed: payment times against the child's school and home schedule, number of attempts and failures, in-game chat content, which device, and when the parent complained. Tencent requires the guardian's ID photo, 户口页, birth or guardianship proof, and payer details. The WeChat Pay bill gives transaction times and merchant | confirmed (from cases and Tencent pages) | §3; Tencent FAQ |
| "8-16岁每月最多200元，超出部分必退" | The 2019 limits bind the platform when it knows the user is a minor. With an adult real-name account, the refund turns on proof, not on automatic excess | corrected | §3, §4 |
| "法院一律全额退" | False. Outcomes in the cases: 100% (最高法 2023), 80% (秦淮), 60% (灵宝, mediated), 0% (鸠江, evidence pointed to an adult). The 2026 指引 第27条 weighs guardian fault for damages | corrected | §1, §3 |
| A "全国未成年人游戏退款热线" or paid refund agents | Tencent warns that its mini program is the only channel and against agents. Hotline numbers in developer-forum posts are unofficial | confirmed (Tencent warning) | youyou.qq.com |
| 中国互联网协会《未成年人网络游戏服务消费管理要求》 responsibility percentages | Draft (征求意见稿), seen only in a search summary | could not verify | — |

## Facts for the key（答案要点）

- **前提错误："账号用家长身份证实名，按规定就是成年人充值，不予退款"。** 没有任何法律或司法文件这样规定。实名信息只是证据之一，不是"一律不退"的依据。
  - 11岁是限制民事行为能力人（民法典第十九条）。超出其年龄、智力的充值，未经监护人同意或追认不生效（第一百四十五条）。
  - 最高法《指导意见（二）》（法发〔2020〕17号）第9条：监护人请求返还的，"人民法院应予支持"。
  - 2026年最高法《人民法院审理涉未成年人民事案件工作指引》第27条要求综合判断合同效力；赔偿责任要结合监护人履职情况认定过错。
- **举证在家长：** 要拿出能证明是孩子充值的证据：充值时间是否在放学后或周末、短时间多笔、失败次数、游戏内聊天内容、所用设备、发现后及时投诉的记录。南京秦淮法院认为"虽然是实名制，但并无人脸识别功能"，按高度可能性认定是孩子充值。反过来，芜湖鸠江法院因操作时间和聊天内容显示是成年人，驳回家长全部请求。
- **部分退款是常态：** 家长保管手机、身份证、支付密码不善，法院常按过错酌减（民法典第一百五十七条）：秦淮退80%，灵宝调解退60%；最高法2023年典型案例全额退。所以家长"申请退一部分"的思路与实践一致，但不必放弃全额主张，也不应自认"就是成年人消费"。
- **正确数字：** 国新出发〔2019〕34号：未满8周岁不得提供付费服务；8周岁以上未满16周岁单次不超过50元、每月不超过200元；16周岁以上未满18周岁单次不超过100元、每月不超过400元。国新出发〔2021〕14号：只能在周五、周六、周日和法定节假日20时至21时提供1小时服务；该通知没有改动充值限额。未成年人保护法第七十五条：22时至次日8时不得提供服务。截至2026-10-22未查到废止或替代文件。
- **投诉渠道：** 先在游戏客服、微信支付账单"对订单有疑惑"中联系商家，可升级投诉；再找12315（市场监管部门协助退费，但对外省企业手段有限）；最后起诉，诉讼时效3年。腾讯游戏只能通过"腾讯未成年人家长服务平台"小程序申请，题面没说是不是腾讯游戏。
- **防再充值（官方可查的）：**
  - 微信：关闭指纹支付（我→服务→钱包→消费者保护→安全保障→安全锁→指纹支付开关）；关闭免密支付和自动续费（钱包→支付设置）；支付密码不让孩子知道。
  - 苹果设备：屏幕时间里把"App 内购买项目"设为"阻止"，但这只管苹果内购，管不住微信支付。
  - 华为：未成年人模式只对华为自有应用和鸿蒙生态应用有效。
  - 腾讯游戏：成长守护平台可设消费限额或一键禁止消费。
- **容易写错的地方：**
  - 把文号写错（应为法发〔2020〕17号，第9条），或说该意见是"司法解释"并且一定现行有效（是否仍有效未核实）。
  - 断言"超过每月200元的部分必须退"或"法院一律全额退"。
  - 说实名认证是家长就完全没希望。
  - 编造"必须在30天/90天内申请"之类的期限（未找到法定期限）。
  - 推荐代办退款机构或非官方"退款热线"。
  - 把iOS屏幕时间当作能拦住微信支付的办法；照搬旧版iOS路径而不说明版本差异。
