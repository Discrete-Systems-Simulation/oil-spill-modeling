import src.CellularAutomaton as ca
from src.Config import Config
import os

config = Config("config.json")


def oil_spill_test():
    cellular_automaton = ca.CellularAutomaton(
        config.params["particles_grid_size"],
        config.params["particles_grid_size"],
        config.params["cells_grid_size"]
    )
    cellular_automaton.evolve(10)
    cellular_automaton.plot_animate_cells(os.path.join('out', 'oil_spill_cells.gif'))
    cellular_automaton.plot_animate_particles(os.path.join('out', 'oil_spill_particles.gif'))


if __name__ == '__main__':
    oil_spill_test()
