import numpy as np


class Face:
    """
    얼굴의 이름 번호와 이미지 데이터를 가지고 있음
    """
    def __init__(self, name: int, image: np.ndarray):
        self.__image: np.ndarray = image 
        self.__name: int = name

    def get_image(self) -> np.ndarray:
        return self.__image

    def get_name(self) -> int:
        return self.__name