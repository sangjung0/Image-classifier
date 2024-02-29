from typing import Type
import cv2

from video.model import Section
from video.logic.StopOverPointInterface import StopOverPointInterface

class Vision(StopOverPointInterface):
    def __init__(self, filter:Type[object], width:int, height:int, scale:int, colors:set, draw:bool):
        self.__filter = filter
        self.__width = width 
        self.__height = height 
        self.__rWidth = width // scale
        self.__rHeight = height // scale
        self.__colors = colors
        self.__draw = draw

    def prepare(self) -> None:
        if self.__filter is not None: self.__filter = self.__filter()
        
    def processing(self, section:Section) -> Section:

        filter = self.__filter
        width = self.__width
        height = self.__height
        rWidth = self.__rWidth
        rHeight = self.__rHeight
        draw = self.__draw
        colors = self.__colors

        for frame in section:
            f = cv2.resize(frame.frame, (rWidth, rHeight))
            cf = filter(f) if filter is not None else f
            if draw:
                frame.frame[:] = cv2.resize(cf,(width, height))
            frame.setFrame(cf)
            for c in colors:
                frame.setFrame(cv2.cvtColor(frame.getFrame(), c), cv2Constant = c)

        return section
