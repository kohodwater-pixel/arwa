// Captures the film frame by frame: seek(t) then screenshot, 1080x1920.
// Run: NODE_PATH=/opt/node-tools/node_modules node _work/capture.cjs [--check | --times 1.5,6,12]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const motion = path.resolve(__dirname, '..');
const html = path.join(motion, 'tbc-restaurants-company_job-advert_motion-direction-a_ar_v02.html');
const TL = JSON.parse(fs.readFileSync(path.join(motion, 'timeline.json'), 'utf8'));
const ALLOWED = [
  'فرصة وظيفية', 'موظف/ـة تسويق وإدارة حسابات التواصل الاجتماعي', 'لشركة متخصصة في قطاع المطاعم', 'العمل عن بُعد',
  'خبرة في التصميم (شرط أساسي)', 'خبرة سابقة في التسويق وإدارة حسابات التواصل الاجتماعي',
  'معرفة جيدة بمنصات إنستغرام وتيك توك وسناب شات وإكس', 'مهارة في كتابة المحتوى وحس إبداعي',
  'يُفضَّل من لديه خبرة في قطاع المطاعم', 'للتقديم: أرسل/ي سيرتك الذاتية وسابقة أعمالك على البريد الإلكتروني', 'hr@otlobny.co',
];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = []; page.on('pageerror', e => errs.push(String(e)));
  await page.goto('file://' + html);
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await page.evaluate(tl => window.initTimeline(tl), TL);
  const sc = await page.evaluate(() => { window.seek(3); return [scrollX, scrollY, document.documentElement.scrollWidth, document.documentElement.scrollHeight]; });
  console.log('scroll state', sc);
  // on-screen text = exactly the allowed advert strings, nothing else
  const txt = await page.evaluate(() => {
    const norm = s => s.replace(/\s+/g, ' ').trim();
    return { units: [...document.querySelectorAll('[data-copy]')].map(e => norm(e.textContent)), all: norm(document.body.innerText).replace(/\s/g, ''),
      fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight),
      email: (() => { const e = document.getElementById('email'), cs = getComputedStyle(e); const r = document.createRange(); r.selectNodeContents(e); return [e.getAttribute('dir'), cs.direction, cs.unicodeBidi, r.getClientRects().length]; })() };
  });
  const issues = [];
  const ph = await page.evaluate(() => [...document.images].map(im => ({ src: im.getAttribute('src'), nat: im.naturalWidth / im.naturalHeight, shown: im.offsetWidth / im.offsetHeight, w: im.naturalWidth, f: getComputedStyle(im).filter })));
  for (const q of ph) { if (!/^\.\.\/assets\/tbc-restaurants-company_(burger|chicken-roll|cheeseburger)-photo_client-supplied\.png$/.test(q.src) || !q.w || Math.abs(q.nat - q.shown) > 0.01 || /hue|saturate|sepia|invert|contrast|brightness|blur/.test(q.f)) issues.push('photo problem ' + JSON.stringify(q)); }
  console.log('photos:', ph.length, 'all client-supplied, aspect kept');
  if (JSON.stringify(txt.units) !== JSON.stringify(ALLOWED)) issues.push('COPY MISMATCH ' + JSON.stringify(txt.units));
  if (txt.all !== txt.units.join('').replace(/\s/g, '')) issues.push('extra visible text');
  if (txt.email.join() !== 'ltr,ltr,isolate,1') issues.push('email: ' + txt.email);
  if (errs.length) issues.push('page errors: ' + errs.join(' | '));
  console.log('copy/dir check:', issues.length ? issues : 'ok', '| fonts:', txt.fonts.join(', '));
  if (issues.length) { await browser.close(); process.exit(1); }
  const arg = n => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : null; };
  if (process.argv.includes('--check')) { await browser.close(); return; }
  const clip = { x: 0, y: 0, width: 1080, height: 1920 };
  if (arg('--times')) {
    const out = path.join(__dirname, 'stills'); fs.mkdirSync(out, { recursive: true });
    for (const t of arg('--times').split(',').map(Number)) {
      await page.evaluate(x => window.seek(x), t);
      await page.screenshot({ path: path.join(out, 't_' + t.toFixed(2).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 90, clip });
    }
    await browser.close(); return;
  }
  const out = path.join(__dirname, 'frames'); fs.mkdirSync(out, { recursive: true });
  for (const f of fs.readdirSync(out)) fs.unlinkSync(path.join(out, f)); // frames are regenerated render cache
  const n = Math.round(TL.duration * TL.fps);
  const t0 = Date.now();
  for (let f = 0; f < n; f++) {
    await page.evaluate(x => window.seek(x), f / TL.fps);
    await page.screenshot({ path: path.join(out, 'f_' + String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 96, clip });
    if (f % 100 === 0) console.log('frame', f, '/', n, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  if (errs.length) console.log('PAGE ERRORS', errs);
  console.log('done', n, 'frames in', ((Date.now() - t0) / 1000).toFixed(0) + 's');
  await browser.close();
})();
