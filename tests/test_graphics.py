import bluesteel.graphics
import bluesteel.graphics.__main__
import matplotlib
import pandas as pd
import pytest
import sys

from matplotlib.testing.decorators import cleanup, image_comparison
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.resolve()))


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
        ).gca().get_ylabel().strip())

        assert ('test_xlabel' == bluesteel.graphics.create_figure(
            test_data,
            xlabel='test_xlabel'
        ).gca().get_xlabel().strip())

    @cleanup
    def test_axis_limits(self):
        """Should limit data to specific bounds on request"""
        assert ((1, 20,) == bluesteel.graphics.create_figure(
            test_data,
            ymin=1,
            ymax=20
        ).gca().get_ylim())
        assert ((1, 20,) == bluesteel.graphics.create_figure(
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
    def test_return_object(self):
        """
        Tests if the returned object has a read() function that produces bytes
        """
        imgbuf = bluesteel.graphics.create_image(
            data=test_data
        )
        assert isinstance(imgbuf.read(), bytes)


class TestImageComparison(object):
    # Scatter plot tests
    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='scatter_test_1.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_scatterplot_1(self):
        data = pd.read_csv('tests/test_data/scatter_test_1.csv', index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="scatter",
            title="Sample Scatter Plot",
            source="Source: Random Data Generation",
            xlabel_off=True,
            ytick_loc=[5000],
            xmin=1500,
            yticklabels=["test_label"],
            grid=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='scatter_test_2.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_scatterplot_2(self):
        data = pd.read_csv('tests/test_data/scatter_test_2.csv', index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="scatter",
            title="Sample Scatter Plot",
            source="Source: Random Data Generation",
            xlabel_off=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='scatter_test_3.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_scatterplot_3(self):
        data = pd.read_csv('tests/test_data/scatter_test_3.csv', index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="scatter",
            title="Sample Scatter Plot",
            source="Source: Random Data Generation",
            xlabel_off=True,
            spines=True
        )
        return fig

    # Line Chart Tests
    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='line_test_1.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_line_1(self):
        data = pd.read_csv('tests/test_data/line_test_1.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title='Accumulation of Federal Regulation, 1970-2016',
            kind='line',
            source='Source: Patrick A. McLaughlin and Oliver Sherouse',
            ylabel='thousands of regulatory restrictions',
            ytick_loc=[250000, 500000, 750000, 1000000, 1250000],
            xlabel_off=True,
            xyear=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='line_test_2.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_line_2(self):
        data = pd.read_csv('tests/test_data/line_test_2.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title='Accumulation of Federal Regulation, 1970-2016',
            kind='line',
            source='Source: Patrick A. McLaughlin and Oliver Sherouse',
            ylabel='thousands of regulatory restrictions',
            xlabel_off=True,
            xtick_loc=[1980, 1990, 2000],
            xticklabels=['hi', 'hello', 'goodbye'],
            xmin=1980
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='line_test_3.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_line_3(self):
        data = pd.read_csv('tests/test_data/line_test_3.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind='line',
            grid=True,
            label_lines=True
        )
        return fig

    # Stacked Area Tests
    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_area_test_1.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_stacked_area_1(self):
        data = pd.read_csv('tests/test_data/stacked_area_test_1.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title='A Test Chart',
            kind='stacked_area',
            spines=True,
            xyear=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_area_test_2.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5.7)
    def test_stacked_area_2(self):
        data = pd.read_csv('tests/test_data/stacked_area_test_2.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title='A Test Chart',
            kind='stacked_area',
            label_area=True,
            xyear=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_area_test_3.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5.7)
    def test_stacked_area_3(self):
        data = pd.read_csv('tests/test_data/stacked_area_test_3.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            title='A Test Chart',
            kind='stacked_area',
            xmin=1980,
            xmax=2010,
            ymin=5000,
            label_area=True,
            xyear=True
        )
        return fig

    # Vertical Bar Chart Tests
    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='vertical_bar_test_1.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_vbar_1(self):
        data = pd.read_csv('tests/test_data/vertical_bar_test_1.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="vertical_bar",
            title="A Test Chart",
            xyear=True,
            label_bars=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='vertical_bar_test_2.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_vbar_2(self):
        data = pd.read_csv('tests/test_data/vertical_bar_test_2.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="vertical_bar",
            title="A Test Chart",
            source="The chart was made with love.",
            spines=True,
            label_bars=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='vertical_bar_test_3.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_vbar_3(self):
        data = pd.read_csv('tests/test_data/vertical_bar_test_3.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="vertical_bar",
            xticklabels=['bar1', 'bar2', 'bar3', 'bar4'],
            ytick_loc=30,
            yticklabels=["label"]
        )
        return fig

    # Stacked Vertical Bar Chart Tests
    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_vbar_test_1.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_vbar_stack_1(self):
        data = pd.read_csv('tests/test_data/stacked_vbar_test_1.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="stacked_vbar",
            xyear=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_vbar_test_2.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_vbar_stack_2(self):
        data = pd.read_csv('tests/test_data/stacked_vbar_test_2.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="stacked_vbar",
            xticklabels=["a", "b", " ", "d", "e", " ", "g"],
            xlabel_off=True,
            spines=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_vbar_test_3.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_vbar_stack_3(self):
        data = pd.read_csv('tests/test_data/stacked_vbar_test_3.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="stacked_vbar",
            xticklabels=["I", "am", "", "rotating", "", "some", "labels"],
            xlabel_off=True,
            rot=45,
            ytick_loc=[20, 40, 45]
        )
        return fig

    # Horizontal Bar Chart Tests
    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='hbar_test_1.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_hbar_1(self):
        data = pd.read_csv('tests/test_data/hbar_test_1.csv', index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="horizontal_bar",
            title="A Test Chart",
            xlabel="hello",
            ylabel_off=True,
            grid=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='hbar_test_2.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_hbar_2(self):
        data = pd.read_csv('tests/test_data/hbar_test_2.csv', index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="horizontal_bar",
            title="A Test Chart",
            xlabel="hello",
            spines=True,
            label_bars=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='hbar_test_3.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_hbar_3(self):
        data = pd.read_csv('tests/test_data/hbar_test_3.csv', index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="horizontal_bar",
            title="A Test Chart",
            xtick_loc=[5, 10],
            xticklabels=["hi", "hello"]
        )
        return fig

    # Stacked Horizontal Bar Chart Tests
    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_hbar_test_1.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_hbar_stack_1(self):
        data = pd.read_csv('tests/test_data/stacked_hbar_test_1.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="stacked_hbar",
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_hbar_test_2.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_hbar_stack_2(self):
        data = pd.read_csv('tests/test_data/stacked_hbar_test_2.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="stacked_hbar",
            spines=True,
            xlabel_off=True
        )
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='baseline',
                                   filename='stacked_hbar_test_3.png',
                                   style=('bluesteel/graphics/mercatus.'
                                          'mplstyle'),
                                   savefig_kwargs={'bbox_inches': 'tight'},
                                   tolerance=5)
    def test_hbar_stack_3(self):
        data = pd.read_csv('tests/test_data/stacked_hbar_test_3.csv',
                           index_col=0)
        fig = bluesteel.graphics.create_figure(
            data=data,
            kind="stacked_hbar",
            xtick_loc=[20, 40],
            xticklabels=["test", "test"]
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
