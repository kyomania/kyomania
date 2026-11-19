// fast.site "Zuhause": das Haus mit Chevron-Dach bleibt stehen, die Welt drumherum bewegt sich.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const css = getComputedStyle(document.documentElement);
const tok = (n) => new THREE.Color(css.getPropertyValue(n).trim());
const C = { blue: tok('--blue'), green: tok('--green'), red: tok('--red'), yellow: tok('--yellow'), ground: tok('--ground'), white: tok('--white') };
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const canvas = document.getElementById('scene');

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  if (!renderer.getContext()) throw 0;
} catch { document.documentElement.classList.add('no-gl'); throw new Error('no webgl'); }
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);

// Licht: eine Sonne, die in Station 4 sieben Tage durchläuft
scene.add(new THREE.HemisphereLight(0xffffff, C.ground, 0.9));
const sun = new THREE.DirectionalLight(0xfff1dc, 2.2);
sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -6, right: 6, top: 6, bottom: -6, near: 0.5, far: 30 });
sun.shadow.radius = 6;
scene.add(sun, sun.target);

// Boden: nur von oben sichtbar, damit die Kamera in Station 2 darunter schauen kann
const ground = new THREE.Mesh(new THREE.CircleGeometry(9, 96), new THREE.MeshStandardMaterial({ color: C.ground, roughness: 0.95, side: THREE.FrontSide }));
ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

// Fundament: Anwendung, Inhalte, Hosting als drei Schichten unter dem Haus
const layers = [C.blue, C.green, C.yellow].map((c, i) => {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(1.9 - i * 0.12, 1.9 - i * 0.12, 0.34, 64), new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.25, clearcoat: 1, clearcoatRoughness: 0.15 }));
  m.position.y = -0.32 - i * 0.48; scene.add(m); return m;
});

// Tempo-Spuren: farbige Bänder, die am Haus vorbeiziehen
const trailMat = (color, off) => new THREE.ShaderMaterial({
  transparent: true, depthWrite: false, side: THREE.DoubleSide,
  uniforms: { uT: { value: 0 }, uC: { value: color }, uO: { value: off }, uA: { value: 1 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
  fragmentShader: `uniform float uT,uO,uA; uniform vec3 uC; varying vec2 vUv;
    void main(){ float h=fract(uT*.35+uO); float d=vUv.x-h; d-=floor(d+.5);
      float a=smoothstep(-.32,0.,d)*smoothstep(.02,0.,d); gl_FragColor=vec4(uC*1.15, a*uA*.95); }`,
});
const trails = [C.blue, C.green, C.red, C.yellow].map((c, i) => {
  const r = 2.4 + i * 0.35, y = 0.35 + i * 0.42;
  const pts = []; for (let k = 0; k <= 64; k++) { const a = -2.6 + (k / 64) * 5.2; pts.push(new THREE.Vector3(Math.sin(a) * r * 1.4, y + Math.sin(a * 2 + i) * 0.12, Math.cos(a) * r * 0.9)); }
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 160, 0.07 - i * 0.008, 12, false), trailMat(c, i * 0.23));
  scene.add(mesh); return mesh;
});

// Modelle laden: Haus im Zentrum, Waage daneben
const loader = new GLTFLoader();
const fitModel = (obj, height) => {
  const box = new THREE.Box3().setFromObject(obj), size = box.getSize(new THREE.Vector3());
  obj.scale.setScalar(height / size.y);
  const b2 = new THREE.Box3().setFromObject(obj), c = b2.getCenter(new THREE.Vector3());
  obj.position.x -= c.x; obj.position.z -= c.z; obj.position.y -= b2.min.y;
  obj.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; if (o.material) o.material.envMapIntensity = 1.1; } });
  return obj;
};
const house = new THREE.Group(); scene.add(house);
const scale = new THREE.Group(); scale.position.set(2.7, 0, 0.6); scale.scale.setScalar(0.001); scene.add(scale);
loader.load('assets/3d/haus.glb', (g) => house.add(fitModel(g.scene, 2.2)), undefined, () => {
  const m = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.3, 1.4), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transmission: 0.4, roughness: 0.3 }));
  m.position.y = 0.65; m.castShadow = true; house.add(m);
});
loader.load('assets/3d/waage.glb', (g) => scale.add(fitModel(g.scene, 2.0)));

// Kameraeinstellungen pro Abschnitt
const shots = [
  { pos: [3.6, 2.6, 7.6], look: [-2.6, 1.0, 0] },
  { pos: [-3.8, -3.2, 9.5], look: [1.8, -0.5, 0] },
  { pos: [5.2, 2.0, 7.6], look: [-1.6, 0.9, 0] },
  { pos: [-4.2, 4.6, 7.4], look: [1.5, 0.6, 0] },
  { pos: [0, 2.2, 11.5], look: [0, -1.4, 0] },
].map((s) => ({ pos: new THREE.Vector3(...s.pos), look: new THREE.Vector3(...s.look) }));

const panels = [...document.querySelectorAll('[data-shot]')];
const dayEl = document.getElementById('day');
const smooth = (x) => x * x * (3 - 2 * x);
function progress() {
  const mid = innerHeight / 2;
  const centers = panels.map((p) => { const r = p.getBoundingClientRect(); return r.top + r.height / 2; });
  let i = 0; while (i < centers.length - 2 && centers[i + 1] < mid) i++;
  const k = Math.min(1, Math.max(0, (mid - centers[i]) / (centers[i + 1] - centers[i])));
  const r3 = panels[3].getBoundingClientRect();
  const days = Math.min(1, Math.max(0, (innerHeight - r3.top) / (r3.height + innerHeight)));
  return { i, k: smooth(k), raw: k, days };
}

const camPos = shots[0].pos.clone(), camLook = shots[0].look.clone();
const tPos = new THREE.Vector3(), tLook = new THREE.Vector3();

function resize() {
  renderer.setSize(innerWidth, innerHeight, false);
  camera.aspect = innerWidth / innerHeight; camera.fov = innerWidth < 700 ? 52 : 35; camera.updateProjectionMatrix();
}
addEventListener('resize', resize); resize();

const clock = new THREE.Clock();
function tick() {
  const dt = Math.min(clock.getDelta(), 0.05), t = clock.elapsedTime;
  const p = progress(), a = shots[p.i], b = shots[p.i + 1];
  tPos.lerpVectors(a.pos, b.pos, p.k); tLook.lerpVectors(a.look, b.look, p.k);
  if (camera.aspect < 1) { tLook.x *= 0.15; tLook.y -= 4.6; tPos.multiplyScalar(1.5); } // Handy: Objekt mittig unter dem Text
  const e = still ? 1 : 1 - Math.pow(0.003, dt);
  camPos.lerp(tPos, e); camLook.lerp(tLook, e);
  camera.position.copy(camPos); camera.lookAt(camLook);

  const at = p.i + p.raw; // 0..4 über die ganze Seite
  // Tempo-Spuren vor allem im Hero
  const trailA = Math.max(0, 1 - at * 1.2) + Math.max(0, 1 - Math.abs(at - 4) * 1.5) * 0.6;
  trails.forEach((m) => { m.material.uniforms.uT.value = still ? 0.4 : t; m.material.uniforms.uA.value = trailA * (camera.aspect < 1 ? 0.5 : 1); m.visible = trailA > 0.01; });
  // Fundament schiebt sich in Station 2 sichtbar auseinander
  const lay = Math.max(0, 1 - Math.abs(at - 1) * 1.3);
  layers.forEach((m, i) => { m.position.y = -0.32 - i * (0.48 + lay * 0.35); });
  // Waage taucht in Station 3 auf
  const sc = Math.max(0.001, Math.min(1, 1 - Math.abs(at - 2) * 0.9));
  scale.scale.setScalar(sc); scale.rotation.y = still ? -0.5 : -0.5 + Math.sin(t * 0.6) * 0.15;
  // Sonne: sonst ruhig, in Station 4 sieben Tage
  const dayPhase = p.days * 7;
  const ang = at > 2.5 && at < 3.8 ? dayPhase * Math.PI * 2 : 0.9;
  sun.position.set(Math.cos(ang) * 8, Math.max(0.6, Math.sin(ang) * 8 + 3), 4);
  const lit = Math.max(0.15, Math.sin(ang) * 0.5 + 0.6);
  sun.intensity = 2.4 * lit;
  sun.color.setHSL(0.09, 0.6, 0.6 + lit * 0.3);
  if (dayEl) dayEl.textContent = Math.min(7, Math.floor(dayPhase) + 1);
  house.rotation.y = still ? 0.35 : 0.35 + Math.sin(t * 0.4) * 0.08;

  renderer.render(scene, camera);
  if (!still) requestAnimationFrame(tick);
}
if (still) addEventListener('scroll', () => requestAnimationFrame(tick), { passive: true });
tick();
