// Renders each option HTML to an exact 1080x1920 PNG.
const {chromium}=require('playwright');const path=require('path');
(async()=>{const dir=path.resolve(__dirname,'..');const b=await chromium.launch();
for(const L of process.argv.slice(2)){const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 const base=`imagine-more_alula-trip-story_option-${L}_ar_v02`;
 await p.goto('file://'+path.join(dir,base+'.html'));await p.evaluate(()=>document.fonts.ready);
 const fonts=await p.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight));
 const imgs=await p.evaluate(()=>[...document.images].map(i=>i.naturalWidth>0));
 await p.waitForTimeout(500);await p.screenshot({path:path.join(dir,base+'.png'),clip:{x:0,y:0,width:1080,height:1920}});
 console.log(L,'fonts:',fonts.join(', '),'| images ok:',imgs.every(Boolean));await p.close();}
await b.close();})();
