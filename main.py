import src.CellularAutomaton as ca
from src.Config import Config
import os
import matplotlib.pyplot as plt
import numpy as np

config = Config("config.json")


def oil_spill_test():
    cellular_automaton = ca.CellularAutomaton(
        config.params["particles_grid_size"],
        config.params["particles_grid_size"],
        config.params["cells_grid_size"]
    )
    cellular_automaton.evolve(30)
    cellular_automaton.plot_animate(os.path.join('out', 'oil_spill.gif'))


if __name__ == '__main__':
    oil_spill_test()
