import numpy as np
from pathlib import Path
from typing import Union

from project_constants import IMAGE_SOURCE, SCALE_EPSILON

class Image:
    def __init__(self, index:int, scale:int, path:Path, img:np.ndarray) -> None:
        self.__data = {IMAGE_SOURCE: img}
        self.__scale = scale
        self.__path = path
        self.__index = index

    @property
    def index(self) -> int:
        return self.__index

    @index.setter
    def index(self, value:int) -> None:
        self.__index = value

    @property
    def scale(self) -> float:
        return self.__scale/SCALE_EPSILON
    
    @scale.setter
    def scale(self, value:float) -> None:
        self.__scale = int(value * SCALE_EPSILON)

    @property
    def path(self) -> Path:
        return self.__path
    
    @path.setter
    def path(self, value:Path) -> None:
        self.__path = value

    @property
    def data(self) -> dict[Union[int, str], np.ndarray]:
        return self.__data
    @property
    def source(self) -> np.ndarray:
        return self.__data[IMAGE_SOURCE]
    
    def getScale(self) -> int:
        return self.__scale
    
    def setImage(self, value:np.ndarray, cv2Constant = IMAGE_SOURCE) -> None:
        if isinstance(value, np.ndarray):
            self.__data[cv2Constant] = value
            return
        raise Exception("value는 이미지이어야 함")

    # cv2 COLOR 상수 와야함
    def getImage(self, cv2Constant = IMAGE_SOURCE) -> np.ndarray:
        if cv2Constant in self.__data:
            return self.__data[cv2Constant]
        raise Exception("이미지 변환 안됨")
    