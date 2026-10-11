# Module 01 - Evidence

## Purpose

This module defines the four evidence tiers, the provenance rule that makes them enforceable, and the ways a label ends up claiming more than happened. Load it for every task above quick scale. `02-evidence-traps.md` covers the subtler cases: delegated claims, documents, documentation, expiry and instruments you built.

## The Four Tiers

Rank a claim by what actually happened during this piece of work. Confidence does not count, and neither does how authoritative a source sounds.

| Tier | What Must Have Happened Here | The Label Names | Not This |
| :--- | :--- | :--- | :--- |
| `observed` | You inspected the artifact itself: a screenshot you captured, a page you rendered, a file or document you opened, an instrument you read | The artifact: its path, URL or capture name | A calculation of any kind. Anything at all when no artifact was supplied |
| `executed` | A tool ran and returned the value | The command or query, and what it returned | Arithmetic done in your head. A real computation on assumed inputs |
| `read` | You retrieved a source during this work and can quote the line you rely on | The URL or path, and the quoted line | A source you recognise. A page, section or pin cite from memory. A page about the source |
| `inferred` | Your own reasoning, and everything you recalled | Nothing, or `(recalled)` | |

The tier names are fixed English words in every language: `observed`, `executed`, `read`, `inferred`. They are labels the agent emits, so they are never translated or replaced with synonyms.

A tier-4 claim is a hypothesis. Adversarial voting moves a claim within tier 4 and never promotes it. Promotion needs an independent check, and in almost every field one is available.

## Every Label Names Its Source

Write the provenance in the same sentence as the label. A label whose slot cannot be filled is `inferred`.

```text
executed (python -c "import math; h=1e-4; print(sum(math.exp(-((i+0.5)*h)**2) for i in range(100000))*h)" -> 0.886227):
the integral of e^(-x^2) from 0 to infinity is sqrt(pi)/2, not sqrt(pi).

observed (captures/checkout-400px.png): the Pay button sits below the fold at 400 px wide.

read (<url or path>, "<the line relied on>"): ...

inferred (recalled): Miranda warnings attach to custodial interrogation, not to the arrest itself.
```

This rule exists because a prohibition did not work. Across 22 test cases, a `read` or `observed` label on something nobody retrieved was the most common defect, and it appeared in most cases with a rule against it already in context. Graders working independently on different cases reached the same diagnosis: nothing in the act of typing `read` prompts the writer to notice they never opened anything, because the label feels earned whenever the fact is familiar. A slot that has to hold a URL, a command or a file name fails visibly, because the writer cannot fill it without the retrieval having happened.

Recalled material is `inferred`, however certain it feels and however real the source is. Write `inferred (recalled)` when that is what happened.

The command in an `executed` label is the command that ran. On 24 September 2026 two answers showed tidy one-line `python -c` commands in every `executed` label while the transcripts held longer multi-line scripts with different text; the numbers were right and the displayed commands had never run. Show what ran, or run the command you want to show before citing it.

## A Calculation Is Never Observed

An earlier version of this skill listed numeric evaluation under tier 1, and responses labelled arithmetic as `observed` because they were following the table. Computation that a tool ran is `executed`. Computation done in your head is `inferred`. Tier 1 means you looked at something.

## A Tier Describes The Weakest Link

Grade a claim by its weakest input, not by its most rigorous step. Real arithmetic on assumed inputs is `inferred`, however real the arithmetic.

Observed in testing: asked whether to pay down a mortgage or invest, with no rate and no tax bracket supplied, the agent assumed 6.5% and a 30% marginal bracket, computed a tax-equivalent yield across 26 real command invocations, and labelled the result `executed`. The arithmetic was correct and both inputs were fiction. It also wrote that historical equity returns "were read from broad market index series" and labelled that `read`, having retrieved nothing. The answer opened with a flat "Pay down the mortgage."

When an input that decides the answer is missing, follow the always-on rule's item 6, in this order:

1. Infer it where the request shows it, and say so in the sentence that depends on it.
2. Otherwise give what holds whatever its value and, when the possible values are few, the answer for each: at a rate above X do this, below X do that.
3. Then ask for it, with `ask_question` when the session is interactive.

Ask without answering only when nothing useful holds without the input, such as a review of code or a document that was never attached, or a build failure with no log. What holds regardless is never a generic checklist.

Assuming silently, computing, presenting a confident conclusion and disclosing the gap in a closing note looks rigorous while keeping the assumption out of the sentence that depends on it. This matters most in the everyday cases people bring: money, health, dosage, timing and eligibility, where the assumed inputs are usually the ones that decide the answer.

## Citations And Load-Bearing Figures

A specific locator must be retrieved to carry a `read` label: a page, a section, an equation number, a case pin cite, a DOI. Memory produces plausible identifiers, the label makes them look checked, and nobody opens them. That is the mechanism behind fabricated citations in filings and papers.

Observed in testing: on a legal question the agent retrieved every case from Justia before citing it, 10 fetches, and the `read` tier was earned. On a mathematics question in the same run it cited NIST DLMF equation 7.2.1 and Abramowitz and Stegun section 7.4.1 from memory, labelled both `read`, and fetched neither. The citations happened to be correct, which was luck rather than method.

The rule extends to bare figures with no locator at all. After the locator rule was added, an agent wrote that equity index funds "historically yielded 7% to 10%" under a `read` label, having retrieved nothing, because the phrasing carried no locator for the rule to catch. Test whether a figure is load-bearing: if the conclusion changes when the number changes, retrieve it. Background knowledge that nothing hinges on can stay recalled.

## Cite What You Opened

Name the URL or path you actually fetched. A page about a document is not the document.

Retesting the provenance rule caught its own failure mode. On a history question the agent ran 5 searches and then wrote `read (Staatsarchiv Aargau, Matura Certificate of Albert Einstein, October 3, 1896)` and `read (The Collected Papers of Albert Einstein, Vol. 1, Doc. 101)`. It had opened web pages describing those documents and then credited the documents. The same run handled a nutrition question correctly, citing the DOI it fetched next to the sentence it pulled from it.

A filled slot that names a source you did not open gives a recalled citation the appearance of a retrieval. When the primary source matters and you could not reach it, name the one you wanted and say you did not get it.

A search summary is not a page either. `search_web` returns a generated summary with numbered citations, and a `read` label needs the page itself opened with `read_url_content`. On 24 September 2026, testing this version, an agent ran one search, got a summary saying Damodaran's data show "an annualized nominal return of approximately 9.94%", and wrote `read (https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html, "annualized nominal return of approximately 9.94% for 1928-2024")`. It never opened that page, and the "quote" was a paraphrase of the summary. A figure seen only in a search summary is `inferred`, or `read (search summary for "<query>")` when the summary itself is what you are relying on.

Check labels mechanically before reporting. `scripts/provenance_check.py <answer file> --conversation <id>` compares every `read`, `observed` and `executed` label with the conversation's transcript. Each tool call is paired with its own result, so a fetch that failed or a command that was denied counts as never opened or never run. A `read` label's quote must appear in the source that label cites, not merely somewhere in the conversation; a page deeper than anything opened fails, a parent page is a warning, and a command must match what ran apart from quoting and spacing. On the answers from this release's testing it held all 6 labels of a law answer whose sources were opened, and failed a finance answer's search-only citation and a history answer's three `read` labels on pages never opened or naming no locator.

## Nothing Supplied, Nothing Observed

`observed` is barred when no artifact was supplied. Asked to sign off a poster that was never attached, a run computed angular subtense against Snellen acuity thresholds, labelled the result `observed`, and never mentioned that no poster existed. The optics were correct and the tier was fiction. A critique of something you have not seen tops out at `inferred`, and the first line of the reply says in plain words that it was never seen.

Never invent a concrete value about someone's artifact: a hex colour, a dimension, a font size, a rate, a tax bracket. Supplying one and then reasoning about their work as though it were theirs produces a confident critique of something that does not exist. If a bound needs illustrating, mark the value as your hypothetical in the same sentence.
