// Cinematic Director Engine.
// A rule-based director: it reads the description (Arabic or English), recognises concepts through a
// bilingual lexicon, and takes the directing decisions itself. It is not a translator and it does not call
// any model: Arabic words the lexicon does not know are reported to the user instead of being passed to a
// video model that was not trained on Arabic.
import { analyze } from './engine/analyze.js';
import { buildStoryboard, alternateScene, describeScene } from './engine/storyboard.js';
import { cameraMoves, shotSizes, styles, videoTypes, byId } from './engine/catalog.js';

export { cameraMoves, shotSizes, styles, videoTypes };

/** The twelve directing decisions. All values are English: they are what the model is prompted with. */
export type Director = {
  main_subject: string; environment: string; scene_composition: string; camera_movement: string; camera_angle: string; lens: string;
  lighting: string; color_grading: string; motion_description: string; atmosphere: string; visual_style: string; negative_instructions: string;
  // context kept with the decisions
  language: 'ar' | 'en'; brief: string; style_id: string; video_type: string; slow_motion: boolean; is_motion_graphics: boolean;
  detected: { id: string; group: string; en: string; ar: string }[]; rationale: { ar: string; en: string }[]; warnings: { ar: string; en: string }[];
  treatment: any;
};
export const DIRECTOR_FIELDS: { key: keyof Director; ar: string; en: string }[] = [
  { key: 'main_subject', ar: 'العنصر الرئيسي', en: 'Main Subject' }, { key: 'environment', ar: 'البيئة', en: 'Environment' },
  { key: 'scene_composition', ar: 'تكوين المشهد', en: 'Scene Composition' }, { key: 'camera_movement', ar: 'حركة الكاميرا', en: 'Camera Movement' },
  { key: 'camera_angle', ar: 'زاوية الكاميرا', en: 'Camera Angle' }, { key: 'lens', ar: 'العدسة', en: 'Lens' },
  { key: 'lighting', ar: 'الإضاءة', en: 'Lighting' }, { key: 'color_grading', ar: 'تدريج الألوان', en: 'Color Grading' },
  { key: 'motion_description', ar: 'وصف الحركة', en: 'Motion Description' }, { key: 'atmosphere', ar: 'الأجواء', en: 'Atmosphere' },
  { key: 'visual_style', ar: 'الأسلوب البصري', en: 'Visual Style' }, { key: 'negative_instructions', ar: 'تعليمات الاستبعاد', en: 'Negative Instructions' },
];

/** How one model family wants to be prompted. A new model gets a new profile; nothing else changes. */
export type PromptProfile = {
  id: string; label: string; maxChars: number; negative: 'separate' | 'ignored';
  notes: { ar: string; en: string }[];
  compile: (scene: SceneDraft, d: Director, index: number, total: number) => string;
  negativeFor: (d: Director) => string;
};
export type SceneDraft = {
  role?: string; variant?: number; title: string; duration: number; description: string; action_en?: string;
  camera_move: string; shot_size: string; camera_angle?: string; lighting?: string; prompt?: string; negative_prompt?: string; prompt_edited?: number;
};

const clean = (s: unknown) => String(s || '').replace(/\s+/g, ' ').trim().replace(/[.،,;]+$/, '');
const sentence = (s: string) => (s ? s.charAt(0).toUpperCase() + s.slice(1) + '.' : '');
const hasArabic = (s: string) => /[؀-ۿ]/.test(s);
function fit(parts: [number, string][], max: number) {
  let kept = parts.filter(([, s]) => s);
  const len = () => kept.reduce((n, [, s]) => n + s.length + 1, -1);
  for (let p = Math.max(...kept.map(([q]) => q)); p > 2 && len() > max; p--) kept = kept.filter(([q]) => q !== p);
  let text = kept.map(([, s]) => s).join(' ');
  if (text.length > max) text = text.slice(0, max - 1).replace(/\s+\S*$/, '') + '.';
  return text;
}
const shotLine = (s: SceneDraft, d: Director) => {
  const move = byId(cameraMoves, s.camera_move) || cameraMoves[0], size = byId(shotSizes, s.shot_size) || shotSizes[2];
  const slow = d.slow_motion && ['detail', 'action', 'human', 'hero'].includes(s.role || '');
  return `${size.p}, ${move.p}${slow ? ', captured in slow motion' : ''}`;
};
/** The English action line of a scene; an Arabic description the user typed is never sent to the model as-is. */
const action = (s: SceneDraft) => clean(s.action_en || (hasArabic(s.description) ? '' : s.description));

// Wan 2.2 text-to-video: the Wan prompt guide asks for plain descriptive prose (subject, scene, motion, then
// aesthetic controls such as light, colour and lens). The workflow takes the negative prompt separately.
const wanT2V: PromptProfile = {
  id: 'wan22-ti2v-5b', label: 'Wan 2.2 TI2V-5B', maxChars: 1400, negative: 'separate',
  notes: [
    { ar: 'نثر وصفي بالإنجليزية: العنصر ثم المكان ثم الحركة ثم الضوء واللون والعدسة.', en: 'Descriptive English prose: subject, setting, motion, then light, colour and lens.' },
    { ar: 'برومبت الاستبعاد يُرسل منفصلًا عن الوصف.', en: 'The negative prompt is sent separately from the description.' },
    { ar: 'عند وجود صورة مرجعية للمشهد تصبح هي الإطار الأول.', en: 'When a scene has a reference image, it becomes the first frame.' },
  ],
  compile: (s, d, i, total) => fit([
    [1, sentence(`${shotLine(s, d)}, ${clean(s.camera_angle || d.camera_angle)}`)],
    [2, sentence(action(s) || clean(d.main_subject))],
    [3, d.main_subject ? `Main subject: ${clean(d.main_subject)}.` : ''],
    [4, d.environment ? `Setting: ${clean(d.environment)}.` : ''],
    [5, `Lighting: ${clean(s.lighting && s.lighting !== d.treatment?.lighting?.scheme ? `${s.lighting}; ${d.lighting}` : d.lighting)}.`],
    [6, `Motion: ${clean(d.motion_description)}.`],
    [7, `Colour: ${clean(d.color_grading)}. Lens: ${clean(d.lens)}.`],
    [8, total > 1 && i === total - 1 ? 'Composition leaves clean negative space for a title; no text in frame.' : `Composition: ${clean(d.scene_composition)}.`],
    [9, d.atmosphere ? `Atmosphere: ${clean(d.atmosphere)}.` : ''],
    [10, `Style: ${clean(d.visual_style)}.`],
  ], 1400),
  negativeFor: (d) => clean(d.negative_instructions),
};
// Wan 2.2 A14B image-to-video with the 4-step LightX2V LoRAs: the picture already fixes subject, place and
// look, so the prompt describes what moves and how the camera moves. The graph runs at CFG 1, where the
// negative conditioning has no effect; the app says so instead of pretending it is used.
const wanI2V: PromptProfile = {
  id: 'wan22-i2v-a14b-4step', label: 'Wan 2.2 I2V-A14B (4-step)', maxChars: 700, negative: 'ignored',
  notes: [
    { ar: 'الصورة المرجعية تحدد العنصر والمكان والشكل؛ البرومبت يصف الحركة وحركة الكاميرا فقط.', en: 'The reference image fixes subject, place and look; the prompt describes motion and camera movement only.' },
    { ar: 'هذا المسار يعمل عند CFG = 1، فلا أثر لبرومبت الاستبعاد فيه.', en: 'This workflow runs at CFG 1, so the negative prompt has no effect.' },
    { ar: 'كل مشهد يحتاج صورة مرجعية.', en: 'Every scene needs a reference image.' },
  ],
  compile: (s, d) => fit([
    [1, sentence(shotLine(s, d))],
    [2, sentence(action(s) || clean(d.main_subject))],
    [3, `Motion: ${clean(d.motion_description)}.`],
    [4, d.atmosphere ? `Atmosphere: ${clean(d.atmosphere)}.` : ''],
    [5, 'The subject keeps the same identity, proportions and details as in the first frame.'],
  ], 700),
  negativeFor: () => '',
};
export const PROFILES: PromptProfile[] = [wanT2V, wanI2V];
export const profileFor = (modelId: string) => PROFILES.find((p) => p.id === modelId) || wanT2V;

function composition(t: any) {
  const c = t.subject.class;
  if (t.videoType === 'motion_graphics') return 'centred graphic layout on a clean grid, generous margins';
  if (c === 'product' || c === 'food') return 'subject centred with clean negative space, soft background separation';
  if (c === 'architecture') return 'symmetrical framing with strong leading lines and straight verticals';
  if (c === 'vehicle') return 'rule of thirds with lead room in the direction of travel, low horizon';
  if (c === 'person') return 'rule of thirds with natural headroom, layered foreground and background';
  return 'rule of thirds with layered foreground, midground and background';
}

function toDirector(t: any): Director {
  const s = t.setting;
  const warnings: Director['warnings'] = [];
  if (t.language === 'ar' && !t.subject.en) warnings.push({ ar: 'لم يتعرّف المخرج على عنصر رئيسي في الوصف. اكتب العنصر الرئيسي بالإنجليزية في حقل «العنصر الرئيسي».', en: 'No main subject was recognised in the description. Write the main subject in English in the "Main Subject" field.' });
  if (t.language === 'ar' && t.detected.length < 4) warnings.push({ ar: `تعرّف المخرج على ${t.detected.length} مفهومًا فقط من الوصف العربي. النماذج المفتوحة لا توثّق دعم العربية، لذلك تُبنى البرومبتات بالإنجليزية من المفاهيم المتعرَّف عليها؛ راجع الحقول وأكمل ما ينقص.`, en: `Only ${t.detected.length} concepts were recognised in the Arabic description. Open video models do not document Arabic support, so prompts are built in English from recognised concepts; review the fields and fill in what is missing.` });
  const moves = (t.camera.preferred as string[]).map((m) => byId(cameraMoves, m)?.en).filter(Boolean);
  return {
    main_subject: [t.subject.en, ...(t.elements as string[]).filter((e) => e !== t.subject.en && !Object.values(s).some((x: any) => x?.en === e))].filter(Boolean).join(', '),
    environment: [s.place?.en, s.env?.en, s.weather?.en, s.time?.en].filter(Boolean).join(', '),
    scene_composition: composition(t),
    camera_movement: moves.length ? `${moves.join(', ')}; smooth and motivated${t.camera.avoidHandheld ? ', no handheld shake' : ''}` : `smooth, motivated moves chosen per scene${t.camera.avoidHandheld ? ', no handheld shake' : ''}`,
    camera_angle: t.camera.angle, lens: `${t.color ? byId(styles, t.styleId)?.lens : ''}; ${t.camera.depthOfField}`,
    lighting: `${t.lighting.scheme}: ${t.lighting.details.join('; ')}`,
    color_grading: t.color.grade,
    motion_description: t.videoType === 'motion_graphics' ? 'smooth eased transitions, shapes stay consistent' : `natural, physically plausible motion at a ${t.pace} pace${t.camera.moving ? ', the subject moving steadily through the frame' : ''}${t.camera.slowMotion ? ', slow motion on detail and action beats' : ''}; one continuous shot, no cuts`,
    atmosphere: [...t.mood.map((m: any) => m.en), s.weather?.en].filter(Boolean).join(', '),
    visual_style: `${byId(styles, t.styleId)?.en}: ${t.color.filmLook}${t.color.grain ? ', subtle film grain' : ''}; ${t.quality.slice(0, 4).join(', ')}`,
    negative_instructions: t.negative.join(', '),
    language: t.language, brief: t.brief, style_id: t.styleId, video_type: t.videoType, slow_motion: !!t.camera.slowMotion, is_motion_graphics: t.videoType === 'motion_graphics',
    detected: t.detected, rationale: t.rationale, warnings, treatment: t,
  };
}

export type DirectInput = { description: string; videoType: string; style: string; duration: number; modelId: string; maxClipSeconds: number };
export type DirectOutput = { director: Director; scenes: SceneDraft[] };

/** Description → directing decisions → storyboard → one prompt per scene, written for the chosen model. */
export function direct(input: DirectInput): DirectOutput {
  const t = analyze(input.description, { videoType: input.videoType, style: input.style });
  const director = toDirector(t);
  const clip = { min: 2, max: Math.max(2, Math.floor(input.maxClipSeconds)) };
  const scenes: SceneDraft[] = buildStoryboard(t, { duration: input.duration, clip, lang: t.language }).map((s: any) => ({ ...s, action_en: describeScene(s.role, t, 'en', s.variant) }));
  return { director, scenes: compileAll(scenes, director, input.modelId) };
}

/** Rewrites the prompt of every scene the user has not edited by hand. */
export function compileAll<T extends SceneDraft>(scenes: T[], d: Director, modelId: string): T[] {
  const p = profileFor(modelId);
  return scenes.map((s, i) => (s.prompt_edited ? s : { ...s, prompt: p.compile(s, d, i, scenes.length), negative_prompt: p.negativeFor(d) }));
}
export function compileOne(scene: SceneDraft, d: Director, modelId: string, index: number, total: number) {
  const p = profileFor(modelId);
  return { prompt: p.compile(scene, d, index, total), negative_prompt: p.negativeFor(d) };
}

/** A different take on one scene: another description variant and a camera move its neighbours do not use. */
export function alternate(scene: SceneDraft, d: Director, neighbours: string[]): SceneDraft {
  const fresh = alternateScene(scene, d.treatment, d.language, neighbours);
  return { ...scene, ...fresh, action_en: describeScene(fresh.role, d.treatment, 'en', fresh.variant), prompt_edited: 0 };
}
/** English action line for a scene of the given role, used when the user adds a scene by hand. */
export const actionFor = (role: string, d: Director, variant = 0) => describeScene(role, d.treatment, 'en', variant);
