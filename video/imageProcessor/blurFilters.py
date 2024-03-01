import cv2
import numpy as np

#현재 inplace 의미 없음. 수정할 것
def meanFiltering(img, inplace=False):
    if inplace:
        img = cv2.blur(img, (50,50))
        return img
    return cv2.blur(img, (50,50))

def medianFiltering(img, inplace=False):
    if inplace:
        img = cv2.medianBlur(img, 5)
        return img
    return cv2.medianBlur(img, 5)

def gaussianFiltering(img, inplace=False):
    if inplace:
        img = cv2.GaussianBlur(img, (5,5), 0)
        return img
    return cv2.GaussianBlur(img, (5,5), 0)

def bilateralFiltering(img, inplace=False):
    if inplace:
        img = cv2.bilateralFilter(img, 5, 30, 30)
        return img
    return cv2.bilateralFilter(img, 5, 30, 30)


    