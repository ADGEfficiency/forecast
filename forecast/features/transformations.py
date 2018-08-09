""" transformations of data - mostly for deseasonalizing """

import numpy as np
import pandas as pd
from scipy.stats import boxcox

from sklearn.base import BaseEstimator, TransformerMixin


test = np.random.uniform(size=10)

class BoxCox(BaseEstimator, TransformerMixin):
    """

    """
    def __init__(self):
        pass
    def fit(self, x, y=None):
        return self

    def transform(self, x):
        trans, lamb, confidence_intervals = boxcox(test)
        print('performed boxcox transformation')
        print('lambda {}'.format(lamb))
        print('confidence_intervals {}'.format(confidence_intervals))
        return trans
