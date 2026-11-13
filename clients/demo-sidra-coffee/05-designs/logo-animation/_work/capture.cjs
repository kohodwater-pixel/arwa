// Frame-by-frame capture: node capture.cjs <html> <framesDir> <refSvg>
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [html, dir, ref] = process.argv.slice(2); fs.mkdirSync(dir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(html) + '?capture');
  const N = 90;                                   // 3.0 s at 30 fps; frame i shows t = i/30, last frame shows t = 3.0
  for (let i = 0; i < N; i++) {
    const t = i === N - 1 ? 3.0 : i / 30;
    await page.evaluate(t => window.setTime(t), t);
    await page.screenshot({ path: path.join(dir, 'f' + String(i).padStart(3, '0') + '.png') });
  }
  // reference: the approved static SVG as an image at the same position and size
  await page.setContent('<body style="margin:0;background:#F3ECE0;width:1080px;height:1080px;overflow:hidden"><img src="file://' + path.resolve(ref) + '" style="position:absolute;left:270px;top:384.2px;width:540px;height:311.6px">');
  await page.waitForLoadState('load');
  await page.screenshot({ path: path.join(dir, 'reference_static-logo.png') });
  await browser.close(); console.log('frames', N);
})();
