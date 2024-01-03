from dataclasses import dataclass
from typing import List
from src.Particle import Particle


@dataclass
class CellInternalVariables:
    oil_thickness: float = 0.0
    water_content: float = 1.0


@dataclass
class CellExternalVariables:
    wind_speed_horizontal: int = 0  # + -> right (units/step)
    wind_speed_vertical: int = 0  # + -> down (units/step)
    sea_current_speed_horizontal: int = 0  # + -> right (units/step)
    sea_current_speed_vertical: int = 0  # + -> down (units/step)
    temperature: float = 15 + 273.15  # Kelwins
    is_land: bool = False


class Cell:
    """
    Cell containing oil particles, represents constitutes the physical space (eg. sea, coast)
    TODO: add all necessary variables such as CEVs and CIVs consistent with mathematical model
    """
    size: int
    x: int
    y: int
    civ: CellInternalVariables
    cev: CellExternalVariables
    particles: List[Particle]

    def __init__(self, x: int, y: int, size: int, civ=CellInternalVariables(), cev=CellExternalVariables(), particles=[]):
        self.size = size
        self.x = x
        self.y = y
        self.particles = particles
        self.civ = civ
        self.cev = cev

    def get_oil_mass(self) -> int:
        return sum([particle.mass for particle in self.particles])
