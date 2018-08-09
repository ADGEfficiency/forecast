""" Various helper functions for pandas """
import numpy as np
import pandas as pd


def make_dt_index(df, timestamp_col, dt_offset=None):
    df.index = pd.to_datetime(df.loc[:, timestamp_col],
                              format='%Y-%m-%dT%H:%M:%S.%f')

    if dt_offset:
        df.index = df.index + dt_offset

    df.drop(timestamp_col, axis=1, inplace=True)

    df.sort_index(inplace=True)

    return df


def check_duplicate_index(df, verbose=True):
    """
    Checks for duplicates in the index of a dataframe
    """
    dupes = df[df.index.duplicated(keep=False)]
    num = dupes.shape[0]
    print('{} index duplicates'.format(num))

    if verbose == True:
        print('duplicates are:')
        print(dupes.head(3))
    return dupes


def check_duplicate_rows(df, verbose=True):
    duplicated_bools = df.duplicated()
    num = np.sum(duplicated_bools)
    print('{} row duplicates'.format(num))

    if verbose:
        df[duplicated_bools].head(3)
    return df[duplicated_bools]


def check_nans(df, verbose=True):
    """
    Checks for NANs in a dataframe
    """
    nans = df[df.isnull().any(axis=1)]
    num = nans.shape[0]

    print('{} nans'.format(num))
    if verbose:
        print('nan values are:')
        print(nans.head())

    return nans


def check_index_length(df, freq, verbose=True):
    """
    Compare a DatetimeIndex with the expected length
    """
    ideal = pd.DatetimeIndex(start=df.index[0],
                             end=df.index[-1],
                             freq=freq)

    ideal_len = ideal.shape[0]
    actual_len = df.shape[0]
    num_missing = ideal_len - actual_len
    print('ideal index len {} actual {} missing {}'.format(
        ideal_len, actual_len, num_missing))

    if ideal.shape[0] != df.shape[0]:
        missing = set(df.index).symmetric_difference(set(ideal))
        if verbose:
            print('missing are:')
            print(missing)
        return missing, ideal


def check_dataframe(df, freq, verbose=False):
    """ wraps together all the checks """
    check_duplicate_index(df, verbose)

    check_duplicate_rows(df, verbose)

    check_nans(df, verbose)

    check_index_length(df, freq, verbose)
