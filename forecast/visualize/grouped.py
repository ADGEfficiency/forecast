import matplotlib.pyplot as plt
import numpy as np

from .savefig import savefig


plt.style.use('ggplot')


@savefig
def plot_grouped(
        df, 
        y, 
        group_type='year_and_month'):

    if group_type == 'year_and_month':
        group_idx = [df.index.year, df.index.month]

    elif group_type == 'month':
        group_idx = [df.index.month]

    elif group_type == 'hour':
        group_idx = [df.index.hour]

    else:
        raise ValueError('group_type of {} not supported'.format(group_type))

    groups = df.groupby(group_idx).agg(
        {y: [np.mean, np.std, np.median, np.min, np.max]})

    fig, axes = plt.subplots(nrows=3, figsize=(15, 10))

    groups[y]['mean'].plot(ax=axes[0], kind='line')
    groups[y]['median'].plot(ax=axes[0], kind='line')
    groups[y]['std'].plot(ax=axes[1], kind='line')
    groups[y]['amin'].plot(ax=axes[2], kind='line')
    groups[y]['amax'].plot(ax=axes[2], kind='line')

    axes[0].set_title('{} grouped by {}'.format(y, group_type))

    for ax in axes:
        ax.legend()

    return fig
