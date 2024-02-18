from abc import ABC, abstractmethod

class FaceDetector(ABC):

    @abstractmethod
    def detect(self): pass

    @abstractmethod
    def colorConstant(self): pass
