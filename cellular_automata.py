import rules


class Cell:
	def __init__(self, value=0):
		self.value = value

	def get_value(self):
		return self.value


class CellularAutomaton:
	def __init__(self, rows, cols, rule):
		self.rows = rows
		self.cols = cols
		self.grid = [[Cell(0) for _ in range(rows)] for _ in range(cols)]
		self.rule = rule

	def evolve(self, timestamps):
		kernel = rules.generate_kernel()
		for iteration in range(timestamps):
			self.convolution(kernel)

	def convolution(self, kernel):
		# TODO: implement
		pass

	def __str__(self):
		return '\n'.join([' | '.join([str(cell.value) for cell in row]) for row in self.grid])
