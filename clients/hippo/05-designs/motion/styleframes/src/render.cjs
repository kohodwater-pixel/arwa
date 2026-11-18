#!/usr/bin/env node
/* Renders the twelve style frames from styleframes.html with Chromium (Playwright).
   node render.cjs [ids...]   -> ../hippo_franchise-motion-ad_styleframe-<a|b|c>-<1..4>_ar_v01.png
   Also writes ../_work/bg_<id>.png (same frame with all text hidden) and ../_work/metrics.json
   (rectangle, colour and font of every text element) for check.py (contrast and safe areas). */
const path = require('path'), fs = require('fs');
let chromium; try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }
const ALL = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4'];
(async () => {
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ALL;
  const out = path.join(__dirname, '..'), work = path.join(out, '_work'); fs.mkdirSync(work, { recursive: true });
  const mfile = path.join(work, 'metrics.json');
  const metrics = fs.existsSync(mfile) ? JSON.parse(fs.readFileSync(mfile, 'utf8')) : {};
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 2; });
  for (const id of ids) {
    const base = 'file://' + path.join(__dirname, 'styleframes.html') + '?f=' + id;
    await page.goto(base); await page.evaluate(() => window.ready);
    const clip = { x: 0, y: 0, width: 1080, height: 1920 };
    await page.screenshot({ path: path.join(out, `hippo_franchise-motion-ad_styleframe-${id[0]}-${id[1]}_ar_v01.png`), clip });
    metrics[id] = await page.evaluate(() => ({
      fonts: window.fontsOk,
      texts: [...document.querySelectorAll('.frame.on .t')].map(el => {
        const r = el.getBoundingClientRect(), cs = getComputedStyle(el.querySelector('[data-fit]') || el);
        return { text: el.innerText.replace(/\n/g, ' '), x: r.x, y: r.y, w: r.width, h: r.height, color: cs.color, size: cs.fontSize, weight: cs.fontWeight, family: cs.fontFamily, spacing: cs.letterSpacing };
      }),
      imgs: [...document.querySelectorAll('.frame.on img')].map(el => { const r = el.getBoundingClientRect(); return { src: el.getAttribute('src'), natural: el.naturalWidth, shown: el.offsetWidth, x: r.x, y: r.y, w: r.width, h: r.height }; })
    }));
    await page.goto(base + '&notext=1'); await page.evaluate(() => window.ready);
    await page.screenshot({ path: path.join(work, `bg_${id}.png`), clip });
    console.log(id, 'fonts', JSON.stringify(metrics[id].fonts));
  }
  fs.writeFileSync(mfile, JSON.stringify(metrics, null, 1));
  await browser.close();
})();
