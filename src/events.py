import math

from src.Cell import Cell


class Advection:

    @classmethod
    def apply(cls, cell: Cell, timestamp: int):
        alpha = 1.1
        beta = 0.03
        for particle in cell.particles_inside:
            x_change = (alpha * cell.cev.sea_current_speed_horizontal + beta * cell.cev.wind_speed_horizontal) * timestamp
            particle.x += x_change
            y_change = (alpha * cell.cev.sea_current_speed_vertical + beta * cell.cev.wind_speed_vertical) * timestamp
            particle.y += y_change
        return cell

class Interaction:

    @classmethod
    def apply(cls, cell: Cell, timestamp: int, board_x: int, board_y: int):
        t1_2 = 100
        if cell.cev.is_land :
            for particle in cell.particles_inside:
                m_change = math.log(2, math.e) / t1_2 * particle.mass * timestamp
                # TODO check if mass > than minimum
        #         TODO add particle to next cell ( which is not a land )


        return cell

# etc...
