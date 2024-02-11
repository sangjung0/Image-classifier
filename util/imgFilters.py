import cv2
import numpy as np

def meanFiltering(img, inplace=False):
    if inplace:
        img = cv2.blur(img, (5,5))
        return img
    return cv2.blur(img, (5,5))

def medianFiltering(img, inplace=False):
    if inplace:
        img = cv2.medianBlur(img, 5)
        return img
    return cv2.medianBlur(img, 5)

def gaussianFiltering(img, inplace=False):
    if inplace:
        img = cv2.GaussianBlur(img, (11,11), 0)
        return img
    return cv2.GaussianBlur(img, (11,11), 0)

def bilateralFiltering(img, inplace=False):
    if inplace:
        img = cv2.bilateralFilter(img, 5, 30, 30)
        return img
    return cv2.bilateralFilter(img, 5, 30, 30)


    