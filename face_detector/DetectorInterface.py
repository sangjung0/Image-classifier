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

    @abstractmethod
    def batch(self, img:np.ndarray) -> None: pass

    @abstractmethod
    def clear(self) -> None: pass

    @abstractmethod
    def extract(self, draw:bool = False, drawFrames:list = None, scales:list = None): pass

    # if draw == True then need drawFrame and scale, drawFrame is original frame 
    def _extract(self, location:list, draw:bool, drawFrames:list, scales:list):
        faceLocations = []
        for idx, lt in enumerate(location):
            faceLocation = []
            for kind, lx, ly, rx, ry in lt:
                if kind == DETECTOR_FACE:
                    faceLocation.append([lx,ly,rx,ry])
                if draw:
                    cv2.rectangle(
                        drawFrames[idx], 
                        (lx*scales[idx], ly*scales[idx]), (rx*scales[idx], ry*scales[idx]), 
                        DetectorInterface.__COLORS[kind], DetectorInterface.__WEIGHT[kind]
                        )
            faceLocations.append(faceLocation)
        return faceLocations
