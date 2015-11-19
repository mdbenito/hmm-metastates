#from https://github.com/statsmodels/statsmodels/blob/5931ec43c72373ed810c1305b87abf025f867306/statsmodels/graphics/utils.py
"""Helper functions for graphics with Matplotlib."""

__all__ = ['create_mpl_ax', 'create_mpl_fig']


def _import_mpl():
    """This function is not needed outside this utils module."""
    try:
        import matplotlib.pyplot as plt
    except:
        raise ImportError("Matplotlib is not found.")

    return plt


#XXX eventually be able to create multiple axes. Check call to
#XXX _subplot in pandas.tools.plotting.py
def create_mpl_ax(ax=None, ax_kw={}, **fig_kw):
    """Helper function for when a single plot axis is needed.

    Parameters
    ----------
    ax : Matplotlib AxesSubplot instance, optional
        If given, this subplot is used to plot in instead of a new figure being
        created.

    Returns
    -------
    fig : Matplotlib figure instance
        If `ax` is None, the created figure.  Otherwise the figure to which
        `ax` is connected.
    ax : Matplotlib AxesSubplot instance
        The created axis if `ax` is None, otherwise the axis that was passed
        in.

    Notes
    -----
    This function imports `matplotlib.pyplot`, which should only be done to
    create (a) figure(s) with ``plt.figure``.  All other functionality exposed
    by the pyplot module can and should be imported directly from its
    Matplotlib module.

    See Also
    --------
    create_mpl_fig

    Examples
    --------
    A plotting function has a keyword ``ax=None``.  Then calls:

    >>> from statsmodels.graphics import utils
    >>> fig, ax = utils.create_mpl_ax(ax)

    """
    if ax is None:
        plt = _import_mpl()
        fig = plt.figure(**fig_kw)
        ax = fig.add_subplot(111, **ax_kw)
    else:
        fig = ax.figure

    return fig, ax


def create_mpl_fig(fig=None, **fig_kw):
    """Helper function for when multiple plot axes are needed.

    Those axes should be created in the functions they are used in, with
    ``fig.add_subplot()``.

    Parameters
    ----------
    fig : Matplotlib figure instance, optional
        If given, this figure is simply returned.  Otherwise a new figure is
        created.

    Returns
    -------
    fig : Matplotlib figure instance
        If `fig` is None, the created figure.  Otherwise the input `fig` is
        returned.

    See Also
    --------
    create_mpl_ax

    """
    if fig is None:
        plt = _import_mpl()
        fig = plt.figure(**fig_kw)

    return fig


def new_lim(cur_lim, new_lim):
    cur_min, cur_max = cur_lim
    new_min, new_max = new_lim

    return  min(cur_min, new_min),  max(cur_max, new_max)


def new_lims(ax, xmin=None, xmax=None, ymin=None, ymax=None):
    """Expand plot boundaries if required by new drawing."""

    if xmin is not None or xmax is not None:
        xlim = new_lim(ax.get_xlim(), (xmin, xmax))
    else:
        xlim = ax.get_xlim()

    if ymin is not None or ymax is not None:
        ylim = new_lim(ax.get_ylim(), (ymin, ymax))
    else:
        ylim = ax.get_ylim()

    return dict(xlim=xlim,
                ylim=(1.1*ylim[0], 1.1*ylim[1]))


def clean_labels(ax, axis):
    """Return ax devoid of labels in `axis`

    ax : Matplotlib.axes instance
    axis : {'x','y'}
    """

    get_ticklabels = getattr(ax, 'get_{}ticklabels'.format(axis))
    get_axis = getattr(ax, '{}axis'.format(axis))

    for label in get_ticklabels():
        label.set_visible(False)
    try:
        # set_visible will not be effective if
        # minor axis has NullLocator and NullFormattor (default)
        import matplotlib.ticker as ticker
        get_axis.set_minor_locator(ticker.AutoLocator())
        get_axis.set_minor_formatter(ticker.FormatStrFormatter(''))
        for label in get_ticklabels(minor=True):
            label.set_visible(False)
    except Exception:   # pragma no cover
        pass

    get_axis.get_label().set_visible(False)

    return ax


def add_subplot_axes(ax, rect, **ax_kw):
    # SO 17458580/embedding-small-plots-inside-subplots-in-matplotlib
    fig = ax.get_figure()
    box = ax.get_position()
    width, height = box.width, box.height

    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_x, infig_y = transFigure.transform(inax_position)

    width *= rect[2]
    height *= rect[3]

    subax = fig.add_axes([infig_x, infig_y,width, height],
                         **ax_kw)

    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)

    return subax
