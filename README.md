notebook-gen
============

This python script will convert a directory full of example implementations and
generate a formatted (and code highlighted) notebook.

Current source languages:
- Java
- C++

Current output formats:
- HTML


Installation
============

Get the code (clone or download this repository if you haven't already).

Install python dependencies:

	pip install -r requirements.txt

Test the installation:

	python notebook-gen.py example-notebook

You should see the 'Hello World' notebook rendered to your terminal.


Usage
=====

Get help for using the python script by running:

	python notebook-gen.py -h

To get started you must put all of your code in a single directory. You can
categorise your algorithms (one level deep) by placing them inside directories.
For example:

	notebook/
		Geometry/
			nope.cpp
			OtherGeom.java
		misc.cpp
		misc.txt

A notebook can then be rendered in HTML by running the following command:

	python notebook-gen.py --outfile notebook.html notebook/

Optionally, you can give your algorithms a description by creating a file with
the same name but an extension of "txt", as with `misc.txt` in the example
above. The first line of this text document will be used as the algorithm' name
and the second line will be used as the algorithm's time complexity. A blank
line should separate these two lines from the algorithm description.

To include only a part of a source file in the notebook, surround the relevant
part with the delimiter lines:

	/* START SOLUTION */
	/* END SOLUTION */


Contributing
============

Please send pull requests to https://github.com/BudgieInWA/notebook-gen
