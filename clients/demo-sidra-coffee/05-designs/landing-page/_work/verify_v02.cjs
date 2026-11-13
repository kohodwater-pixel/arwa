// Verification of the landing page v02 in Chromium. Run from the repo root:
//   node clients/demo-sidra-coffee/05-designs/landing-page/_work/verify_v02.cjs
// Loads index.html over file://, so it also proves the folder is self-contained.
const path = require('path');
const { chromium } = require('playwright');

const dir = path.resolve(__dirname, '..');
const url = 'file://' + path.join(dir, 'index.html');
const shot = (n) => path.join(__dirname, `demo-sidra-coffee_landing-page_${n}_ar_v02.png`);

(async () => {
  const browser = await chromium.launch();
  const out = {};
  for (const [name, width, height] of [['mobile-390', 390, 844], ['desktop-1440', 1440, 900]]) {
    const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const requests = [];
    const failed = [];
    page.on('request', (r) => requests.push(r.url()));
    page.on('requestfailed', (r) => failed.push(r.url()));
    const consoleErrors = [];
    page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text()); });
    page.on('pageerror', (e) => consoleErrors.push(String(e)));

    await page.goto(url);
    await page.evaluate(() => document.fonts.ready);
    const r = {};
    r.loadRequests = requests.map((u) => u.replace('file://' + dir, '.'));
    r.outsideFolder = requests.filter((u) => !u.startsWith('file://' + dir));
    r.failed = failed;

    r.default = await page.evaluate(() => {
      const de = document.documentElement;
      const over = [];
      document.querySelectorAll('body *').forEach((el) => {
        const b = el.getBoundingClientRect();
        if (b.width && (b.right > de.clientWidth + 0.5 || b.left < -0.5) && !el.closest('.skip, .visually-hidden')) {
          over.push(el.tagName + '.' + el.className);
        }
      });
      const faces = [...document.fonts].map((f) => `${f.family} ${f.weight} ${f.status}`);
      const px = (sel) => { const e = document.querySelector(sel); const s = getComputedStyle(e); return `${s.fontSize} / ${s.fontWeight} / ${s.fontStretch}`; };
      const h1 = document.querySelector('.hero h1');
      const spans = [...h1.querySelectorAll('span')].map((s) => Math.round(s.getBoundingClientRect().width));
      const small = [];
      document.querySelectorAll('a, button, input, textarea').forEach((el) => {
        if (el.closest('.skip') || !el.offsetParent) return;
        const b = el.getBoundingClientRect();
        if (b.height < 44) small.push(`${el.tagName} "${(el.textContent || el.name).trim().slice(0, 24)}" ${Math.round(b.height)}`);
      });
      const ember = [];
      document.querySelectorAll('body *').forEach((el) => {
        if (!el.offsetParent) return;
        const s = getComputedStyle(el);
        const isE = (c) => c === 'rgb(194, 58, 32)';
        if (el.tagName !== 'I' && (isE(s.backgroundColor) || isE(s.color) || (isE(s.borderTopColor) && parseFloat(s.borderTopWidth) > 0 && !isE(s.backgroundColor)))) {
          ember.push(`${el.tagName}.${el.className} y=${Math.round(el.getBoundingClientRect().top + scrollY)}`);
        }
      });
      const text = document.body.innerText;
      return {
        scrollWidth: de.scrollWidth, clientWidth: de.clientWidth, overflowing: over,
        faces, h1: px('.hero h1'), body: px('.hero__lead'), sub: px('.h-sub'), caption: px('.caption'), stepNum: px('.step__num'),
        h1LineWidths: spans, h1ColumnWidth: Math.round(document.querySelector('.hero__text').getBoundingClientRect().width),
        targetsUnder44: small, emberNonBarElements: ember,
        hasSampleWord: /عي[ّ]?نة|عينات/.test(text) || /sample/i.test(document.documentElement.outerHTML.replace(/<!--[\s\S]*?-->/g, '')),
        pageHeight: de.scrollHeight,
        letterSpacings: [...new Set([...document.querySelectorAll('body *')].map((e) => getComputedStyle(e).letterSpacing))],
      };
    });
    await page.screenshot({ path: shot(name), fullPage: true });

    // Empty submit -> error state
    const before = requests.length;
    await page.click('#submit-btn');
    r.error = await page.evaluate(() => ({
      summaryVisible: getComputedStyle(document.getElementById('form-summary')).display !== 'none',
      focusOnSummary: document.activeElement.id,
      items: [...document.querySelectorAll('#form-summary-list a')].map((a) => a.textContent),
      invalid: [...document.querySelectorAll('[aria-invalid="true"]')].map((e) => e.id),
      scrollWidth: document.documentElement.scrollWidth,
    }));
    await page.locator('#enquiry-form').screenshot({ path: shot(name + '-form-error') });

    // Bad email only
    await page.fill('#f-name', 'نورة');
    await page.fill('#f-cafe', 'مقهى تجريبي');
    await page.fill('#f-email', 'not-an-email');
    await page.click('#submit-btn');
    r.badEmail = await page.evaluate(() => [...document.querySelectorAll('[aria-invalid="true"]')].map((e) => e.id));

    // Valid -> loading -> success
    await page.fill('#f-email', 'owner@cafe.example');
    await page.click('#submit-btn');
    r.loadingLabel = await page.textContent('#submit-btn');
    await page.waitForSelector('#form-success.is-visible');
    r.success = await page.evaluate(() => ({
      formHidden: getComputedStyle(document.getElementById('enquiry-form')).display === 'none',
      focus: document.activeElement.id,
      text: document.getElementById('form-success').innerText.replace(/\n+/g, ' | '),
      scrollWidth: document.documentElement.scrollWidth,
    }));
    await page.locator('#form-success').screenshot({ path: shot(name + '-form-success') });
    await page.waitForTimeout(300);
    r.requestsAfterSubmits = requests.length - before;
    r.urlUnchanged = page.url() === url;

    // Reset returns the empty form
    await page.click('#reset-btn');
    r.reset = await page.evaluate(() => ({
      formVisible: getComputedStyle(document.getElementById('enquiry-form')).display !== 'none',
      empty: [...document.querySelectorAll('#enquiry-form input, #enquiry-form textarea')].every((e) => e.value === ''),
      button: document.getElementById('submit-btn').textContent,
    }));
    r.consoleErrors = consoleErrors;
    out[name] = r;
    await ctx.close();
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
})();
