// usage: node render.js out.mp4 [fps]
//        node render.js --stills t1,t2,... outdir
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto('file://' + path.resolve(__dirname, 'index.html'));
  await page.evaluate(() => window.ready);
  const canvas = await page.$('canvas');
  if (process.argv[2] === '--stills') {
    const ts = process.argv[3].split(',').map(Number);
    for (const t of ts) {
      await page.evaluate(t => window.render(t), t);
      await canvas.screenshot({ path: path.join(process.argv[4], `still_${t.toFixed(2).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 85 });
    }
  } else {
    const out = process.argv[2], fps = +(process.argv[3] || 30);
    const T = await page.evaluate(() => window.T);
    const n = Math.round(T * fps);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'slow', '-movflags', '+faststart', out],
      { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < n; i++) {
      await page.evaluate(t => window.render(t), i / fps);
      const buf = await canvas.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 90 === 0) console.log(`frame ${i}/${n}`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
