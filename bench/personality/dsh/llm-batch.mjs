// Batch model calls inside one DSH boot, for question drafting and judging.
// Each request is its own one-shot call (no shared history), through DSH's own
// signed-in provider route. Reads a JSONL of {id, system?, user, maxTokens?},
// appends {id, text, reasoningChars, usage, finish, error, ms} to `out`, skips ids
// already in `out` (so a cut run resumes), then exits the process.
import { readFileSync, existsSync, appendFileSync } from 'node:fs'

export const name = 'gravitas-llm-batch'
export const inject = ['llm']

function done(out) {
  const ids = new Set()
  if (!existsSync(out)) return ids
  for (const line of readFileSync(out, 'utf8').split('\n')) {
    if (!line.trim()) continue
    try { const r = JSON.parse(line); if (!r.error) ids.add(r.id) } catch {}
  }
  return ids
}

async function one(ctx, config, req) {
  const t0 = Date.now()
  const options = {
    provider: config.provider ?? 'deepseek-account',
    model: config.model ?? 'deepseek-flash',
    messages: [{ role: 'user', content: [{ type: 'text', text: req.user }] }],
    ...(req.system ? { system: req.system } : {}),
    ...(req.maxTokens ?? config.maxTokens ? { maxTokens: req.maxTokens ?? config.maxTokens } : {}),
    ...(config.temperature !== undefined ? { temperature: config.temperature } : {}),
    ...(config.reasoningEffort ? { reasoningEffort: config.reasoningEffort } : {}),
  }
  let text = '', reasoningChars = 0, usage = null, finish = null
  try {
    for await (const chunk of ctx.llm.stream(options)) {
      if (chunk.type === 'text-delta') text += chunk.text
      else if (chunk.type === 'reasoning-delta') reasoningChars += chunk.text.length
      else if (chunk.type === 'usage') usage = chunk.usage
      else if (chunk.type === 'finish') finish = chunk.reason
    }
  } catch (e) {
    return { id: req.id, error: String(e?.message ?? e), ms: Date.now() - t0 }
  }
  const failed = finish && typeof finish === 'object' && (finish.kind === 'error' || finish.kind === 'aborted')
  return {
    id: req.id, text, reasoningChars, usage, finish,
    ...(failed ? { error: finish.failure?.code ?? finish.kind } : {}),
    model: options.model, ms: Date.now() - t0,
  }
}

export function apply(ctx, config) {
  const timer = setTimeout(async () => {
    const reqs = readFileSync(config.in, 'utf8').split('\n').filter((l) => l.trim()).map((l) => JSON.parse(l))
    const skip = done(config.out)
    const todo = reqs.filter((r) => !skip.has(r.id))
    const limit = config.concurrency ?? 16
    let next = 0, failures = 0
    async function worker() {
      while (next < todo.length) {
        const req = todo[next++]
        let res = await one(ctx, config, req)
        for (let attempt = 1; res.error && attempt <= (config.retries ?? 2); attempt++) {
          await new Promise((r) => setTimeout(r, 2000 * attempt))
          res = await one(ctx, config, req)
        }
        if (res.error) failures++
        appendFileSync(config.out, JSON.stringify(res) + '\n')
      }
    }
    await Promise.all(Array.from({ length: Math.min(limit, todo.length) }, worker))
    appendFileSync(config.log ?? config.out + '.log', JSON.stringify({ at: new Date().toISOString(), requested: reqs.length, skipped: skip.size, ran: todo.length, failures }) + '\n')
    setTimeout(() => process.exit(failures ? 4 : 0), 300)
  }, config.delayMs ?? 3000)
  ctx.effect?.(() => () => clearTimeout(timer))
}
