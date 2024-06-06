import pathlib
import numpy as np

from core.dto import Face, Character


class PacketData:
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.image = None
        self.histogram = None
        self.cale = 1
        self.faces: dict[int: Face] = {}
        self.characters: dict[int: Character] = {}
        
    @property
    def image(self) -> np.ndarray | bytes:
        return self.__image
    @image.setter
    def image(self, value:np.ndarray | bytes):
        if isinstance(value, (np.ndarray, bytes, type(None))):
            self.__image = value
        else: raise TypeError()

    @property
    def path(self) -> pathlib.Path:
        return self.__path
    @path.setter
    def path(self, value: pathlib.Path):
        if isinstance(value, pathlib.Path):
            self.__path = value
        else: raise TypeError()

    @property
    def histogram(self) -> np.ndarray:
        return self.__histogram
    @histogram.setter
    def histogram(self, value:np.ndarray) -> None:
        if isinstance(value, (np.ndarray, type(None))):
            self.__histogram = value
        else: raise TypeError()
        
    @property
    def scale(self) -> float:
        return self.__scale
    @scale.setter
    def scale(self, value:float) -> None:
        if isinstance(value, float):
            self.__scale = value
        else: raise TypeError()
