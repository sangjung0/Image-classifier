from typing import Type

from video.model import Section
from face_tracker import TrackerInterface
from video.processor.ProcessorInterface import ProcessorInterface

class VisionProcessor(ProcessorInterface):
    def __init__(self, tracker: Type[TrackerInterface], sceneDetector: Type[object], draw:bool):
        super().__init__("VisionProcessor")
        self.__tracker = tracker
        self.__draw = draw
        self.__sceneDetector = sceneDetector

    def __prepare__(self):
        if self.__tracker is not None: self.__tracker = self.__tracker()
        if self.__sceneDetector is not None: self.__sceneDetector = self.__sceneDetector()

    def processing(self, section:Section):

        sceneDetector = self.__sceneDetector
        tracker = self.__tracker
        draw = self.__draw
        isNewScene = False

        if sceneDetector is None and tracker is None:
            return section

        for frame in section:
            if sceneDetector is not None:
                isNewScene = sceneDetector.isNewScene(frame.getFrame())
                frame.isDetect(isNewScene)
            if tracker is not None:
                trackingData = tracker.tracking(frame.getFrame(self.__tracker.colorConstant), frame.scale, isNewScene, draw, frame.frame)
            section.compress(frame)
        return section
