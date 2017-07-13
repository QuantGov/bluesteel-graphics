import logging
import matplotlib.pyplot as plt

from bluesteel.graphics import graphics
from bluesteel.graphics import __main__

log = logging.getLogger(__name__)


def save_fig(outfile, **kwargs):
    graphics.draw_chart(**kwargs)
    log.debug(f'attempting to save to {outfile}')
    plt.savefig(str(outfile))


__version__ = '0.1.dev'
