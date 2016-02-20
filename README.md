# metastates

Models a sequence of states coming from an autoregressive Hidden Markov model
again as an HMM. Multiple runs can be run in parallel to compute using different
numbers of hidden states of the HMM (_meta-states_).

Assuming independence of the different experimental trials fed to the algorithm,
it is also possible to use cross-validation to determine the optimal (in the sense
of maximal likelihood of the sequence of states) choice for the number of hidden
states. See [3] for a discussionof two alternative methods in the case that one only
has a single run for training, in which case removing samples for cross-validation
would break the Markov property.

## Dependencies

* Python 2.7, numpy, matplotlib.
* [hmmlearn](https://github.com/hmmlearn): unsupervised learning and
  inference of Hidden Markov Models.
  Install in [conda](http://conda.pydata.org/) with
    `conda install -c https://conda.anaconda.org/bcbio hmmlearn`
  This should also install numpy, scipy, scikit-learn and other
  dependencies.
* [concurrent.futures](https://pypi.python.org/pypi/futures): Backport
  from Python 3.2. Install in [conda](http://conda.pydata.org/) with
    `conda install futures`

## Usage

```
Usage: python metastates.py -i <input-file> -o <output-file>

Other options:
    -h, --help           This help
    -i, --input-file     Specifies the input file
    -o, --output-file    Specifies the output file
                         [default=input-file.out]
    -f, --shift          Apply shift to data in input file [default=-1]
    -t, --trials         Set number of trials for input file [default=1]
    -s, --states         Number of states to use [default=[2]]
                         (interpreted as a maximum when cross-validating)
    -a, --auto           Parse input filename for number of trials and
                         number of states (overrides -s, -t) [default=False]
    -c, --crossval       Perform n-fold cross-validation [default n=None]
    -j, --jobs           Number of concurrent jobs to launch [default=1]
    -v, --verbose        Display progress and time information
```

## References:

[1] L. R. Rabiner, “A tutorial on hidden Markov models and selected applications in speech recognition,” in Proceedings of the IEEE, 1989, vol. 77, pp. 257–286.

[1] M. J. Cassidy and P. Brown, “Hidden Markov based autoregressive analysis of stationary and non-stationary electrophysiological signals for functional coupling studies,” Journal of Neuroscience Methods, vol. 116, no. 1, pp. 35–53, Apr. 2002.

[3] G. Celeux and J.-B. Durand, “Selecting hidden Markov model state number with cross-validated likelihood,” Comput Stat, vol. 23, no. 4, pp. 541–564, Dec. 2007.


## License

This software falls under the GNU general public license version 3 or later.
It comes without **any warranty whatsoever**.
For details see http://www.gnu.org/licenses/gpl-3.0.html.