      function deskSite(loading) {
        return `<div class="site"><div class="bar"><i></i><i></i><i></i><div class="url">dein-shop.de</div>${loading ? '<div class="prog2"></div>' : ""}</div>
          <div class="nav"><div class="brand">ATELIER</div><span>Neu</span><span>Damen</span><span>Herren</span><span>Accessoires</span><span style="color:#b0442a">Sale</span><div class="sp"></div><span>Suche</span><span>Konto</span><span>Warenkorb (0)</span></div>
          <div class="hero"><img src="assets/img/hero.jpg"/><div class="ht"><div class="hk">Herbst / Winter 26</div><div class="hh">Die neue<br/>Kollektion</div><div class="hb">Jetzt entdecken</div></div></div>
          <div class="prods">${P.map((p) => `<div class="pc"><div class="im"><img src="assets/img/${p[2]}.jpg"/></div><div class="n">${p[0]}</div><div class="p">${p[1]}</div></div>`).join("")}</div>
          ${loading ? `<div class="skel"><div class="sk" style="left:34px;top:14px;width:140px;height:28px"></div><div class="sk" style="left:220px;top:18px;width:420px;height:20px"></div>
            <div class="sk" style="left:0;top:58px;width:1084px;height:330px;border-radius:0"></div>
            ${[0, 1, 2, 3].map((i) => `<div class="sk" style="left:${34 + i * 258}px;top:410px;width:240px;height:150px"></div><div class="sk" style="left:${34 + i * 258}px;top:572px;width:160px;height:14px"></div>`).join("")}
            <div class="ring" style="left:507px;top:186px"></div></div>` : ""}</div>`;
      }
      function phoneSite(loading) {
        return `<div class="msite"><div class="mstat"><span>9:41</span><span>5G</span></div><div class="mnav"><div class="brand">ATELIER</div></div>
          <div class="mhero"><img src="assets/img/hero.jpg"/><div class="ht"><div class="hk">Herbst / Winter 26</div><div class="hh">Die neue<br/>Kollektion</div></div></div>
          <div class="mgrid">${P.map((p) => `<div><div class="im"><img src="assets/img/${p[2]}.jpg"/></div><div class="n">${p[0]}</div><div class="p">${p[1]}</div></div>`).join("")}</div>
          ${loading ? `<div class="skel" style="top:52px"><div class="sk" style="left:100px;top:12px;width:112px;height:22px"></div><div class="sk" style="left:0;top:46px;width:312px;height:300px;border-radius:0"></div>
            ${[0, 1, 2, 3].map((i) => `<div class="sk" style="left:${14 + (i % 2) * 147}px;top:${360 + Math.floor(i / 2) * 170}px;width:137px;height:120px"></div>`).join("")}
            <div class="ring" style="left:121px;top:161px"></div></div>` : ""}</div>`;
      }
      function laptop(parent, x, y, s, loading) { const d = mk(parent, "laptop", { left: x + "px", top: y + "px" }, `<div class="lid"><div class="screen" data-layout-ignore>${deskSite(loading)}</div></div><div class="base"></div>`); gsap.set(d, { scale: s }); d.dataset.base = s; return d; }
      function phone(parent, x, y, s, loading) { const d = mk(parent, "phone", { left: x + "px", top: y + "px" }, `<div class="pscreen" data-layout-ignore>${phoneSite(loading)}<div class="island"></div></div>`); gsap.set(d, { scale: s }); d.dataset.base = s; return d; }
