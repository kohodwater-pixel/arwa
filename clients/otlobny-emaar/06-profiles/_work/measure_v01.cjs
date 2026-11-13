// Overflow and fit measurements for the profile HTML. Usage: node measure_v01.cjs <html>
const path = require('path');
const { chromium } = require(require.resolve('playwright', { paths: ['/home/user/arwa', '/home/user/arwa/scripts', process.cwd()] }));
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1200, height: 800 } });
  await pg.goto('file://' + path.resolve(process.argv[2]), { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  const r = await pg.evaluate(() => {
    const mm = v => +(v * 25.4 / 96).toFixed(1); const out = [];
    for (const p of document.querySelectorAll('.page')) {
      const n = p.dataset.page, pr = p.getBoundingClientRect(); const o = { page: n, w: mm(pr.width), h: mm(pr.height), scroll: [mm(p.scrollWidth), mm(p.scrollHeight)], issues: [] };
      const txt = e => (e.textContent || '').trim().slice(0, 28);
      for (const e of p.querySelectorAll('p,h1,h2,h3,div.lbl,div.body,div.hdg,div.lead,span.lbl,.li,.pill,.cval,.num,img.frame,.pc img')) {
        const q = e.getBoundingClientRect(); if (!q.width) continue;
        const L = mm(q.left - pr.left), T = mm(q.top - pr.top), R = mm(q.right - pr.left), B = mm(q.bottom - pr.top);
        if (L < 18.8 || R > 278.2 || T < 9 || B > 201) o.issues.push(`OUT ${e.tagName}.${e.className} [${L},${T},${R},${B}] "${txt(e)}"`);
        if (e.scrollWidth > e.clientWidth + 1 && e.clientWidth) o.issues.push(`WIDE ${e.className} "${txt(e)}"`);
      }
      for (const e of p.querySelectorAll(".fit,.why")) { let m = 0; const q = e.getBoundingClientRect(); for (const c of e.querySelectorAll('*')) m = Math.max(m, c.getBoundingClientRect().bottom); o.issues.push(`fit row h=${mm(q.height)} content-bottom-gap=${mm(q.bottom - m)}`); }
      for (const e of p.querySelectorAll('.svc')) { const q = e.getBoundingClientRect(); const hs = [...e.children].map(c => { let t = 1e9, bt = 0; for (const x of c.querySelectorAll('.hdg,.body,.holder,.pg')) { const z = x.getBoundingClientRect(); t = Math.min(t, z.top); bt = Math.max(bt, z.bottom); } return mm(bt - t); }); o.issues.push(`svc row h=${mm(q.height)} content(en,mid,ar)=${hs}`); }
      for (const e of p.querySelectorAll('.trip,.pindex,.pgrid,.crows,.rows')) { const q = e.getBoundingClientRect(); o.issues.push(`${e.className.split(' ')[0]} top=${mm(q.top - pr.top)} bottom=${mm(q.bottom - pr.top)}`); }
      for (const e of p.querySelectorAll('.ttl-c,.ttl-s,.ttl-p')) { const q = e.getBoundingClientRect(); const rg = document.createRange(); rg.selectNodeContents(e); const t = rg.getBoundingClientRect(); o.issues.push(`title ${e.lang} box[${mm(q.left - pr.left)}..${mm(q.right - pr.left)}] text-w=${mm(t.width)} top=${mm(q.top - pr.top)} bottom=${mm(q.bottom - pr.top)} lines=${Math.round(q.height / parseFloat(getComputedStyle(e).lineHeight))}`); }
      for (const e of p.querySelectorAll('.why .body,.svc .body,.li span,.pj,.r3 span')) { const lh = parseFloat(getComputedStyle(e.closest('.li,.lbl') || e).lineHeight); const n = Math.round(e.getBoundingClientRect().height / lh); if (n > 1) o.issues.push(`lines=${n} ${e.closest('[lang]').lang} "${txt(e)}"`); }
      out.push(o);
    }
    return out;
  });
  for (const o of r) { console.log(`p${o.page} ${o.w}x${o.h} scroll ${o.scroll}`); for (const i of o.issues) console.log('   ' + i); }
  await b.close();
})();
