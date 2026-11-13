// Renders the post HTML to PNG at exact size. Usage: node render.cjs <html> <png>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, png] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  const info = await page.evaluate(() => ({
    fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight),
    failed: [...document.fonts].filter(f => f.status === 'error').map(f => f.family + ' ' + f.weight),
    boxes: Object.fromEntries(['.logo', '.headline', '.sub', '.cta', '.bars'].map(s => {
      const r = document.querySelector(s).getBoundingClientRect();
      return [s, [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]];
    })),
    headlineScrollW: document.querySelector('.headline').scrollWidth,
  }));
  console.log(JSON.stringify(info, null, 1));
  await page.screenshot({ path: png, clip: { x: 0, y: 0, width: 1080, height: 1350 } });
  await browser.close();
})();
