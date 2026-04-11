import math

def generate_bridge(scale):
    """
    Suspension Bridge (Difficulty Level 1+ of Phase 2)
    Scale defines the number of cables per tower.
    """
    n_cables = scale
    
    prompt = f"""Create a horizontal bridge deck beam spanning exactly from `X=-50` to `X=50` at a constant `Y=0, Z=10`.
Create two vertical tower cylinders (Radius 2). The left tower is located at `X=-50, Y=0`, spanning from `Z=0` up to `Z=100`. The right tower is located at `X=50, Y=0`, spanning from `Z=0` up to `Z=100`.
Create exactly {n_cables} cable beams for the left tower. They perfectly connect the absolute top-center point of the left tower (`X=-50, Y=0, Z=100`) to {n_cables} evenly spaced target points perfectly intersecting the deck beam. The spacing begins at `X=-48` and ends at `X=-2`, inclusive.
Mirror this exact logic for the right tower, placing {n_cables} cables connecting the top-center of the right tower to evenly spaced points along the deck starting at `X=2` and ending at `X=48`, inclusive.
All cable and deck beams must have a width and height of 1."""

    shapes = []
    
    # Towers
    shapes.append({"id": 1, "type": "cylinder", "center": [-50, 0, 50], "radius": 2, "height": 100, "axis": [0,0,1]})
    shapes.append({"id": 2, "type": "cylinder", "center": [50, 0, 50], "radius": 2, "height": 100, "axis": [0,0,1]})
    
    # Deck
    shapes.append({"id": 3, "type": "beam", "start": [-50, 0, 10], "end": [50, 0, 10], "width": 2, "height": 1})
    
    sid = 4
    # Left Cables
    if n_cables > 1:
        step = (46.0) / (n_cables - 1)
    else:
        step = 0
        
    for i in range(n_cables):
        x = -48.0 + (i * step)
        shapes.append({
            "id": sid, "type": "beam", 
            "start": [-50, 0, 100], "end": [x, 0, 10],
            "width": 1, "height": 1
        })
        sid += 1
        
    # Right Cables
    for i in range(n_cables):
        x = 2.0 + (i * step)
        shapes.append({
            "id": sid, "type": "beam", 
            "start": [50, 0, 100], "end": [x, 0, 10],
            "width": 1, "height": 1
        })
        sid += 1
        
    return prompt, shapes
