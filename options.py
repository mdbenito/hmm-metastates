from __future__ import print_function
import sys
import getopt
import utils
import re
from bunch import Bunch


def parse(argv):
    opts = Bunch({'input_file': None, 'output_file': None, 'jobs': 1, 'trials': 1, 'states': [2], 'nfold': None,
                  'auto': True, 'verbose': False})
    usage_str = 'Usage: python metastates.py -i <input-file> -o <output-file>\n\nOther options:\n' + \
                '\t-h, --help\t\tThis help\n' + \
                '\t-i, --input-file\tSpecifies the input file\n' + \
                '\t-o, --output-file\tSpecifies the output file [default=input-file.out]\n' + \
                '\t-j, --jobs\t\tNumber of concurrent jobs to launch [default={}]\n'.format(opts.jobs) + \
                '\t-t, --trials\t\tSet number of trials for input file [default={}]\n'.format(opts.trials) + \
                '\t-s, --states\t\tNumber of states to test [default={}]\n'.format(opts.states) + \
                '\t-a, --auto\t\tParse input filename for number of trials and maximal K\n' + \
                '\t\t\t\t(Overrides -s, -t) [default={}]\n'.format(opts.auto) + \
                '\t-c, --crossval\t\tPerform n-fold cross validation [default n={}]'.format(opts.nfold) + \
                '\t-v, --verbose\t\tDisplay progress and time information'
    try:
        vals, args = getopt.getopt(argv, 'hi:o:j:t:s:ac:v',
                                   ['help', 'input-file=', 'output-file=', 'jobs=', 'trials=', 'states=', 'auto',
                                    'crossval=', 'verbose'])
    except getopt.GetoptError as error:
        print('ERROR: ' + error + '\n' + usage_str)
        sys.exit(2)
    for opt, arg in vals:
        if opt in ('-h', '--help'):
            print(usage_str)
            sys.exit()
        elif opt in ('-i', '--input-file'):
            opts.input_file = arg
        elif opt in ('-o', '--output-file'):
            opts.output_file = arg
        elif opt in ('-j', '--jobs'):
            opts.jobs = int(arg)
        elif opt in ('-t', '--trials'):
            opts.trials = int(arg)
        elif opt in ('-s', '--states'):
            opts.states = utils.parse_ranges(arg)
        elif opt in ('-a', '--auto'):
            opts.auto = True
        elif opt in ('-c', '--crossval'):
            opts.nfold = int(arg)
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
