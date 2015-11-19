from __future__ import print_function
import sys
import getopt
from bunch import Bunch


def parse(argv):
    opts = Bunch({'input_file': None, 'output_file': None, 'jobs': 1, 'trials': 1, 'max_states': 2, 'auto': False})
    usage_str = 'Usage: python metastates.py -i <input-file> -o <output-file>\n\nOther options:\n' + \
                '\t-h, --help\t\tThis help\n' + \
                '\t-i, --input-file\tSpecifies the input file\n' + \
                '\t-o, --output-file\tSpecifies the output file [default=input-file.out]\n' + \
                '\t-j, --jobs\tNumber of concurrent jobs to launch [default={}]\n'.format(opts.jobs) + \
                '\t-t, --trials\t\tSet number of trials for input file [default={}]\n'.format(opts.trials) + \
                '\t-s, --max-states\tMaximal number of states to test [default={}]\n'.format(opts.states) + \
                '\t-a, --auto\t\tParse input filename for number of trials and maximal K\n' + \
                '\t\t\t\t(Overrides -s, -t)'
    try:
        opts, args = getopt.getopt(argv, 'hi:o:j:t:s:a:',
                                   ['help', 'input-file=', 'output-file=', 'jobs=', 'trials=', 'max-states=', 'auto='])
    except getopt.GetoptError:
        print(usage_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage_str)
            sys.exit()
        elif opt in ('-i', '--input-file'):
            opts.input_file = arg
        elif opt in ('-o', '--output-file'):
            opts.output_file = arg
        elif opt in ('-j', '--jobs'):
            opts.jobs = arg
        elif opt in ('-t', '--trials'):
            opts.trials = arg
        elif opt in ('-s', '--max-states'):
            opts.max_states = arg
        elif opt in ('-a', '--auto'):
            opts.auto = True
    if not opts.input_file:
        print(usage_str)
        sys.exit(1)
    opts.output_file = opts.output_file or opts.input_file + '.out'
    return opts
