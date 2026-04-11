def generate_truss(scale):
    """
    Cross-Braced Truss Tower (Difficulty Level 3+ of Phase 2)
    Scale defines the number of stories in the tower.
    """
    stories = scale
    
    prompt = f"""Construct an `{stories}`-story vertical tower spanning upwards from `Z=0`.
Each story is exactly 10 units tall. The floorplan of the tower is a square with corners at `X=±5`, `Y=±5`.
For every story, place exactly 4 vertical pillar beams perfectly on the corners connecting the floor of that story to the ceiling of that story.
For every outer face of every story (4 faces total per story), place exactly 2 diagonal beams forming a perfect 'X' across the face, spanning perfectly from corner to corner.
All beams must have a width of 1 and height of 1."""

    shapes = []
    sid = 1
    
    corners = [
        [-5, -5],
        [5, -5],
        [5, 5],
        [-5, 5]
    ]
    
    faces = [
        ([0, 1]), # Front Y=-5
        ([1, 2]), # Right X=5
        ([2, 3]), # Back Y=5
        ([3, 0]), # Left X=-5
    ]
    
    for z_idx in range(stories):
        z_base = z_idx * 10
        z_top = z_base + 10
        
        # Pillars
        for c in corners:
            shapes.append({
                "id": sid, "type": "beam",
                "start": [c[0], c[1], z_base],
                "end": [c[0], c[1], z_top],
                "width": 1, "height": 1
            })
            sid += 1
            
        # Faces diagonals
        for f in faces:
            c1 = corners[f[0]]
            c2 = corners[f[1]]
            
            # Diagonal 1
            shapes.append({
                "id": sid, "type": "beam",
                "start": [c1[0], c1[1], z_base],
                "end": [c2[0], c2[1], z_top],
                "width": 1, "height": 1
            })
            sid += 1
            
            # Diagonal 2
            shapes.append({
                "id": sid, "type": "beam",
                "start": [c2[0], c2[1], z_base],
                "end": [c1[0], c1[1], z_top],
                "width": 1, "height": 1
            })
            sid += 1
            
    return prompt, shapes
