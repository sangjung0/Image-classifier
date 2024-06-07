import cv2
import numpy as np

class Histogram:
    
    __THRESHOLD:float = 0.9
    
    @staticmethod
    def calculate_histogram(value:np.ndarray) -> None:
        hist = cv2.calcHist([value], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist
    
    @staticmethod
    def compare_histograms(hist1:np.ndarray, hist2:np.ndarray) -> bool:
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL) > Histogram.__THRESHOLD