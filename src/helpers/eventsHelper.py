from src.Cell import Cell


def check_boundaries(new_neighbourhood, center_cell: Cell):
    left = center_cell.x
    up = center_cell.y
    right = center_cell.x + center_cell.size - 1
    down = center_cell.y + center_cell.size - 1
    remove_outer_particles(center_cell, left, up, right, down)
    add_particles_from_neighbours(
        new_neighbourhood, center_cell, left, up, right, down)


def add_particles_from_neighbours(new_neighbourhood, center_cell, left, up, right, down):
    for row in new_neighbourhood:
        for cell in row:
            if cell != center_cell:
                for particle in cell.particles:
                    if left <= particle.get_x() <= right and up <= particle.get_y() <= down:
                        center_cell.add_particle(particle)


def remove_outer_particles(center_cell: Cell, left, up, right, down):
    particles = center_cell.particles.copy()
    for particle in center_cell.particles:
        if particle.get_x() < left or particle.get_x() > right or particle.get_y() < up or particle.get_y() > down:
            particles.remove(particle)

    center_cell.particles = particles
