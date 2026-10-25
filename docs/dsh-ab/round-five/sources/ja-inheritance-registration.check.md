# Adversarial check: ja-inheritance-registration.md, items 1 to 25 and "Facts for the key"

Checked by an agent that did not write the source file. On disk I read only `prompts/ja-inheritance-registration.txt` and `sources/ja-inheritance-registration.md`. Every URL below was opened in this session (2026-10-25, running past midnight into 2026-10-26 JST). I downloaded each page with curl and extracted the text locally (HTML parser or pypdf). Statutes were read through the e-Gov law API v1 (`laws.e-gov.go.jp/api/1/articles`, current text). Revision histories and future texts came from API v2 (`/api/2/law_revisions`, `/api/2/law_data`). Quotes are verbatim, two lines at most. Item numbers follow the source file. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: I found no rule, amendment or announcement up to 2026-10-25 that makes the premise true or changes a substantive fact. (1) The e-Gov revision list for 不動産登記法 shows two newer amending acts. 令和八年法律第四十六号 (promulgated 2026-06-24) has parts in force since 2026-06-24 and parts due 2028-12-23. I compared the full article text of the revisions before and after each step. Neither step changes 76条の2, 76条の3, 76条の5, 119条の2 or 164条: the 2026-06-24 step changes no article in the main provisions, and the 2028-12-23 step changes only 100条. (2) 民法 is amended by 令和八年法律第四十五号 (promulgated 2026-06-24). Its steps on 2027-06-23, 2028-12-23 and 2029-06-23 change the will articles (967 to 984, 1004, 1005) and the guardianship articles (7 to 20, 838 to 876, 917). None of them changes 140, 142, 143, 898, 900, 904の3, 909の2, 915, 921, 1028 or 1031. (3) The newest MOJ pages say the same as the source: 相続登記の申請義務化について (令和8年4月1日) and スマート変更登記 (令和8年9月30日). One newer detail is on the スマート変更登記 page. From 2026-10-13, a 登記官 may also mark an owner's death (符号の表示) while reviewing a registration application whose attached 戸籍 shows the death. This does not affect the duty or the deadlines. (4) Pending, not law: in its 令和9年度税制改正要望, MOJ asks to extend the 相続登記 登録免許税 exemptions (租税特別措置法84条の2の2) by two years beyond 2027-03-31. It also asks to relax the 1,000,000 yen land condition. The ruling parties' tax outline normally comes out in December, so nothing is decided as of 2026-10-25 (item 8). (5) The 遺族厚生年金 review in the 2025 pension law takes effect in April 2028 (MHLW), so it does not reach a 2026 death (item 18). (6) The NTA Tax Answer pages used are all marked 「[令和8年4月1日現在法令等]」, and the 日司連 still lists the 令和6年3月 fee survey as its latest.

Tooling note: WebSearch was used only to look for newer rules. All facts were checked against pages I downloaded myself. I used one WebFetch, for the MHLW pension-reform page.

## The premise

**Item 1. 「相続登記は義務じゃない」 is false. Registration has been a legal duty since 2024-04-01: within 3 years of knowing.**
Status: **stands** (the premise is false)
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (法務省「相続登記の申請義務化に関するQ＆A」, 令和7年3月27日, 初回掲載日 令和6年3月28日)
- Quote (A1): 「相続人は、不動産（土地・建物）を相続で取得したことを知った日から３年以内に、相続登記をすることが法律上の義務になりました。」
- Quote (A2, A3): 「令和３年に法律が改正され、これまで任意だった相続登記が義務化されました。」 / 「相続登記の義務化は、令和６年４月１日から始まりました。」
- URL: https://www.moj.go.jp/MINJI/minji05_00599.html (法務省「相続登記の申請義務化について」, 令和8年4月1日)
- Quote: 「…その不動産の所有権を取得したことを知った日から３年以内に相続登記の申請をすることが義務付けられました（不動産登記法第７６条の２第１項）。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=416AC0000000123;article=76_2 (current text; unchanged through the last scheduled revision, see the newer-rule search above)
- Quote: 「…自己のために相続の開始があったことを知り、かつ、当該所有権を取得したことを知った日から三年以内に、所有権の移転の登記を申請しなければならない。」
- 「売るときにやればいい」: also wrong. The duty runs from knowing, not from a sale, and a sale needs a full 相続登記 (item 5).

**Item 2. Deadline for this family: 2029-07-10. 2027-03-31 applies only to inheritances known before 2024-04-01.**
Status: **stands**
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (A4)
- Quote: 「令和６年４月１日より前に相続したことを知った不動産で、相続登記がされていないものについては、令和９年３月３１日までに相続登記をする必要があります。」
- URL: https://www.moj.go.jp/MINJI/minji05_00599.html
- Quote: 「令和９年３月３１日まで（不動産を相続で取得したことを知った日が令和６年４月以降の場合は、その日から３年以内）」
- Calendar rules: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=140 (「期間の初日は、算入しない。」) and article=143 (「…その起算日に応当する日の前日に満了する。」)
- Recomputed: knew 2026-07-10, so the period starts 2026-07-11 and ends 2029-07-10, a Tuesday.

**Item 3. After a later 遺産分割, the result must be registered within 3 years of the 分割. This clock applies after a 法定相続分 registration or a 相続人申告登記.**
Status: **stands**, with one optional precision
- URL: https://www.moj.go.jp/MINJI/minji05_00599.html
- Quote: 「遺産分割が成立した日から３年以内にその内容を踏まえた所有権の移転の登記を申請することが義務付けられました（不動産登記法第７６条の２第２項、第７６条の３第４項等）。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=416AC0000000123;article=76_3 (76条の3第4項)
- Quote: 「第一項の規定による申出をした者は、その後の遺産の分割によって所有権を取得したとき（…）は、当該遺産の分割の日から三年以内に、所有権の移転の登記を申請しなければならない。」
- URL: https://www.moj.go.jp/content/001404761.pdf (flowchart, page 令和６年４月１日以降に相続開始)
- Quote: 「遺産分割の結果に基づく相続登記」「※不動産の相続を知った日から３年以内」, and after a 申告登記: 「※遺産分割の日から３年以内」.
- URL: https://www.moj.go.jp/content/001408564.pdf (令和5年9月12日 法務省民二第927号通達, 第2の2). It contains 「当該遺産の分割の日から３年以内」, as the source says.
- Precision (optional): 76条の2第2項 applies only to an heir who gets more than the 法定相続分 share: 「当該遺産の分割によって当該相続分を超えて所有権を取得した者は」. The source's reading is correct: a 分割 inside the first 3 years does not push back the 2029-07-10 deadline. The flowchart confirms this.

**Item 4. The sanction is a 過料 of up to 100,000 yen, only without a 正当な理由, and only after a 催告. The court decides the amount.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=416AC0000000123;article=164 (current text)
- Quote: 「…第七十六条の二第一項若しくは第二項又は第七十六条の三第四項の規定による申請をすべき義務がある者が正当な理由がないのにその申請を怠ったときは、十万円以下の過料に処する。」
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (3-A2, 3-A4)
- Quote: 「(1)　登記官が、義務違反を把握した場合、義務違反者に登記をするよう催告します（催告書を送付します。）。」 / 「過料は、１０万円以下の範囲内で裁判所において決定されます。」
- Same page, 3-A3: a 催告 is sent only when one of two triggers occurs, each a registration showing another unregistered property (「次の(1)又は(2)を端緒として…職務上知ったときに限り」). 3-A5 lists the 正当な理由 examples, including (5) 「…費用を負担する能力がない場合」.
- URL: https://www.moj.go.jp/MINJI/minji05_00599.html: the 過料 notice goes to 「管轄の地方裁判所」 (不動産登記規則187条1号).

**Item 5. 相続人申告登記 satisfies the basic duty only. It does not cover a later 分割, a sale or a mortgage.**
Status: **stands**, with one optional precision
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (4-A1, 4-A4)
- Quote: 「…遺産分割がされた後にこれに基づく登記をする義務を相続人申告登記によって履行することはできないことや、」「…相続した不動産を売却したり、抵当権の設定をしたりするような場合には相続登記をする必要があることに留意が必要です。」
- Quote (4-A4): 「相続人申告登記は、申出をした相続人についてのみ、相続登記の義務を履行したものとみなされます。」 and 「…複数の相続人が連名で申出書を作成することで、複数人分の申出をまとめてすることもできます。」
- URL: https://www.moj.go.jp/MINJI/minji05_00602.html (「相続人申告登記について」, 令和8年3月24日)
- Quote: 「〇 不動産についての権利関係を公示するものではないため、相続した不動産を売却したり、抵当権の設定をしたりするような場合には、別途、相続登記の申請をする必要がある」
- Quote: 「○ 特定の相続人が単独で申出可（他の相続人の分も含めた代理申出も可）」 / 「○ 登録免許税がかからない」
- Statute, 76条の3第2項 (URL as item 3): 「前条第一項に規定する期間内に前項の規定による申出をした者は、同条第一項に規定する所有権の取得（当該申出の前にされた遺産の分割によるものを除く。）に係る所有権の移転の登記を申請する義務を履行したものとみなす。」
- Precision (optional): the parenthesis means a 申告登記 filed after a 分割 does not cover the share received by that 分割. If the family agrees that the mother takes the house, she must make a full 相続登記 by 2029-07-10. A later 申告登記 would not be enough for her.

**Item 6. Until a 分割, all three heirs co-own the house in 法定相続分 shares, and all three carry the duty.**
Status: **stands**
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (2-A4)
- Quote: 「遺産分割をしていない場合には、全ての相続人が法定相続分の割合で不動産を取得（共有）した状態となるので、あなたも不動産を相続で取得したことになるためです。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=900
- Quote: 「子及び配偶者が相続人であるときは、子の相続分及び配偶者の相続分は、各二分の一とする。」 With 四号 (equal shares among children): mother 1/2, each child 1/4.

## The cost (the uncle's 「何十万」)

**Item 7. 登録免許税 is 0.4% of the 固定資産税評価額: 32,000 + 8,000 = 40,000 yen.**
Status: **stands**
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/inshi/7191.htm (No.7191, [令和8年4月1日現在法令等])
- Quote (land): 「相続、法人の合併または共有物の分割」「不動産の価額（注）」「1,000分の4」. Building: 「相続または法人の合併による所有権の移転」「1,000分の4」.
- Quote (note): 「課税標準となる「不動産の価額」は、市町村役場で管理している固定資産課税台帳に登録された価格がある場合は、原則その価格です。」
- Recomputed: 8,000,000 × 4/1000 = 32,000. 2,000,000 × 4/1000 = 8,000. Total 40,000. The 売買 rate is 1,000分の20, which is the wrong value for this case.

**Item 8. The exemption for land worth 1,000,000 yen or less (until 2027-03-31) does not apply.**
Status: **stands** as of 2026-10-25. See the note on the pending tax request.
- URL: https://houmukyoku.moj.go.jp/homu/page7_000017.html (更新日 2026年4月1日)
- Quote: 「…免税措置の適用期限が令和９年（2027年）３月３１日までに延長されるとともに、…不動産の価額が１００万円以下の土地であれば、この免税措置が適用されることになりました。」
- Quote: 「※１不動産の所有権の持分の取得に係るものである場合は、当該不動産全体の価額に持分の割合を乗じて計算した額が不動産の価額となります。」
- Recomputed: land 8,000,000. The shares would be 4,000,000 (1/2) and 2,000,000 (1/4), all over 1,000,000. The building is never covered.
- Pending request. URL: https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2027/request/moj/09y_moj_k.pdf (法務省民事局 令和9年度税制改正要望事項)
- Quote: 「延長：次の登録免許税の特例措置を２年間延長する。」 / 「新規・拡充：上記②の要件を緩和する等の更なる拡充や新たな特例措置を講ずる。」
- Same document: from 2026-04-01 the legal basis is 租税特別措置法84条の2の2 (formerly 84条の2の3), which matches the source. Caution for the key: this is a ministry request, not law. The family's land qualifies only if the limit were raised above its value. Check again after the December tax outline.

**Item 9. 司法書士 fees are set freely. The 2024 survey average for this exact case is 74,888 yen, tax included.**
Status: **stands**
- URL: https://www.shiho-shoshi.or.jp/about/remuneration/ (日司連「司法書士の報酬」; the page lists 「報酬アンケート結果（2024年（令和6年）3月実施）」 as current)
- Quote: 「司法書士が業務を行ったときに受ける報酬については、各司法書士が自由に定めることになっています。」
- URL: https://www.shiho-shoshi.or.jp/cms/wp-content/uploads/2024/11/2a2e2c594bc4cd9ff2ca0f6d916db85e.pdf
- Quote: 「相続を原因とする土地１筆及び建物１棟（固定資産評価額の合計１０００万円）の所有権移転登記手続」 / 「※法定相続人は３名で、うち１名が単独相続した場合」「【有効回答数:1109 ／ 平均:74,888円】」
- URL: https://www.shiho-shoshi.or.jp/cms/wp-content/uploads/2024/11/ea979f4293415de083eae4a9de3ce36f.pdf (survey notes)
- Quote: 「実施時期・・・・・・・・・令和６年３月」 / 「消費税・・・・・・・・・・金額は全て消費税を含んでいます（税率10％）」
- Recomputed: 40,000 + 74,888 = 114,888, about 115,000 yen plus 戸籍 fees.

## The dated to-do items

**Item 10. 相続放棄 and 限定承認: 3 months from knowing, so 2026-10-10 (Sat). The deadline has passed.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=915
- Quote: 「相続人は、自己のために相続の開始があったことを知った時から三箇月以内に、相続について、単純若しくは限定の承認又は放棄をしなければならない。」
- URL: https://www.courts.go.jp/saiban/syurui/syurui_kazi/kazi_06_13/index.html (裁判所「相続の放棄の申述」, no page date)
- Quote: 「申述は，民法により自己のために相続の開始があったことを知ったときから3か月以内にしなければならないと定められています。」 Filing goes to 「被相続人の最後の住所地の家庭裁判所」, fee 「収入印紙800円分（申述人1人につき）」.
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=921 (二号): 「相続人が第九百十五条第一項の期間内に限定承認又は相続の放棄をしなかったとき。」
- Extension request, re-opened here: https://www.courts.go.jp/saiban/syurui/syurui_kazi/kazi_06_25/index.html. Quote: 「申立ては，自己のために相続の開始があったことを知った時から3か月以内にする必要があります。」
- 民法142条 (article=142) applies only 「その日に取引をしない慣習がある場合に限り」, so the source is right to hedge. Recomputed: 2026-10-10 is a Saturday, 2026-10-12 is スポーツの日, and 2026-10-13 is the latest possible date. Both dates have passed.

**Item 11. 準確定申告: due 2026-11-10 (Tue), and only if the father had to file.**
Status: **stands**, but the citation label **needs change**
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2022.htm ([令和8年4月1日現在法令等])
- Label fix: the page title is 「No.2022 納税者が死亡したときの確定申告(準確定申告)」, not 「確定申告を要する人が死亡したとき（準確定申告）」.
- Quote: 「…相続の開始があったことを知った日の翌日から4か月以内に申告と納税をしなければなりません。これを準確定申告といいます。」
- Quote: 「各相続人等が連署により準確定申告書を提出することになります。」 Same page: 準確定申告書の付表 attached, filed with 「被相続人の死亡当時の納税地の税務署長」.
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=340AC0000000033;article=125
- Quote: 「…第百二十条第一項（確定所得申告）の規定による申告書を提出しなければならない場合に該当するときは、」 / 「その相続の開始があつたことを知つた日の翌日から四月を経過した日の前日」
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1600.htm ([令和8年4月1日現在法令等])
- Quote: 「その年中の公的年金等の収入金額が400万円以下であり、かつ、その年分の公的年金等に係る雑所得以外の所得金額が20万円以下である場合には確定申告の必要はありません。」 Statute: 所得税法121条3項 (article=121), which also has the salaried exemption in 1項一号 (「二十万円以下」).
- URL: https://www.nenkin.go.jp/section/faq/jukyu/uketori/tsuchisho/gensen/junkaku.html (更新日 2025年1月14日)
- Quote: 「準確定申告用源泉徴収票は、死亡届や未支給年金の手続き後、おおむね2～3カ月で発送されます。」
- Recomputed: day after knowing 2026-07-11; four months elapse on 2026-11-11; the day before is 2026-11-10 (Tue), 16 days after 2026-10-25. 2026-11-10 is a weekday, so 国税通則法10条2項 does not move it.

**Item 12. 相続税: no tax and no return. The 基礎控除 is 30,000,000 + 6,000,000 × 3 = 48,000,000 yen.**
Status: **stands**
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4152.htm ([令和8年4月1日現在法令等])
- Quote: 「課税価格の合計額 － 基礎控除額（3,000万円 ＋ 600万円 × 法定相続人の数）」
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4205.htm ([令和8年4月1日現在法令等])
- Quote: 「その取得した財産の価額の合計額が遺産に係る基礎控除額の範囲内であれば申告も納税も必要ありません。」
- Quote (deadline if needed): 「相続税の申告は、被相続人が死亡したことを知った日（通常の場合は、被相続人の死亡の日）の翌日から10か月以内に行うことになっています。」 Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=325AC0000000073;article=27 (「…その相続の開始があつたことを知つた日の翌日から十月以内…」).
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4602.htm. Building: 「固定資産税評価額に1.0を乗じて計算した金額によって評価します。」 Land: 「土地の評価方法には、路線価方式と倍率方式があります。」
- Recomputed: the stated estate is 8,000,000 + 2,000,000 + 12,000,000 = 22,000,000. With the land at double, it is 30,000,000. Both are under 48,000,000. The hypothetical deadline is 2027-05-10 (Mon).

**Item 13. 小規模宅地等 and 配偶者の税額軽減 need a return, and neither matters here.**
Status: **stands**
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4124.htm ([令和8年4月1日現在法令等])
- Quote: 「この特例の適用を受けるためには、相続税の申告書に、この特例の適用を受けようとする旨を記載するとともに、小規模宅地等に係る計算の明細書や遺産分割協議書の写しなど一定の書類を添付する必要があります。」
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4158.htm: 「（1） 1億6千万円」 or the 法定相続分 amount, claimed 「税額軽減の明細を記載した相続税の申告書または更正の請求書に」.
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4205.htm (注2): 「…租税特別措置法第69条の4（小規模宅地等についての相続税の課税価格の計算の特例）…等を適用しない場合における課税価格の合計額をいいます。」

**Item 14. Deposits before the 分割: each heir can withdraw balance × 1/3 × 法定相続分, capped at 1,500,000 yen per bank.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=909_2
- Quote: 「各共同相続人は、遺産に属する預貯金債権のうち相続開始の時の債権額の三分の一に第九百条及び第九百一条の規定により算定した当該共同相続人の相続分を乗じた額（…預貯金債権の債務者ごとに法務省令で定める額を限度とする。）については、単独でその権利を行使することができる。」
- URL: https://laws.e-gov.go.jp/api/1/lawdata/430M60000010029
- Quote: 「民法第九百九条の二に規定する法務省令で定める額は、百五十万円とする。」
- Recomputed for one bank: mother 12,000,000 × 1/3 × 1/2 = 2,000,000, capped at 1,500,000. Each child 12,000,000 × 1/3 × 1/4 = 1,000,000.

**Item 15. 法定相続情報証明制度 is free. 戸籍 can be requested at any 市区町村 (広域交付) since 2024-03-01.**
Status: **stands**
- URL: https://houmukyoku.moj.go.jp/homu/page7_000013.html (更新日 2024年4月1日)
- Quote: 「…その一覧図に認証文を付した写しを無料で交付するというものです（平成２９年５月創設）。」
- URL: https://www.moj.go.jp/MINJI/minji04_00082.html (令和7年3月21日)
- Quote: 「本籍地以外の市区町村の窓口でも、戸籍証明書・除籍証明書を請求できるようになりました（広域交付）。」 The same page says requests must be made in person: 「郵送や代理人による請求はできません。」
- The court's 相続放棄 page accepts the 一覧図 subject to each court: 「戸籍等に代えて「法定相続情報一覧図の写し」を提出できる場合があります（申述される家庭裁判所へ確認してください。）。」

**Item 16. 所有不動産記録証明制度 began on 2026-02-02. A written request costs 1,600 yen per search condition per copy.**
Status: **stands**
- URL: https://www.moj.go.jp/MINJI/minji05_00599.html: 「所有不動産記録証明制度（令和８年２月２日施行）」
- URL: https://www.moj.go.jp/MINJI/minji05_00740.html (no page date)
- Quote: 「検索条件１件につき、１通当たり」「書面請求（収入印紙で納付）」「１，６００円」
- Quote (limit): 「…所有権の登記名義人として検索条件と異なる氏名・住所等で記録されている不動産はリスト化されません。」

**Item 17. Pension: the death report is usually not needed if the My Number is on file. 未支給年金 has a 5-year limit.**
Status: **stands**
- URL: https://www.nenkin.go.jp/faq/jukyu/jukyushatodoke/kyotsu/shibo/20140421.html (更新日 2025年11月4日)
- Quote: 「年金受給権者の死亡届は日本年金機構にマイナンバーが収録されている方につきましては、原則不要です。ただし、未支給年金の届出などは必要です。」 / 「死亡届が必要な場合は、10日（国民年金は14日）以内に…」
- URL: https://www.nenkin.go.jp/service/jukyu/tetsuduki/kyotsu/jukyu/20140731-01.html (更新日 2026年4月1日)
- Quote: 「…生計を同じくしていた、（1）配偶者 （2）子 （3）父母…」 / 「…その支給金を含む一時所得の金額の合計額が50万円以下である場合には、確定申告は不要です。」
- URL: https://www.nenkin.go.jp/shinsei/jukyu/kyotsu/20140731-02.files/514.pdf
- Quote: 「○未支給年金を受ける権利は、５年（未支払給付金は２年）を経過したときは時効によって消滅します。」

**Item 18. The mother gets no 遺族基礎年金, because both children are adults. 遺族厚生年金 depends on the father's record.**
Status: **stands**
- URL: https://www.nenkin.go.jp/service/jukyu/seido/izokunenkin/jukyu-yoken/20150401-04.html (更新日 2026年6月22日)
- Quote: 「子のある配偶者」「子」 / 「子とは18歳になった年度の3月31日までにある方、または20歳未満で障害年金の障害等級1級または2級の状態にある方をさします。」
- URL: https://www.nenkin.go.jp/service/yougo/kagyo/kafunenkin.html (更新日 2021年4月1日)
- Quote: 「ただし、死亡した夫が、老齢基礎年金・障害基礎年金の支給を受けていた場合は、支給されません。」 The page also excludes a wife who already takes her 老齢基礎年金 early (繰上げ).
- Newer rule: https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000147284_00020.html (MHLW, updated 令和7年6月30日): 「法律では、遺族厚生年金の見直しは2028年４月施行予定です。」 It does not apply to a death in 2026.

**Item 19. 葬祭費 (国保 or 後期高齢者医療): 50,000 yen, with a 2-year limit.**
Status: **stands**. The 松本市 後期高齢者 figure is still an inference, as the source says.
- URL: https://www.city.matsumoto.nagano.jp/site/kokuho/1850.html (更新日 2026年6月1日)
- Quote: 「国保の加入者が死亡したとき、その葬祭を行った人に、申請により50，000円の葬祭費が支給されます。」
- URL: https://www.city.nagano.nagano.jp/n104500/contents/p000337.html (長野市, 更新日 2025年12月15日)
- Quote: 「後期高齢者医療保険の被保険者が死亡したとき、葬祭執行者に5万円が支給されます。」 / 「葬祭を行った日の翌日から2年を経過すると時効により支給できません。」
- Statutes: https://laws.e-gov.go.jp/api/1/articles;lawId=333AC0000000192;article=110 and https://laws.e-gov.go.jp/api/1/articles;lawId=357AC0000000080;article=160: 「…これらを行使することができる時から二年を経過したときは、時効によつて消滅する。」
- I searched for a 松本市 or 長野県後期高齢者医療広域連合 page on 葬祭費 and found none.

**Item 20. 世帯主変更届: 14 days (2026-07-24), already past, and not needed if the mother lives alone.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=342AC0000000081;article=25
- Quote: 「…その属する世帯又はその世帯主に変更があつた者（政令で定める者を除く。）は、その変更があつた日から十四日以内に、…市町村長に届け出なければならない。」
- URL: https://www.city.matsumoto.nagano.jp/site/benricho/3354.html (更新日 2026年1月9日)
- Quote: 「※旧世帯主の死亡・転出等により世帯に属する者が1人になった場合には、届出の必要はありません。」

**Item 21. With the title left in the father's name, 松本市 requires a 現所有者申告 within 3 months. That date has passed, so the family should file now.**
Status: **stands**, with one optional precision on the last day
- URL: https://www.city.matsumoto.nagano.jp/uploaded/life/195631_688051_misc.pdf (説明文, undated; linked from https://www.city.matsumoto.nagano.jp/soshiki/15/128666.html, 更新日 2026年2月16日)
- Quote: 「亡くなられた方が所有されていた土地 ・ 建物につき、 相続登記や未登記家屋の所有者変更届が提出されていない場合には、相続人等の現所有者が納税義務者となります。」
- Quote (松本市市税条例68条の3, printed on the sheet): 「現所有者(…)は、現所有者であることを知った日の翌日から 3 月を経過した日までに次に掲げる事項を記載した申告書を市長に提出しなければならない。」
- URL: https://www.city.matsumoto.nagano.jp/uploaded/life/195631_688058_misc.pdf (様式第5号)
- Quote (備考2): 「…賦課期日（１月１日）までに相続登記や未登記家屋の名義変更手続きが行われていない場合に、…３か月を経過する日までに申告していただくものです。」
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=325AC0000000226;article=384_3 (地方税法384条の3, current text). It matches the sheet.
- Precision (optional): 「3月を経過した日まで」 can be read as 2026-10-11 (Sun). 地方税法20条の5第2項 (article=20_5) moves a 条例 deadline that falls on a 休日 to the next day: 「…これらの日の翌日をその期限とみなす。」 With 10-12 a holiday, the latest reading is 2026-10-13. Every reading has passed by 2026-10-25, so "file now" stands.

## Side claims

**Item 22. 住所等変更登記 has been mandatory since 2026-04-01: within 2 years, with a 過料 of up to 50,000 yen.**
Status: **stands**, with one newer detail
- URL: https://www.moj.go.jp/MINJI/minji05_00688.html (スマート変更登記, 令和8年9月30日)
- Quote: 「令和８年４月１日から、不動産の所有者は、住所や氏名・名称の変更日から２年以内に変更登記をすることが義務付けられましたが、」
- Statutes: https://laws.e-gov.go.jp/api/1/articles;lawId=416AC0000000123;article=76_5 (「…その変更があった日から二年以内に…」) and article=164 第2項 (「…五万円以下の過料に処する。」)
- Newer detail, same page: 「令和８年１０月１３日以降にされた登記の申請又は嘱託の審査の過程において、…死亡し、又は失踪の宣告を受けたことを登記官が確認した場合にも、その方について、符号の表示を行うことがあります。」 This adds to the source's 令和8年12月下旬 date. It changes no duty.

**Item 23. 配偶者居住権 is obtained by a 分割 or a will. Asserting it requires a registration.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=1028: 「一　遺産の分割によって配偶者居住権を取得するものとされたとき。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=1031: 「居住建物の所有者は、配偶者（…）に対し、配偶者居住権の設定の登記を備えさせる義務を負う。」

**Item 24. 10-year rule for 分割: 2036-07-10.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=904_3
- Quote: 「前三条の規定は、相続開始の時から十年を経過した後にする遺産の分割については、適用しない。」 The ただし書 exceptions (a 家庭裁判所 request within the 10 years) explain the source's "generally".

**Item 25. Life insurance claims expire after 3 years (保険法95条).**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=420AC0000000056;article=95
- Quote: 「保険給付を請求する権利、…は、これらを行使することができる時から三年間行使しないときは、時効によって消滅する。」

## Facts for the key: overall verdict

- The premise is false and the correction stands: the duty applies since 2024-04-01, the deadline is 2029-07-10, and the 過料 is up to 100,000 yen at the court's discretion after a 催告.
- The cost figures stand: 40,000 yen tax, a 74,888 yen survey average, and no ≤1,000,000 yen exemption for this land.
- Every dated to-do item and every penalty line in the key matches the sources.
- Suggested additions (optional, none required):
  - Item 5: a 申告登記 does not cover a share received by a 分割 made before the 申出 (76条の3第2項).
  - Item 8: MOJ has asked to extend and widen the land exemption. This is pending, not law.
  - Item 11: fix the NTA page title.
  - Item 21: 2026-10-13 is the latest reading of the deadline.

## Not decided in this pass
- The 後期高齢者医療 葬祭費 amount specifically for 松本市 (no 松本市 or 広域連合 page found; 長野市's 50,000 yen is the nearest official figure).
- 遺族厚生年金, 死亡一時金 and 埋葬料 (被用者保険) details, the 戸籍 fees (450 / 750 yen), the time limit for a refund-only 準確定申告, and the 国税通則法 rounding rules. The source also left all of these unverified.
- Whether a late 現所有者申告 carries any penalty in 松本市.

## Addendum A1 (2026-10-26): rounding rules for the 登録免許税 (written by the key-fix step, not by the checker above)

Added on 2026-10-26 by the agent that revised the key after a reviewer's note. The key said 「端数処理（課税標準1,000円未満・税額100円未満の切捨て）は本件の数字に影響しない」 as fact, but the source (item 7) left these rules "not re-opened" and this check listed "the 国税通則法 rounding rules" under "Not decided in this pass". Every article below was read on 2026-10-26 through the e-Gov law API (current text) with curl. Quotes are verbatim, two lines at most. This addendum settles that one entry of "Not decided in this pass". The other entries stay open.

**A1. The 課税標準 of the 登録免許税 is rounded down to the 1,000 yen, and the tax to the 100 yen. Neither changes this case.**
Status: **confirmed**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=337AC0000000066;article=118 (国税通則法118条1項)
- Quote: 「国税（印紙税及び附帯税を除く。…）の課税標準…を計算する場合において、その額に千円未満の端数があるとき、又はその全額が千円未満であるときは、その端数金額又はその全額を切り捨てる。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=337AC0000000066;article=119 (国税通則法119条1項)
- Quote: 「国税（自動車重量税、印紙税及び附帯税を除く。…）の確定金額に百円未満の端数があるとき、又はその全額が百円未満であるときは、その端数金額又はその全額を切り捨てる。」
- The 登録免許税 is a 国税 and is not among the exclusions. URL: https://laws.e-gov.go.jp/api/1/articles;lawId=337AC0000000066;article=2 (2条1号). Quote: 「国が課する税のうち関税、とん税、特別とん税、森林環境税及び特別法人事業税以外のものをいう。」
- The 1-yen exceptions in 118条2項・119条2項 cover only withheld income tax. URL: https://laws.e-gov.go.jp/api/1/articles;lawId=337CO0000000135;article=40 (国税通則法施行令40条). Quote (1項): 「法第百十八条第二項（課税標準の端数計算の特例）に規定する政令で定める国税は、所得税法第四編第一章から第五章まで（源泉徴収）…の規定により徴収する所得税とする。」 2項 adds only 1項's tax and 所得税法190条・192条 withholding.
- 登録免許税法15条 sets only a floor. URL: https://laws.e-gov.go.jp/api/1/articles;lawId=342AC0000000035;article=15. Quote: 「別表第一に掲げる登記又は登録に係る課税標準の金額を計算する場合において、その全額が千円に満たないときは、これを千円とする。」
- NTA No.7191 (https://www.nta.go.jp/taxes/shiraberu/taxanswer/inshi/7191.htm, [令和8年4月1日現在法令等]), opened again on 2026-10-26, does not mention rounding.
- Recomputed: the bases 8,000,000 and 2,000,000 (together 10,000,000) are multiples of 1,000. The taxes 32,000, 8,000 and 40,000 are multiples of 100. Rounding changes nothing, whether the land and building are computed one by one or together.
