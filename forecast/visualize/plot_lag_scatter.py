import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .savefig import savefig


plt.style.use('ggplot')


def plot_lag_scatter(data, column, lags=6):
    t = pd.DataFrame(data.loc[:, column])

    for lag in range(lags):
        t.loc[:, 'lag_{}'.format(lag)] = t.shift(lag)

    t.dropna(axis=0, inplace=True)

    t.head()

    sns.set(style="ticks")

    return sns.pairplot(t)

