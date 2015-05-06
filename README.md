notebook-gen
============

version 1.0.0-beta

This python script will convert a directory full of source code and notes 
into a formatted (and code highlighted) notebook.

Current source languages:
- Java
- C++

Current output formats:
- HTML
- Terminal (because why not)


Installation
============

Get the code (clone or download this repository if you haven't already).

Install python dependencies:

	pip install -r requirements.txt

Test the installation:

	python notebook-gen.py example-notebook

You should see the 'Hello World' notebook rendered to your terminal.

Make the python file executable and put it on your path if you want to run it
directly:

	chmod +x notebook-gen.py
	ln --symbolic $PWD/notebook-gen.py /usr/local/bin/notebook-gen
	notebook-gen -h


Usage
=====

Get help for using the python script by running:

	python notebook-gen.py -h

To get started you must put all of your code and notes under a single directory.
Files with the same base name will be collated into one entry. Entries can be
grouped by placing them in subdirectories. Entries and groups will be presented
in lexographical order. Files and directories starting with a `.` will not be
processed.

For example:

	notebook/
		Geometry/
			nope.cpp
			OtherGeom.java
		-notes.txt
		misc.cpp
		misc.txt

A notebook can then be rendered in HTML by running the following command:

	python notebook-gen.py --outfile notebook.html notebook/

Source Files
------------

Source files for the supported languages will be added as entries. To include
only a part of a source file in the notebook, surround the relevant part with
the delimiter lines:

	/* START SOLUTION */
	/* END SOLUTION */

Text Files
----------

`.txt` files are handled specially.  The first line is used as the algorithm's
name and the second line is used as a short note (usually the algorithm's time
complexity). A blank line separates these from the rest of the file which is the
description that will be interpreted as
[markdown](http://daringfireball.net/projects/markdown/syntax).


Tips For Printing
=================

Use the `--textwidth` argument to specify the column width as a number of code
characters. When your page is wide enough the content will automatically reflow
into columns.

Firefox
-------

Use the scale option to make sure you get the desired number of columns.

To remove the extra margin between the print margin and the page content
navigate to `about:config`, search for "margin" and set
`print.print_margin_right` and `print.print_margin_left` to 0. These settings
might not show up until you have used the UI to change the margins.

Chrome
------

Help!

Contributing
============

Please send pull requests or file bug or request features at [https://github.com/BudgieInWA/notebook-gen](https://github.com/BudgieInWA/notebook-gen).
