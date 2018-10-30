import pandas as pd
import numpy as np

from pipelines import OffsetGenerator, WeekendDummy, HalfHourlyCyclicalFeatures, BinaryLabels, RollingSum	

data = np.arange(10).reshape(-1, 2)
DATA = pd.DataFrame(data)


def test_simple_lag():
    offsetter = OffsetGenerator('lag', [1])

    lagged = offsetter.transform(DATA)

    assert pd.isnull(lagged.iloc[0, 1])
    assert lagged.iloc[2, 0] == 2
    assert lagged.iloc[4, 1] == 7


def test_complex_lag():
    offsetter = OffsetGenerator('lag', [2, 3])

    lagged = offsetter.transform(DATA)

    assert pd.isnull(lagged.iloc[0, 0])
    assert pd.isnull(lagged.iloc[1, 1])
    assert lagged.iloc[2, 0] == 0
    assert lagged.iloc[4, 1] == 5

    assert pd.isnull(lagged.iloc[2, 3])
    assert lagged.iloc[3, 3] == 1
    assert lagged.iloc[4, 2] == 2


def test_simple_horizion():
    offsetter = OffsetGenerator('horizion', [1])

    horizions = offsetter.transform(DATA)

    assert horizions.iloc[0, 0] == 2
    assert horizions.iloc[0, 1] == 3
    assert horizions.iloc[2, 0] == 6
    assert pd.isnull(horizions.iloc[4, 1])


def test_complex_horizion():
    offsetter = OffsetGenerator('horizion', [2, 3])

    horizions = offsetter.transform(DATA)

    assert horizions.iloc[0, 1] == 5
    assert horizions.iloc[1, 0] == 6
    assert pd.isnull(horizions.iloc[3, 1])
    assert pd.isnull(horizions.iloc[4, 0])

    assert horizions.iloc[0, 2] == 6
    assert horizions.iloc[1, 3] == 9
    assert pd.isnull(horizions.iloc[2, 3])
    assert pd.isnull(horizions.iloc[4, 2])

def test_hh_cyclical_features():
    test_index = pd.DatetimeIndex(start='01/01/2018',
                                  end='31/12/2018',
                                  freq='30min')
    test_df = pd.DataFrame(np.random.uniform(size=test_index.shape[0]), index=test_index)

    hh_features_generator = HalfHourlyCyclicalFeatures()

    hh_features = hh_features_generator.transform(test_df)
    assert hh_features.iloc[0, :].values.all() == hh_features.iloc[48, :].values.all()
    assert hh_features.iloc[400, :].values.all() == hh_features.iloc[448, :].values.all()
    assert not np.array_equal(hh_features.iloc[0, :].values , hh_features.iloc[5, :].values)

    #  check that each value is unique for the entire day
    assert not hh_features.iloc[:48, :].duplicated().any()
    #  check that we do have unique values across a longer time period
    assert hh_features.iloc[:, :].duplicated().any()


def test_weekend_dummy():
    test_index = pd.DatetimeIndex(start='01/01/2018',
                                  end='01/14/2018',
                                  freq='24h')
    test_df = pd.DataFrame(np.zeros(14), index=test_index)
    weekend_dummies = WeekendDummy().transform(test_df)
    assert np.mean(weekend_dummies.values) == 2/7


def test_binary_labels():
    b = BinaryLabels(thresh=0)
    test = pd.Series([0, 1, 0.5, -1])
    o = b.transform(test)
    assert o.values.all() == np.array([0, 1, 1, 0], dtype=int).all()
    assert np.min(o) == 0
    assert np.max(o) == 1


def test_rolling_sum_simple_2():
    data = pd.DataFrame(np.arange(6).reshape(-1))
    expected = np.array([0,0,1,3,5,7])
    trans = RollingSum(2).transform(data)
    np.testing.assert_array_equal(trans.values.flatten(), expected)
    
def test_rolling_sum_simple_3():
    data = pd.DataFrame(np.arange(6).reshape(-1))
    expected = np.array([0,0,1,3,6,9])
    trans = RollingSum(3).transform(data)
    np.testing.assert_array_equal(trans.values.flatten(), expected)

def test_complex_rolling_sum():
    data = pd.DataFrame(np.arange(10).reshape(-1, 2))
    expected = np.array([[0,0,2,6,10], [0,1,4,8,12]]).T
    trans = RollingSum(2).transform(data)

    np.testing.assert_array_equal(trans.values, expected)
