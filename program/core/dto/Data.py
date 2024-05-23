import pathlib

from program.core.dto.Face import Face
from program.core.dto.Image import Image


class Data:
    def __init__(self):
        self.__image: dict[pathlib.Path: Image]
        self.__name: dict[int: str]
        self.__faces: dict[int:list[Face]]

    def __call__(self): pass

    def get_image(self, path: pathlib.Path) -> Image: pass

    def get_name(self, name: int) -> str: pass

    def get_face(self, n: int) -> list[Face]: pass

    def set_face(self, n: int, face: Face): pass

    def set_images(self, images: list[Image]): pass
