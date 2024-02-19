import cv2
import numpy as np

class CalcHistogram:
    def __init__(self, threshold:float = 0.1):
        self.__prevHistogram = None
        self.__threshold = threshold
        
    def isNewScene(self, img):
        histogram = cv2.calcHist([img],[0],None,[256],[0,256])
        cv2.normalize(histogram, histogram)

        if self.__prevHistogram is None:
            self.__prevHistogram = histogram
            return False
        else:
            result = cv2.compareHist(self.__prevHistogram, histogram, cv2.HISTCMP_BHATTACHARYYA)
            self.__prevHistogram = histogram
            return result > self.__threshold
    
    
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
        