"""
Generic matplotlib functions

All functions pass **kwargs into the .plot call

All functions have figsize as an optional kwarg
"""

import matplotlib.pyplot as plt
import numpy as np


plt.style.use('ggplot')


def plot_scatter(
        df,
        x,
        y,
        figsize=(10, 10),
        **kwargs):

    f, a = plt.subplots(figsize=figsize)
    df.plot(x=x, y=y, kind='scatter', ax=a, **kwargs)

    return f


def plot_time_series(
        hh_data,
        y,
        fig_name=None,
        figsize=(25, 10),
        **kwargs):

    if isinstance(y, str):
        y = [y]

    f, a = plt.subplots(figsize=figsize, nrows=len(y), sharex=True)
    a = np.array(a).flatten()

    for idx, y_label in enumerate(y):
        a[idx].set_title(y_label)
        hh_data.plot(y=y_label, ax=a[idx], **kwargs)

    if fig_name:
        f.savefig(fig_name)

    return f
