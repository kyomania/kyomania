      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      const $ = (s) => document.querySelector(s), $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
      let seed = 11; const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
      const R = (a, b) => a + (b - a) * rnd();
      const FPS = 12;                      // Stop-Motion-Takt
      // Ease, der in 12-fps-Schritten springt
      const step = (dur, base = "power3.out") => { const e = gsap.parseEase(base), n = Math.max(1, Math.round(dur * FPS)); return (p) => e(Math.min(1, Math.floor(p * n + 1e-6) / n)); };

      // gerissene Kanten
      $$(".torn").forEach((el) => {
        const w = parseFloat(el.style.width), h = parseFloat(el.style.height), pts = [], s = 14, j = 9;
        for (let x = 0; x <= w; x += s) pts.push(`${x}px ${rnd() * j}px`);
        for (let y = 0; y <= h; y += s) pts.push(`${w - rnd() * 4}px ${y}px`);
        for (let x = w; x >= 0; x -= s) pts.push(`${x}px ${h - rnd() * j}px`);
        for (let y = h; y >= 0; y -= s) pts.push(`${rnd() * 4}px ${y}px`);
        el.style.clipPath = `polygon(${pts.join(",")})`;
      });
      $$(".tape").forEach((el) => {
        const w = parseFloat(el.style.width), h = 74, pts = [];
        for (let y = 0; y <= h; y += 8) pts.push(`${rnd() * 10}px ${y}px`);
        for (let y = h; y >= 0; y -= 8) pts.push(`${w - rnd() * 10}px ${y}px`);
        el.style.clipPath = `polygon(${pts.join(",")})`;
      });

      // Szene-Übergang: gerissene Kante wischt von unten nach oben (12 fps)
      function ripIn(sel, t, d = 0.42) {
        const edge = Array.from({ length: 41 }, (_, i) => [i * 27, R(-30, 30)]);
        const o = { y: 1980 };
        const upd = () => { const pts = ["0px 1920px", "1080px 1920px"].concat(edge.slice().reverse().map(([x, dy]) => `${x}px ${o.y + dy}px`));
          $(sel).style.clipPath = `polygon(${pts.join(",")})`; };
        tl.fromTo(o, { y: 1980 }, { y: -60, duration: d, ease: step(d, "power2.inOut"), onUpdate: upd }, t);
        tl.set(sel, { clipPath: "none" }, t + d + 0.01);
      }

      // Auftritte, gesteuert über data-t / data-fx
      $$("[data-fx]").forEach((el) => {
        const t = parseFloat(el.dataset.t), fx = el.dataset.fx;
        tl.set(el, { autoAlpha: 0 }, 0);
        tl.set(el, { autoAlpha: 1 }, t);
        const d = { drop: 0.42, slam: 0.33, right: 0.42, left: 0.42, up: 0.42, tape: 0.17, pop: 0.25, stamp: 0.25, stick: 0.25, type: 0.5 }[fx] || 0.4;
        const e = step(d, fx === "slam" || fx === "stamp" ? "expo.out" : "back.out(1.6)");
        if (fx === "drop") tl.from(el, { y: -900, duration: d, ease: e }, t);
        if (fx === "left") tl.from(el, { x: -1300, duration: d, ease: e }, t);
        if (fx === "right") tl.from(el, { x: 1300, duration: d, ease: e }, t);
        if (fx === "up") tl.from(el, { y: 900, duration: d, ease: e }, t);
        if (fx === "slam") tl.from(el, { scale: 2.4, duration: d, ease: e }, t);
        if (fx === "stamp") tl.from(el, { scale: 3, rotation: "+=14", duration: d, ease: e }, t);
        if (fx === "tape") tl.from(el, { scale: 1.7, duration: d, ease: e }, t);
        if (fx === "pop" || fx === "stick") tl.from(el, { scale: 0, rotation: "-=20", duration: d, ease: e }, t);
        if (fx === "type") { const kids = Array.from(el.children); if (kids.length) kids.forEach((k, i) => tl.from(k, { autoAlpha: 0, duration: 0.01 }, t + i * (1 / FPS) * 1.5)); }
      });
      // Schwärzungsbalken ziehen auf
      $$(".redact").forEach((r) => { const t = parseFloat(r.dataset.t);
        $$("b", r).forEach((b, i) => tl.from(b, { scaleX: 0, transformOrigin: "0 50%", duration: 0.25, ease: step(0.25, "power2.out") }, t + i * 0.12)); });

      // Boil: alles wackelt leicht im 12-fps-Takt (über CSS-Variablen, unabhängig von den Transforms)
      $$(".scene").forEach((sc) => {
        const s0 = parseFloat(sc.dataset.start), s1 = s0 + parseFloat(sc.dataset.duration);
        const els = $$(".boil", sc);
        for (let f = Math.ceil(s0 * FPS); f < s1 * FPS; f++) {
          const tt = f / FPS;
          els.forEach((el) => tl.set(el, { "--bx": R(-2.5, 2.5).toFixed(1) + "px", "--by": R(-2.5, 2.5).toFixed(1) + "px", "--br": R(-0.5, 0.5).toFixed(2) + "deg" }, tt));
        }
      });
      for (let f = 0; f < 25 * FPS; f++) tl.set("#noise", { backgroundPosition: `${Math.round(R(0, 300))}px ${Math.round(R(0, 300))}px` }, f / FPS);

      // Szenen-Übergänge
      [["#s2", 3.05], ["#s3", 5.5], ["#s4", 9.85], ["#s5", 14.6], ["#s6", 19.8]].forEach(([s, t]) => ripIn(s, t));

      // Zähler
      const c1 = { v: 0 }; tl.fromTo(c1, { v: 0 }, { v: 4.8, duration: 2.0, ease: step(2.0, "power1.in"), onUpdate: () => ($("#lcp1").textContent = "LCP · " + c1.v.toFixed(1).replace(".", ",") + " s") }, 0.3);
      const c2 = { v: 4.8 }; tl.fromTo(c2, { v: 4.8 }, { v: 0.4, duration: 0.6, ease: step(0.6, "expo.out"), onUpdate: () => ($("#lcp2").textContent = "LCP " + c2.v.toFixed(1).replace(".", ",") + " s") }, 4.95);
      const c3 = { v: 0 }; tl.fromTo(c3, { v: 0 }, { v: 35, duration: 0.5, ease: step(0.5, "power1.in"), onUpdate: () => ($("#big35").textContent = "−" + Math.round(c3.v) + "%") }, 12.3);
      // Blitz-Akzente
      [3.95, 12.8, 22.05].forEach((t) => tl.fromTo("#flash", { opacity: 0.5 }, { opacity: 0, duration: 0.17, ease: step(0.17, "none"), immediateRender: false }, t));

      window.__timelines["main"] = tl;
      tl.seek(0);
