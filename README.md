# bluesteel-graphics---data visualization module for bluesteel


## Synopsis
This module is a utility for producing simple production-quality charts quickly and easily. There are 2 ways to interact with the module- through the programmatic API, and via the command line interface. 

### Command Line Interface
With the bluesteel-graphics module installed, graphics may be created using python's -m flag. Example:

    `python -m blusteel-graphics PATH/TO/DATA.csv --title "A sample chart"`
The command line interface supports the following options:


* data [required] - must be the first argument. Supports .csv and .xlsx files.
* -o --outfile - path to output file including file type. Supported output file types are
    pdf, png, raw, rgba, svg, and svgz
* --type_ - type of chart. Supported types include line, scatter plot, horizontal bar, 
    vertical bar, and stacked area charts
* --title - Chart main title
* --format - filetype of the output. If not specified, the filetype will be determined
    by the suffix of the outfile
* --size - size of output image in inches
* --ymin - minimum value for y axis 
* --ymax - maximum value for y axis 
* --xmin - minimum value for x axis 
* --xmax - maximum value for x axis 
* --xlabel - x axis label
* --ylabel - y axis label


### Programmatic API
The programmatic API accepts the long form name of all parameters accepted by the Command Line Interface. The input data should still be the first argument, and must consist of a pandas DataFrame with the X-Axis values as the index.


## Installation

The bluesteel graphics module can be installed using `pip install bluesteel-graphics`. 

## Tests
This module uses pytest - simply ensure you have pytest installed (with flake8) and run the command `py.test` from the root directory of the installation.

