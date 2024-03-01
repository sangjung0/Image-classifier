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
        