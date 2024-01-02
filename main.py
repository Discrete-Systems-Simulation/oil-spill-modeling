import src.CellularAutomaton as ca
from src.Config import Config
import os


if __name__ == '__main__':
	config = Config("config.cfg")
	print(config.params)
	# our implementation
	cellular_automaton = ca.CellularAutomaton(20, 20, ca.game_of_life_rule, 4)
	cellular_automaton.draw_initial_state([(8, 10), (9, 11), (10, 9), (10, 11), (10, 10)])
	# cellular_automaton.plot()
	# cellular_automaton.draw_initial_state([(10, 11), (9, 11), (11, 11)])
	cellular_automaton.evolve(25)
	cellular_automaton.plot_animate(os.path.join('out', 'anim.gif'))
	# cellular_automaton.plot()
