// Verification of the landing page v03 in Chromium. Run from the repo root:
//   node clients/demo-sidra-coffee/05-designs/landing-page/_work/verify_v03.cjs
// Loads index.html over file://, so it also proves the folder is self-contained.
// v03 adds: 360 and 320 px widths, hero ink-overhang measurement (L5), last-line word counts (L6),
// bar-row position (L3), standalone-name scan (L1), favicon check at 16 px (L2).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const dir = path.resolve(__dirname, '..');
const url = 'file://' + path.join(dir, 'index.html');
const shot = (n) => path.join(__dirname, `demo-sidra-coffee_landing-page_${n}_ar_v03.png`);

// Rightmost / leftmost x of Ink-dark pixels inside a clip of the live page.
async function inkExtent(browser, page, clip) {
  const buf = await page.screenshot({ clip });
  const p2 = await browser.newPage();
  const res = await p2.evaluate(async (b64) => {
    const img = new Image();
    img.src = 'data:image/png;base64,' + b64;
    await img.decode();
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const g = c.getContext('2d');
    g.drawImage(img, 0, 0);
    const d = g.getImageData(0, 0, c.width, c.height).data;
    let min = null, max = null;
    for (let x = 0; x < c.width; x++) {
      for (let y = 0; y < c.height; y++) {
        const i = (y * c.width + x) * 4;
        if (d[i] < 90 && d[i + 1] < 90 && d[i + 2] < 90) { if (min === null) min = x; max = x; break; }
      }
    }
    return { min, max };
  }, buf.toString('base64'));
  await p2.close();
  return { left: clip.x + res.min, right: clip.x + res.max + 1 };
}

(async () => {
  const browser = await chromium.launch();
  const out = {};

  // L2: favicon file exists, is the small icon, and holds at 16 px
  const html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
  const iconHref = (html.match(/<link rel="icon"[^>]*href="([^"]+)"/) || [])[1];
  const iconPath = path.join(dir, iconHref);
  const fav = { href: iconHref, exists: fs.existsSync(iconPath), otherIconRefs: (html.match(/logo_icon-[a-z-]+_ar-en_v\d+\.svg/g) || []) };
  if (fav.exists) {
    const p = await browser.newPage();
    fav.middleRowAt16px = await p.evaluate(async (svg) => {
      const img = new Image();
      img.src = 'data:image/svg+xml;base64,' + svg;
      await img.decode();
      const c = document.createElement('canvas'); c.width = 16; c.height = 16;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0, 16, 16);
      const row = [];
      for (let x = 0; x < 16; x++) {
        const d = g.getImageData(x, 8, 1, 1).data;
        row.push(d[3] < 40 ? '.' : (d[0] > 120 && d[1] < 110 ? 'E' : 'I'));
      }
      return row.join('');
    }, fs.readFileSync(iconPath).toString('base64'));
    await p.close();
  }
  out.favicon = fav;

  // L1: «سدرة» never alone in page text or attributes (script stripped)
  const noScript = html.replace(/<script>[\s\S]*?<\/script>/g, '');
  out.nameRule = { total: (noScript.match(/سدرة/g) || []).length, standalone: (noScript.match(/سدرة(?! للقهوة)/g) || []).length };
  out.tokensV02Mentions = ['index.html', 'styles.css', 'handoff-notes.md'].map((f) => `${f}: ${(fs.readFileSync(path.join(dir, f), 'utf8').match(/tokens(\.json)?`? v02/g) || []).length}`);

  for (const [name, width, height, shoot] of [['desktop-1440', 1440, 900, true], ['mobile-390', 390, 844, true], ['mobile-360', 360, 800, false], ['mobile-320', 320, 700, true]]) {
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
    r.outsideFolder = requests.filter((u) => !u.startsWith('file://' + dir));
    r.failed = failed;

    const measure = () => page.evaluate(() => {
      const de = document.documentElement;
      const over = [];
      document.querySelectorAll('body *').forEach((el) => {
        const b = el.getBoundingClientRect();
        if (b.width && (b.right > de.clientWidth + 0.5 || b.left < -0.5) && !el.closest('.skip, .visually-hidden')) {
          over.push(el.tagName + '.' + el.className);
        }
      });
      // text runs wider than their own box (nowrap or unbreakable content)
      const textOver = [];
      document.querySelectorAll('h1 span, h2, h3, p, dd, dt, label, a, button').forEach((el) => {
        if (!el.offsetParent || el.closest('.skip, .visually-hidden')) return;
        if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0) textOver.push(`${el.tagName}.${el.className} ${el.scrollWidth}>${el.clientWidth}`);
      });
      return { scrollWidth: de.scrollWidth, clientWidth: de.clientWidth, overflowing: over, textWiderThanBox: textOver };
    });

    r.default = await measure();
    Object.assign(r.default, await page.evaluate(() => {
      const faces = [...document.fonts].map((f) => `${f.family} ${f.weight} ${f.status}`);
      const px = (sel) => { const e = document.querySelector(sel); const s = getComputedStyle(e); return `${s.fontSize} / ${s.fontWeight}`; };
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
      // words on each line of a simple paragraph
      const lines = (el) => {
        const out = [];
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n; let lastTop = null;
        while ((n = walker.nextNode())) {
          const re = /\S+/g; let m;
          while ((m = re.exec(n.data))) {
            const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
            const top = Math.round(rg.getClientRects()[0].top);
            if (lastTop === null || Math.abs(top - lastTop) > 6) { out.push([]); lastTop = top; }
            out[out.length - 1].push(m[0]);
          }
        }
        return out.map((l) => l.join(' '));
      };
      const how = document.querySelector('#how');
      const bars = how.querySelector('.bars').getBoundingClientRect();
      const steps = how.querySelector('.steps').getBoundingClientRect();
      const lit = how.querySelector('.bars i:nth-child(4)').getBoundingClientRect();
      const h1 = document.querySelector('.hero h1');
      const textRect = (el) => { const rg = document.createRange(); rg.selectNodeContents(el); const b = rg.getBoundingClientRect(); return b; };
      return {
        faces: faces.filter((f) => !/ loaded$/.test(f)).length ? faces : `${faces.length} faces, all loaded`,
        h1: px('.hero h1'), body: px('.hero__lead'),
        h1Lines: [...h1.querySelectorAll('span')].map((s) => { const b = textRect(s); return { text: s.textContent, advanceWidth: Math.round(b.width), top: b.top + scrollY, bottom: b.bottom + scrollY, boxWidth: Math.round(s.getBoundingClientRect().width) }; }),
        textEdgeRight: document.querySelector('.hero__text').getBoundingClientRect().right,
        textEdgeLeft: document.querySelector('.hero__text').getBoundingClientRect().left,
        captionRight: document.querySelector('.hero .caption').getBoundingClientRect().right,
        stepLines: [...document.querySelectorAll('.step')].map((s) => ({ title: lines(s.querySelector('h3')), text: lines(s.querySelector('p')) })),
        heroLeadLines: lines(document.querySelector('.hero__lead')),
        howBars: { barsTop: Math.round(bars.top + scrollY), stepsBottom: Math.round(steps.bottom + scrollY), barsBelowSteps: bars.top >= steps.bottom, gap: Math.round(bars.top - steps.bottom), litBarX: `${Math.round(lit.left)}–${Math.round(lit.right)}`, sectionBottom: Math.round(how.getBoundingClientRect().bottom + scrollY) },
        targetsUnder44: small, emberNonBarElements: ember,
        hasSampleWord: /عي[ّ]?نة|عينات/.test(document.body.innerText),
        pageHeight: de_h(),
        letterSpacings: [...new Set([...document.querySelectorAll('body *')].map((e) => getComputedStyle(e).letterSpacing))],
        minFontPx: Math.min(...[...document.querySelectorAll('body *')].filter((e) => e.offsetParent && e.childNodes.length && [...e.childNodes].some((n) => n.nodeType === 3 && n.data.trim())).map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
      function de_h() { return document.documentElement.scrollHeight; }
    }));

    // L5: ink of each headline line against the text edge (page scrolled to top)
    await page.evaluate(() => scrollTo(0, 0));
    r.default.h1Ink = [];
    for (const l of r.default.h1Lines) {
      const ink = await inkExtent(browser, page, { x: Math.floor(r.default.textEdgeLeft) - 10, y: Math.floor(l.top), width: width - Math.floor(r.default.textEdgeLeft) + 10, height: Math.ceil(l.bottom - l.top) });
      r.default.h1Ink.push({ text: l.text, inkRight: ink.right, inkLeft: ink.left, insideRightEdgeBy: +(r.default.textEdgeRight - ink.right).toFixed(1), insideLeftEdgeBy: +(ink.left - r.default.textEdgeLeft).toFixed(1) });
    }
    if (shoot) await page.screenshot({ path: shot(name), fullPage: true });

    // Empty submit -> error state
    const before = requests.length;
    await page.click('#submit-btn');
    r.error = await measure();
    Object.assign(r.error, await page.evaluate(() => {
      const e = document.getElementById('e-email');
      const tops = new Set(); const rg = document.createRange(); rg.selectNodeContents(e);
      [...rg.getClientRects()].forEach((b) => tops.add(Math.round(b.top / 8)));
      const ex = e.querySelector('.ltr').getBoundingClientRect(); const eb = e.getBoundingClientRect();
      const field = e.closest('.field').getBoundingClientRect();
      return {
        focusOnSummary: document.activeElement.id,
        items: [...document.querySelectorAll('#form-summary-list a')].map((a) => a.textContent),
        invalid: [...document.querySelectorAll('[aria-invalid="true"]')].map((x) => x.id),
        emailError: { lineCount: Math.round(eb.height / parseFloat(getComputedStyle(e).lineHeight)), boxWidth: Math.round(eb.width), fieldWidth: Math.round(field.width), exampleWidth: Math.round(ex.width), exampleInsideField: ex.left >= field.left - 0.5 && ex.right <= field.right + 0.5 },
      };
    }));
    if (shoot) await page.locator('#enquiry-form').screenshot({ path: shot(name + '-form-error') });

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
    r.success = await measure();
    Object.assign(r.success, await page.evaluate(() => ({
      formHidden: getComputedStyle(document.getElementById('enquiry-form')).display === 'none',
      focus: document.activeElement.id,
      text: document.getElementById('form-success').innerText.replace(/\n+/g, ' | '),
    })));
    if (shoot) await page.locator('#form-success').screenshot({ path: shot(name + '-form-success') });
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
