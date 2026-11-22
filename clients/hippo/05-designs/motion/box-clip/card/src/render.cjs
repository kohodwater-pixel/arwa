// Renders card.html to PNG at a given card width W (height = 2.6 W).
// Usage: node render.cjs <W> <out.png>
// Prints the element boxes and the fonts Chromium actually used.
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const W = parseInt(process.argv[2] || '1200', 10);
  const out = path.resolve(process.argv[3] || `card_${W}.png`);
  const H = Math.round(W * 2.6);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const failed = [];
  page.on('requestfailed', r => failed.push(r.url()));
  await page.goto('file://' + path.join(__dirname, 'card.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));

  const boxes = await page.evaluate(() => {
    const r = {};
    for (const s of ['.card', '.logo', '.kicker', '.band', '.headline', '.proof', '.qr', '.qr img', '.pill', '.pill span', '.strip']) {
      const el = document.querySelector(s);
      const b = el.getBoundingClientRect();
      r[s] = { x: +b.x.toFixed(2), y: +b.y.toFixed(2), w: +b.width.toFixed(2), h: +b.height.toFixed(2), scrollW: el.scrollWidth };
    }
    // ink width of each text line
    r.lines = [...document.querySelectorAll('.kicker, .headline span, .proof span, .pill span')].map(el => {
      const rg = document.createRange(); rg.selectNodeContents(el);
      const b = rg.getBoundingClientRect();
      return { text: el.textContent, x: +b.x.toFixed(1), w: +b.width.toFixed(1), fontSize: getComputedStyle(el).fontSize, weight: getComputedStyle(el).fontWeight, letterSpacing: getComputedStyle(el).letterSpacing };
    });
    r.fontsLoaded = [...document.fonts].map(f => `${f.family} ${f.weight} ${f.status}`);
    r.doc = { scrollW: document.documentElement.scrollWidth, scrollH: document.documentElement.scrollHeight };
    return r;
  });

  // fonts actually used to draw the glyphs (Chromium DevTools protocol)
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument');
  const used = {};
  for (const s of ['.kicker', '.headline', '.proof', '.pill']) {
    const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: s });
    const { fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId });
    used[s] = fonts.map(f => `${f.familyName} / ${f.postScriptName} (custom=${f.isCustomFont}, glyphs=${f.glyphCount})`);
  }

  await page.screenshot({ path: out, omitBackground: false, clip: { x: 0, y: 0, width: W, height: H } });
  await browser.close();
  console.log(JSON.stringify({ W, H, out, failedRequests: failed, boxes, platformFontsUsed: used }, null, 1));
})();
