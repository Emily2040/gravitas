> **语言说明：** 本参考文件目前仅有英文版。核心技能文件 `SKILL.md` 已完整中文化，这里是按需加载的深度细节。翻译进行中。

# Prose

Every artifact this skill produces goes through this: bug reports, summaries, commit messages, documentation, PR descriptions, release notes, code comments.

Correct work that reads as machine-generated gets discarded before it is evaluated. On a public tracker it costs the author credibility. The fix is not a vocabulary swap.

---

## Word choice is not the tell

A banned-word list catches nothing that matters. Text can contain zero instances of `delve`, `leverage` and `robust` and still read as unmistakably generated, because the signature lives in structure.

The real markers, in rough order of how loudly they announce themselves:

**Em-dash cadence.** Machine text runs an em-dash through every second sentence. Human technical writing uses commas, periods and parentheses. Target zero.

**Contrastive framing.** `Not X, it's Y`. `This isn't a bug, it's a docs issue`. One instance is a rhetorical choice. Every paragraph is a fingerprint.

**Uniform sentence length.** Generated prose clusters tightly around 15 to 20 words. Real writing varies hard: a three-word sentence lands, then a thirty-word one carries the argument. Aim for a standard deviation above 6, with genuine short anchors present.

**Bolded bullet leads.** Every list item opening with a bold phrase and a colon reads as template cadence rather than emphasis.

**Hedge intensifiers.** `precisely`, `genuinely`, `deliberately`, `notably`, `arguably`, `effectively`, `worth noting`, `worth stating`. They add length and no information.

**Meta-commentary.** `Worth stating explicitly so it is not disturbed by a fix`. `Noting this so it is not lost in a refactor`. Nobody writes that about their own bug report.

**Identical scaffolding.** Six documents with the same section headers in the same order reads as generated, because no human writes six of anything to one template.

**Rhetorical questions.** A question like `So what went wrong` followed immediately by its own answer. Ask a question only when you want one answered.

---

## What to do instead

**Vary sentence length on purpose.** Short anchors of three to eight words against compound sentences of twenty-five to forty. The rhythm is the point.

**Ground every abstraction.** An abstraction with no observable mechanism behind it is filler. "The permission system is unreliable" says nothing. "Grants are stored as literal command text, so 175 accumulated and none ever re-matched" says the same thing and can be checked.

**Pass the falsifiability test.** Every declarative sentence must assert something that could be wrong. If the opposite of your sentence would be absurd, the sentence is empty. "We provide scalable solutions" fails. "40,000 writes per second per node, 99th-percentile under 12ms, requires identical NVMe drives, no multi-region replication" passes.

**Cut anything removable.** If a word, sentence or section can go without subtracting meaning, it goes.

**Be terser than feels right.** Real engineers filing bugs write short. A 1,000-word bug report reads as generated regardless of content. 400 to 700 is the range where technical writing lands.

---

## Verify, do not trust your ear

Structural tells are invisible from the inside. Measure instead.

`scripts/slopcheck.py` in this repo reports em-dash density per 1000 words, sentence-length mean and standard deviation, short-anchor count, bold-lead ratio, contrastive patterns, hedge intensifiers, rhetorical questions and banned vocabulary.

```
python scripts/slopcheck.py <files>
```

Targets: zero em-dashes, zero bold-lead bullets, standard deviation above 6, a real count of sentences at eight words or fewer, and no contrastive or hedge flags.

Run it before delivering anything a human will read. A draft that passes the ear and fails the measurement is the normal case.

---

## Where this does not apply

Code comments explaining a non-obvious mechanism should be plain and may be short. Log messages are not prose. Commit subject lines follow the repository's existing convention, whatever it is. Matching the surrounding code beats matching this document.
