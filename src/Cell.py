import numpy as np


class Cell:
    """
    Cell containing oil particles, represents constitutes the physical space (eg. sea, coast)
    TODO: add all necessary variables such as CEVs and CIVs consistent with mathematical model
    """
    size: int
    x: int
    y: int
    particles_inside: np.ndarray

    def __init__(self, x: int, y: int, size: int, particles_inside = np.array([])):
        self.size = size
        self.x = x
        self.y = y
        self.particles = np.array(particles_inside)

    def oil_mass(self) -> int:
        mass = 0
        for particle in self.particles.flatten():
            mass += particle.mass
        return mass
