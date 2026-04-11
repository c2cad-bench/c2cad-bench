"""
Diatom Frustule — Phase 4 Bio-Inspired (Family 3)
====================================================
Models a pennate diatom frustule (siliceous exoskeleton) with
bilateral radial symmetry, the defining structure of single-celled
photosynthetic algae.

Biological function: The frustule is a two-piece silica shell that
protects the cell while allowing nutrient/gas exchange through
precisely arranged pores (areolae) and providing structural rigidity
via longitudinal ribs (costae). The raphe slit enables motility.

Structure (cross-section: pill-shaped):
  • Two valves (top & bottom) — flat box lids with rounded edges
  • Raphe slit (central longitudinal groove) — beam along the
    long axis of each valve
  • Costae (transverse ribs) — evenly spaced cylinders radiating
    from the raphe to the valve margin, perpendicular to the long axis
  • Areolae (pores) — small spheres at regular positions between costae
  • Girdle bands — torus rings connecting the two valves at the margin
  • Central nodule — sphere at the geometric centre

Shape types used: box (valves), beam (raphe), cylinder (costae),
sphere (areolae + nodule), torus (girdle bands), pipe (mantle wall)

Difficulty (scale = number of costae per half-valve):
  L1 = 4 costae/half  →  ~34 shapes   (compact, easy to verify)
  L2 = 7 costae/half  →  ~58 shapes   (medium detail)
  L3 = 10 costae/half → ~82 shapes   (high detail, many parts)

Errors are extremely visible:
  • Asymmetric costae → one side looks different from the other
  • Irregular spacing → ribs bunch up or leave gaps
  • Misaligned areolae → pores wander off the grid
  • Girdle bands at wrong Z → valves float apart
  • Wrong raphe length → slit overshoots or undershoots valve
"""

import math


def generate_diatom(scale):
    """
    Diatom Frustule (Phase 4 Bio-Inspired).
    Scale = number of costae per half-valve (one side of the raphe).
    Total costae = 2 × scale per valve × 2 valves = 4 × scale.
    """
    N = scale  # costae per half-valve

    # ── Dimensions (mm) ──────────────────────────────────────
    valve_length = 80.0                # long axis (X)
    valve_width  = 30.0                # short axis (Y)
    valve_thick  = 3.0                 # thickness (Z) of each valve box
    gap          = 8.0                 # space between the two valves
    costa_r      = 1.0                 # cylinder radius for each costa
    costa_len    = (valve_width / 2) - 2.0  # radial length from raphe to margin
    raphe_width  = 1.5                 # raphe beam cross-section
    areola_r     = 0.8                 # pore sphere radius
    girdle_R     = valve_width / 2     # girdle torus major radius
    girdle_r     = 1.2                 # girdle torus tube radius
    nodule_r     = 2.5                 # central nodule sphere radius
    mantle_ri    = valve_width / 2 - 2.0  # mantle pipe inner radius
    mantle_ro    = valve_width / 2       # mantle pipe outer radius
    mantle_h     = gap                 # mantle height = inter-valve gap

    # Valve Z positions
    z_top    =  gap / 2 + valve_thick / 2   # top valve centre Z
    z_bot    = -gap / 2 - valve_thick / 2   # bottom valve centre Z
    z_mid    =  0.0                         # mid-plane between valves

    # Costa X positions — evenly spaced along the valve length
    usable_len = valve_length - 4.0  # leave 2mm margin each end
    costa_spacing = usable_len / (2 * N)  # spacing between successive costae

    shapes = []
    sid = 0

    # ── 1. Central nodule (sphere at origin) ─────────────────
    shapes.append({
        "id": sid, "type": "sphere",
        "center": [0.0, 0.0, z_mid],
        "radius": nodule_r
    })
    sid += 1

    # ── 2. Top valve (box) ───────────────────────────────────
    shapes.append({
        "id": sid, "type": "box",
        "center": [0.0, 0.0, z_top],
        "size": [valve_length, valve_width, valve_thick]
    })
    sid += 1

    # ── 3. Bottom valve (box) ────────────────────────────────
    shapes.append({
        "id": sid, "type": "box",
        "center": [0.0, 0.0, z_bot],
        "size": [valve_length, valve_width, valve_thick]
    })
    sid += 1

    # ── 4. Top raphe (beam along X on top valve) ─────────────
    rx_start = -valve_length / 2 + 2.0
    rx_end   =  valve_length / 2 - 2.0
    shapes.append({
        "id": sid, "type": "beam",
        "start": [rx_start, 0.0, z_top],
        "end":   [rx_end,   0.0, z_top],
        "width": raphe_width, "height": raphe_width
    })
    sid += 1

    # ── 5. Bottom raphe (beam along X on bottom valve) ───────
    shapes.append({
        "id": sid, "type": "beam",
        "start": [rx_start, 0.0, z_bot],
        "end":   [rx_end,   0.0, z_bot],
        "width": raphe_width, "height": raphe_width
    })
    sid += 1

    # ── 6. Mantle wall (pipe connecting the two valves) ──────
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [0.0, 0.0, z_mid],
        "inner_radius": mantle_ri,
        "outer_radius": mantle_ro,
        "height": mantle_h,
        "axis": [0, 0, 1]
    })
    sid += 1

    # ── 7. Girdle bands (2 torus rings at valve margins) ─────
    for gz in [gap / 2, -gap / 2]:
        shapes.append({
            "id": sid, "type": "torus",
            "center": [0.0, 0.0, round(gz, 4)],
            "ring_radius": girdle_R,
            "tube_radius": girdle_r,
            "axis": [0, 0, 1]
        })
        sid += 1

    n_support = sid  # number of supporting structures

    # ── 8. Costae — transverse ribs on each valve ────────────
    # For each valve (top & bottom), for each side of raphe (+Y, -Y),
    # place N costae as cylinders perpendicular to the raphe (Y-axis).
    for valve_z in [z_top, z_bot]:
        for half_idx, y_sign in enumerate([1, -1]):
            for k in range(1, N + 1):
                # X position: symmetric about centre, spaced by costa_spacing
                x_pos = k * costa_spacing
                for x_sign in [1, -1]:
                    cx = round(x_sign * x_pos, 4)
                    cy = round(y_sign * costa_len / 2, 4)
                    cz = round(valve_z, 4)
                    shapes.append({
                        "id": sid, "type": "cylinder",
                        "center": [cx, cy, cz],
                        "radius": costa_r,
                        "height": round(costa_len, 4),
                        "axis": [0, 1, 0]  # along Y
                    })
                    sid += 1

    n_costae = sid - n_support

    # ── 9. Areolae — pores between costae ────────────────────
    # Place small spheres midway between adjacent costae on each valve
    n_areolae = 0
    for valve_z in [z_top, z_bot]:
        for y_sign in [1, -1]:
            # Place areolae at half-costa positions along Y
            y_pos = y_sign * costa_len * 0.5
            for k in range(N):
                # Midpoint between costa k and costa k+1
                x_mid = (k + 0.5) * costa_spacing
                for x_sign in [1, -1]:
                    shapes.append({
                        "id": sid, "type": "sphere",
                        "center": [round(x_sign * x_mid, 4),
                                   round(y_pos, 4),
                                   round(valve_z, 4)],
                        "radius": areola_r
                    })
                    sid += 1
                    n_areolae += 1

    total = len(shapes)

    # ── Prompt ────────────────────────────────────────────────
    prompt = f"""Model a pennate diatom frustule (siliceous exoskeleton) with bilateral symmetry and {N} transverse costae per half-valve.

Overall dimensions: valve length {valve_length}mm (X-axis), valve width {valve_width}mm (Y-axis).

Support structures ({n_support} shapes):
  • ID 0: Central nodule — sphere at [0, 0, 0], radius {nodule_r}mm.
  • ID 1: Top valve — box at [0, 0, {z_top}], size [{valve_length}, {valve_width}, {valve_thick}]mm.
  • ID 2: Bottom valve — box at [0, 0, {z_bot}], size [{valve_length}, {valve_width}, {valve_thick}]mm.
  • ID 3: Top raphe slit — beam from [{rx_start}, 0, {z_top}] to [{rx_end}, 0, {z_top}], cross-section {raphe_width}mm.
  • ID 4: Bottom raphe slit — beam from [{rx_start}, 0, {z_bot}] to [{rx_end}, 0, {z_bot}], cross-section {raphe_width}mm.
  • ID 5: Mantle wall — pipe at origin, inner radius {mantle_ri}mm, outer radius {mantle_ro}mm, height {mantle_h}mm, Z-axis.
  • ID 6-7: Girdle bands — 2 torus rings at Z={gap/2}mm and Z={-gap/2}mm, ring radius {girdle_R}mm, tube radius {girdle_r}mm.

Costae ({n_costae} cylinders): Transverse ribs on each valve, perpendicular to the raphe.
  On each valve (top & bottom), on each side of the raphe (+Y and -Y), place {N} costae.
  Each costa is a cylinder with radius {costa_r}mm, height {costa_len:.1f}mm, axis along Y.
  X positions: k × {costa_spacing:.2f}mm for k=1…{N}, mirrored on both +X and -X sides.
  Total costae: 2 valves × 2 sides × {N} × 2 (±X mirror) = {n_costae}.

Areolae ({n_areolae} spheres): Small pores between costae.
  Spheres of radius {areola_r}mm placed midway between adjacent costae (at x = (k+0.5)×{costa_spacing:.2f}mm) at Y = ±{costa_len * 0.5:.1f}mm on each valve.

Total shapes: {total} ({n_support} supports + {n_costae} costae + {n_areolae} areolae).

Output only the raw JSON array of geometric elements — no markdown, no explanation."""

    return prompt, shapes


if __name__ == "__main__":
    import json, argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=4)
    args = parser.parse_args()
    prompt, shapes = generate_diatom(args.scale)
    print(f"Diatom Frustule — {args.scale} costae/half, {len(shapes)} shapes")
    print(prompt)
