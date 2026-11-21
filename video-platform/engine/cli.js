#!/usr/bin/env node
/** Operator CLI for datasets (runs on the engine host). Usage: node engine/cli.js help */
import * as d from './lib/datasets.js';
const [cmd, ...a] = process.argv.slice(2);
const opt = (name, fallback) => { const i = a.indexOf(`--${name}`); return i >= 0 ? a[i + 1] : fallback; };
const out = (x) => console.log(JSON.stringify(x, null, 2));
try {
  if (cmd === 'dataset:create') out(d.create({ slug: a[0], specialty: a[1], name: opt('name'), target: JSON.parse(opt('target', '{}')) }));
  else if (cmd === 'dataset:add') out(await d.ingest(a[0], a[1], { source: opt('source'), holder: opt('holder'), license: opt('license'), peopleConsent: opt('people-consent'), doc: opt('doc') }));
  else if (cmd === 'dataset:list') out(d.items(a[0], opt('status')));
  else if (cmd === 'dataset:review') out(d.review(a[0], a[1], { status: opt('status'), reason: opt('reason'), caption: opt('caption') }));
  else if (cmd === 'dataset:show') out(d.summary(a[0]));
  else if (cmd === 'dataset:export') out(d.exportFor(a[0], opt('trainer', 'musubi-tuner'), opt('out', './exports')));
  else console.log(`dataset:create <slug> <gulf_ads|luxury_real_estate|saudi_tourism> [--name N] [--target '{"width":1280,"height":720,"fps":16,"frames":81}']
dataset:add <slug> <folder> --source S --holder H --license L [--people-consent C] [--doc path]
dataset:list <slug> [--status pending|approved|rejected]
dataset:review <slug> <itemId> [--status approved|rejected] [--reason R] [--caption "…"]
dataset:show <slug>
dataset:export <slug> --trainer musubi-tuner|diffusion-pipe --out <folder>`);
} catch (e) { console.error('error:', e.message); process.exit(1); }
