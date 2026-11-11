"""fast.site Markenfilm – 4 symbolische Soft-3D-Szenen (Loop-inspiriert), Blender/Cycles.

Aufruf:
  python brandfilm.py still <scene 1-4> <out.png> [samples] [scale%] [t]
  python brandfilm.py anim  <scene 1-4> <outdir>  [samples] [scale%] [fps]
Hintergrund wird transparent gerendert (Verlauf + Typo kommen in HyperFrames).
"""
import bpy, math, sys, os, time, addon_utils
from mathutils import Vector, Euler

MODE, SCENE, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
SAMPLES = int(sys.argv[4]) if len(sys.argv) > 4 else 32
SCALE = int(sys.argv[5]) if len(sys.argv) > 5 else 50
EXTRA = float(sys.argv[6]) if len(sys.argv) > 6 else None
DUR = 7.0  # Sekunden pro Szene

addon_utils.enable("cycles", default_set=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True; sc.cycles.max_bounces = 12; sc.cycles.transmission_bounces = 12; sc.cycles.transparent_max_bounces = 16
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = SCALE
sc.render.film_transparent = True
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"

world = bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
bgn = world.node_tree.nodes["Background"]; bgn.inputs[0].default_value = (0.74, 0.73, 1.0, 1); bgn.inputs[1].default_value = 0.85

def light(name, loc, rot, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.color = color; d.size = size
    o = bpy.data.objects.new(name, d); o.location = loc; o.rotation_euler = [math.radians(a) for a in rot]; sc.collection.objects.link(o)
light("Key", (4, -6, 9), (35, 0, 25), 2000, 6, (1.0, 0.97, 0.95))
light("Fill", (-7, -3, 2), (80, 0, -70), 500, 10, (0.75, 0.8, 1.0))
light("Rim", (0, 6, 5), (-50, 0, 180), 900, 6, (1.0, 0.8, 0.95))

def srgb(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

def mat(name, hexcol, rough=0.35, coat=0.0, film=0.0, trans=0.0, ior=1.45, sheen=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    col = srgb(hexcol); b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.06
    b.inputs["Thin Film Thickness"].default_value = film; b.inputs["Thin Film IOR"].default_value = 1.4
    b.inputs["Transmission Weight"].default_value = trans; b.inputs["IOR"].default_value = ior
    b.inputs["Sheen Weight"].default_value = sheen
    if emit: b.inputs["Emission Color"].default_value = (*col, 1); b.inputs["Emission Strength"].default_value = emit
    return m

CLAY = lambda h: mat("clay" + h, h, rough=0.5, sheen=0.6, film=300)
GLOSS = lambda h: mat("gloss" + h, h, rough=0.18, coat=1.0, film=220)
GLASS = mat("glass", "#eef2ff", rough=0.02, trans=1.0, ior=1.35, film=480)

def obj_of(op, **kw):
    op(**kw); o = bpy.context.object; bpy.ops.object.shade_smooth(); return o

def rounded_box(size, bevel, m, loc=(0, 0, 0)):
    o = obj_of(bpy.ops.mesh.primitive_cube_add, location=loc); o.scale = [s / 2 for s in size]
    bpy.ops.object.transform_apply(scale=True)
    bv = o.modifiers.new("b", "BEVEL"); bv.width = bevel; bv.segments = 8; bv.limit_method = "NONE"
    o.data.materials.append(m); return o

def capsule(length, radius, m, flat=0.55):
    o = obj_of(bpy.ops.mesh.primitive_uv_sphere_add, segments=64, ring_count=33, radius=radius)
    for v in o.data.vertices:
        v.co.z += length / 2 if v.co.z > 1e-6 else (-length / 2 if v.co.z < -1e-6 else 0)
        v.co.y *= flat
    o.modifiers.new("s", "SUBSURF").levels = 1; o.data.materials.append(m); return o

def sphere(r, m, loc=(0, 0, 0)):
    o = obj_of(bpy.ops.mesh.primitive_uv_sphere_add, segments=64, ring_count=32, radius=r, location=loc); o.data.materials.append(m); return o

def torus(R, r, m, loc=(0, 0, 0), rot=(0, 0, 0)):
    o = obj_of(bpy.ops.mesh.primitive_torus_add, major_radius=R, minor_radius=r, major_segments=96, minor_segments=32, location=loc)
    o.rotation_euler = [math.radians(a) for a in rot]; o.data.materials.append(m); return o

def disc(R, h, m, loc=(0, 0, 0)):
    o = obj_of(bpy.ops.mesh.primitive_cylinder_add, vertices=96, radius=R, depth=h, location=loc)
    bv = o.modifiers.new("b", "BEVEL"); bv.width = min(h * 0.45, 0.3); bv.segments = 8; bv.limit_method = "ANGLE"
    o.data.materials.append(m); return o

def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); e.location = loc; sc.collection.objects.link(e); return e

def parent(child, par):
    child.parent = par

def page(w, h, bend, m):
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object
    o.scale = (w, h, 1); bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=40); bpy.ops.object.mode_set(mode="OBJECT")
    o.rotation_euler = (math.radians(90), 0, 0); bpy.ops.object.transform_apply(rotation=True)
    md = o.modifiers.new("Bend", "SIMPLE_DEFORM"); md.deform_method = "BEND"; md.deform_axis = "Z"; md.angle = math.radians(bend)
    o.modifiers.new("Solid", "SOLIDIFY").thickness = 0.04
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o

PASTELS = ["#b8a6ff", "#9fc3ff", "#ffb3e1", "#a9e7ff", "#c9b5ff", "#ffc9ea", "#b3c7ff", "#d6c2ff"]
def ribbon(n=13, radius=4.6, height=2.0, center=(0, 0, 0)):
    g = empty("Ribbon", center)
    for i in range(n):
        t = i / (n - 1)
        m = mat(f"sheet{i}", PASTELS[i % 8], rough=0.22, coat=1.0, film=320 + (i * 37) % 360)
        p = page(1.7, 2.5, 70 + 40 * math.sin(t * math.pi), m)
        x = -radius + 2 * radius * t; z = height * math.sin(t * math.pi * 1.3) - 0.4; y = 1.6 - 1.0 * t
        p.location = (x, y, z); p.rotation_euler = (math.radians(12 + 10 * math.sin(t * 6)), math.radians(-70 + 140 * t), math.radians(25 * math.sin(t * math.pi * 2)))
        parent(p, g)
    return g

def logo(scale=1.0):
    g = empty("Logo"); L, R = 2.0, 0.42; off = L / 2 * math.sin(math.radians(45)); parts = []
    for col, side, y in (("#3e71b6", -1, 1.0), ("#0c9958", 1, 1.0), ("#df482b", -1, -0.35), ("#fbb419", 1, -0.35)):
        c = capsule(L, R, GLOSS(col)); c.rotation_euler = (0, math.radians(-side * 45), 0)
        c.location = (side * off, 0, y - off); parent(c, g); parts.append(c)
    g.scale = (scale, scale, scale); return g, parts

# ---------- Kamera ----------
cd = bpy.data.cameras.new("Cam"); cd.lens = 55; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.4
cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
focus = empty("Focus"); cd.dof.focus_object = focus
def camera(t, base=(0, -26, 0.6), orbit=6.0, push=1.5):
    a = math.radians(-orbit / 2 + orbit * t)
    cam.location = (base[1] * -math.sin(a) + base[0], base[1] * math.cos(a) + push * t, base[2])
    d = Vector((0, 0, base[2] - 0.6)) - cam.location; cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

ease = lambda x: x * x * (3 - 2 * x)
def seg(t, a, b):
    return ease(max(0.0, min(1.0, (t - a) / (b - a))))

# =================== Szenen ===================
ANIM = []  # Liste von f(t) für t in [0,1]

def house(scale=1.0):
    g = empty("House")
    body = rounded_box((2.6, 2.2, 1.9), 0.18, CLAY("#f7f1ff"), (0, 0, 0.95)); parent(body, g)
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1.9, depth=2.4); roof = bpy.context.object
    roof.rotation_euler = (math.radians(90), 0, 0); roof.location = (0, 0, 2.38); roof.scale = (0.82, 0.66, 1.0)
    bv = roof.modifiers.new("b", "BEVEL"); bv.width = 0.22; bv.segments = 10; bv.limit_method = "NONE"
    roof.data.materials.append(GLOSS("#7f8cff")); bpy.ops.object.shade_smooth(); parent(roof, g)
    win = rounded_box((0.62, 0.1, 0.62), 0.08, mat("win", "#ffcf7a", rough=0.3, emit=6.0), (-0.65, -1.12, 1.15)); parent(win, g)
    win2 = rounded_box((0.62, 0.1, 0.62), 0.08, mat("win2", "#ffcf7a", rough=0.3, emit=6.0), (0.65, -1.12, 1.15)); parent(win2, g)
    door = rounded_box((0.55, 0.1, 0.9), 0.1, GLOSS("#ff9ccc"), (0, -1.12, 0.45)); door.location.x = 0; parent(door, g)
    chim = rounded_box((0.35, 0.35, 0.8), 0.08, CLAY("#ffb5dd"), (0.8, 0.2, 3.0)); parent(chim, g)
    g.scale = (scale,) * 3; return g

def island(loc=(0, 0, 0)):
    g = empty("Island", loc)
    d = disc(3.2, 0.7, CLAY("#c9b5ff"), (0, 0, -0.35)); parent(d, g)
    d2 = disc(2.5, 0.5, CLAY("#a9c8ff"), (0, 0, -0.9)); parent(d2, g)
    for x, y, r in ((-2.0, -1.2, 0.35), (2.2, -0.8, 0.28), (1.6, 1.4, 0.4), (-1.4, 1.5, 0.3)):
        s = sphere(r, CLAY("#ffffff"), (x, y, r * 0.6)); parent(s, g)
    return g

if SCENE == 1:  # Zuhause im Netz
    isl = island((0, 0, -3.2)); h = house(1.0); h.location = (0, 0, -3.2)
    cloud = [sphere(r, CLAY("#ffffff"), loc) for r, loc in ((0.7, (-3.4, 1.5, 3.4)), (0.5, (-2.7, 1.5, 3.3)), (0.55, (-3.9, 1.6, 3.2)))]
    b1 = sphere(0.9, CLAY("#c6b3ff"), (3.4, 2.0, 3.6)); b2 = torus(0.6, 0.24, GLASS, (-3.1, -1.0, -6.4), (60, 20, 0)); b3 = sphere(0.4, CLAY("#9fd2ff"), (3.6, -1.5, -5.6))
    focus.location = (0, 0, -1.8)
    def a1(t):
        k = seg(t, 0.0, 0.35); isl.location.z = -3.2 - 6 * (1 - k); h.location.z = -3.2 - 6 * (1 - seg(t, 0.08, 0.45))
        h.rotation_euler.z = math.radians(-25 + 30 * t); isl.rotation_euler.z = h.rotation_euler.z
        for i, c in enumerate(cloud): c.location.x = -3.4 + 0.6 * t + (i - 1) * 0.6
        b1.location.z = 3.6 + 0.3 * math.sin(t * 6.28); b3.location.z = -5.6 + 0.25 * math.sin(t * 6.28 + 1)
        b2.rotation_euler.z = t * 3.0
        camera(t, base=(0, -26, 0.4), orbit=8, push=2.0)
    ANIM.append(a1)

elif SCENE == 2:  # Behalte, was funktioniert – Glaskuppel schützt
    isl = island((0, 0, -2.6)); h = house(0.85); h.location = (0, 0, -2.6)
    dome = sphere(3.0, GLASS, (0, 0, -1.6)); dome.scale = (1, 1, 0.92)
    rib = ribbon(13, 5.2, 2.2, (0, 1.5, 1.6))
    b1 = sphere(0.45, CLAY("#ffb3e1"), (-3.8, -1.5, 3.6)); b2 = torus(0.55, 0.22, CLAY("#9fc3ff"), (3.5, -1.5, -5.8), (50, 10, 0))
    focus.location = (0, 0, -1.2)
    def a2(t):
        dome.scale = (1, 1, 0.92) if t > 0.3 else tuple(v * (0.6 + 0.4 * seg(t, 0.0, 0.3)) for v in (1, 1, 0.92))
        rib.rotation_euler.z = math.radians(-35 + 70 * t); rib.location.z = 1.6 + 0.3 * math.sin(t * 6.28)
        h.rotation_euler.z = math.radians(10 * math.sin(t * 3.14)); isl.rotation_euler.z = h.rotation_euler.z
        b1.location.z = 3.6 + 0.3 * math.sin(t * 6.28); b2.rotation_euler.z = t * 4
        camera(t, base=(0, -26, 0.6), orbit=-10, push=2.5)
    ANIM.append(a2)

elif SCENE == 3:  # Performance statt Versprechen – Waage
    base = disc(1.6, 0.5, CLAY("#c9b5ff"), (0, 0, -6.0)); pole = capsule(6.2, 0.25, GLOSS("#f2eeff"), flat=1.0); pole.location = (0, 0, -2.8)
    pivot = empty("Pivot", (0, 0, 0.4)); beam = capsule(7.6, 0.22, GLOSS("#f2eeff"), flat=1.0); beam.rotation_euler = (0, math.radians(90), 0); parent(beam, pivot)
    knob = sphere(0.42, GLOSS("#7f8cff"), (0, 0, 0.4))
    pans = []
    for side in (-1, 1):
        hang = empty(f"Hang{side}", (side * 3.6, 0, 0)); parent(hang, pivot)
        rod = capsule(2.0, 0.05, GLOSS("#ffffff"), flat=1.0); rod.location = (0, 0, -1.0); parent(rod, hang)
        pan = disc(1.35, 0.28, GLOSS("#f7f1ff" if side < 0 else "#ffe6f4"), (0, 0, -2.1)); parent(pan, hang)
        pans.append(hang)
    cloud = [sphere(r, CLAY("#ffffff"), (x, 0, z)) for r, x, z in ((0.55, -0.3, -1.4), (0.42, 0.35, -1.5), (0.38, 0.0, -1.1))]
    for c in cloud: parent(c, pans[0])
    lg, parts = logo(0.55); lg.location = (0, 0, -1.25); parent(lg, pans[1])
    deco = [sphere(0.5, CLAY("#9fd2ff"), (-3.6, 1.5, 4.6)), torus(0.6, 0.24, GLASS, (3.4, -1.0, 4.4), (50, 30, 0))]
    focus.location = (0, 0, -1.0)
    def a3(t):
        tilt = -math.radians(14) * seg(t, 0.35, 0.75) + math.radians(3) * math.sin(t * 9) * (1 - seg(t, 0.75, 1.0))
        pivot.rotation_euler = (0, -tilt, 0)
        for hg in pans: hg.rotation_euler = (0, tilt, 0)  # Schalen bleiben waagerecht
        lg.rotation_euler.z = math.radians(-20 + 40 * t)
        deco[0].location.z = 4.6 + 0.3 * math.sin(t * 6.28); deco[1].rotation_euler.z = t * 3
        camera(t, base=(0, -27, 0.2), orbit=10, push=2.0)
    ANIM.append(a3)

else:  # Szene 4 – Logo setzt sich zusammen, Band dahinter
    lg, parts = logo(1.25); lg.location = (0, 0, 0.6)
    homes = [(p.location.copy(), p.rotation_euler.copy()) for p in parts]
    starts = [(-6, -4, 7), (6, -3, 8), (-7, -2, -6), (7, -5, -7)]
    rib = ribbon(13, 4.8, 2.0, (0, 3.0, -2.2))
    g1 = torus(0.75, 0.26, GLASS, (-3.2, -1.5, -5.0), (30, -40, 0)); g2 = sphere(0.9, CLAY("#c6b3ff"), (-3.5, 1.5, 4.6)); g3 = torus(0.6, 0.24, CLAY("#ffb5dd"), (3.4, -1, -5.6), (60, 20, 0))
    focus.location = (0, 0, 0.2)
    def a4(t):
        for i, p in enumerate(parts):
            k = seg(t, 0.05 + i * 0.08, 0.45 + i * 0.08); hl, hr = homes[i]; s = Vector(starts[i]) / lg.scale.x
            p.location = s.lerp(hl, k); p.rotation_euler = Euler((hr.x + (1 - k) * 2.5, hr.y + (1 - k) * 3.0, hr.z), "XYZ")
        lg.rotation_euler = (math.radians(8), math.radians(-25 + 35 * seg(t, 0.5, 1.0)), 0)
        rib.rotation_euler.z = math.radians(20 - 40 * t)
        g2.location.z = 4.6 + 0.3 * math.sin(t * 6.28); g1.rotation_euler.z = t * 3
        camera(t, base=(0, -24, 0.6), orbit=-8, push=3.0)
    ANIM.append(a4)

# =================== Rendern ===================
if MODE == "still":
    ANIM[0](EXTRA if EXTRA is not None else 0.7); sc.render.filepath = OUT
    t0 = time.time(); bpy.ops.render.render(write_still=True); print("RENDER_SECONDS", round(time.time() - t0, 1))
else:
    fps = int(EXTRA) if EXTRA else 24; n = int(DUR * fps); os.makedirs(OUT, exist_ok=True)
    for f in range(n):
        path = os.path.join(OUT, f"f{f:04d}.png")
        if os.path.exists(path): continue  # fortsetzbar
        ANIM[0](f / (n - 1)); sc.render.filepath = path
        t0 = time.time(); bpy.ops.render.render(write_still=True)
        print(f"FRAME {f + 1}/{n} {round(time.time() - t0, 1)}s", flush=True)
    print("DONE")
