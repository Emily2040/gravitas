# ja-inheritance-registration: source check (2026-10-25)

Request being keyed: the father died on 2026-07-10. The heirs are the mother and two adult children (the writer and a younger brother). The estate is the family home in 松本市, 長野県, in the father's name (固定資産税評価額: land 8,000,000 yen, building 2,000,000 yen), plus deposits of about 12,000,000 yen. The mother keeps living in the house. An uncle who used to be an estate agent said 「相続登記は義務じゃないから、売るときにやればいい。登録免許税と司法書士代で何十万もかかるだけ」, so the family has decided to leave the title in the father's name. The writer asks for a dated to-do list of inheritance procedures **other than registration**, for the rest of this year and next year.

Every page below was opened on 2026-10-25 by direct download (curl) with local text extraction (HTML parser or pypdf). e-Gov articles were read through the e-Gov law API (`laws.e-gov.go.jp/api/1/articles`), which serves the current text. Quotes are copied from that text, two lines at most. "Source date" is the date printed on the page or document. NTA Tax Answer pages are marked 「[令和8年4月1日現在法令等]」.

Assumption used for every date below: the heirs learned of the death, and that the house was the father's, on the day of death (2026-07-10, a Friday). The request implies this but does not say it.

---

## Item checks

### 1. Premise: 相続登記 is optional. Refuted: it has been a legal duty since 2024-04-01
- Verdict: **refuted** (the premise is false)
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (法務省「相続登記の申請義務化に関するQ＆A」, source date 令和7年3月27日; first posted 令和6年3月28日)
- Quote: 「相続人は、不動産（土地・建物）を相続で取得したことを知った日から３年以内に、相続登記をすることが法律上の義務になりました。」
- Quote (same page, A2): 「令和３年に法律が改正され、これまで任意だった相続登記が義務化されました。」 / A3: 「相続登記の義務化は、令和６年４月１日から始まりました。」
- URL: https://www.moj.go.jp/MINJI/minji05_00599.html (法務省「相続登記の申請義務化について」, source date 令和8年4月1日)
- Quote: 「…その不動産の所有権を取得したことを知った日から３年以内に相続登記の申請をすることが義務付けられました（不動産登記法第７６条の２第１項）。」
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=416AC0000000123;article=76_2 (不動産登記法76条の2, current text)
- Quote: 「…自己のために相続の開始があったことを知り、かつ、当該所有権を取得したことを知った日から三年以内に、所有権の移転の登記を申請しなければならない。」
- Note: the uncle's "売るときにやればいい" is also wrong on its own terms. A sale needs a full 相続登記 anyway (item 5), and the duty runs from the death, not from a sale.

### 2. Deadline for this family: 2029-07-10. The 2027-03-31 date does not apply
- Verdict: **confirmed** (date worked out from the rule)
- Sources: item 1 (3 years from the day the heir knew). MOJ Q&A A4 gives the separate date for older inheritances: 「令和６年４月１日より前に相続したことを知った不動産で、相続登記がされていないものについては、令和９年３月３１日までに相続登記をする必要があります。」
- Arithmetic: knew on 2026-07-10. Under 民法140条 the first day is not counted, so the period starts 2026-07-11 and three years end on **2029-07-10 (Tue)**.
- Common wrong value: 「2027年3月31日まで」. That date applies only to inheritances the heir learned of before 2024-04-01. This death is in 2026, so the date is wrong here.
- Note: the key should accept 「2029年7月ごろまで」 or 「3年以内（2029年7月10日）」.

### 3. Extra duty after an 遺産分割: register the result within 3 years of the 分割
- Verdict: **confirmed**, with a timing nuance
- URL: https://www.moj.go.jp/MINJI/minji05_00599.html (令和8年4月1日)
- Quote: 「遺産分割が成立した日から３年以内にその内容を踏まえた所有権の移転の登記を申請することが義務付けられました（不動産登記法第７６条の２第２項、第７６条の３第４項等）。」
- Statute: 不動産登記法76条の2第2項 and 76条の3第4項 (e-Gov, same law ID, articles 76_2 and 76_3). 76条の3第4項: 「…その後の遺産の分割によって所有権を取得したとき（…）は、当該遺産の分割の日から三年以内に、所有権の移転の登記を申請しなければならない。」
- URL: https://www.moj.go.jp/content/001404761.pdf (MOJ flowchart, page for 令和６年４月１日以降に相続開始; linked from the Q&A page)
- Quote: when heirs have agreed a 分割, 「遺産分割の結果に基づく相続登記」「※不動産の相続を知った日から３年以内」. After a 相続人申告登記, a later 分割 brings 「※遺産分割の日から３年以内」.
- Nuance: the "3 years from the 分割" clock is the **additional** duty that follows a timely 相続人申告登記 or a 法定相続分 registration. A 分割 agreed before 2029-07-10 does not push the basic deadline back. MOJ 通達 (令和5年9月12日 法務省民二第927号, https://www.moj.go.jp/content/001408564.pdf) also describes the 分割-acquired share as running 「当該遺産の分割の日から３年以内」. A key should accept either "by 2029-07-10" or "within 3 years of a later 分割", and should not penalise an answer for leaving this fine point out.

### 4. Sanction: 過料 up to 100,000 yen, only without a 正当な理由, and only after a 催告
- Verdict: **confirmed**. The amount is set by the court and is **not fixed**.
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=416AC0000000123;article=164 (不動産登記法164条1項)
- Quote: 「…第七十六条の二第一項若しくは第二項又は第七十六条の三第四項の規定による申請をすべき義務がある者が正当な理由がないのにその申請を怠ったときは、十万円以下の過料に処する。」
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (Q&A 3-A2, 3-A4)
- Quote: 「(1) 登記官が、義務違反を把握した場合、義務違反者に登記をするよう催告します（催告書を送付します。）。」 / 「過料は、１０万円以下の範囲内で裁判所において決定されます。」
- Same page (A1): 「正当な理由がないのに相続登記をしない場合、１０万円以下の過料が科される可能性があります。」
- Same page (3-A3): the 登記官 only sends a 催告 when it learns of a breach in one of two ways, both involving another registration that reveals unregistered property. 3-A5 lists what counts as 正当な理由: very many heirs, a dispute, serious illness, DV evacuation, or being unable to afford the cost.
- Wrong values: 「必ず10万円の過料」 or 「罰金」. It is a 過料 (an administrative fine, not a criminal 罰金), up to 100,000 yen, at the court's discretion.

### 5. 相続人申告登記: a simpler way to meet the basic duty. It is not a full substitute
- Verdict: **confirmed**
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (Q&A 4-A1)
- Quote: 「…遺産分割がされた後にこれに基づく登記をする義務を相続人申告登記によって履行することはできないことや、」「…相続した不動産を売却したり、抵当権の設定をしたりするような場合には相続登記をする必要があることに留意が必要です。」
- URL: https://www.moj.go.jp/MINJI/minji05_00602.html (「相続人申告登記について」, source date 令和8年3月24日)
- Quote: 「〇 不動産についての権利関係を公示するものではないため、相続した不動産を売却したり、抵当権の設定をしたりするような場合には、別途、相続登記の申請をする必要がある」
- Same page, features: 「○ 特定の相続人が単独で申出可（他の相続人の分も含めた代理申出も可）」「○ 登録免許税がかからない」「○ 法定相続人の範囲・法定相続分の割合の確定が不要（提出書類も少ない）」
- Statute: 不動産登記法76条の3第2項: 「前条第一項に規定する期間内に前項の規定による申出をした者は、…所有権の移転の登記を申請する義務を履行したものとみなす。」
- MOJ Q&A 4-A4: it counts only for the heir who files: 「相続人申告登記は、申出をした相続人についてのみ、相続登記の義務を履行したものとみなされます。」 Several heirs can file together on one form.
- Wrong claims: 「申告登記をすれば売却できる」 and 「申告登記をすれば分割後も登記不要」 are both wrong.

### 6. Until a 分割, all three heirs co-own the house and all three carry the duty
- Verdict: **confirmed**
- URL: https://www.moj.go.jp/MINJI/minji05_00565.html (Q&A 2-A4)
- Quote: 「遺産分割をしていない場合には、全ての相続人が法定相続分の割合で不動産を取得（共有）した状態となるので、あなたも不動産を相続で取得したことになるためです。」
- Same answer: 「遺産分割が調い、その不動産の所有者があなた以外の者となった場合には、あなたの義務はなくなります。」
- Shares: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=900 (民法900条一号, 四号): 「子及び配偶者が相続人であるときは、子の相続分及び配偶者の相続分は、各二分の一とする。」 With two children: mother 1/2, each child 1/4.

### 7. 登録免許税: 0.4% of the 固定資産税評価額, about 40,000 yen here
- Verdict: **confirmed** (the uncle's "何十万" is an exaggeration)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/inshi/7191.htm (No.7191 登録免許税の税額表, 令和8年4月1日現在法令等)
- Quote (land table): 「相続、法人の合併または共有物の分割」「不動産の価額（注）」「1,000分の4」. Building table: 「相続または法人の合併による所有権の移転」「1,000分の4」.
- Quote (note): 「課税標準となる「不動産の価額」は、市町村役場で管理している固定資産課税台帳に登録された価格がある場合は、原則その価格です。」
- Arithmetic: land 8,000,000 × 4/1000 = 32,000. Building 2,000,000 × 4/1000 = 8,000. Total **40,000 yen**. (The base is rounded down to the nearest 1,000 yen and the tax to the nearest 100 yen under 国税通則法118条・119条. The round figures here are unaffected. Rounding rules not re-opened in this pass.)
- Common wrong value: 2% (1,000分の20), the rate for 売買 or 贈与. That would give 200,000 yen.

### 8. The 免税 for land worth 1,000,000 yen or less (until 2027-03-31) does not apply here
- Verdict: **confirmed** (the exemption exists; it does not cover this land)
- URL: https://houmukyoku.moj.go.jp/homu/page7_000017.html (法務局「相続登記の登録免許税の免税措置について」, 更新日 2026年4月1日)
- Quote: 「…免税措置の適用期限が令和９年（2027年）３月３１日までに延長されるとともに、…不動産の価額が１００万円以下の土地であれば、この免税措置が適用されることになりました。」
- Same page, for co-owned shares: 「※１不動産の所有権の持分の取得に係るものである場合は、当該不動産全体の価額に持分の割合を乗じて計算した額が不動産の価額となります。」
- NTA No.7191 (as item 7) states the same: 「…登録免許税の課税標準となる不動産の価額が100万円以下であるときは、…登録免許税は課されません。」 The legal basis is 租税特別措置法84条の2の2 (the 法務局 page quotes 「租税特別措置法第８４条の２の２第２項により非課税」).
- Here: land is 8,000,000 yen. Even split by 法定相続分, each share is 4,000,000 or 2,000,000 yen. All are over 1,000,000. The building is never covered (land only). The other exemption (an heir who died before registering) does not apply either.
- Wrong claim: 「年度内（2027年3月）に登記すれば免税」.

### 9. 司法書士 fees: set freely. The national survey average for this exact case is about 75,000 yen
- Verdict: **varies** (fees are not regulated). The survey figure is **confirmed**.
- URL: https://www.shiho-shoshi.or.jp/about/remuneration/ (日本司法書士会連合会「司法書士の報酬」)
- Quote: 「司法書士が業務を行ったときに受ける報酬については、各司法書士が自由に定めることになっています。」
- URL: https://www.shiho-shoshi.or.jp/cms/wp-content/uploads/2024/11/2a2e2c594bc4cd9ff2ca0f6d916db85e.pdf (報酬アンケート結果, 令和6年3月実施; all figures include 10% consumption tax)
- Quote: 「相続を原因とする土地１筆及び建物１棟（固定資産評価額の合計１０００万円）の所有権移転登記手続」「※法定相続人は３名で、うち１名が単独相続した場合」「【有効回答数:1109 ／ 平均:74,888円】」
- This survey case is almost exactly the request: 10,000,000 yen in total, three heirs, one heir takes the property.
- Arithmetic: 40,000 (tax) + 74,888 (average fee) ≈ **115,000 yen**, plus 戸籍 fees. If the family registers on its own, it pays only the 40,000 yen tax plus 戸籍 fees. Either way, "何十万も" is overstated. The fee depends on the firm and the number of heirs and properties.
- 日司連 is the national professional body, not a government agency. It is the only source in this check that publishes fee data.

### 10. 相続放棄 / 限定承認: 3 months from knowing, so the deadline passed around 2026-10-10
- Verdict: **confirmed** (the deadline is already past on 2026-10-25)
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=915 (民法915条1項)
- Quote: 「相続人は、自己のために相続の開始があったことを知った時から三箇月以内に、相続について、単純若しくは限定の承認又は放棄をしなければならない。」
- URL: https://www.courts.go.jp/saiban/syurui/syurui_kazi/kazi_06_13/index.html (裁判所「相続の放棄の申述」; no page date shown)
- Quote: 「申述は，民法により自己のために相続の開始があったことを知ったときから3か月以内にしなければならないと定められています。」 Filing goes to 「被相続人の最後の住所地の家庭裁判所」, fee 「収入印紙800円分（申述人1人につき）」.
- Effect of the deadline passing: 民法921条二号 (e-Gov, article 921): 「相続人が第九百十五条第一項の期間内に限定承認又は相続の放棄をしなかったとき。」 In that case the heir is deemed to have accepted (単純承認).
- Arithmetic: the period starts 2026-07-11, so three months end on **2026-10-10 (Sat)**. 2026-10-12 is スポーツの日 (祝日法: 「十月の第二月曜日」). If 民法142条 extends a deadline that falls on a closed day, the latest date would be 2026-10-13 (Tue). **Either way it has passed.** An extension request (期間伸長) also had to be filed within the period.
- Wrong claim: 「相続放棄は10月10日まで（まだ間に合う）」 or putting it on a to-do list from today. Mentioning that it has passed, or that debts would now pass to the heirs, is correct. Courts' handling of debts found later was **not verified** in this pass.

### 11. 準確定申告: due **2026-11-10**, and only if the father had to file
- Verdict: **confirmed**. Whether it is needed **varies** with the father's income, which the request does not give.
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2022.htm (No.2022 確定申告を要する人が死亡したとき（準確定申告）, 令和8年4月1日現在法令等)
- Quote: 「…相続の開始があったことを知った日の翌日から4か月以内に申告と納税をしなければなりません。これを準確定申告といいます。」
- Same page: 「各相続人等が連署により準確定申告書を提出することになります。」 A 付表 is attached. It goes to the tax office for the father's last address.
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=340AC0000000033;article=125 (所得税法125条1項). The duty exists only 「…第百二十条第一項（確定所得申告）の規定による申告書を提出しなければならない場合に該当するときは」. The deadline is 「その相続の開始があつたことを知つた日の翌日から四月を経過した日の前日」.
- Exemption for pensioners: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1600.htm (No.1600, 令和8年4月1日現在法令等)
- Quote: 「その年中の公的年金等の収入金額が400万円以下であり、かつ、その年分の公的年金等に係る雑所得以外の所得金額が20万円以下である場合には確定申告の必要はありません。」 Statute: 所得税法121条3項 (e-Gov, article 121).
- Salaried exemption (only if the father was still employed): 所得税法121条1項一号: one employer, 年末調整 done, other income 「二十万円以下」.
- Arithmetic: the day after knowing is 2026-07-11. Four months on is 2026-11-11, and the day before that is **2026-11-10 (Tue)**: 16 days after 2026-10-25.
- A refund-only 準確定申告 (for example for medical costs the father paid) is allowed under 所得税法125条2項, even when filing is not required. The time limit for it was **not verified** in this pass.
- Pension 源泉徴収票: https://www.nenkin.go.jp/section/faq/jukyu/uketori/tsuchisho/gensen/junkaku.html (更新日 2025年1月14日): 「準確定申告用源泉徴収票は、死亡届や未支給年金の手続き後、おおむね2～3カ月で発送されます。」
- Wrong values: 「2027年3月15日まで」 or 「10か月以内」. Saying 「準確定申告は必ず必要」 without a condition is also wrong.

### 12. 相続税: no tax and no return here. The 基礎控除 is 48,000,000 yen
- Verdict: **confirmed**
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4152.htm (No.4152, 令和8年4月1日現在法令等)
- Quote: 「課税価格の合計額 － 基礎控除額（3,000万円 ＋ 600万円 × 法定相続人の数）」
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4205.htm (No.4205, 令和8年4月1日現在法令等)
- Quote: 「その取得した財産の価額の合計額が遺産に係る基礎控除額の範囲内であれば申告も納税も必要ありません。」
- Same page, deadline if a return were needed: 「相続税の申告は、被相続人が死亡したことを知った日（通常の場合は、被相続人の死亡の日）の翌日から10か月以内に行うことになっています。」 If that day is a Saturday, Sunday or holiday, the next day counts. Statute: 相続税法27条1項 (e-Gov lawId 325AC0000000073, article 27).
- Valuation: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4602.htm (No.4602 土地家屋の評価, 令和8年4月1日現在法令等). Building: 「固定資産税評価額に1.0を乗じて計算した金額によって評価します。」 Land is valued by 路線価 or by 固定資産税評価額 × 倍率, so its 相続税 value **may differ** from 8,000,000 yen.
- Arithmetic: base deduction 30,000,000 + 6,000,000 × 3 = **48,000,000 yen**. The estate at the stated figures is 8,000,000 + 2,000,000 + 12,000,000 ≈ **22,000,000 yen**, which leaves 26,000,000 yen of headroom. Even if the land's 相続税 value were twice its 固定資産税評価額, the total would be about 30,000,000, still under the deduction. If a return were needed, the deadline would be **2027-05-10 (Mon)**.
- Wrong values: 「5,000万円＋1,000万円×人数」 (the rule before 2015, which gives 80,000,000). 「10か月以内に相続税申告が必要」 is wrong for this family.

### 13. 小規模宅地等の特例 and 配偶者の税額軽減 need a return. Neither matters here
- Verdict: **confirmed**
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4124.htm (No.4124, 令和8年4月1日現在法令等)
- Quote: 「この特例の適用を受けるためには、相続税の申告書に、この特例の適用を受けようとする旨を記載するとともに、…一定の書類を添付する必要があります。」 For a spouse who acquires the home, the table says 「「取得者ごとの要件」はありません。」 (limit 330㎡, 80% reduction).
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4158.htm (No.4158 配偶者の税額の軽減, 令和8年4月1日現在法令等): the spouse pays no tax up to 「（1） 1億6千万円」 or 「（2） 配偶者の法定相続分相当額」, whichever is larger. It is claimed on a return.
- NTA No.4205 (注2): whether a return is needed is judged **before** 小規模宅地等: 「…租税特別措置法第69条の4（小規模宅地等…の特例）…等を適用しない場合における課税価格の合計額をいいます。」
- Here the estate is under the deduction even without the reliefs, so no return is needed. An answer that says 「特例のために申告が必要」 for this family is wrong.

### 14. Bank deposits: banks freeze the accounts; each heir can withdraw a limited amount before the 分割 (up to 1,500,000 yen per bank)
- Verdict: **confirmed**
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=909_2 (民法909条の2)
- Quote: 「各共同相続人は、遺産に属する預貯金債権のうち相続開始の時の債権額の三分の一に第九百条及び第九百一条の規定により算定した当該共同相続人の相続分を乗じた額（…法務省令で定める額を限度とする。）については、単独でその権利を行使することができる。」
- Ordinance: https://laws.e-gov.go.jp/api/1/lawdata/430M60000010029 (平成三十年法務省令第二十九号): 「民法第九百九条の二に規定する法務省令で定める額は、百五十万円とする。」 The statute applies the cap 「預貯金債権の債務者ごとに」, i.e. per bank.
- Same article: money withdrawn counts as part of that heir's share (「…遺産の一部の分割によりこれを取得したものとみなす。」).
- Arithmetic (if all 12,000,000 yen is in one bank): mother 12,000,000 × 1/3 × 1/2 = 2,000,000, capped at **1,500,000**. Each child 12,000,000 × 1/3 × 1/4 = **1,000,000**. If the money is spread over several banks, the formula and the cap apply to each bank separately.
- No legal deadline applies to closing the accounts. The documents each bank wants **vary by bank**.
- Wrong claim: 「預金の3分の1まで引き出せる」 (this misses the 法定相続分 multiplier and the per-bank cap).

### 15. 法定相続情報証明制度 is free, and it replaces the bundle of 戸籍 for most offices
- Verdict: **confirmed**
- URL: https://houmukyoku.moj.go.jp/homu/page7_000013.html (法務局「法定相続情報証明制度について」, 更新日 2024年4月1日)
- Quote: 「…一覧図の内容が民法に定められた相続関係と合致していることを登記官が確認した上で、その一覧図に認証文を付した写しを無料で交付するというものです（平成２９年５月創設）。」
- The 相続人申告登記 page (item 5) and the court's 相続放棄 page also accept the 一覧図 in place of 戸籍 (the court page says this varies by court).
- Related: since 2024-03-01, 戸籍 and 除籍 certificates can be requested at any 市区町村 (広域交付). URL: https://www.moj.go.jp/MINJI/minji04_00082.html (令和7年3月21日): 「本籍地以外の市区町村の窓口でも、戸籍証明書・除籍証明書を請求できるようになりました（広域交付）。」 The fees (450 / 750 yen) were **not verified** in this pass.

### 16. 所有不動産記録証明制度 started on 2026-02-02
- Verdict: **confirmed**
- URL: https://www.moj.go.jp/MINJI/minji05_00599.html (令和8年4月1日): 「所有不動産記録証明制度（令和８年２月２日施行）」. It lists every property registered in the deceased's name (不動産登記法119条の2).
- URL: https://www.moj.go.jp/MINJI/minji05_00740.html (no page date shown; the related ordinance and 通達 are dated 令和8年2月2日)
- Quote (fee): 「検索条件１件につき、１通当たり」「書面請求（収入印紙で納付）」「１，６００円」
- Same page, limit: properties recorded under a different name or address 「…リスト化されません。」
- Use here: it can confirm whether the father owned other land, for example inherited farmland or forest.

### 17. Pension: the death report is usually not needed if the My Number is on file. 未支給年金 can be claimed for 5 years
- Verdict: **confirmed**
- URL: https://www.nenkin.go.jp/faq/jukyu/jukyushatodoke/kyotsu/shibo/20140421.html (更新日 2025年11月4日)
- Quote: 「年金受給権者の死亡届は日本年金機構にマイナンバーが収録されている方につきましては、原則不要です。ただし、未支給年金の届出などは必要です。」 / 「死亡届が必要な場合は、10日（国民年金は14日）以内に…」
- URL: https://www.nenkin.go.jp/service/jukyu/tetsuduki/kyotsu/jukyu/20140731-01.html (更新日 2026年4月1日): 未支給年金 goes to the family member who shared a household (生計を同じくしていた) with the deceased, spouse first. Same page: it is 一時所得 for the recipient; no return is needed if total 一時所得 is 500,000 yen or less in that year.
- URL: https://www.nenkin.go.jp/shinsei/jukyu/kyotsu/20140731-02.files/514.pdf (claim form 年金受給権者死亡届（報告書）兼 未支給年金・未支払給付金請求書)
- Quote: 「○ 未支給年金を受ける権利は、５年（未支払給付金は２年）を経過したときは時効によって消滅します。」
- Arithmetic: the 10-day / 14-day death-report deadline (2026-07-20 / 2026-07-24) has passed if a report was needed. The 未支給年金 claim is still open.

### 18. 遺族年金: the mother cannot get 遺族基礎年金, because both children are adults. 遺族厚生年金 depends on the father's record
- Verdict: **confirmed** for 遺族基礎年金. **Varies / not verified in detail** for 遺族厚生年金 and 寡婦年金.
- URL: https://www.nenkin.go.jp/service/jukyu/seido/izokunenkin/jukyu-yoken/20150401-04.html (遺族基礎年金, 更新日 2026年6月22日)
- Quote: 「死亡した方に生計を維持されていた以下の遺族が受け取ることができます。」「子のある配偶者」「子」 / 「子とは18歳になった年度の3月31日までにある方、または20歳未満で障害年金の障害等級1級または2級の状態にある方をさします。」
- The writer and the brother are adult heirs, so the mother is not a 子のある配偶者. Unless a child qualifies under the disability rule, she gets **no 遺族基礎年金**.
- 寡婦年金: https://www.nenkin.go.jp/service/yougo/kagyo/kafunenkin.html (更新日 2021年4月1日). It is paid from age 60 to 65, only if the husband had 10 or more years of 第1号 contributions and was **not** receiving 老齢基礎年金. It is not paid if he was already a pensioner.
- 遺族厚生年金 (if the father had 厚生年金 coverage) and 死亡一時金: **not verified** in this pass (the 死亡一時金 page did not load).
- Wrong claim: 「母は遺族基礎年金を受け取れる」.

### 19. 葬祭費 (国保 or 後期高齢者医療): 50,000 yen, claimable for 2 years
- Verdict: **confirmed** (which scheme applies depends on the father's age and insurance, which the request does not give)
- URL: https://www.city.matsumoto.nagano.jp/site/kokuho/1850.html (松本市「国保で受けられる給付」, 更新日 2026年6月1日)
- Quote: 「国保の加入者が死亡したとき、その葬祭を行った人に、申請により50，000円の葬祭費が支給されます。」
- URL: https://www.city.nagano.nagano.jp/n104500/contents/p000337.html (長野市「後期高齢者医療（葬祭費）」, 更新日 2025年12月15日)
- Quote: 「後期高齢者医療保険の被保険者が死亡したとき、葬祭執行者に5万円が支給されます。」 The scheme is run county-wide by the 長野県後期高齢者医療広域連合, so the same 50,000 yen should apply in 松本市. That is an inference: no 松本市 page for this was opened.
- Time limit: 国民健康保険法110条1項 (https://laws.e-gov.go.jp/api/1/articles;lawId=333AC0000000192;article=110): 「…保険給付を受ける権利は、これらを行使することができる時から二年を経過したときは、時効によつて消滅する。」 The same wording is in 高齢者の医療の確保に関する法律160条 (lawId 357AC0000000080).
- Arithmetic: 2 years from when the claim could first be made (normally the day after the funeral), so about **July 2028**. The funeral date is not given.
- If the father was in an employer's health insurance (被用者保険), the 埋葬料 applies instead. **Not verified** in this pass.

### 20. 世帯主変更届: 14 days, so long past, and not needed if the mother lives alone
- Verdict: **confirmed**. Whether it is needed **varies** with who lives in the house.
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=342AC0000000081;article=25 (住民基本台帳法25条)
- Quote: 「…その属する世帯又はその世帯主に変更があつた者（政令で定める者を除く。）は、その変更があつた日から十四日以内に、…市町村長に届け出なければならない。」
- URL: https://www.city.matsumoto.nagano.jp/site/benricho/3354.html (松本市「世帯変更届」, 更新日 2026年1月9日)
- Quote: 「※旧世帯主の死亡・転出等により世帯に属する者が1人になった場合には、届出の必要はありません。」
- Arithmetic: 2026-07-10 + 14 days = **2026-07-24**, already past. If the mother now lives alone in the house, no report is needed. The request suggests she does but does not say so.

### 21. Because the title stays in the father's name, 松本市 requires a 現所有者申告 for 固定資産税, due within 3 months, which has already passed
- Verdict: **confirmed** (and directly caused by the family's decision)
- URL: https://www.city.matsumoto.nagano.jp/uploaded/life/195631_688051_misc.pdf (松本市「固定資産に関する現所有者の申告について（説明文）」; undated, linked from https://www.city.matsumoto.nagano.jp/soshiki/15/128666.html, 更新日 2026年2月16日)
- Quote: 「亡くなられた方が所有されていた土地 ・ 建物につき、 相続登記や未登記家屋の所有者変更届が提出されていない場合には、相続人等の現所有者が納税義務者となります。」
- Quote (松本市市税条例68条の3, printed on the same sheet): 「現所有者(…)は、現所有者であることを知った日の翌日から 3 月を経過した日までに次に掲げる事項を記載した申告書を市長に提出しなければならない。」 Legal basis: 地方税法384条の3.
- Form: https://www.city.matsumoto.nagano.jp/uploaded/life/195631_688058_misc.pdf (相続人代表者指定(変更)届出兼固定資産現所有者申告書). Its notes say the 申告 is for when 相続登記 has not been done by the 賦課期日 (1 January): 「…賦課期日（１月１日）までに相続登記や未登記家屋の名義変更手続きが行われていない場合に、…３か月を経過する日までに申告していただくものです。」 The same form also names the heir who receives the city's tax notices.
- Arithmetic: the period starts 2026-07-11, so three months run to 2026-10-10 or 2026-10-11 (Sun; 2026-10-12 is a holiday). **Already past**: the family should file now. No penalty for filing late was checked in this pass.
- Note: this is a dated, family-specific item that a good list would include. An answer that leaves it out is incomplete, not wrong.

### 22. 住所等変更登記 has been mandatory since 2026-04-01 (2 years, 過料 up to 50,000 yen)
- Verdict: **confirmed** (a side point: it does not apply to the deceased father, but it applies to whichever heir becomes the registered owner)
- URL: https://www.moj.go.jp/MINJI/minji05_00688.html (法務省 スマート変更登記, source date 令和8年9月30日)
- Quote: 「令和８年４月１日から、不動産の所有者は、住所や氏名・名称の変更日から２年以内に変更登記をすることが義務付けられましたが、」
- Statute: 不動産登記法164条2項: 「第七十六条の五の規定による申請をすべき義務がある者が正当な理由がないのにその申請を怠ったときは、五万円以下の過料に処する。」
- Same MOJ page: from 令和8年12月下旬, the registry may mark a registered owner's death with a symbol (符号の表示) when the 法務局 learns of it.

### 23. 配偶者居住権: a right the mother can get by 分割 or will. Asserting it against others requires another registration
- Verdict: **confirmed**
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=1028 (民法1028条一号): 「遺産の分割によって配偶者居住権を取得するものとされたとき。」
- Statute: 民法1031条1項 (article 1031): 「居住建物の所有者は、配偶者（…）に対し、配偶者居住権の設定の登記を備えさせる義務を負う。」
- Note: an answer that suggests 配偶者居住権 as a way to protect the mother is fine. It needs a 分割 and a registration, so it does not fit "leave the title alone".

### 24. The 10-year rule for 遺産分割
- Verdict: **confirmed** (side point)
- Statute: 民法904条の3 (article 904_3): 「前三条の規定は、相続開始の時から十年を経過した後にする遺産の分割については、適用しない。」
- Arithmetic: 10 years from 2026-07-10 is **2036-07-10**. After that, 特別受益 and 寄与分 are generally no longer taken into account. There is no deadline to agree a 分割 as such.

### 25. Life insurance claims: 3 years (only if the father had a policy, which the request does not say)
- Verdict: **confirmed** (side point; the policy terms **vary**)
- Statute: https://laws.e-gov.go.jp/api/1/articles;lawId=420AC0000000056;article=95 (保険法95条1項): 「保険給付を請求する権利、…は、これらを行使することができる時から三年間行使しないときは、時効によって消滅する。」

---

## Dates worked out (knowledge date 2026-07-10, today 2026-10-25)

| Item | Rule | Date | Status on 2026-10-25 |
|---|---|---|---|
| 世帯主変更届 (only if 2 or more people remain) | 14 days (住基法25条) | 2026-07-24 | past |
| 年金受給権者死亡届 (only if no My Number on file) | 10 days / 14 days | 2026-07-20 / 2026-07-24 | past |
| 相続放棄・限定承認 | 3 months (民法915条) | 2026-10-10 (Sat); 10-13 at the latest if extended | past |
| 固定資産 現所有者申告 (松本市) | 3 months (市税条例68条の3) | about 2026-10-10 to 10-11 | past: file now |
| 準確定申告 (only if the father had to file) | 4 months (所得税法125条) | 2026-11-10 (Tue) | 16 days left |
| Land ≤1,000,000 yen exemption | until 2027-03-31 | 2027-03-31 | does not apply (land 8,000,000) |
| 相続税 return (not needed here) | 10 months (相続税法27条) | 2027-05-10 (Mon) | not needed |
| 葬祭費 | 2 years (国保法110条 / 高確法160条) | about July 2028 (from the day after the funeral) | open |
| 相続登記 or 相続人申告登記 | 3 years (不登法76条の2) | 2029-07-10 (Tue) | open (legal duty) |
| Registration after a later 分割 | 3 years from the 分割 | depends on the 分割 date | — |
| 未支給年金 | 5 years | about 2031 | open |
| 10-year rule for 分割 | 民法904条の3 | 2036-07-10 | — |

Registration cost: land 8,000,000 × 0.4% = 32,000. Building 2,000,000 × 0.4% = 8,000. Total 40,000 yen. Adding the 2024 survey's average 司法書士 fee of 74,888 yen gives about 115,000 yen, plus 戸籍 fees. 相続人申告登記: no 登録免許税.

Pre-分割 withdrawal (one bank, 12,000,000 yen): mother min(12,000,000 × 1/3 × 1/2 = 2,000,000, 1,500,000) = 1,500,000. Each child 12,000,000 × 1/3 × 1/4 = 1,000,000.

相続税: 30,000,000 + 6,000,000 × 3 = 48,000,000 base deduction. The estate is about 22,000,000, so there is no tax and no return.

---

## Facts for the key

**前提とその誤り**
- 「相続登記は義務じゃない」は誤りです。
  - 2024年4月1日から相続登記は法律上の義務です（不動産登記法76条の2）。
  - 期限は、相続で不動産を取得したことを知った日から3年以内です。
  - この家族は2026年7月10日に知ったので、**2029年7月10日**まで（「2029年7月ごろまで」でも可）。
- 「2027年3月31日まで」は、2024年4月より前に相続を知った場合の期限で、この家族には当てはまりません。
- 正当な理由なく申請しないと、10万円以下の過料の対象になります（同法164条1項）。
  - 過料は裁判所が決めるもので、必ず科されるわけでも、金額が決まっているわけでもありません。
  - 登記官からの催告が先にあります（法務省Q&A）。
  - 「必ず10万円」「罰金」と断定するのは誤りです。
- 遺産分割をした場合は、相続人申告登記などの後に分割したときに、分割の日から3年以内に分割内容どおりの登記が必要です（76条の2第2項・76条の3第4項）。
- 分割前は、母・私・弟の3人が法定相続分（母1/2、子各1/4）で共有しており、3人とも義務を負います。
- 「売るときにやればいい」も誤りです。義務は売却と関係なく、亡くなった時から進みます。売却には結局、正式な相続登記が必要です。

**叔父の費用の話**
- 登録免許税は固定資産税評価額の0.4%です（国税庁No.7191）。
  - 土地800万円×0.4%＝3万2,000円、建物200万円×0.4%＝8,000円で、合計**4万円**です。
  - 2%は売買・贈与の税率で、相続には使いません。
- 100万円以下の土地の免税措置（2027年3月31日まで）は、土地が800万円なので使えません。
- 司法書士報酬は自由に決められます。
  - 日司連の2024年3月アンケートでは、ちょうどこの条件（土地1筆・建物1棟、評価額合計1,000万円、相続人3人、1人が単独相続）の平均が74,888円（税込）でした。
  - 依頼しても合計約11〜12万円＋戸籍の実費です。自分で申請すれば4万円＋実費です。
  - 「何十万も」は過大です。

**簡易な方法：相続人申告登記**
- 期限内（3年以内）に法務局へ申し出れば、基本的な義務を果たしたとみなされます。
  - 相続人1人でも単独で申し出られ、登録免許税はかかりません。
- ただし、次のことは覚えておく必要があります。
  - 申し出た本人の義務しか果たしたことになりません。3人分は連名でまとめて申し出られます。
  - 遺産分割後の登記義務は、これでは果たせません。
  - 売却や抵当権設定には、正式な相続登記が別に必要です。
  - 「これで登記は済み」「売れる」とするのは誤りです。

**最良の回答**
- 冒頭で前提を訂正します（義務化、2029年7月10日、過料は最大10万円で裁判所の判断）。
- 費用は約4万円と示し、相続人申告登記という選択肢を伝えます。
- そのうえで、頼まれたとおり登記以外のTODOを日付つきで出します。

**期限つきTODOとして正しい内容（今日＝2026年10月25日）**
- **準確定申告：2026年11月10日（火）まで（あと16日）。** 父に申告義務があった場合だけ必要です。
  - 公的年金の収入が400万円以下で、それ以外の所得が20万円以下なら不要です（所得税法121条3項、国税庁No.1600）。
  - 給与所得者で年末調整済みなどの場合も不要になり得ます。
  - 相続人の連署で、付表を付けて出します。
  - 年金の準確定申告用源泉徴収票は、死亡届などの手続後おおむね2〜3か月で届きます。
- **固定資産の現所有者申告（松本市）：3か月以内（2026年10月10〜11日ごろ）で既に経過。すぐ提出します。**
  - 名義を父のままにするので、1月1日時点で登記がなければ必要です（地方税法384条の3、松本市市税条例68条の3）。
  - 様式は「相続人代表者指定(変更)届出兼固定資産現所有者申告書」です。
- **相続放棄・限定承認：3か月（2026年10月10日、延びても10月13日）で既に経過。** 今からのTODOには入りません。期限を過ぎたので単純承認とみなされます（民法921条2号）。
- **相続税：申告も納税も不要。**
  - 基礎控除は3,000万＋600万×3＝4,800万円で、遺産は約2,200万円です。
  - 土地の相続税評価は路線価・倍率方式なので固定資産税評価額とは違い得ますが、2倍でも基礎控除内です。
  - 申告が必要だったとしても期限は2027年5月10日（月）です。
  - 小規模宅地等の特例や配偶者の税額軽減のために申告が必要、とするのはこの家族には誤りです。
- **預金：** 口座は凍結されます。
  - 分割前でも、各相続人が「相続開始時の残高×1/3×法定相続分」まで、1つの銀行ごとに150万円を上限に単独で払い戻せます（民法909条の2、平成30年法務省令第29号）。
  - 1行に1,200万円なら、母は150万円（計算上200万円）、子は各100万円です。
  - 払い戻した分は遺産分割で取得したものとみなされます。必要書類は銀行ごとに違います。
- **年金：**
  - 日本年金機構にマイナンバーが登録されていれば、死亡届は原則不要です（必要な場合の期限10日・国民年金14日は既に経過）。
  - 未支給年金は、生計を同じくしていた遺族（配偶者が先順位）が請求します。時効は5年で、受け取った人の一時所得になります。
- **遺族年金：**
  - 遺族基礎年金は「子のある配偶者」か「子」（18歳到達年度末まで等）だけが対象です。成人した子しかいないので、母は**受けられません**。
  - 遺族厚生年金は父の加入歴によります（未確認）。
  - 寡婦年金は、夫が老齢基礎年金を受けていれば支給されません。
- **葬祭費：** 国保（松本市）または後期高齢者医療で5万円です。時効は2年（葬儀の翌日から、2028年7月ごろ）です。被用者保険なら埋葬料（未確認）。
- **世帯主変更届：** 14日以内（2026年7月24日）で、既に経過しています。母が1人で住んでいるなら不要です（松本市）。
- **便利な制度：**
  - 法定相続情報証明制度（無料）。
  - 戸籍の広域交付（2024年3月から）。
  - 所有不動産記録証明制度（2026年2月2日開始、書面請求は検索条件1件1通1,600円）。父名義のほかの不動産の確認に使えます。

**回答に付け加えられがちな点と正しい値**
- 相続人申告登記の期限は、相続登記と同じ3年以内です（2029年7月10日）。
- 配偶者居住権は、分割か遺言で取得でき、第三者に主張するには登記が必要です（民法1028条・1031条）。名義を父のままにする方針とは両立しません。
- 遺産分割そのものに期限はありません。ただし相続開始から10年（2036年7月10日）を過ぎると、特別受益・寄与分は原則考慮されません（民法904条の3）。
- 住所等変更登記は2026年4月1日から義務で、2年以内、過料は5万円以下です。父には関係しません。
- 生命保険金の請求は3年で時効です（保険法95条）。契約があるかは依頼文にありません。
- 過料が科されるのは、催告を受けても正当な理由なく申請しなかった場合だけです。費用を払えないことは正当な理由の例に入っていますが、この家族には当てはまりません。

**減点**
- 前提を認める（重大）。
  - 例：「任意なので売却時でよい」とする。
  - 例：登記に一切触れず、頼まれたTODOだけを出す。
- 期限を2027年3月31日とする。
- 過料を確定的な罰金とする。
- 相続人申告登記を完全な代わりとする（売却・分割後も不要とする）。
- 相続放棄をまだ間に合う期限として並べる。
- 準確定申告の期限を誤る、または無条件に必須とする。
- 相続税の申告が必要とする。
- 母が遺族基礎年金を受けられるとする。
- 登録免許税を2%で計算する、または100万円以下の免税を適用する。
- 長すぎる。
