// Wasserlicht (Kaustik) als WebGL-Shader. Zeichnet nur Helligkeit; die Farbe kommt aus CSS (--color-shade).
(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const frag = `precision mediump float;uniform vec2 r;uniform float t;
  void main(){vec2 p=mod(gl_FragCoord.xy/r.y*2.4*6.2832,6.2832)-250.;vec2 i=p;float c=1.;
  for(int n=0;n<5;n++){float k=t*(1.-3.5/float(n+1));i=p+vec2(cos(k-i.x)+sin(k+i.y),sin(k-i.y)+cos(k+i.x));
  c+=1./length(vec2(p.x/(sin(i.x+k)/.005),p.y/(cos(i.y+k)/.005)));}
  c/=5.;c=1.17-pow(c,1.4);float v=pow(abs(c),8.);gl_FragColor=vec4(vec3(1.),clamp(v*1.4,0.,1.));}`;
  document.querySelectorAll('canvas.light').forEach((cv) => {
    const gl = cv.getContext('webgl', { premultipliedAlpha: false, alpha: true });
    if (!gl) return;
    const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
    const pr = gl.createProgram();
    gl.attachShader(pr, sh(gl.VERTEX_SHADER, 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}'));
    gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, frag));
    gl.linkProgram(pr); gl.useProgram(pr);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    const ur = gl.getUniformLocation(pr, 'r'), ut = gl.getUniformLocation(pr, 't');
    const size = () => { const d = Math.min(devicePixelRatio, 1.5); cv.width = cv.clientWidth * d; cv.height = cv.clientHeight * d; gl.viewport(0, 0, cv.width, cv.height); };
    const draw = (ms) => { gl.uniform2f(ur, cv.width, cv.height); gl.uniform1f(ut, 4 + ms / 4000); gl.drawArrays(gl.TRIANGLES, 0, 3); };
    size(); addEventListener('resize', () => { size(); draw(0); });
    if (still) { draw(0); return; }
    let on = false, raf = 0;
    const loop = (ms) => { draw(ms); raf = requestAnimationFrame(loop); };
    new IntersectionObserver(([e]) => { if (e.isIntersecting && !on) { on = true; raf = requestAnimationFrame(loop); } else if (!e.isIntersecting && on) { on = false; cancelAnimationFrame(raf); } }).observe(cv);
  });
})();
