# -*- coding: utf-8 -*-

"""
@Author: ryanlane
@Date:   2016-10-30 10:01:29
@Last Modified by:   Ryan Lane
@Last Modified time: 2016-12-13 23:14:05
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path

from .grid import Grid
from .electrode import Electrode


class Lens(Grid):
    """docstring for Lens"""

    def __init__(self, z=0, electrodes=None, *grid_args, **grid_kws):
        super(Lens, self).__init__(*grid_args, **grid_kws)
        self.z = z
        if electrodes is None:
            electrodes = []
        self.electrodes = electrodes
        self.reflected = False

    def add_electrode(self, electrode):
        """
        Add either an individual or a list of electrodes to lens.
        """
        if self.electrodes is None:
            self.electrodes = []

        if isinstance(electrode, Electrode):
            if electrode not in self.electrodes:
                self.electrodes.append(electrode)
        elif isinstance(electrode, list):
            for e in electrode:
                if e not in self.electrodes:
                    self.electrodes.append(e)
        else:
            raise TypeError('`electrode` must be either an Electrode object '
                            'or a list of Electrode objects.')
        return self

    def rem_electrode(self, electrode):
        """
        Remove either an individual or a list of electrodes from lens.
        """
        # if electrode == Electrode()
        if isinstance(electrode, Electrode):
            if electrode in self.electrodes:
                self.electrodes.remove(electrode)
        # if electrode == [Electrode(), Electrode(), ...]
        elif isinstance(electrode, list):
            for e in electrode:
                if e in self.electrodes:
                    self.electrodes.remove(e)
                else:
                    raise ValueError('Specified electrode not in lens.')
        # if electrode != Electrode() and
        #    electrode != [Electrode(), Electrode(), ...]
        else:
            raise TypeError('`electrode` must be either an Electrode object '
                            'or a list of Electrode objects.')
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

    def reflect_lens(self):
        """ Reflect lens across z-axis """
        u = self.u
        u_z0 = u[:, -1]
        u_top = u[:, :-1]
        u_bot = np.fliplr(u_top)

        u_reflected = np.hstack([u_top, u_z0[:, None], u_bot])
        self.u = u_reflected
        self.reflected = True
        return self

    def solve_lens(self, *args):
        """ """
        u_arr = []
        electrodes = self.electrodes[:]
        self.reset_lens()

        for e in electrodes:
            self.add_electrode(e)
            self.electrodes_to_grid()
            self.reflect_lens()
            self.solve(*args)
            u_arr.append(self.u.copy())
            self.rem_electrode(e)
            self.reset_lens()

        self.u_arr = np.array(u_arr)
        self.u = np.sum(self.u_arr, axis=0)
        self.electrodes = electrodes
        return self

    def reset_lens(self):
        """ """
        # if self.reflected:
        #     pass
        # self.reset()
        self.u = np.zeros((self.nx, self.ny))
        for e in self.electrodes[:]:
            self.rem_electrode(e)
        return self
