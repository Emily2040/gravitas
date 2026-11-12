# Adversarial check: en-debit-card-theft-liability.md

Checked 2026-10-25 by an agent that did not write the source file. On disk I read only `prompts/en-debit-card-theft-liability.txt` and `sources/en-debit-card-theft-liability.md`. I opened every URL below myself on that date. Regulation text came from the eCFR renderer API (title 12 "up_to_date_as_of 2026-10-22"), 15 U.S.C. 1693g from law.cornell.edu and govinfo, and the other pages through WebFetch or a plain download. Quotes are verbatim, two lines at most. Each fact gets a status: **stands** or **refuted/needs change**. Item numbers follow the source file.

Newer-rule search: I found no rule, amendment, figure or announcement up to 2026-10-25 that changes any fact in the source or makes the premise true. Evidence:
- **eCFR version history for Part 1005.** The latest amendment is 2025-10-01, and it touched only § 1005.10 and the matching Supplement I comments (the 2024-12-30 hybrid prepaid-credit/overdraft change and its reversal). § 1005.6 has one version, 2017-01-01, the start of eCFR's history. §§ 1005.2 and 1005.11 were last changed 2019-04-01, § 1005.3 on 2017-01-01, and § 1026.12 (Reg Z) on 2019-04-01.
- **Federal Register API.** Only two documents published 2025-01-01 to 2026-10-25 cite 12 CFR 1005: the 2025-01-15 proposed interpretive rule on emerging payment mechanisms, and its withdrawal on 2025-05-15. Neither touches liability limits. Term searches for "Electronic Fund Transfer" and "Regulation E" since 2025-06-01 found no CFPB rule on consumer liability. The newest CFPB item was a 2025-08-08 larger-participant proposal for international money transfers.
- **CFPB guidance withdrawal of 2025-05-12** (90 FR 20084, FR doc 2025-08286). Its only Regulation E item is the 2012 remittance-rule bulletin. The EFT FAQs cited in items 1 and 18 are not on the list. Their page was last modified January 16, 2025, and it shows no withdrawal notice.
- **15 U.S.C. 1693g.** The govinfo 2024 edition and Cornell both give only the 1978 source credit (Pub. L. 95-630). OLRC says the Code is "current through Public Law 119-124 (October 15, 2026)", but its section page returned 404 because the site is in a temporary format.
- **Congress.** Searches for 2026 EFTA bills turned up the Credit Card Competition Act of 2026 (S.3623 / H.R.7035). It deals with card routing and network competition, not consumer liability for unauthorized use.
- **CFPB consumer pages.** The Ask CFPB page was "Last reviewed: AUG 28, 2026" and still states the $500 tier.
- **Third-party tools.** A compliance-calculator vendor logged a 4/1/2026 "update". That is a change to its own tool, not to the rule.

Tooling note:
- The FTC page returned 404 to a plain download, so I read it through WebFetch.
- Mastercard's zero-liability terms page returned 403, so it is still unchecked.
- ilga.gov refused connections and timed out on https and http throughout this pass.

## Setup facts

**S1. Dates.** 2026-10-19 was a Monday, 10-20 a Tuesday, 10-21 a Wednesday, 10-22 a Thursday, 10-23 a Friday. There was no federal holiday from Oct 13 to Nov 10. Columbus Day was Mon Oct 12 and Veterans Day is Wed Nov 11.
Status: **stands**
- Recomputed with Python `datetime`. The weekdays match.
- URL: https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ (2026 schedule)
- Quote: "Monday, October 12" (Columbus Day) / "Wednesday, November 11" (Veterans Day). No holiday falls between them.

## Item checks

**1. Debit card transactions are EFTs under Regulation E, and the card is an "access device".**
Status: **stands**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.3 (12 CFR 1005.3(b)(1)(v))
- Quote: "( v ) Transfers resulting from debit card transactions, whether or not initiated through an electronic terminal."
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.2 (12 CFR 1005.2(a)(1))
- Quote: "“Access device” means a card, code, or other means of access to a consumer's account, or any combination thereof, that may be used by the consumer to initiate electronic fund transfers."
- URL: https://www.consumerfinance.gov/compliance/compliance-resources/deposit-accounts-resources/electronic-fund-transfers/electronic-fund-transfers-faqs/ (Coverage: Transactions Q3, "Updated December 13, 2021")
- Quote: "The term EFT includes debit card transactions"

**2. Debit cards have statutory liability limits, so "debit cards don't have the protection" is wrong. Debit protection is weaker than credit card protection.**
Status: **stands**
- URL: https://www.law.cornell.edu/uscode/text/15/1693g (15 U.S.C. 1693g(a)). The text matches the govinfo 2024 edition.
- Quote: "In no event, however, shall a consumer’ s liability for an unauthorized transfer exceed the lesser of— (1) $50; or (2) the amount of money or value of property or services obtained"
- Same subsection: "but the consumer’ s liability under this subsection in any such case may not exceed a total of $500"
- URL: https://consumer.ftc.gov/articles/lost-or-stolen-credit-atm-and-debit-cards (FTC, "January 2022")
- Quote: "If your credit, ATM, or debit card is lost or stolen, federal law limits your liability for charges made without your permission, but your protection depends on the type of card — and when you report the loss."

**3. Tier one: report within two business days of learning of the loss, and liability is at most $50. It does not apply here.**
Status: **stands**
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/6/. The page says "This version is the current regulation". The versions page (https://www.consumerfinance.gov/rules-policy/regulations/1005/versions/) lists "April 19, 2023" as the current regulation and shows no upcoming version. The eCFR text is identical.
- Quote (eCFR 1005.6(b)(1)): "If the consumer notifies the financial institution within two business days after learning of the loss or theft of the access device, the consumer's liability shall not exceed the lesser of $50"

**4. Tier two: after a late report, liability is capped at the lesser of $500 or a two-part sum. The cap applies per series of related transfers, not per charge.**
Status: **stands**. The rep's "responsible for all $1,215" is refuted.
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.6 (1005.6(b)(2)). The same text is on the CFPB page above.
- Quote: "the consumer's liability shall not exceed the lesser of $500 or the sum of:"
- Quote (i): "$50 or the amount of unauthorized transfers that occur within the two business days, whichever is less; and"
- Quote (ii): "The amount of unauthorized transfers that occur after the close of two business days and before notice to the institution, provided the institution establishes that these transfers would not have occurred had the consumer notified the institution within that two-day period."
- Quote (1005.6(b) lead-in): "A consumer's liability for an unauthorized electronic fund transfer or a series of related unauthorized transfers shall be determined as follows:"

**5. The day of learning is not counted, so the two business days were Tue Oct 20 and Wed Oct 21, ending 11:59 p.m. Wed Oct 21. The Fri Oct 23 report was late.**
Status: **stands**
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/interp-6/ (Comment 6(b)(1)-3). The same text is in the eCFR Supplement I.
- Quote: "The two business day period does not include the day the consumer learns of the loss or theft or any day that is not a business day."
- Quote: "The rule is calculated based on two 24-hour periods, without regard to the financial institution's business hours or the time of day that the consumer learns of the loss or theft."
- Comment 6(b)(2)-1 uses the same Monday-learn pattern: "(which would have been by midnight Wednesday)".
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.2 (1005.2(d))
- Quote: "“Business day” means any day on which the offices of the consumer's financial institution are open to the public for carrying on substantially all business functions."
- A Saturday-open bank changes nothing, because Sat Oct 24 comes after the report.

**6. The Oct 19 charges ($45 + $380 = $425) count for at most $50.**
Status: **stands**, with one precision note
- URL: https://www.consumercomplianceoutlook.org/articles/2025/third-issue-2025/consumer-liability-for-unauthorized-transactions-under-the-electronic-fund-transfer-act (Kenneth J. Benton, FRB Philadelphia, "October 28, 2025")
- Quote: "the consumer’s first tier liability (i.e., the lesser of $50 or the amount of unauthorized EFTs that occurred before the end of the second business day after the consumer learns of the loss or theft)"
- Quote (First Tier Liability: Example 2. Stolen Monday, $35 EFT Tuesday, learned Wednesday): "The financial institution may hold the consumer liable for the $35 transfer because §1005.6(b)(1) specifies"
- Precision note: Example 2 is a **tier-one** (timely notice) example. It shows that transfers made before the consumer learned of the loss count toward the $50 under (b)(1). For tier two, the support is the Fed's description quoted first. The conclusion stands either way: (b)(2)(ii) reaches only transfers "after the close of two business days", so the Oct 19 charges can count for at most $50. The source's interpretive note is accurate.

**7. The $790 charge on Thu Oct 22 counts only if the bank establishes that timely notice would have prevented it. The bank carries the burden.**
Status: **stands**
- URL: https://www.law.cornell.edu/uscode/text/15/1693g (1693g(b), "Burden of proof")
- Quote: "the burden of proof is upon the financial institution to establish that the conditions of liability set forth in subsection (a) have been met"
- The regulatory text "provided the institution establishes" is quoted under item 4.
- The source says "$500 is the realistic maximum" for a bank that freezes on notice. That is a judgment, and the Fed example's assumption supports it: "the bank’s systems are set up to immediately freeze an account after the notice of an unauthorized EFT."

**8. The official worked example matches this case: learned Monday, reported Friday, $100 Tuesday, $600 Thursday, $500 liability. With the amounts reversed, the liability is $150.**
Status: **stands**
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/interp-6/ (Comment 6(b)(2)-1)
- Quote: "the consumer's total liability is $500 ($50 of the $100 transfer plus $450 of the $600 transfer, in this example)."
- Quote: "But if $600 was taken on Tuesday and $100 on Thursday, the consumer's maximum liability would be $150 ($50 of the $600 plus $100)."
- Fed article (item 6 URL): "If the consumer had provided notice on Wednesday, the $600 transfer would not have occurred."

**9. Arithmetic: total $1,215. Part one min($50, $425) = $50. Cap min($500, $840) = $500, or $50 if the bank cannot make the part-two showing. At least $715 must come back, up to $1,165. The delay cost at most $450.**
Status: **stands**, with one optional precision note
- Recomputed: 45 + 380 + 790 = 1,215. min(500, 50 + 790) = 500. 1,215 − 500 = 715. 1,215 − 50 = 1,165. 500 − 50 = 450.
- Precision note: Regulation E sets ceilings ("shall not exceed"). "$50 to $500" means a $500 ceiling if the bank makes the part-two showing and a $50 ceiling if it does not. It is not a guaranteed floor of $50. The answer should say "at most".

**10. Negligence cannot increase liability. Liability depends only on how promptly the loss was reported, and no agreement can impose more.**
Status: **stands**
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/interp-6/ (Comments 6(b)-2 and 6(b)-3)
- Quote: "Negligence by the consumer cannot be used as the basis for imposing greater liability than is permissible under Regulation E."
- Quote: "The extent of the consumer's liability is determined solely by the consumer's promptness in reporting the loss or theft of an access device."
- Quote: "no agreement between the consumer and an institution may impose greater liability on the consumer for an unauthorized transfer than the limits provided in Regulation E."

**11. Tier three (unlimited) covers only transfers more than 60 days after the statement. It is not triggered here, and the 60-day rule does not restore the $50 tier.**
Status: **stands**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.6 (1005.6(b)(3))
- Quote: "A consumer must report an unauthorized electronic fund transfer that appears on a periodic statement within 60 days of the financial institution's transmittal of the statement to avoid liability for subsequent transfers."
- eCFR Supplement I, Comment 6(b)(3)-1: "The consumer's liability for unauthorized transfers before the statement is sent, and up to 60 days following, is determined based on the first two tiers of liability"

**12. Extenuating circumstances extend the deadline. The official examples are extended travel and hospitalization. "Buried at work" is unlikely to qualify.**
Status: **stands**, as hedged. Whether a busy week qualifies cannot be decided, and the source correctly does not promise it.
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.6 (1005.6(b)(4))
- Quote: "If the consumer's delay in notifying the financial institution was due to extenuating circumstances, the institution shall extend the times specified above to a reasonable period."
- Comment 6(b)(4)-1: "Examples of circumstances that require extension of the notification periods under this section include the consumer's extended travel or hospitalization."

**13. State law or the account agreement can lower liability. Network zero liability is voluntary, not federal law, and Visa lets issuers weigh a delay in reporting.**
Status: **stands**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.6 (1005.6(b)(6))
- Quote: "If state law or an agreement between the consumer and the financial institution imposes less liability than is provided by this section, the consumer's liability shall not exceed the amount imposed under the state law or agreement."
- URL: Fed article (item 6 URL), endnote 16. I confirmed the number: the endnote begins "Comment 6(b)(1)-1."
- Quote: "The payment card networks, such as MasterCard, Visa, and Discover, typically provide in their agreement with participating merchants that the consumer generally has zero liability for unauthorized debit card transactions, subject to specified exclusions."
- URL: https://www.visa.com/en-us/personal/security/zero-liability-policy (undated)
- Quote: "replacement funds are provided on a provisional basis and may be withheld, delayed, limited, or rescinded by your issuer based on gross negligence or fraud, a delay in reporting unauthorized use"
- Same page: "The policy does not apply to certain commercial card and anonymous prepaid card transactions or transactions not processed by Visa." / "within five business days of notification."
- Mastercard is still unchecked: its terms page returned 403.

**14. Illinois law: no lower Illinois cap was verified.**
Status: **stands**, as an honest "could not verify". ilga.gov refused connections and timed out again on 2026-10-25. A search-result summary for 205 ILCS 616/55 again said the Illinois act adopts the federal EFTA and its regulations, and that complying with federal law counts as complying with the section. That is a paraphrase from search results, not text I could open, so I do not quote it. Keep the tag **[varies by state; not verified]**.

**15. Reporting a lost card and alleging unauthorized use starts the bank's error-resolution duties.**
Status: **stands**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/appendix-Supplement%20I%20to%20Part%201005 (Comment 11(a)-3)
- Quote: "A financial institution is required to comply with the error resolution procedures when a consumer reports the loss or theft of an access device if the consumer also alleges possible unauthorized use as a consequence of the loss or theft."
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.11 (1005.11(a)(1)(i), (b)(1)(i))
- Quote: "( i ) An unauthorized electronic fund transfer;" / "no later than 60 days after the institution sends the periodic statement"

**16. Timelines: 10 business days, or provisional credit (minus at most $50) and 45 days, or 90 days for point-of-sale debit purchases but not ATMs. From Oct 23 the dates are Fri Nov 6, Mon Dec 7, 2026 and Thu Jan 21, 2027.**
Status: **stands**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.11 (source note lists 76 FR 81023, 81 FR 84326, 83 FR 6417)
- Quote (c)(1): "shall determine whether an error occurred within 10 business days of receiving a notice of error. The institution shall report the results to the consumer within three business days after completing its investigation."
- Quote (c)(2)(i): "Provisionally credits the consumer's account in the amount of the alleged error (including interest where applicable) within 10 business days of receiving the error notice." / "the institution may withhold a maximum of $50 from the amount credited."
- Quote (c)(3)(ii)(B): "Resulted from a point-of-sale debit card transaction; or"
- Comment 11(c)(3)-1: "The deadlines do not apply to transactions at an ATM, however, even though the ATM may be in a merchant location."
- Recomputed: Oct 23 + 10 Mon-Fri business days = Fri Nov 6, 2026. Counting Saturdays, it is Wed Nov 4. Oct 23 + 45 days = Mon Dec 7, 2026. Oct 23 + 90 days = Thu Jan 21, 2027. 1,215 − 50 = 1,165.
- URL: https://www.consumerfinance.gov/ask-cfpb/how-do-i-get-my-money-back-after-i-discover-an-unauthorized-transaction-or-money-missing-from-my-bank-account-en-1017/
- Quote: "it must generally issue a temporary credit to your account for the amount of the disputed transaction, minus a maximum of $50, while it continues to investigate."

**17. Oral notice is valid. The bank may require written confirmation within 10 business days to keep the provisional-credit right, and it must still investigate.**
Status: **stands**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.6 (1005.6(b)(5)(ii))
- Quote: "The consumer may notify the institution in person, by telephone, or in writing."
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.11 (1005.11(b)(2), (c)(2)(i)(A))
- Quote: "A financial institution may require the consumer to give written confirmation of an error within 10 business days of an oral notice."
- Quote: "The institution requires but does not receive written confirmation within 10 business days of an oral notice of error; or"
- Comment 11(c)-2: "It may not delay until it has received a written confirmation."
- FTC (item 2 URL): "Follow up immediately in writing." / "the date and time when you noticed your card was missing, and when you first reported the loss."

**18. The bank cannot require a police report before investigating.**
Status: **stands**
- URL: https://www.consumerfinance.gov/compliance/compliance-resources/deposit-accounts-resources/electronic-fund-transfers/electronic-fund-transfers-faqs/ (Error Resolution Q4, "Updated June 4, 2021". Not withdrawn: see the newer-rule search above.)
- Quote: "Can a financial institution require a consumer to file a police report or other documentation as a condition of initiating an error resolution investigation?" Answer: "No."

**19. Credit cards: $50 cap regardless of reporting speed, and $0 if reported before use.**
Status: **stands**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1026/section-1026.12 (1026.12(b)(1)(ii). Last amended 2019-04-01, and the 2025-2026 Reg Z rules are threshold and mortgage items that do not touch it.)
- Quote: "The liability of a cardholder for unauthorized use of a credit card shall not exceed the lesser of $50 or the amount of money, property, labor, or services obtained by the unauthorized use before notification to the card issuer"
- FTC table (item 2 URL), credit card reported after use: "The maximum you might be responsible for is $50". Debit row "more than 2 business days after you learn about the loss or theft, but within 60 calendar days after your statement is sent to you": $500.

**20. CFPB consumer guidance matches the tiers and timelines.**
Status: **stands**
- URL: https://www.consumerfinance.gov/ask-cfpb/how-do-i-get-my-money-back-after-i-discover-an-unauthorized-transaction-or-money-missing-from-my-bank-account-en-1017/ ("Last reviewed: AUG 28, 2026", "Page last modified Aug. 31, 2026 @ 11:55 AM EDT")
- Quote: "If you notify your bank or credit union after two business days, you could be responsible for up to $500 in unauthorized transactions."
- Quote: "In unusual circumstances, like lengthy travel or hospitalization that keeps you from notifying the bank within the time allowed, the notification periods above must be extended."
- Quote: "The bank or credit union must then resolve the issue in 45 days, unless the disputed transactions were conducted in a foreign country, were conducted within 30 days of account opening, or were debit card point-of-sale purchases." (The source elides the middle with "...". The elision is fair.)

**21. Denials, reversing a provisional credit, and escalation through the CFPB.**
Status: **stands**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.11 (1005.11(d)(1), (d)(2)(ii))
- Quote: "shall include a written explanation of the institution's findings and shall note the consumer's right to request the documents that the institution relied on in making its determination."
- Quote: "preauthorized transfers from the consumer's account (without charge to the consumer as a result of an overdraft) for five business days after the notification."
- URL: https://www.consumerfinance.gov/complaint/ ("Page last modified Oct. 5, 2026 @ 12:35 PM EDT")
- Quote: "Most companies respond within 15 days." Phone: (855) 411-2372.
- Comment 11(b)(1)-7: "Where the consumer's assertion of error involves an unauthorized EFT, however, the institution must comply with § 1005.6 before it may impose any liability on the consumer."

**22. Budget arithmetic: $3,400 − $1,550 = $1,850. Minus $1,215 leaves $635, minus $500 leaves $1,350 ($715 more), minus $50 leaves $1,800.**
Status: **stands**
- Recomputed: 3,400 − 1,550 = 1,850. 1,850 − 1,215 = 635. 1,850 − 500 = 1,350. 1,350 − 635 = 715. 1,850 − 50 = 1,800.

## Facts for the key

Each key bullet traces back to the items above, and all of them stand:
- **The premise is false.** Items 2, 4, 8, 9 and 10. Both of the rep's claims fail: "all $1,215" and "debit cards don't have the protection".
- **The $50 tier was lost and the user is in the $500 tier.** Items 3, 5 and 11. Window Oct 20-21, deadline 11:59 p.m. Wed Oct 21.
- **Figures.** Items 6, 7 and 9: $50 from Oct 19, $790 only if the bank establishes it, cap $500 or $50, at least $715 back and up to $1,165, all $1,215 only via network policy, agreement or state law. Negligence is irrelevant (item 10).
- **Timelines.** Item 16: 10 business days (Nov 6), provisional credit $1,165, 45 days (Dec 7), 90 days POS (Jan 21, 2027), no ATM extension.
- **Must-say points 1-4.** Items 13, 16, 17, 21 and 22.
- **Side claims.** Items 5, 10, 11, 12, 13, 16, 17, 18, 19 and 22. Each "wrong" label is supported by the quotes above.

Optional addition, not required: under 1005.6(a), a consumer can be held liable at all "only if the financial institution has provided the disclosures required by § 1005.7(b)(1) , (2) , and (3)", and the card must be an "accepted access device". This is a further reason to ask the bank for its basis, but it is a side point.

## Not decided in this pass
- **Illinois law (205 ILCS 616).** The primary text could not be opened because ilga.gov was unreachable. The tag **[varies by state; not verified]** stays.
- **Mastercard's zero-liability terms.** The page returned 403. Which network the card uses is unknown in any case.
- **Whether "buried at work" counts as an extenuating circumstance.** No authority says it does. The official examples are extended travel and hospitalization.
