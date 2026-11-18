/* Motion graphic v04, direction A — deterministic timeline.
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
    const SC = ['headline', 'sector', 'require', 'apply'];
    const C = TL.scenes.hook.cues;                 // hook cue offsets (timeline.json)
    const H = d => 'hook+' + d.toFixed(2);

    /* ---------- warm glow follows the hero ---------- */
    add('glow', { init: { x: CX, y: 1010, s: 0.5, o: 0 }, float: { as: 0.03, p: 5 }, moves: [
      ['hook+0', 0.9, { s: 1, o: 1 }, 'out'],
      ['headline+0', 0.9, { y: 1340, s: 0.95 }, 'io'],
      ['sector+0', 0.8, { y: 1300, s: 1.12 }, 'io'],
      ['require+0', 0.7, { y: 860, s: 1.05 }, 'io'],
      ['apply+0', 0.8, { y: 1060, s: 0.86 }, 'io'],
    ] });

    /* ---------- phone: enters, feed swipes through three posts ---------- */
    const PS = 1.6, PR = -6, PY = 1030;           // phone scale, tilt and centre in the hook
    add('phone', { init: { x: CX, y: 2750, s: PS, r: 16, o: 1 }, moves: [
      ['hook+0', 0.7, { y: PY, r: PR }, 'softback'],
      ['headline+0', 0.9, { y: 1440, s: 1.3, r: -5 }, 'io'],
      ['sector+0', 0.7, { y: 2800, r: -16 }, 'in'],
      ['sector+0.7', 0.01, { o: 0 }, 'io'],
    ] });
    add('feed', { kind: 'rel', init: { x: 0, y: 0, o: 1 }, moves: [
      [H(C.swipes[0]), 0.32, { y: -540 }, 'io'], [H(C.swipes[1]), 0.32, { y: -1080 }, 'io'], [H(C.swipes[2]), 0.32, { y: -1620 }, 'io'],
    ] });
    add('feedBurger', { kind: 'rel', init: { o: 1 }, apply: (el, p) => { el.style.opacity = p.o < 0.5 ? 0 : 1; }, moves: [[H(C.pop), 0.02, { o: 0 }, 'io']] });

    /* ---------- hero burger: starts exactly over the in-screen photo, then pops out ---------- */
    const rad = PR * Math.PI / 180;
    const hx = CX + 70 * PS * Math.sin(rad), hy = PY - 70 * PS * Math.cos(rad) - 252 * 0.02 * PS;   // photo centre on the screen
    add('hero', { init: { x: hx, y: hy, s: 252 * PS / 800, r: PR, o: 0 }, float: { ay: 5, p: 4.4 }, moves: [
      [H(C.pop), 0.02, { o: 1 }, 'io'],
      [H(C.pop + 0.02), 0.6, { x: CX, y: 936, s: 0.94, r: -3 }, 'back'],
      ['headline+0', 0.9, { y: 1290, s: 0.76 }, 'io'],
      ['sector+0', 0.9, { y: 1372, s: 0.78, r: -2 }, 'io'],
      ['require+0', 0.8, { y: 1404, s: 0.5, r: 0 }, 'io'],
      ['apply+0', 0.5, { y: 1062, s: 0.56, r: -2 }, 'io'],
    ] });

    /* ---------- supporting photographs: float in with parallax ---------- */
    add('roll', { init: { x: -320, y: 1150, s: 0.44, r: -14, o: 1 }, float: { ax: 4, ay: 9, ar: 0.6, p: 5.2, ph: 0.2 }, moves: [
      ['sector+0.2', 0.9, { x: 252, y: 1082, r: -6 }, 'out'], ['sector+1.1', 1.5, { x: 276 }, 'io'],
      ['require+0', 0.8, { x: 204, y: 1396, s: 0.33, r: -4 }, 'io'],
      ['apply+0', 0.5, { x: 204, y: 1022, s: 0.33, r: -8 }, 'io'],
    ] });
    add('cheese', { init: { x: 1400, y: 1170, s: 0.44, r: 14, o: 1 }, float: { ax: 4, ay: 8, ar: 0.6, p: 4.6, ph: 0.6 }, moves: [
      ['sector+0.35', 0.9, { x: 836, y: 1096, r: 5 }, 'out'], ['sector+1.25', 1.4, { x: 814 }, 'io'],
      ['require+0', 0.8, { x: 876, y: 1400, s: 0.33, r: 3 }, 'io'],
      ['apply+0', 0.5, { x: 878, y: 1026, s: 0.33, r: 6 }, 'io'],
    ] });

    /* ---------- reactions: a glass card and three hearts fire on each post ---------- */
    const like = [CX + (120 * Math.cos(rad) - 110 * Math.sin(rad)) * PS, PY + (120 * Math.sin(rad) + 110 * Math.cos(rad)) * PS]; // like button on screen
    const fire = C.fire;
    fire.forEach((t0, p) => {
      for (let j = 0; j < 3; j++) {
        const dx = (j - 1) * 120 + (p - 1) * 30, rise = 300 + j * 70 + p * 20, st = 'hook+' + (t0 + j * 0.08).toFixed(2);
        add('bh' + p + j, { init: { x: like[0], y: like[1], s: 0, r: (j - 1) * 18, o: 0 }, moves: [
          [st, 0.05, { o: 1 }, 'out'], [st, 0.35, { s: 1 }, 'back'],
          [st, 1.0, { x: like[0] + dx, y: like[1] - rise }, 'out'],
          ['hook+' + (t0 + j * 0.08 + 0.55).toFixed(2), 0.45, { o: 0 }, 'in'],
        ] });
      }
    });
    const cards = [
      ['cardA', C.fire[0] - 0.04, 1.15, 5, [[884, 624], [900, 1010], [938, 1330], [900, 250], [906, 232]]],
      ['cardB', C.fire[1] - 0.04, 1.05, -5, [[186, 760], [170, 1090], [140, 1330], [176, 236], [170, 222]]],
    ];
    cards.forEach(([id, t0, s, r, pos], i) => {
      const moves = [[H(t0), 0.5, { s }, 'back'], [H(t0), 0.15, { o: 1 }, 'out']];
      SC.forEach((sc, k) => moves.push([sc + '+' + (0.02 + i * 0.05).toFixed(2), 0.6, { x: pos[k + 1][0], y: pos[k + 1][1] }, 'io']));
      add(id, { init: { x: pos[0][0], y: pos[0][1], s: 0, r, o: 0 }, moves, float: { ax: 6, ay: 11, ar: 1.5, p: 4 + i * 0.7, ph: i * 0.3 } });
    });
    add('cardC', { init: { x: 892, y: 930, s: 0, r: 4, o: 0 }, float: { ay: 8, p: 3.6 }, moves: [
      [H(C.fire[2] - 0.04), 0.5, { s: 1.05 }, 'back'], [H(C.fire[2] - 0.04), 0.15, { o: 1 }, 'out'], [H(C.pop), 0.4, { y: 870, o: 0 }, 'in'],
    ] });
    const am = [
      [[150, 566], [86, 900], [58, 934], [56, 596], [58, 884]],
      [[934, 800], [990, 1150], [1022, 940], [1024, 606], [1022, 892]],
      [[110, 1016], [70, 1290], [70, 1500], [56, 1010], [350, 1700]],
      [[960, 1244], [1004, 1500], [1012, 1524], [1026, 1020], [730, 1722]],
      [[172, 1330], [140, 1560], [330, 1650], [330, 180], [540, 1790]],
      [[904, 476], [962, 884], [762, 1660], [760, 170], [80, 1600]],
    ];
    am.forEach((pos, i) => {
      const st = H(C.pop + 0.08 + i * 0.05);
      const moves = [[st, 0.05, { o: 1 }, 'out'], [st, 0.7, { x: pos[0][0], y: pos[0][1], s: 1, r: (i % 2 ? 14 : -14) }, 'back']];
      SC.forEach((sc, k) => moves.push([sc + '+' + (0.02 + (i % 3) * 0.04).toFixed(2), 0.6, { x: pos[k + 1][0], y: pos[k + 1][1] }, 'io']));
      add('am' + i, { init: { x: CX, y: 936, s: 0, r: 0, o: 0 }, moves, float: { ax: 6 + (i % 3) * 3, ay: 12 + (i % 4) * 3, ar: 4, p: 3.2 + (i % 5) * 0.5, ph: i * 0.19 } });
    });

    /* ---------- kicker ---------- */
    add('kicker', { init: { x: CX, y: 372, s: 0, o: 1 }, moves: [
      [H(C.kicker), 0.5, { s: 1 }, 'back'],
      ['headline+0', 0.7, { y: 334, s: 0.5 }, 'io'],
      ['require+0', 0.28, { y: 290, o: 0 }, 'in'],
      ['apply+0.45', 0.4, { y: 330, o: 1 }, 'out'],
    ] });

    /* ---------- headline: word by word ---------- */
    add('h1', { init: { x: CX, y: 620, s: 1, o: 1 }, moves: [
      ['sector+0', 0.7, { y: 566, s: 0.92 }, 'io'],
      ['require+0', 0.28, { y: 500, o: 0 }, 'in'],
      ['apply+0', 0.01, { y: 590, s: 0.78 }, 'io'],
      ['apply+0.45', 0.5, { y: 536, o: 1 }, 'out'],
    ] });
    TL.scenes.headline.words.forEach((d, i) => add('w' + i, { kind: 'rel', init: { x: 0, y: 70, s: 0.7, o: 0 }, moves: [
      ['headline+' + d, 0.45, { y: 0, s: 1 }, 'back'], ['headline+' + d, 0.18, { o: 1 }, 'out'],
    ] }));

    /* ---------- sector line ---------- */
    add('sector', { init: { x: CX + 140, y: 852, s: 1, o: 0 }, moves: [
      ['sector+' + TL.scenes.sector.line, 0.45, { x: CX, o: 1 }, 'out'],
      ['require+0', 0.28, { y: 810, o: 0 }, 'in'],
      ['apply+0', 0.01, { y: 752, s: 0.7 }, 'io'],
      ['apply+0.7', 0.4, { y: 722, o: 1 }, 'out'],
    ] });

    /* ---------- beat 4: three items in turn — experience, design, salary ---------- */
    const IT = TL.scenes.require.items;           // start offsets of the three items (timeline.json)
    const at = (i, d) => 'require+' + (IT[i] + (d || 0)).toFixed(2);
    add('exp', { init: { x: CX, y: 540, s: 0.9, o: 0 }, moves: [
      [at(0), 0.45, { y: 470, s: 1 }, 'back'], [at(0), 0.2, { o: 1 }, 'out'],
      ['apply+0', 0.3, { y: 420, o: 0 }, 'in'],
    ] });
    add('n3', { kind: 'rel', init: { x: 0, y: 0, s: 0, r: -25, o: 1 }, moves: [
      [at(0, 0.12), 0.45, { s: 1.25, r: 0 }, 'back'], [at(0, 0.6), 0.3, { s: 1 }, 'io'],
    ] });
    add('design', { init: { x: CX, y: 980, s: 0.8, o: 0 }, moves: [
      [at(1), 0.55, { y: 800, s: 1 }, 'back'], [at(1), 0.22, { o: 1 }, 'out'],
      ['apply+0', 0.3, { y: 740, o: 0 }, 'in'],
    ] });
    const pen = $('penPath'), penLen = pen.getTotalLength();
    pen.setAttribute('stroke-dasharray', penLen.toFixed(1));
    add('penPath', { kind: 'svg', init: { o: 0 }, apply: (el, p) => el.setAttribute('stroke-dashoffset', (penLen * (1 - Math.max(0, Math.min(1, p.o)))).toFixed(1)), moves: [[at(1, 0.4), 0.75, { o: 1 }, 'io']] });
    add('penNib', { kind: 'svg', init: { o: 0, s: 0 }, apply: (el, p) => {
      const pt = pen.getPointAtLength(penLen * Math.max(0, Math.min(1, p.o)));
      el.setAttribute('transform', `translate(${pt.x.toFixed(1)} ${pt.y.toFixed(1)}) rotate(28) scale(${Math.max(p.s, 0.0001).toFixed(3)})`);
    }, moves: [[at(1, 0.25), 0.35, { s: 1 }, 'back'], [at(1, 0.4), 0.75, { o: 1 }, 'io']] });
    for (let i = 0; i < 5; i++) add('sw' + i, { kind: 'svg', init: { x: 520 + i * 74, y: 76, s: 0, r: -20 }, moves: [[at(1, 0.5 + i * 0.09), 0.4, { s: 1, r: 0 }, 'back']] });
    add('badge', { init: { x: CX, y: 1140, s: 2.6, r: -12, o: 0 }, moves: [
      [at(2), 0.32, { s: 1, r: -4 }, 'softback'], [at(2), 0.12, { o: 1 }, 'out'],
      ['apply+0', 0.25, { o: 0 }, 'in'],
      ['apply+0.3', 0.01, { y: 806, s: 0.36, r: 0 }, 'io'],
      ['apply+0.6', 0.35, { s: 0.44 }, 'back'], ['apply+0.6', 0.18, { o: 1 }, 'out'],
    ] });
    add('shock', { init: { x: CX, y: 1140, s: 0.2, o: 0 }, moves: [
      [at(2, 0.22), 0.01, { o: 0.7 }, 'out'], [at(2, 0.23), 0.7, { s: 1.5, o: 0 }, 'out'],
    ] });

    /* ---------- end card: apply sentence + the email ---------- */
    add('applyline', { init: { x: CX, y: 1340, s: 1, o: 0 }, moves: [['apply+' + TL.scenes.apply.sentence, 0.4, { y: 1314 }, 'out'], ['apply+' + TL.scenes.apply.sentence, 0.22, { o: 1 }, 'out']] });
    /* the pill rises a short way from below its rest position, with no overshoot, so it never reaches the sentence above */
    add('pill', { init: { x: CX, y: 1530, s: 0.82, o: 0 }, float: { as: 0.006, p: 2.4 }, moves: [
      ['apply+' + TL.scenes.apply.email, 0.5, { y: 1476, s: 1 }, 'out'], ['apply+' + TL.scenes.apply.email, 0.2, { o: 1 }, 'out'],
    ] });
    add('shine', { kind: 'rel', init: { x: -300 }, apply: (el, p) => { el.style.transform = `translateX(${p.x.toFixed(1)}px) skewX(-20deg)`; }, moves: [
      ['apply+2.4', 0.9, { x: 1150 }, 'io'], ['apply+4.4', 0.01, { x: -300 }, 'io'], ['apply+4.6', 0.9, { x: 1150 }, 'io'],
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
