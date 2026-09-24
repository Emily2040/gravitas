# Module 11 - Findings

## Purpose

This module covers findings that other people will act on: bug reports, audit results, code reviews, incident write-ups, research summaries, and anything published under a person's name. Load it when the deliverable leaves the conversation. The rules come from filing Antigravity bugs on `google-antigravity/antigravity-cli` in September 2026, where each one was learned by getting it wrong first.

## Before Writing Anything

1. Search for duplicates across the whole tracker, open and closed, by symptom and error text rather than by title. Issue #1062 was filed as new and turned out to describe the same defect as #794, which had been open since 14 August 2026 under a title about `--json-schema`. It was closed as a duplicate, and its evidence was posted to #794 as a comment instead.
2. Separate defects that share a symptom. The `--json-schema` report (#1064) first described one bug. It was two: an argument that is neither a readable file nor a JSON object is silently substituted as a string schema, and a schema whose root is not an object always fails because `properties` and `required` are emitted regardless. Both surface as the same API error. One report per mechanism, or one report that names both mechanisms and keeps their evidence apart.
3. Establish the mechanism with a controlled pair: the smallest change that turns a pass into a failure. `nosuchfile.json` produced the correct "failed to read schema file" error and `no such file.json` did not. The first draft then called spaces the cause. `not-json-at-all` contains no space and was also substituted, so the space was one route into the defect rather than its cause.

## Every Number From A Saved Run

1. Keep the harness as a file and re-run it for the report. The final #1064 table came from 14 arguments run 3 times each, 42 runs, with no case disagreeing with itself, and the script and raw results were kept.
2. Measure costs before stating them. A draft said each failing call "spends a request". The usage block read 0 tokens in every failing case, so the report says no tokens are billed and puts the cost where it is: in the diagnosis.
3. Recount before posting. A survey of affected conversations was quoted as 23 in one draft and was 32 by the time it was posted: 28 involving `command`, 2 `read_file` and 2 `mcp`. The posted comment also says it covers one machine on a single day.
4. A result that cannot be re-run from a saved script is an anecdote. Include it only if it is labelled as one.

## Checks Before Blaming The System

1. Rule out the instrument. A run that looked like a platform failure was the harness removing its own permission grants partway through.
2. Confirm why a pass passed. An injection test that appeared to show the agent resisting a planted instruction had in fact died on a denied `read_file`, so the payload was never read. `05-acceptance.md` covers this in general.
3. Re-run the control next to the case, on the same version, in the same session.

## Writing The Report

1. Follow the tracker's template exactly: version, environment, numbered steps to reproduce, expected behaviour, actual behaviour, logs.
2. Make the steps reproducible from a clean machine, with the fixture created in the steps themselves.
3. Put the evidence in a table: input, exit code, result. Tables carry detail better than paragraphs.
4. Label the cause section as a reading. Say what was not mapped, such as which arguments the resolver accepts as path-like.
5. Suggest a fix only where the evidence points at one, and number the suggestions.
6. State the scope: operating system, shell, versions, models, and what was not tested. For a defect about spaces in an argument, the fact that every run used PowerShell on Windows bounds the claim, and a maintainer will ask.
7. Link related issues and say how each one differs.
8. Keep it short. Real engineers filing bugs write 400 to 700 words. A 1,000-word report reads as generated whatever it contains.

## The Author Is The Person Who Signs It

A finding filed under someone's name is written in their voice, and they are its author. No assistant voice ("I have drafted", "as requested"), no description of how the report was produced, and first person only where the author would use it: "I searched the tracker for `only allowed for OBJECT type` and found nothing."

The first drafts of these reports read as obviously machine-written, although a banned-word scan had returned zero hits on them. The tell was structural: 14 to 21 em-dashes per 1,000 words, contrastive framing on nearly every paragraph, bold lead-ins on most bullets, and six reports built on one template. Rewritten to the standard in `12-prose.md`, they came down from about 1,050 words each to between 390 and 750.

Before posting, run `scripts/provenance_check.py` and `scripts/slopcheck.py` on the draft, read the author's own earlier reports on the same tracker, and match their conventions for headings, spelling and number format.

## Checklist

- Duplicate search done across open and closed issues, by symptom and error text.
- One mechanism per report, or each mechanism named with its own evidence.
- A controlled pair saved in the harness.
- Every figure traceable to a saved, re-runnable run, with runs and repetitions stated.
- Costs measured.
- The harness ruled out, and every pass explained.
- The cause labelled as a reading, with what was not mapped.
- Scope stated.
- Every evidence label checked with `provenance_check.py`.
- Written in the author's voice, measured with `slopcheck.py`.
