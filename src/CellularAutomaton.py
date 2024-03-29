from PIL import Image
from src.Particle import Particle
from src.Cell import Cell, CellExternalVariables
from matplotlib import animation
from typing import List, Tuple
from src.Events import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from src.DataWriter import DataWriter

config = Config("config.json")


class CellularAutomaton:
    """
    Simulation board, contains Particle objects and Cells
    """
    rows: int
    cols: int
    # 3-dim: [frame, row_idx, col_idx] -> Cell
    _cells: np.ndarray
    _cell_size: int
    _cells_grid_size: int
    _fig: plt.Figure
    _ax: any
    _data_writer: DataWriter

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
                                    #    cev=CellExternalVariables(**config.data["cells"][i][j]))
                                 for j in range(cells_grid_size)] for i in range(cells_grid_size)]])
        self._fig, self._ax = plt.subplots()
        # self._ax.set_xticks([x for x in range(0, self.cols, self._cell_size)])
        # self._ax.set_yticks([x for x in range(0, self.rows, self._cell_size)])
        # self._ax.grid(color='w', linewidth=1)
        self.create_cmap()
        self._data_writer = DataWriter("out/data")

    def evolve(self, timestamps: int):
        for iteration in range(timestamps):
            if int(iteration * config.params['step'] / 3600) < 12:
                for i in range(490, 500):
                    for j in range(490, 500):
                        # if (i - 480) ** 2 + (j - 480) ** 2 <= 20 ** 2:
                        self._cells[iteration, 49, 49].add_particle(
                            Particle(i, j))
            print("Iteration:", iteration + 1)
            self._cells = np.concatenate((self._cells, self.convolution(iteration).reshape(
                1, self._cells_grid_size, self._cells_grid_size)), axis=0)
            self._data_writer.write_frame(self._cells[iteration], iteration)

    def convolution(self, iteration: int) -> np.ndarray:
        new_frame = self._cells[-1].copy()
        kernel_size = 3
        kernel_radius = kernel_size//2

        for r in range(kernel_radius, self._cells_grid_size - kernel_radius):
            for c in range(kernel_radius, self._cells_grid_size - kernel_radius):
                neighbourhood = self._cells[-1, r - kernel_radius:r + kernel_radius +
                                            1, c - kernel_radius: c + kernel_radius + 1]
                for rule in ['Advection', 'Spreading']:
                    if rule == 'Advection':
                        new_cell = Advection.apply(neighbourhood)
                        if new_cell is not None:
                            new_frame[r, c] = new_cell
                    if rule == 'Spreading':
                        new_neighbourhood = Spreading.apply(
                            neighbourhood, iteration)
                        # print("New frame:", new_frame[r - kernel_radius:r + kernel_radius + 1, c - kernel_radius: c + kernel_radius + 1], ", new neighbourhood:", new_neighbourhood)
                        new_frame[r - kernel_radius:r + kernel_radius + 1, c - kernel_radius: c + kernel_radius + 1]\
                            = new_neighbourhood
                    if rule == 'Evaporation':
                        new_cell = Evaporation.apply(
                            neighbourhood[kernel_radius, kernel_radius])
                        if new_cell is not None:
                            new_frame[r, c] = new_cell
                    neighbourhood = new_frame[r - kernel_radius:r + kernel_radius +
                                              1, c - kernel_radius: c + kernel_radius + 1]

        # Evaporation
        for r in range(kernel_radius, self._cells_grid_size - kernel_radius):
            for c in range(kernel_radius, self._cells_grid_size - kernel_radius):
                new_cell = Evaporation.apply(new_frame[r, c])
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

    def create_cmap(self):
        ncolors = 256
        color_array = plt.get_cmap('binary')(range(ncolors))
        color_array[:, -1] = np.linspace(0.0, 1.0, ncolors)
        map_object = LinearSegmentedColormap.from_list(
            name='binary_alpha', colors=color_array)
        plt.colormaps.register(cmap=map_object)

    def update_frame_cells(self, i: int) -> Tuple:
        print("Frame:", i)
        im = np.array(Image.open('out/img/map.png'))
        self._ax.axis('off')
        self._ax.set_title(
            f"Time: {int(i * config.params['step'] / 3600)}h")
        self._ax.imshow(im)
        self._ax.imshow([[cell.calculate_mass() for cell in row] for row in self._cells[i]], cmap="binary_alpha", alpha=0.8,
                        extent=(0, self.rows, self.cols, 0))
        return self._ax,

    def update_frame_particles(self, i: int) -> Tuple:
        print("Frame:", i)
        im = np.array(Image.open('out/img/map.png'))
        self._ax.axis('off')
        self._ax.set_title(
            f"Time: {int(i * config.params['step'] / 3600)}h")
        self._ax.imshow(im)
        self._ax.imshow(self.get_all_masses(i), cmap="binary_alpha", alpha=0.8,
                        extent=(0, self.rows, self.cols, 0), vmin=0.0, vmax=5.0)
        return self._ax,

    def plot_animate_cells(self, filename: str):
        self._fig, self._ax = plt.subplots()
        print("Animating cells...")
        ani = animation.FuncAnimation(
            self._fig, self.update_frame_cells, frames=self._cells.shape[0])
        writer = animation.PillowWriter(fps=2)
        ani.save(filename, writer=writer)

    def plot_animate_particles(self, filename: str):
        self._fig, self._ax = plt.subplots()
        self._ax.axis('off')
        print("Animating particles...")
        ani = animation.FuncAnimation(
            self._fig, self.update_frame_particles, frames=self._cells.shape[0])
        writer = animation.PillowWriter(fps=2)
        ani.save(filename, writer=writer)
