#!/usr/bin/env node
/**
 * Capture a website for research: a screenshot, the page title, the fonts
 * and the most-used colours actually computed in the page.
 * Uses Chromium through the session's HTTPS proxy, so it works for hosts the
 * environment's network policy allows even when WebFetch cannot reach them.
 *
 * Usage: node scripts/site_capture.cjs <output-dir> <name=url> [<name=url> ...] [--full]
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const args = process.argv.slice(2);
  const full = args.includes('--full');
  const rest = args.filter((a) => a !== '--full');
  if (rest.length < 2) { console.error('Usage: site_capture.cjs <output-dir> <name=url> ... [--full]'); process.exit(2); }
  const out = path.resolve(rest[0]);
  fs.mkdirSync(out, { recursive: true });
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch(proxy ? { proxy: { server: proxy } } : {});
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'ar-SA' });
  const results = [];
  for (const pair of rest.slice(1)) {
    const i = pair.indexOf('=');
    const name = pair.slice(0, i), url = pair.slice(i + 1);
    const page = await ctx.newPage();
    const r = { name, url };
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.waitForTimeout(4000);
      r.title = await page.title();
      r.lang = await page.evaluate(() => document.documentElement.lang + ' / dir=' + (document.documentElement.dir || getComputedStyle(document.documentElement).direction));
      Object.assign(r, await page.evaluate(() => {
        const count = (m, k) => m.set(k, (m.get(k) || 0) + 1);
        const fonts = new Map(), bg = new Map(), fg = new Map();
        for (const el of Array.from(document.querySelectorAll('body *')).slice(0, 4000)) {
          const cs = getComputedStyle(el);
          const box = el.getBoundingClientRect();
          if (!box.width || !box.height) continue;
          if (el.childNodes.length && Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim())) {
            count(fonts, cs.fontFamily.split(',')[0].replace(/["']/g, '').trim());
            count(fg, cs.color);
          }
          if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)') bg.set(cs.backgroundColor, (bg.get(cs.backgroundColor) || 0) + box.width * box.height);
        }
        const top = (m, n) => [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, n).map((e) => e[0]);
        return { fonts: top(fonts, 5), textColours: top(fg, 5), backgroundColoursByArea: top(bg, 6) };
      }));
      r.screenshot = path.join(out, name + '.png');
      await page.screenshot({ path: r.screenshot, fullPage: full });
      r.ok = true;
    } catch (e) { r.ok = false; r.error = e.message.split('\n')[0]; }
    await page.close();
    results.push(r);
  }
  await browser.close();
  fs.writeFileSync(path.join(out, 'capture.json'), JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));
})();
