import numpy as np
from abc import ABC, abstractmethod

class DetectorInterface(ABC):
    COLOR = None

    @property
    @abstractmethod
    def colorConstant(self) -> int: pass

    @abstractmethod
    def detect(self, img:np.ndarray) -> list: pass

    @abstractmethod
    def batch(self, img:np.ndarray) -> None: pass

    @abstractmethod
    def clear(self) -> None: pass