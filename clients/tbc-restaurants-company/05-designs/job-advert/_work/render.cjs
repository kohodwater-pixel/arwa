// Renders both adverts to PNG and runs copy + layout assertions.
// Run: node _work/render.cjs   (from anywhere)
const { chromium } = require('playwright');
const path = require('path');
const dir = path.resolve(__dirname, '..');
const base = 'tbc-restaurants-company_job-advert_';
const jobs = [
  { name: base + 'post_ar_v01', w: 1080, h: 1350, safeTop: 0, safeBottom: 1350 },
  { name: base + 'story_ar_v01', w: 1080, h: 1920, safeTop: 250, safeBottom: 1580 },
];
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
  'للتقديم: أرسل/ي سيرتك الذاتية ونماذج من أعمالك',
  'مكان الشعار',
  'وسيلة التقديم (بريد / واتساب / رابط)',
];
(async () => {
  const browser = await chromium.launch();
  let bad = 0;
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.join(dir, j.name + '.html'));
    await page.evaluate(() => document.fonts.ready);
    const r = await page.evaluate(({ COPY, j }) => {
      const out = { issues: [], info: {} };
      const norm = s => s.replace(/\s+/g, ' ').trim();
      // exact copy: the visible text units, in order, must equal the brief
      const units = [...document.querySelectorAll('.kicker,h1,.sector,.tag,.block h2,.block li,.apply p,.gap')].map(e => norm(e.textContent));
      const order = ['فرصة وظيفية', 'مكان الشعار', ...COPY.slice(1, 17), 'وسيلة التقديم (بريد / واتساب / رابط)'];
      if (JSON.stringify(units) !== JSON.stringify(order)) out.issues.push('COPY MISMATCH: ' + JSON.stringify(units));
      // no text outside those units
      const all = norm(document.querySelector('main').textContent);
      if (all !== norm(units.join(' '))) out.issues.push('extra text in main');
      // fonts
      out.info.fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
      const boxes = {};
      for (const e of document.querySelectorAll('.kicker,.gap,h1 .a,h1 .b,.sector,.tag,.block h2,.block li,.apply,.apply p,.rail')) {
        const range = document.createRange(); range.selectNodeContents(e);
        const tb = e.matches('.apply,.rail,.gap,.tag') ? e.getBoundingClientRect() : range.getBoundingClientRect();
        const key = (e.className || e.tagName) + ':' + norm(e.textContent).slice(0, 18);
        boxes[key] = [Math.round(tb.left), Math.round(tb.top), Math.round(tb.right), Math.round(tb.bottom)];
        const m = 40;
        const full = e.matches('.apply');
        if (!full && (tb.left < m || tb.right > j.w - m)) out.issues.push('outside side margin: ' + key);
        if (tb.top < j.safeTop || tb.bottom > j.safeBottom) out.issues.push('outside safe zone: ' + key + ' ' + Math.round(tb.top) + '-' + Math.round(tb.bottom));
        if (e.scrollWidth > e.clientWidth + 1 && e.clientWidth) out.issues.push('h-overflow: ' + key);
        const fs = parseFloat(getComputedStyle(e).fontSize);
        if (e.matches('li') && fs < 30) out.issues.push('body < 30px');
        if (e.matches('li')) { const lines = Math.round(tb.height / (fs * parseFloat(getComputedStyle(e).lineHeight) / fs)); if (lines > 1) out.issues.push('li wraps: ' + key); }
        if (getComputedStyle(e).letterSpacing !== 'normal' && getComputedStyle(e).letterSpacing !== '0px') out.issues.push('letter-spacing on ' + key);
      }
      // rail must not collide with list text
      const rail = document.querySelector('.rail').getBoundingClientRect();
      for (const li of document.querySelectorAll('.block li,.block h2')) {
        const range = document.createRange(); range.selectNodeContents(li); const b = range.getBoundingClientRect();
        if (b.left < rail.right + 24) out.issues.push('rail collision: ' + norm(li.textContent).slice(0, 20) + ' left=' + Math.round(b.left));
      }
      const lists = document.querySelector('.lists'), last = document.querySelectorAll('.block')[1].getBoundingClientRect();
      out.info.listSlack = Math.round(lists.getBoundingClientRect().bottom - last.bottom);
      if (out.info.listSlack < 8) out.issues.push('lists overflow into band');
      if (document.documentElement.scrollHeight > j.h || document.documentElement.scrollWidth > j.w) out.issues.push('page overflow');
      out.info.boxes = boxes;
      return out;
    }, { COPY, j });
    await page.screenshot({ path: path.join(dir, '_work', j.name + '_raw.png'), clip: { x: 0, y: 0, width: j.w, height: j.h } });
    console.log('==', j.name, '\n issues:', r.issues.length ? r.issues : 'none', '\n slack:', r.info.listSlack, '\n fonts:', r.info.fonts.join(', '));
    if (process.argv.includes('--boxes')) console.log(r.info.boxes);
    bad += r.issues.length;
    await page.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
