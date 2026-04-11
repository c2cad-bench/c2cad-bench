"""
Clock Tower Mechanism — Phase 3 Semantic
==========================================
A mechanical clock face: dial ring, equiangular hour markers, two hands
at distinct angles, central shaft with a mounting bushing, and a
counterweight cone at the tail of each hand to balance it on the shaft.

Physical layout:
  - The back plate is the clock face surface (Z=0 plane, front face)
  - The dial ring (torus) sits flush ON the back plate surface at Z=0
  - Hour markers also lie flat on the face at Z=0
  - The shaft protrudes FORWARD from the face (+Z direction)
  - Hands float just above the face (Z=+1 and Z=+2) on the shaft
  - No floating elements — everything is grounded to the face plane

WHY THIS IS HARD:
  1. CONTINUOUS ANGULAR COMPUTATION — Each of N markers sits at a unique
     angle, requiring cos(k·360°/N) and sin(k·360°/N) for k=0..N-1.
     Our data shows this is the primary bottleneck: Spiral Staircase
     (similar continuous-angle task) scores only 60.5% on average.
  2. MULTI-TYPE (5 types) — cylinder + pipe + torus + beam + cone must
     all appear simultaneously. The 2→3 type transition drops scores 34%.
  3. BEAM ORIENTATION DIVERSITY — Every hour marker is a beam at a unique
     radial angle. The minute and hour hands are at two independent angles.
  4. CONE ORIENTATION — Counterweight cones at the hand tails must point
     opposite to their hand. Cones are recognised only 54.4% of the time.

Components:
  • Back plate             — cylinder (flat disc, front face at Z=0)
  • Central shaft          — cylinder (protrudes forward from Z=0)
  • Mounting bushing       — pipe (concentric with shaft)
  • Dial ring              — torus (sits flush on face at Z=0)
  • N hour markers         — beams (radiating outward on the face, Z=0)
  • Minute hand            — beam (above face at Z=+1, pointing to 12)
  • Hour hand              — beam (above face at Z=+2, pointing to 10)
  • Minute counterweight   — cone (tail of minute hand, Z=+1)
  • Hour counterweight     — cone (tail of hour hand, Z=+2)

Difficulty (N = number of hour markers):
  L1 =  4 (12 / 3 / 6 / 9 positions)   →  4+2+1+1+1+2 = 11 shapes
  L2 = 12 (full clock face)              → 12+2+1+1+1+2 = 19 shapes
  L3 = 24 (half-hour + hour, 15° step)  → 24+2+1+1+1+2 = 31 shapes
"""

import math


def _reference_solution(scale):
    N = scale         # number of hour markers
    shapes = []
    sid = 0

    # ── Dimensions ────────────────────────────────────────────────────────
    face_z         = 0.0         # clock face plane — all face elements sit here
    shaft_r        = 4.0         # shaft radius
    shaft_h        = 18.0        # shaft height (protrudes forward in +Z)
    back_r         = 85.0        # back plate radius
    back_h         = 3.0         # back plate thickness (behind the face)
    bushing_inner  = 4.3         # 0.3 mm clearance around shaft
    bushing_outer  = 7.0
    bushing_h      = 14.0
    dial_R         = 78.0        # torus major radius
    dial_r         = 3.0         # torus minor radius
    mark_in        = 60.0        # inner tip of each hour marker (radius)
    mark_out       = 72.0        # outer tip (radius)
    mark_w         = 2.0         # marker beam width
    min_hand       = 62.0        # minute hand length from centre
    hour_hand      = 42.0        # hour hand length
    hand_w         = 3.0         # hand beam width
    cw_h           = 10.0        # counterweight cone height
    cw_base        = 4.0         # counterweight base radius
    cw_tip         = 0.5         # counterweight tip radius
    cw_offset      = 12.0        # counterweight tail offset from centre

    # ── Back plate — behind the face, front face flush at Z=0 ─────────────
    shapes.append({
        "id": sid, "type": "cylinder",
        "center": [0.0, 0.0, -(back_h / 2.0)],
        "radius": back_r, "height": back_h,
    }); sid += 1

    # ── Shaft — protrudes forward from the face plane ──────────────────────
    shapes.append({
        "id": sid, "type": "cylinder",
        "center": [0.0, 0.0, shaft_h / 2.0],
        "radius": shaft_r, "height": shaft_h,
    }); sid += 1

    # ── Mounting bushing (pipe, concentric with shaft) ─────────────────────
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [0.0, 0.0, bushing_h / 2.0],
        "inner_radius": bushing_inner,
        "outer_radius": bushing_outer,
        "height": bushing_h,
    }); sid += 1

    # ── Dial ring (torus) — sits flush ON the back plate face at Z=0 ───────
    shapes.append({
        "id": sid, "type": "torus",
        "center": [0.0, 0.0, face_z],
        "major_radius": dial_R, "minor_radius": dial_r,
    }); sid += 1

    # ── Hour markers — beams lying on the face plane (Z=0) ────────────────
    step = 2.0 * math.pi / N
    for k in range(N):
        a = k * step
        ca, sa = math.cos(a), math.sin(a)
        shapes.append({
            "id": sid, "type": "beam",
            "start": [round(mark_in * ca, 2), round(mark_in * sa, 2), face_z],
            "end":   [round(mark_out * ca, 2), round(mark_out * sa, 2), face_z],
            "width": mark_w, "height": mark_w,
        }); sid += 1

    # ── Minute hand — floats just above face (Z=+1), points toward 12 o'clock
    hand1_z = face_z + 1.0
    shapes.append({
        "id": sid, "type": "beam",
        "start": [0.0, 0.0, hand1_z],
        "end":   [0.0, round(min_hand, 2), hand1_z],
        "width": hand_w, "height": 1.5,
    }); sid += 1

    # ── Hour hand — floats above minute hand (Z=+2), points toward 10 o'clock
    # 10 o'clock in standard polar (CCW from +X): 120°
    hand2_z = face_z + 2.0
    hour_rad = math.radians(120.0)
    hx = round(hour_hand * math.cos(hour_rad), 2)
    hy = round(hour_hand * math.sin(hour_rad), 2)
    shapes.append({
        "id": sid, "type": "beam",
        "start": [0.0, 0.0, hand2_z],
        "end":   [hx, hy, hand2_z],
        "width": hand_w, "height": 2.0,
    }); sid += 1

    # ── Minute counterweight — cone at tail of minute hand (−Y side) ───────
    shapes.append({
        "id": sid, "type": "cone",
        "center": [0.0, -(cw_offset / 2.0), hand1_z],
        "base_radius": cw_base, "top_radius": cw_tip, "height": cw_h,
        "axis": [0.0, -1.0, 0.0],
    }); sid += 1

    # ── Hour counterweight — cone at tail of hour hand (opposite direction) ─
    cw_cx = round(-(cw_offset / 2.0) * math.cos(hour_rad), 2)
    cw_cy = round(-(cw_offset / 2.0) * math.sin(hour_rad), 2)
    shapes.append({
        "id": sid, "type": "cone",
        "center": [cw_cx, cw_cy, hand2_z],
        "base_radius": cw_base, "top_radius": cw_tip, "height": cw_h,
        "axis": [round(-math.cos(hour_rad), 4), round(-math.sin(hour_rad), 4), 0.0],
    }); sid += 1

    return shapes


def generate_clock(scale):
    N = scale
    ref = _reference_solution(scale)
    total = len(ref)

    shaft_r       = 4.0
    shaft_h       = 18.0
    back_r        = 85.0
    back_h        = 3.0
    bushing_inner = 4.3
    bushing_outer = 7.0
    bushing_h     = 14.0
    dial_R        = 78.0
    dial_r        = 3.0
    mark_in       = 60.0
    mark_out      = 72.0
    mark_w        = 2.0
    min_hand      = 62.0
    hour_hand     = 42.0
    hand_w        = 3.0
    cw_offset     = 12.0
    cw_base       = 4.0
    cw_tip        = 0.5
    cw_h          = 10.0

    prompt = f"""Design a clock tower mechanism with {N} hour markers.

Physical layout: The clock face plane is at Z=0. The back plate is behind the face (extending in −Z). The shaft protrudes forward (+Z). All face elements (dial ring, hour markers) sit flush on the face at Z=0. Hands float just above the face at Z=+1 and Z=+2.

Components:
- Back plate: Cylinder (radius {back_r}mm, thickness {back_h}mm) centred at (0,0,−{back_h/2:.1f}mm) so its front face is flush at Z=0.
- Central shaft: Cylinder (radius {shaft_r}mm, height {shaft_h}mm) centred at (0, 0, {shaft_h/2:.1f}mm), protruding forward from Z=0 to Z={shaft_h}mm.
- Mounting bushing: Pipe concentric with the shaft (inner radius {bushing_inner}mm, outer radius {bushing_outer}mm, height {bushing_h}mm), centred at (0, 0, {bushing_h/2:.1f}mm).
- Dial ring: Torus (major radius {dial_R}mm, tube radius {dial_r}mm) centred at the origin (Z=0), sitting flat on the clock face surface.
- {N} hour markers: Beams (width {mark_w}mm) lying flat on the face at Z=0, radiating from radius {mark_in}mm to {mark_out}mm, equally spaced at {360.0/N:.1f}° intervals. Compute each marker position using cos and sin.
- Minute hand: Beam (length {min_hand}mm, width {hand_w}mm) from (0,0,+1) toward 12 o'clock (+Y direction), floating 1mm above the face.
- Hour hand: Beam (length {hour_hand}mm, width {hand_w}mm) from (0,0,+2) toward 10 o'clock (120° in standard polar = upper-left), floating 2mm above the face.
- Minute counterweight: Cone (base radius {cw_base}mm, tip radius {cw_tip}mm, height {cw_h}mm) at the tail of the minute hand at Z=+1, pointing in −Y (opposite the minute hand).
- Hour counterweight: Cone (same size) at the tail of the hour hand at Z=+2, pointing opposite to the hour hand direction.

Semantic Constraints:
1. All {N} markers must be equiangular (exactly {360.0/N:.1f}° apart) and lie in the Z=0 face plane.
2. The dial ring (torus) sits flat on the face at Z=0, concentric with the shaft.
3. Minute and hour hands originate at the shaft centre (0,0) at their respective heights (Z=+1, Z=+2).
4. Counterweight cones sit behind centre on the opposite side of each hand, balancing on the shaft.
5. The mounting bushing is concentric with the shaft with {bushing_inner - shaft_r:.1f}mm radial clearance.
6. No parts may overlap.

Total shapes: {total}.
Output only the raw JSON array — no markdown, no explanation."""

    specs = {
        "gravity_check": False,
        "interference_check": True,
        "mates": [{"type": "concentric", "ids": [0, 1, 2, 3]}],
        "clearance_fit": [
            {"shaft_id": 1, "hole_id": 2,
             "expected_clearance": bushing_inner - shaft_r, "tol": 0.1}
        ],
        "reference": ref
    }
    return prompt, specs


if __name__ == "__main__":
    import json, argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=12)
    args = parser.parse_args()
    prompt, specs = generate_clock(args.scale)
    ref = specs["reference"]
    from collections import Counter
    print(f"Clock — {args.scale} markers, {len(ref)} shapes")
    print(f"Types: {dict(Counter(s['type'] for s in ref))}")
    print(prompt)
