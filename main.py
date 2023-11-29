import cellular_automata as ca
import matplotlib.pyplot as plt

import cellpylib as cpl  # for testing

if __name__ == '__main__':
	# our implementation
	cellular_automaton = ca.CellularAutomaton(20, 20, ca.oil_spill_rule, 4)
	cellular_automaton.draw_initial_state([(8, 10), (9, 11), (10, 9), (10, 11)])

	cellular_automaton.evolve(20)

	plt.imshow(cellular_automaton.to_array(), cmap="gray")
	plt.show()
	print(cellular_automaton)

	# library
	cellular_automaton = cpl.init_simple2d(20, 20)
	cellular_automaton[:, [8, 9, 10, 10], [10, 11, 9, 11]] = 1
	cellular_automaton = cpl.evolve2d(cellular_automaton, timesteps=20, neighbourhood='Moore',
	                                  apply_rule=cpl.game_of_life_rule, memoize='recursive')

	cpl.plot2d_animate(cellular_automaton)
