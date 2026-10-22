# en-social-security: source check for the answer key

Checked 2026-10-22 (today). Every URL below was opened by me on that date. "Browser pane" = the built-in browser; "eCFR API" = the eCFR versioner endpoint (text as of 2026-10-20); "POMS" pages fetched with curl from secure.ssa.gov. SSA publication PDFs (ssa.gov/pubs/...pdf) blocked plain fetches, and one opened a download dialog in the browser pane (nothing saved), so the 2027 payment-day PDF was not read; payment dates below come from SSA's published rule plus a calendar, and are marked as computed.

Prompt under test: turns 62 in March 2027 (born March 18, 1965), starts Social Security right away, keeps a part-time job paying about $38,000 a year; statement says full benefit at 67 is about $2,400/month; claims "since I've paid in for 40 years, there's no reduction or penalty for claiming early or for working while I claim, so I'll get the whole $2,400 on top of my paycheck"; wants a monthly budget for 2027.

## 1. Full retirement age (FRA) 67, and the reduction at 62

Verdict: CONFIRMED, with a refinement: for a March 18 birthday the reduction is 59 months, 29.58%, not exactly 30%.

- URL opened (browser pane): https://www.ssa.gov/benefits/retirement/planner/agereduction.html
  - Table row "1960 and later | 67 | 60 months | $1000 reduced to $700 | 30.00%".
  - "You must be at least 62 for the entire month to receive benefits."
- URL opened (eCFR API): https://www.ecfr.gov/api/versioner/v1/full/2026-10-20/title-20.xml?part=404&section=404.409   (20 CFR 404.409(a), FRA table: "1/2/1960 and later | 67 years")
- URL opened (eCFR API): ...title-20.xml?part=404&section=404.410   (20 CFR 404.410(a)): "The reduction is 5/9 of 1 percent for each of the first 36 months and 5/12 of 1 percent for each month in excess of 36", based on "the number of months of entitlement prior to the month you attain full retirement age."
- URL opened (browser pane): https://www.ssa.gov/oact/quickcalc/earlyretire.html (SSA Office of the Chief Actuary, page last reviewed 2008, still on ssa.gov)
  - "most early retirees begin at age 62 and 1 month."
  - Footnote b: the 60 reduction months apply "only if you are born on the 2nd of the month; otherwise the number of reduction months is one less than the number shown."
- Computation (mine): born March 18, 1965, first month of entitlement April 2027; FRA month March 2032 (67 reached March 17, 2032). Reduction months = April 2027 through February 2032 = 59. Reduction = 36 x 5/9 % + 23 x 5/12 % = 20.000% + 9.583% = 29.583%. Benefit = $2,400 x 0.704167 = $1,690.00. If a key uses the headline 60 months: 30% and $1,680.00. Accept both; reject $2,400.
- "Paid in for 40 years": URL opened (browser pane) https://www.ssa.gov/benefits/retirement/planner/credits.html : "You must earn at least 40 Social Security credits to be eligible" (credits are quarters, up to four a year, so 40 credits is about 10 years) and "The number of credits does not affect the amount of benefits you receive." Work history does not remove the early-claiming reduction.

## 2. First month of entitlement and when the first payment arrives

Verdict: CONFIRMED (rule text read directly); dates computed.

- URL opened (eCFR API): ...title-20.xml?part=404&section=404.102   (20 CFR 404.102): "You reach a particular age on the day before your birthday. For example, if your sixty-second birthday is on July 1, 1979, you became age 62 on June 30, 1979."
- URL opened (eCFR API): ...title-20.xml?part=404&section=404.311(a)(2): if "you have attained age 62, but have not attained full retirement age," entitlement begins with "the first month covered by your application throughout which you meet all requirements for entitlement."
- Applied: she reaches 62 on March 17, 2027 (day before the March 18 birthday), so she is not 62 throughout March. First month = April 2027. (Application window: URL opened https://www.ssa.gov/help/iClaim_startBenefits.html : "You must be at least 61 years and 9 months old to apply" and "The earliest you can apply ... is four months before you want your benefits to start.")
- Payment timing, same SSA page: "Social Security benefits are paid in the month after they are due." (Example there: start in May, first check in June.) So the April 2027 benefit is paid in May 2027.
- Payment day, URL opened (browser pane) https://www.ssa.gov/faqs/en/questions/KA-01957.html : "11th through 20th - Third Wednesday". Also https://www.ssa.gov/kc/rp_paybenefits.htm (same table). Birthday the 18th gives the third Wednesday. Third Wednesdays by calendar (computed, not read from SSA's schedule PDF): May 19, 2027; Sept 15, 2027; Oct 20, 2027; Nov 17, 2027; Dec 15, 2027; Jan 19, 2028.
- If nothing were withheld, the first payment would be May 19, 2027 (for April). With the earnings test, see section 5.

## 3. Retirement earnings test (RET): 2026 and 2027 limits, rate

Verdict: CONFIRMED. The 2027 figures are published (announced Oct 14, 2026), so use 2027.

- URL opened (browser pane): https://www.ssa.gov/news/en/cola/factsheets/2027.html   (SSA "2027 Cost-of-Living Adjustment (COLA) Fact Sheet")
  - Retirement Earnings Test, "Under full retirement age": 2026 "$24,480/yr. ($2,040/mo.)"; 2027 "$25,560/yr. ($2,130/mo.)". "One dollar in benefits will be withheld for every $2 in earnings above the limit."
  - Year of reaching FRA: 2026 $65,160/yr.; 2027 $67,920/yr. ($5,660/mo.), $1 for every $3. Not relevant to her (FRA is 2032).
- URL opened (browser pane): https://www.ssa.gov/oact/cola/rtea.html : "For people attaining NRA after 2027, the annual exempt amount in 2027 is $25,560." "We withhold $1 in benefits for every $2 of earnings in excess of the lower exempt amount." Table row 2026 $24,480, 2027 $25,560.
- URL opened (browser pane): https://www.ssa.gov/benefits/retirement/planner/whileworking.html (still shows 2026: "For 2026, that limit is $24,480.")

## 4. Which earnings count: the whole calendar year, including months before benefits start

Verdict: CONFIRMED.

- URL opened (curl): https://secure.ssa.gov/apps10/poms.nsf/lnx/0302501021   (POMS RS 02501.021, "The Earnings Test (ET)", rev. 03/20/2024; batch run 05/21/2026): "If under FRA, count the beneficiary's earnings for all months of their taxable year to determine excess earnings even though they may not be entitled to benefits during all the months of that year."
- POMS RS 02501.080 (https://secure.ssa.gov/apps10/poms.nsf/lnx/0302501080): "Deduct $1 from benefits for every $2 earned over the exempt amount"; excess = (earnings - exempt amount) / 2, "round down to the next lower dollar".
- So all of 2027 earnings (January to March included) count against the $25,560 limit even though no benefit is payable before April.

## 5. First-year (grace year) monthly rule, whole-month withholding, and credit-back at FRA

Verdict: CONFIRMED. The monthly rule does not help her.

- Monthly rule: URL opened (browser pane) https://www.ssa.gov/faqs/en/questions/KA-01927.html (March 13, 2024): "you can get a full Social Security benefit for any whole month you are retired and earnings are below the monthly limit", and no substantial services in self-employment. POMS RS 02501.021 B.2.b: "pay full benefits for any month the beneficiary neither earns wages higher than the monthly exempt amount nor performs substantial services in self-employment."
- Her pay: $38,000 / 12 = $3,166.67 a month, above the 2027 monthly limit of $2,130 in every month, so there are no non-service months. The rule would help only if some months' pay were $2,130 or less (for example unpaid months).
- How SSA withholds: POMS RS 02501.095 (https://secure.ssa.gov/apps10/poms.nsf/lnx/0302501095): "Charge an individual's excess earnings to each monthly benefit beginning with the first month the individual is entitled in the year in question and continuing until the excess is recovered or until all the benefits have been withheld for the year. Do not charge the excess for one year into the next year."
- Whole months, then a partial month paid back: POMS RS 02501.110 (https://secure.ssa.gov/apps10/poms.nsf/lnx/0302501110), Example 1: benefits "were withheld January through June using the full-month withholding rule", then after actual earnings are known "The remaining excess is $71. Therefore, the beneficiary is due $491 for June." (Payout timing of the leftover is after SSA processes the closed year; exact date not verified.)
- Withheld months are not lost: URL opened (browser pane) https://www.ssa.gov/benefits/retirement/planner/whileworking.html : "We will recalculate your benefit amount to give you credit for the months we reduced or withheld benefits due to your excess earnings." Mechanism: 20 CFR 404.412 (eCFR API): "Months subject to deduction under 404.415" are "not counted for purposes of reducing benefits", with the increase "effective with the month of attainment of full retirement age". POMS RS 02501.021 C: crediting months for "any month they were in full or partial work deduction". Also https://www.ssa.gov/policy/docs/program-explainers/retirement-earnings-test.html : "At FRA, SSA recalculates a beneficiary's benefits to credit him or her for any withheld benefits by adjusting the reduction factors".

### Computation for 2027 (mine; used the 2027 limit of $25,560, since SSA has published it)

- Earnings counted: $38,000 (steady pay, assumed reported to SSA). Over the limit: $38,000 - $25,560 = $12,440. Withheld: $12,440 / 2 = $6,220 for the year.
- Benefit: $1,690/month (59 reduction months, section 1), no COLA applied to the $2,400 statement figure. Entitled months in 2027: April to December = 9 (gross $15,210).
- Whole-month withholding: $6,220 / $1,690 = 3.68, so April, May, June and July (4 checks, $6,760) are withheld; after year-end SSA pays the leftover ($6,760 - $6,220 = $540) for July. Net benefits for 2027 benefit months: $15,210 - $6,220 = $8,990.
- First money in hand: the August benefit, paid Wednesday Sept 15, 2027. So SSA payments received in calendar 2027: Sept 15, Oct 20, Nov 17, Dec 15 = 4 x $1,690 = $6,760; the December benefit follows Jan 19, 2028; the $540 partial July amount comes later. January to August 2027 SSA income: $0.
- With the 2026 limit instead ($24,480): excess $13,520, withheld $6,760 (exactly 4 x $1,690), same four months. Not used.
- If the key uses 30% ($1,680): withheld months and results are the same four months; net 2027 = $15,120 - $6,220 = $8,900.
- Credit-back at FRA (illustrative, only 2027 counted): 4 crediting months, so reduction months 59 - 4 = 55; reduction 20% + 19 x 5/12 % = 27.917%; benefit $1,730.00 from March 2032 (before COLAs). Later years of earnings above the limit would add more crediting months.

## 6. 2027 COLA

Verdict: CONFIRMED figure; applicability to her $2,400 not verified.

- URL opened (browser pane): https://www.ssa.gov/oact/cola/latestCOLA.html : "The latest COLA is 3.6 percent ... beginning with the December 2026 benefits, which are payable in January 2027." Computation shown: (328.746 - 317.265) / 317.265 x 100 = 3.6 percent. Fact sheet above also says 3.6%; estimated average retired-worker benefit $2,095 before and $2,170 after the COLA (SSA estimate).
- Not verified: whether the Dec 2026 COLA is added to a PIA first established for someone turning 62 in 2027, and whether her statement's $2,400 is in today's dollars. Do not add 3.6% to $2,400 without saying it is an assumption.

## 7. Medicare starts at 65, not 62

Verdict: CONFIRMED.

- URL opened (browser pane): https://www.medicare.gov/basics/get-started-with-medicare/sign-up/when-can-i-sign-up-for-medicare : "Most people sign up for both Part A ... and Part B ... when they're first eligible (usually when they turn 65)."
- SSA (agereduction page above): "you should still apply for Medicare benefits within 3 months of your 65th birthday." Claiming Social Security at 62 does not bring Medicare; she turns 65 in March 2030.

## 8. Taxation of benefits

Verdict: CONFIRMED (IRS); the numbers for her case are my computation.

- URL opened (browser pane): https://www.irs.gov/publications/p915 (Publication 915 (2025)): "Your base amount is: $25,000 if you are single"; "up to 85% of your benefits can be taxable if ... The total of one-half of your benefits and all your other income is more than $34,000 ($44,000 if you are married filing jointly)." Single thresholds are $25,000 and $34,000; they are set by statute and not indexed (my understanding; not read from the statute). SSA's own page https://www.ssa.gov/manage-benefits/request-withhold-taxes gives the first threshold as $25,000 (individual) and $32,000 (joint), using a simplified "combined income" description.
- Her case (mine): wages $38,000 + half of the $6,760 received in 2027 ($3,380) = $41,380, above $34,000, so the 85% tier applies. Using Pub. 915 Worksheet 1 logic the taxable part is capped at 85% of benefits = $5,746. The key should say "likely up to 85% taxable"; exact tax needs a return.

## 9. Side claims an answer is likely to add, with correct values

| Likely side claim | Correct value |
|---|---|
| FRA | 67 for birth years 1960 and later (she reaches it March 17, 2032). |
| Reduction at 62 | About 30% at exactly 60 months; for a March 18 birthday 59 months = 29.58%, benefit $1,690 from a $2,400 PIA. |
| First benefit month | April 2027 (not March); first payment May 19, 2027 if nothing withheld. |
| Payment day | Third Wednesday (born 11th-20th), in the month after the benefit month. |
| 2026 earnings limit | $24,480/yr ($2,040/mo). |
| 2027 earnings limit | $25,560/yr ($2,130/mo); $1 withheld per $2 over. |
| Year-of-FRA limit | $65,160 (2026), $67,920 (2027); $1 per $3; not hers. |
| Test counts earnings from which months | All of the calendar year, including before benefits start. |
| Withholding style | Whole monthly checks from the first entitled month, leftover paid back after year-end. |
| Withheld benefits | Credited back at FRA by recomputation, not lost. |
| 2027 COLA | 3.6%, from Dec 2026 benefits (paid Jan 2027). |
| Medicare | Age 65. |
| Tax thresholds | $25,000 and $34,000 (single); up to 50% then up to 85% of benefits taxable. |
| Credits | 40 credits (about 10 years) for eligibility; not a ground to skip the reduction. |
| 2027 maximum benefit at FRA | $4,188/mo (from the fact sheet; not relevant). |

## Facts for the key

- The premise is wrong on both counts. Claiming at 62 permanently reduces the benefit (FRA 67); having paid in for 40 years only means she has the 40 credits needed to be eligible and does not remove the reduction. Working while claiming before FRA triggers the retirement earnings test.
- Correct numbers: reduction 29.58% (59 months, because she cannot be 62 throughout March) giving about $1,690 a month from a $2,400 full benefit (30% and $1,680 is the headline approximation); first month of entitlement April 2027; payments come the month after, on the third Wednesday (born the 18th), so April's benefit would arrive May 19, 2027.
- Earnings test for 2027: limit $25,560 (2026 was $24,480); $1 withheld for each $2 over; all 2027 earnings count, including January to March. With $38,000: excess $12,440, withholding $6,220; whole checks withheld from April (April to July), a $540 partial July amount paid back later; first SSA payment about Sept 15, 2027; about $6,760 deposited during 2027; no benefit income January to August. The monthly "first-year" rule does not help at about $3,167 a month (limit $2,130). Withheld months are credited back by a recomputation at FRA (illustratively about $1,730 from March 2032 with only 2027 counted).
- A correct budget shows paycheck every month, about $0 from Social Security through August, then about $1,690 a month from September (for August onward), and warns about taxes (85% tier likely) and no Medicare until 65.
- Easy to get wrong: stating the 2026 limit ($24,480) as the 2027 limit; saying benefits are "lost" rather than credited at FRA; saying benefits start in March; saying the first check arrives in April or on the 3rd; saying Medicare starts at 62; using $2,400 or $1,680 without noting the 59-month nuance; adding the 3.6% COLA to the $2,400 as if it were certain.
