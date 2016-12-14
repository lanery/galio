# -*- coding: utf-8 -*-
"""
@Author: ryanlane
@Date:   2016-10-30 11:38:13
@Last Modified by:   ryanlane
@Last Modified time: 2016-10-30 12:03:45
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Column(object):
    """docstring for Column"""
    def __init__(self, lenses):
        super(Column, self).__init__()
        self.lenses = lenses
        self.zo = zo
        self.zi = zi
