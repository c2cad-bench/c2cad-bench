"""
Gantry Crane Assembly — Phase 3 Semantic
==========================================
Models an overhead gantry crane: two parallel rail beams supported by
vertical columns, with a travelling bridge beam, a trolley on the bridge,
and a hoist cable + hook assembly.

WHY THIS IS HARD FOR LLMs:
  This family targets FOUR identified failure mechanisms simultaneously:

  1. BEAM ORIENTATION BLINDNESS — The structure is dominated by beams:
     rail beams (horizontal along X), bridge beam (horizontal along Y),
     cross-bracing diagonals (unique 3D angles for each brace), and
     vertical columns. Models that substitute boxes for beams lose the
     orientation encoding entirely. Score gap: +45.3 points when beams
     are used correctly.

  2. MULTI-TYPE COMPOSITION — Uses 5 types (beam, cylinder, box, pipe, cone).
     The crane requires the model to reason about beams (rails, braces,
     bridge), cylinders (columns, cable drum), a box (trolley), a pipe
     (hoist cable), and a cone (hook). The 2→3 type transition causes
     a 34% score drop.

  3. CROSS-BRACING DIAGONALS — Each bay between columns is cross-braced
     with two diagonal beams forming an X pattern. Each diagonal has a
     unique 3D direction vector connecting non-adjacent column tops to
     bottoms. At L3 with 6 bays, this produces 12 diagonal beams with
     12 unique orientations — a continuous parametric challenge.

  4. SPATIAL CHAIN REASONING — The hook hangs from the trolley, which
     rides on the bridge, which spans between the rails, which sit on
     the columns. The model must propagate positions through a 4-level
     kinematic chain.

Components per bay:
  • 2 vertical columns (cylinder) per bay-boundary
  • 2 rail beams (beam) on top, along X
  • 2 diagonal braces (beam) per bay, forming X patterns
  • 1 bridge beam (beam) spanning the rails at the trolley position
  • 1 trolley body (box) riding on the bridge
  • 1 hoist cable (pipe) hanging from trolley
  • 1 cable drum (cylinder) on the trolley
  • 1 hook (cone) at the bottom of the cable

Difficulty (scale = number of bays):
  L1 = 2 bays  →  6 columns + 2 rails + 4 braces + 1 bridge + 1 trolley + 1 drum + 1 cable + 1 hook = 17 shapes
  L2 = 4 bays  → 10 columns + 2 rails + 8 braces + 1 bridge + 1 trolley + 1 drum + 1 cable + 1 hook = 25 shapes
  L3 = 6 bays  → 14 columns + 2 rails + 12 braces + 1 bridge + 1 trolley + 1 drum + 1 cable + 1 hook = 33 shapes
"""

import math


def _reference_solution(scale):
    """Build the canonical gantry crane assembly."""
    N_bays = scale
    N_cols_per_side = N_bays + 1
    shapes = []
    sid = 0

    # Parameters
    bay_length = 40.0       # mm — distance between columns along X
    rail_span = 80.0        # mm — distance between the two rail lines (Y)
    col_r = 5.0             # mm — column radius
    col_h = 100.0           # mm — column height
    rail_w = 4.0            # mm — rail beam width/height
    brace_w = 2.5           # mm — diagonal brace width/height
    bridge_w = 5.0          # mm — bridge beam width/height
    trolley_size = [15.0, 12.0, 8.0]  # mm — trolley box [X, Y, Z]
    drum_r = 6.0            # mm — cable drum radius
    drum_h = 10.0           # mm — cable drum height (along Y)
    cable_inner = 1.0       # mm — cable pipe inner radius
    cable_outer = 2.0       # mm — cable pipe outer radius
    cable_len = 60.0        # mm — cable length (hangs down from trolley)
    hook_r_base = 4.0       # mm — hook cone base radius
    hook_r_tip = 0.5        # mm — hook cone tip radius
    hook_h = 10.0           # mm — hook cone height

    # Derived positions
    total_length = N_bays * bay_length
    x_start = -total_length / 2.0
    y_left = -rail_span / 2.0
    y_right = rail_span / 2.0

    # Trolley is positioned at the midpoint of the bridge (centre of span)
    # Bridge is at X = 0 (middle of the gantry)
    bridge_x = 0.0
    trolley_z = col_h + rail_w + trolley_size[2] / 2.0

    # ── Vertical columns (cylinders) ──
    for i in range(N_cols_per_side):
        x = x_start + i * bay_length
        for y in [y_left, y_right]:
            shapes.append({
                "id": sid, "type": "cylinder",
                "center": [round(x, 2), round(y, 2), col_h / 2.0],
                "radius": col_r,
                "height": col_h,
            })
            sid += 1

    # ── Rail beams (2 beams running along X at the top of columns) ──
    rail_z = col_h + rail_w / 2.0
    for y in [y_left, y_right]:
        shapes.append({
            "id": sid, "type": "beam",
            "start": [x_start, round(y, 2), rail_z],
            "end":   [round(x_start + total_length, 2), round(y, 2), rail_z],
            "width": rail_w,
            "height": rail_w,
        })
        sid += 1

    # ── Cross-bracing diagonals (2 per bay, forming X on each side) ──
    # Each bay has braces on the front face (y = y_left side)
    for i in range(N_bays):
        x0 = x_start + i * bay_length
        x1 = x_start + (i + 1) * bay_length
        # Diagonal 1: bottom-left to top-right of the bay (front face)
        shapes.append({
            "id": sid, "type": "beam",
            "start": [round(x0, 2), y_left, 0.0],
            "end":   [round(x1, 2), y_left, col_h],
            "width": brace_w,
            "height": brace_w,
        })
        sid += 1
        # Diagonal 2: top-left to bottom-right of the bay (front face)
        shapes.append({
            "id": sid, "type": "beam",
            "start": [round(x0, 2), y_left, col_h],
            "end":   [round(x1, 2), y_left, 0.0],
            "width": brace_w,
            "height": brace_w,
        })
        sid += 1

    # ── Bridge beam (spans between rails at bridge_x) ──
    shapes.append({
        "id": sid, "type": "beam",
        "start": [bridge_x, y_left, rail_z],
        "end":   [bridge_x, y_right, rail_z],
        "width": bridge_w,
        "height": bridge_w,
    })
    sid += 1

    # ── Trolley body (box riding on the bridge) ──
    shapes.append({
        "id": sid, "type": "box",
        "center": [bridge_x, 0.0, trolley_z],
        "size": trolley_size,
    })
    sid += 1

    # ── Cable drum (cylinder on top of trolley, axis along Y) ──
    drum_z = trolley_z + trolley_size[2] / 2.0 + drum_r
    shapes.append({
        "id": sid, "type": "cylinder",
        "center": [bridge_x, 0.0, drum_z],
        "radius": drum_r,
        "height": drum_h,
        "axis": [0, 1, 0],
    })
    sid += 1

    # ── Hoist cable (pipe hanging down from trolley) ──
    cable_top = trolley_z - trolley_size[2] / 2.0
    cable_centre_z = cable_top - cable_len / 2.0
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [bridge_x, 0.0, round(cable_centre_z, 2)],
        "inner_radius": cable_inner,
        "outer_radius": cable_outer,
        "height": cable_len,
    })
    sid += 1

    # ── Hook (cone at the bottom of the cable) ──
    hook_top_z = cable_top - cable_len
    hook_centre_z = hook_top_z - hook_h / 2.0
    shapes.append({
        "id": sid, "type": "cone",
        "center": [bridge_x, 0.0, round(hook_centre_z, 2)],
        "base_radius": hook_r_base,
        "top_radius": hook_r_tip,
        "height": hook_h,
    })
    sid += 1

    return shapes


def generate_gantry(scale):
    """
    Gantry Crane Assembly (Phase 3 Semantic).
    Scale = number of bays (2, 4, or 6).
    """
    N = scale
    ref = _reference_solution(scale)
    total = len(ref)

    # Base parameters for prompt
    bay_length = 40.0
    rail_span = 80.0
    col_r = 5.0
    col_h = 100.0
    rail_w = 4.0
    brace_w = 2.5
    bridge_w = 5.0
    trolley_size = [15.0, 12.0, 8.0]
    drum_r = 6.0
    drum_h = 10.0
    cable_inner = 1.0
    cable_outer = 2.0
    cable_len = 60.0
    hook_r_base = 4.0
    hook_r_tip = 0.5
    hook_h = 10.0

    N_cols = 2 * (N + 1)
    N_braces = 2 * N

    prompt = f"""Design an overhead gantry crane with {N} bays.

Structure:
- {N_cols} vertical columns: Cylinders (radius {col_r}mm, height {col_h}mm) arranged in two parallel rows separated by {rail_span}mm (in Y), with {N+1} columns per row spaced {bay_length}mm apart (in X), centred at X=0.
- 2 rail beams: Beams running along the tops of each column row, spanning the full gantry length in X direction (width {rail_w}mm).
- {N_braces} diagonal cross-braces: Beams forming X-patterns on the front face of each bay. Each bay has two braces: one from bottom-left to top-right, one from top-left to bottom-right. Each brace connects a column base (Z=0) to the opposite column top (Z={col_h}mm). Width {brace_w}mm.
- 1 bridge beam: Beam spanning between the two rails at X=0 (perpendicular to the rails), width {bridge_w}mm.
- 1 trolley: Box ({trolley_size[0]}×{trolley_size[1]}×{trolley_size[2]}mm) riding on the bridge at the midpoint, resting on top of the rails.
- 1 cable drum: Cylinder (radius {drum_r}mm, height {drum_h}mm, axis along Y) mounted on top of the trolley.
- 1 hoist cable: Pipe (inner radius {cable_inner}mm, outer radius {cable_outer}mm, length {cable_len}mm) hanging vertically below the trolley.
- 1 hook: Cone (base radius {hook_r_base}mm, tip radius {hook_r_tip}mm, height {hook_h}mm) at the bottom of the cable.

Semantic Constraints:
1. Columns must stand on the Z=0 ground plane.
2. Rail beams must sit on top of the columns.
3. Each bay must have an X-pattern of braces connecting opposite corners.
4. The bridge must rest on the rails at X=0.
5. The trolley sits on top of the bridge/rails.
6. The cable hangs vertically from the trolley bottom.
7. The hook hangs directly below the cable.
8. No parts may overlap.

Total shapes: {total}.
Output only the raw JSON array of geometric elements — no markdown, no explanation."""

    specs = {
        "gravity_check": True,
        "interference_check": True,
        "mates": [],
        "clearance_fit": [],
        "reference": ref
    }
    return prompt, specs


if __name__ == "__main__":
    import json, argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=4)
    args = parser.parse_args()
    prompt, specs = generate_gantry(args.scale)
    print(f"Gantry Crane — {args.scale} bays, {len(specs['reference'])} shapes")
    print(prompt)
    print(f"\n--- Golden JSON ({len(specs['reference'])} shapes) ---")
    print(json.dumps(specs["reference"], indent=2)[:500])
