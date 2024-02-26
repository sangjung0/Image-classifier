from typing import Type
import cv2

from video.model import Section
from video.processor.ProcessorInterface import ProcessorInterface

class VisionProcessor(ProcessorInterface):
    def __init__(self, filter:Type[object], sceneDetector: Type[object], width:int, height:int, scale:int, colors:set, draw:bool):
        super().__init__("VisionProcessor")
        self.__filter = filter
        self.__sceneDetector = sceneDetector
        self.__width = width // scale
        self.__height = height // scale
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
        draw = self.__draw
        colors = self.__colors

        for frame in section:
            f = frame.frame
            if draw:
                cf = filter(f) if filter is not None else f
                f[:] = cf
                frame.setFrame(cv2.resize(cf,(width, height)))
            else: frame.setFrame(filter(cv2.resize(f, (width, height))) if filter is not None else cv2.resize(f,width,height))
            for c in colors:
                frame.setFrame(cv2.cvtColor(frame.getFrame(), c), cv2Constant = c)
            if sceneDetector is not None:
                isNewScene = sceneDetector.isNewScene(frame.getFrame())
                if isNewScene : frame.isDetect = isNewScene
                frame.isNewScene = isNewScene
            section.compress(frame)

        return section
