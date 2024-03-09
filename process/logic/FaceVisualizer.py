import cv2
import numpy as np

from process.logic.StopOverPointInterface import StopOverPointInterface

from process.model import Section, Face

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
        DETECTOR_FRONT_FACE : 40,
        DETECTOR_FACE : 40,
        DETECTOR_NOSE : 40,
        DETECTOR_RIGHT_MOUTH : 40,
        DETECTOR_LEFT_MOUTH : 40,
        DETECTOR_LEFT_EYE : 40,
        DETECTOR_RIGHT_EYE : 40
    }

    def prepare(self) -> None: 
        return

    def draw(self, locations: list[Face], source: np.ndarray):
        for face in locations:
            for key in face.faceData:
                lx, ly, rx, ry = face.faceData[key]
                cv2.rectangle(
                    source, 
                    (lx, ly), (rx, ry), 
                    face.rectColor if key == DETECTOR_FACE else FaceVisualizer.__COLORS[key], FaceVisualizer.__WEIGHT[key]
                    )
                if key == DETECTOR_FACE:
                    name = face.name
                    if name:
                        cv2.rectangle(source, (lx, ly), (lx+30, ly-30), face.rectColor, cv2.FILLED)
                        cv2.putText(source, name, (lx, ly),  cv2.FONT_HERSHEY_SIMPLEX, 1, tuple((255 - i) for i in face.rectColor), 4)
    
    def processing(self, section: Section) -> Section:

        for img in section:
            if len(img.face) > 0:
                self.draw(img.face, img.source)

        return section


