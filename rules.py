# def oil_spill_rule(neighbourhood, c: Cell, timestamp):
# 	# TODO: implement real spread rules, for now it's game of life
# 	center_cell_val = neighbourhood[1][1].get_value()
# 	total = 0
# 	for cell in neighbourhood:
# 		total += cell.get_value()
# 	if center_cell_val == 1:
# 		if total - 1 < 2:
# 			return Cell(0)
# 		if total - 1 == 2 or total - 1 == 3:
# 			return Cell(1)
# 		if total - 1 > 3:
# 			return Cell(0)
# 	else:
# 		if total == 3:
# 			return Cell(1)
# 		else:
# 			return Cell(0)


def generate_kernel():
	# TODO: implement kernel that will go over the whole grid and change the cell states based on rules
	pass
