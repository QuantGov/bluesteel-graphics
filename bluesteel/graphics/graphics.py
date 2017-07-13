#!/usr/bin/env python

"""
bluesteel.graphics

Utility functions for generating Mercatus style graphics objects and files.
"""

import logging
import matplotlib.pyplot as plt
import os

from pathlib import Path

log = logging.getLogger(Path(__file__).stem)


def draw_chart(data, ylabel=None, xlabel=None, title=None, source=None,
               type_='Line', xmax=None, xmin=None, ymax=None, ymin=None):
    plt.style.use(os.path.dirname(os.path.abspath(__file__))
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


def line_chart(data, rot=None, title=None, source=None,
               xmax=None, ymax=None, xmin=None, ymin=None,
               size=None, xlabel=None, ylabel=None):

    # Set up the data and style
    plt.style.use('mercatus.mplstyle')
    f, ax = plt.subplots()
    header_list = list(data)
    x_value = data.iloc[:, 0]
    y_value = data.iloc[:, 1]

    # Takes care of graphs with multiple lines and too few input issues
    if len(header_list) > 2:
        header_list.pop(0)
        for i in header_list:
            plt.plot(x_value, data[i])
        if len(x_value) < 6:
            plt.xticks(x_value)
    else:
        plt.plot(x_value, y_value)
        if len(x_value) < 6:
            plt.xticks(x_value)
            plt.yticks(y_value)

    # Formatting
    ax.set_yticklabels('{:,.0f}'.format(i)
                       if i else '' for i in ax.get_yticks())
    ax.set_yticklabels('{:,.0f}'.format(i) for i in ax.get_yticks())
    ax.tick_params(bottom='off', left='off')

    # Axis Labels
    if not xlabel:
        xlabel = header_list[0]
    if not ylabel:
        ylabel = header_list[1]
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Other Options for the Graph
    if title:
        plt.title(title)
    if xmax:
        ax.set_xlim(xmax=xmax)
    if ymax:
        ax.set_ylim(ymax=ymax)
    if xmin:
        ax.set_xlim(xmin=xmin)
    if ymin:
        ax.set_ylim(ymin=ymin)
    if rot:
        plt.xticks(rotation=rot)
    if source:
        f.text(1, 0, source, transform=ax.transAxes,
               fontsize=10, ha='right', va='bottom')

    return f

