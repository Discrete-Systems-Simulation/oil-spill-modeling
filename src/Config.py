import json
from typing import Dict


class Config:
    params: Dict  # public
    data: Dict  # public

    def __init__(self, path: str) -> None:
        self._parse_config(path)

    def _parse_config(self, path: str):
        with open(path) as f:
            settings = json.load(f)

        self.params = settings["params"]
        self.data = settings["cells"]
        # self.data["initial_state"] = [tuple(value) for value in self.data["initial_state"]]
