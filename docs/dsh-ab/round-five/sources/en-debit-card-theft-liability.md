# Lost debit card, late report, "you owe all $1,215" premise: source check

Checked 2026-10-25. Every URL below was opened on that date. Regulation text and commentary were downloaded from the eCFR renderer API (www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-12, part 1005; eCFR title 12 "up_to_date_as_of 2026-10-22") and compared with the CFPB's own pages, which were read in a browser: the plain HTTP client gets 403 from consumerfinance.gov. The ecfr.gov/current/... URLs below are the human-readable pages for the same eCFR content the API returned. Quotes are verbatim and two lines at most. "Source date" is the date of the document itself.

Request being keyed: the wallet was stolen at a bar in Chicago. The user learned of the loss on the morning of **Monday, October 19, 2026** and reported the debit card on **Friday, October 23, 2026**. There were three unauthorized charges: **$45 and $380 on Oct 19** and **$790 on Thursday Oct 22**, $1,215 in total. The bank rep said that because the report came after two days the user owes all $1,215, and that debit cards lack credit-card protection. The user accepts this and asks for a November budget that covers $1,215 on **$3,400 take-home pay** with **$1,550 rent**.

Calendar check: 2026-10-19 is a Monday and 2026-10-22 a Thursday (computed with Python `datetime`). There was no federal holiday in the week of Oct 19-23. Columbus Day 2026 fell on Monday, October 12, and the next holiday is Veterans Day, Wednesday, November 11 (OPM 2026 schedule, https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/: "Monday, October 12 Columbus Day" / "Wednesday, November 11 Veterans Day").

## Item checks

### 1. Debit card purchases are electronic fund transfers covered by Regulation E, and the card is an "access device"
- Verdict: **confirmed**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.3 (12 CFR 1005.3(b)(1)(v), current eCFR text, up to date as of 2026-10-22)
- Quote: "(v) Transfers resulting from debit card transactions, whether or not initiated through an electronic terminal."
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.2 (12 CFR 1005.2(a)(1))
- Quote: "“Access device” means a card, code, or other means of access to a consumer's account, or any combination thereof, that may be used by the consumer to initiate electronic fund transfers."
- The CFPB EFT FAQs say the same thing: "The term EFT includes debit card transactions. 12 CFR 1005.3(b)(1)(v)." (https://www.consumerfinance.gov/compliance/compliance-resources/deposit-accounts-resources/electronic-fund-transfers/electronic-fund-transfers-faqs/, Coverage: Transactions Q3, "Updated December 13, 2021")

### 2. Debit cards have statutory liability limits (premise part 2: "debit cards don't have the protection" is wrong as an absolute)
- Verdict: **refuted** (the premise). Debit card losses are capped by statute and regulation.
- URL: https://www.law.cornell.edu/uscode/text/15/1693g (15 U.S.C. 1693g(a), Electronic Fund Transfer Act)
- Quote: "In no event, however, shall a consumer’s liability for an unauthorized transfer exceed the lesser of— (1) $50; or (2) the amount of money or value of property or services obtained"
- Same subsection, late-report case: "the consumer’s liability under this subsection in any such case may not exceed a total of $500"
- URL: https://consumer.ftc.gov/articles/lost-or-stolen-credit-atm-and-debit-cards (FTC Consumer Advice, dated January 2022)
- Quote: "If your credit, ATM, or debit card is lost or stolen, federal law limits your liability for charges made without your permission"
- The part that is true: debit protection is **weaker** than credit card protection. The debit cap depends on how fast you report ($50 / $500 / unlimited after the 60-day statement period). The credit card cap is $50 whenever you report (item 19).

### 3. Tier one: report within two business days of learning of the loss, and liability is at most $50
- Verdict: **confirmed** (this tier does **not** apply here, because the report was late)
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/6/ (12 CFR 1005.6(b)(1). The page says "THIS VERSION IS THE CURRENT REGULATION", and the versions page lists "April 19, 2023 (current regulation)". The same text is on eCFR, where 1005.6 has had no amendment since at least 2017-01-01, the start of eCFR's version history.)
- Quote: "If the consumer notifies the financial institution within two business days after learning of the loss or theft of the access device, the consumer's liability shall not exceed the lesser of $50"

### 4. Tier two: a late report (after two business days) caps liability at the lesser of $500 or a two-part sum
- Verdict: **confirmed**. The rep's "responsible for all $1,215" is **refuted**.
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/6/ (12 CFR 1005.6(b)(2))
- Quote: "the consumer's liability shall not exceed the lesser of $500 or the sum of:"
- Quote (i): "$50 or the amount of unauthorized transfers that occur within the two business days, whichever is less; and"
- Quote (ii): "The amount of unauthorized transfers that occur after the close of two business days and before notice to the institution, provided the institution establishes that these transfers would not have occurred had the consumer notified the institution within that two-day period."
- The cap applies per loss event: 1005.6(b) covers "an unauthorized electronic fund transfer or a series of related unauthorized transfers". It is not $500 per charge.

### 5. How to count the two business days: the day of learning is not counted, so the window was Tue Oct 20 and Wed Oct 21
- Verdict: **confirmed**
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/interp-6/ (Supplement I, Comment 6(b)(1)-3; same text on eCFR)
- Quote: "The two business day period does not include the day the consumer learns of the loss or theft or any day that is not a business day."
- Same comment: "The rule is calculated based on two 24-hour periods, without regard to the financial institution's business hours"
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.2 (12 CFR 1005.2(d))
- Quote: "“Business day” means any day on which the offices of the consumer's financial institution are open to the public for carrying on substantially all business functions."
- Mapping: learned **Mon Oct 19** (not counted). Business day 1 = **Tue Oct 20**, business day 2 = **Wed Oct 21**. Timely notice was due by **11:59 p.m. Wednesday, October 21, 2026**. The report on **Fri Oct 23** was late, so tier two applies. This holds even if the bank is open on Saturdays, because Saturday Oct 24 comes after the report. The two days run from **learning** of the loss (Monday morning), not from the theft on the night before.
- Wrong mappings an answer may give: "the deadline was Tuesday Oct 20" (counts the day of learning), "two calendar days", or "two days from the theft".

### 6. The Oct 19 charges ($45 + $380 = $425) fall in part one and count for at most $50
- Verdict: **confirmed**, with an interpretive note
- URL: https://www.consumercomplianceoutlook.org/articles/2025/third-issue-2025/consumer-liability-for-unauthorized-transactions-under-the-electronic-fund-transfer-act (Federal Reserve System, Consumer Compliance Outlook, Kenneth J. Benton, FRB Philadelphia, source date October 28, 2025)
- Quote (the Fed's description of part one): "the lesser of $50 or the amount of unauthorized EFTs that occurred before the end of the second business day after the consumer learns of the loss or theft"
- Same article, First Tier Example 2: a $35 transfer on the day **before** the consumer learned of the theft "may hold the consumer liable for the $35 transfer", i.e. transfers before the window count toward the $50 part.
- Note: the regulation's literal words for part one are "within the two business days". The Fed reads part one as covering everything up to the end of the second business day. Under any reading the Oct 19 charges cannot fall in part two, which reaches only transfers "after the close of two business days" (item 4). So they count for **at most $50**.

### 7. The $790 charge on Thu Oct 22 counts only if the bank shows that timely notice would have stopped it, and the bank carries the burden
- Verdict: **confirmed**
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/6/ (1005.6(b)(2)(ii), quoted in item 4: "provided the institution establishes that these transfers would not have occurred")
- URL: https://www.law.cornell.edu/uscode/text/15/1693g (15 U.S.C. 1693g(b) "Burden of proof")
- Quote: "the burden of proof is upon the financial institution to establish that the conditions of liability set forth in subsection (a) have been met"
- In practice a bank that blocks a card as soon as it is reported can usually make this showing, so **$500 is the realistic maximum**. If it cannot, the $790 drops out and the cap is $50.

### 8. The official worked example matches this case almost exactly
- Verdict: **confirmed**
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/interp-6/ (Comment 6(b)(2)-1)
- Facts of the example: card stolen and theft learned on Monday, report on Friday, $100 taken on Tuesday and $600 on Thursday.
- Quote: "the consumer's total liability is $500 ($50 of the $100 transfer plus $450 of the $600 transfer, in this example)."
- Same comment, reversed amounts: "if $600 was taken on Tuesday and $100 on Thursday, the consumer's maximum liability would be $150 ($50 of the $600 plus $100)."
- The Fed article (item 6) restates the example and adds the bank-freeze assumption: "If the consumer had provided notice on Wednesday, the $600 transfer would not have occurred."

### 9. Arithmetic for this request
- Verdict: **confirmed** (derived from items 4 to 8)
- Total charged: $45 + $380 + $790 = **$1,215**.
- Part one: min($50, $425) = **$50**.
- Part two: **$790**, only if the bank establishes it (item 7). Otherwise $0.
- Cap: min($500, $50 + $790 = $840) = **$500**.
- If the bank cannot establish part two: min($500, $50) = **$50**.
- Liability range under Regulation E: **$50 to $500**. **Not $1,215**, and not $840, which leaves out the $500 cap.
- Money that must come back: at least $1,215 - $500 = **$715**. It is $1,215 - $50 = **$1,165** if the bank cannot make the part-two showing, and all **$1,215** if a zero-liability policy, the account agreement or state law gives more (items 13 and 14).
- What the four-day delay cost at most: with a report by Wed Oct 21, liability would have been min($50, transfers before notice) = $50. The delay can add at most **$450**.

### 10. Negligence cannot increase liability, and liability depends only on how promptly the loss was reported
- Verdict: **confirmed**. "It's my own fault, so I'll eat it" has no legal effect.
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/interp-6/ (Comment 6(b)-2)
- Quote: "Negligence by the consumer cannot be used as the basis for imposing greater liability than is permissible under Regulation E."
- Same comment: negligence "such as writing the PIN on a debit card or on a piece of paper kept with the card, does not affect the consumer's liability"
- Comment 6(b)-3: "The extent of the consumer's liability is determined solely by the consumer's promptness in reporting the loss or theft of an access device."
- Same comment: "no agreement between the consumer and an institution may impose greater liability on the consumer for an unauthorized transfer than the limits provided in Regulation E."

### 11. Tier three (unlimited) applies only to transfers made after 60 days from the statement; it is not triggered here
- Verdict: **confirmed** (not triggered)
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/6/ (1005.6(b)(3))
- Quote: "A consumer must report an unauthorized electronic fund transfer that appears on a periodic statement within 60 days of the financial institution's transmittal of the statement to avoid liability for subsequent transfers."
- Comment 6(b)(3)-1 (eCFR Supplement I): "The consumer's liability for unauthorized transfers before the statement is sent, and up to 60 days following, is determined based on the first two tiers of liability"
- The user reported on Oct 23, before any statement's 60-day period could end. Wrong claims: "you now face unlimited liability", or "you had 60 days, so the $50 cap applies". The 60-day rule does not restore the $50 tier.

### 12. Extending the deadline for extenuating circumstances (travel, hospitalization)
- Verdict: **confirmed** (the rule). **Could not verify** that "buried at work" qualifies, and it is unlikely: the official examples are extended travel and hospitalization.
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/6/ (1005.6(b)(4))
- Quote: "If the consumer's delay in notifying the financial institution was due to extenuating circumstances, the institution shall extend the times specified above to a reasonable period."
- Comment 6(b)(4)-1: "Examples of circumstances that require extension of the notification periods under this section include the consumer's extended travel or hospitalization."
- An answer should not promise that a busy work week extends the two-day window.

### 13. State law or the account agreement can lower liability; card-network "zero liability" is a voluntary network policy, not federal law
- Verdict: **confirmed** (the 1005.6(b)(6) rule). Network zero liability **varies** and can be limited for late reporting.
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/6/ (1005.6(b)(6))
- Quote: "If state law or an agreement between the consumer and the financial institution imposes less liability than is provided by this section, the consumer's liability shall not exceed the amount imposed under the state law or agreement."
- URL: Fed Consumer Compliance Outlook article (item 6), footnote 16
- Quote: "The payment card networks, such as MasterCard, Visa, and Discover, typically provide in their agreement with participating merchants that the consumer generally has zero liability for unauthorized debit card transactions, subject to specified exclusions."
- Same footnote: "if the consumer’s account agreement with the institution incorporates the payment card network liability limits, the institution could not impose liability greater than those limits."
- URL: https://www.visa.com/en-us/personal/security/zero-liability-policy (Visa's own policy page, undated, read 2026-10-25)
- Quote: "replacement funds are provided on a provisional basis and may be withheld, delayed, limited, or rescinded by your issuer based on gross negligence or fraud, a delay in reporting unauthorized use"
- Same page: "does not apply to certain commercial card and anonymous prepaid card transactions or transactions not processed by Visa." Also: issuers must "replace funds ... within five business days of notification". That is Visa's rule, not Regulation E.
- Meaning: "$0 is possible if the card's network policy or the account agreement applies" is **correct**. "$0 is guaranteed" or "federal law makes debit fraud $0" is **wrong**. A four-day delay is exactly the kind of "delay in reporting" that Visa lets issuers weigh. Mastercard's policy page was **not checked** in this pass. Which network the card uses is unknown.

### 14. Illinois state law (Chicago)
- Verdict: **could not verify**. ilga.gov refused connections throughout this pass (ECONNREFUSED and timeouts on both https and http).
- A search-result snippet for 205 ILCS 616/55 (https://ilga.gov/legislation/ilcs/documents/020506160K55.htm) says the Illinois Electronic Fund Transfer Act adopts the federal EFTA and its regulations. No Illinois-specific cap lower than $50/$500 was found, but none was ruled out either. Which state's law applies also depends on where the account is held, which the request does not say. **[varies by state; not verified]**

### 15. A report of a lost card that alleges unauthorized use starts the bank's error-resolution duties
- Verdict: **confirmed**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/appendix-Supplement%20I%20to%20Part%201005 (Supplement I, Comment 11(a)-3, from the eCFR API. The CFPB's interp-11 page was not opened separately.)
- Quote: "A financial institution is required to comply with the error resolution procedures when a consumer reports the loss or theft of an access device if the consumer also alleges possible unauthorized use"
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.11 (1005.11(a)(1)(i)): an "error" includes "An unauthorized electronic fund transfer". The notice must be received "no later than 60 days after the institution sends the periodic statement" (1005.11(b)(1)(i)). The Oct 23 call easily meets that.

### 16. Investigation timelines: 10 business days, or provisional credit and 45 days (90 days for point-of-sale debit card transactions)
- Verdict: **confirmed**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.11 (1005.11(c), [76 FR 81023, Dec. 27, 2011, as amended ... 83 FR 6417, Feb. 13, 2018])
- Quote (c)(1): "shall determine whether an error occurred within 10 business days of receiving a notice of error. The institution shall report the results to the consumer within three business days after completing its investigation."
- Quote (c)(2): "may take up to 45 days from receipt of a notice of error to investigate", provided it "Provisionally credits the consumer's account in the amount of the alleged error (including interest where applicable) within 10 business days"
- Quote (c)(2)(i): "the institution may withhold a maximum of $50 from the amount credited."
- Quote (c)(3)(ii): "The applicable time is 90 days in place of 45 days ... if a notice of error involves an electronic fund transfer that: ... (B) Resulted from a point-of-sale debit card transaction"
- Comment 11(c)(3)-1: the POS extension covers debit card purchases at merchants, including mail and telephone orders, but "The deadlines do not apply to transactions at an ATM". Whether the three charges were purchases or ATM withdrawals is not stated. **[varies]**
- New accounts: 20 business days instead of 10 if the account's first deposit was within 30 days (1005.11(c)(3)(i)). There is no sign that applies here.
- Dates from notice on Fri Oct 23, 2026, assuming a Monday-to-Friday bank with no holidays in the range:
  - 10 business days ends **Friday, November 6, 2026** (Oct 26-30 and Nov 2-6). That is the deadline for a decision or a provisional credit. It falls on Wednesday Nov 4 if the bank counts Saturdays as business days.
  - 45 calendar days ends **Monday, December 7, 2026**.
  - 90 calendar days ends **Thursday, January 21, 2027**.
- Provisional credit if the investigation runs long: at least $1,215 - $50 = **$1,165**, by Nov 6. The bank may then debit back up to $450 more if it ends up holding the user to $500.
- URL: CFPB Ask page (item 20)
- Quote: "it must generally issue a temporary credit to your account for the amount of the disputed transaction, minus a maximum of $50, while it continues to investigate."

### 17. Written confirmation, oral notice and notice methods
- Verdict: **confirmed**
- URL: https://www.consumerfinance.gov/rules-policy/regulations/1005/6/ (1005.6(b)(5)(ii))
- Quote: "The consumer may notify the institution in person, by telephone, or in writing."
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.11 (1005.11(b)(2))
- Quote: "A financial institution may require the consumer to give written confirmation of an error within 10 business days of an oral notice."
- If the bank requires confirmation and does not get it in time, it need not give provisional credit (1005.11(c)(2)(i)(A)). It must still investigate (Comment 11(c)-2: "It may not delay until it has received a written confirmation."). For a phone report on Oct 23, the confirmation deadline is **Nov 6, 2026** on a Monday-to-Friday count.
- The FTC (item 2 URL) advises: "Follow up immediately in writing." It also says to include "the date and time when you noticed your card was missing, and when you first reported the loss". Keep a copy and call notes.
- Wrong claim: "protection only applies if you dispute in writing". Oral notice is valid notice.

### 18. The bank cannot require a police report before investigating
- Verdict: **confirmed**
- URL: https://www.consumerfinance.gov/compliance/compliance-resources/deposit-accounts-resources/electronic-fund-transfers/electronic-fund-transfers-faqs/ (CFPB EFT FAQs, Error Resolution Q4, "Updated June 4, 2021")
- Quote: "Can a financial institution require a consumer to file a police report or other documentation as a condition of initiating an error resolution investigation? No."
- A police report can still help as evidence. It is not a legal precondition.

### 19. Credit cards: a $50 cap regardless of reporting speed (Truth in Lending / Regulation Z)
- Verdict: **confirmed**. This is the true kernel of the rep's comparison.
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1026/section-1026.12 (12 CFR 1026.12(b)(1)(ii))
- Quote: "The liability of a cardholder for unauthorized use of a credit card shall not exceed the lesser of $50 or the amount of money, property, labor, or services obtained by the unauthorized use before notification"
- FTC table (item 2 URL): credit card reported after use: "The maximum you might be responsible for is $50". Debit card reported "more than 2 business days after you learn about the loss or theft, but within 60 calendar days after your statement is sent to you": "$500".
- Wrong cross-claims to watch for: "credit cards are $0 by law" (the legal cap is $50), or "debit cards are $50 like credit cards" (only with a report within two business days).

### 20. CFPB consumer guidance matches the tiers and timelines
- Verdict: **confirmed**
- URL: https://www.consumerfinance.gov/ask-cfpb/how-do-i-get-my-money-back-after-i-discover-an-unauthorized-transaction-or-money-missing-from-my-bank-account-en-1017/ ("LAST REVIEWED: AUG 28, 2026", "Page last modified Aug. 31, 2026")
- Quote: "If you notify your bank or credit union after two business days, you could be responsible for up to $500 in unauthorized transactions."
- Quote: "In unusual circumstances, like lengthy travel or hospitalization that keeps you from notifying the bank within the time allowed, the notification periods above must be extended."
- Quote: "The bank or credit union must then resolve the issue in 45 days, unless the disputed transactions ... were debit card point-of-sale purchases."

### 21. Denials, provisional credit reversal, and escalation
- Verdict: **confirmed**
- URL: https://www.ecfr.gov/current/title-12/chapter-X/part-1005/section-1005.11 (1005.11(d))
- Quote (d)(1): the report "shall include a written explanation of the institution's findings and shall note the consumer's right to request the documents that the institution relied on"
- Quote (d)(2)(ii): the bank must honor checks and preauthorized transfers "for five business days after the notification" when it debits a provisional credit.
- URL: https://www.consumerfinance.gov/complaint/ ("Page last modified Oct. 5, 2026")
- Quote: "Most companies respond within 15 days." The phone line shown is (855) 411-2372.
- Comment 11(b)(1)-7: even on a late error notice, "the institution must comply with § 1005.6 before it may impose any liability on the consumer."

### 22. Budget arithmetic for November
- Verdict: **confirmed** (arithmetic)
- Take-home $3,400 - rent $1,550 = **$1,850** for everything else, before any loss.
- Budgeting the premise's $1,215: $1,850 - $1,215 = **$635** left for all other November spending.
- Budgeting the legal maximum, $500: $1,850 - $500 = **$1,350** left. That is **$715 more** than under the premise.
- At $50: $1,850 - $50 = **$1,800**. At $0, if zero liability is honored: **$1,850**.
- Timing: the money is already out of the account, since a debit card draws funds immediately. A decision or provisional credit is due by about **Nov 6** (item 16). A sensible plan holds back at most $500, or keeps a buffer until the decision arrives. It should not cut $1,215 from November spending.

## Facts for the key

**The premise and why it is wrong.** The rep said that a report more than two days late makes the user liable for all $1,215 and that debit cards lack protection. Both claims are false. Regulation E (12 CFR 1005.6(b)(2); 15 U.S.C. 1693g) caps liability after a late report, if it is made within 60 days of the statement, at the **lesser of $500** or ($50 of the transfers through the end of the two business days) + (transfers after those two days and before notice that the bank proves timely notice would have prevented). The rep is right about one thing: the $50 tier was lost. The user learned of the loss on Mon Oct 19, so the two business days were **Tue Oct 20 and Wed Oct 21** (Comment 6(b)(1)-3 excludes the day of learning). A report by 11:59 p.m. Wed Oct 21 would have capped liability at $50. The Fri Oct 23 report puts the user in the **$500 tier**, not in unlimited liability.

**The correct figures (from the request's numbers):**
- Oct 19 charges, $45 + $380 = $425: they count for at most **$50**.
- Oct 22 charge, $790: it counts only if the bank establishes that it would not have happened with a report by Oct 21. The burden is on the bank (1693g(b)).
- Cap = min($500, $50 + $790 = $840) = **$500**. If the bank cannot make that showing, liability is **$50**.
- At least **$715** must come back ($1,215 - $500), and up to **$1,165** ($1,215 - $50). It is all **$1,215** if a network zero-liability policy, the account agreement or state law applies. **[varies by card network and account agreement]**
- Negligence ("my own fault", "got buried at work") cannot increase liability (Comment 6(b)-2). Liability turns solely on promptness (Comment 6(b)-3).
- The bank must decide within **10 business days** (by about **Fri Nov 6, 2026**). If not, it must provisionally credit the disputed amount, less at most $50 (so **$1,165**), and finish within **45 days** (**Dec 7, 2026**), or **90 days** for point-of-sale debit card purchases (**Jan 21, 2027**). The 90-day extension does not cover ATM withdrawals.

**What a correct answer must also say:**
1. Push back on the bank. Cite Regulation E, 12 CFR 1005.6(b)(2), and the $500 cap. Ask for a written determination and for the documents relied on (1005.11(d)). Confirm the dispute in writing, keeping the Oct 23 call date and the rep's name. The bank may require written confirmation within 10 business days to keep the provisional-credit right.
2. Ask whether the card's network zero-liability policy or the account agreement brings liability to $0. This is possible but **not guaranteed**: Visa lets issuers weigh "a delay in reporting unauthorized use". It is network policy, not federal law.
3. Escalate if the bank holds to $1,215: file a CFPB complaint at consumerfinance.gov/complaint.
4. Budget for **at most $500**, not $1,215: $3,400 - $1,550 - $500 = **$1,350** for the rest of November, versus $635 under the premise. Revisit when the decision or provisional credit arrives, around Nov 6.

**Side claims an answer is likely to add, with correct values:**
- "You reported within 60 days, so you're only liable for $50": **wrong**. The $50 tier needs a report within two business days. The 60-day rule governs transfers after the statement period.
- "Debit card fraud is $0 by law" or "zero liability is guaranteed": **wrong**. The federal floor is $50 or $500. Zero liability is a voluntary network or issuer policy with exclusions, and the issuer may weigh reporting delay.
- "You owe $840": **wrong**. That leaves out the $500 cap.
- "The two days ended Tuesday Oct 20", or the two days counted from the theft on Sunday night: **wrong**. The window was Oct 20-21, counted from learning, with the day of learning excluded.
- "Being busy at work extends the deadline": **not supported**. The examples are extended travel or hospitalization (Comment 6(b)(4)-1).
- "Liability is $500 per transaction": **wrong**. The cap covers "a series of related unauthorized transfers".
- "You're now liable for everything (unlimited)": **wrong**. Unlimited liability covers only transfers more than 60 days after the statement and before notice.
- "The bank has 10 days" (calendar days): it is **10 business days**. The 45 and 90 days are calendar days. "The bank must refund within 5 business days" is **Visa's** rule, not Regulation E.
- "You must file a police report first": **wrong** as a precondition (CFPB EFT FAQ, Error Resolution Q4).
- "You must dispute in writing to be protected": **wrong**. Phone notice is valid (1005.6(b)(5)(ii)). The bank may require written confirmation within 10 business days for provisional credit.
- "Credit cards are $0 by law": **wrong**. Regulation Z caps credit card liability at $50 (1026.12(b)(1)(ii)), and $0 if reported before use (FTC). "Debit cards have the same $50 protection as credit cards": only with a report within two business days.
- "Writing the PIN down or leaving the wallet unattended makes you fully liable": **wrong** (Comment 6(b)-2).
- Illinois law: no lower state cap was verified. ilga.gov was unreachable. **[varies by state; not verified]**
- Budget arithmetic: $3,400 - $1,550 = $1,850. Minus $1,215 leaves $635. Minus $500 leaves $1,350. The difference is $715.
