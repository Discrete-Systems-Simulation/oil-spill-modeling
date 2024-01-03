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

class Spreading:

    @classmethod
    def apply(cls, cell: Cell):
        # TODO
        return cell

# etc...
