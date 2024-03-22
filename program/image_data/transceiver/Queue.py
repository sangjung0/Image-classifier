from multiprocessing import Queue as Q

from image_data.transceiver.Interface import Interface

from image_data.compressor import CompressorInterface
from image_data.serializer import SerializerInterface
from image_data.model import Section

class Queue(Interface):

    def __init__(self, source:Q, destination:Q, serializer:SerializerInterface, compressor: CompressorInterface):
        self.__source = source
        self.__destination = destination
        self.__compressor = compressor
        self.__serializer = serializer
 
    def send(self,value: Section) -> None:
        self.__destination.put(self.__compressor.compress(self.__serializer.serialization(value)))

    def receive(self) -> Section:
        if self.__source.empty():
            return False, None
        return True, self.__serializer.deSerialization(self.__compressor.decompress(self.__source.get()))