from dataclasses import dataclass
from typing import List
from src.Particle import Particle


@dataclass
class CellInternalVariables:
    oil_thickness: float = 0.0
    water_content: float = 1.0


@dataclass
class CellExternalVariables: # To read from config()
    wind_speed_horizontal: int = 20  # + -> right (m/s)
    wind_speed_vertical: int = 0  # + -> down (m/s)
    sea_current_speed_horizontal: int = 0  # + -> right (m/s)
    sea_current_speed_vertical: int = -1  # + -> down (m/s)
    temperature: float = 15 + 273.15  # Kelwins
    is_land: bool = False


class Cell:
    """
    Cell containing oil particles, represents constitutes the physical space (eg. sea, coast)
    TODO: add all necessary variables such as CEVs and CIVs consistent with mathematical model
    """
    size: int
    y: int # row number
    x: int # column number
    civ: CellInternalVariables
    cev: CellExternalVariables
    particles: List[Particle]

    def __init__(self, y: int, x: int, size: int, civ=CellInternalVariables(), cev=CellExternalVariables(), particles=[]):
        self.size = size
        self.y = y
        self.x = x
        self.particles = particles.copy()
        self.civ = civ
        self.cev = cev

    def get_oil_mass(self) -> int:
        return sum([particle.mass for particle in self.particles])
    
    #TODO: function to merge particles at the same place
