import path from 'node:path';
import fs from 'node:fs';
import express from 'express';
import cookieParser from 'cookie-parser';
import { config } from './config.js';
import './db.js';
import * as log from './log.js';
import { loadUser, csrfGuard, HttpError } from './auth.js';
import { authRouter } from './routes/auth.js';
import { projectsRouter } from './routes/projects.js';
import { assetsRouter, publicAssetsRouter } from './routes/assets.js';
import { adminRouter } from './routes/admin.js';
import { metaRouter, setFfmpeg } from './routes/meta.js';
import { registerPipeline } from './pipeline.js';
import { startWorker } from './queue.js';
import { ffmpegAvailable } from './ffmpeg.js';

export const app = express();
app.disable('x-powered-by');
app.set('trust proxy', 1);
app.use((_req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Referrer-Policy', 'same-origin');
  res.setHeader('Content-Security-Policy', "default-src 'self'; img-src 'self' data: blob:; media-src 'self' blob:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'");
  next();
});
app.use(express.json({ limit: '200kb' }));
app.use(cookieParser());

const api = express.Router();
api.use(loadUser, csrfGuard);
api.use('/auth', authRouter);
api.use('/', metaRouter);
api.use('/public', publicAssetsRouter);
api.use('/projects', projectsRouter);
api.use('/assets', assetsRouter);
api.use('/admin', adminRouter);
api.use((_req, _res, next) => next(new HttpError(404, 'not_found')));
api.use((err, req, res, _next) => {
  if (err instanceof HttpError) return res.status(err.status).json({ error: err.code, ...(err.extra || {}) });
  if (err?.type === 'entity.parse.failed' || err?.type === 'entity.too.large') return res.status(400).json({ error: 'bad_request' });
  log.error('http.unhandled', String(err?.stack || err).slice(0, 1500), { userId: req.user?.id, path: req.path, method: req.method });
  res.status(500).json({ error: 'server_error' });
});
app.use('/api', api);

// built front end (vite build → dist/)
const dist = path.join(config.root, 'dist');
if (fs.existsSync(dist)) {
  app.use(express.static(dist, { index: false, maxAge: '1h' }));
  app.get(/^(?!\/api\/).*/, (_req, res) => res.sendFile(path.join(dist, 'index.html')));
}

if (process.env.NODE_ENV !== 'test' || process.env.START_SERVER === '1') {
  registerPipeline();
  startWorker();
  ffmpegAvailable().then((ok) => { setFfmpeg(ok); if (!ok) log.error('startup.ffmpeg', 'ffmpeg was not found: demo clips and final assembly will fail'); });
  app.listen(config.port, () => log.info('startup', `${config.appName} listening on :${config.port}`));
}
