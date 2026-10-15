// Loads the built index.html in headless Chromium and fails (exit 1) if the site would ship broken.
//   node tools/sync/smoke.cjs index.html
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

(async () => {
  const file = 'file://' + path.resolve(process.argv[2] || 'index.html');
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const errors = [];
  const check = async (viewport, label) => {
    const p = await (await b.newContext({ viewport })).newPage();
    await p.route(/^https?:/, r => r.abort());  // fonts are external; everything else must be inside the file
    p.on('pageerror', e => errors.push(label + ' pageerror: ' + e.message));
    p.on('console', m => { if (m.type() === 'error' && !/ERR_FAILED|net::/.test(m.text())) errors.push(label + ' console: ' + m.text()); });
    await p.goto(file, { waitUntil: 'load' });
    await p.waitForTimeout(11500);  // the opening always finishes by 10.5s
    const s = await p.evaluate(() => ({
      libs: !!(window.gsap && window.ScrollTrigger && window.Lenis),
      opened: !document.getElementById('pre'),
      silk: !!document.getElementById('silk'),
      tabs: document.querySelectorAll('#tabs .tab').length,
      editor: !!document.getElementById('editor'),
      overflow: document.documentElement.scrollWidth > innerWidth
    }));
    if (!s.libs) errors.push(label + ': GSAP / ScrollTrigger / Lenis missing');
    if (!s.opened) errors.push(label + ': opening never finished');
    if (!s.silk) errors.push(label + ': hero missing');
    if (s.tabs < 1) errors.push(label + ': works tabs missing');
    if (s.editor) errors.push(label + ': Artifact-only editor leaked into the site');
    if (s.overflow) errors.push(label + ': horizontal overflow');
    console.log(label, JSON.stringify(s));
  };
  await check({ width: 1440, height: 900 }, 'desktop');
  await check({ width: 390, height: 844 }, 'mobile');
  await b.close();
  if (errors.length) { console.error('SMOKE FAILED\n' + errors.join('\n')); process.exit(1); }
  console.log('SMOKE OK');
})().catch(e => { console.error('SMOKE FAILED', e); process.exit(1); });
