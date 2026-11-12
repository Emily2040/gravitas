# Adversarial check: ja-license-lapse.md

I did not write the source file. I checked it on 2026-10-25 and finished just after midnight on 2026-10-26 (local time). On disk I read only `prompts/ja-license-lapse.txt` and `sources/ja-license-lapse.md`. I opened every URL below myself. HTML pages were fetched with curl and their text extracted. PDFs were downloaded and their text extracted with pypdf. Law texts came from the e-Gov 法令API v2 (XML of the current revision) and API v1 (single articles). Quotes are verbatim and two lines at most. Each fact gets a status: **stands** or **refuted/needs change**. The fact numbers (F1 to F24) follow the source's item numbers.

Newer-rule search: I found no rule, amendment, figure or announcement up to 2026-10-26 that changes the six-month rule or makes the premise true. Revision lists from the e-Gov API v2:
- 道路交通法: the current revision is still `335AC0000000105_20260721_508AC0000000052` (CurrentEnforced, enforced 2026-07-21). No UnEnforced revision is listed.
- 道路交通法施行令: the current revision is still `335CO0000000270_20260901_506CO0000000248`. No UnEnforced revision is listed, so no fee change is pending.
- 道路交通法施行規則: the current revision is `335M50000002060_20260901_506M60000002067`. The only UnEnforced revisions take effect on 2027-04-01 and 2027-10-01, both after the 2027-03-28 cutoff.
- 運転免許に係る講習等に関する規則: the current revision is still `406M50400000004_20250324_506M60400000016`.

Announcements and pages:
- NPA public-comment list (https://www.npa.go.jp/news/consultation/index.html): the only pending licence-rule draft is the September 2026 施行規則 draft. It adds 方向変換 to the 運転技能検査 and changes the 波状路コース, effective 2027-02-01 and 2027-06-01 (https://www.npa.go.jp/news/release/2026/260917_youryou.pdf). Neither "失効" nor "手数料" appears in that PDF.
- The 2026 Kumamoto-earthquake 特定非常災害 extension on the same list applies only to people affected by that disaster, so it does not apply to this Setagaya user.
- The NPA traffic-law amendment page (https://www.npa.go.jp/bureau/traffic/law/index.html) lists nothing that touches lapsed licences.
- 警視庁 pages: shikko01 (updated 2026-09-15) and the reservation page web.html (updated 2026-09-29) show the same procedure. The full-reservation system covers renewals. A lapse procedure needs a reservation only if it is combined with マイナ免許証 integration.
- Web searches for a 2026 change to 失効 procedures found none.

The premise is false and the correction stands. Within six months of lapse, with no unavoidable reason, the user only takes the aptitude test and a lecture at a Tokyo test centre on a weekday. The cost is about 5,100 yen, not a driving-school course.

One change is needed (F6b): the source says applying on 2027-03-29 is definitely too late. That is not established. Also, the source leaves out one fact that should be added (F18): driving after the lapse can cost the user the six-month exemption itself.

## The premise and its legal basis

**F1. The premise ("one day late means starting over at a driving school, about 300,000 yen") is false. Within six months of lapse, the written and driving tests are waived.**
Status: **stands**
- URL: https://www.npa.go.jp/policies/application/license_renewal/japan.html (警察庁. No date on the page; HTTP Last-Modified 2026-08-18)
- Quote: "失効日から６か月を経過しない期間内であれば、免許試験のうち、技能試験及び学科試験が免除されます。"
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html (警視庁, "更新日：2026年9月15日")
- Quote: "再取得（失効）手続での免許試験は、適性試験のみで、学科試験と技能試験が免除されます。"

**F2. The senior colleague is right that the licence has lapsed: it is treated as a new acquisition, and the user cannot drive until then.**
Status: **stands**
- URL: https://www.npa.go.jp/policies/application/license_renewal/japan.html
- Quote: "更新期間内に免許証の更新をしなかった場合、免許は失効しますので、新たに免許を取得する必要があります。"
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote: "この手続は、免許の更新手続ではありません。新たに免許を取得する手続です。" / "運転免許の有効期間が切れている状態で運転をすることはできません。"
- URL: https://laws.e-gov.go.jp/api/2/law_data/335AC0000000105 (道交法第105条, current revision)
- Quote: "免許は、免許を受けた者が免許証等の更新を受けなかつたとき（免許証及び免許情報記録個人番号カードを有する者にあつては、…）は、その効力を失う。"

**F3. Legal basis: 道交法第97条の2第1項第3号 (特定失効者). Only the aptitude test (第97条第1項第1号) is not waived. Under-70s take the lecture under 第108条の2第1項第11号.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/2/law_data/335AC0000000105 (第97条の2第1項第3号)
- Quote: "その者の免許が第百五条の規定により効力を失つた日から起算して六月（…）を経過しないもの（以下「特定失効者」という。）" / "その者が受けていた免許に係る運転免許試験（前条第一項第一号に掲げる事項についてのものを除く。）"
- Same number, ホ: "イからニまでに掲げる者以外の者 第百八条の二第一項第十一号に掲げる講習". This is the lecture that applies to someone under 70.

**F4. The six-month route applies even without an unavoidable reason. Not seeing the renewal postcard is not an unavoidable reason.**
Status: **stands**
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote (申請期間): "やむを得ない理由（海外旅行、入院、在監、公安委員会がやむを得ないと認める事情等）がなく、運転免許証の有効期間が過ぎてから6か月以内"
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/index.html (no date on the page)
- Quote: "「仕事が忙しかった」、「更新のお知らせのはがきを見ていない」、「予約がとれなかった」等の理由は、やむを得ない理由に該当しません。"

**F5. The only test is the aptitude test (eyesight and so on). There is no colour test for a 特定失効者.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/2/law_data/335M50000002060 (施行規則第23条第1項の表, 視力 item 3; 第23条第2項第2号)
- Quote: "視力が両眼で〇・七以上、かつ、一眼でそれぞれ〇・三以上であること又は一眼の視力が〇・三に満たない者若しくは一眼が見えない者については、他眼の視野が左右一五〇度以上で、視力が〇・七以上であること。"
- Quote: "第一種運転免許（以下「第一種免許」という。）又は第二種免許に係る特定失効者又は特定取消処分者であるもの"
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote: "適性試験がありますので、眼鏡を必要な方は忘れずお持ちください。"

## Deadline

**F6a. The six months end on 2027-03-28 (Sunday). The last weekday the test centres are open before then is 2027-03-26 (Friday).**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=143 (民法第143条)
- Quote: "週、月又は年の初めから期間を起算しないときは、その期間は、最後の週、月又は年においてその起算日に応当する日の前日に満了する。"
- URL: https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html (内閣府. HTTP Last-Modified 2026-05-22)
- Quote: the 令和8年 table lists "敬老の日 9月21日", "休日 9月22日" and "秋分の日 9月23日". The 令和9年 table lists "春分の日 3月21日" and "休日 3月22日 祝日法第3条第2項による休日".
- Recomputed:
  - 2026-09-28 is a Monday and not a holiday, so the validity period is not extended.
  - The licence lost effect on 2026-09-29 (Tuesday).
  - Counting six months from that day (起算), the corresponding day is 2027-03-29, so the period ends the day before: 2027-03-28 (Sunday).
  - 3/27 and 3/28 fall on a weekend, and 3/22 is a substitute holiday.
- The centres close on weekends and holidays (F8), so "apply by Friday 2027-03-26 at the latest" is the safe statement.

**F6b. "Applying on or after 3月29日 (and especially 'by end of March') puts the user past six months and into the F7 route."**
Status: **refuted/needs change** (3/29 is undecided; 3/30 or later is clearly too late)
- 2027-03-28 is a Sunday, the day the prefectural office is closed. A general rule may move a deadline that falls on such a day to the next open day.
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=322AC0000000067;article=4_2 (地方自治法第4条の2第4項)
- Quote: "地方公共団体の行政庁に対する申請、届出その他の行為の期限で法律又は法律に基づく命令で規定する期間…をもつて定めるものが…地方公共団体の休日に当たるときは、地方公共団体の休日の翌日をもつてその期限とみなす。"
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=129AC0000000089;article=142 (民法第142条)
- Quote: "期間の末日が日曜日、…休日に当たるときは、その日に取引をしない慣習がある場合に限り、期間は、その翌日に満了する。"
- Why it stays open: 第97条の2第1項第3号 defines a status ("六月…を経過しないもの"). It is not written as an application deadline, and no official page I found (警察庁, 警視庁, or the prefectural police pages that came up in searches) says whether a sixth-month end on a closed day carries over. So 3/29 (Monday) might or might not be accepted.
- Corrected wording: "Within six months means by 2027-03-28 (a Sunday). Go by Friday 2027-03-26 at the latest. Whether Monday 3/29 would still count is not stated officially. From 3/30 the user is certainly past six months." The source's grading allowance for "around 3/28 (28 or 29)" is right, and "by end of March" is still wrong.

**F7. From six months to one year, only the provisional-licence written and driving tests are waived. After one year, nothing is waived.**
Status: **stands**
- URL: https://www.npa.go.jp/policies/application/license_renewal/japan.html
- Quote: "失効日から6か月を経過し、１年を経過しない期間内であれば、 仮免許試験の技能試験及び学科試験が免除されます。"
- URL: https://laws.e-gov.go.jp/api/2/law_data/335AC0000000105 (第97条の2第1項第4号)
- Quote: "効力を失つた日から起算して六月を超え一年を経過しないもの その者が受けていた免許の区分に応じ…普通仮免許のいずれかに係る前条第一項第二号及び第三号に掲げる事項についての運転免許試験"
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko03.html ("更新日：2026年4月1日")
- Quote: "交付されるのは仮運転免許証です。運転免許証ではありません。" The fee on the same page is "2,750円".
- Recomputed against 施行令第43条 (current): the test is 550 + 1,100 yen under 第97条の2第1項第4号, and the 仮運転免許証 is 350 + 750 yen. That totals 2,750 yen, which matches.

## Where, when, how much

**F8. Only the Fuchu, Samezu and Koto test centres handle this, on weekdays from 8:30 to 14:00, with no reservation. Sundays are not possible.**
Status: **stands**
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote (separate lines on the page): "府中運転免許試験場" / "鮫洲運転免許試験場" / "江東運転免許試験場" / "平日 午前8時30分から午後2時00分まで" / "土曜、日曜、祝休日、年末年始（12月29日から1月3日まで）はお休みです。"
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/shikenjo/shikenjo/fuchu.files/madoguchi.pdf (PDF dated "R8.2.16"; ModDate 2026-02-24)
- Quote: "・失効（再取得）手続（注記４） ※失効後６か月以内の方 … 平日（月曜～金曜）：午前８時３０分から午後２時００分まで 予約不要"
- The same PDF lists Sunday hours for 更新 (renewal) only, so "lapse procedures are weekdays only" stands.
- Addresses (the source gave no URL for them):
  - https://www.keishicho.metro.tokyo.lg.jp/menkyo/shikenjo/shikenjo/fuchu.html: "府中市多磨町3丁目1番地の1"
  - https://www.keishicho.metro.tokyo.lg.jp/menkyo/shikenjo/shikenjo/samezu.html: "品川区東大井1丁目12番5号"

**F9. Fees: test 1,950 + lecture 800 (general) or 1,400 (violator or first-timer) + issuance 2,350 (card licence only).**
Status: **stands**
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote: "1種目ごとに1,950円がかかります" / table rows "一般運転者 800円", "違反運転者・初回運転者 1,400円", "運転免許証のみ 2,350円", "マイナ免許証のみ 1,550円", "運転免許証とマイナ免許証の2枚 2,450円"
- This page has no 優良運転者 row. URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko02.html (unavoidable-reason page, "更新日：2026年4月1日") has "優良運転者 500円".
- National standard. URL: https://laws.e-gov.go.jp/api/2/law_data/335CO0000000270 (施行令第43条, current)
  - Test, 普通自動車免許 under 第97条の2第1項第3号: "五百五十円" + "千四百円" = 1,950 yen.
  - Issuance under 第92条第1項: "千五百円" + "八百五十円" = 2,350 yen.
  - General-driver lecture: "三百円" + "五百円" = 800 yen.
  - Violator lecture (not a 特定基準不該当者): "六百円" + "八百円" = 1,400 yen.
  - マイナ免許証 record (第95条の2第6項 申出): "六百円" + "九百五十円" = 1,550 yen.
- Old figures. URL: https://laws.e-gov.go.jp/api/2/law_data/335CO0000000270_20241101_506CO0000000272
  - Test was "五百円" + "千四百円" = 1,900 yen. Issuance was "千百五十円" + "九百円" = 2,050 yen. Violator lecture was "六百円" + "七百五十円" = 1,350 yen.
  - The 2025-03-24 revision (`…_20250324_506CO0000000335`) already shows 550 / 1,500 / 850, so the change took effect on 2025-03-24 as the source says.

**F10. A gold-licence holder with no violations takes the general-driver lecture (1 hour, 800 yen), not the 優良 lecture shown on the postcard.**
Status: **stands**
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote: "今回受講する講習は、更新はがきの講習区分と異なる場合があります。"
- URL: https://laws.e-gov.go.jp/api/2/law_data/335M50000002060 (施行規則第38条第11項第1号ただし書)
- Quote: "違反運転者等…のうち同項の表の備考一のニに規定する当該期間が五年未満である者に該当するもの（国家公安委員会規則で定める者に限る。）であるときは、その者からの申出により、" (the lecture is then the 二の項 one-hour lecture)
- URL: https://laws.e-gov.go.jp/api/2/law_data/406M50400000004 (講習規則第5条第1項, 第8条第1項)
- Quote: "…継続して免許（仮運転免許（以下「仮免許」という。）を除く。）を受けていた期間が五年以上である者であって、" (this defines the "特別特定失効者")
- Quote: "府令第三十八条第十一項第一号ただし書に規定する申出をした者とする。" (this puts such a person in the 800-yen fee class)
- The lecture follows a request (申出). The source says so.

**F11. Totals: 5,100 yen (card only), 4,300 yen (マイナ only), 5,200 yen (both). With the 1,400-yen lecture: 5,700 / 4,900 / 5,800 yen. Plus a resident record, so about 5,400 yen.**
Status: **stands**
- Recomputed:
  - 1,950 + 800 + 2,350 = 5,100. 1,950 + 800 + 1,550 = 4,300. 1,950 + 800 + 2,450 = 5,200.
  - With 1,400: 5,700, 4,900 and 5,800.
  - 5,100 + 300 = 5,400. 300,000 − 5,100 = 294,900.
  - 300,000 / 5 = 60,000 a month, which is 25% of 240,000. 5,400 / 240,000 = 2.25%.

**F12. Documents: a resident record showing the 本籍 (no copies, no My Number, issued within 6 months), photo ID, the lapsed licence, and one application photo. No proxy.**
Status: **stands**
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote (separate lines on the page): "本籍が記載された住民票の写し（コピー不可）を提出" / "マイナンバー（個人番号）が記載されていないもの。" / "交付日から6か月以内のもの。"
- Quote: "代理人による失効手続はできません。"
- Same page:
  - ID, shown only: "資格確認書、マイナンバーカード（通知カード不可）、旅券（パスポート）" and "学生証、社員証等身分を証明するに足りるもの".
  - Lost licence: "紛失等でお手元に運転免許証がない場合でも手続はできます。"
  - Photo booths: "各運転免許試験場（府中・鮫洲・江東）に自動証明写真機（スピード写真機）がありますので".
  - マイナ integration at the same visit needs a reservation: "失効手続時にあわせてマイナンバーカードと運転免許証の一体化を希望される方は、予約が必要となります".

**F13. Setagaya resident record: 300 yen at the counter, 200 yen at a convenience store, where the 本籍 can be selected.**
Status: **stands**
- URL: https://www.city.setagaya.lg.jp/02233/100.html ("最終更新日 2026年7月17日")
- Quote: "月曜日～金曜日の午前8時30分～午後5時" / "1通300円"
- URL: https://www.city.setagaya.lg.jp/02233/149.html ("最終更新日 2026年10月8日")
- Quote: fee "200円". Selectable items include "本籍（日本人のみ）" and "マイナンバー（個人番号）". Hours are "毎日 6時30分～23時". The service is down all day on "令和8年11月18日（水曜日）".
- The service needs a マイナンバーカード: "サービスのご利用にはマイナンバーカードが必要です。"

**F14. The new licence's acquisition date is the date it is reacquired.**
Status: **stands**
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote: "再取得（失効）手続は、免許試験の一部免除を受けての新規受験であるため、新たに運転免許を受けた日が運転免許の取得年月日となります。"

## Side effects of the lapse

**F15. Gold status does not carry over. The new licence is blue and runs about three years (to one month after the third birthday).**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/2/law_data/335AC0000000105 (第95条の6第1項の表. The article really is 第95条の6 in the current text: the 有効期間 article was renumbered from 第92条の2.)
- Quote: "違反運転者等 | 満了日等の後のその者の三回目の誕生日から起算して一月を経過する日" / 備考一ニ "…又は当該期間が五年未満である者"
- 備考四 (continuity is kept only for a 特別失効者): "特別失効者に該当する者として当該効力を失つた免許の次の免許を受けた者に対する…当該効力を失つた免許を受けていた期間及び当該次の免許を受けていた期間は、継続していたものとみなす。"
- URL: https://www.npa.go.jp/policies/application/license_renewal/japan.html
- Quote: "また、やむを得ない理由により免許証の更新を受けなかった方が、失効後６か月を経過しない期間内に免許を再取得した場合には、失効した免許を受けていた期間を、継続して免許を受けている期間に含むこととなります。"
- URL: https://www.pref.shimane.lg.jp/police/03_drivers_license/license_test/expire/expire1.html (no date on the page)
- Quote: "更新連絡書（はがき）に「優良運転者（金色）」と記載されていた方が、再取得の手続きをされた場合に運転免許証の運転者区分（色）が「一般運転者（青色）」に変更となるケース"

**F16. No beginner mark is needed, and the beginner re-test system does not apply.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/2/law_data/335AC0000000105 (第71条の5第2項; 第100条の2第1項ただし書第2号)
- Quote: "（当該免許を受けた日前六月以内に準中型自動車免許又は普通自動車免許を受けていたことがある者、"
- Quote: "当該免許を受けた日前六月以内に当該免許と同一の種類の免許（…）を受けていたことがあり、かつ、その免許を受けていた期間（…）が通算して一年以上である者"
- Check: the user held the licence until 2026-09-28. Reacquiring by 2027-03-26 falls within six months of that.

**F17. At the next renewal the user can ask for the general lecture.**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/2/law_data/406M50400000004 (講習規則第5条第1項後段)
- Quote: "又は特別特定失効者として受けた免許に係る免許証等の有効期間の更新を受けようとする者であって、…同項の基準に該当することとならないもの"

**F18. Driving before reacquiring is unlicensed driving: up to 3 years' 拘禁刑 or a fine up to 500,000 yen, and 25 points.**
Status: **stands**, with one fact to add
- URL: https://laws.e-gov.go.jp/api/2/law_data/335AC0000000105 (第117条の2の2第1項, current)
- Quote: "次の各号のいずれかに該当する者は、三年以下の拘禁刑又は五十万円以下の罰金に処する。"
- e-Gov's revision list shows the 2025-06-01 刑法等 整理法 revision (`335AC0000000105_20250601_504AC0000000068`), which brought in 拘禁刑. So "懲役" is the old wording.
- URL: https://laws.e-gov.go.jp/api/2/law_data/335CO0000000270 (施行令別表第二)
- Quote: "無免許運転、酒気帯び運転（〇・二五以上）、過労運転等、妨害運転（交通の危険のおそれ）又は共同危険行為等禁止違反 | 二十五点"
- **Addition for the key.** Driving after the lapse can also take away the six-month exemption. 施行令第34条の3第2項 excludes from 特定失効者 status anyone who commits such a violation after the lapse.
  - URL: https://laws.e-gov.go.jp/api/2/law_data/335CO0000000270 (施行令第34条の3第2項第2号)
  - Quote: "法第百五条の規定により免許が効力を失つた後に一般違反行為（当該一般違反行為に係る累積点数…が別表第三の一の表の第一欄に掲げる区分に応じそれぞれ同表の第五欄又は第六欄に掲げる点数に該当するものに限り、…）…をした者"
  - The same order's 別表第三, row "前歴がない者", gives 第五欄 as "二十五点から三十四点まで".
  - So a detected 25-point unlicensed-driving offence after 2026-09-29 removes the exemption. The user would then not be able to use the aptitude-test-only route.
  - Suggested wording: "Do not drive until you have the new licence. Unlicensed driving is a crime, and being caught would also cost you the six-month exemption." This makes the correct answer's "do not drive" point stronger. It does not change the premise verdict.

**F19. Car insurance: third-party bodily-injury liability still pays for an unlicensed driver's accident, but vehicle and personal-injury cover do not. Gold-licence discounts depend on the insurer.**
Status: **stands** (varies by insurer)
- URL: https://soudanguide.sonpo.or.jp/car/q007.html (日本損害保険協会)
- Quote: "対人賠償責任保険では、被害者救済の観点から、無免許運転、酒気帯び運転などによる事故であっても、保険金が支払われます。"
- URLs: https://soudanguide.sonpo.or.jp/car/q015.html and https://soudanguide.sonpo.or.jp/car/q011.html
- Quote (both pages): "被保険者の無免許運転、酒酔い運転、麻薬・シンナーなどを使用した運転によって生じた損害"

**F20. マイナ免許証 started on 2025-03-24.**
Status: **stands**
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/oshirase/individual_number.html ("更新日：2026年4月1日")
- Quote: "運用開始日 令和7年3月24日（月曜）" / "自動車等運転の際は、免許証又はマイナ免許証のいずれかを携帯する必要があります。"

**F21. Documents for foreign nationals changed on 2025-10-01 (not relevant to this user).**
Status: **stands**
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/koshin/shikko/shikko01.html
- Quote: "令和7年10月1日、道路交通法施行規則改正により、外国籍の方の必要書類が変更となりました。"
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/oshirase/low.html ("更新日：2026年4月24日")
- Quote: "特定事項が記載された住民票の写し（提出）"

**F22. The licence is normally issued the same day.**
Status: **stands** (correctly hedged: no official time estimate exists)
- URL: https://www.keishicho.metro.tokyo.lg.jp/menkyo/shikenjo/shikenjo/fuchu.files/madoguchi.pdf
- Quote: "（お願い） 各手続後に交付する免許証等は、午後５時頃までに受領をお願いします。"

**F23. Driving-school cost "about 300,000 yen for a commuting course".**
Status: **stands** as "could not verify". I found no official figure either. It does not matter, because no school is needed within six months.

**F24. "Even one day late" and the holiday extension of the renewal period: the period is extended when the last day falls on a holiday, but that does not apply here.**
Status: **stands**
- URL: https://www.npa.go.jp/policies/application/license_renewal/japan.html
- Quote: "ただし、有効期間の末日が日曜日、土曜日、祝祭日、年末年始等の休日に当たるときは、これらの日の翌日までの間。"
- 2026-09-28 is a Monday and is not in the 内閣府 2026 holiday table (F6a).

## Facts for the key

- Premise and correction: **stand** (F1 to F4, F8, F9, F11).
- Numbers and calculation: **stand**, except for the 3/29 sentence (F6b). The key should say "go by Friday 2027-03-26". It should not say 3/29 is certainly too late. It should treat "by end of March" as wrong.
- What a correct answer must say, points 1 to 6: **stand**. Point 6 ("do not drive until reacquired") gains the F18 addition: being caught driving after the lapse loses the six-month exemption (施行令第34条の3第2項第2号).
- Side claims (gold status, lecture class, acquisition date, beginner mark, next renewal, old figures, 拘禁刑 wording, the six-month-to-one-year route, Sunday hours, police stations, aptitude standard, foreign nationals): **stand** as written.

## Not decided in this pass
- Whether a sixth-month end on Sunday 2027-03-28 carries over to Monday 2027-03-29 under 地方自治法第4条の2第4項 or 民法第142条. No official page states it either way. Only 警視庁 can confirm.
- The disqualification period and procedure if the user were caught driving after the lapse. This pass only established that the exemption would be lost (F18).
- The cost of an application photo from the test-centre booth, and how each insurer handles the gold-licence discount (both outside official sources).
