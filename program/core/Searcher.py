import pathlib

from core.dto import Data, Image
from core.Histogram import Histogram


class Searcher:
    """검색을 지원하는 클래스"""
    
    def __init__(self, images: Data, paths: list[pathlib.Path]):
        self.__images: Data = images
        self.__paths: list[pathlib.Path] = paths

    def search_face(self, name: int) -> list[pathlib.Path]:
        result = []
        for p in self.__paths:
            image = self.__images.get_image(p)
            if image.is_detected:
                for c in image.characters.values():
                    if c.name == name:
                        result.append(p)
                        break
        return result
        

    def search_image(self, source: Image) -> list[pathlib.Path]:
        result = []
        histogram = source.histogram
        for p in self.__paths:
            if p == source.path: result.append(p)
            image = self.__images.get_image(p)
            if image.is_detected and Histogram.compare_histograms(histogram, image.histogram):
                result.append(p)
        return result
            
        
