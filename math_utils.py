import math
import numpy as np

# Map octant to direction
directions = {
    1: "Right",
    2: "Up-Right",
    3: "Up",
    4: "Up-Left",
    5: "Left",
    6: "Down-Left",
    7: "Down",
    8: "Down-Right"
}

def find_closest_indices(indices, target_index, N):
    # Extract coordinates of target_index
    target_coords = indices[target_index]
    # Compute distances between target_index and all other indices
    distances = np.linalg.norm(indices - target_coords, axis=1)
    # Sort indices based on distances and get the N closest ones
    closest_indices = distances.argsort()[:N]
    return closest_indices

def calculate_octant(center, point):
    # Calculate the difference in x and y coordinates
    delta_x = point[0] - center[0]
    delta_y = point[1] - center[1]

    # Calculate the angle in radians
    angle_rad = math.atan2(delta_y, delta_x)

    # Convert radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Ensure angle is between 0 and 360 degrees
    if angle_deg < 0:
        angle_deg += 360

    # Rotate the angle by 45/2 degrees
    angle_deg += 22.5
    if angle_deg >= 360:
        angle_deg -= 360

    # Determine octant
    octant = int(angle_deg // 45) % 8 + 1
    return octant