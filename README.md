# metastates

Runs a Hidden Markov Model on a sequence of states coming from HMMAR.
Multiple runs can be run in parallel to compute using different numbers 
of meta-states.

Cross-validation can be performed on the results...

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
	-h, --help          This help
	-i, --input-file    Specifies the input file
	-o, --output-file   Specifies the output file [default=input-file.out]
	-j, --jobs          Number of concurrent jobs to launch [default=1]
	-t, --trials        Set number of trials for input file [default=1]
	-s, --states        Number of states to test [default=[2]]
	-a, --auto          Parse input filename for number of trials and maximal K
                        (Overrides -s, -t)
	-v, --verbose       Display progress and time information
```


## License

duh...

