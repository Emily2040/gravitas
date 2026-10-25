# Adversarial check: ja-child-allowance-income-cap.md, "Facts for the key"

Checked 2026-10-25 by an agent that did not write the source file (the downloads finished just after midnight, so the last fetches are dated 2026-10-26). On disk I read only `prompts\ja-child-allowance-income-cap.txt` and `sources\ja-child-allowance-income-cap.md`. I opened every URL below myself on that date. HTML pages were downloaded with curl and converted to text. PDFs were downloaded and their text extracted with pypdf. Law text came from the e-Gov API v1 (single articles) and v2 (full text and revision list). Quotes are verbatim, two lines at most. Whitespace that the extraction inserted inside Japanese text is removed. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: I found no rule, amendment, figure or announcement up to 2026-10-26 that brings back an income limit or changes the amounts, the counting rule, the claim rule or the payment months. (1) e-Gov's revision list for 児童手当法 (https://laws.e-gov.go.jp/api/2/law_revisions/346AC0000000073) has as its newest entry the 2025-06-01 enforcement of 令和四年法律第六十八号 (刑法等改正の整理法), status CurrentEnforced. It shows no later revision and no scheduled (unenforced) one. The previous entry is the 2024-10-01 enforcement of 令和六年法律第四十七号, the expansion itself. (2) こども家庭庁's list of laws, orders and notices for 児童手当 (https://www.cfa.go.jp/policies/kokoseido/jidouteate/tsuuchi, HTTP Last-Modified 2025-08-13) ends with the 令和6年9月20日 政令 and the 令和6年9月30日 通知. (3) こども家庭庁's FY2027 budget request (資料1「令和9年度予算概算要求のポイント」, https://www.cfa.go.jp/assets/contents/node/basic_page/field_ref_resources/88749a20-e454-4a5b-9da8-3a32e1788a23/f5ffa79a/20260827_policies_budget_99.pdf, PDF dated 2026-08-27) asks for the expanded allowance to continue unchanged: 「※こども未来戦略により拡充された児童手当の確実な支給のため、２兆663億円を要求」. (4) The 令和8年度税制改正の大綱 (https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2026/20251226taikou.pdf, PDF dated 2025-12-25) contains neither 「扶養控除」 nor 「高校」. The cut to the 高校生年代 dependant deduction that had been discussed was not enacted, so the 2027 deduction figures under F21 are still current law. (5) The Yokohama pages were all re-fetched (最終更新日 2026年6月17日 for 概要 and 請求と届出; 2025年12月2日 for 電子申請; 2026年7月30日 for 年度更新). None changes a fact below. (6) Web searches for 2026 news on a 児童手当 revision found only material about the 2024 expansion. One related newer item does affect this family, but only in the past. Under the one-off 物価高対応子育て応援手当 (2万円 per child, paid in Yokohama from 2026-03-10), the payee is 「「対象児童」の児童手当受給者」, where the child must be 「①令和７年９月分（10月支給）の児童手当支給対象児童」. Source: 横浜市記者発表資料, https://www.city.yokohama.lg.jp/city-info/koho-kocho/press/kodomo/2025/0114ouenteate.files/20260114ouenteate.pdf, 令和８年１月14日. This family had no 認定, so they did not get it. It is not part of a 2027 budget and does not change the key. See "Not decided".

Tooling note: the shared WebSearch budget ran out partway through this check. All later checks used direct fetches of known primary URLs. That covers the 2027年度 就学支援金 and 多子世帯 points: I found no change, but I did not search the news for them.

## The premise

**F1. Since 令和6年10月分, 児童手当 has no income limit and the 特例給付 is abolished. A 1,300万円 salary does not disqualify the family. (source item 1)**
Status: **stands**
- URL: https://www.cfa.go.jp/resources/strategy/kakei-oen (こども家庭庁「子育て世帯の家計を応援」, HTTP Last-Modified 2026-07-23)
- Quote: 「所得によらず、支給の対象となります。」 / 「4か月に1回から、2か月に1回の支給になります。（24年10月から適用、同年12月より支給開始）」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-R6kaisei.html (横浜市, 最終更新日 2025年5月30日)
- Quote (comparison table, 改正前（令和６年９月分まで） / 改正後（令和６年10月分から）): 「所得制限限度額、所得上限限度額あり」 / 「所得制限なし」. Also: 「特例給付は無くなり、受給者全員が上記の支給額に。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=5 (児童手当法 第5条, current text)
- Quote: 「第五条　削除」

**F2. The ward office's answer was right for 2022年10月支給分 to 2024年9月分 and is wrong now. (source item 2)**
Status: **stands** (as history)
- URL: https://www.cao.go.jp/houan/pdf/204/204_2gaiyou.pdf (内閣府 法律案の概要, PDF dated 2021-02-12)
- Quote: 「特例給付の対象者のうちその所得の額が一定の額※以上の者を支給対象外とすることとする（令和4年10月支給分から適用）。」 / 「※児童手当法施行令に、子ども2人+年収103万円以内の配偶者がいる場合は年収1,200万円等となる基準額を規定予定。」
- The end of that period is the Yokohama table under F1 (「改正前（令和６年９月分まで）」).
- Side note in item 2, not in the key: the claim that the husband "was above the cap for any number of dependants" was not re-checked against the old 政令 table, which neither file quotes. The CAO PDF confirms only the 1,200万円 benchmark for two children plus a spouse. A 1,300万円 salary is above that. This does not affect the key.

**F3. Coverage now runs through 高校生年代 (to the first March 31 after reaching 18), so the 16-year-old in 高1 is a 支給対象児童. "上の2人は年齢的に対象外" is wrong for him. (source item 3)**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=3 (児童手当法 第3条第1項)
- Quote: 「この法律において「児童」とは、十八歳に達する日以後の最初の三月三十一日までの間にある者であつて、日本国内に住所を有するもの…をいう。」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai (こども家庭庁「児童手当制度のご案内」, HTTP Last-Modified 2025-07-14)
- Quote: 「児童（0歳から18歳に達する日以後の最初の3月31日までの間にある子をいいます。以下同じ。）を養育している方」

**F4. The 20-year-old is not paid, but she counts toward 「第3子以降」 up to the first March 31 after reaching 22 while the parents carry her living costs. This is not limited to university students. (source item 5)**
Status: **stands**
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/faq/ippan (児童手当Q&A A1, HTTP Last-Modified 2024-10-08)
- Quote: 「「第3子以降」とは、児童及び児童の兄姉等（18歳に達する日以後の最初の3月31日を経過した後の22歳に達する日以後の最初の3月31日までの間にあって親等に経済的負担のある子をいいます。以下同じ。）のうち、年齢が上の子から数えて3人目以降の子のことをいいます。」
- URL: https://www.cfa.go.jp/assets/contents/node/basic_page/field_ref_resources/6a83b8eb-4e0e-4754-b96d-c83e66a6ac81/e935b433/20240809_policies_kokoseido_jidouteate_mottoouen_04.pdf (児童手当制度の概要, PDF dated 2024-08-08)
- Quote: 「大学生に限らず、22歳年度末までの上の子について、親等の経済的負担がある場合をカウント対象とする。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-gaiyou.html (横浜市「児童手当－概要」, 最終更新日 2026年6月17日)
- Quote: 「第一子：２１歳の子は支給対象ではありませんが、第一子と数えます。」 / 「第三子：小学４年生は支給対象で、多子加算が適用されるので、月額30,000円です。」
- Statute: 児童手当法 第6条第2項第2号 (https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=6): 「二十二歳に達する日以後の最初の三月三十一日までの間にある者（児童及び延長者等…を除く。）のうち、個人受給資格者によつて監護に相当する日常生活上の世話及び必要な保護並びにその生計費の相当部分の負担が行われている者」

**F5. Budgeting 児童手当 at 0 yen for 2027 is therefore wrong.**
Status: **stands** (follows from F1, F3, F4 and F7)

## The amount (2027)

**F6. Monthly rates: under 3 = 15,000円. From 3 through 高校生年代 = 10,000円. 第3子以降 = 30,000円. (source item 4)**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=6 (第6条第3項)
- Quote: 「第一項の「三歳未満児童算定額」は一万五千円とし、「三歳以上児童算定額」は一万円とし、「第三子以降算定額」は三万円とする。」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai
- Quote: 「3歳以上 高校生年代まで」 「10,000円（第3子以降は30,000円）」

**F7. 第1子 = the eldest (counted, not paid). 第2子 = the son, 10,000円. 第3子 = the younger son, 30,000円. Total 40,000円 a month, 480,000円 a year. (source item 6)**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=6 (第6条第1項第1号 table)
- Quote (row 第三子以降算定額算定対象者が一人の場合 / 三歳以上支給対象児童がある場合): 「一　三歳以上児童算定額」 「二　第三子以降算定額に、三歳以上支給対象児童の数から一を減じた数を乗じた額」 「三　第三子以降算定額に、三歳未満支給対象児童の数を乗じた額」
- Recomputed: 10,000 + 30,000 × (2 − 1) + 30,000 × 0 = 40,000. 40,000 × 12 = 480,000. The Yokohama example under F4 (21歳 / 高校2年生 / 小学4年生) has the same shape and gives the same split.

**F8. Ages change nothing during 2027. The son is paid through March 2029 (not March 2028). The eldest counts through March 2029. From April 2029 the younger son becomes 第2子 at 10,000円. (source item 13)**
Status: **refuted/needs change** (minor caveat, one clause only). The 2027 conclusion and the son's end date stand. The eldest's end date depends on an inference the key states as fact.
- Statute: 第3条第1項 (児童 to the first March 31 after reaching 18) and 第6条第2項第2号 (兄姉等 to the first March 31 after reaching 22), quoted under F3 and F4.
- Recomputed: a 16-year-old in 高1 in October 2026 was born 2010-04-02 to 2010-10-26. He reaches 18 between 2028-04-01 and 2028-10-25, so his first March 31 after that is 2029-03-31. This stands.
- The eldest: a 20-year-old in 大学2年 with no gap year was born 2006-04-02 to 2006-10-26 and counts through 2029-03-31, which is what the source says. If she had a 浪人 year (not ruled out by the request), she was born 2005-10-27 to 2006-04-01, reaches 22 by 2028-03-31, and counts only through **2028-03-31**. Either way she counts for all of 2027, so 40,000円 a month for all of 2027 still holds.
- Suggested wording for the key: 「長女は浪人・留年がなければ2029年3月まで（いずれにしても2027年中は）カウントされます」.
- The "from April 2029, 10,000円" clause stands for either reading. Under the gap-year reading the drop to 20,000円 a month comes in April 2028, which is outside the 2027 table.

**F9. 児童手当 is not taxed. (source item 14)**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=16 (児童手当法 第16条 公課の禁止)
- Quote: 「租税その他の公課は、児童手当として支給を受けた金銭を標準として、課することができない。」

## The procedure

**F10. Payment is not automatic. A 認定請求 is required, payment starts the month after the claim, and earlier months are lost. (source item 7)**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=8 (第8条第2項)
- Quote: 「児童手当の支給は、受給資格者が前条の規定による認定の請求をした日の属する月の翌月から始め、児童手当を支給すべき事由が消滅した日の属する月で終わる。」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai
- Quote: 「市区町村の認定を受ければ、原則として、申請した月の翌月分の手当から支給します。申請はお早めにお願いします。」 / 「申請が遅れると、原則、遅れた月分の手当を受けられなくなりますので、ご注意ください。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-seikyu.html (横浜市「児童手当－請求と届出」, 最終更新日 2026年6月17日)
- Quote: 「児童手当の支給は、認定請求を行った日の属する月の翌月分から、児童手当を支給すべき事由が消滅した日の属する月までとなっています。」

**F11. The catch-up (claim by 令和7年3月31日 to be paid from 令和6年10月分) has expired. This family was in the group told to apply. (source item 8)**
Status: **stands**
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/mottoouen (こども家庭庁「もっと子育て応援！児童手当」, HTTP Last-Modified 2024-10-01)
- Quote: 「中学生以下の児童を養育しているが、所得上限限度額を超過し、児童手当も特例給付も受給していない方」 / 「児童手当の申請を令和7年3月31日までにしていただいた場合には、令和6年10月分から児童手当が支給されます。」
- URL: https://laws.e-gov.go.jp/api/2/law_data/346AC0000000073 (附則 令和六年六月一二日法律第四七号 第十三条（児童手当法の一部改正に伴う経過措置）第6項)
- Quote: 「施行日から令和七年三月三十一日までの間に児童手当法第七条第一項又は第二項の認定の請求をした者（施行日において新児童手当法第四条第一項各号のいずれかに該当する者に限る。）についての児童手当法第八条第二項の規定の適用については、同項中「受給資格者が前条の規定による認定の請求をした日の属する月の翌月」とあるのは、「令和六年十月」とする。」

**F12. "時効は2年だから2年分さかのぼれる" is wrong. 第23条 limits rights that have already arisen. Under 第8条第2項, no right arises for months before the claim. (source item 9)**
Status: **stands** (the text is verified; the conclusion is a reading of 第8条第2項 with 第23条, and I agree with it)
- URL: https://laws.e-gov.go.jp/api/2/law_data/346AC0000000073 (第23条)
- Quote: 「児童手当の支給を受ける権利及び第十四条第一項の規定による徴収金を徴収する権利は、これらを行使することができる時から二年を経過したときは、時効によつて消滅する。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-denshi.html (横浜市 電子申請, 最終更新日 2025年12月2日). Yokohama applies 第23条 to the accrued rights of existing recipients:
- Quote: 「現況届については、提出しないまま２年間経過すると、「時効」により児童手当の受給権が消滅します。［児童手当法第23条］」

**F13. The claimant is the higher earner (the husband). The account must be in his name. As a 会社員 he claims to 横浜市, not his employer. (source items 11 and 19)**
Status: **stands**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=4 (第4条第3項)
- Quote: 「…当該父若しくは母、未成年後見人又は父母指定者のうちいずれか当該児童の生計を維持する程度の高い者によつて監護され、かつ、これと生計を同じくするものとみなす。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-seikyu.html
- Quote: 「父母ともに所得がある場合は、所得が高い方を請求者として、請求書を記入してください。」 / 「振込口座は、請求者名義の口座に限ります。児童や、請求者の配偶者の口座は指定できません。」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai
- Quote: 「（公務員の場合は勤務先に申請する必要があります。）」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/faq/ippan (A5)
- Quote: 「手当の振込先の預金口座は、原則として、手当を受け取る人が名義人であるものに限ります。」

**F14. How to claim in Yokohama. Online (マイナポータル / パマトコ), by post (the claim date is the day it arrives), or at the ward office's こども家庭支援課. Documents: 認定請求書, an account in the claimant's name, ID, and both spouses' My Number. Add the 確認書 for the eldest, which is allowed even though she lives apart. (source item 12)**
Status: **stands**
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-seikyu.html
- Quote: 「請求書は電子申請・郵送・区役所の窓口で受け付けます」 / 「４．請求者および配偶者の個人番号確認資料」
- Quote: 「郵送請求の場合、請求日は郵便物が「こども青少年局こども家庭課手当給付係」に到達した日となります。消印日ではありませんので、ご注意ください。」 / 「区役所に持参する場合は、区役所の窓口で受け付けた日が請求日となります（開庁日に限ります）。」
- Quote (確認書): 「大学生年代の子（18歳年齢到達後の最初の年度末の翌月から22歳到達後の最初の年度末までの子）を含めて、監護している子が３人以上いる場合に提出が必要です。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-gaiyou.html (postal address and counters)
- Quote: 「〒231-8771」 「横浜市こども青少年局こども家庭課」 「手当給付係（児童手当担当）」. Every ward's counter in the 窓口一覧 is 「こども家庭支援課」.
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-seikyu.files/20260612_11.pdf (確認書, PDF dated 2026-06-05)
- Quote: 「2.　別居しているが、定期的な連絡・面会等をしており、監護相当である」
- Still not decided: which date counts as the claim date for an online application sent on a weekend or holiday. The 電子申請 page does not say.

**F15. Payment months are the even months, each paying the two previous months, around the 15th in Yokohama. 2027 receipts by claim month: accepted in October 2026 → 40,000 in December 2026, then 80,000 × 6 in 2027 = 480,000. November 2026 → 480,000. December 2026 → 440,000. January 2027 → 400,000. (source item 10 and the arithmetic table)**
Status: **stands**. It is time-sensitive: the October row applies only to claims accepted by Fri 2026-10-30.
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=8 (第8条第4項)
- Quote: 「児童手当は、毎年二月、四月、六月、八月、十月及び十二月の六期に、それぞれの前月までの分を支払う。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-gaiyou.html
- Quote: 「※支給日は、支給月の１５日頃になります。」 / 「（支給月の１５日が土曜日・日曜日・祝日である場合には、原則としてその直前の平日になります。）」
- Recomputed: the four rows match 第8条第2項 and 第4項. Weekdays: 2026-12-15 Tue; 2027-02-15 Mon; 2027-04-15 Thu; 2027-06-15 Tue; 2027-08-15 Sun, so the previous weekday, Fri 2027-08-13; 2027-10-15 Fri; 2027-12-15 Wed. 2026-10-31 is a Saturday, so the last counter day in October is Fri 2026-10-30. That leaves five counter days from today (Mon 2026-10-26).
- Keep as flagged: the first payment after a new 認定 can fall outside the regular months (第8条第4項 ただし書: 「前支払期月に支払うべきであつた児童手当…は、その支払期月でない月であつても、支払うものとする。」), so "December 2026" for an October claim is not certain.

**F16. About 1,060,000円 is already lost (October 2024 to October 2026, depending on birth months). (Arithmetic)**
Status: **stands** as a hedged estimate. The key already says 「推計約106万円、生年月による」.
- Recomputed with the source's birth window: October 2024 to March 2025, all three children were 支給対象児童. The 第6条 row 三歳以上支給対象児童が二人以上 gives 10,000 × 2 + 30,000 × 1 = 50,000 × 6 = 300,000. April 2025 to October 2026 gives 40,000 × 19 = 760,000. Total 1,060,000.
- Under the gap-year reading of F8, the eldest was already a 兄姉等 in 2024年度, so every month was 40,000 and the total is 25 × 40,000 = 1,000,000. "約100万円〜106万円" covers both readings.

## The table (the deliverable)

**F17. Rows: income (児童手当), spending (the eldest's tuition and allowance, the son's school debit and juku, the younger son's juku), net. Columns: January to December plus the year. 児童手当 is 80,000 in each even month (480,000 a year). Spending is 147,000 a month plus 500,000 in April and September, 2,764,000 a year. Net 2,284,000.**
Status: **stands**
- Recomputed from the request: 80,000 + 30,000 + 25,000 + 12,000 = 147,000. 147,000 × 12 + 1,000,000 = 2,764,000. 2,764,000 − 480,000 = 2,284,000.
- By month: Feb, Jun, Aug, Oct and Dec at 67,000 each (335,000); Jan, Mar, May, Jul and Nov at 147,000 each (735,000); April 567,000; September 647,000. These sum to 2,284,000.
- The 480,000 assumes a claim accepted by 2026-11-30 (F15).

## Points answers tend to add

**F18. 高等学校等就学支援金: no income limit from April 2026. Private full-time cap 457,200円 a year (up to 38,100円 a month). Public 9,900円 a month. The school receives it and sets it against tuition, and an application is needed. The 2025年度 figures (910万円 cut-off, 590万円, 39万6,000円) are outdated. (source item 15)**
Status: **stands**
- URL: https://www.mext.go.jp/a_menu/shotou/career/05010502/1408866_00004.htm (文部科学省 通知, 令和8年3月31日, 7文科初第2880号)
- Quote: 「所得制限を撤廃し、就学支援金の支給に当たって保護者等の収入の状況を問わないこととしたこと。」 / 「改正法は、令和8年4月1日から施行することとしたこと。」
- URL: https://www.mext.go.jp/a_menu/shotou/mushouka/1342600.htm (文部科学省 Q&A, HTTP Last-Modified 2026-09-14)
- Quote: 「就学支援金の支給上限額が私立高校（全日制）の場合、45万7,200円で引き上げられ」 / 「私立高校の場合、全日制・定時制は最大で月額3万8,100円、通信制は最大で月額2万8,100円が支給されます。」
- Quote: 「公立高校の場合、全日制は月額9,900円」 / 「学校設置者（都道府県や学校法人など）が、生徒本人に代わって受け取り、授業料に充てることになります。」 / 「就学支援金の受給資格を得るための申請が必要です。」
- URL: https://www.mext.go.jp/a_menu/shotou/mushouka/20250411-mxt_shuukyo03-100002595-01.pdf (令和7年度 leaflet). Outdated values: 「年収約910万円以上世帯の高校生」, 「39万6,000円」, and 「590万円」 as the bracket boundary.

**F19. University 多子世帯 reduction (from 2025年度): no income limit while three or more children are dependants. Private university tuition up to 70万円 a year and entrance fee up to 26万円 (national/public: 54万円 and 28万円). It is not cash. Conditions apply (confirmed school, academic tests, assets under 3億円). Apply through JASSO 在学採用 (spring from April, autumn from September). The eldest may qualify, but it is not certain. 給付型奨学金 is out of reach at this income. (source item 16)**
Status: **stands**
- URL: https://www.mext.go.jp/a_menu/koutou/hutankeigen/ (文部科学省, 新着 令和8年9月11日, HTTP Last-Modified 2026-09-30)
- Quote: 「また、令和7年度から、多子世帯の学生に対し所得制限なく、国が定める一定額まで、大学等の授業料・入学金の減免を行っております。」
- URL: https://www.mext.go.jp/content/20260904-mxt_gakushi01-100001505_6.pdf (FAQ, listed as 令和8年9月16日更新, PDF ModDate 2026-09-11)
- Quote: 「「多子世帯」とは、扶養する子供が３人以上の世帯です。」 / 「子供を３人以上同時に扶養している間に、大学等に在学している子供は全員対象となります。」
- Quote (問4-1): 「大学 28万円 54万円 26万円 70万円」 / 「直接、学生本人に現金が支給されるものではありません。」
- Quote: 「多子世帯で授業料等減免の支援を受ける場合は３億円未満」 / 「◆多子世帯の授業料等減免については、所得制限は無し（給付型奨学金の支給は上記の基準額を適用）」 / 「在学採用：春は４月から、秋は９月から」
- The eight-year-old counting toward the three is still an inference, but it is better supported than the source says. The FAQ's own cover diagram counts 「第３子（中学生）」, and its examples count 「第２・３子：高校生以下」.

**F20. 子ども・子育て支援金 is collected with health insurance premiums from the April 2026 premium (employee rate 0.23%). It is a household cost, separate from 児童手当. (source item 18)**
Status: **stands**
- URL: https://www.cfa.go.jp/assets/contents/node/basic_page/field_ref_resources/fb3dbb28-102a-4840-90a5-00ad2e0d117f/47e1295d/20260226policies-kodomokosodateshienkinseido-09.pdf (PDF dated 2026-02-25)
- Quote: 「令和8年4月保険料（5月に給与天引き）より支援金を拠出いただきます。」 / 「子ども・子育て支援金に係る保険料率（支援金率）は0．23％です。」
- URL: https://www.cfa.go.jp/resources/strategy/kakei-oen
- Quote: 「2026年度に創設し、2028年度までに段階的に導入します。医療保険料とあわせて拠出いただきます。」

**F21. 扶養控除 (income tax, ages on 2027-12-31): the eldest at 21 is 特定扶養 at 63万円. The son at 17 is 一般 at 38万円. The younger son at 9 gets none. (source item 17)**
Status: **stands** (current law. The 令和8年度大綱 made no change; see the newer-rule search.)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1180.htm (国税庁 No.1180, [令和8年4月1日現在法令等])
- Quote: 「一般の控除対象扶養親族」「38万円」 / 「特定扶養親族」「63万円」 / 「控除対象扶養親族とは、扶養親族のうち、その年12月31日現在の年齢が16歳以上の人をいいます。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=340AC0000000033;article=2 (所得税法 第2条第1項第34号の3)
- Quote: 「特定扶養親族　控除対象扶養親族のうち、年齢十九歳以上二十三歳未満の者をいう。」
- The gap-year reading of F8 makes the eldest 21 or 22 on 2027-12-31. Either way she is 特定扶養.

## Not decided in this pass
- Whether the family can still claim the one-off 物価高対応子育て応援手当 (2万円 per child, for the son and the younger son) late. Yokohama's release ties it to being a 児童手当 recipient for 令和7年9月分, and this family was not. I found no late-claim route, but I did not open the scheme's own page (`07ouenteate.html`) or check a deadline. It falls outside the 2027 budget either way. If an answer mentions it, it should be described as lost, not as 2027 income.
- Yokohama's 概要 page still says 「受給者の方は毎年６月に現況届を提出する必要があります。」. Its newer 年度更新 page (最終更新日 2026年7月30日) limits the 現況届 to some households, including 「無職、就労中等の大学生年代のお子さんがいる多子加算対象家庭」. A student eldest does not fall in that group. An answer need not mention the 現況届. If it does, "check whether a 現況届 is sent to you each June" is safe.
- The claim date for an online application sent on a weekend or holiday (F14).
- Any 2027年度 change to the 就学支援金 or 多子世帯 amounts. The pages I fetched show none, but I could not search the news once the search budget ran out.
