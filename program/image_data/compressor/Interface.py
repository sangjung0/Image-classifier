from abc import ABC, abstractmethod

class Interface(ABC):

    @abstractmethod
    def compress(self, value: bytes) -> bytes: pass
    @abstractmethod
    def decompress(self, value: bytes) -> bytes: pass