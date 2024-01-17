import json
import os


class DataWriter:
    def __init__(self, dir_: str) -> None:
        self.dir = dir_

    def write_frame(self, frame, i: int):
        with open(os.path.join(self.dir, str(i)+".json"), "w") as f:
            data = []
            for row in frame:
                for cell in row:
                    cell_data = {}
                    cell_data.update({"water_content": cell.civ.water_content})
                    # data.update({"oil_thickness": cell.civ.oil_thickness})
                    cell_data.update({"mass": cell.calculate_mass()})
                    cell_data.update({"n_particles": len(cell.particles)})
                    cell_data.update(
                        {"particles": [{"mass": part.get_mass(), "x": part.get_x(), "y": part.get_y()} for part in cell.particles]})
                    data.append(cell_data)

            json.dump(data, f)
