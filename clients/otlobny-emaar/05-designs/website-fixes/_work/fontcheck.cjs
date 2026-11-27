const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ extraHTTPHeaders: { 'X-Forwarded-Proto': 'https' } });
  p.on('requestfailed', (r) => console.log('FAILED', r.url().slice(0, 90), r.failure()?.errorText));
  p.on('response', (r) => { if (/fonts\./.test(r.url())) console.log(r.status(), r.url().slice(0, 90)); });
  await p.goto('http://127.0.0.1:8765/?service=zzzz'); await p.waitForTimeout(1500);
  const cdp = await p.context().newCDPSession(p); await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument');
  for (const sel of ['h1', 'footer span', '.brand b']) { const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: sel }); const f = await cdp.send('CSS.getPlatformFontsForNode', { nodeId }); console.log(sel, JSON.stringify(f.fonts)); }
  await b.close(); })();
