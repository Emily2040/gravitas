// Claim check for DeepSeek Harness (DSH).
//
// Before a turn closes, list the specifics a drafted answer adds that nothing in
// the turn supports: numbers, dates, article and document numbers, phone numbers,
// links, quoted wording and app menu paths that appear neither in the user's
// message nor in any tool result of the turn, and that no arithmetic shown in the
// answer derives from supported numbers. A shown calculation that does not add up
// is listed too. The plugin then steers the model once with the list (index.js).
//
// Pure functions, no dependencies (see provider.js for why).

const CN_DIGITS = { 零: 0, 〇: 0, 一: 1, 二: 2, 两: 2, 三: 3, 四: 4, 五: 5, 六: 6, 七: 7, 八: 8, 九: 9 }
const CN_UNITS = { 十: 10, 百: 100, 千: 1000 }
const CN_BIG = { 万: 1e4, 亿: 1e8 }
const CN_NUM = '[零〇一二两三四五六七八九十百千万亿]+'

/** Chinese numerals to a number: 三十七 → 37, 一万二千 → 12000, 二〇二六 → 2026. NaN if not a numeral. */
export function cnToNumber(s) {
  if (!s) return NaN
  if (/^[零〇一二两三四五六七八九]+$/.test(s) && s.length > 1) {
    return Number([...s].map((c) => CN_DIGITS[c]).join(''))
  }
  let total = 0
  let section = 0
  let digit = 0
  for (const c of s) {
    if (c in CN_DIGITS) digit = CN_DIGITS[c]
    else if (c in CN_UNITS) { section += (digit || 1) * CN_UNITS[c]; digit = 0 }
    else if (c in CN_BIG) { total += (section + digit) * CN_BIG[c]; section = 0; digit = 0 }
    else return NaN
  }
  return total + section + digit
}

const EN_WORDS = {
  zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10,
  eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15, sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19,
  twenty: 20, thirty: 30, forty: 40, fifty: 50, sixty: 60, seventy: 70, eighty: 80, ninety: 90,
  hundred: 100, thousand: 1000, million: 1e6,
}

/** English number words to a number: "five hundred" → 500, "twenty-one" → 21. NaN if not number words. */
export function wordsToNumber(s) {
  let total = 0
  let cur = 0
  let seen = false
  for (const w of String(s).toLowerCase().split(/[\s-]+/).filter((x) => x && x !== 'and')) {
    const v = EN_WORDS[w]
    if (v === undefined) return NaN
    seen = true
    if (v === 100) cur = (cur || 1) * 100
    else if (v >= 1000) { total += (cur || 1) * v; cur = 0 }
    else cur += v
  }
  return seen ? total + cur : NaN
}

/** NFKC folds full-width digits, letters and punctuation; brackets of document numbers become [ ]. */
export function normalize(text) {
  return String(text ?? '')
    .replace(/，/g, '、') // NFKC would make it an ASCII comma, which reads as a thousands separator
    .normalize('NFKC')
    .replace(/[〔［【]/g, '[')
    .replace(/[〕］】]/g, ']')
    .replace(/[−–—]/g, '-')
    .replace(/\r\n/g, '\n')
}

/** Text squeezed for substring checks: no spaces, no quote marks, lower case. */
function squeeze(text) {
  return normalize(text).toLowerCase().replace(/[\s"'“”‘’「」『』《》<>()（）,.，。:：;；!?！？、*_`#|-]/g, '')
}

const round = (v) => Math.round(v * 1e6) / 1e6

const UNIT_RULES = [
  ['money', /^(?:元|块钱|块|万元|亿元|美元|英镑|欧元|yuan|rmb|dollars?|usd)/i],
  ['percent', /^(?:%|个百分点|percent|per cent)/i],
  ['times', /^(?:倍|times\b)/i],
  ['days', /^(?:个工作日|工作日|天|日|business days?|calendar days?|days?\b)/i],
  ['weeks', /^(?:个星期|星期|周|weeks?\b)/i],
  ['months', /^(?:个月|months?\b)/i],
  ['hours', /^(?:个小时|小时|hours?\b|hrs?\b)/i],
  ['minutes', /^(?:分钟|minutes?\b|mins?\b)/i],
  ['points', /^分(?!钟|之)/],
  ['age', /^(?:周岁|岁|years? old\b)/i],
  ['years', /^(?:年|years?\b)/i],
  ['dose', /^(?:mg\b|毫克|ml\b|毫升|片|粒|caplets?\b|tablets?\b|pills?\b)/i],
  ['distance', /^(?:miles?\b|mi\b|公里|km\b)/i],
]

const MONTHS = { jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12 }
const pad = (n) => String(n).padStart(2, '0')

/** Replace a span with spaces of the same length so later scans skip it but offsets stay put. */
function mask(text, start, end) {
  return text.slice(0, start) + ' '.repeat(end - start) + text.slice(end)
}

/** Where fenced code blocks are, so drafted letters inside them are not read as quotations. */
function fencedRanges(text) {
  const ranges = []
  const re = /```[\s\S]*?(?:```|$)/g
  let m
  while ((m = re.exec(text))) ranges.push([m.index, m.index + m[0].length])
  return ranges
}

/**
 * Every specific in a text, in reading order:
 * { cls, key, raw, index, value? }. cls is one of url, phone, docnum, article,
 * date, year, time, quote, path, or a number class (money, percent, times, days,
 * weeks, months, hours, minutes, points, age, years, dose, distance, num).
 */
export function extract(input) {
  let text = normalize(input)
  const items = []
  const add = (cls, key, raw, index, value) => items.push({ cls, key, raw, index, value })
  const scan = (re, fn) => {
    re.lastIndex = 0
    let m
    const found = []
    while ((m = re.exec(text))) found.push(m)
    for (const m of found) {
      if (fn(m) !== false) text = mask(text, m.index, m.index + m[0].length)
    }
  }
  const code = fencedRanges(text)
  const inCode = (i) => code.some(([a, b]) => i >= a && i < b)

  // Links first: their digits are not claims of their own.
  scan(/\bhttps?:\/\/[^\s)\]>"'“”，。,;；]+/gi, (m) => {
    add('url', m[0].replace(/^https?:\/\//i, '').replace(/[/.]+$/, '').toLowerCase(), m[0], m.index)
  })
  scan(/\b(?:[a-z0-9-]+\.)+(?:gov\.cn|com\.cn|org\.cn|edu\.cn|gov\.uk|co\.uk|gov|com|org|net|edu|cn)\b(?:\/[^\s)\]>"'“”，。,;；]*)?/gi, (m) => {
    add('url', m[0].replace(/[/.]+$/, '').toLowerCase(), m[0], m.index)
  })
  // Long document titles (《关于……的通知》); short ones such as 《劳动合同法》 name the law for an article below.
  scan(/《([^》\n]{8,60})》/g, (m) => add('title', squeeze(m[1]), m[0], m.index))
  // Menu paths written as tapped labels: 点击“我的”，再点“驾驶证”.
  {
    const labels = []
    const re = /(?:点击|点开|再点|然后点|点|进入|选择|打开|找到|tap|click|select|open)\s*[“"「『‘]([^”"」』’\n]{1,14})[”"」』’]/gi
    let m
    while ((m = re.exec(text))) labels.push({ label: m[1].trim(), index: m.index, end: m.index + m[0].length })
    let group = []
    const flush = () => {
      if (group.length >= 2) add('path', group.map((g) => squeeze(g.label)).join('>'), group.map((g) => g.label).join(' > '), group[0].index)
      group = []
    }
    for (const l of labels) {
      if (group.length && l.index - group[group.length - 1].end > 25) flush()
      group.push(l)
    }
    flush()
  }
  // Quoted wording, before its digits are read as numbers.
  scan(/[“"「『‘]([^”"」』’\n]{4,300})[”"」』’]/g, (m) => {
    const inner = m[1].replace(/[*_`]/g, '')
    const cjk = (inner.match(/[㐀-鿿]/g) || []).length
    const words = inner.trim().split(/\s+/).length
    if (inCode(m.index) || (cjk < 8 && words < 5)) return false
    add('quote', squeeze(inner), m[0], m.index) // checked whole, so its digits are not listed again
  })
  // A segment is a short label; Latin labels may hold a few words ("Cancel flight").
  const SEG = '[^\\s→⇒>\\n.。、，,:：；;“”"「」『』()（）]{1,16}(?: [A-Za-z0-9][^\\s→⇒>\\n.。、，,:：；;“”"「」『』()（）]{0,15}){0,3}'
  scan(new RegExp(`(?:${SEG}[ \\t]*(?:→|⇒|->|[ \\t]>[ \\t])[ \\t]*){1,8}${SEG}`, 'g'), (m) => {
    const segs = m[0].split(/→|⇒|->|\s>\s/)
      .map((s) => s.trim().replace(/^[《「“"『【\[(（*]+|[》」”"』】\])）.*]+$/g, '').replace(/^(?:点击|点开|点|打开|进入|选择|找到|tap|click|open|go to|select)\s*/i, '').trim())
      .filter(Boolean)
    if (segs.length < 2 || segs.some((s) => !/[A-Za-z㐀-鿿]/.test(s))) return false
    add('path', segs.map(squeeze).join('>'), segs.join(' > '), m.index)
  })
  // Menu paths written with slashes: 我的/驾驶证/记分查询.
  scan(/(?<![\w/])[㐀-鿿]{2,8}(?:\s?\/\s?[㐀-鿿]{2,8}){2,6}(?![\w/])/g, (m) => {
    const segs = m[0].split('/').map((s) => s.trim())
    add('path', segs.map(squeeze).join('>'), segs.join(' > '), m.index)
  })
  // Phone numbers: US numbers first (so 1-800-... keeps its 1), then numbers with separators and mobiles.
  scan(/(?<![\d.])(?:1[-.\s])?(?:\(\d{3}\)\s?|\d{3}[-.])\d{3}[-.]\d{4}(?![\d.])/g, (m) => {
    add('phone', m[0].replace(/\D/g, '').replace(/^1(?=\d{10}$)/, ''), m[0], m.index)
  })
  scan(/(?<![\d.])(?:\+?86[-\s]?)?(?:0\d{2,3}-\d{7,8}|1[3-9]\d{9}|[48]00-?\d{3}-?\d{4})(?![\d.])/g, (m) => {
    add('phone', m[0].replace(/\D/g, '').replace(/^86/, ''), m[0], m.index)
  })
  // Document numbers: 国办发〔2021〕14号, 公安部令第163号.
  scan(/\[\s?((?:19|20)\d{2})\s?\]\s?(\d+)\s?号/g, (m) => add('docnum', `${m[1]}-${m[2]}`, m[0], m.index))
  scan(/令\s?第\s?(\d+|[零〇一二两三四五六七八九十百千]+)\s?号|第\s?(\d+)\s?号令/g, (m) => {
    const n = m[1] ? (/^\d+$/.test(m[1]) ? Number(m[1]) : cnToNumber(m[1])) : Number(m[2])
    add('docnum', `ling-${n}`, m[0], m.index)
  })
  // Articles and sections, with the law named just before them when there is one.
  const original = normalize(input)
  scan(new RegExp(`第\\s?(\\d+|${CN_NUM})\\s?条(?:\\s?第\\s?(\\d+|${CN_NUM})\\s?款)?`, 'g'), (m) => {
    const a = /^\d+$/.test(m[1]) ? Number(m[1]) : cnToNumber(m[1])
    const before = original.slice(Math.max(0, m.index - 40), m.index)
    const law = (/《([^》]{2,40})》\s*$/.exec(before) || /([㐀-鿿]{2,16}(?:法|条例|办法|规定|细则|解释|意见|通知|决定))\s*$/.exec(before))?.[1]
    items.push({ cls: 'article', key: `art-${a}`, raw: m[0], index: m.index, law: law ? squeeze(law).replace(/^中华人民共和国/, '') : undefined })
  })
  scan(/(?:§+\s?|\bsection\s+|\bsec\.\s?)(\d+(?:\.\d+)?)(?:\s?\(\w{1,4}\))*/gi, (m) => add('article', `sec-${m[1]}`, m[0], m.index))
  scan(/\b(\d{1,2})\s?(?:U\.?S\.?C\.?|C\.?F\.?R\.?)\s?(?:§+\s?|part\s+)?(\d+(?:\.\d+)?)/gi, (m) => add('article', `sec-${m[2]}`, m[0], m.index))
  // Dates.
  scan(/((?:19|20)\d{2})\s?年\s?(\d{1,2})\s?月\s?(\d{1,2})\s?[日号]/g, (m) => add('date', `${m[1]}-${pad(m[2])}-${pad(m[3])}`, m[0], m.index))
  scan(/((?:19|20)\d{2})[-/.](\d{1,2})[-/.](\d{1,2})(?!\d)/g, (m) => add('date', `${m[1]}-${pad(m[2])}-${pad(m[3])}`, m[0], m.index))
  scan(/((?:19|20)\d{2})\s?年\s?(\d{1,2})\s?月(?![\d份]?\s?\d)/g, (m) => add('date', `${m[1]}-${pad(m[2])}`, m[0], m.index))
  scan(/(?<!\d)(\d{1,2})\s?月\s?(\d{1,2})\s?[日号]/g, (m) => add('date', `${pad(m[1])}-${pad(m[2])}`, m[0], m.index))
  scan(/\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?\b(?:,?\s+((?:19|20)\d{2}))?/gi, (m) => {
    const mo = MONTHS[m[1].toLowerCase()]
    add('date', m[3] ? `${m[3]}-${pad(mo)}-${pad(m[2])}` : `${pad(mo)}-${pad(m[2])}`, m[0], m.index)
  })
  scan(/\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+((?:19|20)\d{2})\b/gi, (m) => {
    add('date', `${m[2]}-${pad(MONTHS[m[1].toLowerCase()])}`, m[0], m.index)
  })
  scan(/(?<![\d.])((?:19|20)\d{2})(?![\d.]|,\d{3})\s?年?(?!\s?(?:元|块|美元|dollars|%|倍))/g, (m) => add('year', m[1], m[0], m.index))
  scan(/(?<![\d:])([01]?\d|2[0-4]):([0-5]\d)(?![\d:])/g, (m) => add('time', `${pad(m[1])}:${m[2]}`, m[0], m.index))
  // Chinese numerals with a unit: 三十日, 百分之五十, 三倍.
  scan(/百分之([零〇一二两三四五六七八九十百千]+)/g, (m) => add('percent', `percent:${round(cnToNumber(m[1]))}`, m[0], m.index, cnToNumber(m[1])))
  scan(new RegExp(`(${CN_NUM})(多|余|来)?(个工作日|工作日|天|日|个月|周岁|岁|倍|万元|元|块钱|块|美元|小时|分钟|分(?!之)|年|次|个星期|星期|周|个百分点|成)`, 'g'), (m) => {
    let v = cnToNumber(m[1])
    // 两三百元, 三四天: a rough range, not a figure.
    if (/[一二两三四五六七八九]{2}/.test(m[1]) && !/[〇零]/.test(m[1])) return false
    if (!Number.isFinite(v) || (m[1] === '一' && !m[2] && /^(?:天|日|年|次|周|分|成)$/.test(m[3]))) return false
    if (m[3] === '万元') v *= 1e4
    if (m[3] === '成') v *= 10 // 三成 = 30%
    const cls = m[3] === '成' ? 'percent' : UNIT_RULES.find(([, re]) => re.test(m[3]))?.[0] ?? 'num'
    items.push({ cls, key: `${cls}:${round(v)}`, raw: m[0], index: m.index, value: v, approx: !!m[2] })
  })
  // English number words with a unit: "thirty days", "five hundred dollars".
  scan(new RegExp(`\\b((?:(?:${Object.keys(EN_WORDS).join('|')})(?:[\\s-]+(?:and[\\s-]+)?)?)+)\\s*(business days?|calendar days?|days?|weeks?|months?|years?|hours?|minutes?|percent|dollars?|times)\\b`, 'gi'), (m) => {
    const v = wordsToNumber(m[1])
    if (!Number.isFinite(v) || /^(?:a|an|one)$/i.test(m[1].trim())) return false
    const cls = UNIT_RULES.find(([, re]) => re.test(m[2]))?.[0] ?? 'num'
    items.push({ cls, key: `${cls}:${round(v)}`, raw: m[0], index: m.index, value: v })
  })
  // Arabic numbers, with currency prefix, 万/千/k multiplier and unit.
  const NUM = /(?<![\w.])([$£¥€])?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?:\s?(万亿|亿|万|千|k|K)(?![A-Za-z]))?/g
  let m
  NUM.lastIndex = 0
  while ((m = NUM.exec(text))) {
    const lineStart = text.lastIndexOf('\n', m.index) + 1
    const before = text.slice(lineStart, m.index)
    const after = text.slice(m.index + m[0].length, m.index + m[0].length + 16).replace(/^\s+/, '')
    // List markers: "1.", "2、", "(3)", "第4步", "Step 5".
    if (/^[\s>*#-]*[(（]?$/.test(before) && /^[.、)）:]/.test(after) && !/^\.\d/.test(after)) continue
    if (/(?:第|步骤|step\s?)$/i.test(before) && /^(?:步|项|点|部分|章|节)/.test(after)) continue
    if (/step\s?$/i.test(before)) continue
    let v = Number(m[2].replace(/,/g, ''))
    const mult = { 万: 1e4, 亿: 1e8, 万亿: 1e12, 千: 1e3, k: 1e3, K: 1e3 }[m[3]] ?? 1
    v *= mult
    // 20多天, 300余元: at least the figure, below the next step.
    const approx = /^[多余来]/.test(after)
    const unitText = approx ? after.slice(1) : after
    let cls = m[1] ? 'money' : (UNIT_RULES.find(([, re]) => re.test(unitText))?.[0] ?? 'num')
    if (cls === 'money' && /^万元/.test(unitText)) v *= 1e4
    if (cls === 'years' && v >= 1000) cls = 'year'
    const decimals = (m[2].split('.')[1] || '').length
    let end = m.index + m[0].length
    if (cls !== 'num' && !m[1]) {
      const gap = text.slice(end).match(/^\s*/)[0].length
      const unit = unitText.match(UNIT_RULES.find(([c]) => c === cls)?.[1] ?? /^$/)?.[0] ?? ''
      if (unit) end += gap + (approx ? 1 : 0) + unit.length
    }
    items.push({ cls, key: `${cls}:${round(v)}`, raw: original.slice(m.index, end).trim(), index: m.index, value: v, decimals, approx })
  }
  return items.sort((a, b) => a.index - b.index)
}

const MONEY_CUE = /元|块|￥|¥|\$|费|金额|价|工资|薪|罚款|赔|补偿|fee|cost|price|pay|refund|limit|benefit/i

/**
 * What one source can support: its specifics by class, its squeezed text, its digit runs.
 * kind is 'request' (the person's message), 'tool' (a tool result) or 'shell' (shell output;
 * it supports only numbers, and never a number that its own command wrote).
 */
function indexSource({ text, kind = 'tool', command = '', tool = '' }) {
  const norm = normalize(text)
  const keys = new Set()
  const byClass = new Map()
  const values = new Set()
  for (const it of extract(text)) {
    keys.add(it.key)
    if (it.cls === 'date') keys.add(`date:${it.key}`)
    if (typeof it.value === 'number') {
      const v = round(it.value)
      values.add(v)
      if (!byClass.has(it.cls)) byClass.set(it.cls, new Set())
      byClass.get(it.cls).add(v)
      if (it.cls === 'percent') values.add(round(it.value / 100))
      // A bare figure next to a money word is an amount: "工本费 40" supports "40元".
      if (it.cls === 'num' && MONEY_CUE.test(norm.slice(Math.max(0, it.index - 10), it.index + String(it.raw).length + 10))) {
        keys.add(`money:${v}`)
        if (!byClass.has('money')) byClass.set('money', new Set())
        byClass.get('money').add(v)
      }
    }
  }
  const digitRuns = new Set((norm.replace(/(\d)[-\s.()]+(?=\d)/g, '$1').match(/\d{5,}/g) || []))
  return { kind, tool, command: normalize(command), sq: squeeze(text), keys, byClass, values, digitRuns }
}

/** The support the person's message and the turn's tool results give, one entry per source. */
export function buildIndex(request, sources = []) {
  const parts = [{ text: request ?? '', kind: 'request' }, ...sources.map((s) => (typeof s === 'string' ? { text: s, kind: 'tool' } : s))]
    .filter((s) => s.text)
    .map(indexSource)
  const dayCounts = new Set([1, 7])
  for (const p of parts) if (p.kind !== 'shell') for (const v of p.byClass.get('days') ?? []) dayCounts.add(v)
  return { parts, dayCounts }
}

/** Share of a string's character pairs found in another string. */
export function overlap(a, b) {
  if (a.length < 2) return b.includes(a) ? 1 : 0
  const pairs = new Set()
  for (let i = 0; i + 1 < b.length; i++) pairs.add(b.slice(i, i + 2))
  let hit = 0
  for (let i = 0; i + 1 < a.length; i++) if (pairs.has(a.slice(i, i + 2))) hit++
  return hit / (a.length - 1)
}

/** A tiny arithmetic parser (+ - * / parentheses, unary minus); NaN on anything else. */
export function evaluate(expr) {
  const s = expr.replace(/\s+/g, '')
  let i = 0
  const peek = () => s[i]
  const num = () => {
    const m = /^\d+(?:\.\d+)?/.exec(s.slice(i))
    if (!m) throw new Error('number')
    i += m[0].length
    return Number(m[0])
  }
  const factor = () => {
    if (peek() === '-') { i++; return -factor() }
    if (peek() === '(') { i++; const v = sum(); if (s[i++] !== ')') throw new Error(')'); return v }
    return num()
  }
  const product = () => {
    let v = factor()
    while (peek() === '*' || peek() === '/') v = s[i++] === '*' ? v * factor() : v / factor()
    return v
  }
  const sum = () => {
    let v = product()
    while (peek() === '+' || peek() === '-') v = s[i++] === '+' ? v + product() : v - product()
    return v
  }
  try {
    const v = sum()
    return i === s.length ? v : NaN
  } catch {
    return NaN
  }
}

/**
 * Turn one side of a written calculation into something evaluate() reads. A left side keeps
 * its last piece (it ends at the = sign); a right side keeps its first piece with a figure.
 */
function toExpression(side, keep = 'last') {
  const pick = (parts) => (keep === 'last' ? parts[parts.length - 1] : parts.find((x) => /\d/.test(x)) ?? '')
  let s = normalize(side).replace(/\*\*|__|`/g, ' ') // markdown emphasis is not multiplication
  // A spaced dash after a word is punctuation ("expedited service - $130 + $60"), not a minus;
  // a table pipe ends a cell. Break at both.
  s = s.replace(/([A-Za-z㐀-鿿])\s+-+\s+/g, '$1 | ')
  s = pick(s.split('|'))
  s = s.replace(/\/\s?(?:[A-Za-z]+|[㐀-鿿]+)/g, '') // per-unit slashes: 元/天, $/month
  s = s.replace(/(\d)\s*[xX×✕＊*]\s*(?=[\d(])/g, '$1*').replace(/[×✕＊]/g, '*').replace(/÷/g, '/')
  s = s.replace(/(\d+(?:\.\d+)?)\s?万/g, '($1*10000)').replace(/(\d+(?:\.\d+)?)\s?%/g, '($1/100)')
  s = s.replace(/(\d),(\d{3})/g, '$1$2').replace(/(\d),(\d{3})/g, '$1$2')
  s = s.replace(/[^\d.+\-*/()]/g, ' ').trim()
  // Two figures with only words between them are not one number: break at the gap.
  s = pick(s.replace(/([\d)])\s+(?=[\d(])/g, '$1|').split('|')).trim()
  if (!/\d/.test(s)) return null
  return s
}

/** The longest tail of an expression that parses, so words left before it do not spoil it. */
function longestTail(expr) {
  if (!expr) return null
  for (let i = 0; i < expr.length; i++) {
    if (i > 0 && !/[\d(-]/.test(expr[i])) continue
    if (i > 0 && /[\d.]/.test(expr[i - 1]) && /\d/.test(expr[i])) continue
    const tail = expr.slice(i).trim()
    if (/[+\-*/]/.test(tail.replace(/^-/, '')) && Number.isFinite(evaluate(tail))) return tail
  }
  return null
}

const closeEnough = (shown, decimals, actual, approx) => {
  if (!Number.isFinite(actual)) return false
  const tol = approx ? Math.max(0.005 * Math.abs(actual), 0.5 * 10 ** -decimals) : 0.5 * 10 ** -decimals + 1e-9
  return Math.abs(shown - actual) <= tol || (decimals === 0 && (Math.floor(actual) === shown || Math.ceil(actual) === shown))
}

/**
 * Written calculations: "a × b = c", "a = b = c". Returns, per result number index,
 * { ok, actual, expr }: ok when the left side evaluates to the shown result.
 */
export function calculations(input, items) {
  const text = normalize(input)
  const results = new Map()
  const byIndex = new Map(items.filter((it) => typeof it.value === 'number').map((it) => [it.index, it]))
  const segRe = /[^\n,，;；。:：]*?(?:=|≈|约等于)[^\n;；。:：]*/g
  for (const line of text.split('\n')) {
    const offset = text.indexOf(line)
    const parts = line.split(/(=|≈|约等于)/)
    if (parts.length < 3) continue
    for (let k = 0; k + 2 < parts.length; k += 2) {
      let left = parts[k]
      const sign = parts[k + 1]
      let right = parts[k + 2]
      // The left operand starts after the last clause break; the right one ends at the next break.
      // Only an ASCII comma can be a thousands separator; every other mark ends the clause.
      left = left.split(/,(?!\d{3})|[，、;；。:：]|\.\s|(?<=[㐀-鿿])\s(?!\s*[×xX*÷/+\-−])/).pop().replace(/^\s*[-*•]\s+/, '')
      right = right.split(/,(?!\d{3})|[，、;；。:：]|\.\s|\s(?=[㐀-鿿])/)[0]
      const le = longestTail(toExpression(left))
      const re = toExpression(right, 'first')
      if (!le || !re || !/[+\-*/]/.test(le)) continue
      const a = evaluate(le)
      const b = evaluate(re)
      if (!Number.isFinite(a) || !Number.isFinite(b)) continue
      // The shown result: the first number of the right side, if the right side is a single number.
      const rightStart = offset + parts.slice(0, k + 2).join('').length
      const target = [...byIndex.values()].find((it) => it.index >= rightStart && it.index < rightStart + parts[k + 2].length)
      if (!target || /[+\-*/]/.test(re.replace(/^\(?-?/, '').replace(/^\d+(?:\.\d+)?/, '').replace(/\*10000\)|\/100\)|\)/g, ''))) {
        // The right side is itself an expression; it is checked when it becomes a left side.
        continue
      }
      const approx = sign !== '=' || /约|大约|about|approximately|≈|~/.test(right.slice(0, 6))
      // The operands as written, so a calculation only counts when its inputs have support of their own.
      // 1.2万 is read as 12000 and 300% as 300, the way they are written.
      const written = le.replace(/\((\d+(?:\.\d+)?)\*10000\)/g, (_, x) => String(round(Number(x) * 1e4))).replace(/\((\d+(?:\.\d+)?)\/100\)/g, '$1')
      const operands = [...written.matchAll(/\d+(?:\.\d+)?/g)].map((o) => ({ value: Number(o[0]), decimals: (o[0].split('.')[1] || '').length }))
      results.set(target.index, { ok: closeEnough(target.value, target.decimals ?? 0, a, approx) || closeEnough(b, target.decimals ?? 0, a, approx), actual: a, expr: left.trim(), operands })
    }
  }
  return results
}

// Small whole numbers in these classes are not worth listing: a count, a dose, an age, a plain number.
const TRIVIAL = new Set(['num', 'count', 'dose', 'age'])
// Numbers a calculation may use without a source: small integers and calendar and scale constants.
const CONSTANTS = new Set([...Array.from({ length: 13 }, (_, i) => i), 24, 30, 31, 52, 60, 100, 365, 366, 1000, 10000])

function addDays(key, n) {
  const d = new Date(`${key}T00:00:00Z`)
  d.setUTCDate(d.getUTCDate() + n)
  return d.toISOString().slice(0, 10)
}

const stepOf = (v) => 10 ** Math.floor(Math.log10(Math.max(1, Math.abs(v))))

/** Whether one source supports one specific on its own. */
function supports(p, it) {
  const textual = p.kind !== 'shell'
  switch (it.cls) {
    case 'url': case 'title': return textual && p.sq.includes(squeeze(it.key))
    // A quotation of a source must be in it word for word; one that restates the person may paraphrase them.
    case 'quote': return textual && (p.sq.includes(it.key) || (p.kind === 'request' && overlap(it.key, p.sq) >= 0.6))
    case 'phone': return textual && [it.key, `86${it.key}`, `1${it.key}`].some((k) => p.digitRuns.has(k))
    case 'docnum': case 'time': return textual && p.keys.has(it.key)
    // An article number counts only from a source that also names the same law.
    case 'article': return textual && p.keys.has(it.key) && (!it.law || p.sq.includes(it.law))
    case 'year': return textual && (p.keys.has(it.key) || p.keys.has(`year:${it.key}`) || p.values.has(Number(it.key)))
    case 'date': return textual && p.keys.has(`date:${it.key}`)
    case 'path': return false
    default: {
      if (p.kind === 'shell') {
        // Shell output is a computation; it supports a figure only when its own command did not write it.
        const digits = String(it.raw).replace(/[^\d.]/g, '')
        if (p.command.includes(String(round(it.value))) || (digits && p.command.includes(digits))) return false
        return p.values.has(round(it.value))
      }
      if (it.approx) {
        const lo = it.value
        const hi = it.value + stepOf(it.value)
        return [...(p.byClass.get(it.cls) ?? [])].some((v) => v >= lo && v < hi)
      }
      if (it.cls === 'num') return p.values.has(round(it.value))
      return p.keys.has(it.key)
    }
  }
}

const KNOWN = new Set(['supported', 'computed', 'derived'])

/**
 * Check a drafted answer against the person's message and the turn's tool results.
 * sources: strings (tool results) or { text, kind: 'tool' | 'shell', command?, tool? }.
 * @returns {{flagged: object[], counts: object, items: object[]}}
 */
export function checkDraft({ draft, request, sources = [], today }) {
  const items = extract(draft)
  const idx = buildIndex(request, sources)
  const textual = idx.parts.filter((p) => p.kind !== 'shell')
  const calc = calculations(draft, items)
  const year = Number((today || new Date().toISOString()).slice(0, 4))
  const draftText = normalize(draft)
  const lineOf = (i) => draftText.lastIndexOf('\n', i)
  const lineText = (i) => draftText.slice(lineOf(i) + 1, (draftText.indexOf('\n', i) + 1 || draftText.length + 1) - 1)
  const counts = { specifics: 0, supported: 0, computed: 0, derived: 0, dependent: 0, skipped: 0, flagged: 0 }
  const numberItems = items.filter((it) => typeof it.value === 'number')
  const requestValues = idx.parts.filter((p) => p.kind === 'request').flatMap((p) => [...p.values])
  const known = [...requestValues]
  const isKnown = (v, dec = 0) => CONSTANTS.has(v) || known.some((k) => Math.abs(k - v) <= 0.5 * 10 ** -dec + 1e-9)

  const dateSupported = (it) => {
    if (textual.some((p) => p.keys.has(`date:${it.key}`)) || (today && (it.key === today || it.key === today.slice(5)))) return true
    const knownDates = textual.flatMap((p) => [...p.keys].filter((k) => k.startsWith('date:')))
    // A year and month counted on from a date the person or a source gave (registered 2020-11, inspection 2026-11).
    if (it.key.length === 7) return knownDates.some((k) => k.startsWith(`date:${it.key}`) || k.slice(-5, -3) === it.key.slice(5) || k.slice(-2) === it.key.slice(5))
    // A date counted from a known date by a day count the sources or the person give (±1 for inclusive counting).
    // Month-day dates are read in this year and the next.
    const full = (k) => (k.length === 10 ? [k] : k.length === 5 ? [`${year}-${k}`, `${year + 1}-${k}`] : [])
    const bases = knownDates.filter((k) => /^date:(?:\d{4}-)?\d{2}-\d{2}$/.test(k)).flatMap((k) => full(k.slice(5)))
    if (today) bases.push(today)
    for (const target of full(it.key)) {
      for (const base of bases) for (const n of idx.dayCounts) for (const d of [n - 1, n, n + 1]) {
        if (addDays(base, d) === target || addDays(base, -d) === target) return true
      }
    }
    return false
  }
  const direct = (it) => {
    if (it.cls === 'path') {
      // Each label must appear in a source; a Latin label passes when its longer words all do.
      return it.raw.split(' > ').every((seg) => {
        const s = squeeze(seg)
        if (s.length < 2 || textual.some((p) => p.sq.includes(s))) return true
        const words = seg.toLowerCase().match(/[a-z]{4,}/g)
        return !/[㐀-鿿]/.test(seg) && !!words && words.every((w) => textual.some((p) => p.sq.includes(w)))
      })
    }
    if (it.cls === 'year' && Math.abs(Number(it.key) - year) <= 1) { it.source = 'today'; return true }
    if (it.cls === 'date') return dateSupported(it)
    const p = idx.parts.find((q) => supports(q, it))
    if (p) it.source = p.kind === 'tool' ? p.tool || 'tool' : p.kind
    return !!p
  }

  // Pass 1: direct support; trivial small numbers and schedule times are skipped.
  const pending = []
  for (const it of items) {
    if (typeof it.value === 'number' && TRIVIAL.has(it.cls) && Number.isInteger(it.value) && it.value <= 12) { it.status = 'skipped'; counts.skipped++; continue }
    // A bare calendar or scale constant (× 30, ÷ 365, × 100) is an operand, not a claim of its own.
    if (it.cls === 'num' && CONSTANTS.has(it.value)) { it.status = 'skipped'; counts.skipped++; continue }
    // A clock time is a claim only when it is about opening hours or slots; a dosing schedule is arithmetic.
    if (it.cls === 'time' && !/办公|上班时间|营业|开放|放号|抢号|窗口|受理|开门|关门|截止|hours|opens?|closes?|office|counter/i.test(lineText(it.index))) { it.status = 'skipped'; counts.skipped++; continue }
    counts.specifics++
    if (direct(it)) {
      it.status = 'supported'
      counts.supported++
      if (typeof it.value === 'number') known.push(it.value)
      continue
    }
    pending.push(it)
  }
  // Pass 2, repeated until nothing changes: a written calculation counts when every operand is known;
  // a figure counts as derived when one step of arithmetic makes it from known figures written near it.
  const knownYears = [year, ...textual.flatMap((p) => [...p.keys]).filter((k) => /^(?:year:|date:)?(?:19|20)\d{2}\b/.test(k)).map((k) => Number(k.replace(/^\w+:/, '').slice(0, 4)))]
  let changed = true
  while (changed) {
    changed = false
    for (const it of pending) {
      if (it.status) continue
      const c = calc.get(it.index)
      if (c) {
        if (!c.ok) { it.status = 'miscalculated'; it.note = c; continue }
        if (c.operands.every((o) => isKnown(o.value, o.decimals))) { it.status = 'computed'; counts.computed++; known.push(it.value); changed = true }
        continue
      }
      if (it.cls === 'year') {
        // A year counted on from a known year by a known number on the same line (2020 + 6 → 2026).
        const nums = numberItems.filter((o) => lineOf(o.index) === lineOf(it.index) && isKnown(o.value, o.decimals ?? 0)).map((o) => o.value)
        if (knownYears.some((y) => nums.includes(Math.abs(Number(it.key) - y)))) { it.status = 'derived'; counts.derived++; changed = true }
        continue
      }
      if (typeof it.value !== 'number') continue
      // The same figure stated again after the answer established it ("少算了你300元" before "6525 ÷ 21.75 = 300元").
      const established = items.filter((o) => o !== it && KNOWN.has(o.status) && typeof o.value === 'number').map((o) => o.value)
      if (it.value >= 13 && established.some((v) => Math.abs(v - it.value) <= 0.5 * 10 ** -(it.decimals ?? 0) + 1e-9)) {
        it.status = 'derived'
        counts.derived++
        changed = true
        continue
      }
      const lo = lineOf(lineOf(it.index) - 1)
      // Operands must have support of their own (or be small numbers written beside it); a figure that merely
      // equals a constant does not make a stated figure derived.
      const near = numberItems
        .filter((o) => o !== it && o.index > lo && o.index < it.index + 40 && (KNOWN.has(o.status) || o.status === 'skipped'))
        .map((o) => o.value)
      const pool = [...new Set([...near, ...requestValues])]
      const dec = it.decimals ?? 0
      let found = false
      outer: for (const a of pool) for (const b of pool) {
        for (const v of [a + b, a - b, a * b, b ? a / b : NaN, (a * b) / 100, a * (1 - b / 100), a * (1 + b / 100)]) {
          if (closeEnough(it.value, dec, v, false)) { found = true; break outer }
        }
      }
      if (found) { it.status = 'derived'; counts.derived++; known.push(it.value); changed = true }
    }
  }
  const flagged = []
  for (const it of pending) {
    // A correct calculation from figures that lack support: the figures are listed, not the result.
    if (!it.status && calc.get(it.index)?.ok) { it.status = 'dependent'; counts.dependent++; continue }
    if (!it.status) it.status = 'unsupported'
    if (it.status === 'unsupported' || it.status === 'miscalculated') { counts.flagged++; flagged.push(it) }
  }
  // One entry per distinct specific, most checkable kinds first.
  const ORDER = ['miscalculated', 'phone', 'url', 'docnum', 'article', 'title', 'quote', 'path', 'date', 'money', 'percent', 'times', 'points', 'days', 'months', 'years', 'year', 'time']
  const rank = (it) => {
    const r = ORDER.indexOf(it.status === 'miscalculated' ? 'miscalculated' : it.cls)
    return r < 0 ? ORDER.length : r
  }
  const seen = new Set()
  const unique = flagged.filter((it) => (seen.has(it.key + it.status) ? false : seen.add(it.key + it.status)))
  unique.sort((a, b) => rank(a) - rank(b) || a.index - b.index)
  return { flagged: unique, counts, items }
}

const KIND = {
  'zh-CN': { url: '链接', phone: '电话', docnum: '文件号', article: '条文号', quote: '引用的原话', path: '操作路径', date: '日期', year: '年份', time: '时间', money: '金额', percent: '百分比', times: '倍数', points: '分值', num: '数字' },
  en: { url: 'link', phone: 'phone number', docnum: 'document number', article: 'article or section number', quote: 'quoted wording', path: 'menu path', date: 'date', year: 'year', time: 'time', money: 'amount', percent: 'percentage', times: 'multiple', points: 'points', num: 'number' },
  ja: { url: 'リンク', phone: '電話番号', docnum: '文書番号', article: '条文番号', quote: '引用した文言', path: '操作手順', date: '日付', year: '年', time: '時刻', money: '金額', percent: '割合', times: '倍数', points: '点数', num: '数字' },
  ko: { url: '링크', phone: '전화번호', docnum: '문서 번호', article: '조문 번호', quote: '인용한 문구', path: '메뉴 경로', date: '날짜', year: '연도', time: '시각', money: '금액', percent: '비율', times: '배수', points: '점수', num: '숫자' },
}

const STEER = {
  'zh-CN': {
    head: '【Gravitas 核对】这是回复发出前的自动核对，不是用户的新问题。你的草稿里有下面这些具体内容，在用户的消息和本轮的工具结果里都找不到出处，也不是由有出处的数字在草稿里算出来的：',
    miscalc: (it) => `算式“${it.note.expr}”得 ${fmt(it.note.actual)}，不是 ${it.raw}`,
    tail: '逐条处理：用户要依赖的，现在用工具查官方出处，查到了再保留；是从用户给的数字算出来的，把算式写出来并算对；查不到的，删掉，或者改成用户自己能去确认的说法（例如写“打当地12345问”，而不写具体电话），不要加“可能”“以当地为准”之类的搪塞话。其余内容不动，篇幅不要变长。然后重新给出完整的最终回复，用回复原本的语言，不要提这次核对。',
  },
  en: {
    head: '[Gravitas check] This is an automatic check before the reply is sent, not a new question from the user. Your draft contains the specifics below, which appear neither in the user\'s message nor in any tool result of this turn, and which the draft does not calculate from numbers that do:',
    miscalc: (it) => `the calculation "${it.note.expr}" gives ${fmt(it.note.actual)}, not ${it.raw}`,
    tail: 'Handle each one: if the user will rely on it, look up an official source with a tool now and keep it only if the source confirms it; if it comes from the user\'s numbers, write out the calculation and get it right; otherwise cut it, or loosen it to something the user can confirm themselves (for example "call the agency" without a number you have not seen). Do not add hedges such as "may" or "check locally". Leave everything else as it is and do not make the reply longer. Then give the complete final reply again, in the reply\'s own language, without mentioning this check.',
  },
  ja: {
    head: '【Gravitas 確認】これは返信を送る前の自動確認で、ユーザーからの新しい質問ではありません。下書きにある次の具体的な内容は、ユーザーのメッセージにも、このターンのツール結果にも出典がなく、出典のある数字から下書きの中で計算されたものでもありません：',
    miscalc: (it) => `計算「${it.note.expr}」は ${fmt(it.note.actual)} になり、${it.raw} ではありません`,
    tail: '一つずつ処理してください。ユーザーが頼りにするものは、今ツールで公式の出典を調べ、確認できたものだけ残す。ユーザーの数字から計算したものは、計算式を書いて正しく計算する。確認できないものは削るか、ユーザー自身が確かめられる言い方にする（見ていない電話番号は書かず「窓口に問い合わせる」とする）。「かもしれない」「地域による」のようなごまかしは足さない。ほかの部分は変えず、長くしない。そのうえで、最終的な返信を元の言語でもう一度すべて書き、この確認には触れないでください。',
  },
  ko: {
    head: '[Gravitas 확인] 답변을 보내기 전의 자동 확인이며, 사용자의 새 질문이 아닙니다. 초안의 아래 구체적인 내용은 사용자 메시지에도, 이번 턴의 도구 결과에도 출처가 없고, 출처가 있는 숫자로 초안 안에서 계산한 것도 아닙니다:',
    miscalc: (it) => `계산 "${it.note.expr}"의 결과는 ${fmt(it.note.actual)}이며 ${it.raw}가 아닙니다`,
    tail: '하나씩 처리하세요. 사용자가 의지할 내용은 지금 도구로 공식 출처를 찾아 확인된 것만 남기고, 사용자가 준 숫자로 계산한 것은 계산식을 쓰고 바르게 계산하고, 확인할 수 없는 것은 지우거나 사용자가 직접 확인할 수 있는 표현으로 바꾸세요(보지 않은 전화번호 대신 "해당 기관에 문의"). "그럴 수 있다", "지역마다 다르다" 같은 얼버무림은 넣지 마세요. 나머지는 그대로 두고 길게 늘리지 마세요. 그런 다음 최종 답변 전체를 원래 언어로 다시 쓰고, 이 확인은 언급하지 마세요.',
  },
}

function fmt(v) {
  return Number.isInteger(v) ? String(v) : String(Math.round(v * 100) / 100)
}

/** The language of the steering message: from the user's own text, else the configured one. */
export function steerLanguage(request, configured = 'en') {
  const t = String(request ?? '')
  if (/[぀-ヿ]/.test(t)) return 'ja'
  if (/[가-힯]/.test(t)) return 'ko'
  if (/[㐀-鿿]/.test(t)) return 'zh-CN'
  if (/[A-Za-z]/.test(t)) return 'en'
  return STEER[configured] ? configured : 'en'
}

/** The steering message for a list of flagged specifics, or '' when there is nothing to steer. */
export function steerText(flagged, language = 'en', limit = 15) {
  if (!flagged.length) return ''
  const s = STEER[language] ?? STEER.en
  const k = KIND[language] ?? KIND.en
  const lines = flagged.slice(0, limit).map((it, i) => {
    if (it.status === 'miscalculated') return `${i + 1}. ${s.miscalc(it)}`
    return `${i + 1}. ${it.raw.trim().slice(0, 80)} (${k[it.cls] ?? k.num})`
  })
  return `${s.head}\n${lines.join('\n')}\n${s.tail}`
}
