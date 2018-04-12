from bluesteel.graphics.graphics import create_figure
from bluesteel.graphics.graphics import create_image
from pathlib import Path
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt

plt.style.use(str(Path(__file__).parent.joinpath('mercatus.mplstyle')))
font_dirs = [str(Path(__file__).parent.joinpath('fonts'))]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)

__version__ = '0.2.dev'
