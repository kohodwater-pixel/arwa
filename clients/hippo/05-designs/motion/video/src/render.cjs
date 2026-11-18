#!/usr/bin/env node
/* Renders src/index.html frame by frame with Chromium (Playwright) — no real-time clock involved.
   Full film :  node render.cjs frames <out-dir> [fromFrame] [toFrame]     -> <out-dir>/f_00000.png ... (30 fps)
   Stills    :  node render.cjs stills <out-dir> 0.5 1.05 2.5 ...          -> <out-dir>/still_<t>.png
   Options   :  GUIDES=1 (safe-area guides)  BLINK=1 (optional logo blink)  WORKERS=4
   Then build.sh encodes the frames and muxes the approved audio. */
const path = require('path'), fs = require('fs');
let chromium; try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }
const FPS = 30, DUR = 40;
(async () => {
  const [mode, outDir, ...rest] = process.argv.slice(2);
  if (!mode || !outDir) { console.error('usage: render.cjs frames|stills <out-dir> ...'); process.exit(1); }
  fs.mkdirSync(outDir, { recursive: true });
  const qs = ['render=1']; if (process.env.GUIDES) qs.push('guides=1'); if (process.env.BLINK) qs.push('blink=1');
  const url = 'file://' + path.join(__dirname, 'index.html') + '?' + qs.join('&');
  const browser = await chromium.launch();
  const open = async () => {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 2; });
    await page.goto(url); await page.evaluate(() => window.ready);
    return page;
  };
  const shot = async (page, t, file) => { await page.evaluate(tt => window.seek(tt), t); await page.screenshot({ path: file, clip: { x: 0, y: 0, width: 1080, height: 1920 } }); };
  if (mode === 'stills') {
    const page = await open();
    console.log('fonts:', JSON.stringify(await page.evaluate(() => window.fontsOk)));
    for (const s of rest) { const t = parseFloat(s); await shot(page, t, path.join(outDir, `still_${t.toFixed(3).padStart(6, '0')}.png`)); }
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
