import argparse
import logging
import sys

import bluesteel.graphics

from pathlib import Path

# TODO: fix runtime warning associated with submodule import


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
    parser.add_argument('-d', '--data', required=True)
    parser.add_argument('-o', '--outfile', type=Path)
    parser.add_argument('--type_', default='line', help='chart type')
    parser.add_argument('--title', help='main chart title')
    parser.add_argument('--format', help='output file format')
    parser.add_argument('--size', help='output size in inches')
    parser.add_argument('--ymin', help='minimum y value to display')
    parser.add_argument('--xmin', help='minimum x value to display')
    parser.add_argument('--ymax', help='maximum y value to display')
    parser.add_argument('--xmax', help='maximum x value to display')
    parser.add_argument('--xlabel', help='X axis label')
    parser.add_argument('--ylabel', help='Y axis label')
    parser.add_argument('--source', help='Source attribution')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='store_const',
                           const=logging.DEBUG, default=logging.INFO)
    verbosity.add_argument('-q', '--quiet', dest='verbose',
                           action='store_const', const=logging.WARNING)
    return parser.parse_args(args)


def main(args=sys.argv[1:]):
    """Dispatches request to module. """
    args = parse_args(args)
    kwargs = vars(args)
    logging.basicConfig(level=kwargs.pop('verbose'))

    bluesteel.graphics.save_fig(**vars(args))


if __name__ == "__main__":
    main()

