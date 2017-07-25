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

    header_list = list(data.index.name) + list(data)

    kinds = {
        'line': draw_line_chart,
        "stacked_area": draw_filled_line_chart,
        "scatter": draw_scatter_plot,
        'horizontal_bar': draw_horizontal_bar_chart,
        'vertical_bar': draw_vertical_bar_chart
    }
    if type_ in kinds:
        return kinds[type_](data, header_list=header_list, **kwargs)
    else:
        raise NotImplementedError("This chart type is not supported")


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
    if len(data) < 6:
        plt.xticks([i for i in data.index.values])

    fig = format_figure(data, fig, ax, **kwargs)
    return fig


def draw_line_chart(data, **kwargs):
    """Creates standard line chart and returns figure

    :param data: input data
    :param header_list: columns headers
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    y_list = [data[i] for i in list(data)]
    for y_values in y_list:
        ax.plot(y_values)

    # Better labels for graphs with few x values
    if len(data) < 6:
        plt.xticks([i for i in data.index.values])

    fig = format_figure(data, fig, ax, **kwargs)
    return fig


def draw_horizontal_bar_chart(data, header_list, **kwargs):
    """Creates horizontal bar chart and returns figure

    :param data: input data
    :param header_list: columns headers
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
    fig = format_figure(data, fig, ax, header_list, **kwargs)
    return fig


def draw_vertical_bar_chart(data, header_list, **kwargs):
    """Creates vertical bar chart and returns figure

    :param data: input data
    :param header_list: columns headers
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
    fig = format_figure(data, fig, ax, header_list, **kwargs)
    return fig


def draw_scatter_plot(data, header_list, **kwargs):
    """Creates standard scatter plot and returns figure

    :param data: input data
    :param header_list: columns headers
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    x_value = data.index.values
    y_value = data.iloc[:, 0]
    ax.scatter(x_value, y_value)

    fig = format_figure(data, fig, ax, header_list, **kwargs)
    return fig


def format_figure(data, fig, ax, header_list, default_xmin=None,
                  rot=None, title=None, source=None,
                  xmax=None, ymax=None, xmin=None, ymin=None,
                  size=None, xlabel=None, ylabel=None):
    """Handles general formatting common across all chart types."""

    plt.style.use(str(Path(__file__).parent.joinpath('mercatus.mplstyle')))
    # Axis Labels
    if xlabel is None:
        xlabel = header_list[0]
    if ylabel is None:
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
    else:
        ax.set_xlim(xmin=default_xmin)
    if ymin:
        ax.set_ylim(ymin=ymin)
    else:
        ax.set_ylim(ymin=0)
    if rot:
        plt.xticks(rotation=rot)
    if source:
        fig.text(1, 0, source, transform=ax.transAxes,
                 fontsize=10, ha='right', va='bottom')
    # Formatting
    # Hides the 0 on the y-axis for a cleaner look
    plt.setp(ax.get_yticklabels()[0], visible=False)
    # puts commas in y ticks
    ax.set_yticklabels('{:,.0f}'.format(i) for i in ax.get_yticks())
    # turns ticks marks off
    ax.tick_params(bottom='off', left='off')

    return fig
