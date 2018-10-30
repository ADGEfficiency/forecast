import numpy as np
import pandas as pd

from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import forecast.pipelines as p


if __name__ == '__main__':

    clean = pd.read_csv('./data/clean.csv', index_col=0, parse_dates=True)

    train, test = train_test_split(clean, test_size=0.3, shuffle=False)
    train_index, test_index = train.index, test.index

    HORIZIONS = [0, 1, 2, 3]
    LAGS = [1, 2, 3, 24, 48]

    make_target = make_pipeline(
        p.ColumnSelector('Imbalance_price [£/MWh]'),
        p.OffsetGenerator('horizion', HORIZIONS),
        p.AlignPandas(LAGS, HORIZIONS),
        p.AsMatrix(),
        StandardScaler()
    )

    y_train = make_target.fit_transform(train)
    y_test = make_target.transform(test)

    make_features = make_union(
        make_pipeline(
            p.ColumnSelector('Imbalance_price [£/MWh]'),
            p.OffsetGenerator('lag', LAGS),
            p.AlignPandas(LAGS, HORIZIONS),
            p.AsMatrix(),
            StandardScaler()),
        make_pipeline(
            p.ColumnSelector('ImbalanceVol_[MW]'),
            p.OffsetGenerator('lag', LAGS),
            p.AlignPandas(LAGS, HORIZIONS),
            p.AsMatrix(),
            StandardScaler()),
         make_pipeline(
            p.HalfHourlyCyclicalFeatures(),
            p.AlignPandas(LAGS, HORIZIONS),
            p.AsMatrix()),
         )

    x_train = make_features.fit_transform(train)
    x_test = make_features.transform(test)

    feature_cols = ['price_lag_{}'.format(lag) for lag in LAGS]
    feature_cols += ['vol_lag_{}'.format(lag) for lag in LAGS]
    feature_cols += ['sin_h', 'cos_h']

    train_index = p.Align(LAGS, HORIZIONS).transform(train_index)
    test_index = p.Align(LAGS, HORIZIONS).transform(test_index)

    x_train = pd.DataFrame(
        x_train, index=train_index,
        columns=feature_cols
    )

    x_test = pd.DataFrame(
        x_test, index=test_index,
        columns=feature_cols
    )

    target_cols = ['price_horizion_{}'.format(hor) for hor in HORIZIONS]

    y_train = pd.DataFrame(
        y_train, index=train_index,
        columns=target_cols
    )

    y_test = pd.DataFrame(
        y_test, index=test_index,
        columns=target_cols
    )

    dataset = {
        'x_train': x_train,
        'y_train': y_train,
        'x_test': x_test,
        'y_test': y_test
    }

    for name, df in dataset.items():
        print('{} shape {}'.format(name, df.shape))
        df.to_csv('./data/{}.csv'.format(name))
