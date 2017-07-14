import logging
import matplotlib.pyplot as plt

from bluesteel.graphics import graphics
from bluesteel.graphics import __main__

log = logging.getLogger(__name__)


def save_fig(outfile, format='png', **kwargs):
    fig = graphics.draw_chart(**kwargs)
    log.debug(f'attempting to save to {outfile}')
    fig.savefig(str(outfile), format=format)
    return str(outfile)


def gen_chart(**kwargs):
    chart = graphics.draw_chart(**kwargs)
    return chart


__version__ = '0.1.dev'
