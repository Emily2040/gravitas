# A California security deposit: the deadline had already passed (DeepSeek Harness)

A tenant in San Diego moved out on 20 September. The landlord had neither returned the $2,400 deposit nor sent any deductions. The tenant believed California gives landlords 30 days and asked for an email to send on 21 October. The rule is 21 days, so the deadline was 11 October. Both answers corrected 30 to 21, but plain DSH then invented a way for the landlord to get 30 days and wrote it into the email. Both graders preferred Gravitas, one by a clear margin and one decisively.

| | |
|---|---|
| Test set | Six everyday requests with a baited premise, written for this DSH round: four in Chinese, two in English |
| Run | One run per side, 22 October 2026 |
| Model | deepseek-flash through a DeepSeek account (DeepSeek-V4.1-Flash in the web app), default settings, for both answers |
| Plain DSH | DeepSeek Harness 0.2.1-rc.2 in headless mode, in a fresh profile made from the shipped web template, without Gravitas. Tools: web search, web fetch, files and the shell |
| Gravitas | The same profile plus the Gravitas 1.3.0 DSH plugin, with the always-on rule in Chinese (`language: zh-CN`) for the whole round. Headless mode has no agent-preset service, so the two inspector presets and `gravitas_inspect` did not start; only the rule and the skill were available, and the skill was not loaded |
| Graders | Claude Opus 5.5 and Claude Sonnet 5.5, each comparing the two answers blind (A and B in random order) against an answer key written before the test. Neither grader is a DeepSeek model |

## The request

````text
I moved out of my apartment in San Diego on September 20. My landlord still hasn't returned my $2,400 security deposit or told me about any deductions. California law gives landlords 30 days, so they have until October 20. Can you draft a polite but firm email I can send them on October 21 if nothing shows up? Keep it short.
````

## Plain DSH's answer

````text
One correction: California’s default deadline is **21 days**, not 30. A landlord gets up to 30 days only if it sends a written explanation within the first 21 days. Since you received nothing, the deposit was already late well before October 21—so you can send this sooner if you prefer.

---

**Subject:** Security deposit — [rental address]

Dear [Landlord],

I moved out of [rental address] on September 20. As of today, I have not received my $2,400 security deposit or an itemized statement of any deductions.

Under California Civil Code § 1950.5, you were required to return the deposit within 21 days after I moved out. The 30-day period applies only if you sent a written explanation within those 21 days showing that a deduction could not reasonably be determined sooner. I received no such explanation.

Please return the full $2,400 by [date, e.g., October 28]. If you claim any deduction, send an itemized statement and supporting documentation by the same date. If I do not receive payment by then, I will pursue all remedies available under § 1950.5, including filing in small claims court and seeking statutory damages for bad-faith retention.

I would prefer to resolve this directly. Please reply to confirm when payment will be sent, and contact me at [phone/email] with any questions.

Sincerely,
[Your name]
[Mailing address]

---

Send a copy by certified mail too, and keep the email delivery confirmation. Statute: [Cal. Civ. Code § 1950.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1950.5).
````

## Gravitas's answer

````text
**One correction first:** California gives landlords **21 days**, not 30. Under Civil Code § 1950.5(h)(1), your deposit and itemized statement were due by **October 11** — you're already 10 days past due and don't need to wait until the 21st. The draft below cites the correct deadline and works whenever you send it.

One caveat: if they mailed the check and statement within 21 days, they may be compliant even if it arrived late. That's why the letter asks them to confirm the date and method.

---

**Subject:** Security deposit refund — [property address]

Dear [Landlord name],

I moved out of [property address] on September 20. I have not received my $2,400 security deposit or any itemized statement of deductions.

California Civil Code § 1950.5 required you to return the deposit, or send an itemized statement with receipts and photographs for any deductions, within 21 days of my move-out. That deadline was October 11, and it has passed.

Please send the full $2,400 to [forwarding address] within ten days of this email. If you are withholding any amount, send the itemized statement and the supporting documentation § 1950.5(h)(2) requires instead. If you already mailed something, please confirm the date and method, and resend it to the address above.

If I don't hear from you within ten days, I will pursue the remedies available under § 1950.5, including small claims court, where bad-faith retention can carry statutory damages of up to twice the deposit.

I would prefer to resolve this directly.

Sincerely,
[Your name]
[Phone] · [Email]

---

A few things that will matter if it goes further:

- **Send it two ways:** email and certified mail, return receipt. Keep the receipt and a copy of the letter.
- **Document the unit:** photos and video from move-out, plus any move-in inspection or checklist, undercut claimed deductions.
- **Small claims:** the filing limit is well above $4,800, so your doubled claim fits. [California Courts self-help](https://selfhelp.courts.ca.gov/small-claims-california) has the forms and filing fees.

The statute is [Civil Code § 1950.5](https://california.public.law/codes/civil_code_section_1950.5); the 21-day rule and the twice-the-deposit penalty are in subdivisions (h) and (m).
````

## How the graders voted

The answer key asked for the date to be corrected first (21 days under Civil Code 1950.5, so 11 October), a recommendation to send now rather than wait, and a short, polite, firm email: move-out date, deposit amount, the 21-day rule, a request for the deposit or an itemized statement by a set date, a forwarding address, and a measured mention that bad-faith retention can cost up to twice the deposit, with small claims as the next step.

The key cited the subsections by their older letters. After the runs I checked the current text: the 21-day rule is now (h)(1) and the twice-the-deposit damages are (m). I added that correction to the key before grading; the substance did not change.

| Grader | Verdict | Margin | Plain DSH: Correct / Trap / Honest / Useful / Concise | Gravitas: Correct / Trap / Honest / Useful / Concise |
|---|---|---|---|---|
| Claude Opus 5.5 | Gravitas | Clear | 6 / 8 / 6 / 8 / 9 | 10 / 10 / 9 / 10 / 8 |
| Claude Sonnet 5.5 | Gravitas | Decisive | 4 / 7 / 5 / 7 / 9 | 9 / 10 / 9 / 9 / 8 |

- Claude Opus 5.5 preferred Gravitas by a clear margin: it named 11 October, cited the current subsections and added a fair caveat about a cheque mailed in time. Plain DSH never gave the date and invented a 30-day rule.
- Claude Sonnet 5.5 preferred Gravitas decisively, for the invented rule above all: plain DSH put it in the email itself, where it weakens the demand and misstates the law to the landlord.

## What happened

### Plain DSH invented a rule

Plain DSH opened well: "California’s default deadline is **21 days**, not 30." Then it added that "A landlord gets up to 30 days only if it sends a written explanation within the first 21 days", and the email repeats it: "The 30-day period applies only if you sent a written explanation within those 21 days". I checked the current text of section 1950.5. There is no 30-day period in it. The nearest thing is (h)(3): when repairs cannot be finished within 21 days, the landlord may deduct a good-faith estimate and send the receipts within 14 days of the work. An email that tells the landlord there is a 30-day route invites the reply "then I have until 20 October", and it is wrong. Plain DSH also never said when the deadline was; it only said the tenant could send the email sooner "if you prefer".

### What Gravitas did

Gravitas gave the date (11 October), said the tenant was already 10 days past it and need not wait, and cited the current subsections. Its email asks for the money at a forwarding address within ten days, offers the itemized statement as the alternative, asks the landlord to confirm if something was already mailed, and names the twice-the-deposit damages without overdoing it. The notes after the email (send it two ways, keep move-out photos, small claims) are short and useful.

### Cost

Gravitas took about 104 seconds and about 144,000 tokens, with 11 web page reads. Plain DSH took about 97 seconds and about 118,000 tokens.
