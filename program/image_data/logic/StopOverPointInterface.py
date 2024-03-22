from abc import ABC, abstractmethod

from process.model import Section

class StopOverPointInterface(ABC):
    @abstractmethod
    def prepare(self) -> None:pass

    @abstractmethod
    def processing(self, section:Section) -> Section:pass