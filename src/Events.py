import math
import numpy as np
from src.Cell import Cell
from src.Config import Config
import copy
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
    @classmethod
    def apply(cls, neighbourhood: np.ndarray) -> Cell:
        # kernel_size = neighbourhood.shape[0]
        # new_neighbourhood = neighbourhood.copy()
        # for i, row in enumerate(neighbourhood):
        #     for j, cell in enumerate(row):
        #         cell = copy.deepcopy(cell)
        #         new_neighbourhood[i, j] = cls._apply_single_cell(cell)
        #
        # center_cell = new_neighbourhood[kernel_size // 2][kernel_size // 2]
        # Interaction.check_boundaries(new_neighbourhood, center_cell)
        # return center_cell
        pass

    # @classmethod
    # def _apply_single_cell(cls, cell: Cell) -> Cell:
    #     x_change = (cls.alpha * cell.cev.sea_current_speed_horizontal +
    #                 cls.beta * cell.cev.wind_speed_horizontal) * cls.timestep / cls.unit_length
    #     y_change = (cls.alpha * cell.cev.sea_current_speed_vertical +
    #                 cls.beta * cell.cev.wind_speed_vertical) * cls.timestep / cls.unit_length
    #     for particle in cell.particles:
    #         particle.set_x(particle.get_x() + x_change)
    #         particle.set_y(particle.get_y() + y_change)
    #
    #     return cell


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
