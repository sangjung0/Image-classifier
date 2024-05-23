import pathlib

from program.core.dto import Image


class AutoSave:
    def __init__(self):
        self.__directory: list[pathlib.Path]

    def closed_directory(self) -> int: pass

    def make_directory_name(self) -> str: pass

    def add(self, image: Image): pass
