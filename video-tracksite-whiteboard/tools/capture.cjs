// Schnelle Bild-für-Bild-Aufnahme der HyperFrames-Komposition (gleiche Timeline wie `hyperframes render`).
// node tools/capture.cjs <projektordner> <ausgabeordner> <startFrame> <endFrame> [fps]
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [dir, out, a, b, fpsArg] = process.argv.slice(2); const fps = +(fpsArg || 30); fs.mkdirSync(out, { recursive: true });
const type = (f) => f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html' : f.endsWith('.woff2') ? 'font/woff2' : 'application/octet-stream';
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': type(f) }); r.end(d); }); }).listen(0, async () => {
  const br = await chromium.launch({ args: ['--disable-gpu', '--disable-gpu-compositing', '--mute-audio'] });
  const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('ERR', e.message));
  await p.goto(`http://localhost:${srv.address().port}/index.html`);
  await new Promise((r) => setTimeout(r, 5000));
  for (let f = +a; f < +b; f++) {
    await p.evaluate((t) => { window.__timelines.main.seek(t); return 1; }, f / fps);
    await p.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => r(1))))); // rafWait
    await p.screenshot({ path: path.join(out, `f${String(f).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 95, timeout: 60000 });
    if (f % 50 === 0) console.log('frame', f);
  }
  await br.close(); srv.close();
});
