import matplotlib.pyplot as plt
import numpy as np

from .savefig import savefig


plt.style.use('ggplot')


@savefig
def plot_time_series(
        data,
        y,
        figsize=(25, 10),
        same_plot=False,
        **kwargs):

    if isinstance(y, str):
        y = [y]

    if same_plot:
        nrows = 1

    else:
        nrows = len(y)

    f, axes = plt.subplots(figsize=figsize, nrows=nrows, sharex=True)
    axes = np.array(axes).flatten()

    for idx, y_label in enumerate(y):

        if same_plot:
            idx = 0

        axe = axes[idx]

        #  must be a better way - TODO
        if 'ymin' in kwargs:
            axe.set_ylim(ymin=kwargs.pop('ymin'))

        if 'ymax' in kwargs:
            axe.set_ylim(ymax=kwargs.pop('ymax'))

        axe.set_title(y_label)
        data.plot(y=y_label, ax=axe, **kwargs)


    f.suptitle(
        '{} to {}'.format(data.index[0], data.index[-1]),
         horizontalalignment='center',
         verticalalignment='top',
         size=16
    )


    return f

