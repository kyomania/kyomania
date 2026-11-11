"""3D-Buch 'Die Lizenz zum Erfolg' – Blender/Cycles, transparenter Hintergrund.
python book.py still <out.png> [samples] [scale%] [t]
python book.py anim  <outdir>  [samples] [scale%] [fps]
"""
import bpy, math, sys, os, time, addon_utils
from mathutils import Vector

MODE, OUT = sys.argv[1], sys.argv[2]
SHOT = os.environ.get("SHOT", "hero")
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 48
SCALE = int(sys.argv[4]) if len(sys.argv) > 4 else 50
EXTRA = float(sys.argv[5]) if len(sys.argv) > 5 else None
DUR = 7.3 if os.environ.get("SHOT", "hero") == "hero" else float(os.environ.get("SHOT_DUR", "3.5"))
HERE = os.path.dirname(os.path.abspath(__file__))

addon_utils.enable("cycles", default_set=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = SCALE
sc.render.film_transparent = True
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - High Contrast"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.02, 0.02, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.2

def tex_mat(name, img, rough=0.28, coat=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(os.path.join(HERE, img)); t.extension = "EXTEND"
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.08
    return m

# Taschenbuch 12,5 x 19,9 x 1,6 (Einheiten = dm*0.1 -> skaliert)
Wd, Hd, Dd = 2.5, 3.98, 0.32
bpy.ops.mesh.primitive_cube_add(size=1); book = bpy.context.object; book.name = "Book"
book.scale = (Wd, Dd, Hd); bpy.ops.object.transform_apply(scale=True)
bv = book.modifiers.new("b", "BEVEL"); bv.width = 0.012; bv.segments = 3
mats = {"front": tex_mat("Front", "cover_front.png"), "back": tex_mat("Back", "back.png"), "spine": tex_mat("Spine", "spine.png"),
        "pages": tex_mat("Pages", "pages.png", rough=0.8, coat=0.0)}
for k in ("front", "back", "spine", "pages"): book.data.materials.append(mats[k])
# Faces zuordnen + UVs pro Fläche 0..1
me = book.data; uv = me.uv_layers.active.data
for poly in me.polygons:
    n = poly.normal
    if n.y < -0.9: idx = 0          # Vorderseite (zur Kamera, -Y)
    elif n.y > 0.9: idx = 1         # Rückseite
    elif n.x < -0.9: idx = 2        # Rücken links
    else: idx = 3                   # Schnittkanten
    poly.material_index = idx
    vs = [me.vertices[v].co for v in poly.vertices]
    for li, vi in zip(poly.loop_indices, poly.vertices):
        co = me.vertices[vi].co
        if idx == 0: u, v = (co.x + Wd / 2) / Wd, (co.z + Hd / 2) / Hd
        elif idx == 1: u, v = 1 - (co.x + Wd / 2) / Wd, (co.z + Hd / 2) / Hd
        elif idx == 2: u, v = 1 - (co.y + Dd / 2) / Dd, (co.z + Hd / 2) / Hd
        else: u, v = (co.y + Dd / 2) / Dd, (co.z + Hd / 2) / Hd
        uv[li].uv = (u, v)
bpy.ops.object.shade_flat()
pivot = bpy.data.objects.new("Pivot", None); sc.collection.objects.link(pivot); book.parent = pivot

def area(name, loc, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.size = size; d.color = color
    o = bpy.data.objects.new(name, d); o.location = loc; sc.collection.objects.link(o)
    o.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler(); return o
key = area("Key", (3.5, -6, 3), 700, 3)
rim = area("Rim", (-4, 3, 2), 900, 2.5, (1.0, 0.85, 0.4))      # gelbes Kantenlicht
top = area("Top", (0, -1, 7), 300, 4)
sweep = area("Sweep", (-6, -4, 0), 0, 0.6)                       # wandernder Glanzstreifen

cd = bpy.data.cameras.new("C"); cd.lens = 50
cam = bpy.data.objects.new("C", cd); cam.location = (0, -9.6, 0.3); sc.collection.objects.link(cam); sc.camera = cam
cam.rotation_euler = (Vector((0, 0, 0)) - cam.location).to_track_quat("-Z", "Y").to_euler()

ease_out = lambda x: 1 - (1 - x) ** 4
clamp = lambda x: max(0.0, min(1.0, x))
def anim(t):
    s = DUR * t
    k = 1 - (1 - clamp(s / 1.6)) ** 3                                  # Einflug mit Drehung
    pivot.location = Vector((0, 22 * (1 - k), -1.5 * (1 - k)))
    spin = (1 - k) * math.radians(540)
    drift = math.radians(28 - 16 * clamp((s - 1.6) / 5.7))
    pivot.rotation_euler = (math.radians(4 + 6 * (1 - k)), 0, spin + drift)
    pivot.location.z += 0.08 * math.sin(s * 1.6) * k
    # Glanzstreifen fährt einmal über das Cover
    g = clamp((s - 1.8) / 1.6); sweep.data.energy = 900 * math.sin(math.pi * g)
    sweep.location = (-6 + 12 * g, -4, 0.5)
    sweep.rotation_euler = (Vector((0, 0, 0)) - sweep.location).to_track_quat("-Z", "Y").to_euler()

def look(cam_obj, target):
    cam_obj.rotation_euler = (Vector(target) - cam_obj.location).to_track_quat("-Z", "Y").to_euler()
if SHOT != "hero":
    cd.lens = 85; cd.dof.use_dof = True; cd.dof.aperture_fstop = 1.6
    foc = bpy.data.objects.new("F", None); sc.collection.objects.link(foc); cd.dof.focus_object = foc
    sweep.data.size = 1.2
    def anim(t):
        s = DUR * t; e = t * t * (3 - 2 * t)
        pivot.location = (0, 0, 0)
        if SHOT == "eye":       # Fahrt über das Auge auf dem Cover
            pivot.rotation_euler = (0, 0, math.radians(-8))
            ex, ez = -0.62, 0.42
            cam.location = (ex - 0.55 + 0.75 * e, -2.0 + 0.25 * e, ez + 0.06 - 0.12 * e)
            look(cam, (ex - 0.15 + 0.45 * e, 0, ez)); foc.location = (ex - 0.1 + 0.45 * e, -0.16, ez)
            g = e; sweep.location = (-3 + 6 * g, -3, 1.0); sweep.data.energy = 500
            look(sweep, (0, 0, 0))
        elif SHOT == "spine":   # Kamera gleitet am Rücken entlang
            ang = math.radians(78); pivot.rotation_euler = (0, 0, ang)
            c = Vector((-Wd / 2, 0, 0)); c.rotate(pivot.rotation_euler); nrm = Vector((-1, 0, 0)); nrm.rotate(pivot.rotation_euler)
            side = Vector((-nrm.y, nrm.x, 0))
            cz = -1.5 + 2.6 * e
            cam.location = c + nrm * 1.75 + side * 0.7 + Vector((0, 0, cz - 0.45))
            look(cam, c + Vector((0, 0, cz + 0.15))); foc.location = c + nrm * 0.02 + Vector((0, 0, cz + 0.1))
            key.data.energy = 80; top.data.energy = 0
            sweep.location = c + nrm * 3.0 - side * 1.5 + Vector((0, 0, cz + 1.0)); sweep.data.energy = 120; look(sweep, c + Vector((0, 0, cz)))
        else:                   # Makro über den gelben Titel
            pivot.rotation_euler = (0, 0, math.radians(10))
            tx = 0.5; tz = -0.75 + 1.5 * e
            cam.location = (tx - 0.35 + 0.2 * e, -1.9, tz - 0.25)
            look(cam, (tx, 0, tz)); foc.location = (tx, -0.16, tz)
            key.data.energy = 350
            sweep.location = (-2.5 + 5 * e, -3, tz + 0.8); sweep.data.energy = 140; look(sweep, (tx, 0, tz))

if MODE == "still":
    anim(EXTRA if EXTRA is not None else 0.5); sc.render.filepath = OUT
    t0 = time.time(); bpy.ops.render.render(write_still=True); print("RENDER_SECONDS", round(time.time() - t0, 1))
else:
    fps = int(EXTRA) if EXTRA else 24; n = int(DUR * fps); os.makedirs(OUT, exist_ok=True)
    for f in range(n):
        p = os.path.join(OUT, f"f{f:04d}.png")
        if os.path.exists(p): continue
        anim(f / (n - 1)); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        print(f"FRAME {f + 1}/{n}", flush=True)
    print("DONE")
