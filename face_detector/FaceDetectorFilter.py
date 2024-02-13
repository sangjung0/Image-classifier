import cv2
import numpy as np
from project_constants import FACE, NOSE, MOUTH, EYE
from face_detector.FaceDetector import FaceDetector

class FaceDetectorFilter(FaceDetector):
    __COLORS = {
        FACE : (255, 0, 0),
        NOSE : (0, 255, 0),
        MOUTH : (0, 0, 255),
        EYE : (255,255,0)
    }
    __WEIGHT = {
        FACE : 3,
        NOSE : 3,
        MOUTH : 3,
        EYE : 3
    }

    def __init__(self, detector):
        self.__detector = detector

    @property
    def colorConstant(self):
        return self.__detector.colorConstant

    # if draw == True then need drawFrame and scale, drawFrame is original frame 
    def detect(self, img, draw = False, drawFrame = None, scale = None):
        faceLocation = []
        for kind, lx, ly, rx, ry in self.__detector.detect(img):
            if kind == FACE:
                faceLocation.append([lx,ly,rx,ry])
            if draw:
                cv2.rectangle(
                    drawFrame, 
                    (lx*scale, ly*scale), (rx*scale, ry*scale), 
                    FaceDetectorFilter.__COLORS[kind], FaceDetectorFilter.__WEIGHT[kind]
                    )
        return faceLocation
