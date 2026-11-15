// usage: node stills.cjs out.png t1 t2 ...  -> contact sheet (4 cols, 480px each)
const {chromium}=require('playwright');const path=require('path');
(async()=>{const [out,...ts]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+path.resolve(__dirname,'../build/index.html'));await p.waitForFunction(()=>window.__ready,null,{timeout:20000});
const shots=[];for(const t of ts){await p.evaluate(t=>window.renderAt(t),+t);shots.push((await p.screenshot({type:'jpeg',quality:85})).toString('base64'));}
const q=await b.newPage({viewport:{width:1920,height:Math.ceil(ts.length/4)*(270+22)}});
await q.setContent(`<body style="margin:0;background:#333;display:grid;grid-template-columns:repeat(4,480px);font:14px monospace;color:#fff">${shots.map((s,i)=>`<div><img src="data:image/jpeg;base64,${s}" width=480 height=270 style="display:block"><div>t=${ts[i]}</div></div>`).join('')}</body>`);
await q.screenshot({path:out,fullPage:true});console.log(errs.join('\n')||'ok');await b.close();})();
