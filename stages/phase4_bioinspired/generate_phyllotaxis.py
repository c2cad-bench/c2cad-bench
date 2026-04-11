"""
Phyllotaxis Disc — Phase 4 Bio-Inspired (Family 1)
====================================================
Models a sunflower seed-head: N spheres arranged in a Fibonacci spiral
pattern using the golden angle (≈ 137.508°).  Each seed is placed at
polar coordinates  r(n) = c·√n ,  θ(n) = n · φ  where φ = 137.508°.

The LLM must derive every coordinate from the golden-angle rule — the
prompt gives only the mathematical principle, seed count, seed radius,
and the spacing constant *c*.  Errors are *immediately* visible: wrong
golden angle produces ugly clumps / spoke lines instead of the smooth
counter-rotating Fibonacci spirals the human eye expects.

Difficulty (scale = number of seeds):
  L1 = 21   (Fibonacci number — 1 parastichy visible)
  L2 = 55   (two clear parastichy families)
  L3 = 89   (three parastichy families, 89 seeds)
"""

import math

GOLDEN_ANGLE_DEG = 137.50776405003785   # 360 / φ²  where φ = (1+√5)/2

def generate_phyllotaxis(scale):
    """
    Phyllotaxis Disc (Difficulty Level 4 — Phase 4 Bio-Inspired).
    Scale = number of seeds (should be a Fibonacci number for clean parastichies).
    """
    N = scale
    seed_radius = 3.0               # mm — each seed sphere
    c = seed_radius * 2.2           # spacing constant  (ensures tangent-near contact)
    disc_base_z = seed_radius       # seeds rest on Z=0 ground (center at Z=radius)

    # ── Build golden array ───────────────────────────────────
    shapes = []

    # ID 0 = central receptacle disc (flat cylinder)
    max_r = c * math.sqrt(N)
    shapes.append({
        "id": 0,
        "type": "cylinder",
        "center": [0.0, 0.0, 0.0],
        "radius": round(max_r + seed_radius * 2, 2),
        "height": 1.0,
        "axis": [0, 0, 1]
    })

    for n in range(1, N + 1):
        theta = math.radians(n * GOLDEN_ANGLE_DEG)
        r     = c * math.sqrt(n)
        x     = round(r * math.cos(theta), 4)
        y     = round(r * math.sin(theta), 4)
        shapes.append({
            "id": n,
            "type": "sphere",
            "center": [x, y, disc_base_z],
            "radius": seed_radius
        })

    # ── Prompt (zero-scaffolding — Laws 1-5) ─────────────────
    prompt = f"""Model a sunflower seed-head disc using the phyllotaxis golden-angle rule.

Place exactly {N} seed spheres (IDs 1–{N}), each of radius {seed_radius}mm, on a flat receptacle disc (cylinder, ID 0) that lies in the XY plane centred at the origin.

Seed placement rule — Fibonacci spiral:
  For seed number n (n = 1, 2, …, {N}):
    angle(n) = n × {GOLDEN_ANGLE_DEG:.4f}°   (the golden angle)
    radius(n) = {c} × √n                      (Fermat spiral spacing)
    x(n) = radius(n) × cos(angle(n))
    y(n) = radius(n) × sin(angle(n))
  Every seed centre sits at Z = {disc_base_z}mm (seeds resting on the receptacle surface).

The receptacle disc (ID 0) is a cylinder of height 1mm centred at the origin, with its axis along Z. Its radius must be large enough to contain all seeds.

Output only the raw JSON array of geometric elements — no markdown, no explanation."""

    return prompt, shapes


if __name__ == "__main__":
    import json, argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=21)
    args = parser.parse_args()
    prompt, shapes = generate_phyllotaxis(args.scale)
    print(f"Phyllotaxis Disc — {args.scale} seeds, {len(shapes)} shapes")
    print(prompt)
    with open("phyllotaxis_golden.json", "w") as f:
        json.dump(shapes, f, indent=2)
