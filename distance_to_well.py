# -*- coding: utf-8 -*-
"""
Uncertainty estimation and quantification is increasingly important in geo-
scientific and geotechnical applications. One approach is to quantify
uncertainty in terms of the distance to the next source of information (e.g,
outcrop, well, geophysical profile etc.).

Given a set of wells, this code computes and visualizes a raster that contains
information about the distances from each raster point to the next well.

Author: Dr. Georg H. Erharter
First version released: 24. October 2021
License: MIT License (license file in repository)
"""

from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import numpy as np


###############################################################################
# functions

def compute_grid_extent(well_dict: dict, DIST: float) -> list:
    ''' computes the extent of the distance grid beyond the wells'''
    coords = np.array(list(well_dict.values()))
    x_coords, y_coords = coords[:, 0], coords[:, 1]

    ll = np.array([x_coords.min()-DIST, y_coords.min()-DIST])
    ur = np.array([x_coords.max()+DIST, y_coords.max()+DIST])

    return ll, ur


def compute_grid_coords(ll, ur, RESOLUTION) -> list:
    ''' computes the coordinates of the grid points '''
    xs = np.linspace(ll[0], ur[0], num=int((ur[0] - ll[0]) / RESOLUTION))
    ys = np.linspace(ll[1], ur[1], num=int((ur[1] - ll[1]) / RESOLUTION))
    xs, ys = np.meshgrid(xs, ys)
    # return coordinates and shape of grid
    return xs, ys


def distance(x: float, y: float, well: list) -> float:
    ''' computes the distance between x-y coordinates and a well '''
    dist_x = np.abs(x - well[0])
    dist_y = np.abs(y - well[1])

    return np.sqrt(dist_x**2 + dist_y**2)


###############################################################################
# static variables / constants and well dictionary

DIST = 30  # [m] extend of grid beyond wells
RESOLUTION = 1  # [m]  resolution of grid
SAVE_RASTER = False  # whether or not a .csv raster should be saved
SAVE_IMAGE = True  # whether or not an image of the distances should be saved

# dictionary with wells: keys= well names, values= well koordinates
# exemplary wells
wells = {'W0': [1000, 1000],
         'W1': [1005, 1020],
         'W2': [1011, 1043],
         'W3': [1030, 1085],
         'W4': [1070, 1035],
         'W5': [900, 970],
         'W6': [990, 950],
         'W7': [1090, 945]}

###############################################################################
# computation of distances

ll, ur = compute_grid_extent(wells, DIST)
xs, ys = compute_grid_coords(ll, ur, RESOLUTION)

# compute min distance between each grid point and all wells
dists = [distance(xs, ys, well) for well in list(wells.values())]
distance_grid = np.dstack(dists).min(axis=2)

# eventually save result as coordinates with scalar values
if SAVE_RASTER is True:
    distance_raster = np.vstack((xs.flatten(), ys.flatten(),
                                 distance_grid.flatten())).T
    np.savetxt(r'distance_raster.csv', distance_raster, delimiter=',')

###############################################################################
# result visualization

fig, ax = plt.subplots(figsize=(8, 6))

# add raster image to plot
im = ax.imshow(distance_grid, cmap='RdYlGn_r', origin='lower',
               extent=(ll[0]-RESOLUTION/2, ur[0]+RESOLUTION/2,
                       ll[1]-RESOLUTION/2, ur[1]+RESOLUTION/2))

# add distance contour lines to plot
CS = ax.contour(xs, ys, distance_grid,
                colors='black', alpha=0.5, origin='lower',
                extent=(ll[0]-RESOLUTION/2, ur[0]+RESOLUTION/2,
                        ll[1]-RESOLUTION/2, ur[1]+RESOLUTION/2))

ax.clabel(CS, CS.levels, inline=True, fmt='%d')

# add well positions to plot
for i, d in enumerate(list(wells.values())):
    ax.scatter(d[0], d[1], color='grey', edgecolor='black', marker='D')
    ax.annotate(list(wells.keys())[i], (d[0]+1, d[1]+1))

# add colorbar to plot
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)

cbar = plt.colorbar(im, cax=cax)
cbar.set_label('distance to wells [m]')

# add title to plot
ax.set_title('exemplary well-distance uncertainty estimation')

plt.tight_layout()
# eventually save a visualization of the distance map
if SAVE_IMAGE is True:
    plt.savefig('distance_to_wells.png', dpi=600)
