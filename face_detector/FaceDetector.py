from abc import ABC, abstractclassmethod

class FaceDetector(ABC):

    @abstractclassmethod
    def detect(self): pass
