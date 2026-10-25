# ja-wallpaper-restoration: adversarial check of "Facts for the key"

Checked 2026-10-22 against `ja-wallpaper-restoration.md`. No other file on disk was read.

Method: every URL below was opened on 2026-10-22. PDFs (MLIT guideline, MLIT 参考資料, MOJ pamphlet, Tokyo leaflet, court fee table) were streamed with curl and their text extracted with pypdf. e-Gov articles came from the e-Gov law API v1, and court pages were fetched as HTML. To look for newer rules I checked the MLIT guideline page, the CAA 消費者契約法 page (amendment list), the Tokyo 賃貸住宅の紛争防止 page, and the courts.go.jp 少額訴訟/民事訴訟/デジタル化 pages. WebSearch quota ran out after two searches, so the web-wide search for 2025-2026 changes is incomplete (see "Could not decide").

Summary: 25 facts. 24 stand (several with wording notes). 1 needs change (F23). None is factually refuted.

---

## 前提とその誤り

### F1. 「原状回復」は通常損耗・経年変化を含まない（民法621条）。2020年4月より前の契約でも結論は同じ — **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=621
- Quote: 「賃借人は、賃借物を受け取った後にこれに生じた損傷（通常の使用及び収益によって生じた賃借物の損耗並びに賃借物の経年変化を除く。…）」
- Pre-2020: https://www.moj.go.jp/content/001289628.pdf p.4: 「一般に，通常損耗…及び経年変化はその対象に含まれていないと解されています。」

### F2. 日照によるクロスの変色はガイドライン別表1で貸主負担。法務省パンフレットも日焼けクロスを例に挙げる — **stands (wording note)**
- URL: https://www.mlit.go.jp/common/001016469.pdf (別表1, PDF p.29; 事例区分 PDF p.24)
- Quote: 「●クロスの変色（日照などの自然現象によるもの）」「（考え方）畳等の変色と同様、日照は通常の生活で避けられないものであると考えられる。」
- MOJ: https://www.moj.go.jp/content/001289628.pdf p.4 事例3: 「日焼けしたクロスの張替費用を負担するように求められた。」
- Wording note: the pamphlet sets this case and answers it with the general rule (「通常損耗や経年変化については原状回復義務を負わないことを明記しました」). It does not itself list 日焼け among its examples or say 「借主は負担しない」 about the case in so many words. Safer wording: 「法務省のパンフレットも日焼けしたクロスの張替費用を事例に挙げ、通常損耗・経年変化には原状回復義務がないと説明している」.

### F3. 「原状回復」とだけ書いた条項では通常損耗特約は成立しない。最高裁平成17年12月16日（第二小法廷、平成16(受)1573）。ガイドラインの3要件 — **stands (wording note)**
- URL: https://www.courts.go.jp/hanrei/62594/detail2/index.html (事件番号「平成16(受)1573」, 「最高裁判所第二小法廷」, 「破棄差戻」)
- Quote (裁判要旨1): 「賃借人が補修費用を負担することになる上記損耗の範囲につき，賃貸借契約書自体に具体的に明記されているか，賃貸人が口頭により説明し，賃借人がその旨を明確に認識して，それを合意の内容としたものと認められるなど，その旨の特約が明確に合意されていることが必要である。」
- 3要件: https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf p.8: 「① 特約の必要性があり、かつ、暴利的でないなどの客観的、合理的理由が存在すること」 (②認識, ③意思表示 follow verbatim as in the key)
- Wording note: 「成立しない」 is too absolute on its own. The judgment leaves a second route open: specific oral explanation plus clear agreement. The tenant's account also comes second-hand from the management company, so the contract may contain a separate 特約 that names クロス. Suggested wording: 「契約書に『原状回復』とあるだけでは、通常損耗を借主負担とする特約が成立しているとはいえない（範囲が契約書に具体的に明記されているか、口頭で具体的に説明され明確に合意した場合は別。その場合も3要件と消費者契約法10条で有効性を争える）」.

### F4. 返信は了承せず、根拠と明細を求め、敷金返還を求める（国民生活センター 2026年2月17日） — **stands**
- URL: https://www.kokusen.go.jp/news/data/n-20260217_1.html (「［2026年2月17日:公表］賃貸住宅の原状回復トラブルにご注意！」)
- Quote: 「納得できない請求をされた場合は、貸主側に費用の明細等の説明を求め、費用負担について話し合いましょう。」

## 正しい数字と計算

### F5. 日焼けによる黄ばみ：借主負担0円（経年計算の前に義務がない） — **stands**
- URL: https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf p.3
- Quote: 「経年変化と通常損耗に対しては原状回復義務がありません（A）。」
- Recomputed: no duty means 0 yen. Depreciation is never reached.

### F6. 借主負担割合 = 1 − 経過年数÷6年（下限1円）。7年なら1円（≒0%） — **stands (precision note)**
- URL: https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf p.17
- Quote: 「退去時にはクロスの耐用年数６年を過ぎており、賃借人の負担割合は１円（≒０％）になります。」
- Recomputed: 1 − 7/6 = −0.1667, so the floor applies (residual value 1 yen). 120,000 × ≈0% ≈ 0 yen.
- Precision: the formula is the straight-line (定額法) case. The guideline allows 「直線（または曲線）」, and the 参考資料 graph is labelled 「定額法の場合」. At 7 years both give 1 yen. The "1円" is the residual value of the wallpaper, not 1 yen of the 120,000-yen bill.

### F7. 入居時に新品でなければ経過年数はさらに長く、結論は同じかより有利 — **stands**
- URL: https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf p.17
- Quote: 「入居時にクロスの経過年数が３年の場合、入居年数に３年を加えた年数が退去時の経過年数となります。」

### F8. 参考例：3年50%、4年33.3%、4年8か月約22%（1−56/72） — **stands**
- URL: https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf pp.17, 22
- Quote: 「３年後に退去する場合には、負担割合は50％まで低下」; 「４年８か月後に退去する場合には、負担割合は約 22％（1-（56/72））」; 「１－４/６＝１/３（33.3％）」
- Recomputed: 1−3/6 = 50.0%; 1−4/6 = 33.3%; 1−56/72 = 22.2%.

### F9. 例外：耐用年数を過ぎても、故意の落書きなどは工事費・人件費を請求されうる — **stands (note)**
- URL: https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf p.17
- Quote: 「賃借人の故意・過失による破損等が無ければ継続してクロスが使用可能な場合には、修繕等の工事に伴う負担が必要となることがあり得ます。」
- Note: the trigger is 故意・過失による破損等 generally; the 落書き is the source's example. It does not reach sunburn. Useful for the reply: the 2026-02-17 kokusen release reports a company that waived the wallpaper cost after 6 years but still billed 「工賃の2割の5万円」 for a sofa mark. The reply should therefore also refuse any 工賃 charged for normal wear.

### F10. 負担範囲：㎡単位、最大でも毀損箇所を含む一面分。部屋全体はグレードアップ。ヤニのみ例外 — **stands**
- URL: https://www.mlit.go.jp/common/001016469.pdf (PDF pp.18-19; 別表2)
- Quote: 「当該部屋全体のクロスの張替えを賃借人の義務とすると、原状回復以上の利益を賃貸人が得ることとなり、妥当ではない。」; 「喫煙等により当該居室全体においてクロス等がヤニで変色したり臭いが付着した場合のみ、当該居室全体のクリーニングまたは張替費用を賃借人負担とすることが妥当」

### F11. 敷金：10万円 − 0円 = 10万円全額返還が原則。差し引けるのは賃貸借に基づく金銭債務だけ（民法622条の2）。有効な特約は別 — **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=622_2
- Quote: 「その受け取った敷金の額から賃貸借に基づいて生じた賃借人の賃貸人に対する金銭の給付を目的とする債務の額を控除した残額を返還しなければならない。」
- Recomputed: 100,000 − 0 = 100,000 yen, assuming no unpaid rent, no tenant-caused damage and no valid fixed-fee clause.

### F12. 12万円は敷金10万円を2万円上回る。了承すれば敷金は戻らず、2万円の請求根拠を与えかねない — **stands**
- Arithmetic: 120,000 − 100,000 = 20,000 yen. No source needed. The "かねない" hedge is appropriate.

## 周辺の事実

### F13. 民法621条の施行日2020年4月1日。施行前の契約で合意更新がなければ旧法。結論は同じ — **stands**
- URL: https://www.moj.go.jp/content/001289628.pdf p.1, p.7
- Quote: 「2020 年４月１日から施行されます。」; 「施行日後に当事者が合意によって賃貸借契約や保証契約を更新したときは、…改正後の新しい民法が適用されます。」

### F14. 民法622条の2：返還債務は「賃貸借が終了し、かつ、賃貸物の返還を受けたとき」に生じ、「何日以内」の期限はない — **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=622_2
- Quote: 「一　賃貸借が終了し、かつ、賃貸物の返還を受けたとき。」 (The article contains no time limit.)

### F15. ガイドラインは再改訂版（平成23年8月）が現行、参考資料は令和5年3月、法的拘束力なし — **stands**
- URL: https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000020.html (lists only 「（再改訂版）」 and 「平成23年8月再改訂の概要」; no 令和 revision); https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf p.1 「令和５年３月 国土交通省住宅局参事官」
- Quote: https://www.mlit.go.jp/common/001016469.pdf PDF p.7: 「ガイドラインは、あくまで負担割合等についての一般的な基準を示したものであり、法的な拘束力を持つものでもない」

### F16. クロス耐用年数6年・残存価値1円。「残存価値10%」は再改訂前の古い基準 — **stands**
- URL: https://www.mlit.go.jp/common/001016469.pdf PDF p.16
- Quote: 「償却年数経過後の残存価値は10％となるようにして賃借人の負担を決定してきた。しかしながら、平成19年の税制改正によって残存価値が廃止され」
- Table: 001611293.pdf p.4 「壁クロス ６年」.

### F17. その他の通常損耗：画鋲・ピン穴、ポスター・絵画の跡、電気ヤケ、借主所有エアコンのビス穴 — **stands**
- URL: https://www.mlit.go.jp/common/001016469.pdf 別表1 (PDF p.29)
- Quote: 「3．壁等の画鋲、ピン等の穴（下地ボードの張替えは不要な程度のもの）」「4．エアコン（賃借人所有）設置による壁のビス穴、跡」 (the same column lists 「テレビ、冷蔵庫等の後部壁面の黒ずみ（いわゆる電気ヤケ）」 and 「壁に貼ったポスターや絵画の跡」)
- Note: the 画鋲 item carries a limit (no underlying board replacement needed). Nail or screw holes for heavy objects are in the tenant column.

### F18. 消費者契約法10条は自動無効ではない。最高裁平成23年3月24日は敷引特約を「直ちに」無効とはいえないとした。事業者が前提 — **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=412AC0000000061;article=10 ; https://www.courts.go.jp/hanrei/81180/detail2/index.html (「平成21(受)1679」「最高裁判所第一小法廷」)
- Quote (法): 「民法第一条第二項に規定する基本原則に反して消費者の利益を一方的に害するものは、無効とする。」
- Newer rules: the CAA page (https://www.caa.go.jp/policies/policy/consumer_system/consumer_contract_act/) lists amendments only up to 令和4年 (法律第59号・第99号). The e-Gov text of Article 10 is unchanged.

### F19. 相談先：消費者ホットライン188（局番なし、最寄りの消費生活センター等を案内） — **stands**
- URL: https://www.caa.go.jp/policies/policy/local_cooperation/local_consumer_administration/hotline/ ; https://www.kokusen.go.jp/news/data/n-20260217_1.html
- Quote: 「困ったときは、一人で悩まずに、「消費者ホットライン」188にご相談ください。」; 「全国共通の3桁の電話番号です。」
- Note (optional): some IP phones and prepaid mobiles cannot use it (「一部のIP電話、プリペイド式携帯電話…からは、お住まいの地域の相談窓口に直接おかけください」). Call charges apply, but the consultation itself is free.

### F20. 少額訴訟：60万円以下、原則1回、同じ簡裁で年10回まで、被告の申出で通常訴訟へ移行 — **stands (precision note)**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=408AC0000000109;article=368 ; https://www.courts.go.jp/saiban/syurui/syurui_minzi/minzi_25_02/index.html
- Quote: 「60万円以下の金銭の支払を求める訴えについて、原則として1回の審理で紛争解決を図る手続です。」; 「1人につき同じ裁判所に年間10回までと制限されています。」
- Precision: the defendant's transfer request is time-limited. 民訴法373条1項 (https://laws.e-gov.go.jp/api/1/articles;lawId=408AC0000000109;article=373): 「ただし、被告が最初にすべき口頭弁論の期日において弁論をし、又はその期日が終了した後は、この限りでない。」

### F21. 少額訴訟の手数料：2026年5月21日以降、訴額10万円まで書面3,500円・電子2,400円（郵便費用込み、原則ペイジー）。「1,000円＋郵便切手」は旧法の値 — **stands**
- URL: https://www.courts.go.jp/assets/tesuuryo_hayami.pdf (row 「10万まで」: 人事訴訟 1,000 / 民事・行政訴訟（書面申立て）3,500 / （電子申立て）2,400); https://www.courts.go.jp/saiban/syurui/syurui_minzi/minzi_25_02/index.html
- Quote (少額訴訟 page): 「従来必要であった郵便費用は、申立手数料に一本化されました。」; 「申立手数料は、原則として、ペイジーによる電子納付となります。」
- Column check: the layout-mode extraction shows the 訴えの提起 header in the order 人事訴訟 / 書面 / 電子. The 1,100-yen gap (3,500 − 2,400) matches 「申立手数料が1100円安くなります」 on https://www.courts.go.jp/saiban/syurui/syurui_minzi/minzi_25_20/index.html.
- Old value: the e-Gov API text of 民事訴訟費用等に関する法律 (lawId 346AC0000000040) still reads 「その価額十万円までごとに　千円」 and keeps 「（郵便切手等による予納）」. That copy appears to predate 2026-05-21, which supports the 1,000円 + stamps figure as the old regime.
- Note: if there are two or more defendants, add 2,000 yen per additional defendant (fee table ※1).

### F22. 東京ルール：都内物件で宅建業者が仲介する新規契約のみ対象。契約前の説明義務で、精算方法は規制しない — **stands (precision note)**
- URL: https://www.juutakuseisaku.metro.tokyo.lg.jp/juutaku_seisaku/tintai/310-23-00-jyuutaku.pdf (2022.11 改訂版; the Tokyo page https://www.juutakuseisaku.metro.tokyo.lg.jp/fudosan/tintai/310-23 shows 「最終更新日：令和5（2023）年3月29日」 and no newer leaflet)
- Quote: 「この条例は、契約の前にあらかじめ説明をするよう宅建業者に義務付けたもので、賃貸借契約の内容や敷金の精算方法について規制しているわけではありません。」
- Precision: the scope covers 「媒介（仲介）・代理」 and 「新規賃貸借契約（更新契約は除きます。）」. Contracts made directly with the landlord are excluded.

### F23. 敷引特約：「直ちに」無効ではないが、無効となる場合もある（要旨後半は未確認）。どの地域に多いかは未確認 — **needs change**
- URL: https://www.courts.go.jp/hanrei/81180/detail2/index.html
- Quote (裁判要旨1, latter half, now verified): 「敷引金の額が高額に過ぎると評価すべきものであるときは，当該賃料が近傍同種の建物の賃料相場に比して大幅に低額であるなど特段の事情のない限り，…消費者契約法１０条により無効となる。」
- Corrected wording: 「敷引特約は直ちに無効とはいえないが、通常損耗の補修費用として想定される額、賃料、礼金等に照らして敷引金が高額に過ぎる場合は、賃料が相場より大幅に安いなどの特段の事情がない限り、消費者契約法10条により無効となる（最判平成23年3月24日）。」 Remove the hedge 「要旨の後半は今回原文を確認していない」. The regional claim stays unverified, as the key already says.

### F24. ハウスクリーニング特約・エアコンクリーニング特約は実務で多く、部屋の広さに応じた定額が多い — **stands (minor addition)**
- URL: https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf p.7
- Quote: 「ハウスクリーニング特約については、部屋の広さや間取りに応じて定額の費用を負担する内容となっていることが多いようです。」
- Addition: 「広さや間取り」.

### F25. 返信に入れるべき要素（了承しない、明細・根拠条文・入居時記録の提示、日焼けは通常損耗、敷金全額返還、立会い・写真） — **stands**
- URL: https://www.kokusen.go.jp/news/data/n-20260217_1.html
- Quote: 「退去する時は、入居時と同様に、できる限り貸主側と一緒に、写真を撮ったりメモを取ったりして記録を残しながら、賃貸住宅の現状を確認しましょう。」
- Note: this is advice rather than a checkable fact. Every element is supported by kokusen and by 001611293.pdf p.7 (入居時の記録).

---

## Could not decide
- Which regions use 敷引 most (F23, last clause). Not verified; WebSearch quota was exhausted.
- Whether any 2025-2026 court decision or new prefectural or municipal ordinance changes the outcome. The primary pages checked (MLIT guideline page, CAA 消費者契約法 page, Tokyo page, e-Gov articles, courts.go.jp) show no newer rule. A web-wide search could not be completed (quota exhausted after two searches; neither found a 2026 guideline revision or a 消費者契約法10条 amendment).
