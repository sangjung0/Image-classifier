from abc import ABC, abstractclassmethod

class FaceDetector(ABC):

    @abstractclassmethod
    def detect(self): pass

    @abstractclassmethod
    def colorConstant(self): pass
