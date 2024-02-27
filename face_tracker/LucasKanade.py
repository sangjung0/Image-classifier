import numpy as np
import cv2

from face_tracker.TrackerInterface import TrackerInterface

#https://bkshin.tistory.com/entry/OpenCV-31-%EA%B4%91%ED%95%99-%ED%9D%90%EB%A6%84Optical-Flow
class LucasKanade(TrackerInterface):
    TERMCRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    COLOR = cv2.COLOR_BGR2GRAY

    def __init__(self, pointNumber = 300, color = COLOR) -> None:
            super().__init__()
            self.__color = color
            
            self.__prevImg = None
            self.__prevPt = None
            self.__pointNumber = pointNumber

    @property
    def colorConstant(self) -> int:
        return self.__color
    
    @property
    def pointNumber(self) -> int:
         return self.__pointNumber
    
    def clear(self):
        self.__prevImg = None
        self.__prevPt = None

    def tracking(self, img, isNewScene:bool = False):
        if isNewScene: self.clear()
        if self.__prevPt is None:
            self.__prevImg = img
            self.__prevPt = cv2.goodFeaturesToTrack(img, self.__pointNumber, 0.01, 10)
            return None, self.__prevPt
        nextPt, status, err = cv2.calcOpticalFlowPyrLK(self.__prevImg, img, self.__prevPt, None, criteria=LucasKanade.TERMCRITERIA)
        if nextPt is None:
            return self.tracking(img, True)
        self.__prevImg = img
        prevMv = self.__prevPt[status==1]
        nextMv = nextPt[status==1]
        self.__prevPt = nextMv.reshape(-1, 1, 2)
        return prevMv, nextMv