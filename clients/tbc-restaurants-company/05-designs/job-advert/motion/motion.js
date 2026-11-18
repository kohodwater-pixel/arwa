/* Motion graphic, direction A — deterministic timeline.
   window.initTimeline(json) builds the tracks from timeline.json;
   window.seek(t) puts every element where it belongs at second t.
   Nothing depends on the wall clock, so frame capture is repeatable.

   Times are written as "<scene>+<seconds>" and resolved against timeline.json. */
(function () {
  'use strict';
  const E = {
    out: t => 1 - Math.pow(1 - t, 3),
    in: t => t * t * t,
    io: t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
    back: t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
    softback: t => { const c1 = 0.9, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
    bounce: t => {
      const n = 7.5625, d = 2.75;
      if (t < 1 / d) return n * t * t;
      if (t < 2 / d) return n * (t -= 1.5 / d) * t + 0.75;
      if (t < 2.5 / d) return n * (t -= 2.25 / d) * t + 0.9375;
      return n * (t -= 2.625 / d) * t + 0.984375;
    },
  };
  let TL = null;
  const tracks = [];
  const $ = id => document.getElementById(id);
  const T = expr => {
    if (typeof expr === 'number') return expr;
    const m = /^([a-z]+)([+-][\d.]+)?$/.exec(expr);
    const base = m[1] === 'end' ? TL.duration : TL.scenes[m[1]].start;
    return base + parseFloat(m[2] || 0);
  };

  /* add(id, {kind, init, moves, float, suffix, apply})
     kind  : 'svg' (transform attribute) | 'html' (centre-anchored) | 'rel' (inline, relative)
     init  : starting {x, y, s, r, o}
     moves : [[time, duration, {props}, ease], ...] — each eases from the value before it
     float : {ax, ay, ar, p, ph} continuous idle drift (px, px, deg, period s, phase 0..1) */
  function add(id, def) {
    const el = $(id);
    if (!el) throw new Error('missing element ' + id);
    const segs = {};
    for (const [time, dur, props, ease] of def.moves || []) {
      for (const k in props) (segs[k] = segs[k] || []).push({ t0: T(time), dur, to: props[k], ease: E[ease || 'io'] });
    }
    for (const k in segs) segs[k].sort((a, b) => a.t0 - b.t0);
    tracks.push({ el, kind: def.kind || 'html', init: Object.assign({ x: 0, y: 0, s: 1, r: 0, o: 1 }, def.init), segs, float: def.float, suffix: def.suffix || '', apply: def.apply });
  }
  function valueAt(tr, k, t) {
    let v = tr.init[k];
    const list = tr.segs[k];
    if (!list) return v;
    for (const s of list) {
      if (t >= s.t0 + s.dur) { v = s.to; continue; }
      if (t > s.t0) v = v + (s.to - v) * s.ease((t - s.t0) / s.dur);
      break;
    }
    return v;
  }
  function seek(t) {
    for (const tr of tracks) {
      const p = {};
      for (const k in tr.init) p[k] = valueAt(tr, k, t);
      for (const k in tr.segs) if (!(k in p)) p[k] = valueAt(tr, k, t);
      if (tr.float) {
        const f = tr.float, a = 2 * Math.PI * (t / f.p + (f.ph || 0));
        p.x += (f.ax || 0) * Math.sin(a); p.y += (f.ay || 0) * Math.cos(a); p.r += (f.ar || 0) * Math.sin(a * 0.7 + 1);
        if (f.as) p.s *= 1 + f.as * Math.sin(a * 1.3);
      }
      if (tr.apply) { tr.apply(tr.el, p, t); continue; }
      const o = Math.max(0, Math.min(1, p.o));
      if (tr.kind === 'svg') {
        tr.el.setAttribute('transform', `translate(${p.x.toFixed(2)} ${p.y.toFixed(2)}) rotate(${p.r.toFixed(3)}) scale(${Math.max(p.s, 0.0001).toFixed(4)}) ${tr.suffix}`);
        tr.el.setAttribute('opacity', o.toFixed(3));
      } else {
        const anchor = tr.kind === 'html' ? 'translate(-50%,-50%) ' : '';
        tr.el.style.transform = `translate(${p.x.toFixed(2)}px,${p.y.toFixed(2)}px) ${anchor}rotate(${p.r.toFixed(3)}deg) scale(${Math.max(p.s, 0.0001).toFixed(4)})`;
        tr.el.style.opacity = o.toFixed(3);
      }
    }
  }

  function build() {
    tracks.length = 0;
    const CX = 540;

    /* ---------- red disc behind the hero ---------- */
    add('disc', { kind: 'svg', init: { x: CX, y: 1060, s: 0, o: 1 }, float: { as: 0.012, p: 5 }, moves: [
      ['hook+0.15', 0.8, { s: 1 }, 'back'],
      ['headline+0', 0.9, { y: 1370, s: 0.86 }, 'io'],
      ['sector+0', 0.8, { y: 1330, s: 1.02 }, 'io'],
      ['remote+0', 0.7, { y: 1290, s: 1.0 }, 'io'],
      ['apply+0', 0.8, { y: 1020, s: 0.48 }, 'io'],
    ] });
    add('ring', { kind: 'svg', init: { x: 0, y: 0, o: 1 }, apply: (el, p, t) => el.setAttribute('transform', `rotate(${(t * 6).toFixed(2)})`) });

    /* ---------- phone ---------- */
    add('phone', { kind: 'svg', suffix: 'translate(-180 -350)', init: { x: CX, y: 2700, s: 1.6, r: 22, o: 1 }, float: { ax: 5, ay: 9, ar: 0.8, p: 4.2 }, moves: [
      ['hook+0.1', 0.95, { y: 1060, r: -8 }, 'softback'],
      ['headline+0', 0.9, { y: 1400, s: 1.36, r: -6 }, 'io'],
      ['sector+0', 0.75, { x: -520, y: 1750, r: -46 }, 'in'],
    ] });
    add('screenOff', { kind: 'svg', init: { o: 1 }, apply: (el, p) => el.setAttribute('opacity', Math.max(0, Math.min(1, p.o)).toFixed(3)), moves: [['hook+0.95', 0.3, { o: 0 }, 'out']] });
    add('phoneBurger', { kind: 'svg', suffix: 'translate(-180 -330)', init: { x: 180, y: 330, s: 0 }, moves: [
      ['hook+1.05', 0.55, { s: 1 }, 'back'],
    ] });
    add('likeHeart', { kind: 'svg', suffix: 'translate(-288 -482)', init: { x: 288, y: 482, s: 0 }, moves: [
      ['hook+1.5', 0.4, { s: 1.5 }, 'back'], ['hook+1.9', 0.3, { s: 1 }, 'io'],
    ] });

    /* ---------- reactions: burst out of the phone, then drift; one home per scene ---------- */
    const R = [
      ['r0', 1.25, 8, [[862, 610], [880, 1010], [935, 1010], [870, 220], [915, 1090]]],
      ['r1', 1.05, -10, [[188, 700], [180, 1080], [150, 1000], [180, 210], [160, 960]]],
      ['r2', 0.85, 0, [[940, 980], [945, 1340], [960, 1730], [950, 1720], [930, 1700]]],
      ['r3', 0.95, -12, [[128, 1130], [128, 1470], [110, 1760], [120, 1730], [130, 1710]]],
      ['r4', 0.85, 12, [[936, 1350], [920, 1660], [560, 1800], [540, 1790], [540, 1790]]],
      ['h0', 1.3, 14, [[300, 520], [100, 900], [80, 300], [330, 170], [240, 800]]],
      ['h1x', 1.0, -18, [[880, 800], [985, 1150], [1010, 820], [760, 250], [870, 860]]],
      ['h2', 0.85, 10, [[104, 900], [70, 1290], [330, 1790], [80, 1640], [70, 1250]]],
      ['h3', 0.95, 20, [[968, 1160], [1010, 1520], [800, 1790], [1000, 1600], [1010, 1280]]],
      ['h4', 0.75, -8, [[176, 1400], [70, 1680], [990, 240], [620, 150], [330, 1740]]],
      ['sp0', 1.0, 0, [[900, 470], [960, 860], [960, 330], [960, 380], [960, 760]]],
      ['sp1', 0.8, 0, [[120, 520], [90, 720], [110, 780], [100, 380], [110, 700]]],
      ['sp2', 0.7, 0, [[980, 1560], [300, 1800], [760, 250], [240, 1620], [760, 1640]]],
    ];
    const scenes = ['headline', 'sector', 'remote', 'apply'];
    R.forEach(([id, s, r, pos], i) => {
      const moves = [['hook+' + (1.35 + i * 0.09).toFixed(2), 0.7, { x: pos[0][0], y: pos[0][1], s, r }, 'back']];
      scenes.forEach((sc, k) => moves.push([sc + '+' + (0.05 + (i % 5) * 0.06).toFixed(2), 0.95, { x: pos[k + 1][0], y: pos[k + 1][1] }, 'io']));
      add(id, { kind: 'svg', init: { x: CX, y: 1010, s: 0, r: r - 40, o: 1 }, moves,
        float: { ax: 7 + (i % 3) * 3, ay: 12 + (i % 4) * 3, ar: 3, p: 3.2 + (i % 5) * 0.55, ph: i * 0.17, as: id.startsWith('sp') ? 0.25 : 0 } });
    });

    /* ---------- kicker ---------- */
    add('kicker', { init: { x: CX, y: 392, s: 0, o: 1 }, moves: [
      ['hook+1.9', 0.55, { s: 1 }, 'back'],
      ['headline+0', 0.7, { y: 334, s: 0.5 }, 'io'],
      ['remote+0', 0.4, { y: 290, o: 0 }, 'in'],
      ['apply+0.25', 0.5, { y: 330, o: 1 }, 'out'],
    ] });

    /* ---------- headline: word by word ---------- */
    add('h1', { init: { x: CX, y: 620, s: 1, o: 1 }, moves: [
      ['sector+0', 0.7, { y: 566, s: 0.92 }, 'io'],
      ['remote+0', 0.45, { y: 480, o: 0 }, 'in'],
      ['apply+0', 0.01, { y: 600, s: 0.78 }, 'io'],
      ['apply+0.15', 0.6, { y: 536, o: 1 }, 'out'],
    ] });
    [0.45, 0.95, 1.75, 2.2, 2.9, 3.4].forEach((d, i) => add('w' + i, { kind: 'rel', init: { x: 0, y: 70, s: 0.7, o: 0 }, moves: [
      ['headline+' + d, 0.5, { y: 0, s: 1 }, 'back'], ['headline+' + d, 0.22, { o: 1 }, 'out'],
    ] }));

    /* ---------- sector line + food settling in ---------- */
    add('sector', { init: { x: CX + 140, y: 852, s: 1, o: 0 }, moves: [
      ['sector+0.25', 0.55, { x: CX, o: 1 }, 'out'],
      ['remote+0', 0.4, { y: 800, o: 0 }, 'in'],
      ['apply+0', 0.01, { y: 760, s: 0.7 }, 'io'],
      ['apply+0.35', 0.5, { y: 722, o: 1 }, 'out'],
    ] });
    add('food', { kind: 'svg', init: { x: CX, y: 1424, s: 0.88, o: 1 }, float: { ay: 6, p: 4.6 }, moves: [
      ['remote+0', 0.6, { y: 2500 }, 'in'],
      ['apply+0', 0.01, { s: 0.46 }, 'io'],
      ['apply+0.2', 0.8, { y: 1112 }, 'softback'],
    ] });
    add('plate', { kind: 'svg', init: { x: 0, y: 0, s: 0 }, moves: [['sector+0.15', 0.6, { s: 1 }, 'back']] });
    add('fork', { kind: 'svg', init: { x: -900, y: -10, r: -40 }, moves: [['sector+0.45', 0.65, { x: -445, r: 0 }, 'back']] });
    add('knife', { kind: 'svg', init: { x: 900, y: -10, r: 40 }, moves: [['sector+0.55', 0.65, { x: 445, r: 0 }, 'back']] });
    add('foodBurger', { kind: 'svg', init: { x: 0, y: -1700, o: 1 }, moves: [['sector+0.55', 0.75, { y: 0 }, 'bounce']] });
    add('burgerShadow', { kind: 'svg', init: { x: 0, y: 0, s: 0 }, moves: [['sector+0.7', 0.5, { s: 1 }, 'out']] });
    add('hat', { kind: 'svg', init: { x: 14, y: -360, r: 34, s: 0 }, moves: [['sector+1.15', 0.35, { s: 1 }, 'back'], ['sector+1.2', 0.6, { y: -252, r: 8 }, 'bounce']] });

    /* ---------- remote badge stamps in, then the design requirement ---------- */
    add('tag', { init: { x: CX, y: 520, s: 2.6, r: -12, o: 0 }, moves: [
      ['remote+0.2', 0.32, { s: 1, r: -4 }, 'softback'], ['remote+0.2', 0.12, { o: 1 }, 'out'],
      ['apply+0', 0.7, { y: 806, s: 0.44, r: 0 }, 'io'],
    ] });
    add('shock', { kind: 'svg', init: { x: CX, y: 520, s: 0.2, o: 0 }, moves: [
      ['remote+0.42', 0.01, { o: 0.7 }, 'out'], ['remote+0.43', 0.7, { s: 1.5, o: 0 }, 'out'],
    ] });
    add('design', { init: { x: CX, y: 1120, s: 0.8, o: 0 }, moves: [
      ['remote+1.45', 0.6, { y: 900, s: 1 }, 'back'], ['remote+1.45', 0.25, { o: 1 }, 'out'],
      ['apply+0', 0.4, { y: 800, o: 0 }, 'in'],
    ] });
    const pen = $('penPath'), penLen = pen.getTotalLength();
    pen.setAttribute('stroke-dasharray', penLen.toFixed(1));
    add('penPath', { kind: 'svg', init: { o: 0 }, apply: (el, p) => el.setAttribute('stroke-dashoffset', (penLen * (1 - Math.max(0, Math.min(1, p.o)))).toFixed(1)), moves: [['remote+1.85', 0.75, { o: 1 }, 'io']] });
    add('penNib', { kind: 'svg', init: { o: 0, s: 0 }, apply: (el, p) => {
      const pt = pen.getPointAtLength(penLen * Math.max(0, Math.min(1, p.o)));
      el.setAttribute('transform', `translate(${pt.x.toFixed(1)} ${pt.y.toFixed(1)}) rotate(28) scale(${Math.max(p.s, 0.0001).toFixed(3)})`);
    }, moves: [['remote+1.7', 0.35, { s: 1 }, 'back'], ['remote+1.85', 0.75, { o: 1 }, 'io']] });
    for (let i = 0; i < 5; i++) add('sw' + i, { kind: 'svg', init: { x: 520 + i * 74, y: 76, s: 0, r: -20 }, moves: [['remote+' + (1.95 + i * 0.09).toFixed(2), 0.4, { s: 1, r: 0 }, 'back']] });
    [1170, 1262, 1354, 1446].forEach((y, i) => add('chip' + i, { init: { x: CX + (i % 2 ? -260 : 260), y, s: 0.9, o: 0 }, moves: [
      ['remote+' + (2.2 + i * 0.13).toFixed(2), 0.5, { x: CX, s: 1 }, 'back'], ['remote+' + (2.2 + i * 0.13).toFixed(2), 0.2, { o: 1 }, 'out'],
      ['apply+' + (i * 0.05).toFixed(2), 0.35, { y: y - 70, o: 0 }, 'in'],
    ] }));

    /* ---------- end card: apply sentence + the email ---------- */
    add('applyline', { init: { x: CX, y: 1352, s: 1, o: 0 }, moves: [['apply+0.45', 0.5, { y: 1314, o: 1 }, 'out']] });
    add('pill', { init: { x: CX, y: 1790, s: 0.6, o: 0 }, float: { as: 0.008, p: 2.4 }, moves: [
      ['apply+0.6', 0.6, { y: 1474, s: 1 }, 'back'], ['apply+0.6', 0.2, { o: 1 }, 'out'],
    ] });
    add('shine', { kind: 'rel', init: { x: -300 }, apply: (el, p) => { el.style.transform = `translateX(${p.x.toFixed(1)}px) skewX(-20deg)`; }, moves: [
      ['apply+1.4', 0.9, { x: 1150 }, 'io'], ['apply+3.0', 0.01, { x: -300 }, 'io'], ['apply+3.2', 0.9, { x: 1150 }, 'io'],
    ] });
  }

  window.initTimeline = function (json) { TL = json; build(); seek(0); return { duration: TL.duration, fps: TL.fps }; };
  window.seek = seek;

  /* preview only: open the HTML through a local web server and add ?play to the URL */
  if (location.search.includes('play')) {
    fetch('timeline.json').then(r => r.json()).then(json => {
      window.initTimeline(json);
      const t0 = performance.now();
      (function loop() { seek(((performance.now() - t0) / 1000) % json.duration); requestAnimationFrame(loop); })();
    });
  }
})();
