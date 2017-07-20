import sys

import pytest
import pandas as pd
import matplotlib
from matplotlib.testing.decorators import cleanup

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.resolve()))

import bluesteel.graphics
import bluesteel.graphics.__main__


"""
Main Functionality:

1.  Implement a package named graphics in the bluesteel namespace package.
2.  Be pip-installable with Python 3.6+
3.  Have a docstring for every class and function
4.  Have pytest-compatible tests for all major functionality
5.  Comply with PEP-8


1.  Accepts bluesteel.core data representations for data to visualize
2.  Implements a basic set of plots, including:
A.  Line charts
B.  Bar charts
I.  Horizontal bars
II. Vertical Bars
C.  Stacked Area Charts
D.  Scatter Plots
3.  Applies Mercatus Styles
4.  Accepts additional parameters including:
A.  Chart title
B.  Axes titles
C.  X and Y bounds
D.  A source note
E.  If feasible: Annotations
5.  For appropriate charts, allows for legend or on-data series labeling
6.  Provides two interfaces for producing charts:
A.  A high-level interface that returns an image in user-specified format
B.  A low-level interface that returns objects for further manipulation

1.  Uses UNIX convention for arguments and parameters
2.  Reads in data from a CSV or Excel spreadsheet with an index in rows and
series in columns
3.  Employs the programmatic API exclusively for chart creation logic

"""

# PREPARATION
test_data = pd.read_csv('dev/test_data.csv', index_col=0)

# GENERAL


# PROGRAMMATIC INTERFACE
class TestBadChartParams(object):

    def test_BadChartType(self):
        """Should only run on specific types of charts"""
        with pytest.raises(NotImplementedError):
            bluesteel.graphics.gen_chart(
                type_='Pie',
                data=test_data
            )


class TestValidChartTypes(object):

    def test_chartTypes(self):
        # for type in ['Line', 'Horizontal_Bar', 'Vertical_Bar',
        # 'Stacked_Area', 'Scatter']:
        bluesteel.graphics.gen_chart(
            type_="line",
            data=test_data
        )


class TestChartReturnFormats(object):

    def test_ReturnImage(self):
        """Should return proper image formats when specified"""
        types = ['pdf', 'png', 'raw', 'rgba', 'svg', 'svgz']
        # TODO, figure out : 'ps', 'eps',

        for format in types:
            assert format == Path(bluesteel.graphics.__main__.save_fig(
                data=test_data,
                outfile=f'dev/tests/output.{format}',
                format=format)).suffix[1:]

    def test_ReturnObject(self):
        """Should return a graphics object for further testing when
        requested"""
        assert isinstance(
            bluesteel.graphics.gen_chart(data=test_data),
            matplotlib.figure.Figure
        )


class TestChartElements(object):

    @cleanup
    def test_chart_title(self):
        """Should contain a title when passed a valid string"""
        assert ('test_title' == bluesteel.graphics.gen_chart(
            test_data,
            type_='line',
            title='test_title'
        ).gca().get_title())

    @cleanup
    def test_axis_titles(self):
        """Should contain axes titles when passed valid strings"""
        assert ('test_ylabel' == bluesteel.graphics.gen_chart(
            test_data,
            ylabel='test_ylabel'
        ).gca().get_ylabel())

        assert ('test_xlabel' == bluesteel.graphics.gen_chart(
            test_data,
            xlabel='test_xlabel'
        ).gca().get_xlabel())

    @cleanup
    def test_axis_limits(self):
        """Should limit data to specific bounds on request"""
        assert ((1, 20,) == bluesteel.graphics.gen_chart(
            test_data,
            ymin=1,
            ymax=20
        ).gca().get_ylim())
        assert ((1, 20,) == bluesteel.graphics.gen_chart(
            test_data,
            xmin=1,
            xmax=20
        ).gca().get_xlim())

    @cleanup
    def test_source_notes(self):
        """Should contain source notes when passed valid options"""
        pass

    @cleanup
    def test_annotations(self):
        """Should contain annotations if possible when passed valid
        parameters"""
    pass


class TestImageCreation(object):
    # TODO: Need to check against correct files
    def test_ReturnObject(self):
        """
        Tests if the returned object has a read() function that produces bytes
        """
        imgbuf = bluesteel.graphics.graphics.create_image(
            data=test_data
        )
        assert isinstance(imgbuf.read(), bytes)


# COMMAND LINE INTERFACE

class TestCLI(object):

    def test_file_generation(self):
        """File should run without error for basic arguments."""
        bluesteel.graphics.__main__.main(
            args=['dev/test_data.csv', '-o', 'dev/tests/testchart.png',
                  '--title', 'test_title', '--ylabel', 'count', '--xlabel',
                  'date', '--source', 'quantgov.org']
        )
        assert Path('dev/tests/testchart.png').exists()

