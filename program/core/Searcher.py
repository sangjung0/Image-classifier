import pathlib

from core.dto import Data, Image


class Searcher:
    def __init__(self, images: Data):
        self.__images: Data

    def search_image(self, source: Image) -> list[pathlib.Path]: pass

    def search_face(self, source: Image) -> list[pathlib.Path]: pass
