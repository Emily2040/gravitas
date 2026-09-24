# Module 03 - Domain Checks

## Purpose

This module covers what counts as an independent check in each field, and the proxy trap that catches every field. Load it when a claim sits outside software, or when the check that would settle a claim is not obvious.

## The Proxy Trap

When the real question is hard to check and an adjacent question is easy to check, the easy one gets checked instead, it passes, and the work is reported as verified. This is the most common way careful-looking work turns out wrong, and it happens wherever verification is possible in principle and inconvenient in practice.

| The Question That Matters | The Proxy That Gets Checked |
| :--- | :--- |
| Does this scene look like a chocolate factory? | Are there 10 carriers and 6 rollers? |
| Does this contract create the obligation I claim? | Does the document contain the word *indemnify*? |
| Is this proof correct? | Is every line well-formed? |
| Is this physical answer right? | Do the units cancel? |
| Does this study support the claim? | Does the cited paper exist? |
| Is this translation faithful? | Is the output grammatical? |
| Is this financial model sound? | Does the spreadsheet compute without errors? |
| Is this historical account accurate? | Are there footnotes? |
| Is this page usable by someone with a screen reader? | Does Lighthouse report 100 for accessibility? |
| Does this platform feature work? | Does the documentation describe it? |

Every check on the right is necessary and none is sufficient: each one can pass while the property on the left fails. That is what makes them attractive, because they produce a document full of green results.

The test for a proxy is whether the check can pass while the thing you care about is false. If it can, keep it and add the real check beside it.

A measured case: a run confirmed that a 3D scene held exactly one chocolate mesh whose UUID persisted across every animation phase. An independent viewer given the rendered image reported the chocolate absent, because the mesh was never visible. Both reports were correct. The mesh count stood in for visibility, and no check in the run caught the substitution.

## What Observation Means In Each Field

Tier 1 is looking at the thing itself, and what the thing itself is changes by field. What does not change is that it must be independent of the reasoning that produced the claim. Software and rendered artifacts are covered in `04-runtime-verification.md`.

### Mathematics

A proof read line by line is tier 3. Tier 1 is evaluating the statement numerically at random points, testing boundary cases (zero, one, empty, negative, infinite), checking limits and asymptotics, verifying by a second independent method, and trying to build a counterexample. A closed form that disagrees with a numeric evaluation at a single point is dead, however clean the derivation reads.

### Physics And Engineering

Start with dimensional analysis, because it is free and catches a large fraction of errors. Then check order of magnitude against something already known, expecting agreement within a factor of 10. Then limiting cases, where the formula must collapse to a known result as a variable goes to zero or infinity. Then conservation laws. An energy that grows without bound, a velocity above `c` or a length longer than the apparatus is observable without trusting the derivation.

### Law

Pull the operative text and quote the words that create the duty, not the headnote and not a summary. Confirm the authority exists, is in force, has not been overruled, repealed or superseded, and applies in the relevant jurisdiction on the relevant date. Separate holding from dicta. A citation that resolves to a real case is a proxy for a citation that says what you claim it says.

### Empirical And Factual Claims

Reach the primary source rather than a summary of it. Check that the number in the source is the number being repeated, that the population or scope matches the claim, and that nothing newer supersedes it. A figure that has passed through three secondary sources is tier 3 at best and often tier 4 wearing a citation.

### Statistics And Data

Recompute from the raw figures. Reconcile totals. Compare against base rates before accepting that an effect is large, and check the denominator, which is where most misleading percentages live.

### Medicine And Applied Evidence

Check that the study population resembles the case at hand, that the effect size is clinically meaningful and not merely significant, and that the finding has replicated. Prefer a systematic review to a single trial, and the trial to a press release about the trial. Dosage, interaction and eligibility answers depend on inputs such as weight, renal function and current medication; when those are missing, the answer is given as a function of them or not given.

### Finance And Quantitative Work

Recompute the arithmetic by a second route. Confirm the statements reconcile. Sanity-check growth rates against history, since a model that compounds a plausible rate for 30 years can produce an implausible number: 7% a year for 30 years is a multiple of 7.61, not 3.

### Translation

Back-translate independently and compare what the two versions mean. Check that terms of art, units, dates, names and numbers survive exactly. A grammatical, fluent output is the proxy; a faithful one is the target.

### Craft: Colour, Editing, Writing, Design

These have no single right answer, so the loop rules differ and the proxy trap changes shape. Every craft has a checkable layer and a judgeable layer, and conflating them is how work ships looking wrong.

The checkable layer is real and often objectively violable: broadcast-legal levels and gamut, clipped highlights or crushed shadows, colour space and transfer tags, audio sync across the full duration rather than at the head, frame rate conform, aspect ratio, continuity of names and facts inside a narrative, word count against a spec. These are tier 1 and 2. Measure them.

The judgeable layer is whether the work reads, whether it lands, and whether it looks like the thing it claims to be. No metric reaches it. A grade can sit inside legal range and read as muddy. A cut can land on every beat and have no rhythm. A paragraph can hit its word count in clean active voice with no adverbs and say nothing.

The checkable layer is necessary, which makes passing it feel like verification. For the judgeable layer, use a fresh critic twice. First without the brief: what does this read as, what is it about, what mood does it carry. Then with the brief: does it deliver the intent, and where does it fall short. Running only the second pass invites the critic to confirm the intent it was just handed.

Taste judgements are tier 3 at best and usually tier 4. Label them and still give them, because refusing to judge is its own failure.

### Web Design And Interfaces

The checkable layer here is unusually rich: contrast ratios, target size, heading order, alt text presence, keyboard focus visibility, layout at each breakpoint, no horizontal scroll. An automated audit reports them and produces a score, and that score is the proxy. In a 2017 government test, 13 automated tools found between 13% and 40% of 142 deliberate barriers (read: https://alphagov.github.io/accessibility-tool-audit/), and a tool vendor's study of over 2,000 audits counted 57% of issues by volume (read: https://www.deque.com/blog/automated-testing-study-identifies-57-percent-of-digital-accessibility-issues/). The rest need judgement: whether a heading describes the section beneath it, whether link text means anything out of context, whether reading order matches visual order, whether an error message says what to do. Alt text being present is measurable and alt text being useful is not.

A page can score 100 on Lighthouse and still be unusable. Check whether a first-time visitor finds the primary action, whether the hierarchy reads and whether the interface looks trustworthy, using a viewer who is given the page and no explanation of it.

### History And Interpretation

Go to the document rather than an account of it. Establish provenance and date, and note who benefited from the account surviving. Much of this field sits at tier 3, and the honest report says so.

## Deriving The Split For A New Field

The list above is not exhaustive. Architecture, cooking, music production, teaching, photography and UX research all yield to the same three questions.

1. What can a machine measure here? That is the checkable layer, tiers 1 and 2. Measure it, because it is cheap and necessary.
2. What can only a competent judge decide? That is the judgeable layer, tiers 3 and 4. It needs a critic, and the verdict stays labelled as judgement.
3. Which metric will feel like verification? Name it before you start. It is almost always something real, necessary and satisfying to report, which is what makes it the trap.

If the third question has no answer, verification in that field is easy and the proxy trap does not apply.

Before declaring something uncheckable, ask what a cheap harness would look like: one numeric evaluation, one pull of the statute, one order-of-magnitude comparison, one search for the primary source. These take minutes and settle questions that agents otherwise debate at length and resolve incorrectly. Numeric evaluation does not care how elegant the derivation was, and the statute text does not care what you remember it saying, which is why the same principle carries from code to law to physics unchanged.
