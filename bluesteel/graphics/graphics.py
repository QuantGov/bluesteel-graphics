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


def create_image(data, format='png', **kwargs):
    """
    Create an image of a chart

    :param data: a DataFrame representing the data to be charted
    :param kind: type of chart to create
    :param image_format: three-letter code for the image type to be created
    :param **kwargs: settings for the chart

    :returns: a BytesIO holding the image
    """
    imagebuffer = io.BytesIO()
    create_figure(data, **kwargs).savefig(
        imagebuffer,
        format=format,
        bbox_inches='tight' if 'source' in kwargs else None,
        dpi='figure'
    )

    imagebuffer.seek(0)
    return imagebuffer


def create_figure(data, kind='line', **kwargs):
    """Dispatcher function for different chart types. """

    kinds = {
        'line': draw_line_chart,
        "stacked_area": draw_filled_line_chart,
        "scatter": draw_scatter_plot,
        'horizontal_bar': draw_horizontal_bar_chart,
        'vertical_bar': draw_vertical_bar_chart
    }
    if kind not in kinds:
        raise NotImplementedError("This chart type is not supported")
    fig = kinds[kind](data, **kwargs)
    return fig


def draw_filled_line_chart(data, label_area=False, **kwargs):
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

    if label_area:
        stacked = data.cumsum(axis='columns')
        xmid = sum(ax.get_xbound()) / 2
        midvals = [0] + stacked.xs(xmid).tolist()
        for name, lower, upper in zip(stacked.columns, midvals[: -1],
                                      midvals[1:]):
            ax.text(xmid, (lower + upper) / 2, name, va='center', ha='center')

    return format_figure(data, fig, **kwargs)


def draw_line_chart(data, label_lines=False, **kwargs):
    """Creates standard line chart and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    for _, series in data.items():
        ax.plot(series)

    if label_lines:
        for name, series in data.items():
            ax.text(
                series.index[-1], series.iloc[-1],
                f'{name}: {series.iloc[-1]:,.0f}',
                va='bottom',
                ha='right',
                size='small'
            )

    # Better labels for graphs with few x values
    fix_xticks_for_short_series(data, ax)

    return format_figure(data, fig, **kwargs)


def draw_horizontal_bar_chart(data, xmin=None, xmax=None, ymin=None, ymax=None,
                              **kwargs):
    """Creates horizontal bar chart and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    height = 2 / 3
    values = data.iloc[:, 0]
    ax.barh(bars, values, height)
    ymin = bars.min() - height * .75
    ymax = bars.max() + height * .75
    xmin = ax.get_xlim()[0]
    xmax = ax.get_xlim()[1]
    xlim = [xmin, xmax]
    ylim = [ymin, ymax]
    ax.set_yticks(bars)
    ax.set_yticklabels(data.index, size='small')
    ax.tick_params(bottom='off')
    ax.set_xticklabels('{:,.0f}'.format(i) for i in ax.get_xticks())
    for i, k in zip(bars, values.values):
        ax.text(values.iloc[i] * 1.01, i, "{:,.0f}".format(k),
                va='center', ha='left', size='small')
    for i in ax.get_xticks():
        ax.axvline(x=i, color='white')

    return format_figure(data, fig, xlim=xlim, ylim=ylim, grid=False, **kwargs)


def draw_vertical_bar_chart(data, xmin=None, xmax=None, **kwargs):
    """Creates vertical bar chart and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    width = 2 / 3
    values = data.iloc[:, 0]
    ax.bar(bars, values, width)
    xmin = bars.min() - width * .75
    xmax = bars.max() + width * .75
    xlim = [xmin, xmax]
    ax.set_xticks(bars)
    ax.set_xticklabels(data.index)
    ax.tick_params(bottom='off', left='off')
    ax.set_yticklabels('{:,.0f}'.format(i) for i in ax.get_yticks())
    for i, k in zip(bars, values.values):
        ax.text(i, values.iloc[i] * 1.01, "{:,.0f}".format(k),
                va='bottom', ha='center', size='small')
    for i in ax.get_yticks():
        ax.axhline(y=i, color='white')
    return format_figure(data, fig, xlim=xlim, **kwargs)


def draw_scatter_plot(data, **kwargs):
    """Creates standard scatter plot and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    x_value = data.index.values

    for column in list(data):
        ax.scatter(x_value, data[column])
    if len(list(data)) > 1:
        plt.legend(frameon=True)
    return format_figure(data, fig, **kwargs)


def format_figure(data, fig, spines=True, grid=True,
                  xlabel_off=False, rot=None,
                  source=None, **kwargs):
    """Handles general formatting common across all chart types.

    :param data: pd.DataFrame - data used to generate the chart
    :param fig: figure object - created by drawing functions
    :param source: str - source note (e.g. Source: http://www.quantgov.org
    :param spines: bool - toggle appearance of chart spines (axis lines)
    :param grid: bool - toggle display of grid lines along the y axis
    :param xlabel_off: bool - toggle display of the xaxis label
    :param rot: int - rotation for x-axis labels
    :param **kwargs: holder for values used in ax.set call. Accepts:
        :param ylim: iterable - minimum and maximum for yaxis limits, defaults
            to (0, None)
        :param xlim: iterable - minimum and maximum for xaxis limits
        :param title: str - chart title
        :param xlabel: str - xaxis label (defaults to data.index.name)
        :param ylabel: str - yaxis label
        :param xticks: list - values to use for xaxis ticks
        :param yticks: list - values to use for yaxis ticks
    """
    ax = fig.gca()
    if not xlabel_off:
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = data.index.name
    if 'ylabel' not in kwargs:
        kwargs['ylabel'] = data.columns[0]

    if 'ylim' not in kwargs:
        kwargs['ylim'] = [0, None]

    if 'xlim' not in kwargs:
        kwargs['xlim'] = [data.index.values.min(), data.index.values.max()]

    if 'ylim' not in kwargs:
        kwargs['ylim'] = [0, None]

    # Hides the 0 on the y-axis for a cleaner look if ylabels are not
    if 'yticks' not in kwargs:
        plt.setp(ax.get_yticklabels()[0], visible=False)

    # Puts commas in y ticks
    if 'yticks' in kwargs:
        ax.set_yticks(kwargs['yticks'])
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

    ax.set(**{i: j for i, j in kwargs.items() if j is not None})

    # Spines
    if not spines:
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    # Set source note
    if source:
        fig.text(ax.get_position().x1, 0, source, size=10, ha='right')
    else:
        # If no source is present, adjust the bottom of the figure to leave
        # room for the logo
        fig.subplots_adjust(bottom=0.2)

    # Logo
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
