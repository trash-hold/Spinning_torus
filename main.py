import numpy as np
import math as m

__frame_size__ = 100 

class Camera:
    def __init__(self, objects, trans_mat):
        self.__obj__ = objects
        self.__obj__ = self.camera_cs(trans_mat)
    
    def rotate(self, obj, rot):
        #rot    - list/vector containing three angles (in radians) descibing rotation (OX, OY, OZ)
        #matrix - matrix to rotate
        rot_phi = np.array([[m.cos(rot[0]), m.sin(rot[0]), 0],
                        [-m.sin(rot[0]), m.cos(rot[0]), 0],
                        [0, 0, 1]])

        rot_theta = np.array([[m.cos(rot[1]), 0 , -m.sin(rot[1])],
                        [0, 1, 0],
                        [m.sin(rot[1]), 0, m.cos(rot[1])]])
    
        rot_psi = np.array([[1, 0, 0],
                        [0, m.cos(rot[2]), m.sin(rot[2])],
                        [0, -m.sin(rot[2]), m.cos(rot[2])]])
    
        rot_mat = np.dot(rot_psi, np.dot(rot_theta, rot_phi))
    
        return np.dot(rot_mat, obj)
    
    def camera_cs(self, trans_mat):
        """
        transformation from global cs to camera cs
        points      - matrix containing all objects mesh points
        trans_mat   - matrix consisting of two vectors [par, rot]
        par(arel)         - vector in form of a list pointing to new origin point (OX, OY, OZ)
        rot(ation)         - list containing three angles (in radians) descibing rotation (OX, OY, OZ)  
        """
        par = np.reshape(np.array(trans_mat[:, 0]), (3, 1))
        rot = trans_mat[:, 1]
        obj = self.__obj__ - par

        return self.rotate(obj, rot)

    def projection(self):
        #prep for resterization
        ras_v = np.array([[__frame_size__/2], [-__frame_size__/2], [0]])
        #reduction by z-depth 
        #Not sure if should add +ras_v in 49 or in return line 
        matrix = np.delete(self.__obj__, np.where(self.__obj__.T[:,2] <= 0)[0], axis = 1)
        vec_z = matrix[2]
        matrix[0] = matrix[0]/vec_z
        matrix[1] = matrix[1]/vec_z
        #NEED TO DO STH ABOUT CASES WHEN z = 0
        return matrix + ras_v

    def rasterization(self, w_size):
        """
        w_size = vector defining window size 
        """
        #Transforming into ndc space and then into rasterized space
        ndc_v = np.array([__frame_size__, -__frame_size__ , 1])
        ras = np.rint(((self.projection().T)/ndc_v).T * w_size)
        print("ras:")
        print(ras)
        #Cutting off all points not visible to camera 
        ras = ras.T
        ras_reduced = np.delete(ras, np.where(
            (ras[:, 0] < 0) | (ras[:, 0] >= w_size[0]) | (ras[:, 1] < 0) | (ras[:, 1] >= w_size[1]))[0], axis = 0)
        print("ras reducted:")
        print(ras_reduced)

    def update(self, trans_mat, obj = None):
        pass

class Renderer:
    def __init__(self, obj):
        self.__render__ = obj

def render(matrix, scr_size, frame = __frame_size__):
    pass

class Window:
    def __init__(self, w_size, obj):
        pass

if __name__ == "__main__":
    #mat = np.random.randint(100, size = (3, 5))
    mat = np.array([[100, 50],[100, 3],[1, -5]])
    print("The random matrix:")
    print(mat)
    par = np.array([[0], [0], [0]])
    rot = np.array([0, 0, 0])
    trans = np.column_stack((par, rot))
    cam = Camera(mat, trans)

    #print(cam.__obj__)
    w_size = np.array([[50], [50], [1]])
    cam.rasterization(w_size)
    #print(100*"# ")
    #for i in range(100): print("#")
