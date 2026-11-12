# Adversarial check: en-fsa-rollover.md, "Facts for the key"

Checked 2026-10-22 by an agent that did not write the source file. On disk I read only `en-fsa-rollover.md`. Every URL below was opened on that date, either with WebFetch or by downloading the PDF from that URL and extracting its text. Quotes are verbatim, two lines at most. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: no 2025 or 2026 change to the health FSA carryover or grace-period rules was found. The Pub 969 HTML page was updated 30-Apr-2026 and states the same rules. The § 125 page at law.cornell.edu shows no amendment after 2018. The only FSA change in Pub. L. 119-21 (OBBBA) is the dependent care limit. The IRS newsroom lists releases through IR-2026-125 (Oct 21, 2026). I also checked every IRS 2026 revenue procedure published at irs.gov/pub/irs-drop/rp-26-20.pdf through rp-26-50.pdf. The 2027 HSA figures are out (Rev. Proc. 2026-24), but no § 125(i) figure for 2027 has been published.

Tooling note: the shared WebSearch budget ran out partway through this check. All later checks used direct fetches of known primary URLs.

## The premise

**F1. A health FSA is use-it-or-lose-it by default and does not roll over like an HSA.**
Status: **stands**
- URL: https://www.irs.gov/publications/p969 (Publication 969 (2025), "Page Last Reviewed or Updated: 30-Apr-2026")
- Quote: "FSAs are generally “use-it-or-lose-it” plans." / "This means that amounts in the account at the end of the plan year can’t generally be carried over to the next year."

**F2. Leftover money is forfeited unless the plan has one of two optional features, and a plan can have only one.**
Status: **stands**
- URL: https://www.irs.gov/publications/p969
- Quote: "However, the plan can provide for either a grace period or a carryover." / "A plan adopting a carryover provision is not permitted to also provide a grace period with respect to health FSAs."
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf (Notice 2013-71). This shows both features are optional.
- Quote: "the plan may specify a lower amount as the permissible maximum (and the plan sponsor has the option of not permitting any carryover at all)."
- URL: https://www.irs.gov/pub/irs-drop/n-05-42.pdf (Notice 2005-42)
- Quote: "A cafeteria plan document may, at the employer’s option, be amended to provide for a grace period immediately following the end of each plan year."

**F3. Carryover: at most $680 of unused 2026 money moves into the 2027 plan year. The employer may set a lower cap, and anything above the cap is forfeited.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf (Rev. Proc. 2025-32, section 4.15)
- Quote: "For taxable years beginning in 2026, the dollar limitation under § 125(i) on voluntary employee salary reductions for contributions to health flexible spending arrangements is $3,400. If the cafeteria plan permits the carryover of unused amounts, the maximum carryover amount is $680."
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf
- Quote: "Any unused amount in excess of $500 (or a lower amount specified in the plan) that remains unused as of the end of the plan year (that is, at the end of the run-out period for the plan year) is forfeited."
- Optional precision: the forfeiture is measured at the end of the run-out period, so claims for 2026 expenses filed during the run-out still reduce the amount over the cap.

**F4. Grace period: the whole balance can pay for expenses incurred up to 2.5 months after year end, so no later than March 15, 2027. The plan may set a shorter period.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/n-05-42.pdf
- Quote: "The grace period must not extend beyond the fifteenth day of the third calendar month after the end of the immediately preceding plan year"
- Same notice, with a worked date for a Dec 31 plan year: "(March 15, 2006 for the plan year ending December 31, 2005)." For a plan year ending 2026-12-31, the latest end is 2027-03-15. "Must not extend beyond" allows a shorter period.

**F5. An HSA is the account that truly rolls over.**
Status: **stands**
- URL: https://www.irs.gov/publications/p969
- Quote: "The contributions remain in your account until you use them."

**F6. Leaving the money alone risks losing most or all of it.**
Status: **stands** (correctly hedged)
- Derived from F3, F4 and F10. With the maximum carryover, $1,220 is lost. With neither feature, all $1,900 is lost. With a grace period that covers the March dental date, nothing is lost. "Risks" is the right word. The answer should not say the money will certainly be lost.

## The figures (calendar 2026 plan year, $1,900 balance)

**F7. 2026 limit $3,400. Carryover cap 20% × $3,400 = $680. $660 is the 2025 cap (20% × $3,300), and Pub 969 still shows $660.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf: "$3,400" and "the maximum carryover amount is $680." (quoted under F3)
- URL: https://www.irs.gov/pub/irs-drop/rp-24-40.pdf (Rev. Proc. 2024-40, section 3.16)
- Quote: "For taxable years beginning in 2025, the dollar limitation under § 125(i) on voluntary employee salary reductions for contributions to health flexible spending arrangements is $3,300. If the cafeteria plan permits the carryover of unused amounts, the maximum carryover amount is $660."
- URL: https://www.irs.gov/pub/irs-drop/n-20-33.pdf (Notice 2020-33)
- Quote: "this notice increases the maximum $500 carryover amount for a plan year to an amount equal to 20 percent of the maximum salary reduction contribution under § 125(i) for that plan year."
- URL: https://www.irs.gov/publications/p969 (live page, 2025 edition)
- Quote: "Plans may allow up to $660 of unused amounts remaining at the end of the plan year"
- Recomputed: 0.20 × 3,400 = 680. 0.20 × 3,300 = 660.

**F8. With a carryover at the IRS maximum, $1,900 − $680 = $1,220 is forfeited if nothing is spent. Spending at least $1,220 on expenses incurred by Dec 31, 2026 loses nothing. With a $500 cap, the amount to spend is $1,400.**
Status: **stands**
- Recomputed: 1,900 − 680 = 1,220. 1,900 − 500 = 1,400, which is 1,220 + (680 − 500). Sources as in F3 and F7.

**F9. With a grace period, all $1,900 can pay for dental work done on or before the grace-period end (no later than March 15, 2027). Work done March 16 or later is not covered by 2026 money.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/n-05-42.pdf
- Quote: "those remaining unused benefits or contributions may not be carried forward to any subsequent period (including any subsequent plan year) and are “forfeited” under the “use-it-or-lose-it” rule."

**F10. With neither feature, all $1,900 is forfeited unless it is spent on expenses incurred by Dec 31, 2026.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf
- Quote: "this requires that unused benefits or contributions remaining as of the end of the plan year ... be forfeited."

**F11. The run-out period extends the time to file claims, not the time to incur expenses.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf (footnote 3)
- Quote: "A “run-out period” is a period immediately following the end of a plan year during which a participant can submit a claim for reimbursement of expenses incurred for qualified benefits during the plan year."

## What a correct answer must also say

**F12. Check the plan documents (SPD), HR or the FSA administrator for which feature applies, the plan's cap and the run-out deadline. [varies by plan]**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf. The cap is set by the plan, and a carryover is optional: "the plan may specify a lower amount as the permissible maximum (and the plan sponsor has the option of not permitting any carryover at all)."

**F13. Expenses count when the care is provided, not when it is billed or paid. Prepaying the dentist in December does not create a 2026 expense.**
Status: **stands**
- URL: https://www.irs.gov/publications/p969
- Quote: "The FSA can't make advance reimbursements of future or projected expenses."
- URL: https://www.govinfo.gov/content/pkg/FR-2007-08-06/pdf/E7-14827.pdf (Prop. Treas. Reg. 1.125-6(a)(2)(ii), 72 FR 43961)
- Quote: "medical expenses are incurred when the employee (or the employee’s spouse or dependents) is provided with the medical care that gives rise to the medical expenses, and not when the employee is formally billed, charged for, or pays for the medical care."

**F14. The only exception is advance payment for orthodontia, if the plan allows it. [varies by plan]**
Status: **stands**
- URL: https://www.govinfo.gov/content/pkg/FR-2007-08-06/pdf/E7-14827.pdf (Prop. Treas. Reg. 1.125-5(k)(3)(i))
- Quote: "A cafeteria plan is permitted, but is not required to, reimburse employees for orthodontia services before the services are provided"
- Status of the source: these regulations are still proposed. The same document says: "Taxpayers may rely on these regulations for guidance pending the issuance of final regulations."

**F15. Spend-down items that qualify, and items that do not.**
Status: **stands**, item by item:
- Definition, at https://www.irs.gov/publications/p502 (Publication 502 (2025), page updated 30-Apr-2026): "They include payments for legal medical services rendered by physicians, surgeons, dentists, and other medical practitioners." This covers out-of-pocket copays and deductibles for care.
- Dental, same page: "teeth cleaning, the application of sealants, and fluoride treatments" / "X-rays, fillings, braces, extractions, dentures"
- Eyes: "You can include in medical expenses the amount you pay for eye examinations." / "You can include in medical expenses amounts you pay for eyeglasses and contact lenses needed for medical reasons."
- Contact solution: "the cost of equipment and materials required for using contact lenses, such as saline solution and enzyme cleaner"
- Prescriptions: "You can include in medical expenses amounts you pay for prescribed medicines and drugs."
- Hearing: "You can include in medical expenses the cost of a hearing aid and batteries, repairs, and maintenance needed to operate it."
- Breast pumps: "You can include in medical expenses the cost of breast pumps and supplies that assist lactation."
- Supplies: "You can include in medical expenses the cost of medical supplies such as bandages."
- OTC medicine and menstrual products, FSA-specific, at https://www.irs.gov/publications/p969: "Expenses incurred for over-the-counter medicine (whether or not prescribed)" / "and menstrual care products are considered medical care and are considered a covered expense."
- Not eligible (p502): "You can’t include in medical expenses amounts paid to whiten teeth." / "the cost of a toothbrush and toothpaste is a nondeductible personal expense."
- Not reimbursable from an FSA (p969): "Amounts paid for health insurance premiums." / "Amounts paid for long-term care." / "Amounts that are covered under another health plan."
- Statute for menstrual products: https://www.law.cornell.edu/uscode/text/26/106. 26 U.S.C. 106(f) begins: "For purposes of this section and section 105, expenses incurred for menstrual care products"

**F16. The 2027 election is the better tool for the March work. Under uniform coverage, the full 2027 election is available from the first day of the plan year.**
Status: **stands**
- URL: https://www.irs.gov/publications/p969
- Quote: "You must be able to receive the maximum amount of reimbursement" ... "at any time during the coverage period". The rest of the sentence says this holds whatever amount has been contributed so far; my fetch tool returned that part only as a paraphrase.
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf
- Quote: "The uniform coverage rule requires that the maximum amount of reimbursement from the health FSA ... be available for claims incurred at all times during the period of coverage"

**F17. As of 2026-10-22 the IRS has not published the 2027 limit. Projections of about $3,500 are unofficial. The 2026 limit is $3,400.**
Status: **stands** (as of this check)
- URL: https://www.irs.gov/newsroom/news-releases-for-current-month lists IR-2026-117 through IR-2026-125 (Oct 1 to Oct 21, 2026). None covers 2027 inflation adjustments. The newest is IR-2026-125: "Temporary reporting and recordkeeping relief for certain fuel uses".
- I opened https://www.irs.gov/pub/irs-drop/rp-26-20.pdf through rp-26-32.pdf, every number in 20 to 50 that exists. None sets a § 125(i) amount for 2027. The 2027 health-account figures that are out cover HSAs only (Rev. Proc. 2026-24, below).
- Caution for the key: the annual inflation revenue procedure usually comes out in October or November. Check again on the day the answer is graded.

## Side claims

**F18. "$500" was the original unindexed cap (Notice 2013-71). Notice 2020-33 indexed it from 2020 plan years ($550). Today it is $680 for 2026 and $660 for 2025.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/n-20-33.pdf
- Quote: "the maximum unused amount from a plan year starting in 2020 allowed to be carried over to the immediately following plan year beginning in 2021 is $550 (20 percent of $2,750, the indexed 2020 limit under § 125(i))."

**F19. "$640" was the 2024 figure.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/rp-23-34.pdf (Rev. Proc. 2023-34, section 3.16)
- Quote: "For taxable years beginning in 2024, the dollar limitation under § 125(i) ... is $3,200. If the cafeteria plan permits the carryover of unused amounts, the maximum carryover amount is $640."

**F20. A plan cannot offer both a carryover and a grace period.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf
- Quote: "A plan adopting this carryover provision is not permitted to also provide a grace period with respect to health FSAs."

**F21. The carryover does not count against next year's contribution limit.**
Status: **stands**
- URL: https://www.irs.gov/publications/p969
- Quote: "The carryover doesn’t affect the maximum amount of salary reduction contributions that you are permitted to make."

**F22. Unused money cannot be cashed out.**
Status: **stands**
- URL: https://www.irs.gov/publications/p969
- Quote: "Your employer isn’t permitted to refund any part of the balance to you."
- URL: https://www.irs.gov/pub/irs-drop/n-05-42.pdf
- Quote: "a cafeteria plan may not permit unused benefits or contributions to be cashed-out or converted to any other taxable or nontaxable benefit."

**F23. The balance is forfeited when employment ends, unless COBRA is elected for the FSA.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-drop/n-13-71.pdf
- Quote: "Any unused amount remaining in an employee’s health FSA as of termination of employment also is forfeited (unless, if applicable, the employee elects COBRA continuation coverage with respect to the health FSA)."

**F24. 2026 HSA limits are $4,400 self-only and $8,750 family. An HSA requires HDHP coverage, and a general-purpose FSA generally blocks HSA contributions.**
Status: **stands**, with one optional addition
- URL: https://www.irs.gov/publications/p969
- Quote: "For 2026, if you have self-only HDHP coverage, you can contribute up to $4,400." / "If you have family HDHP coverage, you can contribute up to $8,750."
- Addition: the 2027 HSA limits are now official. Use them if the answer talks about opening an HSA for 2027. URL: https://www.irs.gov/pub/irs-drop/rp-26-24.pdf (Rev. Proc. 2026-24, section 3.01)
- Quote: "For calendar year 2027, the annual limitation on deductions under section 223(b)(2)(A) for an individual with self-only coverage under a high deductible health plan is $4,500." / "... with family coverage under a high deductible health plan is $9,000."

**F25. "Whether a general-purpose carryover blocks HSA eligibility for all of 2027 was not verified."**
Status: **refuted/needs change**. This can now be decided. The URL the source tried (`https://www.irs.gov/pub/irs-wd/201413005.pdf`) returns an IRS 404 page. The document is filed under the 7-digit name.
- URL: https://www.irs.gov/pub/irs-wd/1413005.pdf (Chief Counsel Advice 201413005, released 3/28/2014. It is non-precedential: "This advice may not be used or cited as precedent.")
- Quote (Issue 2): "an individual covered by a general purpose health FSA solely as the result of a carryover of unused amounts in a health FSA may not contribute to an HSA even for months in the plan year after the health FSA no longer has any amounts available"
- Quote (Issues 4 and 6, the exceptions): carrying the money into an HSA-compatible health FSA leaves the person "eligible to contribute to an HSA during the following year", and a person who declines the carryover, where the plan permits, "may contribute to an HSA during the following year".
- Corrected wording: "IRS Chief Counsel advice (CCA 201413005, non-precedential) says a carryover into a general-purpose health FSA blocks HSA contributions for the whole following plan year, even after the carried-over money is used up. The exceptions are when the plan carries the money into a limited-purpose or post-deductible (HSA-compatible) FSA, or lets the employee decline the carryover. This matters only if the user plans to open an HSA in 2027. [varies by plan design]"

**F26. The dependent care FSA is a separate account: $7,500 for 2026 ($3,750 married filing separately). Its money cannot pay medical or dental bills.**
Status: **stands**
- URL: https://www.law.cornell.edu/uscode/text/26/129
- Quote: "shall not exceed $7,500 ($3,750 in the case of a separate return by a married individual)." / effective for "taxable years beginning after December 31, 2025."
- Same page, § 129(e)(1): dependent care assistance covers services that "would be considered employment-related expenses under section 21(b)(2)". That excludes medical care. The page shows no inflation indexing for the $7,500.

**F27. Plan-set items (grace length, cap up to $680, run-out deadline, orthodontia prepayment, items the card accepts) [varies by plan]. Federal figures are uniform nationwide. State tax treatment can differ [varies by state; not verified here].**
Status: **stands**. The state part can be partly decided with one example.
- Plan-set items: Notice 2013-71 ("a lower amount specified in the plan") and Notice 2005-42 ("must not extend beyond"), quoted above.
- State example. URL: https://www.nj.gov/treasury/taxation/pdf/current/njwt.pdf (NJ-WT, New Jersey Income Tax Withholding Instructions, September 2025). Under "Compensation Subject to Withholding":
- Quote: "Amounts an employee takes out of cafeteria plans even if the employee elects to receive benefits rather than cash"
- Suggested wording: "State treatment can differ. For example, New Jersey's employer withholding guide treats cafeteria-plan amounts as state wages, except for limited plan types. [varies by state]" The NJ guide does not name health FSAs specifically, so it should not be stated more strongly than that.

## Not decided in this pass
- The official 2027 § 125(i) limit and 2027 carryover cap. They are unpublished as of 2026-10-22, and the projections ($3,500 / $700) cannot be recomputed without the C-CPI-U figures, which were not fetched.
- Whether a plan may make the carryover conditional on enrolling in the next year's FSA. Notice 2013-71 neither allows nor forbids this. Its Example 2 carries money over for a participant who "elects no salary reduction for the health FSA" in the following year. If the key mentions this, it should stay a "check your plan" point.
