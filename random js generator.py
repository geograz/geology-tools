import random
import math
import matplotlib.pyplot as plt

#creates js orientations
n_js = random.randint(2,5)
dip = []
dipdir = []
setnr = []
n_planes = []

for i in range (n_js):
    dip.append(random.randint(0,90))
    dipdir.append(random.randint(0,360))
    setnr.append(i)
    n_planes.append(random.randint(30,100))

print(dip)
print(dipdir)
print(setnr)


#creates planes
dips = []
dipdirs = []
cluster_nr = []
    
for k in range(n_js):
    for i in range (n_planes[k]):
        dips.append(random.gauss(dip[k],10))
        dipdirs.append(random.gauss(dipdir[k],10))
        cluster_nr.append(k)
    
for i in range(len(dips)):
    if dips[i] > 90:
        dips[i] = 90-(dips[i]-90)
        if dipdirs[i] >= 180:
            dipdirs[i] = dipdirs[i]-180
        else:
            dipdirs[i] = dipdirs[i]+180

print(cluster_nr)

def pole_calculator(a,b):
    ### calculate upward directed normals
    n_X = []
    n_Y = []
    n_Z = []
    for i in range(len(a)):
        dip = float(a[i])
        dipdir = float(b[i])
        X = math.sin(math.radians(dip)) * math.sin(math.radians(dipdir)) #block theory eq. 3.11a
        Y = math.sin(math.radians(dip)) * math.cos(math.radians(dipdir)) #block theory eq. 3.11b
        Z = math.cos(math.radians(dip)) #block theory eq. 3.11c
        n_X.append(X)
        n_Y.append(Y)
        n_Z.append(Z)

    ### calculate position in reference circle for poles -> - for lower hemisphere
    coordinates = []
    pole_x = []
    pole_y = []
    for i in range(len(a)):
        x = n_X[i]/(1+n_Z[i])
        y = n_Y[i]/(1+n_Z[i])
        pole_x.append(-x)
        pole_y.append(-y)
    coordinates.append(pole_x)
    coordinates.append(pole_y)
    return coordinates

plane_poles = pole_calculator(dips, dipdirs)


ax1 = plt.gca()
ax1.cla()
ax1.set_xlim(-1.1,1.1)
ax1.set_ylim(-1.1,1.1)

ax1.scatter (plane_poles[0], plane_poles[1], label = 'poles', color = 'black', s = 1)

ref_circle = plt.Circle((0, 0), 1, color='black', fill=None)
ax1.add_artist(ref_circle)

fig = plt.gcf()
plt.axis('off')
fig.set_size_inches(6,6)
ax1 = fig.gca()
plt.show()
