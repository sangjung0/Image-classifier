import numpy as np
import cv2

"""
화면 전환 탐지만 넣으면 꽤 정확할 듯 하다
"""

#https://bkshin.tistory.com/entry/OpenCV-31-%EA%B4%91%ED%95%99-%ED%9D%90%EB%A6%84Optical-Flow
class LucasKanade:
    TERMCRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    def __init__(self):
        self.__prevImg = None
        self.__lines = None
        self.__prevPt = None
        self.__color = np.random.randint(0,255,(200,3))

    def tracking(self, img, color = cv2.COLOR_BGR2GRAY, inplace=False, isNewScene=False):
        cntImg = img if inplace else img.copy()
        gray = cv2.cvtColor(cntImg, color)
        #if isNewScene: print("New Scene")
        if isNewScene or self.__prevPt is None or self.__prevImg is None:
            #print("재추적", np.random.randint(0,1000, (1)))
            self.__prevImg = gray
            self.__lines = np.zeros_like(cntImg)
            self.__prevPt = cv2.goodFeaturesToTrack(self.__prevImg, 200, 0.01, 10)
        else:
            nextPt, status, err = cv2.calcOpticalFlowPyrLK(self.__prevImg, gray, self.__prevPt, None, criteria=LucasKanade.TERMCRITERIA)
            if nextPt is not None:
                prevMv = self.__prevPt[status==1]
                nextMv = nextPt[status==1]
                for i, (p, n) in enumerate(zip(prevMv, nextMv)):
                    px, py = map(lambda x : int(x),p.ravel())
                    nx, ny = map(lambda x: int(x), n.ravel())
                    cv2.line(self.__lines, (px, py),(nx, ny), self.__color[i].tolist(), 2)
                    cv2.circle(cntImg, (nx, ny), 2, self.__color[i].tolist(), -1)       
                self.__prevPt = nextMv.reshape(-1, 1, 2)
            else:
                self.__prevPt = None
            cv2.addWeighted(cntImg, 1.0, self.__lines, 1.0, 0, cntImg)
            #cntImg = cv2.add(cntImg, self.__lines)
            self.__prevImg = gray