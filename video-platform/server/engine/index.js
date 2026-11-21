import { analyze } from './analyze.js';
import { buildStoryboard, alternateScene } from './storyboard.js';
import { compileScenePrompt, compileMasterPrompt, negativePrompt } from './prompt.js';
import { aiDirectorAvailable, directPlan, directScene } from './llm.js';
import { warn } from '../log.js';

export { analyze, compileMasterPrompt, negativePrompt, aiDirectorAvailable };
export * from './catalog.js';

/**
 * Cinematic Engine entry point: description → treatment → storyboard → per-scene production prompts.
 * `caps` describes what the chosen provider/quality can do (clip durations, prompt length, negative prompt).
 */
export async function direct({ description, videoType, style, duration, caps, useAi = true, ctx = {} }) {
  const t = analyze(description, { videoType, style });
  const lang = t.language;
  let scenes = buildStoryboard(t, { duration, clip: caps.clip, lang });
  if (useAi && aiDirectorAvailable()) {
    try {
      const plan = await directPlan(t, scenes, lang);
      t.engine = 'ai';
      t.briefEn = plan.brief_en; t.subjectLock = plan.subject_lock; t.locationLock = plan.location_lock;
      t.continuity = [`Subject (identical in every shot): ${plan.subject_lock}`, `Location (identical in every shot): ${plan.location_lock}`, t.continuity[t.continuity.length - 1]];
      scenes = scenes.map((s, i) => ({ ...s, description: plan.scenes[i].description, action_en: plan.scenes[i].action_en, camera_move: plan.scenes[i].camera_move, shot_size: plan.scenes[i].shot_size }));
    } catch (e) {
      t.aiError = String(e.message || e).slice(0, 200);
      warn('engine.ai_fallback', t.aiError, ctx);
    }
  }
  return { treatment: { ...t, masterPrompt: compileMasterPrompt(t) }, scenes: withPrompts(scenes, t, caps) };
}

export function withPrompts(scenes, t, caps) {
  return scenes.map((s, i) => (s.prompt_edited ? s : { ...s, prompt: compileScenePrompt(s, t, { index: i, total: scenes.length, maxChars: caps.maxPromptChars, negativeSeparate: caps.negativePrompt }) }));
}

/** New take on one scene (AI when available, rule-based otherwise). */
export async function redirectScene(t, scenes, index, { useAi = true, ctx = {} } = {}) {
  const lang = t.language, cur = scenes[index];
  if (useAi && t.engine === 'ai' && aiDirectorAvailable()) {
    try {
      const s = await directScene(t, scenes, index, lang);
      return { ...cur, ...s, variant: (cur.variant || 0) + 1, prompt_edited: 0 };
    } catch (e) { warn('engine.ai_fallback', String(e.message || e).slice(0, 200), ctx); }
  }
  const neighbours = [scenes[index - 1]?.camera_move, scenes[index + 1]?.camera_move].filter(Boolean);
  return { ...cur, ...alternateScene(cur, t, lang, neighbours), action_en: null, prompt_edited: 0 };
}
