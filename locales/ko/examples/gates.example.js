// Acceptance gates written to the rules in gravitas/references/acceptance.md.
// Every gate states a failing condition and is evaluated, not asserted in prose.
// Exits non-zero if any gate fails. Run: node scripts/gates.js
import { chromium } from 'playwright';

const URL = 'http://localhost:4173/';
const results = [];

function gate(id, requirement, pass, detail) {
  results.push({ id, requirement, pass: !!pass, detail });
}

const run = async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  // Console is asserted on, not collected and forgotten.
  const consoleMsgs = [];
  page.on('console', (m) => consoleMsgs.push({ type: m.type(), text: m.text() }));
  page.on('pageerror', (e) => consoleMsgs.push({ type: 'pageerror', text: String(e) }));

  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.__SCENE_TEST__ !== undefined, { timeout: 15000 });
  await page.waitForTimeout(2500);

  // ---- G1: no console errors -------------------------------------------------
  const errors = consoleMsgs.filter((m) => m.type === 'error' || m.type === 'pageerror');
  gate('G1', 'Zero console errors', errors.length === 0,
       errors.length ? errors.map((e) => e.text).join(' | ') : 'none');

  // ---- G2: no deprecation naming an API we call ------------------------------
  const deprecations = consoleMsgs.filter(
    (m) => /has been removed|deprecat|no longer supported/i.test(m.text));
  gate('G2', 'No deprecation warning for an API this code calls',
       deprecations.length === 0,
       deprecations.length ? deprecations.map((d) => d.text.trim()).join(' | ') : 'none');

  // ---- G3: shadows actually enabled and soft --------------------------------
  const shadow = await page.evaluate(() => {
    const r = window.__APP__?.renderer;
    if (!r) return null;
    return { enabled: r.shadowMap.enabled, type: r.shadowMap.type };
  });
  // THREE: BasicShadowMap 0, PCFShadowMap 1, VSMShadowMap 3
  gate('G3', 'Shadow map enabled and not the hard fallback (type !== 1)',
       shadow && shadow.enabled && shadow.type !== 1,
       shadow ? `enabled=${shadow.enabled} type=${shadow.type}` : 'renderer not reachable');

  // ---- G4: material variety (a scene of one flat material reads as plastic) --
  const mats = await page.evaluate(() => {
    const seen = new Map();
    let flat = 0, total = 0;
    window.__APP__?.scene?.traverse((o) => {
      if (!o.isMesh || !o.material) return;
      const list = Array.isArray(o.material) ? o.material : [o.material];
      for (const m of list) {
        total++;
        seen.set(m.type, (seen.get(m.type) || 0) + 1);
        const hasMap = !!(m.map || m.normalMap || m.roughnessMap || m.bumpMap);
        if (!hasMap) flat++;
      }
    });
    return { types: [...seen.entries()], total, flat };
  });
  const flatRatio = mats.total ? mats.flat / mats.total : 1;
  gate('G4', 'Under 90% of materials are untextured (texture-free scenes read as plastic)',
       flatRatio < 0.9,
       `${mats.flat}/${mats.total} materials have no map (${(flatRatio * 100).toFixed(1)}%); types=${JSON.stringify(mats.types)}`);

  // ---- G5: component counts, compared rather than narrated ------------------
  const counts = await page.evaluate(() => window.__SCENE_TEST__.getComponentCounts());
  const expected = { carriers: 10, rollers: 6, foilLeaves: 4 };
  const mismatches = Object.entries(expected)
    .filter(([k, v]) => counts[k] !== v)
    .map(([k, v]) => `${k}: expected ${v}, got ${counts[k]}`);
  gate('G5', 'Component counts match the brief', mismatches.length === 0,
       mismatches.length ? mismatches.join('; ') : JSON.stringify(counts));

  // ---- G6: self-test, prove a gate can go red ------------------------------
  // Deliberately corrupt a value and confirm the comparison catches it.
  const selfTest = (() => {
    const fakeCounts = { ...counts, carriers: counts.carriers + 1 };
    return Object.entries(expected).some(([k, v]) => fakeCounts[k] !== v);
  })();
  gate('G6', 'SELF-TEST: an injected wrong value is detected by G5 logic', selfTest,
       selfTest ? 'injected carriers+1 and the comparison flagged it' : 'comparison did NOT flag a wrong value');

  await browser.close();

  const failed = results.filter((r) => !r.pass);
  console.log('\n=== ACCEPTANCE GATES ===');
  for (const r of results) {
    console.log(`  ${r.pass ? 'PASS' : 'FAIL'}  ${r.id}  ${r.requirement}`);
    console.log(`        ${r.detail}`);
  }
  console.log(`\n  ${results.length - failed.length}/${results.length} passed, ${failed.length} failed`);
  console.log('  NOT COVERED: perceptual judgement (material read, lighting, recognisability).');
  console.log('               That requires a critic looking at the image and cannot be scripted.\n');

  if (failed.length) process.exit(1);
};

run().catch((e) => { console.error('harness error:', e); process.exit(2); });
