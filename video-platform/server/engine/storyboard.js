import { cameraMoves, shotSizes, byId } from './catalog.js';

/** Narrative beats. `m` = camera move candidates in order of preference; `t` = two description variants per language. */
const ROLES = {
  establish: { w: 1.0, size: 'wide', m: ['drone', 'crane_down', 'dolly_in', 'pan'], title: ['لقطة افتتاحية', 'Opening shot'],
    ar: ['لقطة افتتاحية واسعة تؤسس {L}{A} مع حركة كاميرا بطيئة تمهّد لظهور {S}.', 'منظر عام واسع يكشف {L}{A} ويحدد أجواء الفيلم قبل دخول {S}.'],
    en: ['A wide opening shot establishes {L}{A}, with a slow camera move that sets up the arrival of {S}.', 'A sweeping wide view reveals {L}{A} and sets the tone before {S} appears.'] },
  hook: { w: 0.8, size: 'medium', m: ['dolly_in', 'tracking', 'handheld'], title: ['لقطة الجذب', 'Hook'],
    ar: ['لقطة جذب فورية تملأ الكادر بمشهد {S} وحركة قوية منذ الثانية الأولى{A}.', 'بداية مباشرة على {S} بحركة مفاجئة تشد الانتباه{A}.'],
    en: ['An instant hook: {S} fills the frame with a strong move from the first second{A}.', 'A cold open straight on {S} with an arresting move{A}.'] },
  intro: { w: 1.3, size: 'medium', m: ['tracking', 'dolly_in', 'orbit', 'tilt'], title: ['تقديم العنصر الرئيسي', 'Introducing the subject'],
    ar: ['لقطة متوسطة تقدّم {S} بوضوح في {L}، والكاميرا ترافق الحركة بسلاسة.', 'لقطة متوسطة تركّز على {S} وتُظهر الشكل كاملًا وسط {L}.'],
    en: ['A medium shot introduces {S} clearly in {L}, the camera moving smoothly with it.', 'A medium shot centres on {S}, showing its full form within {L}.'] },
  detail: { w: 1.4, size: 'macro', m: ['dolly_in', 'pan', 'static', 'tilt'], title: ['تفاصيل قريبة', 'Close detail'],
    ar: ['لقطة قريبة جدًا لتفاصيل {S}: الخامات والملمس وانعكاسات الضوء، بعمق ميدان ضحل.', 'تفاصيل دقيقة من {S} تمرّ ببطء أمام العدسة مع إضاءة سينمائية تبرز الملمس.'],
    en: ['An extreme close-up on the details of {S}: materials, texture and light reflections, with shallow depth of field.', 'Fine details of {S} glide slowly past the lens, cinematic light bringing out the texture.'] },
  action: { w: 1.2, size: 'medium_wide', m: ['tracking', 'orbit', 'handheld', 'crane_up'], title: ['الحركة الرئيسية', 'Key action'],
    ar: ['لقطة حركة ديناميكية تكشف الحدث الرئيسي: {S} في ذروة الحركة عبر {L}.', 'ذروة المشهد: حركة قوية يقودها {S} والكاميرا تتابع دون انقطاع.'],
    en: ['A dynamic shot reveals the key moment: {S} at full motion through {L}.', 'The peak of the film: {S} moves with power as the camera follows without a cut.'] },
  context: { w: 1.0, size: 'medium_wide', m: ['pan', 'tracking', 'drone', 'dolly_out'], title: ['المكان والأجواء', 'Place and atmosphere'],
    ar: ['لقطة تُظهر {L}{A} وتفاصيل البيئة التي تحتضن {S}.', 'جولة هادئة في {L} تلتقط الأجواء والعناصر التي تعطي المكان هويته.'],
    en: ['A shot that shows {L}{A} and the environment around {S}.', 'A calm pass through {L}, catching the atmosphere and the elements that give the place its character.'] },
  human: { w: 1.0, size: 'close', m: ['dolly_in', 'handheld', 'static'], title: ['اللحظة الإنسانية', 'Human moment'],
    ar: ['لقطة قريبة للحظة إنسانية صادقة: تفاعل وتعبير طبيعي أمام {S}.', 'لمسة إنسانية: يد أو نظرة أو ابتسامة تتفاعل مع {S} بشكل طبيعي.'],
    en: ['A close-up of an honest human moment: a natural reaction connected to {S}.', 'A human touch: a hand, a look or a smile interacting naturally with {S}.'] },
  reveal: { w: 1.1, size: 'wide', m: ['crane_up', 'dolly_out', 'orbit', 'drone'], title: ['الكشف', 'Reveal'],
    ar: ['لقطة كشف: الكاميرا ترتفع أو تبتعد لتُظهر {S} ضمن {L}{A}.', 'حركة كاميرا واسعة تكشف المشهد كله و{S} في مركزه.'],
    en: ['A reveal: the camera rises or pulls back to show {S} in full within {L}{A}.', 'A broad camera move uncovers the whole scene with {S} at its centre.'] },
  closing: { w: 0.8, size: 'medium_wide', m: ['dolly_out', 'crane_up', 'static', 'orbit'], title: ['لقطة ختامية', 'Closing shot'],
    ar: ['لقطة ختامية قوية تُبرز {S} مع مساحة نظيفة في الكادر مناسبة لإظهار الشعار أو الرسالة.', 'نهاية هادئة وواثقة: {S} في تكوين متوازن مع فراغ واضح للشعار أو العبارة الختامية.'],
    en: ['A strong closing shot of {S} with clean space in the frame for the logo or message.', 'A calm, confident ending: {S} in a balanced composition with clear room for the logo or end line.'] },
  hero: { w: 1, size: 'medium_wide', m: ['tracking', 'dolly_in', 'drone', 'orbit'], title: ['اللقطة البطلة', 'Hero shot'],
    ar: ['لقطة واحدة متكاملة: {S} في {L}{A} بحركة كاميرا سينمائية واحدة متصلة.', 'لقطة بطلة متصلة تجمع {S} و{L}{A} في حركة واحدة.'],
    en: ['One complete shot: {S} in {L}{A}, in a single continuous cinematic camera move.', 'One continuous hero shot bringing together {S} and {L}{A}.'] },
};

/** Per video type: opening beat, closing beat, and the middle beats in order of importance. Story order is ORDER. */
const TYPES = {
  commercial: { open: 'establish', mid: ['intro', 'detail', 'action', 'reveal', 'human', 'context'] },
  short_film: { open: 'establish', mid: ['human', 'action', 'intro', 'reveal', 'detail', 'context'] },
  tourism: { open: 'establish', mid: ['context', 'human', 'detail', 'reveal', 'action', 'intro'] },
  real_estate: { open: 'establish', mid: ['context', 'detail', 'reveal', 'human', 'intro', 'action'] },
  product: { open: 'intro', mid: ['detail', 'action', 'reveal', 'context', 'human', 'establish'] },
  creative: { open: 'establish', mid: ['intro', 'action', 'detail', 'reveal', 'human', 'context'] },
  social: { open: 'hook', mid: ['detail', 'action', 'reveal', 'human', 'context', 'intro'] },
  motion_graphics: { open: 'intro', mid: ['detail', 'action', 'reveal', 'context', 'establish', 'human'] },
};
const ORDER = ['establish', 'hook', 'intro', 'context', 'human', 'detail', 'action', 'reveal', 'closing'];

export function sceneCount(total, maxClip) {
  const base = total <= 6 ? 1 : total <= 11 ? 2 : total <= 19 ? 3 : total <= 26 ? 4 : total <= 35 ? 5 : total <= 45 ? 6 : total <= 60 ? 8 : Math.ceil(total / 8);
  return Math.max(base, Math.ceil(total / maxClip));
}

/** Splits `total` seconds into integer scene durations proportional to weights, each within [min, max]. */
export function splitDuration(total, weights, min, max) {
  const n = weights.length, sum = weights.reduce((a, b) => a + b, 0);
  const exact = weights.map((w) => (total * w) / sum);
  const d = exact.map((x) => Math.min(max, Math.max(min, Math.floor(x))));
  let left = total - d.reduce((a, b) => a + b, 0), guard = 1000;
  while (left !== 0 && guard--) {
    const dir = Math.sign(left);
    let best = -1, score = -Infinity;
    for (let i = 0; i < n; i++) {
      if (dir > 0 ? d[i] >= max : d[i] <= min) continue;
      const s = dir * (exact[i] - d[i]);
      if (s > score) { score = s; best = i; }
    }
    if (best < 0) break;
    d[best] += dir; left -= dir;
  }
  return d;
}

function labels(t, lang) {
  const ar = lang === 'ar';
  const S = ar ? (t.subject.ar || 'العنصر الرئيسي') : (t.subject.en ? t.subject.en.replace(/^(?!the |a )/, 'the ') : 'the main subject');
  const env = t.setting.env, place = t.setting.place;
  const L = ar
    ? (env && place ? `${env.ar} في ${place.ar}` : env?.ar || place?.ar || 'الموقع')
    : (env && place ? `${env.en} in ${place.en}` : env?.en || place?.en || 'the location');
  const parts = [t.setting.time, t.setting.weather].filter(Boolean).map((x) => (ar ? x.ar : x.en.split(',')[0]));
  const A = parts.length ? (ar ? ' ' + parts.join(' ') : ', ' + parts.join(', ')) : '';
  return { S, L, A };
}

function pickMove(role, t, variant, avoid = []) {
  let c = [...ROLES[role].m];
  if (t.camera.avoidHandheld) c = c.filter((m) => m !== 'handheld');
  // cues named by the user come first when they fit this beat
  const pref = t.camera.preferred.filter((m) => c.includes(m));
  if (t.camera.moving && ['intro', 'action', 'hero', 'hook'].includes(role) && !pref.includes('tracking') && c.includes('tracking')) pref.unshift('tracking');
  if (!t.setting.env || ['interior', 'studio'].includes(t.setting.env.id)) c = c.filter((m) => m !== 'drone' || pref.includes('drone'));
  // a subject that does not move is not 'tracked': keep tracking as a last resort
  if (!t.camera.moving && !pref.includes('tracking')) c = [...c.filter((m) => m !== 'tracking'), ...c.filter((m) => m === 'tracking')];
  c = [...pref, ...c.filter((m) => !pref.includes(m))];
  const usable = c.filter((m) => !avoid.includes(m));
  const list = usable.length ? usable : c;
  return list[variant % list.length];
}

export function describeScene(role, t, lang, variant = 0) {
  const { S, L, A } = labels(t, lang);
  const tpl = ROLES[role][lang === 'ar' ? 'ar' : 'en'];
  return tpl[variant % tpl.length].replace('{S}', S).replace('{L}', L).replace('{A}', A);
}

function makeScene(role, t, lang, variant, avoidMoves) {
  const R = ROLES[role];
  const size = t.videoType === 'product' && role === 'intro' ? 'medium' : R.size;
  return {
    role, variant,
    title: R.title[lang === 'ar' ? 0 : 1],
    description: describeScene(role, t, lang, variant),
    shot_size: size,
    camera_move: pickMove(role, t, variant, avoidMoves),
    camera_angle: role === 'establish' || role === 'reveal' ? (t.camera.preferred.includes('drone') ? 'high aerial angle' : 'wide, slightly elevated') : role === 'detail' ? 'macro, eye-level' : t.camera.angle,
    lighting: t.lighting.scheme,
  };
}

/** Builds the scene plan. `clip` = { min, max } seconds a single generated clip may last on the chosen provider. */
export function buildStoryboard(t, { duration, clip, lang }) {
  const cfg = TYPES[t.videoType] || TYPES.creative;
  const minScene = Math.min(2, clip.max);
  const n = Math.min(sceneCount(duration, clip.max), Math.max(1, Math.floor(duration / minScene)));
  let roles;
  if (n === 1) roles = ['hero'];
  else {
    const mids = cfg.mid.slice(0, n - 2);
    while (mids.length < n - 2) mids.push(cfg.mid[mids.length % cfg.mid.length]);
    mids.sort((a, b) => ORDER.indexOf(a) - ORDER.indexOf(b));
    roles = [cfg.open, ...mids, 'closing'];
  }
  const durations = splitDuration(duration, roles.map((r) => ROLES[r].w), minScene, clip.max);
  const seen = {};
  const scenes = [];
  roles.forEach((role, i) => {
    const variant = seen[role] || 0; seen[role] = variant + 1;
    const prev = scenes[i - 1]?.camera_move;
    scenes.push({ ...makeScene(role, t, lang, variant, prev ? [prev] : []), duration: durations[i] });
  });
  return scenes;
}

/** A different take on one scene: next description variant and a camera move not used by its neighbours. */
export function alternateScene(scene, t, lang, neighbours = []) {
  const role = ROLES[scene.role] ? scene.role : 'action';
  const variant = (scene.variant || 0) + 1;
  const fresh = makeScene(role, t, lang, variant, [scene.camera_move, ...neighbours]);
  return { ...fresh, duration: scene.duration };
}

export const roleTitle = (role, lang) => (ROLES[role] || ROLES.action).title[lang === 'ar' ? 0 : 1];
export const isValidMove = (m) => !!byId(cameraMoves, m);
export const isValidSize = (s) => !!byId(shotSizes, s);
