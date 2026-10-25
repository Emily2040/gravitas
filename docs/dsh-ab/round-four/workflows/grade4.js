export const meta = {
  name: 'round-four-blind-grading',
  description: 'Two Claude blind graders (Opus 5.5, Sonnet 5.5) per pair, one pair per session, against the key and its key points; the third judge (Codex) runs from judge_codex.sh',
  phases: [{ title: 'Grade', detail: 'one session per pair per grader' }],
}
// args: { pids: [...], packetDir: 'W:\\AgentData\\logs\\gravitas-dsh-ab4\\blind\\packets', graderPrompt: '<text of grader-prompt4.md>', graders: ['opus', 'sonnet'] }
const SIDE = {
  type: 'object',
  properties: {
    correct: { type: 'integer', minimum: 0, maximum: 10 },
    trap: { type: 'integer', minimum: 0, maximum: 10 },
    honest: { type: 'integer', minimum: 0, maximum: 10 },
    useful: { type: 'integer', minimum: 0, maximum: 10 },
    concise: { type: 'integer', minimum: 0, maximum: 10 },
    added_claim_errors: { type: 'array', items: { type: 'string' } },
    key_points: { type: 'object', additionalProperties: { type: 'string', enum: ['correct', 'vague', 'wrong', 'missing'] } },
  },
  required: ['correct', 'trap', 'honest', 'useful', 'concise', 'added_claim_errors', 'key_points'],
}
const GRADE = {
  type: 'object',
  properties: {
    pair: { type: 'string' },
    winner: { type: 'string', enum: ['A', 'B', 'tie'] },
    margin: { type: 'string', enum: ['slight', 'clear', 'decisive'] },
    A: SIDE,
    B: SIDE,
    reasons: { type: 'string' },
  },
  required: ['pair', 'winner', 'margin', 'A', 'B', 'reasons'],
}
// The grader prompt without trailing whitespace, then the frozen delivery lines. save_grades4.py rebuilds this exact
// string from grader-prompt4.md and refuses any row whose prompt or packet path differs (amendment 2026-10-25).
const graderPrompt = args.graderPrompt.replace(/\s+$/, '')
const packetPath = (pid) => `${args.packetDir}\\${pid}.md`
const prompt = (pid) => `${graderPrompt}

Packet file: ${packetPath(pid)}
Output: do not write any file. Return the JSON object described above through the StructuredOutput tool, with "pair" set to "${pid}". Do not open any other file in ${args.packetDir} or its parent folders, and do not look for other packets, runs, maps or grades.`
const graders = args.graders || ['opus', 'sonnet']
phase('Grade')
const jobs = args.pids.flatMap((pid) => graders.map((grader) => () =>
  agent(prompt(pid), { label: `grade:${pid}:${grader}`, phase: 'Grade', model: grader, schema: GRADE })
    .then((grade) => ({ pid, grader, grade, prompt: prompt(pid), packetPath: packetPath(pid) }))))
const results = await parallel(jobs)
const done = results.filter((r) => r && r.grade)
log(`${done.length} of ${jobs.length} grades returned`)
if (done.length < jobs.length) log(`missing: ${jobs.length - done.length} (save_grades4.py lists them; rerun only those pids)`)
return results.filter(Boolean)
