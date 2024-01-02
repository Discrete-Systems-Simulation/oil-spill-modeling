class Particle:
    """
    Represents a single oil particle in cellular automaton
    TODO: add all necessary variables, transformations and functions consistent with mathematical model
    """
    mass: int
    x: int
    y: int

    def __init__(self, mass, x = 0, y = 0):
        self.mass = mass
        self.x = x
        self.y = y

    def get_mass(self) -> int:
        return self.mass
