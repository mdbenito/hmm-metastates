from __future__ import division

import matplotlib as mpl
import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

from mplutils import create_mpl_ax, new_lims
from vizcol import cm_std
#from gen.seq import ezip

from alv.intv import rle



def states(labels, sr, offset):
    """Return interval DataFrame with run-length encoded intervals
    |i|a (int samples) |b (int samples) |state (int, 1 based) |dt (float, ms)|.

    Parameters
    ----------
    labels (ints) - state labels for each timestamp (Viterbi path).
    sr (float) - sampling rate in Hz.
    offset (int) - states can start only after 'order' samples
    """


    df = pd.DataFrame(rle(np.asarray(labels, dtype='i2')),
                        columns=['a', 'b', 'state'])
    df['a'] += offset
    df['b'] += offset

    df['ds'] = df.b-df.a # in samples
    df['dtms'] = (1000./sr)*(df.b - df.a) # duration of interval *in ms*

    return df


def stack(x, Y, y0=0, dy=0, labels=None, colors=cm_std.colors,
                 hlines=True, ax=None, **parts_kw):
    """Stack traces Y (NxT) around y0 with vertical spacing dy.

    x - 1 x T array
    Y - N x T array
    cols - f: int (0-based) -> color (e.g a colormap)
    labels [str]_Nx1 - line labels
    hlines bool - add horizontal line per trace to help the eye
    """
    fig, ax = create_mpl_ax(ax)

    if labels is None:
        labels = np.arange(Y.shape[0])

    for n, (y, col, label) in ezip(Y, colors, labels):

        line_props = dict(color=col, label=label)
        line_props.update(**parts_kw)

        # XXX if dy is array, use directly for the offsets
        offset = dy*(n-Y.shape[0]/2) + y0 #centered on y0
        ax.plot(x, y+offset, **line_props)
        if hlines: # help the eye find the zero level for each trace
            line_props.update(lw=0.2)
            line_props.pop('label')
            ax.hlines(offset, x[0], x[-1],
                      zorder=0, **line_props)

    # expand y boundaries if needed
    pl.setp(ax, **new_lims(ax, x[0], x[-1], y0-dy*Y.shape[0]/2, offset))

    return ax


# see other attempts at efficient interval representation with collections
# in a notebook in this package


# helper function for ribbon
def get_verts_ribbon(df, y0=0, y_width=1, a='a', b='b'):
    """Return vertices collection in shape (npoly, nvert, 2).
    """

    df['bottom'], df['top'] = y0-y_width/2, y0 + y_width/2

    return df[['a','bottom',
               'b','bottom',
               'b','top',
               'a','top']].values.reshape((-1,4,2))


def ribbon(df, sr, colmap, y0, y_width,
            group_col, a='a', b='b',
            ax=None, legend_loc=0, **ribbon_kw):
    """Show ribbons with a distinct colour for intervals
    of different type in a data frame.

    df (pd.DataFrame) : data frame
    sr (int) : sampling rate
    (a, b are in sample numbers and must be converted).
    colmap (function group_col value -> color) : color map,
      groups will be assigned colors in the order they appear in groupby.
    y0 (float) : ordinate of ribbon
    y_width (float or list) : height(s) of ribbon (one height per group)
    group_col (str) : column name used for grouping
    a, b : column names of start/stop of interval
    ax (Axis) : axis to paint on
    ribbon_kw (dict) : passed to PolyCollection (e.g. use to set alpha)
    """
    from matplotlib.lines import Line2D
    fig, ax = create_mpl_ax(ax)

    dfc = df.copy() # because we will modify it
    dfc[a]/=sr
    dfc[b]/=sr

    # not sure we want these defaults
    ribbon_kw = dict(zorder=0, linewidths=0)
    ribbon_kw.update(**ribbon_kw)

    poly_coll = mpl.collections.PolyCollection

    #http://matplotlib.org/users/legend_guide.html#using-proxy-artist
    proxy_artists, labels = [], []

    for gid, group in dfc.groupby(group_col):

        try:
            yw = y_width[gid]
        except:
            yw = y_width

        pc = poly_coll(get_verts_ribbon(group, y0, yw, a, b),
                                facecolors=colmap(gid), **ribbon_kw)

        # using a proxy artist to get collections labeled
        circ = Line2D([0],[0], linestyle="none",
                      marker='o', alpha=ribbon_kw.get('alpha',1),
                      markersize=10, markerfacecolor=colmap(gid))

        proxy_artists.append(circ)
        labels.append(gid)

        ax.add_collection(pc)

    if legend_loc:
        ncol = len(labels) //4 + 1
        artist = ax.legend(proxy_artists, labels, ncol=3, loc=legend_loc)
        pl.gca().add_artist(artist)

    try:
        max_yw = max(y_width.values())
    except AttributeError:
        max_yw = y_width

    pl.setp(ax, **new_lims(ax, df[a].min()/sr, df[b].max()/sr,
                           y0-max_yw/2, y0+max_yw/2))
    return ax
