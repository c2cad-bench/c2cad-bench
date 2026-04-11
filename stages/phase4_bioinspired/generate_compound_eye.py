"""
Compound Eye Array — Phase 4 Bio-Inspired (Family 2)
======================================================
Models an insect compound eye: a hemispherical dome covered with
ommatidia (individual optical units) arranged in concentric rings.

Each ommatidium consists of:
  • A corneal lens (sphere) on the dome surface
  • A crystalline cone (cone) pointing inward toward the focal centre
  • A rhabdom light-guide (cylinder) connecting cone tip to optic nerve

Supporting structure:
  • Dome shell (hemisphere — approximated as a large sphere)
  • Optic nerve bundle (pipe) at the base
  • Mounting ring (torus) at the equator

Biological function: Each ommatidium captures light from a slightly
different direction (determined by its position on the dome). The
angular separation between adjacent ommatidia determines visual
acuity. The LLM must compute spherical coordinates for every unit.

Difficulty (scale = number of concentric rings):
  L1 = 2 rings →  1+6       =  7 ommatidia × 3 + 3 supports =  24 shapes
  L2 = 3 rings →  1+6+12    = 19 ommatidia × 3 + 3 supports =  60 shapes
  L3 = 4 rings →  1+6+12+18 = 37 ommatidia × 3 + 3 supports = 114 shapes

Errors are extremely visible:
  • Wrong angular spacing → ommatidia cluster or leave gaps on dome
  • Misaligned cones → don't point toward focal centre (visual axes diverge)
  • Size gradient wrong → outer ring lenses too big/small
  • Missing ring → visible bald patch on hemisphere
"""

import math


def generate_compound_eye(scale):
    """
    Compound Eye Array (Phase 4 Bio-Inspired).
    Scale = number of concentric rings around the central ommatidium.
    """
    N_rings = scale
    dome_R      = 50.0      # mm — dome hemisphere radius
    lens_r      = 4.0       # mm — corneal lens sphere radius
    cone_h      = 12.0      # mm — crystalline cone height
    cone_r_base = 3.5       # mm — cone base radius (at lens)
    cone_r_tip  = 0.8       # mm — cone tip radius
    rhabdom_r   = 0.8       # mm — rhabdom cylinder radius
    rhabdom_h   = 10.0      # mm — rhabdom length
    nerve_r_in  = 5.0       # mm — optic nerve pipe inner radius
    nerve_r_out = 7.0       # mm — optic nerve pipe outer radius
    nerve_h     = 20.0      # mm — optic nerve length below dome
    torus_R     = dome_R    # mm — mounting ring major radius
    torus_r     = 3.0       # mm — mounting ring tube radius

    shapes = []
    sid = 0

    # ── Supporting structures ─────────────────────────────────

    # ID 0: Dome shell (sphere representing the hemisphere)
    shapes.append({
        "id": sid, "type": "sphere",
        "center": [0.0, 0.0, 0.0],
        "radius": dome_R
    })
    sid += 1

    # ID 1: Optic nerve bundle (pipe at base, extending downward)
    shapes.append({
        "id": sid, "type": "pipe",
        "center": [0.0, 0.0, -(nerve_h / 2.0)],
        "inner_radius": nerve_r_in,
        "outer_radius": nerve_r_out,
        "height": nerve_h,
        "axis": [0, 0, 1]
    })
    sid += 1

    # ID 2: Mounting ring (torus at equator)
    shapes.append({
        "id": sid, "type": "torus",
        "center": [0.0, 0.0, 0.0],
        "ring_radius": torus_R,
        "tube_radius": torus_r,
        "axis": [0, 0, 1]
    })
    sid += 1

    # ── Ommatidia — concentric rings on upper hemisphere ──────
    # Ring 0: single ommatidium at the pole (zenith)
    # Ring k: 6*k ommatidia equally spaced at polar angle θ_k

    def _add_ommatidium(theta, phi):
        """Place one ommatidium at spherical coords (theta=polar, phi=azimuthal).
        Returns number of shapes added."""
        nonlocal sid

        # Position on dome surface
        st, ct = math.sin(theta), math.cos(theta)
        sp, cp = math.sin(phi), math.cos(phi)

        # Surface point (lens centre, slightly outside dome)
        sx = dome_R * st * cp
        sy = dome_R * st * sp
        sz = dome_R * ct

        # Inward-pointing unit normal (toward dome centre)
        nx, ny, nz = -st * cp, -st * sp, -ct

        # 1) Corneal lens — sphere at dome surface
        shapes.append({
            "id": sid, "type": "sphere",
            "center": [round(sx, 4), round(sy, 4), round(sz, 4)],
            "radius": lens_r
        })
        sid += 1

        # 2) Crystalline cone — just inside the lens, pointing inward
        cone_base = [sx + nx * lens_r, sy + ny * lens_r, sz + nz * lens_r]
        cone_tip  = [sx + nx * (lens_r + cone_h), sy + ny * (lens_r + cone_h),
                     sz + nz * (lens_r + cone_h)]
        cone_center = [round((cone_base[i] + cone_tip[i]) / 2, 4) for i in range(3)]
        shapes.append({
            "id": sid, "type": "cone",
            "center": cone_center,
            "start_radius": round(cone_r_base, 4),
            "end_radius": round(cone_r_tip, 4),
            "height": round(cone_h, 4),
            "axis": [round(nx, 6), round(ny, 6), round(nz, 6)]
        })
        sid += 1

        # 3) Rhabdom light-guide — cylinder continuing inward from cone tip
        rhab_start = cone_tip
        rhab_end = [cone_tip[i] + nx * rhabdom_h if i == 0 else
                    cone_tip[i] + ny * rhabdom_h if i == 1 else
                    cone_tip[i] + nz * rhabdom_h for i in range(3)]
        rhab_center = [round((rhab_start[i] + rhab_end[i]) / 2, 4) for i in range(3)]
        shapes.append({
            "id": sid, "type": "cylinder",
            "center": rhab_center,
            "radius": rhabdom_r,
            "height": rhabdom_h,
            "axis": [round(nx, 6), round(ny, 6), round(nz, 6)]
        })
        sid += 1

    # Ring 0: pole (theta ≈ 0, single unit)
    _add_ommatidium(0.0, 0.0)

    # Rings 1..N_rings
    max_theta = math.radians(70)  # cover upper hemisphere up to 70° from pole
    for ring in range(1, N_rings + 1):
        theta = max_theta * ring / N_rings
        n_in_ring = 6 * ring
        for j in range(n_in_ring):
            phi = 2 * math.pi * j / n_in_ring
            _add_ommatidium(theta, phi)

    # Count ommatidia
    n_omm = 1 + sum(6 * k for k in range(1, N_rings + 1))
    total = 3 + n_omm * 3  # 3 supports + 3 shapes per ommatidium

    # ── Prompt ────────────────────────────────────────────────
    prompt = f"""Model an insect compound eye as a hemispherical dome with {n_omm} ommatidia (optical units) arranged in {N_rings + 1} concentric rings.

Supporting structure (3 shapes):
  • ID 0: Dome shell — sphere at the origin, radius {dome_R}mm.
  • ID 1: Optic nerve bundle — pipe along the -Z axis below the dome, inner radius {nerve_r_in}mm, outer radius {nerve_r_out}mm, height {nerve_h}mm, centred at [0, 0, {-(nerve_h/2.0)}].
  • ID 2: Mounting ring — torus at the dome equator (Z=0), ring radius {torus_R}mm, tube radius {torus_r}mm, axis along Z.

Ommatidia placement — concentric rings on the upper hemisphere:
  Ring 0 (pole): 1 ommatidium at the north pole (θ=0°).
  Ring k (k=1…{N_rings}): exactly 6×k ommatidia equally spaced in azimuth (φ), at polar angle θ_k = {math.degrees(max_theta):.1f}° × k/{N_rings}.
  Total ommatidia: {n_omm} ({' + '.join(str(6*k) if k > 0 else '1' for k in range(N_rings+1))}).

Each ommatidium (at dome surface point [R·sinθ·cosφ, R·sinθ·sinφ, R·cosθ]) consists of 3 shapes pointing inward toward the dome centre:
  a) Corneal lens — sphere of radius {lens_r}mm at the surface point.
  b) Crystalline cone — cone (base radius {cone_r_base}mm, tip radius {cone_r_tip}mm, height {cone_h}mm) just inside the lens, axis pointing inward along the surface normal.
  c) Rhabdom — cylinder (radius {rhabdom_r}mm, height {rhabdom_h}mm) continuing inward from the cone tip along the same axis.

Total shapes: {total} (3 supports + {n_omm} × 3 ommatidia components).
IDs: 0-2 = supports, then groups of 3 per ommatidium (lens, cone, rhabdom).

Output only the raw JSON array of geometric elements — no markdown, no explanation."""

    return prompt, shapes


if __name__ == "__main__":
    import json, argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=2)
    args = parser.parse_args()
    prompt, shapes = generate_compound_eye(args.scale)
    print(f"Compound Eye — {args.scale} rings, {len(shapes)} shapes")
    print(prompt)
