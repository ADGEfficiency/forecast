import matplotlib.pyplot as plt

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from .savefig import savefig


plt.style.use('ggplot')


@savefig
def plot_autocorrelation(data, column, lags=48):
    print("""
    Autocorrelation is the correlation of a variable with a lagged version of itself.
    Spikes in autocorrelation suggest seasonality.  For example, a spike in ACF at lag 24 hours
    would suggest daily seasonality
    Partial autocorrelation measures the degree of association between the variable and a lagged version of itself,
    controlling for the values of the time series at all shorter lags.
    The use of this function was introduced as part of the Box–Jenkins approach to time series modelling,
    whereby plotting the partial autocorrelative functions one could determine the appropriate lags p in an AR (p) model
    or in an extended ARIMA (p,d,q) model.
    """)

    fig, axes = plt.subplots(nrows=2, figsize=(25, 10))

    _ = plot_acf(data.loc[:, column], lags=lags, ax=axes[0])

    _ = plot_pacf(data.loc[:, column], lags=lags, ax=axes[1])

    return fig
