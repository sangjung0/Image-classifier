from abc import ABC, abstractmethod
from typing import Iterable

class StopOverPointInterface(ABC):
    @abstractmethod
    def prepare(self) -> None:pass

    @abstractmethod
    def processing(self, source:Iterable) -> Iterable:pass