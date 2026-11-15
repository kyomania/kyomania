// node capture.cjs outdir [workers] [sub]  -> outdir/%06d.jpg at FPS*sub
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const out=process.argv[2],NW=+(process.argv[3]||4),SUB=+(process.argv[4]||4),FR=900;fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch();
await Promise.all(Array.from({length:NW},async(_,w)=>{const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.resolve(__dirname,'../build/index.html'));await p.waitForFunction(()=>window.__ready);
for(let f=w;f<FR;f+=NW)for(let k=0;k<SUB;k++){await p.evaluate(([f,k,n])=>window.renderSub(f,k,n),[f,k,SUB]);
await p.screenshot({type:'jpeg',quality:93,path:`${out}/${String(f*SUB+k).padStart(6,'0')}.jpg`});}}));
await b.close();console.log('done')})();
