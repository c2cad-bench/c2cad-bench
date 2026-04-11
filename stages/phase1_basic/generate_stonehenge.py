import argparse
import json
import math

def generate_stonehenge(num_arches):
    shapes = []
    pid = 0
    R = 80.0
    pillar_radius = 4.0
    pillar_height = 30.0
    
    dTheta_deg = 3.0 
    arch_spacing_deg = 360.0 / num_arches
    
    for i in range(num_arches):
        theta = i * arch_spacing_deg
        
        # Pillar 1
        t1 = math.radians(theta - dTheta_deg)
        x1 = R * math.cos(t1)
        y1 = R * math.sin(t1)
        z_cyl = pillar_height / 2.0
        shapes.append({
            "id": pid, "type": "cylinder", "radius": pillar_radius, "height": pillar_height,
            "center": [float(x1), float(y1), float(z_cyl)], "axis": [0.0, 0.0, 1.0]
        })
        pid += 1
        
        # Pillar 2
        t2 = math.radians(theta + dTheta_deg)
        x2 = R * math.cos(t2)
        y2 = R * math.sin(t2)
        shapes.append({
            "id": pid, "type": "cylinder", "radius": pillar_radius, "height": pillar_height,
            "center": [float(x2), float(y2), float(z_cyl)], "axis": [0.0, 0.0, 1.0]
        })
        pid += 1
        
        # Header beam connecting top centers
        shapes.append({
            "id": pid, "type": "beam", "width": pillar_radius * 2, "height": pillar_radius * 1.5,
            "start": [float(x1), float(y1), float(pillar_height)],
            "end": [float(x2), float(y2), float(pillar_height)]
        })
        pid += 1

    prompt = f"""Generate a circular Stonehenge-like monument composed of exactly {num_arches} isolated archways arranged in a perfect circle.
The center of the monument is at the origin (0,0,0) and its median radius is exactly {R}mm.
Each arch consists of 3 shapes: 2 upright cylindrical pillars and 1 spanning beam. (Total {pid} shapes).
Pillar dimensions: radius {pillar_radius}mm, height {pillar_height}mm. The pillars stand perfectly vertically, with their bottom bases resting exactly on the Z=0 plane.
Archway placement logic: The {num_arches} arches are distributed equally around the circle (every {arch_spacing_deg} degrees). For a given arch located universally at an angle T, its two isolated pillars are placed exactly at T - {dTheta_deg} degrees and T + {dTheta_deg} degrees on the {R}mm circular path. The first arch is centered at T=0 degrees (the positive X-axis).
Header Beam logic: The spanning beam rests across the top of the two pillars for each arch. The 'start' and 'end' of the beam connect exactly the top-center geometric coordinates of its two pillars. The beam width is {pillar_radius * 2}mm and height is {pillar_radius * 1.5}mm.
"""
    return prompt, shapes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=12, help="Number of arches in the ring")
    args = parser.parse_args()
    
    prompt, shapes = generate_stonehenge(args.scale)
    
    out_file = "stonehenge_golden.json"
    with open(out_file, "w") as f:
        json.dump(shapes, f, indent=2)
        
    print("="*60)
    print(f"PROMPT FOR STONEHENGE RING (SCALE/ARCHES: {args.scale}):")
    print("="*60)
    print(prompt)
    print("\nNote: End your prompt instructing the AI to strictly output only the raw JSON format for C2CAD-Bench.")
    print("="*60)
    print(f"Golden JSON exactly representing this constraint saved to {out_file} ({len(shapes)} parts).")
