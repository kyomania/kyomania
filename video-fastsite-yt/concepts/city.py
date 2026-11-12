"""Konzept 10 – 3D-Server-Stadt bei Nacht (Blender/Cycles), Styleframes.
python city.py <shot: slow|fast|shield> <out.png> [samples] [scale%]
"""
import bpy, math, sys, random, addon_utils
from mathutils import Vector

SHOT, OUT = sys.argv[1], sys.argv[2]
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 48
SCALE = int(sys.argv[4]) if len(sys.argv) > 4 else 50
random.seed(7)

addon_utils.enable("cycles", default_set=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.render.resolution_percentage = SCALE
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Punchy"
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.004, 0.007, 0.02, 1); bg.inputs[1].default_value = 1.0


def mat(name, base=(0.02, 0.025, 0.04), rough=0.35, metal=0.6, emit=None, strength=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    return m


def box(x, y, z, sx, sy, sz, m):
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z)); o = bpy.context.object; o.scale = (sx / 2, sy / 2, sz / 2); o.data.materials.append(m); return o


TOWER = mat("tower", (0.03, 0.035, 0.05), 0.25, 0.8)
GROUND = mat("ground", (0.01, 0.012, 0.02), 0.15, 0.9)
SHOP_C = {"slow": (1.0, 0.12, 0.05), "fast": (0.2, 1.0, 0.45), "shield": (0.2, 1.0, 0.45)}[SHOT]
WIN_A = mat("winA", emit=(0.25, 0.55, 1.0), strength=4.0)
WIN_B = mat("winB", emit=(1.0, 0.72, 0.15), strength=5.0)
WIN_S = mat("winS", emit=SHOP_C, strength=9.0)
YEL = mat("yel", emit=(1.0, 0.7, 0.1), strength=22.0)
CYAN = mat("cyan", emit=(0.2, 0.75, 1.0), strength=16.0)
RED = mat("red", emit=(1.0, 0.08, 0.04), strength=18.0)

# ground with a faint grid of street lines
box(0, 0, -0.05, 400, 400, 0.1, GROUND)
for i in range(-20, 21):
    box(i * 4.0, 0, 0.01, 0.04, 160, 0.02, mat(f"st{i}", emit=(0.15, 0.3, 0.8), strength=0.6))

# server towers on a grid
towers = []
for gx in range(-9, 10):
    for gy in range(-2, 18):
        if random.random() < 0.38 or (abs(gx) < 1 and gy < 3):
            continue
        x, y = gx * 4.0 + random.uniform(-0.3, 0.3), gy * 4.0 + random.uniform(-0.3, 0.3)
        h = random.uniform(2, 9) * (1.6 if gy > 6 else 1.0)
        sx, sy = random.uniform(1.8, 2.8), random.uniform(1.8, 2.8)
        box(x, y, h / 2, sx, sy, h, TOWER)
        # rack lights: thin glowing strips on the front face
        n = int(h / 0.45)
        wm = WIN_B if random.random() < 0.25 else WIN_A
        for k in range(n):
            if random.random() < 0.65:
                box(x, y - sy / 2 - 0.01, 0.3 + k * 0.45, sx * random.uniform(0.4, 0.85), 0.02, 0.06, wm)
        towers.append((x, y, h))

# the hero tower: "DEIN SHOP"
SX, SY, SH = 0.0, 6.0, 7.0
box(SX, SY, SH / 2, 2.8, 2.8, SH, TOWER)
for k in range(int(SH / 0.4)):
    box(SX, SY - 1.41, 0.3 + k * 0.4, 2.2, 0.02, 0.08, WIN_S)
box(SX, SY, SH + 0.05, 2.9, 2.9, 0.1, WIN_S)


def tube(points, m, r=0.05):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 2
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(points) - 1)
    for p, co in zip(sp.bezier_points, points):
        p.co = co; p.handle_left_type = p.handle_right_type = "AUTO"
    o = bpy.data.objects.new("t", cu); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o


if SHOT == "slow":
    # traffic jam: stalled red light streaks crawling towards the shop
    for lane in range(4):
        y0 = -14 + lane * 0.35
        for i in range(26):
            x = -30 + i * 2.2 + random.uniform(-0.2, 0.2)
            box(x, y0 + 8, 0.25, 0.5, 0.12, 0.12, RED)
    for t in towers[:40]:
        if random.random() < 0.3:
            box(t[0], t[1], t[2] + 0.4, 0.15, 0.15, 0.8, RED)
    bg.inputs[0].default_value = (0.01, 0.004, 0.006, 1)

if SHOT in ("fast", "shield"):
    # fast.site: glowing shortcut arcs from edge beacons straight to the shop
    beacons = random.sample([t for t in towers if t[1] < 40], 12)
    for (x, y, h) in beacons:
        box(x, y, h + 0.6, 0.25, 0.25, 1.2, YEL)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=(x, y, h + 1.4)); s = bpy.context.object; s.data.materials.append(YEL)
        mid = Vector(((x + SX) / 2, (y + SY) / 2, max(h, SH) + 4 + random.uniform(0, 3)))
        tube([Vector((x, y, h + 1.4)), mid, Vector((SX, SY, SH + 0.2))], YEL if random.random() < 0.5 else CYAN, 0.045)
    # data streaks on the avenues
    for lane in range(6):
        y0 = -14 + lane * 0.5
        tube([Vector((-40, y0 + 8, 0.3)), Vector((0, y0 + 8, 0.3)), Vector((40, y0 + 8, 0.3))], CYAN if lane % 2 else YEL, 0.03)

if SHOT == "shield":
    # translucent energy dome over the city, attacks burning up on it
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=26, location=(0, 14, -4))
    dome = bpy.context.object
    dm = bpy.data.materials.new("dome"); dm.use_nodes = True; nt = dm.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); mix = nt.nodes.new("ShaderNodeMixShader"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (0.25, 0.6, 1.0, 1); em.inputs[1].default_value = 3.0
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs[0].default_value = 0.35
    wf = nt.nodes.new("ShaderNodeWireframe"); wf.inputs[0].default_value = 0.06
    mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
    nt.links.new(lw.outputs["Facing"], mx.inputs[0]); nt.links.new(wf.outputs[0], mx.inputs[1])
    nt.links.new(mx.outputs[0], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs[0])
    dome.data.materials.append(dm)
    for i in range(14):
        a = random.uniform(0, math.tau); el = random.uniform(0.35, 1.0)
        hit = Vector((0, 14, -4)) + Vector((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el))) * 26
        start = hit + Vector((random.uniform(-6, 6), random.uniform(-6, 6), 0)) + (hit - Vector((0, 14, -4))).normalized() * 18
        tube([start, (start + hit) / 2, hit], RED, 0.06)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.7, location=hit); s = bpy.context.object; s.data.materials.append(mat(f"hit{i}", emit=(1.0, 0.4, 0.1), strength=30))

# camera
cam = bpy.data.cameras.new("cam"); co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); sc.camera = co
cam.lens = 28 if SHOT == "shield" else 35
if SHOT == "shield":
    co.location = (-34, -32, 26)
else:
    co.location = (-16, -18, 9)
tgt = Vector((0, 8, 3)) if SHOT != "shield" else Vector((0, 14, 2))
co.rotation_euler = (tgt - co.location).to_track_quat("-Z", "Y").to_euler()
cam.dof.use_dof = SHOT != "shield"; cam.dof.focus_distance = (Vector((SX, SY, 3)) - co.location).length; cam.dof.aperture_fstop = 2.8

# moon-ish key light + bloom
bpy.ops.object.light_add(type="SUN", location=(0, 0, 20)); sun = bpy.context.object; sun.data.energy = 0.25; sun.data.color = (0.5, 0.6, 1.0); sun.rotation_euler = (0.9, 0.2, 0.6)

sc.use_nodes = True
nt = sc.node_tree; nt.nodes.clear()
rl = nt.nodes.new("CompositorNodeRLayers"); gl = nt.nodes.new("CompositorNodeGlare"); comp = nt.nodes.new("CompositorNodeComposite")
gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 0.6; gl.size = 8
nt.links.new(rl.outputs["Image"], gl.inputs["Image"]); nt.links.new(gl.outputs["Image"], comp.inputs["Image"])

sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("rendered", OUT)
