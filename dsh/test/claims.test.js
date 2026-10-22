// Tests for the claim check in dsh/lib/claims.js. Run: node --test dsh/test/claims.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { cnToNumber, extract, evaluate, calculations, checkDraft, steerText, steerLanguage, overlap } from '../lib/claims.js'

const flaggedRaw = (input) => checkDraft({ today: '2026-10-22', sources: [], ...input }).flagged.map((it) => it.raw)

test('Chinese numerals', () => {
  assert.equal(cnToNumber('三十七'), 37)
  assert.equal(cnToNumber('十五'), 15)
  assert.equal(cnToNumber('一万二千'), 12000)
  assert.equal(cnToNumber('三百'), 300)
  assert.equal(cnToNumber('二〇二六'), 2026)
  assert.ok(Number.isNaN(cnToNumber('三个')))
})

test('the arithmetic parser reads + - * / and parentheses, and nothing else', () => {
  assert.equal(evaluate('3*300*(300/100)'), 2700)
  assert.equal(evaluate('(3*3+4*2)*300'), 5100)
  assert.equal(evaluate('-2+5'), 3)
  assert.ok(Number.isNaN(evaluate('2+')))
  assert.ok(Number.isNaN(evaluate('process.exit()')))
})

test('extract: each kind of specific, with list markers and links left out', () => {
  const items = extract([
    '1. 依据《劳动法》第四十四条和国办发〔2025〕7号，2026年10月26日起，三十日内。',
    '2. 打 020-12345678 或 1-800-772-1213，见 https://www.example.gov.cn/a/123.html 。',
    '3. 原文是“劳动者提前三十日以书面形式通知用人单位”。路径：首页 → 学法减分 → 网上学习',
    '4. 月薪1.2万，涨了15%，补3倍，$3,400 and 7 business days, Section 2302(c).',
  ].join('\n'))
  const kinds = (cls) => items.filter((i) => i.cls === cls).map((i) => i.key)
  assert.deepEqual(kinds('article'), ['art-44', 'sec-2302'])
  assert.deepEqual(kinds('docnum'), ['2025-7'])
  assert.deepEqual(kinds('date'), ['2026-10-26'])
  assert.deepEqual(kinds('phone'), ['02012345678', '8007721213'])
  assert.deepEqual(kinds('url'), ['www.example.gov.cn/a/123.html'])
  assert.deepEqual(kinds('quote'), ['劳动者提前三十日以书面形式通知用人单位'])
  assert.deepEqual(kinds('path'), ['首页>学法减分>网上学习'])
  assert.ok(kinds('days').includes('days:30'))
  assert.ok(items.some((i) => i.value === 12000) && kinds('money').includes('money:3400'))
  assert.ok(kinds('percent').includes('percent:15') && kinds('times').includes('times:3'))
  assert.ok(!items.some((i) => i.key === 'num:1' || i.key === 'num:4'), 'list markers are not specifics')
  assert.ok(!items.some((i) => i.key === 'num:123'), 'digits inside a link are not specifics')
})

test('calculations: a right sum passes, a wrong one is caught, chains are read link by link', () => {
  const draft = '日工资 6525 ÷ 21.75 = 300元；3 × 300 × 300% = 2700元；(3×3 + 4×2) × 300 = 17 × 300 = 5100元；4 × 551.72 × 2 = 4500元'
  const items = extract(draft)
  const calc = calculations(draft, items)
  const at = (raw) => calc.get(items.find((i) => i.raw === raw).index)
  assert.equal(at('300元').ok, true)
  assert.equal(at('2700元').ok, true)
  assert.equal(at('5100元').ok, true)
  assert.equal(at('4500元').ok, false)
  assert.equal(Math.round(at('4500元').actual * 100) / 100, 4413.76)
  assert.equal(calculations('($38,000 − $24,480) / 2 = $6,760', extract('($38,000 − $24,480) / 2 = $6,760')).size, 1)
  // Words between two figures (and the Chinese comma) end the left side; the figures never merge.
  const zh = '我按自己的月工资6525元算了一下，日工资是6525÷21.75 = 300元'
  const zhItems = extract(zh)
  const r = calculations(zh, zhItems).get(zhItems.find((i) => i.raw === '300元').index)
  assert.equal(r.ok, true)
  assert.deepEqual(r.operands.map((o) => o.value), [6525, 21.75])
  for (const [line, raw] of [
    ['**日工资**：6,525 ÷ 21.75 = **300元/天**（21.75是法定月计薪天数）。', '300元'],
    ['| 10月1日—3日 | 法定节假日 | 3天 | 另付300% | 300×300%×3＝**2,700元** |', '2,700元'],
    ['- 应纳税所得额：120,000 - 12,000 = 108,000', '108,000'],
  ]) {
    const its = extract(line)
    assert.equal(calculations(line, its).get(its.find((i) => i.raw === raw).index)?.ok, true, line)
  }
  const days = '从7月1日到今天10月22日共114天，按日万分之五，380×0.05%×114 = 21.66元'
  const dItems = extract(days)
  assert.equal(calculations(days, dItems).get(dItems.find((i) => i.raw === '21.66元').index).ok, true)
})

test('support: the person\'s message, tool results (Chinese or Arabic numerals), and calculations from them', () => {
  const flagged = flaggedRaw({
    request: '我月薪6525元，10月26日交辞职信。',
    sources: ['劳动者提前三十日以书面形式通知用人单位，可以解除劳动合同。日工资按21.75天折算。第三十七条'],
    draft: '依据第三十七条，提前30日通知即可，最早11月25日离职。日工资 6525 ÷ 21.75 = 300元。可打 0571-12345678 咨询，经济补偿按第四十七条。',
  })
  assert.deepEqual(flagged, ['0571-12345678', '第四十七条'])
})

test('support: a quotation restating the person may paraphrase; a quotation of a source may not', () => {
  const request = '劳动合同里写着："员工辞职须提前60天书面申请，经公司批准后方可离职。"'
  assert.deepEqual(flaggedRaw({ request, draft: '合同写的“员工辞职须提前60天书面申请经批准方可离职”这一条约束不了你。' }), [])
  assert.deepEqual(flaggedRaw({ request, draft: '《劳动合同法》写明“用人单位不得以任何理由拒绝劳动者辞职”。' }), ['“用人单位不得以任何理由拒绝劳动者辞职”'])
  assert.ok(overlap('abcd', 'xxabcdxx') === 1 && overlap('abcd', 'wxyz') === 0)
})

test('not listed: small plain numbers, dosing times, rough ranges, today\'s year, years counted from the person\'s year', () => {
  const flagged = flaggedRaw({
    request: '车是2020年11月上的牌。妈妈每4小时吃2片。',
    draft: '每次2片，8:00、12:00、16:00各一次，最多3次。检测费两三百元。2026年11月到期，2020 + 6 = 2026，2024年也要申领。',
  })
  assert.deepEqual(flagged, [])
})

test('listed: opening hours, invented app menu paths, unsourced statute sections and amounts', () => {
  const flagged = flaggedRaw({
    request: 'Can I get my money back? The ticket was $412.',
    draft: 'Under 14 CFR 260.6 you get the $412 back within 7 business days, plus a $75 meal voucher. The counter opens at 5:30. Tap Trips > Cancel flight > Refund.',
  })
  assert.deepEqual(flagged.sort(), ['$75', '14 CFR 260.6', '5:30', '7 business days', 'Trips > Cancel flight > Refund'].sort())
})

test('dates counted from a known date by a day count from the sources are supported', () => {
  const sources = ['应当自受理之日起六十日内办结']
  assert.deepEqual(flaggedRaw({ request: '我10月26日交的申请', sources, draft: '最晚12月25日办结。' }), [])
  assert.deepEqual(flaggedRaw({ request: '我10月26日交的申请', sources, draft: '最晚12月31日办结。' }), ['12月31日'])
})

test('steer text: four languages, numbered items, a calculation note, and a demand for the complete reply', () => {
  const { flagged } = checkDraft({ draft: '打 020-12345678。4 × 551.72 × 2 = 4500元', request: '你好', sources: [] })
  for (const [lang, demand] of [['zh-CN', /完整的最终回复/], ['en', /complete final reply/], ['ja', /最終的な返信/], ['ko', /최종 답변 전체/]]) {
    const t = steerText(flagged, lang)
    assert.match(t, demand, lang)
    assert.match(t, /020-12345678/, lang)
    assert.match(t, /4413\.76/, lang)
    assert.match(t, /^1\. /m, lang)
  }
  assert.equal(steerText([], 'en'), '')
  const many = Array.from({ length: 30 }, (_, i) => ({ cls: 'money', raw: `$${i + 100}`, key: `k${i}` }))
  assert.equal(steerText(many, 'en').match(/^\d+\. /gm).length, 15, 'at most 15 items')
})

// The cheapest passes an independent review found in an earlier version; each must now be caught.
test('cheapest pass: invented figures do not support each other through arithmetic', () => {
  assert.deepEqual(flaggedRaw({ request: '帮我看看', draft: '罚款200元，是标准的10倍，即2000元' }).sort(), ['10倍', '2000元', '200元'].sort())
  assert.deepEqual(flaggedRaw({ request: '帮我看看', draft: '每天加收滞纳金50元，30天共1500元' }).sort(), ['1500元', '30天', '50元'].sort())
  assert.deepEqual(flaggedRaw({ request: '帮我看看', draft: '50元 × 30 = 1500元' }), ['50元'], 'a correct sum from an invented figure lists the figure')
  assert.deepEqual(flaggedRaw({ request: '帮我看看', draft: '赔偿8000元，也就是8000元整' }), ['8000元'])
  assert.deepEqual(flaggedRaw({ request: '帮我看看', draft: '工本费20元，加急费40元，快递费20元，押金60元' }).sort(), ['20元', '40元', '60元'].sort())
})

test('cheapest pass: a source supports only what it states, in the same class', () => {
  const sources = ['本网点去年接待3500人次，网点80个，满意度35分。订单号4008201234567。']
  assert.deepEqual(flaggedRaw({ request: '帮我看看', sources, draft: '罚款3500元，补办80元，退款35%，客服400-820-1234。' }).sort(),
    ['3500元', '35%', '400-820-1234', '80元'].sort())
  const law = ['《中华人民共和国劳动法》第三十七条 对实行计件工作的劳动者……']
  assert.deepEqual(flaggedRaw({ request: '能辞职吗', sources: law, draft: '依据《劳动合同法》第三十七条，可以辞职。' }), ['第三十七条'])
  assert.deepEqual(flaggedRaw({ request: '能辞职吗', sources: ['劳动合同法 第三十七条 劳动者提前三十日以书面形式通知用人单位'], draft: '依据《劳动合同法》第三十七条，可以辞职。' }), [])
  const excerpt = ['第三十八条 用人单位有下列情形之一的，劳动者可以解除劳动合同：（二）未及时足额支付劳动报酬的']
  assert.deepEqual(flaggedRaw({ request: '能辞职吗', sources: excerpt, draft: '法律写明“未及时足额支付劳动报酬的，劳动者可以提前三日以书面形式解除”。' }).length, 1, 'a quotation stitched from a source\'s words is listed')
})

test('cheapest pass: shell output never supports what its own command wrote', () => {
  const echo = { kind: 'shell', command: 'Write-Output "0571-12345678 3500元"', text: '0571-12345678 3500元' }
  assert.deepEqual(flaggedRaw({ request: '帮我看看', sources: [echo], draft: '打 0571-12345678，罚款3500元。' }).sort(), ['0571-12345678', '3500元'].sort())
  const calc = { kind: 'shell', command: '[math]::Round(12000/21.75, 2)', text: '551.72' }
  assert.deepEqual(flaggedRaw({ request: '月薪12000', sources: [calc], draft: '日工资551.72元。' }), [], 'a computed result is support')
})

test('cheapest pass: specifics written in words, ranges, durations, other quote marks and menu forms are still read', () => {
  const flagged = flaggedRaw({
    request: '帮我看看',
    draft: '提前一个月通知，扣十二分，罚款两百块，二十多天办好，10个工作日内，保修12个月。Refunds take thirty days and cost five hundred dollars. 他说‘公司有权不批准任何辞职申请’。依据《关于简化提取已故存款人小额存款相关事宜的通知》。点击“我的”，再点“驾驶证”，或者走 我的/驾驶证/记分查询。',
  })
  for (const raw of ['一个月', '十二分', '两百块', '二十多天', '10个工作日', '12个月', 'thirty days', 'five hundred dollars']) {
    assert.ok(flagged.includes(raw), `${raw} is listed (got ${flagged.join(' | ')})`)
  }
  assert.ok(flagged.some((r) => r.includes('公司有权不批准任何辞职申请')), 'single-quoted wording')
  assert.ok(flagged.some((r) => r.includes('小额存款相关事宜的通知')), 'document title')
  assert.ok(flagged.includes('我的 > 驾驶证'), 'tapped labels')
  assert.ok(flagged.includes('我的 > 驾驶证 > 记分查询'), 'slash path')
  assert.deepEqual(flaggedRaw({ request: '帮我看看', sources: ['一般需要25个工作日办结'], draft: '大约20多个工作日办好。' }), [], 'an approximate figure is supported by a value in its range')
})

test('steer language follows the person\'s own text', () => {
  assert.equal(steerLanguage('帮我算一下'), 'zh-CN')
  assert.equal(steerLanguage('Can you help?', 'zh-CN'), 'en')
  assert.equal(steerLanguage('助けてください'), 'ja')
  assert.equal(steerLanguage('도와주세요'), 'ko')
  assert.equal(steerLanguage('123', 'ko'), 'ko')
})
