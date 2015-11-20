from __future__ import print_function
import sys
import getopt
from bunch import Bunch


def parse(argv):
    opts = Bunch({'input_file': None, 'output_file': None, 'jobs': 1, 'trials': 1, 'states': [2], 'auto': False,
                  'verbose': False})
    usage_str = 'Usage: python metastates.py -i <input-file> -o <output-file>\n\nOther options:\n' + \
                '\t-h, --help\t\tThis help\n' + \
                '\t-i, --input-file\tSpecifies the input file\n' + \
                '\t-o, --output-file\tSpecifies the output file [default=input-file.out]\n' + \
                '\t-j, --jobs\t\tNumber of concurrent jobs to launch [default={}]\n'.format(vals.jobs) + \
                '\t-t, --trials\t\tSet number of trials for input file [default={}]\n'.format(vals.trials) + \
                '\t-s, --states\t\tNumber of states to test [default={}]\n'.format(vals.states) + \
                '\t-a, --auto\t\tParse input filename for number of trials and maximal K\n' + \
                '\t\t\t\t(Overrides -s, -t)' + \
                '\t-v, --verbose\tDisplay progress indicators'
    try:
        vals, args = getopt.getopt(argv, 'hi:o:j:t:s:a:v',
                                   ['help', 'input-file=', 'output-file=', 'jobs=', 'trials=', 'states=', 'auto=',
                                    'verbose'])
    except getopt.GetoptError:
        print(usage_str)
        sys.exit(2)
    for opt, arg in vals:
        if opt in ('-h', '--help'):
            print(usage_str)
            sys.exit()
        elif opt in ('-i', '--input-file'):
            vals.input_file = arg
        elif opt in ('-o', '--output-file'):
            vals.output_file = arg
        elif opt in ('-j', '--jobs'):
            vals.jobs = int(arg)
        elif opt in ('-t', '--trials'):
            vals.trials = int(arg)
        elif opt in ('-s', '--states'):
            vals.states = [int(arg)]  # TODO: parse list of integers
        elif opt in ('-a', '--auto'):
            vals.auto = True
        elif opt in ('-v', '--verbose'):
            vals.verbose = True
    if not opts.input_file:
        print(usage_str)
        sys.exit(1)
    opts.output_file = opts.output_file or opts.input_file + '.out'
    return opts
