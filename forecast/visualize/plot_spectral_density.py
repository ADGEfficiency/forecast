import matplotlib.pyplot as plt

import numpy as np
from scipy.signal import welch

from .savefig import savefig


plt.style.use('ggplot')


def plot_spectral_density(data, column):
    print("""
          The power spectral density - Fourier transform of the autocorrelation

		  TODO - fs = 1 Hz -> half hourly only!
          """)

    fig, axes = plt.subplots(figsize=(25,10))

    freqs, psd = welch(
        data.loc[:, column].values,
        fs=1,  # Hz
        window='hanning',
        nperseg=512,
        scaling='density'
    )

    plt.plot(freqs, np.sqrt(psd), label=column)

    plt.axvline(x=0.5/12, linestyle='--', color='green', label='12')
    plt.axvline(x=0.5/24, linestyle='--', color='red', label='24')
    plt.axvline(x=0.5/48, linestyle='--', color='blue', label='48')
    plt.legend()

    return fig
