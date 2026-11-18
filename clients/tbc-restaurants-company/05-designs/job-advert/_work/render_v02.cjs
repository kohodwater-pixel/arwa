// v02 directions: render, assert copy, check layout, and write the data the
// contrast script needs (text-free background render + text boxes and colours).
// Run: NODE_PATH=/opt/node-tools/node_modules node _work/render_v02.cjs [a|b] [--boxes]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const dir = path.resolve(__dirname, '..');
const only = process.argv.slice(2).filter(a => !a.startsWith('--'));
const VER = { a: 'v03', b: 'v02' }; // current version per direction
const jobs = [];
for (const d of ['a', 'b']) {
  if (only.length && !only.includes(d)) continue;
  jobs.push({ name: `tbc-restaurants-company_job-advert_post-direction-${d}_ar_${VER[d]}`, w: 1080, h: 1350, safeTop: 36, safeBottom: 1314 });
  jobs.push({ name: `tbc-restaurants-company_job-advert_story-direction-${d}_ar_${VER[d]}`, w: 1080, h: 1920, safeTop: 290, safeBottom: 1580 });
}
const COPY = [
  'فرصة وظيفية',
  'موظف/ـة تسويق وإدارة حسابات التواصل الاجتماعي',
  'لشركة متخصصة في قطاع المطاعم',
  'العمل عن بُعد',
  'المهام',
  'إعداد خطة المحتوى الشهرية وتنفيذها',
  'إدارة حسابات التواصل الاجتماعي والنشر والتفاعل مع العملاء',
  'كتابة المحتوى الإعلاني والتنسيق مع المصممين والمصورين',
  'إدارة الحملات الإعلانية المدفوعة ومتابعة نتائجها',
  'إعداد تقارير الأداء الدورية',
  'المتطلبات',
  'خبرة سابقة في التسويق وإدارة حسابات التواصل الاجتماعي',
  'خبرة في التصميم (شرط أساسي)',
  'معرفة جيدة بمنصات إنستغرام وتيك توك وسناب شات وإكس',
  'مهارة في كتابة المحتوى وحس إبداعي',
  'يُفضَّل من لديه خبرة في قطاع المطاعم',
  'للتقديم: أرسل/ي سيرتك الذاتية وسابقة أعمالك على البريد الإلكتروني',
  'hr@otlobny.co',
];
const SEL = '.kicker,h1,.sector,.tag,.block h2,.block li,.apply p,.email';
(async () => {
  const browser = await chromium.launch();
  let bad = 0;
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.join(dir, j.name + '.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
    const r = await page.evaluate(({ COPY, SEL, j }) => {
      const out = { issues: [], info: {}, texts: [] };
      const norm = s => s.replace(/\s+/g, ' ').trim();
      const els = [...document.querySelectorAll(SEL)];
      const units = els.map(e => norm(e.textContent));
      if (JSON.stringify(units) !== JSON.stringify(COPY)) out.issues.push('COPY MISMATCH: ' + JSON.stringify(units));
      // no visible text anywhere else (svg <text>, pseudo content, stray nodes)
      if (norm(document.body.innerText) .replace(/\s/g, '') !== units.join('').replace(/\s/g, '')) out.issues.push('extra visible text: ' + norm(document.body.innerText).slice(0, 200));
      if (document.querySelector('svg text, svg image')) out.issues.push('svg text / svg image present');
      // the only raster allowed is the client's burger photograph, shown at its own aspect ratio
      const imgs = [...document.querySelectorAll('img')];
      for (const im of imgs) { const ok = /assets\/tbc-restaurants-company_burger-photo_client-supplied\.png$/.test(im.getAttribute('src')); const ar = im.naturalWidth / im.naturalHeight, shown = im.offsetWidth / im.offsetHeight; if (!ok || !im.naturalWidth || Math.abs(ar - shown) > 0.01) out.issues.push('image problem: ' + im.getAttribute('src') + ' ' + ar.toFixed(3) + ' vs ' + shown.toFixed(3)); const cs = getComputedStyle(im); out.info.photo = im.offsetWidth + 'x' + im.offsetHeight + ' of ' + im.naturalWidth + 'x' + im.naturalHeight; if (/hue|saturate|sepia|invert|contrast|brightness/.test(cs.filter)) out.issues.push('photo is colour-filtered'); }
      out.info.fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
      const em = document.querySelector('.email'), ecs = getComputedStyle(em);
      if (em.getAttribute('dir') !== 'ltr' || ecs.direction !== 'ltr' || ecs.unicodeBidi !== 'isolate') out.issues.push('email direction');
      const leaves = [...document.querySelectorAll('.kicker span,h1 .a,h1 .b1,h1 .b2,h1 .b:not(:has(span)),.sector,.tag span,.block h2,.block li,.apply p,.email')];
      const rects = [];
      const nLinesOf = ls => Math.max(1, new Set(ls.map(q => Math.round(q.top / 6))).size);
      for (const e of leaves) {
        const cs = getComputedStyle(e), fs = parseFloat(cs.fontSize);
        const range = document.createRange(); range.selectNodeContents(e);
        const lines = [...range.getClientRects()].filter(q => q.width > 2 && q.height > 2);
        const b0 = range.getBoundingClientRect();
        // Cairo reports a very tall line box; trim to the ink zone (cap/descender band) for the geometric checks
        const trim = cs.fontFamily.includes('Cairo') ? b0.height * 0.2 / nLinesOf(lines) : 0;
        const b = { left: b0.left, right: b0.right, top: b0.top + trim, bottom: b0.bottom - trim, width: b0.width, height: b0.height - 2 * trim };
        const key = (e.className || e.parentElement.className || e.tagName) + ':' + norm(e.textContent).slice(0, 22);
        const nLines = new Set(lines.map(q => Math.round(q.top / 6))).size;
        if (b.left < 36 || b.right > j.w - 36) out.issues.push('outside side margin: ' + key + ' ' + Math.round(b.left) + '-' + Math.round(b.right));
        if (b.top < j.safeTop || b.bottom > j.safeBottom) out.issues.push('outside safe zone: ' + key + ' ' + Math.round(b.top) + '-' + Math.round(b.bottom));
        if (e.matches('li') && fs < 28) out.issues.push('body < 28px: ' + key);
        if (!e.matches('li') && nLines > 1) out.issues.push('wraps: ' + key);
        if (cs.letterSpacing !== 'normal' && cs.letterSpacing !== '0px') out.issues.push('letter-spacing: ' + key);
        const lh = parseFloat(cs.lineHeight) / fs;
        if (e.matches('li') && (lh < 1.5 || lh > 1.9)) out.issues.push('line-height ' + lh.toFixed(2) + ': ' + key);
        rects.push({ key, b, e });
        out.texts.push({ key, x: Math.floor(b.left), y: Math.floor(b.top), w: Math.ceil(b.width), h: Math.ceil(b.height), color: cs.color, fs, weight: cs.fontWeight, lines: nLines, kind: e.matches('li,.sector,.apply p') ? 'body' : 'display' });
      }
      // text must not collide with other text
      for (let a = 0; a < rects.length; a++) for (let c = a + 1; c < rects.length; c++) {
        const A = rects[a].b, B = rects[c].b;
        const ox = Math.min(A.right, B.right) - Math.max(A.left, B.left), oy = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
        if (ox > 4 && oy > 10) out.issues.push('text overlap: ' + rects[a].key + ' x ' + rects[c].key + ' (' + Math.round(ox) + 'x' + Math.round(oy) + ')');
      }
      // lists must fit their cards
      for (const blk of document.querySelectorAll('.block')) {
        const bb = blk.getBoundingClientRect(), last = blk.querySelector('li:last-child').getBoundingClientRect();
        const pad = parseFloat(getComputedStyle(blk).paddingBottom) || 0;
        out.info['slack ' + norm(blk.querySelector('h2').textContent)] = Math.round(bb.bottom - last.bottom);
        if (last.bottom > bb.bottom - Math.min(pad, 12)) out.issues.push('list overflows card: ' + norm(blk.querySelector('h2').textContent));
        if (blk.scrollWidth > blk.clientWidth + 1) out.issues.push('card h-overflow');
      }
      if (document.documentElement.scrollHeight > j.h || document.documentElement.scrollWidth > j.w) out.issues.push('page overflow');
      return out;
    }, { COPY, SEL, j });
    const shot = { clip: { x: 0, y: 0, width: j.w, height: j.h } };
    await page.screenshot({ path: path.join(dir, '_work', j.name + '_raw.png'), ...shot });
    // background-only render: same page, glyphs made invisible (used to measure contrast on real pixels)
    await page.addStyleTag({ content: '.kicker,h1 span,.sector,.tag,.block h2,.block li,.apply p,.email{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}' });
    await page.screenshot({ path: path.join(dir, '_work', j.name + '_bg.png'), ...shot });
    fs.writeFileSync(path.join(dir, '_work', j.name + '_texts.json'), JSON.stringify(r.texts, null, 1));
    console.log('==', j.name, '\n issues:', r.issues.length ? r.issues : 'none', '\n', JSON.stringify(r.info));
    if (process.argv.includes('--boxes')) for (const t of r.texts) console.log(' ', t.key, [t.x, t.y, t.x + t.w, t.y + t.h], t.fs + 'px', 'lines', t.lines);
    bad += r.issues.length;
    await page.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
