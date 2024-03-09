import cv2
import numpy as np
    
class CalcEdge:
    def __init__(self, threshold:float=1.25) -> None:
        self.__prevEdge = None
        self.__threshold = threshold

    def isNewScene(self, img, color = cv2.COLOR_BGR2GRAY):
        edge = cv2.Canny(cv2.cvtColor(img, color), 50, 150)
        if self.__prevEdge is None:
            self.__prevEdge = edge
            return False
        else:
            diff = cv2.absdiff(self.__prevEdge, edge)
            result = np.sum(diff) / np.sum(self.__prevEdge)
            self.__prevEdge = edge
            return result > self.__threshold
        