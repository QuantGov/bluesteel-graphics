#!/usr/bin/env python

"""
bluesteel.graphics

Utility functions for generating Mercatus style graphics objects and files.
"""

import argparse
import logging
import matplotlib.pyplot as plt
import pandas as pd
import sys
#
from pathlib import Path

log = logging.getLogger(Path(__file__).stem)

def draw_chart(data, ylabel=None, xlabel=None, title=None, source=None,
               type_='Line', xmax=None, xmin=None, ymax=None, ymin=None):
    if len(data.columns) > 1:
        fig, ax = plt.subplots(1)
        for x in data.columns:
            if type_ == 'Line':
                ax.plot(data[x], label=x)
                
        ax.legend(loc='best')
    if type_ == "Line":
        plt.plot(data)
    elif type_ == "hist":
        plt.hist(data)
    if ylabel:
        plt.ylabel(ylabel)
    if xlabel:
        plt.xlabel(xlabel)
    if title:
        plt.title(title)
    if xmax or xmin or ymax or ymin:
        print('hit')
        plt.axis([xmin, xmax, ymin, ymax])
    if source:
        plt.annotate(source, xy=(10, 10), xycoords = 'figure pixels')    


def save_fig(outfile, **kwargs):
    draw_chart(**kwargs)
    log.debug(f'attempting to save to {outfile}')
    plt.savefig(str(outfile))


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

    save_fig(args.outfile, data=indata)


if __name__ == "__main__":
    main()
