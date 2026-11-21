/** Shared HTTP helper for provider adapters: timeout, JSON handling and a normalised error type. */
export class ProviderError extends Error {
  constructor(message, { status = 0, retryable = false, code = 'provider_error', retryAfterMs } = {}) {
    super(message); this.status = status; this.retryable = retryable; this.code = code; this.retryAfterMs = retryAfterMs;
  }
}

export async function request(url, { method = 'GET', headers = {}, json, timeoutMs = 60_000, raw = false } = {}) {
  let res;
  try {
    res = await fetch(url, {
      method,
      headers: { ...(json !== undefined ? { 'content-type': 'application/json' } : {}), ...headers },
      body: json !== undefined ? JSON.stringify(json) : undefined,
      signal: AbortSignal.timeout(timeoutMs),
    });
  } catch (e) {
    throw new ProviderError(`network error: ${e.cause?.code || e.name || e.message}`, { retryable: true, code: 'provider_unreachable' });
  }
  if (raw && res.ok) return res;
  const text = await res.text();
  let body; try { body = text ? JSON.parse(text) : {}; } catch { body = { raw: text.slice(0, 500) }; }
  if (!res.ok) {
    const msg = body?.error?.message || body?.error || body?.message || body?.detail?.message || body?.detail || body?.raw || res.statusText;
    const ra = Number(res.headers.get('retry-after'));
    throw new ProviderError(`${res.status}: ${typeof msg === 'string' ? msg : JSON.stringify(msg)}`.slice(0, 500), {
      status: res.status,
      retryable: [408, 409, 429].includes(res.status) || res.status >= 500,
      code: res.status === 401 || res.status === 403 ? 'provider_auth' : res.status === 429 ? 'provider_rate_limited' : res.status === 400 || res.status === 422 ? 'provider_rejected' : 'provider_error',
      retryAfterMs: Number.isFinite(ra) && ra > 0 ? ra * 1000 : undefined,
    });
  }
  return body;
}

/** Smallest clip length the provider can generate that covers `seconds`. */
export function fitClip(clip, seconds) {
  if (clip.values) return clip.values.find((v) => v >= seconds) ?? clip.values[clip.values.length - 1];
  return Math.min(clip.max, Math.max(clip.min, Math.ceil(seconds)));
}
