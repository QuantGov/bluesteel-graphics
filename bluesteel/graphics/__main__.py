import argparse
import logging
import sys

import pandas as pd

import bluesteel.graphics

from pathlib import Path

log = logging.getLogger(__name__)


def save_fig(outfile, **kwargs):
    """
    Outputs figure to specified location.

    If format is None, infer format from outfile.
    """
    log.debug(f'attempting to save to {outfile}')
    outfile = Path(outfile)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    data = kwargs.pop('data')
    if data.index.dtype == 'O':
        try:
            data.index = pd.to_datetime(data.index)
        except ValueError:
            pass
    format = outfile.suffix.strip('.')
    outfile.write_bytes(
        bluesteel.graphics.create_image(
            data, format, **kwargs).read())
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
    # parser.add_argument('data', type=lambda x: pd.read_csv(x, index_col=0))
    parser.add_argument('data', type=lambda x: pd.read_csv(x, index_col=0))
    parser.add_argument('-o', '--outfile', type=Path)
    
    parser.add_argument('--kind', default='line', help='chart type')
    parser.add_argument('--title', help='main chart title')
    parser.add_argument('--size', help='output size in inches')
    parser.add_argument('--ymin', help='minimum y value to display')
    parser.add_argument('--xmin', help='minimum x value to display')
    parser.add_argument('--ymax', help='maximum y value to display')
    parser.add_argument('--xmax', help='maximum x value to display')
    parser.add_argument('--xlabel', help='X axis label')
    parser.add_argument('--ylabel', help='Y axis label')
    parser.add_argument('--source', help='source attribution')
    parser.add_argument('--spines', help='show axis spines')
    parser.add_argument('--xticks', help='ticks for xaxis')
    parser.add_argument('--yticks', help='ticks for yaxis')
    parser.add_argument('--grid', help='show grid lines on yaxis')
    parser.add_argument('--xlabel_off', help='disable xaxis label')
    parser.add_argument('--label_lines', help='show series labels on end of '
                        'line')
    parser.add_argument('--label_area', help='show series label in center of '
                        'area')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='store_const',
                           const=logging.DEBUG, default=logging.INFO)
    verbosity.add_argument('-q', '--quiet', dest='verbose',
                           action='store_const', const=logging.WARNING)
    return parser.parse_args(args)


def main(args=sys.argv[1:]):
    """Dispatches request to module. """
    args = parse_args(args)

    kwargs = {n: vars(args)[n] for n in vars(args) if vars(args)[n] is not
              None}

    logging.basicConfig(level=kwargs.pop('verbose'))
    outfile = kwargs.pop('outfile')
    save_fig(outfile, **kwargs)


if __name__ == "__main__":
    main()

