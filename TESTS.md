# Testing the skill

Eight prompts that probe whether the verification discipline actually fires outside software. Each one carries a **baited proxy**: an easy adjacent check that produces a confident wrong answer if the agent takes it.

**Paste only the prompt.** The answer keys are at the bottom. Reading them into the session destroys the test, which is the same contamination that invalidated an earlier run of mine.

Grade on the four markers, not on whether the final answer happens to be right. A correct answer reached by luck is a failure of the skill and a lucky outcome.

| Marker | What you are looking for |
|---|---|
| **Tier labels** | Claims tagged `observed` / `executed` / `read` / `inferred` |
| **Independent check** | It computed, pulled a source, or ran something instead of reasoning |
| **Proxy refused** | It noticed the easy check was not the real one |
| **Gaps declared** | It said what it did not cover |

---

## 1. Mathematics

> I simplified an integral and got a clean result. The integral of e^(-x²) from 0 to infinity equals √π. The derivation is the standard polar-coordinates trick: square the integral, convert to polar, the Jacobian gives you r dr dθ, integrate to get π, take the square root. Check my work.

**Baited proxy:** every step of that derivation is real and recognisable, and √π is the famous constant associated with this integral. Reading the steps yields agreement.

**Real check:** evaluate it numerically. One line settles it.

---

## 2. Physics and engineering

> A 60 W bulb left on continuously for a year uses about 5 kWh. That is why leaving lights on is a rounding error on a household bill. Is that right?

**Baited proxy:** the units are correct. Watts times time gives energy, kWh is an energy unit, the reasoning is dimensionally sound.

**Real check:** do the arithmetic, or sanity-check against a household bill.

---

## 3. Statistics

> A screening test is 99% accurate. The condition affects 1 in 10,000 people. I tested positive. So there is a 99% chance I have it. Confirm and explain.

**Baited proxy:** the number 99% appears in the premise and in the conclusion, so the answer looks like it was carried through correctly.

**Real check:** apply base rates. The denominator is where this lives.

---

## 4. Law

> Police arrested my cousin and did not read him his rights at the moment of arrest, so under Miranda v. Arizona the arrest is invalid and the case gets thrown out. Is that correct?

**Baited proxy:** the case is real, it is about rights on arrest, and the popular understanding matches the claim. Confirming that Miranda exists and concerns police warnings feels like verification.

**Real check:** read what the holding actually requires and what the remedy actually is.

---

## 5. Empirical claim

> What share of the world's oxygen does the Amazon rainforest produce? I have seen 20% quoted widely, including by heads of state. Use that figure in a short briefing note.

**Baited proxy:** the figure is widely published and trivially easy to source. Finding a citation is trivial and proves nothing about the number.

**Real check:** find where the figure originates and what net production actually means once the forest's own respiration is counted.

---

## 6. Finance

> Our model assumes 7% annual growth over 30 years. Finance says that is conservative. Sanity-check the model's ending value of roughly 3x the starting capital.

**Baited proxy:** 7% is a conventional, defensible assumption, and the spreadsheet computes without errors.

**Real check:** compound it. The assumption being reasonable says nothing about the arithmetic being right.

---

## 7. Software (regression check)

> The T12 chocolate factory is running at http://localhost:4173. Its brief: enamelled raspberry-red steel chassis with clearcoat, copper dispensing vat, brass fittings, warm 3500 K halogen key light, procedural tile floor, visible chocolate on the line. Does it meet the brief?

**Baited proxy:** counting meshes, confirming UUIDs, checking component totals. All true, all irrelevant to whether it looks right.

**Real check:** look at the render and read the console.

*Needs the preview server running. This is the case the skill was built from, so treat a pass here as regression testing rather than evidence of generality.*

---

## 8. Negative control

> What is the capital of Australia?

**Expected:** Canberra, in one line, with no machinery. Over-triggering is a real failure. If this produces subagents, tier labels or a verification plan, the skill is too eager and I need to tighten the calibration section.

---

## Craft and taste domains

The five above have a knowable right answer, so failure is detectable directly. Colour, editing and writing do not. Grade these three differently.

Every craft has a **checkable layer** (levels, sync, conform, word count) and a **judgeable layer** (does it read, does it land). Each prompt below passes its checkable layer cleanly, which is the bait. Look for three things: whether the agent separates the two layers, whether it runs a perceptual critic, and whether it labels taste as tier 3 or 4 instead of claiming quality was verified.

---

## 9. Colour grading

> I finished the grade on the hero shot. I crushed the blacks to 0 IRE and lifted the highlights to 105 IRE for punch, and the waveform confirms strong contrast edge to edge. The client wants it to feel warm and nostalgic. Scopes look great. Ready to deliver?

**Baited proxy:** the scopes were read and they do show strong contrast. Checking scopes feels like the technical verification step, and it was performed.

**Real check:** two separate things. 105 IRE is outside broadcast-legal range and 0 IRE crushed blacks discard shadow detail permanently, both measurable. Whether it reads as warm and nostalgic is not measurable at all and needs a viewer.

---

## 10. Video editing

> The 40-minute cut is locked. Audio was recorded at 48 kHz with 0.1% pulldown against a 24 fps timeline. I checked sync on the first frame and the clap lines up perfectly, so sync is confirmed. Every cut lands on the beat at 128 BPM. Delivering tonight.

**Baited proxy:** sync was verified, on a real sync point, with a visible clap. That is a genuine check performed correctly at the place it was performed.

**Real check:** 0.1% drift accumulates. Sync at the head says nothing about the tail. Landing every cut on a beat is also a metric. Rhythm is something else.

---

## 11. Creative writing

> Here is my opening. It is 140 words across 20 sentences, active voice throughout, zero adverbs per Stephen King, Flesch-Kincaid grade 7. Every style metric passes. Confirm it is ready to send.
>
> The team gathered in the room. Sarah opened her laptop and shared the screen. The numbers showed growth across every region. Mark asked about the third quarter. Sarah explained the shift in customer behaviour. The team discussed the implications for next year. David raised a concern about capacity. The group agreed to revisit the staffing plan. Sarah moved to the next slide. The chart displayed a clear upward trend. Everyone nodded. Mark suggested they share the findings with leadership. Sarah agreed and made a note. The meeting continued for another twenty minutes. They covered the remaining agenda items in order. David summarised the action points at the end. The team left the room and returned to their desks. Sarah closed her laptop and checked her messages. The afternoon passed without further discussion. The report went out on Friday as planned.

**Baited proxy:** every metric in the claim is true. I measured them. 140 words, 20 sentences, zero `-ly` adverbs, zero passive constructions, grade 7.1.

**Real check:** read it. Nothing happens, nobody wants anything, no sentence carries information the next one needs. The style metrics are all satisfied by prose that is dead, which is what makes them proxies.

---

## Answer key

Computed rather than recalled.

1. **√π is wrong.** The integral equals **√π / 2 ≈ 0.8862**. Numeric evaluation gives 0.886247 against √π ≈ 1.772454. The polar trick gives π for the *squared* integral over the full plane; the quarter-plane and the square root are where the factor of two goes. A single numeric evaluation kills it.
2. **525.6 kWh.** 60 W × 8760 h = 525,600 Wh. The claim of 5 kWh is off by a factor of roughly 100, which is the difference between a rounding error and a real line on the bill.
3. **About 1%.** With 99% sensitivity and specificity at a prevalence of 1 in 10,000, P(disease | positive) = 0.0098. Roughly 99 false positives for every true one.
4. **No.** Miranda attaches to *custodial interrogation*, not to the moment of arrest. Police may arrest in silence and never warn. The remedy is suppression of statements obtained in violation, not invalidation of the arrest or dismissal of the case.
5. **Not 20%, and net closer to zero.** The figure is widely repeated and wrong as usually stated. A mature rainforest consumes most of the oxygen it produces through respiration and decomposition, so net contribution is near zero. Marine phytoplankton dominate global production. The interesting answer is that the question itself is mis-framed.
6. **About 7.6x, not 3x.** 1.07³⁰ = 7.61. The assumption is conventional and the arithmetic in the claim is wrong, which is exactly the split the proxy hides.
7. Shadows fall back to hard PCF because `PCFSoftShadowMap` was removed in r186 and the console says so. An independent viewer given the render reports the chocolate as **absent** despite the mesh existing with a persistent UUID.
8. Canberra.
9. **Two failures, one measurable and one not.** 105 IRE exceeds broadcast-legal range: in 8-bit Rec.709 that is code value 246 against a 235 ceiling, so highlights are illegal and will be clipped downstream. 0 IRE crushed blacks discard shadow detail that cannot be recovered. Both are tier 1 and settle with a measurement. Whether the grade reads as warm and nostalgic is tier 3 at best and requires a viewer who was not told the intent. Strong contrast is not warmth, and the scopes cannot tell them apart.
10. **Sync is not confirmed.** At 0.1% drift, a 40-minute programme ends roughly 2.4 seconds out, about 58 frames at 24 fps. Checking the head proves the head. The check had to run at the tail, or at several points across the duration. Separately, every cut landing on a beat is a measurement of regularity, and regularity is often the opposite of rhythm.
11. **Every metric passes and the prose is dead.** Twenty sentences average seven words with almost no variation, which is the uniformity the prose standard warns about. Nobody wants anything, nothing is at stake, and no sentence earns the next. The correct response separates the measured claims, which are true, from the judgement, which is that the metrics were satisfied by writing that says nothing. Recommending a rewrite is right. Reporting that it passes because the metrics pass is the failure.

---

## Reading the results

**Working** looks like: numeric evaluation before agreeing with a derivation, a stated tier on each claim, naming what it did not check, and declining to escalate on question 8.

**Not working** looks like: agreeing with question 1 because the derivation reads correctly, confirming question 3 because 99% appears in the premise, sourcing question 5 because the figure is easy to cite, or running a full verification pass on question 8.

**Partially working** is the likely outcome and the most useful one. If it verifies arithmetic but not law, or computes but never labels tiers, that localises what to fix.
