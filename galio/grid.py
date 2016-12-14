# -*- coding: utf-8 -*-

"""
@Author: ryanlane
@Date:   2016-10-30 12:44:41
@Last Modified by:   Ryan Lane
@Last Modified time: 2016-11-28 01:16:05
"""


import numpy as np


class Grid(object):
    """docstring for Grid"""
    def __init__(self, nx=10, ny=10, xmin=0, xmax=10, ymin=0, ymax=10):
        super(Grid, self).__init__()

        self.nx = nx
        self.ny = ny
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self.dx = (xmax - xmin) / (nx - 1)
        self.dy = (ymax - xmin) / (ny - 1)

        self.u = np.zeros((nx, ny))
        self.old_u = self.u.copy()

    def compute_error(self):
        """
        Computes absolute error using an L2 norm for the solution

        Notes
        ----
        self.u and self.old_u must be appropriately
        setup.
        """
        v = (self.u - self.old_u).flat
        return np.sqrt(np.dot(v, v))

    def laplace(self):
        """
        Algorithm used for solving Laplace's Equation.
        """
        dx2, dy2 = self.dx**2, self.dy**2
        dnr = 2 * (dx2 + dy2)
        u = self.u
        self.old_u = u.copy()

        u[1:-1, 1:-1] = np.where(u[1:-1, 1:-1] < 1,
            ((u[0:-2, 1:-1] + u[2:, 1:-1]) * dy2 +
             (u[1:-1, 0:-2] + u[1:-1, 2:]) * dx2) * 1/dnr, 1)

        return self.compute_error()

    def solve(self, n_iter=0, eps=1.0e-3):
        """ Method used for iterating Grid.laplace """
        err = self.laplace()
        c = 0
        while err > eps:
            if n_iter and c >= n_iter:
                return err
            err = self.laplace()
            c += 1
        return c

    def reset(self):
        self.u.fill(0)
        return self
