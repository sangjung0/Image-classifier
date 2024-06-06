import pathlib

from core.dto import Data, Image
from core.Histogram import Histogram


class Searcher:
    def __init__(self, images: Data, paths: list[pathlib.Path]):
        self.__images: Data = images
        self.__paths: list[pathlib.Path] = paths

    def search_image(self, name: int) -> list[pathlib.Path]:
        result = []
        for p in self.__paths:
            image = self.__images.get_image(p)
            for c in image.characters.values():
                if c.get_name() == name:
                    result.append(p)
                    break
        return result
        

    def search_face(self, source: Image) -> list[pathlib.Path]:
        result = []
        histogram = source.get_hash()
        for p in self.__paths:
            if p == source.get_path(): result.append(p)
            image = self.__images.get_image(p)
            if image.is_detected() and Histogram.compare_histograms(histogram, image.get_hash()):
                result.append(p)
        return result
            
        
