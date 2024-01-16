from dataclasses import dataclass
from typing import List
from src.Particle import Particle
from src.Config import Config

config = Config("config.json")


@dataclass
class CellInternalVariables:
    oil_thickness: float = 0.0
    water_content: float = 1.0


@dataclass
class CellExternalVariables:  # To read from config()
    wind_speed_x: int = 10  # + -> right (m/s)
    wind_speed_y: int = 0  # + -> down (m/s)
    sea_current_speed_x: int = 1  # + -> right (m/s)
    sea_current_speed_y: int = -1  # + -> down (m/s)
    temperature: float = 15 + 273.15  # Kelvins
    is_land: bool = False


class Cell:
    """
    Cell containing oil particles, represents constitutes the physical space (eg. sea, coast)
    TODO: add all necessary variables such as CEVs and CIVs consistent with mathematical model
    """
    size: int
    y: int  # row number
    x: int  # column number
    civ: CellInternalVariables
    cev: CellExternalVariables
    particles: List[Particle]

    def __init__(self, y: int, x: int, size: int, particles=[]):
        self.size = size
        self.y = y
        self.x = x
        self.particles = particles.copy()
        config_variables = [data for data in config.data if (data['x'] - 1) * 100 == self.x and (data['y'] - 1) * 100 == self.y][0]
        self.civ = CellInternalVariables(config_variables['oil_thickness'], config_variables['water_content'])
        self.cev = CellExternalVariables(config_variables['wind_speed_x'],
                                         config_variables['wind_speed_y'],
                                         config_variables['sea_current_speed_x'],
                                         config_variables['sea_current_speed_y'],
                                         config_variables['temperature'],
                                         config_variables['is_land'],)

    def get_oil_mass(self) -> int:
        return sum([particle.mass for particle in self.particles])

    def add_particle(self, new_particle: Particle):
        # for op in self.particles:
        # if op.get_x() == new_particle.get_x() and op.get_y() == new_particle.get_y():
        #     op.mass += new_particle.mass
        #     return

        self.particles.append(new_particle)
