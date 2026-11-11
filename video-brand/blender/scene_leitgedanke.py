"""fast.site Markenfilm – Szene 'Behalte, was funktioniert' (Loop-inspiriertes Soft-3D).
Aufruf: python scene_leitgedanke.py <out.png> [samples] [scale%] [frame]
"""
import bpy, math, sys, os, time, addon_utils

OUT = sys.argv[1]
SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 64
SCALE = int(sys.argv[3]) if len(sys.argv) > 3 else 100
FRAME = int(sys.argv[4]) if len(sys.argv) > 4 else 1
HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "..", "3d", "site_hero.png")

addon_utils.enable("cycles", default_set=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6; sc.cycles.transmission_bounces = 6
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = SCALE
sc.render.film_transparent = True
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.fps = 30; sc.frame_start, sc.frame_end = 1, 150; sc.frame_set(FRAME)

# ---------- Welt: Pastell-Verlauf als Hintergrund + weiches Licht ----------
world = bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
nt = world.node_tree; nt.nodes.clear()
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB"); bg = nt.nodes.new("ShaderNodeBackground"); out = nt.nodes.new("ShaderNodeOutputWorld")
ramp.color_ramp.elements[0].color = (0.62, 0.66, 0.98, 1); ramp.color_ramp.elements[1].color = (0.80, 0.72, 0.98, 1)
e = ramp.color_ramp.elements.new(0.55); e.color = (0.55, 0.74, 0.97, 1)
bg.inputs[0].default_value = (0.72, 0.72, 1.0, 1); bg.inputs[1].default_value = 0.8; nt.links.new(bg.outputs[0], out.inputs[0])

def light(name, kind, loc, rot, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, kind); d.energy = energy; d.color = color
    if kind == "AREA": d.size = size
    o = bpy.data.objects.new(name, d); o.location = loc; o.rotation_euler = [math.radians(a) for a in rot]; sc.collection.objects.link(o)
light("Key", "AREA", (4, -6, 9), (35, 0, 25), 2000, 6, (1.0, 0.97, 0.95))
light("Fill", "AREA", (-7, -3, 2), (80, 0, -70), 500, 10, (0.75, 0.8, 1.0))
light("Rim", "AREA", (0, 6, 5), (-50, 0, 180), 900, 6, (1.0, 0.8, 0.95))

# ---------- Materialien ----------
def mat_principled(name, color, rough=0.3, coat=0.0, film=0.0, trans=0.0, ior=1.45, sheen=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.05
    b.inputs["Thin Film Thickness"].default_value = film; b.inputs["Thin Film IOR"].default_value = 1.4
    b.inputs["Transmission Weight"].default_value = trans; b.inputs["IOR"].default_value = ior
    b.inputs["Sheen Weight"].default_value = sheen; b.inputs["Alpha"].default_value = alpha
    return m

def srgb(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

# ---------- Kamera (Hochformat) ----------
cd = bpy.data.cameras.new("Cam"); cd.lens = 55; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2
cam = bpy.data.objects.new("Cam", cd); cam.location = (0, -26, 1.2); cam.rotation_euler = (math.radians(88), 0, 0)
sc.collection.objects.link(cam); sc.camera = cam
focus = bpy.data.objects.new("Focus", None); focus.location = (0.4, 0, -2.0); sc.collection.objects.link(focus); cd.dof.focus_object = focus

# ---------- gebogene Seiten mit echter fast.site-Oberfläche ----------
img = bpy.data.images.load(TEX)
def page(name, w, h, bend, loc, rot, material):
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object; o.name = name
    o.scale = (w, h, 1); bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=48); bpy.ops.object.mode_set(mode="OBJECT")
    o.rotation_euler = (math.radians(90), 0, 0); bpy.ops.object.transform_apply(rotation=True)
    md = o.modifiers.new("Bend", "SIMPLE_DEFORM"); md.deform_method = "BEND"; md.deform_axis = "Z"; md.angle = math.radians(bend)
    so = o.modifiers.new("Solid", "SOLIDIFY"); so.thickness = 0.04
    bv = o.modifiers.new("Bevel", "BEVEL"); bv.width = 0.015; bv.segments = 2
    o.location = loc; o.rotation_euler = [math.radians(a) for a in rot]; o.data.materials.append(material)
    bpy.ops.object.shade_smooth(); return o

screen = bpy.data.materials.new("Screen"); screen.use_nodes = True
sn = screen.node_tree.nodes; sb = sn["Principled BSDF"]; it = sn.new("ShaderNodeTexImage"); it.image = img
screen.node_tree.links.new(it.outputs["Color"], sb.inputs["Base Color"]); sb.inputs["Roughness"].default_value = 0.35
sb.inputs["Coat Weight"].default_value = 1.0; sb.inputs["Coat Roughness"].default_value = 0.08
pastels = ["#b8a6ff", "#9fc3ff", "#ffb3e1", "#a9e7ff", "#c9b5ff", "#ffc9ea", "#b3c7ff", "#d6c2ff"]
N = 13
for i in range(N):
    t = i / (N - 1)
    m = mat_principled(f"Sheet{i}", srgb(pastels[i % len(pastels)]), rough=0.22, coat=1.0, film=320 + (i * 37) % 360)
    # gedrehtes Band: Seiten folgen einer S-Kurve und drehen sich dabei um ihre Längsachse
    x = -4.6 + 9.2 * t; z = 1.6 * math.sin(t * math.pi * 1.3) - 0.4; y = 2.0 - 1.2 * t
    page(f"Sheet{i}", 2.0, 2.9, 70 + 40 * math.sin(t * math.pi), (x, y, z), (12 + 10 * math.sin(t * 6), -70 + 140 * t, 25 * math.sin(t * math.pi * 2)), m)
page("Hero", 5.6, 3.9, 25, (0.5, -2.5, -2.4), (6, 2, -16), screen)

# ---------- fast.site-Logo: vier Kapseln als Doppel-Chevron ----------
def capsule(name, length, radius, color, loc, roll):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=33, radius=radius); c = bpy.context.object; c.name = name
    for v in c.data.vertices:
        v.co.z += length / 2 if v.co.z > 1e-6 else (-length / 2 if v.co.z < -1e-6 else 0)
    c.modifiers.new("Sub", "SUBSURF").levels = 1
    # flach drücken wie im Logo (Pill statt Rohr)
    c.scale = (1, 0.55, 1); bpy.ops.object.transform_apply(scale=True); bpy.ops.object.shade_smooth()
    c.rotation_euler = (0, math.radians(roll), 0); c.location = loc
    c.data.materials.append(mat_principled(name + "M", color, rough=0.18, coat=1.0, film=220)); return c

logo = bpy.data.objects.new("Logo", None); sc.collection.objects.link(logo)
L, R = 2.0, 0.42; off = L / 2 * math.sin(math.radians(45))
parts = [("Blue", "#3e71b6", -1, 1.0), ("Green", "#0c9958", 1, 1.0), ("Red", "#df482b", -1, -0.35), ("Yellow", "#fbb419", 1, -0.35)]
for n, col, side, y in parts:
    o = capsule(n, L, R, srgb(col), (side * off, 0, y - off), -side * 45); o.parent = logo
logo.location = (2.75, -1.0, 3.55); logo.rotation_euler = (math.radians(12), math.radians(-6), math.radians(-22)); logo.scale = (0.85, 0.85, 0.85)

# ---------- weiche Formen ----------
def prim(kind, loc, scale, mat, rot=(0, 0, 0)):
    getattr(bpy.ops.mesh, kind)(location=loc); o = bpy.context.object; o.scale = scale
    o.rotation_euler = [math.radians(a) for a in rot]; bpy.ops.object.shade_smooth(); o.data.materials.append(mat); return o
clay = lambda h: mat_principled("Clay" + h, srgb(h), rough=0.5, sheen=0.6, film=300)
glass = mat_principled("Glass", srgb("#e6ecff"), rough=0.03, trans=1.0, ior=1.4, film=500)
prim("primitive_uv_sphere_add", (-3.4, 1.5, 2.6), (0.95, 0.95, 0.95), clay("#c6b3ff"))
prim("primitive_torus_add", (3.3, -1.0, -5.2), (0.75, 0.75, 1.3), clay("#ffb5dd"), (60, 20, 0))
prim("primitive_torus_add", (-3.2, -1.5, -5.0), (0.9, 0.9, 1.2), glass, (30, -40, 0))
prim("primitive_uv_sphere_add", (4.1, -2.0, -0.2), (0.42, 0.42, 0.42), clay("#9fd2ff"))
prim("primitive_uv_sphere_add", (1.0, -3.0, -6.4), (0.22, 0.22, 0.22), clay("#ffffff"))
for o in bpy.data.objects:
    if o.type == "MESH" and o.name.startswith("Torus"):
        o.data.update()

t = time.time(); sc.render.filepath = OUT; bpy.ops.render.render(write_still=True)
print("RENDER_SECONDS", round(time.time() - t, 1))
