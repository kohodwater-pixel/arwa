#!/usr/bin/env node
/* Renders src/index.html frame by frame with Chromium (Playwright) — no real-time clock involved.
   Full film :  node render.cjs frames <out-dir> [fromFrame] [toFrame]     -> <out-dir>/f_00000.png ... (30 fps)
   Stills    :  node render.cjs stills <out-dir> 0.5 1.03 2.5 ...          -> <out-dir>/still_<t>.png  (t snapped to its frame)
   Check     :  node render.cjs check <out-dir> 2.5 8.3 ...                -> still + text-hidden twin + metrics.json (for check.py)
   Options   :  WORKERS=4 */
const path = require('path'), fs = require('fs');
let chromium; try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }
const FPS = 30, DUR = 40;
(async () => {
  const [mode, outDir, ...rest] = process.argv.slice(2);
  if (!mode || !outDir) { console.error('usage: render.cjs frames|stills|check <out-dir> ...'); process.exit(1); }
  fs.mkdirSync(outDir, { recursive: true });
  const base = 'file://' + path.join(__dirname, 'index.html') + '?render=1';
  const browser = await chromium.launch();
  const open = async (extra = '') => {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 2; });
    await page.goto(base + extra); await page.evaluate(() => window.ready);
    return page;
  };
  const clip = { x: 0, y: 0, width: 1080, height: 1920 };
  const shot = async (page, t, file) => { await page.evaluate(tt => window.seek(tt), t); await page.screenshot({ path: file, clip }); };
  const snap = s => Math.round(parseFloat(s) * FPS) / FPS;
  const name = t => t.toFixed(3).padStart(6, '0');
  if (mode === 'stills') {
    const page = await open();
    console.log('fonts:', JSON.stringify(await page.evaluate(() => window.fontsOk)));
    for (const s of rest) { const t = snap(s); await shot(page, t, path.join(outDir, `still_${name(t)}.png`)); }
  } else if (mode === 'check') {
    const page = await open(), bare = await open('&notext=1'), metrics = {};
    for (const s of rest) {
      const t = snap(s);
      await shot(page, t, path.join(outDir, `chk_${name(t)}.png`)); await shot(bare, t, path.join(outDir, `chk_${name(t)}_bg.png`));
      metrics[name(t)] = await page.evaluate(() => [...document.querySelectorAll('.t')].filter(el => el.offsetParent !== null).map(el => {
        let o = 1; for (let e = el; e && e.id !== 'stage'; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity);
        const r = el.getBoundingClientRect(), cs = getComputedStyle(el.querySelector('[data-fit]') || el);
        return { text: el.innerText.replace(/\n/g, ' '), x: r.x, y: r.y, w: r.width, h: r.height, color: getComputedStyle(el).color, size: cs.fontSize, weight: cs.fontWeight, family: cs.fontFamily, spacing: cs.letterSpacing, opacity: o };
      }).filter(m => m.opacity > 0.99));
    }
    fs.writeFileSync(path.join(outDir, 'metrics.json'), JSON.stringify(metrics, null, 1));
  } else {
    const from = parseInt(rest[0] || '0', 10), to = parseInt(rest[1] || String(FPS * DUR - 1), 10), n = parseInt(process.env.WORKERS || '4', 10);
    let next = from, done = 0;
    await Promise.all(Array.from({ length: n }, async () => {
      const page = await open();
      for (;;) { const f = next++; if (f > to) break; await shot(page, f / FPS, path.join(outDir, `f_${String(f).padStart(5, '0')}.png`)); if (++done % 100 === 0) console.log(done, 'frames'); }
    }));
    console.log('rendered frames', from, '-', to);
  }
  await browser.close();
})();
