from typing import Type

from video.logic.StopOverPointInterface import StopOverPointInterface

from video.face_detector import DetectorInterface
from video.model import Section, Face

class Detector(StopOverPointInterface):
    def __init__(self, detector: Type[DetectorInterface], scale:int):
        self.__detector = detector
        self.__scale = scale

    def prepare(self):
        self.__detector = self.__detector()

    def processing(self, section:Section):

        detector = self.__detector
        scale = self.__scale
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
                for k in f:
                    f[k] = tuple(s * scale for s in f[k])
                faces.append(Face(index, f))
            frame.face = faces

        return section