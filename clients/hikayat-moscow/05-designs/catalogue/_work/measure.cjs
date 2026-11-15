// Usage: node measure.cjs measure <html> <out.json>   -> heights (mm) of every [data-block]
//        node measure.cjs check <html> <out.json>     -> overflow report for every .page
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
(async () => {
  const [mode, html, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 1200 } });
  await page.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const MM = 96 / 25.4;
  let res;
  if (mode === 'measure') {
    res = await page.evaluate((MM) => {
      const o = {};
      document.querySelectorAll('[data-block]').forEach(el => { o[el.dataset.block] = el.getBoundingClientRect().height / MM; });
      return o;
    }, MM);
  } else {
    res = await page.evaluate((MM) => {
      const probs = [];
      document.querySelectorAll('.page').forEach((pg, i) => {
        const pr = pg.getBoundingClientRect();
        const c = pg.querySelector('.content');
        if (c) {
          const cr = c.getBoundingClientRect();
          if (c.scrollHeight > c.clientHeight + 1) probs.push({ page: i + 1, issue: 'content taller than frame', by_mm: (c.scrollHeight - c.clientHeight) / MM });
          c.querySelectorAll('*').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width === 0) return;
            if (r.bottom > cr.bottom + 1 || r.left < cr.left - 1 || r.right > cr.right + 1)
              probs.push({ page: i + 1, issue: 'element outside content frame', tag: el.tagName, cls: el.className, text: (el.textContent || '').slice(0, 40) });
          });
        }
        pg.querySelectorAll('td, th, .fit').forEach(el => {
          if (el.scrollWidth > el.clientWidth + 1) probs.push({ page: i + 1, issue: 'cell text wider than cell', text: (el.textContent || '').slice(0, 40) });
        });
        const used = c ? [...c.children].reduce((m, el) => Math.max(m, el.getBoundingClientRect().bottom), c.getBoundingClientRect().top) - c.getBoundingClientRect().top : 0;
        probs.push({ page: i + 1, fill_mm: used / MM, info: true });
      });
      return probs;
    }, MM);
  }
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
