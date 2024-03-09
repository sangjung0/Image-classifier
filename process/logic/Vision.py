from typing import Type
import cv2

from process.logic.StopOverPointInterface import StopOverPointInterface

from process.model import Section

class Vision(StopOverPointInterface):
    def __init__(self, filter:Type[object], scale:int, colors:set, draw:bool):
        self.__filter = filter
        self.__scale = scale
        self.__colors = colors
        self.__draw = draw

    def prepare(self) -> None:
        if self.__filter is not None: self.__filter = self.__filter()
        
    def processing(self, section:Section) -> Section:

        filter = self.__filter
        scale = self.__scale
        draw = self.__draw
        colors = self.__colors

        for img in section:
            f = cv2.resize(img.source, (img.width // scale, img.height // scale))
            cf = filter(f) if filter is not None else f
            if draw:
                img.source[:] = cv2.resize(cf,(img.width, img.height))
            img.setImage(cf)
            for c in colors:
                img.setImage(cv2.cvtColor(img.getImage(), c), c)

        return section
