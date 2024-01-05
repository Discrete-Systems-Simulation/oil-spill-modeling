import sys

from PIL import Image
from src.Particle import Particle
from src.Cell import Cell
from matplotlib import animation
from typing import Callable, List, Tuple
from src.Events import *
import matplotlib.pyplot as plt
import numpy as np


class CellularAutomaton:
    """
    Simulation board, contains Particle objects and Cells
    """
    rows: int
    cols: int
    # (neighbourhood, timestamp) -> updated Cell
    _rule: Callable[[np.ndarray, int], Cell]
    # 3-dim: [frame, row_idx, col_idx] -> Cell
    _cells: np.ndarray
    _cell_size: int
    _cells_grid_size: int
    _fig: plt.Figure
    _ax: any

    def __init__(self, rows: int, cols: int, cells_grid_size: int):
        self.rows = rows
        self.cols = cols
        # self._rule = rule
        if rows % cells_grid_size == 0 and cols % cells_grid_size == 0:
            self._cell_size = rows // cells_grid_size
        else:
            raise Exception("Incorrect number of cells")

        self._cells_grid_size = cells_grid_size
        self._cells = np.array([[[Cell(i * self._cell_size, j * self._cell_size, self._cell_size)
                                 for j in range(cells_grid_size)] for i in range(cells_grid_size)]])
        self._fig, self._ax = plt.subplots()
        self._ax.set_xticks([x for x in range(0, self.cols, self._cell_size)])
        self._ax.set_yticks([x for x in range(0, self.rows, self._cell_size)])
        self._ax.grid(color='w', linewidth=1)

    def evolve(self, timestamps: int):
        # TEMP - w sumie nie pamiętam na jakich danych wyszedł ten gif co wysłaliśmy
        self._cells[0, 4, 5].cev.sea_current_speed_horizontal = 0.9
        self._cells[0, 4, 5].cev.sea_current_speed_vertical = 0.3
        self._cells[0, 4, 6].cev.sea_current_speed_horizontal = 0.7
        self._cells[0, 4, 6].cev.sea_current_speed_vertical = 0.5
        self._cells[0, 4, 7].cev.sea_current_speed_horizontal = 0.5
        self._cells[0, 4, 7].cev.sea_current_speed_vertical = 0.6
        #
        for iteration in range(timestamps):
            for i in range(1000):
                for j in range(1000):
                    if (i - 480) ** 2 + (j - 480) ** 2 <= 20 ** 2:
                        self._cells[iteration, 4, 4].add_particle(Particle(i, j))
            print("Iteration:", iteration + 1)
            self._cells = np.concatenate((self._cells, self.convolution(iteration).reshape(1, self._cells_grid_size, self._cells_grid_size)), axis=0)

    def convolution(self, timestamp: int) -> np.ndarray:
        new_frame = self._cells[-1].copy()
        kernel_size = 3
        kernel_radius = kernel_size//2
        for r in range(kernel_radius, self._cells_grid_size - kernel_radius):
            for c in range(kernel_radius, self._cells_grid_size - kernel_radius):
                for rule in ['Advection', 'Spreading']:
                    neighbourhood = \
                        self._cells[-1, r - kernel_radius:r + kernel_radius +
                                    1, c - kernel_radius: c + kernel_radius + 1]
                    # new_cell = rule(neighbourhood, timestamp)
                    new_cell = getattr(sys.modules[__name__], rule).apply(neighbourhood)
                    # new_cell = Advection.apply(neighbourhood)

                    if new_cell is not None:
                        new_frame[r, c] = new_cell

        return new_frame

    def draw_initial_state(self, indices: List[Tuple[int, int]]):
        for r, c in indices:
            self._cells[0, r//self._cell_size, c //
                        self._cell_size].add_particle(Particle(r, c))

    def get_all_masses(self, index=-1) -> List[List[int]]:
        oil_masses = np.zeros((self.rows, self.cols), dtype=float)
        for row in self._cells[index]:
            for cell in row:
                for particle in cell.particles:
                    oil_masses[
                        particle.get_y(),
                        particle.get_x()
                    ] = particle.mass

        return oil_masses

    # def __str__(self):
    #     return '\n'.join([' | '.join([str(particle.mass) for particle in row]) for row in self.grid[-1]])

    def plot(self):
        self._ax.imshow(self.get_all_masses(), cmap="gray",
                        extent=(0, self.rows, self.cols, 0))
        plt.show()

    def animation_init(self) -> Tuple:
        im = np.array(Image.open('out/img/map.png'))
        self._ax.imshow(im)
        self._ax.imshow(self.get_all_masses(0), cmap="binary", alpha=0.3,
                        extent=(0, self.rows, self.cols, 0))
        return self._ax,

    def update_frame(self, i: int) -> Tuple:
        im = np.array(Image.open('out/img/map.png'))
        self._ax.imshow(im)
        self._ax.imshow(self.get_all_masses(i), cmap="binary", alpha=0.3,
                        extent=(0, self.rows, self.cols, 0))
        return self._ax,

    def plot_animate(self, filename: str):
        print("Animating...")
        ani = animation.FuncAnimation(self._fig, self.update_frame, init_func=self.animation_init,
                                      frames=self._cells.shape[0])
        writer = animation.PillowWriter(fps=7)
        ani.save(filename, writer=writer)


# def oil_spill_rule(neighbourhood: np.ndarray, timestamp: int) -> Cell:
#     # TODO: implement real spread rules
#
#     # etc...
#
#     return cell


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
