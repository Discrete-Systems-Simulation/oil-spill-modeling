from typing import Tuple
import math
import numpy as np
from src.Cell import Cell
from src.Particle import Particle
from src.Config import Config
import copy
import random

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
                new_neighbourhood[i, j] = cls._apply_single_cell(cell)

        center_cell = new_neighbourhood[kernel_size//2][kernel_size//2]
        Interaction.check_boundaries(new_neighbourhood, center_cell)
        return center_cell

    @classmethod
    def _apply_single_cell(cls, cell: Cell) -> Cell:
        x_change = (cls.alpha * cell.cev.sea_current_speed_horizontal +
                    cls.beta * cell.cev.wind_speed_horizontal) * cls.timestep / cls.unit_length
        y_change = (cls.alpha * cell.cev.sea_current_speed_vertical +
                    cls.beta * cell.cev.wind_speed_vertical) * cls.timestep / cls.unit_length
        for particle in cell.particles:
            particle.set_x(particle.get_x() + x_change)
            particle.set_y(particle.get_y() + y_change)

        return cell


class Spreading:
    n = 3
    g = 9.81
    density_diff = 0.073  # kg/m^3
    kinematic_viscosity = 1.04e-6  # m^2/s
    time_step = config.params["step"]
    # terminal_thickness = 10 ** (-5)

    @classmethod
    def apply(cls, neighbourhood: np.ndarray, iteration: int) -> np.ndarray:
        kernel_size = neighbourhood.shape[0]
        new_neighbourhood = neighbourhood.copy()
        center_cell = new_neighbourhood[kernel_size // 2][kernel_size // 2]
        for i, row in enumerate(neighbourhood):
            for j, cell in enumerate(row):
                cell = copy.deepcopy(cell)
                current_cell_oil_mass = center_cell.calculate_mass()
                neigh_cell_oil_mass = cell.calculate_mass()
                d = ((0.48 / (cls.n**2)) *
                     ((((cell.civ.oil_thickness**2) * cls.g * cls.density_diff)/(cls.kinematic_viscosity**0.5))**(1/3)) *
                     (((iteration * cls.time_step) + (iteration + 1) * cls.time_step) / 2)**-0.5)

                delta_m = (0.5 * (current_cell_oil_mass - neigh_cell_oil_mass) *
                           (1 - np.exp(-2 * (d/(cell.size**2)) * cls.time_step)))
                # print("d:", d)
                # print("delta_m:", delta_m)
                if delta_m < 0:
                    if len(cell.particles) < 2:
                        continue
                    r = abs(delta_m) / neigh_cell_oil_mass
                    for particle in cell.particles:
                        if random.uniform(0, 1) < r:
                            # move to current cell
                            cell, center_cell = cls._move_particle(particle, cell, center_cell)
                            new_neighbourhood[i, j] = cell
                            new_neighbourhood[kernel_size // 2, kernel_size // 2] = center_cell
                else:
                    if len(center_cell.particles) < 2:
                        continue
                    r = abs(delta_m) / current_cell_oil_mass
                    for particle in center_cell.particles:
                        if random.uniform(0, 1) < r:
                            # move to neigh cell
                            center_cell, cell = cls._move_particle(particle, center_cell, cell)
                            new_neighbourhood[i, j] = cell
                            new_neighbourhood[kernel_size // 2, kernel_size // 2] = center_cell

        return new_neighbourhood

    @classmethod
    def _move_particle(cls, particle: Particle, source_cell: Cell, target_cell: Cell) -> Tuple[Cell, Cell]:
        # print("move!")
        source_cell_cpy = copy.deepcopy(source_cell)
        target_cell_cpy = copy.deepcopy(target_cell)

        # source_cell_cpy.particles.remove(particle)
        target_cell_cpy.add_particle(particle)

        return source_cell_cpy, target_cell_cpy


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

    @classmethod
    def check_boundaries(cls, new_neighbourhood, center_cell):
        left = center_cell.x
        up = center_cell.y
        right = center_cell.x + center_cell.size
        down = center_cell.y + center_cell.size
        cls.remove_outer_particles(center_cell, left, up, right, down)
        cls.add_particles_from_neighbours(
            new_neighbourhood, center_cell, left, up, right, down)

    @classmethod
    def add_particles_from_neighbours(cls, new_neighbourhood, center_cell, left, up, right, down):
        for row in new_neighbourhood:
            for cell in row:
                for particle in cell.particles:
                    if cell != center_cell and left <= particle.get_x() < right and up <= particle.get_y() < down:
                        center_cell.add_particle(particle)

    @classmethod
    def remove_outer_particles(cls, center_cell, left, up, right, down):
        for particle in center_cell.particles:
            if particle.get_x() < left or particle.get_x() >= right or particle.get_y() < up or particle.get_y() >= down:
                center_cell.particles.remove(particle)
