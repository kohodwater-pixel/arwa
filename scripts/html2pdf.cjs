#!/usr/bin/env node
/**
 * Render an HTML file to PDF (and optional PNG previews) with Chromium.
 * Chromium shapes Arabic and handles RTL correctly, so this is the agency's
 * standard route for Arabic and bilingual PDFs.
 *
 * Usage: node scripts/html2pdf.cjs <input.html> <output.pdf> [--size A4|A4-landscape|WxHmm] [--png <dir>]
 */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: html2pdf.cjs <input.html> <output.pdf> [--size A4|A4-landscape|WxHmm] [--png <dir>]');
    process.exit(2);
  }
  const input = path.resolve(args[0]);
  const output = path.resolve(args[1]);
  const opt = (name) => { const i = args.indexOf(name); return i > -1 ? args[i + 1] : null; };
  const size = opt('--size') || 'A4';
  const pngDir = opt('--png');

  const pdfOpts = { path: output, printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } };
  if (size === 'A4') pdfOpts.format = 'A4';
  else if (size === 'A4-landscape') { pdfOpts.format = 'A4'; pdfOpts.landscape = true; }
  else { const m = size.match(/^(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)mm$/); if (!m) { console.error('Bad --size'); process.exit(2); } pdfOpts.width = m[1] + 'mm'; pdfOpts.height = m[2] + 'mm'; }

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + input, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => `${f.family} ${f.weight}`));
  const failed = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'error').map(f => `${f.family} ${f.weight}`));
  fs.mkdirSync(path.dirname(output), { recursive: true });
  await page.pdf(pdfOpts);
  if (pngDir) {
    fs.mkdirSync(pngDir, { recursive: true });
    await page.screenshot({ path: path.join(pngDir, path.basename(output, '.pdf') + '_fullpage.png'), fullPage: true });
  }
  await browser.close();
  console.log(JSON.stringify({ output, webfonts_loaded: [...new Set(fonts)], webfonts_failed: [...new Set(failed)] }, null, 2));
  if (failed.length) process.exit(1);
})().catch((e) => { console.error(e); process.exit(1); });
