from src.Cell import Cell


class Particle:
    """
    Represents a single oil particle in cellular automaton
    TODO: add all necessary variables, transformations and functions consistent with mathematical model
    """
    value: int
    mass: int
    containing_cell: Cell | None

    def __init__(self, value = 0, mass = 5):
        self.value = value
        self.mass = mass
        self.containing_cell = None

    def get_value(self) -> int:
        return self.value

    def __str__(self):
        return str(self.value)
