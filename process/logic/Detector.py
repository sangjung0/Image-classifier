from typing import Type

from process.logic.StopOverPointInterface import StopOverPointInterface

from process.face_detector import DetectorInterface
from process.model import Section, Face

class Detector(StopOverPointInterface):
    def __init__(self, detector: Type[DetectorInterface], scale:int):
        self.__detector = detector
        self.__scale = scale

    def prepare(self):
        self.__detector = self.__detector()

    def processing(self, section:Section):

        detector = self.__detector
        scale = self.__scale

        for img in section:
            detector.batch(img.getImage(detector.colorConstant))

        faceLocation = detector.detect()
        detector.clear()

        for img, face in zip(section, faceLocation):
            faces = []
            for f in face:
                for k in f:
                    f[k] = tuple(s * scale for s in f[k])
                faces.append(Face(f))
            img.face = faces

        return section