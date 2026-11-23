// Shared helpers for cardmarket.pro three.js reels (deterministic, seek-safe).
window.CM = (() => {
  const MINT = "#5ee0d4", TEAL = "#00877a", GR = "#0a1118", W = "#ffffff", PAPER = "#f0f3f4";
  const CARD_D = "M210,170 L640,70 L690,130 L605,690 Q600,725 560,730 L180,770 Q110,775 110,700 L150,230 Q155,180 210,170 Z";
  const CC_D = "M435,258 L370,385 L345,410 Q330,440 340,490 Q350,525 380,525 L580,525 L565,640 Q562,648 550,648 L320,648 Q240,640 210,560 Q195,520 205,420 Q220,350 280,320 Z";
  const ACC_D = "M495,238 L610,238 Q620,240 612,252 L548,375 Q540,385 528,385 L420,385 Q410,383 415,372 Z";
  const CARD = new Path2D(CARD_D), CC = new Path2D(CC_D), ACC = new Path2D(ACC_D);
  const mono = (px, w = 500) => `${w} ${px}px "JetBrains Mono", monospace`;
  const disp = (px) => `900 ${px}px "Inter Tight", sans-serif`;
  const mk = (w, h) => Object.assign(document.createElement("canvas"), { width: w, height: h });
  function mark(g, cx, cy, s, card, c, acc) {
    g.save(); g.translate(cx - 400 * s, cy - 420 * s); g.scale(s, s);
    g.fillStyle = card; g.fill(CARD); g.fillStyle = c; g.fill(CC); g.fillStyle = acc; g.fill(ACC); g.restore();
  }
  function minis(g, w, h, col, alpha) {
    g.save(); g.globalAlpha = alpha; g.fillStyle = col;
    for (let r = 0; r < Math.ceil(h / 62); r++) for (let c = 0; c < Math.ceil(w / 62); c++) {
      if ((r * 5 + c * 3) % 4 === 0) continue;
      g.save(); g.translate(30 + c * 62 + (r % 2) * 20, 30 + r * 62); g.rotate(((r + c) % 3 - 1) * 0.3);
      g.beginPath(); g.roundRect(-11, -15, 22, 30, 4); g.fill(); g.restore();
    }
    g.restore();
  }
  function rng(seed) { let a = seed >>> 0; return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const cl = (v) => Math.min(1, Math.max(0, v));
  const E = {
    out: (p) => 1 - Math.pow(1 - p, 3), in: (p) => p * p * p,
    io: (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
    expo: (p) => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * p)),
    back: (p, c1 = 1.6) => { const c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); },
  };
  const lerp = (a, b, p) => a + (b - a) * p;
  function setup() {
    const W3 = 1080, H3 = 1920;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(1); renderer.setSize(W3, H3, false);
    renderer.outputEncoding = THREE.sRGBEncoding; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.1;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(30, W3 / H3, 0.1, 100); camera.position.set(0, 0, 11);
    scene.add(new THREE.HemisphereLight(0xcfe9ec, 0x101820, 0.7));
    const key = new THREE.DirectionalLight(0xffffff, 1.3); key.position.set(-4, 6, 8); scene.add(key);
    const rim = new THREE.DirectionalLight(0x5ee0d4, 1.4); rim.position.set(5, 2, -6); scene.add(rim);
    const texs = [];
    const tex = (cv) => { const t = new THREE.CanvasTexture(cv); t.encoding = THREE.sRGBEncoding; t.anisotropy = 8; texs.push(t); return t; };
    const edge = new THREE.MeshStandardMaterial({ color: 0xd9e3e5, roughness: 0.5 });
    return { renderer, scene, camera, tex, texs, edge, W3, H3 };
  }
  // motion-blurred composite of SUB sub-frames into a 2D canvas
  function blurDraw(og, ctx, pose, t, sub = 5, shutter = (1 / 30) * 0.7) {
    og.clearRect(0, 0, ctx.W3, ctx.H3);
    for (let i = 0; i < sub; i++) {
      pose(Math.max(0, t - shutter * (i / (sub - 1)))); ctx.renderer.render(ctx.scene, ctx.camera);
      og.globalAlpha = i === 0 ? 1 : 1 / (i + 1); og.drawImage(ctx.renderer.domElement, 0, 0);
    }
    og.globalAlpha = 1; return pose(t);
  }
  // sparks: deterministic burst particles
  function sparks(scene, n, seed, color = 0x9ff5ec, size = 0.06) {
    const r = rng(seed), g = new THREE.BufferGeometry(), pos = new Float32Array(n * 3), dir = [];
    for (let i = 0; i < n; i++) { const th = r() * Math.PI * 2, ph = Math.acos(2 * r() - 1); dir.push([Math.sin(ph) * Math.cos(th), Math.sin(ph) * Math.sin(th), Math.cos(ph), 2 + r() * 5]); }
    g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const m = new THREE.PointsMaterial({ color, size, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false });
    const pts = new THREE.Points(g, m); scene.add(pts);
    return { set(t0, t, origin, dur = 1.0) {
      const dt = t - t0; pts.visible = dt >= 0 && dt < dur; if (!pts.visible) return;
      for (let i = 0; i < n; i++) { const [x, y, z, s] = dir[i], d = s * dt * (1 - 0.45 * dt / dur);
        pos[i * 3] = origin.x + x * d; pos[i * 3 + 1] = origin.y + y * d - 1.5 * dt * dt; pos[i * 3 + 2] = origin.z + z * d; }
      g.attributes.position.needsUpdate = true; m.opacity = 1 - dt / dur;
    } };
  }
  function ring(scene, color = 0x5ee0d4) {
    const m = new THREE.MeshBasicMaterial({ color, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(new THREE.RingGeometry(0.92, 1, 96), m); scene.add(mesh);
    return { set(t0, t, origin, maxR = 5, dur = 0.7) { const p = (t - t0) / dur; mesh.visible = p >= 0 && p < 1; if (!mesh.visible) return;
      mesh.position.copy(origin); mesh.scale.setScalar(0.2 + maxR * E.out(p)); m.opacity = 0.9 * (1 - p); } };
  }
  function shake(t, hits, amp = 0.12) {
    let x = 0, y = 0;
    for (const h of hits) { const d = t - h; if (d < 0 || d > 0.5) continue; const k = amp * Math.exp(-d * 9);
      x += Math.sin(d * 90) * k; y += Math.cos(d * 75) * k; }
    return [x, y];
  }
  return { MINT, TEAL, GR, W, PAPER, CARD, CC, ACC, mono, disp, mk, mark, minis, rng, cl, E, lerp, setup, blurDraw, sparks, ring, shake };
})();
