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
        if self.__detector is None: return section

        detector = self.__detector
        draw = self.__draw
        frames = []

        for frame in section.frames:
            if frame.isDetect:
                section.deCompress(frame)
                frames.append(frame)
                detector.batch(frame.getFrame(detector.colorConstant))

        if len(frames) == 0: return section

        faceLocation = detector.extract(draw, [frame.frame for frame in frames], [frame.scale for frame in frames])
        detector.clear()

        for frame in frames:
            section.compress(frame)

        return section