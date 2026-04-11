def _reference_solution(clearance_block):
    """Return a canonical valid axle assembly for the visualizer."""
    BW, BD, BH = 80.0, 50.0, 50.0      # support block
    shaft_r = 8.0
    bore_r = shaft_r + clearance_block  # bore slightly larger
    bearing_inner_r = shaft_r           # press-fit on shaft
    bearing_outer_r = shaft_r + 6.0
    bearing_H = 12.0
    shaft_len = BW + 20.0
    return [
        {"id": 0, "type": "box", "center": [0.0, 0.0, BH / 2.0], "size": [BW, BD, BH]},
        {"id": 1, "type": "cylinder", "center": [0.0, 0.0, BH / 2.0], "radius": bore_r, "height": BW + 2, "axis": [1, 0, 0]},
        {"id": 2, "type": "cylinder", "center": [0.0, 0.0, BH / 2.0], "radius": shaft_r, "height": shaft_len, "axis": [1, 0, 0]},
        {"id": 3, "type": "pipe", "center": [-(BW / 2.0 - bearing_H / 2.0), 0.0, BH / 2.0], "inner_radius": bearing_inner_r, "outer_radius": bearing_outer_r, "height": bearing_H, "axis": [1, 0, 0]},
        {"id": 4, "type": "pipe", "center": [ (BW / 2.0 - bearing_H / 2.0), 0.0, BH / 2.0], "inner_radius": bearing_inner_r, "outer_radius": bearing_outer_r, "height": bearing_H, "axis": [1, 0, 0]},
    ]

def generate_axle(scale):
    clearance_block = float(scale) * 0.5 # 0.5, 1.0, 1.5
    prompt = f"""Design a functional mechanical axle block constraint system. You can choose the spatial dimensional ratios freely.
You must use exactly these IDs for grading tracking:
- Support Block: Box, ID=0
- Shaft Bore Cut Tool: Cylinder, ID=1 (Must be used in a subtract op to pierce heavily through ID 0)
- Axle Shaft: Cylinder, ID=2
- Bearing A: Pipe, ID=3
- Bearing B: Pipe, ID=4

Semantic Constraints:
1. The Shaft Bore Cut Tool (1) must fully penetrate the Support Block (0).
2. The Axle Shaft (2) must run completely through the bore hole.
3. The Axle Shaft (2) must have exactly {clearance_block} mm of radial clearance scaling inside the block's bore tool (1).
4. The two bearing pipes (3 and 4) must fit concentrically around the axle shaft (2) with exactly 0.0 mm of radial clearance.
5. Due to the cut constraints, the Axle Shaft (2) must NOT generate any volumetric intersection/interference with the solid volume of the Support Block (0).
Output only the raw JSON array.
"""
    specs = {
        "interference_check": True,
        "clearance_fit": [
            {"shaft_id": 2, "hole_id": 1, "expected_clearance": clearance_block, "tol": 0.05},
            {"shaft_id": 2, "hole_id": 3, "expected_clearance": 0.0, "tol": 0.05},
            {"shaft_id": 2, "hole_id": 4, "expected_clearance": 0.0, "tol": 0.05}
        ],
        "mates": [
            {"type": "concentric", "ids": [2, 3]},
            {"type": "concentric", "ids": [2, 4]}
        ],
        "reference": _reference_solution(clearance_block)
    }
    return prompt, specs
