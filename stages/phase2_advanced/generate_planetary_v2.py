import math

def generate_planetary(scale):
    """
    Planetary Gear Array (Difficulty Level 2+ of Phase 2)
    Scale defines the number of planet gears.
    """
    n_planets = scale
    
    prompt = f"""Place a central sun cylinder with `Radius=10` and `Height=2` located exactly at the origin `[0,0,0]`.
Place exactly {n_planets} planet cylinders, each with `Radius=3` and `Height=2`.
The planets must perfectly tangentially rest against the outer surface of the sun cylinder on the XY plane — each planet's circular face must just touch the sun's circular face with zero overlap and zero gap.
The planets must be evenly angularly distributed around the sun cylinder in a perfect circle, with the first planet (Planet 0) centered exactly on the positive X-axis."""

    shapes = []
    shapes.append({
        "id": 0, "type": "cylinder", 
        "center": [0,0,0], "radius": 10, "height": 2, "axis": [0,0,1]
    })
    
    sid = 1
    dist = 13.0
    for i in range(n_planets):
        angle = (2 * math.pi * i) / n_planets
        x = dist * math.cos(angle)
        y = dist * math.sin(angle)
        shapes.append({
            "id": sid, "type": "cylinder", 
            "center": [round(x, 4), round(y, 4), 0], 
            "radius": 3, "height": 2, "axis": [0,0,1]
        })
        sid += 1

    return prompt, shapes
