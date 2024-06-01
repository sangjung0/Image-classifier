import pathlib
import numpy as np

from core.Searcher import Searcher
from core.dto import Data, Image


class DataController:
    def __init__(self, image_path: list[pathlib.Path], sub_path: list[pathlib.Path]):
        self.__image_path: list[pathlib.Path] = image_path
        self.__cache: dict[pathlib.Path: np.ndarray]
        self.__images: Data
        self.__searcher: Searcher
        self._sub_path: list[pathlib.Path] # 이거 뭐지
        self._cnt_image_index:int = len(self.__image_path)-1

    def get_cnt_image(self) -> Image:
        if(self._cnt_image_index < 0): return None
        return self.__images.get_image(self.__image_path[self._cnt_image_index])        

    def get_next_image(self) -> Image:
        if(self._cnt_image_index < 0): return None
        self._cnt_image_index = (self._cnt_image_index + 1) % len(self.__image_path)
        return self.__images.get_image(self.__image_path[self._cnt_image_index])

    def get_prev_image(self) -> Image:
        if(self._cnt_image_index < 0): return None
        self._cnt_image_index = (self._cnt_image_index - 1 + len(self.__image_path)) % len(self.__image_path)
        return self.__images.get_image(self.__image_path[self._cnt_image_index])

    def search_image(self) -> 'DataController': pass

    def search_face(self) -> 'DataController': pass

    def stop_search(self): pass

    def move(self, n: int): pass
