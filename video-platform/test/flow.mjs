// End-to-end API walk-through against a running server (demo provider). Usage: node test/flow.mjs http://localhost:4100
const base = process.argv[2] || 'http://localhost:4000';
let cookie = '';
async function api(method, path, body, raw) {
  const res = await fetch(base + '/api' + path, { method, headers: { 'content-type': 'application/json', 'x-requested-with': 'studio', cookie }, body: body ? JSON.stringify(body) : undefined });
  const sc = res.headers.getSetCookie?.() || [];
  if (sc.length) cookie = sc[0].split(';')[0];
  if (raw) return res;
  const j = await res.json().catch(() => ({}));
  return { status: res.status, ...j };
}
const assert = (c, m) => { if (!c) { console.error('FAIL:', m); process.exit(1); } console.log('ok  ', m); };
const email = `t${Date.now()}@example.com`;

let r = await api('POST', '/auth/register', { name: 'Tester', email, password: 'secret-pass-1' });
assert(r.status === 201 && r.user, `register (${r.user?.role})`);
r = await fetch(base + '/api/projects', { method: 'POST', headers: { 'content-type': 'application/json', cookie }, body: '{}' });
assert(r.status === 403, 'CSRF guard rejects calls without the custom header');
r = await api('POST', '/engine/enhance', { description: 'مشهد سينمائي لسيارة رياضية سوداء تسير وسط شوارع طوكيو الممطرة ليلًا، انعكاسات النيون على الأرض', videoType: 'commercial' });
assert(r.treatment?.lighting?.scheme === 'Neon Lighting', 'enhance → Neon Lighting');
r = await api('POST', '/projects', { description: 'x'.repeat(20), videoType: 'commercial', style: 'auto', duration: 30, aspect: '16:9', quality: 'standard', providerId: 'runway' });
assert(r.status === 400 && r.error === 'provider_not_configured', 'unconfigured provider is refused');
r = await api('POST', '/projects', { description: 'x'.repeat(20), videoType: 'commercial', style: 'auto', duration: 30, aspect: '21:9', quality: 'standard', providerId: 'demo' });
assert(r.status === 400 && r.error === 'unsupported_option', 'unsupported aspect is refused');
r = await api('POST', '/projects', { description: 'مشهد سينمائي لسيارة رياضية سوداء تسير وسط شوارع طوكيو الممطرة ليلًا، انعكاسات النيون على الأرض، إضاءة درامية', videoType: 'commercial', style: 'auto', duration: 15, aspect: '9:16', quality: 'standard', providerId: 'demo' });
assert(r.status === 201 && r.project.scenes.length === 3, `project + storyboard (${r.project?.scenes?.length} scenes, ${r.project?.scenes?.map((s) => s.duration)})`);
let p = r.project; const pid = p.id;
r = await api('PATCH', `/projects/${pid}/scenes/${p.scenes[1].id}`, { description: 'لقطة قريبة للعجلات على الأسفلت المبلل', cameraMove: 'orbit', duration: 4 });
assert(r.project.scenes[1].cameraMove === 'orbit' && r.project.scenes[1].prompt.includes('orbit') && r.project.duration === p.duration - p.scenes[1].duration + 4, 'edit scene → prompt recompiled, duration synced');
r = await api('POST', `/projects/${pid}/scenes/${p.scenes[0].id}/regenerate`);
assert(r.project.scenes[0].description !== p.scenes[0].description, 'regenerate one scene → new take');
r = await api('POST', `/projects/${pid}/scenes`, { position: 1 });
assert(r.project.scenes.length === 4 && r.project.scenes.every((s, i) => s.position === i), 'add scene');
const order = r.project.scenes.map((s) => s.id); [order[1], order[2]] = [order[2], order[1]];
r = await api('POST', `/projects/${pid}/scenes/reorder`, { order });
assert(r.project.scenes.map((s) => s.id).join() === order.join(), 'reorder scenes');
r = await api('DELETE', `/projects/${pid}/scenes/${order[2]}`);
assert(r.project.scenes.length === 3, 'delete scene');
r = await api('POST', `/projects/${pid}/generate`);
assert(r.status === 202 && r.project.status === 'generating' && r.project.isDemo, 'generation queued (demo flagged)');
r = await api('PATCH', `/projects/${pid}/scenes/${r.project.scenes[0].id}`, { description: 'تعديل أثناء التوليد' });
assert(r.status === 409, 'edits are refused while generating');
let seen = new Set();
for (let i = 0; i < 90; i++) {
  await new Promise((s) => setTimeout(s, 1000));
  r = await api('GET', `/projects/${pid}`); seen.add(r.project.status);
  if (['completed', 'failed'].includes(r.project.status)) break;
}
assert(r.project.status === 'completed' && r.project.final, `completed (states seen: ${[...seen].join(' → ')}) error=${r.project.error}`);
assert(Math.abs(r.project.final.duration - r.project.duration) < 0.3, `final film ${r.project.final.duration}s ≈ ${r.project.duration}s, ${r.project.final.width}x${r.project.final.height}`);
let v = await api('GET', `/assets/${r.project.final.id}/file`, null, true);
assert(v.status === 200 && v.headers.get('content-type') === 'video/mp4', 'final video downloadable by owner');
v = await fetch(base + `/api/assets/${r.project.final.id}/file`);
assert(v.status === 401, 'video is private without a session');
r = await api('POST', `/projects/${pid}/share`, { enabled: true });
v = await fetch(base + `/api/share/${r.project.shareToken}/video`, { headers: { range: 'bytes=0-99' } });
assert(v.status === 206, 'share link streams with range support');
r = await api('POST', `/projects/${pid}/scenes/${r.project.scenes[1].id}/generate`);
assert(r.status === 202, 're-generate one scene video');
for (let i = 0; i < 60; i++) { await new Promise((s) => setTimeout(s, 1000)); r = await api('GET', `/projects/${pid}`); if (['completed', 'failed'].includes(r.project.status)) break; }
assert(r.project.status === 'completed', 're-assembled after single-scene regeneration');
r = await api('POST', `/projects/${pid}/duplicate`);
assert(r.status === 201 && r.project.status === 'storyboard' && r.project.scenes.every((s) => s.status === 'pending'), 'duplicate project');
r = await api('DELETE', `/projects/${r.project.id}`); assert(r.ok, 'delete project');
r = await api('GET', '/projects'); assert(r.projects.length === 1 && r.counts.completed === 1, 'library lists the project');
r = await api('GET', '/admin/overview'); assert(r.status === 200 || r.status === 403, `admin overview → ${r.status}`);
console.log('ALL PASSED');
