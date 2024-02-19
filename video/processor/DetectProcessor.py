from typing import Type

from video.model import Section
from face_detector import DetectorInterface
from video.processor.ProcessorInterface import ProcessorInterface

class DetectProcessor(ProcessorInterface):
    def __init__(self, detector: Type[DetectorInterface], draw:bool):
        super().__init__("DetectProcessor")
        self.__detector = detector
        self.__draw = draw

    def __prepare__(self):
        if self.__detector is not None: self.__detector = self.__detector()

    def processing(self, section:Section):

        detector = self.__detector
        draw = self.__draw

        for frame in section.frames:
            if frame.isDetect and detector is not None:
                section.deCompress(frame)
                faceLocation = self.__detector.extract(frame.getFrame(detector.colorConstant), draw, frame.frame, frame.scale)
                section.compress(frame)
        return section