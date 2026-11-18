/* hippo style frames v01 — builds the vector graphic devices and fits the headline widths.
   The "ears" device is our own vector approximation of the brand's lid/ear graphic (a rounded head with two ear bumps,
   drawn as a thick outline). It is not traced or cropped from the logo mark. */
(function () {
  const q = new URLSearchParams(location.search);
  const f = q.get('f');
  if (f) { document.body.classList.add('single'); const el = document.getElementById(f); if (el) el.classList.add('on'); }
  if (q.get('notext')) document.body.classList.add('notext');

  // seeded random so every render is identical
  const rng = seed => () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
  let uid = 0;

  // ---- ears: outline of (rounded head ∪ two ear circles), stroke drawn outside the shape via a mask
  document.querySelectorAll('.ears').forEach(el => {
    const c = el.dataset.color, sw = +el.dataset.sw, id = 'e' + (uid++);
    el.style.color = c;
    const shape = `<rect x="100" y="220" width="800" height="720" rx="330"/><circle cx="170" cy="290" r="92"/><circle cx="830" cy="290" r="92"/>`;
    el.innerHTML = `<svg viewBox="0 0 1000 1000"><defs><mask id="${id}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="1400" height="1400">
      <g fill="#fff" stroke="#fff" stroke-width="${sw * 2}" stroke-linejoin="round">${shape}</g><g fill="#000">${shape}</g></mask></defs>
      <rect x="-200" y="-200" width="1400" height="1400" fill="${c}" mask="url(#${id})"/></svg>`;
  });

  // ---- organic blob with the cluster of dots
  document.querySelectorAll('.blob').forEach(el => {
    const fill = el.dataset.fill, dots = el.dataset.nodots ? '' :
      [[250, 190], [320, 190], [215, 250], [285, 250], [355, 250], [250, 310], [320, 310]].map(p => `<circle cx="${p[0]}" cy="${p[1]}" r="15" fill="#fff"/>`).join('');
    el.innerHTML = `<svg viewBox="0 0 760 640"><path fill="${fill}" d="M150,70 C300,-30 520,10 600,130 C670,240 770,300 740,440 C710,580 520,640 370,600 C240,566 110,600 40,470 C-30,340 20,160 150,70Z"/>${dots}</svg>`;
  });

  // ---- impact burst: thick short strokes radiating from a point
  document.querySelectorAll('.burst').forEach(el => {
    const n = +el.dataset.n, r1 = +el.dataset.r1, r2 = +el.dataset.r2, [a0, a1] = el.dataset.arc.split(',').map(Number);
    let s = '';
    for (let i = 0; i < n; i++) {
      const a = (a0 + (a1 - a0) * i / (n - 1)) * Math.PI / 180, k = i % 2 ? 0.86 : 1;
      s += `<line x1="${800 + Math.cos(a) * r1}" y1="${800 + Math.sin(a) * r1 * .62}" x2="${800 + Math.cos(a) * r2 * k}" y2="${800 + Math.sin(a) * r2 * k * .62}"/>`;
    }
    el.innerHTML = `<svg viewBox="0 0 1600 1600"><g stroke="${el.dataset.color}" stroke-width="${el.dataset.w}" stroke-linecap="round">${s}</g></svg>`;
  });

  // ---- sparks / crumbs of light (dark look)
  document.querySelectorAll('.sparks').forEach(el => {
    const r = rng(+el.dataset.seed), n = +el.dataset.n, [x, y, w, h] = el.dataset.box.split(',').map(Number), cols = el.dataset.colors.split(',');
    let s = '';
    for (let i = 0; i < n; i++) {
      const cx = x + r() * w, cy = y + r() * h, rad = 2 + r() * r() * 9, c = cols[Math.floor(r() * cols.length)], o = .25 + r() * .7, b = r() < .35 ? 5 : r() < .5 ? 2 : 0;
      s += `<circle cx="${cx}" cy="${cy}" r="${rad}" fill="${c}" opacity="${o}" ${b ? `filter="blur(${b}px)" style="filter:blur(${b}px)"` : ''}/>`;
    }
    el.innerHTML = `<svg viewBox="0 0 1080 1920">${s}</svg>`;
  });

  // ---- glossy floating spheres with depth blur (floating-cards look). [x, y, r, colour, blur]
  const ORBS = {
    1: [[60, 170, 50, 'lime', 7], [960, 700, 34, 'pink', 2], [90, 800, 26, 'white', 0], [985, 1250, 70, 'violet', 5], [215, 1640, 46, 'pink', 3], [850, 1700, 30, 'lime', 1]],
    2: [[1050, 150, 120, 'pink', 16], [60, 1500, 150, 'lime', 20], [1010, 1760, 90, 'white', 14]],
    3: [[1040, 180, 56, 'lime', 6], [70, 700, 30, 'white', 1], [1010, 1150, 34, 'pink', 2], [560, 1700, 60, 'violet', 4], [240, 1760, 36, 'lime', 2]],
    4: [[40, 1120, 110, 'pink', 16], [1030, 1690, 150, 'lime', 20]],
    5: [[1040, 170, 50, 'lime', 5], [70, 660, 34, 'pink', 2], [540, 760, 22, 'white', 0], [900, 1700, 56, 'violet', 4], [330, 1740, 34, 'pink', 2]],
    6: [[1040, 1380, 110, 'pink', 16], [80, 1760, 140, 'lime', 20]],
    7: [[60, 200, 70, 'lime', 6], [1020, 420, 44, 'pink', 3], [40, 1000, 36, 'white', 1], [1035, 1180, 50, 'violet', 4], [240, 1740, 60, 'pink', 4]],
    8: [[30, 1560, 130, 'lime', 18], [1010, 150, 110, 'pink', 16]]
  };
  const GRAD = { lime: ['#E8F58A', '#BBD032', '#7E8F12'], pink: ['#FFC2DE', '#E75A9E', '#A82C6C'], violet: ['#C9B8FF', '#7B5FC2', '#45308A'], white: ['#ffffff', '#F3E6FF', '#B9A2E6'] };
  document.querySelectorAll('.orbs').forEach(el => {
    const set = ORBS[el.dataset.set] || []; let defs = '', s = '';
    set.forEach(o => {
      const id = 'g' + (uid++), g = GRAD[o[3]];
      defs += `<radialGradient id="${id}" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="${g[0]}"/><stop offset=".5" stop-color="${g[1]}"/><stop offset="1" stop-color="${g[2]}"/></radialGradient>`;
      s += `<circle cx="${o[0]}" cy="${o[1]}" r="${o[2]}" fill="url(#${id})" style="filter:blur(${o[4]}px)"/>`;
    });
    el.innerHTML = `<svg viewBox="0 0 1080 1920"><defs>${defs}</defs>${s}</svg>`;
  });

  // ---- fit headlines to an exact width (px) once the fonts are in
  const fonts = ['300 100px "Tajawal"', '800 100px "Tajawal"', 'italic 500 100px "Playfair Display"'];
  window.ready = Promise.all(fonts.map(x => document.fonts.load(x, 'حُطّ ثقلك Franchise'))).then(() => document.fonts.ready).then(() => {
    document.querySelectorAll('[data-fit]').forEach(el => {
      el.style.fontSize = '100px';
      const w = el.getBoundingClientRect().width;
      el.style.fontSize = (100 * (+el.dataset.fit) / w).toFixed(1) + 'px';
    });
    window.fontsOk = fonts.map(x => document.fonts.check(x, 'حُطّ'));
    return Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => { }) : 0));
  });
})();
