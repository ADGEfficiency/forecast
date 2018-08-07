"""
Generic matplotlib functions

All functions pass **kwargs into the .plot call

All functions have figsize as an optional kwarg
"""

import matplotlib.pyplot as plt
import numpy as np


plt.style.use('ggplot')


def savefig(plot_func):
    """ Decorator to save figure to .png """

    def wrapper(*args, **kwargs):

        try:
            fig_name = kwargs.pop('fig_name')
        except KeyError:
            pass

        fig = plot_func(*args, **kwargs)

        if fig_name:
            fig.savefig(fig_name)

        return fig

    return wrapper


@savefig
def plot_scatter(
        df,
        x,
        y,
        figsize=(10, 10),
        **kwargs):

    f, a = plt.subplots(figsize=figsize)
    df.plot(x=x, y=y, kind='scatter', ax=a, **kwargs)

    return f


@savefig
def plot_time_series(
        data,
        y,
        figsize=(25, 10),
        **kwargs):

    if isinstance(y, str):
        y = [y]

    f, a = plt.subplots(figsize=figsize, nrows=len(y), sharex=True)
    a = np.array(a).flatten()

    for idx, y_label in enumerate(y):
        a[idx].set_title(y_label)
        data.plot(y=y_label, ax=a[idx], **kwargs)

    return f


@savefig
def plot_grouped(
        df, 
        column, 
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
        {column: [np.mean, np.std, np.median, np.min, np.max]})

    fig, axes = plt.subplots(nrows=3, figsize=(15, 10))

    groups[column]['mean'].plot(ax=axes[0], kind='line')
    groups[column]['median'].plot(ax=axes[0], kind='line')
    groups[column]['std'].plot(ax=axes[1], kind='line')
    groups[column]['amin'].plot(ax=axes[2], kind='line')
    groups[column]['amax'].plot(ax=axes[2], kind='line')

    axes[0].set_title('{} grouped by {}'.format(column, group_type))

    for ax in axes:
        ax.legend()

    return fig


@savefig
def plot_distribution(df, column):

    fig, axes = plt.subplots(ncols=2, figsize=(12, 5))

    series = df.loc[:, column]

    series.plot(ax=axes[0], kind='hist', bins=1000)
    series.plot(ax=axes[1], kind='kde')

    xlim = series.mean() + series.std() * 3

    for ax in axes:
        ax.set_xlim([-xlim, xlim])
        ax.set_xlabel(column)

    return fig
