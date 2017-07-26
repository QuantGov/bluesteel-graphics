#!/usr/bin/env python

"""
bluesteel.graphics

Utility functions for generating Mercatus style graphics objects and files.
"""

import io
import logging

import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from PIL import Image as image


LOGO = image.open(str(Path(__file__).parent.joinpath('mercatus_logo.eps')))
LOGO.load(10)

log = logging.getLogger(Path(__file__).stem)
plt.style.use(str(Path(__file__).parent.joinpath('mercatus.mplstyle')))


def create_image(data, type_='line', format='png', **kwargs):
    """
    Create an image of a chart

    :param data: a DataFrame representing the data to be charted
    :param type_: type of chart to create
    :param image_format: three-letter code for the image type to be created
    :param **kwargs: settings for the chart

    :returns: a BytesIO holding the image
    """
    imagebuffer = io.BytesIO()
    draw_chart(data, type_=type_, **kwargs).savefig(
        imagebuffer,
        format=format,
        bbox_inches='tight',
        dpi='figure'
    )
    return imagebuffer


def draw_chart(data, type_='line', **kwargs):
    """Dispatcher function for different chart types. """

    kinds = {
        'line': draw_line_chart,
        "stacked_area": draw_filled_line_chart,
        "scatter": draw_scatter_plot,
        'horizontal_bar': draw_horizontal_bar_chart,
        'vertical_bar': draw_vertical_bar_chart
    }
    if type_ not in kinds:
        raise NotImplementedError("This chart type is not supported")
    fig = kinds[type_](data, **kwargs)
    return format_figure(data, fig, **kwargs)


def draw_filled_line_chart(data, **kwargs):
    """Creates filled line chart and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """

    # Set up the data and style
    fig, ax = plt.subplots()
    x_values = data.index.values

    y_values = np.row_stack(data[i] for i in list(data))
    ax.stackplot(x_values, y_values)

    # Better labels for graphs with few x values
    fix_xticks_for_short_series(data, ax)

    return fig


def draw_line_chart(data, **kwargs):
    """Creates standard line chart and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    for _, series in data.items():
        ax.plot(series)

    # Better labels for graphs with few x values
    fix_xticks_for_short_series(data, ax)

    return fig


def draw_horizontal_bar_chart(data, **kwargs):
    """Creates horizontal bar chart and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    height = 2 / 3
    values = data.iloc[:, 0]
    ax.barh(bars, values, height)
    ax.set_ylim(bars.min() - height * .75, bars.max() + height * .75)
    ax.set_yticks(bars)
    ax.set_yticklabels(data.index)
    ax.tick_params(bottom='off', left='off')
    ax.set_xticklabels('{:,.0f}'.format(i) for i in ax.get_xticks())
    for i, k in zip(bars, values.values):
        ax.text(values.iloc[i] * 1.01, i, "{:,.0f}".format(k),
                va='center', ha='left')
    return fig


def draw_vertical_bar_chart(data, **kwargs):
    """Creates vertical bar chart and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    width = 2 / 3
    values = data.iloc[:, 0]
    ax.bar(bars, values, width)
    ax.set_xlim(bars.min() - width * .75, bars.max() + width * .75)
    ax.set_xticks(bars)
    ax.set_xticklabels(data.index)
    ax.tick_params(bottom='off', left='off')
    ax.set_yticklabels('{:,.0f}'.format(i) for i in ax.get_yticks())
    for i, k in zip(bars, values.values):
        ax.text(i, values.iloc[i] * 1.01, "{:,.0f}".format(k),
                va='bottom', ha='center')
    return fig


def draw_scatter_plot(data, **kwargs):
    """Creates standard scatter plot and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    x_value = data.index.values
    y_value = data.iloc[:, 0]
    ax.scatter(x_value, y_value)

    return fig


def format_figure(data, fig, default_xmin=None, rot=None, title=None,
                  source=None, xmax=None, ymax=None, xmin=None, ymin=None,
                  size=None, xlabel=None, ylabel=None, spines=True,
                  yticks=None, xticks=None, grid=False, xlabel_off=False):
    """Handles general formatting common across all chart types."""

    ax = fig.gca()
    # Axis Labels
    if xlabel is None and not xlabel_off:
        xlabel = data.index.name
        plt.xlabel(xlabel)
    if ylabel is None:  # TODO: this should only be true for one-series charts!
        ylabel = data.columns[0]
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
    else:
        ax.set_xlim(xmin=default_xmin)
    if ymin:
        ax.set_ylim(ymin=ymin)
    else:
        ax.set_ylim(ymin=0)
    if rot:
        plt.xticks(rotation=rot)

    # Hides the 0 on the y-axis for a cleaner look if ylabels are not
    # user-specified
    if not yticks:
        plt.setp(ax.get_yticklabels()[0], visible=False)

    # puts commas in y ticks
    if yticks:
        ax.set_yticks(yticks)
    ax.set_yticklabels('{:,.0f}'.format(i) for i in ax.get_yticks())

    # Reduces size of labels greater than 6 digits
    if max(ax.get_yticks()) >= 1000000:
        ax.set_yticklabels('' if not i else f"{i / 1000:,.0f}"
                           for i in ax.get_yticks())
    # Turns ticks marks off
    ax.tick_params(bottom='off', left='off')

    # Optionally turns on ygrid
    if grid:
        ax.set(axisbelow=True)
        ax.grid(axis='y')

    # spines
    if not spines:
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    if source:
        fig.text(ax.get_position().x1, 0, source, size=10, ha='right')

    # logo
    figwidth = fig.get_size_inches()[0] * fig.dpi
    logo_width = int(figwidth / 3)
    fig.figimage(LOGO.resize(
        (logo_width,
         int(logo_width * LOGO.height / LOGO.width))),
        xo=fig.dpi / 16,
        yo=fig.dpi / 16
    )

    return fig


def fix_xticks_for_short_series(data, ax):
    """
    Fix xticks if there are fewer thank six datapoints

    :data: DataFrame holding the chart data
    :ax: active Axes object

    """
    if len(data.index) < 6:
        ax.set_xticks(data.index)
