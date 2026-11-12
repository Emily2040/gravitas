export const meta = {
  name: 'round-four-blind-labels',
  description: 'Two relabellers (Sonnet 5.5, Opus 5.5) label every added-claim note from all three judges against the key, in shuffled batches with no side shown',
  phases: [{ title: 'Relabel', detail: 'one session per batch per relabeller' }],
}
// args: { batches: [{file, case, key, notes: [{id, note}]}] }  (relabel-batches.json from build_notes4.py)
const LABELS = {
  type: 'object',
  properties: {
    labels: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'integer' },
          label: { type: 'string', enum: ['wrong', 'unverified', 'not an error'] },
          cite: { type: 'string' },
        },
        required: ['id', 'label', 'cite'],
      },
    },
  },
  required: ['labels'],
}
const relabelPrompt = (b) => `You label notes that blind graders wrote about claims in answers to one request. You do not know which assistant wrote any answer, and the notes are shuffled. The request, key and notes may be in Chinese, English, Japanese or Korean. For each note, decide whether the claim it describes is:
- "wrong": the claim is false. You must cite the key line that contradicts it, or an official page you opened (give the URL); otherwise use "unverified".
- "unverified": the claim may be true but neither the key nor an official source you checked confirms it.
- "not an error": the claim is right, or the note is not about a claim (a style remark, a note that says the claim is correct, a duplicate of a point the key accepts).
Judge the claim the note describes, not the grader's opinion of it. You may open official web pages. Return one label per note id through the StructuredOutput tool; every id below must appear exactly once. Leave "cite" empty only when the label is not "wrong".

## Answer key (case ${b.case})

${b.key}

## Notes

${b.notes.map((n) => `- id ${n.id}: ${n.note}`).join('\n')}`
phase('Relabel')
const res = await parallel(args.batches.flatMap((b) => ['sonnet', 'opus'].map((model) => () =>
  agent(relabelPrompt(b), { label: `relabel:${b.file}:${model}`, phase: 'Relabel', model, schema: LABELS })
    .then((r) => ({ file: b.file, case: b.case, model, labels: r ? r.labels : null })))))
const missing = res.filter((r) => !r || !r.labels).length
log(`${res.length - missing} of ${res.length} batches labelled`)
return res.filter(Boolean)
