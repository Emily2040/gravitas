# Adversarial check: en-uk-child-benefit-charge.md, "Facts for the key"

Checked 2026-10-25 by an agent that did not write the source file. On disk I read only the prompt `en-uk-child-benefit-charge.txt` and the source `en-uk-child-benefit-charge.md`. I opened every URL again myself on that date. GOV.UK pages came through the Content API (`https://www.gov.uk/api/content/<path>`, downloaded with curl, HTML stripped locally). Legislation came from the legislation.gov.uk `data.xml` revised text. The Healthy Start page and the 2027 to 2028 rates URL were opened with WebFetch. Quotes are verbatim, two lines at most. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: I found no rule, amendment, figure or announcement up to 2026-10-25 that changes a fact here or makes the premise true. ITEPA 2003 ss.681B and 681C (revised text modified 2026-09-22) still read £60,000 and £200. Neither section has an unapplied effect: the only outstanding effects listed in the XML belong to other sections of the Act (FA 2013 on s.452, FA 2026 on ss.114, 116, 116A and 221A, the last four already applied). The FA 2026 note on the Part 10 heading inserts one word in the heading and changes nothing in Chapter 8. Budget 2025 (26 November 2025) has no HICBC measure. Its only Child Benefit line is the 12-hour rule for 16 to 19-year-olds. A GOV.UK search for items published since 1 April 2026 turned up no HICBC change. HMRC's press release of 18 May 2026 repeats the current figures (£27.05, £1,406.60 a year, £60,000, 48 hours, 3 months' backdating, the PAYE service). The rates table, the HICBC guide and the Child Benefit guide were all last edited 2026-09-30, and all show the same rules. The page https://www.gov.uk/government/publications/benefit-and-pension-rates-2027-to-2028 still returns 404. **Caution for the key:** Budget 2026 is on **28 October 2026**, three days after this check. The Chancellor's letter to the Treasury Select Committee (GOV.UK, 2026-07-31) says: "The Budget will be held on 28 October 2026." The 2025 uprating statement came out with the 2025 Budget. Re-check HICBC and the 2027 to 2028 rate if grading happens after 28 October 2026. Web searches for October 2026 HICBC news found only aggregator pages that restate the 2024 change, and nothing official.

## The premise

**F1. From 2024 to 2025 onward, the HICBC threshold is £60,000 of the individual's adjusted net income. The colleague's £50,000 is out of date.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview; public_updated_at 2024-12-31, updated_at 2026-09-30)
- Quote: "over £60,000 for tax years starting from 2024 to 2025" / "over £50,000 for tax years up to and including the tax year 2023 to 2024"
- URL: https://www.legislation.gov.uk/ukpga/2003/1/section/681B (revised text, dc:modified 2026-09-22)
- Quote: "A person (“P”) is liable to a charge to income tax for a tax year if— (a) P's adjusted net income for the year exceeds £60,000"
- Amendment note in the same XML: "Sum in s. 681B(1)(a) substituted (6.4.2024 for the tax year 2024-25 and subsequent years) by Finance (No. 2) Act 2024 (c. 12), s. 5(1)(3)"

**F2. The taper is 1% for every £200 over £60,000, and the whole benefit is repaid above £80,000. The colleague's "1% per £100" is the 2023 to 2024 rule.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview)
- Quote: "You’ll pay back 1% of your Child Benefit for every £200 you earn over £60,000." / "If you earn over £80,000 you’ll pay it all back."
- Quote (same part): "If you need to pay the charge for the 2023 to 2024 tax year or earlier, you’ll pay back 1% for every £100 you earned over £50,000."
- URL: https://www.legislation.gov.uk/ukpga/2003/1/section/681C (s.681C(2) and (3))
- Quote: "ANI is P's adjusted net income for the tax year; L is £60,000; X is £200." The percentage is "100%, or (b) if less" the formula.
- s.681C(3): if the percentage "is not a whole number ... it is to be rounded down to the nearest whole number." The same rule applies to the total benefit and to the charge in pounds.
- URL: https://www.gov.uk/government/publications/income-tax-increasing-the-high-income-child-benefit-charge-threshold/the-high-income-child-benefit-charge-threshold (HMRC TIIN; published 2024-03-06, updated_at 2026-09-30)
- Quote: "This measure increases the adjusted net income threshold for the High Income Child Benefit Charge (HICBC) from £50,000 to £60,000, from 6 April 2024."
- Quote: "This measure will have effect from 6 April 2024, for the tax year 2024 to 2025 and subsequent tax years."

**F3. At £57,500 there is no charge: nothing to repay, and no Self Assessment return is needed for the charge.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit-tax-charge (part "If your circumstances change", slug `your-circumstances-change`)
- Quote: "You or your partner will not have to pay the tax charge if you or your partner’s individual ‘adjusted net income’ for the whole of a tax year is below the threshold."
- Statute: s.681B(1)(a) (F1). Liability exists only where adjusted net income "exceeds £60,000".
- Same guide, part "Pay the tax charge through Self Assessment": "If you do not usually send a tax return, you need to tell HMRC by 5 October following the tax year you need to pay the tax charge." That obligation exists only when a charge is owed.

**F4. The charge falls on the higher earner, whichever partner claims. Incomes are not added together.**
Status: **stands**
- URL: https://www.legislation.gov.uk/ukpga/2003/1/section/681B (s.681B(3) and (4))
- Quote (Condition A): "there is no other person who is a partner of P throughout the week and has an adjusted net income for the year which exceeds that of P."
- Quote (Condition B): "(b) Q is a partner of P throughout the week, and (c) P has an adjusted net income for the year which exceeds that of Q."
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview)
- Quote: "You or your partner may have to pay the High Income Child Benefit Charge if either of you receives Child Benefit and at least one of you earns more than the threshold."

**F5. The plan to base HICBC on household income was dropped.**
Status: **stands**
- URL: https://www.gov.uk/government/publications/autumn-budget-2024/autumn-budget-2024-html (published 2024-10-30, updated_at 2026-09-02)
- Quote: "The government will not proceed with the reform to base the HICBC on household incomes."
- Statute check: s.681B (F4) still compares each partner's own adjusted net income. Budget 2025 brought back no household test (newer-rule paragraph).

## Correct figures

**F6. The 2026 to 2027 rate is £27.05 a week for an eldest or only child (£17.90 for each additional child). £26.05 and £25.60 are earlier years.**
Status: **stands**
- URL: https://www.gov.uk/government/publications/rates-and-allowances-tax-credits-child-benefit-and-guardians-allowance/tax-credits-child-benefit-and-guardians-allowance (public_updated_at 2026-03-09, updated_at 2026-09-30)
- Quote (table rows): "Tax year 2026 to 2027 | £27.05 | £17.90" / "Tax year 2025 to 2026 | £26.05 | £17.25" / "Tax year 2024 to 2025 | £25.60 | £16.95"
- URL: https://www.gov.uk/child-benefit/what-youll-get (guide public_updated_at 2024-11-22, updated_at 2026-09-30). Rate table: "Eldest or only child | £27.05" and "Additional children | £17.90 per child". No tax year is named.
- URL: https://www.gov.uk/government/news/new-parents-urged-to-claim-child-benefit-for-their-baby-now (HMRC press release, 2026-05-18)
- Quote: "Child Benefit is worth £27.05 per week - or £1,406.60 a year - for the eldest or only child"

**F7. Full value: £1,406.60 a year, about £117.22 a month, paid as £108.20 every 4 weeks.**
Status: **stands**
- Recomputed: 27.05 × 52 = 1,406.60. 1,406.60 / 12 = 117.2167, so £117.22. 27.05 × 4 = 108.20. The £1,406.60 a year matches the HMRC press release (F6).

**F8. Payment is usually every 4 weeks, on a Monday or Tuesday.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit/when-and-how-its-paid
- Quote: "Child Benefit is usually paid every 4 weeks on a Monday or Tuesday."
- Weekly payment applies only to "a single parent or getting certain other benefits, such as Universal Credit" (same part), so not to this family.

**F9. A claim can be made 48 hours after the birth is registered. Here that is from about 20 September 2026.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit/how-to-claim (part "Make a claim")
- Quote: "You can claim Child Benefit 48 hours after you’ve registered the birth of your child, or once a child comes to live with you."
- Dates recomputed: 18 September 2026 is a Friday, so 48 hours later is Sunday 20 September 2026. 3 September 2026 is a Thursday.

**F10. A claim is backdated up to 3 months from the claim date, but not to before the birth.**
Status: **stands**, with one optional precision
- URL: https://www.gov.uk/child-benefit/how-to-claim
- Quote: "Child Benefit can be backdated for up to 3 months from the date you make the claim."
- URL: HMRC TIIN (F2)
- Quote: "New claims to Child Benefit are automatically backdated by three months, or to the child’s date of birth (whichever is later)."
- URL: https://www.gov.uk/hmrc-internal-manuals/child-benefit-technical-manual/cbtm02020 (reg 6; public_updated_at 2021-05-20, updated_at 2026-09-30)
- Quote: "This is 3 months, beginning with any day on which, apart from satisfying the conditions for making the claim, the person making the claim is entitled to the benefit or allowance."
- Optional precision: the HMRC press release of 18 May 2026 counts from when HMRC receives the claim: "can only be backdated for up to 3 months from the date HMRC receives the claim". A postal claim should therefore *arrive* inside the window.

**F11. Benefit is payable from the Monday after the date of entitlement. Here that is Monday 7 September 2026.**
Status: **stands**
- URL: https://www.gov.uk/hmrc-internal-manuals/child-benefit-technical-manual/cbtm02080 (reg 13; public_updated_at 2016-08-23, updated_at 2026-09-30)
- Quote: "Where an award is made for a period of a week or weeks and the date of entitlement is not a Monday, benefit or allowance will become payable from the Monday after the date of entitlement."
- URL: https://www.legislation.gov.uk/ukpga/1992/4/section/147 (SSCBA 1992; revised text dc:modified 2026-08-04)
- Quote: "“week” means a period of 7 days beginning with a Monday."
- Recomputed: Thursday 3 September 2026, so the next Monday is 7 September 2026.

**F12. Deadline: claim by 2 December 2026 to be certain of every week. No week is lost up to 6 December. From 7 December, each week of delay loses £27.05.**
Status: **stands**. One step in the worked example needs a small wording fix, and the result does not change.
- Recomputed under reg 6 (F10): the 3 months beginning with 3 September end on Wednesday 2 December 2026. The 3 months beginning with Monday 7 September end on Sunday 6 December. A claim on Monday 7 December reaches back only to Tuesday 8 September, so it is payable from Monday 14 September and the week of 7 September is lost.
- Worked example (15 January 2027 claim): the source says it "reaches back to 15 October 2026". Under "3 months beginning with", 3 months beginning with 15 October end on 14 January, so the earliest covered day is **16 October** (a Friday). The first payable Monday is still **19 October 2026**. Lost weeks: 7, 14, 21 and 28 September, and 5 and 12 October, which is 6 weeks. 6 × £27.05 = **£162.30**. Corrected wording: "reaches back to about 15 to 16 October 2026".
- Keeping the key lenient on the exact last day (2 to 6 December) is right.

## What a correct answer must also say

**F13. Only one person can get Child Benefit for a child.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit/eligibility (part "Who can get Child Benefit")
- Quote: "Only one person can get Child Benefit for a child."

**F14. Whoever is registered gets Class 3 NI credits for a child under 12, even when payments are switched off. This favours the partner as the claimant.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit/how-it-works
- Quote: "You’ll get National Insurance credits automatically if you claim Child Benefit and your child is under 12."
- URL: https://www.gov.uk/child-benefit/how-to-claim (heading "Deciding who should claim")
- Quote: "Whoever claims will get National Insurance credits towards their state pension. The credits can fill gaps in your record if you’re not working or do not earn enough to pay National Insurance contributions."
- URL: https://www.gov.uk/national-insurance-credits/eligibility (public_updated_at 2025-01-21, updated_at 2026-09-30)
- Quote: "You’re a parent or guardian registered for Child Benefit for a child under 12 (even if you do not receive it) | You get Class 3 credits automatically"
- Transfer (Overview of the same guide): "You can transfer your credits that you got from registering for Child Benefit to your spouse or partner who is living with you if you have paid a year’s National Insurance contributions"
- Statutory Maternity Pay with too little pay for a qualifying year: "Apply for Class 1 credits" (same eligibility table). These credits are not automatic, which matches the source.

**F15. Opting out keeps the registration, the NI credits and the child's NI number. Payments can restart at any time, and the first payment comes within 28 days.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview)
- Quote: "If you opt out of receiving payments, you are still registered for Child Benefit but you do not receive the payment."
- Quote (what you keep): "National Insurance credits, which count towards your State Pension" / "a National Insurance number for your child, without them having to apply shortly before they turn 16 years old"
- URL: https://www.gov.uk/child-benefit/make-a-change-to-your-claim
- Quote: "You can make a claim and choose to opt out of getting Child Benefit payments at any time. For example, you might opt out because your annual income is over £60,000"
- Restart (part "Restart your Child Benefit payments"): "it can take up to 28 days before you get your first payment."

**F16. The child gets an NI number automatically, shortly before 16.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit/how-it-works
- Quote: "a National Insurance number for your child without them having to apply for one - they’ll usually get the number shortly before they turn 16 years old"

**F17. The test is adjusted net income, which pension contributions and Gift Aid reduce (£1.25 for each £1).**
Status: **stands**
- URL: https://www.gov.uk/guidance/adjusted-net-income (public_updated_at 2025-05-30, updated_at 2026-09-30)
- Quote: "Adjusted net income is total taxable income before any Personal Allowances and less certain tax reliefs"
- Quote: "So, for every £1 of pension contribution you made, take £1.25 from your ‘net income’." / "So, for every £1 of Gift Aid donations you made, take £1.25 from your net income."
- Same page: "High Income Child Benefit Charge — where you have an adjusted net income above £60,000"

**F18. Claiming never leaves the family worse off, because the charge cannot exceed the benefit.**
Status: **stands**. This is an extra source for the key's "never worse than break-even" line.
- URL: https://www.gov.uk/child-benefit/what-youll-get
- Quote: "The charge will not be more than the amount you get from Child Benefit payments."
- Statute: s.681C(2)(a) caps the percentage at "100%".

**F19. A charge that is owed can be paid through the tax code (PAYE) without a Self Assessment return.**
Status: **stands**
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview and part "Pay the tax charge through PAYE")
- Quote: "There are two ways to pay the tax charge, you can either: pay the tax charge through PAYE / pay the tax charge through Self Assessment"
- Quote (conditions): "you do not need to send a tax return for another reason" / "it’s on or before 31 January after the tax year you need to pay for"
- URL: Autumn Budget 2024 (F5)
- Quote: "the government will allow employed individuals pay their HICBC through their tax code from 2025"
- Side note for the key: the March 2024 TIIN still says higher earners "will continue to be required, as they are now, to complete a tax return to pay HICBC". The PAYE route has overtaken that. An answer that quotes it as current is out of date.

## Side claims

**F20. The 2027 to 2028 Child Benefit rate has not been published.**
Status: **stands** (as of 2026-10-25)
- URL: https://www.gov.uk/government/publications/benefit-and-pension-rates-2027-to-2028. It returned HTTP 404 both through the Content API and through WebFetch.
- URL: https://www.gov.uk/government/publications/benefit-and-pension-rates-2026-to-2027 (first published 2025-11-27)
- Quote: "as set out in the written ministerial statement made by the Secretary of State for Work and Pensions on 26 November 2025."
- Caution: Budget 2026 is on 28 October 2026 (newer-rule paragraph). Re-check this rate after that date.

**F21. Statutory Maternity Pay 2026 to 2027: 90% of average weekly earnings for 6 weeks, then £194.32 or 90% (whichever is lower) for 33 weeks.**
Status: **stands**
- URL: https://www.gov.uk/maternity-pay-leave/pay (updated_at 2026-10-05)
- Quote: "90% of your average weekly earnings (before tax) for the first 6 weeks" / "£194.32 or 90% of your average weekly earnings (whichever is lower) for the next 33 weeks"
- Eligibility part: "earn on average at least £129 a week". Recomputed: 24,000 / 52 = £461.54, and 90% of that is £415.38.

**F22. Funded childcare (England) for this baby starts 1 September 2027. Applications open 11 February 2027 and close 31 August 2027.**
Status: **stands**
- URL: https://www.gov.uk/free-childcare-if-working (first published 2025-04-01, updated_at 2026-09-30)
- Quote: "You can get 30 hours of free childcare per week for 38 weeks of the year." / "You can apply for 30 hours of free childcare from when your child is 23 weeks old."
- Quote (When to apply table row): "Between 1 April and 31 August | 1 September | 31 August"
- Recomputed: 3 September 2026 + 23 weeks = Thursday 11 February 2027. The baby turns 9 months on 3 June 2027, which gives hours from 1 September 2027. The return-to-work row "Between 1 May to 30 September | 1 September" agrees.
- Income cap (part "Check if you're eligible"): "you or your partner’s expected adjusted net income (including any foreign income) is over £100,000". Minimum earnings: "the National Minimum Wage or Living Wage for 16 hours a week on average."

**F23. Tax-Free Childcare: £2 top-up for every £8 paid in, up to £2,000 a year, with an adjusted net income cap of £100,000.**
Status: **stands**
- URL: https://www.gov.uk/tax-free-childcare (public_updated_at 2024-11-08, updated_at 2026-09-30)
- Quote: "For every £8 you pay into the account, the government will top it up by £2." / "The total top up you can get for each child is £500 every 3 months (up to £2,000 a year)."
- Quote: "£2,643.68 before tax if you’re aged 21 or over (the same as £203.36 per week)". Leave: "You can also usually get Tax-Free Childcare if you’re on: maternity leave".

**F24. The Sure Start Maternity Grant and Healthy Start need qualifying benefits, which this family does not have.**
Status: **stands**
- URL: https://www.gov.uk/sure-start-maternity-grant (updated_at 2026-09-09)
- Quote: "You or your partner must also get one of these benefits: income-related Employment and Support Allowance / Pension Credit / Universal Credit"
- Quote: "You must claim the grant within 11 weeks of the baby’s due date or within 6 months after the baby’s birth."
- URL: https://www.healthystart.nhs.uk/how-to-apply/ (WebFetch 2026-10-25. The only date on the page is the footer copyright, 2026.)
- Quote: "you get Universal Credit" and "your family’s monthly ‘take-home pay’ (also called ‘earned income’) is £408 or less from employment"

**F25. Income tax bands 2026 to 2027 (England), and whether "about £5,100 a month" is plausible.**
Status: **stands**. The NI rates the source assumed are now verified.
- URL: https://www.gov.uk/income-tax-rates (updated_at 2026-10-01)
- Quote: "The current tax year is from 6 April 2026 to 5 April 2027." / "Basic rate | £12,571 to £50,270 | 20%" / "Higher rate | £50,271 to £125,140 | 40%"
- URL: https://www.gov.uk/national-insurance-rates-letters (updated_at 2026-09-30). This closes the source's "not verified" note.
- Quote: "This table shows how much employers deduct from employees’ pay from 6 April 2026 to 5 April 2027." Category A row: "£242.01 to £967" at "8%", and "Over £967 a week" at "2%".
- Recomputed on annual bands: £57,500 nets £43,907.40 and £24,000 nets £20,799.60, so about £5,392 a month combined. Weekly NI thresholds move this by about £1. £5,100 remains plausible after pension or student loan deductions.

## Arithmetic

Status: **stands** for every line. Recomputed:
- Old rule: (57,500 − 50,000) / 100 = 75%. 0.75 × 1,406.60 = £1,054.95 repaid, leaving £351.65.
- Correct rule: £57,500 does not exceed £60,000, so the charge is 0%.
- First year: 7 September 2026 + 51 weeks = Monday 30 August 2027, so 52 payable weeks. 31 of those weeks begin on or before 5 April 2027. The source's "about 30 to 31" in 2026 to 2027 (£811.50 to £838.55) is right, given that the 2027 to 2028 uprating date and rate are unknown.
- Above £60,000 (s.681C(3) rounds the benefit total and the charge down to whole pounds; benefit £1,406): £62,000 gives 10% (£140). £65,000 gives 25% (£351). £70,000 gives 50% (£703). £80,000 gives 100% (£1,406).
- Late claim: 6 × £27.05 = £162.30 (F12).

## Verdict on the premise

The premise is **false** and the correction **stands**. The colleague described the HICBC rule that ended with 2023 to 2024: a £50,000 threshold and 1% per £100. For 2026 to 2027, the charge applies only when one partner's own adjusted net income exceeds £60,000, at 1% per £200 (ITEPA 2003 ss.681B–681C, revised to 2026-09-22; gov.uk/child-benefit-tax-charge, last edited 2026-09-30). At £57,500 there is no charge, nothing to repay and no Self Assessment return. The family should claim. Their full entitlement is £27.05 a week (£1,406.60 a year).

## Not decided in this pass

- Anything Budget 2026 (28 October 2026) or the 2027 to 2028 uprating statement may announce. Both come after this check.
- How the start date of the 2027 to 2028 rate falls within the baby's first year. It does not affect the 2026 to 2027 figures.

## Addendum A (2026-10-26): facts added while fixing the answer key

Checked 2026-10-26 by the agent fixing the key after review, not the agent that wrote the source. Each page was read through the GOV.UK Content API (`https://www.gov.uk/api/content/<path>`, downloaded with curl, HTML stripped locally). Quotes are verbatim, two lines at most.

**A1. The Sure Start Maternity Grant is £500.**
Status: **stands**
- URL: https://www.gov.uk/sure-start-maternity-grant (part "What you'll get", slug `what-youll-get`; public_updated_at 2015-01-12, updated_at 2026-09-09)
- Quote: "A Sure Start Maternity Grant is £500 and you do not have to pay it back."
- Eligibility is as in F24 (a qualifying benefit such as Universal Credit), so the grant is still not available on these facts.

**A2. How much a pension contribution takes off adjusted net income depends on how it is paid: £1.25 per £1 only for relief-at-source contributions (and Gift Aid); net-pay and salary-sacrifice contributions lower taxable pay £1 for £1.**
Status: **stands** (the £1 for £1 step is derived from the quotes below)
- URL: https://www.gov.uk/guidance/adjusted-net-income (public_updated_at 2025-05-30, updated_at 2026-09-30)
- Quote (Step 3): "If you made a contribution to a private pension scheme where your pension provider has already given you tax relief at basic rate, take off the ‘grossed-up’ amount" (the £1.25 per £1 line in F17 follows this sentence; Step 2 does the same for Gift Aid)
- Quote (Step 1 starts from taxable income): "Add up your taxable income" / tax reliefs taken off include "payments made gross to pension schemes — those that have been made without tax relief"; worked example: "Her net income is £65,250 (£70,000 less £4,750)."
- URL: https://www.gov.uk/tax-on-your-private-pension/pension-tax-relief (public_updated_at 2024-11-08, updated_at 2026-09-30)
- Quote (the two automatic kinds): "your employer takes workplace pension contributions out of your pay before deducting Income Tax" / "your pension provider claims tax relief from the government at the basic 20% rate and adds it to your pension pot (‘relief at source’)"
- URL: https://www.gov.uk/guidance/salary-sacrifice-and-the-effects-on-paye (public_updated_at 2026-04-06, updated_at 2026-09-30)
- Quote: "A salary sacrifice arrangement is an agreement to reduce an employee’s entitlement to cash pay, usually in return for a non-cash benefit."
- Quote (example row, £5,000 bonus sacrificed for a £5,000 employer pension contribution): "No employment income tax or National Insurance contributions charge to the employee"
- Derived: a net-pay contribution comes out before Income Tax and a salary sacrifice reduces cash pay, so each lowers taxable pay, and with it adjusted net income, by £1 for each £1. Only relief-at-source contributions and Gift Aid are grossed up to £1.25. This matches the note in source item 6. It matters only if income nears £60,000.
