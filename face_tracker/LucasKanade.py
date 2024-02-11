import numpy as np
import cv2

"""
화면 전환 탐지만 넣으면 꽤 정확할 듯 하다
"""

#https://bkshin.tistory.com/entry/OpenCV-31-%EA%B4%91%ED%95%99-%ED%9D%90%EB%A6%84Optical-Flow
class LucasKanade:
    TERMCRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    def __init__(self, trackerNumber = 100, scale = 1):
        self.__prevImg = None
        self.__lines = None
        self.__prevPt = None
        self.__color = np.random.randint(0,255,(trackerNumber,3))
        self.__scale = scale
        self.__number = trackerNumber

    def tracking(self, img, isNewScene = False, draw = False, drawFrame = None, color = cv2.COLOR_BGR2GRAY):
        gray = cv2.cvtColor(img, color)
        result = []
        if isNewScene: print("New Scene")
        if isNewScene or self.__prevPt is None or self.__prevImg is None:
            print("재추적", np.random.randint(0,1000, (1)))
            self.__prevImg = gray
            self.__prevPt = cv2.goodFeaturesToTrack(self.__prevImg, self.__number, 0.01, 10)
            if draw:
                self.__lines = np.zeros_like(drawFrame)
        else:
            nextPt, status, err = cv2.calcOpticalFlowPyrLK(self.__prevImg, gray, self.__prevPt, None, criteria=LucasKanade.TERMCRITERIA)
            self.__prevImg = gray
            if nextPt is not None:
                prevMv = self.__prevPt[status==1]
                nextMv = nextPt[status==1]
                self.__prevPt = nextMv.reshape(-1, 1, 2)
                result = zip(prevMv, nextMv)
                if draw:
                    for i, (p, n) in enumerate(result):
                        px, py = map(lambda x : int(x*self.__scale),p.ravel())
                        nx, ny = map(lambda x: int(x*self.__scale), n.ravel())
                        cv2.line(self.__lines, (px, py),(nx, ny), self.__color[i].tolist(), 2)
                        cv2.circle(drawFrame, (nx, ny), 2, self.__color[i].tolist(), -1)       
            else:
                self.__prevPt = None
            
            if draw: cv2.addWeighted(drawFrame, 1.0, self.__lines, 1.0, 0, drawFrame)
            #cntImg = cv2.add(cntImg, self.__lines)
            return result