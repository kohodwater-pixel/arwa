const {chromium}=require('playwright');
(async()=>{const [,,src,out,w,h,full]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
await p.goto('file://'+require('path').resolve(src));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
await p.screenshot({path:out,fullPage:full==='full'});await b.close();})();
