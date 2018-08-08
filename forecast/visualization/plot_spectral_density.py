import matplotlib.pyplot as plt

import numpy as np
from scipy.signal import welch

from .savefig import savefig


plt.style.use('ggplot')


def plot_spectral_density(data, column):
    print("""
          The power spectral density

          Fourier transform of the autocorrelation

          """)

    fig, axes = plt.subplots(figsize=(25,10))

    freqs, psd = welch(
        data.loc[:, column].values,
        fs=1,
        window='hanning',
        nperseg=512,
        scaling='density'
    )

    plt.plot(freqs, np.sqrt(psd), label=column)

    plt.axvline(x=1/24, linestyle='--', color='grey')
    plt.axvline(x=1/12, linestyle='--', color='grey')
    plt.legend()

    return fig
