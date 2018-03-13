#!/usr/bin/env python

"""
bluesteel.graphics

Utility functions for generating Mercatus style graphics objects and files.
"""

import io
import logging
import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib.font_manager as font_manager

from pathlib import Path
from PIL import Image as image

font_dirs = [str(Path(__file__).parent.joinpath('fonts'))]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)

LOGO = image.open(str(Path(__file__).parent.joinpath('mercatus_logo.eps')))
LOGO.load(10)

log = logging.getLogger(Path(__file__).stem)
plt.style.use(str(Path(__file__).parent.joinpath('mercatus.mplstyle')))

colors = [i['color'] for i in plt.rcParams['axes.prop_cycle']]


def create_image(data, format='png', **kwargs):
    """
    Create an image of a chart

    :param data: a DataFrame representing the data to be charted
    :param kind: type of chart to create
    :param format: three-letter code for the image type to be created
    :param **kwargs: settings for the chart

    :returns: a BytesIO holding the image
    """
    imagebuffer = io.BytesIO()
    create_figure(data, **kwargs).savefig(
        imagebuffer,
        format=format,
        bbox_inches='tight',
        dpi='figure'
    )

    imagebuffer.seek(0)
    return imagebuffer


def create_figure(data, kind='line', **kwargs):
    """Dispatcher function for different chart types. """

    kinds = {
        'line': draw_line_chart,
        'stacked_area': draw_filled_line_chart,
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


def draw_line_chart(data, lw=2, label_lines=False, color=[0], **kwargs):
    """Creates standard line chart and returns figure

    :param data: input data
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    if (len(data.columns) > 1) and (color == [0]):
        color = list(np.arange(0, len(data.columns)))
    for i, (_, series) in enumerate(data.items()):
        ax.plot(series, lw=lw, color=colors[int(color[i])])

    if label_lines:
        for name, series in data.items():
            ax.text(
                series.index[-1], series.iloc[-1],
                f'{name}: {series.iloc[-1]:,.0f}',
                va='center',
                ha='left',
                size='small'
            )

    # Better labels for graphs with few x values
    fix_xticks_for_short_series(data, ax)

    return format_figure(data, fig, **kwargs)


def draw_horizontal_bar_chart(data, xmin=None, xmax=None, ymin=None, ymax=None,
                              color=[0], **kwargs):
    """Creates horizontal bar chart and returns figure

    :param data: input data
    :param xmin: xaxis minimum value
    :param xmax: xaxis maxium value
    :param ymin: yaxis minimum value
    :param ymax: yaxis maximum value
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
        # Creates value labels as % if maximum value is less than 1
        if series.values.max() < 1:
            for j, k in zip(bars, series.values):
                ax.text(series.iloc[j] + series.values.max() * .01,
                        j + i * height, "{:.2%}".format(k), va='center',
                        ha='left', size=(18 - len(data.columns) * 3))
        else:
            for j, k in zip(bars, series.values):
                ax.text(series.iloc[j] + series.values.max() * .01,
                        j + i * height, "{:,.0f}".format(k), va='center',
                        ha='left', size=(18 - len(data.columns) * 3))
    if not ymin:
        ymin = bars.min() - height * .75 * len(data.columns)
    if not ymax:
        ymax = bars.max() + height * len(data.columns)
    if not xmin:
        xmin = ax.get_xlim()[0]
    if not xmax:
        xmax = ax.get_xlim()[1]
    xlim = [xmin, xmax]
    ylim = [ymin, ymax]
    ax.set_yticks(bars + height * (len(data.columns) * 0.5 - 0.5))
    ax.set_yticklabels(data.index.values, size='small')
    # Creates x labels as % if maximum value is less than 1
    if xmax < 1:
        ax.set_xticklabels('{:.0%}'.format(i) for i in ax.get_xticks())
    else:
        ax.set_xticklabels('{:,.0f}'.format(i) for i in ax.get_xticks())
    ax.tick_params(bottom='off')
    for i in ax.get_xticks():
        ax.axvline(x=i, color='white')
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)
    # Sets default x and y labels if not given
    if 'xlabel' not in kwargs:
        kwargs['xlabel'] = data.columns[0]
    if 'ylabel' not in kwargs:
        kwargs['ylabel'] = data.index.name

    return format_figure(data, fig, xlim=xlim, ylim=ylim, **kwargs)


def draw_vertical_bar_chart(data, xmin=None, xmax=None, ymin=None, ymax=None,
                            color=[0], **kwargs):
    """Creates vertical bar chart and returns figure

    :param data: input data
    :param xmin: xaxis minimum value
    :param xmax: xaxis maximum value
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
        for j, k in zip(bars, series.values):
            ax.text(j + i * width, series.iloc[j] + series.values.max() * .01,
                    "{:,.0f}".format(k),
                    va='bottom', ha='center',
                    size=(18 - len(data.columns) * 3))
    if not xmin:
        xmin = bars.min() - width * .75 * len(data.columns)
    if not xmax:
        xmax = bars.max() + width * len(data.columns)
    if not ymin:
        ymin = ax.get_ylim()[0]
    if not ymax:
        ymax = ax.get_ylim()[1]
    xlim = [xmin, xmax]
    ylim = [ymin, ymax]
    ax.set_xticks(bars + width * (len(data.columns) * 0.5 - 0.5))
    ax.set_xticklabels(data.index.values)
    ax.tick_params(bottom='off', left='off')
    ax.set_yticklabels('{:,.0f}'.format(i) for i in ax.get_yticks())
    for i in ax.get_yticks():
        ax.axhline(y=i, color='white')
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    fix_xaxis_vertical_bar(data, ax)

    return format_figure(data, fig, xlim=xlim, ylim=ylim, grid=True, **kwargs)


def draw_vertical_stacked_bar(data, xmin=None, xmax=None, ymin=None, ymax=None,
                              color=[0], **kwargs):
    """Creates stacked vertical bar chart and returns figure

    :param data input data
    :param xmin: xaxis minimum value
    :param xmax: xaxis maximum value
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    width = .66
    data_bottoms = data.cumsum(axis=1).shift(1, axis=1).fillna(0)
    for column in data.columns[::-1]:
        ax.bar(bars, data[column], bottom=data_bottoms[column],
               width=width, label=column)
    ax.legend()
    if not xmin:
        xmin = bars.min() - width
    if not xmax:
        xmax = bars.max() + width
    if not ymin:
        ymin = ax.get_ylim()[0]
    if not ymax:
        ymax = ax.get_ylim()[1]
    xlim = [xmin, xmax]
    ylim = [ymin, ymax]
    ax.set_xticks(bars)
    ax.set_xticklabels(data.index.values)
    ax.tick_params(bottom='off', left='off')
    ax.set_yticklabels('{:,.0f}'.format(i) for i in ax.get_yticks())
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    fix_xaxis_vertical_bar(data, ax)

    return format_figure(data, fig, xlim=xlim, ylim=ylim, **kwargs)


def draw_horizontal_stacked_bar(data, xmin=None, xmax=None, ymin=None,
                                ymax=None, color=[0], **kwargs):
    """Creates stacked horizontal bar chart and returns figure

    :param data input data
    :param xmin: xaxis minimum value
    :param xmax: xaxis maximum value
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    bars = np.arange(len(data.index))
    height = .66
    data_bottoms = data.cumsum(axis=1).shift(1, axis=1).fillna(0)
    for column in data:
        ax.barh(bars, data[column], left=data_bottoms[column],
                height=height, label=column)
    ax.legend()
    if not ymin:
        ymin = bars.min() - height
    if not ymax:
        ymax = bars.max() + height
    if not xmin:
        xmin = ax.get_xlim()[0]
    if not xmax:
        xmax = ax.get_xlim()[1]
    xlim = [xmin, xmax]
    ylim = [ymin, ymax]
    ax.set_yticks(bars)
    ax.set_yticklabels(data.index.values, size='small')

    # Sets default x and y labels if not given
    if 'xlabel' not in kwargs:
        kwargs['xlabel'] = data.columns[0]
    if 'ylabel' not in kwargs:
        kwargs['ylabel'] = data.index.name
    return format_figure(data, fig, xlim=xlim, ylim=ylim, **kwargs)


def draw_scatter_plot(data, xmin=None, xmax=None, **kwargs):
    """Creates standard scatter plot and returns figure

    :param data: input data
    :param xmin: xaxis minimum value
    :param xmax: xaxis maximum value
    :param **kwargs: passed through to formatting function
    """
    fig, ax = plt.subplots()
    x_value = data.index.values

    for column in list(data):
        ax.scatter(x_value, data[column])
    if len(list(data)) > 1:
        plt.legend(frameon=True)

    ymin = ax.get_ylim()[0]
    ymax = ax.get_ylim()[1]
    ylim = [ymin, ymax]
    xmin = ax.get_xlim()[0]
    xmax = ax.get_xlim()[1]
    xlim = [xmin, xmax]    

    return format_figure(data, fig, xlim=xlim, ylim=ylim, **kwargs)


def format_figure(data, fig, spines=True, grid=True, label_thousands=True,
                  xlabel_off=False, ylabel_off=False, rot=None, title=False,
                  source=None, **kwargs):
    """Handles general formatting common across all chart types.

    :param data: pd.DataFrame - data used to generate the chart
    :param fig: figure object - created by drawing functions
    :param spines: bool - toggle appearance of chart spines (axis lines)
    :param grid: bool - toggle display of grid lines along the y axis
    :param label_thousands: bool - toggle whether or (thousands) should be
           appended to the yaxis label when ticks are truncated
    :param xlabel_off: bool - toggle display of the xaxis label
    :param rot: int - rotation for x-axis labels
    :param title: str - chart title
    :param source: str - source note (e.g. Source: http://www.quantgov.org

    :param **kwargs: holder for values used in ax.set call. Accepts:
        :param ylim: iterable - minimum and maximum for yaxis limits, defaults
            to (0, None)
        :param xlim: iterable - minimum and maximum for xaxis limits
        :param xlabel: str - xaxis label (defaults to data.index.name)
        :param ylabel: str - yaxis label
        :param xticks: list - values to use for xaxis ticks
        :param yticks: list - values to use for yaxis ticks
    """
    ax = fig.gca()

    if not xlabel_off:
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = data.index.name

    if not ylabel_off:
        if 'ylabel' not in kwargs:
            kwargs['ylabel'] = data.columns[0]

    if 'ylim' not in kwargs:
        kwargs['ylim'] = [0, None]

    if 'xlim' not in kwargs:
        kwargs['xlim'] = [data.index.values.min(), data.index.values.max()]

    if 'yticks' in kwargs:
        ax.set_yticks([int(label) for label in kwargs.pop('yticks')])

    # Allows the user to input x-axis tick labels
    # Produces a warning for incorrect number of labels
    if 'xticks' in kwargs:
        if len(kwargs['xticks']) < len(data.index):
            print('You have supplied too few x-axis labels. Please provide'
                  ' the correct number of labels. Input " " to '
                  'the list add a blank label.')
        elif len(kwargs['xticks']) > len(data.index):
            print('You have supplied too many x-axis labels.'
                  ' Please provide the correct number of labels.')
        ax.set_xticklabels(kwargs.pop('xticks'))

    yticklabels = ax.get_yticks()

    # Reduces size of labels greater than 6 digits
    # This section is ignored if ytick labels already exist
    if len(ax.get_yticklabels()[0].get_text()) == 0:
        if max(yticklabels) >= 1000000:
            # Check to see if any labels need to be formatted as floats
            # to avoid losing precision
            if any([i % 1000 for i in yticklabels]):
                yticklabels = ['' if not i else f"{i / 1000:,}" for i in
                               yticklabels]
            else:
                yticklabels = ['' if not i else f"{i / 1000:,.0f}" for i in
                               yticklabels]
            # Append a 'K' to labels to show that they have been truncated
            # This can be disabled using 'label_thousands=False'
            # in call to create_figure()
            if label_thousands:
                yticklabels = [i + 'K' if i else '' for i in yticklabels]
        else:
            yticklabels = ['{:,.0f}'.format(i) for i in ax.get_yticks()]
        ax.set_yticklabels(yticklabels)

    # Format yaxis zeroes
    ax.tick_params(axis='y', pad=10)

    # Turns ticks marks off
    ax.tick_params(bottom='off', left='off')

    # Optionally turns on ygrid
    if grid:
        ax.set(axisbelow=True)
        ax.grid(axis='y')

    # Apply general ax.set arguments
    ax.set(**{i: j for i, j in kwargs.items() if j is not None})

    # Rotates the x-axis according to user input
    if rot:
        plt.xticks(rotation=rot)

    # Adds em-dash to date range in title
    if title:
        title = re.sub(r'(\d{4})-(\d{4})', '\\1\N{EN DASH}\\2', title)
        ax.set_title(title.replace('\\n', '\n'))

    # Spines
    if not spines:
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    # Set source note
    if source:
        source = re.sub(r'(\d{4})-(\d{4})', '\\1\N{EN DASH}\\2', source)
        fig.text(ax.get_position().x1, 0, source.replace('\\n', '\n'),
                 size=10, ha='right')
        # Leaves more space between logo and x-axis
        fig.subplots_adjust(bottom=0.17)
    else:
        fig.text(ax.get_position().x1, 0,
                 u'Produced with Bluesteel Graphics\u2122.',
                 size=10, ha='right')
        fig.subplots_adjust(bottom=0.17)

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


def fix_xaxis_vertical_bar(data, ax):
    """
    Fix x-axis labels from overlapping in bar charts.

    :data: DataFrame holding the chart data
    :ax: active Axes object

    """
    # Informs the user to consider h-bar if labels are too long
    label = ax.xaxis.get_ticklabels()[0]
    if len(label.get_text()) == 4 and label.get_text().isdigit():
        if len(ax.xaxis.get_ticklabels()) > 12:
            for label in ax.xaxis.get_ticklabels()[1::2]:
                label.set_visible(False)
    else:
        length_list = []
        for item in ax.xaxis.get_ticklabels():
            length_list.append(len(item.get_text()))
            total_length = sum(length_list)
            if (len(item.get_text()) > 9) | \
                    (total_length > 49) | \
                    (len(item.get_text()) > 6 and
                     len(ax.xaxis.get_ticklabels()) > 7):
                print("You may want to consider using a horizontal_bar chart"
                      " so that all of your x-axis labels are readable. Use"
                      " the command --kind horizontal_bar")
