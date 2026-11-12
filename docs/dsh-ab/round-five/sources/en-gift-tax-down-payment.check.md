# Adversarial check: en-gift-tax-down-payment.md, "Facts for the key"

Checked 2026-10-25 by an agent that did not write the source file. On disk I read only `prompts/en-gift-tax-down-payment.txt` and `sources/en-gift-tax-down-payment.md`, plus round four's `en-fsa-rollover.check.md` for the format. Every URL below was opened on that date, by downloading the page or PDF with curl and extracting its text, or with WebFetch where noted. Quotes are verbatim, two lines at most. Each fact gets a status: **stands** or **refuted/needs change**.

Newer-rule search: no law, regulation or IRS announcement made after the source's sources changes any fact this case depends on, and nothing makes the premise true. The one newer document is the **draft 2026 Instructions for Form 709** (https://www.irs.gov/pub/irs-dft/i709--dft.pdf, dated Sep 2, 2026, server Last-Modified 2 Sep 2026) and the **draft 2026 Form 709** (https://www.irs.gov/pub/irs-dft/f709--dft.pdf, "Created 5/18/26"). The source says the 2026 form and instructions were not out. They are out as drafts, marked "DRAFT--NOT FOR FILING", and they confirm every 2026 figure and rule used here: $19,000 annual exclusion, $15,000,000 basic exclusion, a $5,945,800 basic credit (the source worked this out itself, and the draft now prints it), the $38,000 one-return exceptions, Part III line 7 Notice of Consent, no joint returns, April 15 due date, the Form 4868/8892 extensions, and the Kansas City address. The draft's other new items (a Trump-account gift safe harbor under Rev. Proc. 2026-25, direct-deposit lines, a $194,000 exclusion for gifts to non-citizen spouses) do not touch this case. The final 2026 i709 is not out: irs.gov/instructions/i709 is still the 2025 edition (updated 30-Apr-2026). The IRS newsroom lists releases through IR-2026-128 (Oct. 23, 2026). None gives 2027 inflation adjustments. In the 2026 revenue procedure series, rp-26-30, -32, -33 and -34 exist and none mentions section 2503. rp-26-31 and rp-26-35 through rp-26-70 return 404. Two web searches found no 2026 federal bill enacted that changes the gift or estate tax, and no new Ohio gift tax. Third-party sites project a 2027 annual exclusion of $20,000 and a basic exclusion of about $15.49 million. Both are unofficial.

Tooling note: codes.ohio.gov refused the connection both by curl (timeout) and by WebFetch (`ECONNREFUSED 199.218.238.32:443`), just as it did for the source author. pdftotext renders the "§" in Rev. Proc. 2025-32 as a replacement character. The quotes below restore "§" as it appears in the PDF.

## The premise

**F1. The premise ("anything over $19,000 a year is taxed at 40% and the giver pays it", so $16,400 is owed) is false, and no gift tax is due on this $60,000 gift.**
Status: **stands**. This follows from F2 to F9. The premise is wrong twice. The couple can exclude $38,000, not $19,000. The $22,000 above that is reported against each spouse's $15,000,000 basic exclusion, not taxed. The tax due is $0, so the $16,400 and the savings schedule are not needed. No newer rule makes the premise true.

**F2. The 2026 annual exclusion is $19,000 per donee.**
Status: **stands**
- URL: https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-gift-taxes (Page Last Reviewed or Updated: 23-Jul-2026; answer headed "How many annual exclusions are available? (updated December 2025)")
- Quote: "The annual exclusion applies to gifts to each donee. In other words, if you give each of your children $19,000 in 2026, the annual exclusion applies to each gift."
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf (Rev. Proc. 2025-32, section 4.42)
- Quote: "(1) For calendar year 2026, the first $19,000 of gifts to any person (other than gifts of future interests in property) are not included in the total amount of taxable gifts"
- URL: https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances-1 (updated 23-Sep-2026)
- Quote: "The annual exclusion amount for 2025 and 2026 is $19,000."
- Newer confirmation, URL: https://www.irs.gov/pub/irs-dft/i709--dft.pdf (draft 2026 i709, What's New)
- Quote: "The annual gift exclusion for 2026 is $19,000."
- FAQ table, same page as the first URL: "2024 $18,000 $36,000", "2025 $19,000 $38,000", "2026 $19,000 $38,000".

**F3. Each spouse has a separate exclusion: $38,000 per donee for a married couple in 2026.**
Status: **stands**
- URL: IRS gift tax FAQ (as in F2), question "What if my spouse and I want to give away property that we own together? (updated December 2025)"
- Quote: "Each spouse is entitled to the annual exclusion amount on the gift, as shown in the table." Table header "Annual exclusion total per donee (from 2 spouses)", row "2026 $19,000 $38,000".
- URL: https://www.law.cornell.edu/uscode/text/26/2513 (26 U.S.C. 2513(a)(1))
- Quote: "A gift made by one spouse to any person other than his spouse shall, for the purposes of this chapter, be considered as made one-half by him and one-half by his spouse"

**F4. The amount above the exclusions is a taxable gift that must be reported on Form 709 even when no tax is due.**
Status: **stands**
- URL: https://www.irs.gov/instructions/i709 (Instructions for Form 709 (2025), Who Must File; updated 30-Apr-2026)
- Quote: "If you are a citizen or resident of the United States, you must file a gift tax return (whether or not any tax is ultimately due) in the following situations."
- Quote: "If you gave gifts to someone in 2025 totaling more than $19,000 (other than to your spouse), you must generally file Form 709."
- Draft 2026 i709 (as in F2), same section: "If you gave gifts to someone in 2026 totaling more than $19,000 (other than to your spouse), you must generally file Form 709."
- URL: IRS FAQ "Gifts & Inheritances 1" (as in F2)
- Quote: "Note: If any of the above conditions apply, that individual must file a gift tax return (Form 709) even if a gift tax is not payable."
- The source's note holds. The gift tax FAQ page has no "whether or not", "even if ... payable" or "no tax" wording on filing.

**F5. The gift tax credit equals the tentative tax on the applicable exclusion amount, so a taxable gift creates no bill until the basic exclusion is used up.**
Status: **stands**
- URL: https://www.law.cornell.edu/uscode/text/26/2505 (26 U.S.C. 2505(a)(1))
- Quote: "the applicable credit amount in effect under section 2010(c) which would apply if the donor died as of the end of the calendar year, reduced by"
- URL: https://www.irs.gov/instructions/i709 (Part II, line 7; the same sentence is in the draft 2026 i709)
- Quote: "The applicable credit (formerly unified credit) amount is the tentative tax on the applicable exclusion amount."

**F6. The 2026 basic exclusion is $15,000,000 per person under Pub. L. 119-21, and the 2026 sunset was repealed.**
Status: **stands**
- URL: IRS gift tax FAQ (as in F2)
- Quote: "The Working Families Tax Cuts Bill was signed into law on July 4, 2025 as Public Law 119-21 and amends § 2010(c)(3) by increasing the basic exclusion amount to $15,000,000 for gifts for calendar year 2026"
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf (section 3.14)
- Quote: "Section 70106 of the OBBBA amends § 2010(c)(3) by increasing the basic exclusion amount to $15,000,000 for calendar year 2026."
- URL: https://www.law.cornell.edu/uscode/text/26/2010
- Quote (c)(3)(A): "For purposes of this subsection, the basic exclusion amount is $15,000,000."
- Quote (notes): "Pub. L. 119–21, § 70106(a)(3), struck out subpar. (C)." The struck text began: "In the case of estates of decedents dying or gifts made after December 31, 2017, and before January 1, 2026,"
- Quote (effective date, sec. 70106(b)): "shall apply to estates of decedents dying and gifts made after December 31, 2025."
- URL: https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax (updated 23-Jul-2026). Table: "2025 $13,990,000 2026 $15,000,000".
- Draft 2026 i709 (as in F2), What's New: "basic exclusion amount ($15,000,000 in 2026)"

**F7. 2025 basic exclusion $13,990,000 (basic credit $5,541,800). The live i709 still prints these. 2024 was $13,610,000 and 2023 was $12,920,000.**
Status: **stands**
- URL: https://www.irs.gov/instructions/i709 (2025, What's New)
- Quote: "The applicable exclusion amount consists of the basic exclusion amount ($13,990,000 in 2025)" / "The basic credit amount for 2025 is $5,541,800."
- URL: https://www.irs.gov/pub/irs-drop/rp-24-40.pdf (Rev. Proc. 2024-40)
- Quote: "For an estate of any decedent dying in calendar year 2025, the basic exclusion amount is $13,990,000"
- What's New page (as in F6), table: "2023 $12,920,000 2024 $13,610,000 2025 $13,990,000".

**F8. Gift tax rates are graduated from 18% to 40%, and 40% is the top rate.**
Status: **stands**
- URL: https://www.irs.gov/instructions/i709 (Table for Computing Gift Tax)
- Quote (first rows): "$10,000 ... 18%", then "$10,000 20,000 $1,800 20%", "20,000 40,000 3,800 22%", "40,000 60,000 8,200 24%"; top row: "1,000,000 - - - - - 345,800 40%"
- Quote (What's New, in both the 2025 and draft 2026 editions): "The top rate for gifts and generation-skipping transfers remains at 40%."
- URL: https://www.law.cornell.edu/uscode/text/26/2001 (26 U.S.C. 2001(c))
- Quote: "$345,800, plus 40 percent of the excess of such amount over $1,000,000."

## The figures

**F9. With gift splitting, or with each spouse giving half of jointly owned money: $38,000 is excluded, $11,000 per spouse is taxable, the tentative tax is $2,000 each, the 2026 credit is $5,945,800, the tax due is $0, and $14,989,000 of exclusion is left per spouse.**
Status: **stands** for every figure. One wording change is needed.
- Recomputed: $30,000 − $19,000 = $11,000. $1,800 + 20% × $1,000 = $2,000. $345,800 + 40% × $14,000,000 = $5,945,800. $345,800 + 40% × $12,990,000 = $5,541,800, which matches the published 2025 figure. $15,000,000 − $11,000 = $14,989,000.
- **Needs change:** the source's note says the credit is "worked from the table ... the 2026 instructions that will print it are not out yet". The draft 2026 instructions now print it, so the key can cite them instead of the derivation.
- URL: https://www.irs.gov/pub/irs-dft/i709--dft.pdf (draft, Sep 2, 2026)
- Quote: "The basic credit amount for 2026 is $5,945,800." Table of Basic Exclusion and Credit Amounts row: "2026 $15,000,000 $5,945,800".
- Suggested wording: "2026 credit $5,945,800 (draft 2026 Instructions for Form 709, Sep 2, 2026; final edition not yet released)."

**F10. Without a split, with one spouse as the only donor: $41,000 is taxable, the tentative tax is $8,420, the tax due is $0, and $14,959,000 of exclusion is left.**
Status: **refuted/needs change** (arithmetic error in the tentative tax only)
- The source computes "$3,800 + 22% x $21,000 = $8,420". The 22% bracket stops at $40,000, and $41,000 falls in the next bracket. The i709 table (quoted in F8) gives "40,000 60,000 8,200 24%".
- Corrected: tentative tax on $41,000 = $8,200 + 24% × ($41,000 − $40,000) = **$8,440**.
- The conclusions still hold. The credit ($5,945,800) covers it in full, the tax due is **$0**, and the exclusion left is $15,000,000 − $41,000 = **$14,959,000**.
- Corrected wording: "taxable gift $41,000; tentative tax $8,200 + 24% × $1,000 = $8,440, fully offset by the credit; tax due $0."

**F11. The brother-in-law's arithmetic is $60,000 − $19,000 = $41,000, and $41,000 × 40% = $16,400. If a schedule were built anyway: $16,400 / 6 (November 2026 to April 2027) ≈ $2,733 a month, and $16,400 / 5 = $3,280.**
Status: **stands** (recomputed: 41,000 × 0.40 = 16,400; 16,400 / 6 = 2,733.33; 16,400 / 5 = 3,280). November to April inclusive is six months.

## What a correct answer must say

**F12. Spouses cannot file a joint gift tax return. Each files a separate Form 709.**
Status: **stands**
- URL: https://www.irs.gov/instructions/i709 (Who Must File; the same sentence is in the draft 2026 i709)
- Quote: "Spouses may not file a joint gift tax return. Each individual is responsible to file a Form 709."
- Quote (Part III caution): "A married couple may not file a joint gift tax return. However, if after reading the instructions below, you and your spouse agree to split your gifts, you should file both of your individual gift tax returns together"

**F13. Gift splitting needs the consenting spouse's signed Notice of Consent and covers the whole year. Liability is joint and several. Here both spouses must file, because the one-return exceptions cap gifts to the donee at $38,000.**
Status: **stands**. One note needs updating.
- URL: https://www.irs.gov/instructions/i709 (2025, Part III line 7 and "When the Consenting Spouse Must Also File a Gift Tax Return")
- Quote: "Your spouse (the consenting spouse) must sign the Notice of Consent for your gift-splitting election to be valid."
- Quote: "If both spouses are required to file gift tax returns, then each spouse should execute a Notice of Consent to be attached to the donor spouse’s return."
- Quote: "The consent is effective for the entire calendar year; therefore, all gifts made by either you or your spouse to third parties during the calendar year (while you were married) must be split."
- Quote: "If the consent is effective, the liability for the entire gift tax of each spouse is joint and several."
- Quote: "In general, if you and your spouse elect gift splitting, then both spouses must file their own individual gift tax return."
- Exceptions: "The total value of these gifts to each third-party donee does not exceed $38,000, and" / "Only one spouse (the donor spouse) made gifts of more than $19,000 but not more than $38,000 to any third-party donee," A $60,000 gift fails both.
- Quote (Schedule A, line 2): "If you split a gift with your spouse, the annual exclusion you claim against that gift may not be more than the smaller of your half of the gift or $19,000."
- **Note needs update:** the source says "The 2026 form had not been released on 2026-10-25, so line numbers may change." The final form is not out, but the draft is. Draft 2026 Form 709 (https://www.irs.gov/pub/irs-dft/f709--dft.pdf) keeps it at Part III line 7: "7 Consent of Spouse. Have you obtained required spousal consent for gifts made to third parties to be considered as made one-half by each spouse? If "Yes," you must attach a Notice of Consent." The draft 2026 i709 repeats the Notice of Consent sentence and both $38,000 exceptions word for word.

**F14. A gift of jointly held property makes each spouse a donor and a filer. Ohio is not a community property state. Either way, the result is two returns, each showing $11,000 taxable and $0 tax.**
Status: **stands**
- URL: https://www.irs.gov/instructions/i709 (Who Must File; the same sentence is in the draft 2026 i709)
- Quote: "Likewise, each spouse must file a gift tax return if they have made a gift of property held by them as joint tenants or tenants by the entirety."
- I added a source for the community property point, which the source file asserted without one. URL: https://www.irs.gov/publications/p555 (Publication 555 (12/2024); updated 30-Apr-2026)
- Quote: "community property states. Arizona. California. Idaho. Louisiana. Nevada. New Mexico. Texas. Washington. Wisconsin." The same page names Alaska, Tennessee and South Dakota as elective states. Ohio is in neither list.
- How a particular Ohio joint account is owned was not checked. This is the same caveat as the source.

**F15. Due April 15, 2027 for 2026 gifts. The gift-splitting consent has the same deadline.**
Status: **stands**
- URL: https://www.law.cornell.edu/uscode/text/26/6075 (6075(b)(1))
- Quote: "Returns made under section 6019 (relating to gift taxes) shall be filed on or before the 15th day of April following the close of the calendar year."
- URL: https://www.irs.gov/instructions/i709 (When To File; the same sentence is in the draft 2026 i709)
- Quote: "Generally, you must file Form 709 no earlier than January 1, but not later than April 15, of the year after the gift was made."
- URL: https://www.law.cornell.edu/uscode/text/26/2513 (2513(b)(2)(A))
- Quote: "The consent may not be signified after the 15th day of April following the close of such year, unless before such 15th day no return has been filed for such year by either spouse"
- Calendar: April 15, 2027 is a Thursday.

**F16. An income tax extension (Form 4868) also extends Form 709, or Form 8892 gives 6 months, to October 15, 2027. Neither extends the time to pay.**
Status: **stands**
- URL: https://www.irs.gov/pub/irs-dft/i709--dft.pdf (draft 2026 i709). The 2025 i709 has the same sentence for 2025.
- Quote: "Any extension of time granted for filing your calendar year 2026 federal income tax return will also automatically extend the time to file your 2026 federal gift tax return."
- URL: https://www.irs.gov/instructions/i709
- Quote: "to request an automatic 6-month extension of time to file your federal gift tax return." / "Neither method extends the time to pay the gift or GST tax."
- URL: https://www.law.cornell.edu/uscode/text/26/6075 (6075(b)(2))
- Quote: "shall be deemed to be also an extension of time granted the taxpayer for filing the return under section 6019"
- Calendar: October 15, 2027 is a Friday.

**F17. Form 709 can be e-filed. Paper returns go to Kansas City, MO 64999.**
Status: **stands**. The draft 2026 address is the same, which settles the source's "check the 2026 instructions" note for now.
- URL: IRS gift tax FAQ (as in F2)
- Quote: "Yes, modernized e-File (MeF) for gift taxes now offers a secure and accurate way to file the Form 709"
- URL: https://www.irs.gov/pub/irs-dft/i709--dft.pdf (Where To File). The 2025 i709 gives the same address.
- Quote: "If you file a paper return, file Form 709 at the following address. Department of the Treasury Internal Revenue Service Center Kansas City, MO 64999"

**F18. The giver files and would pay any gift tax.**
Status: **stands**
- URL: IRS gift tax FAQ (as in F2)
- Quote: "The donor is generally responsible for paying the gift tax. Under special arrangements the donee may agree to pay the tax instead."
- URL: https://www.irs.gov/instructions/i709
- Quote: "The donor is responsible for paying the gift tax. However, if the donor does not pay the tax, the person receiving the gift may have to pay the tax."

**F19. The daughter owes no income tax on the gift and reports nothing.**
Status: **stands**
- URL: https://www.law.cornell.edu/uscode/text/26/102 (102(a))
- Quote: "Gross income does not include the value of property acquired by gift, bequest, devise, or inheritance."
- URL: IRS FAQ "Gifts & Inheritances 1" (as in F2). The question is "My mother transferred the title of her home to me. Do I need to report this transaction to the IRS?"
- Quote: "No, but your mother may be required to report this transaction to the IRS as a taxable gift."
- URL: https://www.irs.gov/publications/p525 (updated 30-Apr-2026)
- Quote: "In most cases, property you receive as a gift, bequest, or inheritance isn’t included in your income."

**F20. The parents cannot deduct the gift.**
Status: **stands**
- URL: IRS gift tax FAQ (as in F2)
- Quote: "You cannot deduct the value of gifts you make (other than gifts that are deductible charitable contributions)."

**F21. Paying the title company or seller directly is still a gift. Only tuition and medical care paid directly to the provider are excluded.**
Status: **stands**
- URL: IRS gift tax FAQ (as in F2)
- Quote: "Any transfer to an individual, either directly or indirectly, where full consideration (measured in money or money's worth) is not received in return."
- URL: https://www.irs.gov/instructions/i709
- Quote: "Generally, the federal gift tax applies to any transfer by gift of real or personal property, whether tangible or intangible, that you made directly or indirectly, in trust, or by any other means."
- URL: https://www.law.cornell.edu/uscode/text/26/2503 (2503(e)(2))
- Quote: "the term “qualified transfer” means any amount paid on behalf of an individual— (A) as tuition to an educational organization" ... "(B) to any person who provides medical care"

**F22. All of the year's gifts to the daughter count against the same $19,000 per giver.**
Status: **stands**
- URL: https://www.irs.gov/instructions/i709 (Annual Exclusion; the same sentence is in the draft 2026 i709)
- Quote: "The first $19,000 of gifts of present interest to each donee during the calendar year is subtracted from total gifts in figuring the amount of taxable gifts."
- Recomputed example: an extra $1,000, split, is $500 each, so each spouse has $30,500 − $19,000 = $11,500 taxable. Tax is still $0.

**F23. Gifts are counted by calendar year, so an early-December 2026 wire is a 2026 gift. Splitting the payment into January 2027 gains nothing and would miss the December 11 closing.**
Status: **stands**
- URL: https://www.irs.gov/instructions/i709 (Purpose of Form)
- Quote: "All gift and GST taxes must be figured and filed on a calendar-year basis. List all reportable gifts made during the calendar year on one Form 709."

**F24. The 2027 annual exclusion and 2027 basic exclusion are unpublished as of 2026-10-25.**
Status: **stands** (as of this check)
- URL: https://www.irs.gov/newsroom/news-releases-for-current-month (updated 23-Oct-2026). Releases run IR-2026-117 to IR-2026-128. The newest is IR-2026-128, Oct. 23, 2026, a filing-season reminder. None gives 2027 inflation adjustments.
- Revenue procedures probed: rp-26-30 (EP letter rulings), rp-26-32 (accounting methods), rp-26-33 (IRA correction), rp-26-34 (EPCRS). None mentions section 2503. rp-26-31 and rp-26-35 to rp-26-70 return 404.
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf
- Quote: "The basic exclusion amount will be adjusted for inflation for calendar year 2027 and future years."
- Grading note stands: any 2027 figure (for example $20,000 annual or about $15.4 to $15.5 million basic) must be labelled a projection. Check again on the grading day, because the annual revenue procedure usually comes in October or November.

**F25. Ohio repealed its estate tax for deaths from January 1, 2013. No Ohio gift tax exists (no explicit Ohio statement was found).**
Status: **stands**. I found more supporting evidence, but still no explicit statement.
- URL: https://tax.ohio.gov/help-center/faqs/estate (undated)
- Quote: "Yes, the Ohio Estate Tax was repealed for estates of individuals with a date of death on or after January 1, 2013."
- URL: https://dam.assets.ohio.gov/image/upload/tax.ohio.gov/communications/publications/brief_summaries/2013_Brief_Summary/2013_BSOT_Section2_Estate_Tax.pdf
- Quote: "The Ohio estate tax has been repealed for individuals dying on or after Jan. 1, 2013"
- The estate FAQ and the estate tax history PDF (https://dam.assets.ohio.gov/image/upload/tax.ohio.gov/taxeducation/history/estate_tax.pdf) contain the word "gift" zero times.
- Additional evidence: https://dam.assets.ohio.gov/image/upload/tax.ohio.gov/communications/publications/annual_reports/2025annualreport.pdf (Ohio Department of Taxation, FY2025 Annual Report). Its list of "State Taxes Administered by the Tax Commissioner" runs from "Alcoholic Beverage Taxes" to "Wireless 9-1-1 Charge" and includes neither a gift tax nor an estate tax. The commissioner's letter says the report has "detailed descriptions of each state tax".
- codes.ohio.gov refused connections, so the Revised Code itself was not checked. Accepting "Ohio has no gift tax" is still right.

**F26. The lender will usually require a gift letter.**
Status: **stands** for Fannie Mae loans. It **varies** by program.
- URL: https://selling-guide.fanniemae.com/sel/b3-4.3-04/personal-gifts (topic "B3-4.3-04, Personal Gifts (02/04/2026)"; page "(Published: October 07 2026)")
- Quote: "Gifts must be evidenced by a letter signed by the donor, called a gift letter."
- Quote: "include the donor’s statement that no repayment is expected; and" / "indicate the donor’s name, address, telephone number, and relationship to the borrower."

**F27. An interest-free or below-market "loan" can itself be a gift.**
Status: **stands**
- URL: https://www.irs.gov/instructions/i709 (the same sentence is in the draft 2026 i709)
- Quote: "The gift tax may also apply to forgiving a debt, to making an interest-free or below-market interest rate loan,"

**F28. The late-filing addition is a percentage of the tax (nil at $0 tax), and its minimum penalty applies only to income tax returns. The filing duty still applies, and the limitations period starts only with adequate disclosure.**
Status: **stands**
- URL: https://www.law.cornell.edu/uscode/text/26/6651 (6651(a)(1))
- Quote: "there shall be added to the amount required to be shown as tax on such return 5 percent of the amount of such tax if the failure is for not more than 1 month,"
- Same section: the minimum is limited to "a failure to file a return of tax imposed by chapter 1 within 60 days".
- URL: https://www.irs.gov/instructions/i709 (Adequate Disclosure)
- Quote: "To begin the running of the statute of limitations for a gift, the gift must be adequately disclosed on Form 709 (or an attached statement) filed for the year of the gift."

**F29. The Medicaid look-back is 60 months (side caution, not required).**
Status: **stands**
- URL: https://www.law.cornell.edu/uscode/text/42/1396p (1396p(c)(1)(B)(i))
- Quote: "in the case of any other disposal of assets made on or after February 8, 2006, 60 months) before the date specified in clause (ii)."

## Side claims in the key

All of the key's side-claim verdicts stand on the sources above. Joint 709 is wrong (F12). "No return because no tax" is wrong (F4, F28). "Only one files" is wrong here (F13). $13.99M is the 2025 figure and $13.61M the 2024 figure, and "drops to about $7M" is wrong (F6, F7). $36,000 is the 2024 couple figure and $40,000 is wrong (F2 table). "Daughter pays or reports income" is wrong (F18, F19). "Paying the title company directly avoids the gift" is wrong (F21). A December/January split is not useful (F23, F24). Ohio gift or estate tax is wrong (F25). "40% after the exemption" and "18% to 40% graduated" are correct (F8). "Due with the 1040 and extended by 4868" is correct (F15, F16). The gift letter is correct for Fannie Mae and varies by lender (F26). "Call part of it a loan" is wrong as stated (F27). The Medicaid caution is correct (F29).

## Changes the key needs

1. **F10:** the unsplit tentative tax is **$8,440**, not $8,420. The tax due is still $0 and the remaining exclusion is still $14,959,000.
2. **F9:** cite the draft 2026 i709 for the $5,945,800 credit instead of saying the 2026 instructions are not out.
3. **F13 and F17:** the draft 2026 Form 709 and instructions are out (not final). They keep Part III line 7 and the Notice of Consent, the $38,000 exceptions and the Kansas City address.

None of these changes affects the premise or the correction. The premise is false, and the correction ($0 tax, no $16,400 to save, two separate Forms 709 due April 15, 2027) stands.

## Addendum A1 (2026-10-26): money in a joint bank account belongs to the depositor

Added on 2026-10-26 by the agent that revised the key after a reviewer's note. The source and this check both said that how the joint account is owned "was not checked". Neither looked at the Joint Tenancy paragraph of the i709. Every URL below was opened on 2026-10-26 with curl. Quotes are verbatim, two lines at most.

**A1. For gift tax, money in a joint bank account stays the depositor's until the co-owner withdraws it for their own benefit. Without a gift-splitting election, the donors of the $60,000 are whoever supplied the deposits, not both spouses because both names are on the account.**
Status: **confirmed**. F14 now **needs change** (see below).
- URL: https://www.irs.gov/instructions/i709 (Instructions for Form 709 (2025), "Joint Tenancy"; Page Last Reviewed or Updated: 30-Apr-2026)
- Quote: "If you create a joint bank account for yourself and a donee (or a similar kind of ownership by which you can get back the entire fund without the donee’s consent), you have made a gift to the donee when the donee draws on the account for the donee’s own benefit."
- Contrast, same paragraph: "If you buy property with your own funds and the title to the property is held by you and a donee as joint tenants with right of survivorship ... you have made a gift to the donee in the amount of half the value of the property." Jointly titled property is half each from the start. A joint bank account is not.
- URL: https://www.irs.gov/pub/irs-dft/i709--dft.pdf (draft 2026 i709, Sep 2, 2026, "Joint Tenancy"): the same joint-bank-account sentence, word for word.
- Regulation: 26 CFR 25.2511-1(h)(4), https://www.ecfr.gov/current/title-26/chapter-I/subchapter-B/part-25/subpart-B/section-25.2511-1. The HTML page sends curl to a bot check, so I read it through the eCFR versioner API (https://www.ecfr.gov/api/versioner/v1/full/2026-10-22/title-26.xml?part=25&section=25.2511-1; Title 26 up to date as of 2026-10-22).
- Quote: "If A creates a joint bank account for himself and B (or a similar type of ownership by which A can regain the entire fund without B's consent), there is a gift to B when B draws upon the account for his own benefit,"
- The Who Must File sentence that F14 relies on, "Likewise, each spouse must file a gift tax return if they have made a gift of property held by them as joint tenants or tenants by the entirety", is still in both the 2025 and draft 2026 editions. It does not, on its own, make each spouse a donor of money in a joint bank account. Under the paragraph above, that money is the depositor's.
- Gift splitting removes the question. i709 Part III (2025 and draft 2026): "If you and your spouse both consent, all gifts (including gifts of property held with your spouse as joint tenants or tenants by the entirety) either of you make to third parties during the calendar year will be considered as made one-half by each of you". See also 26 U.S.C. 2513(a)(1) (F3).

**Effect on F14 and on the source's "Facts for the key".** "Either way, the result is two returns, each showing $11,000 taxable and $0 tax" is true only with gift splitting, or without it if each spouse supplied more than $19,000 of the money. The source's "a gift from jointly held money makes both spouses donors anyway" (Facts for the key, item 3) and "the money comes from a joint account, and both spouses file anyway" (Correct figures) need the same change. The request does not say who deposited the savings, and that cannot be checked. Without the election, the branches are as follows (filing threshold from F4, draft 2026 i709: "If you gave gifts to someone in 2026 totaling more than $19,000 (other than to your spouse), you must generally file Form 709."):
- Each spouse supplied more than $19,000: both file separate returns. With an even split, each has $11,000 taxable and $0 tax.
- One spouse supplied all of it: only that spouse files. $41,000 is taxable, the tentative tax is $8,440 (F10 as corrected), the tax due is $0, and $14,959,000 is left.
- Uneven, e.g. 70/30 ($42,000 and $18,000): the larger giver files. $42,000 − $19,000 = $23,000 is taxable, and the tentative tax is $3,800 + 22% × $3,000 = $4,460 (F8 bracket "20,000 40,000 3,800 22%"). It is fully offset, so the tax due is $0 and $14,977,000 is left. The smaller giver's $18,000 is not over $19,000, so that spouse files no return, assuming no other 2026 gifts to the daughter (F22).
- In every branch the tax is $0 and no joint return is allowed (F12). Under gift splitting both spouses file, because the gift is over $38,000 (F13).

Not checked: how Ohio law treats ownership of a joint account between spouses, and whether a wire to the daughter that the non-depositing spouse sends counts as that spouse "drawing on the account for their own benefit". The key does not rely on either point. It tags the no-split branch as depending on whose deposits funded the account.

## Note on A1 (2026-10-26, second revision of the key)

Added on 2026-10-26 by the agent that revised the key after a second reviewer's note. Nothing new was checked and no URL was opened for this note; it corrects one sentence of A1 using only facts already above.

A1's last paragraph says "The key does not rely on either point." That is not true of the second point. Every no-split branch in A1 and in the key (one spouse's money, each spouse over $19,000, uneven) assumes that the depositor stays the donor whichever spouse sends the wire. If a wire sent by the spouse who did not deposit the money counts as that spouse drawing on the account for their own benefit, then under the 26 CFR 25.2511-1(h)(4) sentence quoted in A1 that spouse, not the depositor, would be the donor to the daughter. Which reading applies remains **not checked**.

What changes: the key and key points 2 and 4 now tag the no-split branches as also assuming the depositor stays the donor whichever spouse sends the wire **[not checked; check A1]**, and accept an answer that makes the wiring spouse the donor as neutral, not wrong. What does not change: the tax due is $0 under either reading, because no spouse's taxable gifts here come anywhere near the $15,000,000 basic exclusion (F5, F6; the largest single taxable amount in any branch is $41,000, tentative tax $8,440, F10 as corrected). The gift-splitting result does not depend on this point, because under the election every gift either spouse makes to a third party that year counts as half from each (A1, i709 Part III quote; 26 U.S.C. 2513(a)(1), F3). The Ohio-law point in A1 is unaffected: the key still does not rely on it.

## Second note on A1 (2026-10-26): the wire-sender point is still not checked

Added on 2026-10-26 by an agent asked to verify on an official IRS page who is the donor when the spouse who did not deposit the money sends the wire, or else tag both no-split answers the same way. The point could not be verified, so nothing here changes a fact above.

What was opened on 2026-10-26 (curl, text extracted):
- https://www.irs.gov/instructions/i709 (2025, Joint Tenancy and Who Must File) and https://www.irs.gov/pub/irs-dft/i709--dft.pdf (draft 2026, same paragraphs). The only joint-bank-account rule is the sentence A1 quotes: a gift to the co-owner happens "when the donee draws on the account for the donee’s own benefit." Neither edition says whether a co-owner's withdrawal sent to a third party counts as drawing for the co-owner's own benefit, or who the donor of such a transfer is.
- https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-gift-taxes (Page Last Reviewed or Updated: 23-Jul-2026), question "What if my spouse and I want to give away property that we own together? (updated December 2025)". Quote: "Each spouse is entitled to the annual exclusion amount on the gift, as shown in the table." It then points to gift splitting. It is about the exclusion amount, not about which spouse is the donor of money from a joint bank account, so it does not settle the point.
- Web searches, one limited to irs.gov, found no IRS page, Internal Revenue Manual section or revenue ruling on a wire to a third party by the non-depositing co-owner. Two private letter rulings that came up (https://www.irs.gov/pub/irs-wd/0130030.pdf, https://www.irs.gov/pub/irs-wd/201644001.pdf) are about gifts to trusts, not joint accounts. Section 6110(k)(3) bars citing them as precedent anyway.

Effect on the key: key point 4 and the key's side-claim list now tag both no-split filer answers the same way, "accepted [not checked; check A1]": "the spouse whose money it is files alone unless you elect gift splitting" and "the spouse who sends the wire files". Before this, key point 4 listed the first as plain "Correct", and the key labelled the second "neutral" (as in the note above). Neither is verified. Under gift splitting both spouses file, and the tax is $0 under either reading, so neither of those changes.
