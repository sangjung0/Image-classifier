import pathlib

from program.core.dto import Data


class Storage:
    def __init__(self):
        self.__path: pathlib.Path

    def save(self, data: Data): pass

    def load(self) -> Data:
        pass

    def get_path(self) -> pathlib.Path: pass
