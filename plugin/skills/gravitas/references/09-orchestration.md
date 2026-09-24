# Module 09 - Orchestration

## Purpose

This module covers how to structure a fan-out: when to wait for results and when not to, which pattern fits which situation, and how to keep counts and deduplication exact with the ledger. Load it at standard scale and above. Each pattern states the problem it solves, its structure, and the failure it prevents, and the patterns compose freely.

The patterns are field-neutral. A finder hunts one dimension of defect across a work list, and the work list can be files, statutes, papers or ledger lines. A multi-modal sweep searches by several angles at once, which in a codebase means by directory, call graph and rendered output, and in a literature review means by citation graph, keyword, author and failed replications.

## Choosing A Pattern

| Situation | Pattern |
| :--- | :--- |
| An independent check exists | Observe-first verification, in `04-runtime-verification.md` |
| Unknown how many issues exist | Loop until dry |
| One search angle will miss things | Multi-modal sweep |
| The solution space is wide | Judge panel |
| A finding could be plausible and wrong | Adversarial refute |
| A finding could be wrong in several ways | Perspective-diverse verify |
| Something may have been missed | Completeness critic |
| Cost per item varies widely | Staged escalation |
| Hundreds of items with exact counts | Scripted orchestration, in `13-platform.md` |
| A fix must be driven to green | Convergent loop, in `10-iteration.md` |
| Output needs polish rather than correction | Gradient loop, in `10-iteration.md` |

## Scout First, Then One Fan-Out Per Phase

Discover the work list with your own tools first: list the files, run the search, pull the index of the statute, read the table of contents. Then fan out over what you found. Multi-phase work runs as a sequence of fan-outs, one per phase (understand, design, implement, review), with the parent reading each result before planning the next. One enormous fan-out planned at the start commits to a work list written before anything was learned.

## Pipeline By Default

Verify each finding as soon as it exists. A finder that returns early should have its findings in front of a refuter while slower finders are still working.

Wait for the whole set only when the next step needs all of it at once: deduplication across every finder's results before expensive verification, an early exit when the total is zero, or a step whose prompt compares findings with each other. Flattening, filtering and reformatting do not need a wait; do them per item. When five finders run and the slowest takes three times as long as the fastest, a wait that nothing needed leaves the fast results idle for two thirds of the run.

## The Ledger

Counting, deduplication and vote tallies are bookkeeping, and bookkeeping belongs in code. A model tracking forty findings across three rounds in its head loses count, re-verifies findings it already rejected, and stops a loop early or late. `scripts/ledger.py` keeps that state in a JSON file and makes the decisions deterministic. It needs Python 3.8 or later and nothing else.

Run it by its full path inside the installed plugin, `<home>/.gemini/config/plugins/gravitas/skills/gravitas/scripts/ledger.py`, and keep the ledger file in the workspace or the artifact directory so it survives the run. The examples below shorten the path.

```bash
python scripts/ledger.py init  run.ledger.json --scale full
python scripts/ledger.py add   run.ledger.json finder-security.json --round 1 --by gravitas-finder
python scripts/ledger.py verdict run.ledger.json <key> --by gravitas-refuter --refuted no \
    --tier executed --source "pytest tests/test_session.py::test_logout -> 1 failed"
python scripts/ledger.py verdicts run.ledger.json refuter-verdicts.json --by gravitas-refuter
python scripts/ledger.py child run.ledger.json --id <conversation-id> --agent gravitas-finder --status denied \
    --note "read_file denied on src/auth"
python scripts/ledger.py close-round run.ledger.json --round 1
python scripts/ledger.py report run.ledger.json
```

What it enforces:

- A record whose tier is `observed`, `executed` or `read` and whose `source` is empty is demoted to `inferred`, and so is a `read` record whose source quotes no content: it needs a quotation of three words or twelve characters, and a quoted path is not one. Records are checked against the finding and verdict schemas, and a malformed one is rejected with the reason. The provenance rule in `01-evidence.md` becomes a check the ledger runs on every record.
- New records are deduplicated against every record ever added, including ones the refuters rejected. Deduplicating only against survivors lets rejected findings return every round, and the loop never converges.
- Two records at the same location merge automatically when their claims share at least 0.25 of their words, and are flagged as possible duplicates from 0.10. Records in the same file within 5 lines of each other merge only when their wording is near-identical (0.8), and are otherwise flagged, because distinct defects a few lines apart are often described alike. On one real audit, true duplicates scored 0.13 to 0.69 and distinct defects on the same line 0.02 to 0.15; the automatic merge took 22 records to 15 with no wrong merge. Decide the flagged ones with `ledger.py merge KEEP DUP`, which moves the votes across.
- A finding survives only with a majority of counted votes that did not refute it, and the number required follows the scale: 1 at standard, 3 at full and exhaustive. Votes are held to the same provenance rule as findings; a demoted vote or one with status `blocked` is recorded but not counted. Quick scale takes no votes, so its report lists findings as unverified.
- `close-round` counts the fresh findings, advances the dry counter, and prints `CONTINUE` or `STOP` with the reason: dry rounds reached, or the round ceiling reached.
- `report` lists survivors by severity with tier and source, then refuted, pending and demoted records, then every child whose status is not `done` and every finder that returned `blocked`, then the caps.

The ledger file also survives a lost final turn, so keep it where the user can find it. If Python is not available, keep the same fields in a table in the plan artifact, apply the same rules by hand, and say in the report that the ledger was kept manually.

## Loop Until Dry

Use it when you do not know how many issues exist: bugs, security findings, dead code, edge cases, contradictions in a document set. Send a round of finders, add their records to the ledger, verify the fresh ones, and close the round. Stop after the number of consecutive dry rounds the scale sets. It prevents fixed-count loops that stop mid-tail, reporting the easy findings and missing the rest.

## Multi-Modal Sweep

One search angle cannot see everything, and what it misses depends on the angle, so run several at once. Finders search by directory, by symbol, by call graph, by recent churn, by test coverage, by error string, and by rendered output. The visual angle matters most on this platform: a sweep of every route with captures finds defects that no text search can express a query for, because the defect is a rendering outcome rather than a string. It prevents the single-angle blind spot, such as a search for a function name that never finds the dynamic dispatch that calls it.

## Judge Panel

When the solution space is wide, the first plausible answer is rarely the best one. Generate several independent attempts from different starting positions: simplest thing that works, risk first, performance first, user first. Score them with fresh judges who authored none of them. Build from the winner and graft the strongest ideas from the others. It prevents one-attempt-then-polish, which locks in the first framing and iterates inside it.

## Adversarial Refute

Send each finding to independent refuters told to refute it and to default to refuted when uncertain. Kill it if a majority refutes. At full scale, use 3 refuters. "Refute this" invites scrutiny, where "is this correct" invites agreement. It prevents plausible but wrong findings from surviving on the strength of their prose.

## Perspective-Diverse Verify

When a finding can be wrong in more than one way, give each verifier a different lens instead of sending identical refuters: correctness, security, performance, does it reproduce. Require a majority. Three agents asking the same question share one blind spot and call it consensus.

## Completeness Critic

Run it before every report. `gravitas-completeness-critic` reads the ledger and the work list and answers one question: what is missing. Which angle was never searched, which claim never verified, which file never opened, which state never exercised, which route never rendered, which child failed. What it names becomes the next round. It prevents confident partial answers, which is the most common way a thorough-looking audit turns out wrong.

## Staged Escalation

When most items are cheap and a few are expensive, paying the expensive price everywhere wastes most of the budget. Run a `flash_lite` pass over everything and promote only what trips a signal. Log both counts, because a promotion rate near zero or near one means the signal is miscalibrated rather than the work being uniform.

## Anti-Patterns

- Fanning out over a guessed work list.
- Waiting for every finder before verifying anything, when nothing downstream compares findings.
- Confirmation-framed verification that asks whether something is correct.
- Deduplicating against survivors instead of everything seen.
- Silent caps: sampling, top-N or early stopping that the report does not state.
- Reasoning about a running system from its source when it could be looked at.
