// Measures white-text contrast against the rendered background behind each text block (text hidden for the sample).
const {chromium}=require('playwright');const path=require('path');const {PNG}=(()=>{try{return require('pngjs')}catch(e){return {}}})();
(async()=>{const dir=path.resolve(__dirname,'..');const b=await chromium.launch();const out={};
for(const L of process.argv.slice(2)){const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await p.goto('file://'+path.join(dir,`imagine-more_alula-trip-story_option-${L}_ar_v02.html`));await p.evaluate(()=>document.fonts.ready);
 const sel={headline:'.headline',sub:'.sub',chip_date:'.chips .cell.date',chip_tag:'.chips .cell:last-child',price_label:'.price .label',price_299:'.price .now',price_320:'.price .was span',group_note:'.price .group',inc_tag:'.inc-label',inc_items:'.inc',phone:'.phone'};
 const rects=await p.evaluate(sel=>{const o={};for(const k in sel){o[k]=[...document.querySelectorAll(sel[k])].map(e=>{const r=document.createRange();r.selectNodeContents(e);const q=r.getBoundingClientRect();return [q.left,q.top,q.right,q.bottom]})}return o},sel);
 await p.addStyleTag({content:'.story *{color:transparent!important}.story svg,.story img,.story .rule,.cta{visibility:hidden!important}.was span::after{display:none!important}'});
 await p.waitForTimeout(300);await p.screenshot({path:path.join(__dirname,`bgonly_${L}.png`)});out[L]=rects;await p.close();}
require('fs').writeFileSync(path.join(__dirname,'rects.json'),JSON.stringify(out));await b.close();})();
