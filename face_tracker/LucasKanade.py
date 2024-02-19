import numpy as np
import cv2

from face_tracker.TrackerInterface import TrackerInterface

#https://bkshin.tistory.com/entry/OpenCV-31-%EA%B4%91%ED%95%99-%ED%9D%90%EB%A6%84Optical-Flow
class LucasKanade(TrackerInterface):
    TERMCRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)

    def __init__(self, pointNumber = 300, color = cv2.COLOR_BGR2GRAY):
            super().__init__()
            self.__colorAry = np.random.randint(0,255,(pointNumber,3))
            self.__color = color
            
            self.__prevImg = None
            self.__lines = None
            self.__prevPt = None
            self.__number = pointNumber

    @property
    def colorConstant(self):
        return self.__color
    
    def clear(self):
        self.__prevImg = None
        self.__prevPt = None
        self.__lines = None

    def tracking(self, img, scale:int = 1, isNewScene:bool = False, draw:bool = False, drawFrame:np.ndarray = None):
        if isNewScene: self.clear()
        if self.__prevPt is None:
            self.__prevImg = img
            self.__prevPt = cv2.goodFeaturesToTrack(img, self.__number, 0.01, 10)
            if draw:
                self.__lines = np.zeros_like(drawFrame)
            return []
        nextPt, status, err = cv2.calcOpticalFlowPyrLK(self.__prevImg, img, self.__prevPt, None, criteria=LucasKanade.TERMCRITERIA)
        self.__prevImg = img
        if nextPt is not None:
            prevMv = self.__prevPt[status==1]
            nextMv = nextPt[status==1]
            self.__prevPt = nextMv.reshape(-1, 1, 2)
            result = zip(prevMv, nextMv)
            if draw:
                for i, (p, n) in enumerate(result):
                    px, py = map(lambda x : int(x*scale),p.ravel())
                    nx, ny = map(lambda x: int(x*scale), n.ravel())
                    cv2.line(self.__lines, (px, py),(nx, ny), self.__colorAry[i].tolist(), 2)
                    cv2.circle(drawFrame, (nx, ny), 2, self.__colorAry[i].tolist(), -1)        
                cv2.addWeighted(drawFrame, 1.0, self.__lines, 1.0, 0, drawFrame)
            return result
        self.__prevPt = None
        return []