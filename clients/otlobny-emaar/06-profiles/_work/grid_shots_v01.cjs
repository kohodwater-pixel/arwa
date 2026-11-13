// Screenshots of pages 3, 8, 15, 18 with the 12-column / 6-row grid overlaid.
const path = require('path');
const { chromium } = require(require.resolve('playwright', { paths: ['/home/user/arwa', '/home/user/arwa/scripts'] }));
(async () => {
  const d = __dirname; const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 1.5 });
  await pg.goto('file://' + path.join(d, 'otlobny-emaar_company-profile_grid-proof_v01.html'), { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  for (const n of [3, 8, 15, 18]) await pg.locator('#p' + n).screenshot({ path: path.join(d, `otlobny-emaar_company-profile_grid-proof_p${String(n).padStart(2, '0')}_v01.png`) });
  await b.close(); console.log('grid proofs written');
})();
