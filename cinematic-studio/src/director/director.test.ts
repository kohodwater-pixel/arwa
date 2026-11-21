import { describe, it, expect } from 'vitest';
import { direct, compileAll, alternate, profileFor, DIRECTOR_FIELDS } from './index';

const AR = 'سيارة رياضية سوداء تسير بسرعة في شوارع الرياض ليلًا تحت المطر مع أضواء نيون وأجواء فاخرة';
const base = { videoType: 'commercial', style: 'auto', duration: 15, modelId: 'wan22-ti2v-5b', maxClipSeconds: 5 };
const arabic = /[؀-ۿ]/;

describe('director engine', () => {
  it('turns an Arabic description into all twelve English decisions', () => {
    const { director } = direct({ ...base, description: AR });
    expect(director.language).toBe('ar');
    for (const f of DIRECTOR_FIELDS) { expect(String(director[f.key]), f.en).not.toBe(''); expect(String(director[f.key]), f.en).not.toMatch(arabic); }
    expect(director.main_subject).toContain('sports car');
    expect(director.environment).toMatch(/Riyadh/);
    expect(director.lighting).toMatch(/Neon/);
    expect(director.camera_movement).toMatch(/Tracking/);
    expect(director.warnings).toHaveLength(0);
  });
  it('writes prompts the model can read: English only, within the profile limit', () => {
    const { scenes } = direct({ ...base, description: AR });
    expect(scenes.length).toBe(3);
    expect(scenes.reduce((n, s) => n + s.duration, 0)).toBe(15);
    for (const s of scenes) {
      expect(s.prompt).not.toMatch(arabic);
      expect(s.prompt!.length).toBeLessThanOrEqual(1400);
      expect(s.duration).toBeLessThanOrEqual(5);
      expect(s.description).toMatch(arabic); // the user still reads the scene in their own language
      expect(s.negative_prompt).toMatch(/flicker/);
    }
  });
  it('is not a word-for-word translation: decisions come from meaning', () => {
    const d = direct({ ...base, description: 'عطر فاخر على طاولة رخام' }).director;
    expect(d.lighting).toMatch(/studio/); // nobody wrote "studio"
    expect(d.visual_style).toMatch(/Luxury/);
  });
  it('says so when it cannot understand the Arabic text', () => {
    const d = direct({ ...base, description: 'شيء غامض لا يوصف' }).director;
    expect(d.warnings.length).toBeGreaterThan(0);
  });
  it('writes a different prompt for each model profile', () => {
    const a = direct({ ...base, description: AR });
    const i2v = compileAll(a.scenes.map((s) => ({ ...s })), a.director, 'wan22-i2v-a14b-4step');
    expect(i2v[0].prompt).not.toBe(a.scenes[0].prompt);
    expect(i2v[0].prompt!.length).toBeLessThanOrEqual(700);
    expect(i2v[0].prompt).not.toMatch(/Colour:/);     // the image already carries the look
    expect(i2v[0].negative_prompt).toBe('');          // CFG 1: negative has no effect, so none is claimed
    expect(profileFor('wan22-i2v-a14b-4step').negative).toBe('ignored');
  });
  it('keeps hand-edited prompts and gives a different take on request', () => {
    const a = direct({ ...base, description: AR });
    a.scenes[1] = { ...a.scenes[1], prompt: 'MY PROMPT', prompt_edited: 1 };
    const again = compileAll(a.scenes, { ...a.director, lighting: 'Hard noon sun' }, base.modelId);
    expect(again[1].prompt).toBe('MY PROMPT');
    expect(again[0].prompt).toMatch(/Hard noon sun/);
    const alt = alternate(a.scenes[0], a.director, [a.scenes[1].camera_move]);
    expect(alt.camera_move).not.toBe(a.scenes[0].camera_move);
    expect(alt.camera_move).not.toBe(a.scenes[1].camera_move);
  });
  it('handles an English description too', () => {
    const { director, scenes } = direct({ ...base, videoType: 'real_estate', description: 'A luxury villa with a pool at sunset, drone shot' });
    expect(director.language).toBe('en');
    expect(director.lighting).toMatch(/Golden Hour/);
    expect(scenes[0].prompt).toMatch(/drone/i);
  });
});
