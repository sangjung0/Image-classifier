import pathlib
import numpy as np

from core.Searcher import Searcher
from core.dto import Data, Image


class DataController:
    
    __CACHE_SIZE = 10
    
    def __init__(self, image_path: list[pathlib.Path], sub_path: list[pathlib.Path]):
        self.__image_path: list[pathlib.Path] = image_path
        self.__cache: dict[pathlib.Path: np.ndarray]
        self.__images: Data
        self.__searcher: Searcher
        self._sub_path: list[pathlib.Path] # 뭐긴 뭐야 폴더 셋이지 ㅋ
        self._cnt_image_index:int = len(self.__image_path)-1

    def get_cnt_image(self) -> tuple[Image, np.ndarray]:
        if(self._cnt_image_index < 0): return None
        path = self.__image_path[self._cnt_image_index]
        image = self.__images.get_image(path)
        if(path in self.__cache):
            ary = self.__cache[path]
        else:
            ary = image.get_image()
            self.__cache[path] = ary                
        return image, ary

    def get_next_image(self) -> tuple[Image, np.ndarray]:
        if(self._cnt_image_index < 0): return None
        self._cnt_image_index = self.__image_index(1)
        return self.get_cnt_image()

    def get_prev_image(self) -> tuple[Image, np.ndarray]:
        if(self._cnt_image_index < 0): return None
        self._cnt_image_index = self.__image_index(-1)
        return self.get_cnt_image()

    def search_image(self) -> 'DataController': pass

    def search_face(self) -> 'DataController': pass

    def stop_search(self): pass

    def move(self, n: int): pass
    
    def __image_index(self, value:int) -> None:
        return (self._cnt_image_index + value) % len(self.__image_path)
    
    def __cache_clear(self) -> None:
        while True:
            pass
