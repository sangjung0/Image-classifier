from abc import ABC, abstractmethod
from typing import Iterable

class StartPointInterface(ABC):
    @abstractmethod
    def prepare(self, setIsFinish:callable) -> None:pass

    @abstractmethod
    def processing(self) -> Iterable:pass