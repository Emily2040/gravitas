# What counts as Gravitas beating plain DeepSeek Harness

Frozen on 2026-10-22, after round three's grades and before any round-four run. Every later round is judged on exactly these criteria. If one of them turns out to be wrong, I write down why, and the next round is judged on both the old and the new version; a round only counts as a win if it wins on the old version too.

## The test

- Arms: plain DSH (profile gv-plain) against DSH with the dsh-gravitas plugin (gv-grav), both on deepseek-flash, the same headless setup, two runs per arm per request.
- A fresh held-out set every round: everyday requests (see the four-language amendment below for the minimum per language) with a baited premise and room for side claims, never used before and never used to tune anything. Each answer key is checked against official sources and written, with its numbered must-state points, before that round's runs.
- Any tuning happens on a separate tuning set, never on a held-out set.
- One change per round, named before the runs.
- Blind grading by two non-DeepSeek graders, one pair per session, A/B order balanced by design; added-claim notes relabelled blind by two relabellers against the key.
- The noise floor is measured again every round: plain r1 against plain r2 and Gravitas r1 against Gravitas r2, graded the same way.

## A win needs all of these, overall and in Chinese and in English separately

1. Votes: Gravitas wins minus plain wins is above zero and above that round's noise floor (the larger absolute net of the two A/A sets; per language, the A/A net within that language).
2. Each grader on its own gives Gravitas more wins than losses (overall).
3. Length: the median Gravitas answer is no longer than the median plain answer (ratio at most 1.00), and no more than 10% of pairs have a Gravitas answer under 0.6 of plain's length.
4. Vague key points: no more than plain's.
5. Wrong added claims (both relabellers say wrong, with a cite): no more than plain's.
6. Correct key points: at least plain's; wrong key points: no more than plain's.
7. Trap scores under 8: no more than plain's.
8. Hedging: no more than plain on the round-one hedge list, and at most 1.10 times plain on the extended list from round three.

A missing metric fails its gate. A round that passes everything overall but fails in one language is not a win.

## When to stop and ask

I stop and report to Emily if three rounds in a row bring no improvement on these criteria, or before the runs pass the budget she set (see the amendment below), so she can decide on more spend. Each round's run count is told to her before it starts.

## Amendment, 2026-10-22, before any round-four run: all four languages

Emily asked that Japanese and Korean be tested beside Chinese and English. From round four on:
- every held-out set has at least two requests (three where the budget allows) in each of Chinese, English, Japanese and Korean, with keys checked against official sources of that country;
- each request runs with the plugin's language set to the request's language (zh-CN, en, ja or ko), except in a round that tests the language setting itself;
- a win must hold overall and in each of the four languages separately, on every criterion above that can be measured per language (votes and that language's A/A net, length, vague key points, wrong added claims, correct and wrong key points, trap scores, hedging). A round that wins overall but fails in one language is not a win. Results are reported per language.

Why: Gravitas ships in four languages, and round three tested only two. A win in two languages says nothing about the other two.

The spend for the rounds after round three is up to 500 new DeepSeek runs (Emily, 2026-10-22), counted from round four.

## Amendment, 2026-10-23, before any round-four run: hedge lists for Japanese and Korean

The round-one and extended hedge lists cover only Chinese and English, so criterion 8 could not be measured in Japanese or Korean. I add these lists now, before any Japanese or Korean answer exists, and apply them the same way (markers per 1000 characters, mean over answers; first list at most 1.00 times plain, second at most 1.10):
- Japanese, first list: かもしれ, おそらく, 恐らく, たぶん, 可能性があ, と思われ, 断言できませ, ご確認ください, 確認してください. Second list: 一般的に, 通常は, 場合によ, 地域によ, 自治体によ, お問い合わせ, 問い合わせて, 相談してください, 目安.
- Korean, first list: 아마, 일지도, 할지도, 가능성이 있, 확실하지, 확인해 보세요, 확인하시기 바랍니다. Second list: 일반적으로, 보통은, 경우에 따라, 지역마다, 다를 수 있, 문의하, 상담하.
In a round that tests the language setting itself, an answer is counted with the list of the language it is written in.

## Amendment, 2026-10-24, before any round-four run: gates restored, a mixed judge panel

An independent audit found that this file, written after round three's results, was weaker than round three's own criteria. Emily approved restoring what was dropped. From round four on, a win also needs, overall and in each language where it can be measured:
- Length: the median length ratio is at least 0.70 as well as at most 1.00 (round three's floor), so a round that wins by gutting answers does not count.
- Requests: more requests net-positive than net-negative (request as the unit, all of its votes summed).
- Scores: mean total score at least plain's; mean correct and mean useful each no more than 0.5 below plain's.
- Fabricated sources: phrases claiming a source was checked, counted only in answers whose run opened no web page, no more than plain's. If neither arm has such a run, the gate is reported as not measurable rather than as a pass; if only plain has such runs, it passes on the count. The zh and en phrases are round three's list. For Japanese and Korean I add these now, before any Japanese or Korean answer exists, as regular expressions: Japanese によると, によれば, 確認したところ, 調べたところ, 公式(?:サイト|発表|ページ)(?:では|で確認), 照会したところ; Korean 에 따르면, 확인한 결과, 확인해 보니, 조회한 결과, 공식 ?(?:홈페이지|발표|사이트)에서 확인.
- Vague key points: also reported is the A/A noise floor for vague key points (the vague-count difference between plain r1 and plain r2, and between Gravitas r1 and r2, graded the same way), because round three showed the same plain answers drawing 55 and 65 vague marks in two pairings. The gate stays "no more than plain"; the floor is reported beside it.
- Wrong added claims stays "no more than plain" (round three used "fewer"), and the count of wrong added claims per 1000 characters is reported beside it.

Judges: three per pair, one pair per session: Claude Opus 5.5, Claude Sonnet 5.5, and one non-Claude judge, OpenAI gpt-6-astra at high reasoning effort through Codex CLI 0.163.0 (read-only sandbox, no session kept), following the AA-PersonalityBench design of a mixed judge panel. All three get the same grader prompt and the same packet. All three votes count in every vote and key-point gate. Gate 2 (each grader on its own) applies to each of the three judges. Two graders were Claude in round three (kappa 0.68), so their errors were correlated; a third model family lowers that. The two relabellers of added-claim notes stay Opus and Sonnet. The version before this amendment is judged with the Opus and Sonnet grades only, exactly as it was written.

Note, 2026-10-25, before any round-four run: the Codex judge also gets live web search (`codex --search`), still in a read-only sandbox, because the grader prompt lets every judge check claims on official pages and the Claude graders can. The first real Codex call is a single pair, checked before the rest.

Also reported, not gated: format metrics per answer (characters for every language and words for English; list items, meaning lines that start with -, *, + or a number followed by . or 、 or ); bold spans, meaning **...** pairs; headings, meaning lines that start with #), so a length change that only strips formatting is visible.

Why: these were round three's own gates, change 4 targets length, and a length change needs a floor and a usefulness guard most of all. The round is judged on this version and on the version before this amendment; it counts as a win only if it wins on both.

## Amendment, 2026-10-25, before any round-four run: what the cheapest-pass review found

Four reviewers who wrote none of the suite looked for the cheapest way to pass each gate without better answers, and a skeptic tried to refute each finding (review/cheapest-pass-review.json in the round folder; 24 of 34 findings survived). These change the amended version only; the version before the 2026-10-24 amendment stays as written and the round still has to win on both.
- Key points left out: missing key-point marks for Gravitas no more than plain's, overall and per language. Gate 4 counted only vague marks, so turning a loosely stated point into an omitted one passed it, and change 4's sentence ("then stop") pushes that way.
- Length, two more readings: the median of the per-pair ratios (same request and round) must also lie between 0.70 and 1.00, and every length check must also pass on visible text (bold markers, list markers, heading marks, table pipes and blank lines removed, runs of spaces collapsed). Pooled medians let one middle-length request decide a language, and stripping markup alone moved round three's rule-only arm from 1.007 to 0.935.
- Off-list hedging: a third hedge list per language, gated overall at no more than 1.10 times plain and reported per language. Chinese: 不一定, 应该是, 多半, 估计, 似乎, 好像, 联系.{0,8}(?:确认|了解|咨询), 拨打.{0,12}(?:咨询|了解). English: \bcould\b, \blikely\b, \bdepends on\b, \bworth (?:confirming|checking)\b, \bask (?:HR|your)\b, \btypically\b. Japanese: でしょう, 場合があります, ケースによって, 確認しましょう, ご相談ください, ご確認を. Korean: 것 같습니다, 상황에 따라, 달라질 수 있, 확인하세요, 문의하세요.
- Unverifiable specifics: added claims both relabellers call unverified, Gravitas no more than 1.10 times plain overall, reported per language beside the same count's A/A difference, so swapping a hedge for a confident specific nobody can check does not pass.
- Fabricated sources, redefined: source-claim phrases are counted in every final of every run (24 per arm), not only in runs that opened no page, because one fetched page of any kind excused a whole answer and the gate could never fail. A phrase is excused when a law article or document number (第N条, 제N조, N条, 〔YYYY〕N号, a publication or section number) or a URL lies within 25 characters of it, or when the final names a host that a completed web_fetch of the same run opened with HTTP 2xx. Gravitas's unexcused phrases no more than plain's, overall and per language. The cell is always measurable.
- Noise floor: the A/A floor in gate 1 is multiplied by the square root of 2 (the main set has twice the pairs of an A/A set), overall and per language, and tie counts per set are reported.
- Reported, not gated: the share of decisive votes that went to the shorter answer, per judge and per set, including the A/A sets, where any length preference is pure bias.
- Integrity, enforced by the code: every grade and label received is appended to a ledger with its packet's hash, and the grade or label used must be the first valid one for its pair and judge; each packet's answer hash is stored in the pair map and rechecked against the run's final; the verdict refuses unless the run validity report is newer than every run file and lists no run still due a rerun; a rerun happens only for a run the validity check archived; the candidate rule files, expected hashes, scripts and this file are committed before freeze-start, which cannot be overwritten, and Emily gets its hash and commit before the first held-out run.
- Scope: every held-out request carries a baited premise, as the brief asks, so a result speaks for requests of that kind. The write-up says so.

## Where results go

Each round is written up in docs/dsh-ab/round-N with every result, losses as plainly as wins.
