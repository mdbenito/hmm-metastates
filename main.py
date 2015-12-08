# coding=utf-8
from __future__ import print_function
import sys
import time as t
import hmmlearn.hmm as hmm
import matplotlib.pyplot as pl
import numpy as np
import alv.vizcol as col
import options
from alv import hmm_viz as viz
from concurrent.futures import ProcessPoolExecutor, as_completed


def load_observations(input_file, shift=-1):
    """
    Loads a text file of integers (emissions of the HMM) into a numpy array.

    Parameters
    ----------
    input_file: duh!
    shift: If the integers in the file start at 1, use a shift of -1 (to conform to zero-indexed arrays)

    """
    series = np.loadtxt(input_file, dtype=np.int8)
    series += shift
    return series


def save_viterbi(viterbi_path, output_file, shift=1):
    """

    Parameters
    ----------
    viterbi_path:
    output_file
    shift

    Returns
    -------

    """

    np.save(output_file, viterbi_path + shift)
    return


def compute_lengths(series, num_trials):
    """
    Computes the array of lengths of trials (size(series)/num_trials) for usage with hmmlearn.
    Currently(?) trivial, since all trials are of the same length.
    """
    trial_length = int(series.size / num_trials)
    assert series.size % num_trials == 0, 'Length of time series is not a multiple of number of trials'
    return trial_length * np.ones(num_trials)


def infer(series, lengths, n_states=2, viterbi=True, verbose=False, start=0, end=0, n_iter=10, tol=5e-1):
    """

    Parameters
    ----------
    series: exepects a column vector (i.e. N x 1)
    lengths: lengths of individual runs (subsets of the series)
    n_states
    viterbi: whether to compute the viterbi path
    verbose
    start: HACK used to compute scores after the futures are done.
    end: HACK
    n_iter
    tol

    Returns
    -------

    """
    outputs = np.unique(series)
    if verbose: print('Inferring parameters of MultinomialHMM for n_states={0}, max. iterations={1}, tolerance={2}'.
                      format(n_states, n_iter, tol))
    m = hmm.MultinomialHMM(n_components=n_states, n_iter=n_iter, tol=tol, verbose=verbose, algorithm='viterbi')
    m.n_features = outputs.size

    tick = t.time()
    m.fit(series, lengths)
    if verbose: print('Time fitting: {}s'.format(t.time() - tick))
    tick = t.time()
    viterbi_path = []
    if viterbi:
        viterbi_path = m.predict(series[:, None], lengths=lengths)
        if verbose: print('Time for viterbi: {}s'.format(t.time() - tick))

    return [[m, start, end], viterbi_path] # HACK HACK


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


def cross_validate(series, opts):
    """
    Reshapes the series as a num_trials x trial_length matrix, then splits its rows in N=opts.nfold subsets.
    For each k ∈ (1, max_states):
      Trains with one subset of trials then tests against the N-1 remaining (computes the log likelihood / score).
    Scores are averaged over all N training/test stages
    """
    if opts.verbose: print('Performing cross-validation with {} folds'.format(opts.nfold))
    scores = {k: 0 for k in opts.states}
    trial_length = compute_lengths(series, opts.trials)[1]  # HACK
    # trial_length = int(series.size / opts.trials)
    # assert series.size % opts.trials == 0, 'Length of time series is not a multiple of number of trials'
    view = series.reshape((opts.trials, trial_length))  # FIXME: Truly a view?
    l = int(np.floor(opts.trials / opts.nfold))
    futures = []
    with ProcessPoolExecutor(max_workers=opts.jobs) as ex:
        for k in opts.states:
            off = 0
            #if opts.verbose: print('Computing scores for k= {} states'.format(k))
            while off < opts.trials:
                start = off
                end = min(off+l, opts.trials)
                off = end
                training_trials = start + opts.trials-end
                training = view[range(0, start)+range(end, opts.trials)].reshape(((start+opts.trials-end)*trial_length, 1))
                training_lengths = compute_lengths(training, training_trials)
                #if opts.verbose: print('\tFitting for fold #{}'.format(int(np.ceil(off/l))))
                futures.append(ex.submit(infer, training, training_lengths,
                                         n_states=k, viterbi=False, verbose=opts.verbose, start=start, end=end))
                # m, _ = infer(training, training_lengths, n_states=k, viterbi=False, verbose=opts.verbose)

    for fut in as_completed(futures):
        [m, start, end], _ = fut.result()
        k = m.n_components
        testing = view[start:end].reshape(((end-start)*trial_length, 1))
        scores[k] += m.score(testing)
        if opts.verbose: print('\tScore for fold {} - {}: {}'.format(start, end, scores[k]))
    for k in scores.keys():
        scores[k] /= np.ceil(opts.trials/l)  # Average score over the number of splits
    return scores


# WARNING: callables run by the Executor must be pickl-able
# See: http://stackoverflow.com/questions/30378971/python-2-7-concurrent-futures-threadpoolexecutor-does-not-parallelize
def main(argv):
    np.random.seed(42)
    opts = options.parse(argv)
    if opts.verbose: print('Loading file {}'.format(opts.input_file))
    series = load_observations(opts.input_file)
    if opts.verbose: print('Working with n_states={0}, trials={1}, jobs={2}'.format(opts.states, opts.trials, opts.jobs))

    if opts.nfold:
        scores = cross_validate(series, opts)
        print("Final scores= {}".format(scores))
    else:
        with ProcessPoolExecutor(max_workers=opts.jobs) as ex:
            n = len(opts.states)
            for _, vpath in ex.map(infer,[series[:, None]] * n, opts.states, [opts.trials] * n, [True] * n,
                                   [opts.verbose] * n):
                if opts.output_file:
                    save_viterbi(vpath, opts.output_file)
                plot(series, vpath)


if __name__ == '__main__':
    main(sys.argv[1:])
