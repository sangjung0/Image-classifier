import numpy as np


class Face:
    def __init__(self, name: int, image: np.ndarray):
        self.__image: np.ndarray
        self.__name: int

    def get_image(self) -> np.ndarray:
        pass

    def get_name(self) -> int:
        pass