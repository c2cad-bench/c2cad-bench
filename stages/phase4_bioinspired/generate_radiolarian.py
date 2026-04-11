"""
Armillary Sphere — Phase 4 Bio-Inspired
=========================================
Models a nested armillary sphere: concentric celestial frameworks
made of great-circle rings at different orientations, connected by
radial axis rods at icosahedral symmetry points, with equatorial
girdle rings at each shell level.

An armillary sphere is an ancient astronomical instrument representing
celestial coordinate systems with nested rings (horizon, meridian,
equatorial, ecliptic circles).  Our model extends it to multiple
concentric shells, each a wireframe cage of 3 orthogonal great-circle
torus rings (XY, XZ, YZ planes), connected by 12 icosahedral spines.

The LLM must derive:
  • Icosahedral vertex unit vectors (12 vertices):
      (0, ±1, ±φ), (±1, ±φ, 0), (±φ, 0, ±1)   normalised
      where φ = (1+√5)/2 ≈ 1.618
  • Shell radii in geometric progression: r_k = r_base × 2^k
  • Each shell = 3 torus rings (XY, XZ, YZ great circles)
  • Spine segment endpoints on each shell surface
  • Girdle torus placement at each shell equator

Errors are extremely visible:
  • Solid spheres instead of rings → opaque blob hiding inner structure
  • Non-icosahedral spine directions → asymmetric instrument
  • Wrong shell radii → shells too close or too far apart
  • Missing spines → incomplete axis rods
  • Wrong girdle placement → rings floating between shells

Difficulty (scale = number of concentric shells):
  L1 = 2 shells  →  2×3 shell tori + 12×1 spines + 2 girdle tori = ~20 shapes
  L2 = 3 shells  →  3×3 shell tori + 12×2 spines + 3 girdle tori = ~36 shapes
  L3 = 4 shells  →  4×3 shell tori + 12×3 spines + 4 girdle tori = ~52 shapes
"""

import math

PHI = (1 + math.sqrt(5)) / 2  # golden ratio ≈ 1.618

# 12 vertices of a regular icosahedron (normalised to unit sphere)
_RAW_VERTS = [
    ( 0,  1,  PHI), ( 0,  1, -PHI), ( 0, -1,  PHI), ( 0, -1, -PHI),
    ( 1,  PHI,  0), ( 1, -PHI,  0), (-1,  PHI,  0), (-1, -PHI,  0),
    ( PHI,  0,  1), ( PHI,  0, -1), (-PHI,  0,  1), (-PHI,  0, -1),
]
_NORM = math.sqrt(1 + PHI**2)
ICO_VERTICES = [(round(x/_NORM, 6), round(y/_NORM, 6), round(z/_NORM, 6))
                for x, y, z in _RAW_VERTS]


def generate_radiolarian(scale):
    """
    Armillary Sphere (Phase 4 Bio-Inspired).
    Scale = number of concentric shells (2, 3, or 4).
    """
    N_shells = scale
    r_base    = 20.0       # mm — innermost shell radius
    spine_r   = 1.2        # mm — spine cylinder radius
    girdle_r  = 1.5        # mm — girdle torus tube radius
    lattice_r = 1.0        # mm — shell lattice torus tube radius

    shapes = []
    sid = 0

    # Shell radii: r_k = r_base × 2^k  (k = 0, 1, ..., N-1)
    shell_radii = [round(r_base * (2 ** k), 4) for k in range(N_shells)]

    # ── Concentric shells (3 orthogonal torus rings per shell) ──
    # Each shell is represented by 3 great-circle torus rings:
    #   - Equatorial (XY plane): axis = [0, 0, 1]
    #   - Meridional 1 (XZ plane): axis = [0, 1, 0]
    #   - Meridional 2 (YZ plane): axis = [1, 0, 0]
    # This creates a wireframe cage that shows the spherical shape
    # while remaining transparent to reveal inner shells.
    shell_axes = [
        [0, 0, 1],  # XY plane (equatorial)
        [0, 1, 0],  # XZ plane (meridional)
        [1, 0, 0],  # YZ plane (meridional)
    ]
    for k, r in enumerate(shell_radii):
        for ax in shell_axes:
            shapes.append({
                "id": sid, "type": "torus",
                "center": [0.0, 0.0, 0.0],
                "ring_radius": r,
                "tube_radius": lattice_r,
                "axis": ax
            })
            sid += 1

    # ── Girdle rings (thicker torus at each shell equator) ────
    for k, r in enumerate(shell_radii):
        shapes.append({
            "id": sid, "type": "torus",
            "center": [0.0, 0.0, 0.0],
            "ring_radius": r,
            "tube_radius": girdle_r,
            "axis": [0, 0, 1]
        })
        sid += 1

    # ── Radial spines (cylinders between consecutive shells) ──
    # 12 icosahedral directions × (N_shells - 1) inter-shell segments
    for shell_idx in range(N_shells - 1):
        r_inner = shell_radii[shell_idx]
        r_outer = shell_radii[shell_idx + 1]
        seg_len = r_outer - r_inner

        for vi, (vx, vy, vz) in enumerate(ICO_VERTICES):
            # Spine segment from inner shell surface to outer shell surface
            cx = round(vx * (r_inner + r_outer) / 2, 4)
            cy = round(vy * (r_inner + r_outer) / 2, 4)
            cz = round(vz * (r_inner + r_outer) / 2, 4)

            shapes.append({
                "id": sid, "type": "cylinder",
                "center": [cx, cy, cz],
                "radius": spine_r,
                "height": round(seg_len, 4),
                "axis": [round(vx, 6), round(vy, 6), round(vz, 6)]
            })
            sid += 1

    n_shell_tori = N_shells * 3
    n_girdle_tori = N_shells
    n_spines_total = 12 * (N_shells - 1)
    total_shapes = n_shell_tori + n_girdle_tori + n_spines_total

    # ── Prompt ────────────────────────────────────────────────
    ico_str = "  (0, ±1, ±φ),  (±1, ±φ, 0),  (±φ, 0, ±1)   where φ=(1+√5)/2≈1.618"
    prompt = f"""Model an Armillary Sphere: {N_shells} concentric celestial shells made of great-circle rings, connected by 12 axis rods at icosahedral symmetry points.

Concentric shells — 3 orthogonal great-circle torus rings per shell:
  Each shell is a wireframe cage of 3 torus rings (NOT solid spheres):
    - Equatorial ring: axis = [0,0,1]
    - Meridional ring 1: axis = [0,1,0]
    - Meridional ring 2: axis = [1,0,0]
  Shell k (k=0..{N_shells - 1}): ring_radius = {r_base} × 2^k, tube_radius = {lattice_r}mm.
  Radii: {', '.join(f'{r}mm' for r in shell_radii)}.
  Total shell tori: {N_shells} × 3 = {n_shell_tori}.

Girdle rings — thicker equatorial torus at each shell:
  For each shell k, place a torus at [0,0,0] with ring_radius = shell radius,
  tube_radius = {girdle_r}mm, axis = [0,0,1].
  Total: {n_girdle_tori} tori.

Axis rods — 12 cylinders in icosahedral directions between consecutive shells:
  The 12 icosahedral vertex unit vectors (before normalisation) are:
{ico_str}
  Normalise each vector to unit length (divide by √(1+φ²) ≈ {_NORM:.4f}).

  For each consecutive shell pair (k, k+1) and each of the 12 directions v̂:
    rod centre = v̂ × (r_k + r_{{k+1}}) / 2
    rod height = r_{{k+1}} − r_k
    rod radius = {spine_r}mm
    rod axis = v̂  (the normalised icosahedral direction)
  Total rod segments: 12 × {N_shells - 1} = {n_spines_total}.

Total shapes: {total_shapes} ({n_shell_tori} shell tori + {n_girdle_tori} girdle tori + {n_spines_total} axis rod cylinders).

Output only the raw JSON array — no markdown, no explanation."""

    specs = {"reference": shapes}
    return prompt, specs


if __name__ == "__main__":
    import json, argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=2)
    args = parser.parse_args()
    prompt, specs = generate_radiolarian(args.scale)
    shapes = specs["reference"]
    print(f"Armillary Sphere — {args.scale} shells, {len(shapes)} shapes")
    print(prompt)
    with open("radiolarian_golden.json", "w") as f:
        json.dump(shapes, f, indent=2)
