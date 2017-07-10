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
import os

#
from pathlib import Path

log = logging.getLogger(Path(__file__).stem)

def draw_chart(data, ylabel=None, xlabel=None, title=None, source=None,
               type_='Line', xmax=None, xmin=None, ymax=None, ymin=None):
    plt.style.use(os.path.dirname(os.path.abspath(__file__))\
                  + '/mercatus.mplstyle')
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
        plt.annotate(source, xy=(10, 10), xycoords='figure pixels')

