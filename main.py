import numpy as np
import math as m

def transformation(points, par, rot):
    """
    points      - matrix containing all objects mesh points
    par     - vector in form of a list pointing to new origin point (OX, OY, OZ)
    rot   - list containing three angles (in radians) descibing rotation (OX, OY, OZ)  
    """
    rot_phi = np.array([[m.cos(rot[0]), m.sin(rot[0]), 0],
                        [-m.sin(rot[0]), m.cos(rot[0]), 0],
                        [0, 0, 1]])

    rot_theta = np.array([[m.cos(rot[1]), 0 , -m.sin(rot[1])],
                        [0, 1, 0],
                        [m.sin(rot[0]), 0, m.cos(rot[1])]])
    
    rot_psi = np.array([[1, 0, 0],
                        [0, m.cos(rot[0]), m.sin(rot[0])],
                        [0, -m.sin(rot[0]), m.cos(rot[0])]])
    
    rot_mat = np.dot(rot_psi, np.dot(rot_theta, rot_phi))
    
    new_points = np.dot(rot_mat, points-par)
    print(rot_mat)
    return new_points


if __name__ == "__main__":
    mat = np.zeros([3, 4])
    par = np.array([[1], [0], [3]])
    rot = np.array([0, 0, 0])
    print(transformation(mat, par, rot))
