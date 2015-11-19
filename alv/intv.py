# -*- coding: utf-8 -*-
"""intv.py: Operations involving intervals in the real line."""

__author__     = "Álvaro Tejero-Cantero"
__copyright__  = "Public domain"
__email__      = "alvaro at minin dot es"


from itertools import izip, chain
import numpy as np


def intervals(bds, lower=[], upper=[]):
    """
    Return a list of intervals from a list of boundaries.

    Each boundary is taken both as the end of an interval and as the
    beginning of the next (with the possible exception of first and
    last, see below).

    Examples
    --------
    >>> list(intervals([1, 4, 29]))
    [(1, 4), (4, 29)]
    >>> list(intervals([1, 4, 29], lower=[0]))
    [(0, 1), (1, 4), (4, 29)]
    >>> list(intervals([1, 4, 29], upper=[55]))
    [(1, 4), (4, 29), (29, 55)]
    >>> list(intervals([1, 4, 29], [0], [55]))
    [(0, 1), (1, 4), (4, 29), (29, 55)]
    """
    L = len(lower)
    if L not in [0, 1]:
        raise Exception('Prepend at most one boundary')

    return izip(chain(lower, bds),
                chain(bds[1 - L:], upper))


def rle(x):
    """
    Return x run-length encoded: iterator over (start, stop, value).

    From
    http://mail.scipy.org/pipermail/numpy-discussion/2007-October/029378.html
    >>> list(rle([1,1,1,1,1,0,0,2,2,9,9,9,9,9,9,9,9,9,9]))
    [(0, 5, 1), (5, 7, 0), (7, 9, 2), (9, 19, 9)]"""

    jumps, = np.nonzero(np.diff(np.asarray(x)))
    # add boundaries 0 and last
    jumps = np.concatenate(([0], jumps + 1, [len(x)]))

    return ((a, b, x[a]) for (a, b) in izip(jumps[:-1], jumps[1:]))


def unrle(r, dtype=None):
    """Return normal (unwound) version of rle-encoded r.  This is the
    array version, requiring simultaneous memory allocation of the
    output and assuming that values are of homogeneous type.

    >>> unrle([(0, 5, 1), (5, 7, 0), (7, 9, 2), (9, 19, 9)])
    array([1, 1, 1, 1, 1, 0, 0, 2, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9])
    """

    tuples = list(r)
    _, totlen, el = tuples[-1]

    if not dtype:
        # if not dtype passed, this will be generous
        # (any integer will result in int64, any float in float64, etc)
        dtype = np.dtype(type(el))

    arr = np.empty(totlen, dtype=dtype)

    for (a, b, el) in tuples:
        arr[a:b] = el

    return arr


def iunrle(r):
    """Return normal (unwound) version of rle-encoded r.  This is the
    iterator version, austere in memory.

    >>> list(iunrle([(0, 5, 1), (5, 7, 0), (7, 9, 2), (9, 19, 9)]))
    [1, 1, 1, 1, 1, 0, 0, 2, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    """

    if type(r) == type(list()):
        r = (x for x in r)

    while 1:
        a, b, el = r.next()
        for i in xrange(b - a):
            yield el



#XXX applicable to seqs, or does it depend on np.arrays?
def indexof_iv(events, starts, stops=None):
    """Return for each event the index of the enclosing interval.

    Parameters
    ----------
    events : array of numbers
        event timestamps

    starts : array of numbers
        starts, sorted ascending

    stops : array of numbers such that stops > starts, or None
        matching stops for each start; sorted ascending; if None the
        starts[1:] are implicitly assumed to be the stops.

    Returns
    -------
    array of floats of length events containing the integer indexes such
    that starts[indexes]<events<stops[indexes] (proper inclusion).  If
    an event is found not to lie in any interval, np.nan.
    """

    #XXX ADD TESTS
    if stops is None:
        # intervals are a covering, i.e. there are no holes. For
        # instance, if starts = [1, 2, 3] intervals are [(-inf,1),
        # (1,2), (2,3), (3, inf)], infs courtesy of default behaviour of
        # searchsorted (see its doc).
        return np.searchsorted(starts, e)
    else:
        # index where to insert the starts and the stops in the events
        alpha = np.searchsorted(starts, events, side='right')
        beta = np.searchsorted(stops, events, side='right')

    # this turned to be the condition of inclusion after some thought
    idx = np.where(alpha-beta==1, alpha-1, np.nan)

    return idx
