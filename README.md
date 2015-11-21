# metastates

Runs a Hidden Markov Model on a sequence of states coming from HMMAR.
Multiple runs can be run in parallel to compute using different numbers of meta-states.

Cross-validation can be performed on the results...

## Dependencies

* Python 2.7
* [hmmlearn](https://github.com/hmmlearn): unsupervised learning and inference of Hidden Markov Models.
  Install in [conda](http://conda.pydata.org/) with
    `conda install -c https://conda.anaconda.org/bcbio hmmlearn`
* [concurrent.futures](https://pypi.python.org/pypi/futures): Backport from Python 3.2

## Usage

`python metastates.py ...`


## License

duh...

