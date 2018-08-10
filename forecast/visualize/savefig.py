def savefig(plot_func):
    """ Decorator to save figure to .png """

    def wrapper(*args, **kwargs):

        fig = plot_func(*args, **kwargs)

        try:
            fig_name = kwargs.pop('fig_name')

            if fig_name:
                fig.savefig(fig_name)

        except KeyError:
            pass

            return fig

    return wrapper
