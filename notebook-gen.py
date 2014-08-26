import os
import sys

import argparse

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


class Recipe:
	"""An entry in the notebook."""

	def __init__(self, location, name, flavour):
		self.id      = name + "." + flavour
		self.name    = name
		self.flavour = flavour # language
		self.complexity = ''
		self.dough   = self.get_dough(os.path.join(location, self.name +'.'+ self.flavour))
		self.icing   = self.get_icing(os.path.join(location, self.name +'.txt'))
		
	def get_dough(self, filename):
		"""Loads the algorithm source from the given file."""

		if verbose: print "\tGathering source from", filename
		
		try:
			with open(filename, 'r') as f:
				# look for the first delimiter
				del_found = False
				for line in f:
					if line.startswith(start_delimiter):
						del_found = True
						break

				# use the whole file if not delimiter was found
				if not del_found:
					if verbose: print "\t\tdelimiter not found: using whole file"
					f.seek(0)
					return f.read()

				# while we haven't hit the end, keep the lines
				lines = []
				for line in f:
					if line.startswith(end_delimiter): break
					else: lines.append(line)
				if verbose: print "\t\t", len(lines), "lines"
				return ''.join(lines).strip()
		
		except IOError as e:
			print "\t\tskipping:", e
			return None
	
	def get_icing(self, filename):
		"""Loads the name and description of an algorithm."""
		opened = False
		try:
			with open(filename) as f:
				if verbose: print "\t\tGetting description from", filename
				opened = True
				self.name = f.readline().strip()
				self.complexity = f.readline().strip()
				return f.read().strip()
		except IOError as e:
			if opened: print "\t\tCouldn't get icing:", e

	def bake(self, method):
		"""Renders the code using pygments."""
		if (not self.dough): return None;

		return pygments.highlight(self.dough.replace("\t","    "), lexers[self.flavour], method)


def collect_recipes(src_path):
	"""Walks a dir doing it for each code file."""

	if verbose: print "Collecting recipes from", src_path + "..."
	recipes = {}
	for root, dirs, files in os.walk(src_path):
		if (verbose): print "In", root
		section = os.path.basename(root)
		for f in files:
			bits = f.rsplit(".", 1);
			if len(bits) != 2: continue;
			name, ext = bits;
			if not ext in lexers: continue
			
			if not section in recipes: recipes[section] = []
			recipes[section].append(Recipe(root, name, ext))
	return recipes


def prepare_feast_terminal(recipes):
	raise NotImplemented("Sorry, terminal formatting is currently broken. Try with --html")

	if verbose: print "\nWe have", len(recipes), "recipes\n"
	if verbose: print "---------------------------\n"

	counter = 1
	for r in recipes:
		print "%i. %s" % (counter, r.name)
		counter += 1;
	print
	for r in recipes:
		print "---------------------------\n"
		print '==', r.name, '==\n'
		if r.complexity: print r.complexity + '\n'
		if r.icing:      print r.icing + '\n'
		print r.bake(TerminalFormatter())


def prepare_feast_html(recipes, o):
	
	if verbose: print "Writing html..."
	
	o.write(
'''<html>
<head>
	<title>Notebook</title>
	<style>

	html { font-family: arial, sans-serif; }
	h3 { margin-bottom: 0; }
	.complexity { float: right; font-weight: normal; font-style: italic; }
	.description { margin-left: 2em; font-style: italic; }

''')
	o.write(HtmlFormatter().get_style_defs('\t\t'))
	o.write(
'''	</style>
</head>
<body>

<h1>Notebook</h1>
<h2>Table of Contents</h2>
''')
	o.write('<ol id="toc">\n')

	for group, rs in recipes.iteritems():
		o.write('\t<li>'+group+'\n\t\t<ol>')
		for r in rs: o.write('\t\t\t<li><a href="#'+r.id+'">' + r.name + '</a></li>\n')
		o.write('\t\t</ol>\n\t</li>\n')
	o.write('</ol>')

	for group, rs in recipes.iteritems():
		o.write('<h2>'+group+'</h2>')
		for r in rs:
			o.write('<h3 id="'+r.id+'">'+r.name)
			if r.complexity:
				o.write('<span class="complexity">'+r.complexity+'</span>\n')
			o.write('</h3>\n')
			if r.icing:
				o.write('<div class="description"><pre>' + r.icing + '</pre></div>')
			o.write(r.bake(HtmlFormatter()))

	o.write('</body>\n</html>\n')
	
	if verbose: print "  written!"


if __name__ == '__main__':
	ap = argparse.ArgumentParser("An HTML notebook generator.")
	ap.add_argument('source_dir')
	ap.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout,
			help="filename for the generated output (if ommited, output is set to stdout)")
	ap.add_argument('--html', action='store_true', default=False,
			help="force the output to be html formatted (default output format for stdout is terminal coloured text)")
	ap.add_argument('-v', '--verbose', action='store_true', default=False,
			help="output progress information (ignored if no out file is specified)")

	args = ap.parse_args()
	verbose = args.verbose
	if args.outfile == sys.stdout and not args.html:
		prepare_feast_terminal(collect_recipes(args.source_dir))
	else:
		prepare_feast_html(collect_recipes(args.source_dir), args.outfile)
