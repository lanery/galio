# -*- coding: utf-8 -*-

"""
@Author: ryanlane
@Date:   2016-10-30 10:01:29
@Last Modified by:   Ryan Lane
@Last Modified time: 2016-11-25 23:41:31
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path

from grid import Grid
from electrode import Electrode


class Lens(Grid):
    """docstring for Lens"""

    def __init__(self, z, electrodes=[],
                 nx=101, ny=51, xmin=0, xmax=30, ymin=0, ymax=10):
        super(Lens, self).__init__(
            nx, ny, xmin, xmax, ymin, ymax)
        self.z = z
        self.electrodes = electrodes

    def add_electrode(self, electrode):
        """
        Add one or more electrodes to lens.
        TODO: handle everything
        """
        if isinstance(electrode, Electrode):
            if electrode not in self.electrodes:
                self.electrodes.append(electrode)
        elif isinstance(electrode, list):
            self.electrodes += electrode
        else:
            raise TypeError('`electrode` must be one of ')


    def rem_electrode(self, electrode):
        """ """
        try:
            self.electrodes.remove(electrode)
        except ValueError:
            raise ValueError('Specified electrode not in lens.')
        return self

    def get_electrodes(self):
        return self.electrodes

    def electrodes_to_grid(self):
        """ """
        for electrode in self.electrodes:
            u_pts = np.indices(self.u.shape).reshape(2, -1).T
            coords_t = electrode.transform(self)
            path = Path(coords_t)
            mask = path.contains_points(u_pts, radius=1e-9)
            mask = mask.reshape(self.u.shape).astype(self.u.dtype)
            self.u = self.u + mask
        return self

    def solve_lens(self, *args):
        """ """
        u_arr = []
        electrodes = self.electrodes[:]
        self.reset_lens()

        for e in electrodes:
            self.add_electrode(e)
            self.electrodes_to_grid()
            self.solve(*args)
            u_arr.append(self.u.copy())
            self.rem_electrode(e)
            self.reset()

        self.u_arr = np.array(u_arr)
        self.u = np.sum(self.u_arr, axis=0)
        self.electrodes = electrodes
        return self

    def reset_lens(self):
        """ """
        self.reset()
        for e in self.electrodes[:]:
            self.rem_electrode(e)
        return self



def imshow_(arr, ax, *kwargs):
    img = ax.imshow(arr.T, interpolation='nearest', origin='lower',
                    cmap='Greys')
    return img


if __name__ == '__main__':

    e1_coords = [[1, 1], [5, 1],
                 [5, 5], [1, 5]]
    e2_coords = [[9, 2], [14, 2],
                 [12, 6]]

    e1 = Electrode(10, e1_coords)
    e2 = Electrode(100, e2_coords)

    L1 = Lens(0, electrodes=[], nx=301, ny=101)
    L1.add_electrode(e1)
    L1.add_electrode(e2)
    L1.electrodes_to_grid()

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.add_patch(e1.poly)
    ax1.add_patch(e2.poly)

    ax1.set_xlim(L1.xmin, L1.xmax)
    ax1.set_ylim(L1.ymin, L1.ymax)
    ax1.set_aspect('equal')

    imshow_(L1.u, ax2)

    L1.solve_lens(1000)

    img = ax2.contour(L1.u.T, interpolation='nearest', origin='lower')
    plt.colorbar(img)
    ax2.set_aspect('equal')
