// Renders the franchise form in Chromium, takes the review screenshots and runs behaviour checks.
// Usage: node _work/verify.cjs   (from anywhere)
const path = require('path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const src = path.join(root, 'src');
const out = path.join(root, 'hippo_franchise-form_screens_ar-en_v01');
const pages = { ar: 'index.html', en: 'index-en.html' };
const views = { phone: { width: 390, height: 844, dsf: 2 }, desktop: { width: 1440, height: 900, dsf: 1 } };
const sample = {
  ar: { full_name: 'اسم تجريبي للعرض', mobile: '0500000000', email: 'name@example.com', city: 'مدينة تجريبية', experience: 'نص تجريبي يوضّح شكل الحقل عند التعبئة.', message: 'رسالة تجريبية للعرض فقط.' },
  en: { full_name: 'Sample Name', mobile: '+966 50 000 0000', email: 'name@example.com', city: 'Sample City', experience: 'Sample text showing the field when filled.', message: 'A sample message, for display only.' },
};
const log = [];
const ok = (name, pass, detail = '') => { log.push({ name, pass, detail }); console.log((pass ? 'PASS ' : 'FAIL ') + name + (detail ? '  — ' + detail : '')); };

async function fill(page, lang, opts = {}) {
  const s = sample[lang];
  for (const k of ['full_name', 'mobile', 'email', 'city', 'experience', 'message']) await page.fill('#' + k, s[k]);
  await page.check('input[name="has_location"][value="searching"]', { force: true });
  await page.selectOption('#heard_from', 'video-ad');
  if (!opts.noConsent) await page.check('#consent');
}

(async () => {
  const browser = await chromium.launch();
  for (const [vname, v] of Object.entries(views)) {
    for (const [lang, file] of Object.entries(pages)) {
      const ctx = await browser.newContext({ viewport: { width: v.width, height: v.height }, deviceScaleFactor: v.dsf, hasTouch: vname === 'phone', isMobile: vname === 'phone' });
      const page = await ctx.newPage();
      const external = [];
      page.on('request', (r) => { if (!r.url().startsWith('file:') && !r.url().startsWith('data:')) external.push(r.url()); });
      const errors = [];
      page.on('pageerror', (e) => errors.push(String(e)));
      page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
      const tag = `${lang} ${vname}`;
      const shot = (n, full) => page.screenshot({ path: path.join(out, `hippo_franchise-form_${vname}-${n}_${lang}_v01.png`), fullPage: !!full });

      await page.goto('file://' + path.join(src, file));
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(1600);
      await shot('01-top');

      // structural checks
      const info = await page.evaluate(() => {
        const used = new Set();
        const fams = new Set();
        document.fonts.forEach((f) => { if (f.status === 'loaded') used.add(f.family.replace(/"/g, '') + ' ' + f.weight + ' ' + f.style); });
        document.querySelectorAll('body *').forEach((el) => { if (el.offsetParent !== null) fams.add(getComputedStyle(el).fontFamily); });
        const small = [];
        document.querySelectorAll('a, button, input:not([tabindex="-1"]), select, textarea, .choice').forEach((el) => {
          if (el.closest('[hidden]') || el.closest('.hp') || el.closest('.choice') && el.tagName === 'INPUT') return;
          let r = el.getBoundingClientRect();
          if (el.id === 'consent') r = { width: r.width + 18, height: r.height + 18 };
          if (r.width && (r.height < 44 || r.width < 44)) small.push(el.tagName + '#' + el.id + '.' + el.className + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
        });
        const over = [];
        const W = document.documentElement.clientWidth;
        document.querySelectorAll('body *').forEach((el) => {
          if (el.closest('.hp') || el.closest('.skip') || el.classList.contains('skip') || el.classList.contains('visually-hidden')) return;
          const r = el.getBoundingClientRect();
          if (r.width && (r.left < -0.5 || r.right > W + 0.5)) over.push(el.tagName + '.' + el.className);
        });
        return { dir: document.documentElement.dir, scrollW: document.documentElement.scrollWidth, W, loaded: [...used], fams: [...fams], small, over,
          logo: (() => { const i = document.querySelector('.masthead .logo'); const r = i.getBoundingClientRect(); return { ratio: r.width / r.height, natural: i.naturalWidth / i.naturalHeight, ok: i.complete && i.naturalWidth > 0 }; })(),
          imgs: [...document.images].filter((i) => !i.closest('[hidden]')).map((i) => i.complete && i.naturalWidth > 0) };
      });
      ok(`${tag}: no horizontal overflow`, info.scrollW <= info.W && info.over.length === 0, `scrollWidth ${info.scrollW}/${info.W} ${info.over.join(',')}`);
      ok(`${tag}: dir`, info.dir === (lang === 'ar' ? 'rtl' : 'ltr'), info.dir);
      ok(`${tag}: fonts loaded`, info.loaded.some((f) => f.startsWith('Tajawal')) && info.loaded.some((f) => f.startsWith('Playfair')), info.loaded.join(' | '));
      ok(`${tag}: logo undistorted + images load`, Math.abs(info.logo.ratio - info.logo.natural) < 0.01 && info.imgs.every(Boolean), `ratio ${info.logo.ratio.toFixed(4)} vs ${info.logo.natural.toFixed(4)}`);
      ok(`${tag}: touch targets >= 44px`, info.small.length === 0, info.small.join('; '));
      ok(`${tag}: draft strip visible`, await page.isVisible('#draft-strip'));

      // validation errors: empty submit, then bad phone + bad email
      await page.click('#submit-btn');
      const nErr = await page.locator('.error:not([hidden])').count();
      ok(`${tag}: empty submit shows 5 required errors`, nErr === 5, String(nErr));
      ok(`${tag}: focus moves to first invalid field`, await page.evaluate(() => document.activeElement.id === 'full_name'));
      await page.fill('#mobile', '12ab');
      await page.fill('#email', 'not-an-email');
      await page.click('#submit-btn');
      ok(`${tag}: bad phone and email flagged`, (await page.locator('.error:not([hidden])').count()) === 6);
      await page.evaluate(() => document.getElementById('form-title').scrollIntoView());
      await shot('03-errors', true);

      // filled
      await fill(page, lang);
      ok(`${tag}: errors clear when corrected`, (await page.locator('.error:not([hidden])').count()) === 0);
      await page.evaluate(() => document.activeElement.blur());
      await shot('02-filled', true);
      await page.focus('#city');
      await page.locator('#city').screenshot({ path: path.join(root, '_work', `focus_${vname}_${lang}.png`) });

      // draft confirmation
      await page.click('#submit-btn');
      await page.waitForTimeout(400);
      ok(`${tag}: draft confirmation shown, live one hidden`, (await page.isVisible('#done-draft')) && !(await page.isVisible('#done-live')) && !(await page.isVisible('#enquiry-form')));
      ok(`${tag}: no network request of any kind`, external.length === 0, external.join(','));
      ok(`${tag}: no console errors`, errors.length === 0, errors.join(' | '));
      await shot('04-confirmation-draft');
      await page.click('#done-draft [data-back]');
      ok(`${tag}: back to form keeps answers`, (await page.inputValue('#full_name')) === sample[lang].full_name);
      await ctx.close();
    }
  }

  // ---- behaviour with a (simulated) endpoint: live success, server failure, honeypot, phone formats, WhatsApp
  const mk = async (cfg, status) => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    const sent = [];
    await page.route('**/js/config.js', (r) => r.fulfill({ contentType: 'text/javascript', body: 'window.HIPPO_FORM_CONFIG=' + JSON.stringify(cfg) + ';' }));
    await page.route('https://endpoint.invalid/**', (r) => { sent.push({ ct: r.request().headers()['content-type'], body: r.request().postData() }); r.fulfill({ status, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: '{}' }); });
    await page.goto('file://' + path.join(src, 'index.html'));
    return { ctx, page, sent };
  };
  {
    const { ctx, page, sent } = await mk({ FORM_ENDPOINT: 'https://endpoint.invalid/x', FORM_FORMAT: 'form', PRIVACY_URL_AR: 'https://endpoint.invalid/privacy' }, 200);
    ok('live: draft strip hidden when connected', !(await page.isVisible('#draft-strip')));
    ok('live: privacy link replaces the marked gap', (await page.locator('#privacy-slot a').count()) === 1 && (await page.locator('.to-supply').count()) === 0);
    await fill(page, 'ar');
    await page.fill('#mobile', '٠٥٠ ٠٠٠ ٠٠٠٠');
    await page.click('#submit-btn');
    await page.waitForSelector('#done-live:not([hidden])');
    const b = new URLSearchParams(sent[0].body);
    ok('live (form format): one POST, success panel, Arabic-Indic digits normalised', sent.length === 1 && b.get('mobile') === '0500000000' && b.get('has_location') === 'searching' && !(await page.isVisible('#done-draft')), sent[0].ct + ' ' + sent[0].body.slice(0, 80));
    await page.screenshot({ path: path.join(root, '_work', 'state_live-success_ar.png') });
    await ctx.close();
  }
  {
    const { ctx, page, sent } = await mk({ FORM_ENDPOINT: 'https://endpoint.invalid/x' }, 500);
    await fill(page, 'ar');
    await page.click('#submit-btn');
    await page.waitForSelector('#form-alert:not([hidden])');
    ok('live: server failure shows an error and keeps the form', (await page.isVisible('#enquiry-form')) && !(await page.isVisible('#done-live')) && (await page.inputValue('#city')) === sample.ar.city && sent[0].ct.includes('application/json'));
    await page.screenshot({ path: path.join(root, '_work', 'state_send-failed_ar.png'), fullPage: true });
    await ctx.close();
  }
  {
    const { ctx, page, sent } = await mk({ FORM_ENDPOINT: 'https://endpoint.invalid/x' }, 200);
    await fill(page, 'ar');
    await page.evaluate(() => { document.getElementById('company_website').value = 'http://spam'; });
    await page.click('#submit-btn');
    await page.waitForTimeout(500);
    ok('honeypot: filled trap sends nothing', sent.length === 0);
    await ctx.close();
  }
  {
    const { ctx, page } = await mk({ WHATSAPP_NUMBER: '000000000000' }, 200);
    await page.addInitScript(() => { window.__opened = []; window.open = (u) => { window.__opened.push(u); return null; }; });
    await page.reload();
    await fill(page, 'ar');
    await page.click('#submit-btn');
    const opened = await page.evaluate(() => window.__opened);
    ok('whatsapp mode: opens wa.me with the enquiry text, shows the "one step left" panel', opened.length === 1 && opened[0].startsWith('https://wa.me/000000000000?text=') && decodeURIComponent(opened[0]).includes(sample.ar.city) && (await page.isVisible('#done-whatsapp')));
    await page.screenshot({ path: path.join(root, '_work', 'state_whatsapp_ar.png') });
    await ctx.close();
  }
  {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    await page.goto('file://' + path.join(src, 'index.html'));
    const res = {};
    for (const p of ['0500000000', '+966500000000', '00971500000000', '+44 20 0000 0000', '050-000-0000', '12345', 'abc', '+']) {
      await page.fill('#mobile', p); await page.locator('#mobile').blur();
      res[p] = !(await page.isVisible('#mobile-error'));
    }
    ok('phone formats', res['0500000000'] && res['+966500000000'] && res['00971500000000'] && res['+44 20 0000 0000'] && res['050-000-0000'] && !res['12345'] && !res['abc'] && !res['+'], JSON.stringify(res));
    // 200% text scaling and 320 px width
    await page.setViewportSize({ width: 320, height: 700 });
    await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
    await page.waitForTimeout(1800);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    ok('320 px wide at 200% text: no horizontal scroll', sw <= 320, String(sw));
    await page.screenshot({ path: path.join(root, '_work', 'stress_320px_200pct_ar.png'), fullPage: true });
    await ctx.close();
  }
  await browser.close();
  const failed = log.filter((l) => !l.pass);
  console.log(`\n${log.length - failed.length}/${log.length} checks passed`);
  process.exit(failed.length ? 1 : 0);
})();
