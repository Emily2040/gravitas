# Module 06 - Perceptual Gates

## Purpose

This module covers checks that only a viewer can answer, for anything a person will look at: scenes, pages, charts, generated images, laid-out documents. Load it with `05-acceptance.md` whenever the work has a visual result. The case it is built from is the chocolate factory described there.

## Screenshots Are Not Verification

The chocolate factory run attached 8 PNGs to its report. Every gate they supported measured geometry: UUID persistence, mesh counts, gripper clearance at `Y = 1.084 m`, cycle boundary error under 0.1 mm. All of it was true, and the scene still looked wrong. Nothing asked whether the image looked right. The screenshots were filed as proof that a script ran, not as images to be judged.

This failure is seductive because it produces a document full of numbers and passes, and it feels more rigorous than looking. It answers a different question.

| | Geometric | Perceptual |
| :--- | :--- | :--- |
| Question | Is the element present, positioned and sized | Does it look right |
| Method | Script assertion on the scene graph or DOM | A model looks at the image and judges |
| Catches | Missing nodes, wrong transforms, count drift | Flat lighting, plastic materials, unreadable form |
| Cannot catch | Anything about appearance | Anything about exact values |

A perceptual check cannot be scripted. It needs the image in front of a fresh critic and a question about how it reads.

## Perceptual Gates

For anything a person will look at, add gates only a viewer can answer. Give `gravitas-visual-critic` the capture and the intent, and require specific answers.

"Does this look good" invites agreement. These invite answers that can be wrong:

- Name the material each major surface reads as. The brief says copper, enamelled steel and brass. What do you see?
- Point to the chocolate. If you cannot find it in this image, say so.
- Is there a visible light direction? Name it. If the lighting reads as flat, say flat.
- List every surface with no texture, wear or variation.
- Would someone who has never read the brief recognise this as a chocolate factory? What do they see instead?

The critic answers as a viewer and does not read the source, because a critic that has read the code describes intent rather than the image. The most useful single prompt is "what does this look like it is made of". A scene of flat-shaded primitives answers "plastic blocks" whatever the material configuration claims.

## Naming The Target Before Building

The run's plan was specific: `#941c33` raspberry enamel at roughness 0.20 with clearcoat 0.85, a 3500 K halogen key at intensity 2.8, procedural tile grout. Those are real acceptance criteria and none of them became a gate. The plan described appearance and the suite measured position.

Every material and lighting specification in a plan is a perceptual gate waiting to be written. If the plan says clearcoat 0.85, a gate asks whether surfaces read as lacquered. If it names a 3500 K key at a position, a gate asks whether a viewer can identify the light direction and its warmth.

## Console Output Is A Gate

The same scene requested `THREE.PCFSoftShadowMap`, which was removed in r186. The renderer fell back to hard shadows and said so in the console:

```text
THREE.WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead.
```

Nothing failed or crashed. The shadows were not what the plan asked for, and the run had console capture wired up and unread. Deprecation warnings are the cheapest defect signal available. A warning naming an API the code calls is a failure until someone triages it.

## A Worked Example That Goes Red

`examples/gates.example.js` is a Playwright gate suite written to these rules and run against the scene described above. It scores 4 of 6 and exits 1.

```text
PASS  G1  Zero console errors
FAIL  G2  No deprecation warning for an API this code calls
          THREE.WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead.
FAIL  G3  Shadow map enabled and not the hard fallback (type !== 1)
          enabled=true type=1
PASS  G4  Under 90% of materials are untextured
          153/193 materials have no map (79.3%)
PASS  G5  Component counts match the brief
PASS  G6  SELF-TEST: an injected wrong value is detected by G5 logic
```

G6 is the self-test the rules require: it injects a wrong value and confirms the comparison catches it, so the suite has shown it can go red. Under the original suite, the same scene reported `ALL TEST GATES PASSED SUCCESSFULLY`.

The perceptual gate was then run separately, by a fresh agent given the screenshot and no source:

> **Chocolate: Absent.** The mold cavities are completely white and empty; there is no liquid chocolate, bar, or brown confectionery substance visible anywhere on the line.
>
> **Lighting: Flat.** No directional cast shadows, no specular hot spots.
>
> **What it looks like it is made of:** injection-molded matte toy plastic and raw CAD primitives.

The original suite's gate on that object read: "Hero Chocolate Identity Persistence - PASS. Exactly 1 mesh throughout; UUID persists across all phases." The mesh exists in the scene graph and is not visible in the render. No geometric gate can close that gap, which is why perceptual gates exist.
