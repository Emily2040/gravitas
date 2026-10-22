// Gravitas for DeepSeek Harness (DSH).
//
// Serves the same built files the Antigravity installers use (dist/<lang>/gravitas):
//   - the `gravitas` skill, with a DSH platform note appended when it loads;
//   - the always-on rule, as a global system-prompt section, with a short DSH tool note;
//   - the claim check: when a turn is about to close, the specifics the drafted answer
//     adds without support in the user's message or the turn's tool results are listed
//     back to the model once, and it revises the answer (lib/claims.js).
// The read-only inspector presets and the `gravitas_inspect` tool are rows in
// dsh/cordis.patch.yml; this file registers the skill, the rule and the check.
import { readFile, access, appendFile } from 'node:fs/promises'
import { randomUUID } from 'node:crypto'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import { createProvider } from './lib/provider.js'
import { checkDraft, steerLanguage, steerText } from './lib/claims.js'

/** Cordis plugin name; equals the row id in dsh/cordis.patch.yml. */
export const name = 'dsh-gravitas'

/** The skill registry and the system-prompt registry. */
export const inject = ['skills', 'systemPrompt']

export const LANGUAGES = ['en', 'zh-CN', 'ja', 'ko']

const ROOT = fileURLToPath(new URL('..', import.meta.url))
const DIST = path.join(ROOT, 'dist')
const HERE = fileURLToPath(new URL('.', import.meta.url))

/** Order of the rule section: after first-party guidance, before the deployment persona suffix (10200). */
export const RULE_ORDER = 10100

/** Pick a language: an explicit config value, else the system locale, else English. */
export function resolveLanguage(configured, locale = Intl.DateTimeFormat().resolvedOptions().locale) {
  if (configured && configured !== 'auto') {
    if (!LANGUAGES.includes(configured)) throw new Error(`dsh-gravitas: language must be auto, ${LANGUAGES.join(', ')}; got "${configured}"`)
    return configured
  }
  const tag = String(locale || '').toLowerCase()
  if (tag.startsWith('zh')) return 'zh-CN'
  if (tag.startsWith('ja')) return 'ja'
  if (tag.startsWith('ko')) return 'ko'
  return 'en'
}

/** Validate the row config. Unknown keys are refused so a typo cannot silently do nothing. */
export function readConfig(config = {}) {
  const allowed = new Set(['language', 'alwaysOnRule', 'claimCheck', 'ruleFile'])
  for (const key of Object.keys(config ?? {})) {
    if (!allowed.has(key)) throw new Error(`dsh-gravitas: unknown config key "${key}" (allowed: language, alwaysOnRule, claimCheck, ruleFile)`)
  }
  // Your own always-on rule in place of the built-in one, for example to try a variant side by side.
  const ruleFile = config?.ruleFile ?? null
  if (ruleFile !== null && (typeof ruleFile !== 'string' || !path.isAbsolute(ruleFile))) {
    throw new Error('dsh-gravitas: ruleFile must be an absolute path to a rule file')
  }
  const alwaysOnRule = config?.alwaysOnRule ?? true
  if (typeof alwaysOnRule !== 'boolean') throw new Error('dsh-gravitas: alwaysOnRule must be true or false')
  // Off by default: in round three of the DSH A/B the check made answers longer and graders
  // preferred the same rule without it (docs/dsh-ab/round-three).
  const claimCheck = config?.claimCheck ?? false
  if (typeof claimCheck !== 'boolean') throw new Error('dsh-gravitas: claimCheck must be true or false')
  return { language: resolveLanguage(config?.language ?? 'auto'), alwaysOnRule, claimCheck, ruleFile }
}

/** Source kind of the claim-check message in the session log (any non-empty kind other than "plugin"). */
export const CLAIM_CHECK_KIND = 'gravitas-claim-check'

const textOf = (content) => (content ?? []).filter((b) => b?.type === 'text').map((b) => b.text).join('')

/** Tools whose output is a computation (shell), that write files, or that read them. */
const SHELL_TOOL = /^(?:pwsh|bash|shell|powershell|terminal)/i
const WRITE_TOOL = /^(?:write|edit|str_replace|apply_patch|multi_edit)/i
const READ_TOOL = /^(?:read)/i

/** Today's date on this machine, as the time-context row tells the model. */
const localToday = () => new Date().toLocaleDateString('sv')

/**
 * The claim check. Collects each root session's turn (the person's message, every
 * tool result, the latest answer) and, when the turn is about to close, steers the
 * model once with the specifics its answer adds without support. Subagent sessions
 * are left alone. Any failure is logged and the turn closes as it would have.
 */
export function registerClaimCheck(ctx, language) {
  const states = new WeakMap()
  const stateFor = (session) => {
    let st = states.get(session)
    if (!st) states.set(session, (st = { turn: 0, request: [], sources: [], calls: new Map(), written: new Set(), draft: null, steeredTurn: 0 }))
    return st
  }
  const isChild = (session) => session?.header?.origin === 'subagent' || (session?.header?.delegationDepth ?? 0) > 0
  const pathOf = (args) => {
    try {
      const a = typeof args === 'string' ? JSON.parse(args) : args
      const p = a?.path ?? a?.file_path ?? a?.filePath ?? a?.file
      return typeof p === 'string' ? path.resolve(p).toLowerCase() : undefined
    } catch {
      return undefined
    }
  }

  // Runs inside Session.append: observe only, never steer from here.
  ctx.on('session/event', (session, event) => {
    try {
      if (isChild(session)) return
      const st = stateFor(session)
      switch (event.type) {
        case 'turn/start':
          Object.assign(st, { turn: event.data.turn, request: [], sources: [], calls: new Map(), written: new Set(), draft: null })
          break
        case 'user/message': {
          // The person's prompt follows turn/start inside the turn. A subagent's report is the
          // model's own writing, so it is not evidence.
          if (event.data?.source?.kind !== 'user') break
          const text = textOf(event.data?.content)
          st.request.push(text)
          st.lastRequest = text
          break
        }
        case 'tool/call': {
          const { callId, name, arguments: args } = event.data ?? {}
          st.calls.set(callId, { name: String(name ?? ''), args: typeof args === 'string' ? args : JSON.stringify(args ?? '') })
          if (WRITE_TOOL.test(name ?? '')) {
            const p = pathOf(args)
            if (p) st.written.add(p)
          }
          break
        }
        case 'tool/result': {
          if (event.surfaceOp !== undefined && event.surfaceOp !== 'append') break
          const message = event.data?.message
          if (message?.isError) break
          const call = st.calls.get(message?.toolCallId) ?? { name: '', args: '' }
          const text = textOf(message?.content)
          if (SHELL_TOOL.test(call.name)) st.sources.push({ text, kind: 'shell', command: call.args, tool: call.name })
          else if (READ_TOOL.test(call.name) && st.written.has(pathOf(call.args))) break // a file the model wrote this turn
          else st.sources.push({ text, kind: 'tool', tool: call.name })
          break
        }
        case 'assistant/message': {
          const text = textOf(event.data?.message?.content)
          if (text.trim()) st.draft = { turn: event.data.turn, text }
          break
        }
      }
    } catch (error) {
      ctx.logger?.warn?.(`dsh-gravitas: claim check collector: ${String(error)}`)
    }
  })

  // Optional diagnostics for measuring the check: GRAVITAS_CLAIM_LOG names a JSON-lines file.
  const log = async (record) => {
    const file = process.env.GRAVITAS_CLAIM_LOG
    if (!file) return
    try {
      await appendFile(file, JSON.stringify({ time: new Date().toISOString(), ...record }) + '\n', 'utf8')
    } catch (error) {
      ctx.logger?.warn?.(`dsh-gravitas: claim check log: ${String(error)}`)
    }
  }
  const summary = (flagged) => flagged.map((it) => ({ cls: it.status === 'miscalculated' ? 'calculation' : it.cls, raw: it.raw, key: it.key }))

  ctx.on('agent/turn-stopping', async ({ agent, turn, signal }) => {
    try {
      const session = agent?.session
      if (!session || isChild(session) || signal?.aborted) return
      const st = states.get(session)
      if (!st || st.turn !== turn || !st.draft || st.draft.turn !== turn) return
      const request = st.request.length ? st.request.join('\n') : st.lastRequest ?? ''
      const { flagged, counts, items } = checkDraft({ draft: st.draft.text, request, sources: st.sources, today: localToday() })
      if (st.steeredTurn === turn) {
        // turn-stopping fires again after the revision; check once per turn, and record what became
        // of each listed item: gone, now supported (and by which tool), or still without support.
        if (!st.revisionLogged) {
          st.revisionLogged = true
          const outcome = (st.listed ?? []).map((l) => {
            const now = items.find((it) => it.key === l.key)
            return { ...l, now: now ? now.status : 'absent', source: now?.source }
          })
          await log({ session: session.id, turn, phase: 'revision', counts, flagged: summary(flagged), outcome, text: st.draft.text })
        }
        return
      }
      const text = steerText(flagged, steerLanguage(request, language))
      await log({ session: session.id, turn, phase: 'draft', steered: !!text, counts, flagged: summary(flagged), text: st.draft.text, sources: st.sources.length })
      if (!text) return
      st.steeredTurn = turn
      st.revisionLogged = false
      st.listed = summary(flagged)
      agent.steer({
        id: randomUUID(),
        role: 'user',
        content: [{ type: 'text', text }],
        source: { kind: CLAIM_CHECK_KIND, form: 'notice', summary: `Gravitas: ${flagged.length} unsupported specifics` },
      })
    } catch (error) {
      ctx.logger?.warn?.(`dsh-gravitas: claim check: ${String(error)}`)
    }
  })
}

export function pathsFor(language) {
  const base = path.join(DIST, language, 'gravitas')
  return {
    skills: path.join(base, 'skills'),
    rule: path.join(base, 'rules', 'AGENTS.md'),
    agents: path.join(base, 'agents'),
    platform: path.join(HERE, 'platform', `${language}.md`),
    ruleNote: path.join(HERE, 'platform', `${language}.rule.md`),
  }
}

/** The platform note appended to the skill, with the agents folder filled in. */
export async function platformNote(language) {
  const p = pathsFor(language)
  const text = await readFile(p.platform, 'utf8')
  return text.replaceAll('AGENTS_DIR', p.agents + path.sep)
}

/** The always-on rule plus the short DSH tool note, as one prompt section text. */
export async function ruleText(language, ruleFile = null) {
  const p = pathsFor(language)
  const [rule, note] = await Promise.all([readFile(ruleFile ?? p.rule, 'utf8'), readFile(p.ruleNote, 'utf8')])
  return `${rule.trimEnd()}\n\n${note.trim()}\n`
}

export async function apply(ctx, config) {
  const { language, alwaysOnRule, claimCheck, ruleFile } = readConfig(config)
  const p = pathsFor(language)
  await access(p.skills)
  const provider = createProvider({
    providerName: name,
    skillsDir: p.skills,
    appendix: (skill) => (skill === 'gravitas' ? platformNote(language) : ''),
    logger: ctx.logger,
  })
  ctx.skills.registerProvider(() => provider)
  if (alwaysOnRule) {
    const text = await ruleText(language, ruleFile)
    ctx.effect(() => ctx.systemPrompt.section({ name: 'gravitas:always-on-rule', order: RULE_ORDER, text, interpolate: false }))
  }
  if (claimCheck) registerClaimCheck(ctx, language)
}
