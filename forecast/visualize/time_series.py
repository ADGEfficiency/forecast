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

    f, a = plt.subplots(figsize=figsize, nrows=nrows, sharex=True)
    a = np.array(a).flatten()

    for idx, y_label in enumerate(y):
        if same_plot:
            idx = 0
        a[idx].set_title(y_label)
        data.plot(y=y_label, ax=a[idx], **kwargs)

    f.suptitle(
        '{} to {}'.format(data.index[0], data.index[-1]),
         horizontalalignment='center',
         verticalalignment='top',
         size=16
    )

    return f

