"""
Honeycomb Lattice — Phase 4 Bio-Inspired
==========================================
Models a bee honeycomb: a hexagonal tiling of prismatic cells
arranged in concentric rings around a central cell, standing on
a base plate and enclosed by a frame ring.

Structural complexity (what makes this HARD):
  1. Hex ring algorithm — axial coordinates with pointy-top orientation
  2. Tilted cells — each cell axis is inclined 13° from vertical toward
     the comb centre (like real bee cells), requiring per-cell axis vectors
  3. Shared hex walls — beam segments connect each pair of adjacent cell
     centres, testing topological adjacency detection
  4. Reinforcement ribs — radial beams from centre to frame perimeter,
     one per ring-1 corner, testing angular placement
  5. Bottom caps — cone-shaped wax closures at the cell base,
     axis matching cell tilt, testing multi-type variety

The LLM must:
  • Compute hex axial coordinates and convert to Cartesian
  • Derive per-cell tilt axis (pointing inward toward centre)
  • Enumerate all unique adjacent pairs for wall beams
  • Place 6 evenly-spaced radial ribs
  • Keep base plate, frame torus, and all pieces connected

Difficulty (scale = number of concentric rings):
  L1 = 2 rings →  19 cells + walls + ribs + caps  = ~100 shapes
  L2 = 3 rings →  37 cells + walls + ribs + caps  = ~190 shapes
  L3 = 4 rings →  61 cells + walls + ribs + caps  = ~310 shapes
"""

import math


def _hex_ring_coords(ring):
    """Return list of (q, r) axial coordinates for a hex ring of given radius.

    Uses the standard ring-walk algorithm (Red Blob Games):
      - Start at cube coord (0, -ring, +ring) → axial (0, -ring)
      - Walk 6 edges, each edge has `ring` steps
      - Directions (axial): (+1,0), (0,+1), (-1,+1), (-1,0), (0,-1), (+1,-1)
    """
    if ring == 0:
        return [(0, 0)]
    coords = []
    directions = [
        (1, 0), (0, 1), (-1, 1),
        (-1, 0), (0, -1), (1, -1)
    ]
    q, r = 0, -ring
    for dq, dr in directions:
        for _ in range(ring):
            coords.append((q, r))
            q += dq
            r += dr
    return coords


def _hex_neighbours(q, r):
    """Return the 6 axial neighbours of hex cell (q, r)."""
    return [
        (q+1, r), (q-1, r), (q, r+1),
        (q, r-1), (q+1, r-1), (q-1, r+1)
    ]


def generate_honeycomb(scale):
    """
    Honeycomb Lattice (Phase 4 Bio-Inspired).
    Scale = number of concentric rings (2, 3, or 4).
    """
    N_rings = scale
    cell_outer_r = 5.0       # mm — cell outer radius (pipe outer)
    cell_inner_r = 4.2       # mm — cell inner radius (pipe inner)
    cell_height  = 12.0      # mm — cell depth (Z)
    base_thick   = 1.5       # mm — base plate thickness
    frame_thick  = 2.0       # mm — frame wall thickness
    cap_thick    = 0.8       # mm — cap cylinder lid thickness
    cone_height  = 3.0       # mm — bottom wax cone height
    tilt_deg     = 13.0      # degrees — cell tilt toward centre (real bee comb ≈ 9-13°)
    wall_width   = 1.0       # mm — wall beam width
    rib_width    = 1.5       # mm — reinforcement rib beam width
    n_ribs       = 6         # radial ribs (one per hex corner direction)

    tilt_rad = math.radians(tilt_deg)

    # Hex size: adjacent centres separated by 2 × cell_outer_r = 10mm.
    # For pointy-top: √3 × size = centre_distance → size = 10/√3
    hex_size = (2.0 * cell_outer_r) / math.sqrt(3)  # ≈ 5.7735 mm

    shapes = []
    sid = 0

    # Collect all cell centres and build coord→index map
    all_qr = []
    for ring in range(N_rings + 1):
        for q, r in _hex_ring_coords(ring):
            all_qr.append((q, r))
    qr_set = set(all_qr)

    def qr_to_xy(q, r):
        x = hex_size * math.sqrt(3) * (q + r / 2.0)
        y = hex_size * (3.0 / 2.0) * r
        return (round(x, 4), round(y, 4))

    cell_centres = [qr_to_xy(q, r) for q, r in all_qr]
    n_cells = len(cell_centres)

    # ── Compute per-cell tilt axis ────────────────────────────────
    # Each cell tilts 13° inward toward (0,0).  The tilt axis is
    # perpendicular to the radial direction in the XY plane.
    # For centre cell (0,0): no tilt (vertical).
    def cell_axis(cx, cy):
        dist = math.sqrt(cx*cx + cy*cy)
        if dist < 0.01:
            return [0.0, 0.0, 1.0]  # centre cell: vertical
        # Radial unit vector from centre to cell
        rx, ry = cx / dist, cy / dist
        # Tilt the Z-axis toward centre by tilt_deg
        az = math.cos(tilt_rad)
        a_radial = -math.sin(tilt_rad)  # negative = toward centre
        ax = a_radial * rx
        ay = a_radial * ry
        mag = math.sqrt(ax*ax + ay*ay + az*az)
        return [round(ax/mag, 6), round(ay/mag, 6), round(az/mag, 6)]

    cell_axes = [cell_axis(cx, cy) for cx, cy in cell_centres]

    # ── Max extent for base plate and frame ───────────────────────
    max_extent = (2.0 * cell_outer_r) * (N_rings + 0.5) + cell_outer_r

    # ── Base plate (flat cylinder underneath all cells) ───────────
    shapes.append({
        "id": sid, "type": "cylinder",
        "center": [0.0, 0.0, -base_thick / 2.0],
        "radius": round(max_extent, 2),
        "height": base_thick,
        "axis": [0, 0, 1]
    })
    sid += 1

    # ── Frame ring (torus around the perimeter) ──────────────────
    shapes.append({
        "id": sid, "type": "torus",
        "center": [0.0, 0.0, cell_height / 2.0],
        "ring_radius": round(max_extent, 2),
        "tube_radius": frame_thick,
        "axis": [0, 0, 1]
    })
    sid += 1

    # ── Honeycomb cells (pipes, tilted) ──────────────────────────
    for i, (cx, cy) in enumerate(cell_centres):
        ax = cell_axes[i]
        shapes.append({
            "id": sid, "type": "pipe",
            "center": [cx, cy, cell_height / 2.0],
            "inner_radius": cell_inner_r,
            "outer_radius": cell_outer_r,
            "height": cell_height,
            "axis": ax
        })
        sid += 1

    # ── Top caps (cylinder lids on top of each cell) ─────────────
    for i, (cx, cy) in enumerate(cell_centres):
        ax = cell_axes[i]
        shapes.append({
            "id": sid, "type": "cylinder",
            "center": [cx, cy, cell_height + cap_thick / 2.0],
            "radius": cell_inner_r,
            "height": cap_thick,
            "axis": ax
        })
        sid += 1

    # ── Bottom cones (wax closures at cell base) ─────────────────
    for i, (cx, cy) in enumerate(cell_centres):
        ax = cell_axes[i]
        shapes.append({
            "id": sid, "type": "cone",
            "center": [cx, cy, -base_thick - cone_height / 2.0],
            "base_radius": cell_inner_r,
            "top_radius": 0.0,
            "height": cone_height,
            "axis": ax
        })
        sid += 1

    # ── Shared hex walls (beams between adjacent cell centres) ────
    # Enumerate unique adjacent pairs: for each cell, check its 6
    # neighbours; only add beam if neighbour has higher index to
    # avoid duplicates.
    qr_to_idx = {qr: i for i, qr in enumerate(all_qr)}
    wall_pairs = []
    for i, (q, r) in enumerate(all_qr):
        for nq, nr in _hex_neighbours(q, r):
            if (nq, nr) in qr_set:
                j = qr_to_idx[(nq, nr)]
                if j > i:
                    wall_pairs.append((i, j))

    wall_z = cell_height / 2.0  # walls at mid-height
    for i, j in wall_pairs:
        cx1, cy1 = cell_centres[i]
        cx2, cy2 = cell_centres[j]
        shapes.append({
            "id": sid, "type": "beam",
            "start": [cx1, cy1, wall_z],
            "end": [cx2, cy2, wall_z],
            "width": wall_width
        })
        sid += 1

    n_walls = len(wall_pairs)

    # ── Reinforcement ribs (radial beams from centre to frame) ────
    # 6 radial ribs at 60° intervals
    rib_z = cell_height * 0.75  # placed at 3/4 height
    rib_endpoints = []
    for k in range(n_ribs):
        angle = k * (2.0 * math.pi / n_ribs)
        ex = round(max_extent * math.cos(angle), 4)
        ey = round(max_extent * math.sin(angle), 4)
        rib_endpoints.append((ex, ey))
        shapes.append({
            "id": sid, "type": "beam",
            "start": [0.0, 0.0, rib_z],
            "end": [ex, ey, rib_z],
            "width": rib_width
        })
        sid += 1

    total_shapes = len(shapes)
    # Breakdown: 1 base + 1 frame + n_cells pipes + n_cells caps
    #          + n_cells cones + n_walls wall beams + 6 rib beams

    # ── Prompt ────────────────────────────────────────────────────
    prompt = f"""Model a honeycomb lattice: a hexagonal grid of {n_cells} prismatic cells arranged in {N_rings} concentric ring(s) around a central cell, with structural reinforcement.

HEXAGONAL GRID — pointy-top axial coordinates (q, r):
  Ring 0 (centre): 1 cell at (q=0, r=0).
  Ring k (k=1..{N_rings}): 6k cells.  Start at (q=0, r=−k), walk 6 edges
  with directions [(+1,0), (0,+1), (−1,+1), (−1,0), (0,−1), (+1,−1)],
  each edge has k steps.
  Total cells: 1 + 3×{N_rings}×({N_rings}+1) = {n_cells}.

  Pointy-top axial → Cartesian with size = {round(hex_size, 4)}mm:
    x = √3 × size × (q + r/2)
    y = 3/2 × size × r
  Adjacent cell centres are exactly {2.0 * cell_outer_r}mm apart.

CELL TILT — each cell axis is inclined {tilt_deg}° inward toward the comb centre:
  For cell at (cx, cy), the radial direction is (cx, cy)/||(cx, cy)||.
  The axis tilts from [0,0,1] toward −radial by {tilt_deg}°:
    axis = [−sin({tilt_deg}°)×rx, −sin({tilt_deg}°)×ry, cos({tilt_deg}°)]
  (normalised). Centre cell (0,0) stays vertical: axis = [0,0,1].

COMPONENTS:
  1. Honeycomb cells: {n_cells} pipes at z={cell_height/2.0}
     inner_radius={cell_inner_r}mm, outer_radius={cell_outer_r}mm,
     height={cell_height}mm, axis=per-cell tilt axis.

  2. Top caps: {n_cells} cylinders at z={cell_height + cap_thick/2.0}
     radius={cell_inner_r}mm, height={cap_thick}mm, axis=per-cell tilt axis.

  3. Bottom cones: {n_cells} cones at z={-base_thick - cone_height/2.0}
     base_radius={cell_inner_r}mm, top_radius=0, height={cone_height}mm,
     axis=per-cell tilt axis.

  4. Shared hex walls: {n_walls} beams connecting each pair of adjacent
     cell centres at z={wall_z}. Width={wall_width}mm.
     Adjacent pairs: for each cell, check its 6 hex neighbours
     [(q+1,r),(q−1,r),(q,r+1),(q,r−1),(q+1,r−1),(q−1,r+1)].
     Only include pairs where both cells exist in the grid.

  5. Reinforcement ribs: {n_ribs} beams from [0,0,{rib_z}] to perimeter
     at 60° intervals (0°, 60°, 120°, 180°, 240°, 300°).
     End points at radius={round(max_extent, 2)}mm. Width={rib_width}mm.

  6. Base plate: 1 cylinder at [0,0,{-base_thick/2.0}],
     radius={round(max_extent, 2)}mm, height={base_thick}mm, axis=[0,0,1].

  7. Frame ring: 1 torus at [0,0,{cell_height/2.0}],
     ring_radius={round(max_extent, 2)}mm, tube_radius={frame_thick}mm,
     axis=[0,0,1].

Total shapes: {total_shapes} (1 base + 1 frame + {n_cells} pipes + {n_cells} caps + {n_cells} cones + {n_walls} wall beams + {n_ribs} rib beams).

Output only the raw JSON array — no markdown, no explanation."""

    return prompt, shapes


if __name__ == "__main__":
    import json, argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=2)
    args = parser.parse_args()
    prompt, shapes = generate_honeycomb(args.scale)
    print(f"Honeycomb Lattice — {args.scale} ring(s), {len(shapes)} shapes")
    print(prompt)
    with open("honeycomb_golden.json", "w") as f:
        json.dump(shapes, f, indent=2)
