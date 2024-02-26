from typing import Type
import cv2

from video.model import Section
from video.processor.ProcessorInterface import ProcessorInterface

class VisionProcessor(ProcessorInterface):
    def __init__(self, filter:Type[object], sceneDetector: Type[object], width:int, height:int, scale:int, colors:set, draw:bool):
        super().__init__("VisionProcessor")
        self.__filter = filter
        self.__sceneDetector = sceneDetector
        self.__width = width 
        self.__height = height 
        self.__rWidth = width // scale
        self.__rHeight = height // scale
        self.__colors = colors
        self.__draw = draw

    def __prepare__(self):
        if self.__filter is not None: self.__filter = self.__filter()
        if self.__sceneDetector is not None: self.__sceneDetector = self.__sceneDetector()
        
    def processing(self, section:Section):

        filter = self.__filter
        sceneDetector = self.__sceneDetector
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
            if sceneDetector is not None:
                isNewScene = sceneDetector.isNewScene(frame.getFrame())
                if isNewScene : frame.isDetect = isNewScene
                frame.isNewScene = isNewScene
            section.compress(frame)

        return section
