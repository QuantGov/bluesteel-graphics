import logging
import matplotlib.pyplot as plt

from pathlib import Path

from bluesteel.graphics import graphics
from bluesteel.graphics import __main__

log = logging.getLogger(__name__)


def save_fig(outfile, format='png', **kwargs):
    """Outputs figure to specified location. """
    fig = graphics.draw_chart(**kwargs)
    log.debug(f'attempting to save to {outfile}')
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(outfile), format=format)
    return str(outfile)


def gen_chart(**kwargs):
    """Return matplotlib.figure.Figure object for further manipulation. """
    chart = graphics.draw_chart(**kwargs)
    return chart


__version__ = '0.1.dev'
