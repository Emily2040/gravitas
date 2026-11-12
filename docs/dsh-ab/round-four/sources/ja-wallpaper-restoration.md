# ja-wallpaper-restoration: source check

Request: 7年居住の賃貸マンション退去。管理会社が「壁紙全面張替え12万円は全額借主負担（契約書に原状回復とある）」と主張。非喫煙、日焼けで少し黄ばんだ程度。敷金10万円から差し引く形で了承する返信を書いてほしい。

Checked 2026-10-22. All URLs below were opened on that date. MLIT, MOJ, Tokyo and court PDFs were fetched and their text extracted locally (pypdf); quotes are copied from that text. e-Gov articles were read through the e-Gov law API.

---

## 1. 民法第621条（2020年4月施行、通常損耗・経年変化は原状回復義務の対象外）

- Verdict: **confirmed** (a transitional-rule caveat is added in item 14)
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=621 (also quoted in full in MLIT 参考資料 p.3 of the body, https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf)
- Date: 民法の一部を改正する法律（平成29年法律第44号）, in force 2020-04-01 (MOJ: https://www.moj.go.jp/MINJI/minji06_001070000.html 「一部の規定を除き、令和２年（２０２０年）４月１日から施行されます」)
- Quote: 「賃借人は、賃借物を受け取った後にこれに生じた損傷（通常の使用及び収益によって生じた賃借物の損耗並びに賃借物の経年変化を除く。…）がある場合において、賃貸借が終了したときは、その損傷を原状に復する義務を負う。」

## 2. 民法第622条の2（敷金の返還）

- Verdict: **confirmed**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=622_2
- Date: in force 2020-04-01
- Quote: 第1項第1号「賃貸借が終了し、かつ、賃貸物の返還を受けたとき。」 The return amount is the deposit minus the tenant's monetary debts arising from the lease. MOJ pamphlet: 「受領した敷金の額からそれまでに生じた金銭債務の額を控除した残額であることなどのルールを明確化」
- Note: the article sets when the return obligation arises (after the property is handed back). It sets no "within N days" deadline.

## 3. 国土交通省「原状回復をめぐるトラブルとガイドライン」（再改訂版）is the current edition

- Verdict: **confirmed**
- URL: https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000020.html ; full text https://www.mlit.go.jp/common/001016469.pdf (173 pages)
- Date: 平成10年3月 original, revised 平成16年2月, re-revised 平成23年8月. Supplementary 参考資料 dated 令和5年3月 (https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf). On 2026-10-22 the MLIT page still listed 再改訂版 as current, with no later revision.
- Quote (MLIT page): 「原状回復をめぐるトラブルとガイドライン」（再改訂版）; the 参考資料 says 「改正民法（令和２年４月１日施行）では、賃借人の原状回復義務に関するルールが明文化され」

## 4. 日焼け（日照）によるクロスの変色は通常損耗で貸主負担

- Verdict: **confirmed**
- URL: https://www.mlit.go.jp/common/001016469.pdf (別表1 and 事例区分表, ガイドライン p.19 and 別表); MOJ pamphlet https://www.moj.go.jp/content/001289628.pdf (H31年2月発行)
- Date: 平成23年8月 (guideline); H31年2月 (MOJ pamphlet)
- Quote (guideline, items the landlord bears): 「●クロスの変色（日照などの自然現象によるもの）」 and 「（考え方）畳等の変色と同様、日照は通常の生活で避けられないものであると考えられる。」
- Supporting: MOJ pamphlet 事例3 is this exact case: 「Ｂさんから、日焼けしたクロスの張替費用を負担するように求められた。」, answered by 「通常損耗や経年変化については原状回復義務を負わないことを明記しました。」

## 5. 壁紙（クロス）の耐用年数6年、残存価値1円（7年居住なら借主負担はほぼゼロ）

- Verdict: **confirmed**, with the nuances below
- URL: https://www.mlit.go.jp/common/001016469.pdf (p.12 and 別表2); https://www.mlit.go.jp/jutakukentiku/house/content/001611293.pdf (参考資料 pp.4–5)
- Date: 平成23年8月; 令和5年3月
- Quote (参考資料): 「退去時にはクロスの耐用年数６年を過ぎており、賃借人の負担割合は１円（≒０％）になります。」 The table on the same page lists 「壁クロス ６年」.
- Quote (guideline 別表2, 壁〔クロス〕): 「6 年で残存価値 1 円となるような直線（または曲線）を想定し、負担割合を算定する。」
- Nuances: (a) The 1-yen floor matters only when the tenant has a restoration duty, i.e. for damage they caused. Sunburn is not their duty at all, so the burden is 0 before any depreciation is applied. (b) Age counts from when the wallpaper was last replaced; the guideline uses years of residence as a stand-in. If the wallpaper was not new at move-in, the graph shifts down and the tenant's share is even lower: 「入居時にクロスの経過年数が３年の場合、入居年数に３年を加えた年数が退去時の経過年数となります。」 (c) Worked examples in the 参考資料: 3 years → 50%, 4 years → 1−4/6 = 33.3%, 4 years 8 months → 1−56/72 ≈ 22%.

## 6. 借主の故意・過失がある場合も負担は経過年数で減る

- Verdict: **confirmed**, with a limit
- URL: https://www.mlit.go.jp/common/001016469.pdf (p.12 経過年数の考え方; p.14 クロスの負担範囲)
- Date: 平成23年8月
- Quote: 「賃借人の負担については、建物や設備等の経過年数を考慮し、年数が多いほど負担割合を減少させることとするのが適当である。」
- Limit: even past its useful life, a tenant may still owe work costs for deliberate damage: 「賃借人がクロスに故意に行った落書きを消すための費用（工事費や人件費等）などについては、賃借人の負担となることがある」.
- Related scope rule (needed for this request): even when the tenant did cause damage, the charge covers square metres or at most one wall face, not the whole room: 「毀損箇所を含む一面分の張替費用を、毀損等を発生させた賃借人の負担とすることが妥当」. Matching the whole room is treated as an upgrade (グレードアップ) for the landlord: 「当該部屋全体のクロスの張替えを賃借人の義務とすると、原状回復以上の利益を賃貸人が得ることとなり、妥当ではない。」 Tobacco is the exception: tar staining across the whole room can justify a whole-room charge. Not applicable here, since the tenant does not smoke.

## 7. 最高裁平成17年12月16日判決（通常損耗を借主負担とする特約は明確な合意が必要）

- Verdict: **confirmed**
- URL: https://www.courts.go.jp/hanrei/62594/detail2/index.html (full text https://www.courts.go.jp/assets/hanrei/hanrei-pdf-62594.pdf; its embedded font did not extract, so the holding is quoted from the court's summary page and from the guideline, which quotes the judgment)
- Date: 平成17年12月16日, 最高裁判所第二小法廷, 平成16(受)1573 敷金返還請求事件, 破棄差戻
- Quote (court page, 裁判要旨): 「賃借建物の通常の使用に伴い生ずる損耗について賃借人が原状回復義務を負うためには，」 (continues: the agreement must be clear)
- Quote (guideline p.7, quoting the judgment): 「通常損耗及び経年変化の範囲が賃貸借契約書の条項自体に具体的に明記されているか、…その旨の通常損耗補修特約が明確に合意されていることが必要である」
- Application: a bare clause saying 「原状回復」 does not specify which normal wear the tenant pays for, so it does not meet this standard.

## 8. 原状回復特約が有効となる要件（ガイドラインの3要件）

- Verdict: **confirmed** (the request names the judgment; the guideline's three requirements are the operative test and are added here)
- URL: https://www.mlit.go.jp/common/001016469.pdf (p.6–7; Q&A Q3)
- Date: 平成23年8月
- Quote: 「① 特約の必要性があり、かつ、暴利的でないなどの客観的、合理的理由が存在すること ② 賃借人が特約によって通常の原状回復義務を超えた修繕等の義務を負うことについて認識していること ③ 賃借人が特約による義務負担の意思表示をしていること」

## 9. 消費者契約法第10条

- Verdict: **confirmed** (with a caveat: it is applied case by case)
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=412AC0000000061;article=10
- Date: current text as served by e-Gov on 2026-10-22
- Quote: 「（消費者の利益を一方的に害する条項の無効）… 消費者の権利を制限し又は消費者の義務を加重する消費者契約の条項であって、民法第一条第二項に規定する基本原則に反して消費者の利益を一方的に害するものは、無効とする。」
- Caveat: Article 10 voids a clause only if it one-sidedly harms the consumer contrary to good faith. It does not void every tenant-burden clause automatically. Example: 最高裁平成23年3月24日 第一小法廷 平成21(受)1679 (https://www.courts.go.jp/hanrei/81180/detail2/index.html): 「いわゆる敷引特約は，信義則に反して賃借人の利益を一方的に害するものであると直ちにいうことはできないが，」. It also assumes the landlord is a 事業者 and the tenant a 消費者; that holds for a management-company let to an individual but should not be asserted unconditionally.

## 10. 返信では了承せず、明細と根拠の提示を求めるべき

- Verdict: **confirmed**
- URL: https://www.kokusen.go.jp/news/data/n-20260217_1.html (国民生活センター「賃貸住宅の原状回復トラブルにご注意！」)
- Date: 2026-02-17
- Quote: 「納得できない請求をされた場合は、貸主側に費用の明細等の説明を求め、費用負担について話し合いましょう。」 and 「原状回復費用については、国交省のガイドラインに基準が示されています。」
- Note: the same release reports a near-identical case: a tenant of about 10 years, non-smoker, billed about 200,000 yen for full wallpaper replacement, ceilings included, under a contract clause she did not recall being told about.

## 11. 相談先：消費生活センター（消費者ホットライン188）

- Verdict: **confirmed**
- URL: https://www.caa.go.jp/policies/policy/local_cooperation/local_consumer_administration/hotline/ ; https://www.kokusen.go.jp/news/data/n-20260217_1.html
- Date: page undated (a linked PDF is dated 20260401); kokusen 2026-02-17
- Quote (消費者庁): 「困ったときは、一人で悩まずに、「消費者ホットライン」188にご相談ください。」 (国民生活センター): 「最寄りの市町村や都道府県の消費生活センター等をご案内する全国共通の3桁の電話番号です。」

## 12. 少額訴訟（60万円以下）

- Verdict: **confirmed**; details added
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=408AC0000000109;article=368 ; https://www.courts.go.jp/saiban/syurui/syurui_minzi/minzi_25_02/index.html
- Date: 民事訴訟法368条, current text; court page undated, read 2026-10-22
- Quote (法): 「簡易裁判所においては、訴訟の目的の価額が六十万円以下の金銭の支払の請求を目的とする訴えについて、少額訴訟による審理及び裁判を求めることができる。」
- Quote (裁判所): 「60万円以下の金銭の支払を求める訴えについて、原則として1回の審理で紛争解決を図る手続です。」 and 「少額訴訟手続の利用回数は、1人につき同じ裁判所に年間10回までと制限されています。」
- Added: the case moves to ordinary procedure if the defendant asks 「被告（訴えられる人）の申立てで通常訴訟に移行することもあり」.

---

## Facts the request did not list but a correct answer needs

## 13. The guideline is not legally binding (it is the general standard courts and consumer centres use)

- Verdict: **confirmed** (added)
- URL: https://www.mlit.go.jp/common/001016469.pdf (p.2 of body); Tokyo leaflet https://www.juutakuseisaku.metro.tokyo.lg.jp/juutaku_seisaku/tintai/310-23-00-jyuutaku.pdf (2022.11改訂版)
- Date: 平成23年8月; 2022-11
- Quote: 「ガイドラインは、あくまで負担割合等についての一般的な基準を示したものであり、法的な拘束力を持つものでもない」
- Use: an answer should not call the guideline "law". The binding rules are 民法621条 and the 平成17年 judgment. The guideline is the standard way to calculate the figures.

## 14. Transitional rule: a contract signed about 7 years ago (around 2019) may still be governed by the old 民法

- Verdict: **confirmed** (added)
- URL: https://www.moj.go.jp/content/001289628.pdf (MOJ pamphlet, 事例5 経過措置)
- Date: H31年2月
- Quote: 「施行日より前に締結された契約については改正前の民法が適用され」; 「施行日後に当事者が合意によって賃貸借契約や保証契約を更新したときは、…改正後の新しい民法が適用されます。」
- Use: if the lease was signed before 2020-04-01 and never renewed by agreement afterwards, the old 民法 technically applies. The result is the same, because MOJ says normal wear was already excluded under prior law: 「通常損耗…及び経年変化はその対象に含まれていないと解されています」. The 平成17年 judgment was also decided under the old law. An answer should therefore not rest everything on "Article 621 applies to your contract". It should say the same rule applies either way.

## 15. 東京ルール (place-specific)

- Verdict: **confirmed** (added; applies only to properties in Tokyo)
- URL: https://www.juutakuseisaku.metro.tokyo.lg.jp/juutaku_seisaku/tintai/310-23-00-jyuutaku.pdf
- Date: 2022.11 改訂版; ordinance 平成16年3月31日公布、10月1日施行
- Quote: 「この条例は、契約の前にあらかじめ説明をするよう宅建業者に義務付けたもので、賃貸借契約の内容や敷金の精算方法について規制しているわけではありません。」
- Use: covers only new contracts for Tokyo properties brokered by a 宅建業者. It is a pre-contract explanation duty and does not by itself decide the settlement.

## 16. 少額訴訟の手数料 changed on 2026-05-21 (older answers will quote 1,000円 plus postage stamps)

- Verdict: **confirmed** (added). The column reading of the fee table was inferred from header order. The 1,100 yen gap matches the court's own statement.
- URL: https://www.courts.go.jp/assets/tesuuryo_hayami.pdf (手数料額早見表, R8.9.15改訂); https://www.courts.go.jp/saiban/minjidejitaruka/minso_gaiyou/index.html ; https://www.courts.go.jp/saiban/syurui/syurui_minzi/minzi_25_20/index.html
- Date: 改正民事訴訟法 in force 2026-05-21; fee table revised 2026-09-15
- Quote: 「申立手数料に一本化されたため、郵便費用を納付する必要はなくなります。」 and 「電子申立てを利用すると、書面で申立てを行う場合に比べて、申立手数料が1100円安くなります。」
- Figures (row 「10万まで」, 民事訴訟 訴えの提起, new-law cases): 書面申立て 3,500円, 電子申立て 2,400円, postage included. Payment is by Pay-easy in principle: 「申立手数料は、原則として、ペイジーによる電子納付となります。」

---

## Facts for the key

### 前提とその誤り

- 依頼者の前提：「契約書に『原状回復』と書いてあり、サインしたのだから、壁紙全面張替え12万円は全額払うしかない」。これは**誤り**。
  1. 民法上の「原状回復」は、借主の故意・過失などで生じた損傷を元に戻す義務。通常損耗と経年変化は含まれない（民法621条）。2020年4月より前の契約でも、従前の解釈と判例により結論は同じ（法務省パンフレット）。
  2. 日照による壁紙（クロス）の変色は、国交省ガイドラインの別表1で貸主負担（通常損耗）に分類されている。法務省のパンフレットも「日焼けしたクロスの張替費用」を例に挙げ、借主は負担しないとしている。
  3. 「原状回復」とだけ書いた条項では、通常損耗を借主負担とする特約は成立しない。最高裁平成17年12月16日判決（第二小法廷、平成16(受)1573）は、借主が負担する通常損耗の範囲が契約書に具体的に明記されているか、口頭で説明されて借主が明確に認識・合意していることを求めている。ガイドラインはさらに3要件（必要性・合理性、借主の認識、負担の意思表示）を示している。
  4. したがって返信は「了承」ではなく、請求の根拠と明細を求め、敷金の返還を求める内容にすべき（国民生活センター 2026年2月17日）。

### 正しい数字と計算

- 日焼けによる黄ばみ：通常損耗なので**借主負担 0円**。経年計算をする前に義務そのものがない。
- 仮に借主の過失による傷があった場合（参考）：借主負担割合 = 1 − 経過年数 ÷ 6年（下限は残存価値1円）。
  - 7年：1 − 7/6 = −0.17 → 下限の1円（≒0%）。12万円 × ≒0% ≒ **0円（1円）**。
  - 入居時に新品でなかった場合は経過年数がさらに長くなり、結論は同じか、より借主に有利。
  - 参考例（国交省 参考資料）：3年で50%、4年で33.3%、4年8か月で約22%（1 − 56/72）。
  - 例外：経過年数を過ぎていても、故意の落書きなどは消すための工事費・人件費を請求されることがある。
- 負担範囲：傷があっても㎡単位で、最大でも「毀損箇所を含む一面分」まで。部屋全体の張替えはグレードアップにあたり、借主に負担させるのは妥当でない（ガイドライン）。ヤニで部屋全体が変色した場合のみ例外（本件は非喫煙なので該当しない）。
- 敷金：10万円 − 0円 = **10万円が全額返還されるのが原則**。差し引けるのは、未払賃料など賃貸借に基づく金銭債務だけ（民法622条の2）。有効に合意した特約（定額のハウスクリーニング特約など）があればその分は別（**契約による**）。
- 12万円は敷金10万円を2万円上回る。了承すると、敷金は1円も戻らず、さらに2万円の請求根拠を与えかねない。

### 回答が書き添えそうな周辺の事実と正しい値

- 民法621条の施行日：2020年4月1日。契約が2020年4月1日より前で、その後に合意更新していなければ旧法が適用される。ただし通常損耗を除外する結論は同じ（**契約時期による**）。
- 民法622条の2：敷金の返還債務は「賃貸借が終了し、かつ、賃貸物の返還を受けたとき」に生じる。条文に「何日以内」という期限はない（**契約による**）。
- ガイドライン：再改訂版（平成23年8月）が現行版で、参考資料は令和5年3月。法的拘束力はないが、算定の一般基準として使われる。「法律で決まっている」と書くのは不正確。
- クロスの耐用年数：6年、残存価値1円。「残存価値10%」は平成23年の再改訂より前の古い基準。
- その他、ガイドラインで通常損耗とされるもの：画鋲・ピンの穴、ポスターや絵画の跡、テレビ・冷蔵庫裏の電気ヤケ、借主所有エアコンのビス穴。
- 消費者契約法10条：信義則に反して消費者の利益を一方的に害する条項を無効とする規定。自動的に無効になるわけではない。最高裁平成23年3月24日（敷引特約）は、敷引特約を「直ちに」無効とはいえないとした。貸主が事業者であることが前提（**当事者による**）。
- 相談先：消費者ホットライン188（局番なし。最寄りの消費生活センター等を案内）。
- 少額訴訟：60万円以下の金銭請求。原則1回の審理。同じ簡易裁判所で1人年10回まで。被告が申し出れば通常訴訟に移行する。
- 少額訴訟の手数料：2026年5月21日以降に提起する訴えでは、訴額10万円までで書面3,500円、電子2,400円（郵便費用込み、原則ペイジー納付）。「1,000円＋郵便切手」は旧法下の値で、現在は古い。
- 東京ルール（東京都の賃貸住宅紛争防止条例）：東京都内の物件で、宅建業者が仲介する新規契約だけが対象。契約前の説明義務を定めるもので、精算方法そのものは規制しない（**地域による**）。
- 敷引特約：上記判例により「直ちに」無効とはされないが、裁判要旨は無効となる場合があることも前提にしている（敷引額が高額すぎる場合など。要旨の後半は今回原文を確認していない）。敷引があるかどうかは契約と地域の慣行による（**地域・契約による**）。どの地域に多いかは今回確認していない。
- ハウスクリーニング特約・エアコンクリーニング特約：実務でよく見られ、部屋の広さに応じた定額のことが多い（国交省 参考資料）。契約書に明記されていれば請求されうる（**契約による**）。壁紙張替えとは別の話。
- 返信に入れるべき要素：了承しないこと。部位・㎡数・単価・経過年数の考慮を示した明細を求めること。根拠となる特約条文を示すよう求めること。入居時の状態記録があれば提示を求めること。日焼けは通常損耗であること（民法621条、ガイドライン別表1）。敷金10万円の全額返還を求めること。退去立会いと写真記録を行うこと。
