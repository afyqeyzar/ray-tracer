
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 14:28:07 2021

@author: afyqeyzar
"""
#%%
import numpy as np
from ray_class import *
        
#%%
#Testing the ray tracer

r1 = Ray(np.array([20.0,0.0,-60.0]), dir_vec = np.array([0.0,0.0,1.0]))
r2 = Ray(np.array([20.0,0.0,-60.0]), dir_vec = np.array([-1.0,0.0,0.9]))
r3 = Ray(np.array([0.2,0.0,-100.0]), dir_vec = np.array([0.0,0.0,1.0]))

s1 = SphericalRefraction(-1/0.03,1/0.03,1.0,1.5,100.0)
out1 = OutputPlane(-32.6,np.array([0.0,0.0,-1.0]))

s1.propagate_ray(r1)
out1.propagate_ray(r1)

s1.propagate_ray(r2)
out1.propagate_ray(r2)

s1.propagate_ray(r3)
out1.propagate_ray(r3)


#%%
#Plotting the raytracer

import matplotlib.pyplot as plt

xlist1 = []
ylist1 = []

xlist2 = []
ylist2 = []

xlist3 = []
ylist3 = []

x = r1.vertices()
x2 = r2.vertices()
x3 = r3.vertices()

for i in range(len(x)):
    ylist1.append(x[i][0])
    xlist1.append(x[i][2])
    ylist2.append(x2[i][0])
    xlist2.append(x2[i][2])
    ylist3.append(x3[i][0])
    xlist3.append(x3[i][2])
    
plt.plot(xlist1,ylist1)
plt.plot(xlist2,ylist2)
#plt.plot(xlist3,ylist3)
plt.xlim(-70,0)
plt.ylim(-100,100)
plt.grid()
plt.xlabel('Distance / mm')
plt.ylabel('Distance / mm')

print(x2)

#%%
#getting staring points for the light beam omg
def beam(radius):
    point_list_a = []
    point_list_b = []
    
    for i in np.linspace(0,radius,20):
        new_point = np.sqrt((radius**2)-(i**2))
        point_list_a.append(new_point)
        point_list_b.append(i)
        
        point_list_a.append(new_point)
        point_list_b.append(-i)
        
        point_list_a.append(-new_point)
        point_list_b.append(-i)
        
        point_list_a.append(-new_point)
        point_list_b.append(i)
        
    return point_list_a, point_list_b
        
circle_x = []
circle_y = []
#circle = [[],[]]
#%%
for i in np.linspace(1,10):
    point = beam(i)
    circle_x.append(point[0])
    circle_y.append(point[1])
    
    #circle.append(circle_x,circle_y)

    
#%%    
#circle = beam(10)
#plt.plot(circle[0],circle[1],'.')

#%%
plt.plot(circle_x,circle_y,'.')
#circle[0].append(circle_x)

#circle[1].append(circle_y)
#print(circle)
plt.grid()
print(circle_x)
print(len(circle_x[0]))


#%%
#function to inticalize rays

def get_rays(points1,points2):
    xlist = []
    ylist = []
    zlist = []
    for a in range(len(circle_x)):
        for i in range(len(points1[0])):
            ray = Ray(np.array([points1[a][i],points2[a][i],-60.0]), dir_vec = np.array([0.0,0.0,1.0]))
        
            s1.propagate_ray(ray)
            out1.propagate_ray(ray)
        
            x = ray.vertices()
            for i in range(len(x)):
                xlist.append(x[i][0])
                ylist.append(x[i][1])
                zlist.append(x[i][2])
    return xlist,ylist,zlist


#%%
#from mpl_toolkits import mplot3d
#%matplotlib auto
fig = plt.figure()
ax = plt.axes(projection='3d')

x,y,z = get_rays(circle_x,circle_y)  
print(len(x))     
#plt.plot(y,z,'x')
ax = plt.axes(projection='3d')

# Data for a three-dimensional line
#%%
#group list into coordinates

def group_into_three(x,y,z):
    coords_list =[]
    for i in range(len(x)):
        coords=[]
        coords.append(x[i])
        coords.append(y[i])
        coords.append(z[i])
        coords_list.append(coords)
    
    return coords_list


#%%

#for i in range(0,len(coords_list)):
#   ax.plot3D(coords_list[i][0], coords_list[i][1], coords_list[i][2])

fig = plt.figure()
ax = plt.axes(projection='3d')

x,y,z = get_rays(circle_x,circle_y)  
print(len(x))     
#plt.plot(y,z,'x')
ax = plt.axes(projection='3d')

coords_list = group_into_three(x,y,z)

ax.plot3D(x,y,z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z') 


#%%

z_plane_y = []
z_plane_x = []


for i in range(len(coords_list)):
    if i % 3 == 2:
        print(coords_list[i][0], coords_list[i][1], coords_list[i][2])
        z_plane_x.append(coords_list[i][0])
        z_plane_y.append(coords_list[i][1])
    else:
       continue                                                        
    
    
plt.show()
#ax.plot3D(x,y,z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z') 

plt.plot(z_plane_x,z_plane_y,'.')
#plt.xlim(-10,10)
#plt.ylim(-10,10)
plt.grid()

#%%

from sklearn.metrics import mean_squared_error

x_rms = mean_squared_error(z_plane_x,np.zeros(len(z_plane_x)),squared=False)
print('x_rms =',x_rms)
y_rms = mean_squared_error(z_plane_y,np.zeros(len(z_plane_y)),squared=False)
print('y_rms =',y_rms)










