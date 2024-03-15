from abc import ABC, abstractmethod
from typing import Union

from image_data.compressor import CompressorInterface
from image_data.serializer import SerializerInterface

class Interface(ABC):

    def __init__(self, serializer:SerializerInterface, compressor: CompressorInterface):
        self._compressor = compressor
        self._serializer = serializer

    @abstractmethod
    def send(self, destination: object, value: object) -> None: pass

    @abstractmethod
    def receive(self, destination: object) -> Union[bool, object]: pass