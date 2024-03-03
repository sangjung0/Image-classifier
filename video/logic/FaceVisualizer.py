import cv2
import numpy as np

from video.logic.StopOverPointInterface import StopOverPointInterface

from video.model import Section, Face

from project_constants import DETECTOR_FACE, DETECTOR_NOSE,DETECTOR_RIGHT_MOUTH, DETECTOR_LEFT_EYE, DETECTOR_LEFT_MOUTH, DETECTOR_RIGHT_EYE,  DETECTOR_FRONT_FACE

class FaceVisualizer(StopOverPointInterface):
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

    def prepare(self) -> None: 
        return

    def draw(self, locations: list[Face], frame: np.ndarray):
        for face in locations:
            for key in face.faceData:
                lx, ly, rx, ry = face.faceData[key]
                cv2.rectangle(
                    frame, 
                    (lx, ly), (rx, ry), 
                    face.rectColor if key == DETECTOR_FACE else FaceVisualizer.__COLORS[key], FaceVisualizer.__WEIGHT[key]
                    )
                if key == DETECTOR_FACE:
                    name = face.name.get()
                    if name:
                        cv2.rectangle(frame, (lx, ly), (lx+30, ly-30), face.rectColor, cv2.FILLED)
                        cv2.putText(frame, name, (lx, ly),  cv2.FONT_HERSHEY_SIMPLEX, 1, tuple((255 - i) for i in face.rectColor), 4)
    
    def processing(self, section: Section) -> Section:

        for frame in section:
            if len(frame.face) > 0:
                self.draw(frame.face, frame.frame)

        return section


