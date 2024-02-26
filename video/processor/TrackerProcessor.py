from typing import Type

from video.model import Section
from face_tracker import TrackerInterface
from video.processor.ProcessorInterface import ProcessorInterface

class TrackerProcessor(ProcessorInterface):
    def __init__(self, tracker: Type[TrackerInterface], scale:int, draw:bool):
        super().__init__("TrackerProcessor")
        self.__tracker = tracker
        self.__draw = draw
        self.__scale = scale

    def __prepare__(self):
        if self.__tracker is not None: self.__tracker = self.__tracker()

    def processing(self, section:Section):
        tracker = self.__tracker
        draw = self.__draw
        scale = self.__scale

        if tracker is None: return section

        for frame in section:
            trackingData = tracker.tracking(frame.getFrame(tracker.colorConstant), scale, frame.isNewScene, draw, frame.frame)
            section.compress(frame)
        return section

