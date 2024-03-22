from abc import ABC, abstractmethod

from process.model import Section

class StartPointInterface(ABC):
    @abstractmethod
    def prepare(self, setIsFinish:callable) -> None:pass

    @abstractmethod
    def processing(self, section:Section) -> Section:pass