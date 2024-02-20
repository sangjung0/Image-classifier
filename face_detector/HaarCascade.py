import cv2
from numpy import ndarray
from face_detector.DetectorInterface import DetectorInterface
from project_constants import DETECTOR_FACE, DETECTOR_EYE, HAARCASCADE_EYE_MODEL, HAARCASCADE_FACE_MODEL

class HaarCascade(DetectorInterface):
    def __init__(self, color = cv2.COLOR_BGR2GRAY):
        super().__init__()
        self.__faceModel = cv2.CascadeClassifier(HAARCASCADE_FACE_MODEL)
        self.__eyeModel = cv2.CascadeClassifier(HAARCASCADE_EYE_MODEL)
        self.__color = color
        self.__batch = []

    @property
    def colorConstant(self):
        return self.__color
    
    def batch(self, img: ndarray) -> None:
        self.__batch.append(img)

    def clear(self):
        self.__batch.clear()
    
    def extract(self, draw:bool = False, drawFrames:list = None, scales:list = None):
        super()._extract(self.detect(), draw, drawFrames, scales)
    
    def detect(self):
        imgs = []
        for img in self.__batch:
            data = []
            faces = self.__faceModel.detectMultiScale(img)
            for x,y,w,h in faces:
                data.append([DETECTOR_FACE, x,y, x+w, y+h])
                face = img[y:y+h, x:x+w]
                eyes = self.__eyeModel.detectMultiScale(face, 1.1, 3)
                for index,(ex, ey, ew, eh) in enumerate(eyes):
                    data.append([DETECTOR_EYE, x+ex, y+ey, x+ex+ew, y+ey+eh])
                    if index == 1: break
            imgs.append(data)
        return imgs