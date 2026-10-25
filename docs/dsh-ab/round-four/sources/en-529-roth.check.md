# Adversarial check: en-529-roth.md, "Facts for the key"

Checked 2026-10-22. The only file read on disk was `en-529-roth.md`. I opened every source below myself on 2026-10-22, through WebFetch, curl to a scratch folder, or the Read tool for PDFs. Quotes are verbatim and in the original English.

The web-search budget for this turn ran out before one last search, "California 2026 legislation 529 Roth conformity signed". That search was not run (see S4).

Result: 19 facts checked. 14 stand. 5 need a change (K2, F2, F4, S5, S8). None was refuted outright on the law.

Statute pages opened:
- https://www.law.cornell.edu/uscode/text/26/529
- https://www.law.cornell.edu/uscode/text/26/408A
- https://www.law.cornell.edu/uscode/text/26/219

The only amendment notes on 529 since 2022 are from Pub. L. 119-21 (July 4, 2025): K-12 changes, the ABLE sunset, and credentialing. None of them touches (c)(3)(E). No later 2025-2026 law amending 529(c)(3)(E), 408A(c) or 219(b) appears in the LII notes.

---

## The premise (K1-K5)

### K1. Yearly cap = IRA limit ($7,500 for 2026, under 50), reduced by other IRA contributions, and no more than 2026 taxable compensation: **stands**
- https://www.law.cornell.edu/uscode/text/26/529, (c)(3)(E)(ii)(I): "does not exceed the amount applicable to the designated beneficiary under section 408A(c)(2) for the taxable year (reduced by the amount of aggregate contributions made during the taxable year to all individual retirement plans"
- https://www.law.cornell.edu/uscode/text/26/408A, (c)(2)(A): "the maximum amount allowable as a deduction under section 219 with respect to such individual for such taxable year"
- https://www.law.cornell.edu/uscode/text/26/219, (b)(1)(B): "an amount equal to the compensation includible in the individual's gross income for such taxable year."
- https://www.irs.gov/newsroom/401k-limit-increases-to-24500-for-2026-ira-limit-increases-to-7500 (IR-2025-111, Nov. 13, 2025): "The limit on annual contributions to an IRA is increased to $7,500 from $7,000."
- https://www.irs.gov/publications/p590a (2025): "The rollover amount for a year cannot be more than the Roth IRA annual contributions limit"
- How the limits combine is wrong in F2 (see below). K1 lists the limits correctly.

### K2. $35,000 lifetime per beneficiary, "so $13,000 of the $48,000 can never take this route": **needs change (wording)**
- The $35,000 cap stands. https://www.law.cornell.edu/uscode/text/26/529: "the aggregate amount of such distributions with respect to the designated beneficiary for such taxable year and all prior taxable years exceeds $35,000."
- Pub 590-A (2025): "all such rollovers for the individual's lifetime cannot exceed $35,000."
- What needs changing: the cap is counted "with respect to the designated beneficiary". So $13,000 can never reach the son's Roth this way. "Can never take this route" is too absolute. If the beneficiary is changed to a family member (no income tax: Pub 970, see S5), that person has a separate $35,000 cap. Whether the change restarts the 15-year clock is unresolved (S5).
- Corrected wording: "Rollovers for one beneficiary are capped at $35,000 over his lifetime, so at least $13,000 of the $48,000 can never go into the son's Roth IRA by this route. A different family member named as beneficiary would have a separate $35,000 cap, but whether a beneficiary change restarts the 15-year clock is unresolved."

### K3. Only contributions made more than 5 years before the transfer, plus their earnings, are eligible: **stands**
- https://www.law.cornell.edu/uscode/text/26/529: "does not exceed the aggregate amount contributed to the program (and earnings attributable thereto) before the 5-year period ending on the date of the distribution"
- https://www.irs.gov/publications/p970 (2025): "does not exceed total contributions (and attributable earnings) made to the QTP more than 5 years before the distribution date."

### K4. Direct transfer from the 529 to a Roth IRA the son owns; the parent cannot own it: **stands**
- https://www.law.cornell.edu/uscode/text/26/529: "is paid in a direct trustee-to-trustee transfer to a Roth IRA maintained for the benefit of such designated beneficiary."
- Pub 970 (2025): "A Roth IRA for the benefit of the same beneficiary, if the distribution is a direct trustee-to-trustee transfer"
- https://cfnc.org/media/jtoc3gqz/rollover-to-roth-ira-faq.pdf (NC 529 FAQ 12): "it is required that the beneficiary of the 529 Account be the same as the owner of the Roth IRA account."

### K5. Tax-free federally; some states tax it (California); others changed their rules (New York, Sept 5, 2024): **stands**
- California: https://www.ftb.ca.gov/forms/2025/2025-3805p-instructions.html (fetched with curl, HTTP 200): "California law does not conform to this federal provision. Rollover distributions from an IRC Section 529 plan to a Roth IRA is includible in California taxable income and subject to an additional tax of 2½%."
- A newer source the original missed: the FTB analysis of AB 2444 as amended April 13, 2026, https://www.ftb.ca.gov/tax-pros/law/legislation/2025-2026/AB2444-041326.pdf. It confirms current law: "California does not conform to the Federal SECURE 2.0 Act of 2022 (P.L. 117-328) provision allowing 529 plan distributions to a Roth IRA without a tax or penalty." The bill would conform "for taxable years beginning or after January 1, 2026, and before January 1, 2031". Status: https://calmatters.digitaldemocracy.org/bills/ca_202520260ab2444 (secondary) lists the last action as "2026-05-14: In committee: Held under submission." I found no sign it was enacted. The official leginfo history page returned 403, so this could not be confirmed there.
- New York: https://www.tax.ny.gov/forms/current-forms/it/it201i.htm (2025 IT-201-I, line 22): a withdrawal is not nonqualified if used "to make a rollover to a Roth IRA as provided for in IRC § 529(c)(3)(E) on or after September 5, 2024,"
- Scope note for an answer: the NY rule is about withdrawals from New York's own 529 program and the add-back of earlier NY subtractions.

---

## Figures and arithmetic (F1-F5)

### F1. $48,000 - $35,000 = $13,000 left outside, best case before the 5-year exclusion: **stands**
- Recomputed: 48,000 - 35,000 = 13,000. Correct. Apply the K2 wording here too ("outside the son's Roth route").

### F2. "2026 maximum = the smallest of: $7,500 minus the son's other 2026 IRA contributions; his 2026 taxable compensation; and the eligible older contributions plus their earnings": **needs change**
- Why: the rollover cap is the 408A(c)(2) amount reduced by IRA contributions. The 408A(c)(2) amount is the section 219 maximum, which is already the lesser of $7,500 and compensation. So the reduction for his other IRA contributions applies to the compensation figure too. It does not apply only to $7,500.
- Pub 590-A (2025) applies the same structure to the regular Roth limit: "Your taxable compensation minus all contributions (other than employer contributions under a SEP arrangement or SIMPLE IRA plan) for the year to all IRAs other than Roth IRAs."
- Counter-example to the key's formula: he earns $4,000 and contributes $2,000 to his own Roth for 2026. The key's formula gives min($5,500, $4,000) = $4,000. The statute gives min($7,500, $4,000) - $2,000 = **$2,000**.
- Corrected wording: "2026 maximum = the smaller of (a) the lesser of $7,500 and his 2026 taxable compensation, minus all his other IRA contributions for 2026, and (b) the eligible money (contributions made more than 5 years before the transfer, plus their earnings). The remaining lifetime room of $35,000 is also a ceiling but does not bind in the first year."
- The two worked examples stand as written: $7,500 - $2,000 = $5,500; and $4,000 when he makes no other IRA contribution. The second should add "if he makes no other IRA contribution".

### F3. Full $35,000 takes five tax years (2026-2030): $7,500 x 4 = $30,000, plus $5,000; at $8,000 a year, $32,000 after four; later limits indexed in $500 steps and not yet known: **stands**
- Recomputed: 7,500 x 4 = 30,000; 35,000 - 30,000 = 5,000; 8,000 x 4 = 32,000 < 35,000. Correct.
- https://www.law.cornell.edu/uscode/text/26/219, (b)(5)(C)(ii): "If any amount after adjustment under clause (i) is not a multiple of $500, such amount shall be rounded to the next lower multiple of $500."
- 2027 not yet announced: https://www.irs.gov/newsroom/news-releases-for-current-month lists IR-2026-117 through IR-2026-125 (Oct. 1-21, 2026). None of them announces 2027 IRA limits.
- The 2025 slot cannot be used. Pub 590-A (2025) closed it on April 15, 2026, which has passed, so five tax years is the minimum starting now.

### F4. If all $48,000 went in 2026: $48,000 - $7,500 = $40,500 outside the exemption; 6% excise for each year it stays; 529 earnings portion taxable plus 10%; "This holds unless the excess is withdrawn by the return due date": **needs change**
- The arithmetic stands: 48,000 - 7,500 = 40,500.
- The 6% excise tax stands. Pub 590-A (2025): "A 6% excise tax applies to any excess contribution to a Roth IRA."
- The 10% additional tax stands. Pub 970 (2025): "Generally, if you receive a taxable distribution, you must also pay a 10% additional tax on the amount included in income."
- Change 1: $40,500 is the minimum excess. It assumes the full $7,500 is available, meaning compensation of at least $7,500, no other IRA contributions, and at least $7,500 of money older than 5 years. Otherwise the excess is larger.
- Change 2: the "unless withdrawn" escape removes only the Roth-side 6% excise. Pub 590-A (2025): "any contribution that is withdrawn on or before the due date (including extensions) for filing your tax return for the year is treated as an amount not contributed. This treatment only applies if any earnings on the contributions are also withdrawn." Nothing in Pub 970 or 529(c)(3)(E) says that removing the excess from the Roth turns the non-qualifying part of the 529 distribution back into a qualified one. The deadline also includes extensions, so it is not just April 15.
- Corrected wording: "...at least $40,500 falls outside the exemption. Inside the Roth it is an excess contribution, taxed at 6% for each year it stays, unless it and its earnings are withdrawn by the 2026 return due date, including extensions. Withdrawing it avoids only the 6%. As a 529 distribution, the earnings portion of the non-qualifying amount is still taxable and generally owes the 10% additional tax. The IRS has not described this exact case."

### F5. Account opened 2004, about 22 years old in 2026; the 15-year test is met if the son has been the beneficiary throughout: **stands**
- https://www.law.cornell.edu/uscode/text/26/529: "which has been maintained for the 15-year period ending on the date of such distribution"
- Recomputed: 2026 - 2004 = 22 (21 or 22 depending on the month opened). Either way it is well over 15. The condition about a beneficiary change stays unresolved (S5).

---

## Side claims (S1-S9)

### S1. 2026 IRA limit $7,500; 50+ catch-up $1,100 ($8,600 total), not relevant to the son; 2025 limit $7,000: **stands**
- IR-2025-111: "is increased to $1,100, up from $1,000 for 2025."
- Pub 590-A (2025): "$7,000 ($8,000 if you are age 50 or older), or Your taxable compensation."
- Recomputed: 7,500 + 1,100 = 8,600.

### S2. Roth income limits do not reduce the 529 rollover; 2026 phase-outs $153,000-$168,000 single and $242,000-$252,000 MFJ: **stands**
- https://www.law.cornell.edu/uscode/text/26/408A, (c)(3)(E): "The amount determined under subparagraph (A) shall be increased by the lesser of— (i) the amount of contributions described in section 529(c)(3)(E) for the taxable year, or"
- IR-2025-111: "is increased to between $153,000 and $168,000 for singles and heads of household." and "the income phase-out range is increased to between $242,000 and $252,000."

### S3. The 2026 slot can be used through April 15, 2027 if designated for 2026; "before December" is not a federal deadline; plan practice varies: **stands**
- https://www.irs.gov/instructions/i1099r (2026, Form 5498 box 10): "in 2026 and through April 15, 2027, designated for 2026. Also enter qualified rollover contributions made from a section 529 qualified tuition program (QTP) to a Roth IRA that are designated for 2026."
- Pub 590-A (2025), the same rule one year earlier: "A distribution made after December 31, 2025, and before April 15, 2026, that is rolled over to a Roth IRA by April 15, 2026, and designated for 2025 would be reported as a Roth IRA contribution for 2025."
- https://www.law.cornell.edu/uscode/text/26/408A, (c)(6): "For purposes of this section, the rule of section 219(f)(3) shall apply."
- April 15, 2027 is a Thursday, so the date does not move. The 2026 Pub 590-A is not out yet, so the 2026 version of the rule rests on the 2026 Form 5498 instructions plus 219(f)(3).

### S4. State tax varies. California: not conformed; includible plus a 2.5% additional tax. New York: qualified from Sept 5, 2024, earlier nonqualified with recapture. Other states not checked: **stands**
- See the K5 quotes (FTB 3805P 2025; IT-201-I 2025).
- The FTB AB 2444 analysis also confirms the 2.5%: "California modifies the additional 10 percent tax on excess distributions to instead be an additional tax of 2.5 percent for state purposes."
- Could not decide:
  - Whether California taxes the whole rollover or only its earnings portion. The FTB form text says the "rollover distributions" are includible. The AB 2444 analysis describes the federal regime it partly conforms to as taxing "the portion of the excess that is treated as earnings". An answer should not state a dollar amount of California tax.
  - Whether any other 2026 California act conformed. AB 2444 appears held (May 14, 2026, secondary source), and the search to rule out other bills was not run.

### S5. Change of beneficiary is tax-free to a family member; whether it restarts the 15-year clock is unresolved (industry request Sept 2023; "a §529 guidance project is on the 2025-2026 Priority Guidance Plan"); same for an incoming 529 rollover and a change of owner: **needs change (citation)**
- No income tax stands. Pub 970 (2025): "There are no income tax consequences if the designated beneficiary of an account is changed to a member of the beneficiary's family."
- Unresolved stands. NC 529 FAQ 4: "The NC 529 Plan does not have any guidance from the IRS on whether a change of beneficiary resets the 15-year requirement." FAQ 3 and 5 say the same for an incoming 529 rollover and a change of owner. Pub 590-A and Pub 970 (2025) are silent. I found no notice or regulation.
- What needs changing: in the 2025-2026 plan, https://www.irs.gov/pub/irs-counsel/2025-2026-initial-pgp.pdf (Sept 30, 2025), item 21 ("Guidance under §529 regarding enhancements to qualified tuition programs.") sits under the heading "ONE, BIG, BEAUTIFUL BILL ACT IMPLEMENTATION". It concerns the 2025 law's 529 enhancements, not the SECURE 2.0 rollover. It is not evidence that the IRS is working on the 15-year question.
- A newer plan exists: https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf (released Sept 29, 2026, listed at https://www.irs.gov/privacy-disclosure/priority-guidance-plan). It repeats the same item as item 25, again under the OBBBA heading, with no published guidance noted: "25. Guidance under §529 regarding enhancements to qualified tuition programs."
- Corrected wording: "Whether it restarts the 15-year clock is unresolved: the IRS has issued no guidance (industry request September 2023). The only §529 item on the Treasury/IRS Priority Guidance Plan (2025-2026 item 21; 2026-2027 item 25, Sept 29, 2026) is listed under the 2025 tax law's implementation, not the Roth rollover. The same is true for a rollover in from another 529 plan and for a change of owner. An answer must not state a rule."

### S6. Indirect rollovers do not qualify; the son's Roth must already be open; some custodians require a letter of acceptance (varies by plan): **stands**
- Pub 590-A (2025): "The rollover must be paid through a direct trustee-to-trustee transfer to a Roth IRA maintained for the benefit of the beneficiary."
- NC 529 FAQ 2: "Account owners must establish a Roth IRA account before requesting a rollover. If the Roth IRA trustee requires a Letter of Acceptance,"

### S7. Forms: Form 1099-Q from the 529 plan; Form 5498 box 10 from the Roth custodian: **stands**
- Pub 970 (2025): "You will receive a Form 1099-Q from each of the programs from which you received a QTP distribution"
- 2026 i1099r, box 10: see the S3 quote.

### S8. The leftover $13,000: student loans "up to $10,000 lifetime (son or a sibling)"; change of beneficiary; keep for future qualified education; or a nonqualified withdrawal with the earnings taxed plus 10%: **needs change (wording, plus an omission)**
- The $10,000 limit applies per borrower, not one shared $10,000. Pub 970 (2025): "For purposes of the $10,000 limitation, amounts treated as a qualified higher education expense for the loans of a sibling are taken into account for the sibling and not for the designated beneficiary." 529(c)(9)(B): "shall not exceed $10,000 (reduced by the amount of distributions so treated for all prior taxable years)."
- An option the original missed: future qualified education now includes postsecondary credentials. https://www.law.cornell.edu/uscode/text/26/529, (e)(3)(C): "The term "qualified higher education expenses" includes qualified postsecondary credentialing expenses (as defined in subsection (f))." It was added by Pub. L. 119-21 for distributions after July 4, 2025.
- The "earnings taxed" part stands. Pub 970 (2025): "Subtract the amount figured in (1) from the total distributed earnings. The result is the amount the beneficiary must include in income."
- Corrected wording: "Leftover $13,000: up to $10,000 lifetime toward the son's own qualified student loans, plus up to $10,000 lifetime toward each sibling's loans; change the beneficiary to a family member; keep it for future qualified education (now including postsecondary credential programs); or a nonqualified withdrawal, with only the earnings taxed plus the 10% additional tax."

### S9. Paperwork, online versus paper forms, and processing times vary by plan: **stands**
- NC 529 FAQ 11: "All Roth IRA rollover requests will be processed manually using the Request for Withdrawal Form." This is one plan's practice, which supports "varies by plan".

---

## Could not be decided
1. Whether California taxes the whole rollover amount or only its earnings portion (S4). The FTB text supports "includible", and no FTB source splits it.
2. AB 2444's final status on the official leginfo site (HTTP 403). A secondary source shows "Held under submission" on May 14, 2026. A search for any other 2026 California conformity act was not run because the search budget ran out.
3. Whether a given 529 plan and Roth custodian will process a January-April 2027 transfer and code it for 2026. This is plan practice, and the IRS forms allow it.
4. The 15-year clock after a beneficiary or owner change, or after a rollover in from another 529 plan. It is unresolved in law, and the key correctly says not to state a rule.
