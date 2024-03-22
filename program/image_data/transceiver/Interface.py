from abc import ABC, abstractmethod
from typing import Union

class Interface(ABC):

    @abstractmethod
    def send(self, value: object) -> None: pass

    @abstractmethod
    def receive(self) -> Union[bool, object]: pass