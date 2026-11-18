/* HIPPO — franchise motion ad «حُطّ ثقلك» — picture draft v01, 9:16, 1080x1920, 30 fps, 40 s.
   Deterministic: everything is a pure function of film time t (seconds). window.seek(t) draws one frame.
   Cut to audio mix v02 (see ../../audio/_work/mix-v02_report_2026-11-18.md). All hit times are in HIT below.

   EDIT HERE ---------------------------------------------------------------------------------- */
const CFG = {
  photos: {                      // the only two photographs in the film (+ the logo file)
    sandwich: 'assets/sandwich.png',   // cut-out of crispy-chicken.jpg  (tools/cutout.py)
    box:      'assets/box.png',        // cut-out of box-breakfast-89.jpg (tools/cutout_box.py)
    logo:     'assets/logo.png',       // client logo file, unmodified copy
  },
  qr: null,          // when the client sends the link: put the QR image at e.g. 'assets/qr.png' and set this path
  blink: false,      // eye-blink on the logo at 38.2 s. OFF in v01: see notes.md (which shapes are the eyes is unconfirmed)
  guides: false,     // draw platform safe-area guides (250 px top, 350 px bottom)
};
const COPY = {       // on-screen lines exactly as in concept-script v03 — do not rewrite
  s1: 'خفيف؟',
  s2: 'بريوش طري.',
  s3: [['فيلي', 'تشيز ستيك'], ['فرايد شرمب'], ['الحلومي']],
  s4a: 'خبز خفيف.', s4b1: 'حضور', s4b2: 'ثقيل.', s4en: 'Soft bread. Heavy presence.',
  s6a: 'وبوكس الجَمعات؟', s6b: 'أثقل.',
  s7a: 'ناقصها ثقلك.', s7b: 'امتياز هيبو التجاري',
  s8: 'حُطّ ثقلك.', s8en: 'Put your weight behind it.',
  s9a: 'امتياز هيبو التجاري', s9en: 'Franchise', s9b: 'للاستفسار عن الامتياز:',
  qrLabel: ['مكان رمز QR', 'يُضاف عند استلام الرابط'],   // draft placeholder label only; removed when CFG.qr is set
};
const C = { lime: '#BBD032', black: '#181717', pink: '#DA6FA2', hot: '#E75A9E', violet: '#7B5FC2', lime2: '#B8E23A', white: '#FFFFFF' };
const HIT = {        // seconds, from the audio timing table
  hook: 1.000, cups: [3.138, 3.523, 3.907, 4.291], squish: 6.600,
  names: [7.200, 8.500, 9.800], heavy: 12.500, thaqeel: 12.867,
  blocks: [15.200, 16.000, 16.800, 17.600, 18.300], box: 19.400, lid: [19.520, 19.740, 19.980],
  athqal: 21.810, musicStop: 24.000, cta: 29.600, endCard: 33.300, logoBlink: 38.200, logoTick: 38.320,
};
/* -------------------------------------------------------------------------------------------- */

const W = 1080, H = 1920, FPS = 30, DUR = 40, DEG = Math.PI / 180;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const IMG = {};

// ---------- maths ----------
const clamp01 = x => x < 0 ? 0 : x > 1 ? 1 : x;
const lerp = (a, b, k) => a + (b - a) * k;
const P = (t, a, b) => clamp01((t - a) / (b - a));
const E = {
  lin: x => x, in2: x => x * x, in3: x => x * x * x, out2: x => 1 - (1 - x) * (1 - x), out3: x => 1 - Math.pow(1 - x, 3),
  io: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  back: x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
};
const spring01 = (tau, f, d) => tau <= 0 ? 0 : 1 - Math.exp(-d * tau) * Math.cos(2 * Math.PI * f * tau);
const wob = (tau, f, d) => tau <= 0 ? 0 : Math.exp(-d * tau) * Math.sin(2 * Math.PI * f * tau);
// squash amount after a landing at tau=0 (0 on the contact frame, peak one frame later, springs back)
const squash = (tau, A, f = 3.0, d = 6) => tau <= 0 ? 0 : A * Math.exp(-d * tau) * Math.cos(2 * Math.PI * f * tau) * Math.min(1, tau / 0.035);
// keyframe track: [[t, v, ease|'step'], ...] (ease belongs to the segment that ARRIVES at the key)
function key(tr, t) {
  if (t <= tr[0][0]) return tr[0][1];
  for (let i = 1; i < tr.length; i++) {
    const [t1, v1, e] = tr[i], [t0, v0] = tr[i - 1];
    if (t < t1) return e === 'step' ? v0 : lerp(v0, v1, (E[e] || E.io)(P(t, t0, t1)));
  }
  return tr[tr.length - 1][1];
}

// ---------- the scale: horizon tilt, camera, shake ----------
// [time, target degrees (+ = right side down), spring Hz, damping]
const TILT_EV = [
  [HIT.hook, 7, 1.5, 3.4], [HIT.squish, 8, 3, 7],
  [HIT.names[0], -7, 1.6, 4.4], [HIT.names[1], 7, 1.6, 4.4], [HIT.names[2], -7, 1.6, 4.4],
  [11.0, -4, 0.7, 5], [HIT.heavy, -6, 2.0, 4.5],
  [HIT.blocks[0], -6.5, 2.6, 6], [HIT.blocks[1], -7, 2.6, 6], [HIT.blocks[2], -7.5, 2.6, 6], [HIT.blocks[3], -8, 2.6, 6], [HIT.blocks[4], -8.5, 2.6, 6],
  [HIT.box, -9, 1.5, 3.2],
  [HIT.cta, 0, 3.2, 7.5],
];
let tiltFn = () => 0;
for (const [te, to, f, d] of TILT_EV) { const prev = tiltFn, s = prev(te); tiltFn = tt => tt < te ? prev(tt) : s + (to - s) * spring01(tt - te, f, d); }

const SHAKES = [[HIT.hook, 30], [HIT.cups[0], 3], [HIT.cups[1], 3], [HIT.cups[2], 3], [HIT.cups[3], 3], [HIT.squish, 4],
  [HIT.names[0], 17], [HIT.names[1], 17], [HIT.names[2], 17], [HIT.heavy, 22], [HIT.thaqeel, 8],
  ...HIT.blocks.map((b, i) => [b, 8 + i]), [HIT.box, 36], [HIT.athqal, 14], [HIT.cta, 24]];
function shake(t) {
  let x = 0, y = 0;
  for (let i = 0; i < SHAKES.length; i++) { const tau = t - SHAKES[i][0]; if (tau < 0 || tau > 0.7) continue; const a = SHAKES[i][1] * Math.exp(-9 * tau); x += a * Math.sin(2 * Math.PI * 13 * tau + i * 1.7) * 0.6; y += a * Math.cos(2 * Math.PI * 11 * tau + i); }
  return { x, y };
}
const DIPS = [[HIT.hook, 34], [HIT.names[0], 18], [HIT.names[1], 18], [HIT.names[2], 18], [HIT.heavy, 22], ...HIT.blocks.map(b => [b, 12]), [HIT.box, 42], [HIT.cta, 26]];
const dip = t => DIPS.reduce((s, [te, a]) => s + a * wob(t - te, 2.6, 7), 0);

const CAM_Z = [[0, 1], [2.7, 1], [3.5, .9], [7.0, .9], [7.0, 1, 'step'], [19.4, 1], [19.72, .85, 'out3'], [22.5, .85], [24.0, .74], [28.85, .74], [29.5, .66, 'io'], [40, .66]];
const CAM_X = [[0, 0], [2.7, 0], [3.5, -46], [7.0, -46], [7.0, 0, 'step'], [19.0, 0], [19.4, 120, 'io'], [22.5, 120], [24.0, 130], [28.85, 130], [29.5, 203, 'io'], [40, 203]];
const CAM_H = [[0, 1000], [2.7, 1000], [3.5, 1086], [7.0, 1086], [7.0, 1150, 'step'], [15.2, 1150], [18.6, 1330], [19.0, 1330], [19.4, 1000, 'in2'], [19.72, 1040, 'out3'], [22.5, 1040], [24.0, 900], [28.85, 900], [29.5, 780, 'io'], [40, 780]];
const camera = t => ({ z: key(CAM_Z, t), x: key(CAM_X, t), h: key(CAM_H, t) });
// screen point -> world point for a given camera and tilt (used to lay text out in screen space)
function s2w(sx, sy, cam, tiltDeg) {
  const dx = sx - 540, dy = sy - cam.h, c = Math.cos(tiltDeg * DEG), s = Math.sin(tiltDeg * DEG);
  return { x: (dx * c + dy * s) / cam.z + cam.x, y: (-dx * s + dy * c) / cam.z };
}
const CAM6 = { z: .85, x: 120, h: 1040 }, CAM7 = { z: .74, x: 130, h: 900 }, CAM8 = { z: .66, x: 203, h: 780 };

// ---------- drawing helpers ----------
function font(weight, size, fam = 'Tajawal', italic = false) { ctx.font = `${italic ? 'italic ' : ''}${weight} ${size}px "${fam}"`; }
// Arabic text is always drawn as whole words/lines (never per letter, never letter-spaced).
function ar(str, x, y, size, weight, color, align = 'center') {
  ctx.direction = 'rtl'; font(weight, size); ctx.fillStyle = color; ctx.textAlign = align; ctx.textBaseline = 'alphabetic'; ctx.fillText(str, x, y);
}
function en(str, x, y, size, color, weight = 500, align = 'center') {
  ctx.direction = 'ltr'; font(weight, size, 'Playfair Display', true); ctx.fillStyle = color; ctx.textAlign = align; ctx.textBaseline = 'alphabetic'; ctx.fillText(str, x, y);
}
function arWidth(str, size, weight) { ctx.direction = 'rtl'; font(weight, size); return ctx.measureText(str).width; }
function arBox(str, size, weight) { ctx.direction = 'rtl'; font(weight, size); ctx.textAlign = 'center'; const m = ctx.measureText(str); return { w: m.width, up: m.actualBoundingBoxAscent, down: m.actualBoundingBoxDescent }; }
// transform about an anchor: translate, rotate, squash (sx, sy)
function at(x, y, rot, sx, sy, fn) { ctx.save(); ctx.translate(x, y); if (rot) ctx.rotate(rot * DEG); if (sx !== 1 || sy !== 1) ctx.scale(sx, sy); fn(); ctx.restore(); }
function rrect(x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
function softShadow(points, blur, alpha) {
  ctx.save(); ctx.filter = `blur(${blur}px)`; ctx.fillStyle = `rgba(24,23,23,${alpha})`; ctx.beginPath();
  points.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath(); ctx.fill(); ctx.restore();
}
function ellipseShadow(x, y, rx, ry, alpha, blur = 10) { ctx.save(); ctx.filter = `blur(${blur}px)`; ctx.fillStyle = `rgba(24,23,23,${alpha})`; ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, 7); ctx.fill(); ctx.restore(); }

// ---------- objects ----------
// hero sandwich (photo cut-out). anchor = middle of its base line in sprite px.
const SW = { ax: 470, ay: 560, shadow: [[70, 500], [110, 600], [250, 668], [560, 545], [905, 345], [890, 262], [520, 420]] };
function sandwich(x, y, scale, rot, q, alpha = 1, shadowA = 1) {
  const im = IMG.sandwich;
  at(x, y, 0, scale, scale, () => { ctx.translate(-SW.ax, -SW.ay); softShadow(SW.shadow, 16, 0.34 * shadowA); });
  ctx.globalAlpha = alpha;
  at(x, y, rot, scale * (1 + 0.6 * q), scale * (1 - q), () => ctx.drawImage(im, -SW.ax, -SW.ay));
  ctx.globalAlpha = 1;
}
// gathering box (photo cut-out). Sprite px. Hinge line H->C splits the lid from the tray.
const BX = { ax: 560, ay: 1000, H: [40, 653], Cc: [660, 476],
  shadow: [[20, 800], [350, 1160], [1075, 915], [1066, 840], [370, 1040], [50, 730]],
  food: [[66, 677], [676, 502], [941, 692], [746, 852], [356, 932]] };
function gbox(x, y, scale, q, lidW, hop, shadowA = 1) {
  const im = IMG.box, [hx, hy] = BX.H, [cx, cy] = BX.Cc;
  const L = Math.hypot(cx - hx, cy - hy), ux = (cx - hx) / L, uy = (cy - hy) / L, nx = uy, ny = -ux;   // n points up, away from the tray
  const yAt = X => hy + (X - hx) * (cy - hy) / (cx - hx);
  at(x, y, 0, scale, scale, () => { ctx.translate(-BX.ax, -BX.ay); softShadow(BX.shadow, 20, 0.36 * shadowA); });
  at(x, y, 0, scale * (1 + 0.5 * q), scale * (1 - q), () => {
    ctx.translate(-BX.ax, -BX.ay);
    // lid: affine that keeps every point of the hinge line fixed (shear + slight foreshortening)
    ctx.save();
    const gx = lidW * (0.11 * ux - 0.05 * nx), gy = lidW * (0.11 * uy - 0.05 * ny);
    const m11 = 1 + gx * nx, m12 = gx * ny, m21 = gy * nx, m22 = 1 + gy * ny;
    ctx.transform(m11, m21, m12, m22, hx - (m11 * hx + m12 * hy), hy - (m21 * hx + m22 * hy));
    ctx.beginPath(); ctx.moveTo(-60, yAt(-60)); ctx.lineTo(1200, yAt(1200)); ctx.lineTo(1200, -200); ctx.lineTo(-60, -200); ctx.closePath(); ctx.clip();
    ctx.drawImage(im, 0, 0); ctx.restore();
    // tray
    ctx.save(); ctx.beginPath(); ctx.moveTo(-60, yAt(-60) - 0.6); ctx.lineTo(1200, yAt(1200) - 0.6); ctx.lineTo(1200, 1300); ctx.lineTo(-60, 1300); ctx.closePath(); ctx.clip();
    ctx.drawImage(im, 0, 0); ctx.restore();
    // the row of sandwiches inside hops once
    if (hop > 0.5) { ctx.save(); ctx.translate(0, -hop); ctx.beginPath(); BX.food.forEach(([px, py], i) => i ? ctx.lineTo(px, py) : ctx.moveTo(px, py)); ctx.closePath(); ctx.clip(); ctx.drawImage(im, 0, 0); ctx.restore(); }
  });
}
// flat sauce cup: black cup, coloured top (identity colours, no photo)
const CUP_TOP = [C.lime, C.hot, C.white, C.lime2];
function cup(x, y, s, rot, wave, col) {
  ellipseShadow(x - 14 * s, y - 4 * s, 78 * s, 20 * s, 0.30, 8);
  at(x, y, rot, s, s, () => {
    ctx.fillStyle = C.black; ctx.beginPath();
    ctx.moveTo(-75, -104); ctx.lineTo(75, -104); ctx.lineTo(56, -14); ctx.quadraticCurveTo(0, 12, -56, -14); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.ellipse(0, -104, 75, 25, 0, 0, 7); ctx.fill();
    ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(0, -104, 61, 17.5 * (1 + 0.32 * wave), wave * 5 * DEG, 0, 7); ctx.fill();
  });
}
// flat carton block: pink with a lime band (blank: the word HIPPO is never typeset)
const BW = 380, BH = 200;
function block(x, y, rot, q) {
  at(x, y, rot, 1 + 0.5 * q, 1 - q, () => {
    ctx.fillStyle = C.hot; rrect(-BW / 2, -BH, BW, BH, 14); ctx.fill();
    ctx.fillStyle = C.lime; ctx.fillRect(-BW / 2, -BH * 0.64, BW, BH * 0.28);
    ctx.fillStyle = 'rgba(24,23,23,0.16)'; ctx.save(); rrect(-BW / 2, -BH, BW, BH, 14); ctx.clip(); ctx.fillRect(-BW / 2, -9, BW, 9); ctx.restore();
  });
}
function dust(x, y, tau, n = 9, spread = 420) {
  if (tau < 0 || tau > 0.9) return;
  const k = tau / 0.9;
  ctx.save(); ctx.filter = 'blur(14px)';
  for (let i = 0; i < n; i++) {
    const u = (i / (n - 1)) * 2 - 1, r = 16 + 34 * E.out2(k) + (i % 3) * 8;
    ctx.fillStyle = `rgba(255,255,255,${0.30 * (1 - k) * (1 - k)})`;
    ctx.beginPath(); ctx.ellipse(x + u * spread * (0.55 + 0.45 * E.out2(k)), y - 4 - (10 + (i % 2) * 14) * E.out2(k), r * 1.5, r * 0.7, 0, 0, 7); ctx.fill();
  }
  ctx.restore();
}
// lime light circle on the floor (ellipse = circle seen on the floor plane)
function limeCircle(x, y, rx, ry, a) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha = a;
  ctx.save(); ctx.filter = 'blur(26px)'; ctx.fillStyle = 'rgba(187,208,50,0.45)'; ctx.beginPath(); ctx.ellipse(x, y, rx * 1.1, ry * 1.14, 0, 0, 7); ctx.fill(); ctx.restore();
  ctx.fillStyle = C.lime; ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, 7); ctx.fill();
  ctx.restore();
}

// ---------- layout constants ----------
const S1 = { sx: 255, sy: 290, sc: 0.62, wordX: -70, wordSize: 86 };
const CUPX = [-42, -207, -372, -537], CUPY = 334;
const S3 = [{ x: -285, size: 150, maxW: 440 }, { x: 285, size: 158, maxW: 440 }, { x: -250, size: 215, maxW: 500 }];
const TOWER = { x: -40, y: 110, dx: [0, 14, -10, 8, -4], r: [0.6, -1.2, 1, -0.8, 0.5] };
const HEAP = [[-330, 170, -2], [-660, 215, 3], [-510, -32, 5], [-280, -30, -6], [-420, -232, -11]];   // after the box hit
const ROW_T = { x: -400, y: 300 };                                                                     // neat stack in scene 8
const BOXP = { x: 260, y: 470, sc: 0.7 };
const SW7 = { x: -385, y: 640, sc: 0.6 }, SW8 = { x: 760, y: 440, sc: 0.6 };
const CUP7 = [[-95, 620], [35, 680], [-215, 735], [-545, 745]], CUP8 = [[-560, 610], [-420, 610], [-280, 610], [-140, 610]];
const T6a = s2w(570, 440, CAM6, -9), T6b = s2w(570, 690, CAM6, -9);
const CIR7 = s2w(838, 1258, CAM7, -9), T7a = s2w(770, 1468, CAM7, -9), T7b = s2w(770, 1540, CAM7, -9);
const CIR8 = { x: 203, y: 900, rx: 660, ry: 250 };

// ---------- scenes: wall layer (behind the floor) and floor layer ----------
function wallLayer(t) {
  // S1 «خفيف؟» — stands on the horizon, slides down the tilt, piles up against the sandwich, tips behind the floor edge
  if (t < 3.2) {
    const b = arBox(COPY.s1, S1.wordSize, 300);
    const slide = 118 * E.in2(P(t, 1.08, 1.62));
    const tip = 13 * spring01(t - 1.62, 2.4, 6) + 70 * E.in2(P(t, 2.7, 3.1));
    const q = squash(t - 1.62, 0.16, 3.5, 7);
    const hop = -26 * Math.sin(Math.PI * P(t, 1.0, 1.3));
    const fall = 190 * E.in2(P(t, 2.72, 3.12));
    at(S1.wordX + slide + b.w / 2, -4 + hop + fall, tip, 1 - q, 1 + 0.5 * q, () => ar(COPY.s1, -b.w / 2, -b.down, S1.wordSize, 300, C.black));
  }
  // S2 «بريوش طري.» — soft word, squashes with the bread
  if (t >= 4.5 && t < 7.0) {
    const land = 4.76, y = -70 - 900 * (1 - E.in2(P(t, land - 0.26, land)));
    const q = squash(t - land, 0.14, 3.2, 6) + squash(t - HIT.squish, 0.2, 3.4, 6);
    at(-250, y, 0, 1 + 0.6 * q, 1 - q, () => ar(COPY.s2, 0, 0, 132, 300, C.black));
  }
  // S4 light line floats up; heavy line falls and sinks into the floor (the floor layer hides what is below the horizon)
  if (t >= 11.3 && t < 15.0) {
    const tau = t - HIT.heavy;
    const a = P(t, 11.3, 11.8) * (1 - P(t, 14.5, 14.9));
    const y = -372 - 20 * (t - 11.3) - 34 * wob(tau, 1.2, 3) - 150 * E.in2(P(t, 14.5, 14.9));
    ctx.globalAlpha = a; at(0, y, 4.5 * spring01(tau, 1.8, 3.5), 1, 1, () => ar(COPY.s4a, 0, 0, 150, 300, C.black)); ctx.globalAlpha = 1;
  }
  if (t >= 12.15 && t < 15.05) heavyLine(t, false);
  // S6 «وبوكس الجَمعات؟ أثقل.»
  if (t >= 20.45 && t < 23.8) {
    const a = 1 - P(t, 23.3, 23.7);
    ctx.globalAlpha = a;
    const la = 20.62, ya = T6a.y - 700 * (1 - E.in2(P(t, la - 0.2, la))), qa = squash(t - la, 0.1, 3.4, 7);
    at(T6a.x, ya, 0, 1 + 0.6 * qa, 1 - qa, () => ar(COPY.s6a, 0, 0, 112, 300, C.black));
    if (t >= HIT.athqal - 0.22) {
      const yb = T6b.y - 1300 * (1 - E.in2(P(t, HIT.athqal - 0.22, HIT.athqal))), qb = squash(t - HIT.athqal, 0.2, 3.0, 6);
      at(T6b.x, yb, 0, 1 + 0.6 * qb, 1 - qb, () => ar(COPY.s6b, 0, 0, 270, 800, C.black));
    }
    ctx.globalAlpha = 1;
  }
}
function heavyLine(t, asShadow) {
  const size = 186, gap = size * 0.26;
  const w1 = arWidth(COPY.s4b1, size, 800), w2 = arWidth(COPY.s4b2, size, 800), total = w1 + gap + w2;
  const tau = t - HIT.heavy, tau2 = t - HIT.thaqeel;
  const fall = -1500 * (1 - E.in2(P(t, HIT.heavy - 0.3, HIT.heavy)));
  const sink = -60 + 30 * (tau > 0 ? Math.exp(-6 * tau) : 0) + 460 * E.in2(P(t, 14.6, 15.0));
  const q = squash(tau, 0.2, 3.0, 6);
  const y = fall + sink;
  const draw = () => {
    ar(COPY.s4b1, total / 2, 0, size, 800, asShadow ? 'rgba(24,23,23,0.9)' : C.black, 'right');             // first word sits on the right (RTL)
    const pop = tau2 > 0 ? 1 + 0.085 * Math.exp(-8 * tau2) : 1, drop = tau2 > 0 ? 12 * Math.exp(-6 * tau2) : 0;
    at(-total / 2 + w2 / 2, drop, 0, pop, pop, () => ar(COPY.s4b2, 0, 0, size, 800, asShadow ? 'rgba(24,23,23,0.9)' : C.black, 'center'));
  };
  if (!asShadow) at(0, y, 0, 1 + 0.6 * q, 1 - q, draw);
  else if (tau > -0.3) { ctx.save(); ctx.globalAlpha = 0.2 * P(t, HIT.heavy - 0.3, HIT.heavy) * (1 - P(t, 14.6, 14.85)); ctx.filter = 'blur(7px)'; ctx.transform(1, 0, -0.5, -0.34, 0, 2); draw(); ctx.restore(); }
}

function floorLayer(t) {
  // ---- S1–S2: hero sandwich + sauce cups ----
  if (t >= 0.5 && t < 7.0) {
    const pf = P(t, 0.5, HIT.hook), off = -1750 * (1 - pf * pf);
    const q = squash(t - HIT.hook, 0.2, 3.0, 5.5) + squash(t - HIT.squish, 0.06, 4, 8);
    const sA = pf * pf;
    at(0, 0, 0, 1, 1, () => {
      const im = IMG.sandwich;
      at(S1.sx, S1.sy, 0, S1.sc, S1.sc, () => { ctx.translate(-SW.ax, -SW.ay); softShadow(SW.shadow, 16, 0.34 * sA); });
      at(S1.sx + 5 * wob(t - HIT.squish, 5, 8), S1.sy + off, -5 * (1 - pf), S1.sc * (1 + 0.6 * q), S1.sc * (1 - q), () => ctx.drawImage(im, -SW.ax, -SW.ay));
    });
    dust(S1.sx - 20, S1.sy + 40, t - HIT.hook, 7, 330);
    for (let i = 0; i < 4; i++) {
      const T = HIT.cups[i]; if (t < T - 0.62) continue;
      let x = CUPX[i] - 950 * (1 - E.in2(P(t, T - 0.62, T)));
      for (let j = i + 1; j < 4; j++) x += 5 * wob(t - HIT.cups[j], 5, 9);
      x += 13 * E.out2(P(t, HIT.squish - 0.07, HIT.squish));
      const wave = wob(t - T, 4.2, 4.5) + 0.7 * wob(t - HIT.squish, 4.2, 5);
      cup(x, CUPY, 1, 7 * wob(t - T, 4, 7), wave, CUP_TOP[i]);
    }
  }
  // ---- S3: the three names are the falling weights (ExtraBold); the horizon is a see-saw ----
  if (t >= 6.9 && t < 11.5) {
    for (let i = 0; i < 3; i++) {
      const T = HIT.names[i], next = i < 2 ? HIT.names[i + 1] : null; if (t < T - 0.3) continue;
      const lines = COPY.s3[i]; let sz = S3[i].size;
      sz = Math.min(sz, sz * S3[i].maxW / Math.max(...lines.map(l => arBox(l, sz, 800).w)));
      const lh = sz * 1.08, boxes = lines.map(l => arBox(l, sz, 800)), wmax = Math.max(...boxes.map(b => b.w)), down = boxes[boxes.length - 1].down;
      let x = S3[i].x, y = -1500 * (1 - E.in2(P(t, T - 0.3, T))), rot = 0, q = squash(t - T, 0.22, 3.0, 6);
      if (next !== null && t >= next) { const tau = t - next; if (tau > 0.62) continue; y += -3300 * tau + 2600 * tau * tau; x += (i === 0 ? -1 : 1) * 380 * tau; rot = (i === 0 ? -1 : 1) * 70 * tau; }
      if (i === 2) x -= 1700 * E.in2(P(t, 10.92, 11.45));
      const cy = -(lines.length * lh) / 2;
      at(x, y + 2, 0, 1 + 0.6 * q, 1 - q, () => at(0, cy, rot, 1, 1, () => {
        lines.forEach((l, k) => ar(l, 0, -cy - down - (lines.length - 1 - k) * lh, sz, 800, C.black));
      }));
      dust(S3[i].x, 0, t - T, 8, wmax * 0.55);
    }
  }
  // ---- S4: shadow of the heavy line on the floor, dust, English support line ----
  if (t >= 12.15 && t < 15.0) {
    heavyLine(t, true);
    dust(0, 4, t - HIT.heavy, 10, 440);
    const a = P(t, 12.9, 13.3) * (1 - P(t, 14.45, 14.8));
    if (a > 0) { ctx.globalAlpha = a; en(COPY.s4en, 0, 150, 50, C.white); ctx.globalAlpha = 1; }
  }
  // ---- S5–S8: blocks, box, wide shot, call to action ----
  if (t >= 14.8) {
    const k8 = E.out3(P(t, HIT.cta, HIT.cta + 0.42)), hop8 = Math.sin(Math.PI * P(t, HIT.cta, HIT.cta + 0.42)), q8 = squash(t - HIT.cta - 0.42, 0.1, 3.2, 7);
    // light circle (floor) — scene 7 on the empty high side, scene 8 it takes the weight
    const cin = E.out2(P(t, 24.2, 24.95)), cg = E.io(P(t, 28.85, 29.5));
    if (t >= 24.2) {
      const pulse = 1 + 0.05 * wob(t - HIT.cta, 3, 6) * -1;
      limeCircle(lerp(CIR7.x, CIR8.x, cg), lerp(CIR7.y, CIR8.y, cg), lerp(300, CIR8.rx, cg) * (0.9 + 0.1 * cin) * pulse, lerp(105, CIR8.ry, cg) * (0.9 + 0.1 * cin) * pulse, cin);
    }
    // blocks
    const kh = E.out3(P(t, HIT.box, HIT.box + 0.7)), hopH = Math.sin(Math.PI * P(t, HIT.box, HIT.box + 0.7));
    const order = [0, 1, 2, 3, 4];
    for (const i of order) {
      const T = HIT.blocks[i]; if (t < T - 0.34) continue;
      let x = TOWER.x + TOWER.dx[i], y = TOWER.y - BH * i - 1750 * (1 - E.in2(P(t, T - 0.34, T))), r = TOWER.r[i];
      let q = squash(t - T, 0.17, 3.2, 6.5);
      for (let j = i + 1; j < 5; j++) q += squash(t - HIT.blocks[j], 0.05, 3.2, 7);
      if (t >= HIT.box) {
        x = lerp(x, HEAP[i][0], kh); y = lerp(y, HEAP[i][1], kh) - (90 + 40 * i) * hopH * (1 - kh * 0.5); r = lerp(r, HEAP[i][2], kh) + (i % 2 ? 1 : -1) * 14 * hopH * (1 - kh);
        q += squash(t - HIT.box - 0.7, 0.06, 3.2, 7);
      }
      if (t >= HIT.cta) { x = lerp(x, ROW_T.x, k8); y = lerp(y, ROW_T.y - BH * i, k8) - (180 + 30 * i) * hop8; r = lerp(r, 0, k8); q += q8; }
      block(x, y, r, q);
    }
    // gathering box
    if (t >= HIT.box - 0.36) {
      const y = BOXP.y - 2000 * (1 - E.in2(P(t, HIT.box - 0.36, HIT.box))) - 120 * hop8;
      const q = squash(t - HIT.box, 0.1, 2.6, 5) + q8;
      const lidW = 1.25 * wob(t - (HIT.lid[0] - 0.0575), 4.35, 3.6) + 0.5 * wob(t - HIT.cta - 0.42, 4.35, 5);
      const hop = 30 * Math.sin(Math.PI * P(t, HIT.box + 0.02, HIT.box + 0.34)) + 16 * Math.sin(Math.PI * P(t, HIT.cta + 0.42, HIT.cta + 0.66));
      gbox(BOXP.x, y, BOXP.sc, q, lidW, hop, P(t, HIT.box - 0.3, HIT.box) * (1 - 0.6 * hop8));
      dust(BOXP.x - 40, BOXP.y + 60, t - HIT.box, 11, 430);
    }
    // hero sandwich and cups slide down the tilted floor into the pile (scene 7), then line up (scene 8)
    if (t >= 22.5) {
      const ks = E.out2(P(t, 22.5, 23.55));
      const sx = lerp(lerp(1650, SW7.x, ks), SW8.x, k8), sy = lerp(SW7.y, SW8.y, k8) - 260 * hop8;
      const q = squash(t - 23.55, 0.07, 3.2, 7) + q8;
      const cupsBehind = [], cupsFront = [];
      for (let i = 0; i < 4; i++) {
        const t0 = 22.8 + i * 0.13, kc = E.out2(P(t, t0, t0 + 1.0));
        const x = lerp(lerp(1500, CUP7[i][0], kc), CUP8[i][0], k8), y = lerp(CUP7[i][1], CUP8[i][1], k8) - (150 + 20 * i) * hop8;
        const wave = wob(t - t0 - 1.0, 4.2, 4.5) + wob(t - HIT.cta - 0.42, 4.2, 4.5);
        (y < sy ? cupsBehind : cupsFront).push(() => cup(x, y, 0.9, 6 * wob(t - t0 - 1.0, 4, 7), wave, CUP_TOP[i]));
      }
      cupsBehind.forEach(f => f());
      sandwich(sx, sy, SW7.sc, 0, q, 1, 1 - 0.6 * hop8);
      cupsFront.forEach(f => f());
    }
    // S7 text at the empty circle (white on violet)
    if (t >= 26.9 && t < 29.3) {
      const out = 1 - P(t, 28.85, 29.2);
      ctx.globalAlpha = E.out2(P(t, 26.9, 27.25)) * out; at(T7a.x, T7a.y + 26 / CAM7.z * (1 - E.out3(P(t, 26.9, 27.3))), 0, 1, 1, () => ar(COPY.s7a, 0, 0, 84 / CAM7.z, 800, C.white));
      ctx.globalAlpha = E.out2(P(t, 27.6, 27.95)) * out; ar(COPY.s7b, T7b.x, T7b.y, 46 / CAM7.z, 300, C.white);
      ctx.globalAlpha = 1;
    }
    // S8 «حُطّ ثقلك.» falls into the circle (black on lime)
    if (t >= HIT.cta - 0.26) {
      const y = CIR8.y + 22 - 1900 * (1 - E.in2(P(t, HIT.cta - 0.26, HIT.cta))), q = squash(t - HIT.cta, 0.2, 3.0, 6);
      at(CIR8.x, y, 0, 1 + 0.6 * q, 1 - q, () => ar(COPY.s8, 0, 0, 205, 800, C.black));
      dust(CIR8.x, CIR8.y + 40, t - HIT.cta, 9, 520);
      const a = P(t, 30.05, 30.4); if (a > 0) { ctx.globalAlpha = a; en(COPY.s8en, CIR8.x, CIR8.y + 132, 62, C.black, 500); ctx.globalAlpha = 1; }
    }
  }
}

// ---------- end card (scene 9) ----------
// Logo: the client's PNG, drawn as is. Approved exception: at 38.2 s the ears piece (a separate shape in the file) twitches;
// optional blink (CFG.blink) flattens the two shapes that hang under the brow line. Nothing is redrawn; proportions never change at rest.
const LG = { w: 1343, h: 2127, ears: [396, 0, 552, 210], earPivot: [671.5, 205], eyes: [[388, 524, 226, 122], [729, 524, 226, 122]] };
function logo(x, y, hgt, t) {
  const im = IMG.logo, s = hgt / LG.h;
  ctx.save(); ctx.translate(x - LG.w * s / 2, y); ctx.scale(s, s);
  const tau = t - HIT.logoBlink, tw = tau > 0 && tau < 0.7 ? wob(tau, 5.2, 7) : 0;
  const [ex, ey, ew, eh] = LG.ears;
  // everything except the ears piece
  ctx.save(); ctx.beginPath(); ctx.rect(0, eh, LG.w, LG.h - eh); ctx.rect(0, 0, ex, eh); ctx.rect(ex + ew, 0, LG.w - ex - ew, eh); ctx.clip(); ctx.drawImage(im, 0, 0); ctx.restore();
  // ears piece: rigid twitch (small rotation + lift) about the middle of its base
  ctx.save(); ctx.translate(LG.earPivot[0], LG.earPivot[1] - 9 * Math.abs(tw)); ctx.rotate(3.6 * tw * DEG); ctx.translate(-LG.earPivot[0], -LG.earPivot[1]);
  ctx.beginPath(); ctx.rect(ex, ey - 40, ew, eh + 40 - 1); ctx.clip(); ctx.drawImage(im, 0, 0); ctx.restore();
  if (CFG.blink && tau > 0 && tau < 0.3) {
    const k = 1 - 0.8 * Math.sin(Math.PI * P(tau, 0, 0.26));
    for (const [bx, by, bw, bh] of LG.eyes) {
      ctx.fillStyle = C.white; ctx.fillRect(bx, by, bw, bh);
      ctx.save(); ctx.translate(0, by); ctx.scale(1, k); ctx.translate(0, -by); ctx.beginPath(); ctx.rect(bx, by, bw, bh); ctx.clip(); ctx.drawImage(im, 0, 0); ctx.restore();
    }
  }
  ctx.restore();
}
function endCard(t) {
  ctx.fillStyle = C.white; ctx.fillRect(0, 0, W, H);
  // logo enters with position and size only
  const k = E.out3(P(t, HIT.endCard, HIT.endCard + 0.55)), hgt = 560 * lerp(0.86, 1, k), ly = 300 + 70 * (1 - k) + (560 - hgt) / 2;
  logo(540, ly, hgt, t);
  let a = E.out2(P(t, 34.2, 34.6));
  if (a > 0) { ctx.globalAlpha = a; ar(COPY.s9a, 540, 985 + 14 * (1 - a), 78, 800, C.black); ctx.globalAlpha = E.out2(P(t, 34.5, 34.9)); en(COPY.s9en, 540, 1052, 48, C.black, 500); ctx.globalAlpha = 1; }
  a = E.out2(P(t, 35.5, 35.9));
  if (a > 0) {
    ctx.globalAlpha = a; ar(COPY.s9b, 540, 1180, 46, 300, C.black);
    const qx = 390, qy = 1222, qs = 300;
    if (CFG.qr && IMG.qr) ctx.drawImage(IMG.qr, qx, qy, qs, qs);
    else {   // clearly marked EMPTY placeholder — no pattern, no link
      ctx.save(); ctx.strokeStyle = C.black; ctx.lineWidth = 4; ctx.setLineDash([18, 12]); ctx.strokeRect(qx + 2, qy + 2, qs - 4, qs - 4); ctx.restore();
      ar(COPY.qrLabel[0], 540, qy + 142, 40, 800, C.black); ar(COPY.qrLabel[1], 540, qy + 196, 27, 300, C.black);
    }
    ctx.globalAlpha = 1;
  }
}

// ---------- frame ----------
function render(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.filter = 'none';
  if (t >= HIT.endCard) endCard(t);
  else {
    const cam = camera(t), sh = shake(t), tilt = tiltFn(t);
    ctx.fillStyle = C.pink; ctx.fillRect(0, 0, W, H);
    ctx.save();
    ctx.translate(540 + sh.x, cam.h + dip(t) + sh.y); ctx.rotate(tilt * DEG); ctx.scale(cam.z, cam.z); ctx.translate(-cam.x, 0);
    wallLayer(t);
    ctx.fillStyle = C.violet; ctx.fillRect(-9000, 0, 18000, 9000);
    floorLayer(t);
    ctx.restore();
  }
  if (CFG.guides) { ctx.strokeStyle = 'rgba(0,255,255,.8)'; ctx.lineWidth = 2; ctx.setLineDash([10, 8]); ctx.strokeRect(0, 250, W, H - 600); ctx.setLineDash([]); }
}
window.seek = t => { render(Math.max(0, Math.min(DUR, t))); return true; };

// ---------- boot ----------
function load(src) { return new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = () => rej(new Error('missing ' + src)); i.src = src; }); }
window.ready = (async () => {
  const q = new URLSearchParams(location.search);
  if (q.has('guides')) CFG.guides = true;
  if (q.has('blink')) CFG.blink = true;
  for (const k of Object.keys(CFG.photos)) IMG[k] = await load(CFG.photos[k]);
  if (CFG.qr) IMG.qr = await load(CFG.qr);
  await Promise.all(['300 80px "Tajawal"', '800 80px "Tajawal"', 'italic 500 40px "Playfair Display"'].map(f => document.fonts.load(f, 'حُطّ ثقلك Franchise')));
  await document.fonts.ready;
  window.fontsOk = { tajawalLight: document.fonts.check('300 80px "Tajawal"', 'ح'), tajawalXB: document.fonts.check('800 80px "Tajawal"', 'ح'), playfair: document.fonts.check('italic 500 40px "Playfair Display"', 'F'), faces: [...document.fonts].map(f => `${f.family} ${f.weight} ${f.style} ${f.status}`) };
  render(0);
  if (!q.has('render')) {            // browser preview with the audio
    document.body.classList.add('preview');
    const aud = document.getElementById('aud'), tc = document.getElementById('tc');
    document.getElementById('play').onclick = () => aud.paused ? aud.play() : aud.pause();
    (function loop() { render(aud.currentTime); tc.textContent = aud.currentTime.toFixed(2) + ' s'; requestAnimationFrame(loop); })();
  }
  return true;
})();
