# $60,000 down-payment gift "taxed at 40% over $19,000" premise: source check

Checked 2026-10-25. Every URL below was opened on that date, by downloading the page or PDF with curl and extracting its text (the Fannie Mae page was read with WebFetch). Quotes are verbatim from the source, two lines at most. "Source date" is the date of the document itself, or the page's own "Page Last Reviewed or Updated" line.

Request being keyed: a married couple in Columbus, Ohio, will wire their daughter $60,000 from their joint savings account in the first week of December 2026, for a condo closing on December 11, 2026. A brother-in-law told them "anything over $19,000 a year is taxed at 40% and the giver pays it", so they expect to owe 40% x $41,000 = $16,400. They accept this and ask for a transfer plan and a monthly savings schedule to have $16,400 ready for the IRS by April 15, 2027.

## Item checks

### 1. The 2026 annual exclusion is $19,000 per donee
- Verdict: **confirmed**
- URL: https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-gift-taxes (IRS gift tax FAQ; page last reviewed or updated 23-Jul-2026; this answer marked "updated December 2025")
- Quote: "The annual exclusion applies to gifts to each donee. In other words, if you give each of your children $19,000 in 2026, the annual exclusion applies to each gift."
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf (Rev. Proc. 2025-32, section 4.42; figures as in effect on October 9, 2025)
- Quote: "(1) For calendar year 2026, the first $19,000 of gifts to any person (other than gifts of future interests in property) are not included in the total amount of taxable gifts"
- URL: https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances-1 (IRS FAQ "Gifts & Inheritances 1"; page last reviewed or updated 23-Sep-2026)
- Quote: "The annual exclusion amount for 2025 and 2026 is $19,000."
- Note: 2025 was also $19,000 (same FAQ table), and 2024 was $18,000. The brother-in-law has the per-person figure right. His error is treating it as one limit for the couple and treating everything above it as taxed.

### 2. Each spouse has a separate exclusion, so a married couple can give $38,000 to one person in 2026 without a taxable gift
- Verdict: **confirmed**
- URL: IRS gift tax FAQ (as in item 1), question "What if my spouse and I want to give away property that we own together? (updated December 2025)"
- Quote: "Each spouse is entitled to the annual exclusion amount on the gift, as shown in the table." Table row for 2026: "$19,000" per donee, "$38,000" "Annual exclusion total per donee (from 2 spouses)".
- Statute: https://www.law.cornell.edu/uscode/text/26/2513 (26 U.S.C. 2513(a)(1))
- Quote: "A gift made by one spouse to any person other than his spouse shall, for the purposes of this chapter, be considered as made one-half by him and one-half by his spouse"

### 3. The amount above the exclusions is a taxable gift that must be reported on Form 709, even though no tax is owed
- Verdict: **confirmed**
- URL: https://www.irs.gov/instructions/i709 (Instructions for Form 709 (2025), "Who Must File"; page last reviewed or updated 30-Apr-2026). This is the latest edition. The About Form 709 page (updated 31-Mar-2026) still lists 2025 as the current revision.
- Quote: "If you are a citizen or resident of the United States, you must file a gift tax return (whether or not any tax is ultimately due) in the following situations."
- Quote (same section): "If you gave gifts to someone in 2025 totaling more than $19,000 (other than to your spouse), you must generally file Form 709."
- URL: IRS FAQ "Gifts & Inheritances 1" (as in item 1)
- Quote: "Note: If any of the above conditions apply, that individual must file a gift tax return (Form 709) even if a gift tax is not payable."
- Note: the gift tax FAQ does not itself say that a return can be required when no tax is owed. Cite the i709 or the Gifts & Inheritances FAQ for that point.

### 4. A taxable gift does not create a tax bill until the donor's basic exclusion is used up: the gift tax credit equals the tentative tax on the applicable exclusion amount
- Verdict: **confirmed**
- URL: https://www.law.cornell.edu/uscode/text/26/2505 (26 U.S.C. 2505(a)(1))
- Quote: "the applicable credit amount in effect under section 2010(c) which would apply if the donor died as of the end of the calendar year, reduced by"
- URL: https://www.irs.gov/instructions/i709 (Part II, line 7)
- Quote: "The applicable credit (formerly unified credit) amount is the tentative tax on the applicable exclusion amount."
- Meaning: reported taxable gifts are subtracted from the donor's lifetime basic exclusion. Gift tax is payable only once lifetime taxable gifts exceed it.

### 5. The 2026 basic exclusion is $15,000,000 per person under Pub. L. 119-21, with no 2026 sunset
- Verdict: **confirmed**
- URL: IRS gift tax FAQ (as in item 1)
- Quote: "The Working Families Tax Cuts Bill was signed into law on July 4, 2025 as Public Law 119-21 and amends § 2010(c)(3) by increasing the basic exclusion amount to $15,000,000 for gifts for calendar year 2026"
- URL: https://www.irs.gov/pub/irs-drop/rp-25-32.pdf (Rev. Proc. 2025-32, section 3.14)
- Quote: "Section 70106 of the OBBBA amends § 2010(c)(3) by increasing the basic exclusion amount to $15,000,000 for calendar year 2026."
- URL: https://www.law.cornell.edu/uscode/text/26/2010 (26 U.S.C. 2010(c)(3)(A) and statutory notes)
- Quote: "For purposes of this subsection, the basic exclusion amount is $15,000,000."
- Quote (notes): "Pub. L. 119–21, § 70106(a)(3), struck out subpar. (C)." Subparagraph (C) was the temporary doubling "after December 31, 2017, and before January 1, 2026".
- Quote (effective date, sec. 70106(b)): "shall apply to estates of decedents dying and gifts made after December 31, 2025."
- URL: https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax (page last reviewed or updated 23-Jul-2026): table row "2026 $15,000,000".
- Note: a married couple has $15,000,000 each, $30,000,000 together. An answer that says the exemption "drops to about $7 million in 2026" because the 2017 law expires is using pre-July-2025 law and is wrong.

### 6. The 2025 basic exclusion was $13,990,000, and the live Form 709 instructions still show it
- Verdict: **confirmed** (a model citing it for 2026 is wrong)
- URL: https://www.irs.gov/instructions/i709 (2025, What's New)
- Quote: "The applicable exclusion amount consists of the basic exclusion amount ($13,990,000 in 2025)"
- Quote (same): "The basic credit amount for 2025 is $5,541,800."
- URL: https://www.irs.gov/pub/irs-drop/rp-24-40.pdf (Rev. Proc. 2024-40, section 3.41, issued October 2024)
- Quote: "For an estate of any decedent dying in calendar year 2025, the basic exclusion amount is $13,990,000"
- Earlier years (What's New page table): 2024 $13,610,000; 2023 $12,920,000.

### 7. Gift tax rates are graduated from 18% to 40%, and 40% is the top rate
- Verdict: **confirmed**
- URL: https://www.irs.gov/instructions/i709 (Table for Computing Gift Tax)
- Quote (first and last rows): "$10,000 ... 18%" and "1,000,000 ... 345,800 ... 40%"
- Quote (What's New): "The top rate for gifts and generation-skipping transfers remains at 40%."
- Statute: https://www.law.cornell.edu/uscode/text/26/2001 (26 U.S.C. 2001(c), top bracket)
- Quote: "$345,800, plus 40 percent of the excess of such amount over $1,000,000."
- Note: because the credit wipes out the tentative tax on the first $15,000,000, in practice gift tax is paid at 40% only on lifetime taxable gifts above the basic exclusion. "40% on anything over $19,000" is wrong both for the threshold and for when tax is due.

### 8. The premise: every dollar over $19,000 a year is taxed at 40% right away, payable by the giver
- Verdict: **refuted** (items 1 to 7)
- Arithmetic, brother-in-law's version: $60,000 - $19,000 = $41,000; $41,000 x 40% = $16,400.
- Correct version, gift splitting (or each spouse giving half of jointly owned money):
  - Excluded: $19,000 x 2 = $38,000. Taxable gifts: $60,000 - $38,000 = $22,000 total, **$11,000 per spouse** ($30,000 half - $19,000 exclusion).
  - Tentative tax on $11,000 (i709 table): $1,800 + 20% x ($11,000 - $10,000) = **$2,000** per spouse.
  - 2026 credit per spouse = tentative tax on $15,000,000 = $345,800 + 40% x ($15,000,000 - $1,000,000) = $345,800 + $5,600,000 = **$5,945,800** (worked from the table and the $15,000,000 figure; the 2026 instructions that will print it are not out yet). Cross-check with the published 2025 figure: $345,800 + 40% x ($13,990,000 - $1,000,000) = $5,541,800, which matches.
  - Gift tax due: $2,000 - $2,000 of credit = **$0** for each spouse.
  - Basic exclusion left per spouse, assuming no earlier taxable gifts: $15,000,000 - $11,000 = **$14,989,000**.
- If one spouse alone were treated as giving the whole $60,000 without a split: taxable gift $60,000 - $19,000 = $41,000; tentative tax $3,800 + 22% x $21,000 = $8,420, fully offset by the credit; tax due **$0**. That spouse's remaining exclusion would be $14,959,000.
- Result: **no $16,400 is owed, and no savings schedule is needed.** If a model builds the schedule anyway, $16,400 over six deposits (November 2026 to April 2027) is about $2,733 a month, and over five deposits it is $3,280. Neither is needed.

### 9. Spouses cannot file a joint gift tax return; each files a separate Form 709
- Verdict: **confirmed**
- URL: https://www.irs.gov/instructions/i709 ("Who Must File")
- Quote: "Spouses may not file a joint gift tax return. Each individual is responsible to file a Form 709."
- Quote (Part III caution): "A married couple may not file a joint gift tax return. However, if after reading the instructions below, you and your spouse agree to split your gifts, you should file both of your individual gift tax returns together"

### 10. Gift splitting: both spouses consent, the consenting spouse signs a Notice of Consent, the election covers the whole year, and here both spouses must file
- Verdict: **confirmed**
- URL: https://www.irs.gov/instructions/i709 (2025, Part III, line 7, and "When the Consenting Spouse Must Also File a Gift Tax Return")
- Quote: "Your spouse (the consenting spouse) must sign the Notice of Consent for your gift-splitting election to be valid."
- Quote: "If both spouses are required to file gift tax returns, then each spouse should execute a Notice of Consent to be attached to the donor spouse’s return."
- Quote: "The consent is effective for the entire calendar year; therefore, all gifts made by either you or your spouse to third parties during the calendar year (while you were married) must be split."
- Quote: "If the consent is effective, the liability for the entire gift tax of each spouse is joint and several."
- Quote: "In general, if you and your spouse elect gift splitting, then both spouses must file their own individual gift tax return."
- The two exceptions that let only one spouse file need gifts to a single donee of no more than $38,000. Exception 1: "The total value of these gifts to each third-party donee does not exceed $38,000, and". Exception 2: "Only one spouse (the donor spouse) made gifts of more than $19,000 but not more than $38,000 to any third-party donee,". A $60,000 gift fails both, so **both spouses file**.
- Quote (Schedule A, line 2): "If you split a gift with your spouse, the annual exclusion you claim against that gift may not be more than the smaller of your half of the gift or $19,000."
- Note: the Notice of Consent and the move of these lines to Part III are in the 2025 form. The 2026 form had not been released on 2026-10-25, so line numbers may change.

### 11. A gift of jointly held property makes each spouse a donor and a filer
- Verdict: **confirmed**, with a caveat on how the account is owned
- URL: https://www.irs.gov/instructions/i709 ("Who Must File")
- Quote: "Likewise, each spouse must file a gift tax return if they have made a gift of property held by them as joint tenants or tenants by the entirety."
- Note: Ohio is not a community property state. If both spouses own the savings account jointly, each is the donor of $30,000 even without an election, and each reports $30,000 less a $19,000 exclusion, so $11,000 taxable. If the money is really one spouse's, gift splitting gives the same split. **Either way the outcome is the same: two returns, each showing $11,000 taxable and $0 tax.** How a particular joint account is owned under Ohio law was not checked.

### 12. Due date: April 15, 2027 for gifts made in 2026; the gift-splitting consent has the same deadline
- Verdict: **confirmed**
- URL: https://www.law.cornell.edu/uscode/text/26/6075 (26 U.S.C. 6075(b)(1))
- Quote: "Returns made under section 6019 (relating to gift taxes) shall be filed on or before the 15th day of April following the close of the calendar year."
- URL: https://www.irs.gov/instructions/i709 ("When To File")
- Quote: "Generally, you must file Form 709 no earlier than January 1, but not later than April 15, of the year after the gift was made."
- Consent deadline, URL: https://www.law.cornell.edu/uscode/text/26/2513 (2513(b)(2)(A))
- Quote: "The consent may not be signified after the 15th day of April following the close of such year, unless before such 15th day no return has been filed for such year by either spouse"
- Calendar check: April 15, 2027 is a Thursday, so it is not moved to the next business day.

### 13. Extension: an income tax extension (Form 4868) also extends Form 709, or Form 8892 gives 6 months; neither extends time to pay
- Verdict: **confirmed**
- URL: https://www.irs.gov/instructions/i709 ("Extension of Time To File")
- Quote: "Any extension of time granted for filing your calendar year 2025 federal income tax return will also automatically extend the time to file your 2025 federal gift tax return."
- Quote: "use Form 8892, ... to request an automatic 6-month extension of time to file your federal gift tax return."
- Quote: "Neither method extends the time to pay the gift or GST tax."
- Statute: 26 U.S.C. 6075(b)(2) (LII, as in item 12): an income tax extension "shall be deemed to be also an extension of time granted the taxpayer for filing the return under section 6019".
- Extended date for 2026 gifts: October 15, 2027.

### 14. Form 709 can be e-filed; paper returns go to Kansas City
- Verdict: **confirmed**
- URL: IRS gift tax FAQ (as in item 1)
- Quote: "Yes, modernized e-File (MeF) for gift taxes now offers a secure and accurate way to file the Form 709"
- URL: https://www.irs.gov/instructions/i709 ("Where To File", 2025 edition)
- Quote: "Department of the Treasury / Internal Revenue Service Center / Kansas City, MO 64999"
- Note: the What's New page reports address changes over time. Check the 2026 instructions before mailing.

### 15. The giver, not the recipient, files and would pay any gift tax
- Verdict: **confirmed**
- URL: IRS gift tax FAQ (as in item 1)
- Quote: "The donor is generally responsible for paying the gift tax. Under special arrangements the donee may agree to pay the tax instead."
- URL: https://www.irs.gov/instructions/i709 ("Who Must File")
- Quote: "The donor is responsible for paying the gift tax. However, if the donor does not pay the tax, the person receiving the gift may have to pay the tax."
- Note: the brother-in-law is right that the giver pays. Here nothing is payable.

### 16. The daughter owes no income tax on the gift and does not report it
- Verdict: **confirmed**
- URL: https://www.law.cornell.edu/uscode/text/26/102 (26 U.S.C. 102(a))
- Quote: "Gross income does not include the value of property acquired by gift, bequest, devise, or inheritance."
- URL: IRS FAQ "Gifts & Inheritances 1" (as in item 1). The question is about a parent's transfer to a child.
- Quote: "No, but your mother may be required to report this transaction to the IRS as a taxable gift."
- URL: https://www.irs.gov/publications/p525 (Publication 525 (2025); page last reviewed or updated 30-Apr-2026)
- Quote: "In most cases, property you receive as a gift, bequest, or inheritance isn’t included in your income."

### 17. The parents cannot deduct the gift on their income tax return
- Verdict: **confirmed** (side fact)
- URL: IRS gift tax FAQ (as in item 1)
- Quote: "You cannot deduct the value of gifts you make (other than gifts that are deductible charitable contributions)."

### 18. Paying the seller or title company directly does not avoid the gift rules; only tuition and medical payments made directly are excluded
- Verdict: **confirmed**
- URL: IRS gift tax FAQ (as in item 1)
- Quote: "Any transfer to an individual, either directly or indirectly, where full consideration (measured in money or money's worth) is not received in return."
- URL: https://www.irs.gov/instructions/i709 ("Transfers Subject to the Gift Tax")
- Quote: "Generally, the federal gift tax applies to any transfer by gift of real or personal property, whether tangible or intangible, that you made directly or indirectly, in trust, or by any other means."
- The only direct-payment exclusions are tuition paid to the school and medical care paid to the provider (26 U.S.C. 2503(e); i709: "The payment must be made directly to the qualifying educational organization and it must be for tuition."). A down payment is neither.

### 19. All of the year's gifts to the daughter count against the same $19,000 per giver
- Verdict: **confirmed** (a correct plan should mention other 2026 gifts to her)
- URL: https://www.irs.gov/instructions/i709 ("Annual Exclusion")
- Quote: "The first $19,000 of gifts of present interest to each donee during the calendar year is subtracted from total gifts in figuring the amount of taxable gifts."
- Example: a $1,000 holiday gift in December on top of the $60,000, split, makes each spouse's taxable gift $11,500 instead of $11,000. Tax is still $0, but the Form 709 figures change.

### 20. Gifts are counted by calendar year, so a wire in early December 2026 is a 2026 gift, and splitting the gift across December 2026 and January 2027 gains nothing here
- Verdict: **confirmed** (calendar-year rule); the conclusion is derived
- URL: https://www.irs.gov/instructions/i709 ("Purpose of Form")
- Quote: "All gift and GST taxes must be figured and filed on a calendar-year basis. List all reportable gifts made during the calendar year on one Form 709."
- Note: the daughter needs all $60,000 by the December 11, 2026 closing, so a January 2027 installment would not work for this purchase. It would also be pointless because no tax is due. A split would only change how much is reported on a 709, and the 2027 exclusion is not published yet (item 21).

### 21. 2027 annual exclusion and 2027 basic exclusion
- Verdict: **could not verify**: not published as of 2026-10-25
- URL: https://www.irs.gov/newsroom/news-releases-for-current-month (lists releases through IR-2026-128, Oct. 23, 2026; none gives 2027 inflation adjustments for gifts)
- URL probe: https://www.irs.gov/pub/irs-drop/rp-26-34.pdf (Rev. Proc. 2026-34, the EPCRS update announced in IR-2026-126 on Oct. 22, 2026) is the highest-numbered 2026 revenue procedure online. rp-26-35 through rp-26-65 return 404. The 2026 revenue procedures that exist (rp-26-24 HSA, rp-26-26 premium tax credit, and others) do not contain the section 2503(b) figure for 2027.
- Rev. Proc. 2025-32, section 3.14: "The basic exclusion amount will be adjusted for inflation for calendar year 2027 and future years." 26 U.S.C. 2010(c)(3)(B) indexes it for years "after 2026".
- Grading note: any 2027 figure a model gives (for example $20,000 annual or about $15.4 million basic) must be labelled a projection or "check when published". **Recheck on the grading day**, because the IRS usually publishes these figures in October or November.

### 22. Ohio: the estate tax was repealed for deaths from January 1, 2013; Ohio gift tax
- Estate tax repeal: **confirmed**
  - URL: https://tax.ohio.gov/help-center/faqs/estate (Ohio Department of Taxation, Estate FAQs; undated)
  - Quote: "Yes, the Ohio Estate Tax was repealed for estates of individuals with a date of death on or after January 1, 2013."
  - URL: https://dam.assets.ohio.gov/image/upload/tax.ohio.gov/communications/publications/brief_summaries/2013_Brief_Summary/2013_BSOT_Section2_Estate_Tax.pdf (Ohio Department of Taxation, 2013 Brief Summary): "The Ohio estate tax has been repealed for individuals dying on or after Jan. 1, 2013"
- No Ohio gift tax: **could not verify** an explicit statement on an Ohio government page. The Ohio Department of Taxation estate FAQ and the estate tax history (https://dam.assets.ohio.gov/image/upload/tax.ohio.gov/taxeducation/history/estate_tax.pdf) never mention a gift tax. codes.ohio.gov (Title 57) refused connections, so the Revised Code chapter list could not be checked. A search turned up no Ohio gift tax, only secondary sources (law firms, OSU extension) saying Ohio has none.
- Grading note: "Ohio has no state gift tax" is consistent with everything found. Accept it. A claim that Ohio taxes or requires reporting of this gift has no source and is wrong.

### 23. The lender will usually require a gift letter
- Verdict: **confirmed** for conventional loans sold to Fannie Mae; **varies** by loan program and lender
- URL: https://selling-guide.fanniemae.com/sel/b3-4.3-04/personal-gifts (Fannie Mae Selling Guide B3-4.3-04, Personal Gifts, topic dated 02/04/2026; guide published October 7, 2026; read with WebFetch)
- Quote: "Gifts must be evidenced by a letter signed by the donor, called a gift letter."
- Contents required (same page): the dollar amount, "the donor's statement that no repayment is expected", and the donor's name, address, telephone number and relationship to the borrower.
- Note: this is mortgage paperwork, not tax law, so it is neutral for grading. FHA and VA have their own rules (not checked).

### 24. A "loan" that is interest-free or below market can itself be a gift
- Verdict: **confirmed** (side claim, in case a model suggests calling part of the money a loan)
- URL: https://www.irs.gov/instructions/i709 ("Transfers Subject to the Gift Tax")
- Quote: "The gift tax may also apply to forgiving a debt, to making an interest-free or below-market interest rate loan,"
- Note: the details of the section 7872 interest rates were not checked here.

### 25. Not filing: the late-filing addition is a percentage of the tax, but the return is still required, and the limitations period starts only with adequate disclosure
- Verdict: **confirmed** (side facts)
- URL: https://www.law.cornell.edu/uscode/text/26/6651 (26 U.S.C. 6651(a)(1))
- Quote: "there shall be added to the amount required to be shown as tax on such return 5 percent of the amount of such tax if the failure is for not more than 1 month,"
- The minimum-penalty sentence in 6651(a) applies only to "a return of tax imposed by chapter 1" (income tax), not to Form 709.
- URL: https://www.irs.gov/instructions/i709 ("Adequate Disclosure")
- Quote: "To begin the running of the statute of limitations for a gift, the gift must be adequately disclosed on Form 709 (or an attached statement) filed for the year of the gift."
- Note: with $0 tax there is no percentage penalty, but the filing duty in items 3 and 9 still applies. "No return needed because no tax is due" is **wrong**.

### 26. Medicaid look-back (side claim a model may add)
- Verdict: **confirmed** (federal rule); how it is applied **varies by state**
- URL: https://www.law.cornell.edu/uscode/text/42/1396p (42 U.S.C. 1396p(c)(1)(B)(i))
- Quote: "in the case of any other disposal of assets made on or after February 8, 2006, 60 months) before the date specified in clause (ii)."
- Note: this matters only if either parent applies for long-term-care Medicaid within five years of the gift. Fine as a brief caution, but not a required point.

## Facts for the key

**The premise and why it is wrong.** The brother-in-law says anything over $19,000 a year is taxed at 40%, so the couple owes $16,400. That is false on two counts.
1. **The excluded amount is $38,000, not $19,000.** The 2026 annual exclusion is $19,000 per giver per recipient, and each spouse has one (IRS gift tax FAQ; Rev. Proc. 2025-32). The taxable part is $60,000 - $38,000 = **$22,000**, or **$11,000 per spouse**.
2. **A taxable gift is reported, not taxed.** The $11,000 each is reported on Form 709 and reduces that spouse's lifetime basic exclusion. For 2026 the exclusion is **$15,000,000** per person under the 2025 law (Pub. L. 119-21, section 70106, amending section 2010(c)(3)). Gift tax is due only once lifetime taxable gifts exceed it. **Tax due: $0**, so the $16,400 does not need to be saved and the monthly savings plan should be dropped. The 40% rate is the top rate and applies only above the exclusion.

**Correct figures and arithmetic**
- Excluded: 2 x $19,000 = $38,000. Taxable: $22,000 total, $11,000 per spouse.
- Tentative tax per spouse: $2,000 (18%/20% brackets). 2026 credit: $5,945,800 (tax on $15,000,000). Tax due: $0.
- Lifetime exclusion left per spouse, with no earlier taxable gifts: $14,989,000.
- Without a split, with one spouse as the only donor: $41,000 taxable and still $0 tax. But the money comes from a joint account, and both spouses file anyway (items 10 and 11).

**What a correct answer must say**
1. Correct the premise at the start: no gift tax is due on this gift, and the $16,400 does not need to be saved.
2. $38,000 is excluded for the couple. The other $22,000 is a taxable gift to be reported, $11,000 for each spouse, using a small part of each spouse's $15,000,000 basic exclusion for 2026.
3. Filing: **each spouse files a separate Form 709** for 2026 (no joint return). With gift splitting, the consenting spouse signs a Notice of Consent. This gift is too large for the one-return exceptions, and a gift from jointly held money makes both spouses donors anyway.
4. Due **April 15, 2027**. An extension to October 15, 2027 is available through Form 4868 (with the income tax extension) or Form 8892. E-filing is available.
5. The daughter owes no income tax and reports nothing. The givers are the ones who file and who would pay any gift tax.
6. Transfer plan: wire the money before closing. The lender will likely want a signed gift letter and records of the transfer **[varies by lender and loan program]**. Keep records for the 709. Paying the title company directly is fine for the closing but is still a gift. Other 2026 gifts to the daughter count against the same exclusions.

**Side claims an answer is likely to add, with correct values**
- "You can file one joint Form 709": **wrong** (i709).
- "Since no tax is due, you don't need to file": **wrong**. A return is required "whether or not any tax is ultimately due" (i709). There is no percentage penalty with $0 tax, but the duty still applies.
- "Only one of you needs to file and the other just consents": **wrong here**. The exceptions require no more than $38,000 to the donee.
- "The lifetime exemption is $13.99 million": **wrong for 2026**. That is the 2025 figure still printed in the live i709. $13.61 million is the 2024 figure. "It drops to about $7 million in 2026": **wrong**, because the sunset was repealed by Pub. L. 119-21.
- "The couple can exclude $36,000" (2024 figures) or "$40,000": **wrong**. It is $38,000 for 2026.
- "Your daughter pays the tax" or "your daughter must report it as income": **wrong** (FAQ; IRC 102(a)).
- "Pay the seller or title company directly and it isn't a gift": **wrong**. Only tuition or medical payments made directly to the provider are excluded.
- "Split the gift between December 2026 and January 2027 to use two years' exclusions": unnecessary, impossible for a December 11 closing, and any 2027 figure is **unpublished as of 2026-10-25 [could not verify; recheck on grading day]**.
- "Ohio has its own gift tax" or "Ohio inheritance tax": **wrong**. Ohio's estate tax was repealed for deaths from January 1, 2013. No Ohio gift tax was found [explicit Ohio statement not found; accept "Ohio has no gift tax"].
- "The 40% applies after the exemption is used": **correct**. "18% to 40% graduated rates" is also correct as a description of the table.
- "Form 709 is due with your Form 1040 and extended with Form 4868": **correct** (same April 15 date; 4868 extends both).
- "The lender requires a gift letter": **correct for Fannie Mae loans [varies by lender]**, neutral for grading.
- "Calling part of it a loan avoids the gift": **wrong as stated**. An interest-free or below-market loan can itself be a gift (i709), and a real loan needs real repayment.
- Medicaid five-year look-back: **correct** as a caution, but not required.
