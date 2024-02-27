import random

class Face:
    def __init__(self, frameIndex, face, nose, lEye, rEye, lMouth, rMouth):
        self.__frameIndex = frameIndex
        self.__face = face
        self.__nose = nose
        self.__lEye = lEye
        self.__rEye = rEye
        self.__lMouth = lMouth
        self.__rMouth = rMouth
        self.__rectColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.__points = []
        self.__nextFace = None

    @property
    def points(self):
        return self.__points
    @property
    def rectColor(self):
        return self.__rectColor 
    @property
    def frameIndex(self):
        return self.__frameIndex
    @property
    def face(self):
        return self.__face
    @property
    def nose(self):
        return self.__nose
    @property
    def lEye(self):
        return self.__lEye
    @property
    def rEye(self):
        return self.__rEye
    @property
    def lMouth(self):
        return self.__lMouth
    @property
    def rMouth(self):
        return self.__rMouth
    @property
    def nextFace(self):
        return self.__nextFace

    @nextFace.setter
    def nextFace(self, value):
        if self.__nextFace is not None : raise Exception("nextFace is not None")
        if isinstance(value, Face):
            self.__nextFace = value
            value.__rectColor = self.__rectColor
        else:
            raise ValueError("nextFace is must be Face")
    