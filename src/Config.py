import configparser
from typing import Dict


class Config:
    params: Dict  # public

    def __init__(self, path: str) -> None:
        self.params = self._parse_config(path)

    def _parse_config(self, path: str):
        configParser = configparser.RawConfigParser()
        configFilePath = path
        configParser.read(configFilePath)
        return dict(configParser.items("PARAMS"))
