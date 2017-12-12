import sys

import pytest
import pandas as pd
import matplotlib
from matplotlib.testing.decorators import cleanup, image_comparison

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
test_data = pd.read_csv('tests/test_data/test_data.csv', index_col=0)

# GENERAL


# PROGRAMMATIC INTERFACE
class TestBadChartParams(object):

    @cleanup
    def test_bad_chart_types(self):
        """Should only run on specific types of charts"""
        with pytest.raises(NotImplementedError):
            bluesteel.graphics.create_figure(
                kind='Pie',
                data=test_data
            )

    def test_extra_params(self):
        """Should raise an error if incorrect params are provided"""
        with pytest.raises(AttributeError):
            bluesteel.graphics.create_figure(
                data=test_data,
                fake_param=True
            )


class TestValidChartTypes(object):

    @cleanup
    def test_chart_types(self):
        for type in ['line', 'stacked_area', 'scatter',
                     'horizontal_bar', 'vertical_bar']:
            bluesteel.graphics.create_figure(kind=type, data=test_data)


class TestChartReturnFormats(object):

    @cleanup
    def test_return_image(self):
        """Should return proper image formats when specified"""
        types = ['pdf', 'png', 'raw', 'rgba', 'svg', 'svgz']
        # TODO, figure out : 'ps', 'eps',

        for format in types:
            assert format == Path(bluesteel.graphics.__main__.save_fig(
                data=test_data,
                outfile=f'tests/test_output/output.{format}')).suffix[1:]

    def test_return_object(self):
        """Should return a graphics object for further testing when
        requested"""
        assert isinstance(
            bluesteel.graphics.create_figure(data=test_data),
            matplotlib.figure.Figure
        )


class TestChartElements(object):

    @cleanup
    def test_chart_title(self):
        """Should contain a title when passed a valid string"""
        assert ('test_title' == bluesteel.graphics.create_figure(
            test_data,
            kind='line',
            title='test_title'
        ).gca().get_title())

    @cleanup
    def test_axis_titles(self):
        """Should contain axes titles when passed valid strings"""
        assert ('test_ylabel' == bluesteel.graphics.create_figure(
            test_data,
            ylabel='test_ylabel'
        ).gca().get_ylabel())

        assert ('test_xlabel' == bluesteel.graphics.create_figure(
            test_data,
            xlabel='test_xlabel'
        ).gca().get_xlabel())

    @cleanup
    def test_axis_limits(self):
        """Should limit data to specific bounds on request"""
        assert ((1, 20,) == bluesteel.graphics.create_figure(
            test_data,
            ylim=[1, 20],
        ).gca().get_ylim())
        assert ((1, 20,) == bluesteel.graphics.create_figure(
            test_data,
            xlim=[1, 20],
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
    def test_return_object(self):
        """
        Tests if the returned object has a read() function that produces bytes
        """
        imgbuf = bluesteel.graphics.create_image(
            data=test_data
        )
        assert isinstance(imgbuf.read(), bytes)


class TestImageComparison(object):

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='accumulation_area.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_accumulation_area(self):
        """Should match given area chart"""
        data = pd.read_csv('tests/test_data/annual_restrictions.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title='Accumulation of Federal Regulation, 1970-2016',
            kind='stacked_area',
            source=('Source: Patrick A. McLaughlin and Oliver Sherouse, '
                    '"RegData 3.0." \n Available at http://quantgov.org.'),
            ylabel=('thousands of regulatory restrictions in the\nCode of '
                    'Federal Regulations'),
            xlim=[data.index.values.min(), data.index.values.max()],
            spines=False,
            yticks=[0, 250_000, 500_000, 750_000, 1_000_000, 1_250_000],
            xlabel_off=True,
            label_thousands=False
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='accumulation_line.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_accumulation_line(self):
        """Should match given area chart"""
        data = pd.read_csv('tests/test_data/annual_restrictions.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title='Accumulation of Federal Regulation, 1970-2016',
            kind='line',
            source=('Source: Patrick A. McLaughlin and Oliver Sherouse, '
                    '"RegData 3.0." \n Available at http://quantgov.org.'),
            ylabel=('thousands of regulatory restrictions in the\nCode of '
                    'Federal Regulations'),
            spines=False,
            yticks=[0, 250_000, 500_000, 750_000, 1_000_000, 1_250_000],
            xlabel_off=True,
            label_thousands=False
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='pre_crisis_chart.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5.7)
    def test_pre_crisis_chart(self):
        """Should match given area chart"""
        data = pd.read_csv('tests/test_data/title_12_17.csv',
                           index_col=0)
        data_mod = data[:-8]
        fig = bluesteel.graphics.create_figure(
            data=data_mod,
            title=('Growth in Pre-Crisis Finanacial Regulatory Restrictions,'
                   '\n1970-2008'),
            kind='stacked_area',
            source=('Source: Patrick A. McLaughlin and Oliver Sherouse, '
                    '"RegData 3.0" \n available at quantgov.org\nProduced by '
                    'Michael Gasvoda'),
            label_area=True,
            spines=False,
            yticks=[0, 10_000, 20_000, 30_000, 40_000, 50_000],
            xlabel_off=True,
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='multiple_line.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_multiple_line(self):
        """Should match given area chart"""
        data = pd.read_csv('tests/test_data/all_laws.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title=('Regulatory Impact of Dodd-Frank vs. All Other\nObama '
                   'Administration Laws, 2009-2016'),
            kind='line',
            source=('Source: Patrick A. McLaughlin and Oliver Sherouse, '
                    '"RegData 3.0." \n Available at http://quantgov.org'),
            ylabel='cumulative new associated restrictions',
            yticks=[0, 10_000, 20_000, 30_000],
            xlabel_off=True,
            label_lines=True,
            spines=False,
        )
        return fig

    @pytest.mark.mpl_image_comapre(baseline_dir='baseline',
                                   filename='sample_scatter.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_scatterplot(self):
        data = pd.read_csv('tests/test_data/test_data.csv', index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title="Sample Scatter Plot",
            source="Source: Random Data Generation",
            xlabel_off=True,
            spines=False
        )
        return fig

    @pytest.mark.mpl_image_comapre(baseline_dir='baseline',
                                   filename='sample_vbar.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_vbar(self):
        data = pd.read_csv('tests/test_data/test_data.csv', index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="vertical_bar",
            title="Sample Bar Chart",
            source="Random data generation",
            ylabel='Sample taxis title',
            spines=False
        )
        return fig


# COMMAND LINE INTERFACE
class TestCLI(object):

    def test_file_generation(self):
        """File should run without error for basic arguments."""
        bluesteel.graphics.__main__.main(
            args=['tests/test_data/test_data.csv', '-o',
                  'tests/test_output/testchart.png', '--title', 'test_title',
                  '--ylabel', 'count', '--xlabel', 'date', '--source',
                  'quantgov.org']
        )
        assert Path('tests/test_output/testchart.png').exists()
