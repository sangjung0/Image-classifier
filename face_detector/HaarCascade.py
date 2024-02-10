import cv2
from face_detector.FaceDetector import FaceDetector
from project_constants import FACE, EYE, FACE_MODEL, EYE_MODEL

class HaarCascade(FaceDetector):
    def __init__(self):
        self.faceModel = cv2.CascadeClassifier(FACE_MODEL)
        self.eyeModel = cv2.CascadeClassifier(EYE_MODEL)

    def detect(self, img, color = cv2.COLOR_BGR2GRAY):
        img = cv2.cvtColor(img, color)
        faces = self.faceModel.detectMultiScale(img, 1.3, 5)
        data = []
        for x,y,w,h in faces:
            data.append([FACE, x,y, x+w, y+h])
            face = img[y:y+h, x:x+w]
            eyes = self.eyeModel.detectMultiScale(face)
            for index,(ex, ey, ew, eh) in enumerate(eyes):
                data.append([EYE, x+ex, y+ey, x+ex+ew, y+ey+eh])
                if index == 1: break
        return data