from abc import ABC, abstractmethod

from project_constants import FRAME_SCALE

class TrackerInterface(ABC):
    COLOR = None

    @property
    def colorConstant(self):
        return FRAME_SCALE

    @abstractmethod
    def clear(self): pass
    
    @abstractmethod
    def tracking(self): pass

