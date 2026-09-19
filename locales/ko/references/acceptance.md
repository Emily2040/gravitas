> **언어 안내:** 이 참조 파일은 현재 영어만 제공됩니다. 핵심 `SKILL.md` 는 한국어로 번역되어 있습니다. 번역은 진행 중입니다.

# Acceptance

How to write a check that can actually fail, and why a screenshot is not verification until something looks at it.

This file exists because of a real failure. An agent built a Three.js scene, captured eight screenshots, wrote a `VERIFICATION.md` with eight gates, and reported `ALL TEST GATES PASSED SUCCESSFULLY`. The scene looked wrong to the user on first glance. Every finding below is drawn from that run.

---

## A gate that cannot fail is not a gate

The suite contained this:

```js
| **T12-R1** | Hero Chocolate Identity Persistence | **PASS** | Exactly 1 mesh; UUID ${uuids[0]} persists. |
```

`PASS` is a string literal in a template. The measured value is interpolated, the verdict is typed. There is no comparison, no threshold, no branch. Nine gates, nine hardcoded passes, zero conditional logic.

It also collected console errors:

```js
const consoleErrors = [];
page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
```

`consoleErrors` is never read again. Captured and discarded.

**Rules:**

1. Every gate compares a measured value against an expected one. If you cannot state the failing condition, you do not have a gate.
2. **Prove the gate can fail before trusting it.** Break the thing on purpose, run the suite, watch it go red, put it back. A suite that has never failed has never been tested.
3. The process exits non-zero when any gate fails. A suite that always exits 0 reports nothing.
4. Anything captured is either asserted on or deleted. Collecting console errors into an array nobody reads is worse than not collecting them, because the code looks like it checks.

---

## Screenshots are not verification

The same run captured eight PNGs and attached them to the report as evidence. Every gate they were attached to measured geometry: UUID persistence, mesh counts, gripper clearance at `Y = 1.084 m`, cycle boundary error under 0.1 mm.

All of it was true. The scene still looked wrong.

**Nothing ever asked whether the image looked right.** The screenshots were filed as artifacts proving a script ran, not as images to be judged.

This is the most seductive failure in the whole skill, because it produces a document full of numbers and passes, and it feels more rigorous than looking. It is not. It answers a different question.

**Two kinds of visual check. They do not substitute for each other.**

| | Geometric | Perceptual |
|---|---|---|
| Question | `Is the element present, positioned, sized` | `Does it look right` |
| Method | Script assertion on scene graph or DOM | A model looks at the image and judges |
| Catches | Missing node, wrong transform, count drift | Flat lighting, plastic materials, unreadable form |
| Cannot catch | Anything about appearance | Anything about exact values |

A perceptual check cannot be scripted. It requires passing the image to a fresh critic and asking a question about how it reads.

---

## Perceptual gates

For anything a person will look at, add gates that only a viewer can answer. Hand a fresh read-only critic the screenshot and the intent, and require specific answers.

Weak, because it invites agreement: `Does this look good`

Strong, because each answer is falsifiable:

- `Name the material each major surface reads as. The brief says copper, enamelled steel and brass. What do you actually see.`
- `Point to the chocolate. If you cannot find it in this image, say so.`
- `Is there a visible light direction. Name it. If the lighting reads as flat, say flat.`
- `List every surface with no texture, wear or variation.`
- `Would someone who has never read the brief recognise this as a chocolate factory. What do they see instead.`

Require the critic to answer as a viewer, without reading the source. A critic that has read the code will describe intent rather than the image.

The single most useful prompt is `what does this look like it is made of`. A scene of flat-shaded primitives answers `plastic blocks` no matter what the material config claims.

---

## Naming the target before building

The run's plan was excellent on specifics: `#941c33` raspberry enamel at roughness 0.20 with clearcoat 0.85, 3500 K halogen key at intensity 2.8, procedural tile grout. Those are real acceptance criteria.

None of them became a gate. The plan described appearance and the suite measured position.

**Every material and lighting specification in a plan is a perceptual gate waiting to be written.** If the plan says clearcoat 0.85, the gate asks whether surfaces read as lacquered. If it says 3500 K halogen key at a named position, the gate asks whether a viewer can identify the light direction and warmth.

Where a reference image exists, or can be made with `generate_image`, diff against it and list concrete differences in spacing, weight, proportion, colour and material read.

---

## Console output is a gate, not a log

The same scene requested `THREE.PCFSoftShadowMap`, removed in r186. The renderer fell back to hard shadows and said so:

```
THREE.WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead.
```

Nothing failed. Nothing crashed. Shadows were simply not what the plan asked for, and the run had console capture wired up and unread.

Deprecation warnings are the cheapest defect signal available and the easiest to leave collected-but-unchecked. Gate on them: a warning naming an API you called is a failure until triaged.

---

## When the native tools are missing

That run had no browser tools at all. Its whole toolset was `view_file`, `grep_search`, `list_dir`, `find_by_name`, `run_command`, `replace_file_content`, `write_to_file`, `schedule`, `manage_task`.

The agent built a Playwright harness through `run_command` and captured screenshots anyway. **That was the right move** and the skill should keep asking for it.

The harness was not the problem. What the harness checked was the problem.

So: check your toolset before planning verification. If `capture_browser_screenshot` is absent, build the harness. Then make sure the harness judges the image rather than only measuring the scene graph, or you have rebuilt the same blind spot at greater cost.

---

## Before reporting

- Every gate has a stated failing condition.
- At least one gate has been watched failing.
- Console output is asserted on. Nothing is merely collected.
- A fresh critic has looked at the rendered result and answered material, lighting and recognition questions.
- Anything the plan specified about appearance has a gate that asks whether it reads that way.
- The report states what was not covered.

A report of all-green with no gate ever demonstrated red is not evidence of correctness. It is evidence that a report was generated.

---

## A worked example that goes red

[examples/gates.example.js](../examples/gates.example.js) is a Playwright gate suite written to these rules and run against the scene described above. It scores 4 of 6 and exits 1.

```
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

G6 is the self-test the rules demand. It injects a wrong value and confirms the comparison catches it, so the suite has demonstrated it can go red.

The same scene, under the original suite, reported `ALL TEST GATES PASSED SUCCESSFULLY`.

Then the perceptual gate was run separately, by a fresh agent given the screenshot and no source. Its verdict on a chocolate factory:

> **Chocolate: Absent.** The mold cavities are completely white and empty; there is no liquid chocolate, bar, or brown confectionery substance visible anywhere on the line.
>
> **Lighting: Flat.** No directional cast shadows, no specular hot spots.
>
> **What it looks like it is made of:** injection-molded matte toy plastic and raw CAD primitives.

The original suite's gate on that same object read: *"Hero Chocolate Identity Persistence — PASS. Exactly 1 mesh throughout; UUID persists across all phases."*

The mesh exists in the scene graph. It is not visible in the render. **No geometric gate can close that gap**, which is the entire reason perceptual gates exist.
