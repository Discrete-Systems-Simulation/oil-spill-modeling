from typing import Union


class Particle:
    """
    Represents a single oil particle in cellular automaton
    TODO: add all necessary variables, transformations and functions consistent with mathematical model
    """
    _y: int  # row number
    _x: int  # column number
    mass: int

    def __init__(self, y: Union[int, float], x: Union[int, float], mass=5.0):
        self._y = round(y)
        self._x = round(x)
        self.mass = mass

    def get_mass(self) -> int:
        return self.mass

    def get_x(self):
        return self._x

    def set_x(self, x: Union[int, float]):
        self._x = round(x)

    def get_y(self):
        return self._y

    def set_y(self, y: Union[int, float]):
        self._y = round(y)
