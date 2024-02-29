from typing import Type

from face_detector import DetectorInterface
from video.model import Section, Face
from video.logic import StopOverPointInterface

class Detector(StopOverPointInterface):
    def __init__(self, detector: Type[DetectorInterface]):
        self.__detector = detector

    def prepare(self):
        self.__detector = self.__detector()

    def processing(self, section:Section):

        detector = self.__detector
        frames = []

        for frame in section.frames:
            if frame.isDetect:
                frames.append(frame)
                detector.batch(frame.getFrame(detector.colorConstant))

        if len(frames) == 0: return section

        faceLocation = detector.detect()
        detector.clear()

        for frame, face in zip(frames, faceLocation):
            faces = []
            index = frame.index
            for f in face:
                faces.append(Face(index, f))
            frame.face = faces

        return section