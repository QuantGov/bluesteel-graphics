#!/usr/bin/env python

"""
bluesteel.graphics

Utility functions for generating Mercatus style graphics objects and files.
"""

import io
import logging

import matplotlib.pyplot as plt

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
    kinds = {
        'line': line_chart,
    }
    try:
        return kinds[type_](data, **kwargs)
    except KeyError:
        raise NotImplementedError("This chart type is not supported")


def filled_line_chart(data, **kwargs):

    #Set up the data and style
    plt.style.use('mercatus.mplstyle')
    fig, ax = plt.subplots()
    header_list = list(data)
    x_value = data.iloc[:,0]
    y_value = data.iloc[:,1]

    #Takes care of graphs with multiple lines and too few input issues
    if len(header_list)>2:
        default_xmin = x_value[0]
        header_list.pop(0)
        if len(x_value)<6:
            plt.xticks(x_value)

        value_dict = {}
        for i in header_list:
            value_dict[i] = data[i][0]
        ordered_list = sorted(value_dict, key=value_dict.__getitem__)
        ax.fill_between(x_value, data[ordered_list[0]], interpolate=True)
        for i in ordered_list:
            ax.fill_between(x_value, data[ordered_list[0]], data[ordered_list[1]], interpolate=True)
            ordered_list.pop(0)
    else:
        plt.plot(x_value, y_value)
        default_xmin = x_value[0]
        if len(x_value)<6:
            plt.xticks(x_value)
            plt.yticks(y_value)
        ax.fill_between(x_value, y_value, interpolate=True)
    fig = formatting(data, fig, ax, header_list,
                    default_xmin, **kwargs)
    return fig


def line_chart(data, **kwargs):
    #Set up the data and style
    plt.style.use('mercatus.mplstyle')
    fig, ax = plt.subplots()
    header_list = list(data)
    x_value = data.iloc[:,0]
    y_value = data.iloc[:,1]

    #Takes care of graphs with multiple lines and too few input issues
    if len(header_list)>2:
        default_xmin = x_value[0]
        header_list.pop(0)
        for i in header_list:
            plt.plot(x_value, data[i])
        if len(x_value)<6:
            plt.xticks(x_value)
    else:
        plt.plot(x_value, y_value)
        default_xmin = x_value[0]
        if len(x_value)<6:
            plt.xticks(x_value)
            plt.yticks(y_value)
    fig = formatting(data, fig, ax, header_list,
                    default_xmin, **kwargs)
    return fig


def scatter_plot(data, **kwargs):

    plt.style.use('mercatus.mplstyle')
    fig, ax = plt.subplots()
    header_list = list(data)
    x_value = data.iloc[:,0]
    y_value = data.iloc[:,1]
    ax.scatter(x_value, y_value)

    fig = formatting(data, fig, ax, header_list,**kwargs)
    return fig


def formatting(data, fig, ax, header_list, default_xmin=None, 
            rot=None, title=None, source=None,
            xmax=None, ymax=None, xmin=None, ymin=None,
            size=None, xlabel=None, ylabel=None):

#Axis Labels
    if xlabel == None:
        xlabel = header_list[0]
    if ylabel == None:
        ylabel = header_list[1]
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

#Other Options for the Graph
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
    #Formatting
    #Hides the 0 on the y-axis for a cleaner look
    plt.setp(ax.get_yticklabels()[0], visible=False)
    #puts commas in y ticks
    ax.set_yticklabels('{:,.0f}'.format(i) for i in ax.get_yticks())
    #turns ticks marks off
    ax.tick_params(bottom='off', left='off')

    return fig
