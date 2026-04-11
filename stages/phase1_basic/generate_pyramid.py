import argparse
import json
import math

def generate_pyramid(layers):
    R = 10.0
    shapes = []
    pid = 0
    
    dz = 2.0 * R * math.sqrt(2.0/3.0)
    
    for layer in range(layers):
        side = layers - layer
        z = R + layer * dz
        x0 = layer * R
        y0 = layer * R / math.sqrt(3.0)
        
        for row in range(side):
            y = y0 + row * R * math.sqrt(3.0)
            for col in range(side - row):
                x = x0 + row * R + col * 2.0 * R
                
                shapes.append({
                    "id": pid,
                    "type": "sphere",
                    "center": [float(x), float(y), float(z)],
                    "radius": R
                })
                pid += 1

    prompt = f"""Generate a {layers}-layer tetrahedral cannonball pyramid made entirely of identical spheres.
There are a total of {pid} spheres, all with a radius of {R}mm.
The base layer lies perfectly flat on the Z=0 plane (meaning the initial layer's center Z is exactly {R}mm).
The spheres in the base form an equilateral triangle grid with {layers} spheres along each outer edge. All touching spheres are perfectly tangent to one another (the center-to-center distance between neighbors is exactly {2*R}mm). 
Grid alignment rules: 
- One corner of this base triangle is precisely at the origin (X=0, Y=0). 
- From this origin corner, the bottom row of spheres extends straightforwardly along the positive X-axis.
Stacking rules:
- Subsequent layers rest perfectly in the equilateral triangular pockets (dips) formed by the three spheres directly below them in the previous layer, exactly as dense-packed spheres or cannonballs stack under gravity.
"""
    return prompt, shapes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=4, help="Number of layers in the pyramid")
    args = parser.parse_args()
    
    prompt, shapes = generate_pyramid(args.scale)
    
    out_file = "pyramid_golden.json"
    with open(out_file, "w") as f:
        json.dump(shapes, f, indent=2)
        
    print("="*60)
    print(f"PROMPT FOR CANNONBALL PYRAMID (SCALE/LAYERS: {args.scale}):")
    print("="*60)
    print(prompt)
    print("\nNote: End your prompt instructing the AI to strictly output only the raw JSON format for C2CAD-Bench.")
    print("="*60)
    print(f"Golden JSON exactly representing this constraint saved to {out_file} ({len(shapes)} parts).")
