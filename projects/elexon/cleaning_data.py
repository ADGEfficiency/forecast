"""
Cleans raw ELEXON data that was scraped using scrape_data.py

Each report requires a slightly different approach for cleaning
"""
import numpy as np
import pandas as pd

from forecast import check_dataframe


def print_duplicates(df):
    dupes = df[df.index.duplicated()]
    num = dupes.shape[0]
    print('{} duplicates'.format(num))
    if num != 0:
          print('duplicates are:')
          print(dupes.head())
    return num


def remove_duplicates(df):
    print('removing duplicates for {}'.format(df.columns))
    print_duplicates(df)
    return df[~df.index.duplicated(keep='first')]


def print_nans(df):
    nans = df[df.isnull().any(axis=1)]
    num = nans.shape[0]
    print('{} nans'.format(num))
    if num != 0:
        print('nan values are:')
        print(nans.head())
    return num


def fill_nans(df):
    print('filling nans in {}'.format(df.columns))
    print_nans(df)
    df = df.fillna(method='backfill')
    return df


def clean_price_data():
    price = pd.read_csv('./data/raw/B1770.csv', parse_dates=True)

    price = price.pivot_table(values='imbalancePriceAmountGBP',
                              index='time_stamp',
                              columns='priceCategory')

    price.index = pd.to_datetime(price.index)

    return remove_duplicates(price)


def clean_vol_data():
    vol = pd.read_csv('./data/raw/B1780.csv', index_col=0, parse_dates=True)

    vol = vol.set_index('time_stamp', drop=True).sort_index()

    vol.index = pd.to_datetime(vol.index)

    return remove_duplicates(vol)


if __name__ == '__main__':
    price = clean_price_data()
    vol = clean_vol_data()

    merged = pd.concat([price, vol], axis=1)

    idx = pd.DatetimeIndex(freq='30min', start=merged.index[0], end=merged.index[-1])
    out = pd.DataFrame(index=idx)

    out.loc[price.index, 'ImbalancePrice_excess_balance_[£/MWh]'] = price.loc[:, 'Excess balance']
    out.loc[price.index, 'ImbalancePrice_insufficient_balance_[£/MWh]'] = price.loc[:, 'Insufficient balance']
    out.loc[vol.index, 'ImbalanceVol_[MW]'] = vol.loc[:, 'imbalanceQuantityMAW']

    out['Imbalance_price [£/MWh]'] = np.where(
        out['ImbalanceVol_[MW]'] > 0,
        out['ImbalancePrice_excess_balance_[£/MWh]'],
        out['ImbalancePrice_insufficient_balance_[£/MWh]']
    )

    out = fill_nans(out)
    check_dataframe(out, freq='30min')

    out.to_csv('data/clean.csv')
