# -*- coding: utf-8 -*-
'''
The primary use of this program is to plot great circles and poles of
structural geological orientation data onto a lower hemisphere projection.
More sophisticated applications like whole sphere projections will eventually
be implemented in future versions.
The better part of the math behind this comes from the book:

Richard E. Goodman & Gen-hua Shi (1985) "Block Theory and Its Application to
Rock Engineering"

freely available under:

https://www.rocscience.com/assets/resources/learning/Block-Theory-and-Its-Application-to-Rock-Engineering.pdf
'''

import matplotlib.pyplot as plt
import numpy as np


class stereonet:

    def __init__(self, color='black', figsize=(6, 6),
                 only_reference_circle=True, grid_steps=10):

        self.color = color
        self.figsize = figsize
        self.only_reference_circle = only_reference_circle
        self.grid_steps = grid_steps

    # calc_small_circle() is used for drawing the stereonet's grid only
    def calc_small_circle(self, kd):

        R = np.tan(np.radians(kd))  # radius
        Cx = 0
        Cy = 1/np.cos(np.radians(kd))
        return Cx, Cy, R

    # draw stereonet grid (wulff met)
    def draw_stereonet(self):

        fig, ax = plt.subplots()

        ref_circle = plt.Circle((0, 0), 1, color=self.color,
                                fill=None, linewidth=1.4, zorder=3)
        ax.add_artist(ref_circle)

        # to hide the second hemisphere and add annotations
        if self.only_reference_circle == True:
            ax.text(0, 1.05, '0° / 360°', horizontalalignment='center',
                    verticalalignment='center')
            ax.text(1.05, 0, '90°', verticalalignment='center',
                    horizontalalignment='left')
            ax.text(0, -1.05, '180°', horizontalalignment='center',
                    verticalalignment='center')
            ax.text(-1.05, 0, '270°', verticalalignment='center',
                    horizontalalignment='right')

            inner, outer = 1, 10  # taken from: https://stackoverflow.com/questions/22789356/plot-a-donut-with-fill-or-fill-between-use-pyplot-in-matplotlib
            x = np.linspace(-outer, outer, 1000, endpoint=True)
            # x-axis values -> outer circle
            yO = outer*np.sin(np.arccos(x/outer))
            # x-axis values -> inner circle (with nan's beyond circle)
            yI = inner*np.sin(np.arccos(x/inner))
            # yI now looks like a boulder hat, meeting yO at the outer points
            yI[np.isnan(yI)] = 0.
            ax.fill_between(x, yI, yO, color="white", zorder=2)
            ax.fill_between(x, -yO, -yI, color="white", zorder=2)

        # horizontal grid line
        ax.plot((-100, 100), (0, 0), color='grey', linewidth=0.2, zorder=1)
        # vertical grid line
        ax.plot((0, 0), (-100, 100), color='grey', linewidth=0.2, zorder=1)

        # draw great circles
        for dipdir in [270, 90]:
            background_dips = np.arange(0, 90, step=self.grid_steps)
            self.plot_great_circles(background_dips,
                                    np.full(background_dips.shape, dipdir),
                                    add_to_snet=True, colors=['grey'],
                                    linewidth=0.2, linestyle='-')

        # draw small circles
        for dip in np.arange(10, 90, step=self.grid_steps):
            SC_params = self.calc_small_circle(dip)
            SC_pos = plt.Circle((SC_params[0], SC_params[1]), SC_params[2],
                                color='grey', fill=None, linewidth=0.2)
            SC_neg = plt.Circle((SC_params[0], -SC_params[1]), SC_params[2],
                                color='grey', fill=None, linewidth=0.2)
            ax.add_artist(SC_pos)
            ax.add_artist(SC_neg)

        ax.axis('equal')
        ax.axis([-1.1, 1.1, -1.1, 1.1])
        ax.set_axis_off()
        fig.set_size_inches(self.figsize)

    def calc_normal_vectors(self, dips, dipdirs):

        # calculate upward directed normals
        n_X = np.sin(np.radians(dips)) * np.sin(np.radians(dipdirs))
        n_Y = np.sin(np.radians(dips)) * np.cos(np.radians(dipdirs))
        n_Z = np.cos(np.radians(dips))
        return n_X, n_Y, n_Z

    def calc_two_d_poles(self, n_vecs):

        pole_x = n_vecs[0] / (1 + n_vecs[2])
        pole_y = n_vecs[1] / (1 + n_vecs[2])
        return -pole_x, -pole_y

    def plot_poles(self, dips, dipdirs, add_to_snet=False, color='black'):

        if add_to_snet == False:
            self.draw_stereonet()
        ax = plt.gca()

        plane_poles = self.calc_two_d_poles(self.calc_normal_vectors(dips,
                                                                     dipdirs))

        # poles become smaler in larger datasets
        if 12 - 1*np.log(len(dips)) > 0.1:
            size = 12 - 1*np.log(len(dips))
        else:
            size = 0.1

        ax.scatter(plane_poles[0], plane_poles[1], color=color,
                   s=size, zorder=4)

    def plot_great_circles(self, dips, dipdirs,
                           add_to_snet=False, colors=[], linewidth=1,
                           linestyle='-'):

        if add_to_snet == False:
            self.draw_stereonet()
        else:
            ax = plt.gca()

        # calculates parameters to plot circles (i.e. center coordinates and
        # radius)
        def calc_great_circle_params(dip, dipdir):
            if dip == 90:
                return [0, 0, 0]
            else:
                R = 1/(np.cos(np.radians(dip)))  # radius
                center_x = np.tan(np.radians(dip))*np.sin(np.radians(dipdir))
                center_y = np.tan(np.radians(dip))*np.cos(np.radians(dipdir))
                return -center_x, -center_y, -R

        # function calculates the coordinates of the straight line that
        # represents a vertical plane. ...otherwise an infinite large
        # circle would be required.
        def calc_vertical_plane_params(dipdir):
            if dipdir < 90:
                x_coord = np.cos(np.radians(dipdir))
                y_coord = -np.sin(np.radians(dipdir))
            elif dipdir > 90 and dipdir < 180:
                x_coord = np.sin(np.radians(dipdir - 90))
                y_coord = np.cos(np.radians(dipdir - 90))
            elif dipdir > 180 and dipdir < 270:
                x_coord = -np.cos(np.radians(dipdir - 180))
                y_coord = np.sin(np.radians(dipdir - 180))
            else:
                x_coord = np.sin(np.radians(dipdir - 270))
                y_coord = np.cos(np.radians(dipdir - 270))

            return x_coord*100, y_coord*100

        colors = (len(dips))*colors

        for i in range(len(dips)):
            GC = calc_great_circle_params(dips[i], dipdirs[i])
            if GC[2] == 0:
                if dipdirs[i] == 270 or dipdirs[i] == 90:
                    # vertical line:
                    ax.plot((0, 0), (-100, 100), color=colors[i],
                            linewidth=linewidth, linestyle=linestyle,
                            zorder=1)
                elif dipdirs[i] == 360 or dipdirs[i] == 180 or dipdirs[i] == 0:
                    # horizontal line:
                    ax.plot((-100, 100), (0, 0), color=colors[i],
                            linewidth=linewidth, linestyle=linestyle,
                            zorder=1)
                else:
                    x_coord, y_coord = calc_vertical_plane_params(dipdirs[i])
                    ax.plot((-x_coord, x_coord), (-y_coord, y_coord),
                            color=colors[i], linewidth=linewidth,
                            linestyle=linestyle, zorder=1)
            else:
                GC = plt.Circle((GC[0], GC[1]), GC[2], fill=None,
                                color=colors[i], linewidth=linewidth,
                                linestyle=linestyle)
                ax.add_artist(GC)


#### example plot #####

# generates a synthetical joint set

def joint_set(dipdir, dip, dip_std=20, dipdir_std=20, size=100):
    dips = np.random.normal(dip, dip_std, size)
    dips = np.where(dips > 90, 90 - (dips - 90), dips)
    dips = np.where(dips < 0, dips*-1, dips)
    dipdirs = np.random.normal(dipdir, dipdir_std, size)
    dipdirs = np.where(dipdirs > 360, dipdirs - 360, dipdirs)
    dipdirs = np.where(dipdirs < 0, 360 + dipdirs, dipdirs)

    return dips, dipdirs


snet = stereonet(only_reference_circle=True, figsize=(6, 6))

snet.draw_stereonet()

colors = ['blue', 'red', 'green', 'yellow', 'cyan', 'orange']


for i in range(3):
    js = joint_set(dipdir=np.random.randint(0, 361, size=1),
                   dip=np.random.randint(0, 91, 1),
                   dip_std=np.random.randint(0, 20, 1),
                   dipdir_std=np.random.randint(0, 30, 1),
                   size=np.random.randint(10, 50, 1))
    snet.plot_poles(js[0], js[1], add_to_snet=True, color=colors[i])
    snet.plot_great_circles(js[0], js[1], add_to_snet=True, colors=[colors[i]])
