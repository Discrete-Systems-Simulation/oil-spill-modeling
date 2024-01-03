from src.Particle import Particle
from src.Cell import Cell
from matplotlib import animation
from typing import Callable, List, Tuple
from src.events import Advection
import matplotlib.pyplot as plt
import numpy as np


class CellularAutomaton:
    """
    Simulation board, contains Particle objects and Cells
    """
    x_size: int
    y_size: int
    # 3-dim: [frame, row_idx, col_idx] -> Particle, TODO: convert to Cell
    grid: np.ndarray
    # (neighbourhood, timestamp) -> updated Particle, TODO: convert to Cells
    _rule: Callable[[np.ndarray, int], Particle]
    n_cells: int
    _cells: np.ndarray
    _fig: plt.Figure
    _ax: any
    timestamp: int

    def __init__(self, rows: int, cols: int, rule: Callable[[np.ndarray, int], Particle], n_cells: int, timestamp: int):
        self.x_size = rows
        self.y_size = cols
        self.grid = np.full((1, rows, cols), Particle(0))
        self._rule = rule
        if rows % n_cells == 0 and cols % n_cells == 0:
            self.cell_size = rows // n_cells
        else:
            raise Exception("Incorrect number of cells")
        self._cells = np.array([[Cell(i * self.cell_size, j * self.cell_size, self.cell_size)
                                 for j in range(n_cells)] for i in range(n_cells)])
        self.update_cells()
        self._fig, self._ax = plt.subplots()
        self._ax.set_xticks([x for x in range(0, self.y_size, self.cell_size)])
        self._ax.set_yticks([x for x in range(0, self.x_size, self.cell_size)])
        self._ax.grid(color='w', linewidth=1)
        self.timestamp = timestamp

    def update_cells(self):
        for i in range(self.x_size):
            for j in range(self.y_size):
                self.grid[-1][i][j].containing_cell = self._cells[(
                    i // self.cell_size)][(j // self.cell_size)]
        for row in self._cells:
            for cell in row:
                cell.particles = [[self.grid[-1, x, y] for y in range(cell.y, cell.y + self.cell_size)]
                                  for x in range(cell.x, cell.x + self.cell_size)]

    def evolve(self, timestamps: int):
        for iteration in range(timestamps):
            self.grid = np.concatenate((self.grid,
                                        self.convolution(self._rule, iteration).reshape(1, self.x_size, self.y_size)), axis=0)
            self.update_cells()

    def convolution(self, rule: Callable[[np.ndarray, int], Particle], timestamp: int) -> np.ndarray:
        out_grid = np.full_like(self.grid[-1], Particle(0))
        kernel_size = 3
        kernel_radius = kernel_size//2
        for r in range(kernel_radius, self.x_size - kernel_radius):
            for c in range(kernel_radius, self.y_size - kernel_radius):
                neighbourhood = \
                    self.grid[-1, r - kernel_radius:r + kernel_radius +
                              1, c - kernel_radius: c + kernel_radius + 1]
                new_cell_value = rule(neighbourhood, timestamp)
                if new_cell_value is not None:
                    out_grid[r, c] = new_cell_value
        return out_grid

    def draw_initial_state(self, indices: List[Tuple[int, int]]):
        for r, c in indices:
            self.grid[0, r, c] = Particle(1)
        self.update_cells()

    def to_list(self, index=-1) -> List[List[Particle]]:
        return self.grid[index].tolist()

    def get_all_masses(self, index=-1) -> List[List[int]]:
        return [[particle.mass for particle in row] for row in self.grid[index]]

    def __str__(self):
        return '\n'.join([' | '.join([str(particle.mass) for particle in row]) for row in self.grid[-1]])

    def plot(self):
        self._ax.imshow(self.get_all_masses(), cmap="gray",
                        extent=(0, self.x_size, self.y_size, 0))
        plt.show()

    def animation_init(self) -> Tuple:
        self._ax.imshow(self.get_all_masses(0), cmap="gray",
                        extent=(0, self.x_size, self.y_size, 0))
        return (self._ax,)

    def update_frame(self, i: int) -> Tuple:
        self._ax.imshow(self.get_all_masses(i), cmap="gray",
                        extent=(0, self.x_size, self.y_size, 0))
        return (self._ax,)

    def plot_animate(self, filename: str):
        ani = animation.FuncAnimation(self._fig, self.update_frame, init_func=self.animation_init,
                                      frames=self.grid.shape[0])
        writer = animation.PillowWriter(fps=15)
        ani.save(filename, writer=writer)


def oil_spill_rule(neighbourhood: np.ndarray, timestamp: int) -> Cell:
    kernel_size = neighbourhood.shape[0]
    cell = neighbourhood[kernel_size//2][kernel_size//2].get_mass()
    # TODO: implement real spread rules
    cell = Advection.apply(cell, timestamp)
    # etc...

    return cell


def game_of_life_rule(neighbourhood: np.ndarray, timestamp: int) -> Particle:
    kernel_size = neighbourhood.shape[0]
    center_cell_val = neighbourhood[kernel_size//2][kernel_size//2].get_mass()
    total = 0
    for row in neighbourhood:
        for particle in row:
            total += particle.get_mass()

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
