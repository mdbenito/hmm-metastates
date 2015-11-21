from __future__ import print_function
import sys
import time as t
import hmmlearn.hmm as hmm
import matplotlib.pyplot as pl
import numpy as np
import alv.vizcol as col
import options
from alv import hmm_viz as viz
from concurrent.futures import ProcessPoolExecutor


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


def infer(series, n_states=2, trials=1, verbose=False):
    """

    Parameters
    ----------
    series
    trials
    n_states
    verbose

    Returns
    -------

    """
    trial_length = int(series.size / trials)
    assert series.size % trials == 0, 'Length of time series is not a multiple of number of trials'
    lengths = trial_length * np.ones(trials)

    outputs = np.unique(series)
    if verbose:
        print('Inferring parameters of MultinomialHMM for n_states={0}, max. iterations={1}, tolerance={2}'.
              format(n_states, 100, 1e-3))
    m = hmm.MultinomialHMM(n_components=n_states, n_iter=100, tol=1e-3, verbose=verbose, algorithm='viterbi')
    m.n_features = outputs.size

    tick = t.time()
    m.fit(series[:, None], lengths)
    if verbose:
        print('Time fitting: {}s'.format(t.time() - tick))
    tick = t.time()
    viterbi_path = m.predict(series[:, None], lengths=lengths)
    if verbose:
        print('Time for viterbi: {}s'.format(t.time() - tick))

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
    if opts.verbose: print('Loading file {}'.format(opts.input_file))
    series = load_file(opts.input_file)
    if opts.verbose: print('Inferring with n_states={0}, trials={1}, jobs={2}'.
                           format(opts.states, opts.trials, opts.jobs))
    with ProcessPoolExecutor(max_workers=opts.jobs) as ex:
        # WARNING: callables run by the Executor must be pickl-able
        # See: http://stackoverflow.com/questions/30378971/python-2-7-concurrent-futures-threadpoolexecutor-does-not-parallelize
        n = len(opts.states)
        for vpath in ex.map(infer, [series] * n, opts.states, [opts.trials] * n, [opts.verbose] * n):
            if opts.output_file:
                save_file(vpath, opts.output_file)
            plot(series, vpath)


if __name__ == '__main__':
    main(sys.argv[1:])
