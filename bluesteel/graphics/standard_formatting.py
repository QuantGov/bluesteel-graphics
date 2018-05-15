import logging
import matplotlib.pyplot as plt
import re
from pathlib import Path
from PIL import Image as image


# Sets overarching style attributes
LOGO = image.open(str(Path(__file__).parent.joinpath('mercatus_logo.eps')))
LOGO.load(10)
log = logging.getLogger(Path(__file__).stem)
plt.style.use(str(Path(__file__).parent.joinpath('mercatus.mplstyle')))
colors = [i['color'] for i in plt.rcParams['axes.prop_cycle']]


# Formatting that every chart type is directed through
def format_figure(data, fig, spines=False, title=False, xlabel_off=False,
                  ylabel_off=False, xlabel=None, ylabel=None, rot=None,
                  source=False, phoenix=False, **kwargs):

    ax = fig.gca()

    # Format yaxis zeroes
    ax.tick_params(axis='y', pad=10)

    # Tick Marks
    ax.tick_params(bottom=False, left=False)

    # Spines
    if not spines:
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    # Title
    if title:
        title = re.sub(r'(\d{4})-(\d{4})', '\\1\N{EN DASH}\\2', title)
        ax.set_title(title.replace('\\n', '\n'))

    # X Label
    if not xlabel_off:
        if xlabel:
            ax.set_xlabel('\n' + xlabel)
        else:
            try:
                ax.set_xlabel('\n' + data.index.name)
            except TypeError:
                pass

    # Y Label
    if not ylabel_off:
        if ylabel:
            ax.set_ylabel(ylabel + '\n')
        else:
            try:
                ax.set_ylabel(data.columns[0] + '\n')
            except TypeError:
                pass

    # Rotates the x-axis according to user input
    if rot:
        plt.xticks(rotation=rot)

    # Source
    if source:
        source = re.sub(r'(\d{4})-(\d{4})', '\\1\N{EN DASH}\\2', source)
        fig.text(ax.get_position().x1, 0, source.replace('\\n', '\n'),
                 size=10, ha='right')
        fig.subplots_adjust(bottom=0.17)
    else:
        fig.text(ax.get_position().x1, 0,
                 u'Produced with Bluesteel Graphics\u2122.',
                 size=10, ha='right')
        fig.subplots_adjust(bottom=0.17)

    # Logo
    figwidth = fig.get_size_inches()[0] * fig.dpi

    logo_width = int(figwidth / 3)
    if phoenix:
        fig.figimage(LOGO.resize(
            (logo_width,
             int(logo_width * LOGO.height / LOGO.width))),
            xo=fig.dpi / 16,
            yo=fig.dpi / 16,
            origin='lower'
        )
    else:
        fig.figimage(LOGO.resize(
            (logo_width,
             int(logo_width * LOGO.height / LOGO.width))),
            xo=fig.dpi / 16,
            yo=fig.dpi / 16,
            origin='upper'
        )

    # Tests for false params
    test_fig, test_ax = plt.subplots()
    variable_list = ['kind', 'title', 'size', 'xmin', 'ymin', 'ymax', 'xmax',
                     'xlabel', 'ylabel', 'source', 'spines', 'xtick_loc',
                     'ytick_loc', 'xticklabels', 'yticklabels', 'xyear',
                     'yyear', 'rot', 'xlabel_off', 'ylabel_off', 'label_bars',
                     'label_lines', 'label_area', 'line_thickness',
                     'color', 'grid']
    for i in variable_list:
        try:
            kwargs.pop(i)
        except KeyError:
            pass
    test_ax.set(**{i: j for i, j in kwargs.items() if j is not None})

    return fig
