from utils import indent
from figure import Figure
from numpy import min, max, inf

class Axis(object):
	"""
	Manages axis properties.

	@type at: tuple
	@ivar at: axis position

	@type width: float
	@ivar width: axis width

	@type height: float
	@ivar height: axis height

	@type title: string
	@ivar title: title above axis

	@type xlabel: string
	@ivar xlabel: label at the x-axis

	@type ylabel: string
	@ivar ylabel: label at the y-axis

	@type xmin: float/None
	@ivar xmin: minimum of x-axis

	@type xmax: float/None
	@ivar xmax: maximum of x-axis

	@type ymin: float/None
	@ivar ymin: minimum of y-axis

	@type ymax: float/None
	@ivar ymax: maximum of y-axis

	@type xtick: list/None
	@ivar xtick: location of ticks at x-axis

	@type ytick: list/None
	@ivar ytick: location of ticks at y-axis

	@type xticklabels: list/None
	@ivar xticklabels: labeling of ticks

	@type yticklabels: list/None
	@ivar yticklabels: labeling of ticks

	@type equal: boolean/None
	@ivar equal: forces units on all axis to have equal lengths

	@type grid: boolean/None
	@ivar grid: enables major grid

	@type axis_x_line: string/None
	@ivar axis_x_line: x-axis position, e.g. 'middle', 'top', 'bottom', 'none'

	@type axis_y_line: string/None
	@ivar axis_y_line: y-axis position, e.g. 'center', 'left', 'right', 'none'

	@type ybar: boolean
	@ivar ybar: enables bar plot (or histogram)

	@type xbar: boolean
	@ivar xbar: enables horizontal bar plot

	@type stacked: boolean
	@ivar stacked: if enabled, bar plots are stacked

	@type pgf_options: list
	@ivar pgf_options: custom PGFPlots axis options

	@type children: list
	@ivar children: list of plots contained in this axis
	"""

	_ca = None

	@staticmethod
	def gca():
		"""
		Returns the currently active axis.
		"""

		if not Axis._ca:
			Axis()
		return Axis._ca


	def __init__(self, fig=None, *args, **kwargs):
		"""
		Initializes axis properties.
		"""

		self.legend = None

		# axis position
		self.at = [0., 0.]

		# width and height of axis
		self.width = 8.
		self.height = 7.

		# parent figure
		self.figure = fig

		# plots contained in this axis
		self.children = []

		# title above this axis
		self.title = kwargs.get('title', '')

		# axis labels
		self.xlabel = kwargs.get('xlabel', '')
		self.ylabel = kwargs.get('ylabel', '')

		# axis boundaries
		self.xmin = kwargs.get('xmin', None)
		self.xmax = kwargs.get('xmax', None)
		self.ymin = kwargs.get('ymin', None)
		self.ymax = kwargs.get('ymax', None)

		# tick positions
		self.xtick = kwargs.get('xtick', None)
		self.ytick = kwargs.get('ytick', None)

		# tick labels
		self.xticklabels = kwargs.get('xticklabels', None)
		self.yticklabels = kwargs.get('yticklabels', None)

		# axis positions
		self.axis_x_line = kwargs.get('axis_x_line', None)
		self.axis_y_line = kwargs.get('axis_y_line', None)

		# bar plots
		self.ybar = kwargs.get('ybar', False)
		self.xbar = kwargs.get('xbar', False)
		self.stacked = kwargs.get('stacked', False)

		# controls aspect ratio
		self.equal = kwargs.get('equal', None)

		# grid lines
		self.grid = kwargs.get('grid', None)

		# add axis to figure
		if not self.figure:
			self.figure = Figure.gcf()
		self.figure.axes.append(self)

		# custom axis options
		self.pgf_options = kwargs.get('pgf_options', [])

		Axis._ca = self


	def render(self):
		"""
		Produces the LaTeX code for this axis.

		@rtype: string
		@return: LaTeX code for this axis
		"""

		options = [
			'at={{({0}, {1})}}'.format(self.at[0], self.at[1]),
			'scale only axis',
			'width={0}cm'.format(self.width),
			'height={0}cm'.format(self.height)]
		options.extend(self.pgf_options)

		properties = [
			'title',
			'xmin',
			'xmax',
			'ymin',
			'ymax',
			'xlabel',
			'ylabel']

		for prop in properties:
			if self.__dict__.get(prop, None) not in ['', None]:
				options.append('{0}={{{1}}}'.format(prop, self.__dict__[prop]))

		# different properties
		if self.legend:
			options.append(self.legend.render())
		if self.xlabel:
			options.append('xlabel near ticks')
		if self.ylabel:
			options.append('ylabel near ticks')
		if self.equal:
			options.append('axis equal=true')
		if self.grid:
			options.append('grid=major')

		# ticks and tick labels
		if self.xtick:
			options.append('xtick={{{0}}}'.format(
				','.join(str(t) for t in self.xtick)))
		if self.ytick:
			options.append('ytick={{{0}}}'.format(
				','.join(str(t) for t in self.ytick)))
		if self.xticklabels:
			options.append('xticklabels={{{0}}}'.format(
				','.join(str(t) for t in self.xticklabels)))
		if self.yticklabels:
			options.append('yticklabels={{{0}}}'.format(
				','.join(str(t) for t in self.yticklabels)))

		# axis positions
		if self.axis_x_line:
			options.append('axis x line={0}'.format(self.axis_x_line))
		if self.axis_y_line:
			options.append('axis y line={0}'.format(self.axis_y_line))

		# bar plots
		if self.ybar and self.stacked:
			options.append('ybar stacked')
		elif self.ybar:
			options.append('ybar')
		elif self.xbar and self.stacked:
			options.append('xbar stacked')
		elif self.xbar:
			options.append('xbar')
		if self.xbar or self.ybar:
			options.append('area legend')

		tex = '\\begin{axis}[\n' + indent(',\n'.join(options)) + ']\n'
		for child in self.children:
			tex += indent(child.render())
		tex += '\\end{axis}\n'

		return tex


	def limits():
		_xmin, _xmax = inf, -inf
		_ymin, _ymax = inf, -inf

		# find minimum and maximum of data points
		for child in self.children:
			xmin, xmax, ymin, ymax = child.limits()
			_xmin = min([_xmin, xmin])
			_xmax = max([_xmax, xmax])
			_ymin = min([_ymin, ymin])
			_ymax = max([_ymax, ymax])

		return [_xmin, _xmax, _ymin, _ymax]
