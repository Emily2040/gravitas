# Health FSA "rollover" premise: source check

Checked 2026-10-22. All URLs were opened on that date, either with WebFetch or by downloading the PDF from the URL and extracting its text. Quotes are verbatim from the source, two lines at most. "Source date" is the date of the document itself.

Request being keyed: about $1,900 left in a work health FSA, a calendar plan year ending December 31 (so the 2026 plan year), and the user believes "FSA money rolls over to next year just like an HSA", so they plan to save it for dental work in March 2027.

## Item checks

### 1. Use-it-or-lose-it is the default rule
- Verdict: **confirmed**
- URL: https://www.irs.gov/publications/p969 (Publication 969 (2025), section "Balance in an FSA"; page last reviewed or updated 30-Apr-2026)
- Quote: "FSAs are generally "use-it-or-lose-it" plans." / "Amounts in the account at the end of the plan year can't generally be carried over to the next year."

### 2. Two optional relief features (carryover or grace period), at the employer's option, never both
- Verdict: **confirmed**
- URL: https://www.irs.gov/publications/p969 (as above)
- Quote: "However, the plan can provide for either a grace period or a carryover." / "A plan adopting a carryover provision is not permitted to also provide a grace period with respect to health FSAs."
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf (Notice 2013-71, source date Oct/Nov 2013, 2013-47 IRB 532)
- Quote: "A plan adopting this carryover provision is not permitted to also provide a grace period with respect to health FSAs."
- URL: https://www.irs.gov/pub/irs-drop/n-05-42.pdf (Notice 2005-42, 2005-1 C.B. 1204)
- Quote: "A cafeteria plan document may, at the employer's option, be amended to provide for a grace period immediately following the end of each plan year."
- Note: neither feature is required. A plan may offer a carryover, a grace period, or neither.

### 3. Grace period length: up to 2.5 months, ending no later than the 15th day of the third month
- Verdict: **confirmed**
- URL: https://www.irs.gov/pub/irs-drop/n-05-42.pdf (Notice 2005-42)
- Quote: "The grace period must not extend beyond the fifteenth day of the third calendar month after the end of the immediately preceding plan year"
- For a plan year ending 2026-12-31, the latest possible grace-period end is **March 15, 2027**. A plan may set a shorter grace period. Leftover grace-period money is forfeited, not carried further (same notice: "may not be carried forward to any subsequent period").

### 4. Carryover limit for plan years beginning in 2025 = $660
- Verdict: **confirmed**
- URL: https://www.irs.gov/pub/irs-drop/rp-24-40.pdf (Rev. Proc. 2024-40, section 3.16, issued Oct 2024)
- Quote: "spending arrangements is $3,300. If the cafeteria plan permits the carryover of unused amounts, the maximum carryover amount is $660."
- Note: this is the 2025 to 2026 carryover. **It is not the limit for this user's 2026 plan year.** Pub 969 (2025 edition, still the live HTML page) also says "$660", so an answer that cites Pub 969 without checking may give the outdated figure.

### 5. Carryover limit for plan years beginning in 2026 = $680
- Verdict: **confirmed**
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf (Rev. Proc. 2025-32, section 4.15 "Cafeteria Plans", issued Oct 9, 2025)
- Quote: "For taxable years beginning in 2026, the dollar limitation under § 125(i) on voluntary employee salary reductions for contributions to health flexible spending arrangements is $3,400. If the cafeteria plan permits the carryover of unused amounts, the maximum carryover amount is $680."
- This is the figure that governs how much of this user's 2026 balance can carry into 2027.

### 6. 2026 health FSA contribution (salary reduction) limit = $3,400
- Verdict: **confirmed**
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf (same quote as item 5)
- Statutory base: https://www.law.cornell.edu/uscode/text/26/125 (26 U.S.C. 125(i)): "may not elect for any taxable year to have salary reduction contributions in excess of $2,500", indexed, "rounded to the next lowest multiple of $50."
- The limit is per employee. An employer may set a lower one.

### 7. The carryover limit is 20% of that plan year's 125(i) limit, keyed to the year the money comes from
- Verdict: **confirmed** (added; needed for the arithmetic)
- URL: https://www.irs.gov/pub/irs-drop/n-20-33.pdf (Notice 2020-33, May 2020)
- Quote: "increases the maximum $500 carryover amount for a plan year to an amount equal to 20 percent of the maximum salary reduction contribution under § 125(i) for that plan year."
- Check: 20% x $3,400 = $680 (2026). 20% x $3,300 = $660 (2025).

### 8. The employer may set a carryover cap below the IRS maximum
- Verdict: **confirmed** (added)
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf (Notice 2013-71)
- Quote: "the amount that may be carried over to the following plan year is equal to the lesser of (1) any unused amounts from the immediately preceding plan year or (2) $500 (or a lower amount specified in the plan)."

### 9. Run-out period vs grace period
- Verdict: **confirmed**
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf (Notice 2013-71, footnote 3)
- Quote: "A "run-out period" is a period immediately following the end of a plan year during which a participant can submit a claim for reimbursement of expenses incurred for qualified benefits during the plan year."
- Quote (same footnote): "By contrast, a grace period is a period of up to two months and 15 days ... during which a participant may use amounts remaining from the previous plan year"
- Meaning: a run-out period only adds time to **file claims** for expenses already incurred by Dec 31. It does **not** cover new expenses in 2027. A grace period does cover new expenses. The run-out length (for example 90 days, or March 31) is set by each plan.

### 10. The carryover does not reduce next year's contribution limit
- Verdict: **confirmed** (added)
- URL: https://www.irs.gov/publications/p969
- Quote: "The carryover doesn't affect the maximum amount of salary reduction contributions that you are permitted to make."

### 11. Dental work in March 2027 is covered by the 2026 money only through a grace period that reaches its date, or only up to the carried-over amount
- Verdict: **confirmed** (derived from items 2 to 5 and 9)
- Sources: Notice 2005-42 (grace period ends no later than March 15, 2027); Rev. Proc. 2025-32 ($680 cap); Notice 2013-71 (the excess is forfeited).
- Quote (Notice 2013-71): "Any unused amount in excess of $500 (or a lower amount specified in the plan) that remains unused as of the end of the plan year (that is, at the end of the run-out period for the plan year) is forfeited."
- Dental treatment itself is a qualified expense: https://www.irs.gov/publications/p502 (Pub 502 (2025), "Dental Treatment"): "You can include in medical expenses the amounts you pay for the prevention and alleviation of dental disease."

### 12. Expenses count when the care is provided, so paying the dentist in December for March work does not help (orthodontia is the only exception)
- Verdict: **confirmed** (added; a correct plan needs this)
- URL: https://www.irs.gov/publications/p969
- Quote: "The FSA can't make advance reimbursements of future or projected expenses." / reimbursement is only for "qualified medical expenses you incurred during the period of coverage."
- URL: https://www.govinfo.gov/content/pkg/FR-2007-08-06/pdf/E7-14827.pdf (Prop. Treas. Reg. 1.125-6(a)(2)(ii), 72 FR 43961, Aug 6, 2007)
- Quote: "medical expenses are incurred when the employee ... is provided with the medical care that gives rise to the medical expenses, and not when the employee is formally billed, charged for, or pays for the medical care."
- Orthodontia exception (same document, Prop. Treas. Reg. 1.125-5(k)(3)(i), 72 FR 43959): "A cafeteria plan is permitted, but is not required to, reimburse employees for orthodontia services before the services are provided"; the services count as incurred when the advance payment is made. **Plan-specific.**

### 13. Eligible expenses to spend down before December 31 (Pub 502 categories)
- Verdict: **confirmed**, with one **correction**: Pub 502 is the itemized-deduction list. For FSAs, over-the-counter medicine and menstrual products are also eligible even though Pub 502 says non-prescribed drugs are not deductible.
- URL: https://www.irs.gov/publications/p502 (Publication 502 (2025))
  - Definition: "Medical expenses are the costs of diagnosis, cure, mitigation, treatment, or prevention of disease"
  - "You can include in medical expenses amounts you pay for eyeglasses and contact lenses needed for medical reasons."
  - "You can include in medical expenses amounts you pay for prescribed medicines and drugs."
  - "You can include in medical expenses the cost of a hearing aid and batteries."
  - "You can include in medical expenses the cost of breast pumps and supplies that assist lactation."
  - "You can include in medical expenses the cost of medical supplies such as bandages." / "You can include in medical expenses the amount you pay for eye examinations."
  - Dental Treatment examples: "teeth cleaning, the application of sealants, and fluoride treatments" and "X-rays, fillings, braces, extractions, dentures"
  - Not eligible: "You can't include in medical expenses amounts paid to whiten teeth." / "the cost of a toothbrush and toothpaste is a nondeductible personal expense."
- FSA-specific rules, URL: https://www.irs.gov/publications/p969
  - OTC: "Expenses incurred for over-the-counter medicine (whether or not prescribed) and menstrual care products" are reimbursable.
  - Not reimbursable: "Amounts paid for health insurance premiums." / "Amounts paid for long-term care." / "Amounts that are covered under another health plan."
- Statute for menstrual products: https://www.law.cornell.edu/uscode/text/26/106 (26 U.S.C. 106(f)): "expenses incurred for menstrual care products shall be treated as incurred for medical care."

### 14. HSAs are different: the balance stays until used, with no annual forfeiture
- Verdict: **confirmed**
- URL: https://www.irs.gov/publications/p969 (HSA section)
- Quote: "The contributions remain in your account until you use them."
- 2026 HSA limits (same page): "For 2026, if you have self-only HDHP coverage, you can contribute up to $4,400." / "If you have family HDHP coverage, you can contribute up to $8,750."
- An HSA requires HDHP coverage. A general-purpose health FSA generally blocks HSA contributions (same page): "An employee covered by an HDHP and a health FSA or an HRA ... can't generally make contributions to an HSA." Limited-purpose and post-deductible FSAs are the exceptions.

### 15. Uniform coverage: the whole annual election is available on day one of the plan year
- Verdict: **confirmed** (added; this makes "elect for 2027 and pay for the March dental work from that" a valid option)
- URL: https://www.irs.gov/publications/p969
- Quote: "You must be able to receive the maximum amount of reimbursement ... at any time during the coverage period, regardless of the amount you have actually contributed."

### 16. Leftover money is forfeited if employment ends (unless COBRA is elected for the FSA)
- Verdict: **confirmed** (added side fact)
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf
- Quote: "Any unused amount remaining in an employee's health FSA as of termination of employment also is forfeited (unless, if applicable, the employee elects COBRA continuation coverage with respect to the health FSA)."

### 17. 2027 health FSA limit and 2027 carryover limit (for the open-enrollment election)
- Verdict: **could not verify**. No official 2027 figure was published as of 2026-10-22.
- URL: https://www.irs.gov/newsroom/news-releases-for-current-month (lists releases through IR-2026-125, Oct 21, 2026; none covers 2027 inflation adjustments)
- Secondary projections (not official) put 2027 at $3,500 contribution and $700 carryover. Do not present these as IRS figures.

### 18. Whether a general-purpose FSA carryover into 2027 blocks HSA contributions for all of 2027
- Verdict: **could not verify** on a primary source in this pass. The IRS ruling URL that was tried (https://www.irs.gov/pub/irs-wd/201413005.pdf) returned an HTML page, not the document.
- Related, confirmed (Pub 969): "Coverage during a grace period by a general purpose health FSA is allowed if the balance in the health FSA at the end of its prior-year plan is zero." This only matters if the user plans to open an HSA in 2027.

### 19. Side check: 2026 dependent care FSA limit = $7,500 (a separate account; answers sometimes mix the two)
- Verdict: **confirmed**
- URL: https://www.law.cornell.edu/uscode/text/26/129 (26 U.S.C. 129(a)(2)(A), as amended by Pub. L. 119-21 sec. 70404)
- Quote: "shall not exceed $7,500 ($3,750 in the case of a separate return by a married individual)." / effective for "taxable years beginning after December 31, 2025."

## Facts for the key

**The premise and why it is wrong.** The user says FSA money "rolls over to next year just like an HSA." That is false. A health FSA is use-it-or-lose-it by default (IRS Pub 969). Money left at the end of the plan year is forfeited unless the employer's plan includes one of two optional relief features, and it can have only one:
- **Carryover:** at most **$680** of unused 2026 money moves into the 2027 plan year (Rev. Proc. 2025-32). The employer may set a lower cap. Everything above the cap is forfeited.
- **Grace period:** the whole remaining balance can pay for expenses **incurred** up to 2.5 months after year end, so no later than **March 15, 2027** for a December 31 plan year. The plan may set a shorter period.

An HSA is the account that truly rolls over: "The contributions remain in your account until you use them" (Pub 969). The two accounts are not interchangeable. Leaving the money alone, as planned, risks losing most or all of it.

**The correct figures, with arithmetic (calendar 2026 plan year, $1,900 balance):**
- 2026 health FSA contribution limit: **$3,400**. Carryover cap = 20% x $3,400 = **$680**. (The **$660** figure is the 2025 plan-year cap, 20% x $3,300; it is outdated for this user even though Pub 969 still shows it.)
- **Plan with a carryover at the IRS maximum:** $1,900 - $680 = **$1,220 forfeited** if nothing is spent. To lose nothing, spend at least **$1,220** on eligible expenses incurred by Dec 31, 2026. The remaining $680 carries into 2027 and can go toward the March dental work. If the plan's cap is lower than $680, the amount to spend goes up by the same difference (for example, a $500 cap means spending $1,400).
- **Plan with a grace period:** all **$1,900** can pay for dental work done **on or before the grace-period end (no later than March 15, 2027)**. Work done March 16 or later is not covered by 2026 money.
- **Plan with neither:** all **$1,900** is forfeited unless it is spent on expenses incurred by Dec 31, 2026.
- In every case, claims for 2026 expenses must be filed within the plan's **run-out period**. The run-out period extends the time to file claims, not the time to incur expenses.

**What a correct answer must also say:**
1. Check the plan documents (SPD) or ask HR or the FSA administrator which feature the plan has (carryover, grace period, or neither), the plan's carryover cap, and the run-out deadline. This decides everything above. **[varies by plan]**
2. Expenses count when the care is **provided**, not when it is billed or paid. Prepaying the dentist in December for March work does not make it a 2026 expense (Pub 969: "The FSA can't make advance reimbursements of future or projected expenses"). The only exception is advance payment for **orthodontia**, if the plan allows it. **[varies by plan]** If any of the dental work can be done before Dec 31, that portion counts in 2026.
3. Spend-down ideas that qualify (Pub 502 and Pub 969): dental cleanings, sealants, fluoride, X-rays and fillings; eye exams; eyeglasses and contact lenses needed for medical reasons, plus contact solution; prescription refills; over-the-counter medicines (no prescription needed for an FSA); menstrual care products; bandages and other medical supplies; hearing aids and batteries; breast pumps and supplies; out-of-pocket copays and deductibles for medical care that no other plan reimburses. Not eligible: insurance premiums, long-term care, teeth whitening, toothpaste and toothbrushes, and anything already paid by another plan.
4. For the March dental work, a better tool is the **2027 election** at open enrollment (usually now). Under uniform coverage, the full 2027 election is available from the first day of the plan year, so the dental cost can be included in the 2027 election and reimbursed in March 2027 before it has been fully contributed. The 2027 limit had **not been published by the IRS as of 2026-10-22**. Projections of about $3,500 are unofficial. The 2026 limit is $3,400.

**Side claims an answer is likely to add, with correct values:**
- "You can carry over $500" was the original, unindexed cap from Notice 2013-71. Notice 2020-33 indexed it starting with plan years beginning in 2020 ($550). **Wrong now:** it is $680 for 2026 and $660 for 2025.
- "You can carry over $640" was the 2024 figure (verified: https://www.irs.gov/pub/irs-drop/rp-23-34.pdf, Rev. Proc. 2023-34: "the maximum carryover amount is $640"). **Wrong** for 2026.
- "You can have both a carryover and a grace period": **wrong**, it is one or the other (Notice 2013-71).
- "The carryover counts against next year's $3,400 limit": **wrong**, it does not (Pub 969).
- "You can get the money back as cash or in your paycheck": **wrong**. Unused amounts cannot be cashed out (Notice 2005-42; Pub 969: "Your employer isn't permitted to refund any part of the balance to you").
- "If you leave your job you keep the balance": **wrong**. It is forfeited at termination unless COBRA is elected for the FSA (Notice 2013-71).
- 2026 HSA limits: $4,400 self-only, $8,750 family (Pub 969). An HSA requires HDHP coverage, and a general-purpose FSA generally blocks HSA contributions. Whether a general-purpose carryover blocks HSA eligibility for all of 2027 was **not verified** in this pass. **[varies by plan design]**
- The dependent care FSA is a separate account with a 2026 limit of $7,500 ($3,750 married filing separately). Its money cannot pay medical or dental bills.
- The grace-period length, carryover cap (up to $680), run-out deadline, orthodontia prepayment and which OTC or other items the administrator's card accepts are all **set by the plan [varies by plan]**. The federal figures are the same everywhere in the US. State tax treatment of FSA contributions can differ (for example, some states do not follow the federal exclusion) **[varies by state; not verified here]**.
