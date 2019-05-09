#!/usr/bin/env python

"""
bluesteel.graphics

Utility functions for generating Mercatus style graphics objects and files.
"""

import io
import logging

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rc
from pathlib import Path

from . import standard_formatting
from . import specific_formatting

log = logging.getLogger(Path(__file__).stem)
colors = [i['color'] for i in plt.rcParams['axes.prop_cycle']]


# Overarching Functions that Direct to the Correct Chart Type
def create_image(data, pubs_format=None, **kwargs):
    """
    Create an image of a chart

    :param data: a DataFrame representing the data to be charted
    :param kind: type of chart to create
    :param format: three-letter code for the image type to be created
    :param **kwargs: settings for the chart

    :returns: a BytesIO holding the image
    """
    if pubs_format:
        plt.style.use(str(Path(__file__).parent.joinpath(
            'mercatuspub.mplstyle')))
        filetype = 'eps'
        rc('text', usetex=True)
    else:
        plt.style.use(str(Path(__file__).parent.joinpath('mercatus.mplstyle')))
        filetype = 'png'
    imagebuffer = io.BytesIO()
    create_figure(data, **kwargs).savefig(
        imagebuffer,
        format=filetype,
        bbox_inches='tight',
        dpi='figure'
    )
    imagebuffer.seek(0)

    return imagebuffer


def create_figure(data, kind='line', **kwargs):
    """
    Dispatcher function for different chart types.
    """
    kinds = {
        'line': draw_line_chart,
        'stacked_area': draw_stacked_area_chart,
        'scatter': draw_scatter_plot,
        'horizontal_bar': draw_horizontal_bar_chart,
        'vertical_bar': draw_vertical_bar_chart,
        'stacked_vbar': draw_vertical_stacked_bar,
        'stacked_hbar': draw_horizontal_stacked_bar
    }
    if kind not in kinds:
        raise NotImplementedError("This chart type is not supported")
    fig = kinds[kind](data, **kwargs)

    return fig


# Start of Individual Chart Types
def draw_scatter_plot(data, grid=None, **kwargs):
    """
    Creates standard scatter plot and returns figure

    :param data: input data
    :param grid: add grid lines
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    x_value = data.index.values

    for column in list(data):
        ax.scatter(x_value, data[column])
    if len(list(data)) > 1:
        plt.legend(frameon=True)
    if grid:
        ax.set(axisbelow=True)
        ax.grid(axis='y')
    fig = specific_formatting.min_max_scatter_formatter(fig, ax, **kwargs)
    fig = specific_formatting.set_ticks_nonbar(fig, ax, **kwargs)

    return standard_formatting.format_figure(data, fig, **kwargs)


def draw_line_chart(data, line_thickness=2, label_lines=None, color=[0],
                    grid=None, **kwargs):
    """Creates standard line chart and returns figure

    :param data: input data
    :param lw: line width
    :param label_lines: shows label at end of line
    :param color: sets starting color
    :param grid: add grid lines
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    if (len(data.columns) > 1) and (color == [0]):
        color = list(np.arange(0, len(data.columns)))
    for i, (_, series) in enumerate(data.items()):
        ax.plot(series, lw=line_thickness, color=colors[int(color[i])])
    if len(data.index) < 6:
        ax.set_xticks(data.index)
    if label_lines:
        for name, series in data.items():
            ax.text(
                series.index[-1], series.iloc[-1],
                f'{name}: {series.iloc[-1]:,.0f}',
                va='center',
                ha='left',
                size='small'
            )
    if grid:
        ax.set(axisbelow=True)
        ax.grid(axis='y')
    fig = specific_formatting.min_max_line_area_formatter(fig, ax,
                                                          data, **kwargs)
    fig = specific_formatting.set_ticks_nonbar(fig, ax, **kwargs)

    return standard_formatting.format_figure(data, fig, **kwargs)


def draw_stacked_area_chart(data, label_area=None, grid=None, **kwargs):
    """Creates filled line chart and returns figure

    :param data: input data
    :param label_area: adds area labels
    :param grid: add grid lines
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    x_values = data.index.values
    y_values = np.row_stack(data[i] for i in list(data))
    ax.stackplot(x_values, y_values)
    if len(data.index) < 6:
        ax.set_xticks(data.index)
    if label_area:
        stacked = data.cumsum(axis='columns')
        xmid = sum(ax.get_xbound()) / 2
        midvals = [0] + stacked.xs(xmid).tolist()
        for name, lower, upper in zip(stacked.columns, midvals[: -1],
                                      midvals[1:]):
            ax.text(xmid, (lower + upper) / 2, name, va='center', ha='center')
    if grid:
        ax.set(axisbelow=True)
        ax.grid(axis='y')
    fig = specific_formatting.min_max_line_area_formatter(fig, ax,
                                                          data, **kwargs)
    fig = specific_formatting.set_ticks_nonbar(fig, ax, **kwargs)

    return standard_formatting.format_figure(data, fig, **kwargs)


def draw_vertical_bar_chart(data, label_bars=None, color=[0],
                            grid=None, **kwargs):
    """Creates vertical bar chart and returns figure

    :param data: input data
    :param label_bars: add data labels to bars
    :param color: starting color
    :grid: turns grid lines off
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    width = (2 / 3) / len(data.columns)
    if (len(data.columns) > 1) and (color == [0]):
        color = list(np.arange(0, len(data.columns)))
    for i, (_, series) in enumerate(data.items()):
        ax.bar(bars + i * width, series.values, width,
               color=colors[int(color[i])])
        if label_bars:
            for j, k in zip(bars, series.values):
                ax.text(j + i * width,
                        series.iloc[j] + series.values.max() * .01,
                        "{:,.0f}".format(k), va='bottom', ha='center',
                        size=(18 - len(data.columns) * 3))
    ax.set_xticks(bars + width * (len(data.columns) * 0.5 - 0.5))
    if len(data.columns) > 1:
        ax.legend(labels=data.columns)
    fig = specific_formatting.axis_labels_vbar(fig, ax, data, **kwargs)

    if grid:
        pass
    else:
        for i in ax.get_yticks():
            ax.axhline(y=i, color='white')

    return standard_formatting.format_figure(data, fig, **kwargs)


def draw_vertical_stacked_bar(data, color=[0], **kwargs):
    """Creates stacked vertical bar chart and returns figure

    :param data input data
    :param color: starting color
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    width = .66
    data_bottoms = data.cumsum(axis=1).shift(1, axis=1).fillna(0)
    if (len(data.columns) > 1) and (color == [0]):
        color = list(np.arange(0, len(data.columns)))
    for i, column in enumerate(data.columns[::-1]):
        ax.bar(bars, data[column], bottom=data_bottoms[column],
               width=width, label=column, color=colors[int(color[i])])
    ax.legend()
    ax.set_xticks(bars)
    fig = specific_formatting.axis_labels_vbar(fig, ax, data, **kwargs)

    return standard_formatting.format_figure(data, fig, **kwargs)


def draw_horizontal_bar_chart(data, label_bars=None, color=[0], xlabel=None,
                              ylabel=None, grid=None, **kwargs):
    """Creates horizontal bar chart and returns figure

    :param data: input data
    :param label_bars: add data labels to bars
    :param color: starting color
    :param xlabel: label for xaxis
    :param ylabel: label for yaxis
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    height = (2 / 3) / len(data.columns)
    if (len(data.columns) > 1) and (color == [0]):
        color = list(np.arange(0, len(data.columns)))
    for i, (_, series) in enumerate(data.items()):
        ax.barh(bars + i * height, series.values, height,
                color=colors[int(color[i])])
        if label_bars:
            for j, k in zip(bars, series.values):
                ax.text(series.iloc[j] + series.values.max() * .01,
                        j + i * height, "{:,.0f}".format(k), va='center',
                        ha='left', size=(18 - len(data.columns) * 3))
    ax.set_yticks(bars + height * (len(data.columns) * 0.5 - 0.5))

    fig = specific_formatting.axis_labels_hbar(fig, ax, data, **kwargs)

    if grid:
        pass
    else:
        ax.xaxis.grid(color='white', lw=2, alpha=1)

    # Sets default x and y labels if not given
    if not xlabel:
        xlabel = data.columns[0]
    if not ylabel:
        ylabel = data.index.name

    return standard_formatting.format_figure(data, fig, xlabel=xlabel,
                                             ylabel=ylabel, **kwargs)


def draw_horizontal_stacked_bar(data, label_bars=None, color=[0], xlabel=None,
                                ylabel=None, grid=None, **kwargs):
    """Creates stacked horizontal bar chart and returns figure

    :param data input data
    :param label_bars: add data labels to bars
    :param color: starting color
    :param xlabel: label for xaxis
    :param ylabel: label for yaxis
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    height = .66
    data_bottoms = data.cumsum(axis=1).shift(1, axis=1).fillna(0)
    if (len(data.columns) > 1) and (color == [0]):
        color = list(np.arange(0, len(data.columns)))
    for i, column in enumerate(data):
        ax.barh(bars, data[column], left=data_bottoms[column],
                height=height, label=column, color=colors[int(color[i])])
    ax.legend()
    ax.set_yticks(bars)
    fig = specific_formatting.axis_labels_hbar(fig, ax, data, **kwargs)

    # Sets default x and y labels if not given
    if not xlabel:
        xlabel = data.columns[0]
    if not ylabel:
        ylabel = data.index.name

    return standard_formatting.format_figure(data, fig, xlabel=xlabel,
                                             ylabel=ylabel, **kwargs)
