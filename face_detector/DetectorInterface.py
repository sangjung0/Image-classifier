import cv2
import numpy as np
from abc import ABC, abstractmethod

from project_constants import DETECTOR_FACE, DETECTOR_NOSE, DETECTOR_MOUTH, DETECTOR_EYE, DETECTOR_FRONT_FACE

class DetectorInterface(ABC):
    COLOR = None
    __COLORS = {
        DETECTOR_FRONT_FACE : (0, 255, 255),
        DETECTOR_FACE : (255, 0, 0),
        DETECTOR_NOSE : (0, 255, 0),
        DETECTOR_MOUTH : (0, 0, 255),
        DETECTOR_EYE : (255,255,0)
    }
    __WEIGHT = {
        DETECTOR_FRONT_FACE : 4,
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
    def extract(self, scale:int, draw:bool = False, drawFrames:list = None): pass

    # if draw == True then need drawFrame and scale, drawFrame is original frame 
    def _extract(self, location:list, scale:int, draw:bool, drawFrames:list):
        faceLocations = []
        for idx, lt in enumerate(location):
            faceLocation = []
            for kind, lx, ly, rx, ry in lt:
                lx *= scale
                ly *= scale
                rx *= scale
                ry *= scale
                if kind == DETECTOR_FRONT_FACE:
                    faceLocation.append([lx,ly,rx,ry])
                if draw:
                    cv2.rectangle(
                        drawFrames[idx], 
                        (lx, ly), (rx, ry), 
                        DetectorInterface.__COLORS[kind], DetectorInterface.__WEIGHT[kind]
                        )
            faceLocations.append(faceLocation)
        return faceLocations
