import Anthropic from '@anthropic-ai/sdk';
import { z } from 'zod';
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';
import { config } from '../config.js';
import { cameraMoves, shotSizes } from './catalog.js';

/**
 * Optional AI director. When ANTHROPIC_API_KEY is configured, Claude rewrites the rule-based plan:
 * it translates the brief into production English, writes a precise appearance lock for the subject
 * and the location (the main lever for continuity between scenes), and writes each scene's action.
 * The rule-based plan stays the skeleton (scene count, durations, look), so a failure here never
 * blocks the user: the caller falls back to the rule-based result.
 */
export const aiDirectorAvailable = () => !!config.anthropicKey;

let client;
const getClient = () => (client ||= new Anthropic({ apiKey: config.anthropicKey, baseURL: config.anthropicBaseUrl, timeout: 90_000, maxRetries: 1 }));

const moveIds = cameraMoves.map((m) => m.id);
const sizeIds = shotSizes.map((s) => s.id);

const SceneOut = z.object({
  description: z.string().describe("One or two sentences in the user's language describing the shot for the storyboard card."),
  action_en: z.string().describe('English, max 45 words: what is in frame, what moves and how, where the shot starts and where it ends. One continuous shot, no cuts.'),
  camera_move: z.enum(moveIds),
  shot_size: z.enum(sizeIds),
});
const PlanOut = z.object({
  brief_en: z.string().describe('The brief rewritten in clear production English, max 60 words. Add nothing the user did not ask for.'),
  subject_lock: z.string().describe('English, max 50 words: exact, repeatable appearance of the main subject or characters (colour, materials, shape, age, hair, wardrobe). Reused verbatim in every scene.'),
  location_lock: z.string().describe('English, max 40 words: exact, repeatable description of the location, time of day and weather.'),
  scenes: z.array(SceneOut),
});

const SYSTEM = `You are the director of photography and first assistant director for a text-to-video production pipeline.
You receive a client brief and a scene skeleton prepared by a planning tool. Each scene will be generated separately by a video model that sees only its own prompt, so anything that must look the same across scenes has to be written down explicitly: that is what subject_lock and location_lock are for.

Write for the camera. Each scene is a single continuous shot of a few seconds: describe one clear action with a start and an end, with physically plausible motion at a natural speed. Keep the story logical from scene to scene (same subject, same place, same time of day, same direction of travel) and make each scene advance the purpose of the film. The last scene should resolve on a composition with room for a logo or end line, without any rendered text.

Stay inside the brief: do not invent brands, slogans, people or locations the client did not mention. Keep the scene count, order and durations of the skeleton. You may change a scene's camera move or shot size when another choice from the allowed list serves the shot better, and avoid repeating the same move in consecutive scenes.

Scene descriptions shown to the client are written natively in the client's language (Arabic briefs get natural Modern Standard Arabic, not a translation of the English). The *_en fields are always English.`;

async function ask(schema, user) {
  const res = await getClient().messages.parse({
    model: config.directorModel,
    max_tokens: 16000,
    thinking: { type: 'adaptive' },
    output_config: { effort: 'medium', format: zodOutputFormat(schema) },
    system: SYSTEM,
    messages: [{ role: 'user', content: user }],
  });
  if (res.stop_reason === 'refusal') throw new Error('ai_director_declined');
  if (!res.parsed_output) throw new Error(`ai_director_unparsed (${res.stop_reason})`);
  return res.parsed_output;
}

const context = (t, scenes, lang) => JSON.stringify({
  client_language: lang === 'ar' ? 'Arabic' : 'English',
  video_type: t.videoType, style: t.styleId, lighting: t.lighting, look: t.color, lens: t.camera.lens, pace: t.pace,
  scenes: scenes.map((s, i) => ({ n: i + 1, beat: s.role, seconds: s.duration, shot_size: s.shot_size, camera_move: s.camera_move, draft: s.description })),
}, null, 2);

/** Returns { briefEn, subjectLock, locationLock, scenes } — throws on any API or validation problem. */
export async function directPlan(t, scenes, lang) {
  const out = await ask(PlanOut, `Client brief:\n<brief>\n${t.brief}\n</brief>\n\nPlan prepared by the planning tool:\n${context(t, scenes, lang)}\n\nReturn exactly ${scenes.length} scenes, in this order.`);
  if (out.scenes.length !== scenes.length) throw new Error('ai_director_scene_count');
  return out;
}

/** A new take on one scene, consistent with the others. */
export async function directScene(t, scenes, index, lang) {
  return ask(SceneOut, `Client brief:\n<brief>\n${t.brief}\n</brief>\n\nCurrent plan:\n${context(t, scenes, lang)}\n\nSubject lock: ${t.subjectLock || 'n/a'}\nLocation lock: ${t.locationLock || 'n/a'}\n\nThe client asked for a different take on scene ${index + 1} (beat: ${scenes[index].role}, ${scenes[index].duration} seconds). Write a clearly different shot for the same beat that still fits between its neighbours. Do not reuse its current camera move (${scenes[index].camera_move}).`);
}
