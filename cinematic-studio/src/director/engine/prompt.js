import { cameraMoves, shotSizes, byId } from './catalog.js';

const clean = (s) => String(s || '').replace(/\s+/g, ' ').trim().replace(/[.،,;]+$/, '');

/**
 * Compiles one scene into a production prompt for the video model. Sections are ordered by
 * importance; when the provider limits prompt length, the least important sections are dropped
 * first instead of cutting a sentence in half.
 */
export function compileScenePrompt(scene, t, { index, total, maxChars = 2000, negativeSeparate = false }) {
  const move = byId(cameraMoves, scene.camera_move) || cameraMoves[0];
  const size = byId(shotSizes, scene.shot_size) || shotSizes[2];
  const slow = t.camera.slowMotion && ['detail', 'action', 'human', 'hero'].includes(scene.role);
  const isLast = total > 1 && index === total - 1;
  const dof = ['macro', 'close'].includes(size.id) ? 'shallow depth of field, creamy bokeh' : size.id === 'wide' ? 'deep focus' : 'moderate depth of field';

  const few = (arr, n) => arr.slice(0, n).join('; ');
  // [priority, full text, compact text]
  const sections = [
    [1, `${size.p}, ${move.p}${slow ? ', captured in slow motion' : ''}. ${clean(scene.camera_angle || t.camera.angle)}, ${dof}.`],
    [2, `Scene ${index + 1} of ${total}: ${clean(scene.action_en || scene.description)}.`],
    [3, t.elements.length ? `Key elements: ${t.elements.join(', ')}.` : ''],
    [4, `Continuity: ${t.continuity.join('; ')}.`, `Continuity: ${few(t.continuity, 2)}.`],
    [5, `Lighting: ${t.lighting.scheme} — ${t.lighting.details.join('; ')}.`, `Lighting: ${t.lighting.scheme} — ${few(t.lighting.details, 1)}.`],
    [6, `Look: ${t.color.grade}; ${t.color.filmLook}; ${t.camera.lens}.`, `Look: ${t.color.grade}.`],
    [7, isLast ? 'Composition leaves clean negative space for a logo or title; render no text in frame.' : ''],
    [8, t.videoType === 'motion_graphics' ? 'Motion: smooth eased transitions, shapes stay consistent.' : 'Motion: natural, physically plausible, steady pace; one continuous shot, no cuts.'],
    [9, `Quality: ${t.quality.join(', ')}.`, `Quality: ${t.quality.slice(0, 4).join(', ')}.`],
    [10, t.mood.length ? `Mood: ${t.mood.map((m) => m.en).join('; ')}.` : ''],
    [11, `Film brief: ${clean(t.briefEn || t.brief).slice(0, 400)}.`],
    [12, negativeSeparate ? '' : `Avoid: ${t.negative.join(', ')}.`, negativeSeparate ? '' : `Avoid: ${t.negative.slice(0, 4).join(', ')}.`],
  ].filter(([, s]) => s).map(([p, full, compact]) => ({ p, text: full, compact }));

  let kept = sections;
  const len = () => kept.reduce((n, s) => n + s.text.length + 1, -1);
  // 1) shorten from the least important upward, 2) then drop — never the shot line or the scene line
  for (let i = kept.length - 1; i >= 0 && len() > maxChars; i--) if (kept[i].compact) kept[i].text = kept[i].compact;
  for (let p = 12; p > 2 && len() > maxChars; p--) kept = kept.filter((s) => s.p !== p);
  let text = kept.map((s) => s.text).join(' ');
  if (text.length > maxChars) text = text.slice(0, maxChars - 1).replace(/\s+\S*$/, '') + '.';
  return text;
}

export const negativePrompt = (t) => t.negative.join(', ');

/** The film-level production prompt shown to the user ("Cinematic Production Prompt"). */
export function compileMasterPrompt(t) {
  return [
    `CINEMATIC PRODUCTION PROMPT`,
    `Brief: ${clean(t.briefEn || t.brief)}.`,
    t.elements.length ? `Key elements: ${t.elements.join(', ')}.` : null,
    `Camera: ${t.camera.lens}; ${t.camera.angle}; ${t.camera.depthOfField}${t.camera.slowMotion ? '; slow motion on detail and action beats' : ''}${t.camera.preferred.length ? `; signature moves: ${t.camera.preferred.map((m) => byId(cameraMoves, m)?.en).join(', ')}` : ''}.`,
    `Lighting: ${t.lighting.scheme} — ${t.lighting.details.join('; ')}.`,
    `Colour and look: ${t.color.grade}; ${t.color.filmLook}${t.color.grain ? '; subtle film grain' : ''}.`,
    t.mood.length ? `Mood: ${t.mood.map((m) => m.en).join('; ')}. Pace: ${t.pace}.` : `Pace: ${t.pace}.`,
    `Image quality: ${t.quality.join(', ')}.`,
    `Continuity rules: ${t.continuity.join('; ')}.`,
    `Avoid: ${t.negative.join(', ')}.`,
  ].filter(Boolean).join('\n');
}
