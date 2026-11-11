const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const f of [1, 2, 3, 4]) {
    await p.goto('file://' + __dirname + '/styleframes.html?f=' + f);
    await p.waitForFunction(() => document.title === 'ready');
    await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode?.())); });
    await p.waitForTimeout(400);
    await p.screenshot({ path: `styleframes/frame${f}.png` });
  }
  await b.close();
})();
