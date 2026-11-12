# ja-medical-deduction: adversarial check of "Facts for the key" (2026-10-22)

Checked file: W:\AgentData\logs\gravitas-dsh-ab4\sources\ja-medical-deduction.md (section "Facts for the key").
I opened every source below again on 2026-10-22, by direct download (curl) and text extraction, not from the draft's quotes. NTA Tax Answer pages are marked 「[令和8年4月1日現在法令等]」. I searched for 2025-2026 amendments: the 令和8年度税制改正 (所得税法等の一部を改正する法律, 令和8年法律第12号), the new resident-tax figures, and the self-medication amendment that takes effect 2027-01-01. I recomputed every figure.

Result: 35 facts checked. 33 stand, 2 need a change (K25 医療費通知, K30 self-medication end date). The undecided points are listed at the end.

---

## 前提とその誤り

**K1. 「医療費が10万円を超えないと受けられない」は誤り** - stands
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1120.htm
- 「（2）10万円」「（注）その年の総所得金額等が200万円未満の人は、総所得金額等の5パーセントの金額」

**K2. 足切り額は10万円と総所得金額等の5%のいずれか少ない方（所得税法73条、No.1120）** - stands
- https://laws.e-gov.go.jp/api/1/articles;lawId=340AC0000000033;article=73 (current text; the 令和8年 reform did not change Art. 73)
- 「…合計額の百分の五に相当する金額（当該金額が十万円を超える場合には、十万円）を超えるときは、その超える部分の金額…を…控除する。」

**K3. 総所得金額等200万円未満は5%基準。年収180万円のパートは該当** - stands
- Recomputed: 総所得金額等 = 106万円 under 2026 rules (K8), or 115万円 under 2025 rules. Both are below 200万円.
- Source: as K1.

**K4. 申告義務はない（No.1900）** - stands (assumes one employer, 年末調整 done, other income 20万円 or less)
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1900.htm
- 「大部分の給与所得者の方は、給与の支払者が行う年末調整によって所得税額が確定し、納税も完了しますから、確定申告の必要はありません。」

**K5. 医療費控除は受けられる。申告は任意（還付申告）** - stands
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2030.htm
- 「（9）多額の医療費を支出したとき（医療費控除）」 is listed as a refund-return case for salaried workers.

## 正しい数字（2026年分）

**K6. 給与所得控除は令和8年分・9年分74万円（令和8年度税制改正）、65万円ではない** - stands
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
- Table 「令和8年分・令和9年分」: 「2,200,000円まで」「740,000円」. Table 「令和7年分」: 「1,900,000円まで」「650,000円」.
- 「（注1）令和8年12月1日に施行され、令和8年分及び令和9年分に適用される金額です。」

**K7. 2026年12月の年末調整で1年分まとめて反映** - stands (only if she is still employed and gets 年末調整 in December)
- https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf (令和8年5月, Q1-1)
- 「令和８年 12 月１日に施行され、令和８年分以後の所得税について適用されます。」「令和８年 11 月までの給与の源泉徴収事務に変更は生じません。」

**K8. 給与所得 180万 − 74万 = 106万円（＝総所得金額等）** - stands
- 1410.htm, 注2 special table: 「74万1,000円以上」〜「219万1,000円未満」 → 「その収入金額－74万円」. The same table is in the Q&A PDF, Q3-1.
- Recomputed: 1,800,000 − 740,000 = 1,060,000.

**K9. 足切り額 106万 × 5% = 5万3,000円** - stands
- Recomputed: 1,060,000 × 0.05 = 53,000. That is below 100,000, so 53,000 is the threshold.

**K10. 医療費控除額 7万 − 5万3,000 = 1万7,000円** - stands
- Recomputed: 70,000 − 53,000 = 17,000 (assumes no reimbursement).

**K11. 2025年ルールなら115万 → 5万7,500 → 1万2,500円。2026年分には使えない** - stands
- 1410.htm, 令和7年分 table, 「1,900,000円まで」「650,000円」. Recomputed: 1,800,000 − 650,000 = 1,150,000. ×5% = 57,500. 70,000 − 57,500 = 12,500.

## 実際にいくら得になるか

**K12. 2026年分の所得税の基礎控除は104万円（合計所得金額489万円以下）** - stands
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm (read from the page HTML)
- Row 「132万円以下」 has `<td rowspan="3">104万円</td>`, which spans 「132万円超 336万円以下」 and 「336万円超 489万円以下」. 「（注１）令和8年分の上記規定は、令和8年12月1日に施行されます。」

**K13. 課税所得 106万 − 104万 = 2万円。社会保険料を引けば通常0円** - stands
- Recomputed: 1,060,000 − 1,040,000 = 20,000. Any social insurance deduction of 20,000 or more brings taxable income to 0.

**K14. 源泉徴収税額0なら還付0円。還付は源泉徴収税額が上限（No.2030）** - stands
- 2030.htm: 「源泉徴収された所得税額や予定納税をした所得税額がない方(…)は、申告しても還付される所得税額はありません。」

**K15. 源泉徴収票の「源泉徴収税額」欄を確認** - stands
- Q&A PDF Q7-1 (注): 「源泉徴収税額のない場合（源泉徴収票の「源泉徴収税額」欄が「０」となっている場合等）には、…還付される税金はありません。」

**K16. 住民税（令和9年度）も給与所得控除74万円、基礎控除43万円のまま、課税の可能性が高い** - stands
- https://www.city.sendai.jp/shiminze-kikaku/kurashi/tetsuzuki/zekin/kojin/kaisei/r8.html (更新日：2026年9月14日)
- 「令和9年度及び令和10年度はさらに5万円加算され、74万円となります。」「個人市県民税の基礎控除に改正はありません。」
- https://www.city.nagano.nagano.jp/n062000/contents/p005573.html (更新日：2026年10月20日): 「合計所得金額が2,400万円以下の場合43万円」
- Rough recomputation: 106万 − 43万 − social insurance (well under 63万 at 180万円 salary) > 0, so she is taxable.

**K17. 住民税の軽減 1万7,000 × 約10% ≒ 1,700円** - stands
- https://www.city.tokorozawa.saitama.jp/faq/kurashifaq/kurashifaq2/iryouhikoujyo.html (更新日：2026年1月5日)
- 「令和7年分の所得税（ここでは10％）と令和8年度の市民税（一律10％）を合わせて2,000円程度の軽減を受けられます。」 For resident tax 総所得金額等 is also 106万, so the threshold is 53,000 and the deduction 17,000. 17,000 × 10% = 1,700.

**K18. 確定申告は住民税に反映。所得税の申告をしないなら住民税申告でも可。手続きは自治体により異なる** - stands
- Tokorozawa (as K17): 「翌年に申告することで所得税の軽減・還付や、市民税の軽減を受けることができます。」
- Same page: 「平成30年度（平成29年分）の市民税・県民税申告から、領収書の代わりに「医療費控除の明細書」…の添付が必要となりました。」 This shows the deduction is claimed through a 市民税・県民税申告.

**K19. 「約600円」は誤り。1万7,000円なら約850円（復興税込み約868円）、実際は通常0円** - stands
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm: 「1,000円 から 1,949,000円まで」「5％」. ※2: 「復興特別所得税（原則としてその年分の基準所得税額の2.1パーセント）」. The ※3 rate change applies 「令和9年以後」, so 2026 still uses 2.1%.
- Recomputed: 17,000 × 5% = 850. × 1.021 = 867.85, so about 868. (2025 basis: 12,500 × 5% = 625, which is the "about 600".)

## 来年に向けてやっておくこと

**K20. 「医療費控除の明細書」を作り、領収書は添付しない。自宅で5年間保管** - stands
- https://www.nta.go.jp/taxes/shiraberu/shinkoku/tokushu/keisubetsu/iryou-koujo.htm (令和7年分 確定申告特集)
- 「医療費控除を受けるためには、「医療費控除の明細書」を所得税の確定申告書に添付する必要があります。」「医療費の領収書は自宅で5年間保管する必要があります。」

**K21. 交通費を日付・金額で記録。ガソリン・駐車場は対象外。タクシーは原則対象外** - stands
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1128.htm: 「通院費は、診察券などで通院した日を確認できるようにしておくとともに金額も記録しておくようにしてください。」
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1122.htm: 「（注1）電車やバスなどの公共交通機関が利用できない場合を除き、タクシー代は控除の対象には含まれません。」「（注2）自家用車で通院する場合のガソリン代や駐車場の料金などは、控除の対象には含まれません。」

**K22. 2026年1月1日〜12月31日に実際に支払った医療費。年内の追加支払いも合算** - stands
- 1120.htm: 「その年の1月1日から12月31日までの間に支払った医療費であること（未払いの医療費は、現実に支払った年の医療費控除の対象となります。）。」

**K23. 生命保険の給付金・高額療養費・付加給付などの補てんは差し引く** - stands (付加給付 is not named in so many words)
- 1120.htm: 「生命保険契約などで支給される入院費給付金や健康保険などで支給される高額療養費・家族療養費・出産育児一時金など」
- https://www.nta.go.jp/law/tsutatsu/kihon/shotoku/16/01.htm (所得税基本通達73-8(1)): 「社会保険又は共済に関する法律その他の法令の規定に基づき支給を受ける給付金のうち、…高額療養費…のように医療費の支出の事由を給付原因として支給を受けるもの」. 付加給付 falls under this catch-all wording. That is my inference.

**K24. 生計を一にする家族の医療費は合算できる。申告するのは支払った人** - stands
- 1120.htm: 「（1）納税者が、自己または自己と生計を一にする配偶者やその他の親族のために支払った医療費であること。」

**K25. 「医療費のお知らせ（医療費通知）」は明細書の代わりに使える** - refuted/needs change
- 1120.htm: 「医療費通知を添付することによって医療費控除の明細書の記載を簡略化することができます。」 For the income-tax return the notice simplifies the statement. It does not replace it, and the notice must contain every item listed in (注2).
- (Tokorozawa's page says that for a 市民税・県民税申告 the 明細書 may be omitted when the notice is attached. That is a municipal practice and does not apply to the 確定申告.)
- Corrected wording: 「健保の「医療費のお知らせ（医療費通知）」を添付すると、「医療費控除の明細書」の記載を簡略化できます（明細書は提出します）。医療費通知に載らない自費診療や通院交通費は、明細書に別に記入します。」

**K26. マイナポータル連携で毎年2月9日以降、保険診療分を自動入力できる** - stands
- https://www.nta.go.jp/taxes/shiraberu/shinkoku/tokushu/keisubetsu/pdf/0025009-005.pdf
- 「毎年２月９日以降、申告する年分の１月から12月までの保険診療分（※）に係る医療費情報を、マイナポータル連携を利用して取得・申告書に自動入力できます」
- Optional addition from the same footnote: 「保険診療分であっても、はり・きゅう等の施術費用や整骨院・接骨院の柔道整復療養費など取得できない情報もあります。」

**K27. 自費診療・交通費は含まれないので手入力（推論）** - stands as labelled inference
- Same leaflet: the data covers only 「保険診療分」. The leaflet does not mention 自費診療 or 交通費 explicitly.

**K28. 還付申告は2027年1月1日から5年間（2031年12月31日まで）。確定申告期間を待つ必要なし** - stands
- 2030.htm: 「還付申告書は、確定申告期間とは関係なく、その年の翌年1月1日から5年間提出することができます。」 Recomputed: 2027-01-01 to 2031-12-31.

## 付け加えられがちな点

**K29. 歯科：保険診療は対象。金・ポーセレン対象。容ぼう美化の矯正は対象外。歯科ローンは契約年、金利・手数料対象外。ホワイトニングは明示なし** - stands
- 1128.htm: 「現在、金やポーセレンは歯の治療材料として一般的に使用されているといえますから、これらを使った治療の対価は、医療費控除の対象になります。」「同じ歯列矯正でも、容ぼうを美化するための費用は、医療費控除の対象になりません。」
- 1128.htm (loan): 「その患者のその立替払をした年（歯科ローン契約が成立した時）の医療費控除の対象になります。」「（注）歯科ローンに係る金利および手数料相当分は医療費控除の対象になりません。」
- Whitening is still not named. Its exclusion is supported by 所得税基本通達73-4 (https://www.nta.go.jp/law/tsutatsu/kihon/shotoku/16/01.htm): 「容姿を美化し、又は容ぼうを変えるなどのための費用は、医療費に該当しないことに留意する。」 Suggested wording: 「ホワイトニングは国税庁の例示にはありませんが、容姿を美化するための費用は医療費に当たらない（所得税基本通達73-4）ため、通常は対象外です。」

**K30. セルフメディケーション税制：選択適用・選び直し不可、1万2,000円超・上限8万8,000円、歯科・交通費は対象外、2027年以降の終期は未確認** - refuted/needs change (the last clause only)
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1131.htm: 「…通常の医療費控除との選択適用となりますので、いずれか一方を選択して適用することになります。」
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1129.htm: 「…から12,000円を差し引いた金額（最高88,000円）です。」「…更正の請求や修正申告によりこの選択を変更することはできません。」 These parts stand.
- The end date can now be decided. https://www.mhlw.go.jp/content/10800000/001738404.pdf (租税特別措置法41条の17, 「令和 9 年 1 月 1 日施行時点」, reflecting 令和8年法律第12号) gives switch OTC 「平成二十九年一月一日以後の期間」 and other items 「平成二十九年一月一日から令和十三年十二月三十一日までの期間」. The amounts stay 「一万二千円」 and 「八万八千円」.
- Tokorozawa (as K17) agrees: 「スイッチＯＴＣ医薬品にかかる適用期限については撤廃されます。」「…令和13年12月31日まで5年延長することとされました。」
- Corrected wording: 「令和8年度税制改正（令和9年1月1日施行）で、スイッチOTC医薬品は適用期限が撤廃され、それ以外の対象医薬品は2031年（令和13年）12月31日まで延長されました。控除額の計算（1万2,000円超、上限8万8,000円）は変わりません。」

**K31. 医療費控除の上限は200万円** - stands
- 1120.htm: 「医療費控除の金額は、次の式で計算した金額（最高で200万円）です。」

**K32. 年末調整では医療費控除を受けられない（所得税法190条に73条なし）** - stands
- https://laws.e-gov.go.jp/api/1/articles;lawId=340AC0000000033;article=190: the deductions listed are 「第七十四条から第七十七条までの規定」 (社会保険料・小規模共済・生命保険料・地震保険料), then 「第七十九条から第八十二条まで（障害者控除等）及び第八十四条（扶養控除）」, then 配偶者 and the others. Art. 73 is not among them.

**K33. 配偶者がいる場合：本人106万円は配偶者控除の62万円を超える。配偶者特別控除26万円（配偶者本人900万円以下）。医療費控除は合計所得金額を変えない** - stands
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1195.htm: 「年間の合計所得金額が62万円超（注）133万円以下」. In the 「令和8年分以降」 table the row 「105万円超　110万円以下」 gives 「26万円」 in the 「900万円以下」 column.
- https://www.nta.go.jp/taxes/shiraberu/taxanswer/yogo/senmon.htm (合計所得金額): 「事業所得、不動産所得、給与所得、総合課税の利子所得・配当所得・短期譲渡所得および雑所得の合計額（損益通算後の金額）」. Income deductions are not subtracted (inference from the definition).

**K34. 住民税の税率・非課税限度額は自治体で異なる。仙台市は2026年給与収入119万円以下が非課税** - stands
- Sendai (as K16): 「令和8年中の給与収入が119万円以下であれば個人市県民税は非課税となります。」

**K35. 社会保険の扶養（130万円）は別制度で未確認。社会保険料控除2万円以上なら所得税0円。保険料は制度により異なる** - stands (the key makes no claim about 130万円 and correctly marks it unverified)
- Arithmetic as K13. I did not check the 130万円 threshold either.

---

## Could not be decided (not counted as refuted)
- 付加給付 (K23): no NTA page names it. It is covered only by the catch-all in 通達73-8(1). That is my inference.
- Self-paid dental work and travel missing from the Mynaportal data (K27): inferred from 「保険診療分」. Not stated outright.
- Whitening (K29): not named anywhere at NTA. Its exclusion follows from 通達73-4.
- 130万円 social-insurance threshold (K35): not verified by either agent.
- K4 rests on facts the request does not state (a single employer, 年末調整 done, no other income over 20万円).
