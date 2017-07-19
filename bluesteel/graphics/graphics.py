#!/usr/bin/env python

"""
bluesteel.graphics

Utility functions for generating Mercatus style graphics objects and files.
"""

import logging
import matplotlib.pyplot as plt

from pathlib import Path

log = logging.getLogger(Path(__file__).stem)
plt.style.use(str(Path(__file__).parent.joinpath('mercatus.mplstyle')))


def draw_chart(data, type_='line', **kwargs):
    """Dispatcher function for different chart types. """
    kinds = {
        'line': line_chart,
    }
    try:
        return kinds[type_](data, **kwargs)
    except KeyError:
        raise NotImplementedError("This chart type is not supported")


def line_chart(data, rot=None, title=None, source=None,
               xmax=None, ymax=None, xmin=None, ymin=None,
               size=None, xlabel=None, ylabel=None, yaxis_title=None):
    """Base function for line chart creation. """
    # Set up the data and style
    fig, ax = plt.subplots()
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
        ax.set_title(title)
    if yaxis_title:
        ax.set_ylabel(yaxis_title)
    if xmax:
        ax.set_xlim(xmax=xmax)
    if ymax:
        ax.set_ylim(ymax=ymax)
    if xmin:
        ax.set_xlim(xmin=xmin)
    if ymin:
        ax.set_ylim(ymin=ymin)
    if rot:
        ax.xticks(rotation=rot)
    if source:
        fig.text(1, 0, source, transform=ax.transAxes,
                 fontsize=10, ha='right', va='bottom')
    return fig
