import cv2
import numpy as np

#https://bkshin.tistory.com/entry/OpenCV-31-%EA%B4%91%ED%95%99-%ED%9D%90%EB%A6%84Optical-Flow
class GunnerFarneback:
    STEP = 64
    def __init__(self):
        self.__prevImg = None

    def tracking(self, img, color = cv2.COLOR_BGR2GRAY, inplace=False):
        cntImg = img if inplace else img.copy()
        gray = cv2.cvtColor(cntImg, color)
        if self.__prevImg is None:
            self.__prevImg = gray
        else:
            flow = cv2.calcOpticalFlowFarneback(self.__prevImg, gray, None, 0.5, 3, 15, 3, 5, 1.1,cv2.OPTFLOW_FARNEBACK_GAUSSIAN)

            h, w = cntImg.shape[:2]

            idx_y, idx_x = np.mgrid[GunnerFarneback.STEP/2:h:GunnerFarneback.STEP, GunnerFarneback.STEP/2:w:GunnerFarneback.STEP].astype(np.int32)
            indices = np.stack((idx_x, idx_y), axis = -1).reshape(-1,2)

            for x,y in indices:
                cv2.circle(img, (x,y), 1, (0,255,0), -1)
                dx,dy = flow[y,x].astype(np.int32)
                cv2.line(img, (x,y), (x+dx, y+dy), (0,255,0),2,cv2.LINE_AA)

            self.__prevImg = gray