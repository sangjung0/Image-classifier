import cv2
import numpy as np
from face_detector.FaceDetector import FaceDetector
from project_constants import FACE, EYE, FACE_MODEL, EYE_MODEL

class HaarCascade(FaceDetector):
    def __init__(self, color = cv2.COLOR_BGR2GRAY):
        self.__faceModel = cv2.CascadeClassifier(FACE_MODEL)
        self.__eyeModel = cv2.CascadeClassifier(EYE_MODEL)
        self.__color = color

    @property
    def colorConstant(self):
        return self.__color
    
    def detect(self, img):
        faces = self.__faceModel.detectMultiScale(img, 1.3, 5)
        data = []
        for x,y,w,h in faces:
            data.append([FACE, x,y, x+w, y+h])
            face = img[y:y+h, x:x+w]
            eyes = self.__eyeModel.detectMultiScale(face)
            for index,(ex, ey, ew, eh) in enumerate(eyes):
                data.append([EYE, x+ex, y+ey, x+ex+ew, y+ey+eh])
                if index == 1: break
        return data