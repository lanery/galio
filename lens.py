# -*- coding: utf-8 -*-
"""
@Author: ryanlane
@Date:   2016-10-30 10:01:29
@Last Modified by:   ryanlane
@Last Modified time: 2016-10-31 23:27:24
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path

from grid import Grid
from electrode import Electrode


class Lens(Grid):
    """docstring for Lens"""

    def __init__(self, z, electrodes, nx=101, ny=51,
                 xmin=0, xmax=30, ymin=0, ymax=10):
        super(Lens, self).__init__(
            nx, ny, xmin, xmax, ymin, ymax)
        self.z = z
        self.electrodes = electrodes

    def add_electrode(self, electrode, to_grid=True):
        """ """
        self.electrodes.append(electrode)

        if to_grid:
            u_pts = np.indices(self.u.shape).reshape(2, -1).T
            electrode.transform(self)
            path = Path(electrode.coords)
            mask = path.contains_points(u_pts, radius=1e-9)
            mask = mask.reshape(self.u.shape).astype(self.u.dtype)
            self.u = self.u + mask

        return self

    # def electrodes_2_grid(self):
    #     """ """
    #     for e in self.electrodes:
    #         u_pts = np.indices(self.u.shape).reshape(2, -1).T
    #         e.transform(self)
    #         path = Path(e.coords)
    #         mask = path.contains_points(u_pts, radius=1e-9)
    #         mask = mask.reshape(self.u.shape).astype(self.u.dtype)
    #         self.u = self.u + mask
    #     return self

    def get_electrodes(self):
        return self.electrodes





if __name__ == '__main__':

    e1_coords = [[0, 0], [5, 0],
                 [5, 5], [0, 5]]
    e2_coords = [[9, 2], [14, 2],
                 [12, 6]]

    e1 = Electrode(10, e1_coords)
    e2 = Electrode(20, e2_coords)

    L1 = Lens(0, electrodes=[e1, e2], nx=101, ny=51)
    L1.add_electrode(e1)
    L1.solve(1000)
    L1.add_electrode(e2)
    # L1.electrodes_2_grid()
    # L1.solve(1000)

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.add_patch(e1.poly)
    ax1.add_patch(e2.poly)

    ax1.set_xlim(L1.xmin, L1.xmax)
    ax1.set_ylim(L1.ymin, L1.ymax)

    ax1.set_aspect('equal')

    img = ax2.imshow(L1.u.T, interpolation='nearest', origin='lower')
    plt.colorbar(img)
    ax2.set_aspect('equal')
