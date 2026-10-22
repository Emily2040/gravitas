// Tests for the DeepSeek Harness plugin in dsh/. Run: node --test "dsh/test/*.test.js"
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import * as plugin from '../index.js'
import { parseSkillFile, BUNDLED_SKILL_RANK } from '../lib/provider.js'

const REPO = fileURLToPath(new URL('../../', import.meta.url))
const pkg = JSON.parse(readFileSync(path.join(REPO, 'package.json'), 'utf8'))
const patch = readFileSync(path.join(REPO, 'dsh', 'cordis.patch.yml'), 'utf8')
const PRUNER_THRESHOLD = 8192

function fakeCtx() {
  const sections = []
  let factory
  return {
    sections,
    provider: () => factory(),
    ctx: {
      skills: { registerProvider: (f) => { factory = f } },
      systemPrompt: { section: (s) => { sections.push(s); return () => {} } },
      effect: (fn) => fn(),
      logger: { warn: (m) => { throw new Error(m) } },
    },
  }
}

test('manifest: a DSH bundle with no dependencies, versioned with the plugin', () => {
  assert.equal(pkg.name, 'dsh-gravitas')
  assert.equal(pkg.type, 'module')
  assert.equal(pkg.dsh.bundle.patch, './dsh/cordis.patch.yml')
  assert.equal(pkg.main, './dsh/index.js')
  assert.equal(pkg.dependencies, undefined)
  for (const s of ['preinstall', 'install', 'postinstall', 'prepare']) assert.equal(pkg.scripts?.[s], undefined)
  assert.match(pkg.engines.dsh, /^>=0\.2\.1-rc\.2 /)
  assert.ok(pkg.keywords.includes('dsh-plugin'))
  const pluginJson = JSON.parse(readFileSync(path.join(REPO, 'plugin', 'plugin.json'), 'utf8'))
  assert.equal(pkg.version, pluginJson.version, 'package.json and plugin/plugin.json carry the same version')
  for (const f of ['dsh/index.js', 'dsh/lib/', 'dsh/platform/', 'dsh/locale/*.json', 'dsh/icon.svg', 'dsh/cordis.patch.yml', 'dist/', 'LICENSE']) {
    assert.ok(pkg.files.includes(f), `files lists ${f}`)
  }
})

test('patch: two presets, one inspector tool naming both, and the plugin row', () => {
  assert.match(patch, /- id: preset-gravitas-inspector\n\s+name: '@deepseek-ai\/dsh-agent-preset'\n\s+config:\n\s+id: gravitas-inspector/)
  assert.match(patch, /- id: preset-gravitas-checker\n\s+name: '@deepseek-ai\/dsh-agent-preset'\n\s+config:\n\s+id: gravitas-checker/)
  assert.match(patch, /toolName: gravitas_inspect\n\s+agentPreset: gravitas-inspector\n\s+allowedAgentPresets: \[gravitas-inspector, gravitas-checker\]/)
  assert.match(patch, /- id: dsh-gravitas\n\s+name: 'dsh-gravitas'\n\s+config:\n\s+language: auto\n\s+alwaysOnRule: true/)
  assert.equal(plugin.name, 'dsh-gravitas')
})

test('patch: the inspector preset cannot write, edit or run commands; the checker can run commands', () => {
  const inspector = patch.slice(patch.indexOf('- id: preset-gravitas-inspector'), patch.indexOf('- id: preset-gravitas-checker'))
  const checker = patch.slice(patch.indexOf('- id: preset-gravitas-checker'), patch.indexOf('- id: tool-gravitas-inspect'))
  for (const p of [inspector, checker]) assert.match(p, /dsh-tool-fs'\n\s+config:\n\s+write: false\n\s+edit: false/)
  assert.doesNotMatch(inspector, /dsh-tool-(pwsh|bash)|tool-subagent|tool-str-replace|tool-jobs/)
  assert.match(checker, /dsh-tool-pwsh/)
  assert.match(checker, /dsh-tool-bash/)
  assert.doesNotMatch(patch.replace(/^\s*#.*$/gm, ''), /\{\{/, 'persona text has no template braces')
})

test('language: config wins, then the system locale, then English', () => {
  assert.equal(plugin.resolveLanguage('auto', 'zh-CN'), 'zh-CN')
  assert.equal(plugin.resolveLanguage('auto', 'zh-Hans-CN'), 'zh-CN')
  assert.equal(plugin.resolveLanguage('auto', 'ja-JP'), 'ja')
  assert.equal(plugin.resolveLanguage('auto', 'ko-KR'), 'ko')
  assert.equal(plugin.resolveLanguage('auto', 'en-AU'), 'en')
  assert.equal(plugin.resolveLanguage('auto', 'fr-FR'), 'en')
  assert.equal(plugin.resolveLanguage('ja', 'zh-CN'), 'ja')
  assert.throws(() => plugin.resolveLanguage('zh'), /language must be/)
  assert.throws(() => plugin.readConfig({ langauge: 'ja' }), /unknown config key/)
  assert.throws(() => plugin.readConfig({ alwaysOnRule: 'yes' }), /true or false/)
})

for (const lang of plugin.LANGUAGES) {
  test(`${lang}: skill, rule and platform note load and fit`, async () => {
    const { ctx, sections, provider } = fakeCtx()
    await plugin.apply(ctx, { language: lang, alwaysOnRule: true })
    const list = await provider().list()
    assert.deepEqual(list.map((c) => c.name), ['gravitas'])
    assert.equal(list[0].rank, BUNDLED_SKILL_RANK)
    const skill = await provider().get(list[0])
    assert.ok(!skill.content.startsWith('---'))
    assert.ok(skill.content.length < PRUNER_THRESHOLD - 200, `skill with note is ${skill.content.length} chars`)
    assert.ok(!skill.content.includes('AGENTS_DIR'), 'agents folder is filled in')
    const agentsDir = plugin.pathsFor(lang).agents
    const agents = readdirSync(agentsDir).filter((f) => f.endsWith('.md'))
    for (const a of agents) assert.ok(skill.content.includes(a), `${lang} note names ${a}`)
    for (const m of skill.content.matchAll(/`(gravitas-[a-z-]+\.md)`/g)) assert.ok(existsSync(path.join(agentsDir, m[1])), `${m[1]} exists`)
    assert.ok(existsSync(skill.resourceBase.path))
    assert.equal(sections.length, 1)
    const s = sections[0]
    assert.equal(s.name, 'gravitas:always-on-rule')
    assert.equal(s.order, plugin.RULE_ORDER)
    assert.equal(s.interpolate, false)
    assert.ok(s.text.includes('DeepSeek Harness'))
    assert.ok(s.text.length < 24000)
  })
}

test('rule can be turned off', async () => {
  const { ctx, sections } = fakeCtx()
  await plugin.apply(ctx, { language: 'en', alwaysOnRule: false })
  assert.equal(sections.length, 0)
})

test('platform notes name the same tools in every language', () => {
  const spans = (lang) => {
    const t = readFileSync(path.join(REPO, 'dsh', 'platform', `${lang}.md`), 'utf8')
    return [...new Set([...t.matchAll(/`([^`]+)`/g)].map((m) => m[1]))].sort()
  }
  const ruleSpans = (lang) => [...readFileSync(path.join(REPO, 'dsh', 'platform', `${lang}.rule.md`), 'utf8').matchAll(/`([^`]+)`/g)].map((m) => m[1]).sort()
  for (const lang of plugin.LANGUAGES.slice(1)) {
    assert.deepEqual(spans(lang), spans('en'), `${lang} platform note`)
    assert.deepEqual(ruleSpans(lang), ruleSpans('en'), `${lang} rule note`)
  }
})

test('locales and icon are present for the Plugins page', () => {
  for (const l of ['en', 'zh', 'ja', 'ko']) {
    const meta = JSON.parse(readFileSync(path.join(REPO, 'dsh', 'locale', `${l}.json`), 'utf8')).meta
    assert.ok(meta.title && meta.description.length > 20, l)
  }
  const icon = readFileSync(path.join(REPO, 'dsh', 'icon.svg'), 'utf8')
  assert.ok(icon.startsWith('<svg') && statSync(path.join(REPO, 'dsh', 'icon.svg')).size < 256 * 1024)
})

test('the skill frontmatter in every language parses with its nested metadata', () => {
  for (const lang of plugin.LANGUAGES) {
    const f = path.join(plugin.pathsFor(lang).skills, 'gravitas', 'SKILL.md')
    const { fields } = parseSkillFile(readFileSync(f, 'utf8'), f)
    assert.equal(fields.name, 'gravitas')
    assert.equal(fields.metadata.version, pkg.version, `${lang} SKILL.md version`)
  }
})

test('index.js imports cleanly as an ES module URL', async () => {
  const mod = await import(pathToFileURL(path.join(REPO, 'dsh', 'index.js')).href)
  assert.deepEqual(mod.inject, ['skills', 'systemPrompt'])
})
