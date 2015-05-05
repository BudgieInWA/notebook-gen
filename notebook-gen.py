#!/bin/python
from __future__ import print_function

import os
import sys

import argparse
import markdown

import pygments
from pygments.lexers import CppLexer, JavaLexer
from pygments.formatters import HtmlFormatter, TerminalFormatter, NullFormatter

start_delimiter = "/* START SOLUTION */";
end_delimiter   = "/* END SOLUTION */";

lexers = {
	'cpp':   CppLexer(),
	'java': JavaLexer()
}

class MissingDough(Exception):
	pass

verbose = False
def log(*args):
	if verbose: print(*args, file=sys.stderr)

class Recipe:
	"""An entry in the notebook."""

	def __init__(self, name):
		self.id          = name
		self.name        = name
		self.complexity  = ''
		self.codeblocks  = [] # A list of (ext, src) pairs.
		self.description = '' # A markdown source description.
		
	def add_code(self, filename, ext):
		"""Loads the algorithm source from the given file and adds it to the
		recipe."""

		log("\tGathering source from", filename);
		
		try:
			with open(filename, 'r') as f:
				# while we haven't hit the end, keep the lines
				lines = []
				for line in f:
					if line.startswith(start_delimiter): lines = []
					elif line.startswith(end_delimiter): break
					else: lines.append(line)
				log("\t\t", len(lines), "lines")
				self.codeblocks.append((ext, ''.join(lines).strip()))
		
		except IOError as e:
			print("\t\tskipping:", e)
			return None
	
	def add_description(self, filename):
		"""Loads the name and description of an algorithm and adds it to the
		recipe."""

		log("\t\tGetting description from", filename)

		try:
			with open(filename) as f:
				self.name = f.readline().strip()
				self.complexity = f.readline().strip()
				self.description = f.read().strip()
		except IOError as e:
			print("\t\tCouldn't load description:", e)

	def render_codeblocks(self, formatter):
		"""Renders the code using pygments."""

		return [pygments.highlight(src.replace("\t","    "), lexers[ext], formatter)
				for (ext, src) in self.codeblocks]


def collect_recipes(src_path):
	"""Walks a dir collecting turning files into recipes."""

	filetypes = lexers.keys() + ["txt"]

	log("Collecting recipes from", src_path + "...")
	recipes = {}
	for root, dirs, files in os.walk(src_path):
		log("In", root)

		# Don't visit "hidden" directories.
		for d in reversed(dirs):
			if d.startswith("."):
				dirs.remove(d)

		section = os.path.basename(root)
		#TODO make section the bit relative to src_path and make sure the top
		#     level section sorts first
		for f in files:
			if f.startswith("."): continue
			name, ext = os.path.splitext(f)
			ext = ext[1:]
			if not ext in filetypes: continue
			
			if not section in recipes: recipes[section] = {}
			if not name in recipes[section]:
				recipes[section][name] = Recipe(name)

			r = recipes[section][name]
			fn = os.path.join(root, f);
			if ext in lexers:
				r.add_code(fn, ext)
			elif ext == "txt":
				r.add_description(fn)

	return recipes


def render_to_terminal(recipes, o):

	log("\nWe have", len(recipes), "recipes\n")
	log("---------------------------\n")

	counter = 1
	keys = sorted(recipes.iterkeys())
	for group in keys:
		o.write("%i. %s\n" % (counter, group))
		counter += 1
		counter2 = 1
		for r in recipes[group].values():
			o.write("  %i. %s\n" % (counter2, r.name))
			counter2 += 1

	for group in keys:
		if group:
			o.write("\n\n\n" + group)

		for r in recipes[group].values():
			if not r.complexity: r.complexity = ""
			o.write("\n\n" + r.name +
					" "*(80 - len(r.name) - len(r.complexity) - 2) +
					r.complexity)
			o.write("\n\n")
			if r.description: o.write(r.description + "\n\n")
			o.write("\n".join(r.render_codeblocks(TerminalFormatter())))


def render_to_html(recipes, o):
	
	log("Writing html...")
	
	o.write('''
<!doctype html>
<html>
<head>
	<title>Notebook</title>
	<style>

	html { font-family: arial, sans-serif; }
	/*
	body {
		-moz-column-width: 80ch;
		-webkit-column-width: 80ch;
		font-family: monospace;
	}
	*/
	h3 { margin-bottom: 0; }
	.complexity { float: right; font-weight: normal; font-style: italic; }
	.description { color: gray; font-style: italic; }

''')
	o.write(HtmlFormatter().get_style_defs('\t'))
	o.write('''
	</style>
</head>
<body>

<h1>Notebook</h1>
<h2>Table of Contents</h2>
''')
	o.write('<ol id="toc">\n')

	keys = sorted(recipes.iterkeys())
	for group in keys:
		o.write('\t<li>'+group+'\n\t\t<ol>')
		for r in recipes[group].values():
			o.write('\t\t\t<li><a href="#'+r.id+'">' + r.name + '</a></li>\n')
		o.write('\t\t</ol>\n\t</li>\n')
	o.write('</ol>')

	for group in keys:
		o.write('<h2>'+group+'</h2>')
		for r in recipes[group].values():
			o.write('<h3 id="'+r.id+'">'+r.name)
			if r.complexity:
				o.write('<span class="complexity">'+r.complexity+'</span>\n')
			o.write('</h3>\n')
			if r.description:
				o.write('<div class="description">' + 
						markdown.markdown(r.description) + '</div>')
			o.write("\n".join(r.render_codeblocks(HtmlFormatter())))

	o.write('</body>\n</html>\n')
	
	log("  written!")


if __name__ == '__main__':
	ap = argparse.ArgumentParser(description="Generate an HTML notebook from source code files. v1.0.0-beta")
	ap.add_argument('source_dir')
	ap.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout,
			help="filename for the generated output (default stdout)")
	ap.add_argument('-f', '--format',
			help="force the format of the output ('html' or 'term')")
	ap.add_argument('-v', '--verbose', action='store_true', default=False,
			help="output progress information")

	args = ap.parse_args()
	verbose = args.verbose
	fmt = args.format
	if not fmt:
		if args.outfile == sys.stdout:
			fmt = 'term'
		else:
			_, ext = os.path.splitext(args.outfile.name)
			fmt = ext[1:] # remove the leading dot

	recipes = collect_recipes(args.source_dir)

	if fmt == 'html':
		render_to_html(recipes, args.outfile)
	elif fmt == 'term':
		render_to_terminal(recipes, args.outfile)
	else:
		print("Error: unknown format:", fmt)
		ap.print_usage()
