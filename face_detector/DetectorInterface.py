import cv2
import numpy as np
from abc import ABC, abstractmethod

from project_constants import DETECTOR_FACE, DETECTOR_NOSE, DETECTOR_MOUTH, DETECTOR_EYE

class DetectorInterface(ABC):
    __COLORS = {
        DETECTOR_FACE : (255, 0, 0),
        DETECTOR_NOSE : (0, 255, 0),
        DETECTOR_MOUTH : (0, 0, 255),
        DETECTOR_EYE : (255,255,0)
    }
    __WEIGHT = {
        DETECTOR_FACE : 3,
        DETECTOR_NOSE : 3,
        DETECTOR_MOUTH : 3,
        DETECTOR_EYE : 3
    }

    @property
    @abstractmethod
    def colorConstant(self) -> int: pass

    @abstractmethod
    def detect(self, img:np.ndarray) -> list: pass

    # if draw == True then need drawFrame and scale, drawFrame is original frame 
    def extract(self, location, draw, drawFrame, scale):
        faceLocation = []
        for kind, lx, ly, rx, ry in location:
            if kind == DETECTOR_FACE:
                faceLocation.append([lx,ly,rx,ry])
            if draw:
                cv2.rectangle(
                    drawFrame, 
                    (lx*scale, ly*scale), (rx*scale, ry*scale), 
                    DetectorInterface.__COLORS[kind], DetectorInterface.__WEIGHT[kind]
                    )
        return faceLocation
