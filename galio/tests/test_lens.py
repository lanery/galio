# -*- coding: utf-8 -*-

"""
@Author: Ryan Lane
@Date:   2016-11-25 17:00:38
@Last Modified by:   Ryan Lane
@Last Modified time: 2016-11-27 01:06:00
"""


import numpy as np
import pandas as pd
import nose.tools as nt
import numpy.testing as npt
import pandas.util.testing as pdt

from .. import lens
from .. import electrode


def create_generic_lens():
    L = lens.Lens(z=0)

    e1_coords = [[1, 1], [5, 1],
                 [5, 5], [1, 5]]
    e2_coords = [[9, 2], [14, 2],
                 [12, 6]]

    e1 = electrode.Electrode(1, e1_coords)
    e2 = electrode.Electrode(2, e2_coords)

    return L, e1, e2


def test_lens_creation():
    L = lens.Lens(z=0, electrodes=[], nx=10, ny=10,
                  xmin=0, xmax=10, ymin=0, ymax=10)
    assert L.z == 0
    assert L.electrodes == []
    assert L.nx == 10
    assert L.ny == 10
    assert L.xmin == 0
    assert L.xmax == 10
    assert L.ymin == 0
    assert L.ymax == 10


def test_add_electrode():
    L, e1, e2 = create_generic_lens()
    L.reset_lens()

    L.add_electrode(e1)
    assert L.electrodes == [e1]

    L.add_electrode(e2)
    assert L.electrodes == [e1, e2]

    e3 = electrode.Electrode(5, [[8, 13], [4, 20], [5, 12]])
    L.add_electrode([e1, e2, e3])
    assert L.electrodes == [e1, e2, e3]


def test_rem_electrode():
    L, e1, e2 = create_generic_lens()
    L.reset_lens()

    L.add_electrode([e1, e2])
    L.rem_electrode(e1)
    assert len(L.electrodes) == 1
    assert L.electrodes[0] == e2

    L.add_electrode(e1)
    L.rem_electrode([e1, e2])
    assert L.electrodes == []



