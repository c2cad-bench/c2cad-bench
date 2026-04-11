"""
Ball Bearing Assembly — Phase 2 Advanced (Engineering CAD)
============================================================
A radial ball bearing: the most ubiquitous machine element in
mechanical engineering. Every rotating shaft in every machine
on Earth rides on bearings — this is THE fundamental CAD assembly.

The assembly has:
  • Inner race   — pipe (hollow cylinder, shaft passes through)
  • Outer race   — pipe (hollow cylinder, housing bore)
  • N balls      — spheres equally spaced on a pitch circle

No cage ring, no shield discs — the bearing is fully open so
the balls are clearly visible between the two races.

WHY THIS IS EXTREMELY HARD FOR LLMs:
  1. PITCH-CIRCLE ANGULAR COMPUTATION — N balls equally spaced on a
     circle of radius R: each at (R·cos(k·2π/N), R·sin(k·2π/N)).
     Same computation that breaks Spiral Staircase (60.5%) but now
     with spheres that have no orientation to help contextualise.

  2. PIPE vs CYLINDER COEXISTENCE — Inner/outer races are PIPES
     (hollow). Pipe recognition is only 69.6%. Models that collapse
     pipe→cylinder will lose the hollow bore semantics (24.1%
     substitution rate).

  3. CONCENTRIC CONSTRAINT CHAINS — Inner race, outer race, and cage
     must ALL share the same Z-axis. The balls must sit on a pitch
     circle concentric with all of these. 3-deep concentric chain.

  4. SPHERE PACKING ON A CIRCLE — Spheres on a pitch circle is
     geometrically unusual. LLMs must compute unique (x,y) for
     each ball while keeping z=0. Spheres are recognised 92.6%
     but placing N of them on a circle is a parametric challenge.

Components:
  • Inner race     — pipe (concentric, along Z-axis)
  • Outer race     — pipe (concentric, along Z-axis)
  • N rolling balls — spheres (on pitch circle in XY plane)

Difficulty (N = number of balls):
  L1 =  6 balls → 1+1+6  =  8 shapes
  L2 = 12 balls → 1+1+12 = 14 shapes
  L3 = 20 balls → 1+1+20 = 22 shapes
"""

import math


def _reference_solution(scale):
    N = scale   # number of balls
    shapes = []
    sid = 0

    # ── Bearing dimensions (loosely based on 6205 deep-groove) ────────────
    inner_bore     = 12.5    # mm — inner race bore radius (shaft hole)
    inner_outer    = 17.0    # mm — inner race outer radius (raceway surface)
    outer_inner    = 23.0    # mm — outer race inner radius (raceway surface)
    outer_outer    = 26.0    # mm — outer race outer radius (housing bore)
    bearing_width  = 15.0    # mm — axial width of bearing
    pitch_r        = 20.0    # mm — pitch circle radius (centre of balls)
    ball_r         = 3.0     # mm — ball radius

    # ── Inner race (pipe along Z-axis) ─────────────────────────────────────
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [0.0, 0.0, 0.0],
        "inner_radius": inner_bore, "outer_radius": inner_outer,
        "height": bearing_width,
    }); sid += 1

    # ── Outer race (pipe along Z-axis) ─────────────────────────────────────
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [0.0, 0.0, 0.0],
        "inner_radius": outer_inner, "outer_radius": outer_outer,
        "height": bearing_width,
    }); sid += 1

    # ── Rolling balls on pitch circle ──────────────────────────────────────
    angle_step = 2.0 * math.pi / N
    for k in range(N):
        angle = k * angle_step
        bx = round(pitch_r * math.cos(angle), 3)
        by = round(pitch_r * math.sin(angle), 3)
        shapes.append({
            "id": sid, "type": "sphere",
            "center": [bx, by, 0.0],
            "radius": ball_r,
        }); sid += 1

    return shapes


def generate_ball_bearing(scale):
    N = scale
    ref = _reference_solution(scale)
    total = len(ref)

    inner_bore    = 12.5
    inner_outer   = 17.0
    outer_inner   = 23.0
    outer_outer   = 26.0
    bearing_width = 15.0
    pitch_r       = 20.0
    ball_r        = 3.0

    prompt = f"""Design an open radial ball bearing assembly with {N} rolling elements — the most common rotary bearing in mechanical engineering.

Components:
- 1 inner race: Pipe (inner radius {inner_bore}mm, outer radius {inner_outer}mm, width {bearing_width}mm) centred at the origin along the Z-axis. This is the hollow ring that fits on the shaft.
- 1 outer race: Pipe (inner radius {outer_inner}mm, outer radius {outer_outer}mm, width {bearing_width}mm) centred at the origin along the Z-axis, concentric with the inner race. This is the ring that sits in the housing.
- {N} rolling balls: Spheres (radius {ball_r}mm) equally spaced on a pitch circle of radius {pitch_r}mm in the XY plane (Z=0). Each ball centre at ({pitch_r}·cos(k·{360.0/N:.1f}°), {pitch_r}·sin(k·{360.0/N:.1f}°), 0) for k=0..{N-1}.

This is a fully open bearing — no cage ring, no shield discs. The balls must be clearly visible sitting in the gap between the inner and outer races.

Geometric Constraints:
1. Inner race and outer race must be concentric (sharing the Z-axis at the origin).
2. The {N} balls must be equally spaced at {360.0/N:.1f}° intervals on the pitch circle. Compute each ball's X,Y using cos and sin of k·{360.0/N:.1f}° for k=0..{N-1}.
3. Inner race and outer race are PIPES (hollow cylinders), NOT solid cylinders. The inner race has a bore for the shaft.
4. Ball centres must all lie in the Z=0 plane, sitting in the annular gap between the inner race outer surface ({inner_outer}mm) and the outer race inner surface ({outer_inner}mm).
5. No parts may overlap.

Total shapes: {total}.
Output only the raw JSON array — no markdown, no explanation."""

    mates = [{"type": "concentric", "ids": [0, 1]}]

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
    parser.add_argument("--scale", type=int, default=12)
    args = parser.parse_args()
    prompt, specs = generate_ball_bearing(args.scale)
    ref = specs["reference"]
    print(f"Ball Bearing — {args.scale} balls, {len(ref)} shapes")
    print(f"Types: {dict(Counter(s['type'] for s in ref))}")
    print(prompt)
