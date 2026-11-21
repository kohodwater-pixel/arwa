/** Thin API client. The session lives in an httpOnly cookie; no secret is ever held in the browser. */
export class ApiError extends Error {
  constructor(status, code, data) { super(code); this.status = status; this.code = code; this.data = data || {}; }
}
async function call(method, path, body, { form } = {}) {
  let res;
  try {
    res = await fetch('/api' + path, {
      method, credentials: 'same-origin',
      headers: { 'x-requested-with': 'studio', ...(body && !form ? { 'content-type': 'application/json' } : {}) },
      body: form ? body : body ? JSON.stringify(body) : undefined,
    });
  } catch { throw new ApiError(0, 'network'); }
  let data = {};
  try { data = await res.json(); } catch { /* empty body */ }
  if (!res.ok) throw new ApiError(res.status, data.error || 'server_error', data);
  return data;
}
export const api = {
  get: (p) => call('GET', p), post: (p, b) => call('POST', p, b), patch: (p, b) => call('PATCH', p, b), put: (p, b) => call('PUT', p, b), del: (p) => call('DELETE', p),
  upload(file, fields = {}) {
    const fd = new FormData();
    Object.entries(fields).forEach(([k, v]) => v != null && fd.append(k, v));
    fd.append('file', file);
    return call('POST', '/assets', fd, { form: true });
  },
};
