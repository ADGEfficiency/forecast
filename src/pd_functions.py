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
    dupes = df[df.index.duplicated()]
    num = dupes.shape[0]

    if num == 0:
        print('no duplicates found on the index')

    if num != 0:
        print('{} duplicates'.format(num))
        if verbose == True:
            print('duplicates are:')
            print(dupes.head())
        return dupes


def check_duplicate_rows(df, verbose=True):
    duplicated_bools = df.duplicated()
    num = np.sum(duplicated_bools)

    if num == 0:
        print('no duplicate rows found')

    if num != 0:
        print('{} duplicate values'.format(num))
        if verbose:
            print('duplicate values are {}'.format(
                df[duplicated_bools]))
        return df[duplicated_bools]


def check_nans(df, verbose=True):
    """
    Checks for NANs in a dataframe
    """
    nans = df[df.isnull().any(axis=1)]
    num = nans.shape[0]

    print('{} nans'.format(num))
    if num != 0:
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

    print('ideal index len {}'.format(ideal.shape[0]))
    print('actual index len {}'.format(df.shape[0]))

    if ideal.shape[0] != df.shape[0]:
        missing = set(df.index).symmetric_difference(set(ideal))
        if verbose:
            print('missing are:')
            print(missing)
        return missing


def check_dataframe(df, freq, verbose=True):
    """ wraps together all the checks """
    check_duplicate_index(df, verbose)

    check_duplicate_rows(df, verbose)

    check_nans(df, verbose)

    check_index_length(df, freq, verbose)
