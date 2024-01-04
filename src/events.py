import math
import numpy as np
from src.Cell import Cell
from src.Config import Config
import copy

config = Config("config.json")


class Advection:
    alpha = 1.1
    beta = 0.03

    @classmethod
    def apply(cls, neighbourhood: np.ndarray):
        kernel_size = neighbourhood.shape[0]
        cell = copy.deepcopy(neighbourhood[kernel_size//2][kernel_size//2])
        x_change = (cls.alpha * cell.cev.sea_current_speed_horizontal +
                    cls.beta * cell.cev.wind_speed_horizontal)
        y_change = (cls.alpha * cell.cev.sea_current_speed_vertical +
                    cls.beta * cell.cev.wind_speed_vertical)
        for particle in cell.particles:
            particle.set_x(particle.get_x() + x_change)
            particle.set_y(particle.get_y() + y_change)

        return cell


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
