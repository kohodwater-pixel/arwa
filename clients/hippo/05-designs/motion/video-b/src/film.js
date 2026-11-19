/* hippo — franchise motion ad «حُطّ ثقلك» — look B — film v03.
   Deterministic: window.seek(t) lays out the whole frame for film time t (seconds); nothing depends on a clock.
   HIT TIMES are frames of the approved audio mix v02 (frame = round(t*30); «أثقل.» = first frame after the VO onset). */
(function () {
  const FPS = 30, DUR = 40, F = f => f / FPS;
  const P_ = '#DA6FA2', L_ = '#BBD032', K_ = '#181717', W_ = '#ffffff';
  const HIT = {
    hook: F(30),                                  // 1.000
    taps: [94, 106, 117, 129].map(F),             // 3.138 / 3.523 / 3.907 / 4.291
    squish: F(198),                               // 6.600
    proof: [216, 255, 294].map(F),                // 7.200 / 8.500 / 9.800
    heavy: F(375), punch: F(386),                 // 12.500 / 12.86
    chips: [456, 480, 504, 528].map(F), stack: F(549),   // 15.2 / 16.0 / 16.8 / 17.6 / 18.3
    box: F(582), athqal: F(655),                  // 19.400 / 21.81 -> 21.833
    quiet: F(720), cta: F(888), end: F(999), logo: F(1146)   // 24.0 / 29.600 / 33.300 / 38.200
  };
  const BEAT = 0.51219, BEAT0 = 3.012;            // music grid (120 BPM slowed 2.44 %)

  // ---------- maths
  const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, k) => a + (b - a) * k;
  const tw = (t, a, b) => cl((t - a) / (b - a));
  const eo3 = k => 1 - Math.pow(1 - cl(k), 3);
  const eio = k => { k = cl(k); return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
  const back = (k, c = 2.4) => { k = cl(k); return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
  const spr = (u, k = 9, w = 30) => u < -1e-6 ? 0 : Math.exp(-k * Math.max(u, 0)) * Math.cos(w * Math.max(u, 0));
  const on = (t, t0) => t - t0 > -1e-6;
  const hop = (t, t0, d, h) => { const k = tw(t, t0, t0 + d); return (k <= 0 || k >= 1) ? 0 : -h * Math.sin(Math.PI * k); };
  const beat = t => ((t >= 3 && t < 24) || (t >= HIT.cta && t < 37.3)) ? Math.exp(-((((t - BEAT0) % BEAT) + BEAT) % BEAT) * 9) : 0;
  // an object that arrives during the 3 frames before its hit and makes contact ON the hit frame, then squashes
  function land(t, t0, { d = 0.1, from = 2.3, A = 0.12 } = {}) {
    const u = t - t0;
    if (u < -d - 1e-6) return { o: 0, sx: 1, sy: 1 };
    if (u < -1e-6) { const k = -u / d, s = 1 + (from - 1) * k; return { o: cl(1.15 - k), sx: s, sy: s }; }
    const q = spr(u, 8, 30); return { o: 1, sx: 1 + A * q, sy: 1 - A * 1.3 * q };
  }
  // a big element that is simply THERE on the hit frame, oversized, and settles
  function slam(t, t0, { z = 0.35, A = 0.1 } = {}) {
    if (!on(t, t0)) return { o: 0, sx: 1, sy: 1 };
    const u = Math.max(t - t0, 0), zz = 1 + z * Math.exp(-u * 16), q = spr(u, 7, 28);
    return { o: 1, sx: zz * (1 + A * q), sy: zz * (1 - A * 1.3 * q) };
  }

  // ---------- DOM helpers
  const $ = id => document.getElementById(id);
  function P(el, o) {
    const r = (+el.dataset.r || 0) + (o.r || 0), s = o.s == null ? 1 : o.s;
    const sx = (o.sx == null ? 1 : o.sx) * s, sy = (o.sy == null ? 1 : o.sy) * s;
    el.style.transform = `translate(${(o.x || 0).toFixed(2)}px,${(o.y || 0).toFixed(2)}px) rotate(${r.toFixed(3)}deg) scale(${sx.toFixed(4)},${sy.toFixed(4)})`;
    el.style.opacity = o.o == null ? 1 : cl(o.o).toFixed(3);
  }

  // ---------- vector devices (our own drawings)
  document.querySelectorAll('.ears').forEach(el => {     // open band: wide low arc between two small bumps, sides running on
    const d = 'M -40 1500 C -30 900 0 520 120 330 C 30 270 20 120 140 85 C 250 55 320 140 300 235 C 430 165 570 165 700 235 C 680 140 750 55 860 85 C 980 120 970 270 880 330 C 1000 520 1030 900 1040 1500';
    el.innerHTML = `<svg viewBox="0 0 1000 700"><path d="${d}" fill="none" stroke="${el.dataset.color}" stroke-width="${el.dataset.sw}" stroke-linejoin="round" stroke-linecap="round"/></svg>`;
  });
  document.querySelectorAll('.blob').forEach(el => {
    const dc = el.dataset.dots || '#fff', dots = el.dataset.nodots ? '' :
      [[250, 190], [320, 190], [215, 250], [285, 250], [355, 250], [250, 310], [320, 310]].map(p => `<circle cx="${p[0]}" cy="${p[1]}" r="15" fill="${dc}"/>`).join('');
    el.innerHTML = `<svg viewBox="0 0 760 640"><path fill="${el.dataset.fill}" d="M150,70 C300,-30 520,10 600,130 C670,240 770,300 740,440 C710,580 520,640 370,600 C240,566 110,600 40,470 C-30,340 20,160 150,70Z"/>${dots}</svg>`;
  });
  document.querySelectorAll('.burst').forEach(el => {
    const n = +el.dataset.n, r1 = +el.dataset.r1, r2 = +el.dataset.r2, [a0, a1] = el.dataset.arc.split(',').map(Number);
    let s = '';
    for (let i = 0; i < n; i++) {
      const a = (a0 + (a1 - a0) * i / (n - 1)) * Math.PI / 180, k = i % 2 ? 0.86 : 1;
      s += `<line x1="${800 + Math.cos(a) * r1}" y1="${800 + Math.sin(a) * r1 * .62}" x2="${800 + Math.cos(a) * r2 * k}" y2="${800 + Math.sin(a) * r2 * k * .62}"/>`;
    }
    el.innerHTML = `<svg viewBox="0 0 1600 1600"><g stroke="${el.dataset.color}" stroke-width="${el.dataset.w}" stroke-linecap="round">${s}</g></svg>`;
  });
  document.querySelectorAll('.star').forEach(el => {     // sticker burst
    const n = +el.dataset.pts; let p = '';
    for (let i = 0; i < n * 2; i++) { const a = Math.PI * i / n, r = i % 2 ? 70 : 100; p += `${100 + Math.cos(a) * r},${100 + Math.sin(a) * r} `; }
    el.innerHTML = `<svg viewBox="0 0 200 200"><polygon points="${p}" fill="#181717" transform="translate(9,10)"/><polygon points="${p}" fill="${el.dataset.fill}" stroke="#181717" stroke-width="5" stroke-linejoin="round"/></svg>`;
  });

  // ---------- global layers
  const SCENES = [['s1', 0, 3], ['s2', 3, 7], ['s34', 7, 15], ['s5', 15, HIT.box], ['s6', HIT.box, 24], ['s78', 24, HIT.end], ['s9', HIT.end, 41]];
  const bgAt = t => t < 3 ? P_ : t < 7 ? K_ : t < HIT.heavy ? P_ : t < 15 ? L_ : t < HIT.box ? K_ : t < HIT.end ? L_ : W_;
  // colour bands that peel away behind the new scene's content, starting on the cut
  const ACCENT = [[7, [L_]], [HIT.heavy, [P_]], [15, [L_, P_]], [HIT.box, [P_]]];   // never a band colour that would swallow the text above it
  const FLASH = [[HIT.hook, .6, '#F3C4DC'], [HIT.box, .6, '#E4EDA6'], [HIT.athqal, .4, '#E4EDA6'], [HIT.cta, .5, '#E4EDA6']];   // a pale tint of the ground itself: never white, never opaque
  const SHAKE = [[HIT.hook, 34, .6], [F(83), 7, .2], ...HIT.taps.map(x => [x, 5, .15]), [F(199), 10, .3], [HIT.proof[0], 16, .35], [HIT.proof[1], 16, .35], [HIT.proof[2], 20, .4],
    [HIT.heavy, 18, .5], [HIT.punch, 10, .25], ...HIT.chips.map(x => [x, 13, .3]), [HIT.stack, 26, .5], [HIT.box, 46, .9], [HIT.athqal, 20, .45], [HIT.cta, 22, .6], [HIT.end, 8, .25]];
  const accentEls = [...document.querySelectorAll('#accent i')];

  function globals(t, te) {
    $('bg').style.background = bgAt(t);
    SCENES.forEach(([id, a, b]) => { $(id).style.display = (on(t, a) && !on(t, b)) ? 'block' : 'none'; });
    accentEls.forEach(e => { e.style.display = 'none'; });
    ACCENT.forEach(([t0, cols]) => {
      if (!on(t, t0) || t - t0 > 0.45) return;
      cols.forEach((c, i) => {
        const k = eo3(tw(t, t0 - 0.03 + i * 0.045, t0 + 0.3 + i * 0.045)), e = accentEls[i];
        e.style.display = 'block'; e.style.background = c;
        e.style.transform = `translateX(${(-1380 + k * 3300).toFixed(1)}px) skewX(-14deg)`;
      });
    });
    let f = 0; FLASH.forEach(([t0, a, c]) => { if (on(t, t0)) { const v = a * Math.exp(-(t - t0) * 20); if (v > f) { f = v; $('flash').style.background = c; } } });
    $('flash').style.opacity = f < 0.01 ? 0 : f.toFixed(3);
    let x = 0, y = 0, r = 0;
    SHAKE.forEach(([t0, amp, dur], i) => {
      const u = te - t0; if (u < -1e-6 || u >= dur) return;
      const a = amp * Math.pow(1 - u / dur, 2);
      x += 0.6 * a * Math.sin(u * 131); y += a * Math.cos(u * 109); r += a * 0.022 * Math.sin(u * 77);   // first frame of a hit: straight down
    });
    return { x, y, r };
  }

  // ---------- scene 1 · hook
  function s1(t) {
    const te = (t >= 0.92 && t < 1 - 1e-6) ? 0.92 : t, u = te - HIT.hook, hit = on(te, HIT.hook), ant = tw(te, 0.45, 0.92);
    P($('s1ears'), { x: 46 * Math.sin(te * 0.9) - ant * 30, y: 22 * spr(u, 5, 20) - ant * 14 });
    P($('s1slab'), { y: 18 * spr(u, 6, 22) });
    P($('s1blob'), { x: 14 * Math.sin(te * 1.3), y: 10 * Math.cos(te * 1.1) + 20 * spr(u, 6, 20), r: 3 * Math.sin(te * 0.8), s: 1 + 0.08 * spr(u, 6, 22) });
    P($('s1shadow'), { o: hit ? 0 : ant * 0.8, s: 0.25 + 0.85 * ant });
    if (!hit) {
      const k = back(tw(te, 0.1, 0.34));
      P($('s1word'), { s: lerp(0.9, 1.06, k) + ant * 0.03, y: 250 + 9 * Math.sin(te * 4.6) - ant * 34, x: ant * 5 * Math.sin(te * 70), r: 1.3 * Math.sin(te * 3.1) });
    } else {
      P($('s1word'), { r: -3.5 - 4 * spr(u, 5, 19), x: -10 - 12 * spr(u, 6, 21), y: 26 + 5 * Math.sin(te * 2.6) - 26 * spr(u, 7, 24), s: 1 + 0.05 * spr(u, 8, 26) });
    }
    const S = slam(te, HIT.hook, { z: 0.28, A: 0.11 }), lift = hop(te, F(74), 0.3, 34), thud = 0.05 * spr(te - F(83), 10, 32);
    P($('s1sw'), { o: S.o, sx: S.sx * (1 + thud), sy: S.sy * (1 - thud * 1.3), y: lift + 4 * Math.sin(te * 2.2), r: 0.6 * Math.sin(te * 1.9) + 2.5 * spr(u, 6, 24) });
    const bs = lerp(0.45, 1, back(tw(te, HIT.hook, HIT.hook + 0.2))) * (1 + 0.03 * Math.sin(te * 7));
    P($('s1bk'), { o: hit ? 1 : 0, s: bs }); P($('s1bw'), { o: hit ? 1 : 0, s: bs, r: 2 * Math.sin(te * 1.4) });
    return { zoom: 1 + 0.03 * eio(tw(te, 1.3, 3.0)) };
  }

  // ---------- scene 2 · «بريوش طري.»
  function s2(t) {
    let q = 0.07 * spr(t - 3, 9, 30); HIT.taps.forEach(h => { q += 0.075 * spr(t - h, 9, 34); });
    const press = on(t, F(196)) ? (t < F(200) ? Math.pow(tw(t, F(196), F(200)), 1.6) : spr(t - F(200), 5.5, 19)) : 0;   // deepest on frame 200 (sound peak 6.64)
    P($('s2sw'), { sx: (1 + q) * (1 + 0.13 * press), sy: (1 - 1.3 * q) * (1 - 0.22 * press), r: 0.6 * Math.sin(t * 1.9), y: 4 * Math.sin(t * 2.3) });
    const wk = back(tw(t, 3.0, 3.22));
    P($('s2word'), { o: 1, s: lerp(0.7, 1, wk), sx: (1 + q * 0.7) * (1 + 0.08 * press), sy: (1 - q) * (1 - 0.14 * press), y: 18 * press + 6 * Math.sin(t * 2.1), r: 0.8 * Math.sin(t * 1.5) });
    ['s2st1', 's2st2', 's2st3', 's2st4'].forEach((id, i) => {
      const h = HIT.taps[i], k = back(tw(t, h, h + 0.2), 3.2);
      P($(id), { o: on(t, h) ? 1 : 0, s: k * (1 + 0.05 * beat(t)) * (1 + 0.28 * (on(t, F(200)) ? spr(t - F(200), 6, 20) : 0)), r: (i % 2 ? -1 : 1) * t * 24, x: (i % 2 ? 1 : -1) * 16 * press, y: 6 * Math.sin(t * 2 + i) });
    });
    let bq = 0; HIT.taps.forEach(h => { bq += spr(t - h, 9, 30); });
    P($('s2bk'), { s: lerp(0.6, 1, back(tw(t, 3.0, 3.2))) * (1 + 0.05 * bq + 0.1 * press + 0.02 * beat(t)), r: 1.5 * Math.sin(t * 1.2) });
    P($('s2ears'), { x: 50 * Math.sin(t * 0.8 + 1), y: 14 * q * 10 });
    P($('s2slab'), { y: 60 * q + 16 * press });
    P($('s2blob'), { x: 12 * Math.sin(t * 1.2), y: 10 * Math.cos(t), r: 4 * Math.sin(t * 0.7), s: 1 + 0.04 * beat(t) });
    return { zoom: 1 };
  }

  // ---------- scenes 3 + 4 · proof, then «خبز خفيف. حضور ثقيل.»
  const LA = { k1: { dx: -217, dy: -431, s: 1.5 }, k2: { dx: 276, dy: -150, s: 1.6 }, k3: { dx: -25, dy: 54, s: 1.15 }, k4: { dx: -6, dy: 25, s: 1.05 } };
  const KH = { k1: 0, k2: 1, k3: 2, k4: 2 };
  function s34(t) {
    const m = eio(tw(t, 11.0, 11.55)), lime = on(t, HIT.heavy);
    $('s3earsL').style.display = lime ? 'none' : 'block'; $('s3earsP').style.display = lime ? 'block' : 'none';
    const ex = { x: 40 * Math.sin(t * 0.7), y: 16 * Math.cos(t * 0.9), r: 2 * Math.sin(t * 0.5) }; P($('s3earsL'), ex); P($('s3earsP'), ex);
    P($('s3blob'), { x: 12 * Math.sin(t * 1.1), y: 10 * Math.cos(t * 0.9), r: 4 * Math.sin(t * 0.6), s: 1 + 0.05 * spr(t - HIT.heavy, 6, 20) });
    $('k3').style.background = lime ? P_ : L_;
    Object.keys(LA).forEach((id, i) => {
      const a = LA[id], h = HIT.proof[KH[id]], Ld = land(t, h, { from: 2.5, A: 0.13 });
      let y = 0; HIT.proof.forEach(hh => { if (hh > h + 1e-6) y += hop(t, hh, 0.26, 20); });
      y += hop(t, HIT.heavy, 0.3, 30) + hop(t, HIT.punch, 0.2, 10);
      P($(id), { o: Ld.o, x: lerp(a.dx, 0, m), y: lerp(a.dy, 0, m) + y, s: lerp(a.s, 1, m) * (1 + 0.012 * beat(t)), sx: Ld.sx, sy: Ld.sy, r: 0.7 * Math.sin(t * 1.7 + i * 2) });
    });
    let sy = 0, sq = 0, bo = 0;
    [...HIT.proof, HIT.heavy].forEach(h => { sy += hop(t, h, 0.32, 56); sq += 0.09 * spr(t - h - 0.32, 9, 30); if (on(t, h)) bo = Math.max(bo, 1 - tw(t, h, h + 0.55)); });
    const g1 = eo3(tw(t, HIT.proof[1] - 0.07, HIT.proof[1] + 0.1)), g2 = eo3(tw(t, HIT.proof[2] - 0.07, HIT.proof[2] + 0.1));
    const ss = lerp(lerp(1.83, 1.36, g1), 1, g2), sty = lerp(lerp(-489, -262, g1), 0, g2), in0 = 0.08 * spr(t - 7, 8, 28);
    P($('s3sw'), { y: sty + (g2 >= 1 ? sy : 0) + 3 * Math.sin(t * 2.2), sx: ss * (1 + sq + in0), sy: ss * (1 - 1.3 * (sq + in0)), r: 0.8 * Math.sin(t * 1.8) + 3 * spr(t - HIT.proof[0], 6, 22) });
    P($('s3b'), { o: on(t, HIT.proof[2] + 0.1) ? bo : 0, s: 0.75 + 0.3 * (1 - bo) });
    // light line: floats in big, is shoved up small when the heavy line lands
    const big = on(t, HIT.heavy) ? 0.22 * spr(t - HIT.heavy, 9, 26) : 1, inn = eo3(tw(t, 11.05, 11.45));
    P($('s4light'), { o: tw(t, 11.05, 11.3), s: 1 + 0.5 * big, y: 170 * big + 70 * (1 - inn) + 8 * Math.sin(t * 2.4), r: 0.9 * Math.sin(t * 1.6) });
    const S = slam(t, HIT.heavy, { z: 0.06, A: 0.1 }), pu = 1 + 0.075 * spr(t - HIT.punch, 8, 30) + 0.012 * beat(t);
    P($('s4heavy'), { o: S.o, sx: S.sx * pu, sy: S.sy * pu });
    P($('s4en'), { o: on(t, F(393)) ? 1 : 0, s: back(tw(t, F(393), F(393) + 0.22)) });
    // the composition tips with each landing and levels out before the headline
    const TG = [-1.2, 1.0, -1.4]; let tilt = 0, prev = 0;
    HIT.proof.forEach((h, i) => { if (on(t, h)) { tilt = prev + (TG[i] - prev) * (1 - spr(t - h, 5, 14)); } prev = TG[i]; });
    tilt = tilt * (1 - m) + 0.8 * Math.exp(-Math.max(t - HIT.heavy, 0) * 6) * Math.sin(Math.max(t - HIT.heavy, 0) * 20);
    return { zoom: 1, tilt };
  }

  // ---------- scene 5 · four chips stack on the bread
  function s5(t) {
    const all = [...HIT.chips, HIT.stack];
    let q = 0, gq = 0, n = 0, bo = 0;
    all.forEach((h, i) => { const big = i === 4; q += (big ? 0.16 : 0.06) * spr(t - h, 8, 28); if (i > 0) gq += (big ? 0.13 : 0.035) * spr(t - h, 8, 28); if (on(t, h)) { n = i + 1; bo = Math.max(bo, 1 - tw(t, h, h + (big ? 1.1 : 0.5))); } });
    const settle = 0.022 * n;
    P($('s5sw'), { sx: (1 + q) * (1 + settle * 0.5), sy: (1 - 1.3 * q) * (1 - settle), r: 0.5 * Math.sin(t * 1.7), y: 3 * Math.sin(t * 2.1) });
    $('s5stack').style.transform = `translateY(${(settle * 180).toFixed(1)}px) scale(${(1 + gq * 0.6).toFixed(4)},${(1 - gq).toFixed(4)})`;
    ['c1', 'c2', 'c3', 'c4'].forEach((id, i) => {
      const Ld = land(t, HIT.chips[i], { from: 2.4, A: 0.15 });
      P($(id), { o: Ld.o, sx: Ld.sx * (1 + 0.012 * beat(t)), sy: Ld.sy, r: 0.8 * Math.sin(t * 1.6 + i * 1.9), x: 5 * Math.sin(t * 1.3 + i) });
    });
    const eu = t - HIT.stack;
    P($('s5ears'), { x: 44 * Math.sin(t * 0.8), y: 12 * Math.cos(t * 0.7) + 30 * spr(eu, 6, 20), s: 1 + (on(t, HIT.stack) ? 0.1 * Math.exp(-eu * 10) : 0) });
    P($('s5slab'), { y: 50 * q });
    P($('s5blob'), { s: back(tw(t, 15.0, 15.25)) * (1 + 0.05 * beat(t) + 0.3 * spr(eu, 6, 20)), x: 12 * Math.sin(t * 1.2), y: 10 * Math.cos(t), r: 4 * Math.sin(t * 0.7) });
    P($('s5bk'), { o: bo, s: 0.8 + 0.25 * (1 - bo) + (on(t, HIT.stack) ? 0.1 : 0) });
    return { zoom: 1 + 0.02 * eio(tw(t, 15, 19.4)) };
  }

  // ---------- scene 6 · the gathering box
  function s6(t) {
    const u = t - HIT.box, ua = t - HIT.athqal, S = slam(t, HIT.box, { z: 0.12, A: 0.1 });
    const down = back(tw(t, F(613), F(613) + 0.3), 1.6), by = -300 * (1 - down), bz = 1 + 0.12 * (1 - down), aq = 0.08 * spr(ua, 8, 28);
    P($('s6box'), { o: S.o, s: bz, sx: S.sx * (1 + aq), sy: S.sy * (1 - 1.3 * aq), y: by + 4 * Math.sin(t * 2), r: 4.5 * spr(t - F(583), 4.5, 27) + 0.5 * Math.sin(t * 1.6) });
    const bs = lerp(0.4, 1, back(tw(t, HIT.box, HIT.box + 0.22))) * (1 + 0.03 * Math.sin(t * 7) + 0.08 * spr(ua, 7, 24));
    P($('s6bk'), { s: bs, y: by }); P($('s6bw'), { s: bs, y: by * 0.4, r: 2 * Math.sin(t * 1.3) });
    P($('s6ears'), { x: 46 * Math.sin(t * 0.8), y: by * 0.7 + 24 * spr(u, 5, 18), s: 1 + 0.18 * Math.exp(-Math.max(u, 0) * 9) });
    P($('s6earsT'), { x: -40 * Math.sin(t * 0.8), y: 560 * back(tw(t, HIT.box, HIT.box + 0.22), 1.4) - 700 * eio(tw(t, F(611), F(611) + 0.3)) + 20 * spr(u, 5, 18) });
    P($('s6blob'), { x: 14 * Math.sin(t * 1.3), y: 10 * Math.cos(t * 1.1) + 26 * spr(u, 6, 20), r: 3 * Math.sin(t * 0.8), s: 1 + 0.1 * spr(ua, 6, 22) + 0.03 * beat(t) });
    P($('s6blob2'), { x: 12 * Math.sin(t * 1.1), y: 10 * Math.cos(t * 0.9), r: 4 * Math.sin(t * 0.6), s: 1 + 0.08 * spr(u, 6, 20) });
    const qk = back(tw(t, F(613), F(613) + 0.24), 2);
    P($('s6q'), { o: on(t, F(613)) ? 1 : 0, y: -150 * (1 - qk) + 6 * Math.sin(t * 2.3) + hop(t, HIT.athqal, 0.25, 16), r: 0.8 * Math.sin(t * 1.5) });
    const A = slam(t, HIT.athqal, { z: 0.14, A: 0.11 }), pu = 1 + 0.014 * beat(t);
    P($('s6a'), { o: A.o, sx: A.sx * pu, sy: A.sy * pu });
    return { zoom: 1, tilt: 1.6 * Math.exp(-Math.max(u, 0) * 4) * Math.sin(Math.max(u, 0) * 16) };
  }

  // ---------- scenes 7 + 8 · the full side heavy and low, the empty seat light and high; «حُطّ ثقلك.» lands in the seat and levels the scale
  // proof stickers n1..n4 (same artwork as scene 4): b = big block in the top half, c = compact row above the food; offsets from their CSS place
  const NC = { n1: [741, 855, 867, 0.47], n2: [264, 915, 607, 0.47], n3: [805, 1161, 402, 0.45], n4: [324, 1210, 187, 0.47] };   // [css centre x, y, row centre x, row scale]
  const BIG = 0.86, NB = {};
  Object.keys(NC).forEach(id => { const [x, y, rx, cs] = NC[id]; NB[id] = { bx: 540 + (x - 545) * BIG - x, by: 505 + (y - 1063) * BIG - y, cx: rx - x, cy: 968 - y, cs }; });
  const SEAT = F(792);                             // the seat pops in at 26.4, already with its dots
  const SAY = F(828);                              // VO «ناقصها ثقلك» starts 27.60 (measured on the voice stem)
  function s78(t) {
    const te = (t >= 29.52 && t < HIT.cta - 1e-6) ? 29.52 : t, u = te - HIT.cta, cta = on(te, HIT.cta), u0 = te - 24;
    const sink = eio(tw(te, 24.0, 28.7)), rise = tw(te, 28.7, 29.52), k = cta ? spr(u, 5, 16) : 1;
    // boundary between the lime (empty) top and the pink (full) bottom: tipped while empty, level once the weight is in
    const Ly = 990 + 70 * sink * k, Ry = 990 - 70 * sink * k, sl = (Ry - Ly) / 1080;
    $('s7pink').style.clipPath = `polygon(0 ${(Ly - sl * 200 + 100).toFixed(1)}px,1480px ${(Ry + sl * 1280 + 100).toFixed(1)}px,1480px 2220px,0 2220px)`;
    P($('s7earsT'), { x: 26 * Math.sin(te * 0.7), y: 18 * Math.cos(te * 0.6) });
    P($('s7blobK'), { x: 10 * Math.sin(te * 0.9), y: 8 * Math.cos(te * 0.8), r: 3 * Math.sin(te * 0.5) });
    P($('s7earsB'), { x: 22 * Math.sin(te * 0.6 + 1), y: 12 * Math.cos(te * 0.7) + 26 * spr(u, 6, 20) });
    P($('s7blobD'), { x: 12 * Math.sin(te * 0.9), y: 10 * Math.cos(te * 0.8), r: 3 * Math.sin(te * 0.6), s: 1 + 0.12 * spr(u, 6, 22) + 0.03 * beat(te) });
    // full side: drops in, sinks and tips while the other side is empty; hops level on the hit
    $('s7full').style.transform = `translateY(${(40 * spr(u0, 5, 17) + 34 * sink * k + hop(te, HIT.cta, 0.34, 70)).toFixed(2)}px) rotate(${(-2.2 * sink * k).toFixed(3)}deg)`;
    const fq = 0.07 * spr(u0, 8, 26) + 0.06 * spr(u - 0.34, 9, 30);
    P($('s7box'), { r: 0.5 * Math.sin(te * 1.1), y: 3 * Math.sin(te * 1.4), sx: 1 + fq, sy: 1 - 1.3 * fq });
    P($('s7sw'), { r: 0.7 * Math.sin(te * 1.3 + 1), y: 4 * Math.sin(te * 1.6 + 2), sx: 1 + fq, sy: 1 - 1.3 * fq });
    const mv = eio(tw(te, 26.1, 26.42));
    Object.keys(NB).forEach((id, i) => {
      const a = NB[id], h = 24 + i * 0.1, pop = lerp(0.6, 1, back(tw(te, h, h + 0.24), 2.6));
      P($(id), { o: on(te, h) ? 1 : 0, x: lerp(a.bx, a.cx, mv), y: lerp(a.by, a.cy, mv) + 5 * Math.sin(te * 1.5 + i * 1.7) + hop(te, HIT.cta, 0.3, 22),
        s: pop * lerp(BIG, a.cs, mv) * (1 + 0.012 * beat(te)), r: 1.1 * Math.sin(te * 1.2 + i * 2) });
    });
    // the seat: pops in, floats high and tilted; swells with the riser; is slammed down and level by the headline
    const sIn = back(tw(te, SEAT, SEAT + 0.26), 2.4), said = on(te, SAY);
    const float = cta ? 0 : 1, sq = cta ? spr(u, 7, 26) : 0;
    P($('s7seat'), {
      o: on(te, SEAT) ? 1 : 0, s: sIn * (1 + rise * (0.03 + 0.012 * Math.sin((te - 28.7) * 34))) * (1 + 0.012 * beat(te)),
      sx: 1 + 0.035 * sq, sy: 1 - 0.09 * sq,
      y: float * (-26 * sink + 10 * Math.sin(te * 1.9)) + (cta ? 46 * spr(u, 6, 20) : 0) + 0.2 * 0,
      r: float * (-4 * sink + 1.1 * Math.sin(te * 1.3)) + (cta ? -4 * spr(u, 5, 17) : 0)
    });
    [...$('s7dots').children].forEach((d, i) => {
      const ph = ((te * 1.6 - i * 0.18) % 1 + 1) % 1, b = ph < 0.4 ? Math.sin(Math.PI * ph / 0.4) : 0;
      d.style.transform = `translateY(${(-26 * b).toFixed(1)}px) scale(${(said ? 1 - tw(te, SAY, SAY + 0.12) : 1).toFixed(3)})`;
    });
    // light line: appears in the seat with the voice; is knocked out of it by the headline
    const ko = cta ? tw(te, HIT.cta, HIT.cta + 0.17) : 0;
    P($('s7line'), { o: said && !cta ? 1 : 0, s: lerp(0.7, 1, back(tw(te, SAY, SAY + 0.24), 2)) * (1 - 0.3 * ko), y: 5 * Math.sin(te * 2.1) - 330 * ko, x: 260 * ko, r: 0.6 * Math.sin(te * 1.4) + 24 * ko });
    const S = slam(te, HIT.cta, { z: 0.04, A: 0.08 }), pu = 1 + 0.014 * beat(te);
    P($('s8cta'), { o: S.o, sx: S.sx * pu, sy: S.sy * pu });
    P($('s8en'), { o: on(te, F(898)) ? 1 : 0, s: back(tw(te, F(898), F(898) + 0.22)) });
    P($('s7pill'), { o: on(te, 24.3) ? 1 : 0, s: back(tw(te, 24.3, 24.55), 2.6) * (1 + 0.012 * Math.sin(te * 2.6) + 0.09 * spr(te - F(910), 7, 26)), y: hop(te, HIT.cta, 0.25, 12) });
    return { zoom: 1 + 0.028 * rise * (cta ? 0 : 1), tilt: cta ? 1.2 * Math.exp(-u * 5) * Math.sin(u * 18) : 0 };
  }

  // ---------- scene 9 · end card (the logo file is only placed and scaled uniformly; the QR is untouched after about 33.8 s)
  function s9(t) {
    const ul = t - HIT.logo;
    P($('s9ears'), { x: 300 * (1 - eo3(tw(t, HIT.end, HIT.end + 0.4))) + 14 * spr(ul, 5, 26) * -1, y: 14 * Math.sin(t * 0.8), r: 5 * spr(ul, 4.5, 26) });
    P($('s9logo'), { o: 1, s: lerp(0.9, 1, back(tw(t, HIT.end, HIT.end + 0.3), 1.8)) });
    const pk = eo3(tw(t, HIT.end, HIT.end + 0.2)), py = 260 * (1 - pk);
    P($('s9pink'), { y: py });
    P($('s9blobK'), { y: py + 8 * Math.cos(t * 0.8), x: 8 * Math.sin(t * 0.9), s: 1 + 0.07 * spr(ul, 6, 24) });
    P($('s9blobL'), { s: back(tw(t, F(1003), F(1003) + 0.3), 2.4) * (1 + 0.1 * spr(ul - 0.12, 6, 24) + 0.015 * Math.sin(t * 2)), x: 10 * Math.sin(t * 0.7), y: 8 * Math.cos(t * 0.9) });
    const H = slam(t, HIT.end, { z: 0.1, A: 0.08 }); P($('s9h'), { o: H.o, sx: H.sx, sy: H.sy, y: py });
    P($('s9en'), { o: on(t, F(1002)) ? 1 : 0, s: back(tw(t, F(1002), F(1002) + 0.2)) });
    P($('s9q'), { o: tw(t, F(1003), F(1003) + 0.15), y: 24 * (1 - eo3(tw(t, F(1003), F(1003) + 0.25))) });
    P($('s9qr'), { o: on(t, F(1004)) ? 1 : 0, s: lerp(0.5, 1, back(tw(t, F(1004), F(1004) + 0.3), 1.8)) });
    return { zoom: 1 };
  }

  const RUN = { s1, s2, s34, s5, s6, s78, s9 };
  window.seek = function (t) {
    t = cl(t, 0, DUR - 1 / FPS / 2);
    const te = (t >= 0.92 && t < 1 - 1e-6) ? 0.92 : (t >= 29.52 && t < HIT.cta - 1e-6) ? 29.52 : t;
    const g = globals(t, te);
    let cam = { zoom: 1, tilt: 0 };
    SCENES.forEach(([id, a, b]) => { if (on(t, a) && !on(t, b)) cam = Object.assign(cam, RUN[id](t)); });
    $('world').style.transform = `translate(${g.x.toFixed(2)}px,${g.y.toFixed(2)}px) rotate(${((cam.tilt || 0) + g.r).toFixed(3)}deg) scale(${(cam.zoom || 1).toFixed(4)})`;
  };
  window.HIT = HIT;

  // ---------- fonts, headline widths, preview
  const fonts = ['300 100px "Tajawal"', '800 100px "Tajawal"', 'italic 500 100px "Playfair Display"'];
  window.ready = Promise.all(fonts.map(x => document.fonts.load(x, 'حُطّ ثقلك Franchise'))).then(() => document.fonts.ready).then(() => {
    const sc = [...document.querySelectorAll('.scene')]; sc.forEach(s => { s.style.display = 'block'; });
    document.querySelectorAll('[data-fit]').forEach(el => {
      el.style.fontSize = '100px'; const w = el.getBoundingClientRect().width;
      el.style.fontSize = (100 * (+el.dataset.fit) / w).toFixed(1) + 'px';
    });
    window.fontsOk = fonts.map(x => document.fonts.check(x, 'حُطّ'));
    return Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => { }) : 0));
  }).then(() => { window.seek(0); });

  const q = new URLSearchParams(location.search);
  if (q.get('notext')) document.body.classList.add('notext');
  if (!q.get('render')) {
    document.body.classList.add('preview');
    const aud = $('aud'); let playing = false;
    $('play').onclick = () => { playing = !playing; playing ? aud.play() : aud.pause(); };
    (function loop() { if (playing) { window.seek(aud.currentTime); $('tc').textContent = aud.currentTime.toFixed(2); } requestAnimationFrame(loop); })();
  }
})();
