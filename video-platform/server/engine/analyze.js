import { detect, hasArabic } from './lexicon.js';
import { styles, byId } from './catalog.js';

const SUBJECT_CLASS = {
  vehicle: ['car', 'sports_car', 'motorcycle', 'plane', 'boat'],
  person: ['man', 'woman', 'child', 'family', 'people'],
  product: ['product', 'perfume', 'watch', 'phone', 'jewelry', 'logo', 'robot'],
  food: ['food', 'coffee'],
  architecture: ['building', 'villa', 'hotel', 'pool'],
  animal: ['horse', 'camel', 'falcon', 'animal'],
};
const classOf = (id) => Object.keys(SUBJECT_CLASS).find((k) => SUBJECT_CLASS[k].includes(id)) || 'generic';

/**
 * Rule-based director: reads the description and decides camera, lighting, colour, quality and
 * continuity. Every decision is traceable to a detected cue (see `rationale`).
 */
export function analyze(description, { videoType = 'creative', style = 'auto' } = {}) {
  const found = detect(description);
  const g = (group) => found.filter((c) => c.group === group);
  const has = (id) => found.some((c) => c.id === id);
  const lang = hasArabic(description) ? 'ar' : 'en';
  const isMotion = videoType === 'motion_graphics';
  const rationale = [];
  const why = (ar, en) => rationale.push({ ar, en });

  // ── subject ──
  let subjects = g('subject');
  if (has('sports_car')) subjects = subjects.filter((s) => s.id !== 'car');
  if (subjects.some((s) => s.id !== 'product' && classOf(s.id) === 'product')) subjects = subjects.filter((s) => s.id !== 'product');
  const main = subjects.find((s) => classOf(s.id) !== 'person' || subjects.length === 1) || subjects[0] || null;
  const subjectClass = main ? classOf(main.id) : (videoType === 'product' ? 'product' : videoType === 'real_estate' ? 'architecture' : 'generic');
  const people = subjects.filter((s) => classOf(s.id) === 'person');
  const colors = g('color').filter((c) => !(c.id === 'gold' && has('golden_hour')));
  const place = g('place')[0] || null;
  const envs = g('env');
  const env = envs.find((e) => e.id !== 'road') || envs[0] || null;
  const weather = g('weather')[0] || null;
  let time = g('time')[0] || null;
  if (!time && has('neon')) time = found.find((c) => c.id === 'night') || { id: 'night', en: 'night', ar: 'ليلًا' };
  const moods = g('mood');
  const moving = has('moving') || has('energetic');

  // ── style ──
  let styleId = style;
  if (style === 'auto' || !byId(styles, style)) {
    if (has('neon') || (time?.id === 'night' && env?.id === 'city' && weather?.id === 'rain')) styleId = 'noir';
    else if (has('luxury') || subjectClass === 'product' && (has('perfume') || has('watch') || has('jewelry')) || videoType === 'real_estate') styleId = 'luxury';
    else if (has('epic') || (videoType === 'tourism' && ['desert', 'mountain', 'heritage'].includes(env?.id))) styleId = 'epic';
    else if (has('energetic') && ['social', 'commercial'].includes(videoType)) styleId = 'energetic';
    else if (has('romantic') || has('calm')) styleId = 'dreamy';
    else if (env?.id === 'studio') styleId = 'minimal';
    else if (videoType === 'social') styleId = 'energetic';
    else styleId = 'realism';
    const s = byId(styles, styleId);
    why(`الأسلوب «${s.ar}» اختير تلقائيًا من دلالات الوصف ونوع الفيديو.`, `Style "${s.en}" was chosen automatically from the cues in the description and the video type.`);
  }
  const st = byId(styles, styleId);

  // ── lighting ──
  let scheme, details = [];
  const explicitLight = g('light').map((l) => l.id);
  if (isMotion) { scheme = 'Graphic Lighting'; details.push('flat even illumination with soft gradient depth, no photographic shadows'); }
  else if (explicitLight.includes('neon') || (!explicitLight.length && st.light === 'neon' && time?.id === 'night')) {
    scheme = 'Neon Lighting'; details.push('saturated neon signs as practical key sources, coloured rim light on the subject');
    why('ذُكر النيون أو مشهد ليلي حضري ← إضاءة نيون عملية مع حواف ملوّنة.', 'Neon or a night-time urban scene → practical neon key light with coloured rims.');
  } else if (time?.id === 'golden_hour') { scheme = 'Golden Hour'; details.push('low warm sun, long soft shadows, backlit rim light and gentle lens flare'); why('وقت الغروب ← إضاءة الساعة الذهبية.', 'Sunset → golden hour lighting.'); }
  else if (time?.id === 'blue_hour') { scheme = 'Blue Hour'; details.push('cool ambient twilight balanced with warm practical lights'); why('الشفق ← إضاءة الساعة الزرقاء.', 'Twilight → blue hour lighting.'); }
  else if (time?.id === 'dawn') { scheme = 'Natural Lighting'; details.push('soft dawn light with a cool-to-warm gradient and light mist'); }
  else if (time?.id === 'night') {
    scheme = env?.id === 'city' || env?.id === 'road' ? 'Cinematic Lighting' : 'Dramatic Lighting';
    details.push(env?.id === 'city' || env?.id === 'road' ? 'night exterior lit by practical street lights and signage, motivated rim light' : 'low-key moonlit scene with one motivated warm source');
    why('مشهد ليلي ← إضاءة منخفضة بمصادر عملية داخل الكادر.', 'Night scene → low-key lighting from practical sources in frame.');
  } else if (explicitLight.includes('candle')) { scheme = 'Cinematic Lighting'; details.push('warm candle and lantern practicals, soft falloff into shadow'); }
  else if (env?.id === 'studio' || (subjectClass === 'product' && !env)) { scheme = 'Cinematic Lighting'; details.push('studio lighting: large soft key, crisp rim light, controlled specular reflections'); why('منتج/استوديو ← إضاءة استوديو ناعمة مع ضوء حافة.', 'Product / studio → soft studio key with rim light.'); }
  else if (env?.id === 'interior' || subjectClass === 'food') { scheme = 'Natural Lighting'; details.push('soft motivated window light with warm practical lamps'); }
  else { scheme = st.light === 'natural' || explicitLight.includes('natural') ? 'Natural Lighting' : 'Cinematic Lighting'; details.push('soft directional daylight with natural contrast and gentle fill'); }
  if (!isMotion) {
    if (explicitLight.includes('dramatic') && scheme !== 'Dramatic Lighting') { details.push('dramatic high-contrast ratio with deep shadows'); if (scheme === 'Cinematic Lighting') scheme = 'Dramatic Lighting'; }
    if (explicitLight.includes('volumetric') || ['fog', 'dust'].includes(weather?.id) || (weather?.id === 'rain' && time?.id === 'night')) {
      details.push('volumetric light shafts through the atmosphere');
      why('جو فيه مطر/ضباب/غبار ← إضاءة حجمية تُظهر حزم الضوء.', 'Rain / fog / dust in the air → volumetric light that reveals the beams.');
    }
    if (weather?.id === 'rain' || explicitLight.includes('reflections')) details.push('wet surfaces mirroring every light source');
  }

  // ── camera ──
  const cues = g('camera').map((c) => c.id);
  const preferred = [];
  if (cues.includes('c_drone')) preferred.push('drone');
  if (cues.includes('c_tracking') || moving) preferred.push('tracking');
  if (cues.includes('c_crane')) preferred.push('crane_up');
  if (cues.includes('c_dolly')) preferred.push('dolly_in');
  if (cues.includes('c_orbit')) preferred.push('orbit');
  if (cues.includes('c_handheld')) preferred.push('handheld');
  if (cues.includes('c_pan')) preferred.push('pan');
  if (moving) why('العنصر الرئيسي متحرك ← لقطات تتبع (Tracking) بسرعة مطابقة.', 'The subject is moving → tracking shots at matching speed.');
  const slowMotion = cues.includes('c_slowmo') || (!moving && ['rain', 'snow', 'dust'].includes(weather?.id)) || subjectClass === 'food';
  const angle = subjectClass === 'vehicle' || subjectClass === 'architecture' ? 'low angle' : subjectClass === 'product' || subjectClass === 'food' ? 'eye-level, slightly above' : 'eye-level';
  const avoidHandheld = ['luxury', 'minimal', 'epic'].includes(styleId) || videoType === 'real_estate' || isMotion;

  // ── quality, continuity, negative ──
  const quality = isMotion
    ? ['clean vector-style motion graphics', 'smooth eased animation', 'crisp shapes and edges', 'consistent design system']
    : ['photorealistic', 'ultra detailed', 'professional cinematography', 'realistic physics', 'natural motion', 'high dynamic range', ...(st.grain ? ['subtle film grain'] : [])];

  const colorEn = colors.map((c) => c.en).join(' and ');
  const subjectEn = main ? `${colorEn ? colorEn + ' ' : ''}${main.en}`.replace(/^(a|the) /, (m) => (colorEn ? '' : m)) : null;
  const elements = [subjectEn, ...people.filter((p) => p !== main).map((p) => p.en), place?.en, env?.en, weather?.en, time?.en].filter(Boolean);

  const continuity = [];
  if (main && classOf(main.id) !== 'person') continuity.push(`the same ${subjectEn} in every shot: identical design, colour, proportions and details`);
  if (people.length) continuity.push('the same people in every shot: identical faces, hair, age, wardrobe and accessories');
  if (place || env) continuity.push(`one consistent location (${[place?.en, env?.en].filter(Boolean).join(', ')}) with matching architecture and props`);
  if (weather || time) continuity.push(`unchanged conditions: ${[time?.en, weather?.en].filter(Boolean).join(', ')}`);
  continuity.push(`one consistent look: ${st.lens}, ${st.grade}`);

  const negative = isMotion
    ? ['photographic realism', 'flicker', 'jittery motion', 'inconsistent shapes between frames', 'illegible or garbled text', 'watermarks']
    : ['morphing or warping objects', 'distorted faces or hands', 'extra limbs or fingers', 'flicker', 'jittery, floaty or sped-up motion', 'duplicated subjects', 'on-screen text, captions, watermarks', 'cartoon or CGI look',
      ...(subjectClass === 'vehicle' ? ['deformed wheels', 'sliding or hovering vehicle'] : []),
      ...(subjectClass === 'architecture' ? ['bent or melting architecture lines'] : [])];

  return {
    engine: 'rules', language: lang, brief: String(description).trim(), videoType, styleId,
    subject: { id: main?.id || null, class: subjectClass, en: subjectEn, ar: main?.ar || null, people: people.map((p) => p.id) },
    setting: { place: place && { en: place.en, ar: place.ar }, env: env && { id: env.id, en: env.en, ar: env.ar }, weather: weather && { id: weather.id, en: weather.en, ar: weather.ar }, time: time && { id: time.id, en: time.en, ar: time.ar } },
    mood: moods.map((m) => ({ en: m.en, ar: m.ar })),
    camera: { preferred, avoidHandheld, slowMotion, angle, lens: st.lens, depthOfField: 'shallow depth of field on close shots, deep focus on wide shots', moving },
    lighting: { scheme, details },
    color: { grade: st.grade, filmLook: st.look, grain: !!st.grain && !isMotion },
    pace: st.pace, quality, continuity, negative, elements,
    detected: found.map((c) => ({ id: c.id, group: c.group, en: c.en, ar: c.ar })),
    rationale,
  };
}
