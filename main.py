import src.CellularAutomaton as ca
from src.Config import Config
import os
import matplotlib.pyplot as plt
import numpy as np

config = Config("config.json")


def game_of_life_test():
    # our implementation
    cellular_automaton = ca.CellularAutomaton(20, 20, ca.game_of_life_rule, 4)
    cellular_automaton.draw_initial_state(
        [(8, 10), (9, 11), (10, 9), (10, 11), (10, 10)])
    # cellular_automaton.plot()
    # cellular_automaton.draw_initial_state([(10, 11), (9, 11), (11, 11)])
    cellular_automaton.evolve(25)
    cellular_automaton.plot_animate(os.path.join('out', 'anim.gif'))
    # cellular_automaton.plot()


def oil_spill_test():
    cellular_automaton = ca.CellularAutomaton(1000, 1000, ca.oil_spill_rule, 10)
    # plt.figure()
    # plt.imshow(np.array([[1 if (r, c) in config.data["initial_state"] else 0 for c in range(1000)] for r in range(1000)]), 'gray')
    # plt.show()
    cellular_automaton.draw_initial_state(config.data["initial_state"])
    cellular_automaton.evolve(25)
    cellular_automaton.plot_animate(os.path.join('out', 'oil_spill.gif'))


if __name__ == '__main__':
    print(config.params)
    # game_of_life_test()
    oil_spill_test()
