import numpy as np
import cv2

"""
화면 전환 탐지만 넣으면 꽤 정확할 듯 하다
"""

#https://bkshin.tistory.com/entry/OpenCV-31-%EA%B4%91%ED%95%99-%ED%9D%90%EB%A6%84Optical-Flow
class LucasKanade:
    TERMCRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)

    def __init__(self, maxTrackerColor = 500, color = cv2.COLOR_BGR2GRAY):
            self.__colorAry = np.random.randint(0,255,(maxTrackerColor,3))
            self.__color = color

    @property
    def colorConstant(self):
        return self.__color

    def getTracker(self, trackerNumber = 200):
        return LucasKanade.tracker(self.__colorAry, trackerNumber)

    class tracker:
        def __init__(self, color, trackerNumber):
            self.__prevImg = None
            self.__lines = None
            self.__prevPt = None
            self.__number = trackerNumber
            self.__color = color

        def tracking(self, img, isNewScene = False, draw = False, drawFrame = None, scale = 1):
            result = []
            #if isNewScene: print("New Scene")
            if isNewScene or self.__prevPt is None or self.__prevImg is None:
                #print("재추적", np.random.randint(0,1000, (1)))
                self.__prevImg = img
                self.__prevPt = cv2.goodFeaturesToTrack(img, self.__number, 0.01, 10)
                if draw:
                    self.__lines = np.zeros_like(drawFrame)
            else:
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
                            cv2.line(self.__lines, (px, py),(nx, ny), self.__color[i].tolist(), 2)
                            cv2.circle(drawFrame, (nx, ny), 2, self.__color[i].tolist(), -1)       
                else:
                    self.__prevPt = None
                
                if draw: 
                    cv2.addWeighted(drawFrame, 1.0, self.__lines, 1.0, 0, drawFrame)
                #cntImg = cv2.add(cntImg, self.__lines)
                return result