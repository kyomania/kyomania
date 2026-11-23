const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto('file://'+process.cwd()+'/phone2.html');await pg.waitForTimeout(2500);
const N=Math.round(11.4*30);for(let i=0;i<N;i++){await pg.evaluate(async t=>{seek(t);try{await document.getElementById('v').decode()}catch(e){}},i/30);await pg.screenshot({path:`fr/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close()})();
