// Gravitas for DeepSeek Harness (DSH).
//
// Serves the same built files the Antigravity installers use (dist/<lang>/gravitas):
//   - the `gravitas` skill, with a DSH platform note appended when it loads;
//   - the always-on rule, as a global system-prompt section, with a short DSH tool note.
// The read-only inspector presets and the `gravitas_inspect` tool are rows in
// dsh/cordis.patch.yml; this file only registers the skill and the rule.
import { readFile, access } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import { createProvider } from './lib/provider.js'

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
  const allowed = new Set(['language', 'alwaysOnRule'])
  for (const key of Object.keys(config ?? {})) {
    if (!allowed.has(key)) throw new Error(`dsh-gravitas: unknown config key "${key}" (allowed: language, alwaysOnRule)`)
  }
  const alwaysOnRule = config?.alwaysOnRule ?? true
  if (typeof alwaysOnRule !== 'boolean') throw new Error('dsh-gravitas: alwaysOnRule must be true or false')
  return { language: resolveLanguage(config?.language ?? 'auto'), alwaysOnRule }
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
export async function ruleText(language) {
  const p = pathsFor(language)
  const [rule, note] = await Promise.all([readFile(p.rule, 'utf8'), readFile(p.ruleNote, 'utf8')])
  return `${rule.trimEnd()}\n\n${note.trim()}\n`
}

export async function apply(ctx, config) {
  const { language, alwaysOnRule } = readConfig(config)
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
    const text = await ruleText(language)
    ctx.effect(() => ctx.systemPrompt.section({ name: 'gravitas:always-on-rule', order: RULE_ORDER, text, interpolate: false }))
  }
}
