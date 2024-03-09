import numpy as np

from project_constants import FRAME_SCALE, FRAME_FRAME

class Frame:
    def __init__(self, index:int, frame:np.ndarray, isDetect:bool, isNewScene:bool = False):
        self.__index = index
        self.__isDetect = isDetect
        self.__imgs = {FRAME_FRAME: frame}
        self.__face = []
        self.__points = (None, None)
        self.__isNewScene = isNewScene

    @property
    def points(self):
        return self.__points
    @points.setter
    def points(self, value):
        if isinstance(value, tuple):
            self.__points = value
        else:
            raise ValueError("points is must be list")

    @property
    def isNewScene(self):
        return self.__isNewScene
    @isNewScene.setter
    def isNewScene(self, value):
        if isinstance(value, bool):
            self.__isNewScene = value
        else:
            raise ValueError("isNewScene is must be bool")

    @property
    def face(self):
        return self.__face
    @face.setter
    def face(self, value):
        if isinstance(value, list):
            self.__face = value
        else:
            raise ValueError("face is must be list")
    @property
    def imgs(self):
        return self.__imgs
    @property
    def frame(self):
        return self.__imgs[FRAME_FRAME]
    @property
    def index(self):
        return self.__index
    @property
    def isDetect(self):
        return self.__isDetect
    @isDetect.setter
    def isDetect(self, value):
        if isinstance(value, bool):
            self.__isDetect = value
        else:
            raise ValueError("isDetect is must be bool")
        
    def setFrame(self, value:np.ndarray, cv2Constant = FRAME_SCALE) -> None:
        if isinstance(value, np.ndarray):
            self.__imgs[cv2Constant] = value
            return
        raise Exception("value는 이미지이어야 함")

    # cv2 COLOR 상수 와야함
    def getFrame(self, cv2Constant = FRAME_SCALE) -> np.ndarray:
        if cv2Constant in self.__imgs:
            return self.__imgs[cv2Constant]
        raise Exception("이미지 변환 안됨")
    