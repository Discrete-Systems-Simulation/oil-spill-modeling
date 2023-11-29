
class Particle:
	"""
	Represents a single oil particle in cellular automaton
	TODO: add all necessary variables, transformations and functions consistent with mathematical model
	"""
	def __init__(self, value=0):
		self.value = value
		self.containing_cell = None

	def get_value(self):
		return self.value


class Cell:
	"""
	Cell containing oil particles, represents constitutes the physical space (eg. sea, coast)
	TODO: add all necessary variables such as CEVs and CIVs consistent with mathematical model
	"""
	def __init__(self, x, y, size):
		self.size = size
		self.x = x
		self.y = y


class CellularAutomaton:
	"""
	Simulation board, contains Particle objects and Cells
	"""
	def __init__(self, rows, cols, rule, n_cells):
		self.rows = rows
		self.cols = cols
		self.grid = [[Particle(0) for _ in range(rows)] for _ in range(cols)]
		self.rule = rule
		if rows % n_cells == 0 and cols % n_cells == 0:
			self.cell_size = rows // n_cells
		else: raise Exception("Incorrect number of cells")
		self.cells = [[Cell(i * n_cells, j * n_cells , self.cell_size) for j in range(n_cells)] for i in range(n_cells)]
		self.update_cells()

	def update_cells(self):
		for i in range(self.rows):
			for j in range(self.cols):
				self.grid[i][j].containing_cell = self.cells[i // self.cell_size][j // self.cell_size]

	def evolve(self, timestamps):
		for iteration in range(timestamps):
			self.convolution(self.rule, iteration)

	def convolution(self, rule, timestamp):
		out_grid = self.grid
		kernel_size = 3
		for r in range(kernel_size//2, self.rows - kernel_size//2):
			for c in range(kernel_size//2, self.cols - kernel_size//2):
				i, j = 0, 0
				neighbourhood = [[Particle(0) for _ in range(kernel_size)] for _ in range(kernel_size)]
				for x in range(r - kernel_size//2, r + kernel_size//2 + 1):
					for y in range(c - kernel_size // 2, c + kernel_size // 2 + 1):
						neighbourhood[i][j] = self.grid[x][y]
						i += 1
					j += 1
					i = 0

				new_cell_value = rule(neighbourhood, self.grid[r][c], timestamp)
				if new_cell_value is not None:
					out_grid[r][c] = new_cell_value
		self.grid = out_grid

	def draw_initial_state(self, indices):
		for r, c in indices:
			self.grid[r][c] = Particle(1)

	def to_array(self):
		return [[p.value for p in row] for row in self.grid]

	def __str__(self):
		return '\n'.join([' | '.join([str(cell.value) for cell in row]) for row in self.grid])


def oil_spill_rule(neighbourhood, c: Particle, timestamp):
	# TODO: implement real spread rules, for now it's game of life
	center_cell_val = neighbourhood[1][1].get_value()
	total = 0
	for row in neighbourhood:
		for cell in row:
			total += cell.get_value()
	if center_cell_val == 1:
		if (total < 2) or (total > 3):
			return Particle(0)
	else:
		if total == 3:
			return Particle(1)



