import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


class Particle:
	"""
	Represents a single oil particle in cellular automaton
	TODO: add all necessary variables, transformations and functions consistent with mathematical model
	"""
	def __init__(self, value=0, mass=5):
		self.value = value
		self.mass = mass
		self.containing_cell = None

	def get_value(self):
		return self.value

	def __str__(self):
		return self.value


class Cell:
	"""
	Cell containing oil particles, represents constitutes the physical space (eg. sea, coast)
	TODO: add all necessary variables such as CEVs and CIVs consistent with mathematical model
	"""
	def __init__(self, x, y, size, particles_inside=None):
		self.size = size
		self.x = x
		self.y = y
		self.particles = np.array(particles_inside)

	def oil_mass(self):
		mass = 0
		for particle in self.particles.flatten():
			mass += particle.mass
		return mass


class CellularAutomaton:
	"""
	Simulation board, contains Particle objects and Cells
	"""
	def __init__(self, rows, cols, rule, n_cells):
		self.rows = rows
		self.cols = cols
		self.grid = np.full((1, rows, cols), Particle(0))
		self.rule = rule
		if rows % n_cells == 0 and cols % n_cells == 0:
			self.cell_size = rows // n_cells
		else:
			raise Exception("Incorrect number of cells")
		self.cells = np.array([[Cell(i * self.cell_size, j * self.cell_size, self.cell_size) for j in range(n_cells)] for i in range(n_cells)])
		self.update_cells()
		self.fig, self.ax = plt.subplots()
		self.ax.set_xticks([x for x in range(0, self.cols, self.cell_size)])
		self.ax.set_yticks([x for x in range(0, self.rows, self.cell_size)])
		self.ax.grid(color='w', linewidth=1)

	def update_cells(self):
		for i in range(self.rows):
			for j in range(self.cols):
				self.grid[-1][i][j].containing_cell = self.cells[(i // self.cell_size)][(j // self.cell_size)]
		for row in self.cells:
			for cell in row:
				cell.particles = [[self.grid[-1, x, y] for y in range(cell.y, cell.y + self.cell_size)]
				                  for x in range(cell.x, cell.x + self.cell_size)]

	def evolve(self, timestamps):
		for iteration in range(timestamps):
			self.grid = np.concatenate((self.grid,
			                            self.convolution(self.rule, iteration).reshape(1, self.rows, self.cols)), axis=0)
			self.update_cells()

	def convolution(self, rule, timestamp):
		out_grid = np.full_like(self.grid[-1], Particle(0))
		kernel_size = 3
		kernel_radius = kernel_size//2
		for r in range(kernel_radius, self.rows - kernel_radius):
			for c in range(kernel_radius, self.cols - kernel_radius):
				neighbourhood = \
					self.grid[-1, r - kernel_radius:r + kernel_radius + 1, c - kernel_radius: c + kernel_radius + 1]
				new_cell_value = rule(neighbourhood, timestamp)
				if new_cell_value is not None:
					out_grid[r, c] = new_cell_value
		return out_grid

	def draw_initial_state(self, indices):
		for r, c in indices:
			self.grid[0, r, c] = Particle(1)
		self.update_cells()

	def to_array(self, index=-1):
		return [[p.value for p in row] for row in self.grid[index]]

	def __str__(self):
		return '\n'.join([' | '.join([str(particle.value) for particle in row]) for row in self.grid[-1]])

	def plot(self):
		self.ax.imshow(self.to_array(), cmap="gray", extent=(0, self.rows, self.cols, 0))
		plt.show()

	def animation_init(self):
		self.ax.imshow(self.to_array(0), cmap="gray", extent=(0, self.rows, self.cols, 0))
		return (self.ax,)

	def update_frame(self, i):
		self.ax.imshow(self.to_array(i), cmap="gray", extent=(0, self.rows, self.cols, 0))
		return (self.ax,)

	def plot_animate(self):
		anim = animation.FuncAnimation(self.fig, self.update_frame, init_func=self.animation_init,
		                               frames=self.grid.shape[0])
		plt.show()


def oil_spill_rule(neighbourhood, timestamp):
	# TODO: implement real spread rules, for now it's game of life
	kernel_size = neighbourhood.shape[0]
	center_cell_val = neighbourhood[kernel_size//2][kernel_size//2].get_value()
	total = 0
	for row in neighbourhood:
		for particle in row:
			total += particle.get_value()

	if center_cell_val == 1:
		if 3 <= total <= 4:
			return Particle(1)
		else:
			return Particle(0)
	else:
		if total == 3:
			return Particle(1)
		else:
			return Particle(0)



