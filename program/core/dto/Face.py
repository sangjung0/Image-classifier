import numpy as np


class Face:
    def __init__(self, name: int, image: np.ndarray):
        self.__image: np.ndarray = image 
        self.__name: int = name

    def get_image(self) -> np.ndarray:
        return self.__image

    def get_name(self) -> int:
        return self.__name