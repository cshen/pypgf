from axis import Axis
from figure import Figure
from settings import Settings
from legend import Legend
from plot import Plot
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

	# if arguments contain multiple rows, create multiple plots
	if (len(args) > 1) and (args[1].shape[0] > 1) and (args[0].shape[0] == 1):
		return [plot(args[0], *[arg[i] for arg in args[1:]], **kwargs)
			for i in range(len(args[0]))]

	elif (len(args) > 0) and (args[0].shape[0] > 1):
		return [plot(*[arg[i] for arg in args], **kwargs)
			for i in range(len(args[0]))]

	return Plot(*args, **kwargs)


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

				ax.xmin, ax.xmax = inf, -inf
				ax.ymin, ax.ymax = inf, -inf

				# find minimum and maximum of data points
				for child in ax.children:
					xmin, xmax, ymin, ymax = child.limits()
					ax.xmin = min([ax.xmin, xmin])
					ax.xmax = max([ax.xmax, xmax])
					ax.ymin = min([ax.ymin, ymin])
					ax.ymax = max([ax.ymax, ymax])

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
