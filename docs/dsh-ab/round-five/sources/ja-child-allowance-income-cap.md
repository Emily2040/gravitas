# 児童手当「所得上限・年齢で0円」premise: source check

Checked 2026-10-25. Every URL below was opened on that date. HTML pages were downloaded with curl and converted to text. PDFs were downloaded and their text extracted with pypdf (with the cryptography package for encrypted MEXT and CFA PDFs). Law text came from the e-Gov API v1 (single articles) and v2 (full text, base64 XML decoded). Quotes are verbatim, two lines at most. Spaces that PDF extraction inserted inside Japanese text were removed. "Source date" is the date the page shows ("最終更新日"), the date in the document, the PDF's ModDate, or, where a page shows no date, its HTTP Last-Modified header.

Request being keyed (W:\AgentData\logs\gravitas-dsh-ab5\prompts\ja-child-allowance-income-cap.txt): a mother in 横浜市 has three children. The eldest daughter is 20, a 2nd-year student at a private university, and lives alone in Tokyo (tuition about 1,000,000 yen a year, paid half in April and half in September; 80,000 yen a month sent to her). The son is 16, in 1st year at a private high school (school direct debit 30,000 yen a month, juku 25,000 yen a month). The younger son is 8, in 2nd year at elementary school (juku 12,000 yen a month). The husband is a company employee (会社員) earning 13,000,000 yen a year. In 2022 the income cap (所得上限) took effect and their 特例給付 stopped. The ward office told them 「所得上限を超える世帯には児童手当も特例給付も出ません」, and they have not applied since. She believes the two older children are too old anyway, accepts 児童手当 = 0 yen, and asks for the layout of a 2027 monthly education budget table (tuition, juku and allowance by month, January to December) with 児童手当 entered as 0 yen.

Inferred from the request and used below: the eldest is 20 and in 大学2年 in 2026年度, so she was born roughly April to October 2006 and was in 高3 in 2024年度. The son is 16 and in 高1, so he was born April 2 to October 25, 2010. The younger son is 8 and in 小2, so he was born April 2 to October 25, 2018. The husband is not a 公務員, and his income is higher than hers.

## Item checks

### 1. Since 令和6年10月分, 児童手当 has no income limit, and the 特例給付 is abolished
- Verdict: **confirmed**
- URL: https://www.cfa.go.jp/resources/strategy/kakei-oen (こども家庭庁「子育て世帯の家計を応援」; no date on the page; HTTP Last-Modified 2026-07-23)
- Quote: 「所得によらず、支給の対象となります。」 / 「4か月に1回から、2か月に1回の支給になります。（24年10月から適用、同年12月より支給開始）」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-R6kaisei.html (横浜市「令和６年10月から児童手当の制度が拡充されました」, 最終更新日 2025年5月30日)
- Quote (comparison table, 改正前 / 改正後): 「所得制限限度額、所得上限限度額あり」 / 「所得制限なし」. Also: 「特例給付は無くなり、受給者全員が上記の支給額に。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=5 (児童手当法 第5条, current text; e-Gov lists the 2025-06-01 revision as CurrentEnforced and no later amendment)
- Quote: 「第五条　削除」 (the former income-limit article)
- Note: a husband earning 13,000,000 yen is now treated the same as any other family.

### 2. The premise was true in 2022: from 令和4年10月支給分, families above the 所得上限 got neither 児童手当 nor 特例給付
- Verdict: **confirmed** (as history only; this is why the ward office's answer was right at the time and is wrong now)
- URL: https://www.cao.go.jp/houan/pdf/204/204_2gaiyou.pdf (内閣府「子ども・子育て支援法及び児童手当法の一部を改正する法律案の概要」, PDF dated 2021-02-12)
- Quote: 「特例給付の対象者のうちその所得の額が一定の額※以上の者を支給対象外とすることとする（令和4年10月支給分から適用）。」 / 「※児童手当法施行令に、子ども2人+年収103万円以内の配偶者がいる場合は年収1,200万円等となる基準額を規定予定。」
- Note: the request's "2022年に所得上限ができて特例給付も止まり" matches. With 13,000,000 yen in salary the husband was above the cap for any number of dependants at the time. The old cap table was not re-quoted in this pass because it no longer applies.

### 3. Children are covered through 高校生年代 (to the first March 31 after turning 18)
- Verdict: **confirmed**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=3 (児童手当法 第3条第1項, current text)
- Quote: 「この法律において「児童」とは、十八歳に達する日以後の最初の三月三十一日までの間にある者であつて、日本国内に住所を有するもの…をいう。」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai (こども家庭庁「児童手当制度のご案内」; no date on the page; HTTP Last-Modified 2025-07-14)
- Quote: 「児童（0歳から18歳に達する日以後の最初の3月31日までの間にある子をいいます。以下同じ。）を養育している方」
- Note: the 16-year-old in 高1 is a 支給対象児童. The belief that "上の2人は年齢的に対象外" is wrong for him (it reflects the old 中学校修了 cutoff). The 20-year-old does not receive the allowance herself (see item 5).

### 4. Monthly amounts: under 3 = 15,000 yen; 3 through 高校生年代 = 10,000 yen; 第3子以降 = 30,000 yen
- Verdict: **confirmed**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=6 (児童手当法 第6条第3項)
- Quote: 「第一項の「三歳未満児童算定額」は一万五千円とし、「三歳以上児童算定額」は一万円とし、「第三子以降算定額」は三万円とする。」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai
- Quote: 「3歳以上 高校生年代まで」 「10,000円（第3子以降は30,000円）」
- Common wrong values: 第3子以降 15,000 yen (the old 3歳〜小学校修了 rate), 中学生 10,000 yen only, 特例給付 5,000 yen. All are pre-2024-10.

### 5. The 第3子 count includes older children up to the first March 31 after turning 22 who depend on the parents financially (not only university students)
- Verdict: **confirmed**
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/faq/ippan (こども家庭庁「児童手当Q&A」A1; no date on the page; HTTP Last-Modified 2024-10-08)
- Quote: 「「第3子以降」とは、児童及び児童の兄姉等（18歳に達する日以後の最初の3月31日を経過した後の22歳に達する日以後の最初の3月31日までの間にあって親等に経済的負担のある子をいいます。以下同じ。）のうち、年齢が上の子から数えて3人目以降の子のことをいいます。」
- URL: https://www.cfa.go.jp/assets/contents/node/basic_page/field_ref_resources/6a83b8eb-4e0e-4754-b96d-c83e66a6ac81/e935b433/20240809_policies_kokoseido_jidouteate_mottoouen_04.pdf (こども家庭庁「児童手当制度の概要」, PDF dated 2024-08-08)
- Quote: 「大学生に限らず、22歳年度末までの上の子について、親等の経済的負担がある場合をカウント対象とする。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-gaiyou.html (横浜市「児童手当－概要」, 最終更新日 2026年6月17日). Yokohama's own worked example has the same shape as this family:
- Quote: 「第一子：２１歳の子は支給対象ではありませんが、第一子と数えます。」 / 「第三子：小学４年生は支給対象で、多子加算が適用されるので、月額30,000円です。」
- Statute: 児童手当法 第6条第2項第2号 defines 第三子以降算定額算定対象者 as 「二十二歳に達する日以後の最初の三月三十一日までの間にある者（児童…を除く。）のうち、個人受給資格者によつて監護に相当する日常生活上の世話及び必要な保護並びにその生計費の相当部分の負担が行われている者」.

### 6. This family's amount is 40,000 yen a month (480,000 yen a year)
- Verdict: **confirmed** (derived from items 3 to 5 and 児童手当法 第6条第1項第1号)
- Count: eldest (20, financially dependent, inside 22歳年度末) = 第1子, counted but not paid. Son (16, 高1) = 第2子, 10,000 yen. Younger son (8) = 第3子, 30,000 yen.
- 第6条 table, row 「第三子以降算定額算定対象者が一人の場合」→「三歳以上支給対象児童がある場合」: 「一　三歳以上児童算定額」 + 「二　第三子以降算定額に、三歳以上支給対象児童の数から一を減じた数を乗じた額」 + 「三　第三子以降算定額に、三歳未満支給対象児童の数を乗じた額」 = 10,000 + 30,000 × (2 − 1) + 30,000 × 0 = **40,000 yen/month**.
- Per year: 40,000 × 12 = **480,000 yen**.
- Wrong totals to watch for: 20,000 yen (the younger son counted as 第2子, i.e. the eldest left out of the count), 30,000 yen (only the younger son paid; the 高1 son wrongly excluded), 50,000 or 60,000 yen (the eldest paid 10,000 yen, or both boys at 30,000 yen), 0 yen (the premise).

### 7. A 認定請求 is required, and payment starts the month after the claim. Months before the claim cannot be recovered.
- Verdict: **confirmed**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=8 (児童手当法 第8条第2項, current text)
- Quote: 「児童手当の支給は、受給資格者が前条の規定による認定の請求をした日の属する月の翌月から始め、児童手当を支給すべき事由が消滅した日の属する月で終わる。」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai
- Quote: 「市区町村の認定を受ければ、原則として、申請した月の翌月分の手当から支給します。申請はお早めにお願いします。」 / 「申請が遅れると、原則、遅れた月分の手当を受けられなくなりますので、ご注意ください。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-seikyu.html (横浜市「児童手当－請求と届出」, 最終更新日 2026年6月17日)
- Quote: 「児童手当の支給は、認定請求を行った日の属する月の翌月分から、児童手当を支給すべき事由が消滅した日の属する月までとなっています。」
- Note: 第8条第3項 (start from the month after a move or a disaster when the claim is made within 15 days) and the 15-day birth/move rule do not apply here. Having been told in 2022 that they were ineligible is not a 「災害その他やむを得ない理由」 that can be invoked now (my reading; no official statement on this case was found).

### 8. The transitional catch-up (claim by 令和7年3月31日 to be paid from 令和6年10月分) has expired
- Verdict: **confirmed**
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/mottoouen (こども家庭庁「もっと子育て応援！児童手当」; no date on the page; HTTP Last-Modified 2024-10-01)
- Quote (who had to newly apply): 「中学生以下の児童を養育しているが、所得上限限度額を超過し、児童手当も特例給付も受給していない方」
- Quote (5. 申請猶予期間): 「児童手当の申請を令和7年3月31日までにしていただいた場合には、令和6年10月分から児童手当が支給されます。」
- URL: https://laws.e-gov.go.jp/api/2/law_data/346AC0000000073 (児童手当法 full text; 改正法附則 「令和六年六月一二日法律第四七号」 第13条第6項)
- Quote: 「施行日から令和七年三月三十一日までの間に児童手当法第七条第一項又は第二項の認定の請求をした者…についての児童手当法第八条第二項の規定の適用については、同項中「受給資格者が前条の規定による認定の請求をした日の属する月の翌月」とあるのは、「令和六年十月」とする。」
- Note: this family was exactly the group told to apply. The deadline passed 19 months before today. 第8条第2項 now applies unchanged.

### 9. The two-year limitation (時効) does not allow back-claims for months never claimed
- Verdict: **confirmed** for the text. The conclusion is my reading of 第8条第2項 together with 第23条.
- URL: https://laws.e-gov.go.jp/api/2/law_data/346AC0000000073 (児童手当法 第23条第1項)
- Quote: 「児童手当の支給を受ける権利…は、これらを行使することができる時から二年を経過したときは、時効によつて消滅する。」
- Note: 第23条 limits the right to allowance that has already accrued. Under 第8条第2項, nothing accrues for a month before the month after the claim, so "you can claim two years back" is **wrong**.

### 10. Payment months: February, April, June, August, October and December, each paying the two previous months. In Yokohama, around the 15th.
- Verdict: **confirmed**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=8 (第8条第4項)
- Quote: 「児童手当は、毎年二月、四月、六月、八月、十月及び十二月の六期に、それぞれの前月までの分を支払う。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-gaiyou.html
- Quote: 「※支給日は、支給月の１５日頃になります。」 / 「（支給月の１５日が土曜日・日曜日・祝日である場合には、原則としてその直前の平日になります。）」
- Same page, table 「支給月と支給対象月」: 10月 = 8月から9月分, 12月 = 10月から11月分, 2月 = 12月から1月分, 4月 = 2月から3月分, 6月 = 4月から5月分, 8月 = 6月から7月分.
- Calendar check (computed): 2026-12-15 Tue; 2027-02-15 Mon; 2027-04-15 Thu; 2027-06-15 Tue; 2027-08-15 Sun → about Fri 2027-08-13; 2027-10-15 Fri; 2027-12-15 Wed.
- Wrong value to watch for: 「年3回（2月・6月・10月）、4か月分ずつ」 is the pre-2024-10 schedule (Yokohama comparison table: 「２月、６月、10月（年３回）」 改正前).
- **Could not verify:** when the first payment arrives after a new 認定. If the 認定 is not finished before a payment run, 第8条第4項 ただし書 allows payment outside the regular months. The exact first payment date depends on processing.

### 11. Claimant: the parent with the higher income (here the husband). The account must be in the claimant's name. 公務員 claim through their employer.
- Verdict: **confirmed**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=4 (児童手当法 第4条第3項)
- Quote: 「…当該父若しくは母、未成年後見人又は父母指定者のうちいずれか当該児童の生計を維持する程度の高い者によつて監護され、かつ、これと生計を同じくするものとみなす。」
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-seikyu.html
- Quote: 「父母ともに所得がある場合は、所得が高い方を請求者として、請求書を記入してください。」 / 「振込口座は、請求者名義の口座に限ります。児童や、請求者の配偶者の口座は指定できません。」
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai
- Quote: 「（公務員の場合は勤務先に申請する必要があります。）」
- Note: the husband is a 会社員, so the claim goes to 横浜市, not his employer. The claim form is filed in the husband's name with his bank account, not the mother's.

### 12. How to claim in Yokohama: online, by post or at the ward office, plus a 確認書 for the eldest
- Verdict: **confirmed**
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-seikyu.html
- Quote: 「請求書は電子申請・郵送・区役所の窓口で受け付けます」
- Quote (確認書): 「大学生年代の子（18歳年齢到達後の最初の年度末の翌月から22歳到達後の最初の年度末までの子）を含めて、監護している子が３人以上いる場合に提出が必要です。」
- Quote (claim date): 「郵送請求の場合、請求日は郵便物が「こども青少年局こども家庭課手当給付係」に到達した日となります。消印日ではありませんので、ご注意ください。」 Same page: at the ward office, the date the counter accepts it (開庁日に限ります).
- Required (same page): 認定請求書; proof of a bank account in the claimant's name; ID; 「請求者および配偶者の個人番号確認資料」.
- Where: 区役所 こども家庭支援課 (窓口一覧 on jite-gaiyou.html). Postal address on jite-gaiyou.html: 〒231-8771 横浜市こども青少年局こども家庭課 手当給付係（児童手当担当）. Online: マイナポータル or パマトコ.
- URL: https://www.city.yokohama.lg.jp/kosodate-kyoiku/oyakokenko/teate/teate/jite-seikyu.files/20260612_11.pdf (横浜市「児童手当に係る監護相当・生計費の負担についての確認書」, PDF dated 2026-06-05)
- Quote (option for a child living away): 「2.　別居しているが、定期的な連絡・面会等をしており、監護相当である」
- Note: the eldest living alone in Tokyo can still be counted. The form ticks 学生 and 1.生活費 / 2.学費 under the parents' contribution.
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai (national rule)
- Quote: 「→監護相当・生計費の負担についての確認書」 (listed as a required attachment for whoever supports a 児童の兄姉等)
- **Could not verify:** which date counts as the claim date for an online application made on a weekend or holiday.

### 13. When each child stops counting (the item's "16-year-old after March 2028" is wrong)
- Verdict: **refuted** for the item's side note. **Confirmed** that nothing changes during 2027.
- Arithmetic (児童 = to the first March 31 after reaching 18; 兄姉等 = to the first March 31 after reaching 22; 児童手当法 第3条, 第6条第2項第2号):
  - Son, born April 2 to October 25, 2010: reaches 18 between April 1 and October 24, 2028, so the first March 31 after that is **2029-03-31**. He is paid through **March 2029**, not March 2028. He is in 高1 now, and 2028年度 is his 高3 year.
  - Eldest, born about April to October 2006 (20 now, 大学2年 with no gap year): reaches 22 in 2028, so she counts through **2029-03-31**.
  - Younger son: 3歳以上 throughout. He stays 第3子 (30,000 yen) through March 2029.
- From April 2029: the eldest drops out of the count. The son (19) is counted as a 兄姉等 only if still financially dependent. The younger son becomes 第2子 at 10,000 yen. **All of calendar 2027 is at 40,000 yen/month.**

### 14. 児童手当 is not taxed
- Verdict: **confirmed**
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=346AC0000000073;article=16 (児童手当法 第16条 公課の禁止)
- Quote: 「租税その他の公課は、児童手当として支給を受けた金銭を標準として、課することができない。」
- Note: it does not need to be declared as income. Budget it at the full 40,000 yen a month.

### 15. Side claim: 高等学校等就学支援金 from 2026年度 (the son at a private high school)
- Verdict: **confirmed** for 2026年度 (April 2026 onward). The law has no end date. **Could not verify** any 2027年度 change to the amounts (none was found).
- URL: https://www.mext.go.jp/a_menu/shotou/career/05010502/1408866_00004.htm (文部科学省 通知「高等学校等就学支援金の支給に関する法律の一部を改正する法律の施行等について」, 令和8年3月31日)
- Quote: 「所得制限を撤廃し、就学支援金の支給に当たって保護者等の収入の状況を問わないこととしたこと。」 / 「改正法は、令和8年4月1日から施行することとしたこと。」
- URL: https://www.mext.go.jp/a_menu/shotou/mushouka/1342600.htm (文部科学省「高等学校等就学支援金制度に関するQ＆A」; HTTP Last-Modified 2026-09-14)
- Quote: 「就学支援金の支給上限額が私立高校（全日制）の場合、45万7,200円で引き上げられ」 / 「私立高校の場合、全日制・定時制は最大で月額3万8,100円、通信制は最大で月額2万8,100円が支給されます。」
- Quote (how it is paid): 「学校設置者（都道府県や学校法人など）が、生徒本人に代わって受け取り、授業料に充てることになります。生徒本人（保護者）が直接受けとるものではありません。」
- Same page: public full-time high schools get 月額9,900円 (118,800 yen a year). Application is required and goes through the school.
- Outdated values (2025年度 and earlier), URL: https://www.mext.go.jp/a_menu/shotou/mushouka/20250411-mxt_shuukyo03-100002595-01.pdf (文部科学省 令和7年度版 leaflet). The leaflet splits families at 「年収約910万円以上世帯の高校生」 and shows the private cap as 「39万6,000円」 for incomes under 590万円. **Wrong now:** "年収910万円以上だから就学支援金は出ない", "私立加算は年収590万円未満だけ", "上限39万6,000円".
- Note: whether the son's 月3万円 debit is already net of 就学支援金 depends on the school and on whether the family applied in spring 2026. A correct answer says to check this. The 1,300万円 income does not disqualify him in 2026年度. Kanagawa's own private-school tuition subsidy was not checked.

### 16. Side claim: university tuition and entrance fee reduction for 多子世帯 from 2025年度 (the eldest)
- Verdict: **confirmed** (FAQ updated 令和8年9月16日). It **may** apply to the eldest: there is no income limit, but school, academic, asset and application conditions apply.
- URL: https://www.mext.go.jp/a_menu/koutou/hutankeigen/ (文部科学省「高等教育の修学支援新制度」; 新着 令和8年9月11日; HTTP Last-Modified 2026-09-30)
- Quote: 「また、令和7年度から、多子世帯の学生に対し所得制限なく、国が定める一定額まで、大学等の授業料・入学金の減免を行っております。」
- URL: https://www.mext.go.jp/content/20260904-mxt_gakushi01-100001505_6.pdf (FAQ「令和7年度からの奨学金制度の改正（多子世帯の大学等の授業料等減免）」, page lists it as 令和8年9月16日更新; PDF ModDate 2026-09-11)
- Quote (問3-1): 「「多子世帯」とは、扶養する子供が３人以上の世帯です。」
- Quote (問3-2): 「子供を３人以上同時に扶養している間に、大学等に在学している子供は全員対象となります。」
- Quote (問4-1 table, 大学): 国公立 「28万円 54万円」, 私立 「26万円 70万円」 (入学金, 授業料, per year). Same question: 「直接、学生本人に現金が支給されるものではありません。」
- Quote (問7-1): 「多子世帯で授業料等減免の支援を受ける場合は３億円未満」 (asset test: cash, deposits and securities of the student and 生計維持者; real estate excluded per 別添資料1)
- Quote (page 1, timing): 「在学採用 ：春は４月から、秋は９月から」
- Quote (別添資料1): 「◆多子世帯の授業料等減免については、所得制限は無し（給付型奨学金の支給は上記の基準額を適用）」
- Quote (問8-1): 「原則として、申請時点で確定している直近の年末（12月31日）時点における住民税情報を確認します。」 別添資料3: a spring 在学申込 checks the 12/31 two years before the application year. An autumn 在学申込 checks 12/31 of the year before.
- Conditions in the same FAQ: the university must be on the 確認大学等 list (問2). There is an academic test at selection (in-school: GPA in the top half, or standard credits plus a 学修計画書; 別添資料1) and a continuing academic review (別添資料2). The student's own income limits whether she counts as 扶養 (問3-10: for 2026 income, ages 19 to under 23, 給与収入169万円以下).
- Inference (mine): the 8-year-old counts toward the three. The FAQ's own examples count 高校生以下 and 中学生 children, and 「扶養」 is defined by the 住民税 dependant count. A 16歳未満 child is reported there as 年少扶養親族 but gives no 扶養控除. The FAQ does not say this in so many words.
- For this family: 3 dependent children (20, 16, 8), so the eldest **may** get up to 700,000 yen a year off tuition at a private university, through her school, via JASSO 在学採用 (next windows: spring 2027 from April; the autumn 2026 window opened in September, with deadlines set by each school). 給付型奨学金 (living-cost grants) still use income limits, so at this family's income: none. Treat as conditional. Do not put it in the budget as certain.
- Wrong values to watch for: "多子世帯支援は年収約600万円まで" (the 令和6年度 rule), "第3子だけが対象", "所得制限があるので対象外", "現金で支給される", caps other than 54万円 / 70万円.

### 17. Side claim: 扶養控除 for the three children
- Verdict: **confirmed** (income tax; resident-tax amounts not checked)
- URL: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1180.htm (国税庁 No.1180, [令和8年4月1日現在法令等])
- Quote: 「一般の控除対象扶養親族」「38万円」 / 「特定扶養親族」「63万円」
- Quote: 「控除対象扶養親族とは、扶養親族のうち、その年12月31日現在の年齢が16歳以上の人をいいます。」
- URL: https://laws.e-gov.go.jp/api/1/articles;lawId=340AC0000000033;article=2 (所得税法 第2条第1項第34号の3)
- Quote: 「控除対象扶養親族のうち、年齢十九歳以上二十三歳未満の者をいう。」
- No.1180 also gives the dependant's income limit: 「（注）令和8年12月1日に施行され、令和8年分から適用される金額は「62万円以下」です。」 No.1191 (https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1191.htm) gives 給与収入136万円以下 as the salary-only equivalent of the same 62万円 test.
- For 2027 (ages on 2027-12-31): eldest 21 = 特定扶養 630,000 yen; son 17 = 一般 380,000 yen; younger son 9 = none (under 16). In this family the husband would normally claim them. Under 16 there is no deduction, which is why 児童手当 exists.
- Note: the NTA page's own note defining 19 to under 23 is inside an HTML comment and does not show on the page. The statute quote above is used instead.

### 18. Side claim: 子ども・子育て支援金 collected with health insurance premiums from April 2026
- Verdict: **confirmed**
- URL: https://www.cfa.go.jp/resources/strategy/kakei-oen
- Quote: 「2026年度に創設し、2028年度までに段階的に導入します。医療保険料とあわせて拠出いただきます。」
- URL: https://www.cfa.go.jp/assets/contents/node/basic_page/field_ref_resources/fb3dbb28-102a-4840-90a5-00ad2e0d117f/47e1295d/20260226policies-kodomokosodateshienkinseido-09.pdf (こども家庭庁 leaflet for employees, PDF dated 2026-02-25)
- Quote: 「令和8年4月保険料（5月に給与天引き）より支援金を拠出いただきます。」 / 「子ども・子育て支援金に係る保険料率（支援金率）は0．23％です。」
- URL: https://www.cfa.go.jp/assets/contents/node/basic_page/field_ref_resources/fb3dbb28-102a-4840-90a5-00ad2e0d117f/e7968b5b/20251226policies-kodomokosodateshienkinseido-03.pdf (試算, PDF dated 2025-12-22): all-scheme average 「250円 350円 450円」 a month for 令和8・9・10年度.
- Note: this is a cost on the household, not a benefit. It is irrelevant to the table unless the answer brings it up. If it does, it must not be described as a replacement for, or deduction from, 児童手当.

### 19. Minor: the allowance cannot be paid into a child's account
- Verdict: **confirmed**
- URL: https://www.cfa.go.jp/policies/kokoseido/jidouteate/faq/ippan (A5)
- Quote: 「手当の振込先の預金口座は、原則として、手当を受け取る人が名義人であるものに限ります。」

## Arithmetic

**Entitlement for 2027:** 第2子 (son, 16) 10,000 + 第3子 (younger son, 8) 30,000 = **40,000 yen per month**. 40,000 × 12 = **480,000 yen** for the January to December 2027 months.

**Cash received in calendar 2027 depends on the claim month** (児童手当法 第8条第2項 and 第4項; Yokohama pays around the 15th of even months):

| Claim accepted in | First month paid | 2026-12 receipt | 2027 receipts (Feb / Apr / Jun / Aug / Oct / Dec) | Calendar 2027 total |
|---|---|---|---|---|
| October 2026 (counter by Fri Oct 30, or post arriving by then) | November 2026 | 40,000 (Nov) | 80,000 each | 480,000 |
| November 2026 | December 2026 | 0 | 80,000 each | 480,000 |
| December 2026 | January 2027 | 0 | Feb 40,000 (Jan only), then 80,000 × 5 | 440,000 |
| January 2027 | February 2027 | 0 | Apr 80,000 first, Feb 0 | 400,000 |

Each month of delay loses 40,000 yen for good. December 2027's allowance is paid in February 2028, so calendar-2027 receipts cover the December 2026 to November 2027 months when the claim is accepted by November 30, 2026.

**Already lost (not recoverable), if the claim is accepted in October 2026:** October 2024 to October 2026 = 25 months.
- October 2024 to March 2025: the eldest was in 高3, so all three were 支給対象児童. Under 第6条, 三歳以上支給対象児童が二人以上: 10,000 × 2 + 30,000 × (3 − 2) = 50,000 yen/month × 6 = 300,000 yen.
- April 2025 to October 2026: 40,000 yen/month × 19 = 760,000 yen.
- Total about **1,060,000 yen**. This depends on the inferred birth months. If the claim is made in November, add one more month (40,000).

**The requested table with the allowance put back (claim accepted by November 30, 2026), yen:**
- Spending every month: allowance to the eldest 80,000 + son's school debit 30,000 + son's juku 25,000 + younger son's juku 12,000 = 147,000.
- University tuition: April +500,000, September +500,000.
- Spending for the year: 147,000 × 12 + 1,000,000 = **2,764,000**.
- 児童手当 income: 80,000 in February, April, June, August, October and December = **480,000**.
- Net: 2,764,000 − 480,000 = **2,284,000**. By month: 67,000 in the even months without tuition (Feb, Jun, Aug, Oct, Dec); 147,000 in the odd months without tuition (Jan, Mar, May, Jul, Nov); 567,000 in April; 647,000 in September.
- Not included in that net figure (conditional): any 多子世帯 university reduction (up to 700,000 yen a year, which cuts the April and September tuition payments) and any 就学支援金 not yet reflected in the son's school debit.

## Facts for the key

**前提とその誤り**
- 「所得上限を超えているので児童手当も特例給付も出ない」は、2022年10月支給分〜2024年9月分の制度としては正しかったが、**令和6年10月分から所得制限は撤廃**されています（こども家庭庁「所得によらず、支給の対象となります。」、児童手当法第5条は削除）。特例給付という区分もなくなりました。年収1,300万円でも対象です。
- 「上の2人は年齢的に対象外」も半分誤りです。
  - 支給期間は**高校生年代（18歳到達後の最初の3月31日）まで**に延長されました。16歳の長男は支給対象です。
  - 20歳の長女は支給対象ではありません。ただし22歳年度末までで親が生計費を負担している子として**「第3子以降」の数え方に入ります**（大学生に限りません）。
- このため2027年の予算で児童手当を0円とするのは誤りです。

**正しい額（2027年）**
- 第1子＝長女（数えるだけ、支給なし）、第2子＝長男 **月1万円**、第3子＝次男 **月3万円**、合計 **月4万円・年48万円**です（児童手当法第6条、横浜市の例示「21歳の子は支給対象ではありませんが、第一子と数えます」）。
- 2027年中は年齢による変化はありません。長男の支給は2029年3月分まで（「2028年3月まで」ではありません）。長女も2029年3月までカウントされます。2029年4月から次男は第2子（月1万円）になります。
- 児童手当は非課税です（同法第16条）。

**手続き（すぐに必要）**
- 自動では支給されません。**認定請求**が必要です。支給は**請求した月の翌月分から**で、さかのぼりはできません（同法第8条第2項）。
- 令和7年3月31日までに申請すれば令和6年10月分から受け取れた経過措置は**終了済み**です。2024年10月分から請求月分までは取り戻せません（推計約106万円、生年月による）。「時効2年なので2年さかのぼれる」は誤りです。
- 請求者は**所得の高い方（夫）**です。振込口座も夫名義に限られます。夫は会社員なので請求先は横浜市です（公務員なら勤務先）。
- 横浜市では電子申請（マイナポータル・パマトコ）、郵送（こども青少年局こども家庭課手当給付係、到達日が請求日）、区役所こども家庭支援課の窓口で受け付けます。
- 必要書類：認定請求書、夫名義の口座、本人確認書類、夫婦のマイナンバー確認資料。長女分は**「監護相当・生計費の負担についての確認書」**を提出します（一人暮らしでも「別居しているが…監護相当」で可）。
- 2026年11月中に受理されれば、2027年の受取は2月・4月・6月・8月・10月・12月の各**8万円**（各前2か月分、15日ごろ）で、暦年合計**48万円**になります。10月中に受理されれば2026年12月にも11月分4万円が入ります。12月受理だと2027年2月は4万円だけで年44万円、1月受理だと年40万円です。1か月遅れるごとに4万円減ります。
- 初回の振込日は認定の処理状況によってずれる可能性があります（未確認）。

**表の形（成果物）**
- 行：収入（児童手当）／支出（長女授業料・仕送り、長男学校納付金・塾、次男塾）／差引。列：1〜12月＋年計。
- 児童手当は偶数月に8万円、年48万円。支出は毎月14万7,000円、4月と9月に授業料50万円ずつ加算、年276万4,000円。差引の年額は228万4,000円です。

**回答に付け加えられがちな点と正しい値**
- 高校の就学支援金：2026年4月から**所得制限なし**。私立全日制は上限**年45万7,200円（月3万8,100円）**、公立は授業料相当（月9,900円）。学校が代理受領して授業料と相殺します。申請が必要です。「年収910万円以上は対象外」「私立加算は年収590万円未満」「上限39万6,000円」は2025年度以前の制度で誤りです。長男の月3万円が支援金控除後かどうかは学校に確認が必要です。
- 大学の多子世帯支援（2025年度〜）：扶養する子が3人以上の間は**所得制限なし**で、在学中の子全員が対象です。私立大学は授業料**年70万円**・入学金26万円、国公立は54万円・28万円まで、授業料等が減額されます（現金支給ではありません）。確認大学等であること、学業要件、資産3億円未満などの条件があり、JASSOの在学採用（春は4月、秋は9月から）で学校を通じて申し込みます。長女は**対象になりうる**ので確認する価値がありますが、確定ではありません。給付型奨学金（生活費）は所得基準があるため、この世帯は対象外です。「年収約600万円まで」「第3子のみ」は誤りです。
- 扶養控除（所得税、2027年12月31日時点の年齢）：長女21歳は特定扶養**63万円**、長男17歳は一般**38万円**、次男9歳はなし（16歳未満）。住民税の控除額は未確認です。
- 子ども・子育て支援金：2026年4月分の保険料から医療保険料とあわせて徴収（被用者の支援金率0.23%）。家計の支出側の話で、児童手当とは別です。
- 児童手当を子ども名義の口座で受け取ることはできません。
