# Module 12 - Prose

## Purpose

Every artifact this skill produces for a person goes through this module: reports, summaries, commit messages, documentation, pull request descriptions, release notes, bug reports and comments. Correct work that reads as machine-generated gets discarded before anyone evaluates it, and on a public tracker it costs the author credibility.

## Word Choice Is Not The Tell

A banned-word list catches nothing that matters. Text can contain no `delve`, `leverage` or `robust` and still read as unmistakably generated, because the signature is in the structure. These markers, roughly in order of how loudly they announce themselves, are what a reader notices.

| Marker | What It Looks Like | Target |
| :--- | :--- | :--- |
| Em-dash cadence | An em-dash in every second sentence | Zero. Use commas, full stops and parentheses |
| Contrastive framing | "Not X, it's Y", "This isn't a bug, it's a docs issue" | None as a habit |
| Uniform sentence length | Sentences clustered at 15 to 20 words | Standard deviation above 6, with real short sentences present |
| Bold lead-ins | Every list item opening with a bold phrase and a colon | Zero in prose lists |
| Hedge intensifiers | `precisely`, `genuinely`, `deliberately`, `notably`, `arguably`, `effectively`, `worth noting` | Zero |
| Meta-commentary | "Worth stating explicitly so it is not lost in a refactor" | Zero |
| Identical scaffolding | Several documents with the same headers in the same order | Each document shaped by its content |
| Rhetorical questions | A question immediately answered by the writer | Questions only when an answer is wanted |

The targets above are for text with no convention of its own to follow. When the text joins existing work (the author's own published writing, a document set, a repository's docs or changelog, but not text written earlier in this task), it reads as part of that work: follow what that work actually does with dashes, bold lead-ins, list form and sentence rhythm, even where it departs from these targets. An API reference whose entries open with a bold parameter name gets new entries in that form, and an author who writes with em-dashes keeps them. Without such work in front of you, the targets stand.

## Constructions That Read As A Second Writer

A reviewer comparing this skill's early drafts with the author's published repositories found about 20 sentences that were built for cadence rather than information. They clustered at the openings and closings of sections, which is where a careful reader notices a second writer. Each one had a plain replacement that said the fact it was standing in for.

| Construction | Example | Plain Version |
| :--- | :--- | :--- |
| Fragment runs for rhythm | "Thoroughly. It passes." | "It gets checked, it passes, and the work is reported as verified." |
| Two-word dramatic sentences | "Gemini sees." | Name what the tools can do: screenshots, console capture, network inspection |
| Free-standing maxims | "Repetition is not improvement." | "Repeating a pass does not reliably improve it." |
| Antithesis as punchline | "Word choice is not the tell. Structure is." | "The tell is structural rather than lexical." |
| Chiasmus | "Every claim carries a label, and the label carries its provenance." | "Every claim carries a tier label, and every label states what produced it." |
| Locative inversion | "Between that and a full pass lies most real work." | "Most real work sits between that gate and a full pass." |
| Anaphora | "What changes is X. What does not change is Y." | State Y as a fact |
| Epigram closers | "...and is the opposite." | End on the consequence |
| Three-beat templates | Three paragraphs that each end "X fixes this." | Vary the shape, or use a table |

## What To Do Instead

Open each section by stating what the thing is or does. Choose the form by the content: a table where several items share the same fields, a numbered list where order matters, a code block for commands and code the reader will run or copy, and prose everywhere else. End on a fact or a pointer to the file or command that goes further, never on a moral.

Steps, procedures and technical reports follow item 7 of the always-on rule: short sentences, one idea each, about 80% of the way to ASD-STE100, or in another language to that language's own plain technical style. Never lengthen one for variety. In all other prose, vary sentence length on purpose: short declaratives of 3 to 8 words next to compound sentences of 25 to 40. A short sentence carries a fact, such as "Load `01-evidence.md` first." It never carries a flourish.

Ground every abstraction in an observable mechanism. "The permission system is unreliable" says nothing. "Grants are stored as literal command text, so 175 accumulated and none ever re-matched" says the same thing and can be checked.

Make every declarative sentence falsifiable. If the opposite of the sentence would be absurd, the sentence is empty. "We provide scalable solutions" fails. "40,000 writes per second per node, 99th percentile under 12 ms, identical NVMe drives required, no multi-region replication" passes.

Write measured figures as numerals: 22 cases, 301 KB, 97.5%, 20,595 output tokens. Keep one form for every item in a list. Cut any word, sentence or section that can go without losing meaning.

## The Author Is The Person Who Signs It

When the output will be published, sent or filed under someone's name, it is written in their voice and they are the author. Read their existing work first and match its conventions: heading case, spelling (British or American), number format, punctuation (dashes included), list form, sentence rhythm, whether they use the first person, how they open and close sections, and how their repositories are laid out.

Leave out anything that reveals an assistant: "I have drafted", "as requested", "here is a version", descriptions of how the text was produced, and hedges the author would not write.

## Measure, Do Not Trust Your Ear

Structural tells are invisible from the inside. `scripts/slopcheck.py`, shipped with this skill, reports every em-dash and its rate per 1,000 words, sentence-length mean and standard deviation, short sentences, bold lead-ins, contrastive patterns, hedge intensifiers, conclusion crutches, rhetorical questions, banned vocabulary and any unclosed code fence.

```bash
python scripts/slopcheck.py <files>            # --strict exits 1 when anything is flagged
```

Targets: zero em-dashes, zero bold-lead bullets, a standard deviation above 6, a real count of sentences at 8 words or fewer, and no contrastive or hedge flags. For Chinese, Japanese or Korean text the script counts characters instead of words, so the targets become a standard deviation above 14 and a real count of sentences at 24 characters or fewer. It skips the contrastive, hedge, banned-word and crutch checks on that text and prints a note saying so. Questions inside quotation marks, blockquotes and code are skipped, but read each flag before acting on it. Em-dashes inside quotation marks are still counted, so a flag can point at a verbatim quotation of someone else's words; leave that quotation as recorded. A draft that passes the ear and fails the measurement is the normal case. In steps and procedures written to item 7, a low standard deviation is expected, so do not lengthen sentences to clear that flag. Where the text follows the conventions of existing work it joins, flags for the dashes, bold lead-ins or sentence rhythm that work uses are expected too; keep the convention.

`slopcheck.py` measures lines and sentences, so it cannot see repeated paragraph shapes or the constructions in the table above. `gravitas-prose-editor` reads for those, and a second reader who knows the author's work reads for the rest.

## Where This Does Not Apply

Code comments explaining a non-obvious mechanism should be plain and may be short. Log messages are not prose. Commit subject lines follow the repository's existing convention. Matching the surrounding code beats matching this module.
