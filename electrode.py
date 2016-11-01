# -*- coding: utf-8 -*-
"""
@Author: ryanlane
@Date:   2016-10-30 02:10:04
@Last Modified by:   ryanlane
@Last Modified time: 2016-10-31 22:14:50
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


class Electrode(object):
    """docstring for Electrode"""
    def __init__(self, V, coords):
        super(Electrode, self).__init__()
        self.V = V
        self.coords = np.array(coords)
        self.poly = Polygon(coords)

    def get_potential(self):
        return self.V

    def get_coords(self):
        return self.coords

    def get_polygon(self):
        return self.poly

    def transform(self, lens):
        """ Transform electrode coords to lens grid. """
        self.coords[:,0] = (
            self.coords[:,0] * lens.nx / (lens.xmax - lens.xmin))
        self.coords[:,1] = (
            self.coords[:,1] * lens.ny / (lens.ymax - lens.ymin))
        return self


if __name__ == '__main__':
    e1_coords = [[0, 0], [5, 0],
                 [5, 5], [0, 5]]
    e1 = Electrode(10, e1_coords)


    fig, ax = plt.subplots()
    ax.add_patch(e1.poly)

    ax.set_xlim(-5, 10)
    ax.set_ylim(-5, 10)
    ax.set_aspect('equal')
