import graphics
from pathlib import Path
import unittest
import os

"""
Main Functionality:

1.	Implement a package named graphics in the bluesteel namespace package.
2.	Be pip-installable with Python 3.6+
3.	Have a docstring for every class and function
4.	Have pytest-compatible tests for all major functionality
5.	Comply with PEP-8


1.	Accepts bluesteel.core data representations for data to visualize
2.	Implements a basic set of plots, including:
    A.	Line charts
    B.	Bar charts
        I.	Horizontal bars
        II.	Vertical Bars
    C.	Stacked Area Charts
    D.	Scatter Plots
3.	Applies Mercatus Styles
4.	Accepts additional parameters including:
    A.	Chart title
    B.	Axes titles
    C.	X and Y bounds
    D.	A source note
    E.	If feasible: Annotations
5.	For appropriate charts, allows for legend or on-data series labeling
6.	Provides two interfaces for producing charts:
    A.	A high-level interface that returns an image in user-specified format
    B.	A low-level interface that returns objects for further manipulation

1.	Uses UNIX convention for arguments and parameters
2.	Reads in data from a CSV or Excel spreadsheet with an index in rows and series in columns
3.	Employs the programmatic API exclusively for chart creation logic

"""

# GENERAL

# PROGRAMMATIC INTERFACE
class BadChartParams(unittest.TestCase):

    def testBadChartType(self):
        """Should only run on specific types of charts"""
        self.assertRaises(NotImplemenetedError,
                         graphics.draw_chart(type='Pie',
                                                      data='testdata.csv'))

    def testEmptyData(self):
        """Should fail if passed an empty csv"""
        self.assertRaises(graphics.EmptyDataError,
                          graphics.draw_chart( data='empty.csv'))


class ValidChartTypes(unittest.TestCase):

    def chartTypes():
        for type in ['Line', 'Horizontal_Bar', 'Vertical_Bar',
                     'Stacked_Area', 'Scatter']:
            graphics.draw_chart(type=type, data='testdata.csv')

class ChartReturnFormats(unittest.TestCase):

    def testReturnImage(self):
        """Should return proper image formats when specified"""
        types = ['ps', 'eps', 'pdf', 'pgf', 'png', 'raw', 'rgba', 'svg',
                 'svgz', 'jpg', 'jpeg', 'tif', 'tiff']

        for format in types:
            self.assertEqual(format,
                             os.path.suffix(graphics\
                                        .chart_to_file(data='testdata.csv',
                                                       format=format)))

    def testReturnObject(self):
        """Should return a graphics object for further testing when
        requested"""
        self.assertEqual(graphics.ChartObject,
                        type(graphics\
                             .chart_object(data='testdata.csv')))

class ChartElements(unittest.TestCase):
    
    def testTitle(self):
        """Should contain a title when passed a valid string"""
        self.assertEqual('Test Title',
                         graphics.chart_object(data='testdata.csv',
                                                         title='Test'
                                                         ' Title').title)

    def testYAxisTitle(self):
        """Should contain axes titles when passed valid strings"""
        self.assertEqual('Y Title',
                        graphics.chart_object(data='testdata.csv',
                                                        yaxis_title='Y'
                                                        ' Title').yaxis_title)

    def testXYBounds(self):
        """Should limit data to specific bounds on request"""
        pass 

    def testSourceNotes(self):
        """Should contain source notes when passed valid options"""
        pass

    def testAnnotations(self):
        """Should contain annotations if possible when passed valid
        parameters"""
        pass



# COMMAND LINE INTERFACE

class CLI(unittest.TestCase):

    def test_file_generation(self):
        """File should run without error for basic arguments."""
        graphics.main(args=['-d', 'sample_data.csv',
                                     '-o', 'testchart.png'])
        self.assertTrue(Path('testchart.png').exists())

if __name__ == "__main__":
    unittest.main()
