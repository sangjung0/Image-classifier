import random

from project_constants import DETECTOR_FACE, DETECTOR_NOSE,DETECTOR_RIGHT_MOUTH, DETECTOR_LEFT_EYE, DETECTOR_LEFT_MOUTH, DETECTOR_RIGHT_EYE,  DETECTOR_FRONT_FACE

class Face:
    def __init__(self, faceData:dict[str:tuple[int,int,int,int]]) -> None:
        self.__faceData = faceData
        self.__rectColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.__name = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def rectColor(self) -> tuple[int, int, int]:
        return self.__rectColor 
    @property
    def faceData(self) -> dict[str:tuple[int,int,int,int]]:
        return self.__faceData
    @property
    def face(self) -> tuple[int,int,int,int]:
        return self.__faceData[DETECTOR_FACE]
    @property
    def nose(self) -> tuple[int,int,int,int]:
        return self.__faceData.get(DETECTOR_NOSE,None)
    @property
    def lEye(self) -> tuple[int,int,int,int]:
        return self.__faceData.get(DETECTOR_LEFT_EYE, None)
    @property
    def rEye(self) -> tuple[int,int,int,int]:
        return self.__faceData.get(DETECTOR_RIGHT_EYE, None)
    @property
    def lMouth(self) -> tuple[int,int,int,int]:
        return self.__faceData.get(DETECTOR_LEFT_MOUTH, None)
    @property
    def rMouth(self) -> tuple[int,int,int,int]:
        return self.__faceData.get(DETECTOR_RIGHT_MOUTH, None)
    