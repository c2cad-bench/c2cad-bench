def generate_bcc(scale):
    """
    Crystalline BCC Lattice Array (Difficulty Level 5+ of Phase 2)
    Scale defines N in an NxNxN array.
    """
    n = scale
    
    prompt = f"""Generate a `{n}x{n}x{n}` grid of Body-Centered Cubic unit cells.
Each cell is a 10x10x10 volume. The grid spans from the origin `[0,0,0]` expanding into the positive `X, Y, Z` space.
Place a sphere of `Radius=1` exactly at every single corner of the grid.
Place a single sphere of `Radius=1` exactly at the volumetric center of every single cell.
Deduplicate any spheres that share the exact same `[X,Y,Z]` coordinate so no two spheres exist in the exact same location!
Finally, for every single unit cell, connect its exact center sphere to all 8 of its own corners using 8 beams of width 1 and height 1."""

    shapes = []
    sid = 1
    
    # Track corner positions to deduplicate
    corners_set = set()
    centers = []
    
    # 1. Centers and Beams logic
    for x in range(n):
        for y in range(n):
            for z in range(n):
                cx = x * 10 + 5
                cy = y * 10 + 5
                cz = z * 10 + 5
                centers.append((cx, cy, cz))
                
                # Register the 8 corners for this unit cell
                cell_corners = [
                    (x*10, y*10, z*10), (x*10+10, y*10, z*10),
                    (x*10, y*10+10, z*10), (x*10+10, y*10+10, z*10),
                    (x*10, y*10, z*10+10), (x*10+10, y*10, z*10+10),
                    (x*10, y*10+10, z*10+10), (x*10+10, y*10+10, z*10+10)
                ]
                
                for corner in cell_corners:
                    corners_set.add(corner)
                    # Beams mapping center to corner
                    shapes.append({
                        "id": sid, "type": "beam",
                        "start": [cx, cy, cz],
                        "end": [corner[0], corner[1], corner[2]],
                        "width": 1, "height": 1
                    })
                    sid += 1

    # 2. Add Deduplicated Corner Spheres
    for corner in sorted(list(corners_set)):
        shapes.append({
            "id": sid, "type": "sphere",
            "center": [corner[0], corner[1], corner[2]],
            "radius": 1
        })
        sid += 1
        
    # 3. Add Center Spheres
    for center in centers:
        shapes.append({
            "id": sid, "type": "sphere",
            "center": [center[0], center[1], center[2]],
            "radius": 1
        })
        sid += 1

    return prompt, shapes
