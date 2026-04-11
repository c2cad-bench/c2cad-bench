import argparse
import json

def generate_rubiks(scale):
    shapes = []
    pid = 0
    box_size = 10.0
    gap = 2.0
    pitch = box_size + gap
    
    for z_idx in range(scale):
        z = (box_size/2.0) + (z_idx * pitch)
        for y_idx in range(scale):
            y = (box_size/2.0) + (y_idx * pitch)
            for x_idx in range(scale):
                x = (box_size/2.0) + (x_idx * pitch)
                
                shapes.append({
                    "id": pid,
                    "type": "box",
                    "center": [float(x), float(y), float(z)],
                    "size": [box_size, box_size, box_size]
                })
                pid += 1

    prompt = f"""Generate a perfect regular {scale}x{scale}x{scale} volumetric grid of identical boxes (total {scale**3} shapes).
Each box is a {box_size}mm cube (width = depth = height = {box_size}mm).
The grid's outermost corner (the vertex where the minimum X, Y, and Z faces of the three outermost boxes meet) is placed exactly at the origin (0, 0, 0). The grid expands into positive X, Y, and Z space.
The gap between the facing surfaces of any two adjacent boxes is exactly {gap}mm on all axes.
The grid is indexed sequentially: X varies fastest, then Y, then Z.
"""
    return prompt, shapes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=3, help="Grid dimension (e.g. 3 for a 3x3x3 grid)")
    args = parser.parse_args()
    
    prompt, shapes = generate_rubiks(args.scale)
    
    out_file = "rubiks_golden.json"
    with open(out_file, "w") as f:
        json.dump(shapes, f, indent=2)
        
    print("="*60)
    print(f"PROMPT FOR VOXEL GRID (SCALE: {args.scale}x{args.scale}x{args.scale}):")
    print("="*60)
    print(prompt)
    print("\nNote: End your prompt instructing the AI to strictly output only the raw JSON format for C2CAD-Bench.")
    print("="*60)
    print(f"Golden JSON exactly representing this constraint saved to {out_file} ({len(shapes)} parts).")
