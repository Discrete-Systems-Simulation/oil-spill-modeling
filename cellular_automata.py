
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
		# kernel = rules.generate_kernel()
		for iteration in range(timestamps):
			self.convolution(self.rule, iteration)

	def convolution(self, rule, timestamp):
		out_grid = self.grid
		kernel_size = 3
		for r in range(kernel_size//2, self.rows - kernel_size//2):
			for c in range(kernel_size//2, self.cols - kernel_size//2):
				i, j = 0, 0
				neighbourhood = [[Cell(0) for _ in range(kernel_size)] for _ in range(kernel_size)]
				for x in range(r - kernel_size//2, r + kernel_size//2 + 1):
					for y in range(c - kernel_size // 2, c + kernel_size // 2 + 1):
						neighbourhood[i][j] = self.grid[x][y]
						i += 1
					j += 1
					i = 0

				new_cell_value = rule(neighbourhood, self.grid[r][c], timestamp)
				out_grid[r][c] = new_cell_value
		self.grid = out_grid

	def draw_initial_state(self, indices):
		for r, c in indices:
			self.grid[r][c] = Cell(1)

	def __str__(self):
		return '\n'.join([' | '.join([str(cell.value) for cell in row]) for row in self.grid])


def oil_spill_rule(neighbourhood, c: Cell, timestamp):
	# TODO: implement real spread rules, for now it's game of life
	center_cell_val = neighbourhood[1][1].get_value()
	total = 0
	for row in neighbourhood:
		for cell in row:
			total += cell.get_value()
	if center_cell_val == 1:
		if total - 1 < 2:
			return Cell(0)
		if total - 1 == 2 or total - 1 == 3:
			return Cell(1)
		if total - 1 > 3:
			return Cell(0)
	else:
		if total == 3:
			return Cell(1)
		else:
			return Cell(0)



