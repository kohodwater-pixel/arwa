/* HIPPO — franchise motion ad «حُطّ ثقلك» — picture draft v02, 9:16, 1080x1920, 30 fps, 40 s.
   Deterministic: everything is a pure function of film time t (seconds). window.seek(t) draws one frame.
   Cut to audio mix v02 (see ../../audio/_work/mix-v02_report_2026-11-18.md). All hit times are in HIT below.
   v01 source is kept in ../_archive/film_v01.js.

   EDIT HERE ---------------------------------------------------------------------------------- */
const CFG = {
  photos: {                      // the only two photographs in the film (+ the logo file)
    sandwich: 'assets/sandwich.png',   // cut-out of crispy-chicken.jpg  (tools/cutout.py)
    box:      'assets/box.png',        // cut-out of box-breakfast-89.jpg (tools/cutout_box.py)
    logo:     'assets/logo.png',       // client logo file, unmodified copy
  },
  qr: null,          // when the client sends the link: put the QR image at e.g. 'assets/qr.png' and set this path
  blink: false,      // eye-blink on the logo. OFF by Creative Director ruling: ears only (see notes.md)
  guides: false,     // draw platform safe-area guides (250 px top, 350 px bottom) and 60 px side margins
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
};
const spring01 = (tau, f, d) => tau <= 0 ? 0 : 1 - Math.exp(-d * tau) * Math.cos(2 * Math.PI * f * tau);
const wob = (tau, f, d) => tau <= 0 ? 0 : Math.exp(-d * tau) * Math.sin(2 * Math.PI * f * tau);
// squash amount after a landing at tau=0 (0 on the contact frame, peak one frame later, springs back)
const squash = (tau, A, f = 3.0, d = 6) => tau <= 0 ? 0 : A * Math.exp(-d * tau) * Math.cos(2 * Math.PI * f * tau) * Math.min(1, tau / 0.035);

// ---------- the scale: horizon tilt, shake ----------
const T67 = -7.5;   // settled tilt of scenes 6–7 (degrees; + = right side down)
// [time, target degrees, spring Hz, damping]
const TILT_EV = [
  [HIT.hook, 7, 1.5, 3.4], [HIT.squish, 8, 3, 7],
  [HIT.names[0], -7, 1.6, 4.4], [HIT.names[1], 7, 1.6, 4.4], [HIT.names[2], -7, 1.6, 4.4],
  [11.0, -5, 0.7, 5], [HIT.heavy, -6, 2.0, 4.5],
  [HIT.box, T67, 1.5, 3.2],
  [HIT.cta, 0, 3.2, 7.5],
];
let tiltBase = () => 0;
for (const [te, to, f, d] of TILT_EV) { const prev = tiltBase, s = prev(te); tiltBase = tt => tt < te ? prev(tt) : s + (to - s) * spring01(tt - te, f, d); }
const tiltFn = t => tiltBase(t) + HIT.blocks.reduce((s, b) => s - 0.9 * wob(t - b, 3, 7), 0) - 2.2 * wob(t - HIT.box, 1.7, 3.6);

const SHAKES = [[HIT.hook, 30], [HIT.cups[0], 3], [HIT.cups[1], 3], [HIT.cups[2], 3], [HIT.cups[3], 3], [HIT.squish, 4],
  [HIT.names[0], 17], [HIT.names[1], 17], [HIT.names[2], 17], [HIT.heavy, 22], [HIT.thaqeel, 8],
  ...HIT.blocks.map((b, i) => [b, 8 + i]), [HIT.box, 36], [HIT.athqal + 0.023, 14], [HIT.cta, 24]];
function shake(t) {
  let x = 0, y = 0;
  for (let i = 0; i < SHAKES.length; i++) { const tau = t - SHAKES[i][0]; if (tau < 0 || tau > 0.7) continue; const a = SHAKES[i][1] * Math.exp(-9 * tau); x += a * Math.sin(2 * Math.PI * 13 * tau + i * 1.7) * 0.6; y += a * Math.cos(2 * Math.PI * 11 * tau + i); }
  return { x, y };
}
const DIPS = [[HIT.hook, 34], [HIT.names[0], 18], [HIT.names[1], 18], [HIT.names[2], 18], [HIT.heavy, 22], ...HIT.blocks.map(b => [b, 12]), [HIT.box, 42], [HIT.cta, 26]];
const dip = t => DIPS.reduce((s, [te, a]) => s + a * wob(t - te, 2.6, 7), 0);

// ---------- cameras ----------
// A camera is {z: zoom, x: world x at screen centre, h: screen y of the horizon at screen centre}. World y = 0 is the horizon.
// screen point -> world point, and "which camera puts world point w at screen point s"
function s2w(sx, sy, cam, tiltDeg) {
  const dx = sx - 540, dy = sy - cam.h, c = Math.cos(tiltDeg * DEG), s = Math.sin(tiltDeg * DEG);
  return { x: (dx * c + dy * s) / cam.z + cam.x, y: (-dx * s + dy * c) / cam.z };
}
function camFor(w, sx, sy, z, tiltDeg) {
  const c = Math.cos(tiltDeg * DEG), s = Math.sin(tiltDeg * DEG), dx = sx - 540;
  const h = sy - (w.y * z + dx * s) / c;
  return { z, x: w.x - (dx * c + (sy - h) * s) / z, h };
}
const CAM7 = { z: 0.447, x: 0, h: 880 };

// ---------- layouts (SCREEN px, at the settled tilt of each scene) -> world ----------
const SW_SC = 0.95, BOX_SC = 0.9, CUP_SC = 1.2, BW = 460, BH = 190;
// scene 7: the full pan (pile on the low left, empty circle on the high right)
const L7 = { box: [470, 1150], heap: [[170, 1075, -4], [300, 1035, 3], [195, 988, 6], [320, 950, -5], [240, 900, -10]],
  sw: [262, 1290], cups: [[92, 1388], [172, 1410], [252, 1390], [140, 1478]], circle: [790, 1445, 240, 95], t1: [780, 1250], t2: [780, 1312] };
const w7 = p => s2w(p[0], p[1], CAM7, T67);
const WD = { box: w7(L7.box), heap: L7.heap.map(p => ({ ...w7(p), r: p[2] })), sw: w7(L7.sw), cups: L7.cups.map(w7), circle: w7(L7.circle), t1: w7(L7.t1), t2: w7(L7.t2), tower: w7([240, 1060]) };
// scene 6 is the same world seen closer; scene 8 is level, the box does not move
const CAM6 = camFor(WD.box, 640, 1480, 0.62, T67), CAM8 = camFor(WD.box, 485, 1120, 0.416, 0);
// scenes 1–4 are staged around the spot where the tower will stand, so the camera barely travels into scene 5
const CAM5b = camFor(WD.tower, 600, 1334, 0.83, -6), CAM5a = camFor(WD.tower, 600, 1250, 0.83, -6), CAM5c = camFor(WD.box, 720, 1470, 0.72, -6);
const CAM34 = { z: 0.83, x: CAM5b.x, h: 1000 }, OX = CAM34.x - 60;   // OX: x offset of the scene 1–2 staging
const CAM1 = { z: 1, x: OX, h: 1000 }, CAM2 = { z: 0.65, x: -290 + OX, h: 1172 };
const w8 = p => s2w(p[0], p[1], CAM8, 0);
const L8 = { tower: [166, 1140], sw: [842, 1130], cups: [[398, 1245], [478, 1245], [558, 1245], [638, 1245]], circle: [540, 1420, 400, 150], text: [540, 1452], en: [540, 1508] };
const W8 = { tower: w8(L8.tower), sw: w8(L8.sw), cups: L8.cups.map(w8), circle: w8(L8.circle), text: w8(L8.text), en: w8(L8.en) };
const T6a = s2w(560, 455, CAM6, T67), T6b = s2w(560, 790, CAM6, T67);

// camera track: [time, camera, ease of the move that ARRIVES here]
const CAMS = [[0, CAM1], [2.7, CAM1], [3.5, CAM2, 'io'], [6.85, CAM2], [7.2, CAM34, 'io'], [14.55, CAM34], [15.2, CAM5a, 'io'], [18.6, CAM5b, 'io'], [19.0, CAM5b],
  [19.4, CAM5c, 'io'], [19.72, CAM6, 'out3'], [22.6, CAM6], [24.0, CAM7, 'io'], [28.85, CAM7], [29.5, CAM8, 'io'], [40, CAM8]];
function camera(t) {
  if (t <= CAMS[0][0]) return CAMS[0][1];
  for (let i = 1; i < CAMS.length; i++) {
    const [t1, c1, e] = CAMS[i], [t0, c0] = CAMS[i - 1];
    if (t < t1) { const k = (E[e] || E.io)(P(t, t0, t1)); return { z: lerp(c0.z, c1.z, k), x: lerp(c0.x, c1.x, k), h: lerp(c0.h, c1.h, k) }; }
  }
  return CAMS[CAMS.length - 1][1];
}

// ---------- the hero sandwich is on stage from 1.0 s to 33.3 s and is thrown about by every weight ----------
const SWP1 = { x: 75 + OX, y: 640 };
const SWP3L = s2w(450, 1640, CAM34, -7), SWP3R = s2w(630, 1640, CAM34, 7), SWP5 = s2w(560, 1690, CAM5b, -6);
// [time of the hit, where it lands, flight seconds, hop height (world px)]
const SWK = [[HIT.names[0], SWP3L, 0.4, 130], [HIT.names[1], SWP3R, 0.4, 130], [HIT.names[2], SWP3L, 0.4, 130], [HIT.heavy, SWP3L, 0.36, 90],
  [HIT.blocks[0], SWP5, 0.4, 90], [HIT.blocks[1], SWP5, 0.28, 40], [HIT.blocks[2], SWP5, 0.28, 44], [HIT.blocks[3], SWP5, 0.28, 48], [HIT.blocks[4], SWP5, 0.28, 52],
  [HIT.box, WD.sw, 0.5, 260], [HIT.cta, W8.sw, 0.42, 300]];
function sandwichState(t) {
  let x = SWP1.x, y = SWP1.y, q = 0, lift = 0, rot = 0;
  for (const [tk, p, d, hop] of SWK) {
    if (t < tk) break;
    const k = P(t, tk, tk + d), e = E.out2(k), arc = Math.sin(Math.PI * k);
    const nx = lerp(x, p.x, e), ny = lerp(y, p.y, e);
    rot = (p.x - x > 5 ? 1 : p.x - x < -5 ? -1 : 0) * 5 * arc; x = nx; y = ny; lift = hop * arc;
    q = squash(t - tk - d, 0.13, 3.2, 6.5);
  }
  return { x, y, q, lift, rot };
}

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
function sandwich(x, y, scale, rot, q, lift = 0, yOff = 0, shadowA = 1) {
  const im = IMG.sandwich, sa = shadowA * (1 - 0.55 * clamp01(lift / 260));
  at(x, y, 0, scale, scale, () => { ctx.translate(-SW.ax, -SW.ay); softShadow(SW.shadow, 16, 0.34 * sa); });
  at(x, y - lift + yOff, rot, scale * (1 + 0.6 * q), scale * (1 - q), () => ctx.drawImage(im, -SW.ax, -SW.ay));
}
// gathering box (photo cut-out). Sprite px. Hinge line H->C splits the lid from the tray.
const BX = { ax: 560, ay: 1000, H: [40, 653], Cc: [660, 476],
  shadow: [[20, 800], [350, 1160], [1075, 915], [1066, 840], [370, 1040], [50, 730]],
  food: [[66, 677], [676, 502], [941, 692], [746, 852], [356, 932]] };
function gbox(x, y, scale, q, lidW, hop, shadowA = 1, yOff = 0) {
  const im = IMG.box, [hx, hy] = BX.H, [cx, cy] = BX.Cc;
  const L = Math.hypot(cx - hx, cy - hy), ux = (cx - hx) / L, uy = (cy - hy) / L, nx = uy, ny = -ux;   // n points up, away from the tray
  const yAt = X => hy + (X - hx) * (cy - hy) / (cx - hx);
  at(x, y, 0, scale, scale, () => { ctx.translate(-BX.ax, -BX.ay); softShadow(BX.shadow, 20, 0.36 * shadowA); });
  at(x, y + yOff, 0, scale * (1 + 0.5 * q), scale * (1 - q), () => {
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
function cup(x, y, s, rot, wave, col, lift = 0) {
  ellipseShadow(x - 14 * s, y - 4 * s, 78 * s, 20 * s, 0.30 * (1 - 0.5 * clamp01(lift / 200)), 8);
  at(x, y - lift, rot, s, s, () => {
    ctx.fillStyle = C.black; ctx.beginPath();
    ctx.moveTo(-75, -104); ctx.lineTo(75, -104); ctx.lineTo(56, -14); ctx.quadraticCurveTo(0, 12, -56, -14); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.ellipse(0, -104, 75, 25, 0, 0, 7); ctx.fill();
    ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(0, -104, 61, 17.5 * (1 + 0.32 * wave), wave * 5 * DEG, 0, 7); ctx.fill();
  });
}
// flat carton block: pink with a lime band (blank: the word HIPPO is never typeset)
function block(x, y, rot, q) {
  at(x, y, rot, 1 + 0.5 * q, 1 - q, () => {
    ctx.fillStyle = C.hot; rrect(-BW / 2, -BH, BW, BH, 16); ctx.fill();
    ctx.fillStyle = C.lime; ctx.fillRect(-BW / 2, -BH * 0.64, BW, BH * 0.28);
    ctx.fillStyle = 'rgba(24,23,23,0.16)'; ctx.save(); rrect(-BW / 2, -BH, BW, BH, 16); ctx.clip(); ctx.fillRect(-BW / 2, -10, BW, 10); ctx.restore();
  });
}
// dust: only where something meets the floor, tinted (a darker violet), never behind lettering
function dust(x, y, tau, n = 7, spread = 420, s = 1) {
  if (tau < 0 || tau > 0.8) return;
  const k = tau / 0.8;
  ctx.save(); ctx.filter = `blur(${12 * s}px)`;
  for (let i = 0; i < n; i++) {
    const u = (i / (n - 1)) * 2 - 1, r = (18 + 30 * E.out2(k) + (i % 3) * 8) * s;
    ctx.fillStyle = `rgba(52,34,104,${0.34 * (1 - k) * (1 - k)})`;
    ctx.beginPath(); ctx.ellipse(x + u * spread * (0.6 + 0.4 * E.out2(k)), y - (6 + (i % 2) * 10) * E.out2(k) * s, r * 1.5, r * 0.6, 0, 0, 7); ctx.fill();
  }
  ctx.restore();
}
// lime light circle on the floor (ellipse = circle seen on the floor plane)
function limeCircle(x, y, rx, ry, a) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha = a;
  ctx.save(); ctx.filter = `blur(${rx * 0.07}px)`; ctx.fillStyle = 'rgba(187,208,50,0.45)'; ctx.beginPath(); ctx.ellipse(x, y, rx * 1.1, ry * 1.14, 0, 0, 7); ctx.fill(); ctx.restore();
  ctx.fillStyle = C.lime; ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, 7); ctx.fill();
  ctx.restore();
}

// ---------- scene constants (world px) ----------
const S1 = { wordSize: 150, slide: 150 };
const CUPX = [-330, -516, -702, -888].map(x => x + OX), CUPY = 735;
const S3 = [{ x: -25, maxW: 843 }, { x: 145, maxW: 843 }, { x: -25, maxW: 843 }], S3_MAX_SIZE = 330;   // names ≈ 65 % of the frame width
const TOWER = { dx: [0, 16, -12, 9, -5], r: [0.6, -1.2, 1, -0.8, 0.5] };

function nameMetrics(i) {
  const lines = COPY.s3[i]; let sz = S3_MAX_SIZE;
  sz = Math.min(sz, sz * S3[i].maxW / Math.max(...lines.map(l => arBox(l, sz, 800).w)));
  const lh = sz * 1.06, boxes = lines.map(l => arBox(l, sz, 800));
  return { lines, sz, lh, down: boxes[boxes.length - 1].down, height: (lines.length - 1) * lh + boxes[0].up + boxes[boxes.length - 1].down };
}
const nameFallY = (i, t) => -1800 * (1 - E.in2(P(t, HIT.names[i] - 0.3, HIT.names[i])));

// ---------- wall layer: drawn BEFORE the floor, so anything below the horizon is hidden by the floor ----------
function wallLayer(t) {
  // S1 «خفيف؟» — centred on the level horizon; after the hit it slides down the tilt and settles upright beside the sandwich
  if (t < 2.96) {
    const b = arBox(COPY.s1, S1.wordSize, 300);
    const k = P(t, 1.08, 1.72), slide = S1.slide * E.io(k);
    const q = squash(t - 1.72, 0.14, 3.5, 7);
    const hop = -30 * Math.sin(Math.PI * P(t, 1.0, 1.3));
    const tip = 2.5 * wob(t - 1.72, 3, 6) + 75 * E.in2(P(t, 2.62, 2.95)), fall = 460 * E.in2(P(t, 2.62, 2.95));
    at(OX + slide + b.w / 2, -6 + hop + fall, tip, 1 - q, 1 + 0.5 * q, () => ar(COPY.s1, -b.w / 2, -b.down, S1.wordSize, 300, C.black));
  }
  // S2 «بريوش طري.» — soft word, squashes with the bread; slides out with the push-in to scene 3
  if (t >= 4.5 && t < 7.4) {
    const land = 4.76, y = -62 - 1300 * (1 - E.in2(P(t, land - 0.26, land)));
    const q = squash(t - land, 0.14, 3.2, 6) + squash(t - HIT.squish, 0.2, 3.4, 6);
    at(OX - 560 - 1500 * E.in2(P(t, 6.85, 7.3)), y, 0, 1 + 0.6 * q, 1 - q, () => ar(COPY.s2, 0, 0, 190, 300, C.black));
  }
  // S3 — the three names are the weights. Each one stamps the previous one down into the floor.
  if (t >= 6.9 && t < 11.5) {
    for (let i = 0; i < 3; i++) {
      const T = HIT.names[i]; if (t < T - 0.3) continue;
      const m = nameMetrics(i);
      let y = nameFallY(i, t), x = S3[i].x + CAM34.x, q = squash(t - T, 0.2, 3.0, 6);
      if (i < 2) { const sink = nameFallY(i + 1, t) + m.height + 14; if (t >= HIT.names[i + 1] - 0.3 && sink > 0) { y += sink; if (sink > m.height + 10) continue; } }
      if (i === 2) x -= 2200 * E.in2(P(t, 10.9, 11.4));
      at(x, y, 0, 1 + 0.6 * q, 1 - q, () => m.lines.forEach((l, k) => ar(l, 0, -m.down - (m.lines.length - 1 - k) * m.lh, m.sz, 800, C.black)));
    }
  }
  // S4 light line floats up; heavy line falls, hits the floor line and tilts the line above
  if (t >= 11.0 && t < 15.0) {
    const tau = t - HIT.heavy;
    const a = P(t, 11.05, 11.6) * (1 - P(t, 14.1, 14.45));
    const y = -520 - 22 * (t - 11.0) - 40 * wob(tau, 1.2, 3) - 180 * E.in2(P(t, 14.1, 14.45));
    ctx.globalAlpha = a; at(CAM34.x, y, 4.5 * spring01(tau, 1.8, 3.5), 1, 1, () => ar(COPY.s4a, 0, 0, 180, 300, C.black)); ctx.globalAlpha = 1;
  }
  if (t >= 12.15 && t < 15.05) heavyLine(t, false);
  // S6 «وبوكس الجَمعات؟ أثقل.»
  if (t >= 20.45 && t < 23.7) {
    ctx.globalAlpha = 1 - P(t, 23.2, 23.6);
    const s = 1 / CAM6.z, la = 20.62, ya = T6a.y - 900 * (1 - E.in2(P(t, la - 0.2, la))), qa = squash(t - la, 0.1, 3.4, 7);
    at(T6a.x, ya, 0, 1 + 0.6 * qa, 1 - qa, () => ar(COPY.s6a, 0, 0, 112 * s, 300, C.black));
    const lb = HIT.athqal + 0.023;   // contact on frame 655, the first frame after 21.810
    if (t >= lb - 0.2) {
      const yb = T6b.y - 3200 * (1 - E.in2(P(t, lb - 0.2, lb))), qb = squash(t - lb, 0.2, 3.0, 6);
      at(T6b.x, yb, 0, 1 + 0.6 * qb, 1 - qb, () => ar(COPY.s6b, 0, 0, 300 * s, 800, C.black));
    }
    ctx.globalAlpha = 1;
  }
}
function heavyLine(t, asShadow) {
  const size = 224, gap = size * 0.26;
  const w1 = arWidth(COPY.s4b1, size, 800), w2 = arWidth(COPY.s4b2, size, 800), total = w1 + gap + w2;
  const tau = t - HIT.heavy, tau2 = t - HIT.thaqeel;
  const fall = -3600 * (1 - E.in2(P(t, HIT.heavy - 0.3, HIT.heavy)));
  const sink = -72 + 36 * (tau > 0 ? Math.exp(-6 * tau) : 0) + 620 * E.in2(P(t, 14.2, 14.55));   // rests just above the floor line (keeps the dots of the ي visible)
  const q = squash(tau, 0.2, 3.0, 6);
  const col = asShadow ? 'rgba(24,23,23,0.9)' : C.black;
  const draw = () => {
    ar(COPY.s4b1, total / 2, 0, size, 800, col, 'right');             // first word sits on the right (RTL)
    const pop = tau2 > 0 ? 1 + 0.085 * Math.exp(-8 * tau2) : 1, drop = tau2 > 0 ? 14 * Math.exp(-6 * tau2) : 0;
    at(-total / 2 + w2 / 2, drop, 0, pop, pop, () => ar(COPY.s4b2, 0, 0, size, 800, col, 'center'));
  };
  if (!asShadow) at(CAM34.x, fall + sink, 0, 1 + 0.6 * q, 1 - q, draw);
  else if (tau > -0.3) { ctx.save(); ctx.globalAlpha = 0.2 * P(t, HIT.heavy - 0.3, HIT.heavy) * (1 - P(t, 14.2, 14.4)); ctx.filter = 'blur(8px)'; ctx.translate(CAM34.x, 0); ctx.transform(1, 0, -0.5, -0.34, 0, 2); draw(); ctx.restore(); }
}

// ---------- floor layer ----------
function floorLayer(t) {
  const sw = sandwichState(t);
  const k8 = E.out3(P(t, HIT.cta, HIT.cta + 0.42)), hop8 = Math.sin(Math.PI * P(t, HIT.cta, HIT.cta + 0.42)), q8 = squash(t - HIT.cta - 0.42, 0.1, 3.2, 7);

  // S4: shadow of the heavy line and the English support line (white on violet)
  if (t >= 12.15 && t < 15.0) {
    heavyLine(t, true);
    const a = P(t, 12.9, 13.3) * (1 - P(t, 14.05, 14.35));
    if (a > 0) { ctx.globalAlpha = a; en(COPY.s4en, CAM34.x, 118, 62, C.white); ctx.globalAlpha = 1; }
  }
  // S7–S8: the lime light circle
  if (t >= 24.2) {
    const cin = E.out2(P(t, 24.2, 24.95)), cg = E.io(P(t, 28.85, 29.5)), pulse = 1 - 0.05 * wob(t - HIT.cta, 3, 6);
    limeCircle(lerp(WD.circle.x, W8.circle.x, cg), lerp(WD.circle.y, W8.circle.y, cg),
      lerp(L7.circle[2] / CAM7.z, L8.circle[2] / CAM8.z, cg) * (0.9 + 0.1 * cin) * pulse, lerp(L7.circle[3] / CAM7.z, L8.circle[3] / CAM8.z, cg) * (0.9 + 0.1 * cin) * pulse, cin);
  }
  // S5–S8: blocks (tower -> heap after the box hit -> neat stack)
  if (t >= HIT.blocks[0] - 0.34) {
    const kh = E.out3(P(t, HIT.box, HIT.box + 0.7)), hopH = Math.sin(Math.PI * P(t, HIT.box, HIT.box + 0.7));
    for (let i = 0; i < 5; i++) {
      const T = HIT.blocks[i]; if (t < T - 0.34) continue;
      let x = WD.tower.x + TOWER.dx[i], y = WD.tower.y - BH * i - 2100 * (1 - E.in2(P(t, T - 0.34, T))), r = TOWER.r[i];
      let q = squash(t - T, 0.17, 3.2, 6.5);
      for (let j = i + 1; j < 5; j++) q += squash(t - HIT.blocks[j], 0.05, 3.2, 7);
      if (t >= HIT.box) {
        const hp = WD.heap[i];
        x = lerp(x, hp.x, kh); y = lerp(y, hp.y, kh) - (120 + 60 * i) * hopH * (1 - kh * 0.5); r = lerp(r, hp.r, kh) + (i % 2 ? 1 : -1) * 14 * hopH * (1 - kh);
        q += squash(t - HIT.box - 0.7, 0.06, 3.2, 7);
      }
      if (t >= HIT.cta) { x = lerp(x, W8.tower.x, k8); y = lerp(y, W8.tower.y - BH * i, k8) - (260 + 50 * i) * hop8; r = lerp(r, 0, k8); q += q8; }
      block(x, y, r, q);
    }
    if (t < HIT.box) dust(WD.tower.x, WD.tower.y + 12, t - HIT.blocks[0], 6, 260);
  }
  // S6–S8: the gathering box
  if (t >= HIT.box - 0.36) {
    const yOff = -2600 * (1 - E.in2(P(t, HIT.box - 0.36, HIT.box))) - 240 * hop8;
    const q = squash(t - HIT.box, 0.1, 2.6, 5) + q8;
    const lidW = 1.25 * wob(t - (HIT.lid[0] - 0.0575), 4.35, 3.6) + 0.5 * wob(t - HIT.cta - 0.42, 4.35, 5);
    const hop = 30 * Math.sin(Math.PI * P(t, HIT.box + 0.02, HIT.box + 0.34)) + 16 * Math.sin(Math.PI * P(t, HIT.cta + 0.42, HIT.cta + 0.66));
    gbox(WD.box.x, WD.box.y, BOX_SC, q, lidW, hop, P(t, HIT.box - 0.3, HIT.box) * (1 - 0.6 * hop8), yOff);
    dust(WD.box.x - 60, WD.box.y + 90, t - HIT.box, 9, 560, 1.4);
  }
  // S2: cups slide in from the high side, stop on the four taps, leave with the first name
  if (t >= HIT.cups[0] - 0.62 && t < 7.9) {
    for (let i = 0; i < 4; i++) {
      const T = HIT.cups[i]; if (t < T - 0.62) continue;
      let x = CUPX[i] - 1300 * (1 - E.in2(P(t, T - 0.62, T)));
      for (let j = i + 1; j < 4; j++) x += 6 * wob(t - HIT.cups[j], 5, 9);
      x += 14 * E.out2(P(t, HIT.squish - 0.07, HIT.squish)) - 2600 * E.in2(P(t, HIT.names[0], HIT.names[0] + 0.6));
      const wave = wob(t - T, 4.2, 4.5) + 0.7 * wob(t - HIT.squish, 4.2, 5);
      cup(x, CUPY, CUP_SC, 7 * wob(t - T, 4, 7), wave, CUP_TOP[i]);
    }
  }
  // the hero sandwich
  if (t >= 0.3) {
    const pf = P(t, 0.3, HIT.hook), off = -2300 * (1 - pf * pf);
    const q = squash(t - HIT.hook, 0.2, 3.0, 5.5) + squash(t - HIT.squish, 0.06, 4, 8) + sw.q;
    sandwich(sw.x + 5 * wob(t - HIT.squish, 5, 8), sw.y, SW_SC, sw.rot - 5 * (1 - pf), q, sw.lift, off, pf * pf);
    dust(SWP1.x - 20, SWP1.y + 50, t - HIT.hook, 7, 420, 1.2);
  }
  // S7–S8: cups slide back in during the pull-back, rest in front of the pile, then line up
  if (t >= 22.7) {
    for (let i = 0; i < 4; i++) {
      const t0 = 22.7 + i * 0.12, kc = E.out2(P(t, t0, t0 + 1.15));
      const x = lerp(lerp(WD.cups[i].x + 2900, WD.cups[i].x, kc), W8.cups[i].x, k8), y = lerp(WD.cups[i].y, W8.cups[i].y, k8);
      const wave = wob(t - t0 - 1.15, 4.2, 4.5) + wob(t - HIT.cta - 0.42, 4.2, 4.5);
      cup(x, y, CUP_SC, 6 * wob(t - t0 - 1.15, 4, 7), wave, CUP_TOP[i], (240 + 30 * i) * hop8);
    }
  }
  // S7 text over the empty circle (white on violet)
  if (t >= 26.6 && t < 29.2) {
    const out = 1 - P(t, 28.8, 29.1), s = 1 / CAM7.z;
    ctx.globalAlpha = E.out2(P(t, 26.6, 26.95)) * out; at(WD.t1.x, WD.t1.y + 26 * s * (1 - E.out3(P(t, 26.6, 27.0))), 0, 1, 1, () => ar(COPY.s7a, 0, 0, 72 * s, 800, C.white));
    ctx.globalAlpha = E.out2(P(t, 27.3, 27.65)) * out; ar(COPY.s7b, WD.t2.x, WD.t2.y, 46 * s, 300, C.white);
    ctx.globalAlpha = 1;
  }
  // S8 «حُطّ ثقلك.» falls into the circle (black on lime)
  if (t >= HIT.cta - 0.2) {
    const s = 1 / CAM8.z, y = W8.text.y - 9000 * (1 - E.in2(P(t, HIT.cta - 0.2, HIT.cta))), q = squash(t - HIT.cta, 0.2, 3.0, 6);
    at(W8.text.x, y, 0, 1 + 0.6 * q, 1 - q, () => ar(COPY.s8, 0, 0, 124 * s, 800, C.black));
    const a = P(t, 30.05, 30.4); if (a > 0) { ctx.globalAlpha = a; en(COPY.s8en, W8.en.x, W8.en.y, 38 * s, C.black, 500); ctx.globalAlpha = 1; }
  }
}

// ---------- end card (scene 9) ----------
// Logo: the client's PNG, drawn as is. Approved exception: at 38.2 s the ears piece (a separate shape in the file) twitches.
// Blink is off by ruling (CFG.blink kept for reference only). Nothing is redrawn; proportions never change at rest.
const LG = { w: 1343, h: 2127, ears: [396, 0, 552, 210], earPivot: [671.5, 205], eyes: [[388, 524, 226, 122], [729, 524, 226, 122]] };
function logo(x, y, hgt, t) {
  const im = IMG.logo, s = hgt / LG.h;
  ctx.save(); ctx.translate(x - LG.w * s / 2, y); ctx.scale(s, s);
  const tau = t - HIT.logoBlink, tw = tau > 0 && tau < 0.7 ? wob(tau, 5.2, 7) : 0;
  const [ex, ey, ew, eh] = LG.ears;
  ctx.save(); ctx.beginPath(); ctx.rect(0, eh, LG.w, LG.h - eh); ctx.rect(0, 0, ex, eh); ctx.rect(ex + ew, 0, LG.w - ex - ew, eh); ctx.clip(); ctx.drawImage(im, 0, 0); ctx.restore();
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
    ctx.fillStyle = C.violet; ctx.fillRect(-20000, 0, 40000, 20000);
    floorLayer(t);
    ctx.restore();
  }
  if (CFG.guides) {
    ctx.save(); ctx.strokeStyle = 'rgba(0,255,255,.9)'; ctx.lineWidth = 2; ctx.setLineDash([10, 8]); ctx.strokeRect(0, 250, W, H - 600);
    ctx.strokeStyle = 'rgba(255,255,0,.9)'; ctx.strokeRect(60, -10, W - 120, H + 20); ctx.restore();
  }
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
