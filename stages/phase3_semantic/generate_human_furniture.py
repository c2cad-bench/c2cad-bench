def _reference_solution(scale):
    """Return a canonical valid table with (scale*2) legs for the visualizer."""
    legs = scale * 2 if scale else 4
    W, D = 100.0, 60.0           # tabletop width / depth
    T = 5.0                       # tabletop thickness
    LH = 70.0                     # leg height
    LR = 3.0                      # leg radius
    table_z = LH + T / 2.0       # top-face centre Z
    shapes = [
        {"id": 0, "type": "box", "center": [0.0, 0.0, table_z], "size": [W, D, T]}
    ]
    # Place legs at the four corners; if more than 4, add along the long edges
    import math
    corners = [
        ( W / 2 - LR * 2,  D / 2 - LR * 2),
        (-W / 2 + LR * 2,  D / 2 - LR * 2),
        (-W / 2 + LR * 2, -D / 2 + LR * 2),
        ( W / 2 - LR * 2, -D / 2 + LR * 2),
    ]
    if legs > 4:
        # Add mid-edge legs along the two long sides
        for k in range(1, (legs - 4) // 2 + 1):
            t = k / ((legs - 4) // 2 + 1)
            xm = W / 2 - LR * 2 - t * (W - 4 * LR * 2)
            corners += [(xm, D / 2 - LR * 2), (xm, -D / 2 + LR * 2)]
    for i in range(legs):
        rx, ry = corners[i] if i < len(corners) else corners[i % 4]
        shapes.append({
            "id": i + 1,
            "type": "cylinder",
            "center": [round(rx, 2), round(ry, 2), LH / 2.0],
            "radius": LR,
            "height": LH,
            "axis": [0, 0, 1]
        })
    return shapes

def generate_furniture(scale):
    legs = scale * 2 if scale else 4
    prompt = f"""Design a functional table. You can choose the dimensions and relative scaling freely.
You must use exactly these IDs for grading tracking:
- Tabletop: Box, ID=0
- Legs: Cylinders, IDs 1 to {legs}.

Semantic Constraints:
1. The {legs} legs must be geometrically mated as COINCIDENT to the bottom face of the tabletop box.
2. The {legs} legs must perfectly touch the Z=0 ground plane (i.e. Gravity support).
3. The legs must act as pillars to support the table corners roughly symmetrically.
Output only the raw JSON array of geometric elements. Do not output anything else.
"""
    specs = {
        "gravity_check": True,
        "mates": [ {"type": "coincident", "ids": [i, 0], "face_a": "top", "face_b": "bottom"} for i in range(1, legs+1) ],
        "reference": _reference_solution(scale)
    }
    return prompt, specs
