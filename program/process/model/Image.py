import numpy as np
from typing import Union
from pathlib import Path

from process.model.Face import Face 

from project_constants import IMAGE_SCALE, IMAGE_SOURCE

class Image:
    def __init__(self, img:np.ndarray, path:Path) -> None:
        self.__data = {IMAGE_SOURCE: img}
        self.__face = []
        self.__path = path

        self.__height, self.__width, _ = img.shape

    @property
    def width(self) -> int:
        return self.__width
    
    @property
    def height(self) -> int:
        return self.__height

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def face(self) -> list[Face]:
        return self.__face
    @face.setter
    def face(self, value) -> None:
        if isinstance(value, list):
            self.__face = value
        else:
            raise ValueError("face is must be list")
        
    @property
    def data(self) -> dict[Union[int, str], np.ndarray]:
        return self.__data
    @property
    def source(self) -> np.ndarray:
        return self.__data[IMAGE_SOURCE]
    
    def setImage(self, value:np.ndarray, cv2Constant = IMAGE_SCALE) -> None:
        if isinstance(value, np.ndarray):
            self.__data[cv2Constant] = value
            return
        raise Exception("value는 이미지이어야 함")

    # cv2 COLOR 상수 와야함
    def getImage(self, cv2Constant = IMAGE_SCALE) -> np.ndarray:
        if cv2Constant in self.__data:
            return self.__data[cv2Constant]
        raise Exception("이미지 변환 안됨")
    