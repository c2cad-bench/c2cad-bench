import argparse
import json
import math
import os

def generate_staircase(steps):
    shapes = []
    
    pillar_radius = 5.0
    rise_per_step = 5.0
    total_height = steps * rise_per_step
    
    # 0 = Pillar
    shapes.append({
        "id": 0,
        "type": "cylinder",
        "center": [0.0, 0.0, total_height / 2.0],
        "radius": pillar_radius,
        "height": total_height,
        "axis": [0.0, 0.0, 1.0]
    })
    
    step_length = 20.0
    step_width = 5.0
    step_height = 2.0
    angle_increment = 15.0 # degrees

    for i in range(steps):
        angle_rad = math.radians(i * angle_increment)
        z = (i * rise_per_step) + (step_height / 2.0)
        
        start_x = pillar_radius * math.cos(angle_rad)
        start_y = pillar_radius * math.sin(angle_rad)
        
        end_r = pillar_radius + step_length
        end_x = end_r * math.cos(angle_rad)
        end_y = end_r * math.sin(angle_rad)
        
        shapes.append({
            "id": i + 1,
            "type": "beam",
            "start": [float(start_x), float(start_y), float(z)],
            "end": [float(end_x), float(end_y), float(z)],
            "width": step_width,
            "height": step_height
        })

    prompt = f"""Generate a continuous spiral staircase wrapped around a central support pillar.
The central pillar is a cylinder of radius {pillar_radius}mm, centered at the origin, extending vertically along the Z-axis. The pillar's base rests on the Z=0 plane and its height must accommodate all {steps} steps.

There are exactly {steps} steps (beams) wrapping around the pillar. (Total {steps + 1} shapes including the pillar).
Each step has a width of {step_width}mm and a height (thickness) of {step_height}mm. The radial length of each step is {step_length}mm.
Step placement rules:
- The first step starts at angle 0 degrees (pointing exactly along the positive X-axis). Its bottom face rests on the Z=0 plane.
- Each step's 'start' point sits exactly on the outer surface of the central pillar at the step's radial angle.
- Each step's 'end' point extends perfectly outward radially from the pillar at the same angle.
- Each subsequent step rises by exactly {rise_per_step}mm in Z and rotates by exactly {angle_increment} degrees around the Z-axis relative to the previous step.
"""
    return prompt, shapes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=24, help="Number of steps in the staircase")
    args = parser.parse_args()
    
    prompt, shapes = generate_staircase(args.scale)
    
    out_file = "staircase_golden.json"
    with open(out_file, "w") as f:
        json.dump(shapes, f, indent=2)
        
    print("="*60)
    print(f"PROMPT FOR SPIRAL STAIRCASE (SCALE/STEPS: {args.scale}):")
    print("="*60)
    print(prompt)
    print("\nNote: End your prompt instructing the AI to strictly output only the raw JSON format for C2CAD-Bench.")
    print("="*60)
    print(f"Golden JSON exactly representing this constraint saved to {out_file} ({len(shapes)} parts).")
