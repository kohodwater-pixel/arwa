import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { api } from './api.js';
import { useI18n } from './i18n.jsx';

const Ctx = createContext(null);
export const useSession = () => useContext(Ctx);

/** Current user, limits and the platform's capabilities (/api/meta). */
export function SessionProvider({ children }) {
  const { setLocale } = useI18n();
  const [state, setState] = useState({ loading: true, user: null, limits: null, usage: null });
  const [meta, setMeta] = useState(null);
  const [metaError, setMetaError] = useState(false);

  const loadMeta = useCallback(() => api.get('/meta').then((m) => { setMeta(m); setMetaError(false); }).catch(() => setMetaError(true)), []);
  const refresh = useCallback(async () => {
    try { const r = await api.get('/auth/me'); setState({ loading: false, ...r }); return r.user; }
    catch { setState({ loading: false, user: null, limits: null, usage: null }); return null; }
  }, []);
  useEffect(() => { refresh(); loadMeta(); }, [refresh, loadMeta]);

  const value = useMemo(() => ({
    ...state, meta, metaError, refresh, loadMeta,
    signIn: (r) => { setState({ loading: false, ...r }); if (r.user?.locale) setLocale(r.user.locale); loadMeta(); },
    signOut: async () => { await api.post('/auth/logout').catch(() => {}); setState({ loading: false, user: null, limits: null, usage: null }); },
  }), [state, meta, metaError, refresh, loadMeta, setLocale]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}
