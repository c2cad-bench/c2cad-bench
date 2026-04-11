import math

def generate_fractal(scale):
    """
    Fractal Y-Branch Recursion (Difficulty Level 4+ of Phase 2)
    Scale defines the recursion depth.
    Level 0 = Trunk only. Level 1 = Trunk + 2 branches. Level 2 = Trunk + 2 + 4.
    """
    depth = scale
    
    prompt = f"""Create a recursively branching tree entirely out of beams with width=1, height=1.
Start with a Level 0 vertical trunk beam from exactly `[0,0,0]` to `[0,0,100]`.
At the tip of any parent branch, spawn exactly 2 child branches. Both children must lie entirely in the XZ plane.
Each child branch is EXACTLY half the length of its parent branch.
The left child's directional axis is rotated exactly +45 degrees around the Y-axis from its parent's directional axis. The right child's directional axis is rotated exactly -45 degrees around the Y-axis from its parent's directional axis.
Recursively apply this splitting rule up to exactly Level `{depth}`.
Ensure the start coordinate of every child branch is mathematically perfectly locked to the end coordinate of its parent branch."""

    shapes = []
    sid = 1
    
    # Internal recursion
    def recurse(start_pt, angle_deg, length, current_level):
        nonlocal sid
        
        angle_rad = math.radians(angle_deg)
        dx = length * math.sin(angle_rad)
        dz = length * math.cos(angle_rad)
        
        end_pt = [
            round(start_pt[0] + dx, 4),
            0.0,
            round(start_pt[2] + dz, 4)
        ]
        
        shapes.append({
            "id": sid, "type": "beam",
            "start": start_pt, "end": end_pt,
            "width": 1, "height": 1
        })
        sid += 1
        
        if current_level < depth:
            child_len = length / 2.0
            recurse(end_pt, angle_deg + 45.0, child_len, current_level + 1)
            recurse(end_pt, angle_deg - 45.0, child_len, current_level + 1)

    recurse([0.0, 0.0, 0.0], 0.0, 100.0, 0)
    
    return prompt, shapes
