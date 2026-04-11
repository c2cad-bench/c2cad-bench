"""
Cochlear Spiral — Phase 4 Bio-Inspired
========================================
Models the inner ear cochlea: a tapered Archimedean helix with N segments.
Each segment carries a basilar membrane partition. The central modiolus
(bony axis) threads through all turns. A basal ring marks the entry plane.
An entry pipe sits physically at the helix start (the oval window port).
A single apex cone caps the helix at the helicotrema (top of the cochlea).

WHY THIS IS HARD:
  1. TAPERED 3D HELIX — Both the radius AND the angle change at every step.
     Each segment endpoint: x = R(t)·cos(θ), y = R(t)·sin(θ), z = h·t
     where R(t) = R₀·(1 − taper·t). Spiral Staircase (constant radius,
     2D) already scores only 60.5%. This is strictly harder.
  2. ALL 6 PRIMITIVE TYPES — cylinder (modiolus), pipe (oval window entry),
     torus (basal ring), beam (tube segments), box (basilar membranes),
     cone (cochlear apex/helicotrema). Maximum compositional load.
  3. COUPLED COORDINATE FRAMES — Each membrane box must be placed at the
     midpoint of its helix segment. Both start/end positions and midpoints
     require 3D parametric computation at every step.
  4. SPATIAL GROUNDING — pipe must sit flush at the helix entry point;
     apex cone must cap the modiolus at the helix top height.

Difficulty (N = total number of helical segments):
  L1 = 12 segments (1 full revolution, 30° per step)  → 12×2 + 4 = 28 shapes
  L2 = 24 segments (2 full revolutions, 30° per step) → 24×2 + 4 = 52 shapes
  L3 = 36 segments (3 full revolutions, 30° per step) → 36×2 + 4 = 76 shapes

Components:
  • Modiolus        — cylinder (central vertical axis, full height)
  • Basal ring      — torus (at Z=0, circumscribes the helix base)
  • Oval window     — pipe (entry port, sits flush at the helix start point)
  • N tube segments — beams (consecutive helix points)
  • N basilar memb. — boxes (midpoint of each segment)
  • Apex cone       — cone (caps the modiolus at the helicotrema, top of helix)
"""

import math


def _reference_solution(scale):
    N = scale   # total segments (12, 24, or 36)
    shapes = []
    sid = 0

    # ── Parameters ────────────────────────────────────────────────────────
    R0           = 30.0    # starting radius (mm)
    taper        = 0.55    # radius shrinks to R0*(1-taper) at apex
    turns        = N / 12  # full revolutions (12 segs = 1 turn)
    pitch        = 6.0     # mm rise per full revolution
    segment_w    = 4.0     # beam width/height (mm)
    mod_r        = 3.5     # modiolus radius (mm)
    basal_R      = R0      # torus major radius (matches helix start)
    basal_r      = 2.0     # torus tube radius (mm)
    oval_inner   = 2.0     # oval window pipe inner radius
    oval_outer   = 5.0     # oval window pipe outer radius (= beam width)
    oval_h       = 6.0     # oval window pipe height
    mem_depth    = 5.0     # basilar membrane box radial depth
    mem_w        = 3.0     # basilar membrane box tangential width
    mem_h        = 0.8     # basilar membrane box thickness
    apex_base_r  = 4.0     # helicotrema cone base radius
    apex_tip_r   = 0.5     # helicotrema cone tip radius
    apex_h       = 8.0     # helicotrema cone height

    total_height = turns * pitch
    total_angle  = turns * 2.0 * math.pi

    # Compute helix points: N+1 points for N segments
    def helix_point(i):
        t = i / N
        R = R0 * (1.0 - taper * t)
        theta = t * total_angle
        return (round(R * math.cos(theta), 3),
                round(R * math.sin(theta), 3),
                round(t * total_height, 3))

    pts = [helix_point(i) for i in range(N + 1)]

    # ── Modiolus (cylinder along Z, full cochlear height) ─────────────────
    shapes.append({
        "id": sid, "type": "cylinder",
        "center": [0.0, 0.0, round(total_height / 2.0, 2)],
        "radius": mod_r,
        "height": round(total_height, 2),
    }); sid += 1

    # ── Basal ring (torus at Z=0 — the cochlear base plane) ───────────────
    # Sits in the Z=0 plane, circumscribes the helix base.
    shapes.append({
        "id": sid, "type": "torus",
        "center": [0.0, 0.0, 0.0],
        "major_radius": basal_R,
        "minor_radius": basal_r,
    }); sid += 1

    # ── Oval window pipe (entry port, flush at the helix start) ───────────
    # Top face of the pipe is at Z=0, coinciding with the first helix point.
    # Pipe hangs downward below the basal plane, physically attached to the
    # first helix segment.
    px, py, pz = pts[0]
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [px, py, round(pz - oval_h / 2.0, 2)],
        "inner_radius": oval_inner,
        "outer_radius": oval_outer,
        "height": oval_h,
    }); sid += 1

    # ── Segments: beam + basilar membrane box ─────────────────────────────
    for i in range(N):
        x0, y0, z0 = pts[i]
        x1, y1, z1 = pts[i + 1]

        # Beam (tube segment of the cochlear duct)
        shapes.append({
            "id": sid, "type": "beam",
            "start": [x0, y0, z0],
            "end":   [x1, y1, z1],
            "width": segment_w,
            "height": segment_w,
        }); sid += 1

        # Basilar membrane (thin box at midpoint of each segment)
        mx = round((x0 + x1) / 2.0, 2)
        my = round((y0 + y1) / 2.0, 2)
        mz = round((z0 + z1) / 2.0, 2)
        shapes.append({
            "id": sid, "type": "box",
            "center": [mx, my, mz],
            "size": [mem_w, mem_depth, mem_h],
        }); sid += 1

    # ── Apex cone (helicotrema — caps the top of the modiolus) ────────────
    # The cochlear apex is the uppermost point of the spiral where the two
    # scalae connect. It caps the modiolus at the top of the helix.
    shapes.append({
        "id": sid, "type": "cone",
        "center": [0.0, 0.0, round(total_height + apex_h / 2.0, 2)],
        "base_radius": apex_base_r,
        "top_radius": apex_tip_r,
        "height": apex_h,
    }); sid += 1

    return shapes


def generate_cochlea(scale):
    N = scale
    ref = _reference_solution(scale)
    total = len(ref)

    R0       = 30.0
    taper    = 0.55
    turns    = N / 12
    pitch    = 6.0
    seg_w    = 4.0
    mod_r    = 3.5
    basal_R  = R0
    basal_r  = 2.0
    oval_inner = 2.0
    oval_outer = 5.0
    oval_h   = 6.0
    mem_dep  = 5.0
    mem_w    = 3.0
    apex_br  = 4.0
    apex_tr  = 0.5
    apex_h   = 8.0

    total_height = round(turns * pitch, 1)
    R_apex       = round(R0 * (1.0 - taper), 1)

    prompt = f"""Design a cochlear spiral (inner ear model) with {N} helical segments ({turns:.0f} full revolution{"s" if turns != 1 else ""}).

Components:
- 1 modiolus: Cylinder (radius {mod_r}mm) along the Z-axis, centred at the origin, height = {total_height}mm (full spiral height). This is the bony central axis the helix winds around.
- 1 basal ring: Torus (major radius {basal_R}mm, tube radius {basal_r}mm) in the Z=0 plane, centred at the origin. This marks the cochlear base and circumscribes the helix start.
- 1 oval window: Pipe (inner radius {oval_inner}mm, outer radius {oval_outer}mm, height {oval_h}mm) hanging below the first helix point with its top face flush at Z=0. It is physically attached to the start of the helix as the cochlear entry port.
- {N} tube segments: Beams (width {seg_w}mm, height {seg_w}mm) connecting consecutive points along the tapered helix. Each segment spans exactly 30° of rotation.
- {N} basilar membrane partitions: Boxes (size [{mem_w}, {mem_dep}, 0.8]mm) placed at the midpoint of each tube segment.
- 1 apex cone: Cone (base radius {apex_br}mm, tip radius {apex_tr}mm, height {apex_h}mm) centred on the Z-axis directly above the modiolus top (at Z = {total_height}mm + half cone height). This caps the helicotrema — the opening at the cochlear apex.

Helix definition:
- The helix has {turns:.0f} full revolution{"s" if turns != 1 else ""}, totalling {round(turns * 360):.0f}° of rotation.
- Starting radius: {basal_R}mm at the base (Z=0). Radius tapers linearly to {R_apex}mm at the apex (Z={total_height}mm).
- Vertical rise: {pitch}mm per full revolution. Total height: {total_height}mm.
- Parametric form: x(t) = R(t)·cos(2π·{turns:.0f}·t), y(t) = R(t)·sin(2π·{turns:.0f}·t), z(t) = {total_height}·t, where R(t) = {R0}·(1 − {taper}·t) and t goes from 0 to 1.
- Divide t into {N} equal steps to get {N+1} helix vertices. Each beam connects vertex i to vertex i+1.
- Each basilar membrane box is placed at the midpoint between vertex i and vertex i+1.

Physical Constraints:
1. All helix points must follow the parametric formula above. Each step increments t by 1/{N}.
2. The oval window pipe top face (Z=0) must be flush with the first helix vertex. Its centre is at the XY position of the first helix vertex, shifted {oval_h/2:.1f}mm below (Z = −{oval_h/2:.1f}mm).
3. The apex cone sits directly on the Z-axis, base touching the top of the modiolus at Z={total_height}mm.
4. No parts may overlap.

Total shapes: {total}.
Output only the raw JSON array — no markdown, no explanation."""

    specs = {
        "gravity_check": False,
        "interference_check": True,
        "mates": [],
        "clearance_fit": [],
        "reference": ref
    }
    return prompt, specs


if __name__ == "__main__":
    import json, argparse
    from collections import Counter
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=12)
    args = parser.parse_args()
    prompt, specs = generate_cochlea(args.scale)
    ref = specs["reference"]
    print(f"Cochlear Spiral — {args.scale} segments, {len(ref)} shapes")
    print(f"Types: {dict(Counter(s['type'] for s in ref))}")
    print(prompt)
