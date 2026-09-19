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

**History and interpretation.** Go to the document, not the account of it. Establish provenance and date. Note who benefited from the account surviving. Much of this domain sits at tier 3, and saying so is the honest move.

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
