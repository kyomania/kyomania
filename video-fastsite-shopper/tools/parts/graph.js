      // ---------------- flow graph: generated clip + captions synced to the voice ----------------
      [["#gc1", 6.4, 8.6], ["#gc2", 8.9, 10.8], ["#gc3", 11.0, 13.0], ["#gc4", 13.2, 15.0]].forEach(([s, a, b]) => {
        tl.fromTo(s, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: EX }, a);
        tl.to(s, { opacity: 0, y: -20, duration: 0.3, ease: "power2.in" }, b);
      });
      tl.fromTo("#gcap .e", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 6.1);
      tl.fromTo("#flowv", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 5.8);

