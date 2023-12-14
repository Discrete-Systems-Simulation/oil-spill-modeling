import cellular_automata as ca


if __name__ == '__main__':
	# our implementation
	cellular_automaton = ca.CellularAutomaton(20, 20, ca.oil_spill_rule, 4)
	cellular_automaton.draw_initial_state([(8, 10), (9, 11), (10, 9), (10, 11), (10, 10)])

	# cellular_automaton.plot()
	# cellular_automaton.draw_initial_state([(10, 11), (9, 11), (11, 11)])
	cellular_automaton.evolve(25)
	cellular_automaton.plot_animate('anim.gif')
	# cellular_automaton.plot()
