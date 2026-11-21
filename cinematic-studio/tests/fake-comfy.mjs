// TEST DOUBLE — not ComfyUI and not a video model. It answers the ComfyUI HTTP routes the app uses and
// returns a test-pattern clip made by FFmpeg, so the app's own flow (queue, download, validation, timeline,
// export) can be exercised in a browser without a GPU. Nothing it returns is a generated video.
import http from 'node:http';
import fs from 'node:fs';
import crypto from 'node:crypto';

export function startFakeComfy(videoFile, { pollsUntilDone = 2 } = {}) {
  const state = { prompts: [], polls: {}, canceled: new Set(), uploads: 0 };
  const known = ['wan2.2_ti2v_5B_fp16.safetensors', 'umt5_xxl_fp8_e4m3fn_scaled.safetensors', 'wan2.2_vae.safetensors'];
  const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, 'http://x');
    const chunks = []; for await (const c of req) chunks.push(c);
    const raw = Buffer.concat(chunks);
    const json = (code, body) => { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(body)); };
    const body = () => { try { return JSON.parse(raw.toString() || '{}'); } catch { return {}; } };
    const p = url.pathname;
    if (req.method === 'GET' && p === '/system_stats') return json(200, { system: { comfyui_version: 'test-double', os: 'posix' }, devices: [{ name: 'TEST DOUBLE (no GPU)', vram_total: 51e9, vram_free: 48e9 }] });
    if (req.method === 'GET' && p.startsWith('/object_info/')) { const c = p.slice(13); return json(200, { [c]: { input: {} } }); }
    if (req.method === 'GET' && p.startsWith('/models/')) return json(200, known);
    if (req.method === 'POST' && p === '/upload/image') { state.uploads++; return json(200, { name: 'ref.png', subfolder: '', type: 'input' }); }
    if (req.method === 'POST' && p === '/prompt') { const b = body(); if (!b.prompt || !b.client_id) return json(400, { error: { type: 'invalid_prompt', message: 'bad body' } }); const id = crypto.randomUUID(); state.prompts.push({ id, graph: b.prompt }); return json(200, { prompt_id: id, number: 1, node_errors: {} }); }
    if (req.method === 'GET' && p === '/queue') return json(200, { queue_running: state.prompts.filter((x) => (state.polls[x.id] || 0) < pollsUntilDone && !state.canceled.has(x.id)).map((x) => [0, x.id]), queue_pending: [] });
    if (req.method === 'GET' && p.startsWith('/history/')) {
      const id = p.slice(9);
      if (state.canceled.has(id)) return json(200, { [id]: { status: { status_str: 'error', completed: false, messages: [['execution_interrupted', {}]] }, outputs: {} } });
      state.polls[id] = (state.polls[id] || 0) + 1;
      if (state.polls[id] < pollsUntilDone) return json(200, {});
      return json(200, { [id]: { status: { status_str: 'success', completed: true, messages: [] }, outputs: { save: { images: [{ filename: 'cs_00001_.mp4', subfolder: 'cinematic-studio', type: 'output' }], animated: [true] } } } });
    }
    if (req.method === 'GET' && p === '/view') { res.writeHead(200, { 'Content-Type': 'video/mp4' }); return res.end(fs.readFileSync(videoFile)); }
    if (req.method === 'POST' && (p === '/interrupt' || p === '/queue')) { const b = body(); for (const id of [...(b.delete || []), b.prompt_id].filter(Boolean)) state.canceled.add(id); return json(200, {}); }
    json(404, { error: 'not found' });
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve({ url: `http://127.0.0.1:${server.address().port}`, state, close: () => server.close() })));
}
