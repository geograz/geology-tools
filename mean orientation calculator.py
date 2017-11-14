import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.patches import Circle, Wedge, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d

import csv
from math import sin, cos, radians, sqrt, atan2, pi, acos

### function definition ###
def normal_vectors(data_import):
    n_X = []
    n_Y = []
    n_Z = []
    
    for i in range(len(data_import[0])):
        dip = float(data_import[0][i])
        dipdir = float(data_import[1][i])
        X = sin(radians(dip)) * sin(radians(dipdir))
        Y = sin(radians(dip)) * cos(radians(dipdir))
        Z = cos(radians(dip))
        n_X.append(X)
        n_Y.append(Y)
        n_Z.append(Z)
    
    return n_X, n_Y, n_Z
        
def mean_unit_vector(normal_vectors):
    # summing up of normal vector coordinates ####
    sum_n_X = round(sum(normal_vectors[0]), 10)
    sum_n_Y = round(sum(normal_vectors[1]), 10)
    sum_n_Z = round(sum(normal_vectors[2]), 10)
    
    ### calculating mean unit vector ### 
    norm_vector = sqrt(sum_n_X**2 + sum_n_Y**2 + sum_n_Z**2)
    norm_n_X = sum_n_X / norm_vector
    norm_n_Y = sum_n_Y / norm_vector
    norm_n_Z = sum_n_Z / norm_vector
    
    return norm_n_X, norm_n_Y, norm_n_Z
        
def backcalculation(mean_unit_vector): # backcalculation to dipdirection and dip
    mean_DipDir = (360 - atan2(mean_unit_vector[1], mean_unit_vector[0]) * (180/pi))+90
    mean_Dip = acos(mean_unit_vector[2])*(180/pi)
    
    return mean_DipDir, mean_Dip
        
def print_result(backcalculation):
    print('mean orientation: (', round((backcalculation[0]-360),1),'/',round((backcalculation[1]),1),')')
    print('mean orientation pole: (', round((backcalculation[0]-180),1),'/',round((90-backcalculation[1]),1),')')


### execution ####
print('''Application for computation of the mean orientation of structural geological data via vector summation from .csv spreadsheets.\n
A 3D, lower hemisphere pole point projection will be given for result inspection.\n
NOTE: App will skip first row\n''')

File_Path = (input(r'filepath to .csv: '))
File_Path = File_Path.replace( '\\' , '/' )

delim = input('delimiter: ')
          
with open(File_Path) as f:
    next(f) #skip first row
    readCSV = csv.reader(f, delimiter=delim)

    dips = []
    dipdirs = []
    
    col_dip = int(input('Column with dip: '))-1
    col_dipdir = int(input('Column with dipdirection: '))-1
    
    # separates orientations
    for row in readCSV:
        a = int(float(row[col_dip]))
        b = int(float(row[col_dipdir]))
        dips.append(a)
        dipdirs.append(b)         
                
data_import = [dips]+[dipdirs]
             
print((print_result(backcalculation(mean_unit_vector(normal_vectors(data_import))))))


### 3D plot ###
n_X = [i*-1 for i in normal_vectors(data_import)[0]] # *-1 for lower hemisphere projection
n_Y = [i*-1 for i in normal_vectors(data_import)[1]] # *-1 for lower hemisphere projection
n_Z = [i*-1 for i in normal_vectors(data_import)[2]] # *-1 for lower hemisphere projection


fig = plt.figure(figsize = (9,9))
ax1 = fig.add_subplot(111, projection = '3d')

ax1.scatter(n_X, n_Y, n_Z,s = 2, color = 'black') #pole points
ax1.plot_wireframe([0, mean_unit_vector(normal_vectors(data_import))[0]*-2], [0, mean_unit_vector(normal_vectors(data_import))[1]*-2], [0, mean_unit_vector(normal_vectors(data_import))[2]*-2], color = 'red') # mean orientation polevector

ax1.plot_wireframe([0,0,0.25,-0.25,0], [-1,1,0.75,0.75,1], [-1.5,-1.5,-1.5,-1.5,-1.5], color = 'black') #North arrow
a = Wedge((0,0),1,180,0,  edgecolor = 'black', facecolor = 'none', linewidth = 0.1) #stereonet
b = Wedge((0,0),1,180,0,  edgecolor = 'black', facecolor = 'none', linewidth = 0.1) #stereonet
p = Circle((0,0), 1, edgecolor = 'black', facecolor = 'none', linewidth = 0.1) #stereonet
ax1.add_patch(a) #stereonet
ax1.add_patch(b) #stereonet
ax1.add_patch(p) #stereonet
art3d.pathpatch_2d_to_3d(a, z=0, zdir="x") #stereonet
art3d.pathpatch_2d_to_3d(b, z=0, zdir="y") #stereonet
art3d.pathpatch_2d_to_3d(p, z=0, zdir="z") #stereonet
ax1.plot_wireframe([0,0],[0,0],[0,-1], linewidth = 0.1 , color = 'black') #stereonet

ax1.set_axis_off()

ax1.set_xlim3d(-1,1)
ax1.set_ylim3d(-1,1)
ax1.set_zlim3d(-1,1)

plt.show()