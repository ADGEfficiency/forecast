"""
A collection of generic sklearn pipelines

TODO
- test for RollingSum
"""

import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class AlignPandas(BaseEstimator, TransformerMixin):

    def __init__(self, LAGS, HORIZIONS):
        self.max_lag = max(LAGS)
        self.max_horizion = max(HORIZIONS)

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        #  catching the edge case with a hack!
        if self.max_horizion == 0:
            self.max_horizion = 1

        if isinstance(x, pd.Series):
            return x.iloc[self.max_lag:-self.max_horizion]
        elif isinstance(x, pd.DataFrame):
            return x.iloc[self.max_lag:-self.max_horizion, :]
        else:
            raise ValueError('The AlignPandas pipeline uses pandas objects')


class AsMatrix(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        rows = x.shape[0]
        return x.as_matrix().reshape(rows, -1)


class BinaryLabels(BaseEstimator, TransformerMixin):
    """
    Takes a series and converts it into a series of binary labels
    """

    def __init__(self, thresh):
        self.thresh = thresh

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        assert isinstance(x, pd.Series)
        out = pd.Series(np.zeros(x.shape[0]),

                        index=x.index)
        out.loc[x > self.thresh] = 1
        out = out.astype(int)

        return out


class ColumnSelector(BaseEstimator, TransformerMixin):

    def __init__(self, columns):
        self.columns = columns

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x.loc[:, self.columns]


class ColumnDropper(BaseEstimator, TransformerMixin):

    def __init__(self, columns):
        assert(isinstance(columns, list))
        self.columns = columns

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x.drop(self.columns, axis=1)


class RollingSum(BaseEstimator, TransformerMixin):
    """
    A rolling sum excluding the current observation

    nan values that occur at the top of the transformation are
    filled with 0
    """
    def __init__(self, window):
        self.window = window

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x.shift(1).rolling(
            window=self.window,
            min_periods=1
        ).sum().fillna(0)


class DropNans(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x.dropna(axis=0)


class HourlyCyclicalFeatures(BaseEstimator, TransformerMixin):
    """
    args
    """
    hours_in_day = 24

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        h = x.index.hour

        sin = np.sin(2 * np.pi * h / self.hours_in_day)
        cos = np.cos(2 * np.pi * h / self.hours_in_day)

        out = pd.DataFrame(index=x.index)
        out.loc[:, 'sin_h'] = sin
        out.loc[:, 'cos_h'] = cos

        return out

class HalfHourlyCyclicalFeatures(BaseEstimator, TransformerMixin):
    """
    args
    """
    hours_in_day = 24

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        hh = x.index.hour + (x.index.minute / 60)

        sin = np.sin(2 * np.pi * hh / self.hours_in_day)
        cos = np.cos(2 * np.pi * hh / self.hours_in_day)

        out = pd.DataFrame(index=x.index)
        out.loc[:, 'sin_hh'] = sin
        out.loc[:, 'cos_hh'] = cos

        return out


class CyclicalFeatures(BaseEstimator, TransformerMixin):

    def __init__(self, max_value):
        self.max_value = max_value

    def fit(self, x, y=None):
        return self

    def transform(self, x):

        sin = np.sin(2 * np.pi * x / self.max_value)
        cos = np.cos(2 * np.pi * x / self.max_value)

        out = pd.DataFrame(index=x.index)
        out.loc[:, 'sin_hh'] = sin
        out.loc[:, 'cos_hh'] = cos

        return out



class OffsetGenerator(BaseEstimator, TransformerMixin):
    """
    args
        mode (str) either lag or horizion
        offsets (list)
    """
    def __init__(self, mode, offsets):
        self.mode = mode
        self.offsets = offsets

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        """
        Not dropping na

        .shift(positive) -> lag
        .shift(negative) -> horizion
        """
        if self.mode == 'lag':
            shifted = [x.shift(abs(o), axis=0) for o in self.offsets]
            return pd.concat(shifted, axis=1)

        elif self.mode == 'horizion':
            shifted = [x.shift(-abs(o), axis=0) for o in self.offsets]
            return pd.concat(shifted, axis=1)

        else:
            raise ValueError('Mode of {} is not correct'.format(self.mode))


class WeekendDummy(BaseEstimator, TransformerMixin):
    """
    Creates a dummy column indicating weekday or weekend
    """
    #  the threshold for the .weekday method on a pandas dt index
    thresh = 5

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        """
        create a column of zeros, fill in the weekends using boolean indexing
        """
        dummies = pd.DataFrame(np.zeros(x.shape[0]),
                               index=x.index,
                               columns=['Weekday/Weekend Dummy'])
        dummies.loc[x.index.weekday >= self.thresh, 'Weekday/Weekend Dummy'] = 1
        return dummies
