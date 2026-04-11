"""
Flanged Pipe Joint — Phase 1 Basic (Engineering CAD)
=====================================================
A real engineering assembly: two flanged pipes bolted together.
This is one of the most common assemblies in mechanical/process
engineering CAD — every piping system has hundreds of these joints.

The assembly has:
  • 2 pipe bodies (pipes, concentric along the X-axis)
  • 2 flange rings (pipes — hollow so the bore is visible through)
  • N bolts on a bolt-circle (cylinders, equally spaced around the flange)
  • N nuts (tori, one per bolt, concentric with each bolt)

WHY THIS IS EXTREMELY HARD FOR LLMs:
  1. BOLT-CIRCLE ANGULAR COMPUTATION — N bolts equally spaced on a circle
     of radius R: each at (R·cos(k·2π/N), R·sin(k·2π/N)). This is the
     same continuous-angle computation that breaks Spiral Staircase (60.5%)
     but now in a horizontal plane. At L3 with 16 bolts, each at a unique
     angle at 22.5° spacing — LLMs must compute 16 cos/sin pairs.

  2. CONCENTRIC CONSTRAINT CHAINS — The bolts pass through BOTH flanges
     (their axis must align perfectly). The flanges and pipes must all
     share the same central axis. Multiple concentric chains.

  3. BOLT ORIENTATION — Each bolt cylinder must be oriented along the
     pipe axis (X-axis), NOT vertically. LLMs default to Z-axis cylinders.
     Getting the bolt axis wrong while keeping position right still fails.

  4. TORUS AS NUT — Each nut is a torus concentric with its bolt. The
     torus must sit at the correct X-position (outer face of flange).
     Tori are recognised 89.5% of the time, but placing N tori at N
     unique bolt-circle positions in 3D requires the same angle computation.

  5. PIPE vs CYLINDER CONFUSION — Pipes (hollow) and cylinders (solid)
     coexist. Flanges and pipe bodies are all pipes (hollow), bolts are
     cylinders (solid). Models that collapse pipe→cylinder (24.1%
     substitution rate) will fail semantically.

Components:
  • 2 pipe bodies (pipe, concentric along X)
  • 2 flange rings (pipe, concentric along X — hollow so the bore shows)
  • N bolts (cylinder, on bolt circle, oriented along X)
  • N nuts (torus, concentric with each bolt)

Difficulty (N = number of bolts):
  L1 =  4 bolts → 2+2+4+4 = 12 shapes
  L2 =  8 bolts → 2+2+8+8 = 20 shapes
  L3 = 16 bolts → 2+2+16+16 = 36 shapes
"""

import math


def _reference_solution(scale):
    N = scale   # number of bolts
    shapes = []
    sid = 0

    # ── Pipe dimensions ────────────────────────────────────────────────────
    pipe_inner   = 25.0     # mm — pipe bore radius
    pipe_outer   = 30.0     # mm — pipe wall outer radius
    pipe_length  = 60.0     # mm — each pipe segment length
    flange_inner = pipe_inner  # mm — flange bore = pipe bore (hollow through)
    flange_outer = 50.0     # mm — flange disc outer radius
    flange_h     = 8.0      # mm — flange disc thickness
    bolt_circle  = 40.0     # mm — bolt circle radius (centre-to-centre)
    bolt_r       = 3.0      # mm — bolt shaft radius
    bolt_length  = 20.0     # mm — bolt shaft length (spans both flanges)
    nut_major    = 3.0      # mm — nut torus major radius (= bolt_r)
    nut_minor    = 2.0      # mm — nut torus tube radius
    gap          = 2.0      # mm — gap between flanges

    # The joint sits at X=0. Left pipe extends in -X, right pipe in +X.
    flange_x_left  = -(gap / 2.0 + flange_h / 2.0)
    flange_x_right = +(gap / 2.0 + flange_h / 2.0)
    pipe_x_left    = flange_x_left - flange_h / 2.0 - pipe_length / 2.0
    pipe_x_right   = flange_x_right + flange_h / 2.0 + pipe_length / 2.0

    # ── Left pipe body ─────────────────────────────────────────────────────
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [round(pipe_x_left, 2), 0.0, 0.0],
        "inner_radius": pipe_inner, "outer_radius": pipe_outer,
        "height": pipe_length, "axis": [1, 0, 0],
    }); sid += 1

    # ── Right pipe body ────────────────────────────────────────────────────
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [round(pipe_x_right, 2), 0.0, 0.0],
        "inner_radius": pipe_inner, "outer_radius": pipe_outer,
        "height": pipe_length, "axis": [1, 0, 0],
    }); sid += 1

    # ── Left flange ring (pipe — hollow so bore is visible) ───────────────
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [round(flange_x_left, 2), 0.0, 0.0],
        "inner_radius": flange_inner, "outer_radius": flange_outer,
        "height": flange_h, "axis": [1, 0, 0],
    }); sid += 1

    # ── Right flange ring (pipe — hollow so bore is visible) ──────────────
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [round(flange_x_right, 2), 0.0, 0.0],
        "inner_radius": flange_inner, "outer_radius": flange_outer,
        "height": flange_h, "axis": [1, 0, 0],
    }); sid += 1

    # ── Bolts + Nuts on bolt circle ────────────────────────────────────────
    angle_step = 2.0 * math.pi / N
    bolt_cx = 0.0
    nut_x = flange_x_right + flange_h / 2.0

    for k in range(N):
        angle = k * angle_step
        by = round(bolt_circle * math.cos(angle), 3)
        bz = round(bolt_circle * math.sin(angle), 3)

        # Bolt (cylinder oriented along X-axis)
        shapes.append({
            "id": sid, "type": "cylinder",
            "center": [bolt_cx, by, bz],
            "radius": bolt_r, "height": bolt_length, "axis": [1, 0, 0],
        }); sid += 1

        # Nut (torus concentric with bolt, at right flange face)
        shapes.append({
            "id": sid, "type": "torus",
            "center": [round(nut_x, 2), by, bz],
            "major_radius": nut_major, "minor_radius": nut_minor,
        }); sid += 1

    return shapes


def generate_flange(scale):
    N = scale
    ref = _reference_solution(scale)
    total = len(ref)

    pipe_inner   = 25.0
    pipe_outer   = 30.0
    pipe_length  = 60.0
    flange_inner = pipe_inner
    flange_outer = 50.0
    flange_h     = 8.0
    bolt_circle  = 40.0
    bolt_r       = 3.0
    bolt_length  = 20.0
    nut_major    = 3.0
    nut_minor    = 2.0
    gap          = 2.0

    prompt = f"""Design a flanged pipe joint with {N} bolts — a standard piping connection used in process engineering.

Components:
- 2 pipe bodies: Pipes (inner radius {pipe_inner}mm, outer radius {pipe_outer}mm, length {pipe_length}mm each) running along the X-axis, meeting at X=0. The left pipe extends in −X, the right pipe in +X.
- 2 flange rings: Pipes (inner radius {flange_inner}mm, outer radius {flange_outer}mm, thickness {flange_h}mm) concentric with the pipe bodies, oriented along the X-axis. The flanges are hollow through the bore so the pipe opening is visible. One at each pipe end, separated by a {gap}mm gap.
- {N} bolts: Cylinders (radius {bolt_r}mm, length {bolt_length}mm) equally spaced on a bolt circle of radius {bolt_circle}mm around the flange centre. Each bolt is oriented along the X-axis (parallel to the pipe), spanning through both flanges.
- {N} nuts: Tori (major radius {nut_major}mm, tube radius {nut_minor}mm) one per bolt, concentric with each bolt, positioned at the outer face of the right flange.

Geometric Constraints:
1. Both pipes and both flanges must all be concentric (sharing the X-axis as centre line). Flanges are PIPES (hollow), NOT solid cylinders — the bore must be visible through.
2. The {N} bolts must be equally spaced at {360.0/N:.1f}° intervals on the bolt circle. Compute each bolt Y,Z using cos and sin of k·{360.0/N:.1f}° for k=0..{N-1}.
3. Each bolt cylinder must be oriented along the X-axis (NOT the default Z-axis).
4. Each nut torus must be centred on its bolt at the same Y,Z position.
5. No parts may overlap.

Total shapes: {total}.
Output only the raw JSON array — no markdown, no explanation."""

    mates = [{"type": "concentric", "ids": [0, 1, 2, 3]}]
    for k in range(N):
        bolt_id = 4 + 2 * k
        nut_id  = 4 + 2 * k + 1
        mates.append({"type": "concentric", "ids": [bolt_id, nut_id]})

    specs = {
        "gravity_check": False,
        "interference_check": True,
        "mates": mates,
        "clearance_fit": [],
        "reference": ref,
    }
    return prompt, specs


if __name__ == "__main__":
    import json, argparse
    from collections import Counter
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=8)
    args = parser.parse_args()
    prompt, specs = generate_flange(args.scale)
    ref = specs["reference"]
    print(f"Flanged Pipe Joint — {args.scale} bolts, {len(ref)} shapes")
    print(f"Types: {dict(Counter(s['type'] for s in ref))}")
    print(prompt)
