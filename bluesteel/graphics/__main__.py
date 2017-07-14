import argparse
import logging
import sys

import bluesteel.graphics

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
    parser.add_argument('-d', '--data')
    parser.add_argument('-o', '--outfile', type=Path)
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='store_const',
                           const=logging.DEBUG, default=logging.INFO)
    verbosity.add_argument('-q', '--quiet', dest='verbose',
                           action='store_const', const=logging.WARNING)
    return parser.parse_args(args)


def main(args=sys.argv[1:]):
    """Dispatches request to module. """
    args = parse_args(args)
    logging.basicConfig(level=args.verbose)

    bluesteel.graphics.save_fig(args.outfile, data=args.data,
                                format=Path(args.outfile).suffix[1:])


if __name__ == "__main__":
    main()

