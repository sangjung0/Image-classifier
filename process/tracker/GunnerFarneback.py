import cv2
import numpy as np

from process.tracker.TrackerInterface import TrackerInterface

#https://bkshin.tistory.com/entry/OpenCV-31-%EA%B4%91%ED%95%99-%ED%9D%90%EB%A6%84Optical-Flow
#수정 필요
class GunnerFarneback(TrackerInterface):
    def __init__(self, step:int = 64, color = cv2.COLOR_BGR2GRAY):
        self.__prevImg = None
        self.__step = step
        self.__color = color

    @property
    def colorConstant(self):
        return self.__color
    
    def clear(self):
        self.__prevImg = None

    def tracking(self, img, scale:int = 1, isNewScene:bool = False, draw:bool = False, drawFrame:np.ndarray = None):
        step = self.__step

        if isNewScene: self.clear()
        if self.__prevImg is None:
            self.__prevImg = img
            return []
        
        flow = cv2.calcOpticalFlowFarneback(self.__prevImg, img, None, 0.5, 3, 15, 3, 5, 1.1,cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
        self.__prevImg = img

        h, w = img.shape[:2]

        idx_y, idx_x = np.mgrid[step/2:h:step, step/2:w:step].astype(np.int32)
        indices = np.stack((idx_x, idx_y), axis = -1).reshape(-1,2)

        if draw:
            for x,y in indices:
                cv2.circle(drawFrame, (x*scale,y*scale), 1, (0,255,0), -1)
                dx,dy = flow[y*scale,x*scale].astype(np.int32)
                cv2.line(img, (x*scale,y*scale), ((x+dx)*scale, (y+dy)*scale), (0,255,0),2,cv2.LINE_AA)

        return [] # 수정 필요