from abc import ABC, abstractmethod

class SerializerInterface(ABC):
    @abstractmethod
    def serialization(self, value: object) -> bytes: pass

    @abstractmethod
    def deSerialization(self, value: bytes) -> object: pass