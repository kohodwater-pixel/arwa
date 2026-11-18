// v02: renders the two-step franchise form in Chromium, takes the review screenshots and runs behaviour checks.
// Usage: node _work/verify.cjs
const path = require('path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const src = path.join(root, 'src');
const out = path.join(root, 'hippo_franchise-form_screens_ar-en_v02');
const pages = { ar: 'index.html', en: 'index-en.html' };
const views = { phone: { width: 390, height: 844, dsf: 2 }, desktop: { width: 1440, height: 900, dsf: 1 } };
const sample = {
  ar: { full_name: 'اسم تجريبي للعرض', profession: 'مهنة تجريبية', age: '35', company_name: 'شركة تجريبية', company_website: 'example.com', mobile: '0500000000', email: 'name@example.com',
        own_brand: 'علامة تجريبية', branches_operated: '2', why_hippo: 'نص تجريبي يوضّح شكل الحقل عند التعبئة.', investment_amount: '123456', target_cities: 'مدينة تجريبية', notes: 'ملاحظة تجريبية للعرض فقط.', other: 'إجابة تجريبية' },
  en: { full_name: 'Sample Name', profession: 'Sample profession', age: '35', company_name: 'Sample Company', company_website: 'example.com', mobile: '+966 50 000 0000', email: 'name@example.com',
        own_brand: 'Sample Brand', branches_operated: '2', why_hippo: 'Sample text showing the field when filled.', investment_amount: '123456', target_cities: 'Sample City', notes: 'A sample note, for display only.', other: 'Sample answer' },
};
const S1 = ['full_name', 'profession', 'age', 'company_name', 'company_website', 'mobile', 'email'];
const log = [];
const ok = (name, pass, detail = '') => { log.push({ name, pass, detail }); console.log((pass ? 'PASS ' : 'FAIL ') + name + (detail ? '  — ' + detail : '')); };
const errCount = (page) => page.locator('.error:not([hidden])').filter({ visible: true }).count();

async function fill1(page, lang) { for (const k of S1) await page.fill('#' + k, sample[lang][k]); }
async function fill2(page, lang) {
  const s = sample[lang];
  await page.check('input[name="experience"][value="other"]', { force: true });
  await page.fill('#experience_other', s.other);
  for (const k of ['own_brand', 'branches_operated', 'why_hippo', 'investment_amount', 'target_cities', 'notes']) await page.fill('#' + k, s[k]);
  await page.check('input[name="branches_wanted"][value="two-to-five"]', { force: true });
  await page.check('input[name="investment_source"][value="savings"]', { force: true });
  await page.check('input[name="start_time"][value="3-6-months"]', { force: true });
  await page.check('input[name="has_location"][value="searching"]', { force: true });
  await page.selectOption('#heard_from', 'video-ad');
  await page.check('#consent');
}
const structural = () => {
  const used = new Set();
  document.fonts.forEach((f) => { if (f.status === 'loaded') used.add(f.family.replace(/"/g, '') + ' ' + f.weight); });
  const vis = (el) => el.getClientRects().length > 0;
  const small = [];
  document.querySelectorAll('a, button, input, select, textarea, .choice').forEach((el) => {
    if (!vis(el) || el.closest('.hp') || el.classList.contains('skip') || (el.closest('.choice') && el.tagName === 'INPUT')) return;
    let r = el.getBoundingClientRect();
    if (el.id === 'consent') r = { width: r.width + 18, height: r.height + 18 };
    if (r.height < 44 || r.width < 44) small.push(el.tagName + '#' + el.id + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  });
  const over = [];
  const W = document.documentElement.clientWidth;
  document.querySelectorAll('body *').forEach((el) => {
    if (!vis(el) || el.closest('.hp') || el.classList.contains('skip')) return;
    const r = el.getBoundingClientRect();
    if (r.left < -0.5 || r.right > W + 0.5) over.push(el.tagName + '#' + el.id + '.' + el.className);
  });
  const i = document.querySelector('.masthead .logo'); const lr = i.getBoundingClientRect();
  return { scrollW: document.documentElement.scrollWidth, W, loaded: [...used], small, over,
    logo: Math.abs(lr.width / lr.height - i.naturalWidth / i.naturalHeight) < 0.01,
    imgs: [...document.images].filter(vis).every((im) => im.complete && im.naturalWidth > 0) };
};

(async () => {
  const browser = await chromium.launch();
  for (const [vname, v] of Object.entries(views)) {
    for (const [lang, file] of Object.entries(pages)) {
      const ctx = await browser.newContext({ viewport: { width: v.width, height: v.height }, deviceScaleFactor: v.dsf, hasTouch: vname === 'phone', isMobile: vname === 'phone' });
      const page = await ctx.newPage();
      const external = [], errors = [];
      page.on('request', (r) => { if (!r.url().startsWith('file:') && !r.url().startsWith('data:')) external.push(r.url()); });
      page.on('pageerror', (e) => errors.push(String(e)));
      page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
      const tag = `${lang} ${vname}`;
      const shot = async (n, full) => { await page.evaluate(() => document.activeElement && document.activeElement.blur()); await page.waitForTimeout(250); await page.screenshot({ path: path.join(out, `hippo_franchise-form_${vname}-${n}_${lang}_v02.png`), fullPage: !!full }); };
      const struct = async (label) => {
        const info = await page.evaluate(structural);
        ok(`${tag} ${label}: no overflow`, info.scrollW <= info.W && !info.over.length, `${info.scrollW}/${info.W} ${info.over.join(',')}`);
        ok(`${tag} ${label}: touch targets >= 44px`, !info.small.length, info.small.join('; '));
        return info;
      };

      await page.goto('file://' + path.join(src, file));
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(1600);
      await shot('00-top');
      const info = await struct('step 1');
      ok(`${tag}: dir + draft strip`, (await page.evaluate(() => document.documentElement.dir)) === (lang === 'ar' ? 'rtl' : 'ltr') && (await page.isVisible('#draft-strip')));
      ok(`${tag}: fonts loaded, logo undistorted, images load`, info.loaded.some((f) => f.startsWith('Tajawal')) && info.loaded.some((f) => f.startsWith('Playfair')) && info.logo && info.imgs, info.loaded.join(' | '));
      ok(`${tag}: step 1 shown, step 2 hidden, indicator 1`, (await page.isVisible('#step-1')) && !(await page.isVisible('#step-2')) && (await page.textContent('#step-now')) === '1');

      // step 1 errors
      await page.click('#next-btn');
      ok(`${tag}: empty step 1 → 5 errors, stays on step 1, focus on first`, (await errCount(page)) === 5 && (await page.isVisible('#step-1')) && (await page.evaluate(() => document.activeElement.id)) === 'full_name', String(await errCount(page)));
      await page.fill('#age', '17'); await page.fill('#mobile', '12ab'); await page.fill('#email', 'not-an-email'); await page.fill('#company_website', 'not a site');
      await page.click('#next-btn');
      ok(`${tag}: under-18, bad phone, bad email, bad website flagged`, (await errCount(page)) === 6 && (await page.textContent('#age-error')).includes('18'));
      await shot('03-errors-step1', true);

      // step 1 filled → next
      await fill1(page, lang);
      ok(`${tag}: step 1 errors clear when corrected`, (await errCount(page)) === 0 && !(await page.isVisible('#alert-1')));
      await shot('01-step1', true);
      await page.click('#next-btn');
      ok(`${tag}: next → step 2, indicator 2`, (await page.isVisible('#step-2')) && !(await page.isVisible('#step-1')) && (await page.textContent('#step-now')) === '2' && (await page.getAttribute('#steps', 'data-step')) === '2');

      // step 2 errors (with "other" chosen and left empty)
      await page.click('#submit-btn');
      ok(`${tag}: empty step 2 → 8 errors`, (await errCount(page)) === 8, String(await errCount(page)));
      await page.check('input[name="experience"][value="other"]', { force: true });
      await page.check('input[name="investment_source"][value="other"]', { force: true });
      await page.fill('#investment_amount', 'abc'); await page.fill('#branches_operated', 'x');
      await page.click('#submit-btn');
      ok(`${tag}: "other" reveals a required text field; bad amount and count flagged`, (await page.isVisible('#experience_other')) && (await page.isVisible('#experience_other-error')) && (await page.isVisible('#investment_source_other-error')) && (await page.isVisible('#investment_amount-error')) && (await page.isVisible('#branches_operated-error')) && !(await page.isVisible('#branches_wanted_other')));
      await shot('04-errors-step2', true);

      // step 2 filled
      await fill2(page, lang);
      ok(`${tag}: step 2 errors clear; un-choosing "other" hides its field`, (await errCount(page)) === 0 && !(await page.isVisible('#investment_source_other')) && !(await page.isVisible('#alert-2')));
      await struct('step 2');
      await shot('02-step2', true);

      // back keeps answers, forward again keeps answers
      await page.click('#back-btn');
      const kept1 = (await page.inputValue('#full_name')) === sample[lang].full_name && (await page.isVisible('#step-1'));
      await page.click('#next-btn');
      ok(`${tag}: back/next keeps answers on both steps`, kept1 && (await page.inputValue('#why_hippo')) === sample[lang].why_hippo && (await page.isChecked('input[name="start_time"][value="3-6-months"]')) && (await page.isChecked('#consent')));

      // draft confirmation
      await page.click('#submit-btn');
      await page.waitForTimeout(400);
      ok(`${tag}: draft confirmation shown, live one hidden`, (await page.isVisible('#done-draft')) && !(await page.isVisible('#done-live')) && !(await page.isVisible('#enquiry-form')));
      ok(`${tag}: no network request of any kind, no console errors`, external.length === 0 && errors.length === 0, external.concat(errors).join(' | '));
      await shot('05-confirmation-draft');
      await page.click('#done-draft [data-back]');
      ok(`${tag}: back to form returns to step 2 with answers`, (await page.isVisible('#step-2')) && (await page.inputValue('#target_cities')) === sample[lang].target_cities);
      await ctx.close();
    }
  }

  // ---- simulated endpoints
  const mk = async (cfg, handler, file = 'index.html') => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    const sent = [];
    await page.route('**/js/config.js', (r) => r.fulfill({ contentType: 'text/javascript', body: 'window.HIPPO_FORM_CONFIG=' + JSON.stringify(cfg) + ';' }));
    const h = (r) => { sent.push({ method: r.request().method(), ct: r.request().headers()['content-type'], body: r.request().postData() }); return handler(r); };
    await page.route('https://endpoint.invalid/**', h);
    await page.route('https://script.google.com/**', h);
    await page.route('https://script.googleusercontent.com/**', (r) => r.fulfill({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: '{"ok":true}' }));
    await page.goto('file://' + path.join(src, file));
    return { ctx, page, sent };
  };
  const json = (status, body) => (r) => r.fulfill({ status, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify(body) });
  const both = async (page, lang = 'ar') => { await fill1(page, lang); await page.click('#next-btn'); await fill2(page, lang); };
  const GS = 'https://script.google.com/macros/s/TEST/exec';
  {
    const { ctx, page, sent } = await mk({ FORM_ENDPOINT: GS, PRIVACY_URL_AR: 'https://endpoint.invalid/privacy' }, json(200, { ok: true }));
    ok('apps-script: draft strip hidden; privacy link replaces the marked gap', !(await page.isVisible('#draft-strip')) && (await page.locator('#privacy-slot a').count()) === 1 && (await page.locator('.to-supply').count()) === 0);
    await both(page);
    await page.fill('#investment_amount', '١٢٣٬٤٥٦');
    await page.click('#back-btn'); await page.fill('#mobile', '٠٥٠ ٠٠٠ ٠٠٠٠'); await page.click('#next-btn');
    await page.click('#submit-btn');
    await page.waitForSelector('#done-live:not([hidden])');
    const posts = sent.filter((s) => s.method === 'POST'); const d = JSON.parse(posts[0].body);
    const keys = ['form', 'lang', 'full_name', 'profession', 'age', 'company_name', 'company_website', 'mobile', 'email', 'experience', 'experience_other', 'own_brand', 'branches_operated', 'why_hippo', 'branches_wanted', 'branches_wanted_other', 'investment_source', 'investment_source_other', 'investment_amount', 'investment_currency', 'start_time', 'target_cities', 'has_location', 'heard_from', 'notes', 'consent', 'submitted_at'];
    ok('apps-script: one POST as text/plain with no preflight; every field in the payload; digits normalised', posts.length === 1 && sent.length === 1 && posts[0].ct.startsWith('text/plain') && keys.every((k) => k in d) && Object.keys(d).length === keys.length && d.mobile === '0500000000' && d.investment_amount === '123456' && d.experience === 'other' && d.experience_other === sample.ar.other && d.investment_source_other === '' && d.investment_currency === 'SAR' && d.age === '35', posts[0].ct + ' ' + Object.keys(d).length + ' keys');
    await page.screenshot({ path: path.join(root, '_work', 'state_live-success_ar.png') });
    await ctx.close();
  }
  {
    // Real local HTTP servers (not route stubs), so the browser's own redirect and CORS rules apply.
    const http = require('http');
    const hits = [];
    const target = http.createServer((q, r) => { hits.push('target ' + q.method); r.writeHead(200, { 'content-type': 'application/json', 'access-control-allow-origin': '*' }); r.end('{"ok":true}'); });
    await new Promise((res) => target.listen(0, '127.0.0.1', res));
    const entry = http.createServer((q, r) => {
      hits.push('entry ' + q.method + ' ' + q.url + ' ' + q.headers['content-type']);
      if (q.url === '/redirect') { r.writeHead(302, { location: 'http://127.0.0.1:' + target.address().port + '/echo', 'access-control-allow-origin': '*' }); return r.end(); }
      r.writeHead(200, { 'content-type': 'application/json' }); r.end('{"ok":true}'); // /nocors
    });
    await new Promise((res) => entry.listen(0, '127.0.0.1', res));
    const base = 'http://127.0.0.1:' + entry.address().port;
    {
      const { ctx, page } = await mk({ FORM_ENDPOINT: base + '/redirect', FORM_FORMAT: 'text' }, json(200, {}));
      await both(page); await page.click('#submit-btn');
      const okk = await page.waitForSelector('#done-live:not([hidden])', { timeout: 5000 }).then(() => true, () => false);
      ok('text/plain POST → 302 to another origin → JSON {"ok":true} (the shape of an Apps Script reply): read as success, no preflight', okk && !hits.some((h) => h.includes('OPTIONS')), hits.join(' | '));
      await ctx.close();
    }
    {
      hits.length = 0;
      const { ctx, page } = await mk({ FORM_ENDPOINT: base + '/nocors', FORM_FORMAT: 'text' }, json(200, {}));
      await both(page); await page.click('#submit-btn');
      await page.waitForSelector('#alert-2:not([hidden])', { timeout: 5000 }).catch(() => {});
      ok('reply the browser may not read (no CORS header): error shown, no false "sent" — although the server DID receive the POST', (await page.isVisible('#alert-2')) && !(await page.isVisible('#done-live')) && hits.some((h) => h.startsWith('entry POST')), hits.join(' | '));
      await ctx.close();
    }
    entry.close(); target.close();
  }
  for (const [label, handler] of [
    ['script replies {"ok":false}', json(200, { ok: false, error: 'x' })],
    ['an HTML page with status 200 (e.g. a Google error or sign-in page)', (r) => r.fulfill({ status: 200, contentType: 'text/html', headers: { 'access-control-allow-origin': '*' }, body: '<html>Error</html>' })],
    ['network failure', (r) => r.abort()],
  ]) {
    const { ctx, page } = await mk({ FORM_ENDPOINT: GS }, handler);
    await both(page); await page.click('#submit-btn');
    await page.waitForSelector('#alert-2:not([hidden])', { timeout: 5000 }).catch(() => {});
    ok(`apps-script: ${label} → error shown, form and answers kept, no false "sent"`, (await page.isVisible('#alert-2')) && (await page.isVisible('#step-2')) && !(await page.isVisible('#done-live')) && (await page.inputValue('#target_cities')) === sample.ar.target_cities && !(await page.isDisabled('#submit-btn')));
    if (label.startsWith('network')) await page.screenshot({ path: path.join(root, '_work', 'state_send-failed_ar.png'), fullPage: true });
    await ctx.close();
  }
  {
    const { ctx, page, sent } = await mk({ FORM_ENDPOINT: 'https://endpoint.invalid/x', FORM_FORMAT: 'form' }, json(200, {}), 'index-en.html');
    await both(page, 'en'); await page.click('#submit-btn');
    await page.waitForSelector('#done-live:not([hidden])');
    const b = new URLSearchParams(sent[0].body);
    ok('generic endpoint, "form" format: urlencoded POST, success on 2xx', sent[0].ct.includes('x-www-form-urlencoded') && b.get('mobile') === '+966500000000' && b.get('lang') === 'en' && b.get('start_time') === '3-6-months');
    await ctx.close();
  }
  {
    const { ctx, page, sent } = await mk({ FORM_ENDPOINT: 'https://endpoint.invalid/x' }, json(500, {}));
    await both(page); await page.click('#submit-btn');
    await page.waitForSelector('#alert-2:not([hidden])');
    ok('generic endpoint, "json" format: HTTP 500 → error shown, form kept', sent[0].ct.includes('application/json') && (await page.isVisible('#step-2')) && !(await page.isVisible('#done-live')));
    await ctx.close();
  }
  {
    const { ctx, page, sent } = await mk({ FORM_ENDPOINT: GS }, json(200, { ok: true }));
    await both(page);
    await page.evaluate(() => { document.querySelector('[name="hp_field"]').value = 'http://spam'; });
    await page.click('#submit-btn'); await page.waitForTimeout(500);
    ok('honeypot: filled trap sends nothing', sent.length === 0);
    await ctx.close();
  }
  {
    const { ctx, page } = await mk({ WHATSAPP_NUMBER: '000000000000' }, json(200, {}));
    await page.addInitScript(() => { window.__opened = []; window.open = (u) => { window.__opened.push(u); return null; }; });
    await page.reload();
    await both(page); await page.click('#submit-btn');
    const opened = await page.evaluate(() => window.__opened);
    const txt = opened.length ? decodeURIComponent(opened[0].split('?text=')[1]) : '';
    ok('whatsapp mode: opens wa.me with the readable enquiry, shows "one step left"', opened.length === 1 && opened[0].startsWith('https://wa.me/000000000000?text=') && txt.includes(sample.ar.target_cities) && txt.includes('123456 SAR') && txt.includes(sample.ar.other) && (await page.isVisible('#done-whatsapp')), txt.replace(/\n/g, ' / ').slice(0, 160));
    await ctx.close();
  }
  {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    await page.goto('file://' + path.join(src, 'index.html'));
    const probe = async (id, vals) => { const res = {}; for (const p of vals) { await page.fill('#' + id, p); await page.locator('#' + id).blur(); res[p] = !(await page.isVisible('#' + id + '-error')); } return res; };
    const ph = await probe('mobile', ['0500000000', '+966500000000', '00971500000000', '+44 20 0000 0000', '050-000-0000', '12345', 'abc', '+']);
    ok('phone formats', ph['0500000000'] && ph['+966500000000'] && ph['00971500000000'] && ph['+44 20 0000 0000'] && ph['050-000-0000'] && !ph['12345'] && !ph['abc'] && !ph['+'], JSON.stringify(ph));
    const ag = await probe('age', ['18', '٤٠', '17', '0', 'abc', '200']);
    ok('age: 18+ in digits (Western or Arabic-Indic)', ag['18'] && ag['٤٠'] && !ag['17'] && !ag['0'] && !ag['abc'] && !ag['200'], JSON.stringify(ag));
    const web = await probe('company_website', ['example.com', 'https://www.example.com/path', 'no dots', 'http://']);
    ok('website: optional, loose format', web['example.com'] && web['https://www.example.com/path'] && !web['no dots'] && !web['http://'], JSON.stringify(web));
    await fill1(page, 'ar'); await page.press('#email', 'Enter');
    ok('Enter in step 1 moves to step 2 (does not submit)', (await page.isVisible('#step-2')) && !(await page.isVisible('#done-draft')));
    const am = await probe('investment_amount', ['123456', '123,456', '١٢٣٤٥٦', '1234.50', '0', 'abc', '-5']);
    ok('amount: free number, no minimum other than above zero', am['123456'] && am['123,456'] && am['١٢٣٤٥٦'] && am['1234.50'] && !am['0'] && !am['abc'] && !am['-5'], JSON.stringify(am));
    await page.setViewportSize({ width: 320, height: 700 });
    await page.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
    await page.waitForTimeout(600);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    console.log(await page.evaluate(() => [...document.querySelectorAll('body *')].filter((el) => el.getClientRects().length && !el.closest('.hp') && !el.classList.contains('skip') && (el.getBoundingClientRect().left < -1 || el.getBoundingClientRect().right > 321)).map((el) => el.tagName + '#' + el.id + '.' + el.className).slice(0, 12).join(', ')));
    ok('320 px wide at 200% text (step 2): no horizontal scroll', sw <= 320, String(sw));
    await page.screenshot({ path: path.join(root, '_work', 'stress_320px_200pct_ar.png'), fullPage: true });
    await ctx.close();
  }
  await browser.close();
  const failed = log.filter((l) => !l.pass);
  console.log(`\n${log.length - failed.length}/${log.length} checks passed`);
  process.exit(failed.length ? 1 : 0);
})();
