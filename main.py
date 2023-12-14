import cellular_automata as ca
import matplotlib.pyplot as plt
import numpy as np

import cellpylib as cpl  # for testing

if __name__ == '__main__':
	# our implementation
	cellular_automaton = ca.CellularAutomaton(20, 20, ca.oil_spill_rule, 4)
	# cellular_automaton.draw_initial_state([(8, 10), (8, 11), (9, 10), (9, 11)])
	# cellular_automaton.draw_initial_state([(7, 9), (7, 8), (6, 9), (6, 8)])
	# cellular_automaton.draw_initial_state([(0, 0), (2, 0), (4, 0), (6, 0), (8, 0), (10, 0), (12, 0), (14, 0), (16, 0), (17, 0), (18, 0)])

	# cellular_automaton.plot()
	cellular_automaton.draw_initial_state([(10, 11), (9, 11), (11, 11)])
	cellular_automaton.evolve(5)
	cellular_automaton.plot_animate()
	# cellular_automaton.plot()

	# # library
	# cellular_automaton = cpl.init_simple2d(20, 20)
	# cellular_automaton[:, [8, 9, 10, 10], [10, 11, 9, 11]] = 1
	# cellular_automaton = cpl.evolve2d(cellular_automaton, timesteps=20, neighbourhood='Moore',
	#                                   apply_rule=cpl.game_of_life_rule, memoize='recursive')
	#
	# cpl.plot2d_animate(cellular_automaton)
