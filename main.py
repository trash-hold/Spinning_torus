import numpy as np
import math as m

__frame_size__ = 100 

class Camera:
    def __init__(self, objects, w_size = __frame_size__):
        self.__obj__ = objects
        self.__wsize__ = w_size
    
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
    
        #rot_mat = np.dot(rot_psi, np.dot(rot_theta, rot_phi))
        rot_mat = np.dot(rot_theta, rot_phi)
        print(rot_mat)

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
        #reduction by z-depth + discarding points that won't be visible due to their depth 
        #Not sure if should add +ras_v in 49 or in return line 
        matrix = np.delete(self.__obj__, np.where(self.__obj__.T[:,2] <= 0)[0], axis = 1)
        vec_z = matrix[2]
        matrix[0] = matrix[0]/vec_z
        matrix[1] = matrix[1]/vec_z
        return matrix + ras_v

    def rasterization(self, w_size):
        """
        w_size = vector defining window size 
        """
        #Transforming into ndc space and then into rasterized space
        ndc_v = np.array([__frame_size__, -__frame_size__ , 1])
        ras = np.rint(((self.projection().T)/ndc_v).T * w_size)
        #Cutting off all points not visible to camera 
        ras = ras.T
        ras_reduced = np.delete(ras, np.where(
            (ras[:, 0] < 0) | (ras[:, 0] >= w_size[0]) | (ras[:, 1] < 0) | (ras[:, 1] >= w_size[1]))[0], axis = 0)
        return ras_reduced

    def update_cam(self, trans_mat, obj = None, w_size = None):
        if obj is not None: self.__obj__ = obj
        if w_size is None: w_size = self.__wsize__

        self.__obj__ = self.camera_cs(trans_mat)
        self.__obj__ = self.rasterization(w_size)

class Renderer:
    def __init__(self, obj, w_size):
        self.__render__ = obj
        self.__size__ = w_size
    
    def draw(self, shape, cp, dim):
        #cp - center point
        obj = None
        if shape == "circle" or "c":
            for x in range(-dim[0], dim[0]):
                if obj is None:
                    obj = np.array([[x, m.sqrt(dim[0]*dim[0] - x*x), dim[1]], [-x, m.sqrt(dim[0]*dim[0] - x*x), dim[1]]])
                else:
                    new_obj = np.array([[x, m.sqrt(dim[0]*dim[0] - x*x), dim[1]], [x, -m.sqrt(dim[0]*dim[0] - x*x), dim[1]]])
                    obj = np.vstack([obj, new_obj])
        #print(self.__render__)
        self.__render__ = np.vstack([self.__render__, obj])

    def render(self):
        # # $ & @ %
        max_z = np.amax(self.__render__, axis = 0)[2]
        buffer_size = max_z // 5 + 1
        sym = {0: "@", 1: "@", 2: "#", 3: "&", 4: "%", 5: "$"}

        #creating map
        mapping = {(x, y): [] for x in range(int(self.__size__[0])) for y in range(int(self.__size__[0]))}
        for i in self.__render__:
            mapping[(i[0], i[1])].append(i[2])
        
        #rewritting map into symbols
        for i in mapping:
            if mapping[i] == []:
                mapping[i] = " "
            else:
                z = mapping[i]
                mapping[i] = sym[sorted(z)[0]//buffer_size]
        
        print(" " + "__" * int(self.__size__[0]))
        for j in range(int(self.__size__[1])):
            x = "|"
            for i in range(int(self.__size__[0])):
                x = x + " " + mapping[i, j]
            print(x + "|")
        print(" " + "--" * int(self.__size__[0]))
    
    def update_renderer(self, camera, obj = None, trans_mat = np.array([[0, 0], [0, 0], [0, 0]]), w_size = None):
        if w_size is None: w_size = self.__size__
        if obj is None: obj = self.__render__.T
        camera.update_cam(trans_mat, obj, w_size)
        self.__render__ = camera.__obj__
        self.render()


class Window:
    def __init__(self, w_size, obj):
        pass

if __name__ == "__main__":
    # PROBLEMS WITH ZERO ARRAY IN RENDER()

    #mat = np.random.randint(10, size = (3, 20))
    #mat = np.array([[4, 4, 4, 4],[4, 4, 4, 4],[3, 8, 7, 1]])
    mat = np.array([[0],[0],[1]])
    #print("The random matrix:")
    #print(mat)
    t = np.zeros(shape = (2, 3))
    par = np.array([[-10], [0], [-1]])
    rot = np.array([m.radians(0), m.radians(4), m.radians(0)])
    trans = np.column_stack((par, rot))
    cam = Camera(mat, t)

    #print(cam.__obj__)
    w_size = np.array([[60], [60], [1]])
    cam.rasterization(w_size)
    
    red = Renderer(mat.T, w_size)
    red.draw("circle", par, [50, 4])
    red.update_renderer(cam, None, trans)
    #print(100*"# ")
    #for i in range(100): print("#")
