from abc import ABC, abstractmethod
from multiprocessing import Queue
from typing import Union

from process.compressor import CompressorInterface
from process.serializer import SerializerInterface

class TransceiverInterface(ABC):

    def __init__(self, serializer:SerializerInterface, compressor: CompressorInterface):
        self._compressor = compressor
        self._serializer = serializer

    @abstractmethod
    def send(self, destination: Queue, value: object) -> None: pass

    @abstractmethod
    def receive(self, destination: Queue) -> Union[bool, object]: pass