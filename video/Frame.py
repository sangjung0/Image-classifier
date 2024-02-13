import cv2
import numpy as np

class Frame:
    def __init__(self, index:int, frame:np.ndarray, width:int, height:int, rWidth:int, rHeight:int, scale:int, isDetect:bool, filter = None):
        self.__frame = frame
        self.__index = index
        self.__width = width
        self.__height = height
        self.__rWidth = rWidth
        self.__rHeight = rHeight
        self.__scale = scale
        self.__isDetect = isDetect
        self.__filter = filter
        self.__imgs = {}

    @property
    def frame(self):
        return self.__frame
    @property
    def index(self):
        return self.__index
    @property
    def isDetect(self):
        return self.__isDetect
    @property
    def scale(self):
        return self.__scale

    # cv2 COLOR 상수 와야함
    def getFrame(self, cv2Constant = 'scale'):
        if cv2Constant in self.__imgs:
            return self.__imgs[cv2Constant]
        if cv2Constant == 'scale':
            self.__imgs[cv2Constant] = self.__filter(cv2.resize(self.frame, (self.__rWidth, self.__rHeight))) if self.__filter is not None else cv2.resize(self.frame, (self.__rWidth, self.__rHeight))
        else:
            self.__imgs[cv2Constant] = self.__filter(cv2.cvtColor(self.getFrame(), cv2Constant)) if self.__filter is not None else cv2.cvtColor(self.getFrame(), cv2Constant) 
        return self.__imgs[cv2Constant]

    
    