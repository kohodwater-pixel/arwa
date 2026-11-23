// Screenshot an HTML file at a given CSS width (full page) - used for mockup captions (Chromium shapes Arabic + bidi).
const { chromium } = require('playwright');
(async () => {
  const [inp, out, width] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +width, height: 100 } });
  await p.goto('file://' + require('path').resolve(inp)); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: out, fullPage: true }); await b.close();
})();
