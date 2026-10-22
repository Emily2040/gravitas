// Once-a-day check for a newer Gravitas release on GitHub.
//
// One unauthenticated GET to the GitHub releases API at most every 24 hours; the
// answer is cached in a small JSON file, so the other boots that day make no request.
// Nothing about the user is sent: the request carries only a User-Agent naming this
// plugin and its version. Any failure (offline, blocked, slow, rate-limited, bad JSON)
// means no notice, never an error. Turn it off with `updateCheck: false` on the row.
import { readFile, writeFile, mkdir } from 'node:fs/promises'
import os from 'node:os'
import path from 'node:path'

export const RELEASES_API = 'https://api.github.com/repos/Emily2040/gravitas/releases/latest'
export const RELEASES_PAGE = 'https://github.com/Emily2040/gravitas/releases/latest'
export const DAY_MS = 24 * 60 * 60 * 1000
const TIMEOUT_MS = 4000

/** Where the last check is cached: $DSH_HOME/gravitas/update-check.json (DSH_HOME defaults to ~/.dsh). */
export function stateFile(env = process.env) {
  const home = env.DSH_HOME || path.join(os.homedir(), '.dsh')
  return path.join(home, 'gravitas', 'update-check.json')
}

/** "v1.3.1" or "1.3.1" -> [1, 3, 1]; anything else, including prereleases, -> undefined. */
export function parseVersion(text) {
  const m = /^v?(\d+)\.(\d+)\.(\d+)$/.exec(String(text ?? '').trim())
  return m ? m.slice(1).map(Number) : undefined
}

/** True when a is a strictly later release than b. */
export function isNewer(a, b) {
  const x = parseVersion(a)
  const y = parseVersion(b)
  if (!x || !y) return false
  for (let i = 0; i < 3; i++) if (x[i] !== y[i]) return x[i] > y[i]
  return false
}

async function readState(file) {
  try {
    const s = JSON.parse(await readFile(file, 'utf8'))
    return typeof s?.checkedAt === 'number' ? s : undefined
  } catch {
    return undefined
  }
}

async function writeState(file, state) {
  try {
    await mkdir(path.dirname(file), { recursive: true })
    await writeFile(file, JSON.stringify(state, null, 1) + '\n')
  } catch {
    // A read-only home only means the next boot asks again.
  }
}

/**
 * The newer release, as { latest, url }, or undefined when there is none or the check failed.
 * At most one network request per DAY_MS; a failed request still waits a day before the next.
 */
export async function checkForUpdate({ current, file = stateFile(), now = Date.now(), fetchImpl = globalThis.fetch } = {}) {
  let state = await readState(file)
  if (!state || !(now - state.checkedAt < DAY_MS && now >= state.checkedAt)) {
    let latest = state?.latest
    let url = state?.url
    try {
      const res = await fetchImpl(RELEASES_API, {
        headers: { Accept: 'application/vnd.github+json', 'User-Agent': `dsh-gravitas/${current}` },
        signal: AbortSignal.timeout(TIMEOUT_MS),
      })
      if (res.ok) {
        const body = await res.json()
        if (parseVersion(body?.tag_name)) {
          latest = String(body.tag_name).replace(/^v/, '')
          url = typeof body.html_url === 'string' && body.html_url.startsWith('https://github.com/') ? body.html_url : RELEASES_PAGE
        }
      }
    } catch {
      // offline, blocked or timed out: keep what we knew
    }
    state = { checkedAt: now, latest, url }
    await writeState(file, state)
  }
  return isNewer(state.latest, current) ? { latest: state.latest, url: state.url || RELEASES_PAGE } : undefined
}
