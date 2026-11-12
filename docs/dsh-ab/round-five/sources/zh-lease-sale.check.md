# Adversarial check: zh-lease-sale.md, "Facts for the key"

Checked by an agent that did not write the source file. On disk I read only `prompts\zh-lease-sale.txt` and `sources\zh-lease-sale.md`. The task's reference date is 2026-10-25. The fetches ran over the turn of the day, so some were made just after midnight on 2026-10-26 (local time). Every URL below was opened by me. Most pages were downloaded with curl and their text extracted locally, so those quotes are exact. Pages marked "(WebFetch)" were read through WebFetch only. Quotes are verbatim, two lines at most. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: I found no new rule, amendment or announcement up to 2026-10-25 that makes the premise true or changes a fact in the key.
- Civil Code. The NPC's list of laws in force, dated to the close of the 24th NPCSC session on 2026-08-28, shows the Civil Code with no amendment. The next NPCSC session (25th) runs 2 to 6 November 2026, and its announced agenda does not name the Civil Code. The agenda does include an unnamed bundle, "突发事件应对法等15部法律的修正案草案". Even if the Code were in that bundle, nothing would be in force by the reference date.
- SPC interpretations. The SPC 司法解释 listing (court.gov.cn/fabu/gengduo/16.html and its pages 2, 3 and 6) shows nothing new on housing leases since the 2020-12-23 revision. The newest item is dated 2026-09-21.
  - The 2026-08-06 decision amending nine interpretations covers only shipping-oil and environmental interpretations, not the lease interpretation.
  - The 2025-07-23 执行异议之诉 interpretation concerns enforcement proceedings, judging by its title (I did not open it). This case is a private sale with no enforcement.
- State Council. The gov.cn policy front page lists nothing on housing leases from late September to 2026-10-23. The 住房租赁条例 page still shows the 2025 text, in force since 2025-09-15. This was a check of one listing page, not of every State Council amending decision.
- Chengdu. The Chengdu regulation's official text (cdrd.gov.cn) refused connections, so its article numbers remain unverified, as the source says. 成办规〔2026〕7号 (dated 2026-07-14, effective 2026-08-15) loaded and contains nothing on sales or deposits. A local regulation cannot override Civil Code Art. 725 in any case.

Tooling note: the shared WebSearch budget for this turn was already used up before my first search, so I made no web searches. Every check used direct fetches of known primary URLs, or links followed from official sites (npc.gov.cn, court.gov.cn, gov.cn, scspc.gov.cn). Four sites would not load:
- cdrd.gov.cn and qdjmfy.sdcourt.gov.cn refused connections from both curl and WebFetch;
- the chengdu.gov.cn and cdzj.chengdu.gov.cn home pages returned HTTP 412, although the chengdu.gov.cn PDF loaded;
- the gongbao.court.gov.cn link did not resolve (302).

## The premise

**F1. "买卖破租赁" is backwards: Civil Code Art. 725 says a change of ownership during the tenant's possession does not affect the lease. The Code has been in force since 2021-01-01 and has not been amended.**
Status: **stands**
- URL: https://www.court.gov.cn/zixun/xiangqing/233181.html (full text of 民法典 on the SPC site, "发布时间：2020-06-01 22:20:13")
- Quote: "第七百二十五条 租赁物在承租人按照租赁合同占有期限内发生所有权变动的，不影响租赁合同的效力。"
- Quote (same page): "第一千二百六十条 本法自2021年1月1日起施行。"
- URL: http://www.npc.gov.cn/npc/c2597/c5854/c5855/202609/P020260904396146393500.pdf (现行有效法律目录（303件）, linked from the npc.gov.cn home page)
- Quote: "（截至 2026 年 8 月 28 日 十四届全国人大常委会第二十四次" / "1．中华人民共和国民法典（2020 年通过）". Other entries on the same list show amendment years, for example "2026 年修订" for the trademark law. The Civil Code entry shows none.
- URL: http://www.npc.gov.cn/npc/c2/kgfb/202610/t20261022_457908.html (Xinhua report of the 74th chairmen's meeting, 2026-10-22)
- Quote: "会议决定，十四届全国人大常委会第二十五次会议11月2日至6日在北京举行。" The agenda that follows does not name the Civil Code.

**F2. The new owner became the landlord under the existing lease when the transfer was registered on 2026-10-20. No new contract and no consent are needed.**
Status: **stands**
- URL: https://zjw.beijing.gov.cn/bjjs/zwgk46/ywtz/fzxc19/yasf79/743864075/index.shtml (北京市住建委, "发布时间：2022年11月17日")
- Quote: "张某在取得涉案房屋所有权之后，虽然没有与原承租人重新签订租赁合同，但袁某就涉案房屋签订的租赁合同对张某具有约束力，张某在取得涉案房屋所有权之时即与原承租人之间成立了租赁合同关系。"
- URL: https://www.court.gov.cn/zixun/xiangqing/456001.html (入库参考案例解读, "发布时间：2025-02-27 09:45:54")
- Quote: "承租人与买受人之间无须另行签订租赁合同，买受人在取得该租赁物的所有权时就概括承受原租赁合同的权利义务，包括承租人继续使用收益租赁物及租金收取权。"
- Quote (same page): "租赁物为不动产的，以登记时取得所有权。" This page is about a court auction. The same paragraph says the rule follows from Art. 725 and that judicial auctions often have the same result as ordinary sales.
- URL: https://tajs.taian.gov.cn/art/2025/4/29/art_215145_10309255.html (泰安市住建局, 2025-04-29; curl failed on the first try and loaded on the second)
- Quote: "即使所有权发生变动，新房主自动承继原房主出租人的主体地位，无须也无法完成房屋交接。"
- Art. 555 (court.gov.cn 233181): "当事人一方经对方同意，可以将自己在合同中的权利和义务一并转让给第三人。" The claim that this consent rule does not apply to a transfer by law is an inference, not a quoted rule. The Beijing and SPC quotes above support it: the buyer is bound without any new agreement.

**F3. The new owner cannot demand that the tenant leave before 2027-02-28. The tenant may stay to the end of the term unless the tenant agrees to leave.**
Status: **stands**
- URL: http://www.laoshan.qdjcy.gov.cn/html/jcwh/20230310/1/588.html (崂山区检察院, "[日期：2023-03-10 18:09:35]")
- Quote: "也就是说，新房东、旧房东都应当继续履行租赁合同，都没权利要求租客搬家。租客可以继续租住房屋，直至合同期满，租客本人协商同意解租的除外。"
- URL: https://tajs.taian.gov.cn/art/2025/4/29/art_215145_10309255.html
- Quote: "如租客坚持按照原租赁合同履行的，新房东必须遵守。"
- URL: https://www.zhongshan.jcy.gov.cn/article/view/cateid/23/id/18846.html (中山检察, "发布时间：2025-05-21")
- Quote: "房子现在已经是我的了，你和小典签的合同自动作废" / "法院最终判决大典败诉，小民有权继续承租至《租房合同》期满。"
- URL: https://zzzyfy.hncourt.gov.cn/public/detail.php?id=718 (郑州中原区法院, "发布时间：2013-09-25 09:57:58")
- Quote: "在租赁期限没有到期的情况下，无权直接要求承租人小高提前返还租赁的房屋，故本院对其要求腾房并赔偿损失的诉讼请求不予支持。"
- The 郑州 buyer made almost the same claim as the WeChat message: "我知道房子租给别人了，但那是承租人和旧房主之间的事，跟我没关系". The court rejected it.
- Precision the source leaves out: the 中山 case concerns a shop (商铺, 奶茶店) and the 郑州 case a shopfront (门面房), not homes. Art. 725 covers every 租赁物, so the rule is the same. The Beijing case (F2) and the 崂山 page are about housing.
- The 中山 page's typo ("…发生变动时影响已经存在的租赁合同的效力", missing "不") is present as the source says. The same page's statute link quotes Art. 725 correctly.

**F4. Exceptions: a mortgage created before the lease and then enforced, a court seizure before the lease, or a contrary agreement. None applies on the stated facts. A voluntary sale of a mortgaged flat is not enforcement of the mortgage.**
Status: **stands**. The source's citation can now be upgraded from the 泰安 reprint to the SPC's own text.
- URL: https://www.court.gov.cn/fabu/xiangqing/282621.html (SPC decision amending 27 civil interpretations, with the revised texts reissued; "发布时间：2020-12-31 18:38:39")
- Quote: "第十四条租赁房屋在承租人按照租赁合同占有期限内发生所有权变动，承租人请求房屋受让人继续履行原租赁合同的，人民法院应予支持。但租赁房屋具有下列情形或者当事人另有约定的除外："
- Quote (same article): "（一）房屋在出租前已设立抵押权，因抵押权人实现抵押权发生所有权变动的；" / "（二）房屋在出租前已被人民法院依法查封的。"
- The 泰安 reprint the source used (http://fg.taian.gov.cn/art/2022/11/15/art_47741_3412251.html, "发布日期：2022-11-15") has the same text, word for word.
- URL: https://www.court.gov.cn/fabu/xiangqing/508041.html (2026-08-06 decision amending nine interpretations, in force 2026-08-15). All nine are shipping-oil or environmental interpretations, so the lease interpretation is untouched.
- Civil Code Art. 405 (court.gov.cn 233181): "抵押权设立前，抵押财产已经出租并转移占有的，原租赁关系不受该抵押权的影响。"
- Added support for "a voluntary sale is not enforcement", from Art. 406 (same page): "抵押期间，抵押人可以转让抵押财产。当事人另有约定的，按照其约定。抵押财产转让的，抵押权不受影响。" A sale by the owner leaves any mortgage in place. Enforcement by the mortgagee is a separate event, and only enforcement is excepted.
- URL: https://www.zhongshan.jcy.gov.cn/article/view/cateid/23/id/18846.html
- Quote: "但也存在例外，如果房屋是先抵押后出租或者被查封后才出租的不适用该原则。"

**F5. The lease has a fixed term, so the new owner has no right to end it by giving notice. Termination on notice is only for indefinite-term contracts.**
Status: **stands**
- URL: https://www.court.gov.cn/zixun/xiangqing/233181.html
- Art. 563, second paragraph: "以持续履行的债务为内容的不定期合同，当事人可以随时解除合同，但是应当在合理期限之前通知对方。"
- Added, the lease-specific version, Art. 730: "当事人对租赁期限没有约定或者约定不明确，依据本法第五百一十条的规定仍不能确定的，视为不定期租赁；当事人可以随时解除合同，但是应当在合理期限之前通知对方。" This lease runs from 2026-03-01 to 2027-02-28, so Art. 730 does not apply.
- The key cites "第五百六十三条第二款". That is correct: on the page this sentence is the article's second paragraph.

## What the tenant can do

**F6. The tenant can choose: (a) stay and keep paying; (b) leave early under a negotiated written agreement; (c) terminate because of the anticipatory refusal and claim losses plus any contract 违约金. No compensation amount is fixed by law.**
Status: **stands**
- URL: https://www.court.gov.cn/zixun/xiangqing/233181.html
- Art. 578: "当事人一方明确表示或者以自己的行为表明不履行合同义务的，对方可以在履行期限届满前请求其承担违约责任。"
- Art. 563 (1)(2): "（二）在履行期限届满前，当事人一方明确表示或者以自己的行为表明不履行主要债务；"
- Art. 577: "当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。"
- Art. 584: "损失赔偿额应当相当于因违约所造成的损失，包括合同履行后可以获得的利益；但是，不得超过违约一方订立合同时预见到或者应当预见到的因违约可能造成的损失。"
- Art. 585: "当事人可以约定一方违约时应当根据违约情况向对方支付一定数额的违约金，也可以约定因违约产生的损失赔偿额的计算方法。"
- Art. 562: "当事人协商一致，可以解除合同。"
- The Beijing award was one month's rent under the contract's own clause, from the Beijing page (F2): "王某要求张某承担相当于一个月租金的违约金，数额并未过高，且符合合同约定，应予支持。"

**F7. Do not just move out: in a Jinan case a tenant who left without evidence of being told to go lost the damages and 违约金 claims. Keep the WeChat message.**
Status: **stands**
- URL: http://society.people.com.cn/n1/2024/0924/c1008-40326816.html (人民网 from 人民法院报, "2024年09月24日08:54"; 济南市槐荫区人民法院)
- Quote: "现孙某无证据证明葛某在卖房前后要求其搬离案涉房屋，也无证据证明其向新房主交纳下半年房租、新房主拒收且不允许孙某继续租赁使用。"
- Quote: "法官提醒，租赁的房屋被出售后，先别急着搬走，承租人可以基于在先的有效租赁合同主张有权占有，适用买卖不破租赁规则继续居住，直至租赁合同期限届满。"
- The page confirms the key's summary: the claims for 2万 in losses and 2400 元 违约金 were rejected.

**F8. Changing the locks or cutting off utilities to force the tenant out is a breach and is prohibited. The national regulation has applied since 2025-09-15. The Chengdu rule is confirmed only through a press report.**
Status: **stands** (Chengdu part unchanged: secondary only)
- URL: https://zjw.beijing.gov.cn/bjjs/zwgk46/ywtz/fzxc19/yasf79/743864075/index.shtml
- Quote: "新的产权人采取换锁等方式以行为表明不继续履行合同，导致承租人无法使用房屋，构成违约，应承担违约责任。"
- URL: https://www.gov.cn/zhengce/content/202507/content_7032955.htm (住房租赁条例, 国令第812号, 成文日期 2025-07-16, 发布日期 2025-07-21)
- Quote: "《住房租赁条例》已经2025年6月27日国务院第62次常务会议通过，现予公布，自2025年9月15日起施行。"
- Art. 12: "出租人依法解除住房租赁合同的，应当通知承租人，并为承租人腾退租赁住房留出合理时间。" / "出租人不得采取暴力、威胁或者其他非法方式迫使承租人解除住房租赁合同或者腾退租赁住房。"
- Art. 2: "城镇国有土地上住房租赁活动及其监督管理，适用本条例。"
- URL: https://m.gmw.cn/2026-05/27/content_1304473020.htm (光明网 reprint of 四川日报, 2026-05-27; curl, decompressed)
- Quote: "将于2026年8月1日起施行" / "3）不得擅自进入租赁住房，不得采取暴力、威胁或者停止供水、供电、供燃气等非法方式，迫使承租人解除合同或者提前腾退租赁住房。"
- The official text at https://www.cdrd.gov.cn/website/dffg/26041.jhtml refused connections from both tools. I could not find the regulation's approval on the 四川人大 site (scspc.gov.cn): the announcement and decision lists for May 2026 hold only provincial items. The session date is confirmed indirectly. 公告第107号 (https://www.scspc.gov.cn/cwhgg/202605/152708.html) says the provincial NPCSC's 27th session met on 2026-05-27: "已由四川省第十四届人民代表大会常务委员会第二十七次会议于2026年5月27日修订通过". Article numbers remain **unverified**.
- Caution for the key: the first sentence of Art. 12 is about a landlord who "依法解除". It does not give the new owner a right to end a fixed-term lease (F5). An answer that reads it as "the new owner just has to give reasonable notice" is wrong.

**F9. The next instalment (December to February, 8,400 元) goes to the new owner. Withholding rent risks giving him a lawful ground to terminate.**
Status: **stands**
- URL: https://www.court.gov.cn/zixun/xiangqing/233181.html
- Art. 722: "承租人无正当理由未支付或者迟延支付租金的，出租人可以请求承租人在合理期限内支付；承租人逾期不支付的，出租人可以解除合同。"
- The payee point rests on F2 (the buyer takes "租金收取权" from registration).

## The old landlord

**F10. Right of first refusal: the seller must notify the tenant a reasonable time before selling, and the tenant has 15 days from notice to answer. No fixed notice period such as one or three months. Exceptions: sale to a close relative, or a co-owner by shares exercising its own right. Art. 727's 5 days applies to auctions only.**
Status: **stands**, with an optional wording point
- URL: https://www.court.gov.cn/zixun/xiangqing/233181.html
- Art. 726: "出租人出卖租赁房屋的，应当在出卖之前的合理期限内通知承租人，承租人享有以同等条件优先购买的权利；但是，房屋按份共有人行使优先购买权或者出租人将房屋出卖给近亲属的除外。"
- Art. 726: "出租人履行通知义务后，承租人在十五日内未明确表示购买的，视为承租人放弃优先购买权。"
- Art. 727: "出租人委托拍卖人拍卖租赁房屋的，应当在拍卖五日前通知承租人。承租人未参加拍卖的，视为放弃优先购买权。"
- Art. 1045, which supports the source's reading that a brother is a close relative (relevant to the 中山 note): "配偶、父母、子女、兄弟姐妹、祖父母、外祖父母、孙子女、外孙子女为近亲属。"
- URL: https://www.gov.cn/zhengce/2022-01/25/content_5711968.htm (商品房屋租赁管理办法, "2010年12月1日中华人民共和国住房和城乡建设部令第6号发布 自2011年2月1日起施行")
- Quote: "第十三条 房屋租赁期间出租人出售租赁房屋的，应当在出售前合理期限内通知承租人，承租人在同等条件下有优先购买权。"
- Wording point for key item 9. It opens "原房东卖房前没有通知，违反民法典第七百二十六条" and only later adds that the buyer is unknown. Stating the qualifier first would be more exact, e.g. "如果买家不是原房东的近亲属，未通知即违反第七百二十六条". The facts stand either way.

**F11. Lack of notice gives the tenant a damages claim against the old landlord, but the sale stays valid: the tenant cannot undo it or buy the flat now.**
Status: **stands**
- URL: https://www.court.gov.cn/zixun/xiangqing/233181.html
- Art. 728: "出租人未通知承租人或者有其他妨害承租人行使优先购买权情形的，承租人可以请求出租人承担赔偿责任。但是，出租人与第三人订立的房屋买卖合同的效力不受影响。"
- URL: http://society.people.com.cn/n1/2024/0924/c1008-40326816.html
- Quote: "承租人不能主张房东与买方之间的房屋买卖合同无效，但可以请求房东承担其优先购买权被侵犯的损害赔偿责任。"
- Same page, confirming that selling is not itself a breach: "葛某将案涉房屋出售，不影响孙某的承租权利，葛某不构成违约也无须因此承担相应的责任".

**F12. The message to the old landlord should be reframed. It should reserve the Art. 728 claim, ask who holds the deposit and the rent prepaid for the period after 10-20, and seek confirmation that the lease continues. Ask for the deposit plus the unused November rent only if the tenant agrees to leave. A reply to the new owner is a bonus.**
Status: **stands** (derived from F1 to F3, F7, F10, F11, F13 and F14; no separate source needed)

## Open points

**F13. Who returns the 2,800 元 deposit after a sale is not settled by any official text found. Several answers are acceptable; stating one as settled law is wrong.**
Status: **stands** (as an open point)
- URL: https://www.gov.cn/zhengce/content/202507/content_7032955.htm
- Art. 10: "出租人收取押金的，应当在住房租赁合同中约定押金的数额、返还时间以及扣减押金的情形等事项。除住房租赁合同约定的情形以外，出租人无正当理由不得扣减押金。"
- Searching the regulation's text, I found nothing on sale or transfer. The SPC commentary (F2) says "概括承受原租赁合同的权利义务", which leans towards the new owner. I could not run new web searches (see the tooling note), so I could not look further than the source did. None of the official pages I opened (Beijing, SPC 2025, 泰安, 崂山, 中山, 郑州, 人民网) mentions deposits.

**F14. Rent for September to November, prepaid to the old landlord before the sale: the tenant should not have to pay twice. The split for 2026-10-20 to 11-30 (about 3,883.87 元) is for the two owners to settle. No official rule was found.**
Status: **stands** (as an open point)
- URL: https://www.court.gov.cn/zixun/xiangqing/456001.html. The buyer gets "租金收取权" from the date of transfer; quoted under F2.
- Art. 546 (court.gov.cn 233181): "债权人转让债权，未通知债务人的，该转让对债务人不发生效力。" As the source says, using this by analogy for a transfer of the landlord's position by law is **not verified**.
- http://qdjmfy.sdcourt.gov.cn/ytzyfy/402552/402555/8201896/index.html refused connections for me too (curl: "Failed to connect to qdjmfy.sdcourt.gov.cn:80"). It is still not relied on.

## Registration

**F15. Lease registration (备案) is not what protects the tenant. Possession is enough. The filing duty falls on the landlord.**
Status: **stands**
- Art. 706 (court.gov.cn 233181): "当事人未依照法律、行政法规规定办理租赁合同登记备案手续的，不影响合同的效力。"
- 住房租赁条例 Art. 8 (gov.cn 7032955): "出租人应当按照规定，通过住房租赁管理服务平台等方式将住房租赁合同向租赁住房所在地房产管理部门备案。" / "出租人未办理住房租赁合同备案的，承租人可以办理备案。"
- SPC interpretation Art. 5, from the SPC's own text (court.gov.cn 282621), confirming the reprint: "（一）已经合法占有租赁房屋的；" / "（二）已经办理登记备案手续的；"
- 泰安住建局: "除了必须是在房屋产权变动前已签订租赁合同外，还需以承租人已合法占有使用租赁物或租赁合同已登记备案为要件。"
- 6号令 (gov.cn 5711968), Art. 14: "房屋租赁合同订立后三十日内，房屋租赁当事人应当到租赁房屋所在地直辖市、市、县人民政府建设（房地产）主管部门办理房屋租赁登记备案。" Art. 12: "房屋租赁期间内，因赠与、析产、继承或者买卖转让房屋的，原房屋租赁合同继续有效。" Whether 6号令 is still in force after the 2025 regulation was **not confirmed** here either.
- URL: https://www.chengdu.gov.cn/gkml/uploadfiles/1607625235320909825/15272604982344417287.pdf (成办规〔2026〕7号, signed "成都市人民政府办公厅 2026年7月14日")
- Quote: "出租人出租住房不得违反本通知明确的租赁住房租住标准,并按规定办理住房租赁合同备案、如实登记承租人及实际居住人信息" (the PDF prints with extra spaces and full-width digits; I removed the spaces and wrote the digits in ASCII, here and in the next quote). Commencement: "本通知自2026年8月15日起实施,有效期五年."
- 光明网/四川日报 (F8 URL): "签约后30日内出租人应当办理备案。" Secondary.

## Numbers

**F16. Arithmetic: deposit 2,800; prepaid 8,400 covering 09-01 to 11-30. Unused 11-21 to 11-30 = 10 days, which is 933.33 (by a 30-day month) or 920.55 (by an annualised day rate). Deposit plus unused rent = 3,733.33 or 3,720.55. Post-transfer prepaid rent (10-20 to 11-30) = 3,883.87. Term left after 11-20 = 100 days. 10-25 to 11-20 = 26 days. A comparable new flat on 押一付三 needs 11,200 up front.**
Status: **stands**. Recomputed in Python:
- 2800/30×10 = 933.33. 2800×12/365 = 92.05 a day, ×10 = 920.55.
- 2800 + 933.33 = 3,733.33. 2800 + 920.55 = 3,720.55.
- October 20 to 31 inclusive is 12 days: 2800/31×12 = 1,083.87, + 2,800 = 3,883.87.
- 2026-11-21 to 2027-02-28 inclusive = 100 days. 2027 is not a leap year.
- 2026-10-25 to 2026-11-20 = 26 days. 2800×3 + 933.33 = 9,333.33. 2800 + 8400 = 11,200.
- Day-of-week check: 2026-10-20 was a Tuesday and 2026-10-25 a Sunday, so the source's change from "上周" to "前几天" is right. "前几天" also stays correct on Monday 2026-10-26.
- Caution for the key: "今天距11月20日只有26天" holds only for 2026-10-25. It is 25 days on 2026-10-26. The prompt gives no "today", so an answer cannot know the count. The key should not require it, or should accept any count consistent with the date the answer states.
- The prompt is 246 characters once the trailing newline is stripped (247 raw), matching the source.

**F17. Moving and agent costs have no official price. Estimates labelled as estimates are fine. "Official" or "legal" figures are wrong.**
Status: **stands**. No official Chengdu price schedule was found. I could not search again (see the tooling note), so I checked nothing further.

## Side claims

**F18. Citing 合同法第229条 or 民法通则第119条 as current law is a minor error: both were repealed on 2021-01-01, and the rule is the same.**
Status: **stands**
- URL: https://www.court.gov.cn/zixun/xiangqing/233181.html
- Quote: "《中华人民共和国民法通则》、《中华人民共和国收养法》、《中华人民共和国担保法》、《中华人民共和国合同法》" / "…同时废止。" (from Art. 1260)
- The 2013 郑州 page shows the old citations, which an answer copying older material might use: "我国《合同法》第229条明确规定：租赁物在租赁期间发生所有权变动的，不影响租赁合同的效力。"

**F19. Disputes go to negotiation, then mediation, arbitration or litigation. The general limitation period is three years.**
Status: **stands**
- 住房租赁条例 Art. 35 (gov.cn 7032955): "在住房租赁活动中，因押金返还、住房维修、住房腾退等产生纠纷的，由出租人和承租人协商解决；协商不成的，可以依法申请调解、仲裁或者提起诉讼。"
- Art. 188 (court.gov.cn 233181): "向人民法院请求保护民事权利的诉讼时效期间为三年。"

**F20. Side note: 泰安住建局 says the rule may not hold if the owner goes bankrupt. This does not apply here.**
Status: **stands**
- URL: https://tajs.taian.gov.cn/art/2025/4/29/art_215145_10309255.html
- Quote: "所以在破产程序中，存续的租赁合同存在终止履行的可能。在这种情况下，如果破产财产变更所有权，不能适用“买卖不破租赁”原则。"

## Premise verdict

The request's premise is false and the correction stands. The user says "买卖破租赁…房子都卖了也没办法". On the stated facts (in possession, fixed term to 2027-02-28, no mortgage or seizure, no sale-termination clause, ordinary private sale), Civil Code Art. 725 and SPC lease interpretation Art. 14 keep the lease binding on the new owner. Neither has been amended up to 2026-10-25. The demand to leave by 11-20 has no legal basis. No newer rule makes the premise true.

## Not decided in this pass
- The Chengdu regulation's article numbers and official wording (cdrd.gov.cn unreachable). The press summary covers only the forced-eviction and filing points.
- Whether MOHURD 6号令 is still in force after the 住房租赁条例.
- Any official rule on who returns the deposit, or on prepaid rent after an ordinary sale (F13, F14). The 山东 court article was unreachable, and no new searches were possible.
- Which 15 laws are in the bill the NPCSC will take up on 2 to 6 November 2026. Nothing from that session can be in force by the reference date.

## Addendum, 2026-10-26: arithmetic for the key fix after review (written by the key-fix step, not by the checker above)

No new legal or factual claim is added here, so no URL applies. The key now accepts any unused-rent figure that matches the move-out date and day-rate method the answer states. These are the extra figures it lists, recomputed in Python from facts that stand above (rent 2,800 a month; 8,400 prepaid covering 2026-09-01 to 11-30, F16):
- September to November 2026 = 30 + 31 + 30 = 91 days. 8400/91 = 92.3077 a day.
- Leaving on 11-20 (unused 11-21 to 11-30, 10 days): 2800×12/365×10 = 920.55 unrounded; with the day rate first rounded to 92.05, ×10 = 920.50; 8400/91×10 = 923.08. Plus the 2,800 deposit: 3,720.55, 3,720.50, 3,723.08.
- Reading "11月20日前搬走" as leaving on 11-19 (unused 11-20 to 11-30, 11 days): 2800/30×11 = 1,026.67; 2800×12/365×11 = 1,012.60 (1,012.55 with the rounded rate); 8400/91×11 = 1,015.38. Plus the deposit: 3,826.67, 3,812.60, 3,815.38.
- The day-count method is a convention: neither the source nor this check found a statutory method, and the key says a method set by the contract governs.

## Addendum 2, 2026-10-26: arithmetic for the second key fix after review (written by the key-fix step, not by the checker above)

No new legal or factual claim is added here, so no URL applies. The key no longer requires the post-transfer prepaid figure (10-20 to 11-30). If an answer gives it, the key accepts any figure that matches the start day and day-rate method the answer states. F2 says ownership passes "以登记时" (2026-10-20); whether 10-20 itself counts for the new owner is a day-count convention, not a checked rule. These are the extra figures the key lists, recomputed in Python from facts that stand above (rent 2,800 a month; 8,400 prepaid covering 2026-09-01 to 11-30, F16):
- Counting 10-20, October by a 31-day month: 12 days, 2800/31×12 = 1,083.87, + 2,800 for November = 3,883.87 (as in F16).
- Not counting 10-20: 11 days, 2800/31×11 = 993.55, + 2,800 = 3,793.55.
- 30-day month, counting 10-20: 2800/30×12 = 1,120.00, + 2,800 = 3,920.00 (not counting 10-20: 1,026.67 + 2,800 = 3,826.67).
- Annualised day rate, counting 10-20: 2800×12/365×12 = 1,104.66, + 2,800 = 3,904.66 (not counting 10-20: 3,812.60).
- 8,400 spread over the 91 days of September to November, counting 10-20: 10-20 to 11-30 inclusive = 12 + 30 = 42 days, 8400/91×42 = 3,876.92 (41 days, not counting 10-20: 3,784.62).
- The key's refund for a negotiated move-out is no longer fixed at 11-21 to 11-30; it is the unused days after whatever move-out date the answer states. Figures for 11-20 and 11-19 are in Addendum 1.
