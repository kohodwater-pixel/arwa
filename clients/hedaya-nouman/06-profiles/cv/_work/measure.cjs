// Measures how much room the side and main columns of each executive HTML need versus what the page gives.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const f of process.argv.slice(2)) {
    await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready);
    const r = await p.evaluate(() => { const mm = v => Math.round(v / 96 * 25.4);
      const q = s => document.querySelector(s); const g = q('.grid').getBoundingClientRect().height;
      const need = el => { const last = el.lastElementChild.getBoundingClientRect().bottom; const cs = getComputedStyle(el);
        return last + parseFloat(cs.paddingBottom) - el.getBoundingClientRect().top; };
      return { avail: mm(g), aside: mm(need(q('aside'))), main: mm(need(q('main'))), band: mm(q('header').scrollHeight) }; });
    console.log(f.split('/').pop().replace('hedaya-nouman_cv_', ''), JSON.stringify(r));
  }
  await b.close();
})();
