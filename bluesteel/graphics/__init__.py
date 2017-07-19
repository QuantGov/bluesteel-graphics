import logging
from pathlib import Path

from bluesteel.graphics import graphics

log = logging.getLogger(__name__)


def save_fig(outfile, **kwargs):
    """Outputs figure to specified location. """
    log.debug(f'attempting to save to {outfile}')
    outfile = Path(outfile)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_bytes(graphics.create_image(**kwargs).read())
    return str(outfile)


def gen_chart(**kwargs):
    """Return matplotlib.figure.Figure object for further manipulation. """
    chart = graphics.draw_chart(**kwargs)
    return chart


__version__ = '0.1.dev'
