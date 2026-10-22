// Tests for the once-a-day update check and the notice it adds. Run: node --test "dsh/test/*.test.js"
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mkdtempSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import * as plugin from '../index.js'
import { checkForUpdate, isNewer, parseVersion, stateFile, DAY_MS, RELEASES_API, RELEASES_PAGE } from '../lib/update-check.js'

const T0 = Date.UTC(2026, 9, 22, 12)
const tmp = () => path.join(mkdtempSync(path.join(os.tmpdir(), 'gv-update-')), 'gravitas', 'update-check.json')

/** A fetch stand-in that counts calls and answers with the given release, status or error. */
function fakeFetch(answer) {
  const calls = []
  const f = async (url, opts) => {
    calls.push({ url, opts })
    if (answer instanceof Error) throw answer
    const { status = 200, body } = answer
    return { ok: status >= 200 && status < 300, status, json: async () => (typeof body === 'string' ? JSON.parse(body) : body) }
  }
  f.calls = calls
  return f
}

test('versions: only plain releases compare, and only a later one is newer', () => {
  assert.deepEqual(parseVersion('v1.3.1'), [1, 3, 1])
  assert.deepEqual(parseVersion('1.10.0'), [1, 10, 0])
  for (const bad of ['', 'v1.3', '1.3.0-rc.1', 'latest', undefined, null]) assert.equal(parseVersion(bad), undefined, String(bad))
  assert.equal(isNewer('1.3.1', '1.3.0'), true)
  assert.equal(isNewer('1.10.0', '1.9.9'), true)
  assert.equal(isNewer('2.0.0', '1.99.99'), true)
  assert.equal(isNewer('1.3.0', '1.3.0'), false)
  assert.equal(isNewer('1.2.9', '1.3.0'), false)
  assert.equal(isNewer(undefined, '1.3.0'), false)
  assert.equal(isNewer('1.4.0-rc.1', '1.3.0'), false)
})

test('the cache lives under DSH_HOME, else ~/.dsh', () => {
  assert.equal(stateFile({ DSH_HOME: path.join('X', 'home') }), path.join('X', 'home', 'gravitas', 'update-check.json'))
  assert.equal(stateFile({}), path.join(os.homedir(), '.dsh', 'gravitas', 'update-check.json'))
})

test('a newer release is found with one request and cached for a day', async () => {
  const file = tmp()
  const f = fakeFetch({ body: { tag_name: 'v1.3.1', html_url: 'https://github.com/Emily2040/gravitas/releases/tag/v1.3.1' } })
  const found = await checkForUpdate({ current: '1.3.0', file, now: T0, fetchImpl: f })
  assert.deepEqual(found, { latest: '1.3.1', url: 'https://github.com/Emily2040/gravitas/releases/tag/v1.3.1' })
  assert.equal(f.calls.length, 1)
  assert.equal(f.calls[0].url, RELEASES_API)
  assert.deepEqual(Object.keys(f.calls[0].opts.headers).sort(), ['Accept', 'User-Agent'], 'nothing else is sent')
  assert.equal(f.calls[0].opts.headers['User-Agent'], 'dsh-gravitas/1.3.0')
  assert.ok(f.calls[0].opts.signal, 'the request has a timeout')
  const later = await checkForUpdate({ current: '1.3.0', file, now: T0 + DAY_MS - 1, fetchImpl: f })
  assert.deepEqual(later, found)
  assert.equal(f.calls.length, 1, 'no second request within 24 hours')
  await checkForUpdate({ current: '1.3.0', file, now: T0 + DAY_MS, fetchImpl: f })
  assert.equal(f.calls.length, 2, 'asks again after 24 hours')
  assert.equal(JSON.parse(readFileSync(file, 'utf8')).latest, '1.3.1')
})

test('no notice when the installed version is the latest, or later', async () => {
  for (const current of ['1.3.1', '1.4.0']) {
    const f = fakeFetch({ body: { tag_name: 'v1.3.1', html_url: 'https://github.com/x' } })
    assert.equal(await checkForUpdate({ current, file: tmp(), now: T0, fetchImpl: f }), undefined, current)
    assert.equal(f.calls.length, 1)
  }
})

test('offline, blocked, rate-limited or bad answers give no notice and wait a day', async () => {
  const answers = [new Error('ENOTFOUND'), new DOMException('timed out', 'TimeoutError'), { status: 403, body: {} }, { status: 200, body: '{"tag_name": 5}' }, { body: { tag_name: 'v1.4.0-rc.1' } }]
  for (const answer of answers) {
    const file = tmp()
    const f = fakeFetch(answer)
    assert.equal(await checkForUpdate({ current: '1.3.0', file, now: T0, fetchImpl: f }), undefined)
    assert.equal(await checkForUpdate({ current: '1.3.0', file, now: T0 + 1000, fetchImpl: f }), undefined)
    assert.equal(f.calls.length, 1, 'a failure is not retried on every boot')
  }
})

test('a failed request keeps the last known release', async () => {
  const file = tmp()
  await checkForUpdate({ current: '1.3.0', file, now: T0, fetchImpl: fakeFetch({ body: { tag_name: 'v1.3.1', html_url: 'https://github.com/a' } }) })
  const found = await checkForUpdate({ current: '1.3.0', file, now: T0 + DAY_MS, fetchImpl: fakeFetch(new Error('offline')) })
  assert.deepEqual(found, { latest: '1.3.1', url: 'https://github.com/a' })
})

test('a missing, corrupt or future-dated cache leads to a fresh check', async () => {
  for (const content of [null, 'not json', JSON.stringify({ checkedAt: T0 + 10 * DAY_MS, latest: '9.9.9' })]) {
    const file = tmp()
    if (content !== null) {
      mkdirSync(path.dirname(file), { recursive: true })
      writeFileSync(file, content)
    }
    const f = fakeFetch({ body: { tag_name: 'v1.3.0', html_url: 'https://github.com/b' } })
    assert.equal(await checkForUpdate({ current: '1.3.0', file, now: T0, fetchImpl: f }), undefined)
    assert.equal(f.calls.length, 1, String(content))
  }
})

test('a release page outside github.com is not passed on', async () => {
  const found = await checkForUpdate({ current: '1.3.0', file: tmp(), now: T0, fetchImpl: fakeFetch({ body: { tag_name: 'v1.3.1', html_url: 'https://evil.example/x' } }) })
  assert.equal(found.url, RELEASES_PAGE)
})

function fakeCtx() {
  const sections = []
  return {
    sections,
    ctx: {
      skills: { registerProvider: () => {} },
      systemPrompt: { section: (s) => { sections.push(s); return () => {} } },
      effect: (fn) => fn(),
      logger: { warn: (m) => { throw new Error(m) } },
    },
  }
}

test('a newer release adds one notice section after the rule, in the configured language', async () => {
  const version = JSON.parse(readFileSync(new URL('../../package.json', import.meta.url), 'utf8')).version
  const url = 'https://github.com/Emily2040/gravitas/releases/tag/v9.0.0'
  for (const lang of plugin.LANGUAGES) {
    const { ctx, sections } = fakeCtx()
    let pending
    let asked
    await plugin.apply(ctx, { language: lang }, {
      checkForUpdate: async (a) => { asked = a; return { latest: '9.0.0', url } },
      onUpdateNotice: (p) => { pending = p },
    })
    assert.equal(sections.length, 1, 'the rule is there before the check answers')
    assert.equal(await pending, true)
    assert.equal(asked.current, version)
    assert.deepEqual(sections.map((s) => s.name), ['gravitas:always-on-rule', 'gravitas:update-notice'])
    const n = sections[1]
    assert.equal(n.order, plugin.UPDATE_ORDER)
    assert.ok(n.order > plugin.RULE_ORDER)
    assert.equal(n.interpolate, false)
    for (const s of ['9.0.0', version, url]) assert.ok(n.text.includes(s), `${lang} names ${s}`)
    assert.ok(!/\{(latest|current|url|step|root)\}/.test(n.text), `${lang} has no unfilled placeholder`)
    assert.ok(n.text.length < 800, `${lang} notice is ${n.text.length} chars`)
  }
})

test('the update step matches how Gravitas was installed', async () => {
  const plain = mkdtempSync(path.join(os.tmpdir(), 'gv-root-'))
  const cloned = mkdtempSync(path.join(os.tmpdir(), 'gv-root-'))
  mkdirSync(path.join(cloned, '.git'))
  for (const lang of plugin.LANGUAGES) {
    const pkg = await plugin.updateNotice(lang, { current: '1.3.0', latest: '1.3.1', url: 'u', root: plain })
    assert.ok(pkg.includes('github:Emily2040/gravitas#v1.3.1'), `${lang} package step`)
    assert.ok(pkg.includes('dsh plugin --profile'), `${lang} terminal step`)
    assert.ok(!pkg.includes('git pull'), lang)
    const git = await plugin.updateNotice(lang, { current: '1.3.0', latest: '1.3.1', url: 'u', root: cloned })
    assert.ok(git.includes('git pull') && git.includes(cloned), `${lang} git step`)
    assert.ok(!git.includes('github:Emily2040/gravitas#'), lang)
  }
})

test('no notice, and no request, when updateCheck is false', async () => {
  const { ctx, sections } = fakeCtx()
  let called = false
  await plugin.apply(ctx, { language: 'en', updateCheck: false }, { checkForUpdate: async () => { called = true } })
  assert.equal(called, false)
  assert.deepEqual(sections.map((s) => s.name), ['gravitas:always-on-rule'])
})

test('no notice when there is nothing newer, and a failing check never breaks the plugin', async () => {
  for (const check of [async () => undefined, async () => { throw new Error('boom') }]) {
    const { ctx, sections } = fakeCtx()
    let pending
    await plugin.apply(ctx, { language: 'zh-CN' }, { checkForUpdate: check, onUpdateNotice: (p) => { pending = p } })
    assert.equal(await pending, false)
    assert.deepEqual(sections.map((s) => s.name), ['gravitas:always-on-rule'])
  }
})
