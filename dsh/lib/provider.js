// Skill provider for DeepSeek Harness (DSH) plugin packages.
//
// Serves every `skills/<name>/SKILL.md` inside a package as a bundled skill:
// the catalog gets the name and description from the frontmatter, and a load
// returns the body with the skill's own folder as its resource base, so the
// model reads `references/` and runs `scripts/` from there on demand.
//
// No dependencies: DSH loads linked and git-installed plugins from their own
// folder, where `@deepseek-ai/*` packages do not resolve. Keep it that way.

import { readFile, readdir, stat } from 'node:fs/promises'
import path from 'node:path'

/** Rank DSH gives bundled skills (`BUNDLED_SKILL_RANK` in @deepseek-ai/dsh-skill 0.2.1-rc.2). */
export const BUNDLED_SKILL_RANK = 600

const SKILL_NAME = /^[a-z0-9]+(?:-[a-z0-9]+)*$/
const BOOLEAN_WORDS = new Map([
  ['true', true], ['yes', true], ['on', true], ['1', true],
  ['false', false], ['no', false], ['off', false], ['0', false],
])

/**
 * Split a SKILL.md file into its frontmatter fields and body.
 * Accepts the subset of YAML these skills use: one `key: value` per line,
 * values plain, single-quoted or double-quoted. Anything else throws, so a
 * malformed skill fails in the tests instead of silently in a session.
 */
export function parseSkillFile(raw, file = 'SKILL.md') {
  const text = raw.replace(/^﻿/, '').replace(/\r\n/g, '\n')
  if (!text.startsWith('---\n')) throw new Error(`${file}: missing frontmatter`)
  const end = text.indexOf('\n---\n', 4)
  if (end < 0) throw new Error(`${file}: frontmatter is not closed`)
  const fields = {}
  let nested = null // a top-level key with an empty value holds an indented block (for example metadata:)
  for (const line of text.slice(4, end).split('\n')) {
    if (line.trim() === '' || line.trimStart().startsWith('#')) continue
    if (/^[ \t]/.test(line)) {
      if (!nested) throw new Error(`${file}: indented line outside a block: ${line}`)
      const m = /^[ \t]+([A-Za-z][\w-]*):[ \t]*(.*)$/.exec(line)
      if (!m) throw new Error(`${file}: unsupported frontmatter line: ${line}`)
      fields[nested][m[1]] = unquote(m[2].trim(), file)
      continue
    }
    const m = /^([A-Za-z][\w-]*):[ \t]*(.*)$/.exec(line)
    if (!m) throw new Error(`${file}: unsupported frontmatter line: ${line}`)
    const [, key, rawValue] = m
    if (Object.hasOwn(fields, key)) throw new Error(`${file}: duplicate key ${key}`)
    if (rawValue.trim() === '') { fields[key] = {}; nested = key; continue }
    nested = null
    fields[key] = unquote(rawValue.trim(), file)
  }
  const body = text.slice(end + 5).replace(/^\n+/, '')
  return { fields, body }
}

function unquote(value, file) {
  if (value.startsWith('"')) {
    if (!value.endsWith('"') || value.length < 2) throw new Error(`${file}: unterminated string ${value}`)
    return JSON.parse(value)
  }
  if (value.startsWith("'")) {
    if (!value.endsWith("'") || value.length < 2) throw new Error(`${file}: unterminated string ${value}`)
    return value.slice(1, -1).replaceAll("''", "'")
  }
  if (/^[|>]/.test(value)) throw new Error(`${file}: block scalars are not supported; write the value on one line`)
  return value
}

function invocationOf(fields, file) {
  const read = (key) => {
    if (!Object.hasOwn(fields, key)) return undefined
    const word = String(fields[key]).toLowerCase()
    if (!BOOLEAN_WORDS.has(word)) throw new Error(`${file}: ${key} must be a boolean`)
    return BOOLEAN_WORDS.get(word)
  }
  const disableModel = read('disable-model-invocation')
  const userInvocable = read('user-invocable')
  return { modelInvocable: disableModel !== true, userInvocable: userInvocable !== false }
}

/** Read and validate one skill folder. Returns the catalog candidate and its body. */
export async function loadSkill(dir, providerName) {
  const file = path.join(dir, 'SKILL.md')
  const { fields, body } = parseSkillFile(await readFile(file, 'utf8'), file)
  const name = fields.name
  if (typeof name !== 'string' || !SKILL_NAME.test(name)) throw new Error(`${file}: name must be kebab-case`)
  if (name !== path.basename(dir)) throw new Error(`${file}: name "${name}" must equal its folder name`)
  if (typeof fields.description !== 'string' || fields.description.trim() === '') {
    throw new Error(`${file}: description is required`)
  }
  const candidate = {
    name,
    description: fields.description.trim(),
    ...(typeof fields.whenToUse === 'string' && fields.whenToUse.trim() ? { whenToUse: fields.whenToUse.trim() } : {}),
    invocation: invocationOf(fields, file),
    provider: providerName,
    source: 'bundled',
    resourceBase: { kind: 'directory', path: dir + path.sep },
    rank: BUNDLED_SKILL_RANK,
    path: file,
    locator: file,
  }
  return { candidate, body }
}

/** List the skill folders under `skillsDir`, sorted by name. */
export async function skillDirs(skillsDir) {
  const entries = await readdir(skillsDir, { withFileTypes: true })
  const dirs = []
  for (const e of entries) {
    if (!e.isDirectory()) continue
    const dir = path.join(skillsDir, e.name)
    try {
      if ((await stat(path.join(dir, 'SKILL.md'))).isFile()) dirs.push(dir)
    } catch { /* a folder without SKILL.md is not a skill */ }
  }
  return dirs.sort()
}

/**
 * Build a DSH skill provider over `skillsDir`.
 * `appendix(name)` may return extra text added after a skill's body at load
 * time (Gravitas uses it for its DeepSeek Harness platform notes).
 */
export function createProvider({ providerName, skillsDir, appendix, logger }) {
  return {
    name: providerName,
    async list() {
      const out = []
      for (const dir of await skillDirs(skillsDir)) {
        try {
          out.push((await loadSkill(dir, providerName)).candidate)
        } catch (error) {
          logger?.warn?.(`${providerName}: skipped ${dir}: ${error.message}`)
        }
      }
      return out
    },
    async get(candidate) {
      const dir = path.join(skillsDir, candidate.name)
      const { candidate: fresh, body } = await loadSkill(dir, providerName)
      const extra = appendix ? await appendix(fresh.name) : ''
      return {
        name: fresh.name,
        description: fresh.description,
        ...(fresh.whenToUse ? { whenToUse: fresh.whenToUse } : {}),
        invocation: fresh.invocation,
        provider: providerName,
        source: 'bundled',
        resourceBase: fresh.resourceBase,
        path: fresh.path,
        content: extra ? `${body.trimEnd()}\n\n${extra.trim()}\n` : body,
      }
    },
  }
}
