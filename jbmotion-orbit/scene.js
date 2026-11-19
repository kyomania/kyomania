// JB Motion "Umlauf": ein leuchtendes Filmbild im Raum, drei Umlaufbahnen (eine pro Leistung),
// die Kamera folgt dem Scrollen von Einstellung zu Einstellung.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const css = getComputedStyle(document.documentElement);
const tok = (n) => new THREE.Color(css.getPropertyValue(n).trim());
const C = { space: tok('--space'), ink: tok('--ink'), accent: tok('--accent') };
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const canvas = document.getElementById('scene');

let renderer;
try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true }); } catch { document.body.classList.add('no-gl'); throw new Error('no webgl'); }
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
const scene = new THREE.Scene();
scene.background = C.space;
scene.fog = new THREE.FogExp2(C.space, 0.035);
const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 200);

// Sterne
{
  const n = 2600, p = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { const r = 30 + Math.random() * 60, a = Math.random() * Math.PI * 2, b = Math.acos(Math.random() * 2 - 1); p.set([r * Math.sin(b) * Math.cos(a), r * Math.cos(b), r * Math.sin(b) * Math.sin(a)], i * 3); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(p, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: C.ink, size: 0.09, sizeAttenuation: true, transparent: true, opacity: 0.7, fog: false })));
}

// Das Filmbild: eine 16:9-Scheibe mit live gezeichneter Sequenz
const fc = document.createElement('canvas'); fc.width = 1024; fc.height = 576;
const fx = fc.getContext('2d');
const tex = new THREE.CanvasTexture(fc); tex.colorSpace = THREE.SRGBColorSpace;
const frame = new THREE.Group(); scene.add(frame);
const screen = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 1.8), new THREE.MeshBasicMaterial({ map: tex, transparent: true, side: THREE.DoubleSide }));
frame.add(screen);
const edge = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(3.28, 1.88)), new THREE.LineBasicMaterial({ color: C.ink, transparent: true, opacity: 0.55 }));
frame.add(edge);
const hex = (c) => '#' + c.getHexString();
function drawFilm(t) {
  const w = fc.width, h = fc.height;
  fx.fillStyle = hex(C.space); fx.fillRect(0, 0, w, h);
  // ein Lichtschlitz, der durchs Bild wandert, und Kreise, die sich wie Blenden öffnen
  for (let i = 0; i < 6; i++) {
    const r = ((t * 90 + i * 110) % 660);
    fx.strokeStyle = hex(C.accent); fx.globalAlpha = Math.max(0, 1 - r / 660); fx.lineWidth = 3;
    fx.beginPath(); fx.arc(w * 0.5, h * 0.5, r, 0, Math.PI * 2); fx.stroke();
  }
  fx.globalAlpha = 1;
  const x = (t * 260) % (w + 400) - 200;
  const g = fx.createLinearGradient(x - 160, 0, x + 160, 0);
  g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(0.5, 'rgba(255,255,255,0.22)'); g.addColorStop(1, 'rgba(255,255,255,0)');
  fx.fillStyle = g; fx.fillRect(0, 0, w, h);
  fx.fillStyle = hex(C.ink); fx.font = '800 96px Syne, sans-serif'; fx.textAlign = 'center'; fx.textBaseline = 'middle';
  fx.fillText('JB', w / 2, h / 2 + 4);
  fx.font = '500 22px Manrope, sans-serif'; fx.globalAlpha = 0.6; fx.textAlign = 'left';
  const fr = Math.floor(t * 24) % 24, sec = Math.floor(t) % 60;
  fx.fillText(`00:00:${String(sec).padStart(2, '0')}:${String(fr).padStart(2, '0')}`, 36, h - 36);
  fx.globalAlpha = 1;
  tex.needsUpdate = true;
}

// Drei Umlaufbahnen, je ein Körper darauf
const orbits = [
  { r: 3.1, tilt: [1.25, 0, 0.2], speed: 0.22 },
  { r: 4.2, tilt: [1.0, 0.6, -0.35], speed: -0.15 },
  { r: 5.4, tilt: [1.45, -0.5, 0.5], speed: 0.1 },
].map((o, i) => {
  const grp = new THREE.Group(); grp.rotation.set(...o.tilt); scene.add(grp);
  const pts = new THREE.EllipseCurve(0, 0, o.r, o.r).getPoints(180).map((p) => new THREE.Vector3(p.x, p.y, 0));
  const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: C.ink, transparent: true, opacity: 0.22 }));
  grp.add(line);
  const body = new THREE.Mesh(new THREE.SphereGeometry(0.11 + i * 0.03, 24, 24), new THREE.MeshBasicMaterial({ color: C.ink.clone().multiplyScalar(0.75) }));
  grp.add(body);
  return { ...o, grp, line, body, phase: i * 2.1, glow: 0 };
});

// Kameraeinstellungen pro Abschnitt: Position, Blickpunkt, aktive Bahn
const shots = [
  { pos: [-2.6, 0.6, 11], look: [-2.2, 0, 0], active: -1 },
  { pos: [4.5, 2.2, 7.5], look: [-0.6, 0, 0], active: 0 },
  { pos: [-6.5, -1.2, 6], look: [1.2, 0.2, 0], active: 1 },
  { pos: [2, 6.5, 6.5], look: [-1, 0, 0], active: 2 },
  { pos: [6, 0.3, 9.5], look: [1.8, 0, 0], active: -1 },
  { pos: [0, 2.5, 26], look: [0, 3.5, 0], active: -1 },
].map((s) => ({ pos: new THREE.Vector3(...s.pos), look: new THREE.Vector3(...s.look), active: s.active }));

const panels = [...document.querySelectorAll('[data-shot]')];
const smooth = (x) => x * x * (3 - 2 * x);
function target() {
  // Abschnitts-Mitten auf die Viewport-Mitte abbilden, dazwischen weich überblenden
  const mid = innerHeight / 2;
  const centers = panels.map((p) => { const r = p.getBoundingClientRect(); return r.top + r.height / 2; });
  let i = 0; while (i < centers.length - 2 && centers[i + 1] < mid) i++;
  const span = centers[i + 1] - centers[i];
  const k = Math.min(1, Math.max(0, (mid - centers[i]) / span));
  return { a: shots[i], b: shots[i + 1], k: smooth(k) };
}

const camPos = new THREE.Vector3().copy(shots[0].pos), camLook = new THREE.Vector3().copy(shots[0].look);
const tPos = new THREE.Vector3(), tLook = new THREE.Vector3();

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.55, 0.4, 0.55);
composer.addPass(bloom);
composer.addPass(new OutputPass());

function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h, false); composer.setSize(w, h); bloom.setSize(w, h);
  camera.aspect = w / h; camera.fov = w < 700 ? 58 : 40; camera.updateProjectionMatrix();
}
addEventListener('resize', resize); resize();

const clock = new THREE.Clock();
function tick() {
  const dt = Math.min(clock.getDelta(), 0.05), t = clock.elapsedTime;
  const { a, b, k } = target();
  tPos.lerpVectors(a.pos, b.pos, k); tLook.lerpVectors(a.look, b.look, k);
  const ease = still ? 1 : 1 - Math.pow(0.002, dt);
  camPos.lerp(tPos, ease); camLook.lerp(tLook, ease);
  camera.position.copy(camPos); camera.lookAt(camLook);

  const act = k < 0.5 ? a.active : b.active;
  orbits.forEach((o, i) => {
    const ang = o.phase + (still ? 0 : t * o.speed);
    o.body.position.set(Math.cos(ang) * o.r, Math.sin(ang) * o.r, 0);
    o.glow += ((act === i ? 1 : 0) - o.glow) * Math.min(1, dt * 4);
    o.line.material.color.copy(C.ink).lerp(C.accent, o.glow);
    o.line.material.opacity = 0.22 + o.glow * 0.7;
    o.body.material.color.copy(C.ink).multiplyScalar(0.75).lerp(C.accent, o.glow);
  });
  frame.rotation.y = still ? -0.25 : Math.sin(t * 0.3) * 0.25 - 0.2;
  frame.position.y = still ? 0 : Math.sin(t * 0.6) * 0.06;
  drawFilm(still ? 2 : t);
  composer.render();
  if (!still) requestAnimationFrame(tick);
}
if (still) { addEventListener('scroll', () => requestAnimationFrame(tick), { passive: true }); }
document.fonts.ready.then(() => tick());
