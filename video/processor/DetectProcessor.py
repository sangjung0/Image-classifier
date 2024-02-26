from typing import Type
import cv2

from video.model import Section
from face_detector import DetectorInterface
from video.processor.ProcessorInterface import ProcessorInterface
from video.model import Face

from project_constants import DETECTOR_FACE, DETECTOR_NOSE,DETECTOR_RIGHT_MOUTH, DETECTOR_LEFT_EYE, DETECTOR_LEFT_MOUTH, DETECTOR_RIGHT_EYE,  DETECTOR_FRONT_FACE

class DetectProcessor(ProcessorInterface):
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

    def __init__(self, detector: Type[DetectorInterface], scale:int, draw:bool):
        super().__init__("DetectProcessor")
        self.__detector = detector
        self.__draw = draw
        self.__scale = scale

    def __prepare__(self):
        if self.__detector is not None: self.__detector = self.__detector()

    def draw(self, locations: list, frames: list):
        scale = self.__scale
        for lt, frame in zip(locations, frames):
            for face in lt:
                for key in face.keys():
                    lx, ly, rx, ry = face[key]
                    lx *= scale
                    ly *= scale
                    rx *= scale
                    ry *= scale
                    cv2.rectangle(
                        frame.frame, 
                        (lx, ly), (rx, ry), 
                        DetectProcessor.__COLORS[key], DetectProcessor.__WEIGHT[key]
                        )


    def processing(self, section:Section):
        if self.__detector is None: return section

        detector = self.__detector
        draw = self.__draw
        frames = []

        for frame in section.frames:
            if frame.isDetect:
                section.deCompress(frame)
                frames.append(frame)
                detector.batch(frame.getFrame(detector.colorConstant))

        if len(frames) == 0: return section

        faceLocation = detector.detect()
        detector.clear()

        if draw: self.draw(faceLocation, frames)

        for frame, face in zip(frames, faceLocation):
            faces = []
            index = frame.index
            for f in face:
                faces.append(Face(
                    index, 
                    f.get(DETECTOR_FACE, None),
                    f.get(DETECTOR_NOSE, None),
                    f.get(DETECTOR_LEFT_EYE, None),
                    f.get(DETECTOR_RIGHT_EYE, None),
                    f.get(DETECTOR_LEFT_MOUTH, None),
                    f.get(DETECTOR_RIGHT_MOUTH, None)
                ))
            frame.face = faces
            section.compress(frame)

        return section