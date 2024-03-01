from abc import ABC, abstractmethod
import numpy as np

class Interface(ABC):
    @abstractmethod
    def isNewCene(self, img:np.ndarray) -> np.ndarray: pass
    