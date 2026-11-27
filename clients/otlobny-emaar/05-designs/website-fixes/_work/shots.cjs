// Browser checks for the v02 files served by the local PHP stub. Scratch tool, not a deliverable.
const { chromium } = require('playwright');
const path = require('path');
const OUT = path.join(__dirname, 'shots-v03');
const BASE = 'http://127.0.0.1:8765';
const results = [];
const ok = (name, pass, detail = '') => { results.push({ name, pass, detail }); console.log((pass ? 'PASS ' : 'FAIL ') + name + (detail ? ' — ' + detail : '')); };
const rect = (page, sel) => page.$eval(sel, (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return { x: r.x, y: r.y, w: r.width, h: r.height, r: r.right, b: r.bottom, display: cs.display, visibility: cs.visibility }; });
const overlap = (a, b) => a.x < b.r && b.x < a.r && a.y < b.b && b.y < a.b;
const hitSelf = (page, sel) => page.$eval(sel, (el) => { const r = el.getBoundingClientRect(); const t = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); return t === el || el.contains(t); });
const noHScroll = (page) => page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth }));
const tabWalk = async (page, n) => { const seen = []; for (let i = 0; i < n; i++) { await page.keyboard.press('Tab'); seen.push(await page.evaluate(() => { const a = document.activeElement; return { tag: a.tagName, cls: a.className || '', inNav: !!a.closest('#mobile-nav'), text: (a.textContent || '').trim().slice(0, 24) }; })); } return seen; };

(async () => {
  const browser = await chromium.launch();
  const fontReq = { ok: 0, failed: 0 };
  for (const vp of [{ w: 390, h: 844, tag: 'm390' }, { w: 1440, h: 900, tag: 'd1440' }, { w: 320, h: 568, tag: 'm320' }]) {
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, extraHTTPHeaders: { 'X-Forwarded-Proto': 'https' }, locale: 'ar-SA' });
    const page = await ctx.newPage();
    // Google Fonts files (fonts.gstatic.com) are blocked in this environment. For the screenshots only, the same
    // family (IBM Plex Sans Arabic, SIL OFL, from the agency's assets/fonts) is served locally in place of the Google CSS.
    await ctx.route(/fonts\.googleapis\.com/, (route) => route.fulfill({ contentType: 'text/css', body: [[400, 'Regular'], [500, 'Medium'], [600, 'SemiBold'], [700, 'Bold']].map(([w, n]) => `@font-face{font-family:'IBM Plex Sans Arabic';font-weight:${w};font-style:normal;src:url('${BASE}/_fonts/IBMPlexSansArabic-${n}.ttf') format('truetype')}`).join('') }));
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('requestfailed', (r) => { if (/fonts\.g/.test(r.url())) fontReq.failed++; });
    page.on('response', (r) => { if (/fonts\.g/.test(r.url()) && r.ok()) fontReq.ok++; });
    const cdp = await ctx.newCDPSession(page); await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
    const shot = (name, opts = {}) => page.screenshot({ path: path.join(OUT, `${vp.tag}_${name}.png`), ...opts });
    const mobile = vp.w <= 780;
    const T = `[${vp.tag}] `;

    await page.goto(BASE + '/', { waitUntil: 'load' }); await page.waitForTimeout(900);
    await shot('01_home_top');
    let hs = await noHScroll(page); ok(T + 'home: no horizontal scroll', hs.sw <= hs.iw, `scrollWidth ${hs.sw} / viewport ${hs.iw}`);
    ok(T + 'footer phone number reads +966… left to right', await page.$eval('footer a[href^="tel:"] span', (el) => el.dir === 'ltr' && el.textContent === '+966549555514'));
    ok(T + 'footer postal code isolated left to right (42313-5041)', await page.$eval('footer .legal-identity span[dir=ltr]', (el) => el.textContent === '42313-5041'));
    ok(T + 'dir=rtl, lang=ar, data-theme', await page.evaluate(() => document.documentElement.dir === 'rtl' && document.documentElement.lang === 'ar' && document.documentElement.dataset.theme === 'dark'));
    const font = await page.evaluate(async () => { await document.fonts.ready; return { plex: document.fonts.check('16px "IBM Plex Sans Arabic"', 'اطلبني'), loaded: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family).filter((v, i, a) => a.indexOf(v) === i) }; });
    console.log(T + 'fonts:', JSON.stringify(font), JSON.stringify(fontReq));

    if (mobile) {
      // closed menu must not take keyboard focus
      const nav0 = await rect(page, '#mobile-nav');
      ok(T + 'closed menu: visibility hidden + inert', nav0.visibility === 'hidden' && await page.$eval('#mobile-nav', (n) => n.hasAttribute('inert') && n.getAttribute('aria-hidden') === 'true'));
      const walk = await tabWalk(page, 14);
      ok(T + 'closed menu: Tab x14 never lands in #mobile-nav', !walk.some((s) => s.inNav), walk.map((s) => s.tag + ':' + s.text).slice(0, 6).join(' > '));
      // open
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.click('.menu'); await page.waitForTimeout(350);
      const nav1 = await rect(page, '#mobile-nav');
      ok(T + 'menu opens (visible, aria-expanded=true, not inert)', nav1.visibility === 'visible' && await page.$eval('.menu', (b) => b.getAttribute('aria-expanded') === 'true') && await page.$eval('#mobile-nav', (n) => !n.hasAttribute('inert') && n.getAttribute('aria-hidden') === 'false'));
      await shot('02_menu_open');
      await page.focus('.menu'); const walkOpen = await tabWalk(page, 3);
      ok(T + 'open menu: Tab from button enters menu links', walkOpen.every((s) => s.inNav), walkOpen.map((s) => s.text).join(' > '));
      const linkH = await page.$$eval('#mobile-nav a', (as) => Math.min(...as.map((a) => a.getBoundingClientRect().height)));
      ok(T + 'menu links >= 44px high', linkH >= 44, 'min ' + linkH);
      const bars = [await rect(page, '.mobile-contact-bar'), await rect(page, '.chat-fab'), await rect(page, '.mobile-whatsapp-bar')];
      ok(T + 'open menu does not cover the bottom bar', !bars.some((b) => overlap(nav1, b)), `menu bottom ${Math.round(nav1.b)} / bar top ${Math.round(bars[0].y)}`);
      await page.keyboard.press('Escape'); await page.waitForTimeout(350);
      const nav2 = await rect(page, '#mobile-nav');
      ok(T + 'Escape closes menu and returns focus to the button', nav2.visibility === 'hidden' && await page.evaluate(() => document.activeElement === document.querySelector('.menu')) && await page.$eval('.menu', (b) => b.getAttribute('aria-expanded') === 'false'));
      const walk2 = await tabWalk(page, 8);
      ok(T + 'after Escape: Tab x8 skips the menu links', !walk2.some((s) => s.inNav));
      await shot('03_menu_closed_after_escape');
      // toggle by button twice
      await page.click('.menu'); await page.waitForTimeout(300); await page.click('.menu'); await page.waitForTimeout(300);
      ok(T + 'menu button toggles closed again', (await rect(page, '#mobile-nav')).visibility === 'hidden');
    } else {
      ok(T + 'desktop: mobile nav and mobile bars not displayed', (await rect(page, '#mobile-nav')).display === 'none' && (await rect(page, '.mobile-contact-bar')).display === 'none' && (await rect(page, '.mobile-whatsapp-bar')).display === 'none');
    }

    // bottom of page
    await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight)); await page.waitForTimeout(700);
    await shot('04_home_bottom');
    const fab = await rect(page, '.chat-fab');
    ok(T + 'chat button >= 44px and receives the tap', fab.h >= 44 && fab.w >= 44 && await hitSelf(page, '.chat-fab'), `${Math.round(fab.w)}x${Math.round(fab.h)}`);
    if (mobile) {
      const call = await rect(page, '.mobile-contact-bar'), wa = await rect(page, '.mobile-whatsapp-bar');
      ok(T + 'call / chat / WhatsApp: no pairwise overlap', !overlap(call, fab) && !overlap(fab, wa) && !overlap(call, wa), `call x${Math.round(call.x)}-${Math.round(call.r)} chat x${Math.round(fab.x)}-${Math.round(fab.r)} wa x${Math.round(wa.x)}-${Math.round(wa.r)}`);
      ok(T + 'call and WhatsApp >= 44px and receive the tap', call.h >= 44 && wa.h >= 44 && call.w >= 44 && wa.w >= 44 && await hitSelf(page, '.mobile-contact-bar') && await hitSelf(page, '.mobile-whatsapp-bar'), `call ${Math.round(call.w)}x${Math.round(call.h)}, wa ${Math.round(wa.w)}x${Math.round(wa.h)}`);
      ok(T + 'order is RTL: call right, chat middle, WhatsApp left', call.x > fab.x && fab.x > wa.x);
      const fit = await page.$$eval('.mobile-contact-bar,.mobile-whatsapp-bar,.chat-fab', (els) => els.every((el) => el.scrollWidth <= el.clientWidth + 1));
      ok(T + 'bar labels fit inside their buttons', fit);
      const foot = await rect(page, 'footer small');
      ok(T + 'footer last line clear of the bar at end of page', foot.b <= Math.min(call.y, fab.y, wa.y), `footer text bottom ${Math.round(foot.b)} / bar top ${Math.round(call.y)}`);
    }
    // chat
    await page.click('.chat-fab'); await page.waitForTimeout(300);
    const chat = await rect(page, '#chat');
    await shot('05_chat_open');
    ok(T + 'chat opens, aria-hidden=false', chat.display === 'block' && await page.$eval('#chat', (c) => c.getAttribute('aria-hidden') === 'false'));
    ok(T + 'chat panel inside viewport', chat.x >= 0 && chat.r <= vp.w && chat.y >= 0 && chat.b <= vp.h, `x ${Math.round(chat.x)}-${Math.round(chat.r)}, y ${Math.round(chat.y)}-${Math.round(chat.b)}`);
    if (mobile) { const call = await rect(page, '.mobile-contact-bar'), wa = await rect(page, '.mobile-whatsapp-bar'), f2 = await rect(page, '.chat-fab'); ok(T + 'open chat does not overlap call / chat button / WhatsApp', !overlap(chat, call) && !overlap(chat, wa) && !overlap(chat, f2), `chat bottom ${Math.round(chat.b)} / bar top ${Math.round(call.y)}`); }
    else { ok(T + 'open chat does not overlap the chat button', !overlap(chat, await rect(page, '.chat-fab'))); }
    ok(T + 'opening chat moves focus to the chat input', await page.evaluate(() => document.activeElement === document.querySelector('#chat-message')));
    for (const sel of ['.chat-fab', '.chat-form button', '.quick button', '[data-close-chat]', '#chat-message'].concat(mobile ? ['.mobile-contact-bar', '.mobile-whatsapp-bar', '.menu'] : ['.header-cta']).concat(['#quote-form button', 'button.ghost', '#quote-form input', '#quote-form select', '#quote-form textarea', 'a.button'])) {
      if (!(await page.$(sel))) { ok(T + 'font: ' + sel + ' present', false); continue; }
      const fam = await page.$eval(sel, (el) => { const cs = getComputedStyle(el); return cs.fontFamily + ' / ' + cs.fontWeight + ' / ' + cs.fontSize; });
      const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: (await cdp.send('DOM.getDocument')).root.nodeId, selector: sel });
      const used = (await cdp.send('CSS.getPlatformFontsForNode', { nodeId })).fonts.map((x) => x.familyName + ':' + x.glyphCount);
      const arabicOk = used.length === 0 || sel === '.menu' /* its only glyph is the symbol ☰, which the Arabic font does not contain */ || used.some((u) => u.startsWith('IBM Plex Sans Arabic'));
      const noArial = !used.some((u) => /Arial|Liberation|DejaVu/.test(u)) || sel === '.menu' || sel === '.chat-fab' || sel === '[data-close-chat]';
      ok(T + 'font: ' + sel + ' computes to IBM Plex Sans Arabic', /^"?IBM Plex Sans Arabic/.test(fam) && arabicOk && noArial, fam + ' | rendered: ' + used.join(', '));
    }
    const close = await rect(page, '[data-close-chat]');
    ok(T + 'chat close: accessible name + >= 44px', close.w >= 44 && close.h >= 44 && await page.$eval('[data-close-chat]', (b) => b.getAttribute('aria-label') === 'إغلاق المحادثة'), `${Math.round(close.w)}x${Math.round(close.h)}`);
    ok(T + 'chat input has a label', await page.$eval('#chat-message', (i) => i.labels.length === 1 && i.labels[0].textContent.trim().length > 0));
    await page.keyboard.press('Escape'); await page.waitForTimeout(200);
    ok(T + 'Escape closes chat, focus back on the opener', (await rect(page, '#chat')).display === 'none' && await page.evaluate(() => document.activeElement === document.querySelector('.chat-fab')));
    await page.click('.chat-fab'); await page.click('[data-close-chat]');
    ok(T + 'close button closes chat', (await rect(page, '#chat')).display === 'none');
    await page.screenshot({ path: path.join(OUT, `${vp.tag}_06_home_full.png`), fullPage: true });

    // service page
    await page.goto(BASE + '/?service=contracting', { waitUntil: 'load' }); await page.waitForTimeout(700);
    await shot('07_service_contracting'); hs = await noHScroll(page); ok(T + 'service page: no horizontal scroll', hs.sw <= hs.iw, `${hs.sw}/${hs.iw}`);

    // 404
    const resp = await page.goto(BASE + '/?service=zzzz', { waitUntil: 'load' }); await page.waitForTimeout(700);
    await shot('08_404');
    ok(T + '404: status 404, noindex, themed, header + footer + chat present', resp.status() === 404 && await page.evaluate(() => document.querySelector('meta[name=robots]').content === 'noindex' && document.documentElement.dataset.theme === 'dark' && !!document.querySelector('header.site-header .brand img') && !!document.querySelector('footer') && !!document.querySelector('.chat-fab') && !document.querySelector('link[rel=canonical]')));
    hs = await noHScroll(page); ok(T + '404: no horizontal scroll', hs.sw <= hs.iw, `${hs.sw}/${hs.iw}`);
    if (mobile) { await page.click('.menu'); await page.waitForTimeout(350); await shot('09_404_menu_open'); ok(T + '404: menu opens', (await rect(page, '#mobile-nav')).visibility === 'visible'); await page.keyboard.press('Escape'); await page.waitForTimeout(300); ok(T + '404: Escape closes menu', (await rect(page, '#mobile-nav')).visibility === 'hidden'); }
    await page.click('.chat-fab'); await page.waitForTimeout(250); ok(T + '404: chat opens', (await rect(page, '#chat')).display === 'block');
    await page.screenshot({ path: path.join(OUT, `${vp.tag}_10_404_full.png`), fullPage: true });
    // 301
    const r301 = await ctx.request.get(BASE + '/?service=operation', { maxRedirects: 0 });
    ok(T + '?service=operation: 301 to https://otlobny.net/', r301.status() === 301 && r301.headers()['location'] === 'https://otlobny.net/');
    ok(T + 'no JavaScript errors', errors.length === 0, errors.join(' | '));
    await ctx.close();
  }
  // what the header looks like if the database still holds today's live settings
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: { 'X-Forwarded-Proto': 'https' } });
  await ctx.route(/fonts\.googleapis\.com/, (route) => route.abort());
  const p = await ctx.newPage(); await p.goto('http://127.0.0.1:8766/', { waitUntil: 'load' }); await p.waitForTimeout(800);
  await p.screenshot({ path: path.join(OUT, 'm390_11_home_top_with-old-database-settings.png') }); await ctx.close();
  await browser.close();
  const failed = results.filter((r) => !r.pass);
  console.log(`\n${results.length - failed.length}/${results.length} checks passed`); if (failed.length) process.exitCode = 1;
})();
