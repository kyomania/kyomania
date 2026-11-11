// Einzelbilder zur Kontrolle: node tools_snap.js 1.5 7 ...  -> snaps/t_XX.png
const { chromium } = require('playwright');
(async () => {
  const ts = process.argv.slice(2).map(Number);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + __dirname + '/index.html');
  await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main), null, { polling: 100 });
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  require('fs').mkdirSync(__dirname + '/snaps', { recursive: true });
  for (const t of ts) {
    await p.evaluate((t) => {
      document.querySelectorAll('[data-start]').forEach((el) => {
        if (el.id === 'root' || el.tagName === 'AUDIO') return;
        const s = +el.dataset.start, d = +el.dataset.duration;
        el.style.visibility = t >= s && t < s + d ? 'visible' : 'hidden';
      });
      window.__timelines.main.seek(t);
    }, t);
    await p.waitForTimeout(60);
    await p.screenshot({ path: `${__dirname}/snaps/t_${t.toFixed(2).padStart(5, '0')}.png` });
  }
  await b.close();
})();
