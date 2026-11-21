import { actionFor, compileOne, type Director, type SceneDraft } from '../director';
import { rpc } from './rpc';

const hasArabic = (s: string) => /[؀-ۿ]/.test(s || '');
/** A stored scene as the director sees it. The English action line is rebuilt from the scene's role when the
 *  description is in Arabic, because the Arabic text is for the user, not for the model. */
export function toDraft(scene: any, d: Director, scenes: any[]): SceneDraft {
  const variant = scenes.filter((s) => s.role === scene.role && s.position < scene.position).length;
  const role = scene.role || 'action';
  let action_en: string | undefined;
  try { action_en = hasArabic(scene.description) ? actionFor(role, d, variant) : undefined; } catch { action_en = undefined; }
  return { ...scene, role, variant, action_en };
}
/** Rewrites the prompts of all scenes the user has not edited by hand, and saves them. Returns the project. */
export async function recompileProject(project: any, d: Director, modelId: string, onlySceneId?: string, force = false) {
  let out = project;
  for (const s of project.scenes) {
    if (onlySceneId && s.id !== onlySceneId) continue;
    if (s.prompt_edited && !force) continue;
    if (['queued', 'generating'].includes(s.status)) continue;
    const c = compileOne(toDraft(s, d, project.scenes), d, modelId, s.position, project.scenes.length);
    if (c.prompt !== s.prompt || c.negative_prompt !== s.negative_prompt || s.prompt_edited) out = await rpc('scene_update', { id: s.id, patch: { ...c, prompt_edited: false } });
  }
  return out;
}
export const sceneVideo = (root: string, s: any) => (s?.video_path ? `${root.replace(/[\\/]+$/, '')}/${s.video_path}` : '');
export const scenePreview = (root: string, s: any) => (s?.preview_path ? `${root.replace(/[\\/]+$/, '')}/${s.preview_path}` : '');
