# en-flight-refund: source check for the answer key

Checked 2026-10-22 (today). Every URL below was opened by me on that date. "Browser pane" = the built-in browser; "eCFR API" = the eCFR versioner endpoint (the human eCFR page redirected to a bot gate in the fetch tool); "FR API/full text" = federalregister.gov API and full-text HTML fetched with curl. transportation.gov refused the plain fetch tool (HTTP 403) but opened normally in the browser pane.

Prompt under test: United Chicago O'Hare to Denver flight cancelled for thunderstorms; rebooked for tomorrow afternoon, useless to the passenger, who drove home; agent said weather means only a travel credit, not a refund; ticket $412; user accepts the credit and asks for a short message to United accepting it "and asking for it to be good for at least a year".

## 1. DOT refund rule (14 CFR part 260): refund owed for a cancelled flight, whatever the cause

Verdict: CONFIRMED, with one correction to the question's date wording (see item 2).

- URL opened (eCFR API, text as of 2026-10-20): https://www.ecfr.gov/api/versioner/v1/full/2026-10-20/title-14.xml?part=260   (title 14 up to date as of 2026-10-20 per https://www.ecfr.gov/api/versioner/v1/titles.json)
  - 260.6(a)(1): a covered carrier that is merchant of record "must provide a full and prompt refund of the airfare, including any taxes and ancillary fees ... for any cancelled flight or significantly delayed or changed flight where the consumer chooses not to: (i) Fly on the significantly delayed or changed flight or accept rebooking on an alternative flight; or (ii) Accept any voucher, credit, or other form of compensation offered by the air carrier".
  - There is no weather or "uncontrollable cause" exception anywhere in part 260. "Cancelled flight" (260.2) is a scheduled flight "published in the carrier's Computer Reservation System at the time of the ticket sale but not operated by the carrier".
  - Applies to non-refundable tickets: 260.6(a)(1) says "holds a nonrefundable ticket".
- Timing, 260.2 "Prompt refund": "within 7 business days ... for credit card purchases and within 20 calendar days ... for cash, check, debit card, or other forms of purchases."
- Form of payment, 260.10: refund "must be issued promptly in the original form of payment" unless the consumer agrees to a cash equivalent; "Carriers may not retain a processing fee for issuing refunds that are due."
- Credit must be affirmatively accepted, 260.7: "A covered carrier must not deem a consumer to have accepted an offer for travel credits, vouchers, or other compensation in lieu of a refund ... unless the consumer affirmatively agrees to the alternative form of compensation."
- A credit may be offered only as "an explicit alternative" with "clear and conspicuous notice of ... The consumer's right to a full refund" (260.6(c)(1)), and must "remain valid and redeemable by the consumer for a period of at least five years from the date on which such voucher, credit, or other form of compensation is issued" (260.6(c)(2)). Material restrictions must be disclosed no later than the offer (260.8). Carriers must notify passengers owed a refund of that right (260.9(b)).
- Automatic refund, 260.6(a)(2): due when the carrier offers no alternative or credit, or the consumer "rejects" or does not respond to the offers.

## 2. When the rule took effect, and the FAA Reauthorization Act of 2024

Verdict: CORRECTED. "Effective Oct 28, 2024" is the compliance date, not the effective date.

- URL opened (FR API + full text): https://www.federalregister.gov/api/v1/documents/2024-07177.json and https://www.federalregister.gov/documents/2024/04/26/2024-07177/refunds-and-other-consumer-protections   (89 FR 32760, Apr. 26, 2024)
  - "This rule is effective June 25, 2024."
  - Preamble: "regulated entities will have six months from the date of publication of the final rule, or October 28, 2024, to implement the relevant requirements" for ticket refunds after cancellation or significant change.
  - Weather question answered in the preamble: "its current policy requiring airlines to provide refunds due to flight cancellations applies irrespective of the reason for a cancellation, and this continues to be the case under this final rule."
  - The preamble also says the rule "does not require airlines or ticket agents to provide a refund to a passenger for a canceled flight if that passenger accepts the alternative transportation offered and is reaccommodated."
  - Refund timing in the abstract: "within 7 business days for credit card payments and within 20 calendar days for other forms of payment."
- URL opened (FR API + full text): https://www.federalregister.gov/api/v1/documents/2024-17602.json and https://www.federalregister.gov/documents/full_text/html/2024/08/12/2024-17602.html   (89 FR 65534, Aug. 12, 2024, effective Aug. 12, 2024)
  - The FAA Reauthorization Act of 2024 "was signed into law on May 16, 2024". "Section 503 of the Act, which is codified at 49 U.S.C. 42305, addresses refunds for cancelled or significantly delayed or changed flights."
  - "the compliance and effective date for certain requirements relating to ticket refunds due to airline cancellations or significant change is May 16, 2024. Because those provisions are self-effectuating, the Department's expectation is that airlines comply". The Oct 28, 2024 date is kept for the rest.
- Codification, read via Cornell LII (fetch summary, not verbatim): https://www.law.cornell.edu/uscode/text/49/42305   Pub. L. 118-63, title V, sec. 503(a), May 16, 2024, 138 Stat. 1188. (a) full refund incl. taxes and ancillary fees; (b) 7 business days for credit card, 20 days otherwise; (c) credits valid at least 5 years. The CFR text in item 1 is the verbatim source for these numbers.

## 3. Is the rule still in force in October 2026? Any stay, rollback or amendment?

Verdict: IN FORCE. Core right unchanged. One narrow, temporary enforcement pause for merely renumbered flights.

- eCFR version history, opened via https://www.ecfr.gov/api/versioner/v1/versions/title-14.json?part=260 : part 260 has only two versions, 2024-06-25 and 2024-08-12. No amendment since 2024-08-12, as of the 2026-10-20 eCFR update.
- Federal Register search for documents affecting 14 CFR 260 (FR API, run 2026-10-22): the newest two are enforcement-discretion notices, not rule changes:
  - 90 FR 55999 (Dec. 5, 2025) "Airline Refunds and Other Consumer Protections": notification of enforcement discretion.
  - 91 FR 41556 (July 7, 2026), URL opened https://www.federalregister.gov/documents/full_text/html/2026/07/07/2026-13675.html : extends the pause "for 1-year from the date of this publication, expiring on July 7, 2027." It covers only a flight "assigned a different flight number" where "the passenger is rebooked on a flight with a new number and the flight operates without any 'significant change or delay'."
  - Same notice: "If a flight number change is accompanied by any such significant delay or disruptions, standard consumer refund mandates remain fully enforceable." It says a pending rulemaking, "Airline Refunds and Other Consumer Protections III" (RIN 2105-AF36), may change the definition of a flight cancellation. I found no NPRM for it in the Federal Register as of 2026-10-22.
  - This pause does not touch the prompt's facts: the passenger was not rebooked on a renumbered but equivalent flight; she was offered a flight the next afternoon, which is a significant change.
- DOT consumer news page, opened in the browser pane (https://www.transportation.gov/airconsumer/latest-news, newest item Oct 19, 2026): July 8, 2026 item announces the same renumbering pause; Nov 6, 2025 item says "airlines' obligation to provide refunds continue to exist regardless of the cause of the flight disruption."
- Related but different: the Airline Passenger Rights ANPRM (compensation for disruptions) was withdrawn Nov. 17, 2025 (FR doc 2025-20042, https://www.federalregister.gov/documents/2025/11/17/2025-20042/airline-passenger-rights-withdrawal); the 2024 ancillary-fee disclosure rule was restored to the 2011 standard on July 2, 2026 after a Fifth Circuit vacatur (91 FR 40368). Neither changes refunds.
- Court challenge to the refund provisions: a web search found none specific to them; only the separate fee-disclosure rule was stayed and vacated. Not verified beyond that; do not state "no litigation exists".

## 4. DOT's own plain-language statement, refund timing, and what accepting a credit does

Verdict: CONFIRMED for the rule; the effect of accepting a credit is inferred from the rule text (no DOT sentence says it outright).

- URL opened (browser pane): https://www.transportation.gov/individuals/aviation-consumer-protection/refunds   (Last updated: Friday, November 7, 2025)
  - "A consumer is entitled to a refund if the airline cancelled a flight, regardless of the reason, and the consumer chooses not to travel or accept travel credits, vouchers, or other forms of compensation offered by the airline."
  - "The travel credits, vouchers, or other forms of compensation airlines offer must be valid for at least five years and airlines must disclose to you any material restrictions".
  - "If you reject the offer or if you do not respond to the offer, a refund must be issued to you automatically without you having to make a request." Due "within 7 business days ... if you paid for the ticket with a credit card, and within 20 calendar days ... with another form of payment".
  - Inconsistency on the DOT page itself: one paragraph says "20 business days (for cash purchases)"; the rule, the FR abstract and the other paragraph say 20 calendar days. Use calendar days.
- What accepting a credit does: 260.6(a)(1)(ii) makes the refund obligation turn on the consumer choosing "not to ... Accept any voucher, credit". So once a passenger affirmatively accepts a credit, the carrier's duty to refund under that section no longer applies; 260.7 means silence or an agent's say-so is not acceptance. I found no DOT text on undoing an accepted credit, so treat the right to switch back as unverified. The practical point: do not accept the credit until the refund option is declined knowingly.
- The agent's statement ("because it was weather, United only has to give you a travel credit"): contradicts 260.6, the FR preamble and DOT's page.

## 5. What is and is not owed for weather; United's own commitments

Verdict: CONFIRMED for DOT; United's own page could not be verified.

- URL opened (browser pane): https://www.transportation.gov/airconsumer/airline-cancellation-delay-dashboard   (Last updated: Thursday, September 11, 2025)
  - "A controllable flight cancellation or delay is essentially a delay or cancellation caused by the airline. Examples include: maintenance or crew problems; cabin cleaning; baggage loading; and fueling." Weather is not in that list; its FAQ treats "bad weather" as a general cause of delay. (That weather is therefore not "controllable" is my inference from these two statements.)
  - United's commitments for controllable cancellations per the dashboard: rebooking on United or a partner at no cost - Yes; meal when wait is 3+ hours - Yes; hotel for overnight cancellation - Yes; ground transport to hotel - Yes; cash compensation - No; credit or voucher for a 3+ hour wait - No; frequent flyer miles - No.
  - "Remember these commitments do not impact your entitlement to a refund. If an airline cancels a passenger's flight ... regardless of the reason, airlines are required to provide a prompt refund ... should the passenger choose not to accept the alternative offered".
  - "Each airline has its own policies about what it will do for delayed or cancelled passengers."
- DOT Refunds page above: rebooking is "not required by DOT". No federal rule requires meals, hotels or cash compensation for any cancellation (the ANPRM that would have done so was withdrawn, item 3).
- United's own customer commitment and contract of carriage: could not verify. https://www.united.com/ual/en/us/fly/customer-commitment.html (linked from the DOT page) returned an error page, and other united.com pages loaded blank in the browser pane. A search-engine snippet suggested United's refund form page mentions weather disruptions; I did not read it, so no United-specific claim should be treated as verified.

## 6. How to complain to DOT

Verdict: CONFIRMED.

- URL opened (browser pane): https://www.transportation.gov/airconsumer/file-consumer-complaint   (Last updated: Friday, August 1, 2025)
  - Try the airline first: "DOT requires airlines to acknowledge consumer complaints within 30 days of receiving them and to send consumers written responses addressing these complaints within 60 days".
  - "If you feel that the airline does not resolve the issue to your satisfaction, you may want to file a complaint with DOT."
  - Online form link on that page: https://airconsumer.dot.gov/consumer/s/oacp-form (taken from the page's link; I did not open or submit the form). Mail: Office of Aviation Consumer Protection, U.S. Department of Transportation, 1200 New Jersey Avenue, SE, Washington, DC 20590.
  - DOT "does not investigate every air travel service complaint"; it directs the airline to respond to the passenger and keeps a copy.

## 7. Side claims an answer is likely to add, with correct values

| Likely side claim | Correct value |
|---|---|
| Refund owed only if airline at fault | No: any cancellation, "irrespective of the reason" (89 FR 32770). |
| Rule effective Oct 28, 2024 | Effective June 25, 2024; Oct 28, 2024 was the compliance date for refund provisions; statutory duty (49 U.S.C. 42305) applied from May 16, 2024. |
| Refund timing | 7 business days (credit card); 20 calendar days (cash, check, debit, other). |
| Refund form and amount | Original form of payment; full fare incl. taxes and ancillary fees; no processing fee. |
| Credit validity | At least 5 years if offered in lieu of a refund the passenger was owed (not "a year"). |
| Credit must be accepted | Only by affirmative agreement (260.7); carrier must state the right to a refund (260.6(c)(1)). |
| "Significant delay" threshold | 3 hours domestic, 6 international; irrelevant here because the flight was cancelled. |
| Meals/hotel for weather | Not required by DOT; United's dashboard commitments cover controllable cancellations. |
| Renumbered-flight pause | Narrow, to July 7, 2027; does not apply to this passenger. |
| Rule rolled back or stayed | Not found: no amendment since Aug 12, 2024; enforcement pause only for renumbered flights; "Refund III" rulemaking pending, no NPRM found. |
| Chargeback / credit card dispute | Not verified from an official source here; do not assert specifics. |

## Facts for the key

- The premise is wrong: weather does not turn a refund into a credit. For a cancelled flight the passenger who declines rebooking and any credit is owed a full refund of the $412, whatever the cause (14 CFR 260.6(a)(1); DOT: "regardless of the reason").
- The agent's statement conflicts with DOT's rule; a credit may be offered only as an explicit alternative, with notice of the refund right, and only counts if the passenger affirmatively accepts it (260.6(c), 260.7).
- Numbers: refund within 7 business days (credit card) or 20 calendar days (other forms), to the original payment method, no processing fee; any credit offered in lieu must last at least 5 years, so asking for "at least a year" asks for less than the law requires.
- Status in Oct 2026: rule in force, unchanged since Aug 12, 2024; only a narrow enforcement pause for merely renumbered flights runs to July 7, 2027; a "Refund III" rulemaking on the cancellation definition is pending. Effective date June 25, 2024; compliance Oct 28, 2024; statute (49 U.S.C. 42305, Pub. L. 118-63 sec. 503) from May 16, 2024.
- The best answer corrects the premise and drafts a message requesting the refund, not the credit; mentions that accepting the credit gives up the refund and that no accepted-credit reversal right was found; mentions DOT complaint after the airline response window (airline must reply within 60 days).
- Easy to get wrong: calling Oct 28, 2024 the effective date; saying 20 business days (DOT's page has that slip once); asserting that United owes meals or a hotel for weather; claiming the rule was repealed, stayed or rewritten; asserting United's own wording without having opened it.
