// Daumenkino: Scrollen ist die Zeitleiste. 24 Bilder, ein springender Ball mit Squash & Stretch.
(() => {
  const N = 24, NS = 'http://www.w3.org/2000/svg';
  const stage = document.getElementById('stage');
  if (!stage) return;
  const onion = document.getElementById('onion'), ball = document.getElementById('ball');
  const counter = document.getElementById('frame'), steps = [...document.querySelectorAll('.steps li')];
  const H = [330, 210, 110];

  // Position und Verformung für Bild f (0..N-1)
  const pose = (f) => {
    const t = f / (N - 1), s = Math.min(2, Math.floor(t * 3)), u = t * 3 - s;
    const y = 480 - H[s] * 4 * u * (1 - u);
    const edge = u < 0.08 || u > 0.92, fast = u < 0.3 || u > 0.7;
    const [sx, sy] = edge ? [1.3, 0.7] : fast ? [0.88, 1.14] : [1, 1];
    return { x: 80 + t * 840, y, sx, sy };
  };
  const tf = (p) => `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)}) scale(${p.sx} ${p.sy})`;


  const render = (f, trail) => {
    onion.replaceChildren();
    for (let k = trail; k >= 1; k--) {
      if (f - k < 0) continue;
      const g = document.createElementNS(NS, 'g'); g.setAttribute('transform', tf(pose(f - k)));
      const e = document.createElementNS(NS, 'ellipse'); e.setAttribute('cx', 0); e.setAttribute('cy', -40); e.setAttribute('rx', 40); e.setAttribute('ry', 40);
      g.style.opacity = (1 - k / (trail + 1)) * 0.5; g.append(e); onion.append(g);
    }
    ball.setAttribute('transform', tf(pose(f)));
    counter.textContent = String(f + 1).padStart(2, '0');
    const st = Math.min(3, Math.floor((f / N) * 4));
    steps.forEach((li, i) => li.classList.toggle('active', i === st));
  };

  // Ohne Bewegung: alle Bilder als Zwiebelhaut, der Ball im letzten Bild
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { render(N - 1, N - 1); return; }

  document.documentElement.classList.add('flip-on');
  const sec = document.querySelector('.flip');
  let last = -1;
  const onScroll = () => {
    const r = sec.getBoundingClientRect(), span = r.height - innerHeight;
    const p = Math.min(1, Math.max(0, -r.top / Math.max(1, span)));
    const f = Math.min(N - 1, Math.floor(p * N));
    if (f !== last) { last = f; render(f, 4); }
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
