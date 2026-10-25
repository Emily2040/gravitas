# zh-commute-injury: adversarial check of "Facts for the key"

Checked 2026-10-23 (task date) by an agent that did not write the source file. Every URL below was opened in this pass unless marked otherwise. Quotes are verbatim in the original language.

Inputs read: `sources\zh-commute-injury.md`. The matching prompt `prompts\zh-commute-injury.txt` does not exist on disk (Read returned "File does not exist"; a glob for `zh-commute-injury*` in `prompts\` found nothing). The request was taken from line 5 of the source file: Suzhou factory worker, e-bike, solo fall on a wet road on the commute home "last Friday", wrist fracture, 3 months' rest, monthly pay 7000.

Verdicts: **stands** / **stands, refine** (correct as written; a precision is worth adding) / **refuted/needs change** (key wording must change) / **could not decide**.

Weekday arithmetic (PowerShell `[datetime]`): 2026-10-16 Friday; 2026-10-22 Thursday; 2026-10-23 Friday; 2026-10-16 + 30 days = 2026-11-15 Sunday; 2026-11-16 Monday; 2027-10-16 Saturday; 2027-10-18 Monday. Recomputed: 7000 x 3 = 21,000; 7 x 7000 = 49,000; 9 x 7000 = 63,000; 2660 x 0.8 = 2,128; 2,128 x 3 = 6,384.

Searches for newer rules (2026-10-23): no State Council amendment of 工伤保险条例 after 2010; no amendment of 社会保险法 after 2018; no Jiangsu or Suzhou document implementing 人社部发〔2025〕62号; no revision of 江苏省实施《工伤保险条例》办法 after 2015; 道路交通事故处理程序规定 has only a 2026-07 draft amendment (施行日期 blank); 道路交通安全法 has a revision draft (first reading 2026-08-25, not yet passed, see K7).

---

## A. 前提及其错误之处

**K1. 条例第十四条第（六）项只覆盖非本人主要责任的交通事故，或城市轨道交通、客运轮渡、火车事故 — stands**
- https://www.gov.cn/zwgk/2010-12/24/content_1772115.htm (国务院令第586号, in force 2011-01-01)
- "在上下班途中，受到非本人主要责任的交通事故或者城市轨道交通、客运轮渡、火车事故伤害的；" (verbatim match confirmed)

**K2. 认定依据是有关部门的法律文书或法院生效裁决（34号第二条；62号第六条）— stands**
- https://www.gov.cn/zwgk/2013-05/03/content_2395049.htm (人社部发〔2013〕34号, 2013-04-25): "《条例》第十四条第（六）项规定的"非本人主要责任"的认定，应当以有关机关出具的法律文书或者人民法院的生效裁决为依据。"
- https://www.gov.cn/gongbao/2026/issue_12526/202601/content_7056483.html (人社部发〔2025〕62号, 2025-11-13, 国务院公报2026年第3号), item 六 第一段: "应当以公安机关交通管理等有关部门出具的法律文书或者人民法院的生效裁决为依据。"

**K3. 交管部门没有确认事故事实、申请人又证明不了的，应当作出不予认定工伤结论（62号第六条）— stands**
- Same 62号 URL, item 六 第二段: "公安机关交通管理等有关部门没有确认交通事故事实存在且申请人不能证明职工受到非本人主要责任交通事故伤害的，社会保险行政部门应当作出不予认定工伤结论。"
- The document is "自印发之日起执行，此前有关规定与本意见不一致的，按本意见执行". The strings 单方, 非机动车, 电动自行车, 交通意外 do not appear in it (checked). It has no clause on facts confirmed but responsibility not allocated.

**K4. 江苏：只有报警证明或没有事故文书，调查后仍证明不了的，不予认定（苏人社规〔2020〕4号）— stands, refine**
- https://jshrss.jiangsu.gov.cn/art/2020/11/16/art_77277_9570699.html (signed 2020-11-06, in force 2021-01-01, page status "有效", no expiry), item (六)2. Verbatim confirmed: "工伤认定申请人认为职工在上下班途中受到交通事故伤害，但未提供公安机关交通管理等有关部门或者司法机关依法出具的事故处理文书，或者仅提供报警证明、交通事故不予受理决定书的，社会保险行政部门经调查核实后也不能证明职工受到非本人主要责任的交通事故伤害的，不予认定为工伤。"
- Refine: the list also names 交通事故不予受理决定书. This matters for the late-report remedy (K16): if 交管 refuses the late report, that refusal alone does not support recognition.
- Suggested wording: "江苏规定：未提供交管等部门的事故处理文书，或者只提供报警证明、交通事故不予受理决定书，人社部门调查后也不能证明非本人主要责任的，不予认定（苏人社规〔2020〕4号）。"

**K5. 江苏：交警确认事实但未划分责任，且无证据证明本人主要及以上责任的，应当认定（同上）— stands**
- Same URL, item (六)1, verbatim confirmed: "公安机关交通管理等部门或者司法机关确认事故事实，但对事故双方当事人责任未作认定或者无法认定的，社会保险行政部门经调查核实后也没有证据证明职工承担主要及以上责任的，应当认定为工伤。"
- Not contradicted by 62号: item 六 covers only the case where the facts were not confirmed.

**K6. 本案结果不确定；本人全部或主要责任基本不能认定；交通意外各方无责（程序规定第六十条）可以认定 — stands, refine**
- https://www.gov.cn/zhengce/2021-12/25/content_5712900.htm (公安部令第146号, in force 2018-05-01), 第六十条: "（一）因一方当事人的过错导致道路交通事故的，承担全部责任；" and "各方均无导致道路交通事故的过错，属于交通意外事故的，各方均无责任" (both confirmed).
- Refine: in a solo fall the rider is the only party, so the realistic outcomes are 全部责任 (60(一)), 无责任 (60(三)), or an 事故证明 (67). Weather alone has been held not to excuse the rider. A 2026-07-13 report (光明网 reprinting 经视直播, case from 2021, city not named) describes a typhoon-day e-bike solo fall where 交警 allocated no responsibility; 人社局 refused, and the court upheld the refusal: "饶某本身具有安全驾驶注意义务，台风暴雨天气并非合理的免责事由". https://m.gmw.cn/2026-07/13/content_1304531686.htm . A contrasting 2026-09-04 report (工人日报 via 光明网, Guangzhou): a dog ran into an e-bike, police certified the rider bore no responsibility, recognition upheld. https://m.gmw.cn/2026-09/04/content_1304559009.htm . Media reports, not binding, neither from Jiangsu.
- Suggested addition: "雨天路滑本身不必然被视为意外：有法院认为骑车人负有安全驾驶注意义务，恶劣天气不是免责事由（媒体报道案例，非江苏）。"

**K7. 电动车摔倒属于"交通事故"；符合国标的电动自行车是非机动车（道路交通安全法第一百一十九条）— stands, refine**
- Current text (2021 amendment) on a government site: https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/202306/t20230605_3121753.html, amendment line "根据2021年4月29日……第三次修正". 第一百一十九条:
  - (二) ""车辆"，是指机动车和非机动车。"
  - (四) ""非机动车"，是指以人力或者畜力驱动，上道路行驶的交通工具，以及虽有动力装置驱动但设计最高时速、空车质量、外形尺寸符合有关国家标准的残疾人机动轮椅车、电动自行车等交通工具。"
  - (五) ""交通事故"，是指车辆在道路上因过错或者意外造成的人身伤亡或者财产损失的事件。"
- This closes the gap the source left open (it had only the 2011 text on mfa.gov.cn).
- Refine 1: the definition requires "在道路上". A fall inside a residential compound or factory yard may fall outside 第一百一十九条（一）"道路".
- Refine 2: a revision draft (9 chapters, 170 articles) went to the NPCSC for first reading on 2026-08-25. https://www.news.cn/legal/20260825/d9969900b0c0498490470662be948e2f/c.html: "8月25日，道路交通安全法修订草案提请十四届全国人大常委会第二十四次会议审议。" It would raise the e-bike speed limit in non-motor lanes from 15 to 20 km/h. No report of a second reading or passage was found by 2026-10-23, so the 2021 text is still in force. Article numbers will change if it passes.

**K8. 工伤保险基金支付医疗费、康复费、住院伙食补助费、一次性伤残补助金、一次性工伤医疗补助金、劳动能力鉴定费等（社会保险法第三十八条）— stands**
- https://fgk.chinatax.gov.cn/zcfgk/c100009/c5192937/content.html (2018-12-29 amendment, "全文有效"). 第三十八条 items (一)(二)(六)(七)(九): "治疗工伤的医疗费用和康复费用；" "住院伙食补助费；" "一次性伤残补助金和一至四级伤残职工按月领取的伤残津贴；" "终止或者解除劳动合同时，应当享受的一次性医疗补助金；" "劳动能力鉴定费。"

**K9. 单位支付停工留薪期工资福利、一次性伤残就业补助金（第三十九条）— stands**
- Same URL, 第三十九条: "（一）治疗工伤期间的工资福利；" "（三）终止或者解除劳动合同时，应当享受的一次性伤残就业补助金。" Item (二) (五级、六级伤残津贴) is also employer-paid; it is unlikely to apply to a wrist fracture, so leaving it out is acceptable.

**K10. 只有单位未依法缴纳工伤保险费时，才由单位支付全部待遇（第四十一条；条例第六十二条）— stands, refine**
- Same URL, 第四十一条第一款: "职工所在用人单位未依法缴纳工伤保险费，发生工伤事故的，由用人单位支付工伤保险待遇。用人单位不支付的，从工伤保险基金中先行支付。"
- 条例第六十二条第二款 confirmed on the gov.cn 586号 URL. 62号 item 十二 defines the employer under 第六十二条第三款 as one that "整体职工（或部分职工）未依法参保登记或仅参保登记未依法缴纳工伤保险费".
- Suggested addition: "单位不支付的，可由工伤保险基金先行支付（社会保险法第四十一条）。"

## B. 程序与时限

**K11. 单位30日内申请（第十七条第一款）；事故日2026-10-16（周五）；期限大约到2026-11-15 — stands, refine**
- gov.cn 586号 URL, verbatim confirmed: "所在单位应当自事故伤害发生之日或者被诊断、鉴定为职业病之日起30日内，向统筹地区社会保险行政部门提出工伤认定申请。"
- 2026-10-16 is a Friday, and +30 days = 2026-11-15, which is a **Sunday**. No national or Jiangsu rule on counting this period was found (苏人社规〔2020〕4号 has none, checked). If the 民法典 rule applied (start day not counted; a period ending on a rest day moves to the next working day), the last day would be Monday 2026-11-16. "大约" covers it, but the reply should tell the employer to file well before the weekend.
- Same paragraph also says "遇有特殊情况，经报社会保险行政部门同意，申请时限可以适当延长。"
- Suggested wording: "以2026年10月16日为事故日，第30日是2026年11月15日（周日），应在此前的工作日提交，不要拖到最后一天。"

**K12. 本人1年内可直接申请（第十七条第二款），约到2027-10-16 — stands, refine**
- Same URL, confirmed: "……1年内，可以直接向用人单位所在地统筹地区社会保险行政部门提出工伤认定申请。" 2027-10-16 is a Saturday.

**K13. 单位逾期期间的工伤待遇等费用由单位负担（第十七条第四款）— stands**
- Same URL, confirmed: "用人单位未在本条第一款规定的时限内提交工伤认定申请，在此期间发生符合本条例规定的工伤待遇等有关费用由该用人单位负担。"

**K14. 职工认为是工伤、单位不认为的，单位举证（第十九条第二款）— stands**
- Same URL, confirmed: "职工或者其近亲属认为是工伤，用人单位不认为是工伤的，由用人单位承担举证责任。"

**K15. 人社部门自受理之日起60日内作出决定（第二十条）— stands**
- Same URL, confirmed: "自受理工伤认定申请之日起60日内作出工伤认定的决定".

**K16. 可以事后报警；交管三日内决定是否受案；查不实的书面告知；成因无法查清出具事故证明（程序规定第十八条、第六十七条）— stands, refine**
- https://www.gov.cn/zhengce/2021-12/25/content_5712900.htm, 第十八条 verbatim confirmed: "发生道路交通事故后当事人未报警，在事故现场撤除后，当事人又报警请求公安机关交通管理部门处理的，公安机关交通管理部门应当按照本规定第十六条规定的记录内容予以记录，并在三日内作出是否接受案件的决定。" and "经核查无法证明道路交通事故事实存在，或者不属于公安机关交通管理部门管辖的，应当书面告知当事人，并说明理由。" If the facts are verified: "经核查道路交通事故事实存在的，公安机关交通管理部门应当受理，制作受案登记表；"
- 第六十七条 confirmed: "道路交通事故基本事实无法查清、成因无法判定的，公安机关交通管理部门应当出具道路交通事故证明".
- Refine: 第一百一十二条 "本规定所称的"一日"、"二日"、"三日"、"五日"、"十日"，是指工作日，不包括节假日。" So 三日 means three working days. The regulation sets no deadline for a late report. 第十三条 required immediate reporting of an injury accident ("发生死亡事故、伤人事故的……当事人应当保护现场并立即报警"), so the late report is allowed but is weaker evidence.
- Status: only a 2026-07 draft amendment exists (公安部征求意见稿, implementation date blank, not opened). The 2017 text is in force.
- Suggested wording: "交管部门应在三个工作日内决定是否受案。"

(K17, the "措辞要求" line, is advice, not a fact. Not scored.)

## C. 如果认定为工伤

**K18. 停工留薪期原工资福利待遇不变，单位按月支付（第三十三条）；7000 x 3 = 21,000 — stands**
- gov.cn 586号 URL, confirmed: "原工资福利待遇不变，由所在单位按月支付". Arithmetic recomputed: 21,000.

**K19. 江苏凭协议医疗机构休假证明确定停工留薪期；一般不超过12个月，延长不超过12个月 — stands**
- https://www.js.gov.cn/art/2015/5/14/art_46657_2556834.html (省政府令第103号, in force 2015-06-01), 第二十五条: "工伤职工的停工留薪期应当凭职工就诊的签订服务协议的医疗机构，或者签订服务协议的工伤康复机构出具的休假证明确定。" "停工留薪期超过12个月的，需经设区的市劳动能力鉴定委员会确认。"
- 条例第三十三条第二款 confirmed: "停工留薪期一般不超过12个月。伤情严重或者情况特殊，经设区的市级劳动能力鉴定委员会确认，可以适当延长，但延长不得超过12个月。"

**K20. "原工资"在苏州问答中按工伤前12个月平均工资计算【因地而异】— stands**
- https://www.suzhou.gov.cn/szsrmzf/rdwd/202001/edc688897bfd426580cefd7862fbf18b.shtml (source 张家港市人民政府, 2020-01-22): "第一、工伤前工作时间满12个月的，按12个月的平均工资计算工伤期间的工资数额；" This is a county-level Q&A, so the 【因地而异】 tag is right.

**K21. 停工留薪期内单位不得解除或终止劳动关系（江苏办法第二十五条）— stands, refine**
- Same js.gov.cn URL: "在停工留薪期间，用人单位不得与工伤职工解除或者终止劳动关系。" It is followed by "法律、法规另有规定的除外。"

**K22. 医疗费由基金支付；住院伙食补助费、统筹地区外就医交通食宿费标准由统筹地区规定 — stands**
- gov.cn 586号 URL, 第三十条第四款 confirmed: the fund pays them and "基金支付的具体标准由统筹地区人民政府规定".

**K23. 只有评上伤残等级才有伤残待遇（第二十一条）— stands**
- Same URL, confirmed: "职工发生工伤，经治疗伤情相对稳定后存在残疾、影响劳动能力的，应当进行劳动能力鉴定。"

**K24. 一次性伤残补助金基金支付：十级7个月、九级9、八级11、七级13个月本人工资（第三十七条）— stands**
- Same URL, confirmed: "七级伤残为13个月的本人工资，八级伤残为11个月的本人工资，九级伤残为9个月的本人工资，十级伤残为7个月的本人工资".
- Suzhou restates it: the 苏州市人社局 page (2026-04-03, image 484571d3…png) lists 本人工资 x 18/16/13/11/9/7 for grades 5 to 10, "由工伤保险基金支付".

**K25. 本人工资是前12个月平均月缴费工资，60%至300%上下限（第六十四条）— stands**
- Same URL, confirmed: "本人工资，是指工伤职工因工作遭受事故伤害或者患职业病前12个月平均月缴费工资", plus the 300%/60% sentence. Jiangsu 办法第四十条 says the same.

**K26. 缴费工资7000时：十级49,000，九级63,000 — stands**
- Recomputed: 7 x 7000 = 49,000; 9 x 7000 = 63,000.

**K27. 七至十级合同终止或本人解除时，基金付医疗补助金、单位付就业补助金（第三十七条第（二）项）— stands**
- gov.cn 586号 URL (37(2) confirmed); 社会保险法第三十八条（七）and 第三十九条（三）say the same.

**K28. 江苏基准：十级3万+1.5万，九级5万+2.5万（江苏办法第二十七条）— stands**
- js.gov.cn 办法 第二十七条: 一次性工伤医疗补助金 五级20万…九级5万、十级3万; 一次性伤残就业补助金 五级9.5万…九级2.5万、十级1.5万. Cities may float up to 20% and must file with the province.

**K29. "设区的市可以上下浮动不超过20%。苏州现行数额未核实【因地而异】" — refuted/needs change (now decided)**
- https://www.suzhou.gov.cn/szsrmzf/rdwd/202604/1f994f0efb944bf881ccbba3748c3396.shtml (source 苏州市人力资源和社会保障局, page date 2026-04-03). The amounts are in images, read in this pass:
  - images/707b09b485664c8b9b9a66b88344d65f.png, 一次性工伤医疗补助金: 五级20万元, 六级16万元, 七级12万元, 八级8万元, 九级5万元, 十级3万元, "由工伤保险基金支付"; note "*患职业病的工伤职工，一次性工伤医疗补助金在上述标准的基础上增发40%。"
  - images/dc986a5691594d9ea80e6e2f1f9beb48.png, 一次性伤残就业补助金: 五级9.5万元, 六级8.5万元, 七级4.5万元, 八级3.5万元, 九级2.5万元, 十级1.5万元, "由用人单位支付".
- So Suzhou applies the Jiangsu base amounts with no float. The "could not verify" note and the 【因地而异】 tag for Suzhou should go.
- Corrected wording: "苏州执行江苏基准数额，未上浮或下浮：十级为一次性工伤医疗补助金3万元（基金支付）加一次性伤残就业补助金1.5万元（单位支付），九级为5万元加2.5万元（苏州市人社局问答，2026-04-03）。"

**K30. "距法定退休年龄不足5年时本人提出解除的，苏州按比例折减（80/60/40/20/10%）" — refuted/needs change (wrong source level, missing exception)**
- The rule is provincial: 江苏办法 **第二十八条**, js.gov.cn URL above. Opening: "工伤职工本人提出与用人单位解除劳动关系，且解除劳动关系时距法定退休年龄不足5年的，一次性工伤医疗补助金和一次性伤残就业补助金按照下列标准执行：不足5年的，按照全额的80%". Last tier: "不足1年的，按照全额的10%，但属于《中华人民共和国劳动合同法》第三十八条规定的情形除外。" Also: "达到法定退休年龄或者按照规定办理退休手续的，不支付一次性工伤医疗补助金和一次性伤残就业补助金。" The Suzhou 2026-04-03 page restates it.
- What changes: (a) cite 江苏办法第二十八条, not "苏州"; (b) it reduces **both** subsidies; (c) add the 劳动合同法第三十八条 exception. That exception matters here: if the worker resigns because the employer failed to pay wages or social insurance, the reduction may not apply. Its scope is ambiguous, because the clause sits after the 10% tier. (d) Nothing is paid once the worker has reached retirement age.
- Corrected wording: "工伤职工本人提出解除劳动关系且距法定退休年龄不足5年的，两项补助金按全额的80%、60%、40%、20%、10%递减支付；但属于劳动合同法第三十八条规定情形的除外；已达到法定退休年龄的不支付（江苏办法第二十八条，苏州执行）。"

## D. 如果不认定为工伤

**K31. 医疗期3至24个月；十年以下：本单位五年以下3个月、五年以上6个月；3个月按6个月内累计病休计算（劳部发〔1994〕479号第三、四条）— stands**
- https://www.gov.cn/zhengce/2022-08/31/content_5711269.htm (1994-12-01, in force 1995-01-01). 第三条: "根据本人实际参加工作年限和在本单位工作年限，给予三个月到二十四个月的医疗期". 第四条: "医疗期三个月的按六个月内累计病休时间计算；六个月的按十二个月内累计病休时间计算；……"

**K32. 病假工资按单位制度、合同约定支付；江苏下限为最低工资80%（江苏省工资支付条例第二十七条）— stands**
- https://www.jiangsu.gov.cn/art/2024/10/16/art_90838_6468.html (省人社厅办公室, 2024-10-16): "根据《江苏省工资支付条例》第二十七条规定，劳动者患病或者非因工负伤停止劳动，且在国家规定医疗期内的，用人单位应当按照工资分配制度的规定以及劳动合同、集体合同的约定或者国家有关规定，向劳动者支付病假工资或者疾病救济费。" and "病假工资、疾病救济费不得低于当地最低工资标准的百分之八十。国家另有规定的，从其规定。"
- https://www.nanjing.gov.cn/hdjl/hygq/202311/t20231130_4111151.html (2023-11-30) gives the same text. No amendment after 2021 was found.

**K33. 苏州（市区及张家港、常熟、太仓、昆山）月最低工资自2026-01-01起为2660元；截至2026-10-01未调整；2490是旧标准 — stands**
- https://www.suzhou.gov.cn/szsrmzf/zwgg/202601/38821c177c7b4c52ba7ae90bb0bbd7f2.shtml (关于调整苏州市最低工资标准的通知, signed 2025-12-31): "苏州市区、张家港市、常熟市、太仓市、昆山市均执行江苏省一类地区月最低工资标准，由原2490元/月调整为2660元/月。" "调整后的最低工资标准从2026年1月1日起执行。" Hourly 24 to 25 元.
- https://www.suzhou.gov.cn/szsrmzf/mszx/202610/d344e1885ec24c259d325feedb953a01.shtml (2026-10-09, national data as of 2026-10-01): "目前，江苏月最低工资标准：一类地区2660元；二类地区2430元；三类地区2180元。"

**K34. 下限2660 x 80% = 2,128元/月，3个月6,384元 — stands**
- Recomputed: 2,128 and 6,384.

**K35. 按80%下限支付的，单位须同时承担个人应缴社保和公积金（第三十二条）— stands**
- nanjing.gov.cn URL: "用人单位依照本条例第二十七条、第三十一条的规定，按照当地最低工资标准的百分之八十支付给劳动者病假工资、疾病救济费和生活费的，必须同时承担应当由劳动者个人缴纳的社会保险费和住房公积金。"

**K36. 医疗期内单位不得依劳动合同法第四十条、第四十一条解除（第四十二条第（三）项）— stands, refine**
- https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_0abfdd261c03417b949df19d869add8d.html (2012 amendment): "劳动者有下列情形之一的，用人单位不得依照本法第四十条、第四十一条的规定解除劳动合同:" "（三）患病或者非因工负伤，在规定的医疗期内的；"
- Refine: 第四十五条 also extends a fixed-term contract that expires during the medical period: "劳动合同期满，有本法第四十二条规定情形之一的，劳动合同应当续延至相应的情形消失时终止。"

**K37. 医疗费走职工医保，不由公司负担；社保法第三十条的排除范围；苏州零星报销要求交通事故认定书等证明 — stands; direct settlement could not decide**
- 社会保险法第三十条 (chinatax URL): "下列医疗费用不纳入基本医疗保险基金支付范围:（一）应当从工伤保险基金中支付的；（二）应当由第三人负担的；（三）应当由公共卫生负担的；（四）在境外就医的。"
- https://www.suzhou.gov.cn/szsrmzf/mszx/202610/ccbc1329800b44f09abb07a18d48d0e3.shtml ("苏州医保", 2026-10-12, 这些垫付的医药费，可以走零星报销), section 四: "意外伤害就医的应提供交通事故认定书、法院判决书、调解协议书等公检法部门出具的相关证明材料等。" It covers only 零星报销. It says nothing about self-caused injuries with no third party, or about a 承诺书 or 情况说明. Whether Suzhou settles a solo-fall injury directly at the hospital, and on what declaration, remains undecided.

## E. 回答可能附带的说法

**K38. "法释〔2014〕9号第六条规定没有交警认定也能认定工伤"是错的：证据规则在第一条 — stands**
- https://www.court.gov.cn/fabu/xiangqing/6775.html (in force 2014-09-01). 第一条第一款 names 第十四条第（六）项"本人主要责任": "应当以有权机构出具的事故责任认定书、结论性意见和人民法院生效裁判等法律文书为依据，但有相反证据足以推翻事故责任认定书和结论性意见的除外。" 第一条第二款: "前述法律文书不存在或者内容不明确，社会保险行政部门就前款事实作出认定的，人民法院应当结合其提供的相关证据依法进行审查。" 第六条（一）: "在合理时间内往返于工作地与住所地、经常居住地、单位宿舍的合理路线的上下班途中；" (all confirmed).

**K39. "交警不出认定书就一定不算工伤"过于绝对 — stands**
- Follows from K3 (both conditions required) and K5 (Jiangsu: facts confirmed but no responsibility allocated, so recognize).

**K40. 无责还要满足合理时间、合理路线（62号第七条；法释第六条）— stands**
- 62号 item 七: "职工以上下班为目的、在合理时间内往返于工作单位和居住地之间的合理路线，属于上下班途中。" It also lists the residences of a spouse, parents or children, and excludes "休假等属于开展个人活动或处理私事的往返时间和路线".

**K41. 停工留薪期合计最长24个月 — stands** (条例第三十三条第二款, K19).

**K42. "苏州最低工资2490元"已过时 — stands** (K33).

**K43. "工伤待遇全部由公司出"错误 — stands** (K8 to K10).

**K44. 十级伤残以本人工资为基数，有60%至300%上下限，须先评残 — stands** (K23 to K25).

**K45. 两项补助金标准由省规定；江苏有基准，市可浮动20% — stands, refine**
- K28 confirms it. Add that Suzhou uses the base amounts unchanged (K29).

**K46. "2026年工伤保险条例已修订"：没有国务院修订，最近一次是2010年；2025年11月出台的是人社部意见（三）— stands**
- The gov.cn 586号 text is the 2010 decision, in force 2011-01-01. Searches on 2026-10-23 for a 2025 or 2026 State Council amendment found none. The 2024-12 omnibus decision (in force 2025-01-20) does not list 工伤保险条例 in the reports seen. 62号 is dated 2025-11-13. Henan passed a provincial 《河南省工伤保险条例》 (2026-08-01, in force 2026-10-01), which is provincial and not relevant to Suzhou (reported in a search summary, not opened).
- Residual: the full text of the 国务院2026年度立法工作计划 (国办发〔2026〕14号) was not checked for a planned revision. A plan would not make the claim true anyway.

**K47. "电动车不是机动车，所以摔倒不算交通事故"错误 — stands** (K7; the definition covers 非机动车 "因过错或者意外", on a 道路).

---

## Tally

- Scored facts: 46 (K1 to K16, K18 to K47; K17 is advice).
- Stand: 44. Ten of them are "stands, refine": K4, K6, K7, K10, K11, K12, K16, K21, K36, K45.
- Refuted/needs change: 2. K29: the Suzhou amounts are now verified and equal the Jiangsu base, so the "未核实" note goes. K30: the reduction is Jiangsu 办法第二十八条, applies to both subsidies, has a 劳动合同法第三十八条 exception, and pays nothing at retirement.
- Could not decide: whether Suzhou 医保 settles a no-third-party solo-fall injury directly and what declaration it requires (K37); how the 30-day and 1-year limits are counted when the last day falls on a weekend (K11, K12; no national or Jiangsu counting rule found); the scope of the 第三十八条 exception in 办法第二十八条 (K30); whether 2026-10-16 is the true accident date (the prompt file is missing).
