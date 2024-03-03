import random

from video.model.Name import Name

from project_constants import DETECTOR_FACE, DETECTOR_NOSE,DETECTOR_RIGHT_MOUTH, DETECTOR_LEFT_EYE, DETECTOR_LEFT_MOUTH, DETECTOR_RIGHT_EYE,  DETECTOR_FRONT_FACE

class Face:
    def __init__(self, frameIndex, faceData):
        self.__frameIndex = frameIndex
        self.__faceData = faceData
        self.__rectColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.__points = []
        self.__nextFace = None
        self.__name = Name()

    @property
    def name(self):
        return self.__name.get()

    @property
    def points(self):
        return self.__points
    @points.setter
    def points(self, value):
        if isinstance(value, list):
            self.__points = value
        else:
            raise ValueError("points is must be list")
    @property
    def rectColor(self):
        return self.__rectColor 
    @property
    def frameIndex(self):
        return self.__frameIndex
    @property
    def faceData(self):
        return self.__faceData
    @property
    def face(self):
        return self.__faceData[DETECTOR_FACE]
    @property
    def nose(self):
        return self.__faceData.get(DETECTOR_NOSE,None)
    @property
    def lEye(self):
        return self.__faceData.get(DETECTOR_LEFT_EYE, None)
    @property
    def rEye(self):
        return self.__faceData.get(DETECTOR_RIGHT_EYE, None)
    @property
    def lMouth(self):
        return self.__faceData.get(DETECTOR_LEFT_MOUTH, None)
    @property
    def rMouth(self):
        return self.__faceData.get(DETECTOR_RIGHT_MOUTH, None)
    @property
    def nextFace(self):
        return self.__nextFace

    @nextFace.setter
    def nextFace(self, value):
        if self.__nextFace is not None : raise Exception("nextFace is not None")
        if isinstance(value, Face):
            self.__nextFace = value
            value.__rectColor = self.__rectColor
            value.__name = self.__name
        else:
            raise ValueError("nextFace is must be Face")
    