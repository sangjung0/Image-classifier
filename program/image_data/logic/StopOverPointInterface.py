from abc import ABC, abstractmethod

from image_data.model import Section

class StopOverPointInterface(ABC):
    @abstractmethod
    def prepare(self) -> None:pass

    @abstractmethod
    def processing(self, section:Section) -> Section:pass