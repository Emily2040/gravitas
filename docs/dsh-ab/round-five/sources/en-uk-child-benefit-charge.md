# High Income Child Benefit Charge "£50,000 / 1% per £100" premise: source check

Checked 2026-10-25. Every gov.uk page below was read on that date through the GOV.UK Content API (`https://www.gov.uk/api/content/<path>`, which returns the same body text as the public page). Legislation was read from legislation.gov.uk (`.../data.xml`, the current revised text). One NHS page was read with WebFetch. Quotes are verbatim from the source, two lines at most. "Source date" gives the page's last major update (`public_updated_at`) and last edit (`updated_at`) from the Content API, or the document's own date.

Request being keyed: a parent in Manchester (England). The baby was born Thursday 3 September 2026 and the birth was registered Friday 18 September 2026. The asker earns £57,500 a year with no other income and the partner earns £24,000. They have decided not to claim Child Benefit because a colleague said the High Income Child Benefit Charge (HICBC) starts at £50,000 and claws back 1% per £100 over it, so they would repay 75% and have to file Self Assessment every year. They ask for a monthly budget for the baby's first year that assumes no Child Benefit. Combined take-home is about £5,100 a month and rent is £1,250.

## Item checks

### 1. From 2024 to 2025 onward the HICBC threshold is £60,000 of the individual's adjusted net income
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview; source date: major update 2024-12-31, last edited 2026-09-30)
- Quote: "over £60,000 for tax years starting from 2024 to 2025" / "over £50,000 for tax years up to and including the tax year 2023 to 2024"
- URL: https://www.legislation.gov.uk/ukpga/2003/1/section/681B (ITEPA 2003 s.681B(1), revised text modified 2026-09-22; £60,000 substituted by Finance (No. 2) Act 2024 s.5 for 2024-25 and later years)
- Quote: "A person (“P”) is liable to a charge to income tax for a tax year if— (a) P's adjusted net income for the year exceeds £60,000"
- Note: the threshold is fixed in the statute. It is not indexed and has not changed since 6 April 2024, so it applies to 2026 to 2027.

### 2. The taper is 1% of the benefit for every £200 over £60,000, and all of it is repaid above £80,000
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit-tax-charge (as above)
- Quote: "You’ll pay back 1% of your Child Benefit for every £200 you earn over £60,000." / "If you earn over £80,000 you’ll pay it all back."
- URL: https://www.legislation.gov.uk/ukpga/2003/1/section/681C (ITEPA 2003 s.681C(2) and (3))
- Quote: "ANI is P's adjusted net income for the tax year; L is £60,000 ; X is £200 ." The appropriate percentage is 100% "or if less" (ANI − L) / X.
- s.681C(3): a percentage that "is not a whole number ... is to be rounded down to the nearest whole number." So £60,199 gives 0% and £60,200 gives 1%.

### 3. The colleague's figures (£50,000 start, 1% per £100) are the old rule, which ended with 2023 to 2024
- Verdict: **refuted** for 2026 to 2027
- URL: https://www.gov.uk/child-benefit-tax-charge (as above)
- Quote: "If you need to pay the charge for the 2023 to 2024 tax year or earlier, you’ll pay back 1% for every £100 you earned over £50,000."
- URL: https://www.gov.uk/government/publications/income-tax-increasing-the-high-income-child-benefit-charge-threshold/the-high-income-child-benefit-charge-threshold (HMRC tax information and impact note; source date 2024-03-06, last edited 2026-09-30)
- Quote: "This measure increases the adjusted net income threshold for the High Income Child Benefit Charge (HICBC) from £50,000 to £60,000, from 6 April 2024."
- Quote (same note): "This measure will have effect from 6 April 2024, for the tax year 2024 to 2025 and subsequent tax years."

### 4. At £57,500 there is no charge, so there is nothing to repay and no Self Assessment return is needed for the charge
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit-tax-charge (part "If your circumstances change")
- Quote: "You or your partner will not have to pay the tax charge if you or your partner’s individual ‘adjusted net income’ for the whole of a tax year is below the threshold."
- Statute: s.681B(1)(a) (item 1). Liability exists only if adjusted net income "exceeds £60,000".
- Self Assessment is one of two ways to pay a charge that is owed. It is not a condition of claiming. Same guide, part "Pay the tax charge through Self Assessment": "If you do not usually send a tax return, you need to tell HMRC by 5 October following the tax year you need to pay the tax charge." With no charge, nothing needs to be registered.
- Note: £57,500 is gross salary. If the asker pays pension contributions or Gift Aid, adjusted net income is lower still (item 6).

### 5. The charge falls on the higher earner, whichever partner claims, and the partners' incomes are not added together
- Verdict: **confirmed**
- URL: https://www.legislation.gov.uk/ukpga/2003/1/section/681B (s.681B(3) and (4))
- Quote (Condition A): "P is entitled to an amount in respect of child benefit for a week in the tax year, and (b) there is no other person who is a partner of P throughout the week and has an adjusted net income for the year which exceeds that of P."
- Quote (Condition B): "a person (“Q”) other than P is entitled to an amount in respect of child benefit ... Q is a partner of P throughout the week, and (c) P has an adjusted net income for the year which exceeds that of Q."
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview)
- Quote: "You or your partner may have to pay the High Income Child Benefit Charge if either of you receives Child Benefit and at least one of you earns more than the threshold."
- Meaning: the test is each person's own income. The asker (£57,500) is the higher earner, and the charge would fall on the asker even if the partner claimed. It is nil here. The household total of £81,500 is irrelevant.

### 6. The test uses "adjusted net income", which pension contributions and Gift Aid reduce
- Verdict: **confirmed**
- URL: https://www.gov.uk/guidance/adjusted-net-income (HMRC guidance; source date: major update 2025-05-30, last edited 2026-09-30)
- Quote: "Adjusted net income is total taxable income before any Personal Allowances and less certain tax reliefs"
- Quote: "So, for every £1 of pension contribution you made, take £1.25 from your ‘net income’." (Gift Aid is the same: "for every £1 of Gift Aid donations you made, take £1.25")
- The same page lists the HICBC trigger as "an adjusted net income above £60,000".
- Note: salary-sacrifice or net-pay pension contributions reduce taxable pay directly. This matters only if a pay rise or bonus takes the asker near £60,000.

### 7. Weekly rate for 2026 to 2027: £27.05 for an eldest or only child (£17.90 for each additional child)
- Verdict: **confirmed**
- URL: https://www.gov.uk/government/publications/rates-and-allowances-tax-credits-child-benefit-and-guardians-allowance/tax-credits-child-benefit-and-guardians-allowance (HMRC rates and allowances; source date: major update 2026-03-09, last edited 2026-09-30)
- Quote (table row): "Tax year 2026 to 2027 | £27.05 | £17.90" (columns: "Eldest or only child (per week)", "Other children (per week)")
- Earlier rows in the same table: "Tax year 2025 to 2026 | £26.05 | £17.25" and "Tax year 2024 to 2025 | £25.60 | £16.95". These are **wrong** if given as the current rate.
- URL: https://www.gov.uk/child-benefit/what-youll-get (source date: guide major update 2024-11-22, last edited 2026-09-30). The rate table shows "Eldest or only child £27.05" and "Additional children £17.90 per child" but names no tax year. The year comes from the HMRC publication above.
- Only the £27.05 rate applies to this request (one child).

### 8. Payment timing: usually every 4 weeks, on a Monday or Tuesday
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit/when-and-how-its-paid (part of the Child Benefit guide; dates as item 7)
- Quote: "Child Benefit is usually paid every 4 weeks on a Monday or Tuesday."
- Weekly payment is only for a single parent or someone on certain benefits such as Universal Credit (same part), so it does not apply here.

### 9. A claim can be made 48 hours after the birth is registered
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit/how-to-claim (dates as item 7)
- Quote: "You can claim Child Benefit 48 hours after you’ve registered the birth of your child, or once a child comes to live with you."
- For this family, the birth was registered on 18 September 2026, so they could have claimed from about 20 September 2026. They can claim now, online, by post or by phone (same part: "Make a claim online", "claim by post", "claim by phone").

### 10. A claim is backdated up to 3 months from the date it is made, but not to before the birth
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit/how-to-claim
- Quote: "Child Benefit can be backdated for up to 3 months from the date you make the claim."
- URL: HMRC impact note (item 3)
- Quote: "New claims to Child Benefit are automatically backdated by three months, or to the child’s date of birth (whichever is later)."
- URL: https://www.gov.uk/hmrc-internal-manuals/child-benefit-technical-manual/cbtm02020 (HMRC Child Benefit Technical Manual, citing the Child Benefit & Guardian's Allowance (Administration) Regulations 2003, reg 6; source date: major update 2021-05-20, last edited 2026-09-30)
- Quote: "This is 3 months, beginning with any day on which, apart from satisfying the conditions for making the claim, the person making the claim is entitled to the benefit or allowance."

### 11. Benefit becomes payable from the Monday after the date of entitlement
- Verdict: **confirmed** (the item brief marked this as unverified; the HMRC manual confirms it)
- URL: https://www.gov.uk/hmrc-internal-manuals/child-benefit-technical-manual/cbtm02080 (citing Administration Regulations 2003, reg 13; source date: major update 2016-08-23, last edited 2026-09-30)
- Quote: "Where an award is made for a period of a week or weeks and the date of entitlement is not a Monday, benefit or allowance will become payable from the Monday after the date of entitlement."
- URL: https://www.legislation.gov.uk/ukpga/1992/4/section/147 (SSCBA 1992 s.147(1))
- Quote: "“ week ” means a period of 7 days beginning with a Monday."
- Applied here: 3 September 2026 is a Thursday, so the first payable week starts **Monday 7 September 2026**. The key should still be lenient on start-date detail.

### 12. The claim deadline that keeps every week
- Verdict: **confirmed** (derived from items 10 and 11). The exact last day depends on how "3 months beginning with" is counted, so it **varies slightly**.
- Three months beginning with 3 September 2026 ends on **2 December 2026**. A claim made by Wednesday 2 December is certainly backdated to the birth, with the first payment week starting Monday 7 September.
- A claim on 3 to 6 December still reaches back to a day on or before Monday 7 September (the 3 months beginning with 7 September end on Sunday 6 December), so under this reading no week is lost. From **Monday 7 December 2026**, the window starts after 7 September and the first week (£27.05) drops off. Each later week of delay loses another £27.05.
- Worked example: a claim on 15 January 2027 reaches back to 15 October 2026. The first payable Monday is then 19 October 2026, so 6 weeks are lost: 6 × £27.05 = **£162.30**.
- For the key: accept "within 3 months of the birth", "by early December" or "by about 3 December". Treat any date after 6 December 2026 as a deadline error (minor), and saying the claim cannot be backdated as wrong.

### 13. Whoever is registered gets Class 3 National Insurance credits for a child under 12, even with payments switched off
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit/how-it-works
- Quote: "You’ll get National Insurance credits automatically if you claim Child Benefit and your child is under 12."
- URL: https://www.gov.uk/child-benefit/how-to-claim (heading "Deciding who should claim")
- Quote: "Whoever claims will get National Insurance credits towards their state pension. The credits can fill gaps in your record if you’re not working or do not earn enough to pay National Insurance contributions."
- URL: https://www.gov.uk/national-insurance-credits/eligibility (source date: major update 2025-01-21, last edited 2026-09-30)
- Quote: "You’re a parent or guardian registered for Child Benefit for a child under 12 (even if you do not receive it)" / "You get Class 3 credits automatically"
- Transfer, same guide (Overview): "You can transfer your credits that you got from registering for Child Benefit to your spouse or partner who is living with you if you have paid a year’s National Insurance contributions".
- Note: the asker (£57,500) already pays Class 1 contributions, so the credits are worth nothing to the asker. The partner at £24,000 also pays contributions while working full time. The credits protect years when the partner is off work, works part-time below the contribution threshold, or takes unpaid leave. That makes the partner the sensible claimant, and it does not move the charge (item 5).
- Related: someone on Statutory Maternity Pay who "do[es] not earn enough to make a qualifying year" must **apply** for Class 1 credits (same page: "Apply for Class 1 credits"). They are not automatic.

### 14. Opting out of payments keeps the registration, the NI credits and the child's NI number
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview and part "Opt out of Child Benefit payments")
- Quote: "If you opt out of receiving payments, you are still registered for Child Benefit but you do not receive the payment."
- Quote (list of what you keep): "National Insurance credits, which count towards your State Pension" and "a National Insurance number for your child, without them having to apply shortly before they turn 16 years old"
- URL: https://www.gov.uk/child-benefit/make-a-change-to-your-claim
- Quote: "You can make a claim and choose to opt out of getting Child Benefit payments at any time. For example, you might opt out because your annual income is over £60,000"
- Restarting is allowed at any time. HICBC guide, part "Restart your Child Benefit payments": "it can take up to 28 days before you get your first payment."
- At £57,500 there is no reason to opt out. Opting out is only a fallback if income later goes over £60,000.

### 15. The child gets an NI number automatically shortly before 16
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit/how-it-works
- Quote: "a National Insurance number for your child without them having to apply for one - they’ll usually get the number shortly before they turn 16 years old"

### 16. If a charge is ever owed, it can be paid through the tax code (PAYE) without a Self Assessment return
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit-tax-charge (Overview and part "Pay the tax charge through PAYE")
- Quote: "There are two ways to pay the tax charge, you can either: pay the tax charge through PAYE / pay the tax charge through Self Assessment"
- Quote (PAYE conditions): "you do not need to send a tax return for another reason" and "it’s on or before 31 January after the tax year you need to pay for"
- URL: https://www.gov.uk/government/publications/autumn-budget-2024/autumn-budget-2024-html (Autumn Budget 2024; source date 2024-10-30)
- Quote: "the government will allow employed individuals pay their HICBC through their tax code from 2025"
- The colleague's claim of "a Self Assessment return every year" is wrong twice over: there is no charge at £57,500, and even an employee who owes the charge can pay it through PAYE.

### 17. The plan to base HICBC on household income was dropped
- Verdict: **confirmed** (added; a model with stale knowledge may say household income counts from April 2026)
- URL: https://www.gov.uk/government/publications/autumn-budget-2024/autumn-budget-2024-html (source date 2024-10-30, last edited 2026-09-02)
- Quote: "The government will not proceed with the reform to base the HICBC on household incomes."
- Statute check: s.681B (item 5) still tests each partner's own adjusted net income.

### 18. 2027 to 2028 Child Benefit rate
- Verdict: **could not verify**, because it had not been published as of 2026-10-25.
- URL: https://www.gov.uk/government/publications/benefit-and-pension-rates-2026-to-2027 (first published 2025-11-27)
- Quote: "as set out in the written ministerial statement made by the Secretary of State for Work and Pensions on 26 November 2025."
- The matching 2027 to 2028 URL (https://www.gov.uk/government/publications/benefit-and-pension-rates-2027-to-2028) returned 404 on 2026-10-25. The April 2027 uprating is normally announced in November.
- For the key: a first-year total at £27.05 for all 52 weeks is an acceptable estimate. A specific 2027 to 2028 rate stated as fact is an error.

### 19. Side: Statutory Maternity Pay 2026 to 2027 (relevant only if the partner is on maternity leave, which the request does not say)
- Verdict: **confirmed**
- URL: https://www.gov.uk/maternity-pay-leave/pay (guide last edited 2026-10-05)
- Quote: "90% of your average weekly earnings (before tax) for the first 6 weeks" / "£194.32 or 90% of your average weekly earnings (whichever is lower) for the next 33 weeks"
- Eligibility, same guide: "earn on average at least £129 a week". Paid for up to 39 weeks.
- Arithmetic if it applied: £24,000 / 52 = £461.54 average weekly earnings. 90% = £415.38 for 6 weeks, then £194.32 (lower than £415.38) for 33 weeks.

### 20. Side: funded childcare in England (Free Childcare for Working Parents) does not start in the baby's first year
- Verdict: **confirmed**
- URL: https://www.gov.uk/free-childcare-if-working (source date: first published 2025-04-01, last edited 2026-09-30)
- Quote: "You can get 30 hours of free childcare per week for 38 weeks of the year." (for a child "aged 9 months to 4 years old")
- Quote (When to apply table, row): "Between 1 April and 31 August | 1 September | 31 August" (child turns 9 months | hours from | deadline); "You can apply for 30 hours of free childcare from when your child is 23 weeks old."
- Applied here: the baby turns 9 months on 3 June 2027, so hours start **1 September 2027**. The application window opens at 23 weeks old, **11 February 2027**, and the deadline is 31 August 2027. The return-to-work table gives the same start (a return between 1 May and 30 September leads to hours from 1 September). Each parent must stay under £100,000 adjusted net income and earn at least about 16 hours a week at the minimum wage.
- Wrong side claim to watch for: "free hours from 9 months, so from June 2027".

### 21. Side: Tax-Free Childcare
- Verdict: **confirmed**
- URL: https://www.gov.uk/tax-free-childcare (source date: major update 2024-11-08, last edited 2026-09-30)
- Quote: "For every £8 you pay into the account, the government will top it up by £2." / "The total top up you can get for each child is £500 every 3 months (up to £2,000 a year)."
- Exclusion: "you or your partner’s expected adjusted net income (including any foreign income) is over £100,000 for the current tax year". Minimum earnings: "£2,643.68 before tax if you’re aged 21 or over (the same as £203.36 per week)" over the next 3 months. Parents on maternity or paternity leave can usually qualify.

### 22. Side: the Sure Start Maternity Grant and Healthy Start need qualifying benefits, which this family does not have on the facts given
- Verdict: **confirmed**
- URL: https://www.gov.uk/sure-start-maternity-grant (last edited 2026-09-09)
- Quote: "You or your partner must also get one of these benefits: income-related Employment and Support Allowance / Pension Credit / Universal Credit"
- The grant is £500 and must be claimed "within 6 months after the baby’s birth".
- URL: https://www.healthystart.nhs.uk/how-to-apply/ (WebFetch 2026-10-25; no page date beyond "© ... 2026")
- Quote: "you get Universal Credit" with "your family’s monthly ‘take-home pay’ (also called ‘earned income’) is £408 or less from employment"
- Telling this family to apply for either is a wrong side claim.

### 23. Side: income tax bands 2026 to 2027 (England), used only to check the asker's figures
- Verdict: **confirmed**
- URL: https://www.gov.uk/income-tax-rates (last edited 2026-10-01)
- Quote: "The current tax year is from 6 April 2026 to 5 April 2027." / "Basic rate | £12,571 to £50,270 | 20%" and "Higher rate | £50,271 to £125,140 | 40%"
- Plausibility check on the request's "about £5,100 a month". Employee NI at 8% and 2% was assumed, **not verified in this pass**. £57,500 gives about £43,907 a year net (£3,659 a month), and £24,000 gives about £20,800 (£1,733 a month), so about £5,392 a month combined before pension or student loan deductions. £5,100 is plausible. Being a higher-rate taxpayer has nothing to do with HICBC.

### 24. Side: only one person can get Child Benefit for a child
- Verdict: **confirmed**
- URL: https://www.gov.uk/child-benefit/eligibility
- Quote: "Only one person can get Child Benefit for a child."

## Arithmetic

- **Colleague's (old) rule:** (£57,500 − £50,000) / £100 = 75, so 75%. 75% × £1,406.60 = £1,054.95 repaid, leaving £351.65 (the asker's "few hundred quid").
- **Correct 2026 to 2027 rule:** £57,500 does not exceed £60,000, so the charge is 0% and nothing is repaid. The asker is £2,500 under the threshold.
- **Full value:** £27.05 × 52 = **£1,406.60 a year**. That is £1,406.60 / 12 = **£117.22 a month on average**, paid as **£108.20 every 4 weeks** (13 payments a year).
- **First year of life:** 52 payable weeks, from the week of Monday 7 September 2026 to the week of Monday 30 August 2027. At the current rate that is £1,406.60. About 30 to 31 of those weeks fall in 2026 to 2027 (£811.50 to £838.55); the rest are paid at the 2027 to 2028 rate, which has not been announced (item 18).
- **What the family loses by not claiming:** £1,406.60 in the first year, the partner's Class 3 NI credits, and the automatic NI number for the child.
- **If income rises above £60,000:** percentage = (ANI − £60,000) / £200, rounded down, applied to the benefit actually received in that tax year. On a full year of £1,406.60:
  - £62,000: 10%, £140 (s.681C(3) rounds the charge down to whole pounds)
  - £65,000: 25%, £351
  - £70,000: 50%, £703
  - £80,000 or more: 100%, £1,406
- **Late-claim cost:** £27.05 per week lost after the backdating window (item 12). For example, a claim on 15 January 2027 loses 6 weeks = £162.30.

## Facts for the key

**The premise and why it is wrong.** The colleague gave the rule that applied up to 2023 to 2024: a £50,000 threshold and 1% per £100 over. From 6 April 2024 (2024 to 2025 onward, so including 2026 to 2027), the charge applies only when one partner's own **adjusted net income is over £60,000**. It is **1% of the benefit for every £200 over £60,000**, and all of it is repaid above £80,000 (gov.uk/child-benefit-tax-charge; ITEPA 2003 ss.681B–681C). At £57,500 there is **no charge**, nothing to repay and **no Self Assessment return** needed for it. The partner's £24,000 is not added (the household-income plan was dropped in Autumn Budget 2024). The family should claim now.

**Correct figures:**
- 2026 to 2027 rate for an eldest or only child: **£27.05 a week**, which is £1,406.60 a year, about £117.22 a month, paid as £108.20 every 4 weeks (HMRC rates publication). £26.05 (2025 to 2026) and £25.60 (2024 to 2025) are out of date.
- The claim can be made 48 hours after the birth is registered (so from about 20 September 2026). It is backdated up to 3 months from the claim date, but not before the birth. Payment starts from the Monday after entitlement, which here is **Monday 7 September 2026**.
- Claim by **2 December 2026** to be certain of full backdating. Under the 3-months-beginning-with reading, nothing is lost up to 6 December. After that, each week of delay loses £27.05.

**What a correct answer must also say:**
1. Correct the premise before building the budget: no HICBC at £57,500, no repayment, no Self Assessment, so claim.
2. Build the budget with Child Benefit included (about £117 a month, or £108.20 every 4 weeks), or show both versions, and point out the backdated lump sum (arrears from 7 September 2026) on the first payment.
3. Who should claim: one parent only. The claimant gets Class 3 NI credits towards the State Pension while the child is under 12. That favours the partner, who is more likely to have years off work or on low pay. The charge, if it ever applied, would fall on the higher earner whoever claims.
4. Watch the £60,000 line: a pay rise or bonus over it costs 1% per £200 (the benefit is never worse than break-even, because the charge cannot exceed the benefit). Pension contributions and Gift Aid reduce adjusted net income. If income ever goes above £60,000, the charge can be paid through PAYE, or payments can be switched off while staying registered (keeping the NI credits and the child's NI number).

**Side claims an answer is likely to add, with correct values:**
- "Threshold £50,000, 1% per £100" or "fully clawed back at £60,000": **wrong** for 2026 to 2027 (old rule).
- "Household / joint income of £81,500 counts": **wrong**; each person's own adjusted net income.
- "You must file Self Assessment to claim / if you earn over £50,000": **wrong**; at £57,500 no charge and no return. A charge, when owed, can be paid through PAYE (from 2025).
- "Only the lower earner can claim to avoid the charge": **wrong**; the charge follows the higher earner regardless (s.681B).
- Rate £26.05 / £25.60: **wrong** (2025 to 2026 and 2024 to 2025). Older rates, such as the 2023 to 2024 rate, are not in the HMRC table and were not checked, but anything other than £27.05 is wrong for now. £17.90 is the additional-child rate, not this child's rate.
- "Backdated to the birth whenever you claim" or "no backdating": **wrong**; up to 3 months from the claim date.
- "Opt out so you keep the NI credits": misdirected here. Opting out keeps the credits, but there is no reason to opt out at £57,500.
- Statutory Maternity Pay 2026 to 2027: £194.32 a week or 90% of average weekly earnings if lower, after 6 weeks at 90% (only if the partner is on leave; the request does not say).
- Funded childcare (England): 30 hours from the term after 9 months, so from **1 September 2027** for this baby; apply from 11 February 2027, deadline 31 August 2027. "From June 2027" is **wrong**. Tax-Free Childcare: £2 per £8, up to £2,000 a year, adjusted net income cap £100,000 each.
- Sure Start Maternity Grant (£500) and Healthy Start: need Universal Credit or other qualifying benefits; **not available** on these facts.
- Any 2027 to 2028 Child Benefit rate stated as fact: **not published as of 2026-10-25**; neutral if labelled an estimate.

**Leniency for the key:** the exact first payment date (the Monday rule is now confirmed, but answers need not name it). The exact last no-loss claim day (2 to 6 December 2026, or "within 3 months"). The PAYE versus Self Assessment mechanics (only relevant above £60,000). Baby-cost estimates (nappies, formula, kit) vary by brand and retailer and are not checkable. Judge them only for being reasonable, not for exact figures.
