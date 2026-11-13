const path = require('path');
const { chromium } = require(require.resolve('playwright', { paths: ['/home/user/arwa', '/home/user/arwa/scripts'] }));
(async () => { const d = __dirname; const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 1.15 });
  await pg.goto('file://' + path.join(d, 'ad-sketch_v01.html'), { waitUntil: 'networkidle' }); await pg.evaluate(() => document.fonts.ready);
  const n = await pg.locator('.page').count(); for (let i = 0; i < n; i++) await pg.locator('.page').nth(i).screenshot({ path: path.join(d, `ad-sketch_v01_${i + 1}.png`) });
  await b.close(); console.log(n, 'sketches'); })();
