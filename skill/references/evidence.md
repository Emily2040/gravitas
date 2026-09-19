# Evidence

What counts as observation outside software, and the trap that catches every domain.

---

## The proxy trap

When the real question is hard to check and an adjacent question is easy to check, the easy one gets checked instead. It gets checked thoroughly. It passes. The result is reported as verified.

This is the single most common way careful-looking work is wrong, and it is not a coding problem. It happens wherever verification is possible in principle and inconvenient in practice.

| The question that matters | The proxy that gets checked instead |
|---|---|
| Does this scene look like a chocolate factory? | Are there 10 carriers and 6 rollers? |
| Does this contract create the obligation I claim? | Does the document contain the word *indemnify*? |
| Is this proof correct? | Is every line syntactically well-formed? |
| Is this physical answer right? | Do the units cancel? |
| Does this study support the claim? | Does the cited paper exist? |
| Is this translation faithful? | Is the output grammatical? |
| Is this financial model sound? | Does the spreadsheet compute without errors? |
| Is this historical account accurate? | Are there footnotes? |

Every proxy on the right is necessary. None is sufficient. Each one produces a clean pass while the real property fails, which is exactly why it is seductive: it yields a document full of green checks and a feeling of rigour.

**The test for a proxy:** establish whether the check can pass while the thing you actually care about is false. If it can, you are holding a proxy. Keep it, and add the real check beside it.

A real case: a run verified that a 3D scene contained exactly one chocolate mesh whose UUID persisted across every animation phase. True. An independent viewer given the rendered image reported the chocolate as **absent**, because the mesh was never visible. Both statements were correct. The count was a proxy for visibility, and nothing in the suite noticed the difference.

---

## What observation means in your domain

Tier 1 of the evidence hierarchy is *you looked at the thing itself*. What "the thing itself" is changes by domain. What does not change is that it must be independent of the reasoning that produced the claim.

**Software and rendered artifacts.** Run it, look at it, read its console and its traffic. Covered in [verification.md](./verification.md).

**Mathematics.** A proof read line by line is tier 3. Tier 1 is evaluating the statement numerically at random points, testing boundary cases (zero, one, empty, negative, infinite), checking limits and asymptotics, verifying by a second independent method, and actively trying to build a counterexample. A closed form that disagrees with a numeric evaluation at a single point is dead, regardless of how clean the derivation reads.

**Physics and engineering.** Dimensional analysis first, since it is free and catches a large fraction of errors. Then order of magnitude, comparing the answer against something you already know and expecting it within a factor of ten. Then limiting cases, where the formula must collapse to a known result as a variable goes to zero or infinity. Then conservation laws. An energy that grows without bound, a velocity above `c`, a length longer than the apparatus: each is observable without trusting the derivation.

**Law.** Pull the operative text. Quote the words that create the duty, not the headnote and not a summary. Confirm the authority exists, is in force, has not been overruled, repealed or superseded, and applies in the relevant jurisdiction on the relevant date. Distinguish holding from dicta. A citation that resolves to a real case is a proxy for a citation that says what you claim it says.

**Empirical and factual claims.** Reach the primary source, not a summary of it. Check that the number in the source is the number being repeated, that the population or scope matches the claim being made, and that the source has not been superseded. A figure that has passed through three secondary sources is tier 3 at best and often tier 4 wearing a citation.

**Statistics and data.** Recompute independently from the raw figures. Reconcile totals. Compare against base rates before accepting that an effect is large. Check the denominator, which is where most misleading percentages live.

**Medicine and any applied evidence.** Check that the study population resembles the case at hand, that effect size is clinically meaningful and not merely significant, and that the finding has replicated. Prefer a systematic review to a single trial, and prefer the trial to a press release about the trial.

**Finance and quantitative work.** Recompute the arithmetic by a second route. Confirm the statements reconcile. Sanity-check growth rates against history, since a model that compounds a plausible rate for thirty years produces implausible numbers.

**Craft and taste work: colour, editing, writing, design.** These have no single right answer, so the loop rules differ and the proxy trap changes shape. Every craft has a **checkable layer** and a **judgeable layer**, and conflating them is how work ships looking wrong.

The checkable layer is real and often objectively violable in ways a measurement settles: broadcast-legal levels and gamut, clipped highlights or crushed shadows, colour space and transfer tags, audio sync across the full duration rather than at the head, frame rate conform, aspect ratio, continuity of names and facts inside a narrative, word count against a spec. These are tier 1 and 2. Measure them.

The judgeable layer is whether it reads, whether it lands, whether it looks like the thing it claims to be. **No metric reaches it.** A grade can sit perfectly inside legal range and still read as muddy. A cut can land on every beat and still have no rhythm. A paragraph can hit its word count in clean active voice with no adverbs and say nothing at all.

The craft-specific danger is that the checkable layer is necessary, which makes passing it feel like verification. Legal scopes are required. Sync is required. Neither is evidence that the work is good, and a report that lists only the measurable results has answered a different question.

For the judgeable layer, use a fresh critic twice. **First without the brief:** what does this read as, what is it about, what mood does it carry. A viewer who has not been told the intent describes what is actually there. **Then with the brief:** does it deliver that intent, and where specifically does it fall short. Running only the second pass invites the critic to confirm the intent it was just handed.

Taste judgments are tier 3 at best and usually tier 4. Label them. A strong opinion from a competent critic is still an opinion, and the honest report says so while still giving the opinion, because refusing to judge is its own failure.

**Web design and interface work.** The checkable layer is unusually rich here, which makes it unusually dangerous. Contrast ratios, touch target size, heading order, alt text presence, keyboard focus visibility, layout at each breakpoint, and no horizontal scroll are all measurable. An automated audit will report them and produce a score.

That score is the proxy. Automated accessibility tools catch roughly a third of WCAG violations, and around half by issue volume depending on how you count. The rest is not machine-testable even in principle, because the criteria require judgement: whether a heading describes the section beneath it, whether link text means anything out of context, whether reading order matches visual order, whether an error message tells someone what to do. Alt text being present is measurable. Alt text being useful is not.

A page can score 100 on Lighthouse and be unusable. The layer no audit reaches is whether a first-time visitor finds the primary action, whether the hierarchy reads, whether the interface looks trustworthy. Check those with a viewer given the page and no explanation of it.

**History and interpretation.** Go to the document, not the account of it. Establish provenance and date. Note who benefited from the account surviving. Much of this domain sits at tier 3, and saying so is the honest move.

---

## A citation you did not open is `inferred`

The `read` tier means a source was consulted. Recalling that a textbook says something is not consulting it, and recalling a specific locator is the dangerous version: a page, a section, an equation number, a case pin cite, a DOI.

Memory produces plausible identifiers. The tier label then makes the claim look checked, and nobody opens it. That is the whole mechanism behind fabricated citations in filings and papers, and it is not exotic. It happens when a model is confident and the locator is the kind of thing it has seen a thousand times.

Observed in testing: on a legal question the agent retrieved every case from Justia before citing it, ten fetches, and the `read` tier was earned. On a mathematics question it cited NIST DLMF equation 7.2.1 and Abramowitz and Stegun section 7.4.1 from memory, labelled both `read`, and fetched neither. The citation happened to be correct. That is luck rather than method, and the two runs were inconsistent because nothing told it which one was right.

**The rule.** A specific locator must be retrieved to be labelled `read`. If you did not open it, either fetch it or drop the locator and label the claim `inferred`. A source named without false precision and marked as recalled is honest. A pin cite from memory wearing a `read` label is a fabricated citation that has not been caught yet.

**The rule extends to bare figures, and this is the part that slips.** A number attributed to no locator at all still implies a source: "historically yielded 7% to 10%", "roughly a third of cases", "about 40 grams". Testing caught exactly this. After the locator rule was added, an agent stopped inventing user inputs and still wrote that equity index funds "historically yielded 7% to 10%" under a `read` label, having retrieved nothing, because the phrasing carried no locator for the rule to catch.

Apply the test of whether the figure is **load-bearing**. If the conclusion changes when the number changes, retrieve it. Background knowledge that nothing hinges on can stay recalled and unlabelled. The equity range was the pivot of the entire recommendation, so it needed a source.

---

## A tier describes the weakest link, not the computation

Real arithmetic on invented inputs is not `executed`. The calculation ran, which makes the label feel earned, and the label then transfers the credibility of the arithmetic to the assumption underneath it.

Observed in testing. Asked whether to pay down a mortgage or invest, with no rate and no tax bracket supplied, the agent assumed 6.5% and a 30% marginal bracket, computed a tax-equivalent yield across twenty-six real command invocations, and labelled the result `executed`. The arithmetic was correct. Both inputs were fiction. It also wrote that historical equity returns "were read from broad market index series" and labelled that `read`, having retrieved nothing at all.

The answer opened with a flat "Pay down the mortgage."

**The rule.** Grade a claim by its weakest input, not its most rigorous step. A computation whose inputs were assumed is `inferred`, however real the computation. When a required input is missing, you have three honest moves and one dishonest one:

1. Ask for it.
2. Give the answer as a function of it: at a rate above X do this, below X do that.
3. State the assumption **in the answer**, in the sentence that depends on it.

The dishonest move is to assume it silently, compute, present a confident conclusion, and disclose the missing inputs in a closing note. That reads as rigour and is the opposite. A gap declared after the conclusion does not travel with the conclusion when someone quotes it.

This matters most in exactly the everyday cases people bring: money, health, dosage, timing, eligibility. The inputs that got assumed are usually the ones that decide the answer.

---

## Deriving the split for a domain not listed here

The list above is not exhaustive and does not need to be. Architecture, cooking, music production, teaching, translation, photography, UX research: the same three questions build the split for any of them.

1. **What can a machine measure here?** That is the checkable layer, tier 1 and 2. Measure it, because it is cheap and it is necessary.
2. **What can only a competent judge decide?** That is the judgeable layer, tier 3 and 4. It needs a critic, and the verdict stays labelled as judgement.
3. **Which metric will feel like verification?** Name it explicitly before you start. It is almost always something real, necessary and satisfying to report, which is exactly what makes it the trap.

A domain where step 3 has no answer is a domain where verification is easy and you were never at risk. Every field that produces work people argue about has one.

---

## The unifying move

In every domain above, the instruction is the same. **Find the check that does not route through your own reasoning.**

Numeric evaluation does not care how elegant the derivation was. The statute text does not care what you remember it saying. A dimensional analysis does not care how confident the argument felt. That independence is the whole value. It is why running the code beats reading the code, and it is why the same principle carries to law and physics without modification.

Before accepting that a claim cannot be checked, ask what a cheap harness would look like. One numeric evaluation. One pull of the actual statute. One order-of-magnitude comparison. One search for the primary source. These cost minutes and settle questions that agents otherwise debate at length and resolve incorrectly.

---

## When nothing is observable

Some claims have no independent check available at all. Interpretive questions, contested law, ethics, prediction, judgments about intent. This is a much larger share of work outside software, so the handling matters more.

1. Take independent opinions with **distinct lenses**, not repeated opinions with the same lens. Three agents asking the same question share one blind spot.
2. State the claim as a hypothesis and label its tier.
3. **Name what would change your mind.** A claim that no possible evidence could falsify is not a finding, it is a position. Saying so is more useful than defending it.
4. Give the strongest version of the opposing reading before concluding. If you cannot state it well, you have not understood the question.
5. Report the disagreement. Averaging two incompatible readings produces a third that nobody holds. Two well-argued incompatible readings is the real answer when that is the situation.

---

## Calibrate to the question

Most questions do not need any of this. A definition, a date, a unit conversion, a quick explanation: answer it and move on. This machinery is for work where being wrong is expensive, where the answer will be relied on, or where the claim will outlive the conversation.

Escalate on consequence. Topic difficulty is a poor signal for it. A simple factual claim that will end up in a filing, a diagnosis, a published paper or a contract deserves the primary source. A hard theoretical question asked out of curiosity does not need a five-agent adversarial pass.
