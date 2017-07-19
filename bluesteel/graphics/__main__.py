import argparse
import logging
import sys

import pandas as pd

import bluesteel.graphics

from pathlib import Path

log = logging.getLogger(__name__)


def save_fig(outfile, format='png', **kwargs):
    """Outputs figure to specified location. """
    fig = bluesteel.graphics.gen_chart(**kwargs)
    log.debug(f'attempting to save to {outfile}')
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(outfile), format=format)
    return str(outfile)


def parse_args(args):
    """Parse command line arguments

    Arguments:
    -o {Path} -- base location for output files
    -v | -q -- verbosity flags

    Returns:
    Arguments[attributes] -- returns object with arguments as attributes.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('data', type=lambda x: pd.read_csv(x, index_col=0))
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
    save_fig(**kwargs)


if __name__ == "__main__":
    main()

