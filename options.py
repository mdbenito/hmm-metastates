from __future__ import print_function
import sys
import getopt
import utils
import re
from bunch import Bunch


def parse(argv):
    opts = Bunch({'input_file': None, 'output_file': None, 'shift': -1, 'jobs': 1, 'trials': 1,
                  'states': [2], 'nfold': None, 'auto': False, 'verbose': False})
    usage_str = str(
        "Usage: python metastates.py -i <input-file> -o <output-file>\n\nOther options:\n"
        "    -h, --help           This help\n"
        "    -i, --input-file     Specifies the input file\n"
        "    -o, --output-file    Specifies the output file\n"
        "                         [default=input-file.out]\n"
        "    -f, --shift          Apply shift to data in input file [default={0}]\n"
        "    -t, --trials         Set number of trials for input file [default={2}]\n"
        "    -s, --states         Number of states to use [default={3}]\n"
        "                         (interpreted as a maximum when cross-validating)\n"
        "    -a, --auto           Parse input filename for number of trials and\n"
        "                         number of states (overrides -s, -t) [default={4}]\n"
        "    -c, --crossval       Perform n-fold cross-validation [default n={5}]\n"
        "    -j, --jobs           Number of concurrent jobs to launch [default={1}]\n"
        "    -v, --verbose        Display progress and time information")\
        .format(opts.shift, opts.jobs, opts.trials, opts.states, opts.auto, opts.nfold)
    try:
        vals, args = getopt.getopt(argv, 'hi:o:f:t:s:ac:j:v',
                                   ['help', 'input-file=', 'output-file=', 'shift=',
                                    'trials=', 'states=', 'auto',
                                    'crossval=', 'jobs=', 'verbose'])
    except getopt.GetoptError as error:
        print('ERROR: ' + error.msg + '\n' + usage_str)
        sys.exit(2)
    for opt, arg in vals:
        if opt in ('-h', '--help'):
            print(usage_str)
            sys.exit()
        elif opt in ('-i', '--input-file'):
            opts.input_file = arg
        elif opt in ('-o', '--output-file'):
            opts.output_file = arg
        elif opt in ('-f', '--shift'):
            opts.shift = int(arg)
        elif opt in ('-t', '--trials'):
            opts.trials = int(arg)
        elif opt in ('-s', '--states'):
            opts.states = utils.parse_ranges(arg)
        elif opt in ('-a', '--auto'):
            opts.auto = True
        elif opt in ('-c', '--crossval'):
            opts.nfold = int(arg)
        elif opt in ('-j', '--jobs'):
            opts.jobs = int(arg)
        elif opt in ('-v', '--verbose'):
            opts.verbose = True

    if not opts.input_file:
        print('ERROR: input file required\n' + usage_str)
        sys.exit(1)

    opts.output_file = opts.output_file or opts.input_file + '.out'

    if opts.auto:
        p = re.compile(r'.*--\w(\d+).*--K(\d+)p(\d+)c(\d+).*', flags=re.IGNORECASE)
        m = p.match(opts.input_file)
        if not m:
            print('ERROR: filename does not match pattern for --auto. Expected:' +
                  r'.*--\w(\d+).*--K(\d+)p(\d+)c(\d+).*')
            sys.exit(2)
        opts.trials = int(m.group(1))
        opts.states = range(2, int(m.group(2)) + 1)
        opts.jobs = utils.available_cpu_count()
        # opts.padding = int(m.group(3))  # Unused
    return opts
