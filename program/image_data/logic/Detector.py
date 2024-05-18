from typing import Type

from image_data.logic.StopOverPointInterface import StopOverPointInterface

from image_data.face_detector import DetectorInterface
from image_data.model import Section, Face, MetaData

class Detector(StopOverPointInterface):
    def __init__(self, detector: Type[DetectorInterface]):
        self.__detector = detector

    def prepare(self):
        self.__detector = self.__detector()

    def processing(self, section:Section):

        detector = self.__detector

        for img in section:
            detector.batch(img.source)

        faceLocation = detector.detect()
        detector.clear()

        for i in range(len(section)):
            data = section.data[i]
            scale = data.scale
            section.data[i] = MetaData(
                data.index,
                data.path,
                [Face({k:tuple(s * scale for s in f[k]) for k in f}) for f in faceLocation[i]]
            )

        return section