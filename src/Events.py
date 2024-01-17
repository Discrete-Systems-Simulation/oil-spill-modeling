from typing import Tuple
import math
import numpy as np
from src.Cell import Cell
from src.Particle import Particle
from src.Config import Config
import copy
import random
from src.helpers.eventsHelper import check_boundaries

config = Config("config.json")


class Evaporation:
    K = 1.25e-3  # m/s
    R = 8.314  # J / (mol * K)
    T_b = 100  # K
    rho_w = 1000  # kg/m^3
    rho_o = 870  # kg/m^3
    # TODO: Rys


class Advection:
    alpha = 1.1
    beta = 0.03
    timestep = config.params["step"]  # s
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
        check_boundaries(new_neighbourhood, center_cell)
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
    particles_grid_size = config.params["particles_grid_size"]
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
        # print("move")
        source_cell_cpy = copy.deepcopy(source_cell)
        target_cell_cpy = copy.deepcopy(target_cell)

        new_particle = Particle(
            particle.get_x() + (target_cell.x - source_cell.x),
            particle.get_y() + (target_cell.y - source_cell.y),
        )
        if new_particle.get_x() > cls.particles_grid_size - 1:
            new_particle.set_x(cls.particles_grid_size - 1)
        if new_particle.get_y() > cls.particles_grid_size - 1:
            new_particle.set_y(cls.particles_grid_size - 1)

        # source_cell_cpy.particles.remove(particle)
        # for i, prt in enumerate(source_cell_cpy.particles):
        #     if prt.get_x() == particle.get_x() and prt.get_y() == particle.get_y():
        #         source_cell_cpy.particles.pop(i)

        # target_cell_cpy.add_particle(new_particle)
        added = False
        for op in target_cell_cpy.particles:
            if op.get_x() != new_particle.get_x() and op.get_y() != new_particle.get_y():
                target_cell_cpy.add_particle(new_particle)
                added = True
                break
        if not added:
            target_cell_cpy.add_particle(new_particle)

        # print("particles:")
        # for particle in target_cell_cpy.particles:
        #     print(particle.get_x(), particle.get_y())

        return source_cell_cpy, target_cell_cpy


class ShoreInteraction:
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
