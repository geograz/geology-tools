import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import axes3d
from matplotlib.patches import Circle, Wedge, PathPatch

import numpy as np
import pandas as pd


##### functions #####
def normal_vectors(dips, dipdirs):
    
    n_X = np.sin(np.radians(dips)) * np.sin(np.radians(dipdirs))
    n_Y = np.sin(np.radians(dips)) * np.cos(np.radians(dipdirs))
    n_Z = np.cos(np.radians(dips))
   
    return n_X, n_Y, n_Z
        
def mean_unit_vector(normal_vectors):
    # summing up of normal vector coordinates ####
    sum_n_X = sum(normal_vectors[0])
    sum_n_Y = sum(normal_vectors[1])
    sum_n_Z = sum(normal_vectors[2])
    
    ### calculating mean unit vector ### 
    norm_vector = np.sqrt(sum_n_X**2 + sum_n_Y**2 + sum_n_Z**2)
    norm_n_X = sum_n_X / norm_vector
    norm_n_Y = sum_n_Y / norm_vector
    norm_n_Z = sum_n_Z / norm_vector
    
    return norm_n_X, norm_n_Y, norm_n_Z
        
def backcalculation(mean_unit_vector): # backcalculation to dipdirection and dip
    mean_DipDir = (360 - np.arctan2(mean_unit_vector[1], mean_unit_vector[0]) * (180/np.pi))+90
    mean_Dip = np.arccos(mean_unit_vector[2])*(180/np.pi)
    
    return round(mean_DipDir, 1), round(mean_Dip,1)
        
def print_result(backcalculation):
    backcalculation = list(backcalculation)
    if backcalculation[0] > 360:
        backcalculation[0] = backcalculation[0]-360
    print('mean orientation: ({}/{})'.format(backcalculation[0],backcalculation[1]))
    if backcalculation[0] > 180:
        backcalculation[0] = backcalculation[0]-360
    print('mean orientation pole: ({}/{})'.format(backcalculation[0] + 180, 90 - backcalculation[1]))


##### data import #####
print('''Calculate the mean orientation of structural geological data 
      via vector summation from .csv spreadsheets.
      Check the results within the 3D, lower hemisphere pole point projection!
      NOTE: App will skip first row\n''')

File_Path = input(r'filepath to .csv: ')
File_Path = File_Path.replace( '\\' , '/' )

delim = input('delimiter: ')
col_dip = input('name of column with dip: ')
col_dipdir = input('name of column with dip direction: ')

df = pd.read_csv(File_Path, delimiter = delim, usecols = [col_dip, col_dipdir],
                 encoding = 'iso8859_15') #with encoding "iso8859_15" pandas is able to read letters like "Ä,Ö,Ü" that are used in German...

##### calculations #####
print_result(backcalculation(mean_unit_vector(normal_vectors(df[col_dip], df[col_dipdir]))))


##### 3D plot #####
n_X = normal_vectors(df[col_dip], df[col_dipdir])[0] * -1 # *-1 for lower hemisphere projection
n_Y = normal_vectors(df[col_dip], df[col_dipdir])[1] * -1
n_Z = normal_vectors(df[col_dip], df[col_dipdir])[2] * -1

fig = plt.figure(figsize = (9,9))
ax1 = fig.add_subplot(111, projection = '3d')

ax1.scatter(n_X, n_Y, n_Z,s = 2, color = 'black') #pole points

ax1.plot([0, mean_unit_vector(normal_vectors(df[col_dip], df[col_dipdir]))[0]*-2],
          [0, mean_unit_vector(normal_vectors(df[col_dip], df[col_dipdir]))[1]*-2],
          [0, mean_unit_vector(normal_vectors(df[col_dip], df[col_dipdir]))[2]*-2],
          color = 'red') # mean orientation polevector


##### draw stereonet #####
ax1.plot([0,0,0.25,-0.25,0], [-1,1,0.75,0.75,1], [-1.5,-1.5,-1.5,-1.5,-1.5], color = 'black') #North arrow
a = Wedge((0,0),1,180,0,  edgecolor = 'black', facecolor = 'none', linewidth = 0.1) #stereonet
b = Wedge((0,0),1,180,0,  edgecolor = 'black', facecolor = 'none', linewidth = 0.1) #stereonet
p = Circle((0,0), 1, edgecolor = 'black', facecolor = 'none', linewidth = 0.1) #stereonet
ax1.add_patch(a) #stereonet
ax1.add_patch(b) #stereonet
ax1.add_patch(p) #stereonet
art3d.pathpatch_2d_to_3d(a, z=0, zdir="x") #stereonet
art3d.pathpatch_2d_to_3d(b, z=0, zdir="y") #stereonet
art3d.pathpatch_2d_to_3d(p, z=0, zdir="z") #stereonet
ax1.plot([0,0],[0,0],[0,-1], linewidth = 0.1 , color = 'black') #stereonet

ax1.set_axis_off()

ax1.set_xlim3d(-1,1)
ax1.set_ylim3d(-1,1)
ax1.set_zlim3d(-1,1)

plt.show()
