import cv2
import numpy as np

from project_constants import FRAME_SCALE, FRAME_FRAME

class Frame:
    def __init__(self, index:int, frame:np.ndarray, width:int, height:int, rWidth:int, rHeight:int, scale:int, isDetect:bool, filter: object = None):
        self.__index = index
        self.__width = width
        self.__height = height
        self.__rWidth = rWidth
        self.__rHeight = rHeight
        self.__scale = scale
        self.__isDetect = isDetect
        self.__filter = filter
        self.__imgs = {FRAME_FRAME: frame}
        self.__face = []

    @property
    def face(self):
        self.__face
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
    @property
    def scale(self):
        return self.__scale

    # cv2 COLOR 상수 와야함
    def getFrame(self, cv2Constant = FRAME_SCALE) -> np.ndarray:
        if cv2Constant in self.__imgs:
            return self.__imgs[cv2Constant]
        if cv2Constant == FRAME_SCALE:
            self.__imgs[cv2Constant] = self.__filter(cv2.resize(self.frame, (self.__rWidth, self.__rHeight))) if self.__filter is not None else cv2.resize(self.frame, (self.__rWidth, self.__rHeight))
        else:
            self.__imgs[cv2Constant] = cv2.cvtColor(self.getFrame(), cv2Constant) 
        return self.__imgs[cv2Constant]
    