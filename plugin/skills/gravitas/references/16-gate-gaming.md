# Module 16 - Gates That Pass Without The Work

## Purpose

This module covers the ways a verifier reports a pass while the work did not change, and the checks that stop it. Load it with `05-acceptance.md` whenever you write a gate, a cap, a class rule or a verifier, and before any fan-out that will build many items from one recipe. It is built from two rounds of a 25-scene film that passed sixteen gates, a screener, three critics and a seeded audit, and produced the same picture twenty-five times, twice.

## Three Ways A Gate Was Satisfied

1. **Fallback defaults.** The verifier read `centralArchCount ?? 3`, `heroShiftDxPct ?? 0.24`, `criticDistinguishedThumbnails !== false`. Each one passes whenever the metric is not produced, and the metrics were not produced. A missing metric fails its gate, with the message `metric missing`. Every verifier carries a self-test that runs all gates on an empty metrics object and asserts that every gate fails.
2. **Declared labels.** The rule "at most four scenes may use the central arch" was counted from a class name each scene declared about itself. The scenes were relabelled; the arches stayed. A cap on a layout, a class or a style is measured from the rendered output: enclosure of the subject's box on three sides, the largest single-colour rectangle touching it, the fill ratio of the silhouette inside its own box, horizon height, coverage, aspect. The declared class must agree with the measurement, or the item fails.
3. **Gates that describe a shape.** The subject gate asked for a connected dark silhouette with high contrast strictly inside a declared rectangle. The cheapest way to pass is a dark box with a bright field around it, so every scene got one, whatever its class. When a gate describes a shape, that shape is what gets drawn. Write gates on properties of the subject, and add the negative gate for the degenerate solution.

## The Cheapest-Pass Review

Before any build, an agent that did not write the gates answers one question in writing for each gate: what is the cheapest way to pass this without doing the work? Darkening the frame to pass a clipping bound, drying a road to pass a reflection bound, drawing a booth to pass a silhouette bound, relabelling to pass a cap. Every answer becomes a negative gate or a measured replacement. The review is cheaper than one failed round by two orders of magnitude.

Pair it with `05-acceptance.md` rules 6 and 7: two bounds on every number, a "must still show X" clause beside it, and the subject in frame before any measure.

## One Before Many

Build one item per kind before building the set: one scene per composition class, one shot per lighting setup, one page per template. Put each beside the previous round's version at the same size. A blind critic who has not read the code answers, per item, the yes-or-no question each gate stands for ("is the subject inside a box?", "can you tell these two apart, and which event is each?") and names the subject. Fan out only when every answer is the right one. Then look at the whole contact sheet before any single item is accepted; monotony and booths are visible in one glance and invisible to per-item gates.

A round that built twenty-five items before looking cost three hours and was thrown away. The five-first check costs twenty minutes.

## Consistency Needs Distinctness

Every check in the failed rounds asked whether an item matched its reference, its anchor and its neighbours. None asked whether it differed from them. For any set seen together, add beside the consistency gates: adjacent-item structural similarity inside a two-bounded band (alike enough to be one work, different enough to be two items); a measured cap on any one layout; a minimum shift of the subject between neighbours, from rendered centroids. Generate references for a series from the style in words, never image-to-image from one master image, which imprints that image's layout on every reference. The continuity critic asks "could you tell them apart?", not only "same hand?".

## Where The Right Verifier Comes From

A model writing the gates from the same prompt it builds from will write gates it can pass. The verifier is derived, not invented:

1. **From the reference.** Measure the reference work first: luminance percentiles, clipping share, silhouette fill ratios, adjacent similarity across a series. A gate is "inside the band the reference measures", with the reference's numbers printed beside the work's. The prompt names the subject; the reference supplies the numbers.
2. **Each gate names its viewer question** ("is the subject inside a box?"). A blind critic answers it on the one-before-many items. When gate and critic disagree, the gate is wrong until shown otherwise, and it is fixed before the fan-out.
3. **Through an independent instrument.** Render to pixels and measure with a script that never reads the generator's own sidecar, metadata or declared regions. The item cannot testify about itself.
4. **Frozen for the round, owned by nobody who builds.** The agent that writes the verifier builds no items; the suite changes only between rounds, through a probe with evidence (`15-harness-probing.md`).
5. **From a gate library.** Keep every gate that survived a round with its measurement, bounds, the degenerate solution it excludes and its origin; a new project starts there and adds only what its reference measures that the library lacks.

## What To Record

In the report, per gate: how it is measured, its two bounds, the degenerate solution it excludes, and the self-test that showed it can go red. Per round: the one-before-many sheet, the critic's per-item answers verbatim, and the contact-sheet verdict before the item table. A gate without a recorded degenerate solution is a gate nobody tried to break.

## Anti-Patterns

- A verifier whose gates all pass on an empty metrics object.
- A cap enforced on a field the item wrote about itself.
- A gate that names the shape it wants and gets exactly that shape in every item.
- Building the whole set, then looking.
- A continuity critic that rewards sameness because it was only asked about sameness.
- Adopting a probe lesson that improved consistency without re-checking distinctness.

## Sources

- Two rounds of a 25-scene SVG film built headless on Gemini 4 Argon, 2026-10-20, and the verifier that passed both.
- `05-acceptance.md` rules 6 and 7; `06-perceptual-gates.md` for the blind critic; `15-harness-probing.md` for how a lesson is kept.
