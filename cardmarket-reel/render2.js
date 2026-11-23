const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto('file://'+process.cwd()+'/reel2.html');await pg.waitForTimeout(4000);
for(let i=0;i<375;i++){await pg.evaluate(t=>seek(t),i/30);await pg.screenshot({path:`fr/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close()})();
