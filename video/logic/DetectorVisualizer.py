import cv2
import numpy as np

from video.model import Section, Face
from video.logic import StopOverPointInterface

from project_constants import DETECTOR_FACE, DETECTOR_NOSE,DETECTOR_RIGHT_MOUTH, DETECTOR_LEFT_EYE, DETECTOR_LEFT_MOUTH, DETECTOR_RIGHT_EYE,  DETECTOR_FRONT_FACE

class DetectorVisualizer(StopOverPointInterface):
    __COLORS = {
        DETECTOR_FRONT_FACE : (0, 255, 255),
        DETECTOR_FACE : (255, 0, 0),
        DETECTOR_NOSE : (0, 255, 0),
        DETECTOR_RIGHT_MOUTH : (0, 0, 255),
        DETECTOR_LEFT_MOUTH : (0, 0, 255),
        DETECTOR_LEFT_EYE : (255,255,0),
        DETECTOR_RIGHT_EYE : (255,255,0)
    }
    __WEIGHT = {
        DETECTOR_FRONT_FACE : 4,
        DETECTOR_FACE : 3,
        DETECTOR_NOSE : 3,
        DETECTOR_RIGHT_MOUTH : 3,
        DETECTOR_LEFT_MOUTH : 3,
        DETECTOR_LEFT_EYE : 3,
        DETECTOR_RIGHT_EYE : 3
    }

    def __init__(self, scale:int):
        self.__scale = scale

    def prepare(self) -> None: 
        return

    def draw(self, locations: list[Face], frame: np.ndarray):
        scale = self.__scale
        for face in locations:
            for key in face.faceData:
                lx, ly, rx, ry = face.faceData[key]
                lx *= scale
                ly *= scale
                rx *= scale
                ry *= scale
                cv2.rectangle(
                    frame, 
                    (lx, ly), (rx, ry), 
                    DetectorVisualizer.__COLORS[key], DetectorVisualizer.__WEIGHT[key]
                    )
    
    def processing(self, section: Section) -> Section:

        for frame in section:
            if len(frame.face) > 0:
                self.draw(frame.face, frame.frame)

        return section


