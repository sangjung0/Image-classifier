import cv2
import numpy as np

from core.Constant import HISTOGRAM_THRESHOLD

class Histogram:
    """이미지의 히스토그램 기반 분석 및 비교 클래스"""
    
    @staticmethod
    def calculate_histogram(value:np.ndarray) -> None:
        hist = cv2.calcHist([value], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist
    
    @staticmethod
    def compare_histograms(hist1:np.ndarray, hist2:np.ndarray) -> bool:
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL) > HISTOGRAM_THRESHOLD