import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os'; import path from 'node:path'; import fs from 'node:fs';
process.env.NODE_ENV = 'test';
process.env.DATA_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-test-'));
process.env.ANTHROPIC_API_KEY = '';

const { analyze } = await import('../server/engine/analyze.js');
const { buildStoryboard, splitDuration, sceneCount, alternateScene } = await import('../server/engine/storyboard.js');
const { compileScenePrompt } = await import('../server/engine/prompt.js');
const { detect } = await import('../server/engine/lexicon.js');
const { direct } = await import('../server/engine/index.js');

const TOKYO = 'مشهد سينمائي لسيارة رياضية سوداء تسير وسط شوارع طوكيو الممطرة ليلًا، انعكاسات النيون على الأرض، إضاءة درامية، واقعية فائقة.';

test('lexicon: Arabic prefixes match, look-alike words do not', () => {
  const ids = detect(TOKYO).map((c) => c.id);
  for (const id of ['sports_car', 'black', 'tokyo', 'rain', 'night', 'neon', 'moving']) assert.ok(ids.includes(id), id);
  assert.ok(!ids.includes('riyadh'), '«رياضية» must not be read as الرياض');
  assert.ok(detect('فندق فاخر بالرياض').some((c) => c.id === 'riyadh'));
});

test('analysis: neon rainy night → neon lighting, noir look, tracking, continuity lock', () => {
  const t = analyze(TOKYO, { videoType: 'commercial' });
  assert.equal(t.lighting.scheme, 'Neon Lighting');
  assert.equal(t.styleId, 'noir');
  assert.ok(t.camera.preferred.includes('tracking'));
  assert.equal(t.subject.en, 'black sports car');
  assert.ok(t.continuity[0].includes('the same black sports car'));
  assert.ok(t.negative.some((n) => n.includes('wheels')));
  assert.equal(t.language, 'ar');
});

test('analysis: English sunset villa → golden hour, luxury, no handheld', () => {
  const t = analyze('A luxury villa with an infinity pool in Dubai at sunset, drone shot', { videoType: 'real_estate' });
  assert.equal(t.lighting.scheme, 'Golden Hour');
  assert.equal(t.styleId, 'luxury');
  assert.ok(t.camera.avoidHandheld && t.camera.preferred.includes('drone'));
});

test('durations: always sum to the total and respect the clip limits', () => {
  for (const total of [5, 10, 15, 30, 60, 47, 120]) for (const max of [5, 8, 10]) {
    const n = sceneCount(total, max);
    const d = splitDuration(total, Array(n).fill(1).map((_, i) => 1 + (i % 3) * 0.2), Math.min(2, max), max);
    assert.equal(d.reduce((a, b) => a + b, 0), total, `${total}s / max ${max}`);
    assert.ok(d.every((x) => x >= 1 && x <= max));
  }
});

test('storyboard: 30 s commercial → 5 scenes, opening first, logo space last, no repeated move back to back', () => {
  const t = analyze(TOKYO, { videoType: 'commercial' });
  const s = buildStoryboard(t, { duration: 30, clip: { min: 2, max: 10 }, lang: 'ar' });
  assert.equal(s.length, 5);
  assert.equal(s[0].role, 'establish'); assert.equal(s.at(-1).role, 'closing');
  assert.equal(s.reduce((n, x) => n + x.duration, 0), 30);
  s.slice(1).forEach((x, i) => assert.notEqual(x.camera_move, s[i].camera_move));
  const alt = alternateScene(s[1], t, 'ar', [s[0].camera_move, s[2].camera_move]);
  assert.notEqual(alt.camera_move, s[1].camera_move);
  assert.notEqual(alt.description, s[1].description);
});

test('prompt: fits the provider limit and keeps shot, scene and continuity', async () => {
  const { treatment, scenes } = await direct({ description: TOKYO, videoType: 'commercial', style: 'auto', duration: 30, caps: { clip: { min: 2, max: 10 }, maxPromptChars: 1000, negativePrompt: false } });
  assert.equal(treatment.engine, 'rules');
  for (const s of scenes) { assert.ok(s.prompt.length <= 1000, String(s.prompt.length)); assert.match(s.prompt, /Continuity: the same black sports car/); assert.match(s.prompt, /Neon Lighting/); }
  assert.match(scenes.at(-1).prompt, /negative space for a logo/);
  const tiny = compileScenePrompt(scenes[0], treatment, { index: 0, total: 5, maxChars: 300 });
  assert.ok(tiny.length <= 300 && tiny.includes('Scene 1 of 5'));
});
