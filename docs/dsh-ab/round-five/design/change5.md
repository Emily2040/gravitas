# Change 5 (round five candidate): exact text and where it goes

## Title

"Plainly" keeps what was found: a limit stays with its figure, a safe pick is written as a pick, and the limit replaces a flat word instead of adding text (one sentence in rule item 4, all four languages)

## Where

Rule item 4 of a copy of W:\Projects\gravitas-claim-check\dist\<lang>\gravitas\rules\AGENTS.md (line 13 in each language). The new text goes between the "thinly known" sentence and the "evidence counts" sentence:
- en: after "...the thinly known or pattern-built checked or widened to what they can confirm." and before "Evidence counts only if independent...".
- zh-CN: after "…要么把说法放宽到用户自己能去确认的程度。" and before "证据只有同时做到两点才算数…".
- ja: after 「…相手が確かめられる程度まで主張の幅を広げます。」 and before 「根拠として数えるのは…」.
- ko: after 「…사용자가 확인할 수 있는 정도까지 범위를 넓혀 말합니다.」 and before 「근거로 치는 것은…」.

Nothing else in the rule changes.

Delivery follows round four's c4 pattern:
- Candidate files: W:\AgentData\logs\gravitas-dsh-ab5\rules\change5\{en,zh-CN,ja,ko}.md.
- Loaded through overlays c5-<lang>.yml: language = the request's language, alwaysOnRule true, claimCheck false, ruleFile = that file.
- Hashes recorded in expected-rule-hashes.json and committed before freeze-start.
- ruleText() in dsh\index.js still appends dsh\platform\<lang>.rule.md, unchanged. The plugin code is unchanged.
- Arm name: gv-grav-c5.

The two revisions allowed after pass 1 are already defined, so neither needs new translation:
- R-b deletes the parenthetical in each language.
- R-a moves the whole inserted text, unchanged, to the end of item 7's technical-writing sentence: en after "never less content."; zh after "每个步骤、数字和注意事项都要保留。"; ja after 「手順、数値、注意点はすべて残します。」; ko after 「단계, 수치, 주의 사항은 모두 남깁니다.」.

## Text

### en
Plainly never means more absolute than what it found: a limit on a figure, date, deadline or rule that the pages it opened or its own working show (a maximum as "up to", a fact of theirs not yet known as "if") stays in the sentence that states it, in a step too; a date or amount chosen to be safe is given as that choice beside the rule it is safer than, with no new figure or reason; and each limit replaces a flat absolute or a bare "may" or "probably", adding no sentence or branch.

### zh-CN
“直接说”不等于说得比查到的更绝对。数字、日期、期限或规定，只要为这次回复打开的网页或自己的分析显示它有限定（上限写成“最多”，用户还没说明的情况写成“如果……”），这个限定就留在说出它的那句话里，写在步骤里也一样。为了稳妥而选的日期或金额，写成为稳妥而作的选择，并在旁边写出实际规定，不另加数字或理由。限定用来替换说得过满的字眼，或只挂一个“可能”“大概”的说法，不另加句子或分支。

### ja
言い切るとは、見つけた以上に断定することではありません。数値、日付、期限、規則について、この返答のために開いたページや自分の検討で限定が分かっていれば（上限は「最大」「〜まで」、相手の事情でまだ分からないことは「〜なら」）、その限定は、それを述べる文の中に残します。手順の中でも同じです。念のために選んだ日付や金額は、念のための選択として書き、実際の規則をその隣に示します。新しい数値や理由は加えません。限定は、言い過ぎの言葉や、条件を示さずに「かもしれません」「たぶん」とだけ添えた言い方の代わりに書き、文や枝分かれは増やしません。

### ko
얼버무리지 않고 말한다는 것이 찾아낸 것보다 더 단정한다는 뜻은 아닙니다. 수치, 날짜, 기한, 규정에 대해 이번 답을 위해 연 페이지나 스스로 따져 본 내용에서 한도나 조건이 드러났다면(상한은 '최대', '~까지'로, 사용자의 사정 가운데 아직 모르는 것은 '~라면'으로 씁니다), 그 한도나 조건은 그것을 말하는 문장 안에 남깁니다. 단계 안내 안에서도 마찬가지입니다. 안전하게 하려고 고른 날짜나 금액은 그런 선택이라고 밝히고 실제 규정을 그 옆에 적되, 새 수치나 이유는 덧붙이지 않습니다. 한도나 조건은 지나치게 단정한 말이나, 조건 없이 '아마', '~일지도'만 붙인 말을 대신해 쓰고, 문장이나 갈래를 늘리지 않습니다.

## Mechanism

On gv-grav-base, deepseek-flash researches more than plain (351 vs 267 searches and fetches, 679K vs 502K thinking characters). Then, at write time, it states rules flatter than its own evidence:
- a maximum becomes a fixed date ("through March 15", where its own thinking said "up to 2½ months");
- a safe pick becomes the rule ("I'll stick with 'December 31 to be safe'", then the final drops "to be safe");
- an open input is settled by assumption ("7~9월 석 달이면 이 요건을 넘고", and the age assumed silently for 150일);
- ≈0 becomes 0円.

What the sentence does:
- It ties the duty to what is visibly in context: a limit that the pages it opened, or its own working, show for a figure, date, deadline or rule. So the model cannot exempt itself by rating the point as settled, which is how it dodged round two's "verify or delete".
- It opens by redefining the word base quotes as its licence (plainly, 直接说, 言い切ります, 얼버무리지 않고), so the licence and the limit are read together.
- "In a step too" covers the STE compression in item 7, where 5 of the 7 cut nuances sat.
- The safe-pick clause turns the triple-marked 529 error into "aim for December 31 to be safe; the federal deadline is April 15, 2027". It adds no new reason, which keeps the unverified count from growing.
- The replacement clause ("each limit replaces a flat absolute or a bare may/probably, adding no sentence or branch") makes the edit length-neutral, and it replaces exactly the bare softeners that make up base's first-list gap.

The scope words it asks for are on none of the three hedge lists in any language: up to, if, 最多, 如果, 最大, まで, なら, 최대, 까지, 라면.

It asks for no new check, no deletion and no length change. Those are the levers that failed in rounds two, three and four.

## Predicted effects

These estimates are for a held-out set like round four's, three judges, 24 pairs.

- **Wrong key points:** 34 falls to about 22-28, against plain's steady 18-19. The nuance-cut and premise-flip classes (11 base items, 10 base-only) should roughly halve. The memory-only items stay (ko-jeonse 무료 at 3 marks, zh-sick 70%). The gate probably still fails overall; chance of passing about 30%.
- **Wrong added claims:** 100 vs 78 falls to about 84-92 vs about 78. The over-generalisation, deadline and safe-pick classes shrink; memory-only side claims stay. The result sits inside the A/A spread of about ±16-21 notes; chance of passing about 35%.
- **First-list hedging:** the rate ratio goes from 1.14 to about 0.95-1.10, with softeners replaced by conditions.
- **Third-list hedging:** about 1.2-1.4, unchanged, because it is keigo in drafts and Korean 확인하세요. Likely still fails.
- **Second list:** flat, with a risk of a small rise.
- **Key points, other marks:**
  - correct 338 rises to about 342-350;
  - vague moves from 142 to about 138-152, a risk because English has a margin of 1;
  - missing moves from 32 to about 30-36.
- **Length:** visible pooled 0.988 moves to about 0.97-1.01, a real risk. English (1.08) and Korean (1.16) stay over 1.00.
- **Unverified claims:** about 105-120, against a bound of about 124.
- **Votes:** about 44-48 of 72, straddling the √2 floor of about 17. Gate cells passed rise from 31 of 52 to about 33-37.
- **Overall:** a held-out win stays unlikely, about 5-10%. Per-language votes in zh, en and ko, the third hedge list and en/ko length fail whatever the sentence does. The realistic yield is a test of whether base's flattening excess can be removed without collateral loss.

**Tuning:** if the change works, its flattened-or-wrong count on the 42 limited key points falls below both base runs and to plain's level, with length, vague, missing and hedges flat. Under no effect, the chance of a GO is about 1 in 20.

**Runs:** 24 tuning plus 72 held-out = 96 DeepSeek runs, leaving 325 of 421; 12 or 24 if tuning abandons. Grading uses about 168 one-answer Claude grader sessions in tuning; held-out grading is the same as round four's, 3 judges per pair.

## Risks

- Ignored, as in round two: the trigger depends on the limit being in pages or thinking. Specifics written from memory that the model never questions are out of reach: 확정일자 무료, K-12 $10,000, 子の看護休暇, zh-sick 70%, which are about 30 of base's 50 distinct wrong claims. So wrong added claims may stay above plain.
- Drags doubt in from thinking: base runs carry a median of about 35 open-point markers each ('not sure', 'to be safe', 可能). 'Its own working' could pull them into the answer as limits, making answers longer and vaguer. English vague has a margin of 1 (29 vs 30).
- Condition spraying: 'up to' or 'if' attached to fixed facts (for example 'up to 600원'), or more 'If X:' lines. Base already writes more conditionals than plain: 如果 57 vs 35, なら/場合は 33 vs 20.
- Blur instead of correction: if extra wrong marks turn into vague marks rather than correct ones, the vague gate fails (diagnosis 2's arithmetic: 158 vs 156).
- Length: visible pooled headroom is 1.2% (0.988). The replacement clause may not hold, and English and Korean are already over 1.00.
- Hedge displacement: doubt moved onto second- or third-list words the rule does not name (generally, depends on, 一般, 場合によ, 경우에 따라). Japanese already fails the second list on 2 vs 3 markers.
- The safe-pick clause makes the model state an 'actual rule' its notes never settled (529 r1 notes end on December 31). That adds unverified or wrong claims, even with 'no new figure or reason'.
- Softened premise corrections lower trap scores, where Japanese is 2 vs 2 and Chinese 0 vs 0 (no margin).
- The tuning prompts are the ones the change was built from, so tuning overstates the effect. Round two fixed 2 of 4 named errors on its source prompts, then lost on new ones. The decision therefore counts all 42 limited key points and requires beating both base runs, not just the named failures disappearing.
- Instrument: a single Claude grader marks few wrong key points (round four: Opus 4 base vs 3 plain over 24 answers; Codex 26 vs 14). The decision rests on a new item-level tally of limited key points, which must be calibrated before any run.
- Noise: at 24 pairs the predicted held-out gains are at or below the A/A floors (about 21 wrong-claim notes, about 15.6 wrong key-point marks). A real effect can read as a fail, and the reverse.

## Runner-up

Notes check, as a plugin mechanism redesigned along its critics' lines. It would compare the draft with the run's own notes and steer once, rewriting at most 2 sentences with no deletion. It needs:
- a length-neutral steer;
- second- and third-list words banned in all four languages;
- 'condition' items only when the notes quote an explicit limit word;
- a later note that chooses to simplify counted as a safe pick, not as a settled conclusion;
- offline calibration on the 48 round-four Gravitas finals.

It goes at the same failure (nuance in hand, then cut) through the steer channel, which this model is known to act on. It is the next candidate if this sentence is abandoned because it was read but had no effect.

## Rejected

- Delete the 'settled knowledge plainly' exit from rule item 4: Only 1 of 24 base runs quotes the clause at a check decision (ja-part r2), and that check was on a correct point. The wrong side details there (子の看護休暇, 확정일자 무료) never reached a check decision. Plain uses the same settled-knowledge reasoning without the clause. c4, which kept the clause, reproduced none of the targeted claims yet had the same excess (103 vs 81). English has the mildest wording and the largest excess; Korean has the strongest wording and already beats plain on wrong claims (9 vs 11). Deleting it also risks the flat, correct claims that give base +16 correct and −11 missing in the four target cases, and the predicted gain is inside the A/A floor.
- "Plainly" keeps the condition (design 2 as written): Its core is kept, but not as written. The 'year that applies', 'exception that applies' and 'names what decides it' limbs ask for new specifics from memory, which hits the unverified gate with about 12 notes of headroom. They invite listed or dependence words (depending on, 视…而定, 場合によ, 경우에 따라), and a year label already passed for a check in the FSA $660/$680 case. It also had no length-neutral clause, and visible length headroom is 1.2%.
- Notes check: send the reply back to what its own notes concluded: Under its own 'the later note counts' rule, most named targets cannot be listed: in FSA r1, Medicare r2, ko-unemp r1 and 529 r1 the notes settle on the flat version. That leaves 2 to 3 of 6, below its own 4-of-6 bar. Round-three revisions grew a median 3.6% even with a 'not longer' clause, and with fire rates near 90% that breaks visible length. The critic is English-only, comparing English notes with CJK replies, the ja and ko steers are unwritten, and it adds a model call per turn. Its own best-case forecast leaves all three failing gates failing.
- Plainly is never wider than the source (design 4 as written): 'Keep the source's limit' has no source for most targeted memory claims: none of the FSA pages mentions the grace period or run-out. ko-unemp kept its source's limit and erred in applying it. 'A page opened this turn outranks memory' gives weight to stale official pages (easylaw 3년/3천만 is in the tuning set), and Medicare r2 saw no conflict. The safer-option limb as written invites unverified processing-time reasons. 'Wider' collides with the rule's own 'widened', which means made less precise. Its trigger idea, evidence in hand, is kept.
- Amend the third hedge list (keigo でしょうか, Korean 확인하세요): This is a criteria change, not a Gravitas change. WIN_CRITERIA counts a round as a win only if it also wins on the old version, so amending the list cannot rescue round five. It should be raised with Emily separately, as a known reason the round is unlikely to be a win.
