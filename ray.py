import numpy as np

class Ray():
    """
    Class Ray() initializes the rays position and direction vector
    """

    def __init__(self, pos_vec = np.array([-0.0,-0.0,-10.0]), dir_vec = np.array([1.0,1.0,1.0])):
        self.__position_vector = pos_vec
        self.__direction_vector = dir_vec
        
        self.__pos_vec_list = [self.__position_vector]
        self.__dir_vec_list = [self.__direction_vector]
    
    def p(self): 
        #return current position of ray
        return self.__position_vector
    
    def k(self): 
        #return currrent direction vector of ray
        return self.__direction_vector
    
    def append(self,p,k):
        #append new position and direction vector into list
      
        
        self.__position_vector = p
        self.__direction_vector = k
        
        self.__pos_vec_list.append(p)
        self.__dir_vec_list.append(k)
        return self
    
    def vertices(self):
        return self.__pos_vec_list

class OpticalElement:
    def propagate_ray(self, ray):
        """"
        propagate a ray through the optical element
        """
        
        raise NotImplementedError()

class SphericalRefraction(OpticalElement):
    """
    class to represent sphere refrective surface
    """
    def __init__(self, z0, curvature, n1, n2, aper_rad):
        self.__z_0 = z0
        self.__curvature = curvature
        self.__n1 = n1
        self.__n2 = n2
        self.__aper_rad = aper_rad
        
    def intercept(self,ray):
        
        if self.__curvature == 0:
            return None
        
        else:
            #calculate interception with a circle at origin
            position = ray.p()
            direction = ray.k()
            direction_hat = direction / np.linalg.norm(direction)
        
            first_dot = -(np.dot(position , direction_hat)) 
            second = np.sqrt((np.dot(position,direction_hat))**2 - ((np.linalg.norm(position))**2-(self.__curvature)**2))
        
            l1 = first_dot + second
            l2 = first_dot - second
            
            #checking negative values of scalar l
            if l1 < 0 and l2 < 0:
                return None
            #Checking if ray start withing the sphere
            elif np.linalg.norm(position) <= self.__curvature:
                return None
            #returning the smaller value of l
            elif abs(l1) <= abs(l2):
                return ray.p() + l1 * direction_hat
            else:
                return ray.p() + l2 * direction_hat
        
    def propagate_ray(self,ray):
        """
        Calculate refracted ray direction and append into ray class

        """
        position = ray.p()
        direction = ray.k()
        direction_hat = direction / np.linalg.norm(direction)
        
        #check is ray actually intercepts
        if (np.dot(position,direction_hat))**2 - ((np.linalg.norm(position))**2-(self.__curvature**2)) < 0:
            return 'Ray Terminated'
        
        else:
            #incident_ray = ray.k()
            surface_normal = self.intercept(ray)
            surf_norm_hat = (surface_normal / np.linalg.norm(surface_normal))
            #calculate refracted ray unit vector form
            refracted_ray = refraction(direction_hat,surf_norm_hat,self.__n1,self.__n2)
        
            #append into ray list
            ray.append(surface_normal,refracted_ray)