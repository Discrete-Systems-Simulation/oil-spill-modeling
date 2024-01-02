import numpy as np
from dataclasses import dataclass


@dataclass
class CellInternalVariables:
    oil_thickness: float = 0.0
    water_content: float = 1.0


@dataclass
class CellExternalVariables:
    wind_speed_horizontal: int = 0  # + -> right (units/step)
    wind_speed_vertical: int = 0  # + -> down (units/step)
    sea_current_speed_horizontal: int = 0  # + -> right (units/step)
    sea_current_speed_vertical: int = 0  # + -> right (units/step)
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
    particles_inside: np.ndarray

    def __init__(self, x: int, y: int, size: int, civ=CellInternalVariables(), cev=CellExternalVariables(), particles_inside=np.array([])):
        self.size = size
        self.x = x
        self.y = y
        self.particles = np.array(particles_inside)
        self.civ = civ
        self.cev = cev

    def oil_mass(self) -> int:
        mass = 0
        for particle in self.particles.flatten():
            mass += particle.mass
        return mass
