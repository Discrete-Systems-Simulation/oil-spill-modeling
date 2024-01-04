import math
import numpy as np
from src.Cell import Cell
from src.Config import Config
import copy

config = Config("config.json")


class Advection:
    alpha = 1.1
    beta = 0.03
    timestep = config.params["step"]
    unit_length = config.params["map_size"] / \
        config.params["particles_grid_size"]  # m

    @classmethod
    def apply(cls, neighbourhood: np.ndarray) -> Cell:
        kernel_size = neighbourhood.shape[0]
        new_neighbourhood = neighbourhood.copy()
        for i, row in enumerate(neighbourhood):
            for j, cell in enumerate(row):
                cell = copy.deepcopy(cell)
                new_neighbourhood[i, j] = cls._aplly_single_cell(cell)

        center_cell = new_neighbourhood[kernel_size//2][kernel_size//2]
        cls._check_boundaries(new_neighbourhood, center_cell)
        return center_cell

    @classmethod
    def _aplly_single_cell(cls, cell: Cell) -> Cell:
        x_change = (cls.alpha * cell.cev.sea_current_speed_horizontal +
                    cls.beta * cell.cev.wind_speed_horizontal) * cls.timestep / cls.unit_length
        y_change = (cls.alpha * cell.cev.sea_current_speed_vertical +
                    cls.beta * cell.cev.wind_speed_vertical) * cls.timestep / cls.unit_length
        for particle in cell.particles:
            particle.set_x(particle.get_x() + x_change)
            particle.set_y(particle.get_y() + y_change)

        return cell

    @classmethod
    def _check_boundaries(cls, new_neighbourhood, center_cell):
        left = center_cell.x
        up = center_cell.y
        right = center_cell.x + center_cell.size
        down = center_cell.y + center_cell.size
        cls._remove_outer_particles(center_cell, left, up, right, down)
        cls._add_particles_from_neighbours(
            new_neighbourhood, center_cell, left, up, right, down)

    @classmethod
    def _add_particles_from_neighbours(cls, new_neighbourhood, center_cell, left, up, right, down):
        for row in new_neighbourhood:
            for cell in row:
                for particle in cell.particles:
                    if cell != center_cell and particle.get_x() >= left and particle.get_x() < right and particle.get_y() >= up and particle.get_y() < down:
                        center_cell.add_particle(particle)

    @classmethod
    def _remove_outer_particles(cls, center_cell, left, up, right, down):
        for particle in center_cell.particles:
            if particle.get_x() < left or particle.get_x() >= right or particle.get_y() < up or particle.get_y() >= down:
                center_cell.particles.remove(particle)


class Interaction:
    @classmethod
    def apply(cls, cell: Cell, timestamp: int, board_x: int, board_y: int):
        t1_2 = 100
        if cell.cev.is_land:
            for particle in cell.particles:
                m_change = math.log(2, math.e) / t1_2 * \
                    particle.mass * timestamp
                # TODO check if mass > than minimum
        #         TODO add particle to next cell ( which is not a land )

        return cell
