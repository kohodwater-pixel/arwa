// Screenshot an HTML file at a given device scale. Usage: node shot.cjs <in.html> <out.png> [scale] [widthPx]
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require(path.resolve(__dirname, '../../../../node_modules/playwright'))); }
(async () => {
  const [input, output, scale = '3', width = '460'] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: Number(scale), viewport: { width: Number(width), height: 100 } });
  await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const bad = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'error').map(f => f.family + ' ' + f.weight));
  const imgs = await page.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.src));
  await page.screenshot({ path: path.resolve(output), fullPage: true });
  console.log('saved', output, 'font errors:', JSON.stringify(bad), 'broken images:', JSON.stringify(imgs));
  await browser.close();
})();
