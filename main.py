from __future__ import print_function
import sys
import time as t
import hmmlearn.hmm as hmm
import matplotlib.pyplot as pl
import numpy as np
import alv.vizcol as col
import options
from alv import hmm_viz as viz


def load_file(input_file, shift=1):
    """

    Parameters
    ----------
    input_file
    shift

    Returns
    -------

    """
    series = np.loadtxt(input_file, dtype=np.int8)
    series -= shift  # series[:77*1000] - 1
    return series


def infer(series, trials=1, n_states=2, output_file=None, verbose=False):
    """

    Parameters
    ----------
    series
    trials
    n_states
    output_file
    verbose

    Returns
    -------

    """
    trial_length = int(series.size / trials)
    assert(series.size % trials == 0, 'Length of time series is not a multiple of number of trials')
    lengths = trial_length * np.ones(trials)

    outputs = np.unique(series)
    m = hmm.MultinomialHMM(n_components=n_states, n_iter=100, tol=1e-3, verbose=True, algorithm='viterbi')
    m.n_features = outputs.size

    tick = t.time()
    m.fit(series[:, None], lengths)
    if verbose:
        print ('Time fitting: {}s'.format(t.time() - tick))
    tick = t.time()
    viterbi_path = m.predict(series[:, None], lengths=lengths)
    if verbose:
        print ('Time for viterbi: {}s'.format(t.time() - tick))
    if output_file:
        np.save(output_file, viterbi_path)
    return viterbi_path


# Alv's plotting
def plot(series, viterbi_path, sr=250):
    """

    Parameters
    ----------
    series
    viterbi_path
    sr: Sampling rate

    Returns
    -------

    """
    df = viz.states(viterbi_path, sr, offset=0)
    ax = viz.ribbon(df, sr, col.cyclic_col(col.cm1.colors), y0=0, y_width=0.1999, group_col='state')

    viz.ribbon(viz.states(series, sr, offset=0), sr, col.cyclic_col(col.cm3.colors), y0=0.2, y_width=0.1999,
               group_col='state', ax=ax)
    pl.show()


def main(argv):
    np.random.seed(42)
    opts = options.parse(argv)
    if opts.auto:
        opts.trials = 77  # TODO
        opts.max_states = 2   # TODO
        opts.jobs = 1  # TODO
    series = load_file(input_file=opts.input_file)
    vpath = infer(series, output_file=opts.output_file, states=opts.states, trials=opts.trials)
    plot(series, vpath)

if __name__ == '__main__':
    main(sys.argv[1:])
