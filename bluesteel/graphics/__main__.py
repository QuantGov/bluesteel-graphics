import argparse
import logging
import sys

import pandas as pd

import bluesteel

from pathlib import Path


def parse_args(args):
    """Parse command line arguments

    Arguments:
    -o {Path} -- base location for output files
    -v | -q -- verbosity flags

    Returns:
    Arguments[attributes] -- returns object with arguments as attributes.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument('settings', nargs='+')
    parser.add_argument('-d', '--data', type=Path)
    parser.add_argument('-o', '--outfile', type=Path)
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='store_const',
                           const=logging.DEBUG, default=logging.INFO)
    verbosity.add_argument('-q', '--quiet', dest='verbose',
                           action='store_const', const=logging.WARNING)
    return parser.parse_args(args)


def main(args=sys.argv[1:]):
    args = parse_args(args)
    logging.basicConfig(level=args.verbose)

    if args.data.suffix == '.csv':
        indata = pd.read_csv(str(args.data))
    elif args.data.suffix in ['.xlsx', '.xls']:
        indata = pd.read_excel((args.data))
    else:
        raise ValueError

    if args.outfile.exists():
        response = input(f'Are you sure you want to overwrite {args.outfile}?')
        if response == 'y':
            pass
        else:
            raise ValueError

    bluesteel.graphics.save_fig(args.outfile, data=indata)


if __name__ == "__main__":
    main()

