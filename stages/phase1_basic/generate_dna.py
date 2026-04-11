import argparse
import json
import math

def generate_dna(base_pairs):
    shapes = []
    pid = 0
    R = 20.0 
    z_step = 4.0
    angle_step = 36.0 
    sphere_radius = 3.0
    
    for i in range(base_pairs):
        theta1 = math.radians(i * angle_step)
        theta2 = math.radians(i * angle_step + 180.0)
        z = i * z_step
        
        x1 = R * math.cos(theta1)
        y1 = R * math.sin(theta1)
        
        x2 = R * math.cos(theta2)
        y2 = R * math.sin(theta2)
        
        # Sphere 1
        shapes.append({
            "id": pid, "type": "sphere", "radius": sphere_radius,
            "center": [float(x1), float(y1), float(z)]
        })
        pid += 1
        
        # Sphere 2
        shapes.append({
            "id": pid, "type": "sphere", "radius": sphere_radius,
            "center": [float(x2), float(y2), float(z)]
        })
        pid += 1
        
        # Rung
        shapes.append({
            "id": pid, "type": "beam", "width": 2.0, "height": 2.0,
            "start": [float(x1), float(y1), float(z)],
            "end": [float(x2), float(y2), float(z)]
        })
        pid += 1

    turns_per_revolution = round(360.0 / angle_step)
    prompt = f"""Generate a double-helical macromolecule (like DNA) extending upward along the Z-axis.
The structure consists of exactly {base_pairs} base pairs (levels). Each level has two spherical backbone nodes and one connecting hydrogen-bond beam. (Total {pid} shapes).
Helical geometry rules:
- The helical backbone radius is exactly {R}mm.
- The first pair of nodes sits at Z=0. One node is on the positive X-axis (angle 0 degrees), its partner is diametrically opposite (angle 180 degrees).
- The helix completes one full turn every {turns_per_revolution} levels. Successive levels are spaced {z_step}mm apart in Z and rotate uniformly counter-clockwise around the Z-axis.
- Every backbone sphere has a radius of {sphere_radius}mm.
- Each connecting bond is a beam whose 'start' and 'end' are exactly the center coordinates of the two partner spheres at that level. Beam width and height are both 2.0mm.
"""
    return prompt, shapes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=10, help="Number of base pairs in the helix")
    args = parser.parse_args()
    
    prompt, shapes = generate_dna(args.scale)
    
    out_file = "dna_golden.json"
    with open(out_file, "w") as f:
        json.dump(shapes, f, indent=2)
        
    print("="*60)
    print(f"PROMPT FOR DNA HELIX (SCALE/BASE_PAIRS: {args.scale}):")
    print("="*60)
    print(prompt)
    print("\nNote: End your prompt instructing the AI to strictly output only the raw JSON format for C2CAD-Bench.")
    print("="*60)
    print(f"Golden JSON exactly representing this constraint saved to {out_file} ({len(shapes)} parts).")
