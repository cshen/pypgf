from axis import Axis
from figure import Figure
from settings import Settings
from legend import Legend
from plot import Plot
from surfplot import SurfPlot
from arrow import Arrow
from text import Text
from numpy import asmatrix, inf, min

def gcf():
	"""
	Returns currently active figure.
	"""
	return Figure.gcf()


def gca():
	"""
	Returns currently active axis.
	"""

	return Axis.gca()


def draw():
	"""
	Draws the currently active figure.
	"""

	gcf().draw()


def figure(idx=None):
	"""
	Creates a new figure or moves the focus to an existing figure.

	@type  idx: integer
	@param idx: a number identifying a figure

	@rtype: Figure
	@return: currently active figure
	"""

	return Figure(idx)


def plot(*args, **kwargs):
	"""
	Plot lines or markers.

	B{Examples:}

		>>> plot(y)           # plot y using values 1 to len(y) for x
		>>> plot(x, y)        # plot x and y using default line style and color
		>>> plot(x, y, 'r.')  # plot red markers at positions x and y
	"""

	# split formatting information from data points
	format_string = ''.join([arg for arg in args if isinstance(arg, str)])
	args = [asmatrix(arg) for arg in args if not isinstance(arg, str)]

	# parse format string into keyword arguments
	if 'color' not in kwargs:
		if 'r' in format_string:
			kwargs['color'] = 'red'
		elif 'g' in format_string:
			kwargs['color'] = 'green'
		elif 'b' in format_string:
			kwargs['color'] = 'blue'
		elif 'c' in format_string:
			kwargs['color'] = 'cyan'
		elif 'm' in format_string:
			kwargs['color'] = 'magenta'
		elif 'y' in format_string:
			kwargs['color'] = 'yellow'
		elif 'k' in format_string:
			kwargs['color'] = 'black'
		elif 'w' in format_string:
			kwargs['color'] = 'white'

	if 'marker' not in kwargs:
		if '.' in format_string:
			kwargs['marker'] = '*'
		elif 'o' in format_string:
			kwargs['marker'] = 'o'
		elif '+' in format_string:
			kwargs['marker'] = '+'
		elif '|' in format_string:
			kwargs['marker'] = '|'
		elif '*' in format_string:
			kwargs['marker'] = 'asterisk'
		elif 'x' in format_string:
			kwargs['marker'] = 'x'
		elif 'd' in format_string:
			kwargs['marker'] = 'diamond'
		elif '^' in format_string:
			kwargs['marker'] = 'triangle'
		elif 'p' in format_string:
			kwargs['marker'] = 'pentagon'

	if 'line_style' not in kwargs:
		if '---' in format_string:
			kwargs['line_style'] = 'densely dashed'
		elif '--' in format_string:
			kwargs['line_style'] = 'dashed'
		elif '-' in format_string:
			kwargs['line_style'] = 'solid'
		elif ':' in format_string:
			kwargs['line_style'] = 'densely dotted'

	# hide markers if no line style
	if 'marker' in kwargs and 'line_style' not in kwargs:
		kwargs['line_style'] = 'only marks'

	# error bar shorthands
	if 'xerr' in kwargs:
		kwargs['xvalues_error'] = kwargs['xerr']
		kwargs.pop('xerr')
	if 'yerr' in kwargs:
		kwargs['yvalues_error'] = kwargs['yerr']
		kwargs.pop('yerr')

	# if arguments contain multiple rows, create multiple plots
	if (len(args) > 1) and (args[1].shape[0] > 1) and (args[0].shape[0] == 1):
		return [plot(args[0], *[arg[i] for arg in args[1:]], **kwargs)
			for i in range(len(args[0]))]

	elif (len(args) > 0) and (args[0].shape[0] > 1):
		return [plot(*[arg[i] for arg in args], **kwargs)
			for i in range(len(args[0]))]

	return Plot(*args, **kwargs)



def stem(*args, **kwargs):
	"""
	Plot data points as stems from the x-axis. Takes the same arguments as the
	L{plot} function.

	B{Examples:}

		>>> stem(y)
		>>> stem(x, y)
		>>> stem(x, y, 'r', marker='none')
	"""

	kwargs['ycomb'] = True

	if 'marker' not in kwargs:
		kwargs['marker'] = 'o'

	return plot(*args, **kwargs)



def bar(*args, **kwargs):
	gca().ybar = True

	return plot(*args, **kwargs)


def errorbar(*args, **kwargs):
	"""
	Plot lines or markers with error bars.

	B{Examples:}

		>>> errorbar(y, y_err)
		>>> errorbar(y, y_err, 'r.')
		>>> errorbar(x, y, y_err)
		>>> errorbar(x, y, x_err, y_err)
	"""

	# split formatting information from data points
	format_string = ''.join([arg for arg in args if isinstance(arg, str)])
	args = [asmatrix(arg) for arg in args if not isinstance(arg, str)]

	if len(args) > 3:
		kwargs['xvalues_error'] = args[-2]
		kwargs['yvalues_error'] = args[-1]
		args = args[:-2]
	if len(args) > 1:
		kwargs['yvalues_error'] = args[-1]
		args = args[:-1]

	plot(format_string, *args, **kwargs)


def surf(*args, **kwargs):
	return SurfPlot(*args, **kwargs)


def title(title):
	gca().title = title


def xlabel(xlabel):
	gca().xlabel = xlabel


def ylabel(ylabel):
	gca().ylabel = ylabel


def xtick(xtick):
	gca().xtick = xtick


def ytick(ytick):
	gca().ytick = ytick


def xticklabels(xticklabels):
	gca().xticklabels = xticklabels

	if not gca().xtick:
		xtick(range(1, len(xticklabels) + 1))


def yticklabels(yticklabels):
	gca().yticklabels = yticklabels


def axis(*args):
	if len(args) < 1:
		return gca()

	if len(args) < 4:
		if isinstance(args[0], str):
			ax = gca()

			if args[0] == 'equal':
				ax.equal = True

			elif args[0] == 'square':
				ax.width = ax.height = min([gca().width, gca().height])

			elif args[0] == 'auto':
				ax.xmin = ax.xmax = ax.ymin = ax.ymax = None

			elif args[0] == 'tight':
				if not ax.children:
					return
				ax.xmin, ax.xmax, ax.ymin, ax.ymax = ax.limits()

			elif (args[0] == 'center') or (args[0] == 'origin'):
				ax.axis_x_line = 'center'
				ax.axis_y_line = 'middle'

		elif isinstance(args[0], list) or isinstance(args[0], ndarray):
			gca().xmin, gca().xmax, gca().ymin, gca().ymax = args[0]


def grid(value=None):
	if value == 'off':
		gca().grid = False
	elif value == 'on':
		gca().grid = True
	else:
		gca().grid = not gca().grid


def render():
	return gcf().render()


def legend(*args, **kwargs):
	return Legend(*args, **kwargs)


def save(filename, format=None):
	gcf().save(filename, format)


def box(value=None):
	box_on = (gca().axis_x_line is None) and (gca().axis_y_line is None)
	if value == 'off' or (value is None and box_on):
		gca().axis_x_line = 'bottom'
		gca().axis_y_line = 'left'
	elif value == 'on' or (value is None and not box_on):
		gca().axis_x_line = None
		gca().axis_y_line = None


def arrow(x, y, dx, dy, arrow_style='-latex', **kwargs):
	return Arrow(x, y, dx, dy, arrow_style=arrow_style, **kwargs)



def text(x, y, text, **kwargs):
	return Text(x, y, text, **kwargs)
