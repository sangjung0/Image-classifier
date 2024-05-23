import pathlib
import numpy as np

from program.core.Searcher import Searcher
from program.core.dto import Data, Image


class DataController:
    def __init__(self, image_path: list[pathlib.Path], sub_path: list[pathlib.Path]):
        self.__image_path: list[pathlib.Path]
        self.__cache: dict[pathlib.Path: np.ndarray]
        self.__images: Data
        self.__searcher: Searcher
        self._sub_path: list[pathlib.Path]
        self._cnt_image: Image

    def get_cnt_image(self) -> Image: pass

    def get_next_image(self) -> Image: pass

    def get_prev_image(self) -> Image: pass

    def search_image(self) -> 'DataController': pass

    def search_face(self) -> 'DataController': pass

    def stop_search(self): pass

    def move(self, n: int): pass
