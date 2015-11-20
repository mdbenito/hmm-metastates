from __future__ import print_function
import sys
import re
import time as t
import hmmlearn.hmm as hmm
import matplotlib.pyplot as pl
import numpy as np
import alv.vizcol as col
import options
import utils
from alv import hmm_viz as viz


def load_file(input_file, shift=-1):
    """

    Parameters
    ----------
    input_file
    shift

    Returns
    -------

    """
    series = np.loadtxt(input_file, dtype=np.int8)
    series += shift  # series[:77*1000] - 1
    return series


def save_file(viterbi_path, output_file, shift=1):
    """

    Parameters
    ----------
    output_file
    shift

    Returns
    -------

    """

    np.save(output_file, viterbi_path + shift)
    return


def infer(series, trials=1, n_states=2, verbose=False):
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
    assert series.size % trials == 0, 'Length of time series is not a multiple of number of trials'
    lengths = trial_length * np.ones(trials)

    outputs = np.unique(series)
    m = hmm.MultinomialHMM(n_components=n_states, n_iter=100, tol=1e-3, verbose=verbose, algorithm='viterbi')
    m.n_features = outputs.size

    tick = t.time()
    m.fit(series[:, None], lengths)
    if verbose:
        print ('Time fitting: {}s'.format(t.time() - tick))
    tick = t.time()
    viterbi_path = m.predict(series[:, None], lengths=lengths)
    if verbose:
        print ('Time for viterbi: {}s'.format(t.time() - tick))

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
        p = re.compile(r'.*--\w(\d+).*--K(\d+)p(\d+)c(\d+).*', flags=re.IGNORECASE)
        m = p.match(opts.input_file)
        if not m:
            print('ERROR: filename does not match pattern for --auto. Expected:' +
                  r'.*--\w(\d+).*--K(\d+)p(\d+)c(\d+).*')
            sys.exit(2)
        opts.trials = int(m.group(1))
        opts.states = int(m.group(2))  # TODO: create list of integers
        # opts.padding = int(m.group(3))  # Unused
        opts.jobs = utils.number_of_cores()  # TODO
    series = load_file(opts.input_file)
    vpath = infer(series, n_states=opts.states, trials=opts.trials, verbose=opts.verbose)
    if opts.output_file:
        save_file(vpath, opts.output_file)
    plot(series, vpath)


if __name__ == '__main__':
    main(sys.argv[1:])
