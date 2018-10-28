from forecast.utils import ensure_dir

def savefig(plot_func):
    """ Decorator to save figure to .png """

    def wrapper(*args, **kwargs):
        try:
            fig_name = kwargs.pop('fig_name')
        except KeyError:
            pass

        fig = plot_func(*args, **kwargs)

        if fig_name:
            ensure_dir(fig_name)
            fig.savefig(fig_name)
        return fig

    return wrapper
